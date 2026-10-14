let data,status='candidate',limit=30,keyword='topic:all',allTags=[],sortOrder='recent',timeline;
const $=s=>document.querySelector(s);
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const safe=s=>/^https?:\/\//i.test(s||'')?esc(s):'#';
const tagParts=s=>{const parts=String(s??'').split(' · ');return [parts.shift()||'',parts.join(' · ')];};
const authorText=a=>[a.name_zh,a.name.replace(/\\aff[\d,]+/g,'')].filter(Boolean).join(' · ');
const orcidLink=a=>/^https:\/\/orcid\.org\/\d{4}-\d{4}-\d{4}-\d{3}[\dX]$/.test(a.orcid||'')?` <a href="${a.orcid}" target="_blank" rel="noopener" aria-label="${esc(a.name)} 的 ORCID">ORCID ↗</a>`:'';
const date=s=>!s?'待核实':/^\d{4}(-\d{2})?$/.test(s)?s.replace('-','/')+'（日期精度有限）':new Date(s).toLocaleDateString('zh-CN',{year:'numeric',month:'2-digit',day:'2-digit',timeZone:'Asia/Shanghai'});
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
  root.innerHTML=`<div class="timeline-heading"><div><h2>发表时间 <small lang="en">Publication timeline</small></h2><p>点击一天，或拖选日期范围</p></div><div class="timeline-views" aria-label="时间条显示范围"><button type="button" data-window="30">30 天</button><button type="button" data-window="90">90 天</button><button type="button" data-window="365">一年</button></div></div><div class="timeline-navigation"><button type="button" data-pan="-1" aria-label="查看更早日期">←</button><span id="timeline-window"></span><button type="button" data-pan="1" aria-label="查看更近日期">→</button><button type="button" id="timeline-latest">近两天</button><button type="button" id="timeline-reset">全部日期</button></div><div class="timeline-plot"><div id="timeline-tooltip" class="timeline-tooltip" hidden></div><div id="timeline-days" class="timeline-days" aria-label="每日文献量热度条"></div><div id="timeline-selection" class="timeline-selection" hidden></div></div><div id="timeline-axis" class="timeline-axis" aria-hidden="true"></div><div class="timeline-bottom"><div class="timeline-dates"><label>起始 <input id="publication-from" type="date" aria-label="发表起始日期"></label><span>—</span><label>结束 <input id="publication-to" type="date" aria-label="发表结束日期"></label><span id="timeline-summary" role="status"></span></div><div class="timeline-legend" aria-label="颜色越深表示当天发表的文献越多"><span>篇/天</span>${['0','1','2–3','4–7','8+'].map((label,i)=>`<span><i class="heat-${i}"></i>${label}</span>`).join('')}</div></div><p id="timeline-note" class="timeline-note"></p>`;
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
  this.strip.innerHTML=Array.from({length:this.days},(_,i)=>{const day=dayString(this.start+i),count=this.counts.get(day)||0;return `<button type="button" class="timeline-day heat-${heatLevel(count)}" data-day="${day}" aria-label="${day}，${count} 篇" aria-pressed="false"><span>${count||''}</span></button>`}).join('');
  const step=this.days<=30?7:this.days<=90?14:60;
  const ticks=[0,...Array.from({length:Math.floor((this.days-1)/step)},(_,i)=>(i+1)*step).filter(i=>i<this.days-1-step/2),this.days-1];
  this.root.querySelector('#timeline-axis').innerHTML=ticks.map(i=>`<span style="left:${(i+.5)/this.days*100}%">${dayString(this.start+i).slice(5).replace('-','/')}</span>`).join('');
  this.root.querySelector('#timeline-note').textContent='按当前来源、标签及搜索条件统计本站文献的首次发表日（含 arXiv 首发）'+(this.undated?`；${this.undated} 篇仅有年月或日期待核实。`:'。');
  this.drawSelection();if(focused)this.strip.querySelector(`[data-day="${focused}"]`)?.focus({preventScroll:true});
 }
 showTooltip(index){
  const day=dayString(this.start+index);this.tooltip.textContent=day.replaceAll('-','/')+' · '+(this.counts.get(day)||0)+' 篇';
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
  this.root.querySelector('#timeline-summary').textContent=this.range?`${from===to?'已选一天':'已选日期范围'} · ${count} 篇`:'全部发表日期';
  if(this.range){this.paint(dayNumber(from)-this.start,dayNumber(to)-this.start)}else this.overlay.hidden=true;
  this.strip.querySelectorAll('[data-day]').forEach(b=>{const selected=this.range&&b.dataset.day>=from&&b.dataset.day<=to;b.setAttribute('aria-pressed',String(Boolean(selected)));b.classList.toggle('outside-selection',Boolean(this.range&&!selected))});
 }
}
function render(){
 const query=$('#search').value.trim().toLowerCase(),days=Number($('#period').value),source=$('#source-filter').value;
 const available=data.papers.filter(p=>(status==='all'||p.status===status)&&(!days||Date.now()-Date.parse(p.first_seen)<=days*86400000)&&(source==='all'||source==='linked'&&p.variants.length>1||p.source_types.includes(source)||p.variants.some(v=>'journal:'+v.journal_id===source))&&(!query||[p.title,p.abstract,...p.authors,...(p.author_affiliations||[]).map(a=>a.name_zh||''),p.reason,p.intro_zh,p.intro_en,...p.institutions,...p.tags,...p.journals].join(' ').toLowerCase().includes(query)));
 const byKeyword=p=>!keyword||keyword==='topic:all'||(keyword.startsWith('topic:')?p.topics.includes(keyword.slice(6)):(p.tags||[]).includes(keyword));
 timeline.setPapers(available.filter(byKeyword));
 const base=available.filter(p=>timeline.matches(p));
 const filtered=base.filter(byKeyword).sort((a,b)=>(sortOrder==='relevance'?Number(b.fit_score||0)-Number(a.fit_score||0):0)||String(b.first_seen||'').localeCompare(a.first_seen||'')||String(b.publication_date||'').localeCompare(a.publication_date||''));
 $('#research-tags').innerHTML=allTags.map(item=>{const key=item.topic?'topic:'+item.id:item.label;const count=item.topic&&item.id==='all'?base.length:base.filter(p=>item.topic?p.topics.includes(item.id):(p.tags||[]).includes(item.label)).length;return `<button type="button" data-keyword="${esc(key)}" aria-pressed="${keyword===key}" class="${keyword===key?'active':''}"><span>${esc(item.name)}<small lang="en">${esc(item.name_en||'')}</small></span><span>${count}</span></button>`}).join('');
 $('#keyword-filter').hidden=!keyword||keyword==='topic:all';
 $('#keyword-label').textContent=keyword?(allTags.find(t=>(t.topic?'topic:'+t.id:t.label)===keyword)?.name||keyword):'';
 $('#count').textContent=`${filtered.length} 篇`;
 $('#papers').innerHTML=filtered.slice(0,limit).map(p=>{
 const mapped=p.author_affiliations||[],authors=[...new Set(mapped.length?mapped.map(authorText):p.authors)],orgs=p.institutions||[],variants=p.variants||[];
 const sourceLabel=p.source==='arXiv'?'arXiv':p.journal;
 const dates=variants.map(v=>`<span>${v.source==='arXiv'?'arXiv 首次发布':'期刊发布'} ${esc(date(v.publication_date))}</span>`).join('');
 const topicTags=p.topics.map(id=>{const t=data.topics.find(x=>x.id===id);return `<span class="tag"><span class="tag-zh">${esc(t?.name||id)}</span>${t?.name_en?`<small class="tag-en" lang="en">${esc(t.name_en)}</small>`:''}</span>`}).join('');
 const contentTags=(p.tags||[]).map(t=>{const [zh,en]=tagParts(t);return `<button type="button" class="tag mechanism" data-keyword="${esc(t)}" aria-pressed="${keyword===t}" title="点击筛选该标签"><span class="tag-zh">${esc(zh)}</span>${en?`<small class="tag-en" lang="en">${esc(en)}</small>`:''}</button>`}).join('');
 return `<article class="paper"><div class="paper-meta"><span class="source">${esc(sourceLabel)}${p.variants.length>1?' · 已关联期刊/预印本':''}</span>${p.intake_kind==='one_year_fallback'?'<span>近一年高相关补充</span>':''}<span>网站收录 ${esc(date(p.first_seen))}</span>${dates}${p.version_date&&!p.version_id.endsWith('v1')?`<span>版本更新 ${esc(date(p.version_date))}</span>`:''}<span class="fit-score">组内方向相关度 ${Number(p.fit_score||0)}/100</span></div><h3><a href="${safe(p.url)}" target="_blank" rel="noopener">${esc(p.title)} ↗</a></h3><div class="authors">${esc(authors.slice(0,6).join(' · '))}${authors.length>6?' 等':''}</div><div class="institutions">${orgs.length?esc(orgs.slice(0,2).join(' · '))+(orgs.length>2?' …':''):'机构信息暂未获取'}</div><div class="tags">${topicTags}${contentTags}</div>${p.fit_matches?.length?`<div class="fit-explanation">相关主题：${esc(p.fit_matches.join(' · '))}</div>`:''}<div class="intro"><p lang="zh-CN">${esc(p.intro_zh||'中文导读待整理')}</p>${p.intro_en?`<p lang="en">${esc(p.intro_en)}</p>`:''}<small>${esc(p.intro_basis||'')} ${p.metadata_limited?'· 自动初筛仅使用元数据标题':'· 导读供阅读参考'}${p.intro_source?` · <a href="${safe(p.intro_source)}" target="_blank" rel="noopener">导读依据 ↗</a>`:''}</small></div><div class="reason">${esc(p.reason)}</div><details><summary>原文摘要</summary><p>${esc(p.abstract||'来源未提供摘要，请访问论文页面。')}</p></details><details><summary>作者、机构与来源</summary>${mapped.length?mapped.map(a=>`<p><b>${esc(authorText(a))}</b>${orcidLink(a)}${a.name_zh&&a.name_source&&a.name_source!==a.orcid?` <a href="${safe(a.name_source)}" target="_blank" rel="noopener">姓名来源 ↗</a>`:''}<br>${esc(a.institutions.join('；')||'未获取该作者的机构对应关系')}</p>`).join(''):`<p>${esc(authors.join(' · '))}</p>`}${orgs.length?`<p>文中列示机构：${esc(orgs.join('；'))}</p>`:'<p>机构信息暂未获取。</p>'}${variants.map(v=>`<p><a href="${safe(v.affiliation_source||v.metadata_source||v.url)}" target="_blank" rel="noopener">${esc(v.journal||'arXiv')} · 元数据与机构来源 ↗</a><br>此来源收录 ${esc(date(v.first_seen))} · ${esc(v.doi||v.version_id)}</p>`).join('')}${p.match_basis.length?`<p>版本关联依据：${esc(p.match_basis.join('；'))}</p>`:''}</details><div class="paper-actions">${variants.map(v=>`<a href="${safe(v.url)}" target="_blank" rel="noopener">${esc(v.journal||'arXiv 原文')} ↗</a>`).join('')}${p.source==='arXiv'?`<a href="https://arxiv.org/pdf/${encodeURIComponent(p.version_id)}" target="_blank" rel="noopener">PDF ↗</a>`:''}<a href="network.html">机构网络 ↗</a></div></article>`;
 }).join('')||'<div class="empty">当前条件下没有文献。<br>可切换方向、来源，清除扩展关键词或搜索。</div>';
 $('#more').hidden=filtered.length<=limit;
}
async function init(){try{
 const response=await fetch('./catalog.json',{cache:'no-store'});if(!response.ok)throw Error();data=await response.json();
 timeline=new PublicationTimeline($('#publication-timeline'),data.papers,()=>{limit=30;render()});
 allTags=[{id:'all',name:'全部标签',name_en:'All tags',topic:true},...data.topics.filter(t=>!data.topic_filter_ids||data.topic_filter_ids.includes(t.id)).map(t=>({...t,topic:true})),...([...new Set(data.papers.flatMap(p=>p.tags||[]))].sort().map(label=>({label,name:label.split(' · ')[0],name_en:label.split(' · ').slice(1).join(' · ')})))];
 const pickKeyword=e=>{const b=e.target.closest('button[data-keyword]');if(!b)return;keyword=keyword===b.dataset.keyword?'topic:all':b.dataset.keyword;limit=30;render()};
 $('#research-tags').addEventListener('click',pickKeyword);$('#papers').addEventListener('click',pickKeyword);
 $('#clear-keyword').addEventListener('click',()=>{keyword='topic:all';limit=30;render()});
 $('.segments').addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;status=b.dataset.status;$('.segments .active')?.classList.remove('active');b.classList.add('active');limit=30;render()});
 for(const j of data.journals.journals.filter(j=>j.enabled!==false)){const opt=document.createElement('option');opt.value='journal:'+j.id;opt.textContent=j.name;$('#source-filter').append(opt)}
 if(data.sources['exoplanet.eu']){const opt=document.createElement('option');opt.value='exoplanet.eu';opt.textContent='Exoplanet.eu';$('#source-filter').append(opt)}
 const requestedJournal=new URLSearchParams(location.search).get('journal');if(data.journals.journals.some(j=>j.enabled!==false&&j.id===requestedJournal))$('#source-filter').value='journal:'+requestedJournal;
 const inactiveJournalKeys=new Set(data.journals.journals.filter(j=>j.enabled===false).map(j=>'journal:'+j.id));const entries=Object.entries(data.sources).filter(([k])=>!inactiveJournalKeys.has(k)).map(([,v])=>v),success=entries.map(s=>s.last_rss_success||s.last_success).filter(Boolean).sort();
 $('#updated').textContent=success.length?`最近成功抓取 ${new Date(success.at(-1)).toLocaleString('zh-CN',{timeZone:'Asia/Shanghai'})} · 北京时间`:'尚未完成首次抓取';
 const failed=entries.filter(s=>s.status!=='ok').length;
 $('#notice').textContent=failed?`${failed} 个来源有补抓或连接问题，已保留历史文献；详情见文献来源页。`:'';
 if(/^https:\/\/github\.com\/[\w.-]+\/[\w.-]+$/.test(data.repository)){$('#admin').href=data.repository+'/edit/main/topics.json';$('#admin').hidden=false}
 $('#search').addEventListener('input',()=>{limit=30;render()});for(const id of ['period','source-filter'])$('#'+id).addEventListener('change',()=>{limit=30;render()});$('#sort-order').addEventListener('change',e=>{sortOrder=e.target.value;limit=30;render()});$('#more').onclick=()=>{limit+=30;render()};render();
 }catch(e){$('#updated').textContent='数据加载失败';$('#papers').innerHTML='<div class="empty">无法读取文献索引，请稍后刷新。<br>这不代表没有新文献。</div>'}}
init();
