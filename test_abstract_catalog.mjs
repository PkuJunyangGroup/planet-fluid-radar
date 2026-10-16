// KATEX_JS=/path/to/katex.min.js node test_abstract_catalog.mjs
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
assert.ok(process.env.KATEX_JS,'Supply the pinned KaTeX 0.16.22 browser bundle');
const ctx=vm.createContext({Date,Intl,Map,Set,console,crypto:{randomUUID:()=> 'test'},localStorage:{getItem:()=>null,setItem:()=>{}}});
vm.runInContext(fs.readFileSync(process.env.KATEX_JS,'utf8'),ctx);
const actual=ctx.katex;assert.equal(actual.version,'0.16.22');
vm.runInContext(fs.readFileSync(new URL('./app.js',import.meta.url),'utf8').replace(/\ninit\(\);\s*$/,''),ctx);
vm.runInContext('recommendations=new PaperRecommendations(""); recommendations.ready=true;',ctx);
const render=vm.runInContext('abstractHTML',ctx), title=vm.runInContext('titleHTML',ctx), row=vm.runInContext('paperRow',ctx), authors=vm.runInContext('paperAuthors',ctx);
let attempts=0, failures=[];
ctx.katex={renderToString:(tex,options)=>{attempts++;try{return actual.renderToString(tex,options)}catch(e){failures.push({tex,error:String(e)});throw e}}};
const input=fs.readFileSync(new URL('./catalog.json',import.meta.url),'utf8');
const papers=JSON.parse(input).papers;let missing=0,mathPapers=0,bilingualPapers=0;
for(const p of papers){
 const before=JSON.stringify(p),start=attempts;const html=render(p.abstract||'');
 if(attempts>start)mathPapers++;
 const full=row(p);
 assert.ok(full.includes(title(p.title)),'The safe rendered title must be included');
 assert.equal(JSON.stringify(p),before,'Renderer must not mutate metadata');
 assert.ok(full.includes('<details class="abstract"><summary>Abstract</summary>'));
 assert.ok(!full.includes('<details open'));
 assert.ok(!/<script|<iframe|<img\b/i.test(html));
 assert.ok(full.includes(html),'Full rendered abstract must be included without truncation');
 if(!p.abstract){missing++;assert.ok(full.includes('The source has not supplied an abstract.'))}
 if(authors(p).some(n=>n.includes(' · ')))bilingualPapers++;
}
assert.equal(fs.readFileSync(new URL('./catalog.json',import.meta.url),'utf8'),input);
assert.deepEqual(failures,[],'All current formula spans must render');
const catalogAttempts=attempts/2; // both titles and abstracts are rendered directly and in paperRow
for(const input of [String.raw`$\upmu$`,String.raw`\ce{CO2}`,String.raw`\ce{H2O}`,String.raw`$3400 \text{ kg/m}^2$`, '$'+Array(300).fill('x').join('+')+'$'])assert.ok(render(input).includes('katex-mathml'));
assert.equal(render(String.raw`18.12\% and 17\,d`),'18.12% and 17\u2009d');
assert.equal(render(String.raw`\textit{Spitzer}`),'<em>Spitzer</em>');
assert.ok(render(String.raw`\textit{<script>alert(1)</script>}`).includes('&lt;script&gt;'));
for(const input of ['$5 and $10.','$5 million and $10 million.',String.raw`\$5`])assert.ok(!render(input).includes('katex-mathml'));
assert.ok(render('$5 and $x$').startsWith('$5 and '));
for(const input of [String.raw`$\href{javascript:alert(1)}{click}$`,String.raw`$\htmlClass{evil}{x}$`,String.raw`\ce{<script>}`])assert.ok(!/<script|href=|class="evil"/.test(render(input)));
assert.equal(render('$\\unknown{x}$'),'$\\unknown{x}$');
const style=fs.readFileSync(new URL('./style.css',import.meta.url),'utf8');
assert.match(style,/\.abstract-math\{[^}]*display:inline[;}]/);
assert.doesNotMatch(style.match(/\.abstract-math\{([^}]*)\}/)[1],/overflow|vertical-align/);
assert.match(style,/\.abstract-math-display\{[^}]*max-width:100%[^}]*overflow-x:auto/);
assert.match(style,/overflow-wrap:anywhere/);
console.log(JSON.stringify({total:papers.length,supplied:papers.length-missing,missing,mathPapers,plainPapers:papers.length-missing-mathPapers,formulaSpans:catalogAttempts,formulaFailures:0,bilingualPapers,closedAndFullRowsChecked:papers.length,visualBrowserCheck:'not performed; CSS/renderer checks are not visual layout verification'},null,2));
