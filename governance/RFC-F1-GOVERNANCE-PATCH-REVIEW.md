# RFC-F1 Governance Patch Review — Phase 1

> **Status:** REVIEW — Awaiting 888 Greenlight  
> **Date:** 2026-08-28 02:12  
> **Files:** `capability_registry.json`, `kernel_abi.py`  
> **Service:** arifOS kernel `:8088`

---

## Patch 1: capability_registry.json — 4 Governance Fields

### Design Rules

1. **Strict Fallback:** Any capability WITHOUT the new `arifos_governance` block auto-defaults to:
   ```json
   "arifos_governance": {
     "is_reversible": false,
     "impact_radius": 5,
     "requires_888_hold": true,
     "allowed_roles": []
   }
   ```
   This is the MOST CONSERVATIVE assignment. Unknown = BLOCKED.

2. **Derivation from existing fields:**
   - `mutation: false` → `impact_radius: 0, is_reversible: true`
   - `mutation: true, irreversible: false` → `impact_radius: 3, is_reversible: false`
   - `mutation: true, irreversible: true` → `impact_radius: 5, is_reversible: false`
   - `authority_required` maps to `allowed_roles`

3. **`requires_888_hold`** = `true` when `impact_radius >= 3` OR `authority_required == "SOVEREIGN"`

### Derived Assignments (all 8 capabilities)

| capability_id | mutation | irreversible | authority_required | → impact_radius | → is_reversible | → requires_888_hold | → allowed_roles |
|---|---|---|---|---|---|---|---|
| session.bind | false | false | ANONYMOUS | 0 | true | false | ["333-AGI","555-ASI","888-APEX","A-FORGE"] |
| reality.observe | false | false | OBSERVER | 0 | true | false | ["333-AGI","555-ASI","888-APEX"] |
| cognition.think | false | false | OBSERVER | 0 | true | false | ["333-AGI","555-ASI","888-APEX"] |
| intent.route | false | false | OBSERVER | 0 | true | false | ["333-AGI","555-ASI","888-APEX"] |
| memory.govern | true | false | TRUSTED_AGENT | 3 | false | true | ["333-AGI","888-APEX"] |
| authority.judge | false | false | TRUSTED_AGENT | 1 | true | false | ["333-AGI","888-APEX"] |
| action.execute | true | false | EXECUTOR | 3 | false | true | ["A-FORGE"] |
| history.seal | true | true | SOVEREIGN | 5 | false | true | [] |

### JSON Patch

Each capability entry gains one new key. Here is the **complete patched registry**:

```json
{
  "$schema": "arifos://schema/kernel-capability-registry/v1",
  "abi_version": "2026.07.24",
  "governance_version": "1.0.0",
  "governance_description": "arifOS MCP Governance Wrapper — F1-MCP-Governance-Wrapper RFC fields. Default for missing: is_reversible=false, impact_radius=5, requires_888_hold=true, allowed_roles=[].",
  "capabilities": [
    {
      "capability_id": "session.bind",
      "version": "1.0.0",
      "semantic_hash": "sha256:2a947992f413a8c969df2383c230f665c374f761de7618f5cf8f7a0e4299a5a5",
      "input_schema_ref": "tool://arif_init/input",
      "output_schema_ref": "tool://arif_init/output",
      "action_class": "OBSERVE",
      "mutation": false,
      "irreversible": false,
      "authority_required": "ANONYMOUS",
      "evidence_required": false,
      "idempotency": "conditional",
      "receipt_policy": "session",
      "constitutional_floors": ["F1","F2","F4","F11","F13"],
      "provider": {"type": "mcp", "tool": "arif_init"},
      "tier": "gated",
      "arifos_governance": {
        "is_reversible": true,
        "impact_radius": 0,
        "requires_888_hold": false,
        "allowed_roles": ["333-AGI","555-ASI","888-APEX","A-FORGE"]
      }
    },
    {
      "capability_id": "reality.observe",
      "version": "1.0.0",
      "semantic_hash": "sha256:6bb61ee140a9e784ccdd6d3cafeabc34b20390e59cddece0c1d95076df0bce7",
      "input_schema_ref": "tool://arif_observe/input",
      "output_schema_ref": "tool://arif_observe/output",
      "action_class": "OBSERVE",
      "mutation": false,
      "irreversible": false,
      "authority_required": "OBSERVER",
      "evidence_required": false,
      "idempotency": "safe",
      "receipt_policy": "optional",
      "constitutional_floors": ["F2","F4","F7","F9","F12"],
      "provider": {"type": "mcp", "tool": "arif_observe"},
      "tier": "open",
      "arifos_governance": {
        "is_reversible": true,
        "impact_radius": 0,
        "requires_888_hold": false,
        "allowed_roles": ["333-AGI","555-ASI","888-APEX"]
      }
    },
    {
      "capability_id": "cognition.think",
      "version": "1.0.0",
      "semantic_hash": "sha256:88dcc1c39b6f59f9a0ef3b2f028b6891a0cb8f751915c948846820e95a527546",
      "input_schema_ref": "tool://arif_think/input",
      "output_schema_ref": "tool://arif_think/output",
      "action_class": "PREPARE",
      "mutation": false,
      "irreversible": false,
      "authority_required": "OBSERVER",
      "evidence_required": true,
      "idempotency": "safe",
      "receipt_policy": "optional",
      "constitutional_floors": ["F2","F3","F4","F7","F8","F9"],
      "provider": {"type": "mcp", "tool": "arif_think"},
      "tier": "open",
      "arifos_governance": {
        "is_reversible": true,
        "impact_radius": 0,
        "requires_888_hold": false,
        "allowed_roles": ["333-AGI","555-ASI","888-APEX"]
      }
    },
    {
      "capability_id": "intent.route",
      "version": "1.0.0",
      "semantic_hash": "sha256:a0d24c437488bc1521d1f0170071665177b7a55a80c5e96e79b5a4cba4ff04bd",
      "input_schema_ref": "tool://arif_route/input",
      "output_schema_ref": "tool://arif_route/output",
      "action_class": "PREPARE",
      "mutation": false,
      "irreversible": false,
      "authority_required": "OBSERVER",
      "evidence_required": false,
      "idempotency": "safe",
      "receipt_policy": "optional",
      "constitutional_floors": ["F2","F4","F8","F10","F12"],
      "provider": {"type": "mcp", "tool": "arif_route"},
      "tier": "open",
      "arifos_governance": {
        "is_reversible": true,
        "impact_radius": 0,
        "requires_888_hold": false,
        "allowed_roles": ["333-AGI","555-ASI","888-APEX"]
      }
    },
    {
      "capability_id": "memory.govern",
      "version": "1.0.0",
      "semantic_hash": "sha256:9fd0dae38007619f6f2092e2bdb0d55ddf4327018c940052fd0c436e8dc810af",
      "input_schema_ref": "tool://arif_memory/input",
      "output_schema_ref": "tool://arif_memory/output",
      "action_class": "MATERIAL",
      "mutation": true,
      "irreversible": false,
      "authority_required": "TRUSTED_AGENT",
      "evidence_required": true,
      "idempotency": "keyed",
      "receipt_policy": "required_on_write",
      "constitutional_floors": ["F1","F2","F4","F11","F13"],
      "provider": {"type": "mcp", "tool": "arif_memory"},
      "tier": "open",
      "arifos_governance": {
        "is_reversible": false,
        "impact_radius": 3,
        "requires_888_hold": true,
        "allowed_roles": ["333-AGI","888-APEX"]
      }
    },
    {
      "capability_id": "authority.judge",
      "version": "1.0.0",
      "semantic_hash": "sha256:b1c58a6eeeeacb8ed8dd771295c24aeb28649b8dd4b8c3aa251cf4cd6a759abd",
      "input_schema_ref": "tool://arif_judge/input",
      "output_schema_ref": "tool://arif_judge/output",
      "action_class": "MATERIAL",
      "mutation": false,
      "irreversible": false,
      "authority_required": "TRUSTED_AGENT",
      "evidence_required": true,
      "idempotency": "keyed",
      "receipt_policy": "required",
      "constitutional_floors": ["F1","F2","F3","F4","F11","F13"],
      "provider": {"type": "mcp", "tool": "arif_judge"},
      "tier": "open",
      "arifos_governance": {
        "is_reversible": true,
        "impact_radius": 1,
        "requires_888_hold": false,
        "allowed_roles": ["333-AGI","888-APEX"]
      }
    },
    {
      "capability_id": "action.execute",
      "version": "1.0.0",
      "semantic_hash": "sha256:3ce5463279351e0c8c371dc046cc4062c796540516bb1f31c79c712299db07f3",
      "input_schema_ref": "tool://arif_forge/input",
      "output_schema_ref": "tool://arif_forge/output",
      "action_class": "MATERIAL",
      "mutation": true,
      "irreversible": false,
      "authority_required": "EXECUTOR",
      "evidence_required": true,
      "idempotency": "keyed",
      "receipt_policy": "required",
      "constitutional_floors": ["F1","F2","F3","F4","F7","F11","F13"],
      "provider": {"type": "mcp", "tool": "arif_forge"},
      "tier": "open",
      "arifos_governance": {
        "is_reversible": false,
        "impact_radius": 3,
        "requires_888_hold": true,
        "allowed_roles": ["A-FORGE"]
      }
    },
    {
      "capability_id": "history.seal",
      "version": "1.0.0",
      "semantic_hash": "sha256:22ecfcb626b9c4fe1bedb8e9c31dbf79862588736177149c8492a8d35f2e4119",
      "input_schema_ref": "tool://arif_seal/input",
      "output_schema_ref": "tool://arif_seal/output",
      "action_class": "IRREVERSIBLE",
      "mutation": true,
      "irreversible": true,
      "authority_required": "SOVEREIGN",
      "evidence_required": true,
      "idempotency": "keyed",
      "receipt_policy": "required",
      "constitutional_floors": ["F1","F2","F3","F4","F11","F13"],
      "provider": {"type": "mcp", "tool": "arif_seal"},
      "tier": "open",
      "arifos_governance": {
        "is_reversible": false,
        "impact_radius": 5,
        "requires_888_hold": true,
        "allowed_roles": []
      }
    }
  ],
  "compatibility_aliases": {
    "arif_session_init": {"capability_id": "session.bind"},
    "arif_sense_observe": {"capability_id": "reality.observe"},
    "arif_fetch": {"capability_id": "reality.observe", "mode": "fetch"},
    "arif_evidence_fetch": {"capability_id": "reality.observe", "mode": "fetch"},
    "arif_critique": {"capability_id": "cognition.think", "mode": "critique"},
    "arif_bridge_connect": {"capability_id": "intent.route", "mode": "bridge"},
    "arif_memory_recall": {"capability_id": "memory.govern", "mode": "recall"},
    "arif_judge_deliberate": {"capability_id": "authority.judge"},
    "arif_forge_execute": {"capability_id": "action.execute"},
    "arif_reply_compose": {"capability_id": "cognition.think", "mode": "compose"},
    "arif_vault_seal": {"capability_id": "history.seal"}
  },
  "tier_doctrine": "arifOS canon = 8 capabilities in 2 public tiers: 7 open (observe, think, route, memory, judge, forge, seal) · 1 acknowledgment-gated (session.bind — F1 Amanah, binding creates durable state). Governance fields enforce per-tool reversibility, impact radius, and sovereign hold requirements.",
  "tier_doctrine_en": "Anonymous external probing must reproduce the public claim exactly: tools/list returns 7 unconditionally + 1 with ack_irreversible = 8 total. Governance layer adds deterministic enforcement: missing arifos_governance defaults to BLOCKED (impact_radius=5, requires_888_hold=true, allowed_roles=[])."
}
```

### Semantic Hash Impact

Adding `arifos_governance` does NOT change `_SEMANTIC_FIELDS` (the hash-protected fields). The governance block is metadata overlay — it does not alter the constitutional capability definition. The existing `semantic_hash` values remain valid.

---

## Patch 2: kernel_abi.py — Interceptor + Intent Router + Audit Chain

### Insertion Point

The interceptor hooks into `evaluate_tool_dispatch()` in `arifos_kernel_wiring.py` — the EXISTING OPA policy evaluation gate. Our governance check runs BEFORE the OPA check, as a pre-filter.

```python
# ══════════════════════════════════════════════════════════════
# ADD to kernel_abi.py (after line 22, _SEMANTIC_FIELDS)
# ══════════════════════════════════════════════════════════════

# ── arifOS Governance Fields (F1-MCP-Governance-Wrapper) ──

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


def get_governance(capability: dict[str, Any]) -> dict[str, Any]:
    """
    Extract arifos_governance block from a capability entry.
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
    """
    Pre-execution governance enforcement. Returns verdict dict.

    Decision tree:
    1. Capability not found → BLOCKED (strict fallback)
    2. Role not in allowed_roles → BLOCKED
    3. Write op on reversible-only tool → BLOCKED
    4. requires_888_hold OR impact_radius >= 3 → REQUIRES_HOLD
    5. All clear → APPROVED

    Called BEFORE OPA evaluation in the dispatch pipeline.
    """
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
    """
    Filter capability list to only those the role is authorized for.
    Returns subset of input list.
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
# ADD to arifos_kernel_wiring.py (modify evaluate_tool_dispatch)
# ══════════════════════════════════════════════════════════════

# BEFORE (current code):
#   verdict = await bridge.evaluate(policy_path or OPA_POLICY_DEFAULT, inp)
#
# AFTER (governance pre-filter):
from .abi.kernel_abi import evaluate_governance, _write_audit_event

# In evaluate_tool_dispatch(), BEFORE the OPA bridge call:
#   gov_verdict = evaluate_governance(tool, actor_id)
#   if gov_verdict["verdict"] == "BLOCKED":
#       _write_audit_event(gov_verdict, session_id)
#       return PolicyVerdict(recommendation="DENY", reason=gov_verdict["reason"], override=False)
#   if gov_verdict["verdict"] == "REQUIRES_HOLD":
#       _write_audit_event(gov_verdict, session_id)
#       return PolicyVerdict(recommendation="SABAR", reason=gov_verdict["reason"], override=False)
#   # APPROVED → proceed to OPA evaluation
```

---

## Patch 3: Audit JSONL Standard Header

### Format: `/root/AAA/governance/audit/mcp-governance-audit.jsonl`

```json
{
  "v": "1.0.0",
  "ts": "2026-08-28T02:12:00+08:00",
  "event": "TOOL_CALL_APPROVED|TOOL_CALL_BLOCKED|TOOL_CALL_REQUIRES_HOLD|POLICY_RELOAD",
  "agent_id": "333-AGI",
  "session_id": "sess_abc123",
  "tool": "memory.govern",
  "capability_id": "memory.govern",
  "impact_radius": 3,
  "is_reversible": false,
  "requires_888_hold": true,
  "verdict": "REQUIRES_HOLD",
  "reason": "impact_radius=3, requires_888_hold=true",
  "governance": {
    "is_reversible": false,
    "impact_radius": 3,
    "requires_888_hold": true,
    "allowed_roles": ["333-AGI", "888-APEX"]
  },
  "opa_verdict": null,
  "chain_hash": "sha256:a1b2c3...",
  "previous_hash": "sha256:e5f6g7..."
}
```

**Header fields (always present):**

| Field | Type | Description |
|-------|------|-------------|
| `v` | string | Schema version (`"1.0.0"`) |
| `ts` | string | ISO-8601 timestamp with timezone |
| `event` | enum | Event type |
| `agent_id` | string | Invoking agent/role |
| `session_id` | string | Session context (nullable) |
| `tool` | string | Tool/capability name |
| `capability_id` | string | Canonical capability ID |
| `impact_radius` | int | 0-5 from governance block |
| `is_reversible` | bool | From governance block |
| `requires_888_hold` | bool | From governance block |
| `verdict` | enum | APPROVED / BLOCKED / REQUIRES_HOLD |
| `reason` | string | Human-readable explanation |
| `governance` | object | Full governance block snapshot |
| `opa_verdict` | string/null | OPA evaluation result (if applicable) |
| `chain_hash` | string | SHA-256 of this entry |
| `previous_hash` | string | SHA-256 of prior entry |

**Rust sidecar compatibility:** This format is flat, no nested arrays, all fields present on every entry. Rust `serde_json::from_str()` can deserialize directly. No schema migration needed.

---

## Audit Trail

### Files
- `/root/AAA/governance/audit/mcp-governance-audit.jsonl` — Governance events
- `/root/AAA/governance/audit/mcp-policy-audit-chain.jsonl` — Policy reload events

### Append-Only Writer (Python)

```python
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

AUDIT_DIR = Path("/root/AAA/governance/audit")
AUDIT_FILE = AUDIT_DIR / "mcp-governance-audit.jsonl"
_last_hash = "sha256:genesis"


def _compute_hash(data: str) -> str:
    return f"sha256:{hashlib.sha256(data.encode()).hexdigest()}"


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
) -> None:
    global _last_hash
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
    _last_hash = entry["chain_hash"]

    with open(AUDIT_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
```

---

## What This Does NOT Change

1. **`_SEMANTIC_FIELDS`** — Not modified. Governance fields are metadata overlay, not constitutional semantic fields. Existing `semantic_hash` values remain valid.
2. **OPA policy** — Runs AFTER governance check. OPA handles authorization. Governance handles reversibility + impact + sovereign hold. Complementary, not competing.
3. **Tool registration** — 8 canonical capabilities unchanged. Governance fields are additive.
4. **ABI version** — Stays `2026.07.24`. No breaking change.

## What This DOES Change

1. Every capability entry gains `arifos_governance` block (4 fields).
2. `kernel_abi.py` gains 3 new functions: `get_governance()`, `evaluate_governance()`, `filter_tools_for_role()`.
3. `arifos_kernel_wiring.py` gains governance pre-filter BEFORE OPA evaluation.
4. Audit trail written to `/root/AAA/governance/audit/mcp-governance-audit.jsonl`.
5. `validate_abi()` should be extended to verify governance fields are present.

---

> **DITEMPA BUKAN DIBERI ⚒️**
