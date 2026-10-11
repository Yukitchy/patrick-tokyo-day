import sys
from playwright.sync_api import sync_playwright
URL=sys.argv[1]
JS="""()=>{
 const vw=document.documentElement.clientWidth, out={vw, scrollW:document.documentElement.scrollWidth, bodyScrollW:document.body.scrollWidth, bad:[]};
 const story=document.querySelector('.story'); const sr=story.getBoundingClientRect(); out.story=[Math.round(sr.left),Math.round(vw-sr.right)];
 let minL=1e9,minR=1e9;
 story.querySelectorAll('h1,h2,p,li,td,dt,dd,.ph,.tt,.cf,.links a,.tool,table,.lead,.note').forEach(e=>{
  const r=e.getBoundingClientRect(); if(r.width===0)return;
  const l=r.left, rr=vw-r.right; minL=Math.min(minL,l); minR=Math.min(minR,rr);
  if(r.right>vw+0.5||r.left<-0.5) out.bad.push(e.tagName+'.'+e.className+' '+Math.round(r.left)+'..'+Math.round(r.right));
 });
 out.minLeft=Math.round(minL*10)/10; out.minRight=Math.round(minR*10)/10;
 // card interior padding: ph / cf / tt children vs their container
 out.cards=[...story.querySelectorAll('.tt,.cf')].map(c=>{const cr=c.getBoundingClientRect();const ch=[...c.querySelectorAll('td,.cb,p,b')].map(x=>x.getBoundingClientRect()).filter(r=>r.width);return [c.className, Math.round(Math.min(...ch.map(r=>r.left))-cr.left), Math.round(cr.right-Math.max(...ch.map(r=>r.right)))]});
 return out}"""
with sync_playwright() as p:
    for eng,name,w,h in [(p.chromium,'pc1280',1280,800),(p.webkit,'wk390',390,844),(p.webkit,'wk320',320,700)]:
        b=eng.launch(); pg=b.new_page(viewport={'width':w,'height':h}); pg.goto(URL); pg.wait_for_timeout(4000)
        r=pg.evaluate(JS); print(name,r)
        pg.screenshot(path=f'{name}-top.png')
        pg.evaluate("document.querySelector('.step[data-i=\"4\"]').scrollIntoView()"); pg.wait_for_timeout(2500); pg.screenshot(path=f'{name}-s3.png')
        pg.evaluate("window.scrollTo(0,document.documentElement.scrollHeight)"); pg.wait_for_timeout(2500); pg.screenshot(path=f'{name}-end.png')
        has=pg.evaluate("!!document.querySelector('#devbar')"); print(name,'devbar',has)
        if name=='pc1280':
            pg.evaluate("window.scrollTo(0,0)"); pg.click('#devbar button[data-dev=sp]'); pg.wait_for_timeout(4500)
            print('iframe width',pg.evaluate("document.querySelector('#devstage iframe').getBoundingClientRect().width"))
            pg.screenshot(path='pc-devsp.png')
            fr=[f for f in pg.frames if 'noframe' in f.url][0]
            print('inner',fr.evaluate("[innerWidth, document.documentElement.scrollWidth, !!document.querySelector('#devbar')]"))
        b.close()
