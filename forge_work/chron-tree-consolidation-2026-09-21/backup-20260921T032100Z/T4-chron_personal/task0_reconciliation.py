#!/usr/bin/env python3
"""CHRON Task 0 — Declared vs Observed Reconciliation.

Daily reconciliation of:
  - jobs.json declared jobs vs executions.db actual fires
  - Provider pin (model/provider) vs runtime reality
  - Delivery claims vs delivery receipts
  - Systemd timers (morning briefing, NIAT) vs journal evidence

Output: ChronEpisode v0 with reconciliation results.
Written to: /root/.hermes/cron/state/chron_personal/

This is the first arrow to close: OUTCOME → MEMORY.
Without this, prediction learning rests on false reality.

DITEMPA BUKAN DIBERI.
"""

from __future__ import annotations

import json
import os
import sqlite3
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

MYT = timezone(timedelta(hours=8))
STATE_DIR = Path("/root/.hermes/cron/state/chron_personal")
JOBS_FILE = Path("/root/.hermes/cron/jobs.json")
EXECUTIONS_DB = Path("/root/.hermes/cron/executions.db")
DELIVERIES_DB = Path("/root/.hermes/cron/deliveries.db")
OUTPUT_FILE = STATE_DIR / "task0_latest.json"

# ChronEpisode v0 schema
EPISODE_SCHEMA = "chron_episode_v0"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def now_myt() -> datetime:
    return datetime.now(MYT)


def today_str() -> str:
    return now_myt().strftime("%Y-%m-%d")


def today_start_utc() -> str:
    """Start of today in UTC for DB queries."""
    midnight_myt = now_myt().replace(hour=0, minute=0, second=0, microsecond=0)
    return midnight_myt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


# ───────────────────────── DECLARED STATE ─────────────────────────

def load_declared_jobs() -> list[dict]:
    """Load jobs from jobs.json."""
    try:
        data = json.loads(JOBS_FILE.read_text())
        jobs = data.get("jobs", data) if isinstance(data, dict) else data
        return jobs if isinstance(jobs, list) else []
    except Exception:
        return []


def classify_declared(jobs: list[dict]) -> dict:
    """Classify declared jobs into enabled/disabled/unknown."""
    enabled = []
    disabled = []
    for j in jobs:
        entry = {
            "id": j.get("id", "?"),
            "name": j.get("name", "?"),
            "schedule": j.get("schedule", {}).get("expr", "?"),
            "model": j.get("model"),
            "provider": j.get("provider"),
            "deliver": j.get("deliver"),
            "state": j.get("state"),
            "last_run_at": j.get("last_run_at"),
        }
        if j.get("enabled", False):
            enabled.append(entry)
        else:
            disabled.append(entry)
    return {"enabled": enabled, "disabled": disabled}


# ───────────────────────── OBSERVED STATE ─────────────────────────

def load_executions_today() -> list[dict]:
    """Load today's executions from executions.db."""
    if not EXECUTIONS_DB.exists():
        return []
    try:
        conn = sqlite3.connect(str(EXECUTIONS_DB))
        conn.row_factory = sqlite3.Row
        cutoff = today_start_utc()
        rows = conn.execute(
            """SELECT id, job_id, source, status, claimed_at, started_at,
                      finished_at, error, delivery_outcome, scheduled_instant
               FROM executions
               WHERE claimed_at >= ?
               ORDER BY claimed_at DESC""",
            (cutoff,),
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception:
        return []


def load_deliveries_today() -> list[dict]:
    """Load today's deliveries from deliveries.db."""
    if not DELIVERIES_DB.exists():
        return []
    try:
        conn = sqlite3.connect(str(DELIVERIES_DB))
        conn.row_factory = sqlite3.Row
        cutoff = today_start_utc()
        rows = conn.execute(
            """SELECT execution_id, status, created_at, finished_at, error
               FROM deliveries
               WHERE created_at >= ?
               ORDER BY created_at DESC""",
            (cutoff,),
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception:
        return []


# ───────────────────────── SYSTEMD TIMERS ─────────────────────────

def check_systemd_timer(name: str) -> dict:
    """Check a systemd timer's last trigger time."""
    try:
        result = subprocess.run(
            ["systemctl", "show", name, "--property=ActiveEnterTimestamp,Result"],
            capture_output=True, text=True, timeout=5,
        )
        props = {}
        for line in result.stdout.strip().splitlines():
            if "=" in line:
                k, v = line.split("=", 1)
                props[k.strip()] = v.strip()
        return {
            "name": name,
            "last_trigger": props.get("ActiveEnterTimestamp", "unknown"),
            "result": props.get("Result", "unknown"),
        }
    except Exception:
        return {"name": name, "last_trigger": "unreachable", "result": "unknown"}


# ───────────────────────── RECONCILIATION ─────────────────────────

def reconcile(declared: dict, executions: list, deliveries: list) -> dict:
    """Compare declared vs observed. Returns reconciliation results."""
    today = today_str()

    # Build lookup of declared job IDs
    declared_ids = {j["id"] for j in declared["enabled"]}
    declared_names = {j["name"]: j for j in declared["enabled"]}
    all_declared_ids = {j["id"] for j in declared["enabled"] + declared["disabled"]}

    # Build lookup of executed job IDs today
    executed_ids = {e["job_id"] for e in executions}
    completed_ids = {e["job_id"] for e in executions if e["status"] == "completed"}
    failed_ids = {e["job_id"] for e in executions if e["status"] == "failed"}
    delivered_exec_ids = {d["execution_id"] for d in deliveries if d["status"] == "delivered"}

    # 1. Fires vs declared
    fired_not_declared = executed_ids - all_declared_ids
    declared_not_fired = declared_ids - executed_ids

    # 2. Provider pin drift
    provider_drift = []
    for exe in executions:
        job_id = exe["job_id"]
        declared_job = next(
            (j for j in declared["enabled"] + declared["disabled"] if j["id"] == job_id), None
        )
        if declared_job:
            declared_model = declared_job.get("model")
            declared_provider = declared_job.get("provider")
            if declared_model and exe.get("source") == "builtin":
                # builtin source = Hermes cron dispatched it
                # We can't easily get the actual model used, but we can flag the pin
                provider_drift.append({
                    "job_id": job_id,
                    "job_name": declared_job.get("name", "?"),
                    "declared_model": declared_model,
                    "declared_provider": declared_provider,
                    "note": "provider pin present but runtime model not directly observable from executions.db",
                })

    # 3. Delivery claims vs receipts
    delivery_mismatches = []
    for exe in executions:
        if exe["status"] == "completed":
            has_delivery = exe["id"] in delivered_exec_ids
            delivery_outcome = exe.get("delivery_outcome")
            if delivery_outcome == "delivered" and not has_delivery:
                delivery_mismatches.append({
                    "execution_id": exe["id"],
                    "job_id": exe["job_id"],
                    "issue": "claims delivered but no delivery receipt",
                })
            elif delivery_outcome == "suppressed" and has_delivery:
                delivery_mismatches.append({
                    "execution_id": exe["id"],
                    "job_id": exe["job_id"],
                    "issue": "claims suppressed but delivery record exists",
                })

    # 4. Systemd timer checks
    timer_checks = [
        check_systemd_timer("arifos-morning-briefing.timer"),
        check_systemd_timer("arifos-niat-loop-picker.timer"),
        check_systemd_timer("arifos-niat-executor.timer"),
    ]

    # 5. Summary
    total_executions = len(executions)
    total_completed = len(completed_ids)
    total_failed = len(failed_ids)
    total_delivered = len(delivered_exec_ids)

    findings = []
    severity = "CLEAN"

    if fired_not_declared:
        findings.append({
            "type": "DRIFT",
            "severity": "CRITICAL",
            "description": f"Jobs fired but absent from jobs.json: {fired_not_declared}",
        })
        severity = "CRITICAL"

    if declared_not_fired:
        findings.append({
            "type": "INERTIA",
            "severity": "INFO",
            "description": f"Enabled jobs that did not fire today (may be weekly/monthly): {declared_not_fired}",
        })

    if delivery_mismatches:
        findings.append({
            "type": "DELIVERY_DRIFT",
            "severity": "HIGH",
            "description": f"Delivery claim/receipt mismatches: {len(delivery_mismatches)}",
            "details": delivery_mismatches[:3],
        })
        if severity != "CRITICAL":
            severity = "HIGH"

    for t in timer_checks:
        if t["result"] == "failed":
            findings.append({
                "type": "TIMER_FAILURE",
                "severity": "HIGH",
                "description": f"Systemd timer {t['name']} last result: failed",
            })

    return {
        "date": today,
        "observed_at": now_iso(),
        "summary": {
            "declared_enabled": len(declared["enabled"]),
            "declared_disabled": len(declared["disabled"]),
            "executions_today": total_executions,
            "completed_today": total_completed,
            "failed_today": total_failed,
            "delivered_today": total_delivered,
            "fired_not_declared": list(fired_not_declared),
            "declared_not_fired": list(declared_not_fired),
        },
        "provider_drift": provider_drift[:5],
        "delivery_mismatches": delivery_mismatches[:5],
        "timer_checks": timer_checks,
        "findings": findings,
        "overall_severity": severity,
    }


# ───────────────────────── EPISODE OUTPUT ─────────────────────────

def build_episode(reconciliation: dict) -> dict:
    """Build a ChronEpisode v0 from reconciliation results."""
    today = today_str()
    return {
        "$schema": EPISODE_SCHEMA,
        "version": "0.1.0",
        "episode_id": f"task0-{today}-{datetime.now(MYT).strftime('%H%M')}",
        "cycle_id": f"T0-{today}",
        "parent_episode_ids": [],
        "principal": "arif",
        "audience": "internal",
        "scope": "declared_vs_observed",

        "event_time": today,
        "observed_at": now_iso(),
        "known_at": now_iso(),

        "observations": [
            {
                "type": "declared_vs_observed",
                "declared_enabled": reconciliation["summary"]["declared_enabled"],
                "executions_today": reconciliation["summary"]["executions_today"],
                "fired_not_declared": reconciliation["summary"]["fired_not_declared"],
                "overall_severity": reconciliation["overall_severity"],
            }
        ],

        "claims": [
            {
                "claim": "jobs.json is the source of truth for dispatch",
                "truth_state": "CONTRADICTED" if reconciliation["summary"]["fired_not_declared"]
                    else "VERIFIED",
                "evidence": f"fired_not_declared={reconciliation['summary']['fired_not_declared']}",
            },
            {
                "claim": "model/provider pin matches runtime",
                "truth_state": "UNKNOWN",
                "evidence": "executions.db does not record actual model used",
            },
            {
                "claim": "delivery receipts match delivery claims",
                "truth_state": "CONTRADICTED" if reconciliation["delivery_mismatches"]
                    else "VERIFIED",
                "evidence": f"mismatches={len(reconciliation['delivery_mismatches'])}",
            },
        ],

        "predictions": [],
        "decisions": [],
        "actions": [],
        "outcomes": [],

        "human_self_reports": [],
        "machine_inferences": reconciliation["findings"],

        "confidence": 0.8,
        "claim_state": "OBSERVED",
        "privacy_scope": "internal",

        "corrections": [],
        "supersedes": [],

        "receipts": [],

        "_reconciliation": reconciliation,
    }


# ───────────────────────── PREDICTION INTEGRATION ─────────────────────────

def load_prediction_status() -> dict:
    """Load prediction store status for inclusion in episode."""
    pred_file = STATE_DIR / "predictions.json"
    if not pred_file.exists():
        return {"status": "NO_STORE", "active": 0, "verified": 0, "due": 0}
    try:
        data = json.loads(pred_file.read_text())
        preds = data.get("predictions", [])
        now = datetime.now(timezone.utc)
        active = [p for p in preds if p["state"] == "ACTIVE"]
        verified = [p for p in preds if p["state"] == "VERIFIED"]
        due = []
        for p in active:
            try:
                vat = datetime.fromisoformat(p["verify_at"].replace("Z", "+00:00"))
                if now >= vat:
                    due.append(p)
            except Exception:
                pass
        return {
            "status": "ACTIVE",
            "active": len(active),
            "verified": len(verified),
            "due": len(due),
            "accuracy": _calc_accuracy(verified),
            "due_predictions": [
                {"id": p["prediction_id"][:12], "claim": p["claim"][:60]}
                for p in due
            ],
        }
    except Exception:
        return {"status": "ERROR", "active": 0, "verified": 0, "due": 0}


def _calc_accuracy(verified: list[dict]) -> float | None:
    if not verified:
        return None
    correct = sum(1 for p in verified if p.get("error", 1) == 0)
    return correct / len(verified)


# ───────────────────────── MAIN ─────────────────────────

def main() -> int:
    STATE_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Load declared state
    jobs = load_declared_jobs()
    declared = classify_declared(jobs)

    # 2. Load observed state
    executions = load_executions_today()
    deliveries = load_deliveries_today()

    # 3. Reconcile
    reconciliation = reconcile(declared, executions, deliveries)

    # 4. Load prediction status
    prediction_status = load_prediction_status()

    # 5. Build ChronEpisode
    episode = build_episode(reconciliation)
    episode["_prediction_status"] = prediction_status

    # 6. Write output
    OUTPUT_FILE.write_text(json.dumps(episode, indent=2, default=str))

    # 7. Regenerate predictions from chron_events
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "prediction_store", str(Path(__file__).parent / "prediction_store.py"))
        ps = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ps)
        existing = ps.load_predictions()
        existing_ids = {p.get("source_id") for p in existing if p.get("source") == "chron_events"}
        new_preds = ps.generate_from_chron_events()
        added = 0
        for p in new_preds:
            if p["source_id"] not in existing_ids:
                existing.append(p)
                added += 1
        if added:
            ps.save_predictions(existing)
            print(f"  Predictions: +{added} new from chron_events")
    except Exception as e:
        print(f"  Predictions: generation skipped ({e})")

    # 8. Print summary
    print(f"CHRON Task 0 — {today_str()}")
    print(f"  Declared enabled: {reconciliation['summary']['declared_enabled']}")
    print(f"  Executions today: {reconciliation['summary']['executions_today']}")
    print(f"  Completed: {reconciliation['summary']['completed_today']}")
    print(f"  Failed: {reconciliation['summary']['failed_today']}")
    print(f"  Delivered: {reconciliation['summary']['delivered_today']}")
    print(f"  Fired but not declared: {reconciliation['summary']['fired_not_declared']}")
    print(f"  Severity: {reconciliation['overall_severity']}")
    print(f"  Predictions: {prediction_status['active']} active, {prediction_status['verified']} verified, {prediction_status['due']} due")
    if prediction_status.get("accuracy") is not None:
        print(f"  Calibration accuracy: {prediction_status['accuracy']:.2f}")
    for f in reconciliation["findings"]:
        print(f"  [{f['severity']}] {f['description']}")
    print(f"  Output: {OUTPUT_FILE}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
