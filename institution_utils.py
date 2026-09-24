"""Conservative parent normalization from explicit affiliation text and aliases."""
import re
import unicodedata
from functools import lru_cache

@lru_cache(maxsize=30000)
def normalize(s):
 s=unicodedata.normalize('NFKD',s).casefold()
 s=''.join(c for c in s if not unicodedata.combining(c))
 return re.sub(r'[^\w]+',' ',s).strip()

def clean(raw):
 raw=re.sub(r'<[^>]*>|\\(?:aff|textsuperscript|thanks)\{?[^\s}]*\}?',' ',raw)
 raw=re.split(r'\b(?:addressline|city|state|country|postcode)\s*=',raw,flags=re.I)[0]
 raw=re.sub(r'\borganization\s*=','',raw,flags=re.I)
 raw=re.sub(r'^\s*(?:Affiliation\s*:|\d+\s*|[a-z](?=[A-Z]))','',raw)
 return re.sub(r'\s+',' ',raw).strip(' ,;.')

def parents(raw,aliases):
 text=normalize(clean(raw));hits=[]
 for a in aliases:
  if a.get('context') and not any(re.search(r'(?<!\w)'+re.escape(normalize(c))+r'(?!\w)',normalize(raw)) for c in a['context']):continue
  for pattern in a.get('_patterns') or [re.compile(r'(?<!\w)'+re.escape(normalize(t))+r'(?!\w)') for t in a['match']]:
   for m in pattern.finditer(text):hits.append((m.start(),m.end(),a['name']))
 # A university name containing another institution name is one affiliation,
 # e.g. University of Chinese Academy of Sciences is distinct from CAS.
 hits=[h for h in hits if not any(g[0]<=h[0] and g[1]>=h[1] and g[1]-g[0]>h[1]-h[0] for g in hits)]
 return list(dict.fromkeys(h[2] for h in sorted(hits)))

def subdivisions(raw,parent,aliases):
 text=clean(raw)
 # Prefix before an explicitly named parent generally contains its departments.
 terms=[k for a in aliases if a['name']==parent for k in a['match']]
 prefix=None
 for i in range(len(text)):
  if any(normalize(text[i:]).startswith(normalize(t)) for t in terms):prefix=text[:i];break
 if prefix is None:return []
 parts=re.split(r'[,;]|\band\b(?=\s+(?:Department|Institute|School|College|Center|Centre|Laboratory))',prefix)
 result=[]
 for part in parts:
  part=part.strip(' ,;./')
  if len(part)<6 or len(part)>180:continue
  if re.search(r'@|\d{4,}|=|\\|https?',part):continue
  if parents(part,aliases):continue
  if re.search(r'\b(?:department|school|faculty|college|laboratory|institute|center|centre|division|observatory|branch|program)\b|学院|实验室|研究所',part,re.I):result.append(part)
 return list(dict.fromkeys(result))

def orcid_url(value):
 m=re.fullmatch(r'(?:https?://(?:www\.)?orcid\.org/)?(\d{4}-\d{4}-\d{4}-\d{3}[\dX])/?',str(value or '').strip(),re.I)
 if not m:return None
 digits=m[1].upper().replace('-','');total=0
 for c in digits[:15]:total=(total+int(c))*2
 check=(12-total%11)%11
 if digits[-1]!=('X' if check==10 else str(check)):return None
 return 'https://orcid.org/'+m[1].upper()

def verified_hierarchy(root):
 import json
 registry=json.loads((root/'institution_registry.json').read_text())
 official=json.loads((root/'institution_units.json').read_text())
 chinese=json.loads((root/'institution_chinese.json').read_text())
 unit_records=json.loads((root/'institution_unit_records.json').read_text())
 def han_name(names):return next((n['value'] for n in names if n.get('lang')=='zh' and re.search(r'[\u3400-\u9fff]',n['value'])),None)
 aliases=[];units={};evidence={};canonical={}
 for original,r in registry.items():
  if r.get('status')!='verified':continue
  name=r['name'];canonical[original]=name;evidence[name]={**r,'name_zh':han_name(r['names']) or chinese.get(name,{}).get('name_zh')}
  matches=[n['value'] for n in r['names'] if len(normalize(n['value']))>4 or n['value'] in ['NASA','NOAA','CNRS','DESY']]
  matches+=r.get('reviewed_aliases',[])
  aliases.append({'name':name,'match':matches,'context':r.get('context',[])})
  for child in r['relationships']:
   if child['type']=='child':units.setdefault(name,[]).append({'name':child['label'],'match':[child['label']],'source':r['source'],'ror':child['id'],'name_zh':han_name(unit_records.get(child['id'],{}).get('names',[]))})
 for u in official:
  parent=canonical.get(u['parent'])
  if parent:units.setdefault(parent,[]).append(u)
 for a in aliases:a['_patterns']=[re.compile(r'(?<!\w)'+re.escape(normalize(t))+r'(?!\w)') for t in a['match']]
 for rows in units.values():
  for u in rows:u['_patterns']=[re.compile(r'(?<!\w)'+re.escape(normalize(t))+r'(?!\w)') for t in u['match']]
 return aliases,units,evidence

def verified_units(raw,parent,units):
 text=normalize(clean(raw));hits=[]
 for u in units.get(parent,[]):
  for pattern in u['_patterns']:
   for m in pattern.finditer(text):hits.append((m.start(),m.end(),u))
 # Do not turn Guangzhou Institute of Geochemistry into Institute of Geochemistry.
 hits=[h for h in hits if not any(g[0]<=h[0] and g[1]>=h[1] and g[1]-g[0]>h[1]-h[0] for g in hits)]
 return list({normalize(h[2]['name']):h[2] for h in hits}.values())
