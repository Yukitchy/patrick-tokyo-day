# goods-hunt

Guest "find this character's goods in Tokyo" kit. One config + photos in, a full set out:

| Output | What |
|---|---|
| `index.html` | Guest page (Dec 10 design): honest-stock note, **show-the-staff card**, timeline, 2 route maps, one card per shop, online back-ups, optional tip, credits |
| `card.png` | Phone card: official product photos + Japanese sentences for shop staff (1080 px wide) |
| `<pdf_name>` | A4 landscape one-sheet: photo strip, chevron timeline, OSM maps, route list, mini card, QR to the page |
| `og.jpg` | Share image (1200x630) |

## Make a new one
1. `cp -r jobs/john jobs/<guest>` (or start from `template/config.template.json`; every `<...>` is an input) and edit `config.json`.
2. Put the character photos in `jobs/<guest>/photos/`. Use official product photos (Good Smile Company product pages work well), never generated art. Fill each `credit`.
3. For each shop fill name, area, what to look for, lat/lon (GSI geocoder: `msearch.gsi.go.jp/address-search/AddressSearch?q=<address>`), Google Maps query. Write `hours` only if you read it on an official page; otherwise "check the shop's page on the day". Do not promise stock.
4. Set `out_dir` to a **new folder outside this repo** (it becomes its own public repo), then:
   `/usr/local/bin/python3 engine/build.py jobs/<guest>/config.json`
   It prints `pdf pages 1 overflow [False, False]`. Anything else means the PDF overflowed: shorten text.
5. Publish: `cd <out_dir> && git init -b main && git add -A && git commit -m init && gh repo create <owner>/<repo> --public --source=. --push`, then enable Pages on `main` `/`.

## Notes
- Needs Pillow, qrcode, playwright (uses installed Google Chrome via `channel='chrome'`).
- `maps[].id` groups stops: put stops that are close together on the same map; set `zmax` 18 for a tight cluster. A stop's `leg` draws the line to the next stop in its map: `foot` (OSM walking route, red), `train` (dashed), `none`.
- `want_ja` starting with `ぬいぐるみやフィギュア` gives the "plush or figure" English gloss, anything else gives "plush or goods".
- `jobs/` is git-ignored (guest data stays local). `.mapcache/` caches OSM tiles.
- Page design source: the Dec 10 page (`engine/page.css` is a copy of its CSS; `engine/extra.css` adds this kit's blocks). Map code is a trimmed copy of `../mkpdf.py` (`engine/maplib.py`).
