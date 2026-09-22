#!/usr/bin/env python3
"""
fed_health_set.py — canonical witnessed health writer (FED Truth Layer v1)

TRUTH LAYER CONSTITUTION (2026-09-22, F13 verdict "Forge the FED Truth Layer"):
    Health cannot exist without evidence.
    Every route_health write MUST carry a witness — how this was known.

    fed_health_set.py PROVIDER MODEL STATUS [NOTE] \\
        --witness chat_completion|models_get|agent_report|direct_canary \\
        [--latency-ms N] [--evidence TEXT] [--receipt REF]

Prior SCAR-context (Phase 0 fix #1, 2026-09-07): probes historically wrote
findings into providers.notes only; router kept rendering LIVE.
SCAR-context v1 (2026-09-22): GET /models 200 while chat 402 — liveness
without witness is a lie class of its own (SCAR-001). Fail-closed: a write
without a witness is REFUSED. Failure statuses are witnessed facts too —
the failure IS the evidence.

Failure classes auto-append to the scar registry
(/root/AAA/federation/provider-failure-patterns/scar_events.jsonl).
"""
import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, timezone

FED_STATE_DB = "/root/.local/share/arifos/token_bank.db"
SCAR_EVENTS = "/root/AAA/federation/provider-failure-patterns/scar_events.jsonl"
VALID_STATUS = {"LIVE", "DEGRADED", "RATE_LIMITED", "DEAD", "AUTH_FAIL",
                "PAYMENT_REQUIRED", "UNREACHABLE"}
VALID_WITNESS = {"chat_completion", "models_get", "agent_report", "direct_canary"}


def _scar_class(status: str, evidence: str) -> str | None:
    e = (evidence or "").lower()
    if "400" in e or "model not" in e or "unsupported" in e:
        return "SCAR-002"          # retired/unknown model name
    if status == "PAYMENT_REQUIRED" or "402" in e or "insufficient balance" in e:
        return "SCAR-003"          # telemetry-overconfidence / money gate
    if status in {"DEAD", "AUTH_FAIL", "RATE_LIMITED", "UNREACHABLE", "DEGRADED"}:
        return "SCAR-001"          # declared-liveness divergence class
    return None


def main() -> int:
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("provider")
    ap.add_argument("model")
    ap.add_argument("status")
    ap.add_argument("note", nargs="?", default="")
    ap.add_argument("--witness", choices=sorted(VALID_WITNESS), default=None)
    ap.add_argument("--latency-ms", type=int, default=None)
    ap.add_argument("--evidence", default="")
    ap.add_argument("--receipt", default="")
    ap.add_argument("--witness-class", choices=["liveness","capability","quality"], default=None)
    ap.add_argument("--score", type=float, default=None, help="0..1 quality score (quality-class witnesses)")
    a = ap.parse_args()

    status = a.status.upper()
    if status not in VALID_STATUS:
        print(f"FAIL-CLOSED: status must be one of {sorted(VALID_STATUS)}, got {status}")
        return 2
    if not a.witness:
        print("FAIL-CLOSED [Truth Layer]: health requires witness. "
              "Pass --witness chat_completion|models_get|agent_report|direct_canary "
              "plus --evidence (the failure or success IS the evidence).")
        return 2

    now = datetime.now(timezone.utc).isoformat()
    wclass = a.witness_class or ("liveness")
    receipt = a.receipt or f"fed-health:{now}#{a.provider}/{a.model}"
    evidence = a.evidence or (f"status={status}" + (f" note={a.note}" if a.note else ""))

    with sqlite3.connect(FED_STATE_DB) as conn:
        conn.execute(
            """INSERT INTO route_health
               (provider_name, model_id, status, last_checked,
                witness_type, witness_time, witness_latency_ms, witness_evidence, witness_receipt, witness_freshness, witness_class, witness_score)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'FRESH', ?, ?)
               ON CONFLICT(provider_name, model_id) DO UPDATE SET
                 status=excluded.status, last_checked=excluded.last_checked,
                 witness_type=excluded.witness_type, witness_time=excluded.witness_time,
                 witness_latency_ms=excluded.witness_latency_ms,
                 witness_evidence=excluded.witness_evidence,
                 witness_receipt=excluded.witness_receipt, witness_freshness='FRESH', witness_class=excluded.witness_class, witness_score=excluded.witness_score""",
            (a.provider, a.model, status, now, a.witness, now,
             a.latency_ms, evidence, receipt, wclass, a.score),
        )
        stamp = f"PROBED_{now[:10]}: {status} [witness={a.witness} {evidence[:80]}]"
        conn.execute(
            "UPDATE providers SET notes = COALESCE(notes,'') || ' | ' || ? WHERE provider_name = ?",
            (stamp, a.provider),
        )
        scar = _scar_class(status, evidence)
        if scar:
            try:
                os.makedirs(os.path.dirname(SCAR_EVENTS), exist_ok=True)
                with open(SCAR_EVENTS, "a", encoding="utf-8") as fh:
                    fh.write(json.dumps({
                        "ts": now, "scar_id": scar, "provider": a.provider,
                        "model": a.model, "status": status, "evidence": evidence[:300],
                        "witness": a.witness, "receipt": receipt,
                    }) + "\n")
            except OSError:
                pass
    print(f"OK WITNESSED: route_health[{a.provider}/{a.model}]={status} "
          f"witness={a.witness} receipt={receipt}" + (f" scar={scar}" if scar else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
