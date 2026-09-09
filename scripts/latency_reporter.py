#!/usr/bin/env python3
"""
latency_reporter.py — Loop 3 Closer
═════════════════════════════════════
Gives reality authority over FED routing via latency data.

Reports latency after each harness call to FED.
FED uses this data for ranking.

This closes Loop 3: Latency → routing influence.
Reality observed → Reality has authority → Ranking changes.

ZEN_KERNEL: Reality must have authority over future behavior.
DITEMPA BUKAN DIBERI.
"""

import os
import sys
import json
import time
import sqlite3
import subprocess
from datetime import datetime, timezone
from pathlib import Path

FED_DB = Path("/root/AAA/state/fed_state.db")
FED_URL = "http://127.0.0.1:7074"
LOG_PATH = Path("/root/scripts/logs/latency_reporter.log")


def log(msg: str):
    """Append to latency reporter log."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).isoformat()
    line = f"[{ts}] {msg}\n"
    with open(LOG_PATH, "a") as f:
        f.write(line)


def report_latency(
    provider: str,
    model: str,
    latency_ms: float,
    success: bool,
    tokens_used: int = 0,
    cost_usd: float = 0.0,
):
    """Report latency to FED via MCP endpoint."""
    payload = {
        "provider": provider,
        "model": model,
        "latency_ms": latency_ms,
        "success": success,
        "tokens_used": tokens_used,
        "cost_usd": cost_usd,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "reporter": "latency_reporter",
    }

    try:
        # Try FED MCP endpoint
        resp = subprocess.run(
            [
                "curl",
                "-sf",
                "-X",
                "POST",
                f"{FED_URL}/mcp",
                "-H",
                "Content-Type: application/json",
                "-H",
                "Accept: application/json, text/event-stream",
                "-d",
                json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "method": "tools/call",
                        "params": {"name": "fed_report_latency", "arguments": payload},
                        "id": 1,
                    }
                ),
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if resp.returncode == 0:
            log(
                f"REPORTED: {provider}/{model} latency={latency_ms}ms success={success}"
            )
            return True
        else:
            # Fallback: write directly to DB
            return write_to_db(
                provider, model, latency_ms, success, tokens_used, cost_usd
            )
    except Exception as e:
        log(f"WARNING: FED endpoint failed, writing to DB: {e}")
        return write_to_db(provider, model, latency_ms, success, tokens_used, cost_usd)


def write_to_db(
    provider: str,
    model: str,
    latency_ms: float,
    success: bool,
    tokens_used: int,
    cost_usd: float,
) -> bool:
    """Write latency data directly to fed_state.db."""
    if not FED_DB.exists():
        log(f"ERROR: FED DB not found")
        return False

    try:
        conn = sqlite3.connect(str(FED_DB))
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS route_latency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                provider TEXT NOT NULL,
                model TEXT NOT NULL,
                latency_ms REAL NOT NULL,
                success INTEGER NOT NULL,
                tokens_used INTEGER DEFAULT 0,
                cost_usd REAL DEFAULT 0.0,
                reported_at TEXT NOT NULL,
                reporter TEXT DEFAULT 'latency_reporter'
            )
        """)

        # Insert latency record
        cursor.execute(
            """INSERT INTO route_latency 
               (provider, model, latency_ms, success, tokens_used, cost_usd, reported_at, reporter)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                provider,
                model,
                latency_ms,
                1 if success else 0,
                tokens_used,
                cost_usd,
                datetime.now(timezone.utc).isoformat(),
                "latency_reporter",
            ),
        )

        # Update provider's average latency
        cursor.execute(
            """UPDATE providers 
               SET avg_latency_ms = (
                   SELECT AVG(latency_ms) FROM route_latency 
                   WHERE provider = ? AND reported_at > datetime('now', '-1 hour')
               ),
               sample_count = (
                   SELECT COUNT(*) FROM route_latency 
                   WHERE provider = ? AND reported_at > datetime('now', '-1 hour')
               )
               WHERE name = ?""",
            (provider, provider, provider),
        )

        conn.commit()
        conn.close()

        log(f"DB_WRITE: {provider}/{model} latency={latency_ms}ms")
        return True
    except Exception as e:
        log(f"ERROR: DB write failed: {e}")
        return False


def wrap_call(provider: str, model: str, call_func, *args, **kwargs):
    """Wrap a function call with latency reporting."""
    start_time = time.time()
    success = False
    result = None

    try:
        result = call_func(*args, **kwargs)
        success = True
    except Exception as e:
        log(f"CALL_FAILED: {provider}/{model} error={str(e)[:100]}")
        raise
    finally:
        latency_ms = (time.time() - start_time) * 1000
        tokens_used = 0
        cost_usd = 0.0

        # Try to extract token/cost info from result
        if isinstance(result, dict):
            tokens_used = result.get("usage", {}).get("total_tokens", 0)
            cost_usd = result.get("cost_usd", 0.0)

        report_latency(provider, model, latency_ms, success, tokens_used, cost_usd)

    return result


def emit_witness(provider: str, latency_ms: float, success: bool):
    """Emit witness to arifFlow about latency report."""
    try:
        payload = {
            "actor_id": "latency_reporter",
            "session_id": f"latency-{provider}",
            "step_type": "Verify",
            "epistemic_label": "Observation",
            "floor_verdict": "Pass",
            "payload": {
                "event": "latency_report",
                "provider": provider,
                "latency_ms": latency_ms,
                "success": success,
                "source": "latency_reporter_loop3",
            },
        }
        subprocess.run(
            [
                "curl",
                "-sf",
                "-X",
                "POST",
                "http://127.0.0.1:7073/ingest",
                "-H",
                "Content-Type: application/json",
                "-d",
                json.dumps(payload),
            ],
            capture_output=True,
            timeout=5,
        )
    except Exception as e:
        pass  # Best effort


def main():
    """CLI interface for latency reporting."""
    if len(sys.argv) < 4:
        print(
            "Usage: latency_reporter.py <provider> <model> <latency_ms> [success] [tokens] [cost]"
        )
        print(
            "Example: latency_reporter.py deepseek deepseek-v4-pro 1500 true 500 0.002"
        )
        sys.exit(1)

    provider = sys.argv[1]
    model = sys.argv[2]
    latency_ms = float(sys.argv[3])
    success = sys.argv[4].lower() == "true" if len(sys.argv) > 4 else True
    tokens_used = int(sys.argv[5]) if len(sys.argv) > 5 else 0
    cost_usd = float(sys.argv[6]) if len(sys.argv) > 6 else 0.0

    report_latency(provider, model, latency_ms, success, tokens_used, cost_usd)
    emit_witness(provider, latency_ms, success)


if __name__ == "__main__":
    main()
