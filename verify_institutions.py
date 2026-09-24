"""Manually invoked ROR verification; only unique exact name/alias matches accepted."""
import concurrent.futures,json,time,urllib.request,urllib.parse
from pathlib import Path
from institution_utils import normalize
ROOT=Path(__file__).resolve().parent

def get(name):
 url='https://api.ror.org/v2/organizations?query='+urllib.parse.quote(name)
 for attempt in range(3):
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'PlanetFluidRadar/1.0 (public institution name verification)'})
   with urllib.request.urlopen(req,timeout=25) as r:return json.load(r)['items']
  except Exception:
   if attempt==2:return []
   time.sleep(2)

def verify(item):
 name=item['name'];results=get(name);target=normalize(name)
 found=[r for r in results if r.get('status')=='active' and any(normalize(n['value'])==target for n in r['names'])]
 if len(found)!=1:return name,{'status':'unverified','query':name}
 r=found[0]
 return name,{'status':'verified','name':next(n['value'] for n in r['names'] if 'ror_display' in n['types']),'ror':r['id'],'names':r['names'],'website':next((l['value'] for l in r['links'] if l['type']=='website'),None),'relationships':r['relationships'],'checked_at':time.strftime('%Y-%m-%d'),'source':'https://api.ror.org/v2/organizations/'+r['id'].split('/')[-1]}
if __name__=='__main__':
 aliases=json.loads((ROOT/'institution_aliases.json').read_text());path=ROOT/'institution_registry.json';cache=json.loads(path.read_text()) if path.exists() else {}
 todo=[a for a in aliases if a['name'] not in cache]
 with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
  for i,(name,result) in enumerate(pool.map(verify,todo)):
   cache[name]=result
   if i%20==0:print(i+1,'/',len(todo),flush=True);path.write_text(json.dumps(cache,ensure_ascii=False,indent=2)+'\n')
 path.write_text(json.dumps(cache,ensure_ascii=False,indent=2)+'\n')
 print('Verified',sum(v['status']=='verified' for v in cache.values()),'of',len(cache),flush=True)
