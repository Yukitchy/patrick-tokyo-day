#!/usr/bin/env python3
"""A4 landscape one-sheet (photo strip + chevron timeline + route maps with arrows) -> patrick-ikebukuro-oct13.pdf/.png
Same design as the adopted model-course sheet (Sample-shibuya.pdf). Needs: Pillow, qrcode, playwright chromium.
Run with /usr/local/bin/python3 (the python that has playwright)."""
import io, os, json, math, time, base64, urllib.request, tempfile
from PIL import Image, ImageDraw, ImageFont
import qrcode

URL = 'https://yukitchy.github.io/patrick-tokyo-day/'
UA = {'User-Agent': 'patrick-route-sheet/1.0 (icchan417@gmail.com)'}
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.mapcache'); os.makedirs(CACHE, exist_ok=True)

# ---- data -------------------------------------------------------------------------------------
STOPS = {1: ('Hotel', 35.6865, 139.7740), 2: ('Koyama Kyugu', 35.6951, 139.7685), 3: ('Animate', 35.7311, 139.7154),
         4: ('Lunch', 35.7295, 139.7124), 5: ('Pokémon Center', 35.7278, 139.7200), 6: ('Disk Union', 35.7287, 139.7138)}
LUNCH = [('a', 'Kikanbo', 'spicy ramen', 35.7291, 139.7153, '11:00-21:30'), ('b', 'Mutekiya', 'tonkotsu ramen', 35.7269, 139.7117, 'from 10:30'),
         ('c', 'Shimizuya', 'pork cutlet', 35.7319, 139.7144, '11:00-20:00'), ('d', 'Wakataka', 'conveyor sushi', 35.7295, 139.7156, '11:30-22:00'),
         ('e', 'Saffron', 'Indian curry', 35.7294, 139.7165, 'lunch 11:00-15:00'), ('f', 'Unatatsu', 'grilled eel', 35.7317, 139.7162, 'lunch 11:30-14:00')]
STN = {'Kanda Stn': (35.69185, 139.77088), 'Awajicho Stn': (35.69470, 139.76751),
       'Ikebukuro Stn': (35.72950, 139.71090), 'Higashi-Ikebukuro Stn': (35.72626, 139.71901)}
HOURS = {1: 'Mitsui Garden Hotel Nihonbashi Premier', 2: 'Open 10:00-19:00', 3: 'Open 10:00-21:00', 5: 'Open 10:00-20:00', 6: 'Open 12:00-20:00'}
NAMES = {1: 'Hotel lobby', 2: 'Koyama Kyugu, bow shop', 3: 'Animate main store', 4: 'Lunch, you pick one of six', 5: 'Pokémon Center Mega Tokyo', 6: 'Disk Union, if it fits'}
LC = {'G': '#f39700', 'M': '#e60012', 'Z': '#8f76d6', 'Y': '#d7c447'}
LN = {'G': 'Ginza Line', 'M': 'Marunouchi Line', 'Z': 'Hanzomon Line', 'Y': 'Yurakucho Line'}
TH = 'https://thumb.wikimedia.org/wikipedia/commons/thumb/'
PHOTOS = [TH + '2/29/Professor_Inagaki_Genshiro.jpg/960px-Professor_Inagaki_Genshiro.jpg', 'https://upload.wikimedia.org/wikipedia/commons/c/c5/ANIMATE-Ikebukuro.JPG',
          TH + '8/8c/Very_hot_tsukemen_%28close-up%29.jpg/960px-Very_hot_tsukemen_%28close-up%29.jpg', TH + 'e/ec/Mega_Tokyo_Pok%C3%A9mon_Center_1.jpg/960px-Mega_Tokyo_Pok%C3%A9mon_Center_1.jpg']
BAND = [('9:30', 'Hotel lobby'), ('9:40', 'Ginza Line to Kanda'), ('10:00', 'Koyama Kyugu bow shop'), ('10:50', 'Marunouchi Line to Ikebukuro'), ('11:30', 'Animate main store'),
        ('12:15', 'Lunch, pick one of six'), ('13:15', 'Pokémon Center'), ('14:15', 'Disk Union, if it fits'), ('14:30', 'Done, in Ikebukuro')]

# ---- map rendering (PIL, OSM tiles, red route + arrows + numbered labelled pins) ----------------
def get(url, binary=False):
    for _ in range(3):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25).read()
            return r if binary else json.loads(r)
        except Exception: time.sleep(2)
def px(lat, lon, z):
    n = 2 ** z * 256
    return (lon + 180) / 360 * n, (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n
def tile(z, x, y):
    p = f'{CACHE}/t_{z}_{x}_{y}.png'
    if not os.path.exists(p):
        open(p, 'wb').write(get(f'https://tile.openstreetmap.org/{z}/{x}/{y}.png', True)); time.sleep(0.15)
    return Image.open(p).convert('RGB')
def foot(a, b):
    p = f'{CACHE}/r_{a[0]:.5f}_{a[1]:.5f}_{b[0]:.5f}_{b[1]:.5f}.json'
    if not os.path.exists(p):
        r = get(f'https://routing.openstreetmap.de/routed-foot/route/v1/foot/{a[1]},{a[0]};{b[1]},{b[0]}?overview=full&geometries=geojson')
        try: line = [[y, x] for x, y in r['routes'][0]['geometry']['coordinates']]
        except Exception: line = [list(a), list(b)]
        json.dump(line, open(p, 'w'))
    return json.load(open(p))
def font(sz):
    for f in ['/System/Library/Fonts/Helvetica.ttc', '/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc']:
        try: return ImageFont.truetype(f, sz)
        except Exception: pass
    return ImageFont.load_default()

def dashed(d, xy, fill, width, on=16, off=12):
    for a, b in zip(xy, xy[1:]):
        L = math.dist(a, b)
        if L == 0: continue
        ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L; t = 0
        while t < L:
            e = min(t + on, L); d.line([(a[0] + ux * t, a[1] + uy * t), (a[0] + ux * e, a[1] + uy * e)], fill=fill, width=width); t += on + off
def arrows(d, xy, fill, every=150, size=17):
    acc = every / 2
    for a, b in zip(xy, xy[1:]):
        L = math.dist(a, b)
        if L == 0: continue
        ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L; pos = 0
        while pos + acc <= L:
            pos += acc; acc = every
            cx, cy = a[0] + ux * pos, a[1] + uy * pos
            tip = (cx + ux * size, cy + uy * size); l = (cx - ux * size * .6 - uy * size * .8, cy - uy * size * .6 + ux * size * .8); r = (cx - ux * size * .6 + uy * size * .8, cy - uy * size * .6 - ux * size * .8)
            d.polygon([tip, l, r], fill=fill, outline='white')
        acc -= (L - pos)

def render(out, W, H, pins, legs, stations, dots=()):
    """pins [(n,label,lat,lon)], legs [(kind,[(lat,lon)..])] kind foot|train, stations [(name,lat,lon)], dots [(letter,lat,lon)]"""
    allpts = [(p[2], p[3]) for p in pins] + [(s[1], s[2]) for s in stations] + [(x[1], x[2]) for x in dots]
    for _, line in legs: allpts += [tuple(q) for q in line]
    lats = [p[0] for p in allpts]; lons = [p[1] for p in allpts]
    z = 17
    while z > 4:
        x0, y1 = px(min(lats), min(lons), z); x1, y0 = px(max(lats), max(lons), z)
        if x1 - x0 < W - 150 and y1 - y0 < H - 150: break
        z -= 1
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; ox, oy = cx - W / 2, cy - H / 2
    img = Image.new('RGB', (W, H), '#ddd')
    for tx in range(int(ox // 256), int((ox + W) // 256) + 1):
        for ty in range(int(oy // 256), int((oy + H) // 256) + 1): img.paste(tile(z, tx, ty), (int(tx * 256 - ox), int(ty * 256 - oy)))
    img = img.convert('RGBA'); d = ImageDraw.Draw(img)
    P = lambda la, lo: (px(la, lo, z)[0] - ox, px(la, lo, z)[1] - oy)
    for kind, line in legs:
        xy = [P(*q) for q in line]
        if kind == 'train': dashed(d, xy, '#444', 7)
        else:
            d.line(xy, fill='white', width=14, joint='curve'); d.line(xy, fill='#e60012', width=8, joint='curve'); arrows(d, xy, '#e60012')
    pinpos = []
    for n, label, la, lo in pins:
        x, y = P(la, lo); pinpos.append((x, y))
        d.ellipse([x - 21, y - 21, x + 21, y + 21], fill='#111', outline='white', width=4); d.text((x, y), str(n), fill='white', font=font(27), anchor='mm')
    occ = [(x - 24, y - 24, x + 24, y + 24) for x, y in pinpos]
    def put(text, x, y, fill, ink, fs, outline):
        ft = font(fs); l, t, r, b = d.textbbox((0, 0), text, font=ft); w, h = r - l + 16, b - t + 10
        for dx, dy in [(26, -h / 2), (-w - 26, -h / 2), (-w / 2, 26), (-w / 2, -h - 26), (26, 10), (-w - 26, 10), (26, -h - 10), (-w - 26, -h - 10)]:
            bx = (x + dx, y + dy, x + dx + w, y + dy + h)
            if bx[0] < 4 or bx[1] < 4 or bx[2] > W - 4 or bx[3] > H - 30: continue
            if any(not (bx[2] < o[0] or bx[0] > o[2] or bx[3] < o[1] or bx[1] > o[3]) for o in occ): continue
            d.rounded_rectangle(bx, radius=8, fill=fill, outline=outline, width=2); d.text((bx[0] + 8, bx[1] + 4 - t), text, fill=ink, font=ft); occ.append(bx); return
    for ltr, la, lo in dots:
        x, y = P(la, lo); d.ellipse([x - 17, y - 17, x + 17, y + 17], fill='white', outline='#e60012', width=5); d.text((x, y), ltr, fill='#e60012', font=font(25), anchor='mm'); occ.append((x - 19, y - 19, x + 19, y + 19))
    for nm, la, lo in stations:
        x, y = P(la, lo); d.ellipse([x - 8, y - 8, x + 8, y + 8], fill='#1d4f91', outline='white', width=3); occ.append((x - 9, y - 9, x + 9, y + 9)); put(nm, x, y, '#1d4f91', 'white', 20, 'white')
    for (n, label, la, lo), (x, y) in zip(pins, pinpos): put(label, x, y, 'white', '#111', 23, '#111')
    d.rectangle([W - 250, H - 24, W, H], fill=(255, 255, 255, 210)); d.text((W - 6, H - 12), '© OpenStreetMap contributors', fill='#333', font=font(16), anchor='rm')
    img.convert('RGB').save(out)

S = lambda n: (STOPS[n][1], STOPS[n][2])
def make_maps():
    k = STN['Kanda Stn']
    render(f'{CACHE}/map_kanda.png', 444, 1000, [(1, 'Hotel', *S(1)), (2, 'Koyama Kyugu', *S(2))],
           [('train', [S(1), k]), ('foot', foot(k, S(2)))], [('Kanda Stn', *k), ('Awajicho Stn', *STN['Awajicho Stn'])])
    legs = [('foot', foot(S(3), S(4))), ('foot', foot(S(4), S(5))), ('foot', foot(S(5), S(6)))]
    render(f'{CACHE}/map_ike.png', 952, 1000, [(3, 'Animate', *S(3)), (4, 'Lunch', *S(4)), (5, 'Pokémon Center', *S(5)), (6, 'Disk Union', *S(6))], legs,
           [('Higashi-Ikebukuro Stn', *STN['Higashi-Ikebukuro Stn'])], [(l[0], l[3], l[4]) for l in LUNCH])

# ---- html ---------------------------------------------------------------------------------------
chip = lambda k: f'<b class="lc" style="background:{LC[k]}">{k}</b>'
def leg(txt): return f'<li class="leg"><u></u>{txt}</li>'
def build_html():
    b64 = lambda p: 'data:image/png;base64,' + base64.b64encode(open(p, 'rb').read()).decode()
    q = qrcode.make(URL, box_size=6, border=1); bb = io.BytesIO(); q.save(bb, 'PNG'); qr = base64.b64encode(bb.getvalue()).decode()
    band = ''.join(f'<div class="s{" first" if i == 0 else " last" if i == len(BAND) - 1 else ""}"><b>{t}</b>{x}</div>' for i, (t, x) in enumerate(BAND))
    photos = ''.join(f'<div><img src="{u}" alt=""></div>' for u in PHOTOS)
    rows = f'<li><i>1</i>{NAMES[1]}<small>{HOURS[1]}</small></li>' + leg(f'{chip("G")}{LN["G"]} to Kanda, 2 min, then walk 5 min')
    rows += f'<li><i>2</i>{NAMES[2]}<small>{HOURS[2]}</small></li>' + leg(f'{chip("M")}{LN["M"]}, Awajicho to Ikebukuro, 17 min')
    rows += f'<li><i>3</i>{NAMES[3]}<small>{HOURS[3]}</small></li>' + leg('walk 2 to 10 min to lunch')
    rows += f'<li><i>4</i>{NAMES[4]}<small>see a to f</small></li>' + leg(f'walk, or {chip("Y")}{LN["Y"]}, 1 stop')
    rows += f'<li><i>5</i>{NAMES[5]}<small>{HOURS[5]}</small></li>' + leg('walk 10 min')
    rows += f'<li><i>6</i>{NAMES[6]}<small>{HOURS[6]}</small></li>'
    rows += f'<li class="back"><span>Back to Nihonbashi, 30 min:</span>{chip("M")}Marunouchi to Otemachi, {chip("Z")}Hanzomon to Mitsukoshimae</li>'
    lunch = ''.join(f'<li><i class="l">{a}</i><span><b>{n}</b> {g}</span><small>{h}</small></li>' for a, n, g, _, _, h in LUNCH)
    return f'''<!doctype html><meta charset=utf-8><title>Tokyo, Tuesday October 13</title>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&display=swap" rel="stylesheet">
<style>@page{{size:A4 landscape;margin:0}}*{{box-sizing:border-box}}html,body{{margin:0;padding:0}}body{{font:11px/1.4 Archivo,-apple-system,"Hiragino Sans",sans-serif;color:#111}}
article{{width:297mm;height:209mm;padding:8mm 11mm;overflow:hidden;display:flex;flex-direction:column}}
header{{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:2.5px solid #111;padding-bottom:4px;gap:14px;flex:none}}
h1{{font:900 40px/1 Archivo;font-stretch:75%;margin:0;white-space:nowrap}}.meta{{text-align:right;font-weight:700;font-size:14px}}
.chips span{{display:inline-block;border:1px solid #111;border-radius:12px;padding:0 9px;margin:4px 0 0 5px;font-size:11.5px}}
.ph{{display:grid;grid-template-columns:1.3fr 1.3fr 1fr 1fr;gap:6px;margin-top:7px;height:32mm;flex:none}}.ph div{{min-height:0;overflow:hidden}}.ph img{{display:block;width:100%;height:100%;object-fit:cover}}
.band{{display:flex;margin-top:7px;flex:none}}.s{{flex:1;background:#e4e0d2;padding:5px 12px 5px 12px;font-size:10.5px;line-height:1.2;font-weight:600;min-height:16mm;clip-path:polygon(0 0,calc(100% - 9px) 0,100% 50%,calc(100% - 9px) 100%,0 100%,9px 50%);margin-right:-4px}}
.s b{{display:block;font-size:16px;font-weight:900}}.s.first{{background:#e60012;color:#fff;clip-path:polygon(0 0,calc(100% - 9px) 0,100% 50%,calc(100% - 9px) 100%,0 100%)}}.s.last{{background:#111;color:#fff}}
.low{{display:grid;grid-template-columns:56mm 120mm 1fr;gap:8px;margin-top:8px;flex:1;min-height:0}}
.map{{width:100%;height:100%;object-fit:cover;border:2px solid #111;display:block;min-height:0}}
.side{{display:flex;flex-direction:column;min-height:0}}h2{{font:900 17px Archivo;margin:0 0 3px}}
ul{{list-style:none;margin:0 0 4px;padding:0}}li{{display:flex;align-items:center;gap:6px;margin-bottom:2px;font-size:11.5px;font-weight:700;line-height:1.15}}li small{{margin-left:auto;font-size:9.5px;font-weight:500;color:#777;text-align:right;white-space:nowrap}}
li.leg{{margin:0 0 2px 5px;font-size:10.5px;font-weight:600;color:#555}}li.leg u{{flex:none;border-left:3px solid #e60012;height:12px;margin-left:8px;margin-right:2px}}
li i{{flex:none;width:19px;height:19px;border-radius:50%;background:#111;color:#fff;font:800 11px/19px Archivo;text-align:center;font-style:normal}}li i.l{{background:#fff;color:#e60012;border:2px solid #e60012;line-height:15px}}
.lc{{display:inline-block;flex:none;width:15px;height:15px;border-radius:50%;color:#fff;font:800 9px/15px Archivo;text-align:center;margin-right:3px}}
.back{{display:block;margin:2px 0 0 5px;font-size:10px;font-weight:600;color:#555;line-height:1.5}}.back span{{display:block}}.lunch li{{font-size:10.5px;font-weight:500;margin-bottom:1px}}.lunch li b{{font-weight:800}}
.foot{{display:flex;gap:8px;align-items:center;margin-top:auto;font-size:9.5px;color:#555;border-top:1px solid #111;padding-top:4px}}.foot img{{width:17mm;height:17mm;flex:none}}.foot p{{margin:0 0 2px}}</style>
<article><header><h1>Tokyo, Tuesday October 13</h1><div class="meta">Guide: Yuuki · meet 9:30, done about 14:30<div class="chips"><span>Bow shop</span><span>Anime</span><span>Pokémon</span><span>Lunch: you pick</span></div></div></header>
<div class="ph">{photos}</div><div class="band">{band}</div>
<div class="low"><img class="map" src="{b64(CACHE + '/map_kanda.png')}" alt=""><img class="map" src="{b64(CACHE + '/map_ike.png')}" alt="">
<div class="side"><h2>Route</h2><ul>{rows}</ul><h2>Lunch, pick one</h2><ul class="lunch">{lunch}</ul>
<div class="foot"><img src="data:image/png;base64,{qr}"><div><p><b>Full plan and maps:</b> yukitchy.github.io/patrick-tokyo-day</p><p>Tonight: Castle Gate (19-24, closed Sun/Mon), LANDSROCK (19-5, closed Sun).</p></div></div></div></div></article>'''

def main():
    make_maps()
    html = build_html(); tmp = os.path.join(tempfile.gettempdir(), 'patrick-sheet.html'); open(tmp, 'w').write(html)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1123, 'height': 794}); pg.goto('file://' + tmp); pg.wait_for_load_state('networkidle'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(2500)
        over = pg.evaluate("(()=>{const a=document.querySelector('article'),s=document.querySelector('.side');return [a.scrollHeight>a.clientHeight+1, s.scrollHeight>s.clientHeight+1]})()")
        pg.pdf(path='patrick-ikebukuro-oct13.pdf', format='A4', landscape=True, print_background=True, prefer_css_page_size=True)
        pg.screenshot(path='patrick-ikebukuro-oct13.png', full_page=False); b.close()
    import re; d = open('patrick-ikebukuro-oct13.pdf', 'rb').read()
    print('pages', len(re.findall(rb'/Type\s*/Page[^s]', d)), 'overflow(article,side)', over)

if __name__ == '__main__': main()
