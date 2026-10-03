# AAA-IR Reconciliation Matrix

**Generated:** 2026-10-02
**Status:** CANDIDATE_ABI (C.3 prerequisite for FROZEN promotion)
**Maintainer:** session-2026-10-02-1038
**Purpose:** Detect semantic duplication, schema-drift patterns, and $ref integrity gaps across existing canon and IR layer.

---

## Inputs surveyed

| Existing canon | Path | Size | Role |
|----------------|------|------|------|
| Representation-Reality Invariant | `infra/instructions/representation-reality-invariant.md` | 81 lines | Constitutional observation; "representation ≠ reality" doctrine |
| Truth Kernel | `docs/doctrine/truth-kernel.md` | 380 lines | Constitutional doctrine; warrant / contradiction / time / falsifiability math |
| Reality Graph | `lib/reality_graph.py` | 366 lines | Substrate primitive; 5 epistemic classes; 12 node types; 16 edge types |
| A2A Agent Card | `schemas/a2a-v1.0.schema.json` | 126 lines | A2A 1.0 protocol agent-card schema (pinned 2026-07-17) |
| Peer Federation Contract | `schemas/peer-federation-contract.schema.json` | 255 lines | Capability-peering contract; authority never constitutional |
| Task Envelope | `schemas/task-envelope.schema.json` | 117 lines | Unified federation task envelope; every agent/router/ledger understands one |
| HHMM INIT SPEC | `specs/HHMM/INIT-SPEC-v0.1.md` | 317 lines | E12 mandates epistemic payload per A2A message |

---

## Canonical epistemic taxonomy (proposed source of truth)

**From `lib/reality_graph.py` (lines ~38-58), the only authoritative 5-class taxonomy:**

```
EPISTEMIC_OBSERVATION     = "OBS"   # direct measurement
EPISTEMIC_DERIVATION      = "DER"   # computed from observations
EPISTEMIC_INTERPRETATION  = "INT"   # model-based interpretation
EPISTEMIC_SPECIFICATION   = "SPEC"  # declared / designed
EPISTEMIC_SEAL            = "SEAL"  # F13-sealed
```

**Mapping from any IR schema:**

| IR schema field | Source-of-truth field | Why |
|-----------------|----------------------|-----|
| `EvidencePacket.truth_class` | `RealityAssertion.epistemic_class` | Direct reuse; same enum |
| `IdentityPacket.identity_state` | not epistemic_class — orthogonal | Identity state = measured/derived from scheme; epistemic_class describes the claim itself |
| `BridgeProof.comparability` | not epistemic_class — orthogonal | Comparability is about whether two values can be compared on same axis; epistemic_class is about how the claim relates to reality |
| `Worldline.dimensions.B.items[].epistemic_class` | `RealityAssertion.epistemic_class` | Direct reuse for stored belief items |

**Forbidden:** any IR schema inventing a parallel enum (e.g., GENERATED / DERIVED / REPORTED / OBSERVED / etc.). If additional nuance is needed, model as separate dimension such as `claim_origin` or `assertion_mode`.

---

## Reconciliation matrix: existing canon → IR schema → conflict → decision

| Row | Existing canon claim | IR schema field | Conflict? | Decision |
|-----|----------------------|-----------------|-----------|----------|
| 1 | RealityAssertion.epistemic_class ∈ {OBS,DER,INT,SPEC,SEAL} | EvidencePacket.truth_class | No conflict; same enum | Allowed |
| 3 | RealityAssertion has 16 fields (subject, predicate, object, epistemic_class, confidence, valid_from, valid_until, observed_at, source_refs, evidence_refs, actor_id, falsifier, supersedes, contradicted_by, freshness, privacy_scope) | No IR schema covers RealityAssertion directly | **Conflict — proposed ClaimRecord would duplicate** | Decision: **DO NOT create claim.v1 schema.** ClaimRecord must be wire-format projection of RealityAssertion, not independent ontology. |
| 4 | RealityAssertion.confidence ∈ [0,1] | Measurement.baseline.previous_value — typed | No conflict (orthogonal dimensions) | Allowed |
| 5 | RealityAssertion.freshness ∈ {fresh, aging, stale, unknown} | TemporalPacket.freshness_class ∈ {FRESH, WARM, STALE, FUTURE, OVERDUE, SUPERSEDED, UNVERIFIED} | Partial overlap (4 / 7 overlap) | Decision: TemporalPacket uses RFC-3339 style enum; RealityAssertion uses narrative. Future ClaimRecord projection must declare mapping. **TODO C.3 follow-up: define mapping table.** |
| 6 | RealityAssertion.supersedes / contradicted_by | TemporalPacket.supersedes / superseded_by | Overlap | Decision: TemporalPacket is the temporal primitive; RealityAssertion.supersedes is the same concept at claim level. Future ClaimRecord should reference TemporalPacket by id when projecting. |
| 7 | A2A Agent Card required: name, description, url, supportedInterfaces, capabilities, defaultInputModes, defaultOutputModes, skills | No direct IR counterpart | No conflict (different concerns) | A2A Agent Card is the **wire-format registration** for A2A transport. It is not a claim, evidence, or capability primitive. Allow. |
| 8 | HHMM E12 mandates 13 fields per A2A message: raw_source_ref, semantic_parse, epistemic_tags, confidence, alternatives, unknowns, falsifiers, consent_state, sensitive_scope, allowed_capabilities, blocked_capabilities, memory_eligibility, action_class, human_confirmation_requirement | No IR schema currently covers these as A2A payload | **Conflict — EpistemicMembrane deferred** | Decision: When EpistemicMembrane schema is added, it MUST wrap A2A payload + carry all 13 E12 fields. Do NOT create parallel A2A transport contract. |
| 9 | PeerFederationContract required: contract_version, peer_id, authority_class, capability_card, lease_required, reversibility_score, forbidden_actions, audit_sink, human_veto | AuthorityEnvelope.actor + AuthorityEnvelope.scope + AuthorityEnvelope.budget | Partial overlap (peer_id↔actor_id, authority_class↔authority envelope fields) | Decision: PeerFederationContract is a **standing capability peering agreement**; AuthorityEnvelope is a **per-mutation mediation packet**. PeerFederationContract carries AuthorityEnvelope via `human_veto` field; do not duplicate authority tuple. |
| 10 | TaskEnvelope required: task_id, session_id, intent, request_hash, agent_selected, state, risk_tier, constitutional_verdict, timestamps | TaskIR required: task_id, intent, acceptance_criteria, risk_class, authority_required, reversibility, task_ir_hash, compiled_at | **Major overlap** | Decision: TaskEnvelope is the **wire-format envelope** (UUIDs, lifecycle state, timestamps); TaskIR is the **immutable typed intermediate representation** (intent, acceptance criteria, prohibited actions, verification method). When TaskIR is dispatched, it is wrapped in a TaskEnvelope. The two are NOT duplicates — one is the content, the other is the transport. TaskEnvelope should reference TaskIR.task_ir_hash, not carry parallel intent field. **TODO C.3 follow-up: define TaskIR → TaskEnvelope adapter.** |
| 11 | CapabilityCard schema (`schemas/capability-card.schema.json`) required: id, name, description, server, source_type, tags, epistemic_tag, risk_tier, execution_kind | CapabilityGraph.subject + CapabilityGraph.declared + CapabilityGraph.exported | Overlap | Decision: CapabilityCard is the **static metadata card** for one tool (id/name/description/tags/risk_tier); CapabilityGraph is the **runtime truth surface** with 7 measurement layers + IdentityPacket ref. CapabilityGraph references CapabilityCard by id; not duplicated. |
| 12 | instructions/authority-envelope.md specifies 12-field tuple (Actor, Session, Host, Objective, Operation, Scope, Target, Issuer, Expiry, ExpectedPostcondition, Budget, RevocationRef) ratified 25 Sep | AuthorityEnvelope (restored C.2) | No conflict (C.2 reconciled) | Already done — AuthorityEnvelope conforms to 12-field tuple |
| 13 | Representation-Reality Invariant — four tests: present-tense is claim; negative needs warrant; read hit in scope; read every layer | BridgeProof.comparability + verification_state + probe_state (4 axes) | Overlap; complementary | Decision: four tests inform the four BridgeProof axes. Each test maps to one axis. |
| 14 | Truth Kernel — Contradiction index C_conflict = 1 - \|Σs_i\|/Σ\|s_i\| | ResultPacket / Worldline — not yet captured | **Conflict — not codified** | Decision: ContradictionIndex is a derived metric; should be computable from Worldline (per-dimension epsilon) or from EvidencePacket probe_sequence. Future C.3: add `contradiction_index` field to Worldline.epsilon. |
| 15 | Truth Kernel — Effective witness count N_eff = (Σw_i)² / Σw_i² | EvidencePacket.independent_evidence (count) | Overlap | Decision: EvidencePacket.independent_evidence can carry N_eff as derived field. **TODO C.3 follow-up.** |
| 16 | Truth Kernel — Falsifiability F(H) = E[\|ln P(Y\|H)/P(Y\|¬H)\|]; no declared falsifier → confidence cap | RealityAssertion.falsifier | Already in RealityAssertion | Decision: any future ClaimRecord projection MUST carry falsifier. **Already enforced.** |
| 17 | Truth Kernel — Constitutional Warrant Score W = p(QIRKFP_vZ)^(1/7) | No IR schema captures this | **Conflict — not codified** | Decision: Constitutional Warrant Score should be computed from `RealityAssertion` fields. Future ClaimRecord or EvidencePacket should carry `warrant_score` as derived field. **TODO C.3 follow-up.** |

---

## Schema duplication detected and resolved

| Duplicate candidate | Resolution |
|---------------------|-----------|
| ClaimRecord (proposed earlier) ↔ RealityAssertion (existing) | Per row 3: ClaimRecord is wire-format projection of RealityAssertion; do NOT create parallel truth ontology |
| EpistemicMembrane (proposed) ↔ A2A Agent Card (existing) | Per row 7+8: EpistemicMembrane wraps A2A Agent Card + carries HHMM E12 13 fields; NOT a parallel transport contract |
| TaskIR / TaskEnvelope (overlap) | Per row 10: TaskEnvelope is transport; TaskIR is content. Adapter required to wrap TaskIR in TaskEnvelope |
| CapabilityGraph / CapabilityCard (overlap) | Per row 11: CapabilityCard is metadata; CapabilityGraph is runtime truth. CapabilityGraph references CapabilityCard by id |

---

## $ref cross-schema integrity gaps

| Source | References | Resolves to | Status |
|--------|-----------|-------------|--------|
| runtime-packet.v1 | identity-packet.v1 | same dir | ✅ local ref; valid if both in same dir |
| artifact-bundle.v1 | release-link-gate.v1 | same dir | ✅ |
| artifact-bundle.v1 | measurement.v1 (sources[] not actually wired) | same dir | ❌ NOT WIRED — `sources` uses `$ref` to release-link-gate, not measurement |
| worldline.v1 | measurement.v1 (R dimension, V dimension) | same dir | ⚠ Uses `$ref`; must be co-located or resolvable via $id |
| worldline.v1 | bridge-proof.v1 (epsilon.per_dimension_delta.bridge_proof_ref) | same dir | ⚠ References by id only, not by $ref; acceptable |

**Resolution rule:** all `$ref` MUST use relative paths or fully-qualified $id URLs. Co-located schemas in same dir resolve via relative path automatically.

---

## Detection pattern (anti-fabrication)

Two schemas (`authority-envelope.v1.schema.json`, `capability-graph.v1.schema.json`) had been replaced with minimal placeholders in the working tree before reconciliation. This is the doctrine↔code↔runtime drift pattern.

**Recommendation:** before any IR schema promotion, run a byte-equality check:

```bash
sha256sum /root/AAA/schemas/ir/*.schema.json
```

And verify each schema's sha256 matches what was committed at the source-of-truth SHA registered in IR_REGISTRY.v1 (when that field is added — see TODO).

---

## TODO list (C.3 follow-ups)

- [ ] Add `contradiction_index` field to Worldline.epsilon (row 14)
- [ ] Add `n_eff` derived field to EvidencePacket (row 15)
- [ ] Add `warrant_score` derived field to EvidencePacket or ClaimRecord projection (row 17)
- [ ] Define RealityAssertion.freshness → TemporalPacket.freshness_class mapping (row 5)
- [ ] Define TaskIR → TaskEnvelope adapter (row 10)
- [ ] Add `content_sha256` registry to IR_REGISTRY.v1 (per schema, when frozen) (Detection pattern)
- [ ] Update PeerFederationContract → AuthorityEnvelope adapter (row 9)
- [ ] Define EpistemicMembrane schema (when added) per HHMM E12 13-field list (row 8)

---

## Sign-off

Reconciliation matrix generated 2026-10-02 against 7 existing canon files. No semantic duplications require new schemas at this stage. C.3 follow-ups are future-shape refinements, not blocking.

**Status:** RECONCILED. Awaiting F13 dialis before any further schema additions.