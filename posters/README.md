# WFCbareng weekly poster

Every Monday: poster for that week's Thursday WFCbareng, posted Monday 18:00 WIB (feed only, after Diah approves).

- Build: `python3 tools/build_wfcbareng_poster.py --number N --date YYYY-MM-DD(Thursday) --bg maroon|pink|gray --illustration posters/<date>-<N>/illustration.svg [--qr qr.png]`
- Slide 1 = poster, slide 2 = "Who Can Join?" (member vs non-member table).
- Background rotates by number: #11 maroon, #12 pink, #13 gray, #14 maroon, ... (N mod 3: 2 = maroon, 0 = pink, 1 = gray). Plain color + grain, never checker.
- Fixed info: 09.00–12.00 Deep Work (No Distract) · 12.00–13.00 Break & Networking · 13.00–End Continue Working · Langgam Coffee & Book Tarumanagara · FREE for member & non-member.
- Illustration: a NEW original SVG every week, same flat style as #11 (ink outlines, Blood Red + pop accents, people working/WFC life). No photos, no Canva elements.
- Title font: put the official WFCbareng font in `fonts/wfcbareng/WFCbareng.ttf` (or .otf); until then Fraunces Black is the stand-in.
- QR code: different per event; Diah sends it after approving the design.
- Skipped Thursday = no poster that week; the next poster keeps the next number.
- Caption: follow `posters/caption-example.md` when it exists.
- `log.md` lists every poster (number, Thursday date, background, status).
