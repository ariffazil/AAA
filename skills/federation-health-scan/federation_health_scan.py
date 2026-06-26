#!/usr/bin/env python3
"""
Federation Health Scan — OpenClaw P0 Skill
Read-only health probe for all arifOS organs, NATS streams, drift, and vault.
Returns structured JSON. No mutations. Safe to run anytime.

DITEMPA BUKAN DIBERI — Forged, Not Given.
"""

import json
import subprocess
import time
import sys
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import URLError
import os

# ─── Configuration ───
ORGANS = {
    "arifOS":  {"port": 8088, "has_drift": True},
    "GEOX":    {"port": 8081},
    "WEALTH":  {"port": 18082},
    "WELL":    {"port": 18083},
    "A-FORGE": {"port": 7071},
}

VAULT_FILE = "/root/arifOS/VAULT999/SEALED_EVENTS.jsonl"
TIMEOUT_SEC = 5
WARN_LATENCY_MS = 2000
NATS_STALE_SEC = 300  # 5 min
VAULT_STALE_HOURS = 24


def check_organ(name: str, port: int) -> dict:
    """Probe an organ's /health endpoint. Returns structured dict."""
    start = time.monotonic()
    try:
        url = f"http://127.0.0.1:{port}/health"
        req = Request(url, headers={"Accept": "application/json"})
        with urlopen(req, timeout=TIMEOUT_SEC) as resp:
            data = json.loads(resp.read().decode())
            latency_ms = round((time.monotonic() - start) * 1000, 1)
            status = data.get("status", "unknown")

            result = {
                "status": "OK" if status == "healthy" else "WARN",
                "latency_ms": latency_ms,
            }

            if name == "arifOS":
                result["drift"] = data.get("runtime_drift", False)
                result["tools"] = data.get("tools_loaded", 0)
                result["build_commit"] = data.get("build_commit", "?")
                result["live_commit"] = data.get("live_commit", "?")
                if result["drift"]:
                    result["status"] = "WARN"

            return result

    except URLError as e:
        return {"status": "DOWN", "latency_ms": None, "error": str(e.reason)}
    except Exception as e:
        return {"status": "DOWN", "latency_ms": None, "error": str(e)[:100]}


def check_nats() -> dict:
    """Probe NATS streams via CLI. Uses stream info per-stream for detail."""
    result = {"server": "OK", "streams": {}}
    KEY_STREAMS = ["arifos-governance", "arifos-organs", "agent_memory"]
    now = time.time()

    try:
        # List streams
        r = subprocess.run(
            ["nats", "stream", "ls", "--json"],
            capture_output=True, text=True, timeout=TIMEOUT_SEC
        )
        if r.returncode != 0:
            result["server"] = "DOWN"
            result["error"] = r.stderr[:200]
            return result

        stream_names = json.loads(r.stdout)  # ["agent_memory", "arifos-governance", ...]

        # Get info per key stream
        for name in KEY_STREAMS:
            if name not in stream_names:
                result["streams"][name] = {"messages": 0, "last_msg_sec_ago": None, "status": "DOWN", "error": "stream not found"}
                continue
            try:
                r2 = subprocess.run(
                    ["nats", "stream", "info", name, "--json"],
                    capture_output=True, text=True, timeout=TIMEOUT_SEC
                )
                if r2.returncode == 0:
                    info = json.loads(r2.stdout)
                    msgs = info.get("config", {}).get("messages", 0) or info.get("state", {}).get("messages", 0)
                    last_ts = info.get("state", {}).get("last_ts")
                    last_sec = None
                    if last_ts:
                        try:
                            dt = datetime.fromisoformat(last_ts.replace("Z", "+00:00"))
                            last_sec = round(now - dt.timestamp())
                        except Exception:
                            pass
                    result["streams"][name] = {
                        "messages": msgs,
                        "last_msg_sec_ago": last_sec,
                        "status": "WARN" if (last_sec and last_sec > NATS_STALE_SEC) else "OK"
                    }
            except Exception as e:
                result["streams"][name] = {"messages": 0, "last_msg_sec_ago": None, "status": "DOWN", "error": str(e)[:100]}

    except Exception as e:
        result["server"] = "DOWN"
        result["error"] = str(e)[:200]
    return result


def check_vault() -> dict:
    """Check VAULT999 sealed events staleness."""
    result = {"status": "OK", "last_seal_sec_ago": None, "sealed_count": 0}
    try:
        if not os.path.exists(VAULT_FILE):
            result["status"] = "DOWN"
            result["error"] = f"File not found: {VAULT_FILE}"
            return result

        lines = 0
        last_line = None
        with open(VAULT_FILE, "r") as f:
            for line in f:
                lines += 1
                last_line = line.strip()
        result["sealed_count"] = lines

        if lines == 0:
            result["status"] = "STALE"
            return result

        if last_line:
            try:
                evt = json.loads(last_line)
                ts = evt.get("timestamp") or evt.get("ts") or evt.get("sealed_at")
                if ts:
                    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                    age_sec = (datetime.now(timezone.utc) - dt).total_seconds()
                    result["last_seal_sec_ago"] = round(age_sec)
                    if age_sec > VAULT_STALE_HOURS * 3600:
                        result["status"] = "STALE"
            except Exception:
                result["status"] = "WARN"
                result["error"] = "Could not parse last event timestamp"
    except Exception as e:
        result["status"] = "DOWN"
        result["error"] = str(e)[:200]
    return result


def compute_summary(organs: dict, nats: dict, drift: dict, vault: dict) -> tuple:
    """Compute overall summary verdict and recommendation."""
    statuses = []
    for o in organs.values():
        statuses.append(o.get("status", "DOWN"))
    for s in nats.get("streams", {}).values():
        statuses.append(s.get("status", "OK"))
    if drift.get("status") == "DRIFTING":
        statuses.append("WARN")
    if vault.get("status") in ("STALE", "WARN"):
        statuses.append("WARN")
    if vault.get("status") == "DOWN":
        statuses.append("CRITICAL")

    if "DOWN" in statuses or "CRITICAL" in statuses:
        summary = "CRITICAL"
    elif "WARN" in statuses or "STALE" in statuses:
        summary = "WARN"
    else:
        summary = "OK"

    recs = []
    if summary == "OK":
        recs.append("All systems nominal. No action required.")
    if summary in ("WARN", "CRITICAL"):
        for name, o in organs.items():
            if o.get("status") == "DOWN":
                recs.append(f"RESTART {name} organ (port {ORGANS.get(name,{}).get('port','?')})")
            elif o.get("status") == "WARN" and name == "arifOS" and o.get("drift"):
                recs.append("arifOS runtime drift detected — rebuild/deploy container to sync")
        if vault.get("status") == "STALE":
            hours = round((vault.get("last_seal_sec_ago", 0) or 0) / 3600, 1)
            recs.append(f"VAULT999 last seal {hours}h ago — check arifOS seal pipeline")
        if vault.get("status") == "DOWN":
            recs.append("VAULT999 unreachable — check /root/arifOS/data/VAULT999/")
        if nats.get("server") == "DOWN":
            recs.append("NATS server down — restart nats-server.service")

    return summary, " | ".join(recs) if recs else "No issues detected"


def main():
    start = time.monotonic()

    # Probe all organs
    organs = {}
    for name, cfg in ORGANS.items():
        organs[name] = check_organ(name, cfg["port"])

    # AAA is not a separate health endpoint — check via gateway
    try:
        req = Request("http://127.0.0.1:8091/health", headers={"Accept": "application/json"})
        with urlopen(req, timeout=TIMEOUT_SEC) as resp:
            gw = json.loads(resp.read().decode())
            organs["AAA"] = {
                "status": "OK" if gw.get("status") == "healthy" else "WARN",
                "latency_ms": round((time.monotonic() - start) * 1000, 1),
                "upstream_organs": gw.get("upstream_organs", {})
            }
    except Exception as e:
        organs["AAA"] = {"status": "DOWN", "latency_ms": None, "error": str(e)[:100]}

    # Probe NATS
    nats = check_nats()

    # Drift from arifOS organ check
    drift = {
        "status": "DRIFTING" if organs["arifOS"].get("drift") else "OK",
        "build_commit": organs["arifOS"].get("build_commit", "?"),
        "live_commit": organs["arifOS"].get("live_commit", "?"),
        "detail": f"build_commit={organs['arifOS'].get('build_commit','?')} vs live_commit={organs['arifOS'].get('live_commit','?')}"
    }

    # Probe VAULT
    vault = check_vault()

    summary, recommendation = compute_summary(organs, nats, drift, vault)

    result = {
        "organs": organs,
        "nats": nats,
        "drift": drift,
        "vault": vault,
        "summary": summary,
        "recommendation": recommendation,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "scan_duration_ms": round((time.monotonic() - start) * 1000)
    }

    print(json.dumps(result, indent=2))
    return 0 if summary == "OK" else 1


if __name__ == "__main__":
    sys.exit(main())
