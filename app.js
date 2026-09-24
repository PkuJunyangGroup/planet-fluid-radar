let data,topic='all',status='candidate',limit=30;
const $=s=>document.querySelector(s);
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const safe=s=>/^https?:\/\//i.test(s||'')?esc(s):'#';
const date=s=>!s?'待核实':/^\d{4}(-\d{2})?$/.test(s)?s.replace('-','/')+'（日期精度有限）':new Date(s).toLocaleDateString('zh-CN',{year:'numeric',month:'2-digit',day:'2-digit',timeZone:'Asia/Shanghai'});
function render(){
 const query=$('#search').value.trim().toLowerCase(),days=Number($('#period').value),source=$('#source-filter').value;
 const filtered=data.papers.filter(p=>(topic==='all'||p.topics.includes(topic))&&(status==='all'||p.status===status)&&(!days||Date.now()-Date.parse(p.first_seen)<=days*86400000)&&(source==='all'||source==='linked'&&p.variants.length>1||p.source_types.includes(source)||p.variants.some(v=>'journal:'+v.journal_id===source))&&(!query||[p.title,p.abstract,...p.authors,p.reason,p.intro_zh,p.intro_en,...p.institutions,...p.tags,...p.journals].join(' ').toLowerCase().includes(query))).sort((a,b)=>date(b.first_seen).localeCompare(date(a.first_seen))||Number(b.topics.some(t=>['planetary','physics','dynamics'].includes(t)))-Number(a.topics.some(t=>['planetary','physics','dynamics'].includes(t)))||String(b.publication_date||'').localeCompare(a.publication_date||''));
 $('#count').textContent=`${filtered.length} 篇`;
 $('#papers').innerHTML=filtered.slice(0,limit).map(p=>{
 const mapped=p.author_affiliations||[],authors=[...new Set(mapped.length?mapped.map(a=>a.name.replace(/\\aff[\d,]+/g,'')):p.authors)],orgs=p.institutions||[],variants=p.variants||[];
 const sourceLabel=p.source==='arXiv'?'arXiv':p.journal;
 const dates=variants.map(v=>`<span>${v.source==='arXiv'?'arXiv 首次发布':'期刊发布'} ${esc(date(v.publication_date))}</span>`).join('');
 return `<article class="paper"><div class="paper-meta"><span class="source">${esc(sourceLabel)}${p.variants.length>1?' · 已关联期刊/预印本':''}</span><span>网站收录 ${esc(date(p.first_seen))}</span>${dates}${p.version_date&&!p.version_id.endsWith('v1')?`<span>版本更新 ${esc(date(p.version_date))}</span>`:''}</div><h3><a href="${safe(p.url)}" target="_blank" rel="noopener">${esc(p.title)} ↗</a></h3><div class="authors">${esc(authors.slice(0,6).join(' · '))}${authors.length>6?' 等':''}</div><div class="institutions">${orgs.length?esc(orgs.slice(0,2).join(' · '))+(orgs.length>2?' …':''):'机构信息暂未获取'}</div><div class="tags">${p.topics.map(id=>`<span class="tag">${esc(data.topics.find(t=>t.id===id)?.name||id)}</span>`).join('')}${(p.tags||[]).map(t=>`<span class="tag mechanism">${esc(t)}</span>`).join('')}</div><div class="intro"><p lang="zh-CN">${esc(p.intro_zh||'中文导读待整理')}</p>${p.intro_en?`<p lang="en">${esc(p.intro_en)}</p>`:''}<small>${esc(p.intro_basis||'')} ${p.metadata_limited?'· 自动初筛仅使用元数据标题':'· 导读供阅读参考'}${p.intro_source?` · <a href="${safe(p.intro_source)}" target="_blank" rel="noopener">导读依据 ↗</a>`:''}</small></div><div class="reason">${esc(p.reason)}</div><details><summary>原文摘要</summary><p>${esc(p.abstract||'来源未提供摘要，请访问论文页面。')}</p></details><details><summary>作者、机构与来源</summary>${mapped.length?mapped.map(a=>`<p><b>${esc(a.name.replace(/\\aff[\d,]+/g,''))}</b><br>${esc(a.institutions.join('；')||'未获取该作者的机构对应关系')}</p>`).join(''):`<p>${esc(authors.join(' · '))}</p>`}${orgs.length?`<p>文中列示机构：${esc(orgs.join('；'))}</p>`:'<p>机构信息暂未获取。</p>'}${variants.map(v=>`<p><a href="${safe(v.affiliation_source||v.metadata_source||v.url)}" target="_blank" rel="noopener">${esc(v.journal||'arXiv')} · 元数据与机构来源 ↗</a><br>此来源收录 ${esc(date(v.first_seen))} · ${esc(v.doi||v.version_id)}</p>`).join('')}${p.match_basis.length?`<p>版本关联依据：${esc(p.match_basis.join('；'))}</p>`:''}</details><div class="paper-actions">${variants.map(v=>`<a href="${safe(v.url)}" target="_blank" rel="noopener">${esc(v.journal||'arXiv 原文')} ↗</a>`).join('')}${p.source==='arXiv'?`<a href="https://arxiv.org/pdf/${encodeURIComponent(p.version_id)}" target="_blank" rel="noopener">PDF ↗</a>`:''}<a href="network.html">机构网络 ↗</a></div></article>`;
 }).join('')||'<div class="empty">当前条件下没有文献。<br>可切换方向、来源或清空搜索。</div>';
 $('#more').hidden=filtered.length<=limit;
}
async function init(){try{
 const response=await fetch('./catalog.json');if(!response.ok)throw Error();data=await response.json();
 $('#topics').innerHTML=[{id:'all',name:'全部方向'},...data.topics].map(t=>`<button data-topic="${esc(t.id)}" class="${t.id==='all'?'active':''}">${esc(t.name)}<span>${data.papers.filter(p=>t.id==='all'||p.topics.includes(t.id)).length}</span></button>`).join('');
 $('#topics').addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;topic=b.dataset.topic;$('#topics .active')?.classList.remove('active');b.classList.add('active');limit=30;render()});
 $('.segments').addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;status=b.dataset.status;$('.segments .active')?.classList.remove('active');b.classList.add('active');limit=30;render()});
 for(const j of data.journals.journals){const opt=document.createElement('option');opt.value='journal:'+j.id;opt.textContent=j.name;$('#source-filter').append(opt)}
 const entries=Object.values(data.sources),success=entries.map(s=>s.last_rss_success||s.last_success).filter(Boolean).sort();
 $('#updated').textContent=success.length?`最近成功抓取 ${new Date(success.at(-1)).toLocaleString('zh-CN',{timeZone:'Asia/Shanghai'})} · 北京时间`:'尚未完成首次抓取';
 const failed=entries.filter(s=>s.status!=='ok').length;
 $('#notice').textContent=failed?`${failed} 个来源有补抓或连接问题，已保留历史文献；详情见文献来源页。`:'';
 if(/^https:\/\/github\.com\/[\w.-]+\/[\w.-]+$/.test(data.repository)){$('#admin').href=data.repository+'/edit/main/topics.json';$('#admin').hidden=false}
 $('#search').addEventListener('input',()=>{limit=30;render()});for(const id of ['period','source-filter'])$('#'+id).addEventListener('change',()=>{limit=30;render()});$('#more').onclick=()=>{limit+=30;render()};render();
 }catch(e){$('#updated').textContent='数据加载失败';$('#papers').innerHTML='<div class="empty">无法读取文献索引，请稍后刷新。<br>这不代表没有新文献。</div>'}}
init();
