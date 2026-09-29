"""Admit recent papers first; use a bounded one-year high-fit fallback only on quiet days."""
import argparse
import datetime as dt
import json
import urllib.parse
from pathlib import Path

from build_catalog import apply_publisher_supplements, match, merge_records
from update import classify
from update_journals import get, parse_record, publisher_abstract

ROOT = Path(__file__).resolve().parent
BEIJING = dt.timezone(dt.timedelta(hours=8))
MIN_FALLBACK_SCORE = 65
MAX_FALLBACK = 3
SEARCHES = (
    'exoplanet atmospheric circulation',
    'exoplanet atmospheric chemistry',
    'planetary climate habitability',
    'icy moon ocean ice shell',
    'exoplanet orbital dynamics',
)


def date_part(value):
    """Only day-precision dates can establish a recent publication or update."""
    if not value or len(value) < 10:
        return None
    try:
        return dt.date.fromisoformat(value[:10])
    except ValueError:
        return None


def version_day(value):
    if not value:
        return None
    try:
        return dt.datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(BEIJING).date()
    except ValueError:
        return date_part(value)


def publication_day(paper):
    return date_part(paper.get('publication_date') or paper.get('published'))


def recent(paper, today):
    start = today - dt.timedelta(days=1)
    dates = [publication_day(paper)]
    # Crossref 'indexed' is an indexing timestamp, not a paper version update.
    if paper.get('source') == 'arXiv':
        dates.append(version_day(paper.get('version_date') or paper.get('updated')))
    return any(day and start <= day <= today for day in dates)


def in_fallback_year(paper, today):
    day = publication_day(paper)
    return bool(day and today - dt.timedelta(days=365) <= day < today - dt.timedelta(days=1))


def known(paper, previous):
    return any(paper['id'] == old['id'] or match(paper, old) for old in previous)


def candidates(root, config):
    archives = [json.loads((root / name).read_text())['papers'] for name in
                ('papers.json', 'journal_records.json', 'exoplanet_records.json')]
    records = [paper for archive in archives for paper in archive]
    supplements_path = root / 'exoplanet_metadata_overrides.json'
    supplements = json.loads(supplements_path.read_text()) if supplements_path.exists() else {}
    apply_publisher_supplements(records, supplements)
    for paper in records:
        paper.update(classify(paper, config))
    notes = json.loads((root / 'editorial.json').read_text())
    return [paper for paper in merge_records(records, notes) if paper['status'] == 'candidate']


def search_one_year(root, config, today, limit=MAX_FALLBACK):
    """Five focused Crossref searches; never enumerate whole journal archives."""
    journal_path = root / 'journal_records.json'
    data = json.loads(journal_path.read_text())
    enabled = {journal['issn']: journal for journal in json.loads((root / 'journals.json').read_text())['journals']
               if journal.get('enabled')}
    existing = {paper['id'] for paper in data['papers']}
    found = []
    errors = []
    stamp = dt.datetime.now(dt.timezone.utc).isoformat()
    oldest = (today - dt.timedelta(days=365)).isoformat()
    newest = (today - dt.timedelta(days=2)).isoformat()
    for phrase in SEARCHES:
        query = urllib.parse.urlencode({'query.title': phrase,
            'filter': f'from-pub-date:{oldest},until-pub-date:{newest},type:journal-article',
            'rows': 40})
        try:
            items = get('https://api.crossref.org/works?' + query).get('items', [])
        except Exception as exc:
            errors.append(f'{phrase}: {type(exc).__name__}')
            continue
        for raw in items:
            journal = next((enabled[issn] for issn in raw.get('ISSN', []) if issn in enabled), None)
            if not journal:
                continue
            paper = parse_record(raw, journal, stamp)
            if not paper or paper['id'] in existing or not in_fallback_year(paper, today):
                continue
            paper = publisher_abstract(paper, {}, stamp)
            if not paper.get('abstract'):
                continue
            paper.update(classify(paper, config))
            if paper['status'] != 'candidate' or paper['fit_score'] < MIN_FALLBACK_SCORE:
                continue
            existing.add(paper['id'])
            found.append(paper)
    found.sort(key=lambda paper: (paper['fit_score'], publication_day(paper)), reverse=True)
    selected = found[:limit]
    if selected:
        data['papers'].extend(selected)
        journal_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    return selected, errors


def select(root=ROOT, today=None, online=True):
    today = today or dt.datetime.now(BEIJING).date()
    config = json.loads((root / 'topics.json').read_text())
    previous_path = root / 'catalog.json'
    previous = json.loads(previous_path.read_text()).get('papers', []) if previous_path.exists() else []
    intake_path = root / 'intake.json'
    intake = json.loads(intake_path.read_text()) if intake_path.exists() else {'approved': []}
    approved = set(intake.get('approved', []))
    unapproved = [paper for paper in candidates(root, config)
                  if paper['id'] not in approved and not known(paper, previous)]
    fresh = [paper for paper in unapproved if any(recent(variant, today) for variant in
             [paper] + [r for r in paper.get('variants', [])])]
    selected = fresh
    errors = []
    mode = 'recent'
    if not fresh:
        mode = 'one_year_fallback'
        fallback = [paper for paper in unapproved if paper['fit_score'] >= MIN_FALLBACK_SCORE
                    and any(in_fallback_year(variant, today) for variant in
                            [paper] + [r for r in paper.get('variants', [])])]
        fallback.sort(key=lambda paper: (paper['fit_score'], publication_day(paper) or dt.date.min), reverse=True)
        selected = fallback[:MAX_FALLBACK]
        if online and len(selected) < MAX_FALLBACK:
            discovered, errors = search_one_year(root, config, today, MAX_FALLBACK - len(selected))
            selected += discovered
    approved.update(paper['id'] for paper in selected)
    kinds = intake.get('kinds', {})
    kinds.update({paper['id']: mode for paper in selected})
    intake.update({'approved': sorted(approved), 'last_run': today.isoformat(), 'mode': mode,
                   'selected': [paper['id'] for paper in selected], 'kinds': kinds, 'search_errors': errors,
                   'policy': {'recent_days': 2, 'fallback_days': 365,
                              'min_fallback_score': MIN_FALLBACK_SCORE, 'max_fallback': MAX_FALLBACK}})
    intake_path.write_text(json.dumps(intake, ensure_ascii=False, indent=2) + '\n')
    print(mode, len(selected), 'selected;', len(errors), 'search errors', flush=True)
    return bool(errors)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--offline', action='store_true')
    args = parser.parse_args()
    raise SystemExit(1 if select(online=not args.offline) else 0)
