"""Fetch public arXiv metadata; deterministic, explicitly non-AI classification."""
import argparse
import datetime as dt
import json
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NS = {'a': 'http://www.w3.org/2005/Atom', 'o': 'http://a9.com/-/spec/opensearch/1.1/'}

def normalize(s):
    return re.sub(r'[^\w.]+', ' ', s.lower()).strip()

def contains(text, term):
    # Word boundaries plus common plural endings; avoid nonvolatile -> volatile.
    word = normalize(term)
    return bool(re.search(r'(?<!\w)'+re.escape(word)+r'(?:s|es|ies)?(?!\w)', text))

def classify(paper, config):
    text = normalize(paper['title']+' '+paper['abstract'])
    matches = {}
    for t in config['topics']:
        terms=[w for w in t['terms'] if contains(text,w)]
        if terms and (not t.get('context') or any(contains(text,w) for w in t['context'])):
            matches[t['id']]=terms
    excluded=[w for w in config['exclude_terms'] if contains(text,w)]
    direct='astro-ph.EP' in paper['categories']
    status='candidate' if any(k!='methods' for k in matches) else 'unmatched'
    if excluded: status='excluded'
    reason='关联线索：'+'、'.join(list(dict.fromkeys(w for terms in matches.values() for w in terms))[:6]) if matches else ('行星科学拓展阅读' if direct else '拓展阅读')
    if excluded: reason='当前研究范围外的候选，供管理员复核'
    override=config.get('overrides',{}).get(paper['id'])
    if override: status,reason=override['status'],override['reason']
    tags=[m['label'] for m in config.get('mechanisms',[]) if any(contains(text,w) for w in m['terms'])]
    return {'topics':list(matches),'matches':matches,'status':status,'reason':reason,'tags':tags[:5],'method':'manual' if override else 'keyword'}

def parse_feed(data):
    root = ET.fromstring(data)
    total = int(root.findtext('o:totalResults', '0', NS))
    items = []
    for e in root.findall('a:entry', NS):
        url = e.findtext('a:id', '', NS)
        if '/abs/' not in url:
            raise ValueError('arXiv returned an error entry')
        full_id = url.split('/abs/')[-1]
        base = re.sub(r'v\d+$', '', full_id)
        clean = lambda name: ' '.join(e.findtext('a:'+name, '', NS).split())
        items.append({'id': base, 'version_id': full_id, 'title': clean('title'), 'abstract': clean('summary'),
            'published': clean('published'), 'updated': clean('updated'),
            'authors': [a.findtext('a:name', '', NS) for a in e.findall('a:author', NS)],
            'doi':e.findtext('{http://arxiv.org/schemas/atom}doi','').strip(),
            'categories': [c.attrib['term'] for c in e.findall('a:category', NS)],
            'url': 'https://arxiv.org/abs/'+base, 'pdf': 'https://arxiv.org/pdf/'+full_id, 'source':'arXiv'})
    return total, items

def request_feed(query, start, size):
    url = 'https://export.arxiv.org/api/query?' + urllib.parse.urlencode({'search_query':query,'start':start,'max_results':size,'sortBy':'lastUpdatedDate','sortOrder':'descending'})
    for attempt in range(3):
        time.sleep(3.1 if attempt == 0 else 5 * 2**attempt)
        try:
            req = urllib.request.Request(url, headers={'User-Agent':'PlanetFluidLiteratureRadar/0.1'})
            with urllib.request.urlopen(req, timeout=45) as r:
                return parse_feed(r.read())
        except Exception:
            if attempt == 2:
                raise

def rss_feed(category):
    req = urllib.request.Request('https://rss.arxiv.org/atom/'+category, headers={'User-Agent':'PlanetFluidLiteratureRadar/0.1'})
    time.sleep(3.1)
    with urllib.request.urlopen(req, timeout=30) as r:
        return parse_rss(r.read())

def parse_rss(data):
    root = ET.fromstring(data)
    result = []
    for e in root.findall('a:entry', NS):
        identity = e.findtext('a:id', '', NS).split(':')[-1]
        if not re.fullmatch(r'(?:[a-z.-]+/)?[0-9.]+v[0-9]+', identity):
            continue
        base = re.sub(r'v\d+$', '', identity)
        clean = lambda name: ' '.join(e.findtext('a:'+name, '', NS).split())
        summary = clean('summary')
        announcement = e.findtext('{http://arxiv.org/schemas/atom}announce_type','')
        result.append({'id':base,'version_id':identity,'title':clean('title'),
            'abstract':summary.split('Abstract:',1)[-1].strip(),
            'authors':[e.findtext('{http://purl.org/dc/elements/1.1/}creator','')],
            'categories':[c.attrib['term'] for c in e.findall('a:category',NS)],
            'published':clean('published'),'updated':clean('updated'),'date_kind':'announcement',
            'announcement_type':announcement,'url':'https://arxiv.org/abs/'+base,
            'pdf':'https://arxiv.org/pdf/'+identity,'source':'arXiv'})
    return result

def update(days=7):
    config = json.loads((ROOT/'topics.json').read_text())
    path = ROOT/'papers.json'
    old = json.loads(path.read_text()) if path.exists() else {'papers':[], 'sources':{}}
    papers = {p['id']:p for p in old['papers']}
    sources = old.get('sources', {})
    now = dt.datetime.now(dt.timezone.utc)
    stamp = now.isoformat()
    failures = []
    for category in config['categories']:
        previous = sources.get(category, {})
        since = dt.datetime.fromisoformat(previous['last_success']) - dt.timedelta(days=2) if previous.get('last_success') else now-dt.timedelta(days=days)
        query = 'cat:'+category
        incoming = []
        try:
            start = 0
            while True:
                total, batch = request_feed(query, start, 100)
                if total and not batch and start < total:
                    raise ValueError('Incomplete pagination')
                for p in batch:
                    if dt.datetime.fromisoformat(p['updated'].replace('Z','+00:00')) >= since:
                        incoming.append(p)
                if not batch or start+len(batch)>=total or any(dt.datetime.fromisoformat(p['updated'].replace('Z','+00:00')) < since for p in batch):
                    break
                start += len(batch)
                if start >= 10000:
                    raise ValueError('Catch-up exceeds safety limit; checkpoint retained')
            for p in incoming:
                prior = papers.get(p['id'], {})
                p['first_seen'] = prior.get('first_seen', stamp)
                p['version_changed'] = prior.get('version_changed', False) or bool(prior and prior['version_id'] != p['version_id'])
                papers[p['id']] = {**prior, **p}
            sources[category] = {'last_attempt':stamp,'last_success':stamp,'status':'ok','fetched':len(incoming)}
            print(category, len(incoming), 'records')
        except Exception as e:
            sources[category] = {**previous,'last_attempt':stamp,'status':'error','error':type(e).__name__}
            try:
                for p in rss_feed(category):
                    prior = papers.get(p['id'], {})
                    p['first_seen'] = prior.get('first_seen', stamp)
                    p['version_changed'] = p.get('announcement_type') == 'replace' or bool(prior and prior['version_id'] != p['version_id'])
                    if prior and prior.get('date_kind') != 'announcement':
                        p['published'] = prior['published']
                        p['date_kind'] = 'published'
                    papers[p['id']] = {**prior, **p}
                sources[category].update(status='partial',last_rss_success=stamp)
            except Exception:
                pass
            failures.append(category)
            print(category, 'failed:', type(e).__name__)
    for p in papers.values():
        p.update(classify(p,config))
    output = {'generated_at':stamp,'ai_enabled':False,'sources':sources,'topics':config['topics'],
              'repository':config.get('repository',''),'papers':sorted(papers.values(),key=lambda p:p['published'],reverse=True)}
    path.parent.mkdir(parents=True,exist_ok=True)
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    temp.replace(path)
    return bool(failures)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--days',type=int,default=7)
    args = parser.parse_args()
    raise SystemExit(1 if update(args.days) else 0)
