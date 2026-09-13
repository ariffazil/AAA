#!/usr/bin/env python3
"""
Warga Bootstrap — Seed the registry from canonical federation sources
=====================================================================
Reads AGENTS_UNIFIED.yaml (the SOT) and AAA_AGENTS_REGISTRY.json,
resolves canonical identities, registers all agents into warga.jsonl.

This is Fix 5: "Seed registry before claiming civilization."
This is Fix 3: "Bind agent_id at write time via canonical function."
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import yaml
from canonical_identity import canonicalize, register_alias, save_identity_card
from warga_manager import register_agent, list_agents

# ── Canonical source: AGENTS_UNIFIED.yaml ────────────────────────────────────
UNIFIED_YAML = Path("/root/AAA/registries/AGENTS_UNIFIED.yaml")
FROZEN_JSON = Path("/root/AAA/registries/AAA_AGENTS_REGISTRY.json")
IDENTITY_YAML = Path("/root/AAA/registry/identity.yaml")


def bootstrap() -> dict:
    """Read canonical sources, resolve identities, register into warga."""
    results = {
        "sources_read": [],
        "agents_registered": 0,
        "aliases_registered": 0,
        "conflicts_found": [],
    }

    # ── Step 1: Read AGENTS_UNIFIED.yaml (the SOT) ──────────────────────────
    unified_agents = {}
    if UNIFIED_YAML.exists():
        with open(UNIFIED_YAML) as f:
            d = yaml.safe_load(f)
        results["sources_read"].append("AGENTS_UNIFIED.yaml")

        # identity_lanes (hexagon primary)
        for lane in d.get("identity_lanes", []):
            aid = lane["id"]
            unified_agents[aid] = {
                "id": aid,
                "name": lane.get("name", aid),
                "role": lane.get("role", "unknown"),
                "source": "identity_lanes",
                "status": "active",
                "species": lane.get("species", ""),
            }

        # forge_instruments (FI-xxx)
        for fi in d.get("forge_instruments", []):
            aid = fi["id"]
            unified_agents[aid] = {
                "id": aid,
                "name": fi.get("name", aid),
                "role": fi.get("role", "forge-instrument"),
                "source": "forge_instruments",
                "status": "active",
                "fi_slot": fi.get("fi_slot", ""),
            }

        # extensions
        for ext in d.get("extensions", []):
            aid = ext["id"]
            unified_agents[aid] = {
                "id": aid,
                "name": ext.get("name", aid),
                "role": ext.get("role", "extension"),
                "source": "extensions",
                "status": "active",
            }

        # organs
        for organ in d.get("organs", []):
            aid = organ["id"]
            unified_agents[aid] = {
                "id": aid,
                "name": organ.get("name", aid),
                "role": organ.get("role", "organ"),
                "source": "organs",
                "status": "active",
            }

        # collapsed (dead agents)
        for c in d.get("collapsed", []):
            aid = c["id"]
            unified_agents[aid] = {
                "id": aid,
                "name": c.get("name", aid),
                "role": c.get("role", "collapsed"),
                "source": "collapsed",
                "status": "collapsed",
                "collapsed_into": c.get("collapsed_into", ""),
                "collapse_date": c.get("collapse_date", ""),
            }

    # ── Step 2: Read frozen AAA_AGENTS_REGISTRY.json ────────────────────────
    frozen_agents = {}
    if FROZEN_JSON.exists():
        with open(FROZEN_JSON) as f:
            d = json.load(f)
        results["sources_read"].append("AAA_AGENTS_REGISTRY.json")

        for agent in d.get("agents", []):
            aid = agent.get("id", agent.get("name", "unknown"))
            frozen_agents[aid] = {
                "id": aid,
                "name": agent.get("name", aid),
                "role": agent.get("role", "unknown"),
                "source": "frozen_registry",
                "status": agent.get("status", "unknown"),
                "fi_slot": agent.get("fi_slot", ""),
            }

    # ── Step 3: Register all unified agents into warga ──────────────────────
    for aid, info in unified_agents.items():
        canonical = canonicalize(aid, role=info["role"], source=info["source"])
        save_identity_card(canonical, {
            "role": info["role"],
            "source": info["source"],
            "status": info["status"],
            "name": info.get("name", ""),
            "species": info.get("species", ""),
            "fi_slot": info.get("fi_slot", ""),
            "collapsed_into": info.get("collapsed_into", ""),
        })

        # Register in warga
        stage = "decommissioned" if info["status"] == "collapsed" else "active"
        band = "sovereign-witness" if aid in ("333-AGI", "555-ASI", "888-APEX") else "novice"

        try:
            register_agent(
                agent_id=canonical,
                role=info["role"],
                authority_band=band,
                stage=stage,
                metadata={
                    "source": info["source"],
                    "original_id": aid,
                    "name": info.get("name", ""),
                },
            )
            results["agents_registered"] += 1
        except Exception as e:
            results["conflicts_found"].append({"id": aid, "error": str(e)})

    # ── Step 4: Register frozen-only agents (not in unified) ────────────────
    for aid, info in frozen_agents.items():
        canonical = canonicalize(aid, role=info["role"], source=info["source"])

        # Skip if already registered from unified
        existing = list_agents()
        if any(a["id"] == canonical for a in existing):
            # Register alias
            if aid != canonical:
                register_alias(aid, canonical)
                results["aliases_registered"] += 1
            continue

        save_identity_card(canonical, {
            "role": info["role"],
            "source": info["source"],
            "status": info["status"],
            "name": info.get("name", ""),
            "fi_slot": info.get("fi_slot", ""),
        })

        try:
            register_agent(
                agent_id=canonical,
                role=info["role"],
                authority_band="novice",
                stage="active",
                metadata={
                    "source": info["source"],
                    "original_id": aid,
                    "name": info.get("name", ""),
                },
            )
            results["agents_registered"] += 1
        except Exception as e:
            results["conflicts_found"].append({"id": aid, "error": str(e)})

    # ── Step 5: Register known aliases ──────────────────────────────────────
    known_aliases = {
        "arif_fazil": "arif",
        "Arif": "arif",
        "777-forge": "777-FORGE",
        "geox-personal": "geox",
        "geox-witness": "geox",
        "wealth-witness": "wealth",
        "copilot-cli": "copilot",
        "codex-cli": "codex",
        "kimi-code-fi008": "kimi-code",
        "FI-008": "kimi-code",
        "fi-008": "kimi-code",
    }

    for variant, canonical in known_aliases.items():
        register_alias(variant, canonical)
        results["aliases_registered"] += 1

    return results


if __name__ == "__main__":
    results = bootstrap()
    print(json.dumps(results, indent=2))

    # Show final state
    agents = list_agents()
    print(f"\n=== FINAL STATE: {len(agents)} agents in warga registry ===")
    for a in sorted(agents, key=lambda x: x["id"]):
        status_icon = "💀" if a["stage"] == "decommissioned" else "✅"
        print(f"  {status_icon} {a['id']:25s} │ {a['stage']:15s} │ band={a['authority_band']:18s} │ role={a.get('role','?')[:30]}")
