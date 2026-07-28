#!/usr/bin/env python3
"""
forge_surface_reconcile.py — Live MCP surface reconciliation engine.
Probes all federation organs, reconciles drift between declared vs. live tools,
and hydrates the canonical MCP server registry.

DITEMPA BUKAN DIBERI — Forged, Not Given.
Forged: 2026-07-28 by FORGE (000Ω) under F13 SOVEREIGN directive.
"""

import json
import os
import sys
import time
import urllib.request
import hashlib
from datetime import datetime, timezone
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────

ORGANS = {
    "arifos": {
        "health": "http://127.0.0.1:8088/health",
        "mcp": "http://127.0.0.1:8088/mcp",
        "port": 8088,
        "public_endpoint": "https://arifos.arif-fazil.com/mcp",
        "category": "kernel",
        "description": "Constitutional AI orchestration kernel — session, judge, vault, seal",
    },
    "aforge": {
        "health": "http://127.0.0.1:7071/health",
        "mcp": "http://127.0.0.1:7072/mcp",
        "port": 7072,
        "public_endpoint": "https://forge.arif-fazil.com/mcp",
        "category": "execution",
        "description": "Governed execution shell — build, deploy, mutate under constitutional lease",
    },
    "geox": {
        "health": "http://127.0.0.1:8081/health",
        "mcp": "http://127.0.0.1:8081/mcp",
        "port": 8081,
        "public_endpoint": "https://geox.arif-fazil.com/mcp",
        "category": "earth-intelligence",
        "description": "Earth intelligence — seismic, petrophysics, basin, prospect evaluation",
    },
    "wealth": {
        "health": "http://127.0.0.1:18082/health",
        "mcp": "http://127.0.0.1:18082/mcp",
        "port": 18082,
        "public_endpoint": "https://wealth.arif-fazil.com/mcp",
        "category": "capital-intelligence",
        "description": "Capital intelligence — NPV, risk, conservation, flow, entropy",
    },
    "well": {
        "health": "http://127.0.0.1:18083/health",
        "mcp": "http://127.0.0.1:18083/mcp",
        "port": 18083,
        "public_endpoint": "https://well.arif-fazil.com/mcp",
        "category": "human-readiness",
        "description": "Human readiness — vitality, fatigue, dignity, homeostasis (REFLECT_ONLY)",
    },
}

REGISTRY_DIR = Path("/root/AAA/registries/mcp_servers")
RECONCILE_DIR = Path("/root/A-FORGE/forge_work/2026-07-28/mcp-registry")
MCP_HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}


# ── Probe Functions ────────────────────────────────────────────


def probe_health(url: str) -> dict | None:
    """Fetch organ /health endpoint."""
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        return {"_error": str(e), "_reachable": False}


def probe_mcp_tools(mcp_url: str) -> list[dict] | None:
    """Probe MCP tools/list with proper initialize handshake."""
    try:
        payload = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-03-26",
                    "capabilities": {},
                    "clientInfo": {"name": "forge-reconcile", "version": "1.0"},
                },
            }
        ).encode()
        req = urllib.request.Request(mcp_url, data=payload, headers=MCP_HEADERS, method="POST")
        with urllib.request.urlopen(req, timeout=8) as r:
            init_resp = json.loads(r.read().decode())

        if "error" in init_resp:
            return None  # auth-gated

        # Now tools/list
        payload2 = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}).encode()
        req2 = urllib.request.Request(mcp_url, data=payload2, headers=MCP_HEADERS, method="POST")
        with urllib.request.urlopen(req2, timeout=8) as r2:
            result = json.loads(r2.read().decode())
            return result.get("result", {}).get("tools", [])
    except Exception:
        return None


def extract_tool_count_from_health(health: dict) -> int:
    """Extract tool count from health response using multiple heuristics."""
    for key in ("tools_loaded", "tool_count", "canonical_tools", "public_tools"):
        val = health.get(key)
        if val is not None and isinstance(val, (int, str)):
            try:
                return int(val)
            except (ValueError, TypeError):
                pass
    return 0


# ── Classification ─────────────────────────────────────────────


def classify_tool_risk(tool: dict) -> str:
    """Classify tool risk tier from description heuristics."""
    desc = tool.get("description", "").lower()
    name = tool.get("name", "").lower()

    if any(kw in desc for kw in ["irreversible", "seal", "mutate", "delete", "destroy"]):
        return "CRITICAL"
    if any(kw in desc for kw in ["mutate", "write", "execute", "commit", "deploy"]):
        return "HIGH"
    if any(kw in desc for kw in ["observe", "read", "list", "health", "probe", "status"]):
        return "LOW"
    return "MEDIUM"


def classify_transport(tool: dict) -> str:
    """Detect transport from tool metadata."""
    desc = tool.get("description", "").lower()
    if "streamable" in desc:
        return "streamable_http"
    if "sse" in desc:
        return "sse"
    return "streamable_http"  # default for arifOS federation


# ── Core Reconciliation ─────────────────────────────────────────


def reconcile_all() -> dict:
    """Run full reconciliation across all organs. Returns summary report."""
    timestamp = datetime.now(timezone.utc).isoformat()
    results = {}
    total_live = 0
    total_drifts = 0

    for organ_id, config in ORGANS.items():
        print(f"\n{'=' * 60}")
        print(f"🔍 Reconciling {organ_id}...")

        health = probe_health(config["health"])
        mcp_tools = probe_mcp_tools(config["mcp"])

        health_ok = health and not health.get("_error")
        mcp_ok = mcp_tools is not None

        # Tool count sources
        h_count = extract_tool_count_from_health(health) if health else 0
        m_count = len(mcp_tools) if mcp_tools else 0

        # Determine canonical count
        canonical_count = m_count if mcp_ok else h_count
        drift_count = abs(h_count - m_count) if (mcp_ok and h_count != m_count) else 0

        status = "ONLINE"
        if not health_ok:
            status = "OFFLINE"
        elif drift_count > 0:
            status = "DRIFT"
        elif not mcp_ok:
            status = "AUTH_GATED"

        total_live += canonical_count
        total_drifts += drift_count

        # Build organ summary
        results[organ_id] = {
            "status": status,
            "health_ok": health_ok,
            "mcp_probe_ok": mcp_ok,
            "tool_count_health": h_count,
            "tool_count_mcp_live": m_count,
            "canonical_tool_count": canonical_count,
            "drift_count": drift_count,
            "health_status": health.get("status", health.get("kernel_verdict", "unknown")) if health else "DEAD",
            "version": health.get("version", "?") if health else "DEAD",
            "tools": [],
        }

        # Populate tool metadata
        if mcp_tools:
            for t in mcp_tools:
                results[organ_id]["tools"].append(
                    {
                        "name": t.get("name", "?"),
                        "description": t.get("description", ""),
                        "risk_tier": classify_tool_risk(t),
                        "transport": classify_transport(t),
                    }
                )
            print(f"  ✅ {canonical_count} tools (live probe), drift={drift_count}")
        else:
            if health_ok:
                print(f"  ⚠️ {canonical_count} tools (health-reported), auth-gated for live probe")
            else:
                err_msg = health.get("_error", "unknown") if isinstance(health, dict) else "no response"
                print(f"  ❌ OFFLINE — {err_msg}")

    summary = {
        "reconciled_at": timestamp,
        "total_organs": len(ORGANS),
        "organs_online": sum(1 for r in results.values() if r["health_ok"]),
        "total_tools_live": total_live,
        "total_drifts_resolved": total_drifts,
        "organs": results,
    }

    return summary


# ── Write Artifacts ────────────────────────────────────────────


def write_server_json(organ_id: str, config: dict, result: dict) -> Path:
    """Write standardized server.json for one organ."""
    server_meta = {
        "$schema": "https://modelcontextprotocol.io/schemas/2026/server.json",
        "id": f"organ.{organ_id}",
        "name": f"{organ_id}-federation",
        "description": config["description"],
        "version": result["version"],
        "author": "Muhammad Arif bin Fazil (F13 SOVEREIGN)",
        "category": config["category"],
        "tags": ["arifos-federation", "governed", organ_id],
        "transport": {
            "type": "streamable_http",
            "endpoint": config["mcp"],
            "public_endpoint": config["public_endpoint"],
        },
        "auth": {
            "type": "sct_bearer",
            "required_scopes": (
                ["organ:read"] if config["category"] in ("human-readiness",) else ["forge:execute", "organ:read"]
            ),
        },
        "constitutional_tier": (
            "F6_DIGNITY" if organ_id == "well" else "F1_MUTATE" if organ_id in ("aforge",) else "F2_TRUTH"
        ),
        "tools_count": result["canonical_tool_count"],
        "tools": result["tools"],
        "status": result["status"],
        "last_reconciled": datetime.now(timezone.utc).isoformat(),
    }

    path = REGISTRY_DIR / f"{organ_id}.json"
    path.write_text(json.dumps(server_meta, indent=2, ensure_ascii=False))
    print(f"  📄 {path}")

    # Also write to dated forge_work
    dated_path = RECONCILE_DIR / f"{organ_id}.json"
    dated_path.write_text(json.dumps(server_meta, indent=2, ensure_ascii=False))

    return path


def write_reconciliation_report(summary: dict) -> Path:
    """Write full reconciliation report."""
    path = RECONCILE_DIR / "RECONCILIATION_REPORT.json"
    path.write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"\n📊 Full report: {path}")
    return path


def write_registry_index(summary: dict) -> Path:
    """Write master registry index."""
    index = {
        "generated_at": summary["reconciled_at"],
        "federation": "arifOS",
        "sovereign": "Muhammad Arif bin Fazil (F13)",
        "total_servers": summary["organs_online"],
        "total_tools": summary["total_tools_live"],
        "servers": {
            organ_id: {
                "id": f"organ.{organ_id}",
                "name": config["description"],
                "category": config["category"],
                "tool_count": result["canonical_tool_count"],
                "status": result["status"],
                "endpoint": config["public_endpoint"],
                "metadata_file": f"{organ_id}.json",
            }
            for organ_id, config in ORGANS.items()
            if (result := summary["organs"].get(organ_id)) and result["health_ok"]
        },
    }

    path = REGISTRY_DIR / "INDEX.json"
    path.write_text(json.dumps(index, indent=2, ensure_ascii=False))
    print(f"📋 Registry index: {path}")
    return path


# ── Public Discovery ───────────────────────────────────────────


def write_well_known() -> dict:
    """Write .well-known/mcp.json and .well-known/agent.json."""
    well_known_dir = Path("/var/www/arif-fazil.com/.well-known")

    # Build endpoints from live reconciled data
    endpoints = []
    for organ_id, config in ORGANS.items():
        srv_path = REGISTRY_DIR / f"{organ_id}.json"
        if srv_path.exists():
            srv = json.loads(srv_path.read_text())
            endpoints.append(
                {
                    "name": f"{organ_id}-public-mcp",
                    "url": config["public_endpoint"],
                    "transport": "streamable_http",
                    "description": config["description"],
                    "category": config["category"],
                    "tools_count": srv["tools_count"],
                    "status": srv["status"],
                }
            )
        else:
            # Include offline organs with zero count
            endpoints.append(
                {
                    "name": f"{organ_id}-public-mcp",
                    "url": config["public_endpoint"],
                    "transport": "streamable_http",
                    "description": config["description"],
                    "category": config["category"],
                    "tools_count": 0,
                    "status": "UNKNOWN",
                }
            )

    mcp_manifest = {
        "version": "1.0",
        "provider": "arifOS Federation",
        "website": "https://arif-fazil.com",
        "documentation": "https://arif-fazil.com/docs",
        "endpoints": endpoints,
    }

    path = well_known_dir / "mcp.json"
    path.write_text(json.dumps(mcp_manifest, indent=2, ensure_ascii=False))
    print(f"\n🌐 {path}")

    # agent.json
    agent_manifest = {
        "provider": "arifOS Federation",
        "version": "1.0",
        "agents": [
            {
                "id": "333-agi",
                "name": "Delta MIND",
                "role": "reasoning + planning + execution (OpenCode)",
                "model": "deepseek/deepseek-v4-pro",
                "endpoint": "https://aaa.arif-fazil.com/a2a",
            },
            {
                "id": "555-asi",
                "name": "Memory Steward",
                "role": "semantic memory, drift detection, recurrence analysis",
                "endpoint": "https://aaa.arif-fazil.com/a2a",
            },
            {
                "id": "888-apex",
                "name": "Constitutional Judge",
                "role": "F1-F13 constitutional verdicts",
                "endpoint": "https://arifos.arif-fazil.com/mcp",
            },
            {
                "id": "hermes-asi",
                "name": "Hermes",
                "role": "Sovereign relay, Telegram bridge, multi-modal routing",
                "endpoint": "https://aaa.arif-fazil.com/a2a",
            },
        ],
    }

    agent_path = well_known_dir / "agent.json"
    agent_path.write_text(json.dumps(agent_manifest, indent=2, ensure_ascii=False))
    print(f"🌐 {agent_path}")

    return {"mcp": str(path), "agent": str(agent_path)}


# ── Main ───────────────────────────────────────────────────────


def main():
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  forge_surface_reconcile.py — MCP Registry Reconciler   ║")
    print("║  DITEMPA BUKAN DIBERI  ·  2026-07-28                     ║")
    print("╚══════════════════════════════════════════════════════════╝")

    summary = reconcile_all()

    print(f"\n{'=' * 60}")
    print(f"📊 RECONCILIATION SUMMARY")
    print(f"{'=' * 60}")
    print(f"  Organs probed:        {summary['total_organs']}")
    print(f"  Organs online:        {summary['organs_online']}")
    print(f"  Total live tools:     {summary['total_tools_live']}")
    print(f"  Drifts detected:      {summary['total_drifts_resolved']}")
    print()

    for organ_id, result in summary["organs"].items():
        icon = "✅" if result["health_ok"] else "❌"
        print(
            f"  {icon} {organ_id:8s}  {result['canonical_tool_count']:3d} tools  "
            f"status={result['status']:<12s}  drift={result['drift_count']}"
        )

    print(f"\n{'=' * 60}")
    print("📝 Writing artifacts...")

    # Write per-organ server.json
    for organ_id, config in ORGANS.items():
        result = summary["organs"][organ_id]
        if result["health_ok"]:
            write_server_json(organ_id, config, result)

    # Write master report
    write_reconciliation_report(summary)

    # Write registry index
    write_registry_index(summary)

    # Write public discovery manifests
    write_well_known()

    # Compute hash
    report_path = RECONCILE_DIR / "RECONCILIATION_REPORT.json"
    report_hash = hashlib.sha256(report_path.read_bytes()).hexdigest()

    print(f"\n{'=' * 60}")
    print(f"🏁 RECONCILIATION COMPLETE")
    print(f"   SHA256: {report_hash}")
    print(f"   Artifacts: {RECONCILE_DIR}")
    print(f"   Registry:  {REGISTRY_DIR}")
    print(f"   Discovery: /var/www/arif-fazil.com/.well-known/")

    return summary


if __name__ == "__main__":
    main()
