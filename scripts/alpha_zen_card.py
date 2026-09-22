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
import html as _html
import json
import re
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


def chron_block(mode: str, n: int = 3) -> list[tuple[str, str]]:
    """CHRON lines for the card as (css_class, text) pairs.

    The clock used to be a bare countdown footer: a title and a number of days.
    Morning now renders the upgraded block — each clock carries what it CHANGES
    when it lands, and the claim CHRON has placed rides directly under the clock
    it belongs to. Night keeps the footer until it is asked for.

    Fail-soft by construction: if the upgrade module is missing, throws, or finds
    nothing, the plain footer renders instead. A broken import must never cost the
    card, and a padding line must never stand in for a real clock.
    """
    if mode == "morning":
        try:
            from alpha_zen_chron import lines_for
            rows = lines_for(mode, n)
            if rows:
                return rows
        except Exception as exc:  # noqa: BLE001
            print(f"  ⚠ CHRON upgrade unavailable ({exc}) — using plain countdown")
    return [("cr", l) for l in chron_lines(n)]


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



#: Known outlets. The trail is derived from per-cell sources, which are written for
#: the gate ("WEALTH capital_market gold, 2026-09-21 07:16 MYT") and read like
#: machine output on a human card. Matching a known outlet recovers the human name;
#: anything unmatched falls back to its first token rather than being invented.
_OUTLETS = [
    "TradingEconomics", "Reuters", "Bloomberg", "CNBC", "USA Today", "NYT",
    "New York Times", "Malay Mail", "FMT", "Free Malaysia Today", "NST",
    "New Straits Times", "The Star", "Bernama", "The Edge", "worldoil",
    "PETRONAS", "MOF", "LHDN", "DOSM", "BNM", "Bank Negara", "WEALTH", "CHRON",
    "Frontiers in Physiology", "J Appl Physiol", "Journal of Applied Physiology",
    "ScienceDaily", "Al Jazeera", "IMF", "OECD", "PMC", "UnderstandingWar",
]


def compact_sources(raw: list[str], cap: int = 12) -> list[str]:
    """Per-cell source strings -> one human-readable outlet line, deduped.

    The cells stay clean prose and provenance still ships — but as outlets a reader
    recognises, not engine paths. Order is first-seen, so the trail is reproducible.
    """
    found, seen = [], set()
    for s in raw:
        for frag in re.split(r"[;/|]", str(s)):
            hit = next((o for o in _OUTLETS if o.lower() in frag.lower()), None)
            if hit is None:
                head = re.split(r",|\s\d{4}-|\bupdated\b", frag.strip())[0].strip()
                head = re.sub(r"\s+", " ", head)
                # machinery (capital_market, node/1234, fphys...) is not a name
                hit = head.split()[0] if head and not re.search(r"[_/]", head.split()[0]) else None
            if not hit or len(hit) < 3:
                continue
            key = hit.lower()
            if key in seen:
                continue
            seen.add(key)
            found.append(hit)
    return found[:cap]


def build_html(c: dict) -> str:
    """SIGNAL ONLY (F13 directive 2026-09-21: "too chaos. signal only.").

    WHAT WAS CROWDING IT — measured on the 21 Sep morning render, not guessed:
    roughly 40-45 typographic units. 27 primary blocks, the ARIF/SYED column
    header repeated three times, a tier subtitle above every band, a grey source
    line under EVERY one of the 18 cells, a moon/mode metadata block in the
    masthead, and a footer that recounted the structure the card was already
    showing. Several text sizes competed with no winner, and 18 micro-lines sat
    inside the reading path — the eye had nowhere to rest.

    WHAT CHANGED
      1. The column frame is declared ONCE, above the grid, not three times.
      2. Tier subtitles ("Bersumber. Tak ada puisi di sini.") are gone. They were
         atmosphere, and atmosphere above every band is noise.
      3. The 18 inline source lines are COLLECTED into one trail under the grid.
         The cells are clean prose now; provenance is still on the card, at the
         place a reader who wants to re-check goes. Moving it beats deleting it —
         a figure nobody can re-check is a claim, not a measurement.
      4. The masthead metadata block is gone; the moon survives as ONE glyph,
         because it is the day's marker and costs one character.
      5. The footer no longer recounts the structure it is showing.
      6. Fewer sizes, bigger body (15.2px/1.42 -> 16.2px/1.55), more air between
         rows. One hierarchy instead of five competing ones.

    The gate is unaffected — it validates the card JSON, never the pixels.
    """
    today = date.today()
    frac, _ = moon_phase(today)
    mode = c["mode"]
    kicker = "SEBELUM HARI MULA" if mode == "morning" else "SEBELUM TUTUP MATA"

    bands = ""
    for tier, tlabel, _tsub in TIERS:
        rows = [r for r in c["rows"] if r["tier"] == tier]
        if not rows:
            continue
        body = ""
        for r in rows:
            a, s = r["arif"], r["syed"]
            body += f"""
<div class="row">
  <div class="rn">{r["n"]}</div>
  <div class="rl">{r["label"]}</div>
  <div class="cell ca">{a["text"]}</div>
  <div class="cell cs">{s["text"]}</div>
</div>"""
        bands += f"""
<div class="band">
  <div class="bt">{tlabel}</div>
  {body}
</div>"""

    # Provenance trail. An explicit `sources` list in the card wins (it is written
    # for a human); otherwise the per-cell sources are deduped and collected here.
    explicit = [s for s in (c.get("sources") or []) if str(s).strip()]
    if explicit:
        src_lines = [str(s) for s in explicit]
    else:
        raw = [(r.get(who) or {}).get("source")
               for r in c["rows"] for who in ("arif", "syed")]
        src_lines = compact_sources([x for x in raw if x])
    srcs = " · ".join(_html.escape(x) for x in src_lines)
    sources = (f'<div class="srcb"><div class="srch">SUMBER</div>{srcs}</div>'
               if src_lines else "")

    # escaped: the event store is hand-edited, so a stray & or < must not be able
    # to break the page it is rendered into.
    chron = "".join(f'<div class="{k}">{_html.escape(t)}</div>'
                     for k, t in chron_block(mode))

    return f"""<!DOCTYPE html><html lang="ms"><head><meta charset="utf-8"><style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:1080px; background:{PAPER}; color:{INK};
        font-family:"Lato","DejaVu Sans",sans-serif; -webkit-font-smoothing:antialiased; }}
.wrap {{ width:1080px; padding:42px 46px 36px; }}

/* ONE hierarchy: masthead > day line > column frame > tier > body > trail */
.head {{ display:flex; align-items:center; gap:18px; border-bottom:2.5px solid {INK};
         padding-bottom:14px; }}
.head .moon {{ margin-left:auto; font-size:22px; color:{ACCENT}; }}
.kick {{ font-size:12px; letter-spacing:.26em; font-weight:700; color:{ACCENT}; }}
.title {{ font-size:27px; font-weight:800; letter-spacing:-.3px; line-height:1.15; }}

/* the two quotes stay — the identity device — but demoted to a quiet strip so
   they stop competing with the tier headings */
.qs {{ display:flex; gap:26px; margin:18px 0 0; }}
.q {{ flex:1; }}
.qt {{ font-size:13.5px; line-height:1.5; font-style:italic; color:{MUTED}; }}
.qa {{ font-size:10.5px; margin-top:4px; color:{MUTED}; font-weight:700;
       letter-spacing:.06em; text-transform:uppercase; }}
.q.g .qt {{ color:#4a4235; }}

.hl {{ font-size:18.5px; line-height:1.45; color:{INK}; margin:18px 0 0;
       padding-left:14px; border-left:4px solid {ACCENT}; }}

/* the column frame, declared ONCE */
.cols {{ display:flex; margin:26px 0 0; padding-bottom:5px;
         border-bottom:1.5px solid {INK}; }}
.ha, .hs {{ font-size:11px; letter-spacing:.24em; font-weight:800; width:calc(50% - 38px); }}
.ha {{ color:{YIN}; }}
.hs {{ color:{ACCENT}; }}

.band {{ margin-top:22px; }}
.bt {{ font-size:14px; letter-spacing:.2em; font-weight:800; color:{ACCENT};
       margin-bottom:6px; }}
.row {{ display:flex; border-bottom:1px solid {RULE}; padding:11px 0; }}
.rn {{ width:30px; font-size:13px; font-weight:800; color:{VIOLET}; }}
.rl {{ width:46px; font-size:10px; font-weight:800; letter-spacing:.07em; color:{MUTED};
       line-height:1.3; text-transform:uppercase; padding-right:6px; }}
.cell {{ width:calc(50% - 38px); font-size:15.8px; line-height:1.5; }}
.ca {{ color:{YIN}; border-right:1px solid {RULE}; padding-right:18px; }}
.cs {{ color:#3f3320; padding-left:18px; }}

/* provenance: collected, quiet, out of the reading path */
.srcb {{ margin-top:26px; padding-top:12px; border-top:1px solid {RULE}; }}
.srch {{ font-size:10.5px; letter-spacing:.22em; font-weight:800; color:{MUTED};
         margin-bottom:6px; }}
.srcr {{ font-size:11.5px; line-height:1.6; color:{MUTED}; }}

.chron {{ background:#fff; border:1px solid {RULE}; border-left:5px solid {ACCENT};
          padding:14px 18px; margin-top:22px; }}
.chronh {{ font-size:11px; letter-spacing:.22em; font-weight:800; color:{ACCENT};
           margin-bottom:8px; }}
.cr {{ font-size:15px; line-height:1.55; font-weight:600; }}
.crp {{ font-size:14px; line-height:1.55; font-weight:600; color:{VIOLET};
        padding-left:22px; border-left:2px solid {RULE}; margin:3px 0 3px 2px; }}
.foot {{ margin-top:22px; padding-top:11px; border-top:1px solid {RULE};
         font-size:11px; letter-spacing:.14em; color:{MUTED}; font-weight:700; }}
</style></head><body><div class="wrap">

<div class="head">
  {disc(66)}
  <div>
    <div class="kick">{kicker}</div>
    <div class="title">ALPHA-ZEN · {today.strftime('%d %b %Y').upper()}</div>
  </div>
  <div class="moon">{moon_glyph(frac)}</div>
</div>

<div class="qs">
  <div class="q y"><div class="qt">&ldquo;{c['yin_quote']['text']}&rdquo;</div>
    <div class="qa">Arif · {c['yin_quote']['author']}</div></div>
  <div class="q g"><div class="qt">&ldquo;{c['yang_quote']['text']}&rdquo;</div>
    <div class="qa">Syed · {c['yang_quote']['author']}</div></div>
</div>

{f'<div class="hl">{_html.escape(c["headline"])}</div>' if c.get("headline") else ''}

<div class="cols"><div class="ha">ARIF</div><div class="hs">SYED</div></div>

{bands}

{sources}

<div class="chron"><div class="chronh">CHRON — JAM YANG SEDANG JALAN</div>{chron}</div>
<div class="foot">DITEMPA BUKAN DIBERI</div>
</div></body></html>"""


def build_signal_html(c: dict) -> str:
    """THE SIGNAL CARD — what actually publishes.

    F13-directed 2026-09-21: "too chaos, signal only". The nine rows are the
    candidate POOL; this renders `signals` and nothing else.

    Everything that was scaffolding for the machine is gone: no tier names, no
    row numbers, no ARCH/REALITY/CLOCK tags, no source strings, no yin-yang
    quote boxes, no "9 KOMPONEN / 18 SIGNAL" imprint. What is left is the
    sentence — because a card nobody reads is not a card, it is a receipt.

    The one piece of machine language that survives is a 6px rule on the left
    of each line, coloured by whose world it belongs to. A colour cannot be
    misread as jargon, and it keeps the duality the product is named after
    without stamping ARIF / SYED over every row.
    """
    today = date.today()
    _, phase = moon_phase(today)
    mode = c["mode"]
    who_class = {"arif": "a", "syed": "s", "shared": "x"}
    body = ""
    for s in c.get("signals") or []:
        k = who_class.get(s.get("who"), "x")
        body += (f'\n<div class="sig {k}"><div class="bar"></div>'
                 f'<div class="txt">{_html.escape(s["text"])}</div></div>')
    chron = "".join(f'<div class="cr2">{_html.escape(t)}</div>' for t in chron_lines(2))
    lead = (f'<div class="slead">{_html.escape(c["headline"])}</div>'
            if c.get("headline") else "")
    return f"""<!DOCTYPE html><html lang="ms"><head><meta charset="utf-8"><style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:1080px; background:{PAPER}; color:{INK};
        font-family:"Lato","DejaVu Sans",sans-serif; -webkit-font-smoothing:antialiased; }}
.wrap {{ width:1080px; padding:46px 58px 40px; }}
.shead {{ display:flex; align-items:center; gap:18px; border-bottom:3px solid {INK};
          padding-bottom:15px; }}
.snm {{ font-size:33px; font-weight:800; letter-spacing:-.4px; line-height:1; }}
.sdt {{ font-size:19px; color:{MUTED}; font-weight:600; margin-top:5px; }}
.smeta {{ margin-left:auto; text-align:right; font-size:13px; letter-spacing:.24em;
          font-weight:800; color:{ACCENT}; line-height:1.6; }}
.slead {{ font-size:25px; line-height:1.42; font-weight:600; color:#2b2b2b;
          margin:26px 0 4px; }}
.sig {{ display:flex; gap:18px; align-items:stretch; padding:20px 0;
        border-bottom:1px solid {RULE}; }}
.bar {{ width:6px; border-radius:3px; flex:0 0 6px; }}
.sig.a .bar {{ background:{YIN}; }}
.sig.s .bar {{ background:{ACCENT}; }}
.sig.x .bar {{ background:{VIOLET}; }}
.txt {{ flex:1; font-size:23.5px; line-height:1.44; }}
.chron2 {{ margin-top:28px; padding-top:15px; border-top:2px solid {INK}; }}
.cr2 {{ font-size:16.5px; line-height:1.6; font-weight:600; color:#3a3a3a; }}
.sfoot {{ display:flex; justify-content:space-between; margin-top:20px; font-size:13px;
          color:{MUTED}; }}
</style></head><body><div class="wrap">

<div class="shead">
  {disc(62)}
  <div>
    <div class="snm">ALPHA-ZEN</div>
    <div class="sdt">{today.strftime('%A, %d %B %Y')}</div>
  </div>
  <div class="smeta">{moon_glyph(((today - date(2000, 1, 6)).days % 29.530588853) / 29.530588853)} {phase.upper()}<br>SIGNAL</div>
</div>

{lead}
{body}

<div class="chron2">{chron}</div>
<div class="sfoot"><span>ALPHA-ZEN · {mode.upper()}</span><span>DITEMPA BUKAN DIBERI</span></div>
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


def render(content: Path, outdir: Path, *, skip_gate: bool = False,
           style: str = "full") -> Path:
    c = json.loads(content.read_text())
    errs = validate(c)
    if errs:
        for x in errs:
            print(f"  ✗ {x}")
        raise SystemExit("card content invalid — refusing to render")

    # signal style is a PROJECTION, not a different card: it publishes `signals`
    # and leaves the nine rows in the file as the candidate pool. Without the
    # array there is nothing to project, and a card that silently rendered the
    # pool instead would be the "signal only" card lying about itself.
    if style == "signal" and not (c.get("signals") or []):
        raise SystemExit("style=signal needs a `signals` array — the pool alone is not a signal card")

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
    import hashlib as _hashlib
    # The style has to live in the filename. Both styles end in the same `mode`,
    # so a signal render would otherwise overwrite the full card's stable
    # ALPHA-ZEN-<MODE>.png — the very path the cron delivery contract names. One
    # render silently destroying the other's artifact is how a card gets sent
    # twice or the wrong one gets sent at all.
    sfx = "" if style == "full" else "-SIGNAL"
    html = outdir / f"{mode}{sfx}.html"
    # CONTENT-ADDRESSED ARTIFACT. The fixed path meant every render overwrote
    # the very file the previous ledger row had hashed, so 4 of 7 entries went
    # stale the moment a new card rendered. A ledger whose target is mutable
    # cannot be re-verified — and re-verifiability is its only reason to exist.
    h8 = _hashlib.sha256(content.read_bytes()).hexdigest()[:8]
    stable_png = outdir / f"ALPHA-ZEN-{mode.upper()}{sfx}.png"
    png = outdir / f"ALPHA-ZEN-{mode.upper()}{sfx}-{h8}.png"
    html.write_text(build_signal_html(c) if style == "signal" else build_html(c),
                    encoding="utf-8")

    r = subprocess.run(["google-chrome", "--headless", "--disable-gpu", "--no-sandbox",
                        "--hide-scrollbars", "--default-background-color=FFFFFFFF",
                        "--window-size=1080,4200", f"--screenshot={png}", f"file://{html}"],
                       capture_output=True, text=True, timeout=180)
    if not png.exists():
        raise SystemExit(f"render failed: {r.stderr[:400]}")
    w, h = _autocrop(png)
    # The delivery contract in the cron prompt names ALPHA-ZEN-<MODE>.png, so a
    # stable copy is kept for the sender. The LEDGER points at the
    # content-addressed file, which never moves and therefore never goes stale.
    stable_png.write_bytes(png.read_bytes())
    print(f"  {png.name}  {w}x{h}")

    # ── observability (spec section 18) ─────────────────────────────────────
    import hashlib
    try:
        rows = c["rows"]
        rec = {
            "cycle_id": f"{mode}-{date.today().isoformat()}-{hashlib.sha256(content.read_bytes()).hexdigest()[:8]}",
            "render_time": datetime.now().astimezone().isoformat(timespec="seconds"),
            "mode": mode,
            "style": style,
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
    ap.add_argument("--style", choices=("full", "signal"), default="full",
                    help="full = the 9-row grid. signal = the published narrow card "
                         "(needs a `signals` array in the content file).")
    a = ap.parse_args()
    render(Path(a.content), Path(a.out), style=a.style)
