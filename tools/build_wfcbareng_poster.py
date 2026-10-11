"""Build the weekly WFCbareng poster carousel (4 slides, 1080x1350).

Usage:
  python3 tools/build_wfcbareng_poster.py --number 11 --date 2026-10-15 --bg maroon \
      --illustration posters/2026-10-15-11/illustration.svg [--qr qr.png] [--website example.com]

Slides: 01 poster · 02 Who Can Join? · 03 member benefits · 04 join-member CTA.
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
  <div class="abs tt" style="left:0; width:1080px; top:66px; text-align:center; font-size:238px; line-height:.76; letter-spacing:-7px;">WFC<br><span style="margin-left:-40px;">bareng</span></div>
  <div class="abs mono" style="left:0; width:1080px; top:506px; text-align:center; font-size:23px; font-weight:700; letter-spacing:2px; line-height:1.55;">CONNECTING TASIK REMOTE WORKERS,<br>FREELANCERS, CREATIVES, AND BUILDERS</div>
  <div class="abs" style="left:858px; top:84px; transform:rotate(-7deg); background:{t['title']}; color:{t['bg']}; padding:2px 20px 8px; box-shadow:0 6px 0 rgba(0,0,0,.13);"><span class="serif" style="font-size:84px; line-height:1;"><i>#{n}</i></span></div>
  {st('ui-accents/png/toggle-mode-fokus-green.png', 46, 52, 210, -7)}
  <div class="card" style="left:90px; top:624px; width:900px; height:420px; border-radius:36px;"></div>
  <img class="abs" src="file://{os.path.abspath(ill)}" style="left:280px; top:634px; width:520px; z-index:3;">
  <div class="abs" style="left:66px; top:628px; transform:rotate(-8deg); z-index:4; background:#F6CB45; color:{RED}; padding:6px 22px 12px; border-radius:6px; box-shadow:0 6px 14px rgba(0,0,0,.15);">
    <div class="serif" style="font-size:64px; line-height:1;"><i>Free</i></div>
    <div class="mono" style="font-size:16px; font-weight:700; margin-top:2px;">for member &amp;<br>non-member</div></div>
  <div class="abs" style="left:90px; top:1078px; width:300px;">
    <div class="serif" style="font-size:92px; line-height:.9; color:{t['title']};">{HARI[d.weekday()].capitalize()}</div>
    <div class="mono" style="font-size:24px; font-weight:700; letter-spacing:1px; margin-top:10px;">{tanggal}</div>
    <div class="mono" style="font-size:21px; font-weight:700; letter-spacing:1px; line-height:1.45; margin-top:22px;">LANGGAM COFFEE &amp; BOOK<br>TARUMANAGARA</div></div>
  <div class="abs" style="left:398px; top:1090px; width:384px;">{sched}</div>
  <div class="abs" style="left:806px; top:1072px; width:184px; text-align:center;">
    <div class="mono" style="font-size:30px; font-weight:700; letter-spacing:2px; margin-bottom:10px;">REGISTER</div>{qr_html}</div>
</div>"""


def who(t):
    cell = "padding:0 26px; display:flex; align-items:center; border-top:2px solid #F2C9CF;"
    rows = [("#E0393E", "Seat", "Book langsung via QR", "Cek ketersediaan H&#8209;1"),
            ("#F6CB45", "Booking", "Scan &rarr; Book &rarr; Done!", "DM @wfcditasik di&nbsp;H&#8209;1"),
            ("#4D83C5", "Join", "Seat langsung terkonfirmasi", "Join jika masih tersedia")]
    body = "".join(
        f'<div style="display:grid; grid-template-columns:220px 1fr 1fr; height:120px;">'
        f'<div style="{cell}"><span style="width:16px; height:16px; border-radius:4px; background:{c}; margin-right:14px; flex:none;"></span><span class="serif" style="font-size:36px;">{a}</span></div>'
        f'<div class="mono" style="{cell} border-left:2px solid #F2C9CF; font-size:23px;">{b}</div>'
        f'<div class="mono" style="{cell} border-left:2px solid #F2C9CF; font-size:23px;">{c2}</div></div>'
        for c, a, b, c2 in rows)
    head = "display:flex; align-items:center; justify-content:center; font-size:25px; font-weight:700; letter-spacing:1px; border-left:2px solid #F2C9CF;"
    return f"""<div class="slide"><div class="grain"></div>
  <div class="abs serif" style="left:90px; top:150px; width:900px; font-size:156px; color:{t['title']};">Who can<br><span class="mk"><i>join?</i></span></div>
  <div class="abs" style="left:90px; top:500px;"><span class="chip" style="font-size:27px; letter-spacing:2px; padding:10px 24px;">MEMBER &amp; NON-MEMBER WFCDITASIK</span></div>
  <div class="card" style="left:90px; top:610px; width:900px; overflow:hidden;">
    <div style="display:grid; grid-template-columns:220px 1fr 1fr; height:96px; background:#EDEDED;">
      <div></div><div class="mono" style="{head}">MEMBER</div><div class="mono" style="{head}">NON-MEMBER</div></div>
    {body}</div>
  {st('ui-accents/png/tag-wfc-blue.png', 880, 568, 130, 8)}
  <div class="abs hand" style="left:90px; top:1100px; font-size:46px; transform:rotate(-3deg); color:{t['text']};">sampai ketemu hari Kamis!</div>
  {foot(2)}
</div>"""


def benefits(t):
    items = [("#F6CB45", "Member Pricing &ndash; Remote Worker Hangout", "Harga khusus untuk sesi belajar &amp; upgrade skill."),
             ("#4D83C5", "Member Pricing &ndash; Digital Resources", "Harga khusus untuk E-book, Career Guide, &amp; resources lainnya."),
             ("#8FCB63", "Connect with Your People", "Bangun koneksi dengan sesama remote worker di Tasik."),
             ("#E0393E", "Cafe Partner Perks", "Nikmati benefit &amp; special perks dari cafe partner WFCditasik.")]
    rows = "".join(
        f'<div style="display:flex; gap:22px; padding:26px 34px; {"border-top:2px solid #F2C9CF;" if i else ""}">'
        f'<span style="width:18px; height:18px; border-radius:5px; background:{c}; flex:none; margin-top:7px;"></span>'
        f'<div><div class="mono" style="font-size:25px; font-weight:700;">{a}</div>'
        f'<div class="mono" style="font-size:23px; margin-top:6px; line-height:1.35; color:#3A1A1C;">{b}</div></div></div>'
        for i, (c, a, b) in enumerate(items))
    return f"""<div class="slide"><div class="grain"></div>
  <div class="abs serif" style="left:90px; top:120px; width:900px; font-size:112px; color:{t['title']};">Join <span class="mk"><i>unlimited</i></span><br>WFCbareng session</div>
  <div class="abs" style="left:90px; top:385px;"><span class="chip" style="font-size:34px; padding:12px 26px;">sebagai Member WFCditasik</span></div>
  <div class="abs serif" style="left:90px; top:492px; font-size:58px; color:{t['title']};">Dan dapatkan <i>benefits</i> lainnya:</div>
  <div class="card" style="left:90px; top:600px; width:900px; overflow:hidden;">{rows}</div>
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
