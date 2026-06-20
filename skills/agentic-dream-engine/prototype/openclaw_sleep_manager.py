#!/usr/bin/env python3
"""
openclaw_sleep_manager.py — Prototype sleep-time compute daemon for OpenClaw.

Authority: OpenClaw AGI gateway sleep-time compute. Writes ONLY to l3_shadow.
Never touches primary memory_records or memory_embeddings.

Doctrine:
- F1 AMANAH: shadow-first writes; snapshot before any primary merge.
- F2 TRUTH: counterfactual + witness before merge (handled by morning_briefing_merge.py).
- F7 HUMILITY: synthesis_score capped and threshold-locked.
- F9 ANTIHANTU: mechanical language only; no consciousness claims.
- F13 SOVEREIGN: threshold/cap/cadence changes require Arif's ratification.

Default mode: dry_run=True. Use --execute only after 888_HOLD clearance.
"""

import argparse
import hashlib
import json
import os
import signal
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ── config ────────────────────────────────────────────────────────────
DEFAULT_CONFIG = {
    "agent_id": "openclaw:sleep-time",
    "trigger_window": "03:00",  # MYT, will be parsed
    "idle_threshold_minutes": 120,
    "epsilon": 1e-6,
    "llm_endpoint": "http://127.0.0.1:18789/v1/chat/completions",
    "llm_model": "minimax/MiniMax-M3",
    "shadow_table": "l3_shadow",
    "audit_table": "l3_shadow_audit",
    "lock_file": "/tmp/openclaw_sleep.lock",
    "max_llm_calls": 10,
}

PG_HOST = os.environ.get("DREAM_PG_HOST", "127.0.0.1")
PG_PORT = int(os.environ.get("DREAM_PG_PORT", "5432"))
PG_DB = os.environ.get("DREAM_PG_DB", "vault999")
PG_USER = os.environ.get("DREAM_PG_USER", "arifos_admin")
PG_PASSWORD = os.environ.get("DREAM_PG_PASSWORD") or os.environ.get(
    "POSTGRES_PASSWORD", "ArifPostgresVault2026!"
)

# ── globals ───────────────────────────────────────────────────────────
INTERRUPTED = False


def _handle_signal(signum, frame):
    global INTERRUPTED
    print(f"[sleep-manager] SIG {signum} received — suspending gracefully", file=sys.stderr)
    INTERRUPTED = True


signal.signal(signal.SIGTERM, _handle_signal)
signal.signal(signal.SIGINT, _handle_signal)


# ── logging ───────────────────────────────────────────────────────────
def _log(msg: str, level: str = "INFO") -> None:
    ts = datetime.now(timezone.utc).isoformat()
    stream = sys.stderr if level in ("ERROR", "WARN") else sys.stdout
    print(f"[{ts}] [{level}] {msg}", file=stream, flush=True)


# ── locks ─────────────────────────────────────────────────────────────
def _acquire_lock(path: str) -> bool:
    """Simple file mutex. Returns True if lock acquired."""
    lock = Path(path)
    if lock.exists():
        try:
            pid = int(lock.read_text().strip())
            if os.path.exists(f"/proc/{pid}"):
                _log(f"lock held by pid {pid}", "WARN")
                return False
        except Exception:
            pass
        lock.unlink(missing_ok=True)
    lock.write_text(str(os.getpid()))
    return True


def _release_lock(path: str) -> None:
    Path(path).unlink(missing_ok=True)


# ── DB helpers ────────────────────────────────────────────────────────
def _pg_conn():
    import psycopg2  # type: ignore

    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DB,
        user=PG_USER,
        password=PG_PASSWORD,
    )


def _audit(event_type: str, shadow_id: str | None, payload: dict, session_id: str) -> None:
    """Write an audit row. Fail-soft."""
    try:
        with _pg_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    INSERT INTO {DEFAULT_CONFIG['audit_table']}
                        (shadow_id, event_type, actor_id, session_id, payload)
                    VALUES (%s, %s, %s, %s, %s::jsonb)
                    """,
                    (
                        shadow_id,
                        event_type,
                        DEFAULT_CONFIG["agent_id"],
                        session_id,
                        json.dumps(payload, default=str),
                    ),
                )
            conn.commit()
    except Exception as e:
        _log(f"audit write failed (fail-soft): {e}", "WARN")


# ── Stage 1: State Monitor ────────────────────────────────────────────
def _is_in_trigger_window(now: datetime, window: str) -> bool:
    """Check if current time is within the scheduled nightly window."""
    hh, mm = map(int, window.split(":"))
    return now.hour == hh and now.minute == mm


def _last_888_activity() -> float:
    """
    Detect last sovereign activity. Stub: reads from a sentinel file or session DB.
    In production this should query OpenClaw's session/heartbeat table.
    """
    sentinel = Path("/tmp/openclaw_last_activity")
    if sentinel.exists():
        try:
            return float(sentinel.read_text().strip())
        except Exception:
            pass
    return 0.0


def _state_monitor(cfg: dict) -> dict:
    now = datetime.now(timezone.utc)
    last_activity = _last_888_activity()
    idle_min = (now.timestamp() - last_activity) / 60.0 if last_activity else float("inf")
    in_window = _is_in_trigger_window(now, cfg["trigger_window"])
    should_run = in_window and idle_min >= cfg["idle_threshold_minutes"]

    state = {
        "now": now.isoformat(),
        "trigger_window": cfg["trigger_window"],
        "idle_minutes": round(idle_min, 2),
        "idle_threshold": cfg["idle_threshold_minutes"],
        "in_window": in_window,
        "should_run": should_run,
    }
    _log(f"state monitor: idle={idle_min:.1f}min, in_window={in_window}, run={should_run}")
    return state


# ── Stage 2: L2 Ingress & Entropy Sorting ─────────────────────────────
def _fetch_l2_traces(since: datetime) -> list[dict]:
    """
    Fetch raw L2 episodic traces. Stub: returns synthetic demo data.
    In production this should read from OpenClaw's session/trajectory store.
    """
    _log(f"fetching L2 traces since {since.isoformat()}")
    # TODO: wire to real OpenClaw trajectory DB
    return [
        {
            "trace_id": "demo-1",
            "timestamp": since.isoformat(),
            "text": "888 asked OpenClaw to route a geoscience query to GEOX.",
            "tokens": 120,
        },
        {
            "trace_id": "demo-2",
            "timestamp": since.isoformat(),
            "text": "OpenClaw delegated a code fix to OpenCode; OpenCode returned a diff.",
            "tokens": 95,
        },
    ]


def _cluster_and_filter(traces: list[dict]) -> list[list[dict]]:
    """
    Lightweight semantic clustering. Stub: groups by simple keyword overlap.
    In production use Qdrant or pgvector clustering.
    """
    # Naive single cluster for prototype
    return [traces] if traces else []


# ── Stage 3: Offline EMD Metabolizer ──────────────────────────────────
def _call_llm(prompt: str, cfg: dict) -> dict | None:
    """Call LLM for gist extraction. Stub: returns deterministic demo output."""
    _log("LLM call stub — replace with real minimax/MiniMax-M3 call")
    return {
        "canonical_statement": "OpenClaw should route geoscience queries to GEOX before falling back to OpenCode.",
        "synthesis_score": 0.78,
        "counterfactual": "A non-geoscience query would be mis-routed to GEOX.",
        "gist": "Routing policy: geoscience → GEOX first; code tasks → OpenCode first.",
        "anticipatory_trees": [
            "If 888 asks about Malay Basin traps, pull GEOX basin profile first.",
            "If 888 asks about arifOS deployment, pull A-FORGE health first.",
        ],
    }


def _metabolize(cluster: list[dict], cfg: dict) -> dict | None:
    raw_tokens = sum(t.get("tokens", 0) for t in cluster)
    prompt = (
        "You are the OpenClaw sleep-time metabolizer. Compress these session traces "
        "into a dense semantic gist and 2-3 anticipatory reasoning trees. "
        "Return STRICT JSON: {canonical_statement, synthesis_score, counterfactual, gist, anticipatory_trees}.\n\n"
        + "\n---\n".join(t.get("text", "") for t in cluster)
    )
    result = _call_llm(prompt, cfg)
    if result is None:
        return None

    gist_tokens = len(result.get("gist", "").split()) + sum(
        len(x.split()) for x in result.get("anticipatory_trees", [])
    )
    delta_s = (gist_tokens - raw_tokens) / raw_tokens if raw_tokens else 0.0
    result["raw_token_count"] = raw_tokens
    result["gist_token_count"] = gist_tokens
    result["delta_s"] = delta_s
    result["cooled"] = delta_s < -cfg["epsilon"]
    return result


# ── Stage 4: Shadow Commit & Seal ─────────────────────────────────────
def _shadow_commit(
    cluster: list[dict],
    metabolized: dict,
    cfg: dict,
    dry_run: bool,
    session_id: str,
) -> dict:
    gist_json = {
        "canonical_statement": metabolized.get("canonical_statement"),
        "synthesis_score": metabolized.get("synthesis_score"),
        "counterfactual": metabolized.get("counterfactual"),
        "gist": metabolized.get("gist"),
        "anticipatory_trees": metabolized.get("anticipatory_trees", []),
    }
    payload_text = json.dumps(gist_json, sort_keys=True)
    h = hashlib.sha256(payload_text.encode()).hexdigest()

    record = {
        "agent_id": cfg["agent_id"],
        "session_id": session_id,
        "dream_cycle": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "gist_json": gist_json,
        "raw_token_count": metabolized["raw_token_count"],
        "gist_token_count": metabolized["gist_token_count"],
        "delta_s": metabolized["delta_s"],
        "source_refs": [t.get("trace_id") for t in cluster],
        "hash": h,
        "status": "pending",
    }

    if dry_run:
        _log("DRY-RUN: would shadow commit: " + json.dumps(record, default=str)[:300])
        return {**record, "shadow_id": "dry-run-uuid"}

    try:
        with _pg_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    INSERT INTO {cfg['shadow_table']}
                        (agent_id, session_id, dream_cycle, gist_json,
                         raw_token_count, gist_token_count, delta_s,
                         source_refs, hash, status)
                    VALUES (%s, %s, %s, %s::jsonb, %s, %s, %s, %s::jsonb, %s, %s)
                    RETURNING shadow_id;
                    """,
                    (
                        record["agent_id"],
                        record["session_id"],
                        record["dream_cycle"],
                        json.dumps(record["gist_json"]),
                        record["raw_token_count"],
                        record["gist_token_count"],
                        record["delta_s"],
                        json.dumps(record["source_refs"]),
                        record["hash"],
                        record["status"],
                    ),
                )
                shadow_id = str(cur.fetchone()[0])
            conn.commit()
        _audit("commit", shadow_id, {"delta_s": record["delta_s"], "hash": h}, session_id)
        _log(f"shadow committed: shadow_id={shadow_id}")
        return {**record, "shadow_id": shadow_id}
    except Exception as e:
        _log(f"shadow commit failed: {e}", "ERROR")
        raise


# ── orchestrator ──────────────────────────────────────────────────────
def run_cycle(cfg: dict, dry_run: bool = True) -> dict:
    session_id = f"openclaw-sleep-{datetime.now(timezone.utc).strftime('%Y-%m-%d')}"
    _log(f"starting sleep cycle session={session_id} dry_run={dry_run}")
    _audit("daemon_start", None, {"dry_run": dry_run}, session_id)

    # Stage 1
    state = _state_monitor(cfg)
    if not state["should_run"] and not dry_run:
        _log("sleep cycle skipped — not in window or user active")
        _audit("skip", None, state, session_id)
        return {"status": "skipped", "reason": state}

    if INTERRUPTED:
        _audit("suspend", None, {"stage": "after_state_monitor"}, session_id)
        return {"status": "suspended", "stage": "state_monitor"}

    # Stage 2
    since = datetime.now(timezone.utc)  # TODO: use last_cycle timestamp
    traces = _fetch_l2_traces(since)
    clusters = _cluster_and_filter(traces)
    _log(f"L2 ingress: {len(traces)} traces, {len(clusters)} clusters")

    if INTERRUPTED:
        _audit("suspend", None, {"stage": "after_l2_ingress"}, session_id)
        return {"status": "suspended", "stage": "l2_ingress"}

    # Stage 3 + 4
    commits: list[dict] = []
    for idx, cluster in enumerate(clusters, 1):
        if len(commits) >= cfg["max_llm_calls"]:
            _log("max LLM calls reached — stopping", "WARN")
            break
        if INTERRUPTED:
            _audit("suspend", None, {"stage": f"metabolize_cluster_{idx}"}, session_id)
            return {"status": "suspended", "stage": f"metabolize_cluster_{idx}"}

        metabolized = _metabolize(cluster, cfg)
        if metabolized is None:
            continue
        if not metabolized["cooled"]:
            _log(
                f"cluster {idx} did not cool (delta_s={metabolized['delta_s']:.6f}) — rejecting",
                "WARN",
            )
            continue

        commit = _shadow_commit(cluster, metabolized, cfg, dry_run, session_id)
        commits.append(commit)

    summary = {
        "status": "completed",
        "session_id": session_id,
        "dry_run": dry_run,
        "state": state,
        "traces_ingested": len(traces),
        "clusters": len(clusters),
        "shadow_commits": len(commits),
        "commits": commits,
    }
    _audit("daemon_end", None, summary, session_id)
    _log(f"sleep cycle complete: {len(commits)} shadow commits")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="OpenClaw sleep-time compute daemon prototype")
    parser.add_argument("--execute", action="store_true", help="Write to l3_shadow (default dry-run)")
    parser.add_argument("--config", type=str, default="", help="Path to JSON config file")
    parser.add_argument("--foreground", action="store_true", help="Run one cycle and exit")
    args = parser.parse_args()

    cfg = dict(DEFAULT_CONFIG)
    if args.config:
        cfg.update(json.loads(Path(args.config).read_text()))

    dry_run = not args.execute
    if args.execute:
        _log("EXECUTE mode: will write to l3_shadow only", "WARN")

    if not _acquire_lock(cfg["lock_file"]):
        _log("could not acquire lock — another instance is running", "ERROR")
        return 1

    try:
        summary = run_cycle(cfg, dry_run=dry_run)
        print(json.dumps(summary, indent=2, default=str))
        return 0 if summary["status"] in ("completed", "skipped") else 1
    finally:
        _release_lock(cfg["lock_file"])


if __name__ == "__main__":
    sys.exit(main())
