"""Build the weekly WFCbareng poster (2 slides, 1080x1350).

Usage:
  python3 tools/build_wfcbareng_poster.py --number 11 --date 2026-10-15 --bg maroon \
      --illustration posters/2026-10-15-11/illustration.svg [--qr path/to/qr.png]

Output: posters/<date>-<number>/slide-01.png (poster) and slide-02.png (Who Can Join?).
Backgrounds rotate maroon -> pink -> gray (plain + grain texture).
"""
import argparse, asyncio, datetime, os
import numpy as np
from PIL import Image
from playwright.async_api import async_playwright

KIT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
U = f"file://{KIT}"
BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus",
         "September", "Oktober", "November", "Desember"]

# Title font: replace with the real WFCbareng font file when available (fonts/wfcbareng/*).
TITLE_FONT = None
for cand in ["fonts/wfcbareng/WFCbareng.ttf", "fonts/wfcbareng/WFCbareng.otf"]:
    if os.path.exists(os.path.join(KIT, cand)):
        TITLE_FONT = cand
TITLE_FACE = (f"@font-face {{ font-family:'TT'; src:url('{U}/{TITLE_FONT}'); }}" if TITLE_FONT else
              f"@font-face {{ font-family:'TT'; src:url('{U}/fonts/Fraunces[SOFT,WONK,opsz,wght].ttf'); font-weight:100 900; }}")
TITLE_VARIATION = "" if TITLE_FONT else "font-weight:900; font-variation-settings:'SOFT' 100, 'WONK' 0, 'opsz' 144;"

THEMES = {
    # bg, title, text, accent (tag bg), tag text, card
    "maroon": dict(bg="#660005", title="#F2C9CF", text="#FFFFFF", sub="#F2C9CF", tag="#F2C9CF", tagtext="#660005"),
    "pink":   dict(bg="#F2C9CF", title="#660005", text="#660005", sub="#660005", tag="#660005", tagtext="#FFFFFF"),
    "gray":   dict(bg="#EDEDED", title="#660005", text="#660005", sub="#660005", tag="#660005", tagtext="#FFFFFF"),
}


def grain():
    path = os.path.join(KIT, "backgrounds/png/grain-overlay.png")
    if not os.path.exists(path):
        rng = np.random.default_rng(7)
        n = rng.random((1350, 1080))
        a = np.zeros((1350, 1080, 4), dtype=np.uint8)
        dark = n < 0.5
        a[..., :3] = np.where(dark[..., None], 0, 255)
        a[..., 3] = (np.abs(n - 0.5) * 2 * 26).astype(np.uint8)
        Image.fromarray(a, "RGBA").save(path)
    return f"{U}/backgrounds/png/grain-overlay.png"


def css(t):
    return f"""
{TITLE_FACE}
@font-face {{ font-family:'IS'; src:url('{U}/fonts/InstrumentSerif-Regular.ttf'); }}
@font-face {{ font-family:'IS'; font-style:italic; src:url('{U}/fonts/InstrumentSerif-Italic.ttf'); }}
@font-face {{ font-family:'CP'; src:url('{U}/fonts/CourierPrime-Regular.ttf'); }}
@font-face {{ font-family:'CP'; font-weight:700; src:url('{U}/fonts/CourierPrime-Bold.ttf'); }}
@font-face {{ font-family:'CV'; src:url('{U}/fonts/Caveat[wght].ttf'); font-weight:400 700; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1350px; overflow:hidden; }}
.slide {{ position:relative; width:1080px; height:1350px; background:{t['bg']}; color:{t['text']}; }}
.grain {{ position:absolute; inset:0; background:url('{grain()}'); z-index:0; pointer-events:none; }}
.abs {{ position:absolute; z-index:2; }}
.title {{ font-family:'TT', serif; {TITLE_VARIATION} color:{t['title']}; line-height:.86; letter-spacing:-2px;
          text-shadow: 0 6px 0 rgba(0,0,0,.12); text-align:center; }}
.mono {{ font-family:'CP', monospace; }}
.serif {{ font-family:'IS', serif; }}
.hand {{ font-family:'CV', cursive; font-weight:600; }}
img.st {{ position:absolute; z-index:3; }}
"""


def st(path, x, y, w, rot=0):
    return f'<img class="st" src="{U}/{path}" style="left:{x}px; top:{y}px; width:{w}px; transform:rotate({rot}deg);">'


def poster(n, date, t, ill, qr):
    d = datetime.date.fromisoformat(date)
    tanggal = f"{d.day} {BULAN[d.month-1].upper()} {d.year}"
    hari = ["SENIN", "SELASA", "RABU", "KAMIS", "JUMAT", "SABTU", "MINGGU"][d.weekday()]
    pill = "background:#FFFFFF; color:#660005; border-radius:26px; height:52px; display:flex; align-items:center; padding:0 22px; margin-bottom:12px; box-shadow:0 4px 10px rgba(0,0,0,.08);"
    rows = [("09.00 - 12.00", "Deep Work (No Distract)"), ("12.00 - 13.00", "Break &amp; Networking"), ("13.00 - End", "Continue Working")]
    sched = "".join(f'<div style="{pill}"><span class="mono" style="font-weight:700; font-size:17px; width:160px; flex:none;">{a}</span>'
                    f'<span class="serif" style="font-size:23px; white-space:nowrap;">{b}</span></div>' for a, b in rows)
    qr_html = (f'<img src="file://{os.path.abspath(qr)}" style="width:190px; height:190px; display:block; background:#fff; padding:10px; border-radius:12px;">' if qr else
               '<div class="mono" style="width:190px; height:190px; background:#FFFFFF; border:4px dashed #DF8F9C; border-radius:12px; color:#660005; display:flex; align-items:center; justify-content:center; text-align:center; font-size:20px; font-weight:700;">QR<br>CODE</div>')
    return f"""<div class="slide"><div class="grain"></div>
  {st('ui-accents/png/toggle-mode-fokus-green.png', 40, 46, 220, -7)}
  <div class="abs title" style="left:0; width:1080px; top:92px; font-size:204px;">WFC<br>bareng</div>
  <div class="abs mono" style="left:0; width:1080px; top:484px; text-align:center; font-size:24px; font-weight:700; letter-spacing:2px; line-height:1.5; color:{t['sub']};">CONNECTING TASIK REMOTE WORKERS,<br>FREELANCERS, CREATIVES, AND BUILDERS</div>
  <div class="abs" style="left:826px; top:150px; transform:rotate(-7deg); background:{t['tag']}; color:{t['tagtext']}; padding:4px 18px 10px; font-family:'TT', serif; {TITLE_VARIATION} font-size:72px; line-height:1; box-shadow:0 6px 0 rgba(0,0,0,.12);">#{n}</div>
  <div class="abs" style="left:90px; top:600px; width:900px; height:440px; background:#FFFFFF; border-radius:36px; box-shadow:0 12px 30px rgba(0,0,0,.12);"></div>
  <img class="abs" src="file://{os.path.abspath(ill)}" style="left:263px; top:612px; width:554px; z-index:3;">
  <div class="abs" style="left:62px; top:612px; transform:rotate(-8deg); z-index:4; background:#F6CB45; color:#660005; padding:8px 22px 12px; border-radius:6px; box-shadow:0 6px 14px rgba(0,0,0,.15);">
    <div style="font-family:'TT', serif; {TITLE_VARIATION} font-size:52px; line-height:1;">FREE</div>
    <div class="mono" style="font-size:16px; font-weight:700; margin-top:2px;">for member &amp;<br>non-member</div></div>
  <div class="abs" style="left:70px; top:1080px; width:320px;">
    <div style="font-family:'TT', serif; {TITLE_VARIATION} font-size:78px; line-height:.95; color:{t['title']};">{hari}</div>
    <div class="mono" style="font-size:24px; font-weight:700; letter-spacing:1px; margin-top:6px;">{tanggal}</div>
    <div class="mono" style="font-size:22px; font-weight:700; letter-spacing:1px; line-height:1.4; margin-top:22px;">LANGGAM COFFEE &amp; BOOK<br>TARUMANAGARA</div></div>
  <div class="abs" style="left:398px; top:1092px; width:400px;">{sched}</div>
  <div class="abs" style="left:822px; top:1072px; width:190px; text-align:center;">
    <div class="mono" style="font-size:32px; font-weight:700; letter-spacing:2px; margin-bottom:10px;">REGISTER</div>{qr_html}</div>
</div>"""


def who(t):
    cell = "padding:0 22px; display:flex; align-items:center; border-top:2px solid #F2C9CF;"
    rows = [("#E0393E", "Seat", "Book langsung via QR", "Cek ketersediaan H-1"),
            ("#F6CB45", "Booking", "Scan &rarr; Book &rarr; Done!", "DM @wfcditasik di H-1"),
            ("#4D83C5", "Join", "Seat langsung terkonfirmasi", "Join jika masih tersedia")]
    body = "".join(
        f'<div style="display:grid; grid-template-columns:220px 1fr 1fr; height:116px;">'
        f'<div style="{cell}"><span style="width:16px; height:16px; border-radius:4px; background:{c}; margin-right:14px;"></span><span class="serif" style="font-size:34px;">{a}</span></div>'
        f'<div class="mono" style="{cell} border-left:2px solid #F2C9CF; font-size:23px;">{b}</div>'
        f'<div class="mono" style="{cell} border-left:2px solid #F2C9CF; font-size:23px;">{c2}</div></div>'
        for c, a, b, c2 in rows)
    return f"""<div class="slide"><div class="grain"></div>
  <div class="abs title" style="left:0; width:1080px; top:180px; font-size:150px;">Who Can<br>Join?</div>
  <div class="abs mono" style="left:0; width:1080px; top:520px; text-align:center;">
    <span style="display:inline-block; background:#FFFFFF; color:#660005; font-size:28px; font-weight:700; letter-spacing:2px; padding:10px 26px; border-radius:10px;">MEMBER &amp; NON-MEMBER WFCDITASIK</span></div>
  <div class="abs" style="left:90px; top:640px; width:900px; background:#FFFFFF; color:#660005; border-radius:24px; overflow:hidden; box-shadow:0 12px 30px rgba(0,0,0,.12);">
    <div style="display:grid; grid-template-columns:220px 1fr 1fr; height:96px; background:#EDEDED;">
      <div></div>
      <div class="mono" style="display:flex; align-items:center; justify-content:center; font-size:26px; font-weight:700; letter-spacing:1px; border-left:2px solid #F2C9CF;">MEMBER</div>
      <div class="mono" style="display:flex; align-items:center; justify-content:center; font-size:26px; font-weight:700; letter-spacing:1px; border-left:2px solid #F2C9CF;">NON-MEMBER</div></div>
    {body}</div>
  {st('ui-accents/png/tag-wfc-blue.png', 880, 600, 130, 8)}
  {st('ui-accents/png/cursor-hand.png', 120, 1110, 74, -8)}
  <div class="abs hand" style="left:210px; top:1130px; font-size:44px; transform:rotate(-3deg); color:{t['text']};">sampai ketemu hari Kamis!</div>
</div>"""


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--number", type=int, required=True)
    ap.add_argument("--date", required=True, help="Thursday date YYYY-MM-DD")
    ap.add_argument("--bg", choices=THEMES, required=True)
    ap.add_argument("--illustration", required=True)
    ap.add_argument("--qr")
    ap.add_argument("--out")
    a = ap.parse_args()
    t = THEMES[a.bg]
    out = a.out or os.path.join(KIT, "posters", f"{a.date}-{a.number}")
    os.makedirs(out, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for i, body in enumerate([poster(a.number, a.date, t, a.illustration, a.qr), who(t)], 1):
            html = f"<!doctype html><html><head><meta charset='utf-8'><style>{css(t)}</style></head><body>{body}</body></html>"
            f = os.path.join(out, f"slide-0{i}.html"); open(f, "w").write(html)
            await pg.goto(f"file://{f}"); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(200)
            await pg.screenshot(path=os.path.join(out, f"slide-0{i}.png"))
            os.remove(f)
        await b.close()
    print(out)

asyncio.run(main())
