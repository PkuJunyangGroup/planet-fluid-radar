"""Parent institution coauthorship with evidence-backed subdivisions and ORCIDs."""
import hashlib
from functools import lru_cache
import itertools
import json
import re
from pathlib import Path
from institution_utils import parents,subdivisions,orcid_url,normalize,verified_hierarchy,verified_units
ROOT=Path(__file__).resolve().parent

def identities(raw,aliases):return parents(raw,aliases)
def key(label):return hashlib.sha256(normalize(label).encode()).hexdigest()[:16]

def researcher_name(value):
 # Remove explicit author footnotes, but reject address/code fragments.
 if re.match(r'^\s*\d{3,}',value):return ''
 value=re.sub(r'\\(?:newauthor|aff[\d,]+)', '', value)
 value=re.sub(r'^\s*[\d,]+\s+|[\d,*†‡]+$', '', value).strip()
 if len(value)>90 or re.search(r'[\d\\{}@]|\b(?:university|univ|institute|observatory|avenue|street|department|laboratory|cedex)\b',value,re.I):return ''
 if ',' in value or len(value.split())>7 or sum(c.isalpha() for c in value)<2:return ''
 return value

def build(data=None):
 data=data or json.loads((ROOT/'catalog.json').read_text());aliases,unit_registry,evidence=verified_hierarchy(ROOT);nodes={};edges={};papers={};researchers={};omitted=0
 @lru_cache(maxsize=None)
 def resolve(raw):return parents(raw,aliases)
 for p in data['papers']:
  if p['status']!='candidate':continue
  ids=set()
  for raw in p.get('institutions',[]):
   for label in resolve(raw):
    k=key(label);ids.add(k)
    n=nodes.setdefault(k,{'id':k,'label':label,'name_zh':evidence[label].get('name_zh'),'papers':set(),'authors':{},'units':{},'raw':set(),'verification':{field:evidence[label].get(field) for field in ['ror','website','source','checked_at']}});n['papers'].add(p['id']);n['raw'].add(raw)
    for unit in verified_units(raw,label,unit_registry):
     u=n['units'].setdefault(key(unit['name']),{'id':key(unit['name']),'label':unit['name'],'name_zh':unit.get('name_zh'),'source':unit['source'],'papers':set()});u['papers'].add(p['id'])
  if not ids:omitted+=1
  mappings=p.get('author_affiliations',[]) or [{'name':name,'institutions':[]} for name in p.get('authors',[]) if len(name)<100 and not re.search(r'[,\\]',name)]
  for a in mappings:
   name=researcher_name(a['name'])
   if not name:continue
   oid=orcid_url(a.get('orcid'));source=a.get('name_source','')
   # A DOI is a paper identifier, never a person identifier.
   profile=source if source.startswith('https://') and not re.search(r'https://(?:doi.org|orcid.org|pub.orcid.org)/',source) and a.get('name_zh') else None
   affiliations=sorted({label for raw in a.get('institutions',[]) for label in resolve(raw)})
   if profile:identity='profile:'+profile+':'+a['name_zh'];basis='verified_profile'
   elif oid:identity=oid;basis='orcid'
   else:identity='name:'+normalize(name)+':'+('|'.join(affiliations) or p['id']);basis='name_and_institution' if affiliations else 'paper_signature'
   aid=key('researcher:'+identity)
   person=researchers.setdefault(aid,{'id':aid,'name':name,'name_zh':a.get('name_zh'),'name_source':source,'orcid':oid,'identity_basis':basis,'papers':set(),'institutions':set(),'aliases':set()})
   person['papers'].add(p['id']);person['aliases'].add(name)
   if oid and not person['orcid']:person['orcid']=oid
   person['institutions'].update(key(label) for label in affiliations if key(label) in ids)
   for raw in a.get('institutions',[]):
    for label in resolve(raw):
     k=key(label)
     if k not in ids:continue
     # ORCID distinguishes namesakes; no surname or cross-paper fuzzy matching.
     ak=aid
     author=nodes[k]['authors'].setdefault(ak,{'id':aid,'name':name,'name_zh':a.get('name_zh'),'name_source':a.get('name_source'),'orcid':oid,'papers':set(),'unit_papers':{}})
     author['papers'].add(p['id'])
     if oid and not author['orcid']:author['orcid']=oid
     for unit in verified_units(raw,label,unit_registry):author['unit_papers'].setdefault(key(unit['name']),set()).add(p['id'])
  for pair in itertools.combinations(sorted(ids),2):edges.setdefault(pair,set()).add(p['id'])
  papers[p['id']]={k:p.get(k) for k in ['id','title','url','topics','first_seen','publication_date','journals']};papers[p['id']]['institutions']=sorted(ids)
 for n in nodes.values():
  n['papers']=sorted(n['papers']);n['raw']=sorted(n['raw'])
  n['units']=[{**u,'papers':sorted(u['papers'])} for u in n['units'].values()]
  n['authors']=[{**a,'papers':sorted(a['papers']),'unit_papers':{k:sorted(v) for k,v in a['unit_papers'].items()}} for a in n['authors'].values()]
 out={'generated_at':data['generated_at'],'nodes':list(nodes.values()),'edges':[{'source':a,'target':b,'papers':sorted(p),'weight':len(p)} for (a,b),p in edges.items()],'papers':papers,'omitted_papers':omitted,'level':'parent','researchers':[{**a,'papers':sorted(a['papers']),'institutions':sorted(a['institutions']),'aliases':sorted(a['aliases'])} for a in researchers.values()]}
 (ROOT/'network.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(len(nodes),'parent institutions',len(edges),'links',len(papers),'papers',omitted,'without confirmed parent')
 return out
if __name__=='__main__':build()
