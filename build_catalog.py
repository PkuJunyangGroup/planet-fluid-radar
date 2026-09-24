"""Merge explicitly linked or conservatively matched preprint/journal records."""
import copy
import datetime as dt
import json
import re
import unicodedata
from pathlib import Path
from enrich import apply_notes
from update import classify
ROOT=Path(__file__).resolve().parent

def norm(s):return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower())
def doi_key(s):return re.sub(r'^https?://(?:dx\.)?doi.org/','',s or '',flags=re.I).lower().strip()
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
 if da and db:return 'DOI' if da==db else None
 if a['id'] in relation_arxiv(b) or b['id'] in relation_arxiv(a):return 'publisher relation'
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

def build():
 arxiv=json.loads((ROOT/'papers.json').read_text());jpath=ROOT/'journal_records.json';journal=json.loads(jpath.read_text()) if jpath.exists() else {'papers':[],'sources':{}};notes=json.loads((ROOT/'editorial.json').read_text());registry=json.loads((ROOT/'journals.json').read_text())
 config=json.loads((ROOT/'topics.json').read_text())
 records=arxiv['papers']+journal['papers']
 for p in records:p.update(classify(p,config))
 arxiv['topics']=config['topics']
 papers=merge_records(records,notes)
 sources={**arxiv['sources'],**{'journal:'+k:v for k,v in journal['sources'].items()}}
 d={**arxiv,'generated_at':dt.datetime.now(dt.timezone.utc).isoformat(),'papers':papers,'sources':sources,'journals':registry,'record_count':len(arxiv['papers'])+len(journal['papers']),'merged_count':sum(len(p['variants'])-1 for p in papers)}
 (ROOT/'catalog.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 print(len(papers),'catalog items;',d['merged_count'],'duplicates linked')
 return d
if __name__=='__main__':build()
