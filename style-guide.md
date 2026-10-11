# WFCditasik carousel style guide

The look: **a café worker's scrapbook.** Real photos, paper, tape, phone-screen bits. Handmade and local, never clean-template.

## Colors

Palette: **Blood Red + cool light gray + White**, with **Ruddy Pink** as the highlight and small accent. No yellow. Cute, but not too feminine.

| Name | Hex | Use |
|---|---|---|
| Blood Red | `#660005` | Main text, handles, full-color statement slides, checker, stripes |
| Cool light gray | `#EDEDED` | Base background |
| Grid gray | `#D9D9D9` | Grid paper lines |
| White | `#FFFFFF` | Cards, notes, polaroids, sticker outlines, white backgrounds |
| Ruddy Pink | `#DF8F9C` | Marker highlight, small accents (tape, folder, tiny details) |
| Pink soft | `#F2C9CF` | Selected-text highlight; accent text on solid red slides |
| Rose | `#A3404F` | Small widget details |
| Ink | `#2B0A0C` | Cursor, rare dark details |

Contrast with Blood Red text: on white 13.6:1, on gray 11.9:1, on pink soft 9.0:1, on Ruddy Pink 5.5:1 (all readable).

### Pink rules (not too feminine)
1. **Blood Red leads.** Gray and white are the base. Pink is only for highlights and small details.
2. **Pink is never a background.** No pink checker, pink stripes, pink cards or big pink blocks.
3. **No yellow or green in the base palette** (backgrounds, highlights, text). They exist only as tiny pop accents (see below).
4. Handwritten notes are Blood Red (white or pink soft on red slides).

### Pop accents (tiny UI elements only)

Notion/phone-style bits that make a slide feel alive: buttons, progress bars, toggles, checkboxes, tags, cursors, badges (`ui-accents/`).

| Name | Hex |
|---|---|
| Leaf green | `#8FCB63` |
| Denim blue | `#4D83C5` |
| Brave red | `#E0393E` |
| Cherry blossom | `#F4B6C2` |
| Sunny yellow | `#F6CB45` |

Rules:
1. Only on small UI elements. Never as backgrounds, text highlights, headings or body text.
2. Max 1 to 2 pop-accent elements per slide, and max 2 different pop colors per slide.
3. Each element stays small (roughly a button or tag size). Blood Red must still clearly lead the slide.
4. Not every slide needs one. Use them where a "UI moment" fits the copy (a toggle for "mode fokus", a progress bar for "deadline", a button for the CTA).

Text rule: Blood Red text on gray or white. Never Blood Red text directly on a checker or stripes; put it on a white paper scrap first. On a solid Blood Red slide, use white text with pink-soft accents.

## Fonts (in `/fonts`, all free, OFL license)

- **Headings:** Instrument Serif, 80 to 110 px. One word per heading in *Italic*.
- **Body:** Courier Prime, 26 to 32 px. Max 3 short lines.
- **Notes and asides:** Caveat, 34 to 44 px, slightly rotated (-4° to 4°).

## Highlights (the readability rules)

Two styles only. See `highlights/png/highlight-styles.png`.

**A. Marker (default)**
- Ruddy Pink band, always behind the text, never on top of it.
- Band covers only the lower part of the letters: top at about 30% of font size above the baseline, height about 36% of font size.
- One band per line. If a phrase wraps, each line gets its own band, the width of that line only.
- Side padding 6 to 10 px. The band never extends past the last letter.
- Line spacing at least 1.15 so bands never touch the line above or below.

**B. Selected text (signature, max once per carousel)**
- Pink-soft block from cap height to just under the descenders.
- Blood Red handles: left handle dot on top, right handle dot on the bottom (`ui-stickers/selection-handle-*`).
- Only for one short phrase (1 to 3 words) on a single line. Never on wrapped text.
- Leave a clear gap between the left handle and the word before it.

**In Canva:** use Text > Effects > Background for the selected-text style (roundness 0, spread 10 to 15). For the marker, use a rectangle behind the text, sized per line, then group them.

## Backgrounds (`/backgrounds`, 1080 × 1350)

Rotate, never the same background twice in a row:
grid paper (gray or white) · solid gray · solid white · solid red (one big statement) · red/gray checker · red/white checker · red stripes · dashed card on red or gray (for quotes) · your own photo. No pink or yellow backgrounds.

## Stickers and paper

- `ui-stickers/`: copy bar, selection handles, notification pill, pink folder (accent), Tasik weather widget, reminders card, wifi pill, cursor, polaroid frame.
- `paper/`: washi tape (gray, red, pink for tiny accents), lined note, torn strip.
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

See `examples/*-preview.png`. These show the right balance: Blood Red leads, gray and white base, pink only as highlights and small accents ("Beneran", "kerjaan", "tiap Kamis").

## Tone

Slightly self-aware and honest. Mix Bahasa Indonesia and casual English the way the community actually talks.

## Rebuilding assets

`python3 tools/build_assets.py` regenerates every SVG and PNG (needs `pip install cairosvg pillow`). Change the colors at the top of the file to recolor everything.
