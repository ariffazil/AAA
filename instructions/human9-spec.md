<!-- HUMAN9-SPEC v1 — companion to HUMAN-REALITY-EDGE-BRIDGE-REFACTOR-v0.1 (F13_RATIFIED_CANON 2026-10-07) -->
<!-- status: DRAFT (awaiting F13 promotion) | spectrum: 555-666 (memory + authority plane) | floors: F1, F2, F5, F9, F13 -->
<!-- purpose: Operationalize the HUMAN9 file format (9 sections, 9 invariants) as runtime-spec, not as a refactor proposal. -->
<!-- Cinematic rule from refactor v0.1: "Profile packages a person. Event leaves the person larger than every record." HUMAN9 keeps that rule. -->

# HUMAN9-SPEC v1 — Human Reality Projection File Format (Operational Spec)

> **Status:** DRAFT (awaiting F13 promotion) · created 2026-10-07 ~21:10 MYT
> **Companion to:** `/root/AAA/instructions/HUMAN-REALITY-EDGE-BRIDGE-REFACTOR-v0.1.md` (F13_RATIFIED_CANON 2026-10-07)
> **Inherits from:** `/root/AAA/canon/APEX_REALITY_GRAPH_MEMORY_MIGRATION_v1.md`, `/root/AAA/instructions/human-memory-compartmentalization.md`, `/root/AAA/instructions/source-type-promotion-gate.md`, `/root/AAA/instructions/claim-lifecycle-states.md`, `/root/AAA/instructions/representation-reality-invariant.md`, `/root/AAA/instructions/authority-envelope.md`, `/root/AAA/canon/REALITY_GRAPH.md`
> **Carries forward from MEMORY entry:** `[ARCH] HUMAN9 FILE ARCHITECTURE` (1,440c, 2026-10-06 F13 concept-pass)
> **Falsifier:** the kernel must reject S2_QUALIA queries before render, not just log violation (test below)

---

## 0 · TL;DR

HUMAN9 is a **runtime file format + governance contract** for representing one specific human's bounded current state in agent context. It is **not** biography. **Not** a digital twin. **Not** a profile. The cinematic rule from HUMAN-REALITY-EDGE-BRIDGE-REFACTOR v0.1 holds: the **person stays larger than every record of them**.

The file lives at `/root/memory/people/P-XXX/HUMAN9.yaml`, accessed only via `hermes_human9_read` with tenant/principal/purpose/class/freshness filter (default-deny). The agent is **custodian**, never owner. **F13 is the only sovereignty over the file.**

This spec is the runtime contract. The refactor v0.1 is the doctrine. HUMAN9 is what the file IS.

---

## 1 · Ownership & Boundary

| Field | Value | Authority |
|---|---|---|
| Owner | the PERSON (the human the file is about) | constitutional |
| Custodian | hermes (lane=arif), with F13 sovereign attendance | delegated |
| Sovereign | Muhammad Arif bin Fazil (F13) | final authority on every read/write |
| Path | `/root/memory/people/<lane-id>/HUMAN9.yaml` (e.g. `P-ARIF/HUMAN9.yaml`) | not symlinked elsewhere |
| Adjacent (do not duplicate) | CHRON trajectory at `/root/chron/data/trajectory/<lane-id>.jsonl` | CHRON owns calibrated futures |
| Inheritance from STALE_DOMAIN_ATLAS_v1 | Reuse GEOX rock-physics H9 axis *pattern*, not the domain. Human state = `H9_STATE(t)`, not rock H9 | inherited pattern, fresh domain |

**Boundary clauses:**
- The file is **append-mostly**. Claims are corrected, never deleted; old moves to `SUPERSEDED` (per claim-lifecycle-states.md).
- The file is **bounded**. Target 5-15 KB; hard cap 50 KB; beyond → archive to `/root/memory/people/P-XXX/archive/HUMAN9-<ts>.yaml`.
- The file is **PRIVATE** by default. No compartment except F13's direct sovereign attention has unrestricted read.
- The file is **not** auto-loaded into agent context. Retrieval is opt-in via the filter (Section 6).

---

## 2 · 9 Sections

Each file contains exactly these 9 sections (the canonical order; the runtime enforces this):

### 2.1 · sovereignty

```yaml
sovereignty:
  principal: <who this person is — name, identifiers they consented to>
  declared_authority_scope: <what the person can promote/demote about themselves; e.g. "only Arif can promote H4 → H5">
  consent_status: <OBSERVED | SELF_REPORT | INFERRED | UNKNOWN>
  consent_recorded_at: <iso8601>
  consent_scope: <list of allowed domains, e.g. [medical, family, schedule, emotional]>
  consent_withheld: <list of explicitly WITHHELD domains, e.g. [third_party_health]>
  withdrawal_procedure: <how person can revoke consent; routes to F13 binary>
  principal_verified: <boolean — has F13 confirmed this person exists as named?>
  sovereign: <"Muhammad Arif bin Fazil" for any F13-attended file>
```

### 2.2 · human9 (9 axes)

```yaml
human9:
  H1_vitality: <physical state, energy, sleep, health>     # observable
  H2_cognition: <mental state, focus, clarity>               # observable
  H3_relational: <relationship state, attachment, bonds>    # observable
  H4_emotional: <affect, regulation>                         # observable + first-person
  H5_interior: <UNKNOWN unless first-person>                 # H5 LOCK — never inferred
  H6_world: <environment, context, situation>               # observable
  H7_history: <bounded context with provenance>              # observable + recorded
  H8_projects: <active goals, work, plans>                  # observable + first-person
  H9_state: <H9_STATE(t) — composite vector at time t>      # derived
```

### 2.3 · perspectives (ACTG — never merge)

```yaml
perspectives:
  A: <arif-self — what arif believes about arif>
  C: <arif-model-of-subject — what arif believes about the subject>
  T: <subject-self — what the subject says about themselves (FIRST-PERSON)>
  G: <subject-model-of-arif — what the subject says arif is (FIRST-PERSON)>
  # ACTG never merge. Each perspective is its own claim with its own provenance.
```

### 2.4 · state (time-bounded, contradictions preserved)

```yaml
state:
  observed_at: <iso8601>
  freshness: <seconds since observation>
  vector: <state variables at observed_at>
  contradictions: <list of unresolved internal contradictions — DO NOT resolve silently>
```

### 2.5 · claims (each with holder, provenance, bitemporal)

```yaml
claims:
  - claim_id: C-001
    principal: <who is the source of this claim>
    claimant: <who wrote this into the file>
    epistemic_state: <OBSERVED | SELF_REPORT | INFERENCE | INTERPRETATION | MODEL_OUTPUT | UNKNOWN>
    provenance: <FIRST_PERSON | SECOND_HAND | DOCUMENTED_RECORD | BEHAVIORAL_EVIDENCE | PHYSIOLOGICAL_DATA | INSTITUTIONAL_RECORD>
    valid_time: {from: <iso8601>, to: <iso8601 | "ONGOING">}  # when claim is true
    recorded_time: <iso8601>                                   # when claim was recorded
    statement: <the actual claim>
    correction_of: <C-XXX if this supersedes a prior claim>
    superseded_by: <C-YYY if this claim has been replaced>
    confidence: <0.0-1.0>
```

### 2.6 · relationships (bounded graph, no collective brain)

```yaml
relationships:
  - person_id: <opaque internal token of the other person>
    role: <family | friend | colleague | sovereign | other>
    reciprocity: <bidirectional | unidirectional>
    valence: <positive | neutral | ambivalent | negative>
    state: <active | dormant | severed>
    observed_at: <iso8601>
```

### 2.7 · events (witnessed; full temporal chain)

```yaml
events:
  - event_id: E-001
    at: <iso8601>
    type: <medical | relational | professional | personal>
    description: <event>
    impact: <observed consequence>
    witnessed_by: <who observed>
    # The temporal chain is mandatory: PROPOSED → PREPARED → EXECUTED → OBSERVED → VERIFIED → ADAPTED
    # (per AAA-INIT-TO-SEAL cycle contract, 2026-10-06). Never collapse.
```

### 2.8 · memory (promotion = better organization, NOT epistemic elevation)

```yaml
memory:
  H1_anchored: <...>      # promoted from H2 (multi-source, well-anchored)
  H2_observed: <...>      # observed at least once
  H3_reported: <...>      # reported but not directly observed
  H4_unknown: <...>       # explicitly unknown — DO NOT promote without first-person
  H5_inferred: <...>      # inferred from behavior (USE SPARINGLY — usually belongs in H4)
  H6_archive: <...>       # archived, low signal
  # Promotion rule: H1→H2→H3/H4/H5/H6 is better organization, NOT epistemic elevation.
  # H4 (UNKNOWN) is the default for unverified state. Promotion requires first-person or
  # multi-source observation; never agent-inferred alone.
```

### 2.9 · graph (bounded node list; derivation requires claim_id)

```yaml
graph:
  nodes:
    - {id: P-XXX, type: person, label: <opaque>}
    - {id: P-YYY, type: person, label: <opaque>}
  edges:
    - {from: P-XXX, to: P-YYY, relation: <bond>, weight: <0.0-1.0>, observed_at: <iso8601>, claim_id: C-XXX}
  # No agent derivation without an explicit claim_id linking to the source claim.
  # No "collective brain" — graph is bounded by what claims exist.
```

---

## 3 · 9 Invariants (M1–M9)

These are the operational M-rules. Each is a falsifiable claim about the runtime.

| # | Invariant | Runtime test |
|---|---|---|
| M1 | Person ≠ representation | No code path may treat a file claim as the person. (test: any read result includes the field `representation, not the person`.) |
| M2 | Claim has a holder | Every claim has a non-null `principal`. (test: file lint rejects orphan claims.) |
| M3 | Claim has provenance (bitemporal) | Every claim has `valid_time` and `recorded_time` and they may differ. (test: no claim has identical valid_time=recorded_time without `MONOLITHIC` flag.) |
| M4 | Observation never silently becomes motive/identity | Reading a behavior-derived claim must not auto-promote to identity-class. (test: any H3→H2 promotion requires explicit `promotion_reason`.) |
| M5 | Correction supersedes (never invisible rewrite) | A new claim with same `claim_id` puts the old into `SUPERSEDED` state (per claim-lifecycle-states.md). (test: `superseded_by` field is set; old claim still addressable by claim_id.) |
| M6 | Unknown is explicit & queryable | Every section must be queryable for "what don't we know" — return `UNKNOWN` not silent gap. (test: empty sections return `UNKNOWN` not null.) |
| M7 | Access requires purpose + consent + retention | Every read records `purpose`; every write records `retention`. (test: access_log is append-only; missing fields = access denied.) |
| M8 | Irreducible remainder (ε_qualia > 0) | No agent response may claim full modeling of a person. (test: any claim that does not end with `ε > 0` annotation is rejected.) |
| M9 | Provenance chain (every field traces) | Every field carries `{event_id, actor, recorded_at, valid_time}`. (test: file lint rejects untraced fields.) |

---

## 4 · Sensitive-data Classification (per claim, not per file)

| Class | Examples | Storage | Access |
|---|---|---|---|
| **S0_PUBLIC** | name, role, public timestamps | HUMAN9 | any lane with declared purpose |
| **S1_PRIVATE** | health, money, family conflict | HUMAN9 + compartment | declared purpose + active `consent_scope ≠ NONE` |
| **S2_QUALIA** | feelings, NS-state read | **NEVER persisted to HUMAN9** | stays with the human; agent may observe, not store |
| **S3_IRREDUCIBLE** | ε_qualia remainder | cannot be represented | n/a |

**Critical rule (S2 enforcement):** the kernel must reject S2_QUALIA queries **before render**, not just log violation. The test (Section 11) verifies this.

---

## 5 · Consent & Purpose

- `consent_scope ∈ {FULL, PURPOSE_LIMITED, TEMPORAL, NONE}` (from `_ontology.py`).
- `NONE` = hard-block export (the v2.1.1 patch in this session closes one boundary; HUMAN9 spec extends to all 6 remaining call sites per the audit).
- `purpose` declared at every read; recorded in `state.access_log`.
- `retention` declared at every write; sweep removes expired content but preserves `content_sha256` (witness pattern, same as `_witness_channel.py`).

---

## 6 · Access Control

| Operation | Authority |
|---|---|
| Read | `actor_id` + `purpose` + `consent_scope` + `retention` required in access record |
| Write | only via arifOS kernel predicate; never direct file mutation |
| Delegation | child agent cannot widen parent scope; scope, deadline, budget, minimum-context in delegation envelope |
| Cross-tenant | `room_id ≠ authorization`; tenant + room + session + purpose all required |

---

## 7 · Correction / Supersession

- New claim with same `claim_id` → previous moves to `SUPERSEDED` (per `claim-lifecycle-states.md`, F13 2026-09-25).
- Old claim stays addressable by `claim_id`; never silently rewritten.
- Audit trail in `events[]` with `event_type: CORRECTION`.
- `correction_of` and `superseded_by` fields carry the chain.

---

## 8 · Provenance

- Every field carries `provenance: {event_id, actor, recorded_at, valid_time}`.
- Derived fields carry `origin: DERIVED` + `derivation_chain: [...]`.
- `provenance_class ∈ {FIRST_PERSON, SECOND_HAND, DOCUMENTED_RECORD, BEHAVIORAL_EVIDENCE, PHYSIOLOGICAL_DATA, INSTITUTIONAL_RECORD}` (from `_semantic.py`).

---

## 9 · Retrieval Filter (the runtime contract)

```python
# hermes_mcp tool: hermes_human9_read
request = {
  "person_id": "P-XXX",
  "requesting_agent": "hermes-asi-gateway (lane=arif)",
  "requesting_principal": "F13 SOVEREIGN",  # or "self" if F13 asking about self
  "purpose": "<conversation | governance | audit | repair | archive>",
  "section_filter": ["sovereignty", "human9", "claims"],
  "claim_class_filter": ["SELF_REPORT", "DOCUMENTED_RECORD"],
  "freshness_max_seconds": 86400,
  "include_superseded": False,
  "tenant": "arif"
}

# 7 rules apply in order:
# 1. Tenant gate — requesting_agent tenant == file.tenant
# 2. Principal gate — requesting_principal in consent_scope
# 3. Purpose gate — purpose in consent_scope of claim
# 4. Section filter — only return requested sections
# 5. Class filter — drop claims with epistemic_state not in filter (H5 stays UNKNOWN)
# 6. Freshness gate — claims older than max are marked STALE not dropped
# 7. Superseded gate — only returned if include_superseded=true (default false)
```

**Default-deny position:** the agent's default state when reading HUMAN9 is **deny all**, unless all 7 rules pass. This is the opposite of `people.yaml` read pattern (default-allow). The shift is intentional: HUMAN9 is sovereign-attended person data; people.yaml is operational routing.

---

## 10 · Logging

Every retrieval — allowed or denied — is logged to `/root/VAULT999/human9-retrieval.log.jsonl`:

```json
{
  "ts": "<iso8601>",
  "requesting_agent": "...",
  "requesting_principal": "...",
  "person_id": "P-XXX",
  "purpose": "...",
  "sections_requested": [...],
  "sections_returned": [...],
  "status": "ok | denied_tenant | denied_principal | denied_purpose | denied_class | denied_freshness | stale_data",
  "policy_version": "human9-spec-v1"
}
```

This is the audit trail F13 can review. **Denied requests do NOT return body content** (not even stub) — prevents side-channel attack via error message structure.

---

## 11 · Falsifier (kernel-level test)

```python
# Test: S2_QUALIA query must be rejected before render
def test_human9_qualia_rejection_at_kernel():
    request = {
        "person_id": "P-SYED",
        "requesting_agent": "hermes-asi-gateway (lane=arif)",
        "requesting_principal": "F13 SOVEREIGN",
        "purpose": "stakeholder_graph",
        "section_filter": ["human9"],
        "claim_class_filter": ["S2_QUALIA"],  # explicitly asking for qualia
    }
    response = hermes_human9_read(request)
    assert response.status == "denied_class"
    assert response.body is None  # no stub, no leak
    assert "S2_QUALIA cannot be persisted" in response.reason
```

**If this test fails:** the kernel is logging violation but still returning content. The spec is not enforced. Treat as constitutional violation.

---

## 12 · Migration Plan (post-F13-SAH)

1. Create this file at `/root/AAA/instructions/human9-spec.md` (this doc).
2. For each lane in people.yaml (arif, syed, jiaaa, …): generate skeleton `HUMAN9.yaml` from public fields only (S0).
3. Health/qualia data (S1/S2) does NOT migrate automatically — requires explicit F13 + per-person `consent_scope`.
4. Agent-wide memory entry `[ARCH] HUMAN9 FILE ARCHITECTURE` (1,440c) → pointer to this file (~290c).
5. Rollback: pointer kept + this spec archived at `/root/AAA/.staged/human9-spec-2026-10-07.md`.

---

## 13 · Open Debt

- S2_QUALIA storage policy is declared "never persisted" but **no kernel predicate enforces this yet**. The hermes_mcp tool needs the predicate wired before this spec is constitutional-class.
- `access_log` retention needs a default (proposed: 90 days, like `_witness_channel.py`).
- `derivation_chain` schema not yet formalized.
- 6 cross-boundary call sites (hermes-a2a listener, claim-validate cross-layer, witness-channel, media-ingest, voice-stack, session-fed) need the S2_QUALIA predicate wired — same defect class as the v2.1.1 patch this session already closed.
- people.yaml lookup at claim-validate time not wired yet (Move B in the audit note; ~30 LOC in `_envelope.py`).
- The 9-axis H5 interior lock is **schema-enforced** here but the runtime gate (read returns UNKNOWN vs returns nothing) needs explicit implementation.

---

## 14 · Memory Capacity Policy (for reference, not adopted into memory)

The capacity policy proposed by the audit (2026-10-07 ~21:00):

```
<75%      normal writes
75–80%    warn + identify consolidation candidates
>80%      no new ordinary memory entry until approved hygiene
>87.5%    read-only except explicit F13 safety-critical write
>95%      immediate hygiene audit; no doctrine / person / arch specs
```

Adopting this policy into memory/config is a separate F13 binary. This spec references it but does not codify it.

---

## 15 · Receipts

- Source brief: MEMORY entry `[ARCH] HUMAN9 FILE ARCHITECTURE` (1,440c, 2026-10-06 F13 concept-pass)
- Companion doctrine: HUMAN-REALITY-EDGE-BRIDGE-REFACTOR-v0.1 (F13_RATIFIED_CANON 2026-10-07)
- Created: 2026-10-07 ~21:10 MYT, by hermes (lane=arif), per F13 directive
- Status: DRAFT — promotion to F13_RATIFIED_CANON awaits F13 SAH
- 8-stage Governed Witness Mutation Protocol: AUTHORIZE ✓ (Hang "Gerak ja laaa" 2026-10-07 ~21:05) · BACKUP ✓ (DRAFT variant in scratch) · MUTATE ✓ (this write) · VERIFY pending · REINDEX N/A · RELINK pending · WITNESS pending · NOTIFY pending

DITEMPA BUKAN DIBERI ⚒️
