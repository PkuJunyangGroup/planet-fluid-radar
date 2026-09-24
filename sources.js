(async()=>{
 const $=s=>document.querySelector(s),el=$('#source-status');
 const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const when=s=>s?new Date(s).toLocaleString('zh-CN',{timeZone:'Asia/Shanghai'}):'尚无成功记录';
 try{
 const r=await fetch('./catalog.json');if(!r.ok)throw Error();const d=await r.json();
 if(el){el.replaceChildren();for(const [name,s]of Object.entries(d.sources).filter(([k])=>!k.startsWith('journal:'))){const p=document.createElement('p');p.textContent=name+' · '+(s.status==='ok'?'正常':s.status==='partial'?'RSS 已更新，API 历史补抓待恢复':'抓取失败，保留历史记录')+' · 最近成功：'+when(s.last_rss_success||s.last_success);el.append(p)}
 $('#journal-directory').innerHTML=Object.entries(d.journals.groups).map(([id,label])=>`<section class="source-group"><h3>${esc(label)}</h3><table><thead><tr><th>期刊</th><th>接入状态与累计收录</th></tr></thead><tbody>${d.journals.journals.filter(j=>j.group===id).map(j=>{const s=d.sources['journal:'+j.id],total=d.papers.filter(p=>p.variants.some(v=>v.journal_id===j.id)).length;return `<tr><td><a href="${esc(j.url)}" target="_blank" rel="noopener">${esc(j.name)} ↗</a><span class="source-state">ISSN ${esc(j.issn)}</span><a href="./?journal=${encodeURIComponent(j.id)}">本站已收录 ${total} 篇 →</a></td><td>${!s?'待首次抓取':s.status==='ok'?`接口正常 · 本次检索 ${s.fetched} 条 / 保留 ${s.retained} 条`:'抓取失败 · 保留历史数据'}${s?.fetched===0?' · 本次检索为空，不代表期刊没有新文章':''}<span class="source-state">最近成功 ${esc(when(s?.last_success))}${s?.coverage_since?' · 起始检索 '+esc(s.coverage_since):''}</span></td></tr>`}).join('')}</tbody></table></section>`).join('');}
 if(!$('#statistics'))return;
 const journals=d.journals.journals,monthly=d.monthly_statistics||{},now=new Date(),months=[];
 const parts=new Intl.DateTimeFormat('en-US',{timeZone:'Asia/Shanghai',year:'numeric',month:'numeric'}).formatToParts(now),year=+parts.find(p=>p.type==='year').value,month=+parts.find(p=>p.type==='month').value;
 for(let i=5;i>=0;i--){const t=new Date(Date.UTC(year,month-1-i,1));months.push(t.toISOString().slice(0,7))}
 $('#stats-journal').innerHTML+=journals.map(j=>`<option value="${esc(j.id)}">${esc(j.name)}</option>`).join('');
 function siteCounts(j){const sets=Object.fromEntries(months.map(m=>[m,new Set()]));for(const p of d.papers){if(p.status!=='candidate')continue;for(const v of p.variants){if(v.journal_id!==j.id)continue;const value=$('#stats-date').value==='added'?(v.first_seen?new Date(v.first_seen).toLocaleDateString('sv-SE',{timeZone:'Asia/Shanghai'}):''):(v.publication_date||''),m=value.slice(0,7);if(sets[m])sets[m].add(v.doi?.toLowerCase()||v.id)}}return months.map(m=>sets[m].size)}
 function series(j){return $('#stats-metric').value==='selected'?siteCounts(j):months.map(m=>{const x=monthly[j.id]?.[m];return x?.status==='ok'?x.count:null})}
 function draw(){const selected=$('#stats-metric').value==='selected',id=$('#stats-journal').value,rows=journals.map(j=>({j,values:series(j)})),chosen=rows.filter(r=>id==='all'||r.j.id===id),values=months.map((m,i)=>chosen.some(r=>r.values[i]===null)?null:chosen.reduce((s,r)=>s+r.values[i],0)),max=Math.max(1,...values.filter(v=>v!==null));
 $('#stats-date-label').hidden=!selected;
 const checks=chosen.flatMap(r=>months.map(m=>monthly[r.j.id]?.[m]?.checked_at)).filter(Boolean).sort();
 $('#stats-note').textContent=selected?'统计本站已收录且匹配研究方向的期刊文献，按 DOI 去重；可切换发表月份与收录月份。历史回溯范围不一，0 仅表示本站暂无相关记录，不代表期刊实际发表量为零。当月尚未结束。':'统计 Crossref 以 journal-article 登记的记录，按其出版日期落入月份检索；包含研究论文、评论等，可能与出版社分期目录不同，未限定本站方向，也不代表完整实际发表量。当月截至最近查询日，灰色表示数据未取得。'+(checks.length?' 最近更新：'+when(checks.at(-1)):'');
 $('#stats-chart').innerHTML=`<div class="bar-scale">数量（篇） · 刻度上限 ${max}</div><div class="bar-columns">${months.map((m,i)=>`<div class="bar-column"><span class="bar-value">${values[i]===null?'未取得':values[i]}</span><div class="bar-track"><div class="bar-fill ${values[i]===null?'missing':''}" style="height:${values[i]===null?100:values[i]/max*100}%" title="${m}：${values[i]===null?'未取得':values[i]+' 篇'}"></div></div><span>${m}${i===5?'*':''}</span></div>`).join('')}</div>`;
 $('#stats-link').innerHTML=id==='all'?'<a href="sources.html#journal-directory">查看各期刊来源与抓取状态 →</a>':`<a href="./?journal=${encodeURIComponent(id)}">查看该期刊相关文献 →</a>`;
 const tableMax=Math.max(1,...rows.flatMap(r=>r.values).filter(v=>v!==null));
 $('#stats-table').innerHTML=`<table><caption>${selected?'本站相关文献':'期刊公开登记量'} · * 当月未结束</caption><thead><tr><th scope="col">期刊</th>${months.map((m,i)=>`<th scope="col">${m}${i===5?'*':''}</th>`).join('')}</tr></thead><tbody>${rows.map(({j,values})=>`<tr><th scope="row">${esc(j.name)}</th>${values.map((v,i)=>`<td>${!selected&&monthly[j.id]?.[months[i]]?.source_url?`<a href="${esc(monthly[j.id][months[i]].source_url)}" target="_blank" rel="noopener" title="查询来源">${v===null?'—':v}</a>`:v===null?'—':v}<span class="cell-bar" style="width:${v===null?0:v/tableMax*100}%"></span></td>`).join('')}</tr>`).join('')}</tbody></table>`;
 }
 for(const id of ['stats-journal','stats-metric','stats-date'])$('#'+id).addEventListener('change',draw);draw();
 }catch(e){if(el)el.textContent='来源状态暂时无法读取，请稍后刷新。';if($('#stats-note'))$('#stats-note').textContent='统计数据暂时无法读取，请稍后刷新。'}
})();
