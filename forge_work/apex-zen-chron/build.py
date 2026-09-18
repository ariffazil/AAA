#!/usr/bin/env python3
"""APEX-ZEN CHRON — build the two balanced Yin-Yang infographics (morning, night).

WHY HTML+CHROME AND NOT IMAGE GENERATION
  An infographic carries EXACT text: names, dates, places, rules, a question in
  Penang Malay. Diffusion models render text as approximate glyph shapes, so
  "Say Less" comes back as "Say Lcss" and a place name becomes unrecognisable.
  HTML laid out by Chrome gives exact typography, exact line breaks, and a
  deterministic byte-for-byte rebuild. Chrome renders a real PNG; nothing is
  hallucinated.

WHY A FIXED PAGE BOX
  1080x1520, fixed. A variable-height screenshot depends on Chrome's viewport
  and silently clips long content — the failure looks like a missing footer, not
  like an error. A fixed box plus a bottom-margin check (the last rows must be
  empty background) proves nothing was cut off.

THE BALANCE RULE — the load-bearing design decision
  "Balance about him and me" is honoured as EQUAL STRUCTURE, not equal
  surveillance. Each man gets three rows of the same shape:

      TAHU      one thing the machine legitimately knows for him
      TAK TAHU  a slot only he can fill

  Why not fill both sides with facts: the machine has no licence to know Syed's
  inner state. The relationship kernel forbids manufacturing shared meaning, and
  inventing symmetric emotional content to make a graphic look balanced would be
  exactly that. So the balance is of dignity and visual weight; where knowledge
  is absent the row says so instead of inventing.

  Alpha/Zen colour assignment (Syed = red/yang, Arif = blue/yin) is a DESIGN
  CHOICE about their public lanes, not a claim about either man. It is one
  constant to flip.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

RUN = Path("/root/AAA/forge_work/apex-zen-chron")
RUN.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1520
ALPHA = "#c0392b"   # red  — Syed's side (action / body / heat)
ZEN = "#1f4e79"     # blue — Arif's side (depth / witness / cool)
INK = "#1d2733"
MUTED = "#5f6b78"
RULE = "#dde3ea"
PANEL = "#f7f9fb"


def yin_yang(size: int = 320, rotate: float = 0.0) -> str:
    """Clean taijitu drawn from unambiguous primitives.

    Built as full circle + half-disc + two full circles, NOT from the classic
    two-arc S-path. The arc version is easy to get subtly wrong (sweep flags
    decide which way each lobe bulges) and a wrong sweep produces a pinwheel
    that still "looks like a yin-yang" at a glance. Full circles cannot be
    mis-swept.

      white disc
      + dark right half
      + dark circle low      -> the dark lobe pushed into the light side
      - light circle high    -> the light lobe pushed into the dark side
      + two dots             -> each side carries the seed of the other
      + outline last         -> so the carves cannot clip the rim
    """
    s = size / 200.0
    return f'''<svg width="{size}" height="{size}" viewBox="0 0 200 200"
     style="transform:rotate({rotate}deg)">
  <defs>
    <clipPath id="yy"><circle cx="100" cy="100" r="96"/></clipPath>
  </defs>
  <circle cx="100" cy="100" r="96" fill="{ALPHA}"/>
  <path d="M100,4 A96,96 0 0 1 100,196 Z" fill="{ZEN}"/>
  <circle cx="100" cy="148" r="48" fill="{ZEN}"/>
  <circle cx="100" cy="52"  r="48" fill="{ALPHA}"/>
  <circle cx="100" cy="52"  r="13" fill="{ZEN}"/>
  <circle cx="100" cy="148" r="13" fill="{ALPHA}"/>
  <circle cx="100" cy="100" r="96" fill="none" stroke="{INK}" stroke-width="2.5"/>
</svg>'''


TEMPLATE = r'''<!DOCTYPE html>
<html lang="ms"><head><meta charset="utf-8"><title>APEX-ZEN $PHASE</title>
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  html,body { width:1080px; height:1520px; }
  body { font-family:"DejaVu Sans","Liberation Sans",sans-serif; color:$INK;
         background:#ffffff; padding:0 44px; }
  .bar { display:flex; justify-content:space-between; align-items:baseline;
         padding:26px 0 14px 0; border-bottom:2px solid $INK; }
  .bar .l { font-size:15px; font-weight:700; letter-spacing:3px; }
  .bar .r { font-size:13px; color:$MUTED; letter-spacing:1px; }
  .bar .l b.a { color:$ALPHA; } .bar .l b.z { color:$ZEN; }
  .hero { text-align:center; padding:22px 0 4px 0; }
  /* Equal-width label boxes. Vision reported the emblem as off-centre; a
     measurement showed it at -0.5px from the page centre. The real asymmetry
     was here: "ALPHA" is five glyphs and "ZEN" is three, so a centre-aligned
     pair looks lopsided even though it is geometrically centred. Fixing the
     label boxes is the honest remedy for the perceived imbalance. */
  .hero .poles { display:flex; justify-content:center; gap:96px;
                 font-size:12px; letter-spacing:4px; font-weight:700;
                 margin-bottom:6px; }
  .hero .poles span { display:inline-block; width:150px; text-align:center; }
  .hero .poles .p1 { color:$ALPHA; } .hero .poles .p2 { color:$ZEN; }
  .hero .cap { font-size:12.5px; color:$MUTED; margin-top:9px; letter-spacing:.4px; }
  .chron { display:flex; gap:14px; margin-top:18px; }
  .chron .c { flex:1; border:1px solid $RULE; background:#ffffff;
              padding:10px 12px 11px 12px; border-left:4px solid $MUTED; }
  .chron .c.a { border-left-color:$ALPHA; } .chron .c.z { border-left-color:$ZEN; }
  .chron .c .who { font-size:9px; font-weight:700; letter-spacing:1.6px;
                   color:$MUTED; margin-bottom:4px; }
  .chron .c .big { font-size:26px; font-weight:700; line-height:1.02; }
  .chron .c.a .big { color:$ALPHA; } .chron .c.z .big { color:$ZEN; }
  .chron .c .unit { font-size:11px; font-weight:400; color:$MUTED; }
  .chron .c .lbl { font-size:10.5px; color:$MUTED; line-height:1.35; margin-top:4px; }
  .duo { display:flex; gap:20px; margin-top:20px; }
  .card { flex:1; background:$PANEL; border:1px solid $RULE;
          border-top:4px solid $ACC; padding:16px 17px 15px 17px; }
  .card h3 { font-size:14px; letter-spacing:2.5px; color:$ACC; margin-bottom:3px; }
  .card .sub { font-size:10.5px; color:$MUTED; margin-bottom:11px; letter-spacing:.3px; }
  .row { padding:7px 0 8px 0; border-top:1px dashed $RULE; }
  .row:first-of-type { border-top:none; }
  .row .k { font-size:9.5px; font-weight:700; letter-spacing:1.6px;
            color:$MUTED; margin-bottom:3px; }
  .row .v { font-size:12.5px; line-height:1.42; }
  .row.open .v { color:$MUTED; font-style:italic; }
  .block { margin-top:22px; }
  .block h2 { font-size:13px; letter-spacing:3px; color:$INK;
              border-bottom:1px solid $RULE; padding-bottom:7px; margin-bottom:12px; }
  .item { display:flex; gap:11px; padding:8px 0; border-bottom:1px solid #eef2f6; }
  .item .tag { flex:0 0 46px; font-size:9px; font-weight:700; letter-spacing:.8px;
               color:#ffffff; background:$MUTED; text-align:center;
               padding:3px 0; height:18px; }
  .item .tag.obs { background:$ZEN; } .item .tag.der { background:#6b7a89; }
  .item .tag.int { background:$ALPHA; }
  .item .txt { font-size:12.5px; line-height:1.45; }
  .item .txt b { color:$ZEN; }
  .q { margin-top:24px; border:2px solid $INK; padding:22px 26px; text-align:center; }
  .q .lab { font-size:10px; letter-spacing:3.5px; color:$MUTED; margin-bottom:9px; }
  .q .txt { font-size:24px; line-height:1.35; font-weight:700; }
  .foot { margin-top:20px; padding-top:11px; border-top:1px solid $RULE;
          display:flex; justify-content:space-between; font-size:9.5px;
          color:$MUTED; letter-spacing:.3px; }
</style></head><body>

<div class="bar">
  <div class="l">APEX<b class="a">&middot;</b>ZEN <span style="color:$MUTED;font-weight:400">&nbsp;CHRON</span></div>
  <div class="r">$PHASELABEL &nbsp;&middot;&nbsp; $DATE &nbsp;&middot;&nbsp; $DAY</div>
</div>

<div class="hero">
  <div class="poles"><span class="p1">ALPHA</span><span class="p2">ZEN</span></div>
  $YINYANG
  <div class="cap">$CAPTION</div>
</div>

<div class="chron">
  $CHRON
</div>

<div class="duo">
  $CARDS
</div>

$BLOCKS

<div class="q">
  <div class="lab">SATU SOALAN</div>
  <div class="txt">$QUESTION</div>
</div>

<div class="foot">
  <span>$FOOTL</span>
  <span>$FOOTR</span>
</div>

</body></html>'''


def card(rec: dict) -> str:
    rows = []
    for r in rec["rows"]:
        cls = "row open" if r.get("open") else "row"
        rows.append(f'<div class="{cls}"><div class="k">{r["k"]}</div>'
                    f'<div class="v">{r["v"]}</div></div>')
    return (f'<div class="card" style="--x:0; border-top-color:{rec["accent"]}">'
            f'<h3 style="color:{rec["accent"]}">{rec["title"]}</h3>'
            f'<div class="sub">{rec["sub"]}</div>' + "".join(rows) + "</div>")


def block(title: str, items: list[dict]) -> str:
    out = [f'<div class="block"><h2>{title}</h2>']
    for it in items:
        tag = it.get("tag", "OBS").lower()
        out.append(f'<div class="item"><div class="tag {tag}">{tag.upper()}</div>'
                   f'<div class="txt">{it["text"]}</div></div>')
    out.append("</div>")
    return "".join(out)


def chron_cell(who: str, big: str, unit: str, label: str, side: str) -> str:
    return (f'<div class="c {side}"><div class="who">{who}</div>'
            f'<div class="big">{big} <span class="unit">{unit}</span></div>'
            f'<div class="lbl">{label}</div></div>')


def build_chron(today: str) -> str:
    """Countdown cells — the CHRON part. Computed from the date, never typed.

    Every number here is DERIVED from `today` and a stated anchor, so it cannot
    silently go stale the way a hardcoded "163 hari" does the moment the poster
    is rebuilt tomorrow. Where an anchor is approximate, the cell says so
    instead of printing a spuriously precise figure.
    """
    from datetime import date
    y, m, d = (int(x) for x in today.split("-"))
    t = date(y, m, d)

    od1 = date(2027, 3, 1)          # earliest possible OD1 window
    budget = date(2026, 10, 9)      # MOF pre-budget statement
    days_od1 = (od1 - t).days
    days_budget = (budget - t).days

    return (
        chron_cell("ARIF &middot; OD1", f"&asymp;{days_od1}", "hari",
                   "anggaran ke tingkap Mac 2027. Tarikh tepat belum dikunci &mdash; "
                   "ini hujung paling awal, bukan janji.", "z")
        + chron_cell("BERSAMA &middot; BAJET", f"{days_budget}", "hari",
                     "Belanjawan 2027, 9 Oktober. Angka petroleum jadi boleh semak "
                     "pada tarikh itu.", "a")
        + chron_cell("SYED &middot; CIRCUIT", f"0&ndash;4", "comps",
                     "julat setahun seorang atlet. Tarikh sebenar hanya Syed tahu.", "a")
    )


def build(spec: dict) -> Path:
    cards = "".join(card(c) for c in spec["cards"])
    blocks = "".join(block(b["title"], b["items"]) for b in spec["blocks"])
    html = (TEMPLATE
            .replace("$ALPHA", ALPHA).replace("$ZEN", ZEN)
            .replace("$INK", INK).replace("$MUTED", MUTED)
            .replace("$RULE", RULE).replace("$PANEL", PANEL)
            .replace("$ACC", spec.get("accent", ZEN))
            .replace("$YINYANG", yin_yang(300, spec.get("rotate", 0)))
            .replace("$CAPTION", spec["caption"])
            .replace("$CARDS", cards).replace("$BLOCKS", blocks)
            .replace("$CHRON", build_chron(spec.get("today", "2026-09-18")))
            .replace("$QUESTION", spec["question"])
            .replace("$FOOTL", spec["foot_left"]).replace("$FOOTR", spec["foot_right"])
            # LONGEST TOKEN FIRST. "$PHASE" is a prefix of "$PHASELABEL", so
            # replacing the short one first turns "$PHASELABEL" into "pagiLABEL"
            # and leaves visible junk on the poster. Caught by the leftover-token
            # check, not by looking at it.
            .replace("$PHASELABEL", spec["phase_label"])
            .replace("$PHASE", spec["phase"])
            .replace("$DATE", spec["date"]).replace("$DAY", spec["day"]))
    src = RUN / f"{spec['phase']}.html"
    src.write_text(html)
    png = RUN / f"APEX-ZEN-{spec['phase'].upper()}-{spec['date']}.png"
    r = subprocess.run([
        "google-chrome", "--headless=new", "--disable-gpu", "--no-sandbox",
        "--hide-scrollbars", "--default-background-color=FFFFFFFF",
        f"--window-size={W},{H}", f"--screenshot={png}", f"file://{src}",
    ], capture_output=True, text=True, timeout=180)
    if not png.exists():
        raise RuntimeError("chrome produced no file: " + (r.stderr or "")[:400])
    return png


# ── verification ─────────────────────────────────────────────────────────────

def yy_selftest() -> dict:
    """Test the yin-yang ON ITS OWN, at a known size, on a known background.

    Measuring it inside the poster does not work: the header logo and the card
    accents use the same two colours, so a whole-page colour count is dominated
    by the chrome, not the emblem. A 320x320 render with nothing else on it
    isolates the thing being tested. Unit test the graphic, integration-test the
    page.
    """
    import numpy as np
    from PIL import Image
    size = 320
    src = RUN / "_yy_selftest.html"
    src.write_text(f"<!DOCTYPE html><html><body style='margin:0;background:#fff'>"
                   f"{yin_yang(size, 0)}</body></html>")
    out = RUN / "_yy_selftest.png"
    subprocess.run(["google-chrome", "--headless=new", "--disable-gpu",
                    "--no-sandbox", "--hide-scrollbars",
                    "--default-background-color=FFFFFFFF",
                    f"--window-size={size},{size}", f"--screenshot={out}",
                    f"file://{src}"], capture_output=True, text=True, timeout=120)
    a = np.asarray(Image.open(out).convert("RGB"))
    scale = size / 200.0          # viewBox 200 -> rendered size

    def mask(hexs, tol=34):
        r, g, b = int(hexs[1:3], 16), int(hexs[3:5], 16), int(hexs[5:7], 16)
        return ((np.abs(a[:, :, 0].astype(int) - r) < tol)
                & (np.abs(a[:, :, 1].astype(int) - g) < tol)
                & (np.abs(a[:, :, 2].astype(int) - b) < tol))

    red, blue = mask(ALPHA), mask(ZEN)
    nr, nb = int(red.sum()), int(blue.sum())
    ratio = min(nr, nb) / max(nr, nb) if max(nr, nb) else 0.0

    def px(vx, vy):
        return a[int(round(vy * scale)), int(round(vx * scale))]

    top, bot = px(100, 52), px(100, 148)

    def near(p, hexs, tol=60):
        r, g, b = int(hexs[1:3], 16), int(hexs[3:5], 16), int(hexs[5:7], 16)
        return (abs(int(p[0]) - r) < tol and abs(int(p[1]) - g) < tol
                and abs(int(p[2]) - b) < tol)

    return {
        "yy_red_px": nr, "yy_blue_px": nb,
        "yy_balance": round(ratio, 3),
        "yy_balanced": ratio > 0.9,          # a true taijitu is half-and-half
        "dot_top_rgb": [int(v) for v in top], "dot_bot_rgb": [int(v) for v in bot],
        "dot_top_hex": ZEN, "dot_bot_hex": ALPHA,
        "dots_visible": bool(near(top, ZEN) and near(bot, ALPHA)),
    }


def verify(png: Path, src: Path) -> dict:
    """Page-level checks. Every one can fail."""
    import numpy as np
    from PIL import Image
    im = Image.open(png).convert("RGB")
    w, h = im.size
    g = np.asarray(im.convert("L"))

    out = {"file": png.name, "size": f"{w}x{h}", "bytes": png.stat().st_size}
    out["exact_box"] = (w == W and h == H)

    ink = float((g < 235).mean())
    out["ink_pct"] = round(100 * ink, 2)
    out["ink_ok"] = 0.06 <= ink <= 0.75

    bottom = g[H - 26:H, :]
    out["bottom_clear"] = bool((bottom > 245).mean() > 0.97)

    # Locate the two cards by their PANEL background, then compare ink inside
    # each. Guessing a y-window instead lands on the wrong bands and reports a
    # content imbalance that is really a measurement bug.
    a = np.asarray(im)
    r, gg, b = int(PANEL[1:3], 16), int(PANEL[3:5], 16), int(PANEL[5:7], 16)
    panel = ((np.abs(a[:, :, 0].astype(int) - r) < 4)
             & (np.abs(a[:, :, 1].astype(int) - gg) < 4)
             & (np.abs(a[:, :, 2].astype(int) - b) < 4))
    rows = np.where(panel.sum(axis=1) > 300)[0]
    if rows.size:
        y0, y1 = int(rows.min()), int(rows.max())
        mid = g[y0:y1 + 1, :]
        half = W // 2
        left = float((mid[:, 44:half - 10] < 200).mean())
        right = float((mid[:, half + 10:W - 44] < 200).mean())
        out["card_band"] = f"y{y0}-{y1}"
        out["card_ink_L"] = round(100 * left, 2)
        out["card_ink_R"] = round(100 * right, 2)
        out["cards_balanced"] = abs(left - right) < 0.03 and min(left, right) > 0.02
    else:
        out["card_band"] = "not found"
        out["cards_balanced"] = False

    html = src.read_text()
    leftovers = sorted(set(re.findall(r"\$[A-Z][A-Z_]{1,}", html)))
    out["leftover_tokens"] = leftovers
    out["no_tokens"] = not leftovers
    return out


def main() -> int:
    specs = json.loads((RUN / "content.json").read_text())
    ok = True
    print("yin-yang unit test (isolated 320x320 render):")
    yy = yy_selftest()
    print(f"  red {yy['yy_red_px']}px  blue {yy['yy_blue_px']}px  "
          f"balance {yy['yy_balance']}  dots visible {yy['dots_visible']}  "
          f"top={yy['dot_top_rgb']} bot={yy['dot_bot_rgb']}")
    yy_bad = [k for k in ("yy_balanced", "dots_visible") if not yy[k]]
    ok &= not yy_bad
    print()
    print("page tests:")
    rows = [yy]
    for spec in specs:
        png = build(spec)
        src = RUN / f"{spec['phase']}.html"
        v = verify(png, src)
        rows.append(v)
        checks = [k for k in ("exact_box", "ink_ok", "bottom_clear",
                              "cards_balanced", "no_tokens") if not v[k]]
        ok &= not checks
        print(f"  {v['file']}  {v['size']}  {v['bytes']}B  ink {v['ink_pct']}%  "
              f"cards {v['card_band']} L{v['card_ink_L']}%/R{v['card_ink_R']}%  "
              + ("PASS" if not checks else f"FAIL {checks}"))
    print()
    print(json.dumps(rows, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
