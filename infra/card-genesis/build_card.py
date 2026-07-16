#!/usr/bin/env python3
"""
Card Genesis — Source-First Agent Card Generator

Single-sourcing pattern: source code (git HEAD) is the primary truth.
Registry and MCP surface are derived views. Cards embed the source
snapshot hash so consumers can verify freshness.

Architecture:
  Layer 1 (PRIMARY):  Source files → enumerate public tool names
  Layer 2 (DERIVED):  Live registry (MCP tools/list) → deployment status
  Layer 3 (DERIVED):  MCP surface → actual callable tools

Drift detection:
  source→registry drift: tool in source but not in registry
  registry→surface drift: tool in registry but not callable
  registry→card drift:    tool in card but not in live registry

Usage:
  python3 build_card.py                    # probe all organs
  python3 build_card.py --organ geox       # probe one organ
  python3 build_card.py --diff             # diff cards vs live registry
  python3 build_card.py --dry-run          # probe only, don't write cards

DITEMPA BUKAN DIBERI — Forged, Not Given.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ─── Organ definitions ───────────────────────────────────────────────────────

ORGANS = {
    "arifos": {
        "port": 8088,
        "source_path": "/root/arifOS/arifosmcp",
        "source_pattern": "*.py",
        "tool_prefix": "arif_",
        "card_path": "/root/AAA/agent-cards/organs/arifos/agent-card.json",
        "description": "Constitutional kernel — F1-F13, session, judge, vault, seal",
        "source_note": "Python @mcp.tool decorators in runtime/tools.py",
    },
    "aforge": {
        "port": 7072,
        # Two source locations: tool classes in infrastructure/tools/ AND
        # MCP registration with forge_* prefix in interfaces/mcp/gatewayTools.ts
        "source_paths": [
            "/root/A-FORGE/src/infrastructure/tools",
            "/root/A-FORGE/src/interfaces/mcp",
        ],
        "source_pattern": "*.ts",
        "tool_prefix": "forge_",
        "card_path": "/root/AAA/agent-cards/organs/aforge/agent-card.json",
        "description": "Execution shell — build, deploy, orchestrate",
        "source_note": "forge_* names registered in gatewayTools.ts via tool_name field",
    },
    "geox": {
        "port": 8081,
        "source_path": "/root/GEOX",
        "source_pattern": "*.py",
        "tool_prefix": "geox_",
        "card_path": "/root/AAA/agent-cards/organs/geox/agent-card.json",
        "description": "Earth intelligence — wells, seismic, petrophysics",
        "source_note": "GEOX repo at /root/GEOX (capital), not /root/geox (data dir)",
    },
    "wealth": {
        "port": 18082,
        "source_paths": [
            "/root/WEALTH/wealth_mcp/tools",
            "/root/WEALTH/wealth_core",
        ],
        "source_pattern": "*.py",
        "tool_prefix": ("wealth_", "capital_"),
        "card_path": "/root/AAA/agent-cards/organs/wealth/agent-card.json",
        "description": "Capital intelligence — NPV, risk, collapse",
        "source_note": "Tools in wealth_mcp/tools/canonical.py + institutional.py",
    },
    "well": {
        "port": 18083,
        "source_path": "/root/WELL/src",
        "source_pattern": "*.py",
        "tool_prefix": "well_",
        "card_path": "/root/AAA/agent-cards/organs/well/agent-card.json",
        "description": "Human readiness — vitality, fatigue, dignity",
        "source_note": "Python @mcp.tool in server.py",
    },
}


# ─── Layer 1: Source enumeration ─────────────────────────────────────────────


def enumerate_source_tools(organ: dict) -> list[str]:
    """Read source files and extract public tool names (Layer 1).

    For Python: look for @mcp.tool() decorators or 'name' fields in tool defs.
    For TypeScript: look for tool_name: "forge_*" in MCP registration files.
    Supports multiple source_paths via organ["source_paths"].
    """
    # Support both single and multiple source paths
    source_paths = []
    if "source_paths" in organ:
        source_paths = [Path(p) for p in organ["source_paths"]]
    elif "source_path" in organ:
        source_paths = [Path(organ["source_path"])]
    else:
        return []

    pattern = organ["source_pattern"]
    prefix = organ["tool_prefix"]
    if isinstance(prefix, str):
        prefix = (prefix,)

    tools = set()

    for source_path in source_paths:
        if not source_path.exists():
            continue

        for fpath in source_path.rglob(pattern):
            try:
                content = fpath.read_text(errors="replace")
            except Exception:
                continue

            # Python: @mcp.tool(name="...") or @mcp.tool("...")
            for m in re.finditer(r'@mcp\.tool\(\s*(?:name\s*=\s*)?["\']([^"\']+)["\']', content):
                name = m.group(1)
                if any(name.startswith(p) for p in prefix):
                    tools.add(name)

            # Python: "name": "tool_name" in tool registry dicts
            for m in re.finditer(r'["\']name["\']\s*:\s*["\']([\w_]+)["\']', content):
                name = m.group(1)
                if any(name.startswith(p) for p in prefix):
                    tools.add(name)

            # TypeScript: tool_name: "forge_*" in MCP registration (gatewayTools.ts)
            for m in re.finditer(r'tool_name\s*:\s*["\']([\w_]+)["\']', content):
                name = m.group(1)
                if any(name.startswith(p) for p in prefix):
                    tools.add(name)

            # TypeScript: readonly name = "forge_*" in tool classes
            for m in re.finditer(r'readonly\s+name\s*=\s*["\']([\w_]+)["\']', content):
                name = m.group(1)
                if any(name.startswith(p) for p in prefix):
                    tools.add(name)

    return sorted(tools)


def compute_source_hash(organ: dict) -> str:
    """Compute SHA256 of all source files for this organ."""
    source_paths = []
    if "source_paths" in organ:
        source_paths = [Path(p) for p in organ["source_paths"]]
    elif "source_path" in organ:
        source_paths = [Path(organ["source_path"])]
    else:
        return "sha256:MISSING"

    pattern = organ["source_pattern"]
    hasher = hashlib.sha256()

    any_found = False
    for source_path in source_paths:
        if not source_path.exists():
            continue
        for fpath in sorted(source_path.rglob(pattern)):
            try:
                any_found = True
                content = fpath.read_bytes()
                hasher.update(fpath.relative_to(source_path).as_posix().encode())
                hasher.update(content)
            except Exception:
                continue

    if not any_found:
        return "sha256:MISSING"

    return f"sha256:{hasher.hexdigest()[:16]}"


# ─── Layer 2: Live registry probe ───────────────────────────────────────────


def probe_mcp_tools(port: int) -> tuple[list[str], bool]:
    """Probe live MCP tools/list on a port. Returns (tools, success).

    success=True only on HTTP 200 + valid JSON-RPC response with tools array.
    success=False on any failure (network, parse, non-200, missing tools key).
    Caller treats False as inconclusive probe (forces inadmissible).
    """
    try:
        result = subprocess.run(
            [
                "curl",
                "-sf",
                f"http://127.0.0.1:{port}/mcp",
                "-X",
                "POST",
                "-H",
                "Content-Type: application/json",
                "-d",
                '{"jsonrpc":"2.0","id":1,"method":"tools/list"}',
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            return [], False
        data = json.loads(result.stdout)
        if "result" not in data or "tools" not in data.get("result", {}):
            return [], False
        tools = data["result"]["tools"]
        return sorted([t["name"] for t in tools]), True
    except Exception:
        return [], False


# ─── Layer 3: MCP surface verification ──────────────────────────────────────


def verify_tool_callable(port: int, tool_name: str) -> bool:
    """Check if a specific tool is callable (dry-run with empty args)."""
    # Just checking tools/list is sufficient — if it's listed, it's registered
    return True  # Placeholder; full check would invoke the tool


# ─── Drift detection ────────────────────────────────────────────────────────


def compute_drift(
    source_tools: list[str],
    registry_tools: list[str],
    card_tools: list[str],
) -> dict:
    """Compute drift between all three layers."""
    source_set = set(source_tools)
    registry_set = set(registry_tools)
    card_set = set(card_tools)

    return {
        "source_to_registry": sorted(source_set - registry_set),
        "registry_to_source": sorted(registry_set - source_set),
        "registry_to_card": sorted(registry_set - card_set),
        "card_to_registry": sorted(card_set - registry_set),
        "source_count": len(source_tools),
        "registry_count": len(registry_tools),
        "card_count": len(card_tools),
        "source_to_registry_drift_pct": (
            round(100 * len(source_set & registry_set) / len(source_set), 1) if source_set else 100.0
        ),
    }


# ─── Card emission ──────────────────────────────────────────────────────────


def load_existing_card(card_path: str) -> dict | None:
    """Load existing agent card if it exists."""
    try:
        return json.loads(Path(card_path).read_text())
    except Exception:
        return None


def emit_card(
    organ_name: str,
    organ: dict,
    source_tools: list[str],
    registry_tools: list[str],
    source_hash: str,
    drift: dict,
    dry_run: bool = False,
    probe_failed: bool = False,
) -> dict:
    """Emit an updated agent card with registry receipt hash.

    INV-007 + probe guard:
      - source_to_registry drift > 0 → admissible = false
      - MCP probe failed or returned 0 while source has tools → admissible = false
    """
    now = datetime.now(timezone.utc).isoformat()
    existing = load_existing_card(organ["card_path"])

    # Build the card
    card = existing.copy() if existing else {}

    # Ensure required fields
    card.setdefault("$schema", "arifOS/agent-card/v2.3.0")
    card.setdefault("schemaVersion", "2.3.0")
    card.setdefault("id", organ_name)
    card.setdefault("name", organ_name.upper())
    card.setdefault("description", organ["description"])
    card.setdefault("version", "1.0.0")
    card.setdefault("protocolVersion", "1.0")
    card.setdefault("url", f"http://127.0.0.1:{organ['port']}/mcp")
    card.setdefault(
        "provider",
        {
            "organization": "arifOS by Muhammad Arif bin Fazil",
            "url": "https://arif-fazil.com",
        },
    )
    card.setdefault("capabilities", {"streaming": True})
    card.setdefault("defaultInputModes", ["application/json"])
    card.setdefault("defaultOutputModes", ["application/json"])

    # Registry truth fields (THE FIX)
    card["registry_receipt_hash"] = source_hash
    card["registry_snapshot_at"] = now
    card["registry_source"] = ["source_enumeration", "mcp_tools_list"]
    card["registry_tool_count"] = {
        "source": drift["source_count"],
        "registry": drift["registry_count"],
        "card": drift["card_count"],
    }
    card["registry_drift"] = {
        "source_to_registry": drift["source_to_registry"],
        "registry_to_source": drift["registry_to_source"],
        "source_to_registry_drift_pct": drift["source_to_registry_drift_pct"],
    }

    # Admissibility: INV-007 + probe guard
    has_source_drift = len(drift["source_to_registry"]) > 0
    has_probe_failure = probe_failed or (drift["registry_count"] == 0 and drift["source_count"] > 0)
    card["admissible"] = not has_source_drift and not has_probe_failure

    # Registry truth verdict
    if has_probe_failure:
        card["registry_truth"] = "DRIFT"
        card["registry_drift"]["note"] = (
            "MCP probe failed or returned 0 tools while source has "
            f"{drift['source_count']} tools; cannot verify registry"
        )
    elif has_source_drift:
        card["registry_truth"] = "DRIFT"
    else:
        card["registry_truth"] = "VERIFIED"

    # Update mcp_surface with live tools
    card["mcp_surface"] = {
        "type": "exposed",
        "endpoints": [
            {
                "url": f"http://127.0.0.1:{organ['port']}/mcp",
                "tool_count": len(registry_tools),
                "tools": registry_tools[:20],  # first 20 for readability
                "key_lanes": [],
                "version": now[:10],
                "registry_receipt_hash": source_hash,
            }
        ],
    }

    # Write card
    if not dry_run:
        card_path = Path(organ["card_path"])
        card_path.parent.mkdir(parents=True, exist_ok=True)
        card_path.write_text(json.dumps(card, indent=2, ensure_ascii=False) + "\n")
        print(f"  ✅ Wrote {organ['card_path']}")
    else:
        print(f"  🔍 DRY RUN — would write {organ['card_path']}")

    return card


# ─── Main ───────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Card Genesis — Source-First Agent Card Generator")
    parser.add_argument("--organ", help="Probe specific organ only")
    parser.add_argument("--diff", action="store_true", help="Diff cards vs live registry")
    parser.add_argument("--dry-run", action="store_true", help="Probe only, don't write cards")
    parser.add_argument("--json", action="store_true", help="Output JSON report")
    args = parser.parse_args()

    organs_to_probe = {args.organ: ORGANS[args.organ]} if args.organ and args.organ in ORGANS else ORGANS

    report = {}

    for name, organ in organs_to_probe.items():
        print(f"\n{'=' * 60}")
        print(f"  PROBING: {name.upper()} :{organ['port']}")
        print(f"{'=' * 60}")

        # Layer 1: Source enumeration
        source_tools = enumerate_source_tools(organ)
        source_hash = compute_source_hash(organ)
        print(f"  Layer 1 (source):  {len(source_tools)} tools, hash={source_hash}")

        # Layer 2: Live registry
        registry_tools, registry_probe_ok = probe_mcp_tools(organ["port"])
        probe_failed = not registry_probe_ok
        print(f"  Layer 2 (registry): {len(registry_tools)} tools" + (" ⚠️ PROBE FAILED" if probe_failed else ""))

        # Load existing card
        existing = load_existing_card(organ["card_path"])
        card_tools = []
        if existing:
            mcp_surface = existing.get("mcp_surface", {})
            for ep in mcp_surface.get("endpoints", []):
                for t in ep.get("tools", []):
                    if isinstance(t, str):
                        card_tools.append(t)
                    elif isinstance(t, dict) and "name" in t:
                        card_tools.append(t["name"])
            # Also check skills
            for s in existing.get("skills", []):
                if isinstance(s, dict) and "id" in s:
                    card_tools.append(s["id"])
        card_tools = sorted(set(card_tools))
        print(f"  Layer 3 (card):    {len(card_tools)} tools")

        # Drift detection
        drift = compute_drift(source_tools, registry_tools, card_tools)
        print(f"\n  DRIFT REPORT:")
        print(
            f"    source→registry drift: {len(drift['source_to_registry'])} tools "
            f"({drift['source_to_registry_drift_pct']}% match)"
        )
        if drift["source_to_registry"]:
            for t in drift["source_to_registry"][:10]:
                print(f"      ❌ {t} (in source, not in registry)")
        if drift["registry_to_source"]:
            for t in drift["registry_to_source"][:10]:
                print(f"      ⚠️  {t} (in registry, not in source)")
        if drift["card_to_registry"]:
            for t in drift["card_to_registry"][:10]:
                print(f"      💀 {t} (in card, not in registry — DEAD NAME)")

        # Emit card
        card = emit_card(name, organ, source_tools, registry_tools, source_hash, drift, args.dry_run, probe_failed)

        report[name] = {
            "source_tools": source_tools,
            "registry_tools": registry_tools,
            "card_tools": card_tools,
            "source_hash": source_hash,
            "drift": drift,
            "admissible": card.get("admissible", False),
        }

    # Summary
    print(f"\n{'=' * 60}")
    print(f"  CARD GENESIS SUMMARY")
    print(f"{'=' * 60}")
    total_source = sum(r["drift"]["source_count"] for r in report.values())
    total_registry = sum(r["drift"]["registry_count"] for r in report.values())
    total_drift = sum(len(r["drift"]["source_to_registry"]) for r in report.values())
    all_admissible = all(r["admissible"] for r in report.values())

    print(f"  Total source tools:  {total_source}")
    print(f"  Total registry tools: {total_registry}")
    print(f"  Total drift:         {total_drift}")
    print(f"  All admissible:      {'✅ YES' if all_admissible else '❌ NO'}")

    if args.json:
        print(f"\n{json.dumps(report, indent=2)}")

    return 0 if all_admissible else 1


if __name__ == "__main__":
    sys.exit(main())
