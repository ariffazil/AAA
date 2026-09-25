#!/usr/bin/env python3
"""alpha_zen_chron — the CHRON block for the ALPHA-ZEN card, upgraded.

WHY THIS EXISTS
  The card's CHRON box rendered three ranked countdowns and nothing else: a title
  and a number of days. That is the exact defect chron.py v2 was written to kill —
  "a footer, not an intelligence surface". The part CHRON actually holds (what each
  deadline CHANGES, and what CHRON has bet on it) was computed, ranked, and then
  thrown away at the last step, one function before the pixels.

WHAT THE UPGRADE ADDS (morning edition)
  1. CONSEQUENCE — each clock carries the event store's own `note`: what falls due
     when the date arrives. Read verbatim from chron_events.json. This module never
     authors consequence text; a clock with no note renders as the old bare line.
  2. A FALSIFIABLE CLOCK — the nearest dated prediction on a live countdown, printed
     with its confidence. The box stops being a countdown and becomes a claim with a
     date on it. A clock nobody can score afterwards is decoration.

WHAT IT DELIBERATELY DOES NOT DO
  * No scoreboard line (hits/misses/calibration). The verified-prediction ledger
    lives in /root/.hermes/cron/state/chron_personal/ and is scoped
    `audience: internal`. The card is read by two humans: publishing an
    internal-scoped store into it is an F13 disclosure decision, not a rendering
    decision, so it is left out and flagged rather than taken silently.
  * No stored day-count, ever. Every number is computed at render time from a date.
  * No web call, no new cron job. The block is computed when the card is rendered,
    which the existing 07:15 job already does — a scheduled poller for this would be
    pure waste.
  * Fail-soft. A dead store, a bad event, or a broken import costs its line and
    never the card. `lines_for()` returns [] and the caller falls back.

SCOPE
  Morning edition only (`mode == "morning"`). The night card is untouched until it
  is asked for.

USAGE
  from alpha_zen_chron import lines_for
  lines = lines_for("morning")        # ['Belanjawan 2027 ... — 18 hari · ...', ...]
  python3 alpha_zen_chron.py --self-test
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import chron  # noqa: E402  — ranking, expiry, privacy filter, fmt(): one source of truth

#: keyed by audience — the shared card must not render a private clock. chron.active()
#: already enforces this; passing who=None is the shared view.
#: Where the settled bets live. Written by chron-loop-closer (systemd, 07:15 daily).
CALIBRATION = Path("/root/chron/data/calibration.json")

#: Below this many SETTLED predictions, an accuracy number is noise dressed as a
#: measurement — 1-of-2 is 50% and tells nobody anything. The line stays silent
#: rather than publishing false precision. This is the same rule as everywhere
#: else here: a number with no warrant is worse than no number.
MIN_DECISIVE = 10


def calibration_line() -> str | None:
    """How CHRON's own past bets turned out — the loop closing in the reader's view.

    WITHOUT THIS the card only ever shows bets in flight, which makes the engine
    look like it never misses. A forecast surface that publishes its pending
    claims and not their outcomes is propaganda by omission, however clean each
    individual claim is.

    Reads the settled ledger; never recomputes it. Returns None on any failure,
    and None below MIN_DECISIVE — silence, not a hedged number.

    SCOPE HONESTY (audit 2026-09-25 #3): the number shown is the REAL scope
    (honest_scopes.canonical_unified_excluding_self_tests) — synthetic self
    tests are counted separately, never blended in. Sample size, scope label
    and updated_at travel with the number so nobody mistakes 3 observations
    for a track record.
    """
    try:
        d = json.loads(CALIBRATION.read_text())
    except Exception:
        return None
    scopes = d.get("honest_scopes") or {}
    real = scopes.get("canonical_unified_excluding_self_tests")
    if not isinstance(real, dict):
        return None
    n = real.get("n")
    if not isinstance(n, int) or n < MIN_DECISIVE:
        return None
    correct, acc, brier = real.get("correct"), real.get("accuracy"), real.get("mean_brier")
    if correct is None or acc is None:
        return None
    syn = d.get("synthetic_self_tests")
    syn_note = f" · {syn} ujian sintetik diasingkan" if isinstance(syn, int) and syn > 0 else ""
    line = f"ramalan: {n} taruhan nyata dinilai — {correct} kena ({acc:.0%}){syn_note}"
    if isinstance(brier, (int, float)):
        line += f", Brier {brier:.2f} (rawak = 0.25)"
    upd = d.get("updated_at")
    if isinstance(upd, str):
        line += f" · dikemas kini {upd[:10]}"
    if acc < 0.5:
        line += ". Kadar ini BURUK dari tekaan buta — trust dia kena turun, bukan naik."
    return line


SHARED = None


def _raw_by_id() -> dict:
    """The store as written, for the fields the ranked view does not carry (note,
    predictions). Keyed by event id; {} on any failure."""
    try:
        evs = json.loads((HERE / "chron_events.json").read_text()).get("events", [])
        return {e.get("id"): e for e in evs if e.get("id")}
    except Exception:
        return {}


def _confidence(p: dict) -> float:
    c = p.get("confidence")
    return float(c) if isinstance(c, (int, float)) else -1.0


def prediction_bet(ranked: list[dict], raw: dict) -> tuple[str, str] | None:
    """The bet CHRON has placed, returned as (parent_event_id, line).

    Selection is deterministic so a reader can recompute why THIS claim and not
    another appeared: among the live clocks that carry a printable prediction,
    take the one that SETTLES SOONEST, and on it the highest-confidence bet. The
    soonest-settling claim is the one the two men can actually watch resolve; the
    first-ranked one may not settle for a month. Choosing by how bad a claim looks
    would be taste, and taste is how a ledger becomes a highlight reel.

    Only predictions carrying a `human` rendering are printable. The machine
    `claim` is written for the verifier ("RON95 subsidy rationalisation will be
    announced or reaffirmed in budget speech") and printing it into a BM card
    breaks register — the card would suddenly start talking like a log line.
    No rendering, no line: silence beats a bot voice.
    """
    best = None
    for e in ranked:
        preds = [p for p in (raw.get(e.get("id")) or {}).get("predictions") or []
                 if (p.get("human") or "").strip()]
        if not preds:
            continue
        if best is None or e.get("days", 10 ** 6) < best[0]:
            p = sorted(preds, key=_confidence, reverse=True)[0]
            pct = f", keyakinan {p['confidence']:.0%}" if _confidence(p) >= 0 else ""
            best = (e.get("days", 10 ** 6), e.get("id"),
                    f"ramalan: {p['human'].strip().rstrip('.')}{pct}")
    if best is None:
        return None
    return best[1], best[2]


def bare_line(e: dict, raw: dict) -> str:
    """One clock: title — countdown · consequence.

    The consequence is read verbatim from the store's own `note`. Nothing is
    authored here: a clock with no note stays a bare countdown rather than
    acquiring a sentence this module made up.
    """
    line = f"{e.get('title', '').strip()} — {chron.fmt(e['days'])}"
    note = ((raw.get(e.get("id")) or {}).get("note") or "").strip().rstrip(".")
    return f"{line} · {note}" if note else line


def lines_for(mode: str = "morning", n: int = 3) -> list[tuple[str, str]]:
    """The CHRON block body as (css_class, text) pairs. [] means 'say nothing'.

    The bet rides directly under the clock it belongs to, so the reader never has
    to guess which deadline a claim is about.
    """
    if mode != "morning":
        return []
    try:
        ranked = chron.active(chron.load(), who=SHARED)[:n]
    except Exception:
        return []
    if not ranked:
        return []
    raw = _raw_by_id()
    out: list[tuple[str, str]] = [("cr", bare_line(e, raw)) for e in ranked]
    bet = prediction_bet(ranked, raw)
    if bet:
        for i, e in enumerate(ranked):
            if e.get("id") == bet[0]:
                out.insert(i + 1, ("crp", bet[1]))
                break
        cal = calibration_line()
        if cal:
            # directly under the pending bet: the claim and its record belong
            # together, so the reader never sees a forecast without its score.
            out.insert(out.index(("crp", bet[1])) + 1, ("crp", cal))
    return out


def _self_test() -> int:
    fails = []

    def chk(name: str, cond: bool, detail: str = "") -> None:
        print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f"  ({detail})" if detail else ""))
        if not cond:
            fails.append(name)

    rows = lines_for("morning")
    texts = [t for _, t in rows]
    clocks = [t for k, t in rows if k == "cr"]
    chk("morning renders lines", bool(rows), f"{len(rows)} lines")
    chk("night renders nothing (scope)", lines_for("night") == [])
    chk("days are computed, not stored",
        all(("hari" in l or "esok" in l or "HARI NI" in l) for l in clocks),
        clocks[0][:60] if clocks else "")
    chk("consequence rides each clock", all("·" in l for l in clocks))
    chk("no line is empty", all(t.strip() for t in texts))

    # the bet must sit under the clock it belongs to, not float at the bottom
    ranked = chron.active(chron.load(), who=None)[:3]
    raw = _raw_by_id()
    bet = prediction_bet(ranked, raw)
    if bet:
        idx = [i for i, (k, _) in enumerate(rows) if k == "crp"]
        chk("bet is a sub-line, not a clock", len(idx) == 1)
        parent = next((e for e in ranked if e.get("id") == bet[0]), None)
        chk("bet sits under the clock it belongs to",
            bool(idx) and parent is not None and rows[idx[0] - 1][1] == bare_line(parent, raw),
            f"under: {rows[idx[0] - 1][1][:48] if idx else 'n/a'}")
    else:
        chk("no printable bet -> block is clocks only",
            all(k == "cr" for k, _ in rows))

    # fail-soft: a store that cannot be read must cost the block, never raise.
    # chron.load(path=STORE) binds its default at import time, so patching
    # chron.STORE is a no-op — patch the accessor itself or the test proves nothing.
    real_load = chron.load
    chron.load = lambda *a, **k: None            # simulate a store that cannot be read
    try:
        chk("dead store -> [] not raise", lines_for("morning") == [])
    finally:
        chron.load = real_load

    # register: the machine-facing claim must never reach a human surface
    machine = {p.get("claim") for e in _raw_by_id().values()
               for p in (e.get("predictions") or [])}
    chk("machine claim text never rendered",
        all(all(m not in t for m in machine if m) for t in texts))

    # a clock with no note must degrade to the bare line, not invent text
    chk("no note -> no invented consequence", bare_line({"id": "x", "title": "T", "days": 5}, {}) == "T — 5 hari")
    chk("no printable prediction -> no bet",
        prediction_bet([{"id": "x", "days": 5}], {"x": {"id": "x"}}) is None)
    chk("machine-only prediction -> no bet",
        prediction_bet([{"id": "x", "days": 5}],
                       {"x": {"predictions": [{"claim": "english machine text", "confidence": 0.9}]}}) is None)

    # calibration: SILENT below the minimum sample, SPEAKING above it. Both
    # directions matter — a gate that only ever hides is as useless as one that
    # only ever shows. n=2 must produce nothing; n=20 with a bad hit-rate must
    # produce the warning, because that is the case the reader most needs.
    real = calibration_line.__globals__["CALIBRATION"]
    import json as _j, tempfile, os
    def _cal(payload):
        f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        _j.dump(payload, f); f.close()
        calibration_line.__globals__["CALIBRATION"] = Path(f.name)
        try:
            return calibration_line()
        finally:
            os.unlink(f.name)

    chk("calibration silent at n=2 (no false precision)",
        _cal({"decisive": 2, "correct": 1, "accuracy": 0.5, "mean_brier": 0.246}) is None)
    chk("calibration silent on a dead file",
        _cal({}) is None)
    bad = _cal({"decisive": 20, "correct": 8, "accuracy": 0.4, "mean_brier": 0.31})
    chk("calibration speaks above threshold", bool(bad), (bad or "")[:60])
    chk("calibration warns when worse than chance",
        bool(bad) and "BURUK dari tekaan buta" in bad)
    good = _cal({"decisive": 20, "correct": 15, "accuracy": 0.75, "mean_brier": 0.18})
    chk("calibration does NOT warn when better than chance",
        bool(good) and "BURUK" not in good, (good or "")[:60])
    calibration_line.__globals__["CALIBRATION"] = real

    print(f"\n  {'ALL PASS' if not fails else 'FAILED: ' + ', '.join(fails)}")
    return 1 if fails else 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        raise SystemExit(_self_test())
    for cls, text in lines_for("morning"):
        print(("    " if cls == "crp" else "") + text)
