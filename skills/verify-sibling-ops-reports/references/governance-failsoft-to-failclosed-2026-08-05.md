# Governance Fail-Soft → Fail-Closed Patches — 2026-08-05

## Context

Three audit reports (Hermes dispatch + OpenClaw peer) converged on 10 nodes. The verification pass identified two concrete governance gaps and one pre-existing fix already landed:

1. **FQ null edge case** — already patched upstream (src: `check_verdict.ts:96` default = 0.0, not 0.5; comment explains the prior bug). No action needed.
2. **Gödel closure gate: fail-soft → fail-closed** — `governance_pipeline.py:1957-1980`
3. **`check_godel_lock()` dead code → wired into forge.py pre-execution** — `tools/forge.py:872-932`

## Patch 1: governance_pipeline.py — fail-closed on Gödel closure

**File:** `/root/arifOS/arifosmcp/runtime/governance_pipeline.py`  
**Method:** `_gate_godel_closure()` around line 1957  
**What changed:**
- If `_GODEL_LOCK_GATE_AVAILABLE` is False → `passed=False` (was `passed=True`)
- If `godel_lock_gate(ctx)` raises an exception → `passed=False` (was `passed=True`)
- `reason` string updated to include "fail-closed (HOLD)" for observability
- `GateResult` has no `verdict` field (only `gate`, `passed`, `reason`, `latency_ms`, `metadata`, `session_id`, `tool_name`, `gate_hash`)

**Why:** A constitutional gate must never degrade to advisory on failure. If the lock can't verify that an agent isn't certifying its own safety, HOLD is the only correct default.

**Reversibility:** T1 — revert `passed=True`, remove comment. Zero schema change.

## Patch 2: tools/forge.py — wire check_godel_lock() pre-execution

**File:** `/root/arifOS/arifosmcp/tools/forge.py`  
**Location:** After the Ed25519 signature check (line ~870), before `_run_forge()`  
**What was added:** A `check_godel_lock()` call for every `_is_mutate` path:
- Imports `arifosmcp.constitution.runtime_hook.check_godel_lock`
- VAULT999 liveness check via `Path("/root/arifOS/VAULT999/outcomes.jsonl").exists()`
- Returns `ForgeOutput(status="HOLD")` if any G1–G7 axiom is violated
- Fail-closed on exception (same principle as patch 1)
- `ImportError` is pass-through (governance_pipeline catches the same gate as a fallback)

**Why:** `check_godel_lock()` was defined (documented as "Called by arif_forge BEFORE any MUTATE action proceeds") but had zero call sites — a fully-formed gate that was never wired.

**Reversibility:** T1 — delete the `if _is_mutate:` block entirely. No downstream dependency.

## Key difference between the two Gödel paths

| Path | Module | Scope | Error behavior |
|---|---|---|---|
| `godel_lock_gate(ctx)` | `runtime/three_locks.py` | Governance orchestrator (all action classes) | Fail-closed (after patch) |
| `check_godel_lock()` | `constitution/runtime_hook.py` | Pre-execution in `tools/forge.py` (MUTATE only) | Fail-closed (after patch) |

Both are now fail-closed. The two paths cover different execution surfaces:
- Three_locks: orchestrator-level (runs before any tool handler)
- Forge.py pre-execution: tool-level (runs inside the MUTATE handler itself)

## Smoke test

```python
from arifosmcp.constitution.runtime_hook import check_godel_lock
r = check_godel_lock(
    action_class="MUTATE",
    actor_id="test",
    actor_signature="",  # missing — should trigger G3
    has_judge_hash=False,
    has_plan_id=False,
    has_vaul_entry=False,
    has_vaul999_connection=True,
    failure_cause="",
)
# Result: {'ok': False, 'verdict': 'HOLD', 'axiom_id': 'G3', 'axiom_name': 'External Witness Axiom', ...}
```

## Audit verdict taxonomy (updated)

After this patch, the N9-A verdict in the enforcement table should read **ENFORCED — fail-closed (patched 2026-08-05)** rather than "ENFORCED — fail-soft wrapper."

The `references/governance-enforcement-audit-2026-08-05.md` file is now historically accurate for the *pre-patch* state. The current state is captured here.
