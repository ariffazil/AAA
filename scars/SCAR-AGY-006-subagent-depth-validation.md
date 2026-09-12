# SCAR-AGY-006 - Subagent Depth + Validation Cascade

Scar ID: SCAR-AGY-006 (catalog: Scar #23)
Domain: Subagent Orchestration / arifOS Schema Validation / Recursion Limits
Severity: P2 (200+ errors in 60 days)
Status: SEALED (autonomous scar extraction, 2026-09-12)
Confidence: 0.85

---

## 1. Failure Pattern

Two correlated failure modes:

(a) **task tool - subagent depth limit** (146 errors in 60 days):
  "Subagent depth limit reached (1). Increase 'subagent_depth' to allow nested subagents"

(b) **arifOS arif_seal / arif_route - validation errors** (~155+27 errors):
  - arifos_arif_seal: 888_HOLD Capability 'kernel.seal' requires 888_HOLD. Requires SOVEREIGN authority.
  - arifos_arif_route: "1 validation error for call[arif_route] mode - Unexpected keyword argument [type]"

## 2. The Echo

(a) **Agent assumes flat subagent tree.** When the orchestrator itself is a subagent, calling another `task` exceeds the default depth=1.

(b) **Agent sends wrong schema types.** arif_route expects `intent` not `type`. arif_seal expects `constitutional_chain_id` not `seal_verdict_id` alone.

## 3. The Law

(a) Before `task` call:
- Check current agent depth: `arifos_arif_memory(mode=inspect, memory_id=session_id)`
- If depth >= 1: use `arifos_arif_route(intent=...)` to delegate DOWN to a worker organ instead of recursing UP
- Never exceed `subagent_depth` config without F13 escalation

(b) Before `arif_route`/`arif_seal`/`arif_judge` call:
- Read tool schema: `arifos_arif_observe(mode=compass)` for canonical verb mapping
- Map old arg names: type->intent, seal_verdict_id->constitutional_chain_id
- Verify required args via `arif_route(mode=...)` contract

## 4. The Eureka (unused capability)

- `arifos_arif_route(intent=..., organ=...)` - cross-organ delegation without subagent recursion
- `aforge_forge_parallel(mode=parallel, tasks=[...])` - bounded fan-out (max 8, fail_fast)
- `arifos_arif_memory(mode=inspect, memory_id=...)` - depth visibility

## 5. Verified Fix

```python
# (a) Depth check before nested subagent
depth = arif_memory(mode=inspect, memory_id=session_id).depth
if depth >= 1:
    # Delegate down instead of recursing up
    arif_route(intent="...", organ="aforge")
else:
    task(subagent_type="...", prompt="...")

# (b) Schema-correct call
arif_route(intent="interpret this seismic section", organ="geox")  # NOT type=
arif_seal(payload="...", constitutional_chain_id="cc_...")         # NOT seal_verdict_id alone
```

## 6. Hardening

- **OPENCODE-task tool**: surface current depth + remaining before each call
- **arifos_arif_route**: more forgiving schema (accept `type` as alias for `intent`)
- **FORGE-subagent-spawn**: pre-flight depth probe

```yaml
scar_id: SCAR-AGY-006
n_incidents: 200
severity: P2
law: Check subagent depth before task call. Verify schema args before arif_route/arif_seal.
eureka: arif_route + forge_parallel + arif_memory(inspect)
confidence: 0.85
```
