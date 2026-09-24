"""Read public names only from ORCIDs explicitly supplied by paper metadata."""
import concurrent.futures
import datetime as dt
import json
import re
import time
import urllib.request
from pathlib import Path
from institution_utils import orcid_url
ROOT=Path(__file__).resolve().parent
HAN=r'[\u3400-\u9fff·・]'

def chinese_name(person):
 name=person.get('name') or {};candidates=[]
 def add(value):
  value=re.sub(r'\s+','',value or '')
  if re.fullmatch(HAN+'{2,10}',value) and not any(x in value for x in ['教授','大学','研究','博士']):candidates.append(value)
 add((name.get('credit-name') or {}).get('value'))
 given=(name.get('given-names') or {}).get('value','');family=(name.get('family-name') or {}).get('value','')
 if re.fullmatch(HAN+'{1,5}',family) and re.fullmatch(HAN+'{1,5}',given):add(family+given)
 for n in (person.get('other-names') or {}).get('other-name',[]):add(n.get('content'))
 unique=list(dict.fromkeys(candidates))
 return unique[0] if len(unique)==1 else None

def fetch_name(url):
 source='https://pub.orcid.org/v3.0/'+url.split('/')[-1]+'/person'
 try:
  time.sleep(.25)
  req=urllib.request.Request(source,headers={'Accept':'application/json','User-Agent':'PlanetFluidRadar/1.0 (public author names)'})
  with urllib.request.urlopen(req,timeout=15) as r:person=json.load(r)
  # Never persist biography, email, address, or unrelated personal fields.
  return url,{'name_zh':chinese_name(person),'status':'checked','source':url,'checked_at':dt.datetime.now(dt.timezone.utc).isoformat()}
 except Exception:
  return url,{'name_zh':None,'status':'unavailable','source':url,'checked_at':dt.datetime.now(dt.timezone.utc).isoformat()}

def update_names(records,limit=60):
 path=ROOT/'author_names.json';cache=json.loads(path.read_text()) if path.exists() else {};now=dt.datetime.now(dt.timezone.utc)
 ids=list(dict.fromkeys(oid for p in records if p.get('status')=='candidate' for a in p.get('author_affiliations',[]) if (oid:=orcid_url(a.get('orcid')))))
 todo=[]
 for oid in ids:
  old=cache.get(oid,{})
  if old and (now-dt.datetime.fromisoformat(old['checked_at'])).days<(7 if old['status']=='unavailable' else 90):continue
  todo.append(oid)
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  for i,(oid,result) in enumerate(pool.map(fetch_name,todo[:limit])):
   if result['status']=='unavailable' and cache.get(oid,{}).get('name_zh'):continue
   cache[oid]=result
   if i%50==0:print('Author name records',i+1,'/',min(len(todo),limit),flush=True);path.write_text(json.dumps(cache,ensure_ascii=False,indent=2)+'\n')
 path.write_text(json.dumps(cache,ensure_ascii=False,indent=2)+'\n')
 print('Names confirmed:',sum(bool(v['name_zh']) for v in cache.values()),'of',len(cache),flush=True)
 return cache
if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser();parser.add_argument('--limit',type=int,default=60);args=parser.parse_args()
 update_names(json.loads((ROOT/'catalog.json').read_text())['papers'],args.limit)

def publisher_name(given,family):
 """Recover bilingual names only from explicit publisher given/family fields."""
 def han(value):return ''.join(re.findall(r'[\u3400-\u9fff]+',value or ''))
 g,f=han(given),han(family)
 if not (1<=len(g)<=5 and 1<=len(f)<=3):return None
 if any(x in g+f for x in ['教授','大学','研究','博士']):return None
 latin=lambda value:re.sub(r'\s+',' ',re.sub(r'[\u3400-\u9fff()（）]+',' ',value or '')).strip()
 en=' '.join(filter(None,[latin(given),latin(family)]))
 return {'name':en or f+g,'name_zh':f+g}
