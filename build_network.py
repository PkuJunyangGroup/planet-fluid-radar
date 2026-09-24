"""Evidence-backed institution co-occurrence, not inferred personal relationships."""
import hashlib
import itertools
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def identities(raw,aliases):
 text=raw.lower()
 if '@' in raw:return []
 found=[a['name'] for a in aliases if any(k in text for k in a['match'])]
 if found:return found
 if not re.search(r'univ|institut|laborator|observator|academy|cnrs|nasa|school|college|centre|center|研究|大学',text):return []
 cleaned=re.sub(r'(?:organization|addressline|city|state|country|postcode)\s*=\s*','',raw)
 cleaned=re.sub(r'^\W*\d*(?:affiliation:\s*)?','',cleaned)
 return [cleaned.strip()] if cleaned.strip() else []

def build(data=None):
 data=data or json.loads((ROOT/'catalog.json').read_text());aliases=json.loads((ROOT/'institution_aliases.json').read_text());nodes={};edges={};papers={};omitted=0
 for p in data['papers']:
  if p['status']!='candidate':continue
  ids=set()
  for raw in p.get('institutions',[]):
   for label in identities(raw,aliases):
    key=hashlib.sha256(label.encode()).hexdigest()[:16];ids.add(key)
    n=nodes.setdefault(key,{'id':key,'label':label,'papers':set(),'authors':{},'raw':set()});n['papers'].add(p['id']);n['raw'].add(raw)
  if not ids:omitted+=1;continue
  # Names only come from explicit local author-affiliation mappings.
  for a in p.get('author_affiliations',[]):
   name=re.sub(r'\\aff[\d,]+','',a['name']).strip()
   for raw in a.get('institutions',[]):
    for label in identities(raw,aliases):
     key=hashlib.sha256(label.encode()).hexdigest()[:16]
     if key in nodes and key in ids:nodes[key]['authors'].setdefault(name,set()).add(p['id'])
  for pair in itertools.combinations(sorted(ids),2):edges.setdefault(pair,set()).add(p['id'])
  papers[p['id']]={k:p.get(k) for k in ['id','title','url','topics','first_seen','publication_date','journals']}
  papers[p['id']]['institutions']=sorted(ids)
 for n in nodes.values():
  n['papers']=sorted(n['papers']);n['raw']=sorted(n['raw']);n['authors']=[{'name':name,'papers':sorted(p)} for name,p in n['authors'].items()]
 out={'generated_at':data['generated_at'],'nodes':list(nodes.values()),'edges':[{'source':a,'target':b,'papers':sorted(p),'weight':len(p)} for (a,b),p in edges.items()],'papers':papers,'omitted_papers':omitted}
 (ROOT/'network.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(len(nodes),'institutions',len(edges),'links',len(papers),'papers',omitted,'without institutions')
if __name__=='__main__':build()
