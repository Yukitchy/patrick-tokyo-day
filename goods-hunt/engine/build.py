#!/usr/bin/env python3
"""goods-hunt: config.json -> guest page (index.html) + show-the-staff card (card.png) + A4 one-sheet PDF + og.jpg.
Usage: /usr/local/bin/python3 engine/build.py jobs/<name>/config.json      (needs Pillow, qrcode, playwright chromium)
Everything guest-specific lives in config.json and its photos; see ../README.md."""
import sys, os, io, json, shutil, base64, html, urllib.parse
from PIL import Image
import qrcode
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import maplib

HERE = os.path.dirname(os.path.abspath(__file__))
E = lambda s: html.escape(str(s), quote=True)
gm = lambda q: 'https://www.google.com/maps/search/?api=1&query=' + urllib.parse.quote_plus(q)

def card_sentences(c):
    """The Japanese lines the guest shows to staff (+ English gloss)."""
    out = [(c['card']['generic_ja'], c['card']['generic_en'])]
    for ch in c['characters']:
        out.append((f"{ch['ja']}（『{ch['series_ja']}』）の{ch['want_ja']}を探しています",
                    f"I am looking for a plush or figure of {ch['en']} (from {ch['series_en']})." if ch['want_ja'].startswith('ぬいぐるみやフィギュア')
                    else f"I am looking for plush or goods of {ch['en']} (from {ch['series_en']})."))
    out.append((c['card']['used_ja'], c['card']['used_en']))
    return out

# ---------------------------------------------------------------- maps
def make_maps(c, outdir):
    paths = {}
    stops = {s['n']: s for s in c['stops']}
    for m in c['maps']:
        ss = [s for s in c['stops'] if s['map'] == m['id']]
        pins = [(s['n'], s['label'], s['lat'], s['lon']) for s in ss]
        legs = []
        for a, b in zip(ss, ss[1:]):
            if a['leg'] == 'foot': legs.append(('foot', maplib.foot((a['lat'], a['lon']), (b['lat'], b['lon']))))
            elif a['leg'] == 'train': legs.append(('train', [(a['lat'], a['lon']), (b['lat'], b['lon'])]))
        st = [(n, la, lo) for n, la, lo in m.get('stations', [])]
        W, H = (1000, 480) if m['id'] == 'A' else (1000, 480)
        p = os.path.join(outdir, f"map_{m['id']}.png")
        maplib.render(p, W, H, pins, legs, st, zmax=m.get('zmax', 17)); paths[m['id']] = p
    return paths

# ---------------------------------------------------------------- page
def build_page(c, job, outdir):
    ch = c['characters']; ex = c.get('extra_photos', [])
    os.makedirs(outdir + '/img', exist_ok=True)
    for p in [x['photo'] for x in ch] + [x['photo'] for x in ex]:
        shutil.copy(os.path.join(job, p), outdir + '/img/' + os.path.basename(p))
    img = lambda p: 'img/' + os.path.basename(p)
    css = open(HERE + '/page.css', encoding='utf8').read() + open(HERE + '/extra.css', encoding='utf8').read()
    url = c['base_url']
    hero = ''.join(f'<figure><img src="{img(x["photo"])}" alt="{E(x["caption"])}"><figcaption>{E(x["caption"])}</figcaption></figure>' for x in ch)
    honest = ''.join(f'<li>{E(t)}</li>' for t in c['honest'])
    sents = ''.join(f'<li><span class="ja" lang="ja">{E(j)}</span><span class="en">{E(e)}</span></li>' for j, e in card_sentences(c))
    stops = c['stops']
    tl = ''.join(f'<li><b>{s["n"]}</b><span><a href="#s{s["n"]}">{s["n"]} {E(s["name"])}</a><em>{E(s["next"]) if s["next"] else "Done. Head back to your hotel."}</em></span></li>' for s in stops)
    tiles = ''
    cards = ''
    for s in stops:
        btns = f'<a class="btn" href="{gm(s["q"])}" target="_blank" rel="noopener">Google Maps <i>&rarr;</i></a>' + (f'<a class="btn" href="{E(s["url"])}" target="_blank" rel="noopener">Shop page <i>&nearr;</i></a>' if s['url'] else '')
        cards += (f'<article class="card" id="s{s["n"]}"><div class="hd"><span class="big">{s["n"]:02d}</span><div><span class="genre">{E(s["tag"])}</span>'
                  f'<h3>{E(s["name"])}</h3><p class="jp" lang="ja">{E(s["jp"])}</p></div></div>'
                  f'<p class="strip"><span><b class="today">{E(s["area"])}</b></span></p>'
                  f'<p class="tx look"><b>What to look for.</b> {E(s["look"])}</p><p class="hrs">{E(s["hours"])}</p><div class="bt">{btns}</div></article>')
    maps = ''.join(f'<h3 class="mh">{E(m["label"])}</h3><img class="rmap" src="img/map_{m["id"]}.png" alt="Route map: {E(m["label"])}">' for m in c['maps'])
    online = ''.join(f'<li><a href="{E(o["url"])}" target="_blank" rel="noopener"><b>{E(o["name"])}</b> &nearr;</a><span>{E(o["text"])}</span></li>' for o in c['online'])
    tip = c['tip']
    credits = ''.join(f'<li>{E(x["credit"])}</li>' for x in ch + ex)
    exph = ''.join(f'<img src="{img(x["photo"])}" alt="">' for x in ex)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(c["title"])}</title><meta name="robots" content="noindex,nofollow"><meta name="description" content="{E(c["intro"])}">
<meta property="og:title" content="{E(c["title"])}"><meta property="og:description" content="{E(c["date_line"])}"><meta property="og:type" content="website"><meta property="og:url" content="{url}">
<meta property="og:image" content="{url}og.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 64 64%22%3E%3Crect width=%2264%22 height=%2264%22 fill=%22%23D9342B%22/%3E%3C/svg%3E">
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&family=Noto+Sans+JP:wght@500;700;900&display=swap" rel="stylesheet">
<style>{css}</style></head><body>
<div class="col"><div class="top"><span>{E(c["kicker"])}</span><span class="topr"><span>TOKYO &middot; {len(stops)} SHOPS</span></span></div>
<h1>{E(c["title"])}</h1></div>
<div class="col" style="padding:0"><div class="duo">{hero}</div><div class="hb"><span>{E(c["date_line"])}</span><b>Made for {E(c["guest"]["for"])} &middot; guide: {E(c["guide"])}</b></div></div>
<div class="col"><p class="lead">{E(c["intro"])}</p>
<div class="honest"><h2>{E(c["honest_title"])}</h2><ul>{honest}</ul><p>{E(c["already_tried"])}</p></div>
<section class="showcard" id="card"><span class="tagline">Most useful thing on this page</span><h2>{E(c["card"]["title"])}</h2>
<p class="cs">Open this on your phone and hand it to a clerk, or save the picture. The photos are the official product pictures.</p>
<img class="cardimg" src="card.png" alt="Card with photos of Boxxo and Sui and Japanese sentences for shop staff">
<div class="bt"><a class="btn" href="card.png" download="show-the-staff-card.png">Save the card (PNG) <i>&darr;</i></a></div>
<ol class="sent">{sents}</ol></section>
<div class="bar"><h2>THE DAY</h2><span>{len(stops)} stops</span></div><ul class="tl">{tl}</ul>
<div class="maphd"><h2 class="map">The map</h2></div>{maps}
<p class="gp">Dashed line: train. Red line: walking. Map data &copy; OpenStreetMap contributors.</p>
<div class="bt"><a class="btn" href="{E(c["pdf_name"])}" target="_blank" rel="noopener">Open the one-page PDF (A4) <i>&nearr;</i></a></div></div>
<div class="col">{cards}</div>
<div class="know"><div class="col"><h2>{E(c["online_title"]).upper()}</h2><ul class="onl">{online}</ul></div></div>
<div class="col"><div class="tipbox"><h2>{E(tip["title"])}</h2><p>{E(tip["text"])}</p><div class="bt"><a class="btn" href="{E(tip["url"])}" target="_blank" rel="noopener">{E(tip["button"])} <i>&nearr;</i></a></div></div>
<p class="note">{E(c["footer_note"])}</p></div>
<div class="crd"><details><summary>Photo credits</summary><div class="exph">{exph}</div><ul>{credits}</ul><p>Product photos belong to their makers and are shown only as a reference for what to look for. Map: &copy; OpenStreetMap contributors.</p></details></div>
</body></html>'''

# ---------------------------------------------------------------- card (phone PNG) + og
def b64(p):
    ext = 'jpeg' if p.lower().endswith(('jpg', 'jpeg')) else 'png'
    return f'data:image/{ext};base64,' + base64.b64encode(open(p, 'rb').read()).decode()

FONTS = '<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=Noto+Sans+JP:wght@500;700;900&display=swap" rel="stylesheet">'

def card_html(c, job):
    chs = ''.join(f'<div class="c"><img src="{b64(os.path.join(job, x["photo"]))}"><b lang="ja">{E(x["ja"])}</b><small>{E(x["en"])}</small></div>' for x in c['characters'])
    sents = ''.join(f'<p class="s"><span lang="ja">{E(j)}</span><small>{E(e)}</small></p>' for j, e in card_sentences(c))
    return f'''<!doctype html><meta charset=utf-8>{FONTS}<style>*{{box-sizing:border-box}}body{{margin:0;width:1080px;background:#F1EFEA;font:28px/1.4 "Noto Sans JP",Archivo,sans-serif;color:#121212}}
.h{{background:#D9342B;color:#fff;padding:34px 44px;font:900 54px/1 Archivo,"Noto Sans JP";font-stretch:70%;letter-spacing:.01em;text-transform:uppercase}}.h small{{display:block;margin-top:10px;font:700 28px "Noto Sans JP";text-transform:none;letter-spacing:0}}
.cs{{display:flex;gap:24px;padding:36px 44px 8px}}.c{{flex:1;background:#fff;border:4px solid #121212;text-align:center;padding-bottom:18px}}.c img{{display:block;width:100%;aspect-ratio:1/1;object-fit:cover}}
.c b{{display:block;margin-top:14px;font-size:62px;font-weight:900;line-height:1.1}}.c small{{display:block;font-size:24px;color:#5D5A54;font-weight:700}}
.t{{padding:20px 44px 40px}}.s{{margin:0 0 20px;background:#fff;border-left:12px solid #D9342B;padding:18px 24px}}.s span{{display:block;font-size:37px;font-weight:900;line-height:1.35}}.s small{{display:block;margin-top:6px;font-size:22px;color:#5D5A54}}
.f{{padding:0 44px 34px;font-size:20px;color:#5D5A54}}</style>
<div class="h">{E(c["card"]["title"])}<small>店員さんに見せてください</small></div><div class="cs">{chs}</div><div class="t">{sents}</div><div class="f">Product photos: Good Smile Company / Overlap. Reference only.</div>'''

def og_html(c, job):
    imgs = ''.join(f'<img src="{b64(os.path.join(job, x["photo"]))}">' for x in c['characters'])
    return f'''<!doctype html><meta charset=utf-8>{FONTS}<style>body{{margin:0;width:1200px;height:630px;background:#F1EFEA;display:flex;font-family:Archivo,"Noto Sans JP";overflow:hidden}}
.l{{width:620px;padding:56px 48px;display:flex;flex-direction:column;justify-content:space-between;background:#D9342B;color:#fff}}.l h1{{font:900 84px/.95 Archivo;font-stretch:62%;text-transform:uppercase;margin:0}}.l p{{font:800 26px Archivo;letter-spacing:.1em;margin:0}}
.r{{flex:1;display:flex}}.r img{{width:50%;height:100%;object-fit:cover}}</style><div class="l"><p>GUEST GUIDE &middot; TOKYO</p><h1>{E(c["title"])}</h1><p>{E(c["date_line"])}</p></div><div class="r">{imgs}</div>'''

# ---------------------------------------------------------------- PDF sheet
def sheet_html(c, job, maps, outdir):
    qr = io.BytesIO(); qrcode.make(c['base_url'], box_size=6, border=1).save(qr, 'PNG'); qrb = base64.b64encode(qr.getvalue()).decode()
    stops = c['stops']; ch = c['characters']; ex = c.get('extra_photos', [])
    photos = ''.join(f'<div><img src="{b64(os.path.join(job, x["photo"]))}"></div>' for x in ch + ex)
    n = len(stops)
    band = f'<div class="s first"><b>1</b>{E(stops[0]["label"])}</div>' + ''.join(
        f'<div class="s{" last" if i == n - 2 else ""}"><b>{i + 2}</b>{E(s["label"])}</div>' for i, s in enumerate(stops[1:]))
    rows = ''.join(f'<li><i>{s["n"]}</i><span>{E(s["name"])}</span><small>{E(s["tag"])}</small></li>' for s in stops)
    on = ''.join(f'<li><span><b>{E(o["name"])}</b></span></li>' for o in c['online'])
    sents = ''.join(f'<p><span lang="ja">{E(j)}</span></p>' for j, _ in card_sentences(c))
    chcards = ''.join(f'<div class="c"><img src="{b64(os.path.join(job, x["photo"]))}"><b lang="ja">{E(x["ja"])}</b><small>{E(x["en"])}</small></div>' for x in ch)
    mp = ''.join(f'<div class="mp"><img src="{b64(maps[m["id"]])}"><span>{E(m["label"])}</span></div>' for m in c['maps'])
    return f'''<!doctype html><meta charset=utf-8><title>{E(c["title"])}</title>{FONTS}
<style>@page{{size:A4 landscape;margin:0}}*{{box-sizing:border-box}}html,body{{margin:0;padding:0}}body{{font:11px/1.4 Archivo,"Noto Sans JP",sans-serif;color:#111}}
article{{width:297mm;height:209mm;padding:8mm 11mm;overflow:hidden;display:flex;flex-direction:column}}
header{{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:2.5px solid #111;padding-bottom:4px;gap:14px;flex:none}}
h1{{font:900 36px/1 Archivo;font-stretch:75%;margin:0;white-space:nowrap}}.meta{{text-align:right;font-weight:700;font-size:13px}}
.ph{{display:grid;grid-template-columns:repeat({len(ch+ex)},1fr);gap:6px;margin-top:7px;height:18mm;flex:none}}.ph div{{min-height:0;overflow:hidden;background:#eee}}.ph img{{display:block;width:100%;height:100%;object-fit:cover;object-position:50% 25%}}
.band{{display:flex;margin-top:7px;flex:none}}.s{{flex:1;background:#e4e0d2;padding:5px 12px;font-size:10.5px;line-height:1.2;font-weight:600;min-height:15mm;clip-path:polygon(0 0,calc(100% - 9px) 0,100% 50%,calc(100% - 9px) 100%,0 100%,9px 50%);margin-right:-4px}}
.s b{{display:block;font-size:16px;font-weight:900}}.s.first{{background:#D9342B;color:#fff;clip-path:polygon(0 0,calc(100% - 9px) 0,100% 50%,calc(100% - 9px) 100%,0 100%)}}.s.last{{background:#111;color:#fff}}
.low{{display:grid;grid-template-columns:94mm 54mm 1fr;gap:9px;margin-top:8px;flex:1;min-height:0}}
.maps{{display:flex;flex-direction:column;gap:6px;min-height:0}}.mp{{position:relative;flex:none}}.mp img{{width:100%;aspect-ratio:1000/480;object-fit:cover;border:2px solid #111;display:block}}.mp span{{position:absolute;left:0;top:0;background:#111;color:#fff;font:800 9px Archivo;padding:2px 6px;letter-spacing:.06em;text-transform:uppercase}}
.mid{{display:flex;flex-direction:column;min-height:0}}h2{{font:900 14px Archivo;margin:0 0 3px;text-transform:uppercase}}
ul{{list-style:none;margin:0 0 6px;padding:0}}li{{display:flex;align-items:center;gap:6px;margin-bottom:3px;font-size:10px;font-weight:700;line-height:1.15}}li small{{display:block;max-width:19mm;font-size:8px;font-weight:500;color:#777}}li span{{flex:1}}
li i{{flex:none;width:17px;height:17px;border-radius:50%;background:#111;color:#fff;font:800 10px/17px Archivo;text-align:center;font-style:normal}}
.cardbox{{display:flex;flex-direction:column;min-height:0}}.card{{flex:1;min-height:0;border:3px solid #D9342B;padding:8px 10px;display:flex;flex-direction:column;gap:7px}}
.chs{{display:flex;gap:8px;flex:none}}.chs .c{{flex:1;border:2px solid #111;text-align:center}}.chs img{{display:block;width:100%;height:46mm;object-fit:cover}}.chs b{{display:block;font:900 19px/1.15 "Noto Sans JP"}}.chs small{{display:block;font:700 9.5px Archivo;color:#555;padding-bottom:3px}}
.tx{{flex:1;min-height:0;display:flex;flex-direction:column;justify-content:space-between}}.tx p{{margin:0;border-left:4px solid #D9342B;padding:2px 0 2px 8px;font:800 16.5px/1.4 "Noto Sans JP"}}
.foot{{margin-top:auto;display:flex;gap:8px;align-items:center;font-size:8.5px;color:#555;border-top:1px solid #111;padding-top:4px}}.foot img{{width:17mm;height:17mm;flex:none}}.foot p{{margin:0 0 2px}}</style>
<article><header><h1>{E(c["title"])}</h1><div class="meta">For {E(c["guest"]["for"])} &middot; guide: {E(c["guide"])}<br>{E(c["date_line"])}</div></header>
<div class="ph">{photos}</div><div class="band">{band}</div>
<div class="low"><div class="maps">{mp}<div class="foot"><img src="data:image/png;base64,{qrb}"><div><p><b>Full page, maps and the phone card:</b> {E(c["base_url"].replace("https://", ""))}</p><p>{E(c["footer_note"])}</p></div></div></div><div class="mid"><h2>Route</h2><ul>{rows}</ul>
<h2>{E(c["online_title"])}</h2><ul>{on}</ul>
</div>
<div class="cardbox"><h2>Show this to the staff &middot; 店員さんに見せてください</h2><div class="card"><div class="chs">{chcards}</div><div class="tx">{sents}</div></div></div></div></article>'''

def main(cfg_path):
    job = os.path.dirname(os.path.abspath(cfg_path)); c = json.load(open(cfg_path, encoding='utf8'))
    out = c['out_dir']; os.makedirs(out + '/img', exist_ok=True)
    maps = make_maps(c, out + '/img')
    open(out + '/index.html', 'w', encoding='utf8').write(build_page(c, job, out))
    tmp = os.path.join(job, '_tmp'); os.makedirs(tmp, exist_ok=True)
    pages = {'card': (card_html(c, job), 1080, 800), 'og': (og_html(c, job), 1200, 630), 'sheet': (sheet_html(c, job, maps, out), 1123, 794)}
    for k, (h, w, hh) in pages.items(): open(f'{tmp}/{k}.html', 'w', encoding='utf8').write(h)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(channel='chrome')  # uses installed Google Chrome; no 'playwright install' needed
        def shot(name, w, h, path, full=False, scale=1):
            pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=scale); pg.goto(f'file://{tmp}/{name}.html'); pg.wait_for_load_state('networkidle'); pg.wait_for_timeout(1500)
            pg.screenshot(path=path, full_page=full); return pg
        shot('card', 1080, 800, out + '/card.png', full=True)
        shot('og', 1200, 630, tmp + '/og.png'); Image.open(tmp + '/og.png').convert('RGB').save(out + '/og.jpg', quality=88)
        pg = b.new_page(viewport={'width': 1123, 'height': 794}); pg.goto(f'file://{tmp}/sheet.html'); pg.wait_for_load_state('networkidle'); pg.wait_for_timeout(2500)
        over = pg.evaluate("(()=>{const a=document.querySelector('article'),s=document.querySelector('.cardbox');return [a.scrollHeight>a.clientHeight+1,s.scrollHeight>s.clientHeight+1]})()")
        pdf = out + '/' + c['pdf_name']; pg.pdf(path=pdf, format='A4', landscape=True, print_background=True, prefer_css_page_size=True)
        pg.screenshot(path=tmp + '/sheet.png'); b.close()
    import re; d = open(pdf, 'rb').read()
    print('pdf pages', len(re.findall(rb'/Type\s*/Page[^s]', d)), 'overflow(article,side)', over)
    print('out', out)

if __name__ == '__main__': main(sys.argv[1])
