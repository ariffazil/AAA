# AAA-IR Migration Guide

**Status:** v1, frozen 2026-10-02
**Maintainer:** AAA Compilation Fabric steering
**Applies to:** all AAA organs (A-FORGE, HERMES, GEOX, WEALTH, WELL, CHRON, FRAME, arifFlow, arifOS, VAULT999)

---

## Purpose

Move AAA from skill-oriented routing to a **typed, measured, falsifiable control plane**.
Every state machine in the federation becomes a typed packet; every comparison becomes
a BridgeProof; every measurement carries a typed tuple instead of a naked status string.

This file is the **adoption order**. Every step is small, falsifiable, and reversible
until promoted to PROVEN. No legacy tombstoning happens until
`Behavior_old ~= Behavior_compiled` is verified for the affected surface.

---

## The seven invariants (machine-enforced)

| # | Invariant | Source |
|---|-----------|--------|
| 1 | `Identity != Capability != Authority != Dispatch != Execution != Evidence != Judgment != Seal` | IR_REGISTRY.v1 (original) |
| 2 | `CapabilityIndex (declared) != CapabilityGraph (measured)` | IR_REGISTRY.v1 |
| 3 | `MATCH/DRIFT forbidden until every equivalence edge carries measured evidence` | IR_REGISTRY.v1 |
| 4 | `Behavior_old ~= Behavior_compiled` REQUIRED before legacy tombstone | IR_REGISTRY.v1 |
| 5 | **NO EQUIVALENCE WITHOUT A BRIDGE PROOF** (`A == B iff Bridge(A,B)=WITNESSED`) | 2026-10-02 |
| 6 | **Same status word != same measured reality** (liveness ≠ availability ≠ integrity ≠ governance ≠ readiness ≠ outcome) | 2026-10-02 |
| 7 | **No naked status string** may be emitted (every measurement carries `metric/unit/scope/referent/method/baseline/observed_at/does_not_imply`) | 2026-10-02 |
| 8 | **`Type(A) == Type(B)` mandatory before any comparison** | 2026-10-02 |
| 9 | **`emitted_URL ∈ observed_URLs`** (renderer refuses hyperlink outside tool evidence) | 2026-10-02 |
| 10 | **EPISTEMIC STATE MUST NOT UPGRADE ACROSS AN AGENT HOP WITHOUT NEW EVIDENCE** | 2026-10-02 |
| 11 | **`BridgeProof` self-law** — relation != verification_state != probe_state. `ProbeFailure != RelationRefuted`. `TYPE_MISMATCH != DIVERGES_FROM` | 2026-10-02 |
| 12 | **`Comparable(A,B) = SameType(A,B) ∨ WitnessedBridge(A,B)`** — strict type-equality is too narrow; bridge functions make heterogeneous types comparable when witnessed | 2026-10-02 |

---

## Adoption order

The migration proceeds in **four tracks** running in parallel. Each track has
explicit gates; nothing moves to the next stage without the gate.

```
Track A — Substrate primitives (zero mutation)
Track B — Live probes emit typed packets
Track C — BridgeProof semantic
Track D — R6 readiness test (E_{n+1} < E_n)
```

### Track A — Substrate primitives (DONE 2026-10-02)

**Goal:** All twelve typed-ABI schemas exist and validate. No existing surface mutated.

| Schema | Question | Status |
|--------|----------|--------|
| IdentityPacket | what exactly is this thing? | SCHEMA_ONLY |
| CapabilityGraph | what can actually be done now? | SCHEMA_ONLY |
| TaskIR | what exactly is being requested? | PROMOTED |
| AuthorityEnvelope | what may this actor do? | SCHEMA_ONLY |
| RuntimePacket | what is actually running? | SCHEMA_ONLY |
| EvidencePacket | what was observed and how? | SCHEMA_ONLY |
| TemporalPacket | when is this claim valid? | SCHEMA_ONLY |
| DispatchPlan | who/what executes which node? | SCHEMA_ONLY |
| ResultPacket | what actually happened? | SCHEMA_ONLY |
| ArtifactBundle | the human-consumable product | ACTIVE_VIA (pdf-federation door) |
| ContextPacket | what context matters? | SCHEMA_ONLY |
| ReleaseLinkGate | is this release linked to reality? | SCHEMA_ONLY |
| Measurement | what exactly was measured? | SCHEMA_ONLY (added 2026-10-02) |
| BridgeProof | is A equivalent to B? | SCHEMA_ONLY (added 2026-10-02) |
| Worldline | nine-dimension state vector S_t | SCHEMA_ONLY (added 2026-10-02) |

**Gate:** All 15 schemas validate against JSON Schema draft 2020-12.
**Verification command:**
```
for f in /root/AAA/schemas/ir/*.schema.json; do
  python3 -c "import json, jsonschema; jsonschema.Draft2020123Validator.check_schema(json.load(open('$f')))" && echo "OK $f"
done
```
**Status:** `CANDIDATE_ABI` — not FROZEN. Promotion to FROZEN requires:
1. All schemas validate (above)
2. All `$ref` cross-schema dependencies resolve
3. Reconciliation matrix produced against existing canon (instructions/representation-reality-invariant.md, docs/doctrine/truth-kernel.md, lib/reality_graph.py, schemas/a2a-v1.0.schema.json, schemas/peer-federation-contract.schema.json, schemas/task-envelope.schema.json, specs/HHMM/INIT-SPEC-v0.1.md)
4. Validator + fixture suite passes
5. A2A round-trip test passes
6. No semantic duplicate exists (e.g. BridgeProof vs new claim schema — must be projection of RealityAssertion)
7. GitHub diff independently reviewed

**Promote to PROVEN when:** at least one organ produces a packet that another organ consumes, and the BridgeProof four-axis guards (`relation ≠ comparability ≠ verification_state ≠ probe_state`) pass per-snapshot.

---

### Track B — Live probes emit typed packets (P0.5, F13 dialis)

**Goal:** A-FORGE emits a live `CapabilityGraph` for itself and one peer organ.

| Step | Action | Gate |
|------|--------|------|
| B.1 | A-FORGE emits its own `CapabilityGraph` for the 122 already-exposed tools | packet validates against schema; observed_at populated |
| B.2 | A-FORGE probes ONE peer (GEOX recommended — recent interface contradiction) and emits its `CapabilityGraph` | callable set differs from declared set by ≥1 (proves schema carries real signal) |
| B.3 | A-FORGE emits its own `RuntimePacket` (multi-layer identity snapshot) | at least 3 of 6 identity layers measured; bridge_PROof entries required for any MATCH/DRIFT claim |
| B.4 | A-FORGE emits `EvidencePacket` for one consequential claim with `witness_refs` populated | independent witness implementation inspects and signs |

**Gate for Track B → next track:** every emitted packet carries
`(metric, unit, scope, referent, method, baseline, observed_at, does_not_imply)`
— no naked status strings anywhere.

---

### Track C — BridgeProof semantic (PARTIALLY COMPLETE 2026-10-02)

**Goal:** Every equivalence claim is bridged before being emitted; canonical ratifications are honored; mutating tools are excluded from capability proof.

**Sub-track C.1 — BridgeProof four-axis (DONE 2026-10-02):**
- ✅ Replaced single-enum relation with four independent axes: `relation` (ontological), `comparability` (meaningfulness), `verification_state` (witness result), `probe_state` (procedural health).
- ✅ Hard invariants: EQUIVALENT_TO requires COMPARABLE ∧ WITNESSED. ProbeFailure ≠ REFUTED. TYPE_MISMATCH ≠ DIVERGES_FROM. Empty evidence → UNRESOLVED.
- ✅ `Comparable(A,B) = SameType(A,B) ∨ WitnessedBridge(A,B)` — heterogeneous types comparable through witnessed bridge function.

**Sub-track C.2 — Canonical ratification reconciliation (DONE 2026-10-02):**
- ✅ AuthorityEnvelope restored to 12-field tuple: Actor, Session, Host, Objective, Operation, Scope, Target, Issuer, Expiry, ExpectedPostcondition, Budget, RevocationRef (per instructions/authority-envelope.md, ratified 25 Sep). Added `bridge_proof_refs` for identity verification.
- ✅ ReleaseLinkGate hardened: added required `observed_at`, `canonical_url`, `retrieval_method`, `verifier_identity`, `content_source_identity_hash`. JSON Schema if/then enforces `region_match` mandatory for app/paper kinds. Removed unexplained "(Karim et al)" attribution.
- ✅ CapabilityGraph expanded from 4 layers to 7: declared → registered → exported → reachable → contract_valid → safely_probeable → observed_callable. New `mutating_tools[]` set identifies MUTASI/DEPLOY tools EXCLUDED from observed_callable via HARD INVARIANT (capability proof cannot create consequences while measuring truth).

**Sub-track C.3 — Reconciliation outputs (DONE 2026-10-02):**
- ✅ `/root/AAA/schemas/ir/RECONCILIATION.md` — 7-canon survey; 17-row reconciliation matrix; 4 semantic-duplication resolutions detected and rejected; 7 C.3 follow-ups documented.
- ✅ `/root/AAA/schemas/ir/DEPENDENCIES.md` — schema DAG; 8 cross-schema `$ref` instances verified; co-location rule documented.
- ✅ `/root/AAA/schemas/ir/EPISTEMIC_TAXONOMY.md` — canonical 5-class taxonomy from `lib/reality_graph.py`; 11-row "want to write X → use Y" mapping; new-class addition protocol documented.
- ✅ `/root/AAA/schemas/ir/VALIDATOR_PLAN.md` — 7 validators; gold + adversarial fixture catalog; CI integration blueprint.

**Sub-track C.4 — Deferred until C.4 prerequisites (Auth C.3 follow-ups):**
- ❌ Add `contradiction_index` field to Worldline.epsilon (RECONC row 14)
- ❌ Add `n_eff` derived field to EvidencePacket (RECONC row 15)
- ❌ Add `warrant_score` derived field (RECONC row 17)
- ❌ Define RealityAssertion.freshness → TemporalPacket.freshness_class mapping (RECONC row 5)
- ❌ Define TaskIR → TaskEnvelope adapter (RECONC row 10)
- ❌ Add `content_sha256` registry to IR_REGISTRY.v1 (Detection pattern in RECONCILIATION)
- ❌ Update PeerFederationContract → AuthorityEnvelope adapter (RECONC row 9)
- ❌ Define EpistemicMembrane schema (when added) per HHMM E12 13-field list (RECONC row 8)
- ❌ Fixture authoring per VALIDATOR_PLAN.md
- ❌ GitHub diff independent review

**C.3 gate before FROZEN status:
1. All $ref cross-schema dependencies validate
3. Reconciliation matrix produced against existing canon (representation-reality-invariant.md, truth-kernel.md, lib/reality_graph.py, a2a-v1.0.schema.json, peer-federation-contract.schema.json, task-envelope.schema.json, specs/HHMM/INIT-SPEC-v0.1.md)
4. Validator + fixture suite passes
5. A2A round-trip test passes
6. No semantic duplicate exists
7. GitHub diff independently reviewed

---

### Track D — R6 readiness test (`E_{n+1} < E_n`) (P1)

**Goal:** Demonstrate recursive improvement — the institution makes measurably
fewer of the same mistakes twice.

**Operational definition:** For each active prediction in CHRON, compare the
epsilon between `(S_{t+1} - Ŝ_{t+1})` for the prior prediction vs the current
prediction in the same class. If `epsilon_direction = IMPROVING` for ≥1 dimension
across ≥3 consecutive predictions in the same class, R6 is **demonstrated** for
that class.

**Mechanism:**
1. Every organ emits a `Worldline` per the schema at regular intervals.
2. CHRON computes `epsilon` between consecutive worldlines for the same subject.
3. PHOENIX-72 cools any lesson candidate extracted from `epsilon`.
4. Subsequent predictions in the same class retrieve the lesson before
   generating Ŝ_{t+1}.

**Gate for Track D → CHRON_LEARNING_READY:** ≥1 class achieves
`E_{n+1} < E_n` for ≥3 consecutive cycles, with full causal lineage.

---

## Per-organ checklist

Each organ must reach each gate in order. The order matters: substrate before
probes before bridges before learning.

- [ ] A-FORGE — Track A done. Track B.1 in progress.
- [ ] GEOX — interface contradiction pending; Track C end-state applicable.
- [ ] WEALTH — health probe timeout blocks B.2 for this organ; revisit.
- [ ] WELL — REGISTRY_PASS; substrate DEGRADED; both reflected via Measurement.v1.
- [ ] HERMES — surface coherent; semantic Membrane integration pending.
- [ ] CHRON — R1–R3 ready; R4–R6 in progress; Track D primary stakeholder.
- [ ] FRAME — observation frame; ReleaseLinkGate gate as URL emitter.
- [ ] arifFlow — separate organ (Track A confirmation); trajectory component of Worldline.
- [ ] arifOS — kernel substrate; TemporalPacket infrastructure live.
- [ ] VAULT999 — witness layer; persists BridgeProofs and Worldlines immutably.

---

## What does NOT migrate

- Capability ≠ Authority doctrine (already kernel-bound; not a schema concern).
- Constitutional floors F1–F13 (kernel-owned; not part of the IR layer).
- Human-9 substrate contract (H1–H9; pointer-only in SOUL.md, never restated).
- Sovereignty / F13 dialis binary (always human, never automated).

The IR layer **encodes the substrate of how agents observe, claim, and witness**.
It does not encode authority, judgment, or seal. Those remain with arifOS 888,
F13, and VAULT999 respectively.

---

## Open questions

1. Should `ReleaseLinkGate` deprecate naked-URL skill prose in the SKILL.md layer?
   (Pending F13 dialis.)
2. Should the BridgeProof schema include a `time_budget_seconds` constraint to prevent
   agents from spawning infinite bridge-construction loops?
3. Should the Worldline `epsilon` field auto-populate on schema level (e.g. as
   a derived field) or remain strictly CHRON-populated?
4. When an organ emits Measurement with `freshness_class=STALE`, should the
   organ's own Worldline automatically demote its `A.dimension` (authority) tier?

---

## Revision history

| Date | Change | Source |
|------|--------|--------|
| 2026-10-02 | Initial v1 frozen; 12 schemas, 4 invariants | IR_REGISTRY.v1 (concurrent-worker provenance) |
| 2026-10-02 | +3 schemas (Measurement, BridgeProof, Worldline) | session-2026-10-02-1038 (post CHRON probe) |
| 2026-10-02 | +6 laws (invariants 5–10) | session-2026-10-02-1038 |
| 2026-10-02 | MIGRATION.md created | this document |