import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const ctx=vm.createContext({Date,Intl,Map,Set,console,crypto:{randomUUID:()=> 'test'},localStorage:{getItem:()=>null,setItem:()=>{}}});
vm.runInContext(fs.readFileSync(new URL('./app.js',import.meta.url),'utf8').replace(/\ninit\(\);\s*$/,''),ctx);
vm.runInContext('recommendations=new PaperRecommendations(""); recommendations.ready=true;',ctx);
const title=vm.runInContext('titleHTML',ctx),row=vm.runInContext('paperRow',ctx);
const raw=String.raw`O$_3$ detection & <img src=x onerror=alert(1)>`;
assert.equal(title(raw),'O$_3$ detection &amp; &lt;img src=x onerror=alert(1)&gt;');
assert.equal(title(undefined),'');
const calls=[];
ctx.katex={renderToString:(tex,options)=>{calls.push({tex,options});return '<math>safe</math>'}};
for(const input of ['O$_3$', '$$x^2$$', String.raw`\[x^2\]`, '<disp-formula><tex-math>x^2</tex-math></disp-formula>']){
 calls.length=0;
 const html=title(input);
 assert.equal(calls.length,1);
 assert.equal(calls[0].options.displayMode,false,'Titles must stay inline');
 assert.equal(calls[0].options.trust,false);
 assert.equal(calls[0].options.maxExpand,200);
 assert.ok(!html.includes('abstract-math-display'));
}
const paper=JSON.parse(fs.readFileSync(new URL('./catalog.json',import.meta.url))).papers.find(p=>p.id==='2610.19081');
assert.ok(paper,'Keep a regression for the UV Coronagraph paper');
const before=JSON.stringify(paper);
assert.ok(row(paper).match(/<h3>.*<math>safe<\/math>.*<\/h3>/));
assert.equal(JSON.stringify(paper),before,'Rendering must preserve the raw title/abstract');
if(process.env.KATEX_JS){
 vm.runInContext(fs.readFileSync(process.env.KATEX_JS,'utf8'),ctx);
 const html=row(paper),heading=html.match(/<h3>(.*?)<\/h3>/)[1];
 assert.ok(heading.includes('katex-mathml'));
 assert.ok(!heading.includes('O$_3$'));
 assert.ok(html.includes('<details class="abstract"><summary>Abstract</summary>'));
 for(const input of [String.raw`$\href{javascript:alert(1)}{click}$`,String.raw`$\htmlClass{evil}{x}$`]){
  assert.ok(!/<a\b|class="evil"/.test(title(input)));
 }
 const unsafe=row({...paper,title:raw,url:'javascript:alert(1)'});
 assert.ok(unsafe.includes('<h3><a href="#"'));
 assert.ok(!/<img\b|<script\b/.test(unsafe));
 assert.ok(unsafe.includes('&lt;img src=x onerror=alert(1)&gt;'));
 assert.equal(title('$\\unknowncommand{x}$'),'$\\unknowncommand{x}$');
 assert.equal(title('$5 and $10.'),'$5 and $10.');
}
console.log('Safe inline title math, source preservation, renderer fallback and title-link escaping passed.');
