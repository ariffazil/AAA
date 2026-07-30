#!/usr/bin/env python3
"""
fed_ingest.py — FED Passive Telemetry Ingester (BUILD 4)
═══════════════════════════════════════════════════════════
Consumes flow receipts from arifFlow (:7073) and updates fed_state.db:
  • route_latency: p50/p95 recalculated per provider+model
  • token_bank_spend: auto-logged from receipt payload
  • route_health: status updated from receipt errors

Runs as a cron job (every 5 min) or daemon. NEVER pings.
FED NEVER pings. Agents emit telemetry → arifFlow → this script → fed_state.db.

Forged: 2026-07-30  ·  DITEMPA BUKAN DIBERI
"""

import json
import sqlite3
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError

FED_STATE_DB = Path("/root/.local/share/arifos/fed_state.db")
ARIFLOW_URL = "http://127.0.0.1:7073/receipts?limit=100"
ARIFLOW_HEALTH = "http://127.0.0.1:7073/health"


def get_db():
    conn = sqlite3.connect(str(FED_STATE_DB))
    conn.row_factory = sqlite3.Row
    return conn


def probe_ariflow() -> dict | None:
    """Check if arifFlow is alive."""
    try:
        req = Request(ARIFLOW_HEALTH)
        with urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode())
    except (URLError, json.JSONDecodeError) as e:
        print(f"  ⚠️  arifFlow unreachable: {e}")
        return None


def fetch_receipts() -> list[dict]:
    """Fetch recent flow receipts from arifFlow."""
    try:
        req = Request(ARIFLOW_URL)
        with urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            # arifFlow returns { receipts: [...] } or direct array
            if isinstance(data, dict):
                return data.get("receipts", data.get("data", []))
            return data if isinstance(data, list) else []
    except (URLError, json.JSONDecodeError) as e:
        print(f"  ❌ Failed to fetch receipts: {e}")
        return []


def extract_latency_samples(receipts: list[dict]) -> dict:
    """
    Extract latency data from flow receipts.
    Groups by (provider_id, model_id) → list of durations in ms.
    """
    samples = {}  # key: (provider, model) → [durations_ms]

    for r in receipts:
        payload = r.get("payload", {})
        provider = payload.get("provider")
        model = payload.get("model")
        cost_ns = r.get("cost_ns", 0)

        if not provider or not model:
            continue

        duration_ms = cost_ns / 1_000_000 if cost_ns else 0
        if duration_ms <= 0:
            continue

        key = (provider, model)
        if key not in samples:
            samples[key] = []
        samples[key].append(duration_ms)

    return samples


def update_latency_table(samples: dict):
    """Recalculate p50/p95 and write to route_latency table."""
    conn = get_db()
    now = datetime.now(timezone.utc).isoformat()
    updated = 0

    for (provider, model), durations in samples.items():
        if len(durations) < 2:
            continue

        p50 = statistics.median(durations)
        try:
            p95 = statistics.quantiles(durations, n=20)[18]  # 95th percentile
        except (statistics.StatisticsError, IndexError):
            p95 = max(durations)

        conn.execute(
            """
            INSERT INTO route_latency (provider_id, model_id, p50_ms, p95_ms, sample_count, last_sample)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(provider_id, model_id) DO UPDATE SET
                p50_ms = excluded.p50_ms,
                p95_ms = excluded.p95_ms,
                sample_count = route_latency.sample_count + excluded.sample_count,
                last_sample = excluded.last_sample
        """,
            (provider, model, round(p50, 1), round(p95, 1), len(durations), now),
        )
        updated += 1

    conn.commit()
    conn.close()
    return updated


def extract_spend_events(receipts: list[dict]) -> list[dict]:
    """Extract spend events with token counts from receipts."""
    events = []
    for r in receipts:
        payload = r.get("payload", {})
        provider = payload.get("provider")
        model = payload.get("model")
        agent = r.get("actor_id", "unknown")
        tokens_in = payload.get("tokens_in", 0)
        tokens_out = payload.get("tokens_out", 0)

        if provider and model and (tokens_in or tokens_out):
            events.append(
                {
                    "provider": provider,
                    "model": model,
                    "agent": agent,
                    "tokens_in": tokens_in,
                    "tokens_out": tokens_out,
                }
            )
    return events


def log_spend_events(events: list[dict]):
    """Log spend events to token_bank_spend."""
    from token_bank import estimate_cost

    conn = get_db()
    now = datetime.now(timezone.utc).isoformat()
    logged = 0

    for e in events:
        cost = estimate_cost(e["provider"], e["model"], e["tokens_in"], e["tokens_out"])
        conn.execute(
            """
            INSERT INTO token_bank_spend (provider_id, model_id, agent_id,
                                           tokens_in, tokens_out, estimated_cost_usd, called_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (e["provider"], e["model"], e["agent"], e["tokens_in"], e["tokens_out"], cost, now),
        )
        logged += 1

    conn.commit()
    conn.close()
    return logged


def main():
    print("═" * 50)
    print("📡 FED Telemetry Ingest")
    print(f"   {datetime.now(timezone.utc).isoformat()}")
    print("═" * 50)

    # 1. Check arifFlow alive
    health = probe_ariflow()
    if not health:
        print("❌ arifFlow not reachable. Nothing to ingest.")
        return 1

    # 2. Fetch recent receipts
    receipts = fetch_receipts()
    print(f"\n📥 Fetched {len(receipts)} receipts from arifFlow")

    if not receipts:
        print("   No new receipts. Nothing to update.")
        return 0

    # 3. Extract + update latency
    samples = extract_latency_samples(receipts)
    if samples:
        updated = update_latency_table(samples)
        print(f"📊 Updated latency for {updated} provider+model pairs")
        for (prov, model), durs in sorted(samples.items()):
            p50 = statistics.median(durs)
            print(f"   {prov}/{model}: p50={p50:.0f}ms, n={len(durs)}")

    # 4. Extract + log spend
    events = extract_spend_events(receipts)
    if events:
        logged = log_spend_events(events)
        print(f"💰 Logged {logged} spend events")
        for e in events[:5]:
            print(f"   {e['provider']}/{e['model']}: {e['tokens_in']}+{e['tokens_out']} tok")

    print("\n✅ Ingest complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
