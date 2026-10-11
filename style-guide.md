# WFCditasik carousel style guide

The look: **a café worker's scrapbook.** Real photos, paper, tape, phone-screen bits. Handmade and local, never clean-template.

## Colors

| Name | Hex | Use |
|---|---|---|
| Maroon | `#6E1F2B` | Main text, handles, full-color statement slides |
| Maroon dark | `#4A1219` | Text on matcha backgrounds |
| Matcha | `#B5C48A` | Marker highlight, checker, stripes |
| Matcha soft | `#D6DFB8` | Selected-text highlight, soft backgrounds |
| Olive | `#5F6B33` | Small labels, widgets, accents |
| Cream | `#F5EFE4` | Base background |
| Paper | `#FBF8F2` | Cards, notes, polaroids |
| Ink | `#2B1B18` | Cursor, rare dark details |

Rule: maroon text on cream or paper. Never maroon text directly on matcha checker; put it on a paper scrap first.

## Fonts (in `/fonts`, all free, OFL license)

- **Headings:** Instrument Serif, 80 to 110 px. One word per heading in *Italic*.
- **Body:** Courier Prime, 26 to 32 px. Max 3 short lines.
- **Notes and asides:** Caveat, 34 to 44 px, slightly rotated (-4° to 4°).

## Highlights (the readability rules)

Two styles only. See `highlights/png/highlight-styles.png`.

**A. Marker (default)**
- Matcha band behind the text, never on top of it (text layer above the band).
- Band covers only the lower part of the letters: top at about 30% of font size above the baseline, height about 36% of font size.
- One band per line. If a phrase wraps, each line gets its own band, the width of that line only.
- Side padding 6 to 10 px. The band never extends past the last letter.
- Line spacing at least 1.15 so bands never touch the line above or below.

**B. Selected text (signature, max once per carousel)**
- Matcha-soft block from cap height to just under the descenders.
- Maroon handles: left handle dot on top, right handle dot on the bottom (`ui-stickers/selection-handle-*`).
- Only for one short phrase (1 to 3 words) on a single line. Never on wrapped text.
- Leave a clear gap between the left handle and the word before it.

**In Canva:** use Text > Effects > Background for the selected-text style (roundness 0, spread 10 to 15). For the marker, use a rectangle behind the text, sized per line, then group them.

## Backgrounds (`/backgrounds`, 1080 × 1350)

Rotate, never the same background twice in a row:
grid paper · matcha checker · maroon checker · matcha stripes · maroon stripes · solid cream · solid maroon (one big statement) · dashed card on maroon/matcha (for quotes) · your own photo.

## Stickers and paper

- `ui-stickers/`: copy bar, selection handles, notification pill, folder, Tasik weather widget, reminders card, wifi pill, cursor, polaroid frame.
- `paper/`: washi tape (matcha, maroon, kraft), lined note, torn strip.
- `photo-stickers/`: your own cut-out photos from WFC sessions (kopi, laptop, notebook, charger). This is what makes the feed feel local.
- Max 3 to 4 stickers per slide. Overlap edges a little, tilt between -8° and 8°.

## Layout rules

1. No two slides in a row with the same layout.
2. Text is never just centered in a box. Put it on a paper scrap, a note, or straight on the background off-center.
3. One idea per slide.
4. Cover: big serif title plus 2 to 3 stickers scattered around it.
5. Last slide: a CTA on paper ("simpan buat sesi WFC berikutnya", "tag temen kerjamu").
6. Text keeps a 90 px safe margin from all edges.

## Tone

Slightly self-aware and honest. Mix Bahasa Indonesia and casual English the way the community actually talks.

## Rebuilding assets

`python3 tools/build_assets.py` regenerates every SVG and PNG (needs `pip install cairosvg pillow`). Change the colors at the top of the file to recolor everything.
