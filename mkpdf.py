#!/usr/bin/env python3
"""One-page A4 summary of the single course -> patrick-ikebukuro-oct13.pdf/.png (needs playwright chromium + qrcode)"""
import qrcode,io,base64,json,tempfile,os
URL='https://yukitchy.github.io/patrick-tokyo-day/'
q=qrcode.make(URL,box_size=6,border=1);b=io.BytesIO();q.save(b,'PNG');qr=base64.b64encode(b.getvalue()).decode()
# n, name, lat, lon, hours on Tue Oct 13
PL=[(1,'Hotel lobby',35.6865,139.7740,'Mitsui Garden Hotel Nihonbashi Premier'),
(2,'Koyama Kyugu, Kanda main store',35.6951,139.7685,'Open 10:00-19:00'),
(3,'Animate Ikebukuro',35.7311,139.7154,'Open 10:00-21:00'),
(5,'Pokémon Center Mega Tokyo',35.7278,139.7200,'Open 10:00-20:00'),
(6,'Disk Union Ikebukuro (if it fits)',35.7287,139.7138,'Open 12:00-20:00')]
# lunch options: letter, name, lat, lon, hours
LU=[('a','Kikanbo, spicy ramen',35.7291,139.7153,'11:00-21:30'),('b','Mutekiya, tonkotsu ramen',35.7269,139.7117,'from 10:30'),
('c','Shimizuya, pork cutlet',35.7319,139.7144,'11:00-20:00'),('d','Wakataka, conveyor sushi',35.7295,139.7156,'11:30-22:00'),
('e','Saffron, Indian curry',35.7294,139.7165,'lunch 11:00-15:00'),('f','Unatatsu, grilled eel',35.7317,139.7162,'lunch 11:30-14:00')]
TT=[('9:30','Meet at the hotel lobby (1)'),('9:40','Ginza Line, Mitsukoshimae to Kanda, 2 min, then walk 5 min'),('10:00','Koyama Kyugu bow shop (2)'),
('10:50','Marunouchi Line, Awajicho to Ikebukuro, 17 min'),('11:30','Animate main store (3)'),('12:15','Lunch, you pick one of a to f (4)'),
('13:15','Pokémon Center, Sunshine City (5)'),('14:15','Disk Union, if it fits (6)'),('14:30','Done, in Ikebukuro'),
('','Back to Nihonbashi: Marunouchi Line to Otemachi, Hanzomon Line one stop, about 30 min')]
tt=''.join(f'<li><b>{t}</b>{x}</li>' for t,x in TT)
legend=''.join(f'<li><i>{n}</i>{nm}<span>{h}</span></li>' for n,nm,_,_,h in PL)
lunch=''.join(f'<li><i class="l">{n}</i>{nm}<span>{h}</span></li>' for n,nm,_,_,h in LU)
html=f'''<!doctype html><html><head><meta charset="utf-8"><title>Tokyo, Tuesday October 13</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<style>@page{{size:A4;margin:0}}*{{box-sizing:border-box}}html,body{{margin:0;width:210mm;height:297mm;overflow:hidden}}
body{{font:10pt/1.4 -apple-system,"Helvetica Neue",Arial,sans-serif;color:#1a1a1a;background:#fff;padding:12mm 14mm}}
.k{{font-size:8pt;letter-spacing:.12em;text-transform:uppercase;color:#e5382b;font-weight:700;margin:0}}
h1{{font-size:24pt;margin:1mm 0 1mm;letter-spacing:-.02em;line-height:1.1;font-weight:900}} .sub{{color:#5c5c5c;margin:0 0 4mm;font-size:10pt}}
#map,#map2{{height:86mm;border:1px solid #1a1a1a;border-radius:2mm}}
.maps{{display:grid;grid-template-columns:1fr 1.25fr;gap:4mm}}
.cols{{display:grid;grid-template-columns:1fr 1fr;gap:8mm;margin-top:5mm}}
h2{{font-size:8pt;letter-spacing:.12em;text-transform:uppercase;color:#e5382b;margin:0 0 2mm}}
ol,ul{{list-style:none;margin:0;padding:0}}
.tt li{{display:grid;grid-template-columns:13mm 1fr;padding:1.1mm 0;border-top:1px solid #e6e6e6;font-size:9.5pt}} .tt li:first-child{{border-top:0}} .tt b{{font-variant-numeric:tabular-nums}}
.lg li{{display:grid;grid-template-columns:6mm 1fr;gap:0 2mm;margin-bottom:1.2mm;line-height:1.25;font-size:9.5pt;font-weight:700}} .lg i{{font-style:normal;background:#e5382b;color:#fff;border-radius:50%;width:5mm;height:5mm;text-align:center;font-weight:900;font-size:8pt;line-height:5mm;grid-row:span 2}} .lg span{{color:#5c5c5c;font-weight:500;font-size:8.5pt}}
.lg i.l{{background:#fff;color:#e5382b;border:1.5px solid #e5382b}} .num.l{{background:#fff;color:#e5382b;border:2px solid #e5382b;width:20px;height:20px;font:900 11px/16px Arial}}
.num{{background:#e5382b;color:#fff;border:2px solid #fff;border-radius:50%;width:24px;height:24px;text-align:center;font:900 13px/20px Arial;box-shadow:0 0 0 1px #1a1a1a}}
.ft{{display:flex;gap:5mm;align-items:center;margin-top:4mm;font-size:8.5pt;color:#5c5c5c;border-top:1px solid #1a1a1a;padding-top:4mm}} .ft img{{width:24mm;height:24mm;flex:none}} .ft p{{margin:0 0 1mm}}
</style></head><body>
<p class="k">Tokyo · Tuesday, October 13 · Guide: Yuuki</p>
<h1>Bows first, then Ikebukuro</h1>
<p class="sub">Meet at your hotel lobby (Mitsui Garden Hotel Nihonbashi Premier) at 9:30. Done around 14:30 in Ikebukuro.</p>
<div class="maps"><div id="map"></div><div id="map2"></div></div>
<div class="cols"><div class="tt"><h2>The day</h2><ol>{tt}</ol></div><div class="lg"><h2>Where and when it is open</h2><ul>{legend}</ul><h2 style="margin-top:3mm">Lunch, you pick one of six (4)</h2><ul>{lunch}</ul></div></div>
<div class="ft"><img src="data:image/png;base64,{qr}"><div><p><b>Full plan, photos and route map:</b> {URL}</p><p>If you want more tonight: Castle Gate (19:00-24:00, closed Sun/Mon) and LANDSROCK (19:00-5:00, closed Sun), both rock bars in Ikebukuro. Times are approximate. Hours are from each shop's own site.</p></div></div>
<script>var P={json.dumps([[n,la,lo] for n,_,la,lo,_ in PL])},LU={json.dumps([[n,la,lo] for n,_,la,lo,_ in LU])};
function mk(id,ids,lu){{var m=L.map(id,{{zoomControl:false}});L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',{{maxZoom:19,attribution:'© OpenStreetMap'}}).addTo(m);var pts=P.filter(function(p){{return ids.indexOf(p[0])>=0}}),all=[];
pts.forEach(function(p){{all.push([p[1],p[2]]);L.marker([p[1],p[2]],{{icon:L.divIcon({{className:'',html:'<div class="num">'+p[0]+'</div>',iconSize:[24,24],iconAnchor:[12,12]}})}}).addTo(m)}});
if(lu)LU.forEach(function(p){{all.push([p[1],p[2]]);L.marker([p[1],p[2]],{{icon:L.divIcon({{className:'',html:'<div class="num l">'+p[0]+'</div>',iconSize:[20,20],iconAnchor:[10,10]}})}}).addTo(m)}});
L.polyline(pts.map(function(p){{return [p[1],p[2]]}}),{{color:'#1a1a1a',weight:2,opacity:.5,dashArray:'4 6'}}).addTo(m);
m.fitBounds(all,{{padding:[30,30]}})}}
mk('map',[1,2],0);mk('map2',[3,5,6],1);window.READY=0;setTimeout(function(){{window.READY=1}},6000);</script></body></html>'''
tmp=os.path.join(tempfile.gettempdir(),'patrick-pdf.html');open(tmp,'w').write(html)
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':794,'height':1123})
    pg.goto('file://'+tmp);pg.wait_for_function('window.READY==1');pg.wait_for_timeout(1500)
    pg.pdf(path='patrick-ikebukuro-oct13.pdf',format='A4',print_background=True,prefer_css_page_size=True)
    pg.screenshot(path='patrick-ikebukuro-oct13.png',full_page=False)
    over=pg.evaluate('document.body.scrollHeight>document.body.clientHeight+1 || document.documentElement.scrollHeight>1124')
    b.close()
import re;d=open('patrick-ikebukuro-oct13.pdf','rb').read();print('pages',len(re.findall(rb'/Type\s*/Page[^s]',d)),'overflow',over)
