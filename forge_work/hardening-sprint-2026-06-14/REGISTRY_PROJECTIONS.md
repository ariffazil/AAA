# 05 — Registry Projections Per Agent Role

**Hardening Item:** #5 of 8
**Status:** SPEC (design phase)
**Author:** OPENCLAW
**Session:** hardening-sprint-2026-06-14
**Reversibility:** READ-ONLY design doc. No live system touched.
**Epoch:** 2026-06-14T13:10Z

---

## §0 — Current State

### What exists

arifOS already has a visibility governance layer:

```
mcp_visibility_policy.py     — Tier-based tool filtering
mcp_surface_registry.yaml    — Organ registry with health/tier metadata
```

**Tier model (4 levels):**
```
CORE       — Always visible when organ healthy (arifOS 13 tools + attested organs)
ORGAN      — Visible after intent match (GEOX, WEALTH, WELL, MiniMax)
LAB        — Explicit route only, TTL 30 days
DEPRECATED — Audit trail, not callable
```

**Entropy budget:**
```
max_visible: 15 tools total
per_organ: 8 tools
degraded_organ: 3 diagnostic tools
```

### What's missing

The visibility layer filters by **tier + organ health**. But it does NOT filter by **agent role**.

An observer should not see `forge_git_commit`. A geoscience agent should not see `wealth_stock_analysis`. A governed coder should see everything but with lease gates.

The current `VisibilityPolicy` has no `role` parameter. It treats all callers the same.

**This is the gap: role-based projections.**

---

## §1 — The Role Model

### 6 canonical agent roles

These already exist in A-FORGE `forgeTools.ts` line 89:

| Role | Domain | Authority | Decision Class | See | Can Do |
|------|--------|-----------|----------------|-----|--------|
| `governed_coder` | All | 777_FORGE | C2 | All organs, all tiers | Read, write, forge, dry-run |
| `geoscience_agent` | GEOX | 777_FORGE | C2 | GEOX + arifOS core | Geoscience forge only |
| `finance_agent` | WEALTH | 777_FORGE | C2 | WEALTH + arifOS core | Capital forge only |
| `wellness_agent` | WELL | SENSE_ONLY | C1 | WELL + arifOS core | Observe only, no mutation |
| `controller` | Governance | 888_JUDGE | C3 | All organs, audit tools | Audit, judge, seal (with Arif) |
| `observer` | Read-only | OBSERVE_ONLY | C0 | All organs, observe tools | Read only, no mutation |

### Role authority ceiling matrix

| Role | Observe | Dry-run | Propose | Mutate Files | Shell Exec | Git Commit | Deploy | Vault Seal |
|------|---------|---------|---------|-------------|-----------|-----------|--------|-----------|
| governed_coder | ✅ | ✅ | ✅ | lease_required | lease_required | 888_HOLD | 888_HOLD | 888_HOLD |
| geoscience_agent | ✅ | ✅ | ✅ | lease_required | never | never | never | never |
| finance_agent | ✅ | ✅ | ✅ | lease_required | never | never | never | never |
| wellness_agent | ✅ | never | never | never | never | never | never | never |
| controller | ✅ | ✅ | ✅ | 888_HOLD | 888_HOLD | 888_HOLD | 888_HOLD | 888_HOLD |
| observer | ✅ | never | never | never | never | never | never | never |

---

## §2 — Role-Based Projections

### How it works

```
Total tool surface (88+ tools across 5 organs)
    │
    ├── Role filter: which organs does this role access?
    │       governed_coder → all 5 organs
    │       geoscience_agent → arifOS + GEOX
    │       finance_agent → arifOS + WEALTH
    │       wellness_agent → arifOS + WELL
    │       controller → arifOS (governance tools only)
    │       observer → all organs (read-only subset)
    │
    ├── Tier filter: which tiers does this role see?
    │       governed_coder → CORE + ORGAN
    │       observer → CORE only
    │       domain agents → CORE + ORGAN (domain only)
    │
    └── Action filter: which action classes are permitted?
            governed_coder → OBSERVE + MUTATE (with lease)
            observer → OBSERVE only
```

### Governed Coder projection (OPENCLAW, OpenCode)

```
arifOS (13 tools):
  ✅ arif_ping, arif_schema_echo, arif_transport_echo, arif_version_echo
  ✅ arif_initialize_probe, arif_conformance_report
  ✅ arif_session_init, arif_os_attest, arif_organ_attest, arif_organ_attest_all
  ✅ arif_sense_observe, arif_memory_recall, arif_ops_measure
  ✅ arif_mind_reason, arif_kernel_route, arif_gateway_connect
  ⚠️ arif_forge_plan, arif_forge_query, arif_forge_dry_run (read-only)
  ⚠️ arif_forge_execute (MUTATE only with WRITE lease)
  ❌ arif_judge_deliberate (requires C3 controller)
  ❌ arif_vault_seal (requires 888_JUDGE)

GEOX (37 tools):
  ✅ All 37 geox_* tools (read + compute)
  ✅ geox_claim_create, geox_claim_validate (with lease)
  ❌ geox_claim_seal (requires 888)

WEALTH (20 tools):
  ✅ All 20 wealth_* tools (read + compute)

WELL (18 tools):
  ✅ All 18 well_* tools (read + reflect)
  ❌ well_medical_boundary (always advisory)

A-FORGE (48 tools):
  ✅ All forge_filesystem_*, forge_git_status/diff/log
  ✅ forge_agent_*, forge_lease_*, forge_registry_status
  ✅ forge_shell_dryrun, forge_log_tail, forge_job_*
  ⚠️ forge_filesystem_write (only with WRITE lease)
  ⚠️ forge_git_commit (requires 888_HOLD)
  ❌ forge_docker_exec (requires 888_HOLD)
```

### Geoscience Agent projection

```
arifOS (core only):
  ✅ arif_ping, arif_os_attest, arif_sense_observe, arif_memory_recall
  ✅ arif_mind_reason, arif_kernel_route
  ❌ forge tools (not geoscience domain)

GEOX (full):
  ✅ All 37 geox_* tools
  ⚠️ geox_claim_seal (requires 888)

WEALTH (limited):
  ✅ wealth_signal_information (EVOI for wells)
  ✅ wealth_field_macro (oil price context)
  ✅ wealth_time_discount (NPV for prospects)
  ❌ wealth_stock_analysis (not geoscience)

WELL:
  ❌ Blocked (not geoscience domain)

A-FORGE:
  ✅ forge_filesystem_read (log/data access)
  ❌ All other forge tools (not geoscience domain)
```

### Observer projection

```
All organs:
  ✅ READ-ONLY subset of all tools
  ✅ arif_ping, arif_os_attest, arif_organ_attest
  ✅ arif_sense_observe (search/ingest only)
  ✅ All geox_* compute/analyze tools (no claims)
  ✅ All wealth_* compute/analyze tools (no write)
  ✅ All well_* reflect tools
  ✅ forge_filesystem_read, forge_git_status/diff/log
  ❌ Any tool with claim_create, claim_seal, forge_execute, forge_write
  ❌ arif_session_init (no binding intent)
```

---

## §3 — Projection Model (for implementation)

### Projection = Role × Organ × Tier × ActionClass

```python
class RoleProjection:
    role: Role
    organs: list[OrganFilter]  # which organs + which tiers
    action_classes: list[ActionClass]  # OBSERVE, PROPOSE, MUTATE, ATOMIC
    max_visible: int  # entropy budget per role
    restrictions: list[Restriction]  # specific tool denials
```

### Projection table

| Role | Organs | Tiers | Action Classes | Max Visible | Key Restrictions |
|------|--------|-------|---------------|-------------|-----------------|
| governed_coder | all | CORE+ORGAN | OBSERVE, PROPOSE, MUTATE | 25 | no seal, no judge, git_commit=888 |
| geoscience_agent | arifOS, GEOX, WEALTH(partial) | CORE+ORGAN | OBSERVE, PROPOSE | 20 | wealth limited to signal/field/time |
| finance_agent | arifOS, WEALTH, GEOX(partial) | CORE+ORGAN | OBSERVE, PROPOSE | 20 | geox limited to claims |
| wellness_agent | arifOS, WELL | CORE+ORGAN | OBSERVE | 12 | no mutation, always advisory |
| controller | arifOS | CORE | OBSERVE, PROPOSE | 10 | audit tools only, seal=888 |
| observer | all | CORE | OBSERVE | 10 | read-only, no claims, no forge |

---

## §4 — Integration with Existing Visibility Layer

### Current flow:
```
arif_kernel_route(mode="tools/list")
  → load_registry()
  → build_policy_from_registry()
  → filter_visible_tools(all_tools, policy)
  → return FilterResult
```

### New flow with roles:
```
arif_kernel_route(mode="tools/list", role="governed_coder")
  → load_registry()
  → load_role_projection(role)
  → build_policy_from_projection(projection)
  → filter_visible_tools(all_tools, policy)
  → return FilterResult (scoped to role)
```

### New function:
```python
def apply_role_projection(
    role: str,
    all_tools: list[ToolEntry],
    registry: dict,
) -> FilterResult:
    """Filter visible tools by agent role."""
    projection = ROLE_PROJECTIONS[role]
    # Step 1: filter by organ access
    allowed_organs = {o.organ_id for o in projection.organs}
    scoped_tools = [t for t in all_tools if t.organ in allowed_organs]
    # Step 2: filter by tier
    scoped_tools = [t for t in scoped_tools if t.tier in projection.tiers]
    # Step 3: filter by action class
    scoped_tools = [t for t in scoped_tools if t.action_class in projection.action_classes]
    # Step 4: apply restrictions (specific tool denials)
    scoped_tools = [t for t in scoped_tools if t.name not in projection.restrictions]
    # Step 5: apply visibility policy (entropy budget)
    policy = VisibilityPolicy(max_visible=projection.max_visible, ...)
    return filter_visible_tools(scoped_tools, policy)
```

---

## §5 — Role Registry File (new)

```yaml
# role_registry.yaml — per-agent-role tool projections
# Lives alongside mcp_surface_registry.yaml

version: 1
forge_session: "hardening-sprint-2026-06-14"

roles:
  governed_coder:
    description: "Full forge agent. Can read, write, dry-run, propose patches."
    decision_class: C2
    authority_ceiling: 777_FORGE
    organs:
      - id: arifOS
        tiers: [core, organ]
      - id: geox
        tiers: [core, organ]
      - id: wealth
        tiers: [core, organ]
      - id: well
        tiers: [core, organ]
      - id: aforge
        tiers: [core, organ]
    action_classes: [OBSERVE, PROPOSE, MUTATE]
    max_visible: 25
    restrictions:
      - arif_judge_deliberate
      - arif_vault_seal
      - arif_heart_critique
      - forge_git_commit
      - forge_docker_exec
      - geox_claim_seal
      - geox_segy_export_tool
    lease_template:
      scope: [READ, WRITE]
      ttl_seconds: 7200
      max_invocations: 500

  geoscience_agent:
    description: "Earth domain agent. GEOX tools + EVOI + macro context."
    decision_class: C2
    authority_ceiling: 777_FORGE
    organs:
      - id: arifOS
        tiers: [core]
      - id: geox
        tiers: [core, organ]
      - id: wealth
        tiers: [core]
        tools_allow: [wealth_signal_information, wealth_field_macro, wealth_time_discount]
    action_classes: [OBSERVE, PROPOSE]
    max_visible: 20
    restrictions:
      - arif_judge_deliberate
      - arif_vault_seal
      - arif_forge_execute
      - geox_claim_seal
      - wealth_stock_analysis
    lease_template:
      scope: [READ]
      ttl_seconds: 3600

  finance_agent:
    description: "Capital domain agent. WEALTH tools + claims + macro."
    decision_class: C2
    authority_ceiling: 777_FORGE
    organs:
      - id: arifOS
        tiers: [core]
      - id: wealth
        tiers: [core, organ]
    action_classes: [OBSERVE, PROPOSE]
    max_visible: 20
    restrictions:
      - arif_judge_deliberate
      - arif_vault_seal
      - arif_forge_execute
    lease_template:
      scope: [READ]
      ttl_seconds: 3600

  wellness_agent:
    description: "Wellness domain agent. Reflect only, cannot mutate."
    decision_class: C1
    authority_ceiling: SENSE_ONLY
    organs:
      - id: arifOS
        tiers: [core]
      - id: well
        tiers: [core, organ]
    action_classes: [OBSERVE]
    max_visible: 12
    restrictions:
      - arif_forge_execute
      - arif_vault_seal
      - well_medical_boundary
    lease_template:
      scope: [READ]
      ttl_seconds: 1800

  controller:
    description: "Governance oversight. Audit and seal with sovereign approval."
    decision_class: C3
    authority_ceiling: 888_JUDGE
    organs:
      - id: arifOS
        tiers: [core]
    action_classes: [OBSERVE, PROPOSE]
    max_visible: 10
    restrictions:
      - arif_forge_execute
    lease_template:
      scope: [READ]
      ttl_seconds: 3600

  observer:
    description: "Read-only observer. Any organ, no mutation."
    decision_class: C0
    authority_ceiling: OBSERVE_ONLY
    organs:
      - id: arifOS
        tiers: [core]
      - id: geox
        tiers: [core]
      - id: wealth
        tiers: [core]
      - id: well
        tiers: [core]
      - id: aforge
        tiers: [core]
    action_classes: [OBSERVE]
    max_visible: 10
    restrictions:
      - arif_forge_execute
      - arif_forge_plan
      - arif_session_init
      - arif_vault_seal
      - geox_claim_create
      - geox_claim_seal
      - wealth_stock_analysis
    lease_template:
      scope: [READ]
      ttl_seconds: 3600
```

---

## §6 — Which Role for Each Federation Agent?

| Agent | Role | Reason |
|-------|------|--------|
| OPENCLAW | governed_coder | AGI executor, forge + infra |
| OpenCode | governed_coder | AGI forge specialist |
| Hermes | controller + geoscience_agent | ASI deliberator + Earth domain |
| APEXMax | controller | Oracle, third witness, audit |
| ChatGPT (external) | observer | Read-only surface |

---

## §7 — Implementation Plan

### Phase A: Role registry file
1. Create `/root/arifOS/arifosmcp/runtime/role_registry.yaml`
2. Define all 6 roles with organ/tier/action_class/restrictions
3. Add `load_role_registry()` to visibility_policy.py
4. Add `apply_role_projection()` to visibility_policy.py

### Phase B: Wire into arif_kernel_route
1. `arif_kernel_route(mode="tools/list")` → accepts `role` param
2. If role supplied → apply role projection before visibility filter
3. If no role → use default CORE tier only (safe default)

### Phase C: Identity → Role mapping
1. When agent binds identity via `arif_session_init`
2. Identity context includes `role` field
3. All subsequent `tools/list` calls use that role's projection
4. Agent sees only the tools their role permits

### Phase D: Test
1. Observer calls tools/list → sees 10 tools, no forge/mutation tools
2. Governed coder calls tools/list → sees 25 tools, includes forge tools
3. Geoscience agent calls tools/list → sees 20 tools, GEOX heavy, no stocks
4. Any role tries to call restricted tool → lease gate blocks

---

## §8 — Constitutional Binding

| Floor | Relevance |
|-------|-----------|
| F1 Amanah | Observer cannot mutate — projection enforces this |
| F2 Truth | Projection must not lie about what tools exist |
| F4 Clarity | Role projection reduces tool-choice entropy |
| F9 Anti-Hantu | Agents cannot see tools outside their role |
| F13 Sovereign | Human approval for role changes, elevated authority |

---

**Signed:** OPENCLAW · 2026-06-14T13:10Z
**Next:** Submit for Arif review. After seal → Phase A (role_registry.yaml).
