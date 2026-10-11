#!/usr/bin/env python3
"""One-page A4 summary -> patrick-ikebukuro-oct13.pdf/.png (needs playwright chromium + qrcode)"""
import qrcode,io,base64,json
URL='https://yukitchy.github.io/patrick-tokyo-day/'
q=qrcode.make(URL,box_size=6,border=1);b=io.BytesIO();q.save(b,'PNG');qr=base64.b64encode(b.getvalue()).decode()
# n, name, lat, lon, hours on Tue Oct 13
PL=[(1,'Hotel lobby',35.6882,139.7735,'Mitsui Garden Hotel Nihonbashi Premier'),
(2,'Kanda Myojin (shrine)',35.7019,139.7678,'Grounds open to walk through'),
(3,'Koyama Kyugu (Kanda)',35.6949,139.7690,'10:00-19:00'),
(4,'Animate Ikebukuro',35.7303,139.7152,'10:00-21:00'),
(5,'Kikanbo Ikebukuro',35.7308,139.7132,'11:00-21:30'),
(6,'Pokémon Center Mega Tokyo',35.7289,139.7192,'10:00-20:00'),
(7,'Kikanbo Kanda',35.6930,139.7715,'11:00-21:30'),
(8,'Toudoukan (Sugamo)',35.7340,139.7390,'11:00-21:00, off the map: 2 stops before Ikebukuro'),
(9,'Disk Union Metal (Ochanomizu)',35.6998,139.7647,'12:00-20:00'),
(10,'Disk Union Ikebukuro',35.7262,139.7135,'12:00-20:00'),
(11,'Castle Gate (bar)',35.7312,139.7141,'19:00-24:00, closed Sun/Mon'),
(12,'LANDSROCK (bar)',35.7345,139.7085,'19:00-5:00, closed Sun')]
S=[('9:00','Pickup, hotel lobby (1)'),('9:15','Ginza Line to Suehirocho, 5 min'),('9:30','Kanda Myojin shrine (2)'),('10:15','Koyama Kyugu (3)')]
COURSE=[('A','Bows & anime','1 → 2 → 3 → 4 → 5 → 6',S+[('11:00','Marunouchi Line to Ikebukuro, 17 min'),('11:30','Animate main store (4)'),('12:30','Lunch, Kikanbo (5)'),('13:30','Pokémon Center, Sunshine City (6)'),('14:00','Done in Ikebukuro')]),
('B','Bows, wrestling & anime','1 → 2 → 3 → 7 → 8 → 4',S+[('11:00','Lunch, Kikanbo Kanda (7)'),('11:55','Yamanote Line to Sugamo, 20 min'),('12:20','Toudoukan wrestling shop (8)'),('13:10','Yamanote, 2 stops to Ikebukuro'),('13:20','Animate main store (4)'),('14:00','Done in Ikebukuro')]),
('C','Bows, records & metal','1 → 2 → 3 → 5 → 10 → 9 → 11',S+[('11:00','Marunouchi Line to Ikebukuro, 17 min'),('11:20','Early lunch, Kikanbo (5)'),('12:10','Disk Union Ikebukuro (10)'),('13:00','Marunouchi Line to Ochanomizu, 15 min'),('13:15','Disk Union Hard Rock / Metal (9)'),('14:00','Done at Ochanomizu'),('19:00','Optional: Castle Gate (11)')])]
cols=''.join(f'<div class="c"><h3><b>{i}</b> {n}</h3><p class="r">{r}</p><ol>'+''.join(f'<li><b>{t}</b>{x}</li>' for t,x in s)+'</ol></div>' for i,n,r,s in COURSE)
legend=''.join(f'<li><i>{n}</i>{nm}<span>{h}</span></li>' for n,nm,_,_,h in PL)
html=f'''<!doctype html><html><head><meta charset="utf-8"><title>Tokyo, Tuesday October 13</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<style>@page{{size:A4;margin:0}}*{{box-sizing:border-box}}html,body{{margin:0;width:210mm;height:297mm;overflow:hidden}}
body{{font:9.5pt/1.35 -apple-system,"Helvetica Neue",Arial,sans-serif;color:#111;background:#fffdf6;padding:11mm 12mm}}
.k{{font-size:8pt;letter-spacing:.12em;text-transform:uppercase;color:#1a5c3a;font-weight:700;margin:0}}
h1{{font-size:21pt;margin:1mm 0 1mm;letter-spacing:-.02em;line-height:1.1}} .sub{{color:#767065;margin:0 0 3mm;font-size:9.5pt}}
.top{{display:flex;gap:4mm;height:78mm}} #map,#map2{{flex:1;border:1px solid #111;border-radius:2mm}}
ul.lg{{list-style:none;margin:3mm 0 0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:0 4mm;font-size:7.8pt}} .lg li{{display:grid;grid-template-columns:5mm 1fr;gap:0 2mm;margin-bottom:1.3mm;line-height:1.25}} .lg i{{font-style:normal;background:#1a5c3a;color:#fff;border-radius:50%;width:4.6mm;height:4.6mm;text-align:center;font-weight:700;font-size:7.5pt;line-height:4.6mm;grid-row:span 2}} .lg span{{color:#767065}}
.num{{background:#1a5c3a;color:#fff;border:1.5px solid #fff;border-radius:50%;width:22px;height:22px;text-align:center;font:700 12px/19px Arial}}
.cs{{display:grid;grid-template-columns:repeat(3,1fr);gap:4mm;margin-top:4mm}} .c{{border:1px solid #eae4d6;background:#fff;border-radius:2mm;padding:3mm}}
.c h3{{margin:0;font-size:10.5pt}} .c h3 b{{background:#111;color:#fff;border-radius:1mm;padding:0 1.6mm;margin-right:1mm}} .r{{margin:1mm 0 2mm;color:#1a5c3a;font-weight:700;font-size:8.5pt}}
.c ol{{list-style:none;margin:0;padding:0}} .c li{{display:grid;grid-template-columns:10mm 1fr;font-size:8.6pt;padding:.9mm 0;border-top:1px solid #eae4d6}} .c li b{{color:#1a5c3a;font-variant-numeric:tabular-nums}}
.ft{{display:flex;gap:5mm;align-items:center;margin-top:4mm;font-size:8.3pt;color:#555}} .ft img{{width:24mm;height:24mm}} .ft p{{margin:0 0 1mm}}
</style></head><body>
<p class="k">Tokyo · Tuesday, October 13 · Guide: Yuuki</p>
<h1>Bows first, then Ikebukuro</h1>
<p class="sub">Pickup at your hotel lobby (Mitsui Garden Hotel Nihonbashi Premier) at 9:00. Done around 14:00. Pick one course.</p>
<div class="top"><div id="map"></div><div id="map2"></div></div><ul class="lg">{legend}</ul>
<div class="cs">{cols}</div>
<div class="ft"><img src="data:image/png;base64,{qr}"><div><p><b>Full plan, photos and route maps:</b> {URL}</p><p>The two bars open in the evening, after the day plan, and are open on Tuesdays. Hours are from each shop's own site. Times are approximate.</p></div></div>
<script>var P={json.dumps([[n,la,lo] for n,_,la,lo,_ in PL])};
function mk(id,ids){{var m=L.map(id,{{zoomControl:false}});L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',{{maxZoom:19,attribution:'© OpenStreetMap'}}).addTo(m);var pts=P.filter(function(p){{return ids.indexOf(p[0])>=0}});
pts.forEach(function(p){{L.marker([p[1],p[2]],{{icon:L.divIcon({{className:'',html:'<div class="num">'+p[0]+'</div>',iconSize:[22,22],iconAnchor:[11,11]}})}}).addTo(m)}});
m.fitBounds(pts.map(function(p){{return [p[1],p[2]]}}),{{padding:[26,26]}})}}
mk('map',[1,2,3,7,9]);mk('map2',[4,5,6,10,11,12]);window.READY=0;
setTimeout(function(){{window.READY=1}},6000);</script></body></html>'''
open('/tmp/pdf.html','w').write(html)
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':794,'height':1123})
    pg.goto('file:///tmp/pdf.html');pg.wait_for_function('window.READY==1');pg.wait_for_timeout(1500)
    pg.pdf(path='patrick-ikebukuro-oct13.pdf',format='A4',print_background=True,prefer_css_page_size=True)
    pg.screenshot(path='patrick-ikebukuro-oct13.png',full_page=False)
    b.close()
import subprocess;print(subprocess.run(['python3','-c','import re;d=open("patrick-ikebukuro-oct13.pdf","rb").read();print("pages",len(re.findall(rb"/Type\\s*/Page[^s]",d)))'],capture_output=True,text=True).stdout)
