/* Anonymous shared recommendations; no author identities or visitor IPs are sent. */
class PaperRecommendations {
 constructor(endpoint) {
  this.endpoint=endpoint?.replace(/\/$/,'');this.counts={};this.mine=new Set();this.pending=new Set();this.ready=false;
  try {this.reader=localStorage.getItem('radar-reader');if(!/^[\da-f-]{36}$/i.test(this.reader||'')){this.reader=crypto.randomUUID();localStorage.setItem('radar-reader',this.reader)}}catch(_){this.reader=crypto.randomUUID()}
 }
 async request(options={}) {
  if(!this.endpoint)throw Error('Recommendations are not configured.');
  const response=await fetch(this.endpoint+'/recommendations'+(options.method?'':'?reader='+encodeURIComponent(this.reader)),{...options,cache:'no-store',signal:AbortSignal.timeout(15000)});
  if(!response.ok)throw Error('Recommendations are unavailable. Please try again later.');
  const result=await response.json();this.counts=result.counts||{};this.mine=new Set(result.mine||[]);this.ready=true;
 }
 async load(){await this.request()}
 count(id){return Number(this.counts[id]||0)}
 async toggle(id){
  if(!this.ready||this.pending.has(id))return;
  this.pending.add(id);
  try{await this.request({method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({paper_id:id,reader_id:this.reader,recommended:!this.mine.has(id)})})}finally{this.pending.delete(id)}
 }
}

let data,status='all',limit=30,keyword='topic:all',allTags=[],sortOrder='recent',timeline,recommendations;
const $=s=>document.querySelector(s);
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const safe=s=>/^https?:\/\//i.test(s||'')?esc(s):'#';
const tagParts=s=>{const parts=String(s??'').split(' · ');return [parts.shift()||'',parts.join(' · ')];};
const englishTag=s=>tagParts(s)[1]||tagParts(s)[0];
const date=s=>!s?'Unknown':/^\d{4}(-\d{2})?$/.test(s)?s:new Date(s).toLocaleDateString('en-CA',{year:'numeric',month:'2-digit',day:'2-digit',timeZone:'Asia/Shanghai'});
// Day precision is required: never invent a day for a month-only publication date.
const DAY_MS=86400000;
function publicationDay(p){
 const value=String(p.publication_date||'');
 if(!/^\d{4}-\d{2}-\d{2}$/.test(value))return null;
 const number=Date.parse(value+'T00:00:00Z');
 return Number.isFinite(number)&&new Date(number).toISOString().slice(0,10)===value?value:null;
}
const dayNumber=value=>Math.floor(Date.parse(value+'T00:00:00Z')/DAY_MS);
const dayString=value=>new Date(value*DAY_MS).toISOString().slice(0,10);
const beijingToday=()=>new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Shanghai',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
const heatLevel=count=>count===0?0:count===1?1:count<=3?2:count<=7?3:4;
function publicationCounts(papers){
 const counts=new Map();let undated=0;
 for(const p of papers){const day=publicationDay(p);if(day)counts.set(day,(counts.get(day)||0)+1);else undated++}
 return {counts,undated};
}
class PublicationTimeline{
 constructor(root,papers,onChange){
  this.root=root;this.onChange=onChange;this.today=dayNumber(beijingToday());this.end=this.today;
  const known=papers.map(publicationDay).filter(Boolean).map(dayNumber);
  this.earliest=Math.min(this.today,...known);this.days=matchMedia('(max-width:640px)').matches?30:90;this.range=null;
  root.hidden=false;
  root.innerHTML=`<div class="timeline-heading"><h2>Publication dates</h2><div class="timeline-navigation"><button type="button" data-pan="-1" aria-label="Earlier dates">←</button><span id="timeline-window"></span><button type="button" data-pan="1" aria-label="Later dates">→</button></div><div class="timeline-views" aria-label="Timeline window"><button type="button" data-window="30">30d</button><button type="button" data-window="90">90d</button><button type="button" data-window="365">1y</button></div></div><div class="timeline-plot"><div id="timeline-tooltip" class="timeline-tooltip" hidden></div><div id="timeline-days" class="timeline-days" aria-label="Daily publication heatmap; click or drag to select"></div><div id="timeline-selection" class="timeline-selection" hidden></div></div><div id="timeline-axis" class="timeline-axis" aria-hidden="true"></div><div class="timeline-bottom"><span id="timeline-summary" role="status"></span><button type="button" id="timeline-latest">Last 2 days</button><button type="button" id="timeline-reset">Clear dates</button><details class="custom-dates"><summary>Custom range</summary><div class="timeline-dates"><label>From <input id="publication-from" type="date" aria-label="Published from"></label><label>To <input id="publication-to" type="date" aria-label="Published to"></label></div></details><div class="timeline-legend" aria-label="Darker blue means more papers"><span>Papers/day</span>${['0','1','2–3','4–7','8+'].map((label,i)=>`<span><i class="heat-${i}"></i>${label}</span>`).join('')}</div></div><p id="timeline-note" class="timeline-note"></p>`;
  this.strip=root.querySelector('#timeline-days');this.overlay=root.querySelector('#timeline-selection');this.tooltip=root.querySelector('#timeline-tooltip');
  root.querySelectorAll('[data-window]').forEach(button=>button.addEventListener('click',()=>{this.days=Number(button.dataset.window);this.draw()}));
  root.querySelectorAll('[data-pan]').forEach(button=>button.addEventListener('click',()=>{this.end=Math.min(this.today,Math.max(this.earliest,this.end+Number(button.dataset.pan)*this.days));this.draw()}));
  root.querySelector('#timeline-latest').addEventListener('click',()=>{this.end=this.today;this.select([dayString(this.today-1),dayString(this.today)])});
  root.querySelector('#timeline-reset').addEventListener('click',()=>this.select(null));
  for(const id of ['publication-from','publication-to']){
   const input=root.querySelector('#'+id);input.max=dayString(this.today);
   input.addEventListener('change',()=>{
    const from=root.querySelector('#publication-from'),to=root.querySelector('#publication-to');
    if(!from.value&&!to.value){this.select(null);return}
    if(!from.checkValidity()||!to.checkValidity()){input.reportValidity();return}
    const a=from.value||to.value,b=to.value||from.value;this.select(a<=b?[a,b]:[b,a]);
   });
  }
  this.strip.addEventListener('pointerdown',e=>{
   if(e.button!==0||!e.target.closest('[data-day]'))return;
   this.anchor=this.indexAt(e.clientX);this.cursor=this.anchor;this.dragging=true;this.strip.setPointerCapture(e.pointerId);e.preventDefault();this.preview();
  });
  this.strip.addEventListener('pointermove',e=>{
   const index=this.indexAt(e.clientX);this.showTooltip(index);
   if(this.dragging){this.cursor=index;this.preview()}
  });
  this.strip.addEventListener('pointerup',()=>{
   if(!this.dragging)return;this.dragging=false;
   this.select([dayString(this.start+Math.min(this.anchor,this.cursor)),dayString(this.start+Math.max(this.anchor,this.cursor))]);
  });
  this.strip.addEventListener('pointercancel',()=>{this.dragging=false;this.drawSelection()});
  this.strip.addEventListener('pointerleave',()=>{if(!this.dragging)this.tooltip.hidden=true});
  this.strip.addEventListener('click',e=>{const button=e.target.closest('[data-day]');if(button&&e.detail===0)this.select([button.dataset.day,button.dataset.day])});
  this.strip.addEventListener('focusin',e=>{if(e.target.dataset.day)this.showTooltip(dayNumber(e.target.dataset.day)-this.start)});
  this.strip.addEventListener('focusout',()=>{this.tooltip.hidden=true});
  this.strip.addEventListener('keydown',e=>{
   const button=e.target.closest('[data-day]');if(!button)return;
   if(e.key==='Escape'){this.select(null);return}
   if(!['ArrowLeft','ArrowRight','Home','End'].includes(e.key))return;
   e.preventDefault();const current=dayNumber(button.dataset.day)-this.start;
   const next=e.key==='Home'?0:e.key==='End'?this.days-1:Math.max(0,Math.min(this.days-1,current+(e.key==='ArrowLeft'?-1:1)));
   if(e.shiftKey){const anchor=this.keyAnchor??current;this.keyAnchor=anchor;this.select([dayString(this.start+Math.min(anchor,next)),dayString(this.start+Math.max(anchor,next))])}else this.keyAnchor=null;
   this.strip.querySelectorAll('button')[next]?.focus({preventScroll:true});
  });
 }
 indexAt(x){const r=this.strip.getBoundingClientRect();return Math.max(0,Math.min(this.days-1,Math.floor((x-r.left)/r.width*this.days)))}
 select(range){this.range=range;this.drawSelection();this.onChange()}
 matches(p){const day=publicationDay(p);return !this.range||day&&day>=this.range[0]&&day<=this.range[1]}
 setPapers(papers){this.papers=papers;const {counts,undated}=publicationCounts(papers);this.counts=counts;this.undated=undated;this.draw()}
 draw(){
  const focused=document.activeElement?.dataset.day;this.start=this.end-this.days+1;
  this.root.querySelectorAll('[data-window]').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.window)===this.days)));
  this.root.querySelector('[data-pan="1"]').disabled=this.end>=this.today;
  this.root.querySelector('[data-pan="-1"]').disabled=this.start<=this.earliest;
  this.root.querySelector('#timeline-window').textContent=dayString(this.start).replaceAll('-','/')+' — '+dayString(this.end).replaceAll('-','/');
  this.strip.dataset.window=this.days;
  this.strip.innerHTML=Array.from({length:this.days},(_,i)=>{const day=dayString(this.start+i),count=this.counts.get(day)||0;return `<button type="button" class="timeline-day heat-${heatLevel(count)}" data-day="${day}" aria-label="${day}, ${count} papers" aria-pressed="false"><span>${count||''}</span></button>`}).join('');
  const step=this.days<=30?7:this.days<=90?14:60;
  const ticks=[0,...Array.from({length:Math.floor((this.days-1)/step)},(_,i)=>(i+1)*step).filter(i=>i<this.days-1-step/2),this.days-1];
  this.root.querySelector('#timeline-axis').innerHTML=ticks.map(i=>`<span style="left:${(i+.5)/this.days*100}%">${dayString(this.start+i).slice(5).replace('-','/')}</span>`).join('');
  this.root.querySelector('#timeline-note').textContent=this.undated?`${this.undated} papers have no exact publication day.`:'';
  this.drawSelection();if(focused)this.strip.querySelector(`[data-day="${focused}"]`)?.focus({preventScroll:true});
 }
 showTooltip(index){
  const day=dayString(this.start+index);this.tooltip.textContent=day.replaceAll('-','/')+' · '+(this.counts.get(day)||0)+' papers';
  this.tooltip.hidden=false;this.tooltip.style.left=`${Math.max(8,Math.min(92,(index+.5)/this.days*100))}%`;
 }
 preview(){this.paint(Math.min(this.anchor,this.cursor),Math.max(this.anchor,this.cursor))}
 paint(start,end){
  const a=Math.max(0,start),b=Math.min(this.days-1,end);this.overlay.hidden=start>this.days-1||end<0;
  this.overlay.style.left=a/this.days*100+'%';this.overlay.style.width=(b-a+1)/this.days*100+'%';
 }
 drawSelection(){
  const [from,to]=this.range||['',''];this.root.querySelector('#publication-from').value=from;this.root.querySelector('#publication-to').value=to;
  this.root.querySelector('#timeline-reset').disabled=!this.range;
  const count=this.papers?.filter(p=>this.matches(p)).length||0;
  this.root.querySelector('#timeline-summary').textContent=this.range?`${from===to?from:from+' – '+to} · ${count} papers`:'Click a day or drag a range';
  if(this.range){this.paint(dayNumber(from)-this.start,dayNumber(to)-this.start)}else this.overlay.hidden=true;
  this.strip.querySelectorAll('[data-day]').forEach(b=>{const selected=this.range&&b.dataset.day>=from&&b.dataset.day<=to;b.setAttribute('aria-pressed',String(Boolean(selected)));b.classList.toggle('outside-selection',Boolean(this.range&&!selected))});
 }
}
function paperAuthors(p){
 const clean=name=>String(name??'').replace(/\\aff[\d,]+/g,'').trim();
 const key=name=>clean(name).normalize('NFKC').replace(/\s+/g,' ').toLowerCase();
 const names=p.authors?.length?p.authors:(p.author_affiliations||[]).map(a=>a.name);
 return [...new Set(names.map(clean).filter(Boolean))].map(name=>{
  // Match only this paper's explicit author metadata; never infer Hanzi from pinyin.
  const confirmed=(p.author_affiliations||[]).filter(a=>key(a.name)===key(name)&&a.name_zh&&/^https?:\/\//i.test(a.name_source||''));
  const chinese=[...new Set(confirmed.map(a=>clean(a.name_zh)))];
  return chinese.length===1&&chinese[0]!==name?`${chinese[0]} · ${name}`:name;
 });
}

// Render only explicit TeX spans. Source data stays untouched; all prose is escaped.
// Currency and unmatched/unsupported TeX remain readable when KaTeX is unavailable.
function abstractHTML(value){
 const text=String(value), renderer=globalThis.katex;
 const escapedAt=i=>{let n=0;while(i>0&&text[--i]==='\\')n++;return n%2===1};
 const renderMath=(tex,raw,display)=>{
  if(!renderer)return esc(raw);
  try{return `<span class="abstract-math${display?' abstract-math-display':''}">${renderer.renderToString(tex,{displayMode:display,throwOnError:true,trust:false,strict:'ignore',output:'htmlAndMathml',maxExpand:200,maxSize:20})}</span>`}
  catch{return esc(raw)}
 };
 let html='',plain='',i=0;
 const flush=()=>{html+=esc(plain);plain=''};
 while(i<text.length){
  // Common JATS publisher TeX wrappers, not arbitrary publisher HTML.
  const xml=text.slice(i).match(/^<(?:jats:)?(inline-formula|disp-formula)>\s*<(?:jats:)?tex-math>([\s\S]*?)<\/(?:jats:)?tex-math>\s*<\/(?:jats:)?\1>/);
  if(xml){let tex=xml[2].replace(/^<!\[CDATA\[([\s\S]*)\]\]>$/,'$1').trim();tex=tex.replace(/^\$\$([\s\S]*)\$\$$/,'$1').replace(/^\$([\s\S]*)\$$/,'$1');flush();html+=renderMath(tex,xml[0],xml[1]==='disp-formula');i+=xml[0].length;continue}
  let open='',close='',display=false;
  if(!escapedAt(i)){
   if(text.startsWith('$$',i)){open=close='$$';display=true}
   else if(text[i]==='$'&&!/\s/.test(text[i+1]||' ')){open=close='$'}
   else if(text.startsWith('\\(',i)){open='\\(';close='\\)'}
   else if(text.startsWith('\\[',i)){open='\\[';close='\\]';display=true}
  }
  if(open){
   let end=i+open.length;
   while((end=text.indexOf(close,end))!==-1){
    if(!escapedAt(end)&&(close!=='$'||(!/\s/.test(text[end-1])&&!/\d/.test(text[end+1]||'')&&text[end+1]!=='$')))break;
    end+=close.length;
   }
   if(end!==-1){
    const tex=text.slice(i+open.length,end),raw=text.slice(i,end+close.length);
    // Single-dollar prose across a paragraph is almost always monetary text.
    if(tex.trim()&&(open!=='$'||(!tex.includes('\n')&&!/\$/.test(tex)))){
     flush();html+=renderMath(tex,raw,display);i=end+close.length;continue;
    }
   }
  }
  plain+=text[i++];
 }
 flush();return html;
}

function paperRow(p){
 const authors=paperAuthors(p),short=authors.slice(0,3).join(', ')+(authors.length>3?', et al.':'');
 const source=(p.journals||[]).join(' / ')||p.journal||p.source;
 const year=(p.publication_date||'').slice(0,4),id=String(p.id);
 const rec=recommendations,starred=rec.mine.has(id),count=rec.count(id);
 const variants=p.variants||[];
 return `<article class="paper" data-paper="${esc(id)}"><div class="paper-line"><h3><a href="${safe(p.url)}" target="_blank" rel="noopener">${esc(p.title)} <span class="external-mark" aria-hidden="true">↗</span></a></h3><button type="button" class="recommend-button${starred?' is-recommended':''}" data-recommend="${esc(id)}" aria-pressed="${starred}" aria-label="${starred?'Remove your recommendation':'Recommend this paper'}; ${count} recommendations" title="${starred?'Remove your recommendation':'Recommend this paper to other readers'}" ${!rec.ready||rec.pending.has(id)?'disabled':''}><span aria-hidden="true">${starred?'★':'☆'}</span><span class="recommend-count">${rec.ready?count:'–'}</span></button></div><div class="paper-info"><span class="authors" title="${esc(authors.join(', '))}">${esc(short||'Authors unavailable')}</span><span class="source">${esc(source)}</span><span>${esc(year||'Year unknown')}</span><details class="abstract"><summary>Abstract</summary><div class="abstract-body"><p lang="en">${abstractHTML(p.abstract||'The source has not supplied an abstract. Open the paper to read more.')}</p><div class="abstract-provenance"><span>Published ${esc(date(p.publication_date))}</span><span>Added ${esc(date(p.first_seen))}</span>${p.version_date&&p.version_date!==p.publication_date?`<span>Version updated ${esc(date(p.version_date))}</span>`:''}</div><div class="paper-actions"><a href="${safe(p.abstract_source||p.url)}" target="_blank" rel="noopener">${p.abstract?'Abstract source':'Open paper'} ↗</a>${variants.filter(v=>v.url!==p.url).map(v=>`<a href="${safe(v.url)}" target="_blank" rel="noopener">${esc(v.journal||v.source)} ↗</a>`).join('')}${p.source==='arXiv'?`<a href="https://arxiv.org/pdf/${encodeURIComponent(p.version_id||p.id)}" target="_blank" rel="noopener">PDF ↗</a>`:''}</div></div></details></div></article>`;
}
function render(){
 const query=$('#search').value.trim().toLowerCase(),days=Number($('#period').value),source=$('#source-filter').value;
 const available=data.papers.filter(p=>(status!=='recommended'||recommendations.count(p.id)>0)&&(!days||Date.now()-Date.parse(p.first_seen)<=days*DAY_MS)&&(source==='all'||source==='linked'&&p.variants.length>1||p.source_types.includes(source)||p.variants.some(v=>'journal:'+v.journal_id===source))&&(!query||[p.title,p.abstract,...paperAuthors(p),...p.institutions,...p.tags,...p.journals].join(' ').toLowerCase().includes(query)));
 const byKeyword=p=>!keyword||keyword==='topic:all'||(keyword.startsWith('topic:')?p.topics.includes(keyword.slice(6)):(p.tags||[]).includes(keyword));
 timeline.setPapers(available.filter(byKeyword));
 const base=available.filter(p=>timeline.matches(p));
 const filtered=base.filter(byKeyword).sort((a,b)=>(sortOrder==='recommended'?recommendations.count(b.id)-recommendations.count(a.id):sortOrder==='relevance'?Number(b.fit_score||0)-Number(a.fit_score||0):0)||String(b.first_seen||'').localeCompare(a.first_seen||'')||String(b.publication_date||'').localeCompare(a.publication_date||''));
 const tagRow=item=>{const key=item.topic?'topic:'+item.id:item.label;const count=item.topic&&item.id==='all'?base.length:base.filter(p=>item.topic?p.topics.includes(item.id):(p.tags||[]).includes(item.label)).length;return `<button type="button" data-keyword="${esc(key)}" aria-pressed="${keyword===key}" class="${keyword===key?'active':''}"><span>${esc(item.name_en||item.name)}</span><span>${count}</span></button>`};
 $('#research-tags').innerHTML=allTags.filter(t=>t.topic).map(tagRow).join('');
 $('#content-tags').innerHTML=allTags.filter(t=>!t.topic).map(tagRow).join('');
 $('#keyword-filter').hidden=!keyword||keyword==='topic:all';
 const selected=allTags.find(t=>(t.topic?'topic:'+t.id:t.label)===keyword);
 $('#keyword-label').textContent=selected?.name_en||selected?.name||keyword;
 $('#count').textContent=String(filtered.length);
 $('#papers').innerHTML=filtered.slice(0,limit).map(paperRow).join('')||`<div class="empty">${status==='recommended'&&!recommendations.ready?'Recommendations are temporarily unavailable.':'No papers match these filters.'}</div>`;
 $('#more').hidden=filtered.length<=limit;
}
async function init(){try{
 const response=await fetch('./catalog.json',{cache:'no-store'});if(!response.ok)throw Error();data=await response.json();
 recommendations=new PaperRecommendations(window.PLANET_FLUID_STATS_ENDPOINT);
 timeline=new PublicationTimeline($('#publication-timeline'),data.papers,()=>{limit=30;render()});
 allTags=[{id:'all',name_en:'All topics',topic:true},...data.topics.filter(t=>!data.topic_filter_ids||data.topic_filter_ids.includes(t.id)).map(t=>({...t,topic:true})),...([...new Set(data.papers.flatMap(p=>p.tags||[]))].map(label=>({label,name_en:englishTag(label)})).sort((a,b)=>a.name_en.localeCompare(b.name_en)))];
 const pickKeyword=e=>{const b=e.target.closest('button[data-keyword]');if(!b)return;keyword=keyword===b.dataset.keyword?'topic:all':b.dataset.keyword;limit=30;render()};
 $('#research-tags').addEventListener('click',pickKeyword);$('#content-tags').addEventListener('click',pickKeyword);
 $('#papers').addEventListener('click',async e=>{
  const button=e.target.closest('[data-recommend]');if(!button||button.disabled)return;
  const id=button.dataset.recommend;button.disabled=true;$('#recommendation-notice').textContent='';
  try{await recommendations.toggle(id);render()}catch(error){$('#recommendation-notice').textContent=error.message;button.disabled=false}
 });
 $('#clear-keyword').addEventListener('click',()=>{keyword='topic:all';limit=30;render()});
 $('.segments').addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;status=b.dataset.status;$('.segments .active')?.classList.remove('active');b.classList.add('active');limit=30;render()});
 for(const j of data.journals.journals.filter(j=>j.enabled!==false)){const opt=document.createElement('option');opt.value='journal:'+j.id;opt.textContent=j.name;$('#source-filter').append(opt)}
 if(data.sources['exoplanet.eu']){const opt=document.createElement('option');opt.value='exoplanet.eu';opt.textContent='Exoplanet.eu';$('#source-filter').append(opt)}
 const requestedJournal=new URLSearchParams(location.search).get('journal');if(data.journals.journals.some(j=>j.enabled!==false&&j.id===requestedJournal))$('#source-filter').value='journal:'+requestedJournal;
 const inactive=new Set(data.journals.journals.filter(j=>j.enabled===false).map(j=>'journal:'+j.id));const entries=Object.entries(data.sources).filter(([k])=>!inactive.has(k)).map(([,v])=>v),success=entries.map(s=>s.last_rss_success||s.last_success).filter(Boolean).sort();
 $('#updated').textContent=success.length?`Last successful fetch: ${new Date(success.at(-1)).toLocaleString('en-GB',{timeZone:'Asia/Shanghai'})} (Beijing)`:'No successful fetch yet';
 const failed=entries.filter(s=>s.status!=='ok').length;
 $('#notice').textContent=failed?`${failed} sources need attention; existing papers are retained. See source status.`:'';
 $('#search').addEventListener('input',()=>{limit=30;render()});for(const id of ['period','source-filter'])$('#'+id).addEventListener('change',()=>{limit=30;render()});$('#sort-order').addEventListener('change',e=>{sortOrder=e.target.value;limit=30;render()});$('#more').onclick=()=>{limit+=30;render()};render();
 recommendations.load().then(()=>render()).catch(()=>{$('#recommendation-notice').innerHTML='Shared recommendations are temporarily unavailable. <button type="button" id="retry-recommendations">Retry</button>';$('#retry-recommendations').onclick=async()=>{try{await recommendations.load();$('#recommendation-notice').textContent='';render()}catch(_){}}});
 }catch(e){$('#updated').textContent='Data could not be loaded';$('#papers').innerHTML='<div class="empty">Unable to load the literature index. Please refresh later.<br>This does not mean there are no new papers.</div>'}}
init();
