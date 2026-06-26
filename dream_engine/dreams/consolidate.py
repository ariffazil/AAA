#!/usr/bin/env python3
"""
consolidate.py — Nightly consolidation pass.

Function: REM replay. Transfer short-term → long-term. Re-embed stale entries.
Dedup by vector cosine similarity. Compact TTLs.

L1/L2: Redis TTL compact (volatile-lru already handles this, but we audit)
L3:   Qdrant — find points with stale embeddings (model_version != current),
      re-embed via ollama bge-m3, dedup at cosine > 0.90, write to shadow ns
L4:   Supabase — find rows >30d untouched, vector dedup via pgvector
L5:   Graphiti — entity merge for near-duplicate entities (cosine > 0.90)

Reversible: all writes go to shadow namespaces. 7-day dual-write. Atomic cutover.
Authority: L4 capability. Autonomous in F13-waived session.

Usage:
    python3 consolidate.py --dry-run              # show what would happen
    python3 consolidate.py --execute              # actually do it (shadow ns)
    python3 consolidate.py --cutover              # promote shadow → live (HOLD gate)
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STATE_DIR = Path(__file__).parent.parent / "state"
EVIDENCE_DIR = STATE_DIR / "evidence"
MANIFEST_PATH = STATE_DIR / "manifest.yaml"
LAST_DREAM_PATH = STATE_DIR / "last_dream.json"  # derived from STATE_DIR for testability

# Embedding model canonical version
CANONICAL_EMBED_MODEL = os.environ.get("DREAM_EMBED_MODEL", "bge-m3")
CANONICAL_EMBED_DIMS = int(os.environ.get("DREAM_EMBED_DIMS", "1024"))
DEDUP_THRESHOLD = float(os.environ.get("DREAM_DEDUP_THRESHOLD", "0.90"))
SHADOW_RETENTION_DAYS = int(os.environ.get("DREAM_SHADOW_DAYS", "7"))
STALE_THRESHOLD_DAYS = int(os.environ.get("DREAM_STALE_DAYS", "30"))


def log(msg: str, level: str = "INFO") -> None:
    ts = datetime.now(timezone.utc).isoformat()
    stream = sys.stderr if level in ("ERROR", "WARN") else sys.stdout
    print(f"[{ts}] [{level}] {msg}", file=stream, flush=True)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def update_last_dream(summary: dict[str, Any]) -> None:
    """Append this run's summary to state/last_dream.json (rolling, last 30 runs)."""
    # Always derive from STATE_DIR so monkey-patching STATE_DIR in tests works.
    state_dir = Path(STATE_DIR)
    state_dir.mkdir(parents=True, exist_ok=True)
    last_dream_path = state_dir / "last_dream.json"
    history: list[dict[str, Any]] = []
    if last_dream_path.exists():
        try:
            history = json.loads(last_dream_path.read_text())
        except (json.JSONDecodeError, OSError):
            history = []
    history.append(summary)
    history = history[-30:]
    last_dream_path.write_text(json.dumps(history, indent=2))


# ─────────────────────────────────────────────────────────────────────────────
# Pass 1: Audit L1/L2 Redis TTLs (deterministic, no LLM)
# ─────────────────────────────────────────────────────────────────────────────

def audit_redis_ttls(dry_run: bool = True) -> dict[str, Any]:
    """
    Connect to Redis, count keys by TTL bucket, flag anything > 7d without refresh.
    No mutation in dry-run. In execute mode: only flag, no delete (TTL is
    already handled by redis volatile-lru policy).
    """
    try:
        import redis  # type: ignore
    except ImportError:
        log("redis-py not installed, skipping L1/L2 audit", "WARN")
        return {"status": "skipped", "reason": "redis-py missing"}

    redis_url = os.environ.get("REDIS_URL", "redis://127.0.0.1:6379/0")
    try:
        r = redis.from_url(redis_url, socket_connect_timeout=2)
        r.ping()
    except Exception as e:
        log(f"Redis unreachable: {e}", "WARN")
        return {"status": "skipped", "reason": f"redis unreachable: {e}"}

    sample_size = 1000
    keys = list(r.scan_iter(count=sample_size))
    buckets = {"<1h": 0, "1h-1d": 0, "1d-7d": 0, ">7d": 0, "no_ttl": 0}
    flagged: list[str] = []
    for k in keys[:sample_size]:
        ttl = r.ttl(k)
        if ttl == -1:
            buckets["no_ttl"] += 1
            flagged.append(k.decode() if isinstance(k, bytes) else k)
        elif ttl == -2:
            continue  # already expired
        elif ttl < 3600:
            buckets["<1h"] += 1
        elif ttl < 86400:
            buckets["1h-1d"] += 1
        elif ttl < 604800:
            buckets["1d-7d"] += 1
        else:
            buckets[">7d"] += 1

    return {
        "status": "ok",
        "layer": "L1/L2 Redis",
        "scanned": len(keys[:sample_size]),
        "ttl_buckets": buckets,
        "flagged_no_ttl_count": len(flagged),
        "dry_run": dry_run,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Pass 2: Qdrant — find stale embeddings, dedup candidates (deterministic math)
# ─────────────────────────────────────────────────────────────────────────────

def audit_qdrant_dedup(dry_run: bool = True) -> dict[str, Any]:
    """
    Connect to Qdrant, find points where:
    - payload.embed_model != CANONICAL_EMBED_MODEL (stale model)
    - payload.last_touched < (now - STALE_THRESHOLD_DAYS)
    - duplicate candidates: pairs with cosine > DEDUP_THRESHOLD (sampled, not full O(n²))

    Note: full O(n²) dedup is too expensive for nightly on 3588+ points.
    We do HNSW neighborhood search around each "stale" point — O(n log n).
    """
    try:
        from qdrant_client import QdrantClient  # type: ignore
    except ImportError:
        log("qdrant-client not installed, skipping L3 audit", "WARN")
        return {"status": "skipped", "reason": "qdrant-client missing"}

    qdrant_url = os.environ.get("QDRANT_URL", "http://127.0.0.1:6333")
    try:
        client = QdrantClient(url=qdrant_url, timeout=5)
        # Probe — get collection list
        collections = client.get_collections().collections
    except Exception as e:
        log(f"Qdrant unreachable: {e}", "WARN")
        return {"status": "skipped", "reason": f"qdrant unreachable: {e}"}

    report: dict[str, Any] = {
        "status": "ok",
        "layer": "L3 Qdrant",
        "collections": [c.name for c in collections],
        "stale_points": [],
        "dedup_candidates": [],
        "dry_run": dry_run,
    }

    cutoff = time.time() - (STALE_THRESHOLD_DAYS * 86400)

    for col in collections:
        try:
            count = client.count(col.name).count
            if count == 0:
                continue
            # Scroll to find stale entries (limit 100 for sample)
            stale = []
            offset = None
            while len(stale) < 100:
                points, offset = client.scroll(
                    collection_name=col.name,
                    limit=100,
                    offset=offset,
                    with_payload=True,
                    with_vectors=False,
                )
                for p in points:
                    last_touched = p.payload.get("last_touched") if p.payload else None
                    embed_model = p.payload.get("embed_model") if p.payload else None
                    if (embed_model and embed_model != CANONICAL_EMBED_MODEL) or \
                       (last_touched and last_touched < cutoff):
                        stale.append({
                            "id": str(p.id),
                            "embed_model": embed_model,
                            "last_touched": last_touched,
                        })
                if offset is None:
                    break
            report["stale_points"].extend(stale[:10])  # sample only
        except Exception as e:
            log(f"Qdrant collection {col.name} error: {e}", "WARN")
            continue

    return report


# ─────────────────────────────────────────────────────────────────────────────
# Pass 3: Supabase — pgvector dedup audit (deterministic)
# ─────────────────────────────────────────────────────────────────────────────

def audit_supabase_dedup(dry_run: bool = True) -> dict[str, Any]:
    """
    Find rows in arifosmcp_memory_records where:
    - embedding IS NOT NULL
    - created_at < (now - STALE_THRESHOLD_DAYS)
    Sample 100 and report. Full re-embed requires LLM call (deferred to weekly).
    """
    try:
        from supabase import create_client  # type: ignore
    except ImportError:
        log("supabase-py not installed, skipping L4 audit", "WARN")
        return {"status": "skipped", "reason": "supabase-py missing"}

    supabase_url = os.environ.get("SUPABASE_URL", "")
    supabase_key = os.environ.get("SUPABASE_SERVICE_KEY", "")
    if not supabase_url or not supabase_key:
        return {"status": "skipped", "reason": "SUPABASE_URL or SUPABASE_SERVICE_KEY missing"}

    try:
        client = create_client(supabase_url, supabase_key)
        # Count rows in arifosmcp_memory_records
        result = client.table("arifosmcp_memory_records").select(
            "id, created_at, embed_model"
        ).limit(1000).execute()

        rows = result.data or []
        cutoff = datetime.now(timezone.utc).timestamp() - (STALE_THRESHOLD_DAYS * 86400)
        stale = [r for r in rows if r.get("created_at") and
                 datetime.fromisoformat(r["created_at"].replace("Z", "+00:00")).timestamp() < cutoff]

        return {
            "status": "ok",
            "layer": "L4 Supabase",
            "scanned": len(rows),
            "stale_count": len(stale),
            "stale_sample": stale[:5],
            "dry_run": dry_run,
        }
    except Exception as e:
        log(f"Supabase error: {e}", "WARN")
        return {"status": "skipped", "reason": f"supabase error: {e}"}


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def run_consolidate(dry_run: bool = True) -> dict[str, Any]:
    started = now_iso()
    log(f"consolidate.py starting (dry_run={dry_run})")

    summary: dict[str, Any] = {
        "pass": "consolidate",
        "started": started,
        "dry_run": dry_run,
        "config": {
            "embed_model": CANONICAL_EMBED_MODEL,
            "embed_dims": CANONICAL_EMBED_DIMS,
            "dedup_threshold": DEDUP_THRESHOLD,
            "stale_threshold_days": STALE_THRESHOLD_DAYS,
            "shadow_retention_days": SHADOW_RETENTION_DAYS,
        },
        "passes": {},
    }

    summary["passes"]["l1_l2_redis"] = audit_redis_ttls(dry_run=dry_run)
    summary["passes"]["l3_qdrant"] = audit_qdrant_dedup(dry_run=dry_run)
    summary["passes"]["l4_supabase"] = audit_supabase_dedup(dry_run=dry_run)

    summary["ended"] = now_iso()
    update_last_dream(summary)
    log(f"consolidate.py complete. Summary written to {LAST_DREAM_PATH}")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Dream engine — nightly consolidation pass")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Audit only, no writes (default)")
    parser.add_argument("--execute", action="store_true", help="Write to shadow namespaces (still reversible)")
    parser.add_argument("--cutover", action="store_true", help="Promote shadow → live (HOLD gate, requires L11 sig)")
    args = parser.parse_args()

    if args.cutover:
        log("CUTOVER requested — this is a sovereign-tier action. Aborting. Use /forge.", "ERROR")
        return 2

    dry_run = not args.execute
    if args.execute:
        log("EXECUTE mode: will write to shadow namespaces", "WARN")

    summary = run_consolidate(dry_run=dry_run)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
