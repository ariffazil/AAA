#!/usr/bin/env python3
"""
governance_cards — Model Governance Card compiler (runtime wiring Phase 1).

ARIFOS::AAA_MODEL_GOVERNANCE_RUNTIME_WIRING::2026-10-30::v1 (as ratified with the
six JUDGE corrections). Cards are DETERMINISTIC PROJECTIONS of the sealed supply-chain
registry. A card may LOWER confidence; it may NEVER raise authority.

REALITY > EVERYTHING: OBSERVED > DECLARED > REQUESTED > IMAGINED(forbidden).
  resolved_model comes only from a probe receipt — else UNKNOWN.

Card contract: target 1200B / hard max 2048B (fail-closed compaction), ≤ 40 lines
rendered, biography forbidden, probe history forbidden, secrets forbidden.
Cards are LANE-scoped and revision-bound; session binding happens at INIT
(arifOS), not here — a compiled card carries no session_id by design.

DITEMPA BUKAN DIBERI.
"""

from __future__ import annotations

import hashlib
import json
import re

SCHEMA_VERSION = 1
CARD_TARGET_BYTES = 1200
CARD_HARD_MAX_BYTES = 2048

# assignment_id -> lane (the AAA role lane the runtime will request)
LANE_BY_ASSIGNMENT = {
    "aaa-333-coding-primary": "333",
    "aaa-555-verify-lane": "555",
    "aaa-888-judge-lane": "888",
    "aaa-999-seal-lane": "999",
    "forge-000-builder-lane": "forge",
    "hermes-asi-lane": "hermes",
}

# Fields a card must keep even under compaction (in order); everything else
# drops before these do.
_COMPACT_ORDER = [
    "schema_version", "card_id", "lane_id", "registry_revision",
    "requested_model", "resolved_model", "identity_state",
    "route_id", "mutability", "last_probe_state", "failure_domain",
    "eligible_roles", "forbidden_roles", "authority_ceiling", "verdict", "card_hash",
]


def _canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)


def _card_hash(card: dict) -> str:
    clean = {k: v for k, v in card.items() if k != "card_hash"}
    return hashlib.sha256(_canon(clean).encode("utf-8")).hexdigest()


def _latest_probe_for(entities: dict, route_id: str, requested_model: str):
    best = None
    for p in sorted(entities.get("probes", []), key=lambda x: x.get("observed_at", "")):
        if p.get("route_ref") == route_id and p.get("requested_model") == requested_model:
            best = p  # keep overwriting → latest wins
    return best


def _authority_ceiling(assignment: dict) -> dict:
    forbidden = set(assignment.get("forbidden_tasks", []))
    role_class = (assignment.get("independence") or {}).get("role_class", "UNKNOWN")
    return {
        "propose": role_class in ("proposer", "executor"),
        "verify": role_class == "verifier",
        "authorize": False,   # no card ever grants authorization — F13/888 only
        "execute": role_class == "executor" and "production_mutation_without_grant" in forbidden,
    }


def build_card(assignment: dict, entities: dict, meta: dict) -> dict:
    lane = LANE_BY_ASSIGNMENT.get(assignment.get("assignment_id", ""), "UNKNOWN")
    models = assignment.get("allowed_model_refs") or [None]
    routes = assignment.get("allowed_route_refs") or [None]
    requested_model = models[0]
    route_id = routes[0]
    route = next((r for r in entities.get("routes", []) if r.get("route_id") == route_id), {})

    probe = _latest_probe_for(entities, route_id, requested_model) if route_id else None
    resolved = probe.get("resolved_model") if probe else None
    requested = requested_model
    if resolved is not None and requested is not None and resolved == requested:
        identity_state = "matched"
    elif resolved is not None and requested is not None and str(resolved).startswith("fp:"):
        identity_state = "UNRESOLVED"   # fingerprint-only echo — no clean identity
    elif resolved is None:
        identity_state = "UNRESOLVED"
    else:
        identity_state = "MISMATCH"

    fd = route.get("failure_domain") or {}
    verdict = "HOLD" if identity_state in ("UNRESOLVED", "MISMATCH") else (
        "WARN" if identity_state == "classified_remap" else "BOUND")

    card = {
        "schema_version": SCHEMA_VERSION,
        "card_id": f"mgc-{lane}-{(meta.get('source_commit') or 'UNKNOWN')[:10]}",
        "lane_id": lane,
        "registry_revision": meta.get("source_commit", "UNKNOWN"),
        "source_manifest_hash": meta.get("source_manifest_hash"),
        "requested_model": requested,
        "resolved_model": resolved if identity_state in ("matched", "MISMATCH") else (
            resolved if resolved else "UNKNOWN"),
        "identity_state": identity_state,
        "resolution_evidence_ref": probe.get("probe_id") if probe else None,
        "route_id": route_id,
        "mutability": route.get("mutability_class", "UNKNOWN"),
        "last_probe_state": (probe.get("verdict") if probe else "NONE"),
        "failure_domain": "/".join(str(x) for x in filter(None, [fd.get("provider"), fd.get("endpoint_cluster"), fd.get("account")])) or "UNKNOWN",
        "eligible_roles": assignment.get("allowed_tasks", []),
        "forbidden_roles": assignment.get("forbidden_tasks", []),
        "tool_policy_ref": "policies/independence-verification-v1",
        "memory_policy_ref": "registry/docs/RUNTIME_WIRING.md#producer-context",
        "authority_ceiling": _authority_ceiling(assignment),
        "knowledge": {"cutoff": "UNKNOWN", "current_fact_policy": "retrieve_and_cite"},
        "verdict": verdict,
    }
    return card


def _compact(card: dict) -> dict:
    """Fail-closed compaction: drop optional fields until under hard max."""
    card = dict(card)
    optional = [k for k in card if k not in _COMPACT_ORDER]
    for key in optional + [k for k in reversed(_COMPACT_ORDER) if k not in ("schema_version", "card_id", "lane_id", "registry_revision", "card_hash", "verdict", "identity_state", "resolved_model", "requested_model")]:
        if len(_canon(card).encode("utf-8")) <= CARD_HARD_MAX_BYTES:
            break
        if key in card:
            card.pop(key, None)
    return card


def finalize_card(card: dict) -> dict:
    card = dict(card)
    card.pop("card_hash", None)
    raw = len(_canon(card).encode("utf-8"))
    if raw > CARD_HARD_MAX_BYTES:
        card = _compact(card)
    if len(_canon(card).encode("utf-8")) > CARD_HARD_MAX_BYTES:
        raise ValueError(f"card {card.get('lane_id')} exceeds hard max after compaction")
    card["card_hash"] = _card_hash(card)
    if len(_canon(card).encode("utf-8")) > CARD_HARD_MAX_BYTES:
        raise ValueError(f"card {card.get('lane_id')} exceeds hard max after hash")
    return card


def build_cards(entities: dict, meta: dict) -> dict[str, dict]:
    cards: dict[str, dict] = {}
    for a in entities.get("assignments", []):
        lane = LANE_BY_ASSIGNMENT.get(a.get("assignment_id", ""))
        if not lane:
            continue
        cards[lane] = finalize_card(build_card(a, entities, meta))
    return cards


def render_yaml(card: dict) -> str:
    """Compact, deterministic YAML-ish rendering (≤40 lines target)."""
    lines = [f"{k}: {json.dumps(v, ensure_ascii=False, default=str) if not isinstance(v, str) else v}"
             for k, v in card.items()]
    return "\n".join(lines) + "\n"


def unknown_lane_card(lane: str, reason: str) -> dict:
    """Fail-closed card for a lane with no assignment — never an empty card."""
    card = {
        "schema_version": SCHEMA_VERSION,
        "card_id": f"mgc-{lane}-UNKNOWN",
        "lane_id": lane,
        "registry_revision": "UNKNOWN",
        "requested_model": None,
        "resolved_model": "UNKNOWN",
        "identity_state": "UNRESOLVED",
        "route_id": None,
        "verdict": "HOLD",
        "note": reason,
        "authority_ceiling": {"propose": False, "verify": False, "authorize": False, "execute": False},
    }
    card["card_hash"] = _card_hash(card)
    return card
