# Deep Research → Readiness Gate Cross-Reference

> **Forged:** 2026-06-26 | **Authority:** F13 SOVEREIGN
> Cross-referencing 108-agent deep research against federation readiness gates and Inspector hooks.

---

## Cross-Reference Matrix

### External Finding → Internal Hook → Gap Assessment

| # | External Finding (Confidence) | Internal Hook | Status | Gap |
|---|-----------------------------|---------------|--------|-----|
| 1 | Type-safe capability tracking +0.8 to +3.7pp (HIGH) | `capability-registry.yaml` + `registry_truth_test.py` (DONE) | ARCHITECTURE READY, RUNTIME GAP | Per-tool runtime type-checking not yet wired. Registry maps tools→authority but doesn't enforce at call time. |
| 2 | Constitutional AI = harmlessness without human labels (HIGH) | F1-F13 floor consensus via `core/shared/floors.py` | LIVE | arifOS gates actions, not content. This is the stronger form — action authorization > content filtering. |
| 3 | {L5-L7}×{T3-T4} is 93% under-studied (HIGH) | No systematic evidence framework | GAP | readiness-gate tracks `phantom_tools`, `guard_conflicts`, `runtime_drift` but doesn't measure governance effectiveness (violation rates, HOLD/SEAL ratios, audit completeness). |
| 4 | ESAA agent-orchestrator separation (HIGH) | `forge_gate_active: PASS`, `irreversible_without_hold: PASS` | ARCHITECTURE EXISTS, NO PER-TOOL CONTRACTS | F1-F13 judge proxy exists but lacks JSON Schema boundary contracts per tool call. HOLD/SEAL verdicts are human-readable, not machine-verifiable at per-tool granularity. |
| 5 | Safety ≠ task completion — independent dimension (HIGH) | F2 TRUTH, F7 HUMILITY | LIVE | Floors enforce policy adherence as independent concern. 42/42 cognitive tests verify this. |
| 6 | Governance = action authorization (HIGH) | AAA→Supabase→VAULT999 chain | UNBUILT | Nothing writes to Supabase as intermediate queryable record layer. This is the complete answer to "what, under which conditions, with what oversight, recorded and audited" — and it's the single most critical gap. |

---

## Inspector Hook Coverage

### Current Inspector Hooks (from INVARIANTS.md + readiness-gate)

| Hook | What It Checks | Covers External Finding # |
|------|---------------|--------------------------|
| F1 AMANAH | Reversible-first, 888_HOLD for irreversible | #6 (action authorization) |
| F2 TRUTH | ≥0.99 fidelity, cheap claims = VOID | #5 (safety ≠ completion) |
| F4 CLARITY | ΔS ≤ 0, every output reduces entropy | All |
| F7 HUMILITY | Ω₀ ∈ [0.03, 0.05], no fake certainty | #5 (safety ≠ completion) |
| F11 AUDIT | Every decision logged, inspectable | #6 (governance = authorization) |
| F13 SOVEREIGN | Human veto FINAL | All |
| capability-registry.yaml | Tool → authority mapping | #1 (type-safe capabilities) |
| registry_truth_test.py | manifest == runtime == guard | #1 (type-safe capabilities) |
| forge_gate_active | A-FORGE 4-layer gate | #4 (ESAA pattern) |

### Missing Inspector Hooks (New Requirements from Deep Research)

| Hook | What It Would Check | Maps to External Finding | Priority |
|------|--------------------|--------------------------|----------|
| **Per-tool capability enforcement** | Every `forge_*` call verified against capability-registry.yaml at call time | #1 (Odersky type-safe tracking) | MEDIUM |
| **Governance effectiveness metrics** | Floor violation rates, HOLD-to-SEAL ratios, drift detection latency, audit completeness | #3 (Chu under-studied zone) | STRATEGIC |
| **JSON Schema boundary contracts** | Per-tool JSON Schema validation in adjudication pipeline — machine-verifiable HOLD/SEAL/VOID | #4 (ESAA deterministic adjudication) | HIGH |
| **AAA→Supabase→VAULT999 seal chain** | AAA approval writes to Supabase (queryable record) → arifOS judges → VAULT999 seals (immutable) | #6 (Moghaddasi action authorization) | CRITICAL |
| **VAULT999 cryptographic hardening** | Hash-chain, per-entry signature, off-VPS anchor | Caveat #2 | HIGH |
| **F13 trigger migration path** | F13 trigger in standard migrations/ (not custom triggers/) — reproducible from `supabase db reset` | Open Question #1 | MEDIUM |

---

## Synthesis: The Prioritized Action Stack

### Layer 1 — CRITICAL (Unblocks Everything Else)

**AAA→Supabase→VAULT999 Seal Chain**
- What: AAA approval → Supabase (queryable structured record) → arifOS judge → VAULT999 (immutable seal)
- Why: Every external paper identifies provenance + audit as THE critical missing layer. The arifOS architecture has the complete answer designed but not built.
- Blocks: Publishing empirical governance evidence (Rec 2), complete governance stack (Rec 3)
- Effort: Medium (schema design + API wiring, no new paradigm)
- Files: New — AAA Supabase schema + API endpoints + VAULT999 writer integration

### Layer 2 — HIGH (Hardens Core Governance)

**A) JSON Schema Boundary Contracts Per Tool**
- What: Every MCP tool gets a JSON Schema boundary contract. Adjudication pipeline validates tool calls against contracts before HOLD/SEAL/VOID.
- Why: Closes the gap between human-readable verdict semantics and machine-verifiable authorization (ESAA pattern validated by Rec 3)
- Files: `arifOS/core/schemas/tool_boundaries/`, adjudication pipeline hardening

**B) VAULT999 Cryptographic Hardening**
- What: Minimum viable — SHA-256 hash chain, per-entry Ed25519 signature, off-VPS witness anchor
- Why: Append-only by convention ≠ immutable audit. Current NUL-byte corruption proves the gap is real, not theoretical.
- Files: `arifOS/VAULT999/crypto.py`, hash chain verification

### Layer 3 — MEDIUM (Completes the Architecture)

**A) Per-Tool Capability Enforcement at Runtime**
- What: Every tool call validated against capability-registry.yaml at invocation time — static type-checking at the MCP surface
- Why: Odersky et al. results demonstrate safety + benchmark improvement from static enforcement
- Files: `arifOS/core/capability_enforcer.py`, MCP tool wrapper

**B) F13 Trigger Migration Path**
- What: Move `trg_f13_sovereign_patch` from `custom triggers/` to standard `migrations/` directory as thin wrapper
- Why: Silent failure mode on `supabase db reset` — F13 protection must survive DB rebuild
- Files: New migration file in `arifOS/supabase/migrations/`

### Layer 4 — STRATEGIC (Publishes the Reference Architecture)

**Governance Effectiveness Evidence Framework**
- What: Systematic metrics collection and publishing framework for floor violation rates, HOLD-to-SEAL ratios, audit completeness, drift detection latency
- Why: Establish arifOS as the reference architecture for the {L5-L7}×{T3-T4} zone that Chu 2026 finds 93% under-studied
- Files: New — metrics pipeline, evidence publishing framework
- Dependency: Requires Layer 1 (AAA-Supabase-VAULT999) to be built first (can't publish what you can't measure)

---

## Update to readiness-gate.yaml

These 6 new Inspector hooks should be added to readiness-gate.yaml as new `pass_conditions`:

```yaml
pass_conditions:
  # ... existing conditions ...

  per_tool_capability_enforcement:
    status: NOT_YET_BUILT
    required: true
    note: "Every forge_* call must be validated against capability-registry.yaml at call time."

  json_schema_boundary_contracts:
    status: NOT_YET_BUILT
    required: true
    note: "Per-tool JSON Schema contracts for machine-verifiable adjudication."

  aaa_supabase_vault999_chain:
    status: NOT_YET_BUILT
    required: true
    note: "AAA approval → Supabase record → VAULT999 seal. The complete governance stack."

  vault999_cryptographic_hardening:
    status: NOT_YET_BUILT
    required: true
    note: "SHA-256 hash chain + Ed25519 per-entry signatures + off-VPS anchor."

  f13_trigger_migration_path:
    status: GAP
    required: true
    note: "F13 trigger must survive supabase db reset. Move to standard migrations/."

  governance_effectiveness_metrics:
    status: NOT_YET_DESIGNED
    required: false
    note: "Systematic evidence framework for {L5-L7}×{T3-T4} zone publishing."
```

---

*DITEMPA BUKAN DIBERI — 999 SEAL ALIVE.*
