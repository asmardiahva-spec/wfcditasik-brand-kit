# WFCbareng weekly poster

Every Monday: ~07:00 WIB build the poster + slides, ~07:30 ask Diah for the QR code, finish with the QR, Diah approves, posted Monday 12:00 WIB (feed only).

- Build: `python3 tools/build_wfcbareng_poster.py --number N --date YYYY-MM-DD(Thursday) --bg maroon|pink|gray --illustration posters/<date>-<N>/illustration.svg [--qr qr.png]`
- 4 slides: 01 poster · 02 "Who can join?" Member WFCditasik + "How to be a member? It's very easy! Start from FREE, bisa jadi member basic" · 03 Member Basic vs Member Pro table · 04 CTA: "Yuk jadi member WFCditasik" + website (`--website`).
- Membership (since 19 Oct 2026): only members join WFCbareng; Basic is FREE. Basic vs Pro: kartu digital member ✅/✅ · booking seat WFCbareng ✅/✅ · daftar event (RWH, dll) harga normal / harga khusus member · beli produk digital harga normal / harga khusus member · redeem benefit cafe partner ❌ terkunci / ✅. No more "non-member" wording.
- Background rotates by number: #11 maroon, #12 pink, #13 gray, #14 maroon, ... (N mod 3: 2 = maroon, 0 = pink, 1 = gray). Plain color + grain, never checker.
- Fixed info: 09.00–12.00 Deep Work (No Distract) · 12.00–13.00 Break & Networking · 13.00–End Continue Working · Langgam Coffee & Book Tarumanagara · FREE for member WFCditasik (Basic membership is free).
- Illustration: a NEW original SVG every week, same flat style as #11 (ink outlines, Blood Red + pop accents, people working/WFC life). No photos, no Canva elements.
- Fonts: ONLY the "WFC bareng" title uses Cooper BT (put a licensed file at `fonts/wfcbareng/WFCbareng.ttf`/.otf; until then Fraunces Black Soft is the stand-in), set big and tight like the original. Everything else uses the brand-kit fonts (Instrument Serif, Courier Prime, Caveat).
- QR code: different per event; Diah sends it after approving the design.
- Skipped Thursday = no poster that week; the next poster keeps the next number.
- Caption: follow `posters/caption-example.md` when it exists.
- `log.md` lists every poster (number, Thursday date, background, status).
