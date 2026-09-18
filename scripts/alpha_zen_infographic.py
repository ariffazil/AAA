#!/usr/bin/env python3
"""alpha_zen_infographic — the yin-yang daily card for the ALPHA-ZEN group.

WHY THIS SHAPE
  The card holds TWO people. A yin-yang is the right form because it makes a
  claim that a bar chart cannot: the two halves are EQUAL WEIGHT and neither is
  the baseline the other is measured against.

  This matters, and it is the whole design problem: measured by message volume,
  Arif posts ~761 and Syed ~209 in that group. A chart drawn to scale would
  render Syed at 27% of Arif and would thereby state something false about the
  relationship — that one of them matters less. VOLUME IS NOT WEIGHT. The
  yin-yang deliberately cannot encode volume, which is exactly why it is honest
  here.

WHAT IS REAL AND WHAT IS NOT
  Real, live, every render:
    - CHRON counters, computed from dated facts (chron.py)
    - moon phase, day-of-year, week number (pure arithmetic, offline)
    - the date
  Fixed, because they are documented facts about two people:
    - Arif: executive geoscientist, PETRONAS Carigali, UPSTREAM. Deep time.
    - Syed: fitness and strength coach. Immediate time.
  Deliberately NOT rendered:
    - anything about Syed's body, health, training, family or inner state.
      He is a recipient of this card, never its subject.
    - any inference about the bond between them. The machine witnesses; it does
      not model what it cannot know. The unresolved part of the relationship is
      represented by structure (the dot each half carries), never by content.

THE DOT
  Each half carries a dot of the other's field. That is the actual meaning of the
  symbol and it is also the honest move: what each one needs sits outside his own
  domain. The card asserts the shape of that, and stops.

LIGHT BACKGROUND by standing instruction (F13, 2026-09-18): "I hate black dark
background in pdf." The yin-yang disc is dark, the page is not.
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

OUT = Path("/root/AAA/forge_work/alpha-zen")
CHRON = Path("/root/AAA/scripts/chron.py")

# ── palette (contrast-checked on the paper ground) ───────────────────────────
PAPER = "#faf8f4"
INK = "#1c1c1c"
MUTED = "#6b6b6b"
RULE = "#dedad2"
YIN = "#16293d"        # deep navy — Arif's half
YANG = "#e7dcc6"       # warm sand — Syed's half
YANG_INK = "#3a2f18"   # text on the sand half
ACCENT = "#8a5a10"     # bronze, >7:1 on paper


def moon_phase(d: date) -> tuple[float, str]:
    """Fraction through the synodic cycle + the phase name. Pure arithmetic.

    The name is prefixed with a moon glyph at render time. Without it, "suku
    pertama" sits next to a date and reads as a CALENDAR quarter — a silent
    misread that makes the card look wrong on any month that is not Q1.
    """
    known_new = date(2000, 1, 6)
    frac = ((d - known_new).days % 29.530588853) / 29.530588853
    names = [(0.03, "anak bulan"), (0.22, "bulan sabit muda"), (0.28, "suku pertama"),
             (0.47, "hampir purnama"), (0.53, "purnama"), (0.72, "hampir gerhana"),
             (0.78, "suku akhir"), (0.97, "bulan tua"), (1.01, "anak bulan")]
    for lim, nm in names:
        if frac < lim:
            return frac, nm
    return frac, "anak bulan"


def moon_glyph(frac: float) -> str:
    """A crescent indicator so the phase can never be read as a calendar quarter."""
    if frac < 0.03 or frac >= 0.97:
        return "●"          # new
    if frac < 0.22:
        return "☽"          # waxing crescent
    if frac < 0.28:
        return "◐"          # first quarter
    if frac < 0.47:
        return "◑"
    if frac < 0.53:
        return "○"          # full
    if frac < 0.72:
        return "◑"
    if frac < 0.78:
        return "◑"
    if frac < 0.97:
        return "☾"          # waning crescent
    return "●"


def chron_lines() -> list[str]:
    """Call the CHRON script so the two share one source of truth."""
    try:
        r = subprocess.run([sys.executable, str(CHRON)], capture_output=True,
                           text=True, timeout=30)
        return [l for l in r.stdout.strip().splitlines() if l.strip()]
    except Exception:
        return []


def yinyang_svg(size: int = 460, variant: str = "a") -> str:
    """The taijitu. Two halves, each carrying a dot of the OPPOSITE field.

    The dot colour must invert relative to the half it sits in, or it vanishes:
    a dark dot on the dark head is invisible, and the symbol then reads as two
    plain blobs. Each dot is the OTHER half's colour, which is also the meaning —
    what each one needs sits outside his own domain.
    """
    c = size / 2
    r = size / 2 - 6
    half = r / 2
    dot = r / 7
    # which end the dark half's head bulges to
    dark_head_at_bottom = (variant == "a")

    if dark_head_at_bottom:
        dark = (f"M {c},{c-r} A {r},{r} 0 0 0 {c},{c+r} "
                f"A {half},{half} 0 0 0 {c},{c} "
                f"A {half},{half} 0 0 1 {c},{c-r} Z")
    else:
        dark = (f"M {c},{c-r} A {r},{r} 0 0 0 {c},{c+r} "
                f"A {half},{half} 0 0 1 {c},{c} "
                f"A {half},{half} 0 0 0 {c},{c-r} Z")

    # dot inside the DARK head takes the light colour; dot inside the LIGHT head
    # takes the dark colour. Tie it to the variant so it can never be wrong.
    dot_in_dark = YANG
    dot_in_light = YIN
    lower_dot = dot_in_dark if dark_head_at_bottom else dot_in_light
    upper_dot = dot_in_light if dark_head_at_bottom else dot_in_dark

    return f"""
<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}"
     xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="Yin-yang: two halves of equal weight">
  <defs>
    <clipPath id="disc"><circle cx="{c}" cy="{c}" r="{r}"/></clipPath>
  </defs>
  <circle cx="{c}" cy="{c}" r="{r}" fill="{YANG}"/>
  <g clip-path="url(#disc)">
    <path d="{dark}" fill="{YIN}"/>
  </g>
  <circle cx="{c}" cy="{c+half}" r="{dot}" fill="{lower_dot}"/>
  <circle cx="{c}" cy="{c-half}" r="{dot}" fill="{upper_dot}"/>
  <circle cx="{c}" cy="{c}" r="{r}" fill="none" stroke="{YIN}" stroke-width="2"/>
</svg>"""


def build_html(mode: str) -> str:
    today = date.today()
    frac, phase_name = moon_phase(today)
    glyph = moon_glyph(frac)
    chron = chron_lines()
    chron_html = "".join(f"<div class='chronrow'>{l}</div>" for l in chron[:3])

    if mode == "morning":
        kicker = "SEBELUM HARI MULA"
        title = "APA YANG HARI NI MINTA"
        sub = "Dua orang, dua jam yang berbeza. Tak ada siapa baseline siapa."
        pairs = [
            ("Baca batu", "Baca badan"),
            ("Masa: juta tahun", "Masa: satu rep"),
            ("Ambil dari bumi", "Bentuk dari badan"),
            ("Kepala — abstrak", "Badan — konkrit"),
        ]
        tail_label = "HARI NI"
        tail = "Satu benda yang tak perlu diselesaikan hari ni, dan satu yang perlu."
    else:
        kicker = "SEBELUM TIDUR"
        title = "APA YANG HARI NI TINGGAL"
        sub = "Dua orang, dua jam yang berbeza. Tak ada siapa baseline siapa."
        pairs = [
            ("Apa yang naik", "Apa yang tahan"),
            ("Apa yang difikir", "Apa yang dibuat"),
            ("Apa yang jauh", "Apa yang dekat"),
            ("Apa yang tinggal", "Apa yang lepas"),
        ]
        tail_label = "SEBELUM TUTUP MATA"
        tail = "Satu benda yang benar hari ni. Satu benda yang boleh ditinggal."

    rows = "".join(
        f"<div class='row'><div class='cell yin'>{a}</div>"
        f"<div class='cell yang'>{b}</div></div>"
        for a, b in pairs)

    return f"""<!DOCTYPE html>
<html lang="ms"><head><meta charset="utf-8"><style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ width:1080px; background:{PAPER}; font-family:"Lato","DejaVu Sans",sans-serif;
          color:{INK}; -webkit-font-smoothing:antialiased; }}
  .wrap {{ width:1080px; padding:54px 64px 48px; }}
  .top {{ display:flex; justify-content:space-between; align-items:baseline;
          border-bottom:2px solid {INK}; padding-bottom:14px; }}
  .kicker {{ font-size:19px; letter-spacing:.32em; font-weight:700; color:{ACCENT}; }}
  .date {{ font-size:19px; color:{MUTED}; font-weight:600; }}
  h1 {{ font-size:62px; line-height:1.04; font-weight:800; margin:30px 0 12px; letter-spacing:-.5px; }}
  .sub {{ font-size:23px; color:{MUTED}; line-height:1.4; max-width:820px; margin-bottom:34px; }}
  .discwrap {{ display:flex; justify-content:center; margin:6px 0 30px; }}
  .names {{ display:flex; justify-content:space-between; width:760px; margin:0 auto 14px; }}
  .nm {{ font-size:22px; font-weight:800; letter-spacing:.14em; }}
  .nm.yin {{ color:{YIN}; }} .nm.yang {{ color:{ACCENT}; }}
  .rows {{ margin:8px 0 30px; border-top:1px solid {RULE}; }}
  .row {{ display:flex; border-bottom:1px solid {RULE}; }}
  .cell {{ flex:1; padding:16px 20px; font-size:24px; font-weight:600; }}
  .cell.yin {{ text-align:right; border-right:1px solid {RULE}; color:{YIN}; }}
  .cell.yang {{ text-align:left; color:{ACCENT}; }}
  .chron {{ background:#fff; border:1px solid {RULE}; border-left:5px solid {ACCENT};
            padding:22px 26px; margin-bottom:28px; }}
  .chronh {{ font-size:17px; letter-spacing:.24em; font-weight:800; color:{ACCENT}; margin-bottom:10px; }}
  .chronrow {{ font-size:22px; color:{INK}; line-height:1.6; font-weight:600; }}
  .tail {{ border-top:2px solid {INK}; padding-top:18px; }}
  .taill {{ font-size:16px; letter-spacing:.24em; font-weight:800; color:{MUTED}; margin-bottom:8px; }}
  .tailt {{ font-size:25px; line-height:1.42; font-weight:600; }}
  .foot {{ display:flex; justify-content:space-between; margin-top:30px; padding-top:14px;
           border-top:1px solid {RULE}; font-size:17px; color:{MUTED}; }}
</style></head><body><div class="wrap">

  <div class="top">
    <div class="kicker">{kicker}</div>
    <div class="date">{glyph} fasa bulan: {phase_name} · {today.strftime('%d.%m.%Y')}</div>
  </div>

  <h1>{title}</h1>
  <div class="sub">{sub}</div>

  <div class="names">
    <div class="nm yin">ARIF</div>
    <div class="nm yang">SYED</div>
  </div>
  <div class="discwrap">{yinyang_svg()}</div>

  <div class="rows">{rows}</div>

  <div class="chron">
    <div class="chronh">CHRON — JAM YANG SEDANG JALAN</div>
    {chron_html}
  </div>

  <div class="tail">
    <div class="taill">{tail_label}</div>
    <div class="tailt">{tail}</div>
  </div>

  <div class="foot">
    <span>ALPHA-ZEN · {mode.upper()}</span>
    <span>DITEMPA BUKAN DIBERI</span>
  </div>

</div></body></html>"""


def _autocrop_tail(png: Path, pad: int = 0) -> tuple[int, int]:
    """Trim trailing whitespace from the bottom of a full-height render.

    Chrome's --screenshot captures exactly the window height, so a short card
    leaves dead space and a long one gets clipped. Rendering tall and cropping
    the tail is the only approach that is correct for BOTH, and it removes the
    need to hand-tune a window height per mode.
    """
    from PIL import Image
    im = Image.open(png).convert("RGB")
    w, h = im.size
    odd = im.getpixel((2, 2))
    bg: tuple[int, int, int] = odd if isinstance(odd, tuple) else (int(odd), int(odd), int(odd))
    last = 0
    for y in range(h - 1, 0, -4):
        row_diff = False
        for x in range(0, w, 8):
            p = im.getpixel((x, y))
            pp: tuple[int, int, int] = p if isinstance(p, tuple) else (int(p), int(p), int(p))
            if sum(abs(int(a) - int(b)) for a, b in zip(pp, bg)) > 24:
                row_diff = True
                break
        if row_diff:
            last = y
            break
    new_h = min(h, max(200, last + 1 + pad))
    if new_h < h:
        im.crop((0, 0, w, new_h)).save(png)
    return w, new_h


def render(mode: str, outdir: Path) -> Path:
    outdir.mkdir(parents=True, exist_ok=True)
    html = outdir / f"{mode}.html"
    png = outdir / f"ALPHA-ZEN-{mode.upper()}.png"
    html.write_text(build_html(mode), encoding="utf-8")
    # deliberately taller than any realistic card; the tail is cropped after
    cmd = ["google-chrome", "--headless", "--disable-gpu", "--no-sandbox",
           "--hide-scrollbars", "--default-background-color=FFFFFFFF",
           "--window-size=1080,2600", f"--screenshot={png}", f"file://{html}"]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if not png.exists():
        raise RuntimeError(f"render failed: {r.stderr[:400]}")
    w, h = _autocrop_tail(png)
    print(f"  {png.name}: {w}x{h} (tail cropped)")
    return png


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["morning", "night", "both", "html"])
    ap.add_argument("--variant", default="a", choices=["a", "b"])
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()
    od = Path(a.out)
    if a.mode == "html":
        p = od / "shape-test.html"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(
            f"<body style='background:{PAPER};margin:0;display:flex'>"
            f"<div style='padding:20px'><div style='font:14px Lato;color:{INK}'>variant a</div>"
            f"{yinyang_svg(400, 'a')}</div>"
            f"<div style='padding:20px'><div style='font:14px Lato;color:{INK}'>variant b</div>"
            f"{yinyang_svg(400, 'b')}</div></body>", encoding="utf-8")
        print(p)
        sys.exit(0)
    modes = ["morning", "night"] if a.mode == "both" else [a.mode]
    for m in modes:
        print(render(m, od))
