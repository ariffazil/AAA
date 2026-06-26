#!/usr/bin/env python3
"""AAA STOP-SEAL — Session-level entropy trend + telemetry seal."""
from __future__ import annotations

import json
import socket
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import hook_lib as h


def main() -> None:
    event = h.read_event()
    session_id = event.get("session_id", "unknown")
    cwd = event.get("cwd", "/root")
    hook_event = event.get("hook_event_name", "Stop")
    if event.get("stop_hook_active"):
        return

    epoch = int(__import__("time").time())

    session_events = 0
    high_risk = 0
    hold_count = 0
    tier_a = 0
    cross_repo = 0
    pre_deltas: list[float] = []
    post_deltas: list[float] = []

    try:
        if h.AUDIT_LOG.exists():
            with h.AUDIT_LOG.open() as f:
                for line in f:
                    try:
                        rec = json.loads(line)
                        if rec.get("session_id") != session_id:
                            continue
                        session_events += 1
                        if rec.get("risk_class") in ("high", "irreversible") or rec.get("chaos_band") == "red":
                            high_risk += 1
                        if rec.get("hold_recommended"):
                            hold_count += 1
                        if rec.get("tier_a_touch"):
                            tier_a += 1
                        if rec.get("scope_guess") == "cross-repo" or rec.get("cross_domain"):
                            cross_repo += 1
                        if rec.get("type") == "opencode-thermo-pre" and "deltaS_projected" in rec:
                            pre_deltas.append(float(rec["deltaS_projected"]))
                        if rec.get("type") == "opencode-thermo-post" and "deltaS_realized" in rec:
                            post_deltas.append(float(rec["deltaS_realized"]))
                    except Exception:
                        pass
    except Exception:
        pass

    all_deltas = pre_deltas + post_deltas
    max_delta = max(all_deltas) if all_deltas else 0.0
    avg_delta = round(sum(all_deltas) / len(all_deltas), 4) if all_deltas else 0.0

    dirty_repos: list[str] = []
    for repo in ("arifOS", "A-FORGE", "geox", "WEALTH"):
        p = Path(f"/root/{repo}/.git")
        if not p.exists():
            continue
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=f"/root/{repo}",
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.stdout.strip():
                dirty_repos.append(repo)
        except Exception:
            pass

    bg_tasks_running = False
    # Best-effort: we cannot see other sessions' tasks from here.

    chaos_trend = "stable"
    if avg_delta < 0.25:
        chaos_trend = "stable"
    elif avg_delta < 0.55:
        chaos_trend = "warming"
    elif avg_delta < 0.80:
        chaos_trend = "hot"
    else:
        chaos_trend = "redline"

    rollback_coverage = "unknown"
    if session_events > 0:
        try:
            if h.AUDIT_LOG.exists():
                with h.AUDIT_LOG.open() as f:
                    for line in f:
                        try:
                            rec = json.loads(line)
                            if rec.get("session_id") == session_id and rec.get("rollback_detected"):
                                rollback_coverage = "present"
                                break
                        except Exception:
                            pass
            if rollback_coverage == "unknown":
                rollback_coverage = "missing"
        except Exception:
            pass

    unresolved: list[str] = []
    if dirty_repos:
        unresolved.append(f"Dirty repos: {' '.join(dirty_repos)}")
    if rollback_coverage == "missing" and high_risk > 0:
        unresolved.append("High-risk actions with no rollback coverage")
    if max_delta > 0.80:
        unresolved.append(f"Max entropy spike exceeded redline ({max_delta})")

    if chaos_trend == "redline" or high_risk > 2:
        verdict = "REDLINE"
    elif chaos_trend == "hot" or len(unresolved) > 2:
        verdict = "DEGRADED"
    elif unresolved:
        verdict = "STABLE_WITH_WARNINGS"
    else:
        verdict = "STABLE"

    seal = {
        "type": "opencode-stop-seal",
        "timestamp": h.now_utc(),
        "session_id": session_id,
        "epoch": epoch,
        "thermodynamics": {
            "dS_session_avg": avg_delta,
            "dS_session_max": max_delta,
            "chaos_trend": chaos_trend,
            "rollback_coverage": rollback_coverage,
        },
        "telemetry": {
            "session_events": session_events,
            "high_risk_actions": high_risk,
            "hold_recommended_count": hold_count,
            "tier_a_touches": tier_a,
            "cross_repo_touches": cross_repo,
            "background_tasks_running": bg_tasks_running,
        },
        "dirty_repos": dirty_repos,
        "unresolved_warnings": unresolved,
        "verdict": verdict,
        "seal_note": "Session closed with full thermodynamic telemetry.",
    }

    h.audit_log(seal)
    seal_file = h.TELEMETRY_DIR / f"seal-{session_id}.jsonl"
    with seal_file.open("a") as f:
        f.write(json.dumps(seal) + "\n")

    reason = (
        f"[CLAIM] AAA StopSeal: VERDICT={verdict} | avgΔS={avg_delta} maxΔS={max_delta} "
        f"trend={chaos_trend} rollback={rollback_coverage} | Events={session_events} "
        f"HighRisk={high_risk} HoldRec={hold_count} TierA={tier_a} CrossRepo={cross_repo}"
    )
    if unresolved:
        reason += " | UNRESOLVED: " + "; ".join(unresolved)

    h.allow(
        hook_event,
        reason,
        {
            "seal_verdict": verdict,
            "dS_session_avg": avg_delta,
            "dS_session_max": max_delta,
            "chaos_trend": chaos_trend,
            "rollback_coverage": rollback_coverage,
            "session_events": session_events,
            "high_risk_actions": high_risk,
            "hold_recommended_count": hold_count,
            "tier_a_touches": tier_a,
            "cross_repo_touches": cross_repo,
            "background_tasks_running": bg_tasks_running,
            "dirty_repos": dirty_repos,
        },
    )


if __name__ == "__main__":
    main()
