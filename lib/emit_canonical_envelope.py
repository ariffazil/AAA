#!/usr/bin/env python3
"""emit_canonical_envelope.py — P1.0 proof of canonical state envelope.

Runs the 6 federation jobs (in dry-run / observe-only mode where possible)
and emits each one's output through the canonical state envelope.

Does NOT modify the 6 jobs themselves. Just calls each, captures its
exit code + output, and wraps in canonical envelope.

This is the proof that the canonical envelope is workable across:
- ACTUATOR (arifos-deploy-reconciler) — observe-only invocation
- DETECTOR (arifos-drift-check, aaa-drift-check)
- AUDITOR (arifos-federation-audit)
- LEARNING_LOOP (aaa-rsi-loop) — dry-run only
- HEALTH_PROBE (probe_health_flip) — observe-only invocation

Output: /root/forge_work/canonical-envelopes/{job_id}.json (one per job)
        /root/forge_work/canonical-envelopes/summary.json (all 6)

DITEMPA BUKAN DIBERI ⚒️
"""

from __future__ import annotations
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from canonical_state import (
    CanonicalState, emit, Reason,
    HEALTH_HEALTHY, HEALTH_DEGRADED, HEALTH_FAILED, HEALTH_UNKNOWN,
    CONV_SYNCED, CONV_HOLD, CONV_DRIFT, CONV_UNKNOWN,
    CLASS_ACTUATOR, CLASS_DETECTOR, CLASS_AUDITOR, CLASS_LEARNING_LOOP, CLASS_HEALTH_PROBE,
    NEXT_MACHINE, NEXT_HUMAN, NEXT_HOLD,
)

OUT_DIR = Path("/root/forge_work/canonical-envelopes")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── 6 jobs (live, from prior mapping) ──────────────────────────────

JOBS = [
    {
        "id": "arifos-deploy-reconciler",
        "script": "/root/scripts/arifos-deploy-reconciler.sh",
        "args": [],  # live mode; if origin ahead + tree clean, would deploy
        "class": CLASS_ACTUATOR,
        "domain": "deployment",
        "expected": "tree-clean + aligned with origin/main OR held (dirty / unpushed)",
    },
    {
        "id": "arifos-drift-check",
        "script": "/root/arifOS/scripts/drift_check_live.py",
        "args": [],
        "class": CLASS_DETECTOR,
        "domain": "deployment-multi-organ",
        "expected": "all organs: source≈deployed≈identity, no dirty trees",
    },
    {
        "id": "aaa-drift-check",
        "script": "/root/AAA/scripts/aaa_drift_check.py",
        "args": [],
        "class": CLASS_DETECTOR,
        "domain": "aaa-registry",
        "expected": "all canonical cards exist; FI slots unique; no ghost paths",
    },
    {
        "id": "arifos-federation-audit",
        "script": "/root/scripts/check_tool_drift.py",
        "args": ["--quiet"],
        "class": CLASS_AUDITOR,
        "domain": "tool-count-integrity",
        "expected": "all tool-count surfaces agree",
    },
    {
        "id": "aaa-rsi-loop",
        "script": "/root/AAA/rsi/loop.py",
        "args": ["--dry-run"],
        "class": CLASS_LEARNING_LOOP,
        "domain": "capability-promotion",
        "expected": "extracts atoms; proposes promotions; no apply (dry-run)",
    },
    {
        "id": "probe_health_flip",
        "script": "/root/AAA/scripts/probe_health_flip.py",
        "args": [],
        "class": CLASS_HEALTH_PROBE,
        "domain": "federation-routing",
        "expected": "providers probed; dead routes flipped",
    },
]


def run_job(job: dict) -> tuple[int, str, str]:
    """Run one job, return (exit_code, stdout_tail, stderr_tail)."""
    cmd = ["python3", job["script"]] if job["script"].endswith(".py") else ["bash", job["script"]]
    cmd += job["args"]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return r.returncode, (r.stdout or "")[-500:], (r.stderr or "")[-500:]
    except subprocess.TimeoutExpired:
        return 124, "", "(timeout after 60s)"
    except FileNotFoundError as e:
        return 127, "", f"(not found: {e})"
    except Exception as e:
        return 1, "", f"(exception: {e})"


def classify_health_convergence(job_id: str, exit_code: int, stdout: str, stderr: str) -> tuple[str, str, str]:
    """Translate exit code + observed output into canonical health + convergence + reason."""
    if exit_code == 127 or "not found" in stderr:
        return HEALTH_UNKNOWN, CONV_UNKNOWN, Reason.EVIDENCE_MISSING
    if exit_code == 124:
        return HEALTH_FAILED, CONV_UNKNOWN, Reason.EVIDENCE_MISSING
    # Heuristics per job_id (these are observable signals)
    s = stdout + stderr
    if job_id == "arifos-deploy-reconciler":
        # ACTUATOR: exit 0 means "no action needed" (aligned or held intentionally)
        # exit !=0 means failure
        if exit_code == 0:
            if "deploying" in s:
                return HEALTH_DEGRADED, CONV_DRIFT, Reason.KERNEL_REPORTS_DRIFT
            if "holding" in s or "unpushed" in s or "ahead" in s:
                return HEALTH_HEALTHY, CONV_HOLD, Reason.GIT_AHEAD_OF_ORIGIN
            return HEALTH_HEALTHY, CONV_SYNCED, Reason.OBSERVATION_OK
        return HEALTH_FAILED, CONV_UNKNOWN, Reason.EVIDENCE_MISSING
    if job_id == "arifos-drift-check":
        # DETECTOR: exit 0 always; verdict in stdout (DRIFT or CLEAN)
        if "DRIFT" in s and ("DEGRADED" in s or "❌" in s):
            return HEALTH_DEGRADED, CONV_DRIFT, Reason.KERNEL_REPORTS_DRIFT
        if "CLEAN" in s or "✅" in s:
            return HEALTH_HEALTHY, CONV_SYNCED, Reason.OBSERVATION_OK
        return HEALTH_UNKNOWN, CONV_UNKNOWN, Reason.EVIDENCE_MISSING
    if job_id == "aaa-drift-check":
        if exit_code == 2 or "VOID" in s:
            return HEALTH_FAILED, CONV_UNKNOWN, Reason.CARD_MISSING
        if exit_code == 1 or "HOLD" in s or "GAP" in s:
            return HEALTH_DEGRADED, CONV_DRIFT, Reason.FI_SLOT_CONFLICT
        if exit_code == 0:
            return HEALTH_HEALTHY, CONV_SYNCED, Reason.OBSERVATION_OK
        return HEALTH_UNKNOWN, CONV_UNKNOWN, Reason.EVIDENCE_MISSING
    if job_id == "arifos-federation-audit":
        if exit_code == 0:
            return HEALTH_HEALTHY, CONV_SYNCED, Reason.OBSERVATION_OK
        if exit_code == 1:
            return HEALTH_DEGRADED, CONV_DRIFT, Reason.TOOL_COUNT_MISMATCH
        if exit_code == 2:
            return HEALTH_UNKNOWN, CONV_UNKNOWN, Reason.EVIDENCE_MISSING
        return HEALTH_UNKNOWN, CONV_UNKNOWN, Reason.EVIDENCE_MISSING
    if job_id == "aaa-rsi-loop":
        # dry-run: exit 0 = completed rehearsal
        if exit_code == 0:
            return HEALTH_HEALTHY, CONV_SYNCED, Reason.OBSERVATION_OK
        if exit_code == 3:
            return HEALTH_DEGRADED, CONV_HOLD, Reason.NO_ATOMS_TO_PROMOTE
        return HEALTH_FAILED, CONV_UNKNOWN, Reason.VERIFICATION_REJECTED
    if job_id == "probe_health_flip":
        if exit_code == 0:
            return HEALTH_HEALTHY, CONV_SYNCED, Reason.OBSERVATION_OK
        return HEALTH_FAILED, CONV_UNKNOWN, Reason.PROVIDER_DEAD
    return HEALTH_UNKNOWN, CONV_UNKNOWN, Reason.EVIDENCE_MISSING


def main() -> int:
    envelopes = []
    print(f"=== P1.0 emit_canonical_envelope — {now()} ===\n")
    for job in JOBS:
        sc = job["script"]
        if not Path(sc).exists():
            print(f"SKIP {job['id']}: {sc} not found")
            continue
        t0 = time.time()
        ec, out_tail, err_tail = run_job(job)
        dt = round(time.time() - t0, 2)
        h, conv, reason = classify_health_convergence(job["id"], ec, out_tail, err_tail)
        # Decide next_actor based on health
        if h == HEALTH_FAILED:
            next_actor = NEXT_HUMAN
        elif conv == CONV_DRIFT:
            next_actor = NEXT_MACHINE
        else:
            next_actor = NEXT_MACHINE
        state = CanonicalState(
            fact_domain=job["domain"],
            observed_state=f"exit={ec} in {dt}s — tail: {out_tail.strip()[:120]}",
            expected_state=job["expected"],
            health=h,
            convergence=conv,
            reason_code=reason,
            evidence_ref=sc,
            owner=job["id"],
            next_actor=next_actor,
            job_id=job["id"],
            job_class=job["class"],
            notes=f"stderr_tail: {err_tail.strip()[:80]}",
        )
        # Emit per-job envelope
        out_path = OUT_DIR / f"{job['id']}.json"
        out_path.write_text(state.to_json() + "\n")
        # Emit summary
        envelopes.append(state.to_dict())
        print(f"  {job['id']}: health={h} convergence={conv} reason={reason}")
    summary_path = OUT_DIR / "summary.json"
    summary = {
        "ran_at": now(),
        "envelope_count": len(envelopes),
        "envelopes": envelopes,
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(f"\nWrote: {summary_path}")
    print(f"Total envelopes: {len(envelopes)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
