#!/usr/bin/env python3
"""
memory_health.py — Single-command memory subsystem probe.

Checks L1 (Redis), L3 (Qdrant), L4 (Postgres), L5 (FalkorDB/Graphiti), L6 (VAULT999),
plus supporting state files. Returns a compact verdict table.

Usage: python3 scripts/memory_health.py [--brief]
Exit 0 = all OK, 1 = at least one component degraded.
"""

import json
import os
import socket
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta
from urllib.request import urlopen
from urllib.error import URLError


def probe_port(host: str, port: int, timeout: float = 2.0) -> bool:
    try:
        s = socket.socket()
        s.settimeout(timeout)
        s.connect((host, port))
        s.close()
        return True
    except Exception:
        return False


def curl_get(url: str, timeout: float = 3.0):
    try:
        with urlopen(url, timeout=timeout) as r:
            return json.loads(r.read())
    except (URLError, json.JSONDecodeError, Exception):
        return None


def check_redis() -> dict:
    try:
        r = subprocess.run(["redis-cli", "ping"], capture_output=True, text=True, timeout=3)
        alive = r.stdout.strip() == "PONG"
        info = subprocess.run(["redis-cli", "info", "memory"],
                              capture_output=True, text=True, timeout=3).stdout
        used = next((l.split(":")[1] for l in info.splitlines() if l.startswith("used_memory_human")), "?")
        frag = next((l.split(":")[1] for l in info.splitlines() if l.startswith("mem_fragmentation_ratio")), "?")
        keys = subprocess.run(["redis-cli", "KEYS", "*"], capture_output=True, text=True, timeout=5).stdout.strip().split("\n")
        keys = [k for k in keys if k]
        return {"status": "✅" if alive else "❌", "alive": alive,
                "used": used, "frag_ratio": frag, "key_count": len(keys)}
    except FileNotFoundError:
        return {"status": "⚠️", "alive": None, "note": "redis-cli not installed"}


def check_qdrant() -> dict:
    health = curl_get("http://127.0.0.1:6333/health")
    cols = curl_get("http://127.0.0.1:6333/collections")
    if health is None:
        return {"status": "❌", "alive": False}
    n_cols = len(cols.get("result", {}).get("collections", [])) if cols else 0
    return {"status": "✅", "alive": True, "collections": n_cols}


def check_postgres() -> dict:
    """Requires kunci-mas.env to be sourced first."""
    try:
        env = os.environ.copy()
        result = subprocess.run(
            ["psql", "-h", env.get("POSTGRES_HOST", "127.0.0.1"),
             "-U", env.get("POSTGRES_USER", "postgres"),
             "-d", env.get("POSTGRES_DB", "postgres"),
             "-tAc", "SELECT count(*) FROM information_schema.tables WHERE table_schema='public';"],
            capture_output=True, text=True, timeout=5, env=env,
        )
        if result.returncode != 0:
            return {"status": "❌", "alive": False, "err": result.stderr.strip()[:80]}
        return {"status": "✅", "alive": True, "public_tables": int(result.stdout.strip())}
    except FileNotFoundError:
        return {"status": "⚠️", "alive": None, "note": "psql not installed"}


def check_graph_stack() -> dict:
    falkor = probe_port("127.0.0.1", 6380)
    graphiti = probe_port("127.0.0.1", 8000)
    return {
        "status": "✅" if falkor and graphiti else ("❌" if not falkor else "⚠️"),
        "falkor_6380": falkor, "graphiti_8000": graphiti,
    }


def check_vault999() -> dict:
    path = "/root/arifOS/VAULT999/outcomes.jsonl"
    if not os.path.exists(path):
        return {"status": "❌", "exists": False}
    # append-only flag
    try:
        la = subprocess.run(["lsattr", path], capture_output=True, text=True, timeout=3).stdout
        append_only = "a" in la.split()[0] if la.strip() else False
    except Exception:
        append_only = None
    # count + recent activity
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()
    total, recent, last_ts, valid_json = 0, 0, None, True
    with open(path) as f:
        for line in f:
            total += 1
            try:
                o = json.loads(line)
                ts = o.get("ts") or o.get("timestamp") or ""
                if ts > cutoff:
                    recent += 1
                last_ts = ts
            except json.JSONDecodeError:
                valid_json = False
    size_mb = os.path.getsize(path) / (1024 * 1024)
    return {
        "status": "✅" if (append_only and valid_json) else "⚠️",
        "lines": total, "size_mb": round(size_mb, 1),
        "last_24h": recent, "latest": last_ts,
        "append_only": append_only, "valid_json": valid_json,
    }


def check_state_files() -> dict:
    out = {}
    for p in ["/root/.local/share/arifos/carry_forward.json",
              "/root/AAA/state/flow_state.json"]:
        if not os.path.exists(p):
            out[p] = {"status": "❌"}
            continue
        try:
            data = json.load(open(p))
            refreshed = data.get("refreshed_at") or data.get("session_slug")
            out[p] = {"status": "✅", "key": refreshed}
        except Exception as e:
            out[p] = {"status": "⚠️", "err": str(e)[:80]}
    return out


def main():
    brief = "--brief" in(sys.argv)
    print("=" * 60)
    print("MEMORY SUBSYSTEM HEALTH — arifOS Federation")
    print(f"Probed at: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)

    components = {
        "L1 Redis (ephemeral + session)": check_redis(),
        "L3 Qdrant (vector store)": check_qdrant(),
        "L4 Postgres (structured)": check_postgres(),
        "L5 FalkorDB + Graphiti (relationships)": check_graph_stack(),
        "L6 VAULT999 (immutable)": check_vault999(),
    }
    state = check_state_files()

    for name, r in components.items():
        print(f"\n{name}: {r.get('status','?')}")
        if brief:
            continue
        for k, v in r.items():
            if k != "status":
                print(f"  {k}: {v}")

    print("\nSupporting state files:")
    for path, r in state.items():
        print(f"  {path}: {r.get('status','?')}  {r}")

    # Overall verdict
    statuses = [c.get("status", "?") for c in components.values()]
    if "❌" in statuses:
        print("\nVERDICT: ❌ DEGRADED")
        sys.exit(1)
    if "⚠️" in statuses:
        print("\nVERDICT: ⚠️ OK WITH WARNINGS")
        sys.exit(0)
    print("\nVERDICT: ✅ ALL OK")
    sys.exit(0)


if __name__ == "__main__":
    main()