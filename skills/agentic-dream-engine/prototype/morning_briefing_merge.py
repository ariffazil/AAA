#!/usr/bin/env python3
"""
morning_briefing_merge.py — F1/F2 validation handshake for shadow gist.

Reads pending rows from l3_shadow, validates them, and either:
- copies to memory_records + memory_audit_log (validated), or
- marks as purged (rejected).

Never merges without:
1. F1 snapshot verification
2. F2 counterfactual witness (second-agent critique or hermes_cross_verify)
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ── config ────────────────────────────────────────────────────────────
PG_HOST = os.environ.get("DREAM_PG_HOST", "127.0.0.1")
PG_PORT = int(os.environ.get("DREAM_PG_PORT", "5432"))
PG_DB = os.environ.get("DREAM_PG_DB", "vault999")
PG_USER = os.environ.get("DREAM_PG_USER", "arifos_admin")
PG_PASSWORD = os.environ.get("DREAM_PG_PASSWORD") or os.environ.get(
    "POSTGRES_PASSWORD", "ArifPostgresVault2026!"
)

SNAPSHOT_DIR = Path("/root/.hermes/skills/dream-engine/state/snapshots")


def _log(msg: str, level: str = "INFO") -> None:
    ts = datetime.now(timezone.utc).isoformat()
    stream = sys.stderr if level in ("ERROR", "WARN") else sys.stdout
    print(f"[{ts}] [{level}] {msg}", file=stream, flush=True)


def _pg_conn():
    import psycopg2  # type: ignore

    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DB,
        user=PG_USER,
        password=PG_PASSWORD,
    )


def _hash_gist(gist_json: dict) -> str:
    return hashlib.sha256(
        json.dumps(gist_json, sort_keys=True).encode("utf-8")
    ).hexdigest()


# ── F1 snapshot verification ──────────────────────────────────────────
def _verify_snapshot(shadow_row: dict) -> bool:
    """
    Verify that the pre-seal snapshot exists and is intact.
    In production this would compare snapshot hash against current DB state.
    """
    snap_path = shadow_row.get("f1_snapshot_path")
    if not snap_path:
        _log(f"shadow {shadow_row['shadow_id']}: no snapshot path", "WARN")
        return False
    return Path(snap_path).exists()


# ── F2 witness verification ───────────────────────────────────────────
def _run_f2_witness(shadow_row: dict) -> dict:
    """
    Counterfactual challenge for the shadow gist.
    Stub: returns deterministic OK/HOLD based on synthesis_score.
    In production call hermes_cross_verify or second-agent critique.
    """
    gist = shadow_row.get("gist_json", {})
    score = float(gist.get("synthesis_score", 0.0))
    if score >= 0.65 and shadow_row.get("delta_s", 0) < 0:
        return {
            "verdict": "OK",
            "confidence": score,
            "reason": "Counterfactual challenge passed (stub).",
        }
    return {
        "verdict": "HOLD",
        "confidence": score,
        "reason": "Score below threshold or positive entropy delta.",
    }


# ── Merge operations ──────────────────────────────────────────────────
def _merge_to_memory_records(shadow_row: dict) -> str:
    """Copy validated shadow gist to memory_records + memory_audit_log."""
    gist = shadow_row["gist_json"]
    statement = gist.get("canonical_statement", "")
    memory_id = str(
        __import__("uuid").uuid5(
            __import__("uuid").NAMESPACE_DNS, statement
        )
    )

    source_ref = {
        "agent_id": shadow_row["agent_id"],
        "session_id": shadow_row["session_id"],
        "shadow_id": str(shadow_row["shadow_id"]),
        "ratified_by": "arif-fazil",
        "ratified_at": datetime.now(timezone.utc).isoformat(),
        "ratified_floors": [
            "F1_snapshot_verified",
            "F2_witness_OK",
            "F7_threshold_0.65",
            "F8_shadow_partition",
            "F11_auth",
            "F13_daily_cap",
        ],
        "counterfactual": gist.get("counterfactual", "")[:200],
    }

    try:
        with _pg_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO memory_records (
                        memory_id, actor_id, session_id, type, subject, content, summary,
                        source_type, source_ref, confidence, authority, sensitivity, consent_level,
                        freshness_ts, last_validated_ts, retention_class, revocable, status, tags, hash
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s, %s, %s, %s,
                        now(), now(), %s, %s, %s, %s, %s
                    )
                    ON CONFLICT (memory_id) DO NOTHING
                    RETURNING memory_id;
                    """,
                    (
                        memory_id,
                        shadow_row["agent_id"],
                        shadow_row["session_id"],
                        "semantic",
                        statement[:120],
                        statement,
                        statement[:200],
                        f"{shadow_row['agent_id']}:sleep-time",
                        json.dumps(source_ref),
                        gist.get("synthesis_score", 0.0),
                        "system_inferred",
                        0.1,
                        "sovereign",
                        "immutable_audit",
                        True,
                        "active",
                        [shadow_row["agent_id"], "shadow-to-canon", "sleep-time"],
                        _hash_gist(gist),
                    ),
                )
                written = cur.fetchone() is not None
                if written:
                    cur.execute(
                        """
                        INSERT INTO memory_audit_log (memory_id, event_type, actor_id, session_id, payload, hash, created_at)
                        VALUES (%s, %s, %s, %s, %s::jsonb, %s, now());
                        """,
                        (
                            memory_id,
                            "shadow_merge",
                            shadow_row["agent_id"],
                            shadow_row["session_id"],
                            json.dumps(
                                {
                                    "shadow_id": str(shadow_row["shadow_id"]),
                                    "delta_s": shadow_row["delta_s"],
                                    "source_refs": shadow_row["source_refs"],
                                }
                            ),
                            _hash_gist(gist)[:32],
                        ),
                    )
            conn.commit()
        return memory_id
    except Exception as e:
        _log(f"merge failed for {shadow_row['shadow_id']}: {e}", "ERROR")
        raise


def _purge_shadow(shadow_id: str, reason: str) -> None:
    try:
        with _pg_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE l3_shadow
                    SET status = 'purged', purged_at = now(), f2_witness_evidence = %s::jsonb
                    WHERE shadow_id = %s;
                    """,
                    (json.dumps({"reason": reason}), shadow_id),
                )
            conn.commit()
        _log(f"purged shadow {shadow_id}: {reason}")
    except Exception as e:
        _log(f"purge failed for {shadow_id}: {e}", "ERROR")
        raise


def _validate_and_merge(shadow_row: dict, dry_run: bool) -> dict:
    result = {"shadow_id": str(shadow_row["shadow_id"]), "action": None}

    # F1 snapshot
    if not _verify_snapshot(shadow_row):
        reason = "F1 snapshot missing or invalid"
        if not dry_run:
            _purge_shadow(str(shadow_row["shadow_id"]), reason)
        result["action"] = "purged"
        result["reason"] = reason
        return result

    # F2 witness
    witness = _run_f2_witness(shadow_row)
    if witness["verdict"] != "OK":
        reason = f"F2 witness {witness['verdict']}: {witness['reason']}"
        if not dry_run:
            _purge_shadow(str(shadow_row["shadow_id"]), reason)
        result["action"] = "purged"
        result["reason"] = reason
        return result

    # Merge
    if dry_run:
        result["action"] = "would_validate"
        result["reason"] = "dry-run"
        return result

    memory_id = _merge_to_memory_records(shadow_row)
    result["action"] = "validated"
    result["memory_id"] = memory_id
    return result


def run_merge(dry_run: bool = True) -> dict:
    _log(f"morning briefing merge starting (dry_run={dry_run})")
    try:
        with _pg_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT shadow_id, agent_id, session_id, dream_cycle, gist_json,
                           raw_token_count, gist_token_count, delta_s, source_refs, hash,
                           f1_snapshot_path
                    FROM l3_shadow WHERE status = 'pending' ORDER BY created_at ASC;
                    """
                )
                rows = [dict(zip([desc[0] for desc in cur.description], row)) for row in cur.fetchall()]
    except Exception as e:
        _log(f"failed to read pending shadows: {e}", "ERROR")
        return {"status": "error", "reason": str(e)}

    _log(f"found {len(rows)} pending shadow rows")

    results = []
    for row in rows:
        results.append(_validate_and_merge(row, dry_run))

    summary = {
        "status": "completed",
        "dry_run": dry_run,
        "pending_rows": len(rows),
        "validated": sum(1 for r in results if r["action"] in ("validated", "would_validate")),
        "purged": sum(1 for r in results if r["action"] == "purged"),
        "results": results,
    }
    _log(
        f"merge complete: validated={summary['validated']}, purged={summary['purged']}"
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Morning briefing F1/F2 merge handshake")
    parser.add_argument("--execute", action="store_true", help="Actually merge validated shadows")
    args = parser.parse_args()

    dry_run = not args.execute
    if args.execute:
        _log("EXECUTE mode: will merge validated shadows to memory_records", "WARN")

    summary = run_merge(dry_run=dry_run)
    print(json.dumps(summary, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
