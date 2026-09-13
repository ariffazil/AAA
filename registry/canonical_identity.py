#!/usr/bin/env python3
"""
Canonical Agent Identity — arifOS Federation
=============================================
Single source of truth for agent identity resolution.
Every agent_id passes through canonicalize() before any write.

The problem: the same agent has 7 different spellings across 6 registries.
This module resolves ALL of them to ONE canonical ID.

Schema: arifos.canonical_identity.v1
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

# ── Canonical paths ──────────────────────────────────────────────────────────
REGISTRY_DIR = Path("/root/AAA/registry")
CANONICAL_MAP_FILE = REGISTRY_DIR / "canonical_identity.json"
ALIAS_MAP_FILE = REGISTRY_DIR / "alias_map.json"

# ── Hard-coded known aliases ────────────────────────────────────────────────
# These are the REAL identity conflicts found in the federation.
# Format: variant → canonical_id
# Populated by audit, not by guesswork.
KNOWN_ALIASES: dict[str, str] = {
    # Will be populated from audit results
}

# ── Normalization rules ─────────────────────────────────────────────────────
def _normalize(s: str) -> str:
    """Strip, lowercase, collapse whitespace/underscores/hyphens."""
    if not s:
        return "unknown"
    s = str(s).strip().lower()
    s = re.sub(r'[\s_]+', '-', s)          # whitespace/underscores → hyphen
    s = re.sub(r'-+', '-', s)              # collapse multiple hyphens
    s = re.sub(r'^-|-$', '', s)            # strip leading/trailing hyphens
    return s


def _hash_identity(canonical_id: str, role: str, source: str) -> str:
    """Deterministic hash for a canonical identity."""
    content = f"{canonical_id}|{role}|{source}"
    return hashlib.sha256(content.encode()).hexdigest()[:16]


# ── Core resolution ─────────────────────────────────────────────────────────
def load_alias_map() -> dict[str, str]:
    """Load the persistent alias map."""
    if ALIAS_MAP_FILE.exists():
        try:
            return json.loads(ALIAS_MAP_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def save_alias_map(alias_map: dict[str, str]) -> None:
    """Persist the alias map."""
    REGISTRY_DIR.mkdir(parents=True, exist_ok=True)
    ALIAS_MAP_FILE.write_text(json.dumps(alias_map, indent=2, sort_keys=True))


def canonicalize(agent_id: str, role: str = "unknown", source: str = "unknown") -> str:
    """
    Resolve any agent_id variant to its canonical form.
    
    Resolution order:
    1. Exact match in KNOWN_ALIASES (hard-coded from audit)
    2. Normalized match in alias_map (learned from previous resolutions)
    3. New identity — register it and return canonical form
    
    Returns: canonical_id string
    """
    alias_map = load_alias_map()
    
    # Step 1: Check hard-coded aliases
    if not agent_id:
        return "unknown"
    if agent_id in KNOWN_ALIASES:
        canonical = KNOWN_ALIASES[agent_id]
        # Also learn the normalized variant
        normalized = _normalize(agent_id)
        if normalized not in alias_map:
            alias_map[normalized] = canonical
            save_alias_map(alias_map)
        return canonical
    
    # Step 2: Check learned aliases (normalized lookup)
    normalized = _normalize(agent_id)
    if normalized in alias_map:
        return alias_map[normalized]
    
    # Step 3: Check if any existing alias maps to a known canonical
    for variant, canonical in alias_map.items():
        if _normalize(variant) == normalized:
            return canonical
    
    # Step 4: New identity — this IS the canonical form
    # Register the normalized form as canonical
    if normalized not in alias_map:
        alias_map[normalized] = normalized
        save_alias_map(alias_map)
    
    return normalized


def register_alias(variant: str, canonical_id: str) -> dict:
    """Explicitly register a variant as an alias of a canonical ID."""
    alias_map = load_alias_map()
    
    # Don't allow circular references
    if canonical_id in alias_map and alias_map[canonical_id] != canonical_id:
        # canonical_id is itself an alias — resolve it
        canonical_id = alias_map[canonical_id]
    
    alias_map[_normalize(variant)] = canonical_id
    save_alias_map(alias_map)
    
    return {
        "status": "alias_registered",
        "variant": variant,
        "normalized": _normalize(variant),
        "canonical_id": canonical_id,
    }


def resolve_all(agent_ids: list[str]) -> dict[str, str]:
    """Resolve a batch of agent IDs to their canonical forms.
    Returns: {original_id: canonical_id}
    """
    return {aid: canonicalize(aid) for aid in agent_ids}


def get_identity_card(canonical_id: str) -> dict | None:
    """Get the canonical identity card for an agent."""
    if CANONICAL_MAP_FILE.exists():
        try:
            cards = json.loads(CANONICAL_MAP_FILE.read_text())
            return cards.get(canonical_id)
        except (json.JSONDecodeError, OSError):
            pass
    return None


def save_identity_card(canonical_id: str, card: dict) -> None:
    """Save a canonical identity card."""
    REGISTRY_DIR.mkdir(parents=True, exist_ok=True)
    cards = {}
    if CANONICAL_MAP_FILE.exists():
        try:
            cards = json.loads(CANONICAL_MAP_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    cards[canonical_id] = card
    CANONICAL_MAP_FILE.write_text(json.dumps(cards, indent=2, sort_keys=True))


def list_identities() -> list[dict]:
    """List all canonical identity cards."""
    if CANONICAL_MAP_FILE.exists():
        try:
            cards = json.loads(CANONICAL_MAP_FILE.read_text())
            return [{"canonical_id": k, **v} for k, v in cards.items()]
        except (json.JSONDecodeError, OSError):
            pass
    return []


def bootstrap_from_federation() -> dict:
    """
    Scan all known federation registries and build canonical identity map.
    This is the "seed registry before claiming civilization" step.
    """
    results = {
        "scanned_systems": [],
        "total_agents_found": 0,
        "canonical_identities": [],
        "conflicts_found": [],
    }
    
    # System 1: forge_agent (look for agent cards in A-FORGE)
    aforge_reg = Path("/root/A-FORGE/registry")
    if aforge_reg.exists():
        for f in aforge_reg.glob("*.json"):
            try:
                data = json.loads(f.read_text())
                agent_id = data.get("agent_id") or data.get("id") or data.get("name", f.stem)
                role = data.get("role", "unknown")
                canonical = canonicalize(agent_id, role=role, source="forge_agent")
                save_identity_card(canonical, {
                    "role": role,
                    "source": "forge_agent",
                    "source_file": str(f),
                    "created_at": data.get("created_at"),
                    "status": data.get("status", "unknown"),
                })
                results["canonical_identities"].append({"id": agent_id, "canonical": canonical, "source": "forge_agent"})
            except (json.JSONDecodeError, OSError):
                continue
        results["scanned_systems"].append({"system": "forge_agent", "path": str(aforge_reg), "agents": len(results["canonical_identities"])})
    
    # System 2: AAA registry (identity.yaml)
    aaa_identity = Path("/root/AAA/registry/identity.yaml")
    if aaa_identity.exists():
        try:
            import yaml
            data = yaml.safe_load(aaa_identity.read_text())
            if isinstance(data, dict):
                for k, v in data.items():
                    if isinstance(v, dict):
                        agent_id = v.get("id") or v.get("name") or k
                        role = v.get("role", "unknown")
                        canonical = canonicalize(agent_id, role=role, source="aaa_identity")
                        save_identity_card(canonical, {
                            "role": role,
                            "source": "aaa_identity",
                            "source_file": str(aaa_identity),
                            **v,
                        })
                        results["canonical_identities"].append({"id": agent_id, "canonical": canonical, "source": "aaa_identity"})
        except Exception:
            pass
        results["scanned_systems"].append({"system": "aaa_identity", "path": str(aaa_identity)})
    
    # System 3: arifOS registry
    arifos_reg = Path("/root/arifOS/registry")
    if arifos_reg.exists():
        for f in arifos_reg.glob("*.json"):
            try:
                data = json.loads(f.read_text())
                agent_id = data.get("agent_id") or data.get("id") or f.stem
                canonical = canonicalize(agent_id, source="arifos_registry")
                save_identity_card(canonical, {
                    "source": "arifos_registry",
                    "source_file": str(f),
                    **data,
                })
                results["canonical_identities"].append({"id": agent_id, "canonical": canonical, "source": "arifos_registry"})
            except (json.JSONDecodeError, OSError):
                continue
        results["scanned_systems"].append({"system": "arifos_registry", "path": str(arifos_reg)})
    
    # System 4: GEOX cards
    geox_cards = Path("/root/GEOX/registry")
    if geox_cards.exists():
        for f in geox_cards.glob("*.json"):
            try:
                data = json.loads(f.read_text())
                agent_id = data.get("agent_id") or data.get("id") or f.stem
                canonical = canonicalize(agent_id, source="geox_cards")
                save_identity_card(canonical, {
                    "source": "geox_cards",
                    "source_file": str(f),
                    **data,
                })
                results["canonical_identities"].append({"id": agent_id, "canonical": canonical, "source": "geox_cards"})
            except (json.JSONDecodeError, OSError):
                continue
        results["scanned_systems"].append({"system": "geox_cards", "path": str(geox_cards)})
    
    # System 5: arifFlow lanes
    arifflow_reg = Path("/root/AAA/registry/arifflow_lanes.json")
    if arifflow_reg.exists():
        try:
            data = json.loads(arifflow_reg.read_text())
            # Process lanes
        except (json.JSONDecodeError, OSError):
            pass
    
    results["total_agents_found"] = len(results["canonical_identities"])
    
    # Detect conflicts (same canonical ID from multiple sources)
    canonical_sources = {}
    for entry in results["canonical_identities"]:
        cid = entry["canonical"]
        if cid not in canonical_sources:
            canonical_sources[cid] = set()
        canonical_sources[cid].add(entry["source"])
    
    for cid, sources in canonical_sources.items():
        if len(sources) > 1:
            results["conflicts_found"].append({
                "canonical_id": cid,
                "sources": list(sources),
                "conflict_type": "multi_source",
            })
    
    return results


# ── CLI ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Canonical Agent Identity")
    sub = parser.add_subparsers(dest="command")
    
    p_resolve = sub.add_parser("resolve", help="Resolve agent ID to canonical form")
    p_resolve.add_argument("agent_id")
    p_resolve.add_argument("--role", default="unknown")
    p_resolve.add_argument("--source", default="cli")
    
    p_alias = sub.add_parser("alias", help="Register an alias")
    p_alias.add_argument("variant")
    p_alias.add_argument("canonical_id")
    
    p_list = sub.add_parser("list", help="List all canonical identities")
    
    p_bootstrap = sub.add_parser("bootstrap", help="Scan federation and build identity map")
    
    p_card = sub.add_parser("card", help="Get identity card")
    p_card.add_argument("canonical_id")
    
    args = parser.parse_args()
    
    if args.command == "resolve":
        canonical = canonicalize(args.agent_id, role=args.role, source=args.source)
        print(json.dumps({"input": args.agent_id, "canonical": canonical}, indent=2))
    elif args.command == "alias":
        result = register_alias(args.variant, args.canonical_id)
        print(json.dumps(result, indent=2))
    elif args.command == "list":
        identities = list_identities()
        for i in identities:
            print(json.dumps(i, indent=2))
    elif args.command == "bootstrap":
        result = bootstrap_from_federation()
        print(json.dumps(result, indent=2, default=str))
    elif args.command == "card":
        card = get_identity_card(args.canonical_id)
        if card:
            print(json.dumps({"canonical_id": args.canonical_id, **card}, indent=2))
        else:
            print(f"No identity card for: {args.canonical_id}")
    else:
        parser.print_help()
