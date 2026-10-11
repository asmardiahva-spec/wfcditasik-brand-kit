# WFCditasik carousel style guide

The look: **a café worker's scrapbook.** Real photos, paper, tape, phone-screen bits. Handmade and local, never clean-template.

## Colors

Palette: **Blood Red, Light Goldenrod Yellow, White**, with **Golden** for highlights and **Ruddy Pink** as a small accent only. Cute, but not too feminine.

| Name | Hex | Use |
|---|---|---|
| Blood Red | `#660005` | Main text, handles, full-color statement slides |
| Light Goldenrod Yellow | `#FAF4D4` | Base background |
| White | `#FFFFFF` | Cards, notes, polaroids, sticker outlines, white backgrounds |
| Golden | `#EFC94C` | Marker highlight on yellow pages, gold stripes, folder, tape |
| Gold soft | `#F7E6A6` | Selected-text highlight on yellow pages |
| Ruddy Pink | `#DF8F9C` | Small accent only: marker on white/red pages, tape, tiny details |
| Pink soft | `#F2C9CF` | Selected-text highlight on white pages |
| Rose | `#A3404F` | Small widget details |
| Ink | `#2B0A0C` | Cursor, rare dark details |

Contrast with Blood Red text: on white 13.6:1, on yellow 12.1:1, on pink soft 9.0:1, on Ruddy Pink 5.5:1, on Golden 7+:1 (all readable).

### Pink rules (not too feminine)
1. **Pink is never a background.** No pink checker, pink stripes, pink cards or big pink blocks.
2. **Pink and yellow are never both dominant on one page.** If a page has both, one of them is only a tiny accent.
3. **Yellow pages:** highlights are golden, never pink. Pink can only appear as a tiny detail.
4. **White or red pages:** the pink marker or pink-soft selected text is allowed (that is the "cute" touch).
5. Handwritten notes are Blood Red (or white/yellow on red slides), never pink.

Text rule: Blood Red text on yellow or white. Never Blood Red text directly on a checker or stripes; put it on a white paper scrap first. On a solid Blood Red slide, use white or yellow text.

## Fonts (in `/fonts`, all free, OFL license)

- **Headings:** Instrument Serif, 80 to 110 px. One word per heading in *Italic*.
- **Body:** Courier Prime, 26 to 32 px. Max 3 short lines.
- **Notes and asides:** Caveat, 34 to 44 px, slightly rotated (-4° to 4°).

## Highlights (the readability rules)

Two styles only. See `highlights/png/highlight-styles.png`. The color depends on the page (see Pink rules).

**A. Marker (default)**
- Golden band on yellow pages, Ruddy Pink band on white or red pages. Always behind the text, never on top of it.
- Band covers only the lower part of the letters: top at about 30% of font size above the baseline, height about 36% of font size.
- One band per line. If a phrase wraps, each line gets its own band, the width of that line only.
- Side padding 6 to 10 px. The band never extends past the last letter.
- Line spacing at least 1.15 so bands never touch the line above or below.

**B. Selected text (signature, max once per carousel)**
- Pink-soft block on white pages, gold-soft on yellow pages, from cap height to just under the descenders.
- Blood Red handles: left handle dot on top, right handle dot on the bottom (`ui-stickers/selection-handle-*`).
- Only for one short phrase (1 to 3 words) on a single line. Never on wrapped text.
- Leave a clear gap between the left handle and the word before it.

**In Canva:** use Text > Effects > Background for the selected-text style (roundness 0, spread 10 to 15). For the marker, use a rectangle behind the text, sized per line, then group them.

## Backgrounds (`/backgrounds`, 1080 × 1350)

Rotate, never the same background twice in a row:
grid paper (yellow or white) · solid white · solid yellow · solid red (one big statement) · red/yellow checker · red/white checker · red stripes · gold stripes · dashed card on red or yellow (for quotes) · your own photo. No pink backgrounds.

## Stickers and paper

- `ui-stickers/`: copy bar, selection handles, notification pill, gold folder, Tasik weather widget, reminders card, wifi pill, cursor, polaroid frame.
- `paper/`: washi tape (kraft, red, gold, pink for tiny accents), lined note, torn strip.
- `photo-stickers/`: your own cut-out photos from WFC sessions (kopi, laptop, notebook, charger). This is what makes the feed feel local.
- Max 3 to 4 stickers per slide. Overlap edges a little, tilt between -8° and 8°.

## Layout rules

1. No two slides in a row with the same layout.
2. Text is never just centered in a box. Put it on a paper scrap, a note, or straight on the background off-center.
3. One idea per slide.
4. Cover: big serif title plus 2 to 3 stickers scattered around it.
5. Last slide: a CTA on paper ("simpan buat sesi WFC berikutnya", "tag temen kerjamu").
6. Text keeps a 90 px safe margin from all edges.

## Reference examples

See `examples/*-preview.png`. These show the right balance: Blood Red + yellow lead, golden markers on yellow pages, pink only as a highlight on white pages ("Beneran", "kerjaan", "tiap Kamis").

## Tone

Slightly self-aware and honest. Mix Bahasa Indonesia and casual English the way the community actually talks.

## Rebuilding assets

`python3 tools/build_assets.py` regenerates every SVG and PNG (needs `pip install cairosvg pillow`). Change the colors at the top of the file to recolor everything.
