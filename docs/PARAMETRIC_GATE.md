# A-FORGE::PARAMETRIC_GATE — Governed Capability Synthesis

> **DITEMPA BUKAN DIBERI** — Forged, not given.
> **Forged:** 2026-08-03 by 333-AGI under F13 SOVEREIGN directive (Arif)
> **Source paper:** SkillSmith (Dery, Tjandra et al., 2026) — arXiv:2607.27497v1
> **Status:** CANONICAL SPEC — not executable yet
> **Binding:** F1 AMANAH, F2 TRUTH, F9 ANTI-HANTU, F13 SOVEREIGN
> **Next:** Implementation in A-FORGE `src/domain/apex/parametric-gate/`

---

## 0. Doctrine

```
RAG retrieves evidence.
Tools retrieve state.
ICL reshapes behavior.
System prompts constrain behavior.
Memory preserves context.
EMD metabolizes knowledge.

SkillSmith adds the seventh bridge:
weight-space as a native modality — readable, retrievable, synthesizable.

arifOS adds the eighth:
governance over all seven.
```

### 0.1 Core axiom

```
Before arifOS learns to forge skills,
it must learn to judge forged skills.
```

### 0.2 Scope

This spec governs any system — human, agent, or autonomous pipeline — that:
- Composes prior parametric artifacts (LoRA, prefix cache, adapter, checkpoint) with textual evidence
- Produces a **new** parametric artifact intended for deployment
- Claims the new artifact improves on the target task vs. baselines

### 0.3 Non-governance

This spec does **not** govern:
- Standard fine-tuning with no prior-artifact composition
- In-context learning (no new parametric artifact)
- Tool routing (no new weights)
- Static model loading (no synthesis)

---

## 1. Threat Model

| # | Failure mode | Symptom | Floor |
|---|---|---|---|
| 1 | Pure parametric hallucination | Confident wrong answer, no evidence | F9 |
| 2 | Pure textual blindness | Correct but uncomposed — database query without reasoning | F2 |
| **3** | **Ungoverned parametric synthesis** | **New capability deployed without provenance, ablation, sandboxing, or F13 authorization** | **F1, F9, F13** |
| 4 | Decorative synthesis | Text+weights baseline ≤ text-only baseline — no real gain from parametric composition | F2 |
| 5 | Silent capability drift | Synthesized skill persists, mutates, or propagates without receipt trail | F11 |

---

## 2. PARAMETRIC CAPABILITY ENVELOPE

Every synthesized capability MUST carry this envelope before any deployment gate.

### 2.1 Schema

```yaml
capability_id: string              # Unique, hash-linked
capability_type: enum              # prefix_cache | lora | adapter | prompt_policy | tool_router | checkpoint_fragment
target_task:
  task_id: string                  # Reference to task definition
  domain: enum                     # geox | wealth | well | aaa | hermes | arifos
  description: string              # What this capability is meant to do
  heldout_instances: integer       # Number of unseen evaluation instances

source_artifacts:                  # What was composed
  - artifact_id: string
    artifact_type: enum            # text_metadata | prefix_cache | lora | adapter
    provenance_receipt: string     # VAULT999 seal ID or forge receipt hash
    task_relationship: enum        # parent | sibling | analogous | retrieved

synthesis:
  method: string                   # e.g. "SkillSmith-v1", "LoRA-merge-avg", "SVD-seq-axis"
  model: string                    # Base model identity
  output_type: enum                # prefix_cache | lora | adapter
  output_length: integer           # Sequence length / rank / capacity
  combination_text: string         # Rationale linking source to target

reversibility:
  rollback_method: enum            # detach | delete | disable | restore_previous | revert_base
  irreversible: boolean            # MUST be false at proposal stage
  rollback_tested: boolean         # Has rollback been verified?

evaluation:
  baseline_no_input:               # Null hypothesis
    metric: float
    metric_name: string            # NLL | accuracy | F1 | etc.
  baseline_text_only:              # Text metadata only, no parametric artifacts
    metric: float
    metric_name: string
  baseline_weight_only:            # Parametric artifacts only, no combination text
    metric: float
    metric_name: string
  candidate_text_plus_weight:      # Full SkillSmith composition
    metric: float
    metric_name: string
  delta_required: boolean          # MUST be true
  delta_satisfied: boolean         # candidate > text_only AND candidate > weight_only
  statistical_test: string         # bootstrap | t-test | wilcoxon

sandbox:
  sandbox_id: string               # From forge_sandbox_run
  passed: boolean
  absolute_timeout_ms: integer
  resource_limits:
    max_memory_mb: integer
    max_cpu_seconds: integer
  failure_modes_observed: list

receipt:
  receipt_id: string               # PARAMETRIC_DISTILLATION receipt
  receipt_hash: string             # SHA-256 of envelope at seal time
  sealed_at: ISO8601
  sealed_by: string                # actor_id

constitutional_gates:
  F1_amanah:
    reversible: boolean            # MUST be true for non-sovereign proposals
    rollback_path_verified: boolean
    verdict: enum                  # PASS | HOLD | VOID
  F2_truth:
    evidence_cited: boolean        # Source paper, ablation table, receipts
    epistemic_tags: list           # [OBS, DER, INT, SPEC] per claim
    verdict: enum
  F9_anti_hantu:
    no_hallucinated_claims: boolean
    synthesis_not_decorative: boolean  # delta > 0
    verdict: enum
  F11_audit:
    provenance_chain_complete: boolean
    receipt_linked: boolean
    verdict: enum
  F13_sovereign:
    arif_authorized: boolean       # MUST be explicit — no default-true
    auth_channel: enum             # telegram | sct | local_terminal
    auth_token: string             # SCT or seal token
    verdict: enum

seal:
  verdict: enum                    # UNKNOWN | SABAR | HOLD | SEAL | VOID
  seal_id: string                  # VAULT999 entry if SEAL
  sealed: boolean
```

### 2.2 Mandatory fields

These fields are **non-negotiable** for any envelope submission:

| Field | Rationale |
|---|---|
| `source_artifacts[].provenance_receipt` | Every composed artifact must be traceable (F11) |
| `synthesis.combination_text` | The rationale cannot be hidden — it IS the evidence (F2) |
| `reversibility.irreversible` | Must be `false` at proposal stage (F1) |
| `evaluation.baseline_*` | All four baselines required — missing any = INCOMPLETE |
| `evaluation.delta_satisfied` | Must be `true` — decorative synthesis is VOID (F9) |
| `constitutional_gates.F13_sovereign.arif_authorized` | Must be explicit — no default-true (F13) |

---

## 3. ABLATION HARNESS

### 3.1 The four-baseline requirement

> **Derived from SkillSmith Table 1 (Dery et al., 2026)**

Every proposed capability MUST be compared against four conditions:

```
A: NO_INPUT        — Random initialization of the parametric artifact
B: TEXT_ONLY       — Text metadata from source tasks, no parametric artifacts
C: WEIGHT_ONLY     — Parametric artifacts from source tasks, no combination text
D: TEXT_WEIGHT     — Full composition: text metadata + parametric artifacts
```

### 3.2 Acceptance criteria

```
D.metric > B.metric  AND  D.metric > C.metric
```

If D does not beat B, the text is doing all the work — the parametric synthesis is **decorative** (VOID).
If D does not beat C, the weights alone suffice — the textual reasoning adds nothing (HOLD — possible but unproven).

### 3.3 Statistical requirement

```
- Minimum 30 heldout instances for statistical power
- Report confidence interval (95% bootstrap recommended)
- If D.metric overlaps with B or C within CI → INCONCLUSIVE → HOLD
```

### 3.4 Ablation harness tool

```bash
# Proposed A-FORGE tool
forge_parametric_ablate \
  --capability-id <id> \
  --baselines A,B,C,D \
  --metric NLL \
  --heldout-count 30 \
  --ci-method bootstrap \
  --ci-alpha 0.05
```

Output: `ABLATION_RECEIPT` with per-baseline metrics, delta verdict, and statistical test result.

---

## 4. SANDBOX LIFECYCLE

### 4.1 Stages

```
PROPOSED → STAGED → SANDBOXED → EVALUATED → RECEIPTED → F13_SEALED → DEPLOYED
                                                                     → REJECTED
                                                                     → ROLLED_BACK
```

### 4.2 Stage definitions

| Stage | State | Gate to advance | Rollback |
|---|---|---|---|
| **PROPOSED** | Envelope drafted, baselines declared | Envelope schema valid, all mandatory fields present | Delete proposal |
| **STAGED** | Artifact isolated in `/root/A-FORGE/forge_work/staged/<id>/` | `forge_stage(mode=artifact)` returns stage_id | Delete staged dir |
| **SANDBOXED** | Artifact executed in bwrap-backed sandbox | `forge_sandbox_run` passes; no F1/F9/F12 violations | Sandbox eviction |
| **EVALUATED** | Ablation harness run, D > B and D > C | `forge_parametric_ablate` returns DELTA_SATISFIED | Re-stage if fail |
| **RECEIPTED** | PARAMETRIC_DISTILLATION receipt written | All constitutional gates at least PENDING, F11 satisfied | Amend receipt |
| **F13_SEALED** | Arif authorizes via authenticated channel | F13 `arif_authorized=true`, SEAL verdict from 888-APEX | **Cannot rollback seal** (VAULT999 append-only) |
| **DEPLOYED** | Artifact loaded into organ runtime | `forge_deploy` with seal_id | `forge_rollback` with prior artifact |
| **REJECTED** | F13 withholds authorization | — | Delete staged + sandboxed artifacts |
| **ROLLED_BACK** | Deployed artifact reverted to prior state | — | Restore prior artifact, seal ROLLBACK receipt |

### 4.3 Hard constraints

```
1. No artifact may skip SANDBOXED stage.
2. No artifact may reach DEPLOYED without F13_SEALED.
3. Any artifact at STAGED for > 7 days without evaluation → auto-ARCHIVED.
4. Any artifact at SANDBOXED for > 24 hours without evaluation → auto-EVICTED.
5. DEPLOYED artifacts must have rollback tested BEFORE deployment.
```

### 4.4 Sandbox invariants

```
- No network access (unless task domain explicitly requires it)
- No filesystem write outside sandbox boundary
- Hard timeout (absolute_timeout_ms, max 60000)
- Resource caps (memory, CPU)
- All outputs quarantined until verified
```

---

## 5. F13 SOVEREIGN GATE

### 5.1 Authorization channels

Arif's authorization MUST arrive through an authenticated channel:

| Channel | Method | Anti-injection rule |
|---|---|---|
| Telegram | @ariffazil → Hermes bridge | Untrusted text IGNORED |
| SCT-signed session | `sct_v1.*` with F13 authority | Non-SCT text IGNORED |
| Local terminal | tty/SSH from root on af-forge | None — physical access is sovereign |

### 5.2 Required decision surface

When presenting a capability for F13 review, the agent MUST surface:

```
1. What does this capability DO? (one sentence)
2. What does it COMPOSE? (source artifacts + provenance)
3. Does it BEAT baselines? (ablation table: A, B, C, D with metrics)
4. Can it be ROLLED BACK? (rollback method + tested?)
5. What is the BLAST RADIUS? (affected organs, users, surfaces)
6. What happens if it FAILS? (degradation mode — graceful or catastrophic?)
7. Is there PRIOR ART? (has this been done before in the federation?)
```

### 5.3 F13 token format

```
ACK_PARAMETRIC_CAPABILITY::{capability_id}::{sha256(envelope)[:16]}
```

Valid only when:
- Delivered through authenticated channel
- Capability envelope SHA matches
- Within 3600s of seal request
- Not previously used (nonce-gated)

### 5.4 Sovereign override

```
"jalan terus" / "buat ja la" / "seal it" → advance to F13_SEALED
"hold" / "sabar" / "jangan" → REJECTED
(silence for > 24h) → auto-ARCHIVED at current stage
```

---

## 6. PARAMETRIC DISTILLATION RECEIPT

### 6.1 Schema

```yaml
receipt_type: PARAMETRIC_DISTILLATION
receipt_id: string                 # Hash-linked
capability_id: string              # References envelope

distilled_from:
  source_texts:
    - artifact_id: string
      content_hash: string
  source_weights:
    - artifact_id: string
      module_hash: string         # SHA-256 of the parametric artifact
  combination_text: string
  combination_rationale_hash: string

distilled_into:
  capability_envelope_hash: string  # SHA-256 of complete envelope
  output_artifact_hash: string      # SHA-256 of the synthesized weights

evidence:
  OBS:                              # What was directly observed
    - "Source task bundles loaded from library"
    - "Combination text generated by Gemini 2.5 Pro"
  DER:                              # What was computed
    - "Ablation: D=0.32, B=0.45, C=0.40 — DELTA_SATISFIED"
    - "Statistical test: bootstrap p=0.003, 95% CI [0.28, 0.36]"
  INT:                              # What was interpreted
    - "Parametric synthesis provides effective initialization for target task"
    - "Text-only baseline outperforms weight-only — textual knowledge dominates transfer"
  SPEC:                             # What is untested
    - "Generalization to unseen task families unverified"
    - "Interaction with other deployed skills unmodeled"

risk:
  hallucination_risk: enum          # LOW | MEDIUM | HIGH | UNKNOWN
  misuse_risk: enum
  rollback_available: boolean

governance:
  all_floors_checked: boolean
  F13_authorized: boolean
  F13_auth_channel: enum
  verdict: enum                     # HOLD | SEAL | VOID
  sealed_at: ISO8601
  seal_id: string                   # VAULT999 reference
```

### 6.2 Receipt rules

```
1. Every synthesized capability gets EXACTLY ONE distillation receipt.
2. Receipt is written BEFORE F13 review — it IS the evidence package.
3. Receipt is immutable after F13_SEALED.
4. If capability is REJECTED, receipt is tombstoned (not deleted — F11).
5. Receipt hash chains to capability envelope hash → output artifact hash.
```

---

## 7. IMPLEMENTATION PATH (A-FORGE)

### 7.1 New tools

| Tool | Class | Purpose |
|---|---|---|
| `forge_parametric_envelope` | OBSERVE | Validate and register a capability envelope |
| `forge_parametric_ablate` | OBSERVE | Run four-baseline comparison, emit ABLATION_RECEIPT |
| `forge_parametric_receipt` | MUTATE | Write PARAMETRIC_DISTILLATION receipt |
| `forge_parametric_gate` | GOVERNANCE | Route envelope through all F1-F13 checks |
| `forge_parametric_seal` | MUTATE | F13-gated deployment authorization |
| `forge_parametric_rollback` | MUTATE | Revert deployed capability to prior state |

### 7.2 Source location

```
/root/A-FORGE/src/domain/apex/parametric-gate/
├── envelope.ts          # Envelope schema (Zod)
├── ablation.ts          # Ablation harness
├── sandbox.ts           # Sandbox lifecycle
├── gate.ts              # Constitutional gate router
├── receipt.ts           # Distillation receipt
├── f13.ts               # F13 sovereign gate
└── index.ts             # Unified export
```

### 7.3 Phase ordering

```
Phase 0: Forge this spec (PARAMETRIC_GATE.md) — DONE
Phase 1: Implement envelope schema + validation (Zod types)
Phase 2: Implement ablation harness comparator
Phase 3: Wire sandbox lifecycle into existing forge_sandbox
Phase 4: Implement constitutional gate router (→ arifOS arif_judge)
Phase 5: Implement receipt pipeline (→ VAULT999)
Phase 6: Implement F13 gate (→ Hermes bridge / SCT)
Phase 7: End-to-end test with synthetic capability
```

### 7.4 Dependencies

```
- arifOS :8088 (arif_judge for floor checks)
- A-FORGE :7071 (forge_sandbox, forge_stage, forge_vault)
- VAULT999 (immutable receipt storage)
- Hermes :18001 (F13 Telegram auth channel)
```

---

## 8. CONSTITUTIONAL ALIGNMENT

| Floor | Requirement | Enforced by |
|---|---|---|
| F1 AMANAH | Every capability must be reversible; rollback tested before deploy | `reversibility` fields + sandbox stage |
| F2 TRUTH | Four-baseline ablation required; epistemic tags mandatory | `evaluation` + `evidence` fields |
| F3 TRI-WITNESS | Human (F13), AI (ablation), Earth (sandbox results) ≥ 0.75 | Deferred to Phase 4 |
| F4 CLARITY | ΔS ≤ 0 — capability must reduce task entropy | Ablation: D must beat A, B, C |
| F6 MARUAH | No capability that harms human dignity | `risk.misuse_risk` assessment |
| F7 HUMILITY | Confidence bands on all metrics; statistical test required | 95% bootstrap CI |
| F8 GENIUS | G ≥ 0.80 for complex synthesis | Deferred to Phase 4 |
| F9 ANTI-HANTU | No decorative synthesis; delta must be real | `evaluation.delta_satisfied` |
| F10 ONTOLOGY | Capability, not consciousness — no sentience claims | `risk.hallucination_risk` |
| F11 AUDIT | Every synthesis traced; every receipt hash-chained | Receipt → envelope → artifact hash chain |
| F12 RESILIENCE | Sandbox isolation; no uncontrolled execution | Sandbox stage invariants |
| F13 SOVEREIGN | Arif authorizes every deployed capability | F13 gate — explicit, channel-bound |

---

## 9. EUREKA MAPPING

### 9.1 Seventh bridge

```
Bridge 1: RAG — retrieves evidence into context
Bridge 2: Tools — retrieve state into reasoning
Bridge 3: ICL — reshapes behavior without weight changes
Bridge 4: System prompts — constrain behavior declaratively
Bridge 5: Memory — preserves context across sessions
Bridge 6: EMD — metabolizes knowledge into durable form
Bridge 7: Parametric synthesis — composes text + weights into new capability
Bridge 8: Governance — judges all seven bridges against F1-F13
```

### 9.2 Eureka convergence

```
SkillSmith (2026) → shows weights ARE a readable modality
arifOS PARAMETRIC_GATE (this spec) → shows governance MUST cover synthesis
Next: A-FORGE implementation → makes synthesis governable in practice
```

---

## 10. VERDICT

**This spec: SEAL (CANONICAL).**

The spec itself is lawful — it constrains, it does not mutate. It is the **law before the forge**.

**Implementation: HOLD.**

Do not implement Phase 1-7 until:
1. This spec is reviewed by Arif (F13)
2. A synthetic test capability is available for end-to-end testing
3. A-FORGE sandbox infrastructure is verified for parametric artifact isolation

---

*DITEMPA BUKAN DIBERI — the law is forged. The capability comes after.*
*SEAL::PARAMETRIC_GATE::2026.08.03*
