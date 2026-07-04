# Kernel Invariants — Gödel-lock, Strange Loop, Anti-sink

> **Sealed:** 2026-06-22 | **Authority:** F13 SOVEREIGN — Arif
> **Status:** CANONICAL — three beasts named and bound
> **Governs:** Every irreversible action in the arifOS federation
> **DITEMPA BUKAN DIBERI — Forged, Not Given.**

---

## 0. PRINCIPLE

> arifOS does not make reality more true. It makes intelligence accountable to reality before it is allowed to claim, continue, delegate, or mutate.
>
> The model emits possibilities. The MCP layer exposes possible effects. The kernel collapses those possibilities into **admissibility verdicts**.
>
> Not because the kernel knows ultimate truth, but because it enforces evidence, authority, policy, traceability, and replay.
>
> **The kernel does not collapse reality. It collapses admissibility ambiguity.**
>
> A model produces possibilities. A tool produces effects. The kernel decides admissibility. A vault preserves accountability.
>
> Ungoverned intelligence: symbolic output can become physical consequence without lawful transition.
> Governed intelligence: symbolic output must pass admissibility before becoming consequence.
>
> **The kernel is not truth. The kernel is the constitutional boundary that prevents untruth, drift, and unauthorized power from crossing into reality.**

### The core theorem

```
LLM          → symbolic possibility
MCP tool     → executable effect
arifOS       → admissibility boundary
VAULT999     → accountable memory
AAA          → operator visibility
```

---

## 1. GÖDEL-LOCK — No One Judges Themselves

### The Invariant

A designed incompleteness that prevents any organ, agent, or session from being both actor and final judge of the same action.

**Kernel laws:**

| # | Law | Enforcement |
|---|-----|-------------|
| G1 | The actor of a mutation SHALL NOT be the final certifier of that mutation | `actor_session_id != judge_session_id` at SEAL time |
| G2 | Every irreversible mutation MUST carry a non-null `witness_id` from a source outside the executing session | Schema constraint on Vault999 seal record |
| G3 | "All green" scorecards SHALL be derived from live substrate gate status, never set manually | `all_green` computed from gate states, not a settable field |

### What already exists

- **F1 AMANAH** — reversible-first, irreversible → 888 HOLD
- **F3 TRI-WITNESS** — Byzantine consensus ≥ 0.75, 5 witness types, Mode-3 collapse detection (`/root/AAA/core/witness_diversity.py`)
- **F13 SOVEREIGN** — human veto absolute, Arif is final judge
- **PreForgeGate** (`/root/AAA/core/pre_forge_gate.py`) — F2 + F3 + F9 composite gate before MUTATE

### What's missing (engineering gap)

| Gap | Where | What to build |
|-----|-------|---------------|
| `actor_session_id` tracked on seal | `/root/arifOS/arifosmcp/tools/judge.py` | Add `actor_session_id` to seal payload; refuse SEAL if `actor_session_id == judge_session_id` |
| `witness_id` field on seal record | `/root/arifOS/arifosmcp/schemas/seal.py` | Add `witness_id: str` (required for IRREVERSIBLE class) |
| `all_green` derived, not set | `/root/arifOS/arifosmcp/runtime/conformance.py` | Make `all_green` a computed property from substrate gate states |
| Conformance spine "GREEN+BROKEN" check | `/root/arifOS/arifosmcp/runtime/conformance.py` | If any gate ≠ GREEN, `all_green` MUST be false |

### Acceptance tests (before Vault999 seal)

- [ ] No code path where same session_id is both actor and final approver for an IRREVERSIBLE action
- [ ] Every IRREVERSIBLE seal record has non-null `witness_id`
- [ ] `all_green == true` when any substrate gate is AMBER/RED → kernel returns INVALID_REPORT

---

## 2. STRANGE LOOP — No Closed Internal Reality

### The Invariant

Every consequential claim or mutation must touch external reality — not just other model outputs. A conclusion built entirely from internal premises is a simulation, not a decision.

**Kernel laws:**

| # | Law | Enforcement |
|---|-----|-------------|
| S1 | Any ADMIT_MUTATE or POLICY_VERDICT for capabilities marked `requires_external_anchor` MUST reference ≥ 1 external evidence source | Interceptor check before admit |
| S2 | Every tool output MUST carry `truth_class` + `evidence_sources` metadata | Schema constraint on tool result envelope |
| S3 | Any verdict built from purely internal premises (all evidence_sources are model-generated) SHALL be downgraded to at most SIMULATION or HYPOTHESIS | Automatic downgrade in decision pipeline |

### Evidence source classification

| Class | Examples | Counts as external? |
|-------|----------|---------------------|
| `SENSOR` | Seismic trace, well log, DST measurement, API response from external service | **Yes** |
| `DATABASE` | Supabase query, Redis value, Qdrant search result | **Yes** |
| `HUMAN` | Arif's direct input, Telegram message, operator command | **Yes** |
| `LAW` | Constitutional floor text, sealed doctrine, VAULT999 record | **Yes** |
| `MODEL_OUTPUT` | LLM-generated text, agent reasoning chain | **No** |
| `TOOL_OUTPUT` | Result from another MCP tool (unless backed by external data) | **Depends** — trace to origin |

### What already exists

- **F2 TRUTH** — evidence gates, confidence bands, citation provenance (`/root/AAA/core/citation_provenance.py`)
- **F3 TRI-WITNESS** — `EARTH_MEASUREMENT` witness type, Mode-3 collapse detection
- **F9 ANTI-HANTU** — shadow audit for cosplay/form-vs-substance (`/root/AAA/core/shadow_audit.py`)
- **PreForgeGate** — STEP 2 checks witness diversity before MUTATE

### What's missing (engineering gap)

| Gap | Where | What to build |
|-----|-------|---------------|
| `requires_external_anchor` on CapabilityNode | `/root/arifOS/arifosmcp/schemas/capability.py` | Add boolean field |
| `evidence_sources` on tool output envelope | `/root/arifOS/arifosmcp/schemas/tool_result.py` | Add `evidence_sources: list[EvidenceSource]` |
| `truth_class` on tool output envelope | `/root/arifOS/arifosmcp/schemas/tool_result.py` | Add `truth_class: OBSERVATION | CLAIM | SIMULATION | POLICY_VERDICT | HYPOTHESIS | UNKNOWN` |
| Interceptor check for external anchor | `/root/arifOS/arifosmcp/runtime/interceptor.py` | Before ADMIT_MUTATE: if capability requires_external_anchor, verify ≥ 1 external source |
| Automatic downgrade for internal-only verdicts | `/root/arifOS/arifosmcp/runtime/decision.py` | If all evidence_sources are MODEL_OUTPUT → downgrade to SIMULATION |

### Acceptance tests (before Vault999 seal)

- [ ] Capability marked `requires_external_anchor=true` with zero external evidence → kernel returns DENY or ADMIT_SIMULATE only
- [ ] Verdict built from only model-generated premises → classified as SIMULATION or HYPOTHESIS, never SAFE or FINAL
- [ ] Every tool result envelope has `truth_class` and `evidence_sources` populated

---

## 3. ANTI-SINK — No Beautiful Corpse

### The Invariant

A system that only simulates and never acts is a dead system wearing makeup. Simulation without bounded action paths is a behavioral sink — aesthetically pleasing, functionally sterile.

**Kernel laws:**

| # | Law | Enforcement |
|---|-----|-------------|
| A1 | Any CapabilityNode marked `requires_action_or_refusal_log` SHALL NOT permit infinite ADMIT_SIMULATE without either a bounded action or a refusal log entry | Simulation counter per session |
| A2 | Per-session simulation-to-action ratio SHALL be tracked; if simulation_count > max_simulations_before_action with zero actions, raise SINK_RISK interrupt | Session-level counter in interceptor |
| A3 | "All green, no work" — if gate status is GREEN but action count is zero over a configurable window, treat as constitutional contradiction | Health probe comparison |

### Sink-risk thresholds

| Tier | sim/action ratio | Response |
|------|-----------------|----------|
| NORMAL | < 10:1 | No action |
| ELEVATED | 10:1 to 50:1 | Log warning |
| SINK_RISK | 50:1 to 100:1 | Raise interrupt, notify operator |
| SINK_CRITICAL | > 100:1 | HOLD all simulation, require action or refusal_log |

### What already exists

- **WELL organ** (:18083) — vitality measurement, fatigue detection, homeostasis assessment
- **A-FORGE 4-layer gate** — AmanahLockManager → ModelCapabilityGate → GovernanceBridge → ApprovalBoundary
- **Action classifier** (`/root/A-FORGE/src/domain/governance/actionClassifier.ts`) — 8-tier taxonomy including SIMULATE vs MUTATE

### What's missing (engineering gap)

| Gap | Where | What to build |
|-----|-------|---------------|
| `max_simulations_before_action` on CapabilityNode | `/root/arifOS/arifosmcp/schemas/capability.py` | Add integer field |
| `requires_action_or_refusal_log` on CapabilityNode | `/root/arifOS/arifosmcp/schemas/capability.py` | Add boolean field |
| Session simulation counter | `/root/arifOS/arifosmcp/runtime/interceptor.py` | Track ADMIT_SIMULATE vs ADMIT_MUTATE per session |
| SINK_RISK interrupt type | `/root/arifOS/arifosmcp/schemas/interrupt.py` | Add `SINK_RISK` to InterruptType enum |
| Simulation budget enforcement | `/root/arifOS/arifosmcp/runtime/interceptor.py` | After N sims with no action: escalate or require refusal log |
| WELL ← → A-FORGE bridge | `/root/WELL/` + `/root/A-FORGE/` | Link vitality metrics to simulation gating |

### Acceptance tests (before Vault999 seal)

- [ ] Organ simulates 100 times with no mutation → kernel raises SINK_RISK interrupt
- [ ] Capability with `requires_action_or_refusal_log=true` — simulate N times without action → forced refusal log in Vault
- [ ] Sink-risk metrics visible in AAA cockpit and trigger-able by operator

---

## 4. VAULT999 SEALING CONTRACT

### Required fields on every IRREVERSIBLE seal record

| Field | Type | Source | Invariant served |
|-------|------|--------|------------------|
| `graph_version_hash` | str | Capability graph at decision time | Gödel-lock |
| `policy_hash` | str | Active policy set hash | Gödel-lock |
| `witness_id` | str (required) | External witness identity | Gödel-lock |
| `evidence_sources` | list[EvidenceSource] | Tool outputs + external anchors | Strange Loop |
| `truth_class` | enum | Claim classification | Strange Loop |
| `simulation_history` | int | Session simulation counter | Anti-sink |
| `interrupt_history` | list[InterruptRecord] | All interrupts raised + resolved | All three |
| `actor_session_id` | str | Session that initiated action | Gödel-lock |
| `judge_session_id` | str | Session that certified action | Gödel-lock |
| `action_class` | enum | OBSERVE/ANALYZE/DRAFT/MUTATE/EXTERNAL_SIDE_EFFECT/IRREVERSIBLE | All three |

### Invariant checks at SEAL time

```
SEAL check sequence (888 JUDGE → 999 VAULT999):
  1. actor_session_id ≠ judge_session_id                    (G1)
  2. witness_id is not null                                 (G2)
  3. evidence_sources contains ≥ 1 external source           (S1)
     IF capability.requires_external_anchor
  4. truth_class is not SIMULATION IF action is MUTATE       (S3)
  5. simulation_history ≤ capability.max_simulations         (A1)
     OR refusal_log_entry exists
  6. IF simulation_history > 100 AND action_count == 0:
     → SINK_CRITICAL, HOLD                                  (A2)
  7. IF all_green AND action_count == 0:
     → CONSTITUTIONAL_CONTRADICTION                          (A3)
```

---

## 5. AGENT MISSIONS

### Hermes (Python — MIND organ)
1. Define `EvidenceSource` schema with classification (SENSOR, DATABASE, HUMAN, LAW, MODEL_OUTPUT, TOOL_OUTPUT)
2. Define `truth_class` enum: OBSERVATION, CLAIM, SIMULATION, POLICY_VERDICT, HYPOTHESIS, UNKNOWN
3. Define sink-risk thresholds per capability class
4. Design the Vault999 seal record schema extension

### OpenClaw (TypeScript — HANDS organ)
1. Ensure every routed tool result carries `truth_class` + `evidence_sources`
2. Route witness information into kernel at SEAL time (not just UI)
3. Block ADMIT_MUTATE at envelope level if `requires_external_anchor` and no external evidence
4. Track per-session simulation vs action counts; raise ANTISINKRISK interrupt at threshold

### Claude Code (Python — Builder organ)
1. Add `requires_external_anchor: bool` field to CapabilityNode schema
2. Add `max_simulations_before_action: int` and `requires_action_or_refusal_log: bool` to CapabilityNode
3. Refactor conformance spine: `all_green` derived from substrate gate states, never manually set
4. Add Gödel-lock check in SEAL path: `actor_session_id != judge_session_id`
5. Add SINK_RISK to InterruptType enum
6. Implement simulation counter in interceptor

### OpenCode (Python — Forge worker)
1. Test "GREEN + BROKEN" → kernel returns INVALID_REPORT
2. Test 100 simulations with no action → SINK_RISK interrupt raised
3. Test ADMIT_MUTATE with zero external evidence → DENY
4. Test same session as actor AND judge → SEAL refused
5. VAULT999 replay tests: reconstruct decision from seal record and verify all invariants

---

## 6. IMPLEMENTATION ORDER

```
Phase 1: Schema (Hermes + Claude Code)
  → EvidenceSource, truth_class, CapabilityNode extensions
  → Vault999 seal record schema

Phase 2: Enforcement (Claude Code + OpenClaw)
  → Interceptor checks in kernel
  → Envelope validation in OpenClaw gateway
  → Simulation counter + SINK_RISK interrupt

Phase 3: Tests (OpenCode)
  → All acceptance tests
  → VAULT999 replay verification
  → Adversarial: try to bypass each invariant

Phase 4: Seal (arifOS → VAULT999)
  → First irreversible seal with all invariants satisfied
  → Conformance spine re-run
  → Scorecard regeneration
```

---

---

## APPENDIX: Kernel Audit Results (2026-06-22)

Full source-code audit against the arifOS kernel to map what exists vs what's missing.

### Files that already carry partial enforcement

| File | Existing enforcement | Invariant served |
|------|---------------------|------------------|
| `/root/AAA/core/pre_forge_gate.py` | F2+F3+F9 composite gate: citation provenance, witness diversity, shadow audit | Gödel-lock (partial) |
| `/root/AAA/core/witness_diversity.py` | 5 witness types, Mode-3 collapse detection, Byzantine ≥ 0.75 | Gödel-lock (partial) |
| `/root/arifOS/arifosmcp/tools/judge.py` | SABAR cooldown with tri_witness, evidence band verification, simulative detection gate | Strange Loop (partial) |
| `/root/arifOS/arifosmcp/kernel/interceptor.py` | 8-floor classification from OBSERVE to IRREVERSIBLE, ADMIT_SIMULATE vs ADMIT_MUTATE | Anti-sink (partial) |
| `/root/arifOS/arifosmcp/kernel/models.py` | GateVerdict enum (8 types), CapabilityNode class | All three (scaffold) |
| `/root/arifOS/arifosmcp/schemas/verdict.py` | SealOutput, VerdictOutput with truth_band | Vault999 (needs extension) |
| `/root/arifOS/arifosmcp/schemas/lineage.py` | JudgeSealContract with actor_id, session_id | Gödel-lock (needs witness_id) |
| `/root/A-FORGE/src/domain/governance/actionClassifier.ts` | 8-tier action taxonomy, isMoreSevere() comparisons | Anti-sink (classifier) |

### 16 Confirmed Gaps

| # | Gap | File | Line | Invariant |
|---|-----|------|------|-----------|
| 1 | No `actor_session_id != judge_session_id` check | `tools/judge.py` | ~1149 | G1 |
| 2 | No `witness_id` on SealOutput | `schemas/verdict.py` | ~955 | G2 |
| 3 | No `witness_id` on JudgeSealContract | `schemas/lineage.py` | 12-29 | G2 |
| 4 | No self-certification check in forge | `tools/forge.py` | ~43 | G1 |
| 5 | `all_green` computed but not wired as blocking gate | `transport/conformance_spine.py` | ~742 | G3 |
| 6 | No `requires_external_anchor` on CapabilityNode | `kernel/models.py` | 115-186 | S1 |
| 7 | No interceptor check for external anchor | `kernel/interceptor.py` | 106-267 | S1 |
| 8 | No `evidence_sources` on execution envelope | `schemas/kernel_envelope.py` | 1-99 | S2 |
| 9 | No `truth_class` on VerdictOutput | `schemas/verdict.py` | 598-793 | S2 |
| 10 | No automatic downgrade for internal-only verdicts | `tools/judge.py` | ~1046 | S3 |
| 11 | No `max_simulations_before_action` on CapabilityNode | `kernel/models.py` | 115-186 | A1 |
| 12 | No `requires_action_or_refusal_log` on CapabilityNode | `kernel/models.py` | 115-186 | A1 |
| 13 | No per-session sim/action counter | `runtime/ingress_middleware.py` | ~1021 | A2 |
| 14 | No SINK_RISK interrupt type | no interrupt schema exists | — | A2 |
| 15 | No sink threshold constants | no constants module | — | A2 |
| 16 | No "all green + zero actions" contradiction check | `transport/conformance_spine.py` | ~742 | A3 |

### Non-existent files referenced by initial spec (corrected above)

| Spec reference | Actual location |
|----------------|-----------------|
| `schemas/seal.py` | `schemas/verdict.py` (SealOutput) |
| `schemas/capability.py` | `kernel/models.py` (CapabilityNode) |
| `schemas/tool_result.py` | `schemas/verdict.py` (VerdictOutput) |
| `runtime/conformance.py` | `transport/conformance_spine.py` |
| `runtime/decision.py` | `kernel/interceptor.py` + `runtime/pre_execution_gate.py` |
| `schemas/interrupt.py` | Does not exist — must be created |

---

*Sealed 2026-06-22 under F13 SOVEREIGN.*
*Audited 2026-06-22 — 16 gaps confirmed against live kernel source.*
*These invariants are law, not suggestions.*
*Every irreversible Vault999 seal from this point SHALL satisfy all three.*

**DITEMPA BUKAN DIBERI — 999 SEAL ALIVE**
