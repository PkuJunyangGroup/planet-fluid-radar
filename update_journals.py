"""Retrieve publisher-deposited metadata from Crossref; no full-text scraping."""
import datetime as dt
import json
import re
import time
import urllib.parse
import urllib.request
from html import unescape
from pathlib import Path
from update import classify
ROOT=Path(__file__).resolve().parent

def plain(s):return ' '.join(unescape(re.sub('<[^>]+>',' ',s or '')).split())
def date_value(record,key):
 parts=record.get(key,{}).get('date-parts',[[]])[0]
 if not parts:return None
 # Preserve month/year precision; never invent a day.
 return '-'.join(str(n).zfill(4 if i==0 else 2) for i,n in enumerate(parts))
def publication(record):
 values=[date_value(record,k) for k in ['published-online','published-print','published']]
 valid=[v for v in values if v]
 return min(valid) if valid else None

def parse_record(r,journal,stamp):
 doi=r.get('DOI','').lower();title=plain((r.get('title') or [''])[0])
 if not doi or not title:return None
 authors=[];mappings=[];orgs=[]
 for a in r.get('author',[]):
  name=' '.join(filter(None,[a.get('given'),a.get('family')])) or a.get('name','')
  ins=list(dict.fromkeys(plain(o.get('name','')) for o in a.get('affiliation',[]) if o.get('name')))
  if name:authors.append(name);mappings.append({'name':name,'institutions':ins,'orcid':a.get('ORCID')})
  orgs.extend(ins)
 pub=publication(r)
 relation=r.get('relation',{})
 return {'id':'doi:'+doi,'doi':doi,'version_id':'doi:'+doi,'title':title,'abstract':plain(r.get('abstract','')),'authors':authors,'author_affiliations':mappings,'institutions':list(dict.fromkeys(orgs)),'affiliation_status':'verified' if orgs else 'unavailable','affiliation_source':'https://api.crossref.org/works/'+urllib.parse.quote(doi,safe=''),'source':'journal','journal':journal['name'],'journal_id':journal['id'],'source_group':journal['group'],'categories':[],'url':'https://doi.org/'+doi,'published':pub or '', 'publication_date':pub,'publication_date_source':'Crossref publisher metadata','date_kind':'journal','first_seen':stamp,'updated':r.get('indexed',{}).get('date-time',stamp),'metadata_source':'https://api.crossref.org/works/'+urllib.parse.quote(doi,safe=''),'relations':relation,'metadata_limited':not bool(r.get('abstract')),'publication_dates':{k:date_value(r,k) for k in ['published-online','published-print'] if date_value(r,k)}}

def get(url):
 for attempt in range(2):
  try:
   time.sleep(.65 if attempt==0 else 3)
   req=urllib.request.Request(url,headers={'User-Agent':'PlanetFluidResearchRadar/0.3 (https://pkujunyanggroup.github.io/planet-fluid-radar/sources.html)'})
   with urllib.request.urlopen(req,timeout=25) as resp:return json.load(resp)['message']
  except Exception:
   if attempt:raise

def update(days=14,only=None):
 registry=json.loads((ROOT/'journals.json').read_text());config=json.loads((ROOT/'topics.json').read_text());path=ROOT/'journal_records.json';old=json.loads(path.read_text()) if path.exists() else {'papers':[],'sources':{}}
 papers={p['id']:p for p in old['papers']};sources=old['sources'];now=dt.datetime.now(dt.timezone.utc);stamp=now.isoformat();failures=[]
 for j in registry['journals']:
  if not j['enabled'] or (only and j['id'] not in only):continue
  prev=sources.get(j['id'],{});since=(dt.datetime.fromisoformat(prev['last_success'])-dt.timedelta(days=2)).date().isoformat() if prev.get('last_success') else (now-dt.timedelta(days=days)).date().isoformat()
  filters=('from-update-date:' if prev.get('last_success') else 'from-pub-date:')+since+',until-pub-date:'+now.date().isoformat()+',type:journal-article'
  cursor='*';fetched=0;kept=0;incoming=[]
  try:
   while True:
    q=urllib.parse.urlencode({'filter':filters,'rows':100,'cursor':cursor})
    m=get('https://api.crossref.org/journals/'+j['issn']+'/works?'+q);items=m.get('items',[])
    for raw in items:
     p=parse_record(raw,j,stamp)
     if not p:continue
     p.update(classify(p,config))
     # Keep relevant mechanisms and existing records; do not flood the site with unrelated general-journal content.
     if p['topics'] or p['id'] in papers:
      prior=papers.get(p['id'],{});p['first_seen']=prior.get('first_seen',stamp);incoming.append(p);kept+=1
    fetched+=len(items)
    if len(items)<100:break
    if fetched>=1000:raise RuntimeError('Pagination safety limit; retain checkpoint')
    nxt=m.get('next-cursor')
    if not nxt or nxt==cursor:raise RuntimeError('Incomplete pagination')
    cursor=nxt
   for p in incoming:papers[p['id']]={**papers.get(p['id'],{}),**p}
   sources[j['id']]={'name':j['name'],'status':'ok','last_attempt':stamp,'last_success':stamp,'fetched':fetched,'retained':kept,'method':'Crossref publisher metadata','coverage_since':prev.get('coverage_since',since)}
   print(j['name'],fetched,'retrieved',kept,'retained',flush=True)
  except Exception as e:
   sources[j['id']]={**prev,'name':j['name'],'status':'error','last_attempt':stamp,'error':type(e).__name__};failures.append(j['id']);print(j['name'],'FAILED',type(e).__name__,flush=True)
  path.write_text(json.dumps({'generated_at':stamp,'sources':sources,'papers':list(papers.values())},ensure_ascii=False,indent=2)+'\n')
 for p in papers.values():p.update(classify(p,config))
 path.write_text(json.dumps({'generated_at':stamp,'sources':sources,'papers':list(papers.values())},ensure_ascii=False,indent=2)+'\n')
 return bool(failures)
if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--days',type=int,default=14);ap.add_argument('--only',nargs='*');args=ap.parse_args();raise SystemExit(update(args.days,args.only))
