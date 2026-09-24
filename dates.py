"""Verify arXiv first submission dates; RSS dates are announcement dates only."""
import datetime as dt
import json
import re
import time
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parent
class Metadata(HTMLParser):
 def __init__(self):super().__init__();self.date=None;self.doi=None
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='meta' and a.get('name')=='citation_doi':self.doi=a.get('content')
  if tag=='meta' and a.get('name')=='citation_date':
   try:self.date=dt.datetime.strptime(a['content'],'%Y/%m/%d').date().isoformat()
   except (ValueError,KeyError):pass

def apply_dates(p, entry):
 p.pop('version_date',None)
 if entry and entry.get('published'):
  p['publication_date']=entry['published'];p['publication_date_source']=entry['source']
 elif p.get('date_kind')!='announcement':
  p['publication_date']=p.get('published');p['publication_date_source']='arXiv API'
 if entry and entry.get('version_date'):p['version_date']=entry['version_date']
 if entry and entry.get('doi'):p['doi']=entry['doi']

def run(offline=False,limit=60):
 path=ROOT/'papers.json';data=json.loads(path.read_text());cp=ROOT/'dates.json';cache=json.loads(cp.read_text()) if cp.exists() else {};count=0
 for p in data['papers']:
  key=p['version_id'];entry=cache.get(key)
  if not offline and not entry and count<limit:
   count+=1
   try:
    time.sleep(3.1)
    url='https://arxiv.org/abs/'+key
    req=urllib.request.Request(url,headers={'User-Agent':'PlanetFluidLiteratureRadar/0.2'})
    with urllib.request.urlopen(req,timeout=15) as r:html=r.read(4_000_000).decode('utf-8','replace')
    meta=Metadata();meta.feed(html)
    entry={'published':meta.date,'source':url,'doi':meta.doi}
    version=re.search(r'v(\d+)$',key).group(1)
    hit=re.search(r'\[v'+version+r'\]</(?:strong|a)>\s*([A-Za-z]{3}, \d{1,2} [A-Za-z]{3} \d{4} \d{2}:\d{2}:\d{2} UTC)',html)
    if hit:entry['version_date']=dt.datetime.strptime(hit[1],'%a, %d %b %Y %H:%M:%S UTC').replace(tzinfo=dt.timezone.utc).isoformat()
    if meta.date:cache[key]=entry;cp.write_text(json.dumps(cache,ensure_ascii=False,indent=2)+'\n')
    print(key,meta.date,flush=True)
   except Exception as e:print(key,type(e).__name__,flush=True)
  apply_dates(p,entry)
 path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--offline',action='store_true');ap.add_argument('--limit',type=int,default=60);args=ap.parse_args();run(args.offline,args.limit)
