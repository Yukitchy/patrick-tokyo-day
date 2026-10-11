#!/usr/bin/env python3
"""Patrick, Tue Oct 13: one-route map-led scroll story (shibuya-walk/shiori style).
python3 build.py -> index.html   (CSS in style.css, map code in map.js)
DEVBAR=True shows the PC/phone toggle on the public URL while Yuuki reviews. Set False before sending to Patrick."""
import json
DEVBAR = True

gm = lambda q: 'https://www.google.com/maps/search/?api=1&query=' + q.replace(' ', '+')
A = lambda u, t: f'<a href="{u}" target="_blank" rel="noopener">{t}</a>'
def links(*ls): return '<ul class="links">' + ''.join('<li>' + A(u, t) + '</li>' for t, u in ls) + '</ul>'
def pts(*ps): return '<ul class="pts">' + ''.join(f'<li><b>{a}</b><span>{b}</span></li>' for a, b in ps) + '</ul>'
def nums(*ns): return '<dl class="nums">' + ''.join(f'<div><dt>{a}</dt><dd class="n">{b}</dd><dd class="s">{c}</dd></div>' for a, b, c in ns) + '</dl>'
def ph(src, alt): return f'<div class="ph"><img src="{src}" alt="{alt}"></div>'

# Tokyo Metro line chips
LINE = dict(G=('Ginza Line', '#f39700'), M=('Marunouchi Line', '#e60012'), Z=('Hanzomon Line', '#8f76d6'), Y=('Yurakucho Line', '#d7c447'))
def ln(k): return f'<span class="ln" style="--c:{LINE[k][1]}">{k}</span>{LINE[k][0]}'
def nxt(*rows): return '<div class="next"><p class="nl">Next</p>' + ''.join(f'<p>{r}</p>' for r in rows) + '</div>'

TH = 'https://thumb.wikimedia.org/wikipedia/commons/thumb/'
IMG = dict(
    kyudo=TH + '2/29/Professor_Inagaki_Genshiro.jpg/960px-Professor_Inagaki_Genshiro.jpg',
    animate='https://upload.wikimedia.org/wikipedia/commons/c/c5/ANIMATE-Ikebukuro.JPG',
    poke=TH + 'e/ec/Mega_Tokyo_Pok%C3%A9mon_Center_1.jpg/960px-Mega_Tokyo_Pok%C3%A9mon_Center_1.jpg',
    kikanbo=TH + '8/8c/Very_hot_tsukemen_%28close-up%29.jpg/960px-Very_hot_tsukemen_%28close-up%29.jpg',
    mutekiya=TH + '8/8a/Ikkousha_tonkotsu_bowl.jpg/960px-Ikkousha_tonkotsu_bowl.jpg',
    anpuku=TH + '5/54/Kama-age_Udon.jpg/960px-Kama-age_Udon.jpg',
    yan=TH + '4/44/Dandannoodles.jpg/960px-Dandannoodles.jpg',
    motomura=TH + 'b/b4/Gyukatsu_%2846075415774%29.jpg/960px-Gyukatsu_%2846075415774%29.jpg')

# lat, lon, full name, short label, label side, time  (coordinates from GSI geocoder / Tabelog)
P = [None,
     (35.6865, 139.7740, 'Hotel lobby, Nihonbashi', 'Hotel', 'r', '9:30'),
     (35.6951, 139.7685, 'Koyama Kyugu, Kanda', 'Koyama', 'r', '10:00'),
     (35.7311, 139.7154, 'Animate Ikebukuro', 'Animate', 'r', '11:30'),
     (35.7295, 139.7124, 'Lunch, pick one of five', '', 'r', '12:15'),
     (35.7278, 139.7200, 'Pokémon Center Mega Tokyo', 'Pokémon Center', 'r', '13:15'),
     (35.7287, 139.7138, 'Disk Union Ikebukuro (if it fits)', 'Disk Union', 'l', '14:15')]
LI = 4
# lunch options: name, lat, lon, label side, photo, photo credit, Tabelog score, reviews note, what, hours, walk from Animate, map query
LUNCH = [
    ('Kikanbo', 35.7291, 139.7153, 't', 'kikanbo', 'Very hot tsukemen (close-up).jpg by insatiablemunch, CC BY 2.0', '3.6', 'Tabelog, 1,800+ reviews',
     'Spicy miso ramen. You choose how hot and how numbing (Sichuan pepper) it is, and you can ask for it mild. Counter seats only, and a short line is normal at lunch.',
     'Open 11:00 to 21:30, every day', 4, 'Kikanbo Ikebukuro', 'https://kikanbo.co.jp/pages/shop'),
    ('Gyukatsu Motomura', 35.7290, 139.7186, 'b', 'motomura', 'Gyukatsu (46075415774).jpg by Raita Futo, CC BY 2.0', '3.1', 'Tabelog, 23 reviews, opened Feb 2026',
     'Beef cutlet fried quickly so the middle stays rare. You finish each slice on a small hot stone at your table. Inside Sunshine City, in the same Alpa building as the Pokémon Center.',
     'Open 11:00 to 22:00, every day', 7, 'Gyukatsu Motomura Sunshine Ikebukuro', 'https://tabelog.com/tokyo/A1305/A130501/13318857/'),
    ('Mutekiya', 35.7269, 139.7117, 'b', 'mutekiya', 'Ikkousha tonkotsu bowl.jpg by Wesoree, CC BY-SA 4.0', '3.6', 'Tabelog, 2,000+ reviews',
     'Rich pork-bone (tonkotsu) ramen with thick slices of roast pork. Only 17 counter seats, so expect a line, and it closes when the soup runs out.',
     'Open from 10:30, every day', 10, 'Mutekiya Ikebukuro', 'https://tabelog.com/tokyo/A1305/A130501/13003927/'),
    ('Anpuku', 35.7324, 139.7090, 'r', 'anpuku', 'Kama-age Udon.jpg by Lombroso, public domain', '3.6', 'Tabelog, 1,900+ reviews, Udon East 100 (2024)',
     'Creative udon served like pasta. The famous bowl is carbonara udon in a bonito-dashi sauce. On the west side of the station. No reservations at lunch.',
     'Lunch 11:00 to 15:00, closed only at New Year', 12, 'Anpuku Ikebukuro', 'https://tabelog.com/tokyo/A1305/A130501/13097934/'),
    ('Yan, Sichuan home cooking', 35.7301, 139.7072, 'b', 'yan', 'Dandannoodles.jpg by Alpha from Melbourne, CC BY-SA 2.0', '3.5', 'Tabelog, 1,600+ reviews',
     'Sichuan food, known for dry tantan noodles (no soup) and handmade fried and boiled gyoza. It appeared in the TV show Kodoku no Gourmet. The spice can be made milder on request.',
     'Weekday lunch 11:30 to 15:00', 14, 'Chinese Kateiryori Yan 2 Ikebukuro', 'https://tabelog.com/tokyo/A1305/A130501/13009261/'),
]
LUNCH_JS = [[l[1], l[2], l[0].split(',')[0].replace('Gyukatsu ', ''), l[3]] for l in LUNCH]

TT = [('9:30', 'Meet at the hotel lobby (to be confirmed)'), ('9:40', 'Ginza Line to Kanda, then 5 min on foot'), ('10:00', 'Koyama Kyugu, Kanda main store'),
      ('10:50', 'Marunouchi Line from Awajicho to Ikebukuro'), ('11:30', 'Animate Ikebukuro main store'), ('12:15', 'Lunch, you pick one of five'),
      ('13:15', 'Pokémon Center Mega Tokyo'), ('14:15', 'Disk Union Ikebukuro, if it fits'), ('14:30', 'Done, in Ikebukuro')]
tt = ''.join(f'<tr class="st-plain"><td class="v">{t}</td><td><span class="k">{k}</span></td></tr>' for t, k in TT)

def step(i, h, body):
    t = P[i][5]
    return f'<article class="step" data-i="{i}"><p class="no"><i>{i}</i>{t}</p><h2>{h}</h2>{body}</article>'

def lunch_card(l):
    name, _, _, _, img, cred, score, rn, what, hours, walk, q, url = l
    return (f'<div class="cf"><img class="sv" loading="lazy" src="{IMG[img]}" alt="Example photo of the dish at {name}">'
            f'<div class="cb"><b>{name}</b><p class="rt"><span class="st">★ {score}</span> · {rn}</p><p>{what}</p>'
            f'<p class="rt">{hours} · about {walk} min on foot from Animate</p>'
            f'<a class="mini" href="{gm(q)}" target="_blank" rel="noopener">Map ↗</a> <a class="mini" href="{url}" target="_blank" rel="noopener">Details ↗</a>'
            f'<small>Photo: example of the dish. {cred}</small></div></div>')

S = []
S.append(f'<article class="step" data-i="0"><p class="no"><i>0</i>The whole day</p><h2>One route,<span class="l2">9:30 to <em>14:30</em></span></h2>'
         '<p class="lead">A bow maker in Kanda in the morning, then Ikebukuro for anime, a lunch you choose, Pokémon and, if it fits, metal records. Two train rides, no changes, and the rest on foot.</p>'
         f'<div class="tt"><p class="cap">The day</p><table>{tt}</table></div>'
         + pts(('Good for', 'Bows, anime and manga, Pokémon, heavy metal records, and one proper lunch in the middle.'),
               ('Keep in mind', 'Times are approximate and can move on the day. Kanda Myojin shrine is a short walk from the bow shop, and we can stop by if we have a few minutes.'))
         + links(('Open the whole route in Google Maps', 'https://www.google.com/maps/dir/?api=1&origin=Mitsui+Garden+Hotel+Nihonbashi+Premier&destination=Disk+Union+Ikebukuro&waypoints=Koyama+Kyugu+Kanda%7CAnimate+Ikebukuro+Main+Store%7CPokemon+Center+Mega+Tokyo+Sunshine+City&travelmode=transit')) + '</article>')
S.append(step(1, 'We meet in <em>the lobby</em>',
              '<p class="lead">I come to the lobby of the Mitsui Garden Hotel Nihonbashi Premier. Mitsukoshimae station is right next to the hotel.</p>'
              + nums(('Time', '9:30', 'Tuesday, October 13'), ('Finish', '14:30', 'Ikebukuro'))
              + '<p class="note" style="font-size:13px;color:var(--mute)">Meeting time 9:30, still being confirmed with Tree.</p>'
              + links(('Hotel on Google Maps', gm('Mitsui Garden Hotel Nihonbashi Premier')))
              + nxt(f'{ln("G")} · Mitsukoshimae to Kanda, 1 stop, 2 min', 'Then 5 min on foot to the bow shop.')))
S.append(step(2, 'The <em>bow maker</em>', ph(IMG['kyudo'], 'An archer in hakama at full draw')
              + '<p class="lead">Koyama Kyugu has made bows for over 200 years and has its own workshop for bows, arrows and gloves. We arrive when it opens at 10:00, so the shop is calm. You can hold the bows and ask the staff anything. This is the main morning stop, so we take our time.</p>'
              '<div class="cafes"><div class="cf"><div class="cb"><b>Koyama Kyugu, Kanda main store</b><p class="rt"><span class="st">★ 4.2</span> · 217 Google reviews</p><p>Open Tuesday 10:00 to 19:00.</p><small>Rating from Google Maps, October 2026.</small></div></div></div>'
              '<p class="note" style="font-size:14px">The Kanda Myojin shrine is a short walk away. If we have a few minutes, we stop by.</p>'
              + links(('Koyama Kyugu on Google Maps', gm('Koyama Kyugu Kanda')), ('Official site', 'https://koyama-kyugu.co.jp/store/'), ('Kanda Myojin', gm('Kanda Myojin')))
              + nxt(f'{ln("M")} · Awajicho to Ikebukuro, about 17 min, no changes', 'Awajicho station is 1 min from the shop (Shin-Ochanomizu exit A1).')))
S.append(step(3, '<em>Animate</em>,<span class="l2">Japan\'s biggest anime shop</span>', ph(IMG['animate'], 'The Animate Ikebukuro main store building')
              + '<p class="lead">Animate\'s main store is about 5 minutes on foot from the east exit of Ikebukuro station: manga, character goods, and anime shops on the streets around it.</p>'
              + nums(('Open', '10:00 to 21:00', 'Tuesday'))
              + links(('Animate on Google Maps', gm('Animate Ikebukuro Main Store')), ('Official site', 'https://www.animate.co.jp/shop/ikebukuro/'))
              + nxt('On foot to lunch. The five places are 4 to 14 minutes away, and you choose at the next stop.')))
S.append(step(4, '<em>Lunch</em>,<span class="l2">you pick one of five</span>',
              '<p class="lead">All five are in Ikebukuro, and all are open at lunchtime on Tuesday. Tell me which one you feel like and we go. The photos show the dish, not the shop.</p>'
              '<div class="cafes">' + ''.join(lunch_card(l) for l in LUNCH) + '</div>'
              '<p class="asof">Scores are from Tabelog, October 2026. Tabelog scores run lower than Google, and 3.5 is already very good.</p>'
              + nxt('On foot to Sunshine City, 5 to 20 min depending on where we eat. Or ' + ln('Y') + ', Ikebukuro to Higashi-Ikebukuro, 1 stop, then 5 min on foot.')))
S.append(step(5, '<em>Pokémon Center</em>,<span class="l2">Sunshine City</span>', ph(IMG['poke'], 'Inside the Pokémon Center Mega Tokyo')
              + '<p class="lead">The Pokémon Center Mega Tokyo is on the second floor of the Alpa shopping area in Sunshine City, the biggest Pokémon store in Tokyo. We have about an hour here.</p>'
              + nums(('Open', '10:00 to 20:00', 'Tuesday'))
              + links(('Pokémon Center on Google Maps', gm('Pokemon Center Mega Tokyo Sunshine City')), ('Official site', 'https://shop.pokemon.co.jp/ja/shop/pokemoncenter-megatokyo/'))
              + nxt('To Disk Union: about 10 min on foot. Or ' + ln('Y') + ', Higashi-Ikebukuro to Ikebukuro, 1 stop, then 5 min on foot.')))
S.append(step(6, '<em>Metal</em> records,<span class="l2">and done</span>',
              '<p class="lead">Disk Union Ikebukuro has rock and metal records and band T-shirts, new and used. We only go if we still have time and energy. If not, we finish at the Pokémon Center. Either way we are done around 14:30 in Ikebukuro, and we can split here.</p>'
              + nums(('Open', '12:00 to 20:00', 'Tuesday'))
              + links(('Disk Union on Google Maps', gm('Disk Union Ikebukuro')), ('Official site', 'https://diskunion.net/shop/ikebukuro'))
              + nxt('Back to Nihonbashi, about 30 min: ' + ln('M') + ' to Otemachi, then ' + ln('Z') + ' one stop to Mitsukoshimae.')))
night = ('<section class="x"><p class="note" style="font-size:13px;color:var(--mute);margin-top:0"><b style="color:var(--ink)">If you want a bit more tonight:</b> two rock bars in Ikebukuro, both open on Tuesdays. '
         + A(gm('Rock Bar Castle gate Ikebukuro'), 'Castle Gate') + ' 19:00 to 24:00 (closed Sun and Mon), ' + A(gm('LANDSROCK Ikebukuro'), 'LANDSROCK') + ' 19:00 to 5:00 (closed Sun). Hours from '
         + A('https://peraichi.com/landing_pages/view/castlegate', 'Castle Gate') + ' and ' + A('https://lands-rock.com/', 'LANDSROCK') + '.</p></section>')
credit_items = ['Professor Inagaki Genshiro.jpg CC BY-SA 3.0', 'ANIMATE-Ikebukuro.JPG by Itasan, CC BY-SA 3.0', 'Mega Tokyo Pokémon Center 1.jpg by Maplestrip, CC BY 3.0'] + [l[5] for l in LUNCH]
credit = ('<footer class="credit"><p class="note" style="margin:0 0 10px">Times are approximate and can move on the day. Message Yuuki if you want to change anything.</p><details><summary>Photo credits</summary><ul>'
          + ''.join(f'<li>{c}</li>' for c in credit_items)
          + '</ul><p>Photos via Wikimedia Commons. Map: Tiles © Esri / © ' + A('https://www.openstreetmap.org/copyright', 'OpenStreetMap') + '</p></details></footer>')
dn = ''.join(f'<button type="button" class="dn" data-i="{i}" aria-label="{"The whole day" if i == 0 else P[i][5]}">{i}</button>' for i in range(len(P)))
head = ('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light"><meta name="robots" content="noindex,nofollow"><title>Your day in Tokyo</title>'
        '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@500;700;900&display=swap">'
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css"><script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script><style>' + open('style.css').read() + '</style></head><body>')
intro = ('<div class="wrap"><div class="mapbox"><div id="map" aria-label="Map of the day"></div><p class="where"><small>Tue, October 13</small><b>The whole day</b></p>'
         '<nav class="dial" aria-label="Switch stop"><button type="button" class="ar" data-d="-1" aria-label="Previous stop">&lsaquo;</button><div class="nums-r">' + dn + '</div><button type="button" class="ar" data-d="1" aria-label="Next stop">&rsaquo;</button></nav></div>'
         '<main class="story"><header class="intro"><p class="date">Tuesday, October 13 · 9:30 to 14:30</p><h1>Your day<br>in Tokyo</h1><p class="who">Patrick, with Yuuki. Kanda and Ikebukuro: a bow maker, anime, Pokémon, and a lunch you choose.</p>'
         '<dl class="cn"><div><dt>Meet</dt><dd class="n">9:30</dd><dd class="s">Hotel lobby</dd></div><div><dt>Finish</dt><dd class="n">14:30</dd><dd class="s">Ikebukuro</dd></div></dl>'
         '<div class="tools"><a class="tool" href="patrick-ikebukuro-oct13.pdf" download>Save as PDF</a></div></header>')
js = ('<script>const LI=%d,LUNCH=%s,DAYS=%s,P=%s,GEO=[[35.6985,139.7585,"Kanda"],[35.7345,139.7158,"Ikebukuro"]];'
      % (LI, json.dumps(LUNCH_JS), json.dumps(['The whole day'] + [p[5] for p in P[1:]]), json.dumps([None] + [[p[0], p[1], p[2], p[3], p[4], 0] for p in P[1:]])))
js += open('map.js').read() + '</script>'
dev = '<script>window.DEVBAR_FORCE=innerWidth>=900</script><script src="devbar.js"></script>' if DEVBAR else '<script src="devbar.js"></script>'
open('index.html', 'w').write(head + intro + ''.join(S) + night + credit + '</main></div>' + js + dev + '</body></html>')
