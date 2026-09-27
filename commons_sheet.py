import json,urllib.request,urllib.parse,io,sys
from PIL import Image,ImageDraw
H={'User-Agent':'yuki-manga-week/1.0'}
import time
def api(**kw):
    u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(dict(format='json',**kw))
    for k in range(6):
        try:
            time.sleep(1.2);return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=H)))
        except urllib.error.HTTPError as e:
            if e.code==429: time.sleep(15*(k+1));continue
            raise
    raise SystemExit('429 persists')
def resolve(c):
    r=api(action='query',list='categorymembers',cmtitle='Category:'+c,cmlimit=1)
    if r.get('query',{}).get('categorymembers'): return c
    kw=c.split(' ')[0]
    for a in api(action='query',list='allcategories',acprefix=kw,aclimit=30).get('query',{}).get('allcategories',[]):
        n=a['*']
        if c.lower()[:5] in n.lower(): print('  resolved',c,'->',n);return n
    return None
def files_in(cat,depth=1):
    out=[]
    r=api(action='query',list='categorymembers',cmtitle=cat,cmtype='file|subcat',cmlimit=200)
    for m in r.get('query',{}).get('categorymembers',[]):
        if m['ns']==6: out.append(m['title'])
        elif depth>0 and len(out)<60: out+=files_in(m['title'],depth-1)
    return out
def run(name,cats,maxn=30):
    titles=[]
    for c in cats:
        c=resolve(c)
        if not c: continue
        titles=[t for t in files_in('Category:'+c) if t.lower().endswith(('.jpg','.jpeg','.png'))]
        if titles: print(name,'<-',c,len(titles)); break
    if not titles: print(name,'NONE'); return
    titles=titles[:maxn]; info=[]
    for i in range(0,len(titles),50):
        r=api(action='query',titles='|'.join(titles[i:i+50]),prop='imageinfo',iiprop='url|extmetadata',iiurlwidth=960)
        for p in r['query']['pages'].values():
            if 'imageinfo' in p:
                ii=p['imageinfo'][0];info.append(dict(title=p['title'][5:],thumb=ii['thumburl'].split('?')[0],lic=ii.get('extmetadata',{}).get('LicenseShortName',{}).get('value','')))
    cells=[]
    for i,x in enumerate(info):
        try: im=Image.open(io.BytesIO((time.sleep(0.4) or urllib.request.urlopen(urllib.request.Request(x['thumb'].replace('/960px-','/330px-'),headers=H))).read())).convert('RGB')
        except Exception: continue
        im.thumbnail((200,200));c=Image.new('RGB',(200,200),'white');c.paste(im,((200-im.width)//2,(200-im.height)//2));d=ImageDraw.Draw(c);d.rectangle([0,0,30,18],fill='black');d.text((4,3),str(i),fill='white');cells.append(c)
    cols=6;rows=(len(cells)+cols-1)//cols;sh=Image.new('RGB',(cols*200,rows*200),'white')
    for k,c in enumerate(cells): sh.paste(c,((k%cols)*200,(k//cols)*200))
    sh.save(f'S-{name}.jpg',quality=75);json.dump(info,open(f'S-{name}.json','w'),ensure_ascii=False)
for name,cats in json.loads(sys.argv[1]).items(): run(name,cats)
