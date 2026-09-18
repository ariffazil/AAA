#!/usr/bin/env python3
"""alpha_zen_card — render THE 9. Layout only; never invents content.

VISUAL BUDGET
  The earlier version spent ~40% of the page saying "Arif and Syed are different
  but equal". They know that. The yin-yang is now an IDENTITY DEVICE in the
  header — small, doing its job — and the space goes to information instead.

  The disc still matters: it is the only mark that states the two halves are
  equal weight. Measured by message volume in that group Arif posts ~761 and
  Syed ~209, so a bar chart would render Syed at 27% and would say something
  false. VOLUME IS NOT WEIGHT. Keeping the disc small keeps the claim without
  paying a third of the page for it.

THE MEMORY BOUNDARY
  Memory informs SELECTION, never DISCLOSURE. Both men read this card. Known
  facts choose what is relevant; they are never reprinted, and the reason an item
  was chosen never appears. Perspective A != Perspective B — the card personalises
  without ever claiming either man's inner state.

LIGHT BACKGROUND — standing instruction (F13, 2026-09-18).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHRON = HERE / "chron.py"
OUT = Path("/root/AAA/forge_work/alpha-zen")

PAPER = "#faf8f4"
INK = "#1c1c1c"
MUTED = "#6b6b6b"
RULE = "#dedad2"
YIN = "#16293d"
YANG = "#e7dcc6"
ACCENT = "#8a5a10"
VIOLET = "#43357a"
SOFT = "#f4f1ea"

TIERS = [
    ("KENA_TAHU", "KENA TAHU", "Bersumber. Tak ada puisi di sini."),
    ("SUKA_TAHU", "SUKA TAHU", "Personal, tapi mesti ada isi."),
    ("EUREKA", "EUREKA", "Di sini mesin berhak wujud. Sambung, bukan petik."),
]


def moon_phase(d: date) -> tuple[float, str]:
    frac = ((d - date(2000, 1, 6)).days % 29.530588853) / 29.530588853
    for lim, nm in [(0.03, "anak bulan"), (0.22, "bulan sabit muda"), (0.28, "suku pertama"),
                    (0.47, "hampir purnama"), (0.53, "purnama"), (0.72, "hampir gerhana"),
                    (0.78, "suku akhir"), (0.97, "bulan tua"), (1.01, "anak bulan")]:
        if frac < lim:
            return frac, nm
    return frac, "anak bulan"


def moon_glyph(f: float) -> str:
    if f < 0.03 or f >= 0.97:
        return "●"
    if f < 0.22:
        return "☽"
    if f < 0.28:
        return "◐"
    if f < 0.72:
        return "◑"
    return "☾"


def chron_lines(n: int = 3) -> list[str]:
    try:
        r = subprocess.run([sys.executable, str(CHRON)], capture_output=True, text=True, timeout=30)
        return [l for l in r.stdout.strip().splitlines() if l.strip()][:n]
    except Exception:
        return []


def disc(size: int = 74) -> str:
    """Small identity device. Opposite-coloured dots, or the symbol degrades."""
    c, r, half, dot = size / 2, size / 2 - 2, (size / 2 - 2) / 2, (size / 2 - 2) / 7
    dark = (f"M {c},{c-r} A {r},{r} 0 0 0 {c},{c+r} A {half},{half} 0 0 0 {c},{c} "
            f"A {half},{half} 0 0 1 {c},{c-r} Z")
    return f"""<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}"
  xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Yin-yang">
  <defs><clipPath id="dc"><circle cx="{c}" cy="{c}" r="{r}"/></clipPath></defs>
  <circle cx="{c}" cy="{c}" r="{r}" fill="{YANG}"/>
  <g clip-path="url(#dc)"><path d="{dark}" fill="{YIN}"/></g>
  <circle cx="{c}" cy="{c+half}" r="{dot}" fill="{YANG}"/>
  <circle cx="{c}" cy="{c-half}" r="{dot}" fill="{YIN}"/>
  <circle cx="{c}" cy="{c}" r="{r}" fill="none" stroke="{YIN}" stroke-width="1.6"/>
</svg>"""


def build_html(c: dict) -> str:
    today = date.today()
    frac, phase = moon_phase(today)
    mode = c["mode"]
    kicker = "SEBELUM HARI MULA" if mode == "morning" else "SEBELUM TUTUP MATA"

    bands = ""
    for tier, tlabel, tsub in TIERS:
        rows = [r for r in c["rows"] if r["tier"] == tier]
        if not rows:
            continue
        body = ""
        for r in rows:
            a, s = r["arif"], r["syed"]
            ab = f'<span class="src">{a["source"]}</span>' if a.get("source") else ""
            sb = f'<span class="src">{s["source"]}</span>' if s.get("source") else ""
            body += f"""
<div class="row">
  <div class="rn">{r["n"]}</div>
  <div class="rl">{r["label"]}</div>
  <div class="cell ca">{a["text"]}{ab}</div>
  <div class="cell cs">{s["text"]}{sb}</div>
</div>"""
        bands += f"""
<div class="band">
  <div class="bh"><span class="bt">{tlabel}</span><span class="bs">{tsub}</span></div>
  <div class="hdr"><div class="rn"></div><div class="rl"></div>
    <div class="ha">ARIF</div><div class="hs">SYED</div></div>
  {body}
</div>"""

    chron = "".join(f'<div class="cr">{l}</div>' for l in chron_lines())

    return f"""<!DOCTYPE html><html lang="ms"><head><meta charset="utf-8"><style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:1080px; background:{PAPER}; color:{INK};
        font-family:"Lato","DejaVu Sans",sans-serif; -webkit-font-smoothing:antialiased; }}
.wrap {{ width:1080px; padding:38px 46px 34px; }}

.head {{ display:flex; align-items:center; gap:20px; border-bottom:2.5px solid {INK};
         padding-bottom:13px; }}
.kick {{ font-size:15px; letter-spacing:.28em; font-weight:700; color:{ACCENT}; }}
.title {{ font-size:30px; font-weight:800; letter-spacing:-.3px; line-height:1.1; }}
.meta {{ margin-left:auto; text-align:right; font-size:14px; color:{MUTED}; font-weight:600;
         line-height:1.5; }}

.qs {{ display:flex; gap:16px; margin:16px 0 6px; }}
.q {{ flex:1; padding:12px 15px; border-radius:2px; }}
.q.y {{ background:{YIN}; color:#eef2f7; }}
.q.g {{ background:{SOFT}; border-left:4px solid {ACCENT}; }}
.qwho {{ font-size:11px; letter-spacing:.24em; font-weight:800; opacity:.78; margin-bottom:5px; }}
.qt {{ font-size:16.5px; line-height:1.4; font-style:italic; }}
.qa {{ font-size:12px; margin-top:5px; opacity:.75; font-weight:600; }}
.hl {{ font-size:19px; color:{MUTED}; line-height:1.4; margin:14px 0 4px; }}

.band {{ margin-top:22px; }}
.bh {{ display:flex; align-items:baseline; gap:12px; margin-bottom:9px; }}
.bt {{ font-size:19px; letter-spacing:.22em; font-weight:800; color:{ACCENT}; }}
.bs {{ font-size:13px; color:{MUTED}; font-style:italic; }}
.hdr {{ display:flex; border-bottom:1.5px solid {INK}; padding-bottom:4px; }}
.ha, .hs {{ font-size:12px; letter-spacing:.22em; font-weight:800; }}
.ha {{ width:calc(50% - 86px); color:{YIN}; }}
.hs {{ width:calc(50% - 86px); color:{ACCENT}; }}
.row {{ display:flex; border-bottom:1px solid {RULE}; padding:8px 0; align-items:flex-start; }}
.rn {{ width:34px; font-size:15px; font-weight:800; color:{VIOLET}; padding-top:1px; }}
.rl {{ width:52px; font-size:11px; font-weight:800; letter-spacing:.08em; color:{MUTED};
       line-height:1.25; padding-top:3px; text-transform:uppercase; }}
.cell {{ width:calc(50% - 86px); font-size:15.2px; line-height:1.42; padding-right:12px; }}
.ca {{ color:{YIN}; border-right:1px solid {RULE}; padding-right:14px; }}
.cs {{ color:#3f3320; padding-left:2px; }}
.src {{ display:block; font-size:10.5px; color:{MUTED}; font-weight:600; margin-top:3px;
        letter-spacing:.02em; }}

.chron {{ background:#fff; border:1px solid {RULE}; border-left:5px solid {ACCENT};
          padding:13px 17px; margin-top:24px; }}
.chronh {{ font-size:12px; letter-spacing:.22em; font-weight:800; color:{ACCENT}; margin-bottom:7px; }}
.cr {{ font-size:15.5px; line-height:1.5; font-weight:600; }}
.foot {{ display:flex; justify-content:space-between; margin-top:20px; padding-top:11px;
         border-top:1px solid {RULE}; font-size:13px; color:{MUTED}; }}
</style></head><body><div class="wrap">

<div class="head">
  {disc(74)}
  <div>
    <div class="kick">{kicker}</div>
    <div class="title">ALPHA-ZEN · {today.strftime('%d %b %Y').upper()}</div>
  </div>
  <div class="meta">{moon_glyph(frac)} fasa bulan: {phase}<br>{mode.upper()} EDITION</div>
</div>

<div class="qs">
  <div class="q y"><div class="qwho">ARIF · YIN</div>
    <div class="qt">&ldquo;{c['yin_quote']['text']}&rdquo;</div>
    <div class="qa">— {c['yin_quote']['author']}</div></div>
  <div class="q g"><div class="qwho">SYED · YANG</div>
    <div class="qt">&ldquo;{c['yang_quote']['text']}&rdquo;</div>
    <div class="qa">— {c['yang_quote']['author']}</div></div>
</div>

{f'<div class="hl">{c["headline"]}</div>' if c.get("headline") else ''}

{bands}

<div class="chron"><div class="chronh">CHRON — JAM YANG SEDANG JALAN</div>{chron}</div>
<div class="foot"><span>ALPHA-ZEN · {mode.upper()} · 9 KOMPONEN / 18 SIGNAL</span>
  <span>DITEMPA BUKAN DIBERI</span></div>
</div></body></html>"""


def _autocrop(png: Path) -> tuple[int, int]:
    from PIL import Image
    im = Image.open(png).convert("RGB")
    w, h = im.size
    o = im.getpixel((2, 2))
    bg = o if isinstance(o, tuple) else (int(o), int(o), int(o))
    last = 0
    for y in range(h - 1, 0, -4):
        for x in range(0, w, 8):
            p = im.getpixel((x, y))
            pp = p if isinstance(p, tuple) else (int(p), int(p), int(p))
            if sum(abs(int(a) - int(b)) for a, b in zip(pp, bg)) > 24:
                last = y
                break
        if last:
            break
    nh = min(h, max(200, last + 1))
    if nh < h:
        im.crop((0, 0, w, nh)).save(png)
    return w, nh


def validate(c: dict) -> list[str]:
    e: list[str] = []
    for k in ("mode", "yin_quote", "yang_quote", "rows"):
        if k not in c:
            e.append(f"missing {k}")
    if e:
        return e
    rows = c["rows"]
    if len(rows) != 9:
        e.append(f"rows: must be exactly 9, got {len(rows)}")
    for z in ("yin_quote", "yang_quote"):
        q = c.get(z) or {}
        if not q.get("text") or not q.get("author"):
            e.append(f"{z}: a quote without attribution is not a quote")
    want = ["01", "02", "03", "04", "05", "06", "07", "08", "09"]
    got = [r.get("n") for r in rows]
    if got != want:
        e.append(f"row numbers must run 01..09 in order, got {got}")
    for r in rows:
        for who in ("arif", "syed"):
            if not (r.get(who) or {}).get("text"):
                e.append(f"row {r.get('n')}: {who} signal is empty — a half-filled row is worse than an omitted one")
        if r.get("tier") == "KENA_TAHU":
            for who in ("arif", "syed"):
                if not (r.get(who) or {}).get("source"):
                    e.append(f"row {r.get('n')} ({who}): KENA TAHU needs a source — no poetry in this tier")
    return e


def render(content: Path, outdir: Path, *, skip_gate: bool = False) -> Path:
    c = json.loads(content.read_text())
    errs = validate(c)
    if errs:
        for x in errs:
            print(f"  ✗ {x}")
        raise SystemExit("card content invalid — refusing to render")

    # The quality gate is a WALL, not a checklist. Rendering is cheap; sending a
    # padded card is expensive. Gate before bytes exist so nothing to send can
    # be produced from a card that failed section 16.
    if not skip_gate:
        g = subprocess.run([sys.executable, str(HERE / "alpha_zen_gate.py"), str(content)],
                           capture_output=True, text=True)
        print(g.stdout.rstrip())
        if g.returncode != 0:
            raise SystemExit("quality gate: HOLD — no artifact produced")

    outdir.mkdir(parents=True, exist_ok=True)
    mode = c["mode"]
    html = outdir / f"{mode}.html"
    png = outdir / f"ALPHA-ZEN-{mode.upper()}.png"
    html.write_text(build_html(c), encoding="utf-8")
    r = subprocess.run(["google-chrome", "--headless", "--disable-gpu", "--no-sandbox",
                        "--hide-scrollbars", "--default-background-color=FFFFFFFF",
                        "--window-size=1080,4200", f"--screenshot={png}", f"file://{html}"],
                       capture_output=True, text=True, timeout=180)
    if not png.exists():
        raise SystemExit(f"render failed: {r.stderr[:400]}")
    w, h = _autocrop(png)
    print(f"  {png.name}  {w}x{h}")

    # ── observability (spec section 18) ─────────────────────────────────────
    import hashlib
    try:
        rows = c["rows"]
        rec = {
            "cycle_id": f"{mode}-{date.today().isoformat()}-{hashlib.sha256(content.read_bytes()).hexdigest()[:8]}",
            "render_time": datetime.now().astimezone().isoformat(timespec="seconds"),
            "mode": mode,
            "selected_count": len(rows),
            "signal_count": sum(1 for r in rows if (r.get("arif") or {}).get("text"))
                           + sum(1 for r in rows if (r.get("syed") or {}).get("text")),
            "source_count": sum(1 for r in rows if (r.get("arif") or {}).get("source"))
                          + sum(1 for r in rows if (r.get("syed") or {}).get("source")),
            # These three were hardcoded 0. That is not an absence of data — it is
            # an ASSERTION that no candidate was ever rejected for privacy,
            # duplication or weakness. Nothing populates them, so the ledger was
            # stating a confident falsehood inside a verifiable record: exactly
            # the defect class this whole day was spent catching in others.
            #
            # null is the honest value: "not measured". A funnel cannot be claimed
            # until a producer actually records the funnel.
            "privacy_rejections": None,
            "duplicate_rejections": None,
            "weak_signal_rejections": None,
            "rejection_tracking": "NOT_MEASURED",
            "render_status": "OK",
            "artifact": str(png),
            "artifact_sha256": hashlib.sha256(png.read_bytes()).hexdigest(),
            "dimensions": [w, h],
            "gate": "PASS",
        }
        log = outdir / "cycles.jsonl"
        with log.open("a") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(f"  cycle logged → {log}")
    except Exception as exc:  # noqa: BLE001
        print(f"  ⚠ cycle log failed: {exc}")

    return png


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("content")
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()
    render(Path(a.content), Path(a.out))
