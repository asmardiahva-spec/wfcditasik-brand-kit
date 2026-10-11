"""Generate WFCditasik brand kit SVGs + PNG exports.
Palette: Blood Red #660005, cool light gray #EDEDED, White #FFFFFF, Ruddy Pink #DF8F9C (accent only)."""
import os, sys, cairosvg

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
MAROON = "#660005"
MAROON_DK = "#3F0003"
PINK = "#DF8F9C"
PINK_SOFT = "#F2C9CF"
ROSE = "#A3404F"
GRAY = "#EDEDED"
PAPER = "#FFFFFF"
INK = "#2B0A0C"
GRID = "#D9D9D9"

SANS = "Helvetica, Arial, sans-serif"
SERIF = "'Instrument Serif', Georgia, serif"
MONO = "'Courier Prime', 'Courier New', monospace"
HAND = "Caveat, cursive"

SHADOW = """<filter id="sh" x="-20%" y="-20%" width="140%" height="150%">
<feDropShadow dx="0" dy="6" stdDeviation="7" flood-color="#2B1B18" flood-opacity="0.18"/></filter>"""


def svg(w, h, body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}"><defs>{defs}</defs>{body}</svg>\n')


def save(rel, content, scale=2):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    png = path.replace("/svg/", "/png/").replace(".svg", ".png")
    os.makedirs(os.path.dirname(png), exist_ok=True)
    cairosvg.svg2png(bytestring=content.encode(), write_to=png, scale=scale)


def sticker(w, h, inner, pad=24):
    """Wrap a shape group in a white die-cut outline + soft shadow."""
    W, H = w + pad * 2, h + pad * 2
    body = (f'<g filter="url(#sh)"><g transform="translate({pad},{pad})">'
            f'<g stroke="#FFFFFF" stroke-width="16" stroke-linejoin="round" fill="#FFFFFF">{inner["outline"]}</g>'
            f'{inner["art"]}</g></g>')
    return svg(W, H + 10, body, SHADOW)


# ---------------- BACKGROUNDS (1080x1350, IG 4:5) ----------------
W, H = 1080, 1350


def grid_paper(base=None, grid=None):
    base = base or GRAY
    grid = grid or GRID
    step = 36
    lines = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}"/>' for x in range(0, W + 1, step))
    lines += "".join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>' for y in range(0, H + 1, step))
    return svg(W, H, f'<rect width="{W}" height="{H}" fill="{base}"/>'
                     f'<g stroke="{grid}" stroke-width="1.5">{lines}</g>')


def checker(c1, c2, size=90):
    defs = (f'<pattern id="ck" width="{size*2}" height="{size*2}" patternUnits="userSpaceOnUse">'
            f'<rect width="{size*2}" height="{size*2}" fill="{c1}"/>'
            f'<rect width="{size}" height="{size}" fill="{c2}"/>'
            f'<rect x="{size}" y="{size}" width="{size}" height="{size}" fill="{c2}"/></pattern>')
    return svg(W, H, f'<rect width="{W}" height="{H}" fill="url(#ck)"/>', defs)


def stripes(c1, c2, w=40):
    defs = (f'<pattern id="st" width="{w*2}" height="10" patternUnits="userSpaceOnUse">'
            f'<rect width="{w*2}" height="10" fill="{c1}"/><rect width="{w}" height="10" fill="{c2}"/></pattern>')
    return svg(W, H, f'<rect width="{W}" height="{H}" fill="url(#st)"/>', defs)


def solid(c):
    return svg(W, H, f'<rect width="{W}" height="{H}" fill="{c}"/>')


def dashed_frame(bg, card, dash):
    return svg(W, H, f'<rect width="{W}" height="{H}" fill="{bg}"/>'
                     f'<rect x="90" y="110" width="{W-180}" height="{H-220}" rx="34" fill="{card}"/>'
                     f'<rect x="120" y="140" width="{W-240}" height="{H-280}" rx="22" fill="none" '
                     f'stroke="{dash}" stroke-width="4" stroke-dasharray="16 12"/>')


save("backgrounds/svg/grid-paper-gray.svg", grid_paper())
save("backgrounds/svg/grid-paper-white.svg", grid_paper("#FFFFFF", "#E6E6E6"))
save("backgrounds/svg/solid-white.svg", solid("#FFFFFF"))
save("backgrounds/svg/checker-red-white.svg", checker("#FFFFFF", MAROON))
save("backgrounds/svg/checker-red-gray.svg", checker(GRAY, MAROON))
save("backgrounds/svg/stripes-red.svg", stripes(GRAY, MAROON, 26))
save("backgrounds/svg/solid-red.svg", solid(MAROON))
save("backgrounds/svg/solid-gray.svg", solid(GRAY))
save("backgrounds/svg/dashed-card-on-gray.svg",
     dashed_frame(GRAY, PAPER, MAROON))
save("backgrounds/svg/dashed-card-on-red.svg", dashed_frame(MAROON, GRAY, PINK))

# ---------------- UI STICKERS ----------------

# 1. Selection handles (left + right), for the signature highlight
def handle(flip=False):
    # bar + dot; dot on top for left handle, bottom for right handle
    dot_y = 10 if not flip else 150
    art = (f'<rect x="7" y="10" width="6" height="140" rx="3" fill="{MAROON}"/>'
           f'<circle cx="10" cy="{dot_y}" r="10" fill="{MAROON}"/>')
    return svg(20, 160, art)


save("ui-stickers/svg/selection-handle-left.svg", handle(False), 4)
save("ui-stickers/svg/selection-handle-right.svg", handle(True), 4)

# 2. Copy / Select All / Share bar
bar_w, bar_h = 420, 64
outline = f'<rect width="{bar_w}" height="{bar_h}" rx="14"/>'
art = (f'<rect width="{bar_w}" height="{bar_h}" rx="14" fill="#EEEEEE"/>'
       f'<line x1="118" y1="14" x2="118" y2="50" stroke="#CCCCCC" stroke-width="2"/>'
       f'<line x1="282" y1="14" x2="282" y2="50" stroke="#CCCCCC" stroke-width="2"/>'
       f'<g font-family="{SANS}" font-size="24" fill="{INK}" text-anchor="middle">'
       f'<text x="59" y="41">Copy</text><text x="200" y="41">Select All</text>'
       f'<text x="351" y="41">Share…</text></g>'
       f'<path d="M190 {bar_h} l12 14 l12 -14z" fill="#EEEEEE"/>')
save("ui-stickers/svg/copy-select-bar.svg", sticker(bar_w, bar_h + 14, {"outline": outline, "art": art}))

# 3. Notification pill
pw, ph = 560, 120
outline = f'<rect width="{pw}" height="{ph}" rx="28"/>'
art = (f'<rect width="{pw}" height="{ph}" rx="28" fill="{PAPER}"/>'
       f'<rect x="20" y="22" width="76" height="76" rx="18" fill="{MAROON}"/>'
       f'<text x="58" y="74" font-family="{SERIF}" font-size="40" fill="{GRAY}" text-anchor="middle">wfc</text>'
       f'<text x="116" y="48" font-family="{SANS}" font-size="20" font-weight="bold" fill="{INK}">WFC di Tasik</text>'
       f'<text x="{pw-24}" y="48" font-family="{SANS}" font-size="18" fill="#999999" text-anchor="end">now</text>'
       f'<text x="116" y="82" font-family="{SANS}" font-size="22" fill="{INK}">Kopi sudah siap. Laptop kamu?</text>')
save("ui-stickers/svg/notification-pill.svg", sticker(pw, ph, {"outline": outline, "art": art}))

# 4. Folder (pink)
fw, fh = 240, 180
folder_path = f"M0 30 Q0 14 16 14 H86 Q96 14 102 24 L110 36 H{fw-16} Q{fw} 36 {fw} 52 V{fh-16} Q{fw} {fh} {fw-16} {fh} H16 Q0 {fh} 0 {fh-16}Z"
outline = f'<path d="{folder_path}"/>'
art = (f'<path d="{folder_path}" fill="{ROSE}"/>'
       f'<rect x="0" y="56" width="{fw}" height="{fh-56}" rx="16" fill="{PINK}"/>'
       f'<rect x="0" y="56" width="{fw}" height="10" fill="{PINK_SOFT}" opacity="0.6"/>')
save("ui-stickers/svg/folder-pink.svg", sticker(fw, fh, {"outline": outline, "art": art}))

# 5. Weather-style widget, Tasik version
ww, wh = 360, 190
outline = f'<rect width="{ww}" height="{wh}" rx="26"/>'
art = (f'<rect width="{ww}" height="{wh}" rx="26" fill="{ROSE}"/>'
       f'<text x="24" y="40" font-family="{SANS}" font-size="20" fill="{GRAY}">Tasikmalaya</text>'
       f'<text x="20" y="118" font-family="{SANS}" font-size="74" fill="{GRAY}">27°</text>'
       f'<text x="{ww-24}" y="40" font-family="{SANS}" font-size="20" fill="{GRAY}" text-anchor="end">Hujan sore</text>'
       f'<text x="{ww-24}" y="68" font-family="{SANS}" font-size="18" fill="{PINK_SOFT}" text-anchor="end">cocok buat WFC</text>'
       + "".join(f'<circle cx="{40+i*56}" cy="160" r="9" fill="{PINK_SOFT if i<3 else GRAY}"/>' for i in range(6)))
save("ui-stickers/svg/widget-weather-tasik.svg", sticker(ww, wh, {"outline": outline, "art": art}))

# 6. Reminders / to-do card
rw, rh = 220, 220
outline = f'<rect width="{rw}" height="{rh}" rx="48"/>'
dots = [MAROON, ROSE, PINK]
art = f'<rect width="{rw}" height="{rh}" rx="48" fill="{PAPER}"/>' + "".join(
    f'<circle cx="54" cy="{58+i*52}" r="14" fill="none" stroke="{c}" stroke-width="5"/>'
    f'<circle cx="54" cy="{58+i*52}" r="7" fill="{c}"/>'
    f'<rect x="84" y="{54+i*52}" width="96" height="8" rx="4" fill="#DCDCDC"/>' for i, c in enumerate(dots))
save("ui-stickers/svg/reminders-card.svg", sticker(rw, rh, {"outline": outline, "art": art}))

# 7. Wi-Fi + battery status pill
sw, sh = 320, 76
outline = f'<rect width="{sw}" height="{sh}" rx="38"/>'
wifi = (f'<g transform="translate(36,20)" fill="none" stroke="{GRAY}" stroke-width="5" stroke-linecap="round">'
        f'<path d="M0 14 Q22 -6 44 14"/><path d="M8 24 Q22 12 36 24"/></g>'
        f'<circle cx="58" cy="54" r="5" fill="{GRAY}"/>')
art = (f'<rect width="{sw}" height="{sh}" rx="38" fill="{MAROON}"/>' + wifi +
       f'<text x="104" y="48" font-family="{SANS}" font-size="22" fill="{GRAY}">wifi kencang</text>'
       f'<rect x="246" y="26" width="44" height="24" rx="6" fill="none" stroke="{GRAY}" stroke-width="3"/>'
       f'<rect x="250" y="30" width="30" height="16" rx="3" fill="{PINK}"/>'
       f'<rect x="292" y="33" width="4" height="10" rx="2" fill="{GRAY}"/>')
save("ui-stickers/svg/status-wifi-battery.svg", sticker(sw, sh, {"outline": outline, "art": art}))

# 8. Cursor arrow
cur = "M0 0 L0 56 L14 43 L24 66 L34 61 L24 39 L42 39Z"
outline = f'<path d="{cur}"/>'
art = f'<path d="{cur}" fill="{INK}" stroke="{PAPER}" stroke-width="3" stroke-linejoin="round"/>'
save("ui-stickers/svg/cursor-arrow.svg", sticker(42, 66, {"outline": outline, "art": art}, pad=16), 4)

# 9. Polaroid frame (empty photo slot)
qw, qh = 320, 380
outline = f'<rect width="{qw}" height="{qh}"/>'
art = (f'<rect width="{qw}" height="{qh}" fill="{PAPER}"/>'
       f'<rect x="20" y="20" width="{qw-40}" height="{qw-40}" fill="#D6D6D6"/>'
       f'<text x="{qw/2}" y="{qh-24}" font-family="{HAND}" font-size="34" fill="{MAROON}" text-anchor="middle">tempel foto di sini</text>')
save("ui-stickers/svg/polaroid-frame.svg", sticker(qw, qh, {"outline": outline, "art": art}))

# 10. Washi tape strips
def tape(color, name):
    tw, th = 220, 56
    edge = "".join(f"L{tw - (6 if i % 2 else 0)} {i*7}" for i in range(1, 9))
    d = f"M0 0 L{tw} 0 {edge} L0 {th} " + "".join(f"L{6 if i % 2 else 0} {th - i*7}" for i in range(1, 9)) + "Z"
    save(f"paper/svg/tape-{name}.svg", svg(tw, th, f'<path d="{d}" fill="{color}" opacity="0.82"/>'))


tape(PINK, "pink")
tape("#CFCFCF", "gray")
tape(MAROON, "red")

# 11. Note paper scrap (lined) and torn-edge strip
nw, nh = 460, 300
lines = "".join(f'<line x1="24" y1="{70+i*40}" x2="{nw-24}" y2="{70+i*40}" stroke="#DEDEDE" stroke-width="2"/>' for i in range(6))
save("paper/svg/note-lined.svg", svg(nw + 20, nh + 20,
     f'<g filter="url(#sh)"><rect x="10" y="6" width="{nw}" height="{nh}" fill="{PAPER}"/>{lines}'
     f'<line x1="70" y1="6" x2="70" y2="{nh+6}" stroke="{MAROON}" stroke-opacity="0.35" stroke-width="2"/></g>', SHADOW))

import random
random.seed(7)
tw = 900
pts = " ".join(f"L{x} {random.randint(0, 14)}" for x in range(0, tw + 1, 18))
save("paper/svg/torn-strip-gray.svg", svg(tw, 180,
     f'<g filter="url(#sh)"><path d="M0 8 {pts} L{tw} 140 L0 140Z" fill="{GRAY}"/></g>', SHADOW))

# ---------------- POP ACCENT UI (tiny elements only) ----------------
LEAF = "#8FCB63"
DENIM = "#4D83C5"
BRAVE = "#E0393E"
BLOSSOM = "#F4B6C2"
SUNNY = "#F6CB45"


def pill_button(label, color, text="#FFFFFF", w=None):
    w = w or (60 + len(label) * 17)
    h = 64
    outline = f'<rect width="{w}" height="{h}" rx="32"/>'
    art = (f'<rect width="{w}" height="{h}" rx="32" fill="{color}"/>'
           f'<text x="{w/2}" y="42" font-family="{SANS}" font-size="26" font-weight="bold" fill="{text}" text-anchor="middle">{label}</text>')
    return sticker(w, h, {"outline": outline, "art": art}, pad=18)


save("ui-accents/svg/button-follow-red.svg", pill_button("Follow", BRAVE))
save("ui-accents/svg/button-join-green.svg", pill_button("Ikut WFC", LEAF, INK))
save("ui-accents/svg/button-save-blue.svg", pill_button("Simpan", DENIM))
save("ui-accents/svg/button-yes-yellow.svg", pill_button("Gas!", SUNNY, INK))


def progress(label, pct, color, w=420):
    h = 110
    bw = w - 48
    outline = f'<rect width="{w}" height="{h}" rx="18"/>'
    art = (f'<rect width="{w}" height="{h}" rx="18" fill="{PAPER}"/>'
           f'<text x="24" y="42" font-family="{SANS}" font-size="22" fill="{INK}">{label}</text>'
           f'<text x="{w-24}" y="42" font-family="{SANS}" font-size="22" fill="#888888" text-anchor="end">{pct}%</text>'
           f'<rect x="24" y="62" width="{bw}" height="18" rx="9" fill="#E3E3E3"/>'
           f'<rect x="24" y="62" width="{bw*pct/100:.0f}" height="18" rx="9" fill="{color}"/>')
    return sticker(w, h, {"outline": outline, "art": art}, pad=18)


save("ui-accents/svg/progress-produktif-green.svg", progress("Produktivitas", 70, LEAF))
save("ui-accents/svg/progress-semangat-yellow.svg", progress("Loading semangat...", 45, SUNNY))
save("ui-accents/svg/progress-deadline-red.svg", progress("Deadline", 90, BRAVE))


def toggle(label, color, on=True, w=360):
    h = 84
    kx = w - 56 if on else w - 108
    outline = f'<rect width="{w}" height="{h}" rx="20"/>'
    art = (f'<rect width="{w}" height="{h}" rx="20" fill="{PAPER}"/>'
           f'<text x="24" y="52" font-family="{SANS}" font-size="24" fill="{INK}">{label}</text>'
           f'<rect x="{w-128}" y="22" width="92" height="40" rx="20" fill="{color if on else "#D6D6D6"}"/>'
           f'<circle cx="{kx}" cy="42" r="16" fill="#FFFFFF"/>')
    return sticker(w, h, {"outline": outline, "art": art}, pad=18)


save("ui-accents/svg/toggle-mode-fokus-green.svg", toggle("Mode fokus", LEAF))
save("ui-accents/svg/toggle-notif-off.svg", toggle("Notif HP", LEAF, on=False))


def checklist(items, color, w=420):
    h = 40 + 56 * len(items)
    outline = f'<rect width="{w}" height="{h}" rx="18"/>'
    art = f'<rect width="{w}" height="{h}" rx="18" fill="{PAPER}"/>'
    for i, (t, done) in enumerate(items):
        y = 28 + i * 56
        if done:
            art += (f'<rect x="24" y="{y}" width="30" height="30" rx="7" fill="{color}"/>'
                    f'<path d="M31 {y+15} l6 7 l11 -13" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
                    f'<text x="72" y="{y+23}" font-family="{SANS}" font-size="24" fill="#999999" text-decoration="line-through">{t}</text>'
                    )
        else:
            art += (f'<rect x="25" y="{y+1}" width="28" height="28" rx="7" fill="none" stroke="#BBBBBB" stroke-width="3"/>'
                    f'<text x="72" y="{y+23}" font-family="{SANS}" font-size="24" fill="{INK}">{t}</text>')
    return sticker(w, h, {"outline": outline, "art": art}, pad=18)


save("ui-accents/svg/checklist-wfc-blue.svg", checklist([("Pesan kopi", 1), ("Cari colokan", 1), ("Kerja beneran", 0)], DENIM))


def chip(label, bg, fg):
    w = 36 + len(label) * 14
    h = 44
    outline = f'<rect width="{w}" height="{h}" rx="8"/>'
    art = (f'<rect width="{w}" height="{h}" rx="8" fill="{bg}"/>'
           f'<text x="{w/2}" y="30" font-family="{SANS}" font-size="22" fill="{fg}" text-anchor="middle">{label}</text>')
    return sticker(w, h, {"outline": outline, "art": art}, pad=14)


for label, bg, fg, name in [("WFC", "#DCE8F6", DENIM, "wfc-blue"), ("Deadline", "#FBDCDC", BRAVE, "deadline-red"),
                            ("Santai", "#E4F3D8", "#4E8A2A", "santai-green"), ("Kopi", "#FDF1C9", "#9A7410", "kopi-yellow"),
                            ("Fokus", "#FBE6EA", "#B8546A", "fokus-blossom")]:
    save(f"ui-accents/svg/tag-{name}.svg", chip(label, bg, fg))


# pointing-hand cursor
hand = ("M18 4 Q18 0 22 0 Q26 0 26 4 V30 Q28 27 31 27 Q35 27 35 31 V33 Q37 30 40 30 Q44 30 44 34 V36 "
        "Q46 33 49 33 Q53 33 53 37 V54 Q53 70 40 70 H28 Q20 70 15 62 L4 44 Q2 40 5 38 Q8 36 11 39 L18 47Z")
save("ui-accents/svg/cursor-hand.svg", sticker(56, 72, {"outline": f'<path d="{hand}"/>',
     "art": f'<path d="{hand}" fill="#FFFFFF" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'}, pad=14), 4)

# notification badge
save("ui-accents/svg/badge-red-3.svg", sticker(56, 56, {"outline": '<circle cx="28" cy="28" r="28"/>',
     "art": f'<circle cx="28" cy="28" r="28" fill="{BRAVE}"/><text x="28" y="38" font-family="{SANS}" font-size="28" font-weight="bold" fill="#FFFFFF" text-anchor="middle">3</text>'}, pad=12), 3)

# blue arrow cursor (tiny accent)
cur2 = "M0 0 L0 56 L14 43 L24 66 L34 61 L24 39 L42 39Z"
save("ui-accents/svg/cursor-arrow-blue.svg", sticker(42, 66, {"outline": f'<path d="{cur2}"/>',
     "art": f'<path d="{cur2}" fill="{DENIM}" stroke="#FFFFFF" stroke-width="3" stroke-linejoin="round"/>'}, pad=16), 4)


# ---------------- HIGHLIGHT STYLES (reference renders) ----------------
from PIL import ImageFont
F = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fonts", "")
REG = ImageFont.truetype(F + "InstrumentSerif-Regular.ttf", 96)
ITA = ImageFont.truetype(F + "InstrumentSerif-Italic.ttf", 96)


def tw(parts):
    """Measured width of [(text, italic), ...] at 96px."""
    return sum((ITA if it else REG).getlength(t) for t, it in parts)


def tspans(parts):
    return "".join(f'<tspan font-style="italic">{t}</tspan>' if it else t for t, it in parts)


def marker_line(x, base, parts, size=96, pad=8, color=None):
    color = color or PINK
    """Marker band: from ~x-height middle to just under baseline. Never reaches other lines."""
    w = tw(parts)
    top, h = base - size * 0.30, size * 0.36
    return (f'<rect x="{x-pad}" y="{top:.1f}" width="{w+pad*2:.1f}" height="{h:.1f}" rx="3" fill="{color}"/>'
            f'<text x="{x}" y="{base}" font-family="{SERIF}" font-size="{size}" fill="{MAROON}">{tspans(parts)}</text>')


def selected_line(x, base, parts, size=96, pad=10):
    """Selection block: cap-height to descender, with maroon handles."""
    w = tw(parts) + pad * 2
    top, h = base - size * 0.78, size * 0.98
    x0, x1 = x - pad, x - pad + w
    return (f'<rect x="{x0}" y="{top:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{PINK_SOFT}"/>'
            f'<rect x="{x0-3}" y="{top:.1f}" width="5" height="{h:.1f}" fill="{MAROON}"/>'
            f'<circle cx="{x0-0.5}" cy="{top:.1f}" r="9" fill="{MAROON}"/>'
            f'<rect x="{x1-2}" y="{top:.1f}" width="5" height="{h:.1f}" fill="{MAROON}"/>'
            f'<circle cx="{x1+0.5}" cy="{top+h:.1f}" r="9" fill="{MAROON}"/>'
            f'<text x="{x}" y="{base}" font-family="{SERIF}" font-size="{size}" fill="{MAROON}">{tspans(parts)}</text>')


def highlight_demo():
    H2 = 1120
    body = f'<rect width="{W}" height="400" fill="{GRAY}"/><rect y="400" width="{W}" height="{H2-400}" fill="{PAPER}"/>'
    body += f'<text x="80" y="80" font-family="{MONO}" font-size="24" fill="{MAROON}">A. GRAY pages: pink marker behind the text</text>'
    body += marker_line(80, 210, [("kerja dari ", 0), ("kafe", 1)])
    body += marker_line(80, 320, [("bukan kabur", 0)])
    body += f'<text x="80" y="480" font-family="{MONO}" font-size="24" fill="{MAROON}">B. WHITE pages: same pink marker</text>'
    body += marker_line(80, 610, [("tiap ", 0), ("Kamis", 1)])
    body += f'<text x="80" y="760" font-family="{MONO}" font-size="24" fill="{MAROON}">C. selected text: max once per carousel</text>'
    body += f'<text x="80" y="910" font-family="{SERIF}" font-size="96" fill="{MAROON}">jadi</text>'
    body += selected_line(80 + REG.getlength("jadi ") + 22, 910, [("produktif", 0), ("-ish", 1)])
    body += f'<text x="80" y="1060" font-family="{MONO}" font-size="22" fill="{MAROON}">pink-soft block + Blood Red handles, one short phrase</text>'
    return svg(W, H2, body)


save("highlights/svg/highlight-styles.svg", highlight_demo(), 1)
print("done")
