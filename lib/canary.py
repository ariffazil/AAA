"""canary.py — P2 generic behavioral canary primitive.

Per F13 directive 2026-09-21:
    "Build ONE generic behavioral-canary primitive. Don't make 24 bespoke scripts."

Contract:
    CANARY(service, candidate_env)

    1. capture baseline
    2. instantiate candidate
    3. start isolated/canary instance if possible
    4. execute service-specific capability probes
    5. compare baseline ↔ candidate
    6. observe for bounded window
    7. PASS → eligible_for_promotion
    8. FAIL → automatic rollback
    9. leave receipt

Each service supplies only:
    START_CONDITION          # how to start the service
    CRITICAL_PROBES          # list of probes that exercise real capability
    SUCCESS_RULES            # how to decide "still works"
    FAILURE_RULES            # how to decide "broken"
    ROLLBACK_ACTION          # how to revert the slice
    OBSERVATION_WINDOW       # how long to observe

Infrastructure stays shared.

DITEMPA BUKAN DIBERI ⚒️
"""

from __future__ import annotations
import json
import os
import shutil
import subprocess
import time
import traceback
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


RECEIPTS_DIR = Path("/root/forge_work/canary-receipts")
RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)


# ── Service contract ────────────────────────────────────────────────

@dataclass
class Probe:
    """One concrete capability probe."""
    name: str
    fn: Callable[[], dict]                # returns {"ok": bool, "evidence": str, "metrics": {...}}
    weight: float = 1.0                    # for overall score
    timeout_s: int = 30


@dataclass
class CanaryContract:
    """What a service must declare to be canary-tested."""
    service: str
    description: str
    start_condition: Callable[[], dict]     # returns {"ok": bool, "instance_id": str, ...}
    critical_probes: list[Probe]
    success_rules: Callable[[list[dict]], bool]
    failure_rules: Callable[[list[dict]], bool]   # takes precedence over success
    rollback_action: Callable[[str], dict]   # takes "reason", returns {"ok": bool, "actions": [...]}
    observation_window_s: int = 30          # how long to observe after canary start


# ── Result types ────────────────────────────────────────────────────

@dataclass
class CanaryResult:
    service: str
    verdict: str   # PASS / FAIL / INCONCLUSIVE / SKIPPED
    baseline_captured: dict
    candidate_observed: dict
    probe_results: list[dict]
    elapsed_s: float
    receipt_path: str
    notes: list[str] = field(default_factory=list)


# ── Public API ──────────────────────────────────────────────────────

def canary(contract: CanaryContract, candidate_env_path: str | os.PathLike | None = None) -> CanaryResult:
    """Run a full canary cycle for one service against an optional candidate env file.

    Args:
        contract: the service-specific contract
        candidate_env_path: optional path to candidate minimal env (None = use current)

    Returns:
        CanaryResult with verdict + receipt path
    """
    t0 = time.time()
    notes: list[str] = []
    probe_results: list[dict] = []

    # 1. Capture baseline
    print(f"[canary] {contract.service}: capturing baseline")
    try:
        baseline = contract.start_condition()
        if not baseline.get("ok"):
            notes.append(f"baseline start failed: {baseline.get('error', '?')}")
            return _emit_result(contract, "SKIPPED", baseline, {}, probe_results, t0, notes)
    except Exception as e:
        notes.append(f"baseline start exception: {e}")
        return _emit_result(contract, "SKIPPED", {}, {}, probe_results, t0, notes)

    # 2. Probe baseline (these probes should currently PASS)
    print(f"[canary] {contract.service}: probing baseline")
    baseline_probes = _run_probes(contract.critical_probes)
    probe_results.append({"phase": "baseline", "results": baseline_probes})

    # 3. Apply candidate env (if provided)
    if candidate_env_path:
        print(f"[canary] {contract.service}: applying candidate env at {candidate_env_path}")
        apply_result = _apply_candidate_env(contract, candidate_env_path)
        notes.append(f"apply: {apply_result}")

    # 4. Start candidate (in production this would be an isolated instance)
    print(f"[canary] {contract.service}: starting candidate")
    try:
        candidate_start = contract.start_condition()
        if not candidate_start.get("ok"):
            notes.append(f"candidate start failed: {candidate_start.get('error', '?')}")
            # Rollback
            rollback = contract.rollback_action("start_failed")
            notes.append(f"rollback: {rollback}")
            return _emit_result(contract, "FAIL", baseline, candidate_start, probe_results, t0, notes)
    except Exception as e:
        notes.append(f"candidate start exception: {e}")
        rollback = contract.rollback_action("start_exception")
        notes.append(f"rollback: {rollback}")
        return _emit_result(contract, "FAIL", baseline, {"error": str(e)}, probe_results, t0, notes)

    # 5. Observe for bounded window
    print(f"[canary] {contract.service}: observing for {contract.observation_window_s}s")
    time.sleep(min(contract.observation_window_s, 60))  # cap at 60s for safety in dev

    # 6. Probe candidate
    candidate_probes = _run_probes(contract.critical_probes)
    probe_results.append({"phase": "candidate", "results": candidate_probes})

    # 7. Decide
    verdict = _decide(contract, baseline_probes, candidate_probes, notes)
    print(f"[canary] {contract.service}: verdict={verdict}")

    # 8. Rollback or pass-through
    if verdict == "FAIL":
        print(f"[canary] {contract.service}: rolling back")
        rollback = contract.rollback_action("verdict_fail")
        notes.append(f"rollback: {rollback}")

    # 9. Receipt
    elapsed = round(time.time() - t0, 2)
    return _emit_result(contract, verdict, baseline, candidate_start, probe_results, t0, notes)


# ── Helpers ──────────────────────────────────────────────────────────

def _run_probes(probes: list[Probe]) -> list[dict]:
    results = []
    for probe in probes:
        t0 = time.time()
        try:
            res = probe.fn()
            elapsed = round(time.time() - t0, 2)
            results.append({
                "probe": probe.name,
                "ok": res.get("ok", False),
                "weight": probe.weight,
                "elapsed_s": elapsed,
                "evidence": res.get("evidence", "")[:300],
                "metrics": res.get("metrics", {}),
            })
        except subprocess.TimeoutExpired:
            results.append({"probe": probe.name, "ok": False, "weight": probe.weight, "error": "timeout"})
        except Exception as e:
            results.append({"probe": probe.name, "ok": False, "weight": probe.weight, "error": str(e)[:200]})
    return results


def _decide(contract: CanaryContract, baseline: list[dict], candidate: list[dict], notes: list[str]) -> str:
    # Failure rules take precedence
    if contract.failure_rules(candidate):
        return "FAIL"
    if not contract.success_rules(candidate):
        return "FAIL"
    # Compare baseline ↔ candidate
    base_pass = sum(p["weight"] for p in baseline if p.get("ok"))
    cand_pass = sum(p["weight"] for p in candidate if p.get("ok"))
    if cand_pass < base_pass * 0.9:  # 10% regression tolerance
        notes.append(f"score regression: baseline={base_pass} candidate={cand_pass}")
        return "FAIL"
    return "PASS"


def _apply_candidate_env(contract: CanaryContract, candidate_env_path: str | os.PathLike) -> dict:
    """Apply candidate env file. In production this would be on a canary instance only.
    This default implementation is NO-OP for safety (the canary infra doesn't yet
    have an isolated instance runner — that's pending work).

    Returns a marker dict describing what would happen.
    """
    p = Path(candidate_env_path)
    if not p.exists():
        return {"ok": False, "error": f"candidate env not found: {p}"}
    # Count keys (no values)
    keys = sum(1 for line in p.read_text(errors='ignore').splitlines()
               if '=' in line and not line.startswith('#'))
    return {
        "ok": True,
        "applied": False,  # NOT actually applied — pending isolated-instance runner
        "candidate_keys": keys,
        "candidate_path": str(p),
        "note": "candidate_env NOT actually applied in this dev cycle — pending isolated instance runner"
    }


def _emit_result(contract: CanaryContract, verdict: str,
                 baseline: dict, candidate: dict, probe_results: list[dict],
                 t0: float, notes: list[str]) -> CanaryResult:
    elapsed = round(time.time() - t0, 2)
    receipt = {
        "service": contract.service,
        "verdict": verdict,
        "elapsed_s": elapsed,
        "baseline": baseline,
        "candidate": candidate,
        "probe_results": probe_results,
        "notes": notes,
        "ran_at": datetime.now(timezone.utc).isoformat(),
    }
    fname = f"{contract.service}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    receipt_path = RECEIPTS_DIR / fname
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"[canary] {contract.service}: receipt at {receipt_path}")
    return CanaryResult(
        service=contract.service,
        verdict=verdict,
        baseline_captured=baseline,
        candidate_observed=candidate,
        probe_results=probe_results,
        elapsed_s=elapsed,
        receipt_path=str(receipt_path),
        notes=notes,
    )


# ── Helpers for writing contracts ────────────────────────────────────

def http_probe(url: str, expect_keys: list[str], timeout_s: int = 3, weight: float = 1.0) -> Probe:
    """Build an HTTP probe that checks /health (or any GET endpoint)."""
    import urllib.request

    def probe_fn() -> dict:
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=timeout_s) as resp:
                raw = resp.read().decode(errors='ignore')
                d = json.loads(raw)
            missing = [k for k in expect_keys if k not in d]
            return {
                "ok": not missing,
                "evidence": f"GET {url} → status={resp.status}, missing_keys={missing or 'none'}",
                "metrics": {"status_code": resp.status, "missing": missing},
            }
        except Exception as e:
            return {"ok": False, "evidence": f"GET {url} → exception: {e}", "metrics": {}}

    return Probe(name=f"http_{url}", fn=probe_fn, weight=weight, timeout_s=timeout_s)


def process_probe(service: str, weight: float = 0.5) -> Probe:
    """Probe whether a systemd service has a non-zero MainPID."""
    def probe_fn() -> dict:
        try:
            out = subprocess.check_output(
                ["systemctl", "show", "-p", "MainPID", "--value", service],
                text=True, timeout=3,
            ).strip()
            pid = int(out) if out.isdigit() else 0
            return {
                "ok": pid > 0,
                "evidence": f"systemctl MainPID={out}",
                "metrics": {"pid": pid},
            }
        except Exception as e:
            return {"ok": False, "evidence": f"systemctl exception: {e}", "metrics": {}}

    return Probe(name=f"process_{service}", fn=probe_fn, weight=weight, timeout_s=5)


def always_pass_rules(candidate_results: list[dict]) -> bool:
    """Default success rule: every probe must pass."""
    return all(r.get("ok") for r in candidate_results)


def critical_failure_rules(candidate_results: list[dict]) -> bool:
    """Default failure rule: any probe that timed out or exceptioned fails the canary."""
    for r in candidate_results:
        if "error" in r and r.get("error") in ("timeout", "exception"):
            return True
        if r.get("weight", 1.0) >= 1.0 and not r.get("ok"):
            return True
    return False


def noop_rollback(reason: str) -> dict:
    """Default rollback action: log only, no action.
    In production this would revert systemd unit + restart.
    Pending isolated instance runner.
    """
    return {"ok": True, "reason": reason, "actions": ["noop (pending isolated instance runner)"]}
