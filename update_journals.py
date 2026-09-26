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
from author_names import publisher_name
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
  if name:
   author={'name':name,'institutions':ins,'orcid':a.get('ORCID')}
   bilingual=publisher_name(a.get('given',''),a.get('family',''))
   if bilingual:author.update(bilingual,name_source='https://doi.org/'+doi)
   authors.append(author['name']);mappings.append(author)
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

def publisher_abstract(p, prior, stamp):
 # Reuse verified publisher metadata when Crossref still omits the abstract.
 if p['abstract'] or not p['journal'].startswith('Nature'):return p
 if prior.get('title')==p['title'] and prior.get('publisher_abstract'):
  p.update(abstract=prior['publisher_abstract'],publisher_abstract=prior['publisher_abstract'],abstract_source=prior['abstract_source'],metadata_limited=False)
  return p
 checked=prior.get('publisher_checked_at')
 if checked and (dt.datetime.fromisoformat(stamp)-dt.datetime.fromisoformat(checked)).days<7:return p
 suffix=p['doi'].split('/')[-1]
 if not re.fullmatch(r's[0-9]+-[0-9]+-[0-9]+-[a-z0-9]+',suffix):return p
 url='https://www.nature.com/articles/'+suffix
 try:
  time.sleep(.8)
  req=urllib.request.Request(url,headers={'User-Agent':'PlanetFluidResearchRadar/0.3 (public abstract metadata)'})
  with urllib.request.urlopen(req,timeout=18) as response:html=response.read(3000000).decode('utf-8','replace')
  hit=re.search(r'id="Abs1-content"[^>]*>(.*?)</div>',html,re.S)
  abstract=plain(hit[1]) if hit else ''
  if abstract:p.update(abstract=abstract,publisher_abstract=abstract,abstract_source=url,metadata_limited=False)
 except Exception:pass
 p['publisher_checked_at']=stamp
 return p

def update_filters(now, previous, days=1, backfill=False):
 today=now.date().isoformat()
 publication_since=(now-dt.timedelta(days=days if backfill else 0)).date().isoformat()
 filters=['from-pub-date:'+publication_since+',until-pub-date:'+today+',type:journal-article']
 if previous.get('last_success') and not backfill:
  updated_since=dt.datetime.fromisoformat(previous['last_success']).date().isoformat()
  filters.append('from-update-date:'+updated_since+',until-update-date:'+today+',type:journal-article')
 return filters

def update(days=1,only=None,backfill=False):
 registry=json.loads((ROOT/'journals.json').read_text());config=json.loads((ROOT/'topics.json').read_text());path=ROOT/'journal_records.json';old=json.loads(path.read_text()) if path.exists() else {'papers':[],'sources':{}}
 papers={p['id']:p for p in old['papers']};sources=old['sources'];now=dt.datetime.now(dt.timezone.utc);stamp=now.isoformat();failures=[]
 for j in registry['journals']:
  if not j['enabled'] or (only and j['id'] not in only):continue
  prev=sources.get(j['id'],{});filters=update_filters(now,prev,days,backfill)
  since=(now-dt.timedelta(days=days if backfill else 0)).date().isoformat()
  fetched=0;kept=0;incoming=[];seen=set()
  cache=old.setdefault('publisher_cache',{})
  try:
   for selection in filters:
    cursor='*';page_count=0
    while True:
     q=urllib.parse.urlencode({'filter':selection,'rows':100,'cursor':cursor})
     m=get('https://api.crossref.org/journals/'+j['issn']+'/works?'+q);items=m.get('items',[])
     for raw in items:
      p=parse_record(raw,j,stamp)
      if not p or p['id'] in seen:continue
      seen.add(p['id']);fetched+=1
      prior=papers.get(p['id'],cache.get(p['id'],{}));p=publisher_abstract(p,prior,stamp)
      if p.get('publisher_checked_at') or p.get('publisher_abstract'):
       cache[p['id']]={k:p[k] for k in ['title','publisher_checked_at','publisher_abstract','abstract_source'] if k in p}
      p.update(classify(p,config))
      if p['topics'] or p['id'] in papers:
       p['first_seen']=papers.get(p['id'],{}).get('first_seen',stamp);incoming.append(p);kept+=1
     page_count+=len(items)
     if len(items)<100:break
     if page_count>=5000:raise RuntimeError('Pagination safety limit; retain checkpoint')
     nxt=m.get('next-cursor')
     if not nxt or nxt==cursor:raise RuntimeError('Incomplete pagination')
     cursor=nxt
   for p in incoming:papers[p['id']]={**papers.get(p['id'],{}),**p}
   sources[j['id']]={'name':j['name'],'status':'ok','last_attempt':stamp,'last_success':stamp,'fetched':fetched,'retained':kept,'method':'Crossref publisher metadata','coverage_since':min(prev.get('coverage_since',since),since)}
   print(j['name'],fetched,'retrieved',kept,'retained',flush=True)
  except Exception as e:
   sources[j['id']]={**prev,'name':j['name'],'status':'error','last_attempt':stamp,'error':type(e).__name__};failures.append(j['id']);print(j['name'],'FAILED',type(e).__name__,flush=True)
  path.write_text(json.dumps({**old,'generated_at':stamp,'sources':sources,'papers':list(papers.values())},ensure_ascii=False,indent=2)+'\n')
 for p in papers.values():p.update(classify(p,config))
 path.write_text(json.dumps({**old,'generated_at':stamp,'sources':sources,'papers':list(papers.values())},ensure_ascii=False,indent=2)+'\n')
 return bool(failures)
def month_windows(today, count=6):
 end=today.replace(day=1); result=[]
 for _ in range(count):
  start=end; following=(start.replace(day=28)+dt.timedelta(days=4)).replace(day=1)
  result.append((start.isoformat()[:7],start,min(today,following-dt.timedelta(days=1))))
  end=(start-dt.timedelta(days=1)).replace(day=1)
 return list(reversed(result))

def update_monthly():
 """Public Crossref journal-article registration counts, not selected-paper counts."""
 path=ROOT/'journal_records.json';d=json.loads(path.read_text()); registry=json.loads((ROOT/'journals.json').read_text())
 now=dt.datetime.now(dt.timezone.utc); stamp=now.isoformat(); windows=month_windows(now.date()); stats=d.setdefault('monthly_statistics',{})
 for j in registry['journals']:
  if not j.get('enabled',True):continue
  series=stats.setdefault(j['id'],{})
  for month,start,end in windows:
   prior=series.get(month,{})
   age=(now-dt.datetime.fromisoformat(prior['checked_at'])).total_seconds()/86400 if prior.get('checked_at') else 999
   # Refresh current/previous month daily; older counts monthly for late deposits.
   if prior.get('status')=='ok' and age < (1 if month>=windows[-2][0] else 28):continue
   q=urllib.parse.urlencode({'filter':f'from-pub-date:{start},until-pub-date:{end},type:journal-article','rows':0})
   url='https://api.crossref.org/journals/'+j['issn']+'/works?'+q
   try:
    m=get(url);series[month]={'count':m['total-results'],'status':'ok','checked_at':stamp,'through':end.isoformat(),'source_url':url}
   except Exception as e:
    series[month]={**prior,'status':'error','last_attempt':stamp,'error':type(e).__name__,'source_url':url}
   path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
  print('Monthly counts',j['name'],flush=True)
 return stats

if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--days',type=int,default=14);ap.add_argument('--only',nargs='*');ap.add_argument('--backfill',action='store_true');args=ap.parse_args();failed=update(args.days,args.only,args.backfill);update_monthly();raise SystemExit(failed)
