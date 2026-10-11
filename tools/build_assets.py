"""Generate WFCditasik brand kit SVGs + PNG exports.
Palette: Blood Red #660005, Ruddy Pink #DF8F9C, Light Goldenrod Yellow #FAF4D4."""
import os, sys, cairosvg

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
MAROON = "#660005"
MAROON_DK = "#3F0003"
PINK = "#DF8F9C"
PINK_SOFT = "#F2C9CF"
ROSE = "#A3404F"
CREAM = "#FAF4D4"
PAPER = "#FFFBEA"
INK = "#2B0A0C"
GRID = "#EADFB4"

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


def grid_paper():
    step = 36
    lines = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}"/>' for x in range(0, W + 1, step))
    lines += "".join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>' for y in range(0, H + 1, step))
    return svg(W, H, f'<rect width="{W}" height="{H}" fill="{PAPER}"/>'
                     f'<g stroke="{GRID}" stroke-width="1.5">{lines}</g>')


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


save("backgrounds/svg/grid-paper-cream.svg", grid_paper())
save("backgrounds/svg/checker-pink-cream.svg", checker(CREAM, PINK))
save("backgrounds/svg/checker-red-cream.svg", checker(CREAM, MAROON))
save("backgrounds/svg/stripes-pink.svg", stripes(CREAM, PINK))
save("backgrounds/svg/stripes-red.svg", stripes(CREAM, MAROON, 26))
save("backgrounds/svg/solid-red.svg", solid(MAROON))
save("backgrounds/svg/solid-cream.svg", solid(CREAM))
save("backgrounds/svg/dashed-card-on-pink.svg",
     dashed_frame(PINK_SOFT, PAPER, MAROON))
save("backgrounds/svg/dashed-card-on-red.svg", dashed_frame(MAROON, CREAM, PINK))

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
art = (f'<rect width="{bar_w}" height="{bar_h}" rx="14" fill="#EFE9DF"/>'
       f'<line x1="118" y1="14" x2="118" y2="50" stroke="#CFC6B6" stroke-width="2"/>'
       f'<line x1="282" y1="14" x2="282" y2="50" stroke="#CFC6B6" stroke-width="2"/>'
       f'<g font-family="{SANS}" font-size="24" fill="{INK}" text-anchor="middle">'
       f'<text x="59" y="41">Copy</text><text x="200" y="41">Select All</text>'
       f'<text x="351" y="41">Share…</text></g>'
       f'<path d="M190 {bar_h} l12 14 l12 -14z" fill="#EFE9DF"/>')
save("ui-stickers/svg/copy-select-bar.svg", sticker(bar_w, bar_h + 14, {"outline": outline, "art": art}))

# 3. Notification pill
pw, ph = 560, 120
outline = f'<rect width="{pw}" height="{ph}" rx="28"/>'
art = (f'<rect width="{pw}" height="{ph}" rx="28" fill="{PAPER}"/>'
       f'<rect x="20" y="22" width="76" height="76" rx="18" fill="{MAROON}"/>'
       f'<text x="58" y="74" font-family="{SERIF}" font-size="40" fill="{CREAM}" text-anchor="middle">wfc</text>'
       f'<text x="116" y="48" font-family="{SANS}" font-size="20" font-weight="bold" fill="{INK}">WFC di Tasik</text>'
       f'<text x="{pw-24}" y="48" font-family="{SANS}" font-size="18" fill="#9A8F80" text-anchor="end">now</text>'
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
       f'<text x="24" y="40" font-family="{SANS}" font-size="20" fill="{CREAM}">Tasikmalaya</text>'
       f'<text x="20" y="118" font-family="{SANS}" font-size="74" fill="{CREAM}">27°</text>'
       f'<text x="{ww-24}" y="40" font-family="{SANS}" font-size="20" fill="{CREAM}" text-anchor="end">Hujan sore</text>'
       f'<text x="{ww-24}" y="68" font-family="{SANS}" font-size="18" fill="{PINK_SOFT}" text-anchor="end">cocok buat WFC</text>'
       + "".join(f'<circle cx="{40+i*56}" cy="160" r="9" fill="{PINK_SOFT if i<3 else CREAM}"/>' for i in range(6)))
save("ui-stickers/svg/widget-weather-tasik.svg", sticker(ww, wh, {"outline": outline, "art": art}))

# 6. Reminders / to-do card
rw, rh = 220, 220
outline = f'<rect width="{rw}" height="{rh}" rx="48"/>'
dots = [MAROON, ROSE, PINK]
art = f'<rect width="{rw}" height="{rh}" rx="48" fill="{PAPER}"/>' + "".join(
    f'<circle cx="54" cy="{58+i*52}" r="14" fill="none" stroke="{c}" stroke-width="5"/>'
    f'<circle cx="54" cy="{58+i*52}" r="7" fill="{c}"/>'
    f'<rect x="84" y="{54+i*52}" width="96" height="8" rx="4" fill="#DDD4C4"/>' for i, c in enumerate(dots))
save("ui-stickers/svg/reminders-card.svg", sticker(rw, rh, {"outline": outline, "art": art}))

# 7. Wi-Fi + battery status pill
sw, sh = 320, 76
outline = f'<rect width="{sw}" height="{sh}" rx="38"/>'
wifi = (f'<g transform="translate(36,20)" fill="none" stroke="{CREAM}" stroke-width="5" stroke-linecap="round">'
        f'<path d="M0 14 Q22 -6 44 14"/><path d="M8 24 Q22 12 36 24"/></g>'
        f'<circle cx="58" cy="54" r="5" fill="{CREAM}"/>')
art = (f'<rect width="{sw}" height="{sh}" rx="38" fill="{MAROON}"/>' + wifi +
       f'<text x="104" y="48" font-family="{SANS}" font-size="22" fill="{CREAM}">wifi kencang</text>'
       f'<rect x="246" y="26" width="44" height="24" rx="6" fill="none" stroke="{CREAM}" stroke-width="3"/>'
       f'<rect x="250" y="30" width="30" height="16" rx="3" fill="{PINK}"/>'
       f'<rect x="292" y="33" width="4" height="10" rx="2" fill="{CREAM}"/>')
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
       f'<rect x="20" y="20" width="{qw-40}" height="{qw-40}" fill="#D9D2C5"/>'
       f'<text x="{qw/2}" y="{qh-24}" font-family="{HAND}" font-size="34" fill="{MAROON}" text-anchor="middle">tempel foto di sini</text>')
save("ui-stickers/svg/polaroid-frame.svg", sticker(qw, qh, {"outline": outline, "art": art}))

# 10. Washi tape strips
def tape(color, name):
    tw, th = 220, 56
    edge = "".join(f"L{tw - (6 if i % 2 else 0)} {i*7}" for i in range(1, 9))
    d = f"M0 0 L{tw} 0 {edge} L0 {th} " + "".join(f"L{6 if i % 2 else 0} {th - i*7}" for i in range(1, 9)) + "Z"
    save(f"paper/svg/tape-{name}.svg", svg(tw, th, f'<path d="{d}" fill="{color}" opacity="0.82"/>'))


tape(PINK, "pink")
tape(MAROON, "red")
tape("#E8DCC6", "kraft")

# 11. Note paper scrap (lined) and torn-edge strip
nw, nh = 460, 300
lines = "".join(f'<line x1="24" y1="{70+i*40}" x2="{nw-24}" y2="{70+i*40}" stroke="#E4D9C8" stroke-width="2"/>' for i in range(6))
save("paper/svg/note-lined.svg", svg(nw + 20, nh + 20,
     f'<g filter="url(#sh)"><rect x="10" y="6" width="{nw}" height="{nh}" fill="{PAPER}"/>{lines}'
     f'<line x1="70" y1="6" x2="70" y2="{nh+6}" stroke="{MAROON}" stroke-opacity="0.35" stroke-width="2"/></g>', SHADOW))

import random
random.seed(7)
tw = 900
pts = " ".join(f"L{x} {random.randint(0, 14)}" for x in range(0, tw + 1, 18))
save("paper/svg/torn-strip-cream.svg", svg(tw, 180,
     f'<g filter="url(#sh)"><path d="M0 8 {pts} L{tw} 140 L0 140Z" fill="{CREAM}"/></g>', SHADOW))

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


def marker_line(x, base, parts, size=96, pad=8):
    """Marker band: from ~x-height middle to just under baseline. Never reaches other lines."""
    w = tw(parts)
    top, h = base - size * 0.30, size * 0.36
    return (f'<rect x="{x-pad}" y="{top:.1f}" width="{w+pad*2:.1f}" height="{h:.1f}" rx="3" fill="{PINK}"/>'
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
    body = f'<rect width="{W}" height="760" fill="{PAPER}"/>'
    body += f'<text x="80" y="90" font-family="{MONO}" font-size="26" fill="{ROSE}">A. marker: lower band only, one band per line</text>'
    body += marker_line(80, 220, [("kerja dari ", 0), ("kafe", 1)])
    body += marker_line(80, 330, [("bukan kabur", 0)])
    body += f'<text x="80" y="470" font-family="{MONO}" font-size="26" fill="{ROSE}">B. selected text: signature, one phrase per slide</text>'
    body += f'<text x="80" y="620" font-family="{SERIF}" font-size="96" fill="{MAROON}">jadi</text>'
    body += selected_line(80 + REG.getlength("jadi ") + 22, 620, [("produktif", 0), ("-ish", 1)])
    return svg(W, 760, body)


save("highlights/svg/highlight-styles.svg", highlight_demo(), 1)
print("done")
