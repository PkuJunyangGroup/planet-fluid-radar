"""Fetch public arXiv metadata; deterministic, explicitly non-AI classification."""
import argparse
import datetime as dt
import json
import re
import time
import urllib.parse
import urllib.request
import urllib.error
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

def planetary_context(paper, config):
    # arXiv's Earth and Planetary Astrophysics category is an explicit planetary
    # scope signal, although topical matching below is still required.
    if 'astro-ph.EP' in paper.get('categories', []):
        return True
    rules=config.get('scope_exclusion_rules',{})
    for term in rules.get('planetary_context',[]):
        if is_focus_term(paper,term):return True
    return False

def teacher_author(paper, config):
    names={normalize(n) for n in config.get('scope_exclusion_rules',{}).get('excluded_teacher_authors',[])}
    for author in paper.get('authors',[]):
        raw=author.strip()
        candidates={normalize(raw)}
        if ',' in raw:
            parts=[x.strip() for x in raw.split(',',1)]
            candidates.add(normalize(' '.join(parts[::-1])))
        if candidates & names:return True
    return False

def is_focus_term(paper, term):
    if normalize(term)=='mars':
        raw_title=paper.get('title','')
        raw_abstract=paper.get('abstract','')
        if re.search(r'(?<!\w)Mars(?!\w)',raw_title):return True
        return len(re.findall(r'(?<!\w)Mars(?!\w)',raw_abstract))>=2
    title=normalize(paper.get('title',''))
    abstract=normalize(paper.get('abstract',''))
    if contains(title,term):return True
    word=normalize(term)
    return len(re.findall(r'(?<!\w)'+re.escape(word)+r'(?:s|es|ies)?(?!\w)',abstract))>=2

def relevance(text, topic_ids, config):
    weights=config.get('relevance_scoring',{}).get('topic_weights',{})
    ranked=sorted((weights.get(topic,0) for topic in topic_ids),reverse=True)
    topic_score=(ranked[0] if ranked else 0)+min(18,sum(ranked[1:])*.35)
    themes=[t for t in config.get('relevance_scoring',{}).get('themes',[]) if any(contains(text,w) for w in t['terms'])]
    signal_score=min(24,sum(t['weight'] for t in themes)) if topic_ids else 0
    score=min(100,round(20+topic_score+signal_score)) if topic_ids else 0
    return score,[t['label'] for t in themes]

def priority_journal(paper, rules):
    name=normalize(paper.get('journal',''))
    prefixes=[normalize(x) for x in rules.get('priority_journal_prefixes',[]) ]
    exact=[normalize(x) for x in rules.get('priority_journal_names',[]) ]
    venue=any(name.startswith(prefix) for prefix in prefixes if prefix) or any(x in name for x in exact)
    if not venue:return False
    # A prestigious venue is not enough by itself: the exception is only for
    # work with a clear planetary/exoplanet signal, not unrelated ecology or
    # broad Earth climate/ocean papers that happen to match generic keywords.
    return any(is_focus_term(paper,term) for term in rules.get('priority_exception_terms',[]))

def classify(paper, config):
    text = normalize(paper['title']+' '+paper['abstract'])
    matches = {}
    for t in config['topics']:
        if any(not any(contains(text,w) for w in group) for group in t.get('required_context_groups',[])):continue
        terms=[w for w in t['terms'] if contains(text,w) and (w not in t.get('term_context',{}) or any(contains(text,x) for x in t['term_context'][w]))]
        if any(contains(text,w) for w in t.get('reject_context',[])) and not any(contains(text,w) for w in t.get('allow_context',[])):continue
        if terms and (not t.get('context') or any(contains(text,w) for w in t['context'])):
            matches[t['id']]=terms
    rules=config.get('scope_exclusion_rules',{})
    planetary=planetary_context(paper,config)
    excluded=[w for w in config['exclude_terms'] if contains(text,w)]
    # CMIP papers are Earth-system projections; the other field and regional
    # exclusions apply only without an explicit planetary target.
    excluded += [w for w in rules.get('hard_earth_scope_terms',[]) if is_focus_term(paper,w) and (w in {'cmip','cmip5','cmip6'} or not planetary)]
    excluded += [w for w in rules.get('earth_only_scope_terms',[]) if is_focus_term(paper,w) and not planetary]
    excluded= list(dict.fromkeys(excluded))
    low_priority=set(rules.get('low_priority_earth_topics',[]))
    low_matches=low_priority.intersection(matches)
    if low_matches and not planetary and not priority_journal(paper,rules):
        excluded.extend('低优先级地球学科：'+topic for topic in sorted(low_matches))
    if 'cryosphere' in matches and not planetary and not priority_journal(paper,rules):
        excluded.append('冰冻圈/冰动力缺少行星语境')
    # A broad topic hit (for example, mantle dynamics or climate modelling)
    # cannot by itself make an Earth paper relevant. Keep non-planetary work
    # only when it appears in the user's specified general-interest journals.
    focused=any(k!='methods' for k in matches)
    if focused and not planetary and not priority_journal(paper,rules):
        excluded.append('缺少明确行星语境，且不属于指定综合顶刊')
    if teacher_author(paper,config):excluded.append('组内教师署名论文')
    direct='astro-ph.EP' in paper.get('categories',[])
    status='candidate' if any(k!='methods' for k in matches) else 'unmatched'
    if excluded: status='excluded'
    reason='关联线索：'+'、'.join(list(dict.fromkeys(w for terms in matches.values() for w in terms))[:6]) if matches else ('行星科学拓展阅读' if direct else '拓展阅读')
    if excluded: reason='当前研究范围外的候选，供管理员复核'
    override=config.get('overrides',{}).get(paper['id'])
    if override: status,reason=override['status'],override['reason']
    fit_score,fit_matches=relevance(text,list(matches),config)
    tags=[m['label'] for m in config.get('mechanisms',[]) if any(contains(text,w) for w in m['terms'])]
    return {'topics':list(matches),'matches':matches,'status':status,'reason':reason,'tags':tags,'method':'manual' if override else 'keyword','fit_score':fit_score,'fit_matches':fit_matches}

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

def checkpoint_since(previous, now, days=1):
    """Use only the normal recent window; never add a multi-day backfill overlap."""
    if previous.get('last_success'):
        return dt.datetime.fromisoformat(previous['last_success'])
    return now - dt.timedelta(days=days)

def error_label(exc):
    if isinstance(exc, urllib.error.HTTPError):
        return f'HTTP {exc.code}'
    return type(exc).__name__

def update(days=1):
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
        since = checkpoint_since(previous, now, days)
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
            api_error = error_label(e)
            sources[category] = {**previous,'last_attempt':stamp,'status':'error','error':api_error}
            try:
                rss_items = rss_feed(category)
                rss_added = 0
                for p in rss_items:
                    if dt.datetime.fromisoformat(p['updated'].replace('Z','+00:00')) < since:
                        continue
                    prior = papers.get(p['id'], {})
                    p['first_seen'] = prior.get('first_seen', stamp)
                    p['version_changed'] = p.get('announcement_type') == 'replace' or bool(prior and prior['version_id'] != p['version_id'])
                    if prior and prior.get('date_kind') != 'announcement':
                        p['published'] = prior['published']
                        p['date_kind'] = 'published'
                    papers[p['id']] = {**prior, **p}
                    rss_added += 1
                sources[category].update(status='partial',last_rss_success=stamp,last_rss_fetched=rss_added,error=api_error)
                print(category, 'API failed:', api_error, '; RSS fallback:', rss_added, 'records')
            except Exception as rss_error:
                failures.append(category)
                sources[category].update(error=f'{api_error}; RSS {error_label(rss_error)}')
                print(category, 'API and RSS failed:', api_error, error_label(rss_error))
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
    parser.add_argument('--days',type=int,default=1)
    args = parser.parse_args()
    raise SystemExit(1 if update(args.days) else 0)
