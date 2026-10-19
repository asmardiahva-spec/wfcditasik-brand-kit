"""Build the weekly WFCbareng poster carousel (4 slides, 1080x1350).

Usage:
  python3 tools/build_wfcbareng_poster.py --number 11 --date 2026-10-15 --bg maroon \
      --illustration posters/2026-10-15-11/illustration.svg [--qr qr.png] [--website example.com]

Slides: 01 poster · 02 Who can join? (member WFCditasik, start from FREE) · 03 Member Basic vs Pro table · 04 join-member CTA.
Backgrounds rotate maroon -> pink -> gray (plain + grain texture).
Fonts: "WFC bareng" title = Cooper BT (fonts/wfcbareng/WFCbareng.ttf|.otf if provided; else Fraunces
Black Soft as stand-in). Everything else = brand-kit fonts (Instrument Serif, Courier Prime, Caveat).
"""
import argparse, asyncio, datetime, os
import numpy as np
from PIL import Image
from playwright.async_api import async_playwright

KIT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
U = f"file://{KIT}"
BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus",
         "September", "Oktober", "November", "Desember"]
HARI = ["SENIN", "SELASA", "RABU", "KAMIS", "JUMAT", "SABTU", "MINGGU"]

TITLE_FONT = None
for cand in ["fonts/wfcbareng/WFCbareng.ttf", "fonts/wfcbareng/WFCbareng.otf"]:
    if os.path.exists(os.path.join(KIT, cand)):
        TITLE_FONT = cand
TITLE_FACE = (f"@font-face {{ font-family:'TT'; src:url('{U}/{TITLE_FONT}'); }}" if TITLE_FONT else
              f"@font-face {{ font-family:'TT'; src:url('{U}/fonts/Fraunces[SOFT,WONK,opsz,wght].ttf'); font-weight:100 900; }}")
TITLE_VARIATION = "" if TITLE_FONT else "font-weight:900; font-variation-settings:'SOFT' 100, 'WONK' 0, 'opsz' 144;"

THEMES = {
    "maroon": dict(bg="#660005", title="#F2C9CF", text="#FFFFFF", mk="#A3404F"),
    "pink":   dict(bg="#F2C9CF", title="#660005", text="#660005", mk="#FFFFFF"),
    "gray":   dict(bg="#EDEDED", title="#660005", text="#660005", mk="#F2C9CF"),
}
RED = "#660005"


def grain():
    path = os.path.join(KIT, "backgrounds/png/grain-overlay.png")
    if not os.path.exists(path):
        rng = np.random.default_rng(7)
        n = rng.random((1350, 1080))
        a = np.zeros((1350, 1080, 4), dtype=np.uint8)
        a[..., :3] = np.where((n < 0.5)[..., None], 0, 255)
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
.tt {{ font-family:'TT', serif; {TITLE_VARIATION} color:{t['title']}; text-shadow:0 7px 0 rgba(0,0,0,.13); }}
.serif {{ font-family:'IS', serif; font-weight:400; line-height:1.02; letter-spacing:-.5px; }}
.serif i {{ font-style:italic; }}
.mono {{ font-family:'CP', monospace; }}
.hand {{ font-family:'CV', cursive; font-weight:600; }}
.mk {{ background:linear-gradient(to bottom, transparent 52%, {t['mk']} 52%, {t['mk']} 80%, transparent 80%);
       -webkit-box-decoration-break:clone; box-decoration-break:clone; padding:0 8px; margin:0 -8px; }}
.card {{ position:absolute; z-index:2; background:#FFFFFF; color:{RED}; border-radius:28px; box-shadow:0 12px 30px rgba(0,0,0,.12); }}
.chip {{ display:inline-block; background:#FFFFFF; color:{RED}; font-family:'CP', monospace; font-weight:700; border-radius:12px; }}
.foot {{ position:absolute; z-index:2; bottom:56px; font-family:'CP', monospace; font-size:22px; letter-spacing:1px; color:{t['text']}; }}
img.st {{ position:absolute; z-index:3; }}
"""


def st(path, x, y, w, rot=0):
    return f'<img class="st" src="{U}/{path}" style="left:{x}px; top:{y}px; width:{w}px; transform:rotate({rot}deg);">'


def foot(i, total=4):
    return f'<div class="foot" style="left:90px;">@wfcditasik</div><div class="foot" style="right:90px;">0{i} / 0{total}</div>'


def poster(n, date, t, ill, qr):
    d = datetime.date.fromisoformat(date)
    tanggal = f"{d.day} {BULAN[d.month-1]} {d.year}"
    pill = f"background:#FFFFFF; color:{RED}; border-radius:26px; height:54px; display:flex; align-items:center; padding:0 22px; margin-bottom:12px; box-shadow:0 4px 10px rgba(0,0,0,.08);"
    rows = [("09.00 - 12.00", "Deep Work (No Distract)"), ("12.00 - 13.00", "Break &amp; Networking"), ("13.00 - End", "Continue Working")]
    sched = "".join(f'<div style="{pill}"><span class="mono" style="font-weight:700; font-size:17px; width:154px; flex:none;">{a}</span>'
                    f'<span class="serif" style="font-size:24px; white-space:nowrap;">{b}</span></div>' for a, b in rows)
    qr_html = (f'<img src="file://{os.path.abspath(qr)}" style="width:184px; height:184px; display:block; background:#fff; padding:10px; border-radius:14px;">' if qr else
               f'<div class="mono" style="width:184px; height:184px; background:#FFFFFF; border:4px dashed #DF8F9C; border-radius:14px; color:{RED}; display:flex; align-items:center; justify-content:center; text-align:center; font-size:20px; font-weight:700;">QR<br>CODE</div>')
    return f"""<div class="slide"><div class="grain"></div>
  <div class="abs tt" style="left:0; width:1080px; top:116px; text-align:center; font-size:238px; line-height:.57; letter-spacing:-7px;">WFC<br><span style="margin-left:-40px;">bareng</span></div>
  <div class="abs mono" style="left:0; width:1080px; top:504px; text-align:center; font-size:23px; font-weight:700; letter-spacing:2px; line-height:1.55;">CONNECTING TASIK REMOTE WORKERS,<br>FREELANCERS, CREATIVES, AND BUILDERS</div>
  <div class="abs" style="left:858px; top:122px; transform:rotate(-7deg); background:{t['title']}; color:{t['bg']}; padding:2px 20px 8px; box-shadow:0 6px 0 rgba(0,0,0,.13);"><span class="serif" style="font-size:84px; line-height:1;"><i>#{n}</i></span></div>
  {st('ui-accents/png/toggle-mode-fokus-green.png', 46, 88, 210, -7)}
  <div class="card" style="left:90px; top:632px; width:900px; height:410px; border-radius:36px;"></div>
  <img class="abs" src="file://{os.path.abspath(ill)}" style="left:285px; top:642px; width:510px; z-index:3;">
  <div class="abs" style="left:66px; top:636px; transform:rotate(-8deg); z-index:4; background:#F6CB45; color:{RED}; padding:6px 22px 12px; border-radius:6px; box-shadow:0 6px 14px rgba(0,0,0,.15);">
    <div class="serif" style="font-size:64px; line-height:1;"><i>Free</i></div>
    <div class="mono" style="font-size:16px; font-weight:700; margin-top:2px;">for member<br>WFCditasik</div></div>
  <div class="abs" style="left:90px; top:1078px; width:300px;">
    <div class="serif" style="font-size:92px; line-height:.9; color:{t['title']};">{HARI[d.weekday()].capitalize()}</div>
    <div class="mono" style="font-size:24px; font-weight:700; letter-spacing:1px; margin-top:10px;">{tanggal}</div>
    <div class="mono" style="font-size:21px; font-weight:700; letter-spacing:1px; line-height:1.45; margin-top:22px;">LANGGAM COFFEE &amp; BOOK<br>TARUMANAGARA</div></div>
  <div class="abs" style="left:398px; top:1090px; width:384px;">{sched}</div>
  <div class="abs" style="left:806px; top:1072px; width:184px; text-align:center;">
    <div class="mono" style="font-size:30px; font-weight:700; letter-spacing:2px; margin-bottom:10px;">REGISTER</div>{qr_html}</div>
</div>"""


CHECK = ('<svg width="30" height="30" viewBox="0 0 30 30" style="flex:none;"><rect x="2" y="2" width="26" height="26" rx="7" fill="#8FCB63" stroke="#2B0A0C" stroke-width="2.5"/>'
         '<path d="M8 15.5 L13 20 L22 10" fill="none" stroke="#2B0A0C" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>')
LOCK = ('<svg width="30" height="30" viewBox="0 0 30 30" style="flex:none;"><rect x="2" y="2" width="26" height="26" rx="7" fill="#EDEDED" stroke="#2B0A0C" stroke-width="2.5"/>'
        '<rect x="9" y="14" width="12" height="9" rx="2" fill="#A3404F" stroke="#2B0A0C" stroke-width="2"/>'
        '<path d="M11.5 14 V11.5 Q11.5 8 15 8 Q18.5 8 18.5 11.5 V14" fill="none" stroke="#2B0A0C" stroke-width="2"/></svg>')


def who(t):
    return f"""<div class="slide"><div class="grain"></div>
  <div class="abs serif" style="left:90px; top:150px; width:900px; font-size:156px; color:{t['title']};">Who can<br><span class="mk"><i>join?</i></span></div>
  <div class="abs" style="left:90px; top:500px;"><span class="chip" style="font-size:30px; letter-spacing:2px; padding:12px 26px;">MEMBER WFCDITASIK</span></div>
  <div class="card" style="left:90px; top:620px; width:900px; height:370px; padding:56px 60px;">
    <div class="serif" style="font-size:76px; line-height:1.05;">How to be a <i>member?</i></div>
    <div class="hand" style="font-size:50px; margin-top:14px; transform:rotate(-2deg); transform-origin:left;">It's very easy!</div>
    <div style="display:flex; align-items:center; gap:22px; margin-top:40px;">
      <span class="mono" style="flex:none; background:#8FCB63; color:#2B0A0C; border:3px solid #2B0A0C; border-radius:14px; font-size:30px; font-weight:700; padding:8px 18px;">Start from FREE</span>
      <span class="mono" style="font-size:25px; line-height:1.35;">bisa jadi member basic WFCditasik.</span></div>
  </div>
  {st('ui-accents/png/tag-wfc-blue.png', 880, 578, 130, 8)}
  <div class="abs hand" style="left:90px; top:1060px; font-size:46px; transform:rotate(-3deg); color:{t['text']};">sampai ketemu hari Kamis!</div>
  {foot(2)}
</div>"""


def benefits(t):
    def cell(ok, note=""):
        icon = CHECK if ok else LOCK
        txt = f'<span class="mono" style="font-size:19px; line-height:1.2;">{note}</span>' if note else ""
        return f'<div style="display:flex; align-items:center; gap:12px; padding:0 20px; border-left:2px solid #F2C9CF; border-top:2px solid #F2C9CF;">{icon}{txt}</div>'
    rows = [("Kartu digital member", (True, ""), (True, "")),
            ("Booking seat WFCbareng", (True, ""), (True, "")),
            ("Daftar event (RWH, dll)", (True, "harga normal"), (True, "harga khusus member")),
            ("Beli Career Guide", (True, "harga normal"), (True, "harga khusus member")),
            ("Redeem benefit cafe partner", (False, "terkunci"), (True, ""))]
    grid = "display:grid; grid-template-columns:330px 1fr 1fr;"
    body = "".join(f'<div style="{grid} height:104px;"><div class="mono" style="display:flex; align-items:center; padding:0 26px; border-top:2px solid #F2C9CF; font-size:23px; font-weight:700; line-height:1.25;">{f}</div>{cell(*b)}{cell(*p)}</div>'
                   for f, b, p in rows)
    head = "display:flex; align-items:center; justify-content:center; font-size:24px; font-weight:700; letter-spacing:1px; border-left:2px solid #F2C9CF;"
    return f"""<div class="slide"><div class="grain"></div>
  <div class="abs serif" style="left:90px; top:120px; width:900px; font-size:120px; color:{t['title']};">Member <span class="mk"><i>Basic</i></span><br>&amp; <i>Pro</i></div>
  <div class="abs" style="left:90px; top:395px;"><span class="chip" style="font-size:30px; padding:12px 26px;">Start from FREE</span></div>
  <div class="card" style="left:90px; top:500px; width:900px; overflow:hidden;">
    <div style="{grid} height:90px; background:#EDEDED;">
      <div class="mono" style="display:flex; align-items:center; padding:0 26px; font-size:24px; font-weight:700; letter-spacing:1px;">FITUR</div>
      <div class="mono" style="{head}">MEMBER BASIC</div><div class="mono" style="{head}">MEMBER PRO</div></div>
    {body}</div>
  {foot(3)}
</div>"""


def cta(t, website):
    web = (f'<span class="chip" style="font-size:36px; padding:14px 30px;">{website}</span>' if website else
           f'<span class="chip" style="font-size:30px; padding:14px 30px; border:3px dashed #DF8F9C;">[ link website ]</span>')
    return f"""<div class="slide"><div class="grain"></div>
  <div class="abs mono" style="left:90px; top:170px; font-size:26px; font-weight:700; letter-spacing:3px;">SIAP KERJA BARENG TIAP KAMIS?</div>
  <div class="abs serif" style="left:90px; top:240px; width:900px; font-size:150px; color:{t['title']};">Yuk, jadi<br><span class="mk"><i>member</i></span><br>WFCditasik.</div>
  <div class="abs mono" style="left:90px; top:760px; width:820px; font-size:30px; line-height:1.45;">Daftar &amp; cek semua benefit member<br>di website kami:</div>
  <div class="abs" style="left:90px; top:880px;">{web}</div>
  {st('ui-accents/png/button-join-green.png', 560, 1000, 300, -4)}
  {st('ui-accents/png/cursor-hand.png', 820, 1060, 80, 0)}
  <div class="abs hand" style="left:90px; top:1030px; font-size:46px; transform:rotate(-3deg); color:{t['text']};">see you di WFCbareng!</div>
  {foot(4)}
</div>"""


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--number", type=int, required=True)
    ap.add_argument("--date", required=True, help="Thursday date YYYY-MM-DD")
    ap.add_argument("--bg", choices=THEMES, required=True)
    ap.add_argument("--illustration", required=True)
    ap.add_argument("--qr")
    ap.add_argument("--website")
    ap.add_argument("--out")
    a = ap.parse_args()
    t = THEMES[a.bg]
    out = a.out or os.path.join(KIT, "posters", f"{a.date}-{a.number}")
    os.makedirs(out, exist_ok=True)
    slides = [poster(a.number, a.date, t, a.illustration, a.qr), who(t), benefits(t), cta(t, a.website)]
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for i, body in enumerate(slides, 1):
            html = f"<!doctype html><html><head><meta charset='utf-8'><style>{css(t)}</style></head><body>{body}</body></html>"
            f = os.path.join(out, f"slide-0{i}.html"); open(f, "w").write(html)
            await pg.goto(f"file://{f}"); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(200)
            await pg.screenshot(path=os.path.join(out, f"slide-0{i}.png"))
            os.remove(f)
        await b.close()
    print(out)

asyncio.run(main())
