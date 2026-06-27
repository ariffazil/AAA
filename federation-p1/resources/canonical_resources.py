#!/usr/bin/env python3
"""
canonical_resources.py — The 14 resource families aligned across WEALTH, GEOX, WELL.

Each resource is a URI-based, read-only, versionable data slot.
FastMCP resources are built exactly for this kind of canonical context,
thresholds, registries, and contracts.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

VERSION = "2026.06.28"


def _hash(uri: str) -> str:
    return hashlib.sha256(uri.encode()).hexdigest()[:16]


# ═══════════════════════════════════════════════════════════════════════════
# The 14 Resource Families
# ═══════════════════════════════════════════════════════════════════════════
RESOURCE_FAMILIES = [
    "schema",
    "health",
    "registry",
    "canon",
    "glossary",
    "contract",
    "intake",
    "regime",
    "uncertainty",
    "contradiction",
    "bandwidth",
    "handoff",
    "envelope",
    "receipt",
]


def _make_resource_uri(organ_prefix: str, family: str) -> str:
    """Generate a canonical URI for a resource family."""
    return f"{organ_prefix}://{family}"


def _make_resource_entry(uri: str, mime: str = "application/json") -> dict:
    return {
        "uri": uri,
        "version": VERSION,
        "mime_type": mime,
        "resource_sha256": _hash(uri),
        "read_only": True,
    }


# ═══════════════════════════════════════════════════════════════════════════
# WEALTH RESOURCES — 14 families
# ═══════════════════════════════════════════════════════════════════════════
WEALTH_RESOURCES = {
    "schema": _make_resource_entry("wealth://schema"),
    "health": _make_resource_entry("wealth://health"),
    "registry": _make_resource_entry("wealth://tools/registry"),
    "canon": _make_resource_entry("wealth://canon/index", "text/markdown"),
    "glossary": _make_resource_entry("wealth://glossary", "text/markdown"),
    "contract": _make_resource_entry("wealth://federation/contract", "text/markdown"),
    "intake": _make_resource_entry("wealth://reality/context"),
    "regime": _make_resource_entry("wealth://market/sources"),
    "uncertainty": _make_resource_entry("wealth://risk/thresholds"),
    "contradiction": _make_resource_entry("wealth://affordance/contracts"),
    "bandwidth": _make_resource_entry("wealth://runtime/policy"),
    "handoff": _make_resource_entry("wealth://handoff/arifos-schema"),
    "envelope": _make_resource_entry("wealth://domains/index"),
    "receipt": _make_resource_entry("wealth://replay/receipt-schema"),
}


# ═══════════════════════════════════════════════════════════════════════════
# GEOX RESOURCES — 14 families
# ═══════════════════════════════════════════════════════════════════════════
GEOX_RESOURCES = {
    "schema": _make_resource_entry("geox://capabilities"),
    "health": _make_resource_entry("geox://surface/truth"),
    "registry": _make_resource_entry("geox://resources/index"),
    "canon": _make_resource_entry("geox://literature/index"),
    "glossary": _make_resource_entry("geox://identity"),
    "contract": _make_resource_entry("geox://claims/index"),
    "intake": _make_resource_entry("geox://reality/context"),
    "regime": _make_resource_entry("geox://basins/index"),
    "uncertainty": _make_resource_entry("geox://resources/schemas/index"),
    "contradiction": _make_resource_entry("geox://claims/graph"),
    "bandwidth": _make_resource_entry("geox://resources/playbooks/index"),
    "handoff": _make_resource_entry("geox://resources/prompts/index"),
    "envelope": _make_resource_entry("geox://artifacts/index"),
    "receipt": _make_resource_entry("geox://registry/apps"),
}


# ═══════════════════════════════════════════════════════════════════════════
# WELL RESOURCES — 14 families
# ═══════════════════════════════════════════════════════════════════════════
WELL_RESOURCES = {
    "schema": _make_resource_entry("well://schema"),
    "health": _make_resource_entry("well://vitals/arif"),
    "registry": _make_resource_entry("well://registry"),
    "canon": _make_resource_entry("well://doctrine", "text/plain"),
    "glossary": _make_resource_entry("well://identity", "text/plain"),
    "contract": _make_resource_entry("well://tools/canon_map"),
    "intake": _make_resource_entry("well://state/arif"),
    "regime": _make_resource_entry("well://machine/substrate"),
    "uncertainty": _make_resource_entry("well://sovereign_entropy/arif"),
    "contradiction": _make_resource_entry("well://coupling"),
    "bandwidth": _make_resource_entry("well://decision/classes"),
    "handoff": _make_resource_entry("well://bridge/arifos-kernel"),
    "envelope": _make_resource_entry("well://transport/loop"),
    "receipt": _make_resource_entry("well://events/recent"),
}


# ═══════════════════════════════════════════════════════════════════════════
# RESOURCE CONTENT TEMPLATES — what each resource returns
# ═══════════════════════════════════════════════════════════════════════════
RESOURCE_CONTENT_TEMPLATES = {
    "schema": lambda organ: {
        "organ": organ.upper(),
        "version": VERSION,
        "protocol": "fastmcp",
        "canonical_surface": "tools + resources + prompts",
        "authority_boundary": {
            "wealth": "COMPUTE_ONLY",
            "geox": "EVIDENCE_ONLY",
            "well": "REFLECT_ONLY",
        }.get(organ, "UNKNOWN"),
    },
    "health": lambda organ: {
        "organ": organ.upper(),
        "status": "ALIVE",
        "version": VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    },
    "registry": lambda organ: {
        "organ": organ.upper(),
        "tool_count": 0,  # Populated at runtime
        "resource_count": 0,
        "prompt_count": 0,
        "last_verified": datetime.now(timezone.utc).isoformat(),
    },
    "canon": lambda organ: {
        "organ": organ.upper(),
        "canon_entries": [],
        "version": VERSION,
    },
    "glossary": lambda organ: {
        "organ": organ.upper(),
        "terms": {},
        "version": VERSION,
    },
    "contract": lambda organ: {
        "organ": organ.upper(),
        "position": f"{organ.upper()} organ in the arifOS federation",
        "authority": {
            "wealth": "WEALTH computes. arifOS judges. Arif decides.",
            "geox": "GEOX provides evidence. No drilling authority. No self-seal.",
            "well": "WELL reflects. Does not veto. Does not judge.",
        }.get(organ, "UNKNOWN"),
        "version": VERSION,
    },
    "intake": lambda organ: {
        "organ": organ.upper(),
        "reality_frame": {},
        "freshness_ttl": "5m",
        "version": VERSION,
    },
    "regime": lambda organ: {
        "organ": organ.upper(),
        "regime_type": {
            "wealth": "market",
            "geox": "basin",
            "well": "substrate",
        }.get(organ, "unknown"),
        "current_regime": "UNKNOWN",
        "version": VERSION,
    },
    "uncertainty": lambda organ: {
        "organ": organ.upper(),
        "thresholds": {
            "LOW": 0.3,
            "MEDIUM": 0.6,
            "HIGH": 0.8,
            "CRITICAL": 0.9,
        },
        "confidence_cap": 0.90,
        "version": VERSION,
    },
    "contradiction": lambda organ: {
        "organ": organ.upper(),
        "active_contradictions": [],
        "resolved_count": 0,
        "version": VERSION,
    },
    "bandwidth": lambda organ: {
        "organ": organ.upper(),
        "decision_classes": ["C0", "C1", "C2", "C3", "C4", "C5"],
        "current_class": "C3",
        "version": VERSION,
    },
    "handoff": lambda organ: {
        "organ": organ.upper(),
        "target": "arifos",
        "packet_schema": f"{organ}://handoff/arifos-schema",
        "version": VERSION,
    },
    "envelope": lambda organ: {
        "organ": organ.upper(),
        "envelope_schema": "federation-envelope.schema.json",
        "version": VERSION,
    },
    "receipt": lambda organ: {
        "organ": organ.upper(),
        "receipt_schema": "replay-receipt.schema.json",
        "chain_active": True,
        "version": VERSION,
    },
}


def generate_resource_content(organ: str, family: str) -> dict:
    """Generate the content for a resource family for a given organ."""
    template = RESOURCE_CONTENT_TEMPLATES.get(family)
    if template:
        return template(organ)
    return {"organ": organ, "family": family, "version": VERSION}


# ═══════════════════════════════════════════════════════════════════════════
# REGISTRY
# ═══════════════════════════════════════════════════════════════════════════
ALL_RESOURCES = {
    "wealth": WEALTH_RESOURCES,
    "geox": GEOX_RESOURCES,
    "well": WELL_RESOURCES,
}


if __name__ == "__main__":
    for organ, resources in ALL_RESOURCES.items():
        print(f"\n{organ.upper()} RESOURCES ({len(resources)}):")
        for family, entry in resources.items():
            print(f"  - {family:15s} → {entry['uri']}")
