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
