#!/usr/bin/env python3
"""Patrick(10/13・Tree紹介)向け 東京1日コース選択ページ。 python3 build.py -> index.html"""
import json, html

# 写真は「ワクワク採点」で選ぶ。建物の外観でなく、そこで人が楽しんでいる絵を最優先。
# 採点と選定理由は photos.json の score / note を見る。
PH = json.load(open('photos.json'))
gm = lambda q: 'https://www.google.com/maps/search/?api=1&query=' + q.replace(' ', '+')
emb = lambda q: 'https://maps.google.com/maps?q=' + q.replace(' ', '+') + '&output=embed&z=12'
def route_emb(stops):
    s = [x.replace(' ', '+') for x in stops]
    return 'https://maps.google.com/maps?saddr=' + s[0] + '&daddr=' + '+to:'.join(s[1:]) + '&output=embed'
def route_link(stops):
    s = [x.replace(' ', '+') for x in stops]
    return ('https://www.google.com/maps/dir/?api=1&origin=' + s[0] + '&destination=' + s[-1]
            + ('&waypoints=' + '%7C'.join(s[1:-1]) if len(s) > 2 else '') + '&travelmode=transit')

HOTEL = 'Mitsui Garden Hotel Nihonbashi Premier'
KOYAMA = ('10:15','Koyama Kyugu, Kanda main store','Bow maker for over 200 years, with its own workshop for bows, arrows and gloves. It opens at 10:00. You can hold the bows and ask the staff anything. This is the main stop, so we take our time.')
START = [('9:00','Pickup at your hotel lobby','Confirmed for 9:00. Mitsukoshimae station is right next to the hotel.'),
         ('9:15','Train to Kanda Myojin','Ginza Line from Mitsukoshimae to Suehirocho, about 5 minutes, then a short walk.'),
         ('9:30','Kanda Myojin shrine','An old Edo shrine above Akihabara, popular with anime fans. We walk the grounds in the quiet before the bow shop opens.'),
         ('10:00','Walk to Koyama Kyugu','About 15 minutes on foot, downhill.')]
BAR = ('19:00','Optional evening finish: Castle Gate','Rock bar for hard rock and heavy metal in Higashi-Ikebukuro. It opens at 19:00, so this is after our day. Open Tuesday, last order 23:30. Say the word and I will meet you there.')
COURSES = [
 dict(id='A', chips=['Shrine and kyudo shop','Anime and manga','Pokémon Center'], name='Bows & anime', tag='Kanda and Ikebukuro',
  why='The anime course. The shrine and the bow shop first, then Ikebukuro: the big Animate store, spicy ramen, and the Pokémon Center in Sunshine City. Everything is open by the time we arrive.',
  steps=START+[KOYAMA,
         ('11:00','Train to Ikebukuro','Marunouchi Line from Awajicho station, one minute from the bow shop. About 17 minutes, no changes.'),
         ('11:30','Animate Ikebukuro main store','The flagship store of Japan\'s biggest anime shop chain. About 5 minutes on foot from the east exit. Manga, character goods, and the streets around it are full of anime shops.'),
         ('12:30','Lunch at Kikanbo Ikebukuro','Spicy miso ramen with chili and Sichuan pepper. You can ask for it milder.'),
         ('13:15','Walk to Sunshine City','Down Sunshine 60 Street, a long shopping street of anime, game and manga shops. About 15 minutes at a slow pace.'),
         ('13:30','Pokémon Center Mega Tokyo','On the second floor of the Alpa shopping area in Sunshine City. The biggest Pokémon store in Tokyo.'),
         ('14:00','Done','In Ikebukuro. Back to Nihonbashi is about 30 minutes: Marunouchi Line to Otemachi, then one stop on the Hanzomon Line. Or we split here.')],
  stops=[HOTEL,'Kanda Myojin','Koyama Kyugu Kanda','Animate Ikebukuro Main Store','Kikanbo Ikebukuro','Pokemon Center Mega Tokyo Sunshine City'],
  moves='Hotel → Kanda Myojin about 5 min on the Ginza Line plus a short walk. Awajicho → Ikebukuro about 17 min on the Marunouchi Line. In Ikebukuro everything is on foot.',
  food=[('Kikanbo Ikebukuro','Ikebukuro · spicy miso ramen','Red miso broth with chili and Sichuan pepper. You pick how hot and how numbing. Open 11:00 to 21:30.','Kikanbo Ikebukuro')],
  good='The most anime of the three, and only one long train ride.',
  mind='Kikanbo is spicy, but you can ask for it milder. The metal bars in Ikebukuro open at 19:00, after this plan ends.',
  links=[('Kanda Myojin','https://www.kandamyoujin.or.jp/'),('Koyama Kyugu','https://koyama-kyugu.co.jp/store/'),('Animate Ikebukuro','https://www.animate.co.jp/shop/ikebukuro/'),('Kikanbo','https://kikanbo.co.jp/pages/shop'),('Pokémon Center Mega Tokyo','https://shop.pokemon.co.jp/ja/shop/pokemoncenter-megatokyo/')]),
 dict(id='B', chips=['Shrine and kyudo shop','Pro wrestling shop','Animate'], name='Bows, wrestling & anime', tag='Kanda, Sugamo and Ikebukuro',
  why='The shrine and the bow shop, then ramen, two floors of pro wrestling goods in Sugamo, and Animate in Ikebukuro. It is the day after Ryogoku, so you will have things to look for.',
  steps=START+[KOYAMA,
         ('11:00','Lunch at Kikanbo Kanda','About 7 minutes on foot from the bow shop. Spicy miso ramen with chili and Sichuan pepper. It opens at 11:00, so no line yet.'),
         ('11:55','Train to Sugamo','JR Yamanote Line from Kanda. About 20 minutes, no changes.'),
         ('12:20','Toudoukan pro wrestling shop','Two floors of wrestling and MMA goods: masks, costumes, signed items, old programs and figures. One minute from the north exit of Sugamo station.'),
         ('13:10','Train to Ikebukuro','Yamanote Line, two stops, about 5 minutes.'),
         ('13:20','Animate Ikebukuro main store','About 5 minutes on foot from the east exit. Manga, character goods, and anime shops on the streets around it.'),
         ('14:00','Done','In Ikebukuro. Back to Nihonbashi is about 30 minutes: Marunouchi Line to Otemachi, then one stop on the Hanzomon Line.')],
  stops=[HOTEL,'Kanda Myojin','Koyama Kyugu Kanda','Kikanbo Kanda Honten','Toudoukan Sugamo','Animate Ikebukuro Main Store'],
  moves='Hotel → Kanda Myojin about 5 min on the Ginza Line plus a short walk. Kanda → Sugamo about 20 min on the Yamanote Line. Sugamo → Ikebukuro about 5 min.',
  food=[('Kikanbo Kanda','Kanda · spicy miso ramen','Red miso broth with chili and Sichuan pepper. You can ask for it milder. Open 11:00 to 21:30 Monday to Saturday.','Kikanbo Kanda Honten')],
  good='The wrestling course. Toudoukan is open every day of the year and sells things you will not find at the venue.',
  mind='Three train rides, but short ones. Pokémon Center and the Ikebukuro metal bars are not in this plan; the bars open at 19:00.',
  links=[('Kanda Myojin','https://www.kandamyoujin.or.jp/'),('Koyama Kyugu','https://koyama-kyugu.co.jp/store/'),('Kikanbo','https://kikanbo.co.jp/pages/shop'),('Toudoukan','https://toudoukan.com/'),('Animate Ikebukuro','https://www.animate.co.jp/shop/ikebukuro/')]),
 dict(id='C', chips=['Shrine and kyudo shop','Heavy metal records','Metal bar at night'], name='Bows, records & metal', tag='Kanda, Ikebukuro and Ochanomizu',
  why='The music course. The shrine and the bow shop, then an early ramen and a rock record store in Ikebukuro, then the world\'s biggest hard rock and heavy metal record store in Ochanomizu, close to Kanda on the way home. At night, if you want, a metal bar.',
  steps=START+[KOYAMA,
         ('11:00','Train to Ikebukuro','Marunouchi Line from Awajicho station, one minute from the bow shop. About 17 minutes, no changes.'),
         ('11:20','Early lunch at Kikanbo Ikebukuro','Spicy miso ramen with chili and Sichuan pepper, just after it opens at 11:00. You can ask for it milder.'),
         ('12:10','Disk Union Ikebukuro','Rock records and band T-shirts on the 9th floor, open from 12:00. A short walk south-east of the station.'),
         ('13:00','Train to Ochanomizu','Marunouchi Line, about 15 minutes, no changes.'),
         ('13:15','Disk Union Hard Rock / Heavy Metal store','In the basement by Ochanomizu station, only rock and metal. Japanese pressings with the paper obi, new and used. Guitar shops line the streets nearby.'),
         ('14:00','Done','At Ochanomizu, close to Kanda. Back to Nihonbashi is about 15 minutes, or stay for the evening option below.'),
         BAR],
  stops=[HOTEL,'Kanda Myojin','Koyama Kyugu Kanda','Kikanbo Ikebukuro','Disk Union Ikebukuro','Disk Union Ochanomizu Hard Rock Heavy Metal','Rock Bar Castle gate Ikebukuro'],
  moves='Hotel → Kanda Myojin about 5 min on the Ginza Line plus a short walk. Awajicho → Ikebukuro about 17 min on the Marunouchi Line, and about 15 min back to Ochanomizu.',
  food=[('Kikanbo Ikebukuro','Ikebukuro · spicy miso ramen','Red miso broth with chili and Sichuan pepper. You pick how hot and how numbing. Open 11:00 to 21:30.','Kikanbo Ikebukuro')],
  good='Metal records in the day and a metal bar at night, with the bow shop in between. The day ends near Kanda.',
  mind='Both record stores open at 12:00 on weekdays, so we eat first. The bar is an evening add-on, not part of the 9:00 to 14:00 plan.',
  links=[('Kanda Myojin','https://www.kandamyoujin.or.jp/'),('Koyama Kyugu','https://koyama-kyugu.co.jp/store/'),('Disk Union Ikebukuro','https://diskunion.net/shop/ikebukuro'),('Disk Union Hard Rock / Heavy Metal','https://diskunion.net/shop/ochanomizu_metal'),('Castle Gate','https://peraichi.com/landing_pages/view/castlegate')]),
]

def menu(c):
    x = PH[c['id']]['card']
    ch = ''.join(f'<li>{html.escape(t)}</li>' for t in c['chips'])
    return f'''<button class="mcard" type="button" data-course="{c['id']}" aria-expanded="false" aria-controls="detail-{c['id']}">
<img src="{x["thumb"]}" alt="{html.escape(x["title"])}" loading="lazy">
<span class="mb"><span class="mk">Course {c['id']}</span><span class="mt">{html.escape(c['name'])}</span>
<span class="mtag">{html.escape(c['tag'])}</span><ul class="mch">{ch}</ul><span class="mopen">See the plan</span></span></button>'''

def detail(c):
    ph = ''.join(f'<img src="{x["thumb"]}" alt="{html.escape(x["title"])}" loading="lazy">' for x in PH[c['id']]['detail'])
    st = ''.join(f'<li><b>{t}</b><div><strong>{h}</strong><span>{d}</span></div></li>' for t, h, d in c['steps'])
    fd = ''.join(f'<a class="eat" href="{gm(q)}" target="_blank" rel="noopener">'
                 f'<img src="{im["thumb"]}" alt="{html.escape(im["title"])}" loading="lazy">'
                 f'<span class="eb"><strong>{n}</strong><em>{a}</em><span>{d}</span>'
                 f'<i>Open in Google Maps ↗</i></span></a>'
                 for (n, a, d, q), im in zip(c['food'], PH[c['id']]['food']))
    ln = ' '.join(f'<a href="{u}" target="_blank" rel="noopener">{html.escape(t)} ↗</a>' for t, u in c['links'])
    sub = f'Oct 13 tour: I choose course {c["id"]} ({c["name"]})'
    return f'''<section class="detail" id="detail-{c['id']}" hidden><div class="dwrap"><div class="dtop"></div>
<div class="dhead"><div><p class="kicker">Course {c['id']} · {html.escape(c['tag'])}</p><h2>{html.escape(c['name'])}</h2></div>
<button class="dclose" type="button" aria-label="Close">Close ✕</button></div>
<p class="why">{html.escape(c['why'])}</p>
<div class="photos">{ph}</div>
<div class="dgrid">
<div><h3>The day</h3><ol class="steps">{st}</ol></div>
<div><h3>The route</h3><div class="mapbox"><iframe src="{route_emb(c['stops'])}" loading="lazy" title="Route for course {c['id']}" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
<p class="moves">{c['moves']} <a href="{route_link(c['stops'])}" target="_blank" rel="noopener">Open the route in Google Maps ↗</a></p></div>
</div>
<h3>Where we eat</h3><div class="eats" style="--n:{len(c['food'])}">{fd}</div>
<div class="notes"><p><b>Good for</b> {html.escape(c['good'])}</p><p><b>Keep in mind</b> {html.escape(c['mind'])}</p></div>
<p class="links">{ln}</p>
<a class="choose" href="mailto:icchan417@gmail.com?subject={html.escape(sub)}">Choose course {c['id']}</a>
</div></section>'''

HERO_CSS = """
.hpic{position:relative;background:#111;color:#fff}
.slides{position:absolute;inset:0;overflow:hidden}
.slides img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transform:scale(1.06);transition:opacity 1.1s ease,transform 5s linear}
.slides img.on{opacity:1;transform:scale(1)}
.slides:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.08) 30%,rgba(0,0,0,.74))}
.hcap{position:relative;z-index:1;min-height:62vh;max-height:600px;display:flex;flex-direction:column;justify-content:flex-end;padding-top:48px;padding-bottom:22px}
.hcap .kicker{color:#9ee3b8}
.hcap h1{color:#fff;margin:0 0 14px;text-shadow:0 2px 14px rgba(0,0,0,.3)}
.snav{display:flex;align-items:center;gap:10px}
.slabel{font:inherit;font-size:12.5px;font-weight:600;color:#fff;background:rgba(0,0,0,.38);border:1px solid rgba(255,255,255,.4);border-radius:999px;padding:7px 13px;cursor:pointer;backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);max-width:100%;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.dots{display:flex;gap:7px;margin-left:auto;flex:none}
.dots button{width:9px;height:9px;padding:0;border:none;border-radius:50%;background:rgba(255,255,255,.45);cursor:pointer}
.dots button.on{background:#fff}
.hbody{padding-top:22px;padding-bottom:26px}
@media(prefers-reduced-motion:reduce){.slides img{transition:none;transform:none}}
"""
HERO_JS = """
 (function(){
  var sl=[].slice.call(document.querySelectorAll('.slides img')),dots=[].slice.call(document.querySelectorAll('.dots button')),lab=document.querySelector('.slabel'),i=0,t;
  function show(n){i=n;sl.forEach(function(x,k){x.classList.toggle('on',k===n)});dots.forEach(function(x,k){x.classList.toggle('on',k===n)});
   lab.textContent='Course '+sl[n].dataset.course+' · '+sl[n].dataset.name;lab.dataset.course=sl[n].dataset.course}
  function go(){clearInterval(t);if(!matchMedia('(prefers-reduced-motion: reduce)').matches)t=setInterval(function(){show((i+1)%sl.length)},4000)}
  dots.forEach(function(d,k){d.addEventListener('click',function(){show(k);go()})});
  lab.addEventListener('click',function(){document.querySelector('.mcard[data-course="'+lab.dataset.course+'"]').click()});
  show(0);go();
 })();
"""

credits = '; '.join(dict.fromkeys(html.escape(x['title'].replace('File:','')) + (' by ' + html.escape(x['artist']) if x.get('artist') else '') + ' (' + x['lic'] + ')' for v in PH.values() for x in [v['card']] + v['detail'] + v['food']))
page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tokyo, Tuesday October 13: three courses for Patrick</title><meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{{--bg:#fffdf6;--card:#fff;--ink:#111;--mute:#767065;--line:#eae4d6;--acc:#1a5c3a;--r:10px}}
*{{box-sizing:border-box;min-width:0}} html,body{{overflow-x:hidden;max-width:100%}} img{{max-width:100%}}
body{{margin:0;font-family:Inter,-apple-system,"Hiragino Sans",sans-serif;color:var(--ink);background:var(--bg);line-height:1.6}}
.wrap{{max-width:1080px;margin:0 auto;padding:0 20px}}
.kicker{{font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--acc);margin:0 0 10px}}
h1,h2,.mt{{text-wrap:balance}} .nb{{white-space:nowrap}}
h1{{font-weight:800;font-size:clamp(34px,5.4vw,54px);line-height:1.06;letter-spacing:-.025em;margin:0 0 16px}}
h2{{font-weight:800;font-size:clamp(30px,4.2vw,42px);line-height:1.06;letter-spacing:-.025em;margin:0}}
h3{{font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--acc);margin:0 0 12px}}
{HERO_CSS}
header p{{font-size:18px;color:var(--mute);margin:0;max-width:620px}}
.facts{{display:flex;flex-wrap:wrap;gap:6px 20px;margin:20px 0 0;padding:0;list-style:none;font-size:14px;color:var(--mute)}} .facts b{{color:var(--ink);font-weight:600}}
.sechead{{display:flex;align-items:baseline;gap:14px;padding:26px 0 16px;border-top:1px solid var(--line)}}
.sechead .n{{font-weight:800;font-size:26px;line-height:1;letter-spacing:-.02em;color:var(--acc)}}
.sechead b{{font-size:19px;font-weight:600}} .sechead span{{font-size:14px;color:var(--mute)}}
.menu{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}}
.mcard{{display:flex;flex-direction:column;text-align:left;font:inherit;color:inherit;background:var(--card);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;padding:0;cursor:pointer;transition:transform .18s,box-shadow .18s,border-color .18s}}
.mcard:hover{{transform:translateY(-3px);box-shadow:0 10px 24px rgba(34,31,27,.10)}}
.menu.picked .mcard:not([aria-expanded=true]){{opacity:.42;filter:saturate(.45)}}
.menu.picked .mcard:not([aria-expanded=true]):hover{{opacity:.75;filter:none}}
.mcard[aria-expanded=true]{{border:2px solid var(--ink);box-shadow:0 12px 28px rgba(17,17,17,.16);transform:translateY(-3px)}}
.mcard[aria-expanded=true] .mopen{{color:var(--acc);border-bottom-color:var(--acc)}}
.mcard>img{{display:block;width:100%;aspect-ratio:4/3;object-fit:cover;background:#f0ebe0}}
.mb{{display:flex;flex-direction:column;flex:1;padding:18px 20px 20px}}
.mk{{display:block;font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--acc);margin-bottom:6px}}
.mt{{display:block;font-weight:800;font-size:26px;line-height:1.12;letter-spacing:-.025em;margin-bottom:6px}}
.mtag{{display:block;font-size:15px;color:var(--mute);margin-bottom:12px}}
.mch{{list-style:none;margin:auto 0 14px;padding:0;display:flex;flex-wrap:wrap;gap:6px}}
.mch li{{font-size:11px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;border:1px solid var(--line);border-radius:4px;padding:3px 8px;color:var(--mute)}}
.mopen{{align-self:flex-start;display:inline-block;font-size:14px;font-weight:600;border-bottom:2px solid var(--acc);padding-bottom:1px}}
.mcard[aria-expanded=true] .mopen::after{{content:" ▲"}} .mcard[aria-expanded=false] .mopen::after{{content:" ▾"}}
.detail{{scroll-margin-top:12px;display:grid;grid-template-rows:0fr;transition:grid-template-rows .32s ease;margin-top:14px;position:relative}}
.detail[hidden]{{display:none}} .detail.open{{grid-template-rows:1fr}}
.dwrap{{overflow:hidden;min-height:0;background:var(--card);border:2px solid var(--ink);border-radius:var(--r);position:relative}}
.detail::before{{content:'';position:absolute;top:-11px;left:var(--arrow,50%);width:20px;height:20px;margin-left:-10px;background:var(--acc);border-left:2px solid var(--acc);border-top:2px solid var(--acc);transform:rotate(45deg);z-index:2;opacity:0;transition:opacity .2s .12s}}
.detail.open::before{{opacity:1}}
.dtop{{height:5px;background:var(--acc)}}
.detail.open .dwrap{{overflow:visible}}
.dwrap>*{{margin-left:26px;margin-right:26px}} .dwrap>.dtop{{margin:0}} .dwrap>.photos{{margin-left:26px;margin-right:26px}}
.dhead{{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;padding-top:26px}}
.dclose{{flex:none;font:inherit;font-size:12px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;color:var(--mute);background:none;border:1px solid var(--line);border-radius:6px;padding:8px 14px;cursor:pointer}}
.dclose:hover{{color:var(--ink);border-color:var(--ink)}}
.why{{font-size:17px;color:var(--mute);margin:10px 0 20px;max-width:640px}}
.photos{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-bottom:26px}}
.photos img{{display:block;width:100%;aspect-ratio:16/10;object-fit:cover;border-radius:8px;background:#f0ebe0}}
.dgrid{{display:grid;grid-template-columns:1fr 1fr;gap:30px;margin-bottom:28px}}
.steps{{list-style:none;padding:0;margin:0;border-top:1px solid var(--line)}}
.steps li{{display:grid;grid-template-columns:60px minmax(0,1fr);gap:12px;padding:11px 0;border-bottom:1px solid var(--line)}}
.steps b{{font-variant-numeric:tabular-nums;color:var(--acc);font-weight:600;font-size:14px}} .steps strong{{display:block;font-weight:600;font-size:16px}} .steps span{{color:var(--mute);font-size:14px}}
.mapbox{{border-radius:8px;overflow:hidden;background:#f0ebe0}} .mapbox iframe{{display:block;width:100%;height:300px;border:0}}
.moves{{font-size:14px;color:var(--mute);margin:12px 0 0}} .moves a{{color:var(--ink);text-decoration:underline;text-underline-offset:3px;white-space:nowrap}}
.eats{{display:grid;grid-template-columns:repeat(var(--n,3),minmax(0,1fr));max-width:calc(var(--n,3)*360px);gap:12px;margin-bottom:26px}}
.eat{{display:flex;flex-direction:column;text-decoration:none;color:inherit;background:var(--bg);border:1px solid var(--line);border-radius:8px;overflow:hidden}}
.eat>img{{display:block;width:100%;aspect-ratio:3/2;object-fit:cover;background:#f0ebe0}}
.eb{{display:flex;flex-direction:column;flex:1;padding:14px 16px 16px}}
.eat:hover{{border-color:var(--ink)}}
.eat strong{{display:block;font-weight:700;font-size:18px;line-height:1.2;letter-spacing:-.015em}}
.eat em{{display:block;font-style:normal;font-size:11px;color:var(--acc);font-weight:600;letter-spacing:.08em;text-transform:uppercase;margin:5px 0 9px}}
.eb>span{{display:block;font-size:14px;color:var(--mute)}} .eat i{{display:block;font-style:normal;font-size:12px;margin-top:auto;padding-top:10px;text-decoration:underline;text-underline-offset:3px}}
.notes{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:20px;font-size:14px}} .notes p{{margin:0;padding:16px 18px;background:var(--bg);border:1px solid var(--line);border-radius:8px}} .notes b{{display:block;font-weight:600;margin-bottom:3px}}
.links{{margin:0 0 22px;font-size:14px;display:flex;flex-wrap:wrap;gap:6px 18px}} .links a{{color:var(--ink);text-decoration:underline;text-underline-offset:3px}}
.nights{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin-bottom:14px;max-width:760px}}
.hint a{{color:var(--ink)}}
.tools{{display:flex;flex-wrap:wrap;gap:10px;margin:18px 0 0}}
.tool{{font:inherit;font-size:13px;font-weight:600;color:var(--ink);background:#fff;border:1px solid var(--ink);border-radius:6px;padding:9px 14px;cursor:pointer;text-decoration:none}}
.tool:hover{{background:var(--ink);color:#fff}}
@media print{{
 @page{{size:A4;margin:12mm}}
 .slides,.mapbox,.menu,.dclose,.choose,.tools,.dots,.snav,.sechead.pk,.cred summary,.detail::before,.dtop{{display:none!important}}
 html,body{{background:#fff}} .hpic{{background:none;color:#000}} .hcap{{min-height:0;padding-top:0}} .hcap h1{{color:#000;text-shadow:none}} .hcap .kicker{{color:var(--acc)}}
 .detail,.detail[hidden]{{display:block!important;margin-top:18px;break-inside:avoid-page}} .dwrap{{border:1px solid #999;overflow:visible}}
 .dgrid,.eats,.notes,.photos{{grid-template-columns:1fr 1fr}} .dgrid{{grid-template-columns:1fr}} .photos img{{max-height:120px}}
 .eat>img{{display:none}} a{{color:#000}}
}}
.choose{{display:inline-block;background:var(--ink);color:#fff;text-decoration:none;font-weight:700;padding:16px 32px;border-radius:8px;font-size:16px;letter-spacing:-.01em;margin-bottom:28px}} .choose:hover{{background:#333}}
.arrival{{display:grid;grid-template-columns:1fr 1fr;gap:26px;align-items:start;padding-bottom:40px}}
.arrival p{{margin:0 0 10px;font-size:16px}} .arrival .hint{{color:var(--mute);font-size:15px}}
.arrival .mapbox iframe{{height:260px}}
footer.wrap{{padding:26px 20px 60px;font-size:13px;color:var(--mute);border-top:1px solid var(--line)}} footer p{{margin:0 0 6px}}
.cred summary{{cursor:pointer;font-size:12px;color:var(--mute);opacity:.75;list-style:none;display:inline-block;text-decoration:underline;text-underline-offset:3px}}
.cred summary::-webkit-details-marker{{display:none}} .cred p{{margin:8px 0 0;font-size:11.5px;line-height:1.6;opacity:.8}}
@media(max-width:820px){{
 .menu{{grid-template-columns:1fr}} .mcard>img{{aspect-ratio:16/9}}
 .dgrid,.eats,.notes,.arrival,.photos,.nights{{grid-template-columns:1fr}} .eats{{max-width:none}}
 .dwrap>*{{margin-left:18px;margin-right:18px}} .mapbox iframe{{height:230px}}
}}
@media(max-width:560px){{
 .wrap{{padding:0 18px}}
 .hcap{{min-height:58vh;padding-bottom:18px}} .hbody{{padding-top:18px;padding-bottom:22px}} .kicker{{margin-bottom:12px}}
 h1{{font-size:33px;line-height:1.08;letter-spacing:-.03em;margin-bottom:14px}}
 header p{{font-size:16px;line-height:1.55;max-width:none}}
 .facts{{display:grid;grid-template-columns:auto 1fr;gap:3px 10px;margin-top:16px;font-size:13px;line-height:1.5}}
 .facts li{{display:contents}} .facts b{{white-space:nowrap}}
 .sechead{{display:block;padding:22px 0 12px}}
 .sechead .n{{font-size:20px;margin-right:8px;display:inline}}
 .sechead b{{font-size:17px}} .sechead span{{display:block;font-size:13px;line-height:1.5;margin-top:2px}}
 .menu{{gap:12px}}
 .mb{{padding:15px 16px 16px}} .mt{{font-size:23px;line-height:1.15}} .mtag{{font-size:14px;margin-bottom:10px}}
 .mch{{gap:5px;margin-bottom:12px}} .mch li{{font-size:10.5px;padding:2px 7px}}
 .mopen{{font-size:13.5px}}
 h2{{font-size:26px;line-height:1.12}}
 .dhead{{padding-top:20px}} .why{{font-size:15.5px;line-height:1.55;margin:8px 0 16px}}
 .dwrap>*{{margin-left:16px;margin-right:16px}}
 .photos{{gap:8px;margin-bottom:20px}} .photos img{{aspect-ratio:3/2}}
 h3{{margin:22px 0 10px}} .dgrid{{gap:0;margin-bottom:0}}
 .steps li{{grid-template-columns:52px minmax(0,1fr);gap:10px;padding:10px 0}}
 .steps strong{{font-size:15.5px}} .steps span{{font-size:13.5px;line-height:1.5}}
 .eats{{gap:10px;margin-bottom:20px}} .eat>img{{aspect-ratio:16/9}} .eb{{padding:12px 14px 14px}}
 .notes{{gap:10px;margin-bottom:16px}} .notes p{{padding:14px 16px;font-size:13.5px}}
 .links{{font-size:13.5px;gap:4px 14px;margin-bottom:18px}}
 .choose{{display:block;text-align:center;padding:15px 0;margin-bottom:22px}}
 .arrival{{gap:16px;padding-bottom:32px}} .arrival p{{font-size:15.5px;line-height:1.55}} .arrival .hint{{font-size:14px}}
 .mapbox iframe{{height:210px}}
 footer.wrap{{padding:20px 18px 44px;font-size:11.5px;line-height:1.55}}
}}
</style></head><body>
<header class="hero">
<div class="hpic"><div class="slides">{''.join(f'<img src="{PH[c["id"]]["card"]["thumb"]}" alt="{html.escape(c["name"])}" data-course="{c["id"]}" data-name="{html.escape(c["name"])}">' for c in COURSES)}</div>
<div class="wrap hcap">
<p class="kicker">Tokyo · Tuesday, October 13</p>
<h1>Bows first, <span class="nb">then pick your noise.</span></h1>
<div class="snav"><button class="slabel" type="button"></button><div class="dots">{''.join(f'<button type="button" aria-label="Show course {c["id"]}"></button>' for c in COURSES)}</div></div>
</div></div>
<div class="wrap hbody">
<p>Every course starts at Kanda Myojin shrine and Koyama Kyugu and then goes to Ikebukuro, the district for anime, manga and Pokémon. What goes around it is up to you. The metal bars open in the evening, so that part is optional.</p>
<p style="font-size:15px;color:var(--mute);margin-top:10px">Pickup is at your hotel lobby (Mitsui Garden Hotel Nihonbashi Premier) at 9:00. The bow shop opens at 10:00, so we start with a walk around Kanda Myojin shrine.</p>
<div class="tools"><button class="tool" type="button" onclick="window.print()">Save as PDF</button><a class="tool" href="patrick-ikebukuro-oct13.pdf" target="_blank" rel="noopener">One-page summary (PDF)</a></div>
<ul class="facts"><li><b>Guide</b> Yuuki</li><li><b>Time</b> 9:00 to about 14:00</li><li><b>Pickup</b> your hotel lobby, 9:00</li><li><b>Included</b> trains and entry</li></ul>
</div>
</header>
<div class="wrap">
<div class="sechead pk"><span class="n">1</span><div><b>Pick a course</b> <span>Tap one to see the plan, the route and where we eat.</span></div></div>
<div class="menu">{''.join(menu(c) for c in COURSES)}</div>
{''.join(detail(c) for c in COURSES)}
<div class="sechead"><span class="n">2</span><div><b>Optional evening</b> <span>Two rock bars in Ikebukuro. Both open after the day plan ends, and both are open on Tuesdays.</span></div></div>
<div class="nights">
<a class="eat" href="{gm('Rock Bar Castle gate Ikebukuro')}" target="_blank" rel="noopener"><span class="eb"><strong>Castle Gate</strong><em>Higashi-Ikebukuro · hard rock and heavy metal</em><span>Basement bar a few minutes from Animate. Open 19:00 to 24:00, last order 23:30. Closed Sundays and Mondays.</span><i>Open in Google Maps ↗</i></span></a>
<a class="eat" href="{gm('LANDSROCK Ikebukuro')}" target="_blank" rel="noopener"><span class="eb"><strong>LANDSROCK</strong><em>West Ikebukuro · metal and hard rock</em><span>Sixth-floor bar with a DJ and a big screen, requests welcome. Open 19:00 to 5:00. Closed Sundays.</span><i>Open in Google Maps ↗</i></span></a>
</div>
<p class="hint" style="margin:0 0 6px;font-size:14px">Hours are from each bar's own page: <a href="https://peraichi.com/landing_pages/view/castlegate" target="_blank" rel="noopener">Castle Gate</a>, <a href="https://lands-rock.com/" target="_blank" rel="noopener">LANDSROCK</a>.</p>
<div class="sechead"><span class="n">3</span><div><b>Where we meet</b> <span>Your hotel lobby at 9:00.</span></div></div>
<div class="arrival">
<div><p>I come to the lobby of the Mitsui Garden Hotel in Nihonbashi (Mitsui Garden Hotel Nihonbashi Premier). Pickup is at 9:00. Kanda, where the bow shop is, is about 15 minutes away.</p>
<p class="hint">If you would rather meet at a station, or start a little later after the night in Ryogoku, tell me and I will change it.</p></div>
<div class="mapbox"><iframe src="{emb(HOTEL)}" loading="lazy" title="Mitsui Garden Hotel Nihonbashi" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
</div>
</div>
<footer class="wrap"><p>Reply to Tree or Yuuki with A, B or C, or mix them. Times are approximate and can move on the day. Shop hours are from each shop's own site for Tuesday, October 13.</p>
<details class="cred"><summary>Photo credits</summary><p>{credits}, via Wikimedia Commons.</p></details></footer>
<script>
(function(){{
 var cards=[].slice.call(document.querySelectorAll('.mcard'));
 function close(id,now){{var d=document.getElementById('detail-'+id);d.classList.remove('open');document.querySelector('.menu').classList.remove('picked');if(now){{d.hidden=true;return}}setTimeout(function(){{if(!d.classList.contains('open'))d.hidden=true}},320);
   document.querySelector('.mcard[data-course="'+id+'"]').setAttribute('aria-expanded','false')}}
 function land(id){{var d=document.getElementById('detail-'+id),done=false;function go(){{if(done)return;done=true;d.scrollIntoView({{behavior:'smooth',block:'start'}})}}
   d.addEventListener('transitionend',function f(e){{if(e.target===d){{d.removeEventListener('transitionend',f);go()}}}});setTimeout(go,420)}}
 var menuEl=document.querySelector('.menu');
 function point(id){{var b=document.querySelector('.mcard[data-course="'+id+'"]'),d=document.getElementById('detail-'+id);
   var r=b.getBoundingClientRect(),w=d.getBoundingClientRect();
   d.style.setProperty('--arrow',(r.left+r.width/2-w.left)+'px')}}
 function open_(id){{var d=document.getElementById('detail-'+id);d.hidden=false;menuEl.classList.add('picked');
   requestAnimationFrame(function(){{d.classList.add('open');point(id)}});
   document.querySelector('.mcard[data-course="'+id+'"]').setAttribute('aria-expanded','true')}}
 window.addEventListener('resize',function(){{var o=document.querySelector('.mcard[aria-expanded=true]');if(o)point(o.dataset.course)}});
 var want=(location.hash.match(/^#detail-([ABC])$/)||[])[1]||(location.search.match(/[?&]open=([ABC])/)||[])[1];
 if(want){{open_(want);setTimeout(function(){{document.getElementById('detail-'+want).scrollIntoView()}},80)}}
 cards.forEach(function(b){{
  b.addEventListener('click',function(){{
   var id=b.dataset.course,was=b.getAttribute('aria-expanded')==='true';
   cards.forEach(function(o){{if(o.getAttribute('aria-expanded')==='true')close(o.dataset.course,true)}});
   if(was)return;
   open_(id);history.replaceState(null,'','#detail-'+id);
   land(id);
  }});
 }});
 document.querySelectorAll('.dclose').forEach(function(x){{
  x.addEventListener('click',function(){{var d=x.closest('.detail'),id=d.id.replace('detail-','');close(id);
   document.querySelector('.mcard[data-course="'+id+'"]').scrollIntoView({{behavior:'smooth',block:'center'}})}});
 }});
}})();
{HERO_JS}
</script>
{{DEVBAR}}</body></html>'''
open('index.html', 'w').write(page.replace('{DEVBAR}', ''))
open('preview.html', 'w').write(page.replace(
    '{DEVBAR}',
    '<script>window.DEVBAR_FORCE=1</script><script src="devbar.js?v=3"></script>'))
print('written', len(page), '-> index.html + preview.html')
