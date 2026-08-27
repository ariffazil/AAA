"""
arifOS Kernel ABI — Capability Registry + Governance Enforcement.

Provides:
  - capability_registry(): Load and validate the capability registry JSON.
  - get_governance(): Extract governance block from a capability entry.
  - evaluate_governance(): Pre-execution governance enforcement.
  - filter_tools_for_role(): Filter capability list by role authorization.
  - _write_audit_event(): Append governance event to audit trail.

Governance fields are metadata overlay — they do NOT alter _SEMANTIC_FIELDS
or existing semantic_hash values.

DITEMPA BUKAN DIBERI ⚒️
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ══════════════════════════════════════════════════════════════
# Registry
# ══════════════════════════════════════════════════════════════

_REGISTRY_PATH = Path(__file__).parent / "capability_registry.json"

# Fields protected by semantic_hash — DO NOT ADD to this tuple
_SEMANTIC_FIELDS = (
    "capability_id",
    "version",
    "input_schema_ref",
    "output_schema_ref",
    "action_class",
    "mutation",
    "irreversible",
    "authority_required",
    "evidence_required",
    "idempotency",
    "receipt_policy",
    "constitutional_floors",
    "provider",
    "tier",
)

# ══════════════════════════════════════════════════════════════
# Governance Fields (F1-MCP-Governance-Wrapper)
# ══════════════════════════════════════════════════════════════

_GOVERNANCE_FIELDS = (
    "is_reversible",
    "impact_radius",
    "requires_888_hold",
    "allowed_roles",
)

# Strict fallback: missing governance = MOST CONSERVATIVE
_GOVERNANCE_DEFAULTS = {
    "is_reversible": False,
    "impact_radius": 5,
    "requires_888_hold": True,
    "allowed_roles": [],
}

# ══════════════════════════════════════════════════════════════
# Audit Trail
# ══════════════════════════════════════════════════════════════

AUDIT_DIR = Path("/root/AAA/governance/audit")
AUDIT_FILE = AUDIT_DIR / "mcp-governance-audit.jsonl"

# Chain hash state — initialized from file on first access
_last_hash: str | None = None


def _init_audit_chain() -> None:
    """Read last chain_hash from existing audit file to maintain chain integrity.

    Called once on module load. Reads the tail of the audit file to find
    the last valid entry's chain_hash, preventing chain breaks on restart.
    """
    global _last_hash
    if _last_hash is not None:
        return  # Already initialized

    if AUDIT_FILE.exists():
        try:
            with open(AUDIT_FILE, "rb") as f:
                f.seek(0, 2)  # end of file
                file_size = f.tell()
                if file_size > 0:
                    # Read last 4KB to find the most recent valid entry
                    read_size = min(file_size, 4096)
                    f.seek(max(0, file_size - read_size))
                    tail = f.read().decode("utf-8", errors="replace")
                    for line in reversed(tail.split("\n")):
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            last = json.loads(line)
                            _last_hash = last.get("chain_hash", "sha256:genesis")
                            return
                        except json.JSONDecodeError:
                            continue
        except OSError:
            pass

    _last_hash = "sha256:genesis"


def _compute_hash(data: str) -> str:
    return f"sha256:{hashlib.sha256(data.encode()).hexdigest()}"


# ══════════════════════════════════════════════════════════════
# Core Functions
# ══════════════════════════════════════════════════════════════

_registry_cache: dict[str, Any] | None = None


def capability_registry() -> dict[str, Any]:
    """Load and cache the capability registry from JSON.

    Returns the full registry dict. Raises FileNotFoundError if the
    registry file is missing.
    """
    global _registry_cache
    if _registry_cache is None:
        if not _REGISTRY_PATH.exists():
            raise FileNotFoundError(
                f"Capability registry not found: {_REGISTRY_PATH}"
            )
        with open(_REGISTRY_PATH, "r") as f:
            _registry_cache = json.load(f)
    return _registry_cache


def get_governance(capability: dict[str, Any]) -> dict[str, Any]:
    """Extract arifos_governance block from a capability entry.

    Returns strict fallback defaults if block is missing or incomplete.
    ZERO ASSUMPTION on missing fields.
    """
    gov = capability.get("arifos_governance", {})
    return {
        field: gov.get(field, _GOVERNANCE_DEFAULTS[field])
        for field in _GOVERNANCE_FIELDS
    }


def evaluate_governance(
    capability_id: str,
    invoking_role: str,
    is_write_operation: bool = False,
) -> dict[str, Any]:
    """Pre-execution governance enforcement. Returns verdict dict.

    Decision tree:
    1. Capability not found → BLOCKED (strict fallback)
    2. Role not in allowed_roles → BLOCKED
    3. Empty allowed_roles + not 888-APEX → BLOCKED (sovereign-exclusive)
    4. Write op on read-only tool → BLOCKED
    5. requires_888_hold OR impact_radius >= 3 → REQUIRES_HOLD
    6. All clear → APPROVED

    Called BEFORE OPA evaluation in the dispatch pipeline.
    """
    _init_audit_chain()

    registry = capability_registry()
    capabilities = {c["capability_id"]: c for c in registry["capabilities"]}

    cap = capabilities.get(capability_id)
    if cap is None:
        return {
            "verdict": "BLOCKED",
            "reason": f"Capability '{capability_id}' not found in registry. UNCHECKED_BLOCK.",
            "tool": capability_id,
            "role": invoking_role,
            "governance": _GOVERNANCE_DEFAULTS,
        }

    gov = get_governance(cap)

    # Check 1: Role authorization
    allowed = gov["allowed_roles"]
    if allowed and invoking_role not in allowed:
        return {
            "verdict": "BLOCKED",
            "reason": f"Role '{invoking_role}' not authorized for '{capability_id}'. Allowed: {allowed}",
            "tool": capability_id,
            "role": invoking_role,
            "governance": gov,
        }
    # Empty allowed_roles = sovereign only (888-APEX)
    if not allowed and invoking_role != "888-APEX":
        return {
            "verdict": "BLOCKED",
            "reason": f"Capability '{capability_id}' is sovereign-exclusive. Role '{invoking_role}' denied.",
            "tool": capability_id,
            "role": invoking_role,
            "governance": gov,
        }

    # Check 2: Write operation on read-only tool
    if is_write_operation and gov["is_reversible"]:
        return {
            "verdict": "BLOCKED",
            "reason": f"Write operation on read-only tool '{capability_id}'. Mutation not permitted.",
            "tool": capability_id,
            "role": invoking_role,
            "governance": gov,
        }

    # Check 3: Sovereign hold required
    if gov["requires_888_hold"] or gov["impact_radius"] >= 3:
        return {
            "verdict": "REQUIRES_HOLD",
            "reason": f"Tool '{capability_id}' requires 888 Sovereign Hold. impact_radius={gov['impact_radius']}, reversible={gov['is_reversible']}.",
            "tool": capability_id,
            "role": invoking_role,
            "governance": gov,
        }

    # All clear
    return {
        "verdict": "APPROVED",
        "reason": "Governance check passed.",
        "tool": capability_id,
        "role": invoking_role,
        "governance": gov,
    }


def filter_tools_for_role(
    capability_ids: list[str],
    role: str,
) -> list[str]:
    """Filter capability list to only those the role is authorized for.

    Returns subset of input list. Unknown capabilities are skipped
    (strict fallback = not authorized).
    """
    registry = capability_registry()
    capabilities = {c["capability_id"]: c for c in registry["capabilities"]}
    filtered = []
    for cid in capability_ids:
        cap = capabilities.get(cid)
        if cap is None:
            continue  # Unknown capability = skip (strict fallback)
        gov = get_governance(cap)
        allowed = gov["allowed_roles"]
        if allowed and role in allowed:
            filtered.append(cid)
        elif not allowed and role == "888-APEX":
            filtered.append(cid)
    return filtered


# ══════════════════════════════════════════════════════════════
# Audit Trail Writer
# ══════════════════════════════════════════════════════════════

def _write_audit_event(
    event: str,
    agent_id: str,
    tool: str,
    capability_id: str,
    governance: dict,
    verdict: str,
    reason: str,
    session_id: str | None = None,
    opa_verdict: str | None = None,
) -> str:
    """Append a governance event to the audit trail.

    Returns the chain_hash of the written entry.
    Uses tamper-evident append-only chain: each entry hashes its content
    plus the previous entry's chain_hash.
    """
    global _last_hash
    _init_audit_chain()

    AUDIT_DIR.mkdir(parents=True, exist_ok=True)

    entry = {
        "v": "1.0.0",
        "ts": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "agent_id": agent_id,
        "session_id": session_id,
        "tool": tool,
        "capability_id": capability_id,
        "impact_radius": governance.get("impact_radius", 5),
        "is_reversible": governance.get("is_reversible", False),
        "requires_888_hold": governance.get("requires_888_hold", True),
        "verdict": verdict,
        "reason": reason,
        "governance": governance,
        "opa_verdict": opa_verdict,
        "chain_hash": "",
        "previous_hash": _last_hash,
    }

    # Compute chain hash (everything except chain_hash itself)
    snapshot = {k: v for k, v in entry.items() if k != "chain_hash"}
    raw = json.dumps(snapshot, sort_keys=True, separators=(",", ":"))
    entry["chain_hash"] = _compute_hash(raw)

    # Update chain state
    _last_hash = entry["chain_hash"]

    # Append to audit file
    with open(AUDIT_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

    return entry["chain_hash"]
