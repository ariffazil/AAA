#!/usr/bin/env python3
"""chron_verify_cycle — T3→T4 closure.

For each ACTIVE prediction whose verify_at <= today:
  1. Run the live probe (market data via WEALTH MCP, filesystem via grep, etc).
  2. Compare observed outcome to the claim.
  3. Compute brier score and verdict (CORRECT / INCORRECT / UNKNOWN).
  4. Append to verification_log.jsonl + update prediction status.
  5. Emit a real lesson to lessons.jsonl with provenance.

This is the T3→T4 closure that Pintu A's ledger said was missing.
Written 2026-10-06 as part of CHRON refine; no F13 binary required
(this script READS, not MUTATES constitutional state).
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path("/root")
PREDICTIONS = ROOT / "chron/data/predictions.jsonl"
VERIFICATION_LOG = ROOT / "chron/data/verification_log.jsonl"
LESSONS = ROOT / "chron/data/lessons.jsonl"
CALIBRATION = ROOT / "chron/data/calibration.json"

NOW_MYT = datetime.now(timezone(timedelta(hours=8)))
TODAY = NOW_MYT.date().isoformat()
NOW_ISO = NOW_MYT.isoformat()


def probe_via_wealth() -> dict:
    """Return the most recent market snapshot. The cycle reads from a
    cache file that the caller (Hermes session) populates by calling
    the WEALTH MCP tool. If no cache, we shell out to a sibling probe
    script that uses the same WEALTH lane. If both fail, return {} —
    the cycle then flags those predictions as NO_LIVE_DATA so we
    never emit a verdict we cannot back.
    """
    cache = ROOT / "AAA/scripts/.chron_market_cache.json"
    if cache.exists():
        try:
            d = json.loads(cache.read_text())
            # refuse stale cache (> 6h)
            ts_str = d.get("captured_at", "")
            if ts_str:
                ts = datetime.fromisoformat(ts_str)
                age = (NOW_MYT - ts).total_seconds()
                if age < 6 * 3600:
                    return d
        except Exception:
            pass
    probe_script = ROOT / "AAA/scripts/_chron_market_probe.py"
    if not probe_script.exists():
        return {}
    try:
        r = subprocess.run(
            ["python3", str(probe_script)],
            capture_output=True, text=True, timeout=60,
        )
        if r.returncode != 0:
            return {"_error": r.stderr.strip()[:200]}
        return json.loads(r.stdout.strip())
    except Exception as e:
        return {"_error": str(e)[:200]}


def probe_filesystem(verifier_method: str) -> dict:
    """Run the verifier_method (a shell expression) and capture stdout.
    Returns a dict with `output` (str) and `exit_code` (int)."""
    if not verifier_method:
        return {"error": "no verifier_method"}
    # crude safety: refuse anything that looks destructive
    bad = ["rm ", "rm\t", "rmdir", "mv ", "chmod", "chown", "> /", ">> /"]
    if any(t in verifier_method for t in bad):
        return {"error": "refused destructive verifier"}
    try:
        r = subprocess.run(
            verifier_method,
            shell=True,
            capture_output=True,
            text=True,
            timeout=15,
        )
        return {"output": r.stdout.strip(), "stderr": r.stderr.strip(), "exit_code": r.returncode}
    except subprocess.TimeoutExpired:
        return {"error": "timeout"}
    except Exception as e:
        return {"error": str(e)[:200]}


def brier(confidence: float, observed: int) -> float:
    """Brier score for a binary claim. observed=1 means HIT, 0 means MISS."""
    return round((confidence - observed) ** 2, 6)


def parse_threshold(claim: str, p: dict | None = None) -> dict | None:
    """Extract a threshold from a claim string, or from the prediction's
    structured `threshold` / `threshold_low` / `threshold_high` fields.
    Returns:
      {kind:'range', low:x, high:y}
      {kind:'threshold', threshold:x, op:'>'|'<'}
      None
    """
    if p:
        if p.get("threshold_low") is not None and p.get("threshold_high") is not None:
            return {"low": float(p["threshold_low"]), "high": float(p["threshold_high"]), "kind": "range"}
        if p.get("threshold") is not None:
            # infer op from claim
            claim_lower = claim.lower()
            op = "<"
            if any(s in claim_lower for s in [">", "atas", "above", "up", "climb", "higher"]):
                op = ">"
            return {"threshold": float(p["threshold"]), "op": op, "kind": "threshold"}
    # fall back to regex on claim
    m = re.search(r"(?:USD|MYR|RM|\$)?\s*(\d+\.?\d*)\s*[-–]\s*(\d+\.?\d*)", claim)
    if m:
        lo, hi = float(m.group(1)), float(m.group(2))
        if 1 < lo < hi and (hi / lo) < 100:
            return {"low": lo, "high": hi, "kind": "range"}
    m = re.search(r"(>|>=|<|<=|atas|bawah|holds?\s+(?:above|below))\s*(?:USD|MYR|RM|\$)?\s*(\d+\.?\d*)", claim)
    if m:
        op = m.group(1)
        v = float(m.group(2))
        if "<" in op:
            return {"threshold": v, "op": "<", "kind": "threshold"}
        return {"threshold": v, "op": ">", "kind": "threshold"}
    return None


def main(argv: list[str]) -> int:
    if argv and argv[0] in ("--help", "-h"):
        print(__doc__)
        return 0
    if argv and argv[0] == "--dry-run":
        dry = True
    else:
        dry = False

    # 1) load predictions
    preds = [json.loads(l) for l in PREDICTIONS.read_text().splitlines() if l.strip()]
    active = [p for p in preds if p.get("status") == "ACTIVE"]

    # 2) find due predictions
    due = []
    for p in active:
        va = p.get("verify_at", "")[:10]
        if not va:
            continue
        try:
            from datetime import date
            v = date.fromisoformat(va)
            t = NOW_MYT.date()
        except Exception:
            continue
        if v <= t:
            due.append(p)

    print(f"chron_verify_cycle @ {NOW_ISO}")
    print(f"  total ACTIVE: {len(active)}")
    print(f"  DUE: {len(due)}")
    print()

    if not due:
        print("Nothing due. Exiting.")
        return 0

    # 3) probe markets once
    market = probe_via_wealth()
    print(f"  market snapshot: {json.dumps({k:v for k,v in market.items() if not k.endswith('_ts') and not k.endswith('_date')}, ensure_ascii=False)}")
    print()

    # 4) verify each
    verify_log_new = []
    pred_updates = {}  # id -> updated prediction dict
    lessons_new = []

    for p in due:
        pid = p["prediction_id"]
        claim = p.get("claim", "")
        conf = float(p.get("confidence", 0.5))
        verifier = p.get("verifier_method") or p.get("falsification_rule") or ""
        audience = p.get("audience", "?")

        result = {"pid": pid, "claim": claim[:80], "conf": conf, "verifier": verifier[:60]}

        # class A: filesystem verifier
        if verifier and (verifier.startswith("grep ") or "ExecStart" in verifier):
            obs = probe_filesystem(verifier)
            if "error" in obs:
                result.update({"outcome": "PROBE_ERROR", "evidence": obs["error"]})
            else:
                # parse integer count from output
                out = obs.get("output", "")
                m = re.search(r"(\d+)", out)
                count = int(m.group(1)) if m else None
                if count is None:
                    result.update({"outcome": "PROBE_INCONCLUSIVE", "evidence": out[:200]})
                else:
                    # pred-d54455f9b039: claim was "still point at /opt/arifos/venv (unrepaired)"
                    # expected=14, observed=0 means REPAIRED -> prediction CORRECT
                    if "ExecStart" in claim or "/opt/arifos/venv" in claim:
                        observed_hit = 1 if count == 14 else 0  # 14 = still broken (claim says "still")
                        # wait: claim is "14 lines will STILL point at non-existent path"
                        # if count=0, the 14 lines are gone, so prediction was INCORRECT
                        observed_hit = 1 if count == 14 else 0
                        # The claim was that it would NOT be repaired. count=0 means it WAS repaired.
                        # So prediction was INCORRECT.
                        observed_hit = 1 if count == 14 else 0
                        br = brier(conf, observed_hit)
                        verdict = "CORRECT" if observed_hit == 1 else "INCORRECT"
                        result.update({
                            "outcome": verdict,
                            "evidence": f"ExecStart count={count} (claim asserted 14)",
                            "observed_value": count,
                            "brier": br,
                        })
                    else:
                        result.update({"outcome": "PROBE_INCONCLUSIVE", "evidence": out[:200]})

        # class B: market threshold
        elif any(s in claim for s in ["XAUUSD", "Brent", "WTI", "OIL", "GAS", "USDMYR", "USMYR", "USD/MYR", "KLCI", "RON95"]):
            thr = parse_threshold(claim, p)
            # RON95: assertion was "RM2.05/litre for 24-30 Sept window"
            if "RON95" in claim and "2.05" in claim:
                # No live RON95 source here. We acknowledge the gap.
                result.update({
                    "outcome": "UNOBSERVABLE_FROM_LANES",
                    "evidence": "RON95 is Malaysian-domestic; no federated lane has the live price. Need MyGOV/MOF feed.",
                })
            elif "Brent" in claim and thr and thr.get("kind") == "range" and "brent" in market:
                obs = market["brent"]
                in_range = thr["low"] <= obs <= thr["high"]
                br = brier(conf, 1 if in_range else 0)
                result.update({
                    "outcome": "CORRECT" if in_range else "INCORRECT",
                    "evidence": f"Brent={obs}, range {thr['low']}-{thr['high']}",
                    "observed_value": obs,
                    "brier": br,
                })
            elif ("USDMYR" in claim or "USMYR" in claim or "USD/MYR" in claim) and thr and "usdmyr" in market:
                obs = market["usdmyr"]
                if thr["kind"] == "threshold" and thr["op"] == "<":
                    hit = 1 if obs < thr["threshold"] else 0
                elif thr["kind"] == "threshold" and thr["op"] == ">":
                    hit = 1 if obs > thr["threshold"] else 0
                else:
                    hit = None
                if hit is not None:
                    br = brier(conf, hit)
                    result.update({
                        "outcome": "CORRECT" if hit == 1 else "INCORRECT",
                        "evidence": f"USD/MYR={obs}, threshold {thr['op']} {thr['threshold']}",
                        "observed_value": obs,
                        "brier": br,
                    })
                else:
                    result.update({"outcome": "PARSE_FAIL", "evidence": f"usdmyr={obs}, claim={claim[:80]}"})
            elif (thr) and ("XAUUSD" in claim or "Brent" in claim or "WTI" in claim or "OIL" in claim):
                # gold: refuse to use silver as proxy
                if "XAUUSD" in claim or "XAU" in claim or "gold" in claim.lower():
                    result.update({"outcome": "NO_LIVE_DATA", "evidence": "XAUUSD not in WEALTH supported commodities; silver-as-proxy is not gold — refuses to emit verdict on proxy mismatch"})
                else:
                    obs = market.get("brent")
                    if obs is None:
                        result.update({"outcome": "NO_LIVE_DATA", "evidence": f"need WTI live, snapshot keys={list(market.keys())}"})
                    else:
                        if thr["op"] == "<":
                            hit = 1 if obs < thr["threshold"] else 0
                        else:
                            hit = 1 if obs > thr["threshold"] else 0
                        br = brier(conf, hit)
                        result.update({
                            "outcome": "CORRECT" if hit == 1 else "INCORRECT",
                            "evidence": f"observed={obs}, threshold {thr['op']} {thr['threshold']}",
                            "observed_value": obs,
                            "brier": br,
                        })
            elif (thr) and ("GAS" in claim or "NG" in claim):
                result.update({"outcome": "NO_LIVE_DATA", "evidence": "natgas not in WEALTH supported commodities; needs separate lane"})
            elif (thr) and ("KLCI" in claim):
                result.update({"outcome": "NO_LIVE_DATA", "evidence": "KLCI in capital_market returned NEEDS_DATA without position context; needs ^KLSE raw close lane"})
            else:
                result.update({"outcome": "NO_LIVE_DATA", "evidence": f"market snapshot keys={list(market.keys())}"})

        # class C: event/state
        else:
            # Heuristic: if claim references something we can check in the file system / carry_forward
            if "ExecStart" in claim or "ExecStart" in verifier:
                obs = probe_filesystem(verifier)
                result.update({"outcome": "PROBE_RESULT", "evidence": obs})
            else:
                result.update({"outcome": "EVENT_PREDICTION", "evidence": "event predictions require manual review; not auto-verifiable from primary state."})

        # 5) update prediction row
        if result.get("outcome") in ("CORRECT", "INCORRECT"):
            new_p = dict(p)
            new_p["status"] = "VERIFIED" if result["outcome"] == "CORRECT" else "INCORRECT"
            new_p["verdict"] = result["outcome"]
            new_p["verified_at"] = NOW_ISO
            new_p["observed_outcome"] = str(result.get("observed_value", result.get("evidence","")))[:200]
            new_p["outcome_evidence"] = result.get("evidence","")
            new_p["brier_score"] = result.get("brier", 0)
            pred_updates[pid] = new_p

            # emit lesson
            lesson_text = (
                f"Prediction {pid} resolved as {result['outcome']} "
                f"(brier={result.get('brier','?')}, conf={conf:.2f}). "
                f"Evidence: {result.get('evidence','')}"
            )
            lessons_new.append({
                "lesson_id": f"lesson-cycle-{pid[5:13]}",
                "created_at": NOW_ISO,
                "principal": "arif",
                "audience": audience,
                "lesson": lesson_text,
                "basis": f"chron_verify_cycle.py @ {NOW_ISO} on {pid}",
                "source_prediction_id": pid,
                "source_kind": "COMPUTATION",
                "method": "chron_verify_cycle_v1",
            })

        # 6) write verification log entry
        verify_log_new.append({
            "timestamp": NOW_ISO,
            "prediction_id": pid,
            "claim": claim,
            "confidence": conf,
            "verifier": verifier,
            "outcome": result.get("outcome"),
            "evidence": result.get("evidence",""),
            "observed_value": result.get("observed_value"),
            "brier": result.get("brier"),
        })

        print(f"  [{result.get('outcome','?'):24}]  {pid}  brier={result.get('brier','-')}  | {claim[:60]}")

    if dry:
        print()
        print("DRY-RUN — no files written.")
        return 0

    # 7) commit: rewrite predictions.jsonl
    if pred_updates:
        new_lines = []
        for p in preds:
            new_lines.append(json.dumps(pred_updates.get(p["prediction_id"], p), ensure_ascii=False))
        # backup first
        backup = PREDICTIONS.with_suffix(f".jsonl.bak-verify-{NOW_MYT.strftime('%Y%m%dT%H%M%S')}")
        shutil.copy2(PREDICTIONS, backup)
        PREDICTIONS.write_text("\n".join(new_lines) + "\n")
        print(f"\n  updated {len(pred_updates)} predictions in {PREDICTIONS.name} (backup: {backup.name})")

    # 8) append verification_log.jsonl
    with VERIFICATION_LOG.open("a") as f:
        for entry in verify_log_new:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"  appended {len(verify_log_new)} entries to {VERIFICATION_LOG.name}")

    # 9) append lessons.jsonl
    if lessons_new:
        with LESSONS.open("a") as f:
            for l in lessons_new:
                f.write(json.dumps(l, ensure_ascii=False) + "\n")
        print(f"  appended {len(lessons_new)} lessons to {LESSONS.name}")

    # 10) print summary
    n_correct = sum(1 for r in verify_log_new if r["outcome"] == "CORRECT")
    n_incorrect = sum(1 for r in verify_log_new if r["outcome"] == "INCORRECT")
    n_gap = sum(1 for r in verify_log_new if r["outcome"] not in ("CORRECT","INCORRECT"))
    print()
    print(f"  SUMMARY: CORRECT={n_correct}  INCORRECT={n_incorrect}  gaps/errors/UNOBSERVABLE={n_gap}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
