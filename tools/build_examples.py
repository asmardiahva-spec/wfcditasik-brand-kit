"""Build 3 example WFCditasik carousels (3 slides each) from the brand kit."""
import os, asyncio
from playwright.async_api import async_playwright

KIT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUT = os.path.join(KIT, "examples")
U = f"file://{KIT}"

CSS = f"""
@font-face {{ font-family: 'IS'; src: url('{U}/fonts/InstrumentSerif-Regular.ttf'); }}
@font-face {{ font-family: 'IS'; font-style: italic; src: url('{U}/fonts/InstrumentSerif-Italic.ttf'); }}
@font-face {{ font-family: 'CP'; src: url('{U}/fonts/CourierPrime-Regular.ttf'); }}
@font-face {{ font-family: 'CP'; font-weight: 700; src: url('{U}/fonts/CourierPrime-Bold.ttf'); }}
@font-face {{ font-family: 'CV'; src: url('{U}/fonts/Caveat[wght].ttf'); font-weight: 400 700; }}
:root {{ --red:#660005; --pink:#DF8F9C; --pinksoft:#F2C9CF; --rose:#A3404F; --white:#FFFFFF; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1350px; overflow:hidden; }}
.slide {{ position:relative; width:1080px; height:1350px; background-size:cover; color:var(--red); }}
.serif {{ font-family:'IS', serif; font-weight:400; line-height:1.12; letter-spacing:-0.5px; }}
.serif i {{ font-style:italic; }}
.mono {{ font-family:'CP', monospace; line-height:1.45; }}
.hand {{ font-family:'CV', cursive; font-weight:500; line-height:1.1; }}
.abs {{ position:absolute; }}
/* marker: sits behind the lower part of the letters, one band per line */
.mk {{ background:linear-gradient(to bottom, transparent 52%, var(--pink) 52%, var(--pink) 80%, transparent 80%);
       -webkit-box-decoration-break:clone; box-decoration-break:clone; padding:0 8px; margin:0 -8px; }}
.mk.soft {{ background:linear-gradient(to bottom, transparent 52%, var(--pinksoft) 52%, var(--pinksoft) 80%, transparent 80%); }}
/* selected text with handles */
.mk.pk {{ background:linear-gradient(to bottom, transparent 52%, var(--pink) 52%, var(--pink) 80%, transparent 80%); }}
.sel.pk {{ background:var(--pinksoft); }}
.sel {{ position:relative; background:var(--pinksoft); padding:0 10px; margin:0 6px; }}
.sel .h {{ position:absolute; top:0; bottom:0; width:5px; background:var(--red); }}
.sel .h::after {{ content:''; position:absolute; left:-6.5px; width:18px; height:18px; border-radius:50%; background:var(--red); }}
.sel .l {{ left:-3px; }} .sel .l::after {{ top:-14px; }}
.sel .r {{ right:-3px; }} .sel .r::after {{ bottom:-14px; }}
.card {{ position:absolute; background:var(--white); box-shadow:0 10px 24px rgba(43,10,12,.16); }}
.page {{ position:absolute; right:90px; bottom:64px; font-family:'CP', monospace; font-size:22px; letter-spacing:2px; }}
.handle {{ position:absolute; left:90px; bottom:64px; font-family:'CP', monospace; font-size:22px; letter-spacing:1px; }}
img.st {{ position:absolute; }}
.chip {{ background:var(--white); padding:6px 14px; bottom:58px; }}
.handle.chip {{ left:84px; }} .page.chip {{ right:84px; }}
"""


def bg(name):
    return f"background-image:url('{U}/backgrounds/png/{name}.png');"


def st(path, x, y, w, rot=0, z=1):
    return (f'<img class="st" src="{U}/{path}" style="left:{x}px; top:{y}px; width:{w}px; '
            f'transform:rotate({rot}deg); z-index:{z};">')


def foot(n, color="var(--red)", chip=False):
    c = " chip" if chip else ""
    return (f'<div class="handle{c}" style="color:{color}">@wfcditasik</div>'
            f'<div class="page{c}" style="color:{color}">0{n} / 03</div>')


SLIDES = {}

# ---------------- A. Lifestyle: Minuman kamu = kerjaan kamu ----------------
SLIDES["A-minuman-kerjaan"] = [
    # A1 cover: diner checker, white card, tape, notification sticker
    f"""<div class="slide" style="{bg('stripes-red')}">
      <div class="card" style="left:90px; top:250px; width:820px; height:660px; transform:rotate(-2deg);"></div>
      {st('paper/png/tape-gray.png', 380, 205, 300, -4, 3)}
      <div class="abs" style="left:150px; top:330px; width:720px; transform:rotate(-2deg); z-index:2;">
        <div class="mono" style="font-size:26px; letter-spacing:3px; color:var(--red);">TES KEPRIBADIAN (NGGAK ILMIAH)</div>
        <div class="serif" style="font-size:128px; margin-top:26px;">Minuman kamu<br>= <span class="mk pk"><i>kerjaan</i></span><br>kamu</div>
      </div>
      <div class="hand abs" style="left:520px; top:800px; font-size:50px; transform:rotate(-5deg); z-index:2; color:var(--red);">geser, terus ngaku →</div>
      {st('ui-stickers/png/notification-pill.png', 390, 980, 580, 4, 4)}
      {foot(1, chip=True)}
    </div>""",
    # A2 content: gray, list with marker on drink names, reminders sticker
    f"""<div class="slide" style="{bg('solid-gray')}">
      <div class="serif abs" style="left:90px; top:150px; font-size:92px; width:900px;">Kamu tim <i>yang mana?</i></div>
      {st('ui-stickers/png/reminders-card.png', 90, 1010, 190, -7, 2)}
      <div class="abs" style="left:90px; top:370px; width:900px;">
        <div class="serif" style="font-size:64px;"><span class="mk">Kopi susu</span></div>
        <div class="mono" style="font-size:30px; margin:14px 0 54px;">= deadline jam 5 sore, baru mulai jam 4.</div>
        <div class="serif" style="font-size:64px;"><span class="mk">Matcha latte</span></div>
        <div class="mono" style="font-size:30px; margin:14px 0 54px;">= meeting yang harusnya cukup lewat email.</div>
        <div class="serif" style="font-size:64px;"><span class="mk">Es teh manis</span></div>
        <div class="mono" style="font-size:30px; margin-top:14px;">= "nanti aja deh" (padahal nggak nanti).</div>
      </div>
      <div class="hand abs" style="left:310px; top:1080px; font-size:48px; transform:rotate(-4deg); color:var(--red);">air putih = sudah tercerahkan</div>
      {foot(2)}
    </div>""",
    # A3 CTA: solid red, white/pink text, white scrap with tape
    f"""<div class="slide" style="{bg('solid-red')}">
      <div class="serif abs" style="left:90px; top:230px; width:920px; font-size:104px; color:var(--white);">Komen minuman<br>kamu, <i style="color:var(--pinksoft);">kita tebak</i><br>kerjaanmu.</div>
      <div class="card" style="left:300px; top:790px; width:560px; height:230px; transform:rotate(3deg);"></div>
      {st('paper/png/tape-gray.png', 360, 760, 200, -8, 3)}
      <div class="abs mono" style="left:340px; top:860px; width:500px; transform:rotate(3deg); font-size:40px; font-weight:700; z-index:2; text-align:center;">Follow @wfcditasik</div>
      <div class="abs hand" style="left:340px; top:925px; width:500px; transform:rotate(3deg); font-size:40px; color:var(--red); z-index:2; text-align:center;">biar ada temen kerja</div>
      {st('ui-stickers/png/cursor-arrow.png', 790, 940, 90, -10, 4)}
      {foot(3, 'var(--pinksoft)')}
    </div>""",
]

# ---------------- B. Skills & Tools: WFC tapi beneran kerja ----------------
SLIDES["B-wfc-beneran-kerja"] = [
    # B1 cover: white grid, selected-text highlight + copy bar sticker
    f"""<div class="slide" style="{bg('grid-paper-white')}">
      {st('ui-stickers/png/copy-select-bar.png', 60, 300, 420, 0, 3)}
      <div class="serif abs" style="left:96px; top:420px; width:920px; font-size:150px;"><span class="sel pk"><span class="h l"></span><i>Beneran</i><span class="h r"></span></span> kerja,<br>bukan cuma WFC.</div>
      <div class="hand abs" style="left:96px; top:850px; font-size:56px; transform:rotate(-3deg); color:var(--red);">(alias pindah tempat scroll)</div>
      {st('ui-stickers/png/status-wifi-battery.png', 640, 1020, 340, 5, 2)}
      {foot(1)}
    </div>""",
    # B2 content: pink stripes, lined note with 3 rules
    f"""<div class="slide" style="{bg('grid-paper-gray')}">
      {st('paper/png/note-lined.png', 70, 210, 940, 2, 1)}
      {st('paper/png/tape-red.png', 420, 180, 240, -3, 3)}
      <div class="abs" style="left:180px; top:300px; width:760px; transform:rotate(2deg); z-index:2;">
        <div class="serif" style="font-size:76px;"><span class="mk">3 aturan</span> <i>kecil</i></div>
        <div class="mono" style="font-size:32px; margin-top:34px;"><b>01</b>&nbsp; Tulis 1 target sebelum pesan minum.</div>
        <div class="mono" style="font-size:32px; margin-top:24px;"><b>02</b>&nbsp; Cari colokan dulu, baru laptop.</div>
        <div class="mono" style="font-size:32px; margin-top:24px;"><b>03</b>&nbsp; HP mode senyap 50 menit. Beneran.</div>
      </div>
      <div class="card" style="left:560px; top:930px; width:420px; height:150px; transform:rotate(-4deg);"></div>
      <div class="hand abs" style="left:590px; top:965px; width:380px; font-size:48px; transform:rotate(-4deg); z-index:2;">kecil, tapi ngaruh</div>
      {foot(2, chip=True)}
    </div>""",
    # B3 CTA: gray, folder sticker, save prompt
    f"""<div class="slide" style="{bg('solid-gray')}">
      {st('ui-stickers/png/folder-pink.png', 600, 170, 370, 6, 2)}
      <div class="hand abs" style="left:620px; top:520px; font-size:44px; transform:rotate(6deg); color:var(--red);">folder: niat 2026</div>
      <div class="serif abs" style="left:90px; top:680px; width:900px; font-size:108px;">Simpan dulu,<br><span class="mk"><i>praktekkin</i></span> Kamis ini.</div>
      <div class="mono abs" style="left:90px; top:1020px; width:820px; font-size:30px;">Tag partner WFC kamu &amp; follow @wfcditasik<br>buat kerja bareng tiap Kamis.</div>
      {foot(3)}
    </div>""",
]

# ---------------- C. Community: kerja sendiri vs kerja bareng ----------------
SLIDES["C-sendiri-vs-bareng"] = [
    # C1 cover: solid red, white text, weather widget
    f"""<div class="slide" style="{bg('solid-red')}">
      <div class="mono abs" style="left:90px; top:150px; font-size:26px; letter-spacing:3px; color:var(--pinksoft);">STUDI KASUS: KITA SEMUA</div>
      <div class="serif abs" style="left:90px; top:250px; width:900px; font-size:140px; color:var(--white);">Kerja <i style="color:var(--pinksoft);">sendiri</i><br>vs kerja<br>bareng</div>
      {st('ui-stickers/png/widget-weather-tasik.png', 560, 880, 420, -5, 2)}
      <div class="hand abs" style="left:96px; top:960px; font-size:52px; transform:rotate(-4deg); color:var(--pinksoft);">spoiler: yang kedua.</div>
      {foot(1, 'var(--pinksoft)')}
    </div>""",
    # C2 content: red checker, two white scraps
    f"""<div class="slide" style="{bg('checker-red-gray')}">
      <div class="card" style="left:90px; top:170px; width:640px; height:400px; transform:rotate(-3deg);"></div>
      <div class="abs" style="left:140px; top:200px; width:560px; transform:rotate(-3deg); z-index:2;">
        <div class="serif" style="font-size:74px;"><i>Sendiri</i></div>
        <div class="mono" style="font-size:30px; margin-top:20px;">Fokus 20 menit.<br>Buka TikTok 40 menit.<br>Ulangi sampai maghrib.</div>
      </div>
      {st('paper/png/tape-gray.png', 330, 120, 200, 4, 3)}
      <div class="card" style="left:350px; top:690px; width:640px; height:400px; transform:rotate(2.5deg);"></div>
      <div class="abs" style="left:400px; top:750px; width:560px; transform:rotate(2.5deg); z-index:2;">
        <div class="serif" style="font-size:74px;"><span class="mk"><i>Bareng</i></span></div>
        <div class="mono" style="font-size:30px; margin-top:20px;">Malu buka TikTok,<br>ada yang lihat.<br>Kerjaan beres. Wow.</div>
      </div>
      {st('paper/png/tape-red.png', 590, 670, 200, -5, 3)}
      {foot(2, chip=True)}
    </div>""",
    # C3 CTA: white, Thursday invite with marker, polaroid-style card
    f"""<div class="slide" style="{bg('solid-white')}">
      <div class="serif abs" style="left:90px; top:200px; width:900px; font-size:116px;">Yuk WFC bareng,<br><span class="mk pk"><i>tiap Kamis.</i></span></div>
      <div class="mono abs" style="left:90px; top:520px; width:620px; font-size:32px;">Bawa laptop, bawa kerjaan.<br>Teman kerjanya dari kami.</div>
      <div class="abs" style="left:90px; top:760px; width:900px; height:420px; background:var(--red);"></div>
      {st('ui-stickers/png/notification-pill.png', 380, 700, 580, -4, 2)}
      {st('paper/png/tape-gray.png', 120, 735, 220, -6, 3)}
      <div class="mono abs" style="left:150px; top:950px; font-size:44px; font-weight:700; color:var(--white);">Follow @wfcditasik</div>
      <div class="hand abs" style="left:156px; top:1020px; font-size:48px; transform:rotate(-2deg); color:var(--pinksoft);">biar nggak ketinggalan info</div>
      {foot(3)}
    </div>""",
]


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for name, slides in SLIDES.items():
            d = os.path.join(OUT, name); os.makedirs(d, exist_ok=True)
            for i, body in enumerate(slides, 1):
                html = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"
                f = os.path.join(d, f"slide-0{i}.html"); open(f, "w").write(html)
                await pg.goto(f"file://{f}"); await pg.evaluate("document.fonts.ready")
                await pg.wait_for_timeout(150)
                await pg.screenshot(path=os.path.join(d, f"slide-0{i}.png"))
        await b.close()

asyncio.run(main())
