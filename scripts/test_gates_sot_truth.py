"""Tests for the g_sot_truth TRUTH_DRIFT gate (docforge/gates.py).

Negative-bearing by design: a gate that can only return ok=True is decoration.
Every branch that must FAIL is asserted to FAIL, on a real PDF artifact.

Run: python3 /root/AAA/scripts/test_gates_sot_truth.py
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "/root/AAA/scripts")
from docforge.gates import CHAIN, Finding, g_sot_truth, _sot_value  # noqa: E402

CALIB = Path("/root/chron/data/calibration.json")
REAL_PDF = Path("/root/AAA/forge_work/2026-10-08-edition-016/EDITION-016.pdf")

results: list[tuple[bool, str]] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    results.append((bool(cond), f"{name}{(' — ' + detail) if detail else ''}"))


# ── 0. wiring ────────────────────────────────────────────────────────────────
check("CHAIN has 7 gates", len(CHAIN) == 7, f"got {len(CHAIN)}")
check("g_sot_truth is in CHAIN", g_sot_truth in CHAIN)
check("g_sot_truth is last (cannot mask earlier gates)", CHAIN[-1] is g_sot_truth)

# ── 1. SOT reader against the REAL calibration file ─────────────────────────
val, err = _sot_value(CALIB, "mean_brier")
check("_sot_value reads live mean_brier", err is None and abs(val - 0.14881943646798773) < 1e-12,
      f"val={val!r} err={err!r}")

_, err = _sot_value(CALIB, "no_such_key")
check("absent key -> error, not silent None", err is not None and "absent" in err, f"err={err!r}")

_, err = _sot_value(Path("/root/does-not-exist-fi003.json"), "mean_brier")
check("absent SOT file -> error", err is not None and "absent" in err, f"err={err!r}")

bad = Path(tempfile.gettempdir()) / "fi003-malformed-sot.json"
bad.write_text("{ this is not json")
_, err = _sot_value(bad, "x")
check("malformed SOT -> error (fail closed)", err is not None and "unreadable" in err, f"err={err!r}")

# ── 2. opt-in contract: no assertions => pass, cannot break existing editions ─
f = g_sot_truth(REAL_PDF, {})
check("no sot_assertions -> ok=True", f.ok is True and f.gate == "sot_truth", f.detail)
check("  ...and says so explicitly", "not asserted" in f.detail or "no SOT-backed" in f.detail, f.detail)

# ── 3. NEGATIVE: the actual 0.088 drift class must FAIL ─────────────────────
f = g_sot_truth(REAL_PDF, {"sot_assertions": [
    {"label": "mean_brier", "sot": str(CALIB), "key": "mean_brier", "render": "0.149"}]})
check("document lacking the SOT value -> ok=False", f.ok is False, f.detail)
check("  ...and names it TRUTH_DRIFT", "TRUTH_DRIFT" in f.detail, f.detail)
check("  ...and cites the real SOT number", "0.14881943646798773" in f.detail, f.detail)

# ── 4. NEGATIVE: unreadable SOT fails closed (Void Guard) ───────────────────
f = g_sot_truth(REAL_PDF, {"sot_assertions": [
    {"label": "x", "sot": "/root/does-not-exist-fi003.json", "key": "x"}]})
check("unreadable SOT -> ok=False, NOT a pass", f.ok is False, f.detail)

# ── 5. POSITIVE + forbid branch, on the real PDF ────────────────────────────
txt_marker = "EDITION-016"
sot_ok = Path(tempfile.gettempdir()) / "fi003-sot-positive.json"
sot_ok.write_text(json.dumps({"marker": txt_marker}))

f = g_sot_truth(REAL_PDF, {"sot_assertions": [
    {"label": "marker", "sot": str(sot_ok), "key": "marker"}]})
check("SOT value present in document -> ok=True", f.ok is True, f.detail)
check("  ...and witnesses the value", txt_marker in f.detail, f.detail)

f = g_sot_truth(REAL_PDF, {"sot_assertions": [
    {"label": "marker", "sot": str(sot_ok), "key": "marker", "forbid": ["EDITION"]}]})
check("forbidden stale literal present -> ok=False", f.ok is False, f.detail)
check("  ...and names the stale literal", "EDITION" in f.detail, f.detail)

# ── 6. default render formatting for floats (no explicit `render`) ──────────
f = g_sot_truth(REAL_PDF, {"sot_assertions": [
    {"label": "mean_brier", "sot": str(CALIB), "key": "mean_brier"}]})
check("float with no `render` defaults to 3dp and fails honestly",
      f.ok is False and "0.149" in f.detail, f.detail)

# ── report ──────────────────────────────────────────────────────────────────
bad_n = sum(1 for ok, _ in results if not ok)
for ok, name in results:
    print(f"{'PASS' if ok else 'FAIL'}  {name}")
print(f"\n{len(results) - bad_n}/{len(results)} passed")
sys.exit(1 if bad_n else 0)
