let data, topic='all', status='candidate', limit=30;
const $=s=>document.querySelector(s);
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const date=s=>s?new Date(s).toLocaleDateString('zh-CN',{year:'numeric',month:'2-digit',day:'2-digit',timeZone:'Asia/Shanghai'}):'未记录';
function render(){
 const query=$('#search').value.trim().toLowerCase(), days=Number($('#period').value);
 const filtered=data.papers.filter(p=>(topic==='all'||p.topics.includes(topic))&&(status==='all'||p.status===status)&&(!days||Date.now()-Date.parse(p.first_seen)<=days*86400000)&&(!query||[p.title,p.abstract,...p.authors,p.reason,p.intro_zh,p.intro_en,...(p.institutions||[]),...(p.tags||[])].join(' ').toLowerCase().includes(query))).sort((a,b)=>date(b.first_seen).localeCompare(date(a.first_seen))||Number(b.topics.some(t=>['planetary','physics','dynamics'].includes(t)))-Number(a.topics.some(t=>['planetary','physics','dynamics'].includes(t)))||String(b.publication_date||b.published).localeCompare(a.publication_date||a.published));
 $('#count').textContent=`${filtered.length} 篇`;
 $('#papers').innerHTML=filtered.slice(0,limit).map(p=>{
 const mapped=p.author_affiliations||[], authors=mapped.length?mapped.map(a=>a.name.replace(/\\aff[\d,]+/g,'')):p.authors, orgs=p.institutions||[];
 return `<article class="paper"><div class="paper-meta"><span class="source">arXiv</span><span>网站收录 ${esc(date(p.first_seen))}</span><span>首次发布 ${p.publication_date?esc(date(p.publication_date)):'待核实'}</span>${p.version_date&&!p.version_id.endsWith('v1')?`<span>版本更新 ${esc(date(p.version_date))}</span>`:''}<span>${esc(p.version_id)}</span></div><h3><a href="https://arxiv.org/abs/${encodeURIComponent(p.id)}" target="_blank" rel="noopener">${esc(p.title)} ↗</a></h3><div class="authors">${esc(authors.slice(0,6).join(' · '))}${authors.length>6?' 等':''}</div><div class="institutions">${orgs.length?esc(orgs.slice(0,2).join(' · '))+(orgs.length>2?` 等 ${orgs.length} 个机构`:''):'机构信息暂未获取'}</div><div class="tags">${p.topics.map(id=>`<span class="tag">${esc(data.topics.find(t=>t.id===id)?.name||id)}</span>`).join('')}${(p.tags||[]).map(t=>`<span class="tag mechanism">${esc(t)}</span>`).join('')}</div><div class="intro"><p lang="zh-CN">${esc(p.intro_zh||'中文导读待整理')}</p><p lang="en">${esc(p.intro_en||'')}</p><small>${esc(p.intro_basis||'')} · 导读供阅读参考</small></div><div class="reason">${esc(p.reason)}</div><details><summary>展开原文摘要</summary><p>${esc(p.abstract||'来源未提供摘要')}</p></details><details><summary>作者与机构${orgs.length?' · '+orgs.length+' 个机构':''}</summary>${mapped.length?mapped.map(a=>`<p><b>${esc(a.name)}</b><br>${esc(a.institutions.join('；')||'未获取该作者的机构对应关系')}</p>`).join(''):`<p>${esc(authors.join(' · '))}</p>`}${orgs.length?`<p>文中列示机构：${esc(orgs.join('；'))}</p><a href="https://arxiv.org/html/${encodeURIComponent(p.version_id)}" target="_blank" rel="noopener">机构来源：论文 HTML ↗</a>`:'<p>来源未提供可解析的机构信息，请查阅原文。</p>'}</details><div class="paper-actions"><a href="https://arxiv.org/abs/${encodeURIComponent(p.id)}" target="_blank" rel="noopener">原文页面 ↗</a><a href="https://arxiv.org/pdf/${encodeURIComponent(p.version_id)}" target="_blank" rel="noopener">PDF ↗</a></div></article>`;
 }).join('')||'<div class="empty">当前条件下没有文献。<br>可以切换方向、清空搜索，或查看全部文献。</div>';
 $('#more').hidden=filtered.length<=limit;
}
async function init(){try{
 const response=await fetch('./papers.json');if(!response.ok)throw Error('fetch');data=await response.json();
 $('#topics').innerHTML=[{id:'all',name:'全部方向'},...data.topics].map(t=>`<button data-topic="${esc(t.id)}" class="${t.id==='all'?'active':''}">${esc(t.name)}<span>${data.papers.filter(p=>t.id==='all'||p.topics.includes(t.id)).length}</span></button>`).join('');
 $('#topics').addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;topic=b.dataset.topic;$('#topics .active')?.classList.remove('active');b.classList.add('active');limit=30;render()});
 $('.segments').addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;status=b.dataset.status;$('.segments .active')?.classList.remove('active');b.classList.add('active');limit=30;render()});
 const entries=Object.entries(data.sources), success=entries.map(([,s])=>(s.last_rss_success||s.last_success)).filter(Boolean).sort();
 $('#updated').textContent=success.length?`最近成功抓取 ${new Date(success.at(-1)).toLocaleString('zh-CN')}`:'尚未完成首次抓取';
 $('#sources').innerHTML=entries.map(([k,s])=>`<div>${esc(k)} · ${s.status==='ok'?'正常':s.status==='partial'?'RSS 已更新；历史补抓待恢复':'抓取失败，保留历史记录'} · 上次成功：${esc((s.last_rss_success||s.last_success)?new Date(s.last_rss_success||s.last_success).toLocaleString('zh-CN'):'暂无')}</div>`).join('')||'尚未接入数据';
 if(entries.some(([,s])=>s.status!=='ok'))$('#notice').textContent='部分来源正在使用 RSS 补充或抓取失败，历史回查未完成；详见数据源状态。';
 else if(success.length&&Date.now()-Date.parse(success[0])>48*3600000)$('#notice').textContent='部分来源超过 48 小时未更新，请管理员检查自动任务。';
 if(/^https:\/\/github\.com\/[\w.-]+\/[\w.-]+$/.test(data.repository)){$('#admin').href=data.repository+'/edit/main/topics.json';$('#admin').hidden=false}
 $('#search').addEventListener('input',()=>{limit=30;render()});$('#period').addEventListener('change',()=>{limit=30;render()});$('#more').onclick=()=>{limit+=30;render()};
 $('#source-toggle').onclick=()=>{$('#sources').hidden=!$('#sources').hidden;$('#source-toggle').setAttribute('aria-expanded',String(!$('#sources').hidden))};render();
 }catch(e){$('#updated').textContent='数据加载失败';$('#papers').innerHTML='<div class="empty">无法读取文献数据，请稍后刷新。<br>这不代表今天没有新文献。</div>'}}
init();
