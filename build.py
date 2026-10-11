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
    shimizuya=TH + '1/15/Pork_loin_cutlet_set_meal_of_Katsuya.jpg/960px-Pork_loin_cutlet_set_meal_of_Katsuya.jpg',
    wakataka=TH + '2/27/Conveyor_belt_sushi_at_Mashiro_Sushi.jpg/960px-Conveyor_belt_sushi_at_Mashiro_Sushi.jpg',
    saffron='https://upload.wikimedia.org/wikipedia/commons/0/09/NANAK_lunch_set.jpg',
    unatatsu='https://upload.wikimedia.org/wikipedia/commons/b/b6/Unadon_%E3%81%86%E3%81%AA%E4%B8%BC.jpg')

# lat, lon, full name, short label, label side, time  (coordinates from GSI geocoder / Tabelog)
P = [None,
     (35.6865, 139.7740, 'Hotel lobby, Nihonbashi', 'Hotel', 'r', '9:30'),
     (35.6951, 139.7685, 'Koyama Kyugu, Kanda', 'Koyama', 'r', '10:00'),
     (35.7311, 139.7154, 'Animate Ikebukuro', 'Animate', 'r', '11:30'),
     (35.7295, 139.7124, 'Lunch, pick one of six', '', 'r', '12:15'),
     (35.7278, 139.7200, 'Pokémon Center Mega Tokyo', 'Pokémon Center', 'r', '13:15'),
     (35.7287, 139.7138, 'Disk Union Ikebukuro (if it fits)', 'Disk Union', 'l', '14:15')]
LI = 4
# lunch options: name, lat, lon, label side, photo, photo credit, genre, Tabelog score, short note, hours, walk min from Animate, map query, details url
LUNCH = [
    ('Kikanbo', 35.7291, 139.7153, 't', 'kikanbo', 'Very hot tsukemen (close-up).jpg by insatiablemunch, CC BY 2.0', 'Spicy ramen', '3.6',
     'Spicy miso ramen. You choose how hot and how numbing it is, or ask for mild. Counter seats only.',
     'Open 11:00 to 21:30', 4, 'Kikanbo Ikebukuro', 'https://kikanbo.co.jp/pages/shop'),
    ('Mutekiya', 35.7269, 139.7117, 'b', 'mutekiya', 'Ikkousha tonkotsu bowl.jpg by Wesoree, CC BY-SA 4.0', 'Tonkotsu ramen', '3.6',
     'Rich pork-bone ramen with thick roast pork. 17 counter seats, so expect a line. Closes when the soup runs out.',
     'Open from 10:30', 10, 'Mutekiya Ikebukuro', 'https://tabelog.com/tokyo/A1305/A130501/13003927/'),
    ('Shimizuya', 35.7319, 139.7144, 'r', 'shimizuya', 'Pork loin cutlet set meal of Katsuya.jpg by 毒島みるく, CC0', 'Pork cutlet', '3.5',
     'Tonkatsu (breaded pork cutlet) set meals, plus katsudon and curry. On the 2nd floor of a building near the east exit.',
     'Open 11:00 to 20:00', 3, 'Shimizuya Ikebukuro tonkatsu', 'https://tabelog.com/tokyo/A1305/A130501/13008961/'),
    ('Wakataka', 35.7295, 139.7156, 'l', 'wakataka', 'Conveyor belt sushi at Mashiro Sushi.jpg by JIP, CC BY-SA 4.0', 'Conveyor sushi', '3.5',
     'Conveyor-belt sushi that scores higher on Tabelog than the big chains. On Sunshine 60 Street, right by Animate.',
     'Open 11:30 to 22:00', 4, 'Mawashizushi Wakataka Ikebukuro Sunshine 60', 'https://tabelog.com/tokyo/A1305/A130501/13009868/'),
    ('Saffron', 35.7294, 139.7165, 'b', 'saffron', 'NANAK lunch set.jpg by OpenCage Systems, CC BY-SA 2.0', 'Indian curry', '3.4',
     'North Indian curry and naan, if you want a change from Japanese food. Lunch ends at 15:00.',
     'Lunch 11:00 to 15:00', 4, 'Saffron Ikebukuro', 'https://tabelog.com/tokyo/A1305/A130501/13100839/'),
    ('Unatatsu', 35.7317, 139.7162, 'r', 'unatatsu', 'Unadon うな丼.jpg by masa from JAPAN, CC BY 2.0', 'Grilled eel', '3.5',
     'Grilled eel (unagi) on rice. Lunch is 11:30 to 14:00. Closed on Sundays and holidays.',
     'Lunch 11:30 to 14:00', 2, 'Unatatsu Ikebukuro', 'https://tabelog.com/tokyo/A1305/A130501/13037960/'),
]
LUNCH_JS = [[l[1], l[2], l[0], l[3]] for l in LUNCH]

TT = [('9:30', 'Hotel lobby'), ('9:40', 'Ginza Line to Kanda'), ('10:00', 'Koyama Kyugu bow shop'),
      ('10:50', 'Marunouchi to Ikebukuro'), ('11:30', 'Animate main store'), ('12:15', 'Lunch, you pick one of six'),
      ('13:15', 'Pokémon Center'), ('14:15', 'Disk Union, if it fits'), ('14:30', 'Done, in Ikebukuro')]
tt = ''.join(f'<tr class="st-plain"><td class="v">{t}</td><td><span class="k">{k}</span></td></tr>' for t, k in TT)

def step(i, h, body):
    t = P[i][5]
    return f'<article class="step" data-i="{i}"><p class="no"><i>{i}</i>{t}</p><h2>{h}</h2>{body}</article>'

POPS = []
def lunch_card(l):
    name, _, _, _, img, cred, genre, score, what, hours, walk, q, url = l
    pid = 'pop-' + name.lower()
    POPS.append(f'<dialog class="pop" id="{pid}" aria-label="{name}"><button type="button" class="pclose" aria-label="Close">✕</button>'
                f'<img class="pimg" src="{IMG[img]}" alt="Example photo: {genre.lower()}"><div class="pbody"><p class="gn">{genre}</p><h3>{name}</h3>'
                f'<p class="rt"><span class="st">★ {score}</span> Tabelog</p><p class="pt">{what}</p>'
                f'<p class="rt">{hours}<br>About {walk} min on foot from Animate</p>'
                f'<p class="pl"><a href="{gm(q)}" target="_blank" rel="noopener">Map ↗</a><a href="{url}" target="_blank" rel="noopener">Details ↗</a></p>'
                f'<p class="pc">Photo: example of the dish, not the shop. {cred}</p></div></dialog>')
    return (f'<button type="button" class="tile" data-pop="{pid}"><img src="{IMG[img]}" alt="Example photo: {genre.lower()}" loading="lazy">'
            f'<span class="cb"><span class="gn">{genre}</span><b>{name}</b></span></button>')

S = []
S.append(f'<article class="step" data-i="0"><p class="no"><i>0</i>The whole day</p><h2>One route, <span class="l2">9:30 to <em>14:30</em></span></h2>'
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
              + nxt(f'{ln("G")} to Kanda, 2 min + 5 min walk')))
S.append(step(2, 'The <em>bow maker</em>', ph(IMG['kyudo'], 'An archer in hakama at full draw')
              + '<p class="lead">Koyama Kyugu has made bows for over 200 years and has its own workshop for bows, arrows and gloves. We arrive when it opens at 10:00, so the shop is calm. You can hold the bows and ask the staff anything. This is the main morning stop, so we take our time.</p>'
              '<div class="cafes"><div class="cf"><div class="cb"><b>Koyama Kyugu, Kanda main store</b><p class="rt"><span class="st">★ 4.2</span> · 217 Google reviews</p><p>Open Tuesday 10:00 to 19:00.</p><small>Rating from Google Maps, October 2026.</small></div></div></div>'
              '<p class="note" style="font-size:14px">The Kanda Myojin shrine is a short walk away. If we have a few minutes, we stop by.</p>'
              + links(('Koyama Kyugu on Google Maps', gm('Koyama Kyugu Kanda')), ('Official site', 'https://koyama-kyugu.co.jp/store/'), ('Kanda Myojin', gm('Kanda Myojin')))
              + nxt(f'{ln("M")} to Ikebukuro, 17 min')))
S.append(step(3, '<em>Animate</em> Ikebukuro', ph(IMG['animate'], 'The Animate Ikebukuro main store building')
              + '<p class="lead">Animate is Japan\'s biggest anime shop chain. The main store is about 5 minutes on foot from the east exit of Ikebukuro station: manga, character goods, and anime shops on the streets around it.</p>'
              + nums(('Open', '10:00 to 21:00', 'Tuesday'))
              + links(('Animate on Google Maps', gm('Animate Ikebukuro Main Store')), ('Official site', 'https://www.animate.co.jp/shop/ikebukuro/'))
              + nxt('Walk to lunch, 2 to 10 min. You choose next.')))
S.append(step(4, '<em>Lunch</em>, pick one of six',
              '<p class="lead">Six places in Ikebukuro, all open at lunchtime on Tuesday: two noodle shops and four other kinds of food. Tap a tile for details. Tell me which one you feel like and we go.</p>'
              '<div class="cafes tiles">' + ''.join(lunch_card(l) for l in LUNCH) + '</div>'
              '<p class="asof">Scores are from Tabelog, October 2026. Tabelog scores run lower than Google, and 3.5 is already very good.</p>'
              + nxt('Walk, or ' + ln('Y') + ' 1 stop')))
S.append(step(5, '<em>Pokémon Center</em>', ph(IMG['poke'], 'Inside the Pokémon Center Mega Tokyo')
              + '<p class="lead">The Pokémon Center Mega Tokyo is on the second floor of the Alpa shopping area in Sunshine City, the biggest Pokémon store in Tokyo. We have about an hour here.</p>'
              + nums(('Open', '10:00 to 20:00', 'Tuesday'))
              + links(('Pokémon Center on Google Maps', gm('Pokemon Center Mega Tokyo Sunshine City')), ('Official site', 'https://shop.pokemon.co.jp/ja/shop/pokemoncenter-megatokyo/'))
              + nxt('Walk 10 min, or ' + ln('Y') + ' 1 stop')))
S.append(step(6, '<em>Metal</em> records, and done',
              '<p class="lead">Disk Union Ikebukuro has rock and metal records and band T-shirts, new and used. We only go if we still have time and energy. If not, we finish at the Pokémon Center. Either way we are done around 14:30 in Ikebukuro, and we can split here.</p>'
              + nums(('Open', '12:00 to 20:00', 'Tuesday'))
              + links(('Disk Union on Google Maps', gm('Disk Union Ikebukuro')), ('Official site', 'https://diskunion.net/shop/ikebukuro'))
              + nxt(ln('M') + ' to Otemachi', ln('Z') + ', 30 min in all')))
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
         '<main class="story"><header class="intro"><p class="date">Tuesday, October 13 · 9:30 to 14:30</p><h1>Your day in Tokyo</h1><p class="who">Patrick, with Yuuki. Kanda and Ikebukuro: a bow maker, anime, Pokémon, and a lunch you choose.</p>'
         '<dl class="cn"><div><dt>Meet</dt><dd class="n">9:30</dd><dd class="s">Hotel lobby</dd></div><div><dt>Finish</dt><dd class="n">14:30</dd><dd class="s">Ikebukuro</dd></div></dl>'
         '<div class="tools"><a class="tool" href="patrick-ikebukuro-oct13.pdf" download>Save as PDF</a></div></header>')
js = ('<script>const LI=%d,LUNCH=%s,DAYS=%s,P=%s,GEO=[[35.6985,139.7585,"Kanda"],[35.7345,139.7158,"Ikebukuro"]];'
      % (LI, json.dumps(LUNCH_JS), json.dumps(['The whole day'] + [p[5] for p in P[1:]]), json.dumps([None] + [[p[0], p[1], p[2], p[3], p[4], 0] for p in P[1:]])))
js += open('map.js').read() + '</script>'
dev = '<script>window.DEVBAR_FORCE=innerWidth>=900</script><script src="devbar.js"></script>' if DEVBAR else '<script src="devbar.js"></script>'
popjs = ("<script>document.querySelectorAll('.tile').forEach(function(t){t.addEventListener('click',function(){document.getElementById(t.dataset.pop).showModal()})});"
         "document.querySelectorAll('dialog.pop').forEach(function(d){d.addEventListener('click',function(e){if(e.target===d)d.close()});d.querySelector('.pclose').addEventListener('click',function(){d.close()})});</script>")
open('index.html', 'w').write(head + intro + ''.join(S) + night + credit + '</main></div>' + ''.join(POPS) + js + popjs + dev + '</body></html>')
