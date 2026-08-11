#!/usr/bin/env python3
"""AAA Cockpit Probe — Standalone background organ prober.

Runs every 15s via systemd timer. Probes all 10 organs/services,
maintains TTL tombstoning (3 missed = DEAD), writes status.json.

State is persisted via the status.json file itself — no in-memory state.
Each run reads the prior state, probes, updates, and writes.

DITEMPA BUKAN DIBERI.
"""

import json
import time
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# ── Config ───────────────────────────────────────────────────────────────

STATUS_JSON_PATH = Path("/root/AAA/state/status.json")
MAX_MISSED_PROBES = 3  # 45 seconds at 15s interval

# P3B — Closure SLO (doctrine: ARIFOS::CLOSURE_RECOVERY::v1 LEVERAGE POINT #3)
CLOSURE_SLO_DIR = Path("/root/forge_work/closure-slo")
RECOVERY_SCAN_DIR = Path("/root/forge_work/recovery-scans")
FORGE_WORK_DIR = Path("/root/forge_work")
PENDING_RECEIPTS_PATH = Path("/root/.local/share/arifos/pending_receipts.jsonl")
SEAL_PENDING_DIR = Path("/root/.local/share/arifos/seal-pending")
OPENCODE_RECEIPTS_PATH = Path("/root/.local/share/arifos/opencode_receipts.jsonl")

PROBED_ORGANS = [
    {"id": "arifos", "port": 8088, "role": "Kernel", "ceiling": "JUDGE_ONLY", "class": "CORE"},
    {"id": "a-forge", "port": 7071, "role": "Execution", "ceiling": "EXECUTE_AFTER_SEAL", "class": "CORE"},
    {"id": "aaa", "port": 3001, "role": "Control Plane", "ceiling": "DISPLAY_ONLY", "class": "CORE"},
    {"id": "geox", "port": 8081, "role": "Earth Intelligence", "ceiling": "COMPUTE_ONLY", "class": "CORE"},
    {"id": "wealth", "port": 18082, "role": "Capital Intelligence", "ceiling": "COMPUTE_ONLY", "class": "CORE"},
    {"id": "well", "port": 18083, "role": "Vitality Mirror", "ceiling": "REFLECT_ONLY", "class": "CORE"},
    {"id": "arifflow", "port": 7073, "role": "Metabolism", "ceiling": "METABOLIZE_ONLY", "class": "METABOLISM"},
    {"id": "flame", "port": 18901, "role": "Free Inference", "ceiling": "ADVISORY_WORKER", "class": "ADVISORY"},
    {"id": "fed", "port": 7074, "role": "Model Router", "ceiling": "ADVISORY_ONLY", "class": "ADVISORY"},
    {"id": "hermes", "port": 18086, "role": "Telegram Bridge", "ceiling": "RELAY_ONLY", "class": "EDGE"},
]


def probe_one(organ: dict) -> dict:
    """Probe a single organ via GET /health. Returns result dict."""
    agent_id = organ["id"]
    port = organ["port"]
    url = f"http://127.0.0.1:{port}/health"
    result = {
        "agent_id": agent_id,
        "port": port,
        "healthy": False,
        "status_code": 0,
        "latency_ms": 0.0,
        "error": None,
        "apex_scalars": {},
        "tools_count": 0,
        "version": None,
    }

    t0 = time.monotonic()
    try:
        req = Request(url, headers={"User-Agent": "AAA-Cockpit-Probe/2.0"})
        with urlopen(req, timeout=5) as resp:
            result["status_code"] = resp.status
            result["latency_ms"] = round((time.monotonic() - t0) * 1000, 1)
            if resp.status == 200:
                result["healthy"] = True
                try:
                    body = json.loads(resp.read().decode())
                    apex = body.get("apex_scalars", {})
                    if apex:
                        result["apex_scalars"] = {
                            "G": apex.get("G", {}).get("value") if isinstance(apex.get("G"), dict) else apex.get("G"),
                            "C_dark": apex.get("C_dark", {}).get("value")
                            if isinstance(apex.get("C_dark"), dict)
                            else apex.get("C_dark"),
                            "W3": apex.get("W3", {}).get("value")
                            if isinstance(apex.get("W3"), dict)
                            else apex.get("W3"),
                        }
                    tc = body.get("tools_count") or body.get("tools_loaded") or body.get("tools")
                    if isinstance(tc, (int, float)):
                        result["tools_count"] = int(tc)
                    elif isinstance(tc, list):
                        result["tools_count"] = len(tc)
                    result["version"] = body.get("version") or body.get("software_release", {}).get("release_id")
                except (json.JSONDecodeError, TypeError, AttributeError):
                    pass
    except HTTPError as e:
        result["status_code"] = e.code
        result["latency_ms"] = round((time.monotonic() - t0) * 1000, 1)
        result["error"] = f"HTTP {e.code}"
    except URLError:
        result["latency_ms"] = round((time.monotonic() - t0) * 1000, 1)
        result["error"] = "connection refused"
    except Exception as e:
        result["latency_ms"] = round((time.monotonic() - t0) * 1000, 1)
        result["error"] = str(e)[:200]

    return result


def load_prior_state() -> dict:
    """Load prior agent states from status.json, or return empty."""
    try:
        if STATUS_JSON_PATH.exists():
            data = json.loads(STATUS_JSON_PATH.read_text())
            agents = {}
            for a in data.get("agent_list", []):
                agents[a["agent_id"]] = {
                    "missed_probes": a.get("missed_probes", 0),
                    "status": a.get("status", "unknown"),
                    "last_seen": a.get("last_seen", 0),
                }
            return agents
    except Exception:
        pass
    return {}


def compute_status(prior: dict, agent_id: str, healthy: bool) -> dict:
    """Apply TTL tombstoning logic to determine new status."""
    prev = prior.get(agent_id, {"missed_probes": 0, "status": "unknown"})
    missed = prev.get("missed_probes", 0)

    if healthy:
        return {"status": "healthy", "missed_probes": 0}
    else:
        missed += 1
        if missed >= MAX_MISSED_PROBES:
            return {"status": "dead", "missed_probes": missed}
        elif missed >= 2:
            return {"status": "degraded", "missed_probes": missed}
        else:
            return {"status": "unreachable", "missed_probes": missed}


def ttl_label(status: str, age: float) -> str:
    """Human-readable TTL label."""
    if status == "dead":
        return "🪦 DEAD"
    if age < 30:
        return "🟢 LIVE"
    elif age < 60:
        return "🟡 STALE"
    elif age < 120:
        return "🟠 GHOST"
    return "🔴 LOST"


def _probe_memory_tiers() -> dict:
    """Probe all memory tiers (L1-L6) and return health status."""
    import subprocess

    result = {
        "L1-L2_redis": {"status": "unknown", "detail": ""},
        "L3_qdrant": {"status": "unknown", "detail": ""},
        "L5_graphiti": {"status": "unknown", "detail": ""},
        "L6_vault999": {"status": "unknown", "detail": ""},
    }
    # L1-L2 Redis
    try:
        r = subprocess.run(["redis-cli", "PING"], capture_output=True, text=True, timeout=3)
        result["L1-L2_redis"]["status"] = "healthy" if "PONG" in r.stdout else "degraded"
        result["L1-L2_redis"]["detail"] = r.stdout.strip()
    except Exception as e:
        result["L1-L2_redis"]["status"] = "dead"
        result["L1-L2_redis"]["detail"] = str(e)[:80]
    # L3 Qdrant
    try:
        r = Request("http://127.0.0.1:6333", headers={"User-Agent": "Cockpit-Probe"})
        with urlopen(r, timeout=3) as resp:
            result["L3_qdrant"]["status"] = "healthy" if resp.status == 200 else "degraded"
            result["L3_qdrant"]["detail"] = f"HTTP {resp.status}"
    except Exception as e:
        result["L3_qdrant"]["status"] = "dead"
        result["L3_qdrant"]["detail"] = str(e)[:80]
    # L5 Graphiti
    try:
        r = Request("http://127.0.0.1:8000/health", headers={"User-Agent": "Cockpit-Probe"})
        with urlopen(r, timeout=3) as resp:
            body = json.loads(resp.read().decode())
            result["L5_graphiti"]["status"] = body.get("status", "degraded")
            result["L5_graphiti"]["detail"] = body.get("service", "")
    except Exception as e:
        result["L5_graphiti"]["status"] = "dead"
        result["L5_graphiti"]["detail"] = str(e)[:80]
    # L6 VAULT999
    from pathlib import Path

    vault_path = Path("/root/arifOS/VAULT999/outcomes.jsonl")
    if vault_path.exists():
        result["L6_vault999"]["status"] = "healthy"
        try:
            lines = vault_path.read_text().strip().split("\n")
            result["L6_vault999"]["detail"] = f"{len(lines)} entries"
        except Exception:
            result["L6_vault999"]["detail"] = "present"
    else:
        result["L6_vault999"]["status"] = "dead"
        result["L6_vault999"]["detail"] = "missing"
    return result


def _closure_slo() -> dict:
    """P3B — Closure SLO metrics for cockpit.

    Surfaces at boot:
      - unsealed_sessions_over_24h  (from opencode_receipts.jsonl)
      - pending_receipts            (count from pending_receipts.jsonl)
      - seal_pending_oldest_days    (max mtime in seal-pending/)
      - zombie_count                (latest reaper snapshot)
      - closure_velocity_24h        (forge_work .md created last 24h)
      - forge_velocity_24h          (forge_work all files created last 24h)

    Doctrine: ARIFOS::CLOSURE_RECOVERY::v1 LEVERAGE POINT #3
    """
    metrics = {
        "unsealed_sessions_over_24h": 0,
        "pending_receipts": 0,
        "seal_pending_oldest_days": 0.0,
        "zombie_count": 0,
        "closure_velocity_24h": 0,
        "forge_velocity_24h": 0,
        "doctrine_ref": "ARIFOS::CLOSURE_RECOVERY::v1",
        "leverage_point": 3,
        "verdict": "GREEN",
        "thresholds": {"unsealed_24h_max": 10, "pending_max": 5, "zombie_max": 20},
    }

    # 1. Unsealed > 24h (sessions with last activity > 24h ago)
    if OPENCODE_RECEIPTS_PATH.exists():
        try:
            from collections import defaultdict
            from datetime import datetime, timezone, timedelta

            sess = defaultdict(list)
            with open(OPENCODE_RECEIPTS_PATH) as f:
                for line in f:
                    try:
                        d = json.loads(line)
                        sid = d.get("sessionID") or d.get("session_id")
                        if not sid or sid == "boot":
                            continue
                        sess[sid].append(d)
                    except Exception:
                        pass
            cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
            old = 0
            for sid, evs in sess.items():
                evs.sort(key=lambda x: x.get("ts", ""))
                if not evs:
                    continue
                try:
                    last = datetime.fromisoformat(evs[-1].get("ts", "").replace("Z", "+00:00"))
                    if last < cutoff:
                        old += 1
                except Exception:
                    pass
            metrics["unsealed_sessions_over_24h"] = old
        except Exception:
            pass

    # 2. Pending receipts
    if PENDING_RECEIPTS_PATH.exists():
        try:
            with open(PENDING_RECEIPTS_PATH) as f:
                metrics["pending_receipts"] = sum(1 for _ in f)
        except Exception:
            pass

    # 3. Seal-pending oldest age
    if SEAL_PENDING_DIR.exists():
        try:
            from datetime import datetime as _dt

            files = [f for f in SEAL_PENDING_DIR.iterdir() if f.is_file()]
            if files:
                oldest_mtime = max(f.stat().st_mtime for f in files)
                metrics["seal_pending_oldest_days"] = round((_dt.now().timestamp() - oldest_mtime) / 86400, 1)
        except Exception:
            pass

    # 4. Zombie count from latest reaper scan (live probe over cron-snapshots)
    try:
        snaps = sorted(RECOVERY_SCAN_DIR.glob("cron-snapshots/reaper-*.json"))
        if snaps:
            d = json.loads(snaps[-1].read_text())
            metrics["zombie_count"] = d.get("zombie_count", 0)
        else:
            # fall back to latest reap scan
            reaps = sorted(RECOVERY_SCAN_DIR.glob("reap-*.json"))
            if reaps:
                d = json.loads(reaps[-1].read_text())
                metrics["zombie_count"] = d.get("summary", {}).get("by_verdict", {}).get("HOLD", 0)
    except Exception:
        pass

    # 5+6. Closure velocity + forge velocity (last 24h)
    if FORGE_WORK_DIR.exists():
        try:
            cutoff_ts = time.time() - 86400
            md_count = 0
            all_count = 0
            for p in FORGE_WORK_DIR.rglob("*"):
                try:
                    if p.is_file() and p.stat().st_mtime >= cutoff_ts:
                        all_count += 1
                        if p.suffix == ".md":
                            md_count += 1
                except Exception:
                    continue
            metrics["closure_velocity_24h"] = md_count
            metrics["forge_velocity_24h"] = all_count
        except Exception:
            pass

    # Verdict — yellow/red if thresholds breached
    verdict = "GREEN"
    if metrics["unsealed_sessions_over_24h"] > metrics["thresholds"]["unsealed_24h_max"]:
        verdict = "YELLOW"
    if metrics["pending_receipts"] > metrics["thresholds"]["pending_max"]:
        verdict = "YELLOW"
    if metrics["zombie_count"] > metrics["thresholds"]["zombie_max"]:
        verdict = "RED"
    if metrics["forge_velocity_24h"] == 0:
        verdict = "RED"
    metrics["verdict"] = verdict

    return metrics


def main():
    t0 = time.monotonic()
    prior = load_prior_state()
    now = time.time()
    agent_list = []

    alive_count = 0
    dead_count = 0

    for organ in PROBED_ORGANS:
        probe_result = probe_one(organ)
        ttl = compute_status(prior, organ["id"], probe_result["healthy"])

        if ttl["status"] == "healthy":
            alive_count += 1
        elif ttl["status"] == "dead":
            dead_count += 1

        last_seen = now if probe_result["healthy"] else prior.get(organ["id"], {}).get("last_seen", now)
        age = 0 if probe_result["healthy"] else (now - last_seen) if last_seen else 999

        agent_list.append(
            {
                "agent_id": organ["id"],
                "role": organ["role"],
                "class": organ["class"],
                "authority_ceiling": organ["ceiling"],
                "port": organ["port"],
                "status": ttl["status"],
                "ttl": ttl_label(ttl["status"], age),
                "age_seconds": round(age, 1),
                "missed_probes": ttl["missed_probes"],
                "latency_ms": round(probe_result["latency_ms"], 1),
                "tools_count": probe_result["tools_count"],
                "apex_scalars": probe_result["apex_scalars"],
                "version": probe_result.get("version"),
                "error": probe_result.get("error"),
                "last_seen": last_seen if last_seen else now,
            }
        )

    # Track probe count across runs
    probe_count = prior.get("_probe_count", 0) + 1
    boot_time = prior.get("_boot_time", now)
    uptime = round(now - boot_time, 1)

    status = {
        "cockpit_version": "2.0.0-live",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "probe_count": probe_count,
        "probe_duration_ms": round((time.monotonic() - t0) * 1000, 1),
        "uptime_seconds": uptime,
        "agents": {
            "total": len(agent_list),
            "alive": alive_count,
            "dead": dead_count,
        },
        "memory_tiers": _probe_memory_tiers(),
        "closure_slo": _closure_slo(),
        "agent_list": agent_list,
        "_probe_count": probe_count,
        "_boot_time": boot_time,
        "_note": "Auto-generated by AAA Cockpit Probe. Do not edit manually.",
    }

    # Atomic write
    tmp = STATUS_JSON_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(status, indent=2, default=str))
    tmp.rename(STATUS_JSON_PATH)

    # Summary to stdout (for journal)
    print(f"COCKPIT: {alive_count}/{len(PROBED_ORGANS)} alive, {dead_count} dead ({status['probe_duration_ms']}ms)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
