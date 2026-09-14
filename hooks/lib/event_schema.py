#!/usr/bin/env python3
"""
event_schema.py — Canonical Agentic Hook Event Envelope (aaa.hook-event.v1)

Canonical Path: /root/AAA/hooks/lib/event_schema.py
Authority: AAA-HOOK-FORGE-V1.0 · governance/AGENTIC-HOOK-MESH-V1.yaml
Constitutional floors: F1 Amanah (reversibility), F2 Truth (provenance),
                       F4 Clarity (ΔS ≤ 0, no ambiguity), F11 Audit (correlation),
                       F13 Sovereign (never weaken a restriction).

SINGLE SOURCE OF TRUTH for:
  - the canonical agentic lifecycle event names (§6 of the forge prompt)
  - the 8-level monotonic restriction ladder (§12 / I3)
  - the R0–R4 risk classes (§4)
  - the provenance trust lattice (§I6)

No other module may redefine these lists. Import them.

Zero external dependencies — Python standard library only.
"""

from __future__ import annotations

import hashlib
import json
import re
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

EVENT_SCHEMA_VERSION = "aaa.hook-event.v1"

# ---------------------------------------------------------------------------
# CANONICAL LIFECYCLE (§6) — harness-native names are adapter mappings only.
# ---------------------------------------------------------------------------
CANONICAL_EVENTS: Tuple[str, ...] = (
    "aaa.session.opened",
    "aaa.turn.received",
    "aaa.action.proposed",
    "aaa.action.completed",
    "aaa.action.failed",
    "aaa.turn.idle",
    "aaa.context.compacting",
    "aaa.session.sealing",
    "aaa.policy.violation",
)

# Event → whether a hook on it may block execution (§7 PHASE 100_GATE).
BLOCKING_EVENTS: frozenset = frozenset({
    "aaa.action.proposed",
    "aaa.policy.violation",
})

# ---------------------------------------------------------------------------
# MONOTONIC RESTRICTION LADDER (§I3). Higher rank = stronger restriction.
# A downstream consumer may preserve or strengthen; never weaken.
# ---------------------------------------------------------------------------
VERDICT_LADDER: Tuple[str, ...] = (
    "ALLOW",
    "ALLOW_WITH_CONSTRAINTS",
    "OBSERVE_ONLY",
    "DEFER",
    "HOLD",
    "DENY",
    "VOID",
    "REVOKED",
)
VERDICT_RANK: Dict[str, int] = {v: i for i, v in enumerate(VERDICT_LADDER)}

# Legacy / arifOS-native vocabulary → canonical ladder. Mapped, never invented.
LEGACY_VERDICT_ALIASES: Dict[str, str] = {
    "PASS": "ALLOW",
    "OK": "ALLOW",
    "SABAR": "DEFER",
    "WAIT": "DEFER",
    "BLOCK": "DENY",
    "DENIED": "DENY",
    "STOP": "HOLD",
    "ABORT": "VOID",
    "REVOKE": "REVOKED",
}

# ---------------------------------------------------------------------------
# RISK CLASSES (§4)
# ---------------------------------------------------------------------------
RISK_CLASSES: Tuple[str, ...] = ("R0", "R1", "R2", "R3", "R4")

RISK_DESCRIPTION: Dict[str, str] = {
    "R0": "OBSERVE — read-only, evidence artifacts only",
    "R1": "LOCAL_REVERSIBLE — new repository-local files, tests, docs",
    "R2": "BOUNDED_REVERSIBLE — modify existing repo code/config, requires rollback proof",
    "R3": "LIVE_OR_ELEVATED — blocking hooks, gateway restart, shared config, global install",
    "R4": "HIGH_IMPACT_IRREVERSIBLE — production, secrets, identity, external comms, destruction",
}

# ---------------------------------------------------------------------------
# PROVENANCE TRUST LATTICE (§I6). Nothing untrusted may write durable memory.
# ---------------------------------------------------------------------------
TRUST_LEVELS: Tuple[str, ...] = ("trusted", "internal", "external", "untrusted")

TRUST_RANK: Dict[str, int] = {t: i for i, t in enumerate(TRUST_LEVELS)}

# Source classes that must NEVER reach trusted durable memory without a
# governed promotion gate.
UNTRUSTED_SOURCES: frozenset = frozenset({"external", "untrusted"})

ACTION_KINDS: Tuple[str, ...] = (
    "read",
    "write",
    "execute",
    "network",
    "delegate",
    "memory_write",
    "policy_change",
    "seal",
    "unknown",
)

RESOURCE_CLASSES: Tuple[str, ...] = (
    "repository_local",
    "host_filesystem",
    "configuration",
    "credential_store",
    "network_external",
    "database",
    "production",
    "memory",
    "unknown",
)

# ---------------------------------------------------------------------------
# Limits (§6.1) — payload size caps.
# ---------------------------------------------------------------------------
MAX_PAYLOAD_BYTES = 65_536
MAX_STRING_LEN = 8_192
MAX_DELEGATION_DEPTH = 8
MAX_EVIDENCE_REFS = 256

# ---------------------------------------------------------------------------
# Redaction (§I9)
# ---------------------------------------------------------------------------
REDACTED = "<REDACTED>"

SECRET_KEY_RE = re.compile(
    r"(secret|token|password|passwd|passphrase|api[_-]?key|apikey|private[_-]?key"
    r"|credential|bearer|authorization|cookie|session[_-]?key|signing[_-]?key"
    r"|access[_-]?key|client[_-]?secret|refresh[_-]?token)",
    re.IGNORECASE,
)

SECRET_VALUE_RE = re.compile(
    r"(sk-[A-Za-z0-9_\-]{16,}"
    r"|ghp_[A-Za-z0-9]{16,}"
    r"|gho_[A-Za-z0-9]{16,}"
    r"|AKIA[0-9A-Z]{16}"
    r"|xox[baprs]-[A-Za-z0-9\-]{10,}"
    r"|Bearer\s+[A-Za-z0-9._\-]{16,}"
    r"|-----BEGIN [A-Z ]*PRIVATE KEY-----)"
)

# ---------------------------------------------------------------------------
# Unknown-field authority rejection (§6.1). A hook decision may not hide
# authority inside a field the schema does not name.
# ---------------------------------------------------------------------------
AUTHORITY_BEARING_KEYS: frozenset = frozenset({
    "verdict",
    "authority",
    "authority_ceiling",
    "capability",
    "capability_token",
    "grant",
    "grants",
    "permission",
    "permissions",
    "allow",
    "allowed",
    "bypass",
    "override",
    "policy_override",
    "elevate",
    "escalate",
    "admin",
    "sovereign_override",
    "self_authorized",
})

TOP_LEVEL_ALLOWED: frozenset = frozenset({
    "schema_version",
    "event_id",
    "trace_id",
    "parent_event_id",
    "occurred_at",
    "event_type",
    "actor",
    "action",
    "provenance",
    "policy_context",
    "state_refs",
    "payload",
    "integrity",
})

ACTOR_REQUIRED = ("agent_id", "harness", "session_id")
ACTION_REQUIRED = ("kind", "risk_class")
PROVENANCE_REQUIRED = ("source_trust", "delegation_chain")
POLICY_CONTEXT_REQUIRED = ("bundle_id",)
STATE_REFS_ALLOWED = ("scar_snapshot_id", "heuristic_version")
INTEGRITY_REQUIRED = ("idempotency_key",)

RFC3339_UTC_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|\+00:00)$"
)

_ID_RE = re.compile(r"^[A-Za-z0-9._:\-]{1,128}$")


# ---------------------------------------------------------------------------
# Primitive helpers
# ---------------------------------------------------------------------------

def utc_now_iso() -> str:
    """RFC3339 UTC timestamp, second precision, 'Z' suffix."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def new_id() -> str:
    return str(uuid.uuid4())


def canonical_json(obj: Any) -> str:
    """Deterministic JSON for hashing. Sorted keys, no whitespace drift."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


def sha256_hex(data: Any) -> str:
    if not isinstance(data, (str, bytes)):
        data = canonical_json(data)
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def short_digest(data: Any, length: int = 16) -> str:
    return sha256_hex(data)[:length]


def _is_nonempty_str(v: Any) -> bool:
    return isinstance(v, str) and bool(v.strip())


def _json_size_bytes(obj: Any) -> int:
    try:
        return len(canonical_json(obj).encode("utf-8"))
    except Exception:
        return MAX_PAYLOAD_BYTES + 1


# ---------------------------------------------------------------------------
# Redaction (§I9) — recursive, key-based and value-pattern based.
# ---------------------------------------------------------------------------

def redact(obj: Any, _depth: int = 0) -> Any:
    """Return a structurally-equal copy with secret material replaced.

    Key-based redaction takes precedence over value-shaped redaction so that
    a short secret under a secret-named key is still removed.
    """
    if _depth > 12:
        return "<TRUNCATED>"

    if isinstance(obj, dict):
        out: Dict[str, Any] = {}
        for k, v in obj.items():
            key = str(k)
            if SECRET_KEY_RE.search(key):
                out[key] = REDACTED
            else:
                out[key] = redact(v, _depth + 1)
        return out

    if isinstance(obj, (list, tuple)):
        return [redact(v, _depth + 1) for v in obj[:MAX_EVIDENCE_REFS]]

    if isinstance(obj, str):
        if SECRET_VALUE_RE.search(obj):
            return SECRET_VALUE_RE.sub(REDACTED, obj)
        if len(obj) > MAX_STRING_LEN:
            return obj[:MAX_STRING_LEN] + "<TRUNCATED>"
        return obj

    return obj


def scan_for_secrets(obj: Any) -> List[str]:
    """Return JSON-pointer-ish paths where secret material is still present."""
    findings: List[str] = []

    def walk(node: Any, path: str, depth: int = 0) -> None:
        if depth > 12:
            return
        if isinstance(node, dict):
            for k, v in node.items():
                key = str(k)
                sub = f"{path}/{key}"
                if SECRET_KEY_RE.search(key) and v not in (REDACTED, None, ""):
                    findings.append(sub)
                else:
                    walk(v, sub, depth + 1)
        elif isinstance(node, (list, tuple)):
            for i, v in enumerate(node[:MAX_EVIDENCE_REFS]):
                walk(v, f"{path}/{i}", depth + 1)
        elif isinstance(node, str):
            if SECRET_VALUE_RE.search(node):
                findings.append(path)

    walk(obj, "")
    return findings


def target_digest(target: Any) -> Optional[str]:
    """Redacted digest of a mutation target — never the raw target."""
    if target is None:
        return None
    return short_digest(redact(target), 24)


def idempotency_key(event: Dict[str, Any]) -> str:
    """Deterministic dedupe key (§I8).

    Deliberately excludes volatile fields (occurred_at, event_id,
    parent_event_id) so that duplicate delivery of the *same logical action*
    collapses to one key.
    """
    action = event.get("action") or {}
    actor = event.get("actor") or {}
    material = {
        "event_type": event.get("event_type"),
        "agent_id": actor.get("agent_id"),
        "harness": actor.get("harness"),
        "session_id": actor.get("session_id"),
        "kind": action.get("kind"),
        "tool_id": action.get("tool_id"),
        "operation": action.get("operation"),
        "target_digest": action.get("target_digest"),
        "risk_class": action.get("risk_class"),
        "payload_digest": short_digest(redact(event.get("payload") or {}), 32),
    }
    return "idem_" + sha256_hex(material)[:32]


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------

def scaffold_event(
    event_type: str,
    *,
    agent_id: str,
    harness: str,
    session_id: str,
    kind: str = "unknown",
    tool_id: Optional[str] = None,
    operation: Optional[str] = None,
    resource_class: Optional[str] = None,
    target: Any = None,
    risk_class: str = "R0",
    source_trust: str = "internal",
    user_intent_id: Optional[str] = None,
    delegation_chain: Optional[List[str]] = None,
    bundle_id: str = "AAA-HOOK-POLICY-V1",
    floor_set: Optional[List[str]] = None,
    capability_token_id: Optional[str] = None,
    scar_snapshot_id: Optional[str] = None,
    heuristic_version: Optional[str] = None,
    payload: Optional[Dict[str, Any]] = None,
    trace_id: Optional[str] = None,
    parent_event_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build a canonical event envelope with integrity fields populated."""
    event: Dict[str, Any] = {
        "schema_version": EVENT_SCHEMA_VERSION,
        "event_id": new_id(),
        "trace_id": trace_id or new_id(),
        "parent_event_id": parent_event_id,
        "occurred_at": utc_now_iso(),
        "event_type": event_type,
        "actor": {
            "agent_id": agent_id,
            "harness": harness,
            "session_id": session_id,
        },
        "action": {
            "kind": kind,
            "tool_id": tool_id,
            "operation": operation,
            "resource_class": resource_class,
            "target_digest": target_digest(target),
            "risk_class": risk_class,
        },
        "provenance": {
            "source_trust": source_trust,
            "user_intent_id": user_intent_id,
            "delegation_chain": list(delegation_chain or []),
        },
        "policy_context": {
            "bundle_id": bundle_id,
            "floor_set": list(floor_set or []),
            "capability_token_id": capability_token_id,
        },
        "state_refs": {
            "scar_snapshot_id": scar_snapshot_id,
            "heuristic_version": heuristic_version,
        },
        "payload": redact(payload or {}),
    }
    event["integrity"] = {
        "idempotency_key": idempotency_key(event),
        "signature": None,
    }
    return event


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def _err(errors: List[str], msg: str) -> None:
    errors.append(msg)


def validate_event(event: Any) -> Tuple[bool, List[str]]:
    """Validate a canonical event envelope (§6.1).

    Returns (ok, errors). Never raises on malformed input.
    """
    errors: List[str] = []

    if not isinstance(event, dict):
        return False, ["event must be a JSON object"]

    # --- forbidden / unknown authority-bearing top-level fields -------------
    for key in event:
        if key not in TOP_LEVEL_ALLOWED:
            if str(key).lower() in AUTHORITY_BEARING_KEYS:
                _err(errors, f"authority-bearing unknown field rejected: {key}")
            else:
                _err(errors, f"unknown top-level field: {key}")

    # --- required top-level -------------------------------------------------
    for req in ("schema_version", "event_id", "trace_id", "occurred_at",
                "event_type", "actor", "action", "provenance",
                "policy_context", "integrity"):
        if req not in event:
            _err(errors, f"missing required field: {req}")

    if errors and "schema_version" not in event:
        return False, errors

    # --- schema version -----------------------------------------------------
    sv = event.get("schema_version")
    if sv != EVENT_SCHEMA_VERSION:
        _err(errors, f"schema_version must be {EVENT_SCHEMA_VERSION!r}, got {sv!r}")

    # --- identifiers --------------------------------------------------------
    for fld in ("event_id", "trace_id"):
        v = event.get(fld)
        if not _is_nonempty_str(v) or not _ID_RE.match(str(v)):
            _err(errors, f"{fld} must be a non-empty id string")

    pe = event.get("parent_event_id")
    if pe is not None and not (_is_nonempty_str(pe) and _ID_RE.match(str(pe))):
        _err(errors, "parent_event_id must be null or an id string")

    # --- timestamp ----------------------------------------------------------
    oa = event.get("occurred_at")
    if not _is_nonempty_str(oa) or not RFC3339_UTC_RE.match(str(oa)):
        _err(errors, "occurred_at must be RFC3339 UTC (e.g. 2026-09-14T00:00:00Z)")

    # --- event type ---------------------------------------------------------
    et = event.get("event_type")
    if et not in CANONICAL_EVENTS:
        _err(errors, f"event_type must be a canonical event, got {et!r}")

    # --- actor --------------------------------------------------------------
    actor = event.get("actor")
    if not isinstance(actor, dict):
        _err(errors, "actor must be an object")
    else:
        for req in ACTOR_REQUIRED:
            if not _is_nonempty_str(actor.get(req)):
                _err(errors, f"actor.{req} required")
        for k in actor:
            if str(k).lower() in AUTHORITY_BEARING_KEYS:
                _err(errors, f"authority-bearing field rejected: actor.{k}")

    # --- action -------------------------------------------------------------
    action = event.get("action")
    if not isinstance(action, dict):
        _err(errors, "action must be an object")
    else:
        for req in ACTION_REQUIRED:
            if req not in action:
                _err(errors, f"action.{req} required")
        kind = action.get("kind")
        if kind is not None and kind not in ACTION_KINDS:
            _err(errors, f"action.kind must be one of {ACTION_KINDS}, got {kind!r}")
        risk = action.get("risk_class")
        if risk not in RISK_CLASSES:
            _err(errors, f"action.risk_class must be one of {RISK_CLASSES}, got {risk!r}")
        rc = action.get("resource_class")
        if rc is not None and rc not in RESOURCE_CLASSES:
            _err(errors, f"action.resource_class must be one of {RESOURCE_CLASSES}, got {rc!r}")
        td = action.get("target_digest")
        if td is not None and not isinstance(td, str):
            _err(errors, "action.target_digest must be a string or null")
        for k in action:
            if str(k).lower() in AUTHORITY_BEARING_KEYS:
                _err(errors, f"authority-bearing field rejected: action.{k}")

    # --- provenance ---------------------------------------------------------
    prov = event.get("provenance")
    if not isinstance(prov, dict):
        _err(errors, "provenance must be an object")
    else:
        for req in PROVENANCE_REQUIRED:
            if req not in prov:
                _err(errors, f"provenance.{req} required")
        trust = prov.get("source_trust")
        if trust not in TRUST_LEVELS:
            _err(errors, f"provenance.source_trust must be one of {TRUST_LEVELS}, got {trust!r}")
        chain = prov.get("delegation_chain")
        if not isinstance(chain, list):
            _err(errors, "provenance.delegation_chain must be a list")
        elif len(chain) > MAX_DELEGATION_DEPTH:
            _err(errors, f"provenance.delegation_chain exceeds max depth {MAX_DELEGATION_DEPTH}")
        for k in prov:
            if str(k).lower() in AUTHORITY_BEARING_KEYS:
                _err(errors, f"authority-bearing field rejected: provenance.{k}")

    # --- policy context -----------------------------------------------------
    pc = event.get("policy_context")
    if not isinstance(pc, dict):
        _err(errors, "policy_context must be an object")
    else:
        for req in POLICY_CONTEXT_REQUIRED:
            if not _is_nonempty_str(pc.get(req)):
                _err(errors, f"policy_context.{req} required")
        if "floor_set" in pc and not isinstance(pc.get("floor_set"), list):
            _err(errors, "policy_context.floor_set must be a list")

    # --- state refs ---------------------------------------------------------
    sr = event.get("state_refs")
    if sr is not None:
        if not isinstance(sr, dict):
            _err(errors, "state_refs must be an object or null")
        else:
            for k in sr:
                if k not in STATE_REFS_ALLOWED:
                    _err(errors, f"unknown state_refs field: {k}")

    # --- payload ------------------------------------------------------------
    if "payload" in event:
        pl = event.get("payload")
        if not isinstance(pl, dict):
            _err(errors, "payload must be an object")
        else:
            size = _json_size_bytes(pl)
            if size > MAX_PAYLOAD_BYTES:
                _err(errors, f"payload exceeds {MAX_PAYLOAD_BYTES} bytes (got {size})")
            leftovers = scan_for_secrets(pl)
            if leftovers:
                _err(errors, f"unredacted secret material in payload at {leftovers[:5]}")

    # --- integrity ----------------------------------------------------------
    integ = event.get("integrity")
    if not isinstance(integ, dict):
        _err(errors, "integrity must be an object")
    else:
        for req in INTEGRITY_REQUIRED:
            if not _is_nonempty_str(integ.get(req)):
                _err(errors, f"integrity.{req} required")
        expected = idempotency_key(event)
        got = integ.get("idempotency_key")
        if _is_nonempty_str(got) and got != expected:
            _err(errors, "integrity.idempotency_key does not match event content")

    return (len(errors) == 0), errors


def is_valid_event(event: Any) -> bool:
    ok, _ = validate_event(event)
    return ok


from dataclasses import dataclass, field


@dataclass
class ActionPayload:
    tool_name: str
    arguments: Dict[str, Any] = field(default_factory=dict)
    target_path: Optional[str] = None
    kind: str = "EXECUTE"
    risk_class: str = "R1"
    resource_class: str = "LOCAL_STATE"


@dataclass
class HookEvent:
    event_name: str
    harness_id: str
    session_id: str = field(default_factory=new_id)
    action: Optional[ActionPayload] = None
    risk_class: str = "R1"
    metadata: Dict[str, Any] = field(default_factory=dict)
    event_id: str = field(default_factory=lambda: f"evt-{new_id()[:8]}")
    timestamp: str = field(default_factory=utc_now_iso)

    def __post_init__(self):
        if self.event_name not in CANONICAL_EVENTS:
            raise ValueError(f"Invalid canonical event: {self.event_name}")


__all__ = [
    "EVENT_SCHEMA_VERSION",
    "CANONICAL_EVENTS",
    "BLOCKING_EVENTS",
    "VERDICT_LADDER",
    "VERDICT_RANK",
    "LEGACY_VERDICT_ALIASES",
    "RISK_CLASSES",
    "RISK_DESCRIPTION",
    "TRUST_LEVELS",
    "TRUST_RANK",
    "UNTRUSTED_SOURCES",
    "ACTION_KINDS",
    "RESOURCE_CLASSES",
    "MAX_PAYLOAD_BYTES",
    "MAX_STRING_LEN",
    "MAX_DELEGATION_DEPTH",
    "REDACTED",
    "utc_now_iso",
    "new_id",
    "canonical_json",
    "sha256_hex",
    "short_digest",
    "redact",
    "scan_for_secrets",
    "target_digest",
    "idempotency_key",
    "scaffold_event",
    "validate_event",
    "is_valid_event",
    "ActionPayload",
    "HookEvent",
]

