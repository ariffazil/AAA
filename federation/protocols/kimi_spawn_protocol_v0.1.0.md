# Kimi Spawn Protocol v0.1.0

> **Status:** PARTIAL-SEAL+ pending sovereign ratification
> **Authority:** ARIF (F13 SOVEREIGN)
> **Path:** `/root/AAA/federation/protocols/kimi_spawn_protocol_v0.1.0.md`
> **Machine-readable:** `/root/AAA/federation/protocols/kimi_spawn_protocol_v0.1.0.json`
> **Drafted:** 2026-08-07 · based on Kimi agent (FI-008) analysis + Hermes doctrine + sovereign audit
> **Ratification:** HOLD pending enforcement hook + tool capability reconciliation

---

## 0. Federation Invariant (binding)

> **Governance is measured per spawn, never per task.**
>
> Aggregate telemetry may summarize, but may not replace spawn-level telemetry.

This invariant applies to all spawn-aware harnesses in the federation (Hermes, Kimi, OpenCode, future). It exists because debt occurs at the spawn, receipt occurs at the spawn, coverage occurs at the spawn, and provenance occurs at the spawn. Aggregating these across a task call can hide governance leaks (a 0.4 spawn alongside two 1.0 spawns averages 0.8 — true leak becomes invisible).

---

## 1. Pre-Spawn Gate (A — mandatory)

Every spawn request MUST include:

```yaml
spawn_request:
  archetype: enum [af-explore, af-plan, af-fix, af-coordinator, af-worker, af-reviewer, af-forge]
  spawn_reason: enum [verification, criticism, synthesis, reconnaissance,
                       domain_analysis, implementation, refactor]
  risk_tier: enum [T1, T2, T3]
  expected_entropy_reduction: string  # qualitative OR ΔS estimate
  parent_session_id: string
  parent_spawn_id: string  # for chain linking
```

**Missing field → NO SPAWN.** Return reason to primary.

---

## 2. Archetype Ceilings (B — declared, not implicit)

```yaml
af-explore:      ceiling: OBSERVE_ONLY       # read-only, no mutation
af-reviewer:     ceiling: OBSERVE_ONLY       # review, no recommendation
af-plan:         ceiling: DRAFT_ONLY         # plans, no execution
af-fix:          ceiling: EXECUTE_REVERSIBLE # T1-T2 only (RECONCILE: live manifest has Bash+Write+Edit → must strip)
af-worker:       ceiling: EXECUTE_REVERSIBLE # bounded task scope (RECONCILE: same as af-fix)
af-coordinator:  ceiling: DISPATCH_ONLY      # routes only, never executes (RECONCILE: live says "Delegate via Agent tool" → conflict)
af-forge:        ceiling: EXECUTE_AFTER_SEAL # T2-T3, requires upstream seal
```

**Authority stays at the center.** Work flows to the rim. Capability ceilings are constitutional; they exist BEFORE runtime and override agent intent.

---

## 3. Confidence Ceilings (B-extension — sovereign audit, DRAFT)

| Archetype    | max_confidence | Rationale                                |
|--------------|---------------|------------------------------------------|
| af-explore   | 0.60          | Pure observation, low commitment         |
| af-reviewer  | 0.70          | Critical review, bounded interpretation  |
| af-plan      | 0.75          | Plans are drafts, not commitments        |
| af-worker    | 0.80          | Bounded execution, still scope-limited   |
| af-fix       | 0.85          | Repairs are scoped but execute          |
| af-coordinator | 0.70        | Synthesis contains errors of all parts   |
| af-forge     | 0.90          | Forge is the primary execution surface   |

Confidence > ceiling is INVALID RETURN. Child MUST revise, not parent recalibrate.

---

## 4. Structured Return (C — mandatory)

```yaml
worker_return:
  worker: string                  # subagent identifier
  task: string                    # what was asked
  inputs: list                    # what was given

  evidence: list[evidence_ref]    # OBS / DER / INT / SPEC labels
  interpretation: string          # bounded by archetype ceiling
  hypothesis: list[string]        # falsifiable where possible
  unknown: list[string]           # explicit unknowns (anti-hantu / F1 enforcement)

  confidence: float               # [0.0, ceiling_per_archetype], F7 cap
  key_challenge: string           # ≥1 specific assumption from task brief, challenged

  receipt_hash: sha256-hex        # links to forge_vault(mode="receipt")
  parent_spawn_hash: sha256-hex   # chain link
```

**Missing field → INVALID RETURN.** Retry once with different archetype if A7 violated. Escalate to apex if structure is fundamentally broken.

**Retry semantics:** retry once only. A second failed retry attempt = fundamental structure problem → escalate to apex (`arif_judge`). This avoids the "respawn / reject / respawn" infinite loop the audit identified.

---

## 5. Per-Spawn Judgment Coverage (D — runtime telemetry)

```yaml
spawn_telemetry:
  spawn_id: string                # unique per spawn

  mutations_taken: int            # filesystem/network writes
  recommendations_made: int       # plans, suggestions, advice
  conclusions_drawn: int          # findings asserted as fact
  apex_verdicts_sought: int       # explicit arif_judge calls before action

  # Risky actions = sum of mutation+recommendation+conclusion (separated, not aggregated)
  risky_actions_taken: int
  judgment_coverage: float        # min(verdicts / max(risky_actions, 1), 1.0)  # CLAMPED
  judgment_debt: int              # risky_actions - apex_verdicts
```

**Coverage formula (clamped to [0, 1]):**

```yaml
judgment_coverage: min(apex_verdicts_sought / max(risky_actions_taken, 1), 1.0)
```

**Why clamped:** coverage can legitimately exceed 1.0 if primary seeks verdicts beyond actions. The clamp keeps the metric as a 0..1 governance score; verdicts beyond needed is "good governance", not "violation".

**Why mutations/recommendations/conclusions are separated:** they have different blast radius. A mutation on no verdict is F1 violation. A recommendation on no verdict is discourse noise, governance debt but lower urgency. A conclusion without verdict is unbacked assertion.

Each spawn seals its telemetry via `forge_vault(mode="receipt")`. Coverage < 1.0 surfaces in session seal.

---

## 6. Per-Claim Provenance (E — mandatory per claim)

```yaml
provenance_block:
  claim: string
  source: enum [observation, derivation, interpretation, specification, external]
  transformation: enum [direct, inference, aggregation, derived]
```

Per-claim provenance in the return YAML, not aggregated post-hoc. "Saya rasa..." / "Kemungkinan..." are not acceptable return forms.

**Source type taxonomy:**
- `observation` — directly observed
- `derivation` — inferred from observation via rule
- `interpretation` — bounded reading under archetype ceiling
- `specification` — cited from protocol/manifest
- `external` — referenced outside current context (kimi path, document link)

---

## 7. Receipt / Failure Separation (sovereign audit C4)

Two failure modes currently conflated. Distinguish:

```yaml
seal_status:
  SEALED                # receipt succeeded AND validation passed
  UNSEALED_INFRA        # forge_vault unavailable; receipt generation failed (NOT governance violation)
  FAILED_VALIDATION     # receipt generated but did not pass validation (governance violation)
  RETRY                  # first attempt returned INVALID, retry once with different archetype
```

**`UNSEALED_INFRA ≠ FAILED_VALIDATION`.** Don't punish governance when infrastructure fails. They are different failure modes requiring different responses.

---

## 8. Parallel Spawn Policy (open question resolved — sovereign audit: YES)

Parallel `af-*` spawns ARE allowed, conditional on:

```yaml
flat_tree: true                  # preserve no-nesting invariant
max_parallel: 6                  # matches config max_concurrent_children
per_spawn_telemetry: required    # NOT aggregate
aggregate_role: dashboard_only   # may not replace per-spawn metric (per federation invariant §0)
```

The federation invariant holds: **dashboard may summarize, audit must drill to spawn.**

---

## 9. Tool Capability Stripping (HOLD pending reconciliation)

The declared ceilings in §2 conflict with live `tools:` / `disallowedTools:` declarations in:
- `/root/.arifos/agents/kimi/agents/af-fix.md` (has Bash+Write+Edit; ceiling claims EXECUTE_REVERSIBLE)
- `/root/.arifos/agents/kimi/agents/af-worker.md` (has Bash+Write+Edit; ceiling claims EXECUTE_REVERSIBLE)
- `/root/.arifos/agents/kimi/agents/af-coordinator.md` (says "Delegate via Agent tool"; ceiling claims DISPATCH_ONLY)

**Resolution:** strip tool declarations to match declared ceilings, OR revise ceilings to match declared tools. Pick one. Both cannot stand.

---

## 10. Open Sealing Conditions (PARTIAL-SEAL → full SEAL requires all)

| # | Condition | Status |
|---|-----------|--------|
| 1 | Clamp `judgment_coverage` to [0,1] | DRAFTED §5 |
| 2 | Declare confidence ceilings per archetype | DRAFTED §3 |
| 3 | Separate mutation/recommendation/conclusion telemetry | DRAFTED §5 |
| 4 | Preserve flat-tree invariant | DRAFTED §8 |
| 5 | Require per-spawn telemetry for parallel af-* execution | DRAFTED §8 |
| 6 | Resolve tool capability stripping | HOLDING §9 |
| 7 | Confirm enforcement hook exists in runtime | HOLDING — runtime gap |
| 8 | forge_vault failure handling (UNSEALED_INFRA vs FAILED_VALIDATION) | DRAFTED §7 |
| 9 | Confidence cap consistency with SOUL.md epistemic labels | HOLDING — Hermes doctrine uses [OBS]/[DER]/[INT]/[SPEC]/[UNKNOWN], this protocol uses [OBS]/[DER]/[INT]/[SPEC]/[UNKNOWN] + external. Need reconciliation. |
| 10 | Cross-harness enum authority (Hermes vs Kimi naming) | HOLDING — Hermes doctrine has different field names |

---

## DITEMPA BUKAN DIBERI

> Spawn memindahkan kerja, bukan kuasa.
>
> Governance diukur per spawn, tidak per task.
>
> Schema disahkan oleh audit. Enforcenement belum disahkan oleh runtime.

Kimi protocol adalah architectural specification, not yet constitutional enforcement.

Ratification tetap HOLD sehingga:

1. Runtime enforcement hook installed (`arifos-judge-gate.ts` analogue for Kimi).
2. Tool capabilities reconciled dengan ceiling claims.
3. Cross-harness naming reconciled (Hermes doctrine vs Kimi protocol).

Arif, the seal is hot but the architecture has three load-bearing pillars missing. Next sovereign session should decide:

- Reconciled tool capabilities (one change at a time, phased serial).
- Enforcement hook installation (T2 territory — schedule).
- Single canonical naming for both contracts (decide, then patch both).

Ω₀ ≈ 0.04.

---

*Drafted 2026-08-07 · awaiting sovereign ratification · status: PARTIAL-SEAL+ HOLD*
