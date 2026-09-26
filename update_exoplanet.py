"""Import only current Exoplanet.eu bibliography additions; never backfill its archive."""
import argparse
import datetime as dt
import html
from html.parser import HTMLParser
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from update import classify, priority_journal

ROOT = Path(__file__).resolve().parent
BASE = 'https://exoplanet.eu/bibliography/all/'
TZ = dt.timezone(dt.timedelta(hours=8))


def clean(value):
    return ' '.join(html.unescape(value or '').split())


class BibliographyParser(HTMLParser):
    VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows = []
        self.row = None
        self.depth = 0
        self.title_depth = None
        self.anchor = None
        self.lines = []
        self.line = ''

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if self.row is None and tag == 'li' and 'publication' in attrs.get('class', '').split():
            self.row = {'id': attrs.get('id', ''), 'title': '', 'anchors': []}
            self.depth = 1
            self.lines = []
            self.line = ''
        elif self.row is not None and tag not in self.VOID:
            self.depth += 1
        if self.row is None:
            return
        if tag == 'h5' and self.title_depth is None:
            self.title_depth = self.depth
        if tag == 'p' and self.line.strip():
            self.lines.append(clean(self.line)); self.line = ''
        if tag == 'br':
            self.lines.append(clean(self.line)); self.line = ''
        if tag == 'a':
            self.anchor = {'href': attrs.get('href', ''), 'text': ''}

    def handle_endtag(self, tag):
        if self.row is None:
            return
        if tag == 'a' and self.anchor is not None:
            self.row['anchors'].append(self.anchor)
            self.anchor = None
        if tag == 'h5' and self.title_depth == self.depth:
            self.title_depth = None
            self.lines.append(clean(self.line)); self.line = ''
        if tag == 'li' and self.depth == 1:
            self.lines.append(clean(self.line))
            self.row['title'] = clean(self.row['title'])
            self.row['lines'] = [x for x in self.lines if x]
            self.row['text'] = clean(' '.join(self.row['lines']))
            self.rows.append(self.row)
            self.row = None
            self.depth = 0
        elif tag not in self.VOID:
            self.depth -= 1

    def handle_data(self, data):
        if self.row is None:
            return
        self.line += data
        if self.title_depth is not None:
            self.row['title'] += data
        if self.anchor is not None:
            self.anchor['text'] += data


def parse_date(row, label):
    match = re.search(label + r'\s*:\s*(\d{2}/\d{2}/\d{4})', row['text'], re.I)
    if not match:
        return None
    try:
        return dt.datetime.strptime(match.group(1), '%d/%m/%Y').date()
    except ValueError:
        return None


def absolute_url(href):
    return urllib.parse.urljoin(BASE, html.unescape(href or ''))


def arxiv_id(value):
    hit = re.search(r'(?:arxiv(?:\.org/(?:abs|pdf)/|[:.])|10\.48550/arxiv[./])\s*(\d{4}\.\d{4,5})(?:v\d+)?', value, re.I)
    return hit.group(1) if hit else None


def parse_row(row, stamp, config):
    bib = re.search(r'publication_(\d+)', row.get('id', ''))
    if not bib or not row.get('title'):
        return None
    anchors = [(a.get('text', '').strip().lower(), absolute_url(a.get('href'))) for a in row['anchors']]
    paper_url = next((u for label, u in anchors if label == 'paper'), '')
    arxiv_url = next((u for label, u in anchors if label == 'arxiv'), '')
    paper_doi = ''
    if paper_url:
        hit = re.search(r'(?:doi\.org/|doi:)(10\.\d{4,9}/\S+)', paper_url, re.I)
        if hit and not hit.group(1).lower().startswith('10.48550/arxiv.'):
            paper_doi = urllib.parse.unquote(hit.group(1)).rstrip('.,;)')
    axid = arxiv_id(arxiv_url) or arxiv_id(paper_url)
    text = row['text']
    lines = [clean(line) for line in row.get('lines', [])]
    authors = []
    author_line = ''
    for line in lines:
        if line == row['title'] or re.search(r'(?:publication date|creation date|last update)\s*:', line, re.I):
            continue
        if re.search(r'^[A-ZÀ-ÖØ-Þ][A-ZÀ-ÖØ-Þ .\-&,]+(?:\s+et al\.)?$', line):
            author_line = line
            break
    if author_line:
        authors = [clean(x) for x in re.split(r',\s*|\s*&\s*', author_line.replace(' et al.', '')) if clean(x)]
    citation = ''
    if author_line:
        index = lines.index(author_line)
        citation = next((line for line in lines[index + 1:] if line and not re.search(r'(?:publication date|creation date|last update|^(?:paper|arxiv)$)', line, re.I)), '')
    created = parse_date(row, 'creation date')
    updated = parse_date(row, 'last update')
    effective = max([x for x in (created, updated) if x], default=None)
    publication = re.search(r'publication date\s*:\s*(\d{4})(?:-(\d{2}))?', text, re.I)
    publication_date = publication.group(1) + ('-' + publication.group(2) if publication.group(2) else '') if publication else None
    journal = citation.split(',')[0].strip() if citation else ''
    p = {
        'id': 'exoplanet-bib:' + bib.group(1), 'version_id': 'exoplanet-bib:' + bib.group(1),
        'exoplanet_id': bib.group(1), 'title': row['title'], 'abstract': '', 'authors': authors,
        'source': 'exoplanet.eu', 'source_group': 'exoplanet bibliography', 'journal': journal,
        'url': paper_url or arxiv_url or BASE + '?page=1#publication_' + bib.group(1),
        'doi': paper_doi or None, 'publication_date': publication_date, 'published': publication_date or '',
        'publication_date_source': 'Exoplanet.eu bibliography', 'date_kind': 'bibliography',
        'first_seen': stamp, 'updated': effective.isoformat() if effective else stamp,
        'metadata_source': BASE + '#publication_' + bib.group(1), 'affiliation_status': 'unavailable',
        'metadata_limited': True, 'categories': [], 'exoplanet_update_date': effective.isoformat() if effective else None,
    }
    if axid:
        p['relations'] = {'preprint': [{'id': 'https://arxiv.org/abs/' + axid}]}
        p['arxiv_id'] = axid
    p.update(classify(p, config))
    if p.get('status') == 'candidate' and priority_journal(p, config.get('scope_exclusion_rules', {})):
        p['status'] = 'candidate'
    return p


def fetch_page(page):
    url = BASE + '?' + urllib.parse.urlencode({'page': page})
    req = urllib.request.Request(url, headers={'User-Agent': 'PlanetFluidLiteratureRadar/0.4 (daily metadata index)'})
    with urllib.request.urlopen(req, timeout=30) as response:
        content = response.read(5_000_000).decode('utf-8', 'replace')
    parser = BibliographyParser()
    parser.feed(content)
    return parser.rows


def apply_metadata_supplements(records, supplements):
    for paper in records.values():
        doi = (paper.get('doi') or '').lower().strip()
        supplement = supplements.get(doi) or supplements.get('doi:' + doi)
        if supplement and supplement.get('abstract'):
            paper['abstract'] = supplement['abstract']
            paper['abstract_source'] = supplement.get('source_url', '')
            paper['metadata_limited'] = False


def update(days=1, max_pages=20, now=None):
    config = json.loads((ROOT / 'topics.json').read_text())
    supplement_path = ROOT / 'exoplanet_metadata_overrides.json'
    supplements = json.loads(supplement_path.read_text()) if supplement_path.exists() else {}
    path = ROOT / 'exoplanet_records.json'
    old = json.loads(path.read_text()) if path.exists() else {'papers': [], 'sources': {}}
    source = old.get('sources', {}).get('exoplanet.eu', {})
    now = now or dt.datetime.now(TZ)
    stamp = now.isoformat()
    previous_day = dt.date.fromisoformat(source['last_success'][:10]) if source.get('last_success') else now.date() - dt.timedelta(days=max(1, days))
    since = previous_day
    records = {p['id']: p for p in old.get('papers', [])}
    fresh = 0
    retained = 0
    pages = 0
    try:
        for page in range(1, max_pages + 1):
            if page > 1:
                time.sleep(1.0)
            rows = fetch_page(page)
            pages += 1
            if not rows:
                break
            newest_on_page = None
            for row in rows:
                parsed = parse_row(row, stamp, config)
                if not parsed:
                    continue
                effective = dt.date.fromisoformat(parsed['exoplanet_update_date']) if parsed.get('exoplanet_update_date') else None
                if effective and (newest_on_page is None or effective > newest_on_page):
                    newest_on_page = effective
                if not effective or effective < since:
                    continue
                fresh += 1
                if parsed.get('status') != 'candidate':
                    continue
                previous = records.get(parsed['id'])
                parsed['first_seen'] = previous.get('first_seen', stamp) if previous else stamp
                records[parsed['id']] = {**(previous or {}), **parsed}
                retained += 1
            if newest_on_page is None or newest_on_page < since:
                break
        source = {'name': 'Exoplanet.eu bibliography', 'url': BASE, 'status': 'ok', 'last_attempt': stamp,
                  'last_success': stamp, 'coverage_since': source.get('coverage_since', since.isoformat()),
                  'pages_checked': pages, 'fetched': fresh, 'retained': retained,
                  'method': 'daily incremental bibliography page scan; candidate-only'}
    except Exception as exc:
        source = {**source, 'name': 'Exoplanet.eu bibliography', 'url': BASE, 'status': 'error',
                  'last_attempt': stamp, 'error': type(exc).__name__}
        print('Exoplanet.eu FAILED', type(exc).__name__, flush=True)
        # Publisher abstracts are local metadata supplements, so apply them even
        # when the remote bibliography is temporarily unavailable.
        apply_metadata_supplements(records, supplements)
        old.setdefault('sources', {})['exoplanet.eu'] = source
        old.update(generated_at=stamp, papers=sorted(records.values(), key=lambda p: p.get('first_seen', ''), reverse=True))
        path.write_text(json.dumps(old, ensure_ascii=False, indent=2) + '\n')
        return True
    old.setdefault('sources', {})['exoplanet.eu'] = source
    apply_metadata_supplements(records, supplements)
    old.update(generated_at=stamp, papers=sorted(records.values(), key=lambda p: p.get('first_seen', ''), reverse=True))
    path.write_text(json.dumps(old, ensure_ascii=False, indent=2) + '\n')
    print('Exoplanet.eu', fresh, 'recent entries;', retained, 'relevant additions from', pages, 'pages', flush=True)
    return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--days', type=int, default=1)
    parser.add_argument('--max-pages', type=int, default=20)
    args = parser.parse_args()
    raise SystemExit(1 if update(args.days, args.max_pages) else 0)
