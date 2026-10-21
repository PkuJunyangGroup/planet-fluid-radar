import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
// Optional integration: KATEX_JS=/path/to/katex.min.js node test_abstract_math.mjs
const context=vm.createContext({Date,Intl,Map,Set,console,crypto:{randomUUID:()=> 'test'},localStorage:{getItem:()=>null,setItem:()=>{}}});
vm.runInContext(fs.readFileSync(new URL('./app.js',import.meta.url),'utf8').replace(/\ninit\(\);\s*$/,''),context);
const render=vm.runInContext('abstractHTML',context);
const raw=String.raw`Full original $T_{eq}=300\,\mathrm{K}$ and <script>alert(1)</script>. Final sentence.`;
assert.equal(render(raw),raw.replaceAll('<','&lt;').replaceAll('>','&gt;'));
const calls=[];
context.katex={renderToString:(tex,options)=>{calls.push({tex,options});if(tex==='\\bad')throw Error();return '<math>safe</math>'}};
for(const [input,expected] of [[String.raw`H$_2$O`,['_2']],['$x$ and $$y^2$$',['x','y^2']],[String.raw`\(\alpha\) and \[E=mc^2\]`,['\\alpha','E=mc^2']],['$5 and $10. No formula.',[]],[String.raw`\$5 and \$10`,[]],['$unmatched',[]],['<img src=x onerror=alert(1)>',[]],['$x$1',[]],[String.raw`$\sim$$1350$`,['\\sim','1350']],[String.raw`$\sim$$70$%`,['\\sim','70']],[String.raw`$\lesssim$$50$%`,['\\lesssim','50']],['$x$$y$',['x','y']],['$$x^2$$$$y^2$$',['x^2','y^2']],['<jats:inline-formula><jats:tex-math><![CDATA[$x_1$]]></jats:tex-math></jats:inline-formula>',['x_1']]]){
 calls.length=0;render(input);assert.deepEqual(calls.map(x=>x.tex),expected,input);
 for(const c of calls){assert.equal(c.options.trust,false);assert.equal(c.options.output,'htmlAndMathml');assert.equal(c.options.maxExpand,200)}
}
assert.equal(render('$\\bad$'),'$\\bad$');
assert.ok(render('<script>alert(1)</script>').startsWith('&lt;script&gt;'));
if(process.env.KATEX_JS){
 vm.runInContext(fs.readFileSync(process.env.KATEX_JS,'utf8'),context);
 for(const input of [String.raw`$\sim$$1350$`,String.raw`$\sim$$70$%`,String.raw`$\lesssim$$50$%`,String.raw`H$_2$O`,String.raw`$T_{\rm eq}=300\,\mathrm K$`,String.raw`\(\frac{a}{b}\)`,String.raw`$$\int_0^1 x^2 dx$$`]){
  const html=render(input);assert.ok(html.includes('katex-mathml'));assert.ok(html.includes('<math'));assert.ok(!html.includes('katex-error'));
 }
 assert.ok(!render(String.raw`$\href{javascript:alert(1)}{click}$`).includes('href='));
 assert.ok(!render(String.raw`$\htmlClass{evil}{x}$`).includes('class="evil"'));
 assert.equal(render('$\\unknowncommand{x}$'),'$\\unknowncommand{x}$');
 const papers=JSON.parse(fs.readFileSync(new URL('./catalog.json',import.meta.url))).papers;
 let n=0;for(const p of papers){if(render(p.abstract||'').includes('katex-mathml'))n++}
 console.log(`Real KaTeX integration passed; ${n} existing abstracts typeset.`);
}
console.log('Math delimiters, currency, fallback, escaping, publisher TeX and safe options passed.');
