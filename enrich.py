"""Source-backed affiliations and versioned bilingual editorial notes; no AI API."""
import datetime as dt
import hashlib
import json
import re
import time
import urllib.request
import unicodedata
from html.parser import HTMLParser
from pathlib import Path
from institution_utils import orcid_url

ROOT = Path(__file__).resolve().parent
VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
class Node:
    def __init__(self, attrs=None): self.attrs=dict(attrs or []); self.children=[]
    def text(self): return ''.join(x.text() if isinstance(x,Node) else x for x in self.children)
    def has(self, name): return name in self.attrs.get('class','').split()
    def find(self, name):
        out=[self] if self.has(name) else []
        for c in self.children:
            if isinstance(c,Node):out.extend(c.find(name))
        return out
class Tree(HTMLParser):
    def __init__(self):super().__init__();self.root=Node();self.stack=[self.root]
    def handle_starttag(self,tag,attrs):
        node=Node(attrs);self.stack[-1].children.append(node)
        if tag not in VOID:self.stack.append(node)
    def handle_endtag(self,tag):
        if tag not in VOID and len(self.stack)>1:self.stack.pop()
    def handle_startendtag(self,tag,attrs):self.handle_starttag(tag,attrs);self.handle_endtag(tag)
    def handle_data(self,data):self.stack[-1].children.append(data)

def clean(s):return re.sub(r'\s+',' ',s).strip()
class Byline(HTMLParser):
    """Read individual author links from arXiv's authoritative abstract page."""
    def __init__(self):
        super().__init__(); self.depth=0; self.in_link=False; self.parts=[]; self.authors=[]
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag=='div':
            if self.depth:self.depth+=1
            elif 'authors' in attrs.get('class','').split():self.depth=1
        if self.depth and tag=='a':self.in_link=True;self.parts=[]
    def handle_data(self, data):
        if self.in_link:self.parts.append(data)
    def handle_endtag(self, tag):
        if tag=='a' and self.in_link:
            name=clean(''.join(self.parts))
            if name:self.authors.append(name)
            self.in_link=False
        if tag=='div' and self.depth:self.depth-=1

def byline(html):
    parser=Byline();parser.feed(html);return parser.authors

def name_key(name):return unicodedata.normalize('NFC',clean(name)).casefold()

def reconcile_affiliations(authors, expected):
    """Reject demonstrably malformed converted pages, not legitimate name variants.

    Digits/TeX remnants in unverified person fields and multiple *complete*
    official author names in one field demonstrate conversion contamination.
    Initials versus full names alone never invalidate an existing association.
    """
    allowed={name_key(name) for name in (expected or [])}
    for author in authors:
        name=name_key(author['name'])
        if name in allowed:continue
        if re.search(r'[0-9\\\\]',name):return []
        hits=[value for value in allowed if re.search(r'(?<!\w)'+re.escape(value)+r'(?!\w)',name)]
        if len(hits)>1:return []
    return authors

def validate_affiliation_entry(entry, expected):
    original=entry.get('author_affiliations',[])
    checked=reconcile_affiliations(original,expected)
    if original and not checked:
        # Retain source evidence for review, but never consume it as people.
        entry.setdefault('rejected_author_affiliations',original)
        entry['author_affiliation_status']='unavailable'
        entry['author_affiliation_note']='Malformed experimental HTML; person-level mappings withheld'
    entry['author_affiliations']=checked
    return entry

def affiliations(html, expected=None, validate=True):
    tree=Tree();tree.feed(html)
    def org(n):return re.sub(r'^Affiliation\s*:\s*','',clean(n.text())).strip()
    all_orgs=list(dict.fromkeys(org(n) for n in tree.root.find('ltx_role_affiliation') if org(n)))
    authors=[]
    for n in tree.root.find('ltx_role_author'):
        names=n.find('ltx_personname')
        if not names:continue
        name=clean(names[0].text())
        # Explicit local author block only; never infer mappings from global ordering.
        orgs=list(dict.fromkeys(org(a) for a in n.find('ltx_role_affiliation') if org(a)))
        if name:
            def links(node):
                found=[orcid_url(node.attrs.get('href'))]
                for child in node.children:
                    if isinstance(child,Node):found.extend(links(child))
                return [x for x in found if x]
            ids=set(links(n))
            authors.append({'name':name,'institutions':orgs,'orcid':next(iter(ids)) if len(ids)==1 else None})
    return all_orgs,reconcile_affiliations(authors,expected) if validate else authors

def digest(p):return hashlib.sha256((p['title']+'\n'+p['abstract']).encode()).hexdigest()
def apply_notes(p, notes):
    doi=re.sub(r'^https?://(?:dx\.)?doi\.org/','',p.get('doi') or '',flags=re.I).lower().strip()
    n=notes.get(p['id'])
    if n:
        version_matches=n.get('version_id')==p.get('version_id')
    else:
        n=notes.get('doi:'+doi) if doi else None
        version_matches=n and (n.get('doi','').lower()==doi or n.get('version_id')=='doi:'+doi)
    if n and version_matches and n.get('abstract_sha256')==digest(p):
        p['intro_zh']=n['zh'];p['intro_en']=n['en'];p['intro_kind']='bilingual_editorial';p['intro_basis']=({'title only':'仅依据标题整理；未取得摘要或正文','publisher text':'基于出版社正文／研究简报整理','publisher abstract':'基于出版社页面摘要整理'}.get(n.get('basis'),'基于公开摘要整理') + (' · 英文为摘要节选' if n.get('english_basis')=='abstract excerpt' and n.get('en') else ''));p['intro_source']=n.get('source_url','');p['intro_version']=n['version_id']
        p['tags']=list(dict.fromkeys(p.get('tags',[])+n.get('tags',[])))
    else:
        abstract=p.get('abstract','')
        sentences=re.split(r'(?<=[.!?])\s+(?=[A-Z])',abstract)
        selected=' '.join(sentences[:2])
        p['intro_en']=selected[:650]+('…' if len(selected)>650 else '')
        if abstract:
            p['intro_zh']='中文导读待整理；可展开英文摘要查看研究内容。'
            p['intro_kind']='abstract_excerpt';p['intro_basis']='英文摘要节选'
        else:
            p['intro_zh']='仅依据标题，待补摘要。'
            p['intro_kind']='title_only';p['intro_basis']='仅依据标题；未取得摘要或正文'
        p.pop('intro_version',None);p.pop('intro_source',None)


def enrich(fetch=True, max_fetch=60):
    data=json.loads((ROOT/'papers.json').read_text())
    notes=json.loads((ROOT/'editorial.json').read_text()) if (ROOT/'editorial.json').exists() else {}
    cache_path=ROOT/'affiliations.json'
    cache=json.loads(cache_path.read_text()) if cache_path.exists() else {}
    count=0;now=dt.datetime.now(dt.timezone.utc)
    # Relevant records first; failed extractions are retried after a week.
    for p in sorted(data['papers'],key=lambda p:p.get('status')!='candidate'):
        key=p['version_id'];entry=cache.get(key)
        # RSS dc:creator is an opaque byline, not one person. Recover boundaries
        # from the versioned abstract page, never by splitting on punctuation.
        needs_byline=(not p.get('authors') and bool(p.get('authors_raw'))) or (len(p.get('authors',[]))==1 and ',' in p['authors'][0])
        if entry and entry.get('byline_authors'):
            p['authors']=entry['byline_authors'];p['authors_source']=entry['byline_source']
            needs_byline=False
        if fetch and needs_byline and count<max_fetch:
            count+=1;url='https://arxiv.org/abs/'+key
            try:
                time.sleep(3.1)
                req=urllib.request.Request(url,headers={'User-Agent':'PlanetFluidLiteratureRadar/0.3'})
                with urllib.request.urlopen(req,timeout=18) as r:names=byline(r.read(4_000_000).decode('utf-8','replace'))
                if names:
                    entry=entry or {'institutions':[],'author_affiliations':[],'status':'unavailable','source_url':'https://arxiv.org/html/'+key,'checked_at':'1970-01-01T00:00:00+00:00'}
                    entry.update(byline_authors=names,byline_source=url)
                    validate_affiliation_entry(entry,names)
                    cache[key]=entry;p['authors']=names;p['authors_source']=url;needs_byline=False
            except Exception:pass
        retry=not entry or (entry['status']!='verified' and (now-dt.datetime.fromisoformat(entry['checked_at'])).days>=7)
        if fetch and retry and count<max_fetch:
            count+=1;url='https://arxiv.org/html/'+key
            prior_entry=entry or {}
            try:
                time.sleep(3.1)
                req=urllib.request.Request(url,headers={'User-Agent':'PlanetFluidLiteratureRadar/0.2'})
                with urllib.request.urlopen(req,timeout=18) as r: html=r.read(8_000_000).decode('utf-8','replace')
                orgs,authors=affiliations(html,validate=False)
                entry={'institutions':orgs,'author_affiliations':authors,'status':'verified' if orgs else 'unavailable','source_url':url,'checked_at':now.isoformat()}
                validate_affiliation_entry(entry,p.get('authors') if not needs_byline else None)
                if needs_byline and entry['author_affiliations']:
                    entry.update(rejected_author_affiliations=entry['author_affiliations'],author_affiliations=[],author_affiliation_status='unavailable',author_affiliation_note='Structured source byline unavailable; mappings withheld')
            except Exception:
                entry={'institutions':[],'author_affiliations':[],'status':'unavailable','source_url':url,'checked_at':now.isoformat()}
            entry.update({k:prior_entry[k] for k in ('byline_authors','byline_source','rejected_author_affiliations') if k in prior_entry and k not in entry})
            cache[key]=entry
            cache_path.write_text(json.dumps(cache,ensure_ascii=False,indent=2)+'\n')
            print(key,entry['status'],len(entry['institutions']),flush=True)
        if entry:
            validate_affiliation_entry(entry,p.get('authors') if not needs_byline else None)
            if entry.get('author_affiliation_status'):
                p['author_affiliation_status']=entry['author_affiliation_status']
            p['institutions']=entry['institutions'];p['author_affiliations']=entry['author_affiliations'];p['affiliation_status']=entry['status'];p['affiliation_source']=entry['source_url']
        else:
            p.update(institutions=[],author_affiliations=[],affiliation_status='pending')
        apply_notes(p,notes)
    if fetch:
        from author_names import update_names
        journals=json.loads((ROOT/'journal_records.json').read_text()) if (ROOT/'journal_records.json').exists() else {'papers':[]}
        update_names(data['papers']+journals['papers'],max_fetch)
    cache_path.write_text(json.dumps(cache,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'papers.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--offline',action='store_true');parser.add_argument('--limit',type=int,default=60)
    args=parser.parse_args();enrich(not args.offline,args.limit)
