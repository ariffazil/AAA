#!/usr/bin/env python3
"""APEX-ZEN CHRON v3 — nine shared components, eighteen individually selected signals.

WHAT CHANGED FROM v2, AND WHY
  v2 spent ~40% of the visual budget on a large yin-yang and then asked nine
  GENERIC items to serve two different men. Both were wrong.

  1. The yin-yang is now an IDENTITY device — small, at the top. Arif already
     knows he and Syed are different-but-equal; that idea does not need a third
     of the page. The budget goes to information.
  2. Nine components, EACH carrying two signals, one selected for Arif and one
     selected for Syed, independently. 18 selections, 9 rows. Symmetry in the
     structure, asymmetry in the content.

THREE EPISTEMIC TIERS
  KENA TAHU  externally grounded — news, market data, deadline, observation.
             No poetry in this tier. A claim that cannot be sourced does not ship.
  SUKA TAHU  personalised curiosity. May be softer, but must still carry substance.
  EUREKA     where the machine earns its existence — it CONNECTS rather than
             fetches. Two facts neither reader would place together, plus the
             invariant that links them. Marked INT when the link is this lane's
             construction rather than a published finding.

THE PRIVACY LINE — unchanged and enforced
  Memory may answer "what is worth putting in front of this person today?"
  Memory may NOT answer publicly "why do we know this about him?"
  An item may be SELECTED because of private knowledge; it may not CONTAIN any.
  privacy.json holds the deny patterns and the gate fails the BUILD. The item
  text is written by hand, not generated, so the gate is a backstop rather than
  the only control.

NEVER FILL A SLOT BECAUSE THE TEMPLATE ASKS FOR NINE
  If today's random fact is thin, something better from another domain takes the
  slot. Nine rows is a floor on effort, not a quota of filler.
"""
import json
import re
import subprocess
import sys
import datetime
from pathlib import Path

RUN = Path("/root/AAA/forge_work/apex-zen-chron")
RUN.mkdir(parents=True, exist_ok=True)

W = 1080
H = 1084          # measured against the rendered content, not guessed. Raised
                  # from 984 when the CHRON strip landed and content hit the
                  # bottom edge (dead space 0px, bottom_clear FAIL).
ALPHA = "#c0392b"   # red  — Yang / Syed
ZEN = "#1f4e79"     # blue — Yin  / Arif
INK = "#1d2733"
MUTED = "#5f6b78"
RULE = "#dde3ea"
PANEL = "#f7f9fb"


def yin_yang(size: int = 54, rotate: float = 0.0) -> str:
    """Small identity mark. Full circles rather than the two-arc S-path: a wrong
    sweep flag yields a pinwheel that still reads as a yin-yang at a glance."""
    return f'''<svg width="{size}" height="{size}" viewBox="0 0 200 200"
     style="vertical-align:-12px;transform:rotate({rotate}deg)">
  <circle cx="100" cy="100" r="96" fill="{ALPHA}"/>
  <path d="M100,4 A96,96 0 0 1 100,196 Z" fill="{ZEN}"/>
  <circle cx="100" cy="148" r="48" fill="{ZEN}"/>
  <circle cx="100" cy="52"  r="48" fill="{ALPHA}"/>
  <circle cx="100" cy="52"  r="13" fill="{ZEN}"/>
  <circle cx="100" cy="148" r="13" fill="{ALPHA}"/>
  <circle cx="100" cy="100" r="96" fill="none" stroke="{INK}" stroke-width="3"/>
</svg>'''


# ── privacy gate ─────────────────────────────────────────────────────────────

def privacy_scan(text: str, priv: dict) -> list[str]:
    """Return the rules that fire on `text`. Case-insensitive, word-bounded."""
    low = text.lower()
    hits = []
    for rule in priv["never_emit"]:
        m = re.search(rule["pattern"].lower(), low)
        if m:
            hits.append(f"{rule['pattern']!r} -> {m.group(0)[:60]!r} ({rule['why']})")
    return hits


def privacy_selftest(priv: dict) -> tuple[bool, list[str]]:
    """Prove the gate can FAIL, and prove it does not cry wolf.

    The first version of this gate failed both halves: it passed real leaks it
    should have caught inside a long document, and it rejected 'forward-deployed'
    (contains 'ward') and 'ketakselarasan' (contains 'rasa'). Both failures were
    found by running it, not by reading it.
    """
    problems = []
    for bad in priv["_selftest_must_catch"]:
        if not privacy_scan(bad, priv):
            problems.append(f"MISSED: {bad!r}")
    for good in priv["_selftest_must_allow"]:
        h = privacy_scan(good, priv)
        if h:
            problems.append(f"FALSE ALARM: {good!r} -> {h[0][:70]}")
    return (not problems), problems


def privacy_gate(spec: dict, priv: dict) -> list[str]:
    """Fail the build if anything private could reach a third reader."""
    return privacy_scan(json.dumps(spec, ensure_ascii=False), priv)


# ── CHRON — the clock that is computed, never typed ──────────────────────────

BANDS = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}


def load_chron(path: Path, now: datetime.date) -> tuple[list, list]:
    """Split events into live and expired, and compute each delta.

    The delta is the whole point. §6: `delta = target_date - render_timestamp`.
    A number that is typed into a template is a number that is wrong tomorrow.
    """
    data = json.loads(path.read_text())
    live, expired = [], []
    for e in data["events"]:
        tgt = datetime.date.fromisoformat(e["target_date"])
        days = (tgt - now).days
        rec = dict(e, days=days, target_iso=e["target_date"])
        if days < 0:
            rec["state"] = "EXPIRED"
            expired.append(rec)
        else:
            rec["state"] = "ACTIVE"
            live.append(rec)
    return live, expired


def rank_chron(live: list) -> list:
    """Rank by urgency x consequence x relevance x actionability — not by date.

    §6 is explicit that the nearest date is not the most important one. Banded
    inputs, banded output: a fake-precise float over qualitative inputs would be
    arithmetic theatre.
    """
    def relevance(e):
        a = set(e.get("audience", []))
        return 3 if {"arif", "syed"} <= a else (2 if a else 1)

    def urgency(e):
        d = e["days"]
        return 3 if d <= 30 else (2 if d <= 120 else 1)

    for e in live:
        e["urgency"] = urgency(e)
        e["relevance"] = relevance(e)
        e["score"] = (e["urgency"] * BANDS[e["consequence"]]
                      * e["relevance"] * BANDS[e["actionability"]])
    return sorted(live, key=lambda e: (-e["score"], e["days"]))


def render_chron(live: list, expired: list, limit: int = 3) -> str:
    """One strip of computed countdowns. Expired events never render a number."""
    ranked = rank_chron(live)[:limit]
    cells = []
    for e in ranked:
        cells.append(
            f'<div class="cc"><div class="ct">{e["title"]}</div>'
            f'<div class="cd">{e["days"]}<span class="cu">hari</span></div>'
            f'<div class="cn">{e["note"]}</div>'
            f'<div class="cm">{e["confidence"]} keyakinan tarikh &middot; '
            f'{e["target_iso"]}</div></div>')
    exp = ""
    if expired:
        exp = ('<div class="cx">luput: ' +
               ", ".join(f'{e["title"]} ({e["target_iso"]})' for e in expired) +
               "</div>")
    return (f'<div class="ch-hd">CHRON &mdash; jam yang berjalan '
            f'<span>(dikira dari tarikh, bukan ditaip)</span></div>'
            f'<div class="ch-row">{"".join(cells)}</div>{exp}')


# ── template ─────────────────────────────────────────────────────────────────

TEMPLATE = r'''<!DOCTYPE html>
<html lang="ms"><head><meta charset="utf-8"><title>APEX-ZEN $PHASELABEL</title>
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  html,body { width:1080px; height:${HEIGHT}px; }
  body { font-family:"DejaVu Sans","Liberation Sans",sans-serif; color:$INK;
         background:#ffffff; padding:0 40px; }

  .bar { display:flex; justify-content:space-between; align-items:baseline;
         padding:20px 0 10px 0; border-bottom:2px solid $INK; }
  .bar .l { font-size:15px; font-weight:700; letter-spacing:3px; }
  .bar .r { font-size:12px; color:$MUTED; letter-spacing:1px; }

  .hero { display:flex; align-items:center; gap:14px; padding:14px 0 10px 0; }
  .hero .t { font-size:19px; font-weight:700; letter-spacing:2.5px; }
  .hero .t .sub { font-size:11px; font-weight:400; color:$MUTED;
                  letter-spacing:1.2px; margin-left:10px; }

  .cols { display:grid; grid-template-columns:118px 1fr 1fr; gap:10px;
          align-items:end; padding-bottom:9px; border-bottom:2px solid $INK; }
  .cols .who { font-size:12.5px; font-weight:700; letter-spacing:4px; }
  .cols .who.a { color:$ZEN; } .cols .who.s { color:$ALPHA; }
  .cols .lens { font-size:11.5px; color:$MUTED; font-style:italic; margin-top:2px;
                letter-spacing:.2px; }

  .sec { display:grid; grid-template-columns:118px 1fr 1fr; gap:10px;
         margin:12px 0 3px 0; align-items:center; }
  .sec .nm { font-size:10.5px; font-weight:700; letter-spacing:3px; color:#fff;
             background:$INK; text-align:center; padding:3px 0; }
  .sec .ln { grid-column:2 / span 2; height:1px; background:$RULE; }

  .row { display:grid; grid-template-columns:118px 1fr 1fr; gap:10px;
         padding:8px 0 9px 0; border-bottom:1px solid #eef2f6; }
  .row .lb { }
  .row .lb .n { font-size:13px; font-weight:700; color:$MUTED; letter-spacing:1px; }
  .row .lb .t { font-size:10px; font-weight:700; letter-spacing:1.6px; color:$INK;
                margin-top:1px; }
  .cell { font-size:10.8px; line-height:1.42; }
  .cell .tg { display:inline-block; font-size:7.5px; font-weight:700; letter-spacing:.6px;
              color:#fff; padding:1px 4px; margin-right:4px; vertical-align:1px; }
  .tg.o { background:$ZEN; } .tg.d { background:#6b7a89; } .tg.i { background:$ALPHA; }
  .cell.a { border-left:2px solid #cfe0ef; padding-left:8px; }
  .cell.s { border-left:2px solid #f0d3ce; padding-left:8px; }
  .cell.q { font-style:italic; }
  .cell b { color:$ZEN; }

  .foot { margin-top:12px; padding-top:9px; border-top:1px solid $RULE;
          display:flex; justify-content:space-between; font-size:9px; color:$MUTED; }

  .chron { margin-top:11px; padding-top:9px; border-top:2px solid $INK; }
  .ch-hd { font-size:9.5px; font-weight:700; letter-spacing:2.6px; margin-bottom:6px; }
  .ch-hd span { font-weight:400; letter-spacing:.6px; color:$MUTED;
                text-transform:none; font-size:9px; }
  .ch-row { display:grid; grid-template-columns:repeat(3,1fr); gap:9px; }
  .cc { background:$PANEL; border-left:3px solid $INK; padding:6px 8px 7px 8px; }
  .cc .ct { font-size:9.5px; font-weight:700; letter-spacing:.6px; }
  .cc .cd { font-size:21px; font-weight:700; line-height:1.05; margin:1px 0 2px 0; }
  .cc .cd .cu { font-size:9.5px; font-weight:400; color:$MUTED; margin-left:3px;
                letter-spacing:.6px; }
  .cc .cn { font-size:8.6px; line-height:1.34; color:#3c4855; }
  .cc .cm { font-size:7.2px; color:$MUTED; margin-top:3px; letter-spacing:.3px; }
  .cx { font-size:8px; color:$MUTED; margin-top:5px; font-style:italic; }
</style></head><body>

<div class="bar">
  <div class="l">APEX&middot;ZEN <span style="color:$MUTED;font-weight:400">&nbsp;CHRON</span></div>
  <div class="r">$DATE &nbsp;&middot;&nbsp; $DAY &nbsp;&middot;&nbsp; $PHASELABEL</div>
</div>

<div class="hero">
  $YINYANG
  <div class="t">TODAY BETWEEN TWO WORLDS<span class="sub">$CAPTION</span></div>
</div>

<div class="cols">
  <div></div>
  <div><div class="who a">ARIF &mdash; YIN</div><div class="lens">&ldquo;$LENS_YIN&rdquo;</div></div>
  <div><div class="who s">SYED &mdash; YANG</div><div class="lens">&ldquo;$LENS_YANG&rdquo;</div></div>
</div>

$BODY

$CHRON

<div class="foot"><span>$FOOTL</span><span>$FOOTR</span></div>

</body></html>'''


def render_body(spec: dict) -> str:
    out = []
    for sec_name, rows in spec["sections"]:
        out.append(f'<div class="sec"><div class="nm">{sec_name}</div>'
                   f'<div class="ln"></div></div>')
        for r in rows:
            def cell(d, side):
                cls = "cell " + side + (" q" if r.get("question") else "")
                return (f'<div class="{cls}"><span class="tg {d["tier"]}">'
                        f'{d["tier"].upper()}</span>{d["text"]}</div>')
            out.append(
                f'<div class="row"><div class="lb"><div class="n">{r["n"]}</div>'
                f'<div class="t">{r["label"]}</div></div>'
                + cell(r["arif"], "a") + cell(r["syed"], "s") + "</div>")
    return "".join(out)


def build(spec: dict, now: datetime.date | None = None) -> Path:
    """Render one poster. `now` is injectable so the clock self-test can prove
    the countdowns move — a hardcoded number cannot move."""
    now = now or datetime.date.today()
    live, expired = load_chron(RUN / "chron.json", now)
    html = (TEMPLATE
            .replace("${HEIGHT}", str(H))
            .replace("$ALPHA", ALPHA).replace("$ZEN", ZEN)
            .replace("$INK", INK).replace("$MUTED", MUTED).replace("$RULE", RULE)
            .replace("$PANEL", PANEL)
            .replace("$YINYANG", yin_yang(54, spec.get("rotate", 0)))
            .replace("$BODY", render_body(spec))
            .replace("$CHRON", render_chron(live, expired))
            .replace("$LENS_YIN", spec["lens_yin"])
            .replace("$LENS_YANG", spec["lens_yang"])
            .replace("$CAPTION", spec["caption"])
            .replace("$FOOTL", spec["foot_left"]).replace("$FOOTR", spec["foot_right"])
            # longest token first — a prefix collision leaves bare uppercase junk
            .replace("$PHASELABEL", spec["phase_label"])
            .replace("$DATE", spec["date"]).replace("$DAY", spec["day"]))
    src = RUN / f"{spec['phase']}.html"
    src.write_text(html)
    png = RUN / (f"APEX-ZEN-CHRON-{spec['num']}-{spec['phase']}-"
                 f"{spec['date_key']}.png")
    r = subprocess.run([
        "google-chrome", "--headless=new", "--disable-gpu", "--no-sandbox",
        "--hide-scrollbars", "--default-background-color=FFFFFFFF",
        f"--window-size={W},{H}", f"--screenshot={png}", f"file://{src}",
    ], capture_output=True, text=True, timeout=180)
    if not png.exists():
        raise RuntimeError("chrome produced no file: " + (r.stderr or "")[:300])
    return png


# ── verification ─────────────────────────────────────────────────────────────

YY_NAMES = ["QYANG", "QYIN", "PHASELABEL", "LENS_YIN", "LENS_YANG", "YINYANG",
            "BLOCKS", "BODY", "CELLS", "FOOTL", "FOOTR", "SECNAME", "HEIGHT"]


def leak_check(html: str) -> tuple[list, list]:
    leftovers = sorted(set(re.findall(r"\$[A-Z][A-Z_]{1,}", html)))
    leaked = [t for t in YY_NAMES if t in html]
    return leftovers, leaked


def leak_selftest() -> bool:
    """Prove the detector can FAIL before trusting it to pass."""
    bad = 'Do nothing which is of no use.QYANGSRC'
    good = 'Do nothing which is of no use.'
    caught = bool(leak_check(bad)[1] or leak_check("<p>$QYANG</p>")[0])
    clean = not leak_check(good)[0] and not leak_check(good)[1]
    return caught and clean


def verify(png: Path, src: Path, spec: dict) -> dict:
    import numpy as np
    from PIL import Image
    im = Image.open(png).convert("RGB")
    w, h = im.size
    g = np.asarray(im.convert("L"))

    out = {"file": png.name, "size": f"{w}x{h}", "bytes": png.stat().st_size,
           "exact_box": (w == W and h == H)}
    out["ink_pct"] = round(100 * float((g < 235).mean()), 2)
    out["ink_ok"] = 6.0 <= out["ink_pct"] <= 80.0
    out["bottom_clear"] = bool((g[H - 22:H, :] > 245).mean() > 0.97)

    rows = np.where((g < 235).sum(axis=1) > 3)[0]
    out["content_end_y"] = int(rows.max()) if rows.size else 0
    out["dead_space_px"] = int(H - rows.max() - 1) if rows.size else H

    html = src.read_text()
    # Per-row cell pairing. The first version used a non-greedy
    # r'<div class="row">.*?</div></div>' and reported (0,0) for all nine rows:
    # the match ended at the FIRST '</div></div>', which occurs inside the label
    # block before any cell. Splitting on the row marker is exact.
    # Prefix, not exact: row 09 is the question row and renders
    # class="cell a q" / class="cell s q". Matching the closing quote made the
    # final row look empty — a check that would have passed a poster with a
    # missing question cell.
    chunks = html.split('<div class="row">')[1:]
    pairs = [(c.count('class="cell a'), c.count('class="cell s'))
             for c in chunks]
    out["row_count"] = html.count('<div class="row">')
    out["rows_nine"] = out["row_count"] == 9
    out["cell_pairs"] = pairs
    out["every_row_has_both"] = bool(pairs) and all(a == 1 and s == 1 for a, s in pairs)
    leftovers, leaked = leak_check(html)
    out["leftover_tokens"], out["leaked_names"] = leftovers, leaked
    out["no_tokens"] = not leftovers and not leaked
    # both lenses rendered
    out["lenses_ok"] = spec["lens_yin"] in html and spec["lens_yang"] in html
    return out


def clock_selftest() -> tuple[bool, list[str]]:
    """Prove the countdowns are COMPUTED, not typed.

    Renders the same spec ten days apart and requires every displayed day-count
    to shift by exactly ten. A hardcoded "164 hari" cannot move, so this test
    fails on the exact defect §6 forbids — which both lanes shipped: the parallel
    lane's HTML still contains a literal "164 days" and "21 days".

    It also proves expiry: an event past its target must stop rendering a number
    and appear in the missed list instead.
    """
    problems = []
    spec = json.loads((RUN / "content.json").read_text())[0]
    d0 = datetime.date(2026, 9, 18)
    d1 = d0 + datetime.timedelta(days=10)

    def counts(now):
        live, _ = load_chron(RUN / "chron.json", now)
        return {e["id"]: e["days"] for e in rank_chron(live)[:3]}

    a, b = counts(d0), counts(d1)
    if set(a) != set(b):
        problems.append(f"active set changed with only the render date: {a} vs {b}")
    for k in a:
        if k in b and b[k] != a[k] - 10:
            problems.append(f"{k}: {a[k]} -> {b[k]}, expected a 10-day shift")

    # expiry: push the clock past every target
    live_far, expired_far = load_chron(RUN / "chron.json", datetime.date(2027, 6, 1))
    if live_far:
        problems.append(f"events still ACTIVE past their dates: {[e['id'] for e in live_far]}")
    if not expired_far:
        problems.append("no events expired — the expiry path is untested")
    html_far = render_chron(live_far, expired_far)
    # Check for the day-count CELL, not for digits: the expired line prints
    # ISO dates, which are digits, so a naive digit scan fails on correct output.
    if '<div class="cd">' in html_far:
        problems.append("a day-count cell still rendered for an expired event")

    return (not problems), problems


def main() -> int:
    specs = json.loads((RUN / "content.json").read_text())
    priv = json.loads((RUN / "privacy.json").read_text())
    ok = True

    print()
    ok_priv, priv_problems = privacy_selftest(priv)
    print(f"privacy gate self-test (must catch real leaks, must not cry wolf): "
          f"{'PASS' if ok_priv else 'FAIL'}")
    for p in priv_problems:
        print(f"    {p}")
    ok &= ok_priv

    print()
    print("privacy gate on content (before anything renders):")
    for spec in specs:
        hits = privacy_gate(spec, priv)
        ok &= not hits
        if hits:
            print(f"  FAIL {spec['phase']}:")
            for x in hits:
                print(f"       {x}")
        else:
            print(f"  PASS {spec['phase']}: {len(priv['never_emit'])} patterns, 0 hits")
    if not ok:
        print("\nREFUSED TO RENDER — private material reached a public artifact.")
        return 1

    print()
    print(f"leak-detector self-test: {'PASS' if leak_selftest() else 'FAIL'}")
    ok &= leak_selftest()

    print()
    ok_clock, clock_problems = clock_selftest()
    print(f"CHRON clock self-test (countdowns must MOVE, expired must EXPIRE): "
          f"{'PASS' if ok_clock else 'FAIL'}")
    for p in clock_problems:
        print(f"    {p}")
    ok &= ok_clock
    live, expired = load_chron(RUN / "chron.json", datetime.date.today())
    for e in rank_chron(live)[:3]:
        print(f"    {e['id']:<24} {e['days']:>4} hari  score {e['score']:>3}  "
              f"conf {e['confidence']}")
    if expired:
        print(f"    expired: {[e['id'] for e in expired]}")

    print()
    print("page tests:")
    for spec in specs:
        png = build(spec)
        v = verify(png, RUN / f"{spec['phase']}.html", spec)
        bad = [k for k in ("exact_box", "ink_ok", "bottom_clear", "rows_nine",
                           "every_row_has_both", "no_tokens", "lenses_ok")
               if not v.get(k)]
        ok &= not bad
        print(f"  {v['file']}")
        print(f"    {v['size']}  {v['bytes']}B  ink {v['ink_pct']}%  "
              f"rows {v['row_count']}  pairs {v['cell_pairs'][:2]}...  "
              f"dead {v['dead_space_px']}px")
        print(f"    " + ("PASS" if not bad else f"FAIL {bad}"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
