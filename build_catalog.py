"""Merge explicitly linked or conservatively matched preprint/journal records."""
import copy
import datetime as dt
import json
import re
import unicodedata
from pathlib import Path
from enrich import apply_notes
from update import classify
from institution_utils import orcid_url,verified_hierarchy,parents,normalize
from functools import lru_cache
ROOT=Path(__file__).resolve().parent

def norm(s):return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower())
def doi_key(s):return re.sub(r'^https?://(?:dx\.)?doi.org/','',s or '',flags=re.I).lower().strip()
def author_override_matches(item, author, paper, parent_names):
 """Require exact name and an explicit identity scope; never match a name alone."""
 if normalize(author.get('name','')) not in [normalize(n) for n in item.get('names',[])]:return False
 oid=orcid_url(author.get('orcid'))
 if item.get('orcid'):
  return bool(oid and oid==orcid_url(item['orcid']))
 if item.get('paper_ids'):
  paper_ids={paper.get('id')} | {v.get('id') for v in paper.get('variants',[])}
  return bool(paper_ids.intersection(item['paper_ids']))
 institution=item.get('institution')
 return bool(institution and any(institution in parent_names(raw) for raw in author.get('institutions',[])))

def author_keys(p):return {norm(a.split(',')[0].split()[-1]) for a in p.get('authors',[]) if a.split()}
def relation_arxiv(p):
 result=set()
 for rel in p.get('relations',{}).values():
  for r in rel:
   ident=r.get('id','')
   hit=re.search(r'(?:arxiv[.:/]|arxiv.org/abs/)(\d{4}\.\d{4,5})(?:v\d+)?',ident,re.I)
   if hit:result.add(hit[1])
 return result

def match(a,b):
 da,db=doi_key(a.get('doi')),doi_key(b.get('doi'))
 if da and db and da==db:return 'DOI'
 if a['id'] in relation_arxiv(b) or b['id'] in relation_arxiv(a):return 'publisher relation'
 if da and db and da!=db:return None
 ta,tb=norm(a['title']),norm(b['title'])
 # Exact substantial title plus a shared author surname; no fuzzy title merging.
 if len(ta)>=40 and ta==tb and author_keys(a)&author_keys(b):return 'exact title + author'
 return None

def merge_records(records,notes):
 groups=[]
 for p in records:
  found=None;reason=None
  for g in groups:
   for q in g['records']:
    reason=match(p,q)
    if reason:found=g;break
   if found:break
  if found:found['records'].append(p);found['match_basis'].append(reason)
  else:groups.append({'records':[p],'match_basis':[]})
 output=[]
 for g in groups:
  rows=g['records'];primary=next((p for p in rows if p['source']=='arXiv'),rows[0]);p=copy.deepcopy(primary)
  apply_notes(p,notes)
  p['first_seen']=min(r['first_seen'] for r in rows)
  p['topics']=list(dict.fromkeys(t for r in rows for t in r.get('topics',[])))
  p['fit_score']=max((r.get('fit_score',0) for r in rows),default=0)
  p['fit_matches']=list(dict.fromkeys(t for r in rows for t in r.get('fit_matches',[])))
  p['tags']=list(dict.fromkeys(t for r in rows for t in r.get('tags',[])))
  p['institutions']=list(dict.fromkeys(t for r in rows for t in r.get('institutions',[])))
  p['author_affiliations']=list({json.dumps(a,sort_keys=True):a for r in rows for a in r.get('author_affiliations',[])}.values())
  p['variants']=[{k:r.get(k) for k in ['id','source','journal','journal_id','title','url','doi','version_id','first_seen','publication_date','version_date','metadata_source','affiliation_source']} for r in rows]
  p['match_basis']=g['match_basis'];p['source_types']=list(dict.fromkeys(r['source'] for r in rows))
  p['journals']=list(dict.fromkeys(r['journal'] for r in rows if r.get('journal')))
  p['source_groups']=list(dict.fromkeys(r['source_group'] for r in rows if r.get('source_group')))
  p['status']='candidate' if any(r['status']=='candidate' for r in rows) else primary['status']
  output.append(p)
 return output

def apply_publisher_supplements(records, supplements):
 """Apply verified DOI-keyed publisher abstracts across all source archives."""
 for p in records:
  doi=doi_key(p.get('doi'))
  supplement=supplements.get(doi) if doi else None
  if not supplement or not supplement.get('abstract'):
   continue
  p['abstract']=supplement['abstract']
  p['abstract_source']=supplement.get('source_url','')
  p['abstract_source_type']=supplement.get('source_type','publisher_abstract')
  p['metadata_limited']=False
 return records

def daily_brief(papers,sources,registry,now):
 """A factual cloud-built digest; never imply that rules read an abstract."""
 zone=dt.timezone(dt.timedelta(hours=8));today=now.astimezone(zone).date()
 def day(value):
  value=str(value or '')
  if re.fullmatch(r'\d{4}-\d{2}-\d{2}',value):return value
  if 'T' in value:
   try:return dt.datetime.fromisoformat(value.replace('Z','+00:00')).astimezone(zone).date().isoformat()
   except ValueError:pass
  return None
 new=[p for p in papers if day(p.get('first_seen'))==str(today)]
 recent=lambda p:any(str(today-dt.timedelta(days=n)) in [day(p.get('publication_date')),day(p.get('version_date'))] for n in [0,1])
 disabled={'journal:'+j['id'] for j in registry['journals'] if j.get('enabled') is False}
 return {'date':str(today),'built_at':now.isoformat(),'review_basis':'Automated rule screening; reading review is recorded separately.',
  'new_count':len(new),'recent_ids':[p['id'] for p in new if recent(p)],
  'older_ids':[p['id'] for p in new if not recent(p)],
  'updated_ids':[p['id'] for p in papers if p not in new and day(p.get('version_date'))==str(today) and p.get('source')=='arXiv' and not str(p.get('version_id','')).endswith('v1')],
  'source_issues':[{'name':k,'status':v.get('status','unknown')} for k,v in sources.items() if k not in disabled and v.get('status')!='ok']}

def build():
 arxiv=json.loads((ROOT/'papers.json').read_text());jpath=ROOT/'journal_records.json';journal=json.loads(jpath.read_text()) if jpath.exists() else {'papers':[],'sources':{}};epath=ROOT/'exoplanet_records.json';exoplanet=json.loads(epath.read_text()) if epath.exists() else {'papers':[],'sources':{}};notes=json.loads((ROOT/'editorial.json').read_text());registry=json.loads((ROOT/'journals.json').read_text())
 config=json.loads((ROOT/'topics.json').read_text())
 records=arxiv['papers']+journal['papers']+exoplanet['papers']
 supplement_path=ROOT/'exoplanet_metadata_overrides.json'
 supplements=json.loads(supplement_path.read_text()) if supplement_path.exists() else {}
 apply_publisher_supplements(records,supplements)
 for p in records:p.update(classify(p,config))
 arxiv['topics']=config['topics']
 papers=merge_records(records,notes)
 # Keep provenance in source archives; publish and graph only the narrow,
 # in-scope candidate set. The filter is reversible by changing topics.json.
 papers=[p for p in papers if p.get('status')=='candidate']
 intake_path=ROOT/'intake.json'
 intake=json.loads(intake_path.read_text()) if intake_path.exists() else None
 if intake is not None:
  previous_path=ROOT/'catalog.json'
  previous=json.loads(previous_path.read_text()).get('papers',[]) if previous_path.exists() else []
  approved=set(intake.get('approved',[]))
  kinds=intake.get('kinds',{})
  def admitted(p):
   ids={p['id']}|{v['id'] for v in p.get('variants',[])}
   return bool(ids&approved) or any(p['id']==old['id'] or match(p,old) for old in previous)
  papers=[p for p in papers if admitted(p)]
  for p in papers:
   p['intake_kind']=next((kinds[v] for v in [p['id']]+[v['id'] for v in p.get('variants',[])] if v in kinds),None)
 # Keep broad atmospheric/ocean/climate/method topic codes for transparent
 # scoring, but show only planetary-domain categories as public tags. The
 # mechanism vocabulary remains data-driven and can grow with the corpus.
 display_ids=set(config.get('scope_exclusion_rules',{}).get('public_topic_ids',[]))
 for p in papers:
  p['topics']=[topic for topic in p.get('topics',[]) if topic in display_ids]
  # Keep historical editorial notes in the source archive, but publish only
  # the original abstract. The reading list no longer offers AI summaries.
  for key in list(p):
   if key.startswith('intro_'):p.pop(key)
 names_path=ROOT/'author_names.json';names=json.loads(names_path.read_text()) if names_path.exists() else {}
 overrides_path=ROOT/'author_name_overrides.json';overrides=json.loads(overrides_path.read_text()) if overrides_path.exists() else []
 aliases,_,_=verified_hierarchy(ROOT)
 @lru_cache(maxsize=None)
 def parent_names(raw):return parents(raw,aliases)
 for p in papers:
  # A verified paper-scoped name can be displayed even if no affiliation was
  # supplied. This scaffold adds neither an institution nor an ORCID.
  known={normalize(a.get('name','')) for a in p.get('author_affiliations',[])}
  for byline in p.get('authors',[]):
   if normalize(byline) in known:continue
   candidate={'name':byline,'institutions':[],'orcid':None}
   if any(author_override_matches(item,candidate,p,parent_names) for item in overrides):
    p.setdefault('author_affiliations',[]).append(candidate);known.add(normalize(byline))
  for a in p.get('author_affiliations',[]):
   a['orcid']=orcid_url(a.get('orcid'))
   confirmed=names.get(a['orcid'],{})
   if not a.get('name_zh') and confirmed.get('name_zh'):a.update(name_zh=confirmed['name_zh'],name_source=confirmed['source'])
   for item in overrides:
    if author_override_matches(item,a,p,parent_names):
     a.update(name_zh=item['name_zh'],name_source=item['source'])
 sources={**arxiv['sources'],**{'journal:'+k:v for k,v in journal['sources'].items()},**exoplanet.get('sources',{})}
 d={**arxiv,'generated_at':dt.datetime.now(dt.timezone.utc).isoformat(),'papers':papers,'intake':intake,'topic_filter_ids':[t['id'] for t in config['topics'] if t['id'] in display_ids],'sources':sources,'journals':registry,'monthly_statistics':journal.get('monthly_statistics',{}),'record_count':len(arxiv['papers'])+len(journal['papers'])+len(exoplanet['papers']),'merged_count':sum(len(p['variants'])-1 for p in papers)}
 d['daily_brief']=daily_brief(papers,sources,registry,dt.datetime.now(dt.timezone.utc))
 (ROOT/'catalog.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 print(len(papers),'catalog items;',d['merged_count'],'duplicates linked')
 return d
if __name__=='__main__':build()
