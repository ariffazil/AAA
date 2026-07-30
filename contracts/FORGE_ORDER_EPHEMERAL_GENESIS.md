# FORGE ORDER — Ephemeral Tool Genesis Wiring

> **DITEMPA BUKAN DIBERI** — Issued 2026-07-30 by 333-AGI (Δ Mind)
> **P0 gap:** arif_forge genesis modes not wired to A-FORGE sandbox
> **Substrate:** A-FORGE SandboxPolicy.ts + ContainmentEngine.ts (bwrap) — EXISTS
> **Contract:** /root/AAA/contracts/ephemeral-tool-genesis.json — RATIFIED
> **Iron rule:** Agent creates CAPABILITY. Agent NEVER creates AUTHORITY.

---

## What exists

```
✅ ephemeral-tool-genesis.json    — Contract defining 7 genesis modes
✅ CAPABILITY_ARCHITECTURE.md     — 7 primitives mapped to 189 tools
✅ MISSION_INTERFACE.md           — Human contract: 6 missions, zero tool selection
✅ mission_router.py              — Intent → mission classifier (keyword + ML-ready)
✅ A-FORGE SandboxPolicy.ts       — 3 presets (READONLY_BUILD, NETWORKED_READ, FULL_TRUSTED)
✅ A-FORGE ContainmentEngine.ts   — bwrap isolation, filesystem/network/resource limits
✅ arifOS kernel 8 canonical verbs
✅ Federation Registry Spine v2.0 — all 189 tools classified
✅ Callability Matrix v1.1        — all 5 organs proven callable
```

## What's missing — the P0 gap

```
❌ arif_forge genesis modes       — inspect_gap, generate_ephemeral, sandbox_test,
                                    invoke_ephemeral, verify_output, propose_promotion, retire
❌ arif_route bridge              — mode=bridge not in Pydantic schema
❌ Identity semantics deploy       — state_axes fix in rest_routes.py:3179, blocked by classifier
```

---

## Wiring Specification

### 1. arif_forge mode: inspect_gap

**Purpose:** Agent detects missing capability before creating anything.

**Schema addition:**
```json
{
  "name": "arif_forge",
  "modes": [..., "inspect_gap"],
  "mode_schemas": {
    "inspect_gap": {
      "mission_description": "string — what the agent needs to accomplish",
      "failed_tools": ["optional — tools already attempted and why they failed"],
      "input_format": "string — mime type or data shape of input"
    }
  }
}
```

**Logic:**
1. Search registry spine for existing tool matching input_format
2. Search capability registry for partial matches
3. If found → return REUSE with tool name
4. If not found → return GAP with minimum viable capability spec
5. Include sandbox preset recommendation (READONLY_BUILD, NETWORKED_READ, or REJECT)

**Output:**
```json
{
  "verdict": "GAP | REUSE",
  "existing_match": null,
  "gap_spec": {
    "capability_type": "parser | calculator | transformer | scraper | adapter | converter | simulation",
    "input_format": "custom_binary_v17",
    "output_format": "structured_json",
    "suggested_language": "python",
    "suggested_packages": ["struct"],
    "sandbox_preset": "READONLY_BUILD",
    "estimated_lines": 60,
    "network_required": false
  },
  "reason": "No existing tool handles custom_binary_v17 format"
}
```

---

### 2. arif_forge mode: generate_ephemeral

**Purpose:** Create temporary tool code inside A-FORGE sandbox.

**Schema addition:**
```json
{
  "mode_schemas": {
    "generate_ephemeral": {
      "gap_spec": "from inspect_gap output",
      "sample_input": "string — small sample for tool to process",
      "language": "python | bash | node",
      "sandbox_preset": "READONLY_BUILD (default) | NETWORKED_READ"
    }
  }
}
```

**Logic:**
1. Validate gap_spec passes GREEN autonomy tier (no network unless NETWORKED_READ preset)
2. Allocate sandbox ID via A-FORGE ContainmentEngine
3. Generate tool code (Python script or function)
4. Write to sandbox filesystem
5. Record: sandbox_id, tool_hash, creation_timestamp, sandbox_preset
6. Return tool reference (not the full code unless requested)

**Output:**
```json
{
  "verdict": "GENERATED",
  "ephemeral_tool_id": "eph-abc123",
  "sandbox_id": "sbx-xyz789",
  "tool_hash": "sha256:...",
  "language": "python",
  "sandbox_preset": "READONLY_BUILD",
  "permissions_granted": ["read: sandbox/input", "write: sandbox/output"],
  "expires_at": "ISO8601 — max 1 hour",
  "auto_retire": true
}
```

**Safety:** Tool hash recorded. Sandbox ID recorded. Auto-retire after 1 hour. Never persists across sessions.

---

### 3. arif_forge mode: sandbox_test

**Purpose:** Test ephemeral tool against sample input before any real data touches it.

**Schema addition:**
```json
{
  "mode_schemas": {
    "sandbox_test": {
      "ephemeral_tool_id": "from generate_ephemeral",
      "test_input": "string — sample input data",
      "expected_output_shape": "optional — {type, keys, range} for validation"
    }
  }
}
```

**Logic:**
1. Execute tool in sandbox with test input
2. Capture stdout, stderr, exit code, execution time, memory
3. If expected_output_shape provided, validate output structure
4. Return test report

**Output:**
```json
{
  "verdict": "PASS | FAIL | FLAKY",
  "exit_code": 0,
  "execution_time_ms": 42,
  "memory_kb": 8192,
  "output_valid": true,
  "output_sample": "first 200 chars of output",
  "errors": [],
  "warnings": [],
  "ready_for_real_data": true
}
```

**Gate:** Must PASS before invoke_ephemeral is allowed. FAIL → back to generate_ephemeral or ABANDON.

---

### 4. arif_forge mode: invoke_ephemeral

**Purpose:** Execute ephemeral tool against real mission data. YELLOW autonomy.

**Schema addition:**
```json
{
  "mode_schemas": {
    "invoke_ephemeral": {
      "ephemeral_tool_id": "from generate_ephemeral",
      "mission_data": "string or path — real data to process",
      "permission_scope": "{read: [...], write: [...], network: [...]}",
      "timeout_ms": 30000
    }
  }
}
```

**Logic:**
1. Verify sandbox_test was PASS
2. Verify permission_scope ⊆ sandbox_preset limits
3. Expand sandbox to include mission_data (read-only mount)
4. Execute
5. Capture full execution receipt
6. Log to audit trail

**Output:**
```json
{
  "verdict": "COMPLETED | TIMEOUT | ERROR",
  "result": "tool output (truncated to 100KB)",
  "execution_receipt": {
    "tool_hash": "sha256:...",
    "sandbox_id": "sbx-xyz789",
    "exit_code": 0,
    "execution_time_ms": 234,
    "input_hash": "sha256:...",
    "output_hash": "sha256:..."
  },
  "irreversible_action": "NONE — sandboxed"
}
```

---

### 5. arif_forge mode: verify_output

**Purpose:** Independent verification — did the tool produce correct output?

**Schema addition:**
```json
{
  "mode_schemas": {
    "verify_output": {
      "ephemeral_tool_id": "from generate_ephemeral",
      "expected_properties": "optional — {row_count, schema, value_ranges, checksums}",
      "cross_check_method": "optional — 'manual' | 'heuristic' | 'alternative_tool'"
    }
  }
}
```

**Logic:**
1. If expected_properties provided: validate structurally
2. If cross_check_method = alternative_tool: run different tool on same input
3. Compare outputs, flag discrepancies
4. Return verification report

**Output:**
```json
{
  "verdict": "VERIFIED | SUSPICIOUS | FAILED",
  "structural_check": true,
  "cross_check_match": null,
  "discrepancies": [],
  "confidence": 0.95
}
```

---

### 6. arif_forge mode: propose_promotion

**Purpose:** After ≥3 successful uses, agent proposes permanent registration. RED — human approval REQUIRED.

**Schema addition:**
```json
{
  "mode_schemas": {
    "propose_promotion": {
      "ephemeral_tool_id": "from generate_ephemeral",
      "usage_count": "must be ≥ 3",
      "success_rate": "must be ≥ 0.9",
      "promotion_justification": "string — why should this be permanent?"
    }
  }
}
```

**Logic:**
1. Verify usage_count ≥ 3 and success_rate ≥ 0.9
2. Generate promotion proposal with all usage receipts
3. Create 888_HOLD ticket for Arif
4. Do NOT register. Do NOT persist. Await human approval.

**Output:**
```json
{
  "verdict": "PROPOSED — AWAITING SOVEREIGN APPROVAL",
  "hold_ticket_id": "hold-proposal-abc123",
  "tool_spec": {
    "name": "proposed: custom_binary_v17_parser",
    "capability": "SENSE / READ",
    "organ": "A-FORGE",
    "autonomy_tier": "GREEN",
    "usage_history": [
      {"timestamp": "...", "mission": "INVESTIGATE", "success": true},
      {"timestamp": "...", "mission": "INVESTIGATE", "success": true},
      {"timestamp": "...", "mission": "INTERPRET", "success": true}
    ]
  },
  "requires": "F13 sovereign approval via 888_HOLD resolution"
}
```

---

### 7. arif_forge mode: retire

**Purpose:** Destroy ephemeral tool. Clean sandbox. Always allowed, always required.

**Schema addition:**
```json
{
  "mode_schemas": {
    "retire": {
      "ephemeral_tool_id": "from generate_ephemeral",
      "reason": "completed | failed | expired | replaced"
    }
  }
}
```

**Logic:**
1. Delete ephemeral tool code from sandbox
2. Wipe sandbox filesystem
3. Release sandbox resources
4. Record retirement in tool ledger
5. Return clean confirmation

**Output:**
```json
{
  "verdict": "RETIRED",
  "tool_hash": "sha256:...",
  "sandbox_freed": true,
  "artifacts_removed": 3,
  "retirement_reason": "completed"
}
```

---

## Integration Points

### arif_route → arif_forge bridge

When `arif_route` classifies a mission requiring a tool that doesn't exist:

```
arif_route: "No tool for custom_binary_v17"
    ↓ (automatic)
arif_forge(mode=inspect_gap): "GAP: need parser"
    ↓ (automatic)
arif_forge(mode=generate_ephemeral): "Created eph-abc123"
    ↓ (automatic)
arif_forge(mode=sandbox_test): "PASS"
    ↓ (automatic)
arif_forge(mode=invoke_ephemeral): "Output: {parsed data}"
    ↓ (automatic)
arif_forge(mode=verify_output): "VERIFIED"
    ↓ (automatic)
arif_forge(mode=retire): "RETIRED"
    ↓
arif_route: "Mission complete. Here's the data."
```

**Arif never saw any of it.** That's the contract.

### Sandbox Preset Mapping

| Genesis Mode | Minimum Preset | Max Permission |
|-------------|---------------|----------------|
| inspect_gap | NONE | registry read only |
| generate_ephemeral | READONLY_BUILD | write to sandbox fs only |
| sandbox_test | READONLY_BUILD | read sample input |
| invoke_ephemeral | READONLY_BUILD | read mission data, write sandbox output |
| verify_output | READONLY_BUILD | read outputs |
| propose_promotion | NONE | registry inspection |
| retire | NONE | sandbox cleanup |

**FULL_TRUSTED preset is NEVER used for ephemeral tools.**

---

## Tests Required Before Merge

```python
def test_inspect_gap_finds_existing():
    """When tool exists, returns REUSE not GAP."""

def test_inspect_gap_detects_missing():
    """When no tool matches, returns GAP with spec."""

def test_generate_ephemeral_rejects_network_when_not_net_read():
    """READONLY_BUILD preset blocks network requests."""

def test_sandbox_test_must_pass_before_invoke():
    """FAIL in sandbox_test blocks invoke_ephemeral."""

def test_invoke_ephemeral_rejects_full_trusted():
    """FULL_TRUSTED preset is rejected for ephemeral tools."""

def test_retire_cleans_sandbox():
    """After retire, sandbox is empty and reusable."""

def test_propose_promotion_requires_three_uses():
    """Less than 3 uses → rejected."""

def test_propose_promotion_requires_human():
    """Even with 3 uses, returns HOLD not SEAL."""

def test_autonomy_never_creates_authority():
    """Ephemeral tool cannot grant itself API keys, privileges, or persistence."""

def test_auto_retire_after_timeout():
    """Ephemeral tools auto-retire after 1 hour."""

def test_pipeline_recursion_bounded():
    """generate→test→invoke→retire loop bounded at 10 iterations."""

def test_dry_run_zero_external_effects():
    """Dry run does not mutate filesystem, network, or registry."""
```

---

## Files to Create/Modify

| File | Action |
|------|--------|
| `arifOS/arifosmcp/schemas/forge_modes.py` | Add 7 genesis mode schemas |
| `A-FORGE/src/domain/containment/EphemeralToolGenesis.ts` | Wire genesis modes to SandboxPolicy |
| `A-FORGE/src/interfaces/tools/forge_ephemeral.ts` | MCP tool handlers for each mode |
| `arifOS/arifosmcp/runtime/tools.py` | Register genesis modes as arif_forge sub-modes |
| `tests/test_ephemeral_genesis.py` | 12 mandatory tests |

---

*DITEMPA BUKAN DIBERI — From inventory to intelligence. From tools to capability.*
*Issued 2026-07-30. Next agent: implement Phase 1 — deterministic router core.*
