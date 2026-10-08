# KCP-002 — Memory Lifecycle and Forgetting Policy (RATIFIED)

> **Status:** F13_RATIFIED_CANON · Tier A · 2026-10-07 (TURN 123)
> **Promoted by:** F13 SOVEREIGN (Muhammad Arif bin Fazil) via TURN 123 ("123" → execute 1+2+3)
> **Promoted from:** `/root/AAA/instructions/memory-lifecycle-forgetting-policy-DRAFT.md` (2026-09-24)
> **Ratifikator:** Codex CLI (FI-005), session `01a1120c-e752-7422-9acc-ec0717ee5df8`
> **Ratification trace:** `/root/AAA/reports/memory-lifecycle-promotion-receipt-2026-10-07.md`
> **Predecessor binding doctrine:** `evidence-discipline.md` (F13 2026-08-10) — **NOT overridden**
> **Authority:** F13 SOVEREIGN · `actor_verified=true` · `band=SOVEREIGN`
> **Mutability:** Reversible (F13 may amend)

---

## 0 · Resolution of DRAFT §10 self-conflict (binding)

The DRAFT's self-audit (§10) honestly flagged: the 7-class taxonomy
(OBSERVED, MEASURED, DERIVED, INTERPRETED, POLICY, HYPOTHESIS, UNKNOWN)
**conflicts** with `evidence-discipline.md` (F13 2026-08-10, line 84):
> "do not invent EVIDENCE/INTERPRET/UNKNOWN"

**Resolution adopted (KCP-002 §11 path b):**

1. **The 4-class binding subset is the canonical evidence vocabulary for ALL 333-AGI → 888-APEX packets:**
   `OBS · DER · INT · SPEC` (full names: OBSERVED, DERIVED, INTERPRETED, SPECULATED).
2. **The 7-class KCP-002 taxonomy is EXTENDED, not contradictory.** The four new classes (MEASURED, POLICY, HYPOTHESIS, UNKNOWN) are admitted as **a second tier** specifically for *memory lifecycle* decisions (when to retain, archive, tombstone) — NOT for *truth labels* in evidence packets.
3. **No evidence packet or 888-APEX SEAL may use the extended classes.** They are KCP-002-only and bind to *forgetting decisions*, not *truth claims*.

This makes the 4-class and 7-class **non-overlapping** in their binding scope. Evidence-discipline remains unchanged.

---

## 1 · Principle

```
Evidence is preserved.
Claims are contestable.
Memory is fallible.
Canon is scarce.
Authority remains human.
```

The wise system is not "remember everything" or "forget everything". It is **selective institutional memory** — high retention on authority/evidence/reusability, deprioritized retrieval on staleness, restricted access on sensitivity, and F13-gated irreversibility.

## 2 · The Five Questions (Policy Contract)

The policy answers only five questions. Anything that cannot answer one of these is out of scope.

```text
1. What may enter memory?
2. In what form: evidence, claim, decision, entity, procedure, or archive?
3. Who may create, revise, supersede, or delete it?
4. When does it leave default retrieval?
5. What requires F13 authorization before irreversible removal or canon promotion?
```

## 3 · Intake (UNCHANGED from DRAFT)

```yaml
intake:
  default_status: untrusted_input
  preserve_raw_source: true   # immutable, access-controlled
  agent_may_write: workspace_only
  required_metadata:
    - provenance_reference
    - timestamp
    - source_identity
    - classification_basis
```

Raw sources (original files, probe responses, logs) are **preserved separately** from agent interpretation. The agent's claim and the supporting evidence are stored as distinct objects so that one may be superseded without erasing the other.

## 4 · Consolidation — typed record required (CLASS-EXTENDED, KCP-002 SCOPE ONLY)

```yaml
consolidation:
  requires:
    - typed_record (with declared schema)
    - provenance_reference (who/where/when)
    - evidence_class:           # KCP-002 EXTENDED taxonomy
        class: OBSERVED | MEASURED | DERIVED | INTERPRETED | POLICY | HYPOTHESIS | UNKNOWN
        confidence: CONFIRMED | DERIVED | SPECULATIVE | OPINION
        binding_scope: memory_lifecycle_only   # NOT for evidence packets to 888-APEX
    - scope_and_timestamp

  agent_may_promote_to:
    - candidate_knowledge          # reviewable, not authoritative
    - workspace_artifact           # draft, advisory, in-flight

  agent_may_not_promote_to:
    - canon
    - F13_decision
    - constitutional_rule
    - external_authority_claim
```

**BINDING-NOTE:** For 888-APEX evidence packets, the 4-class subset
(OBSERVED · DERIVED · INTERPRETED · SPECULATED) per `evidence-discipline.md` (F13 2026-08-10) is mandatory. The extended classes (MEASURED · POLICY · HYPOTHESIS · UNKNOWN) are reserved for *forgetting decisions* in this policy.

A good prose passage is not canon. A confident answer is not authority. Retrieval is not validation. Promotion to canon requires F13.

## 5 · Retrieval Priority Order (UNCHANGED)

```yaml
retrieval:
  priority_order:
    - 1: verified_current_decision
    - 2: live_observation
    - 3: evidence_linked_claim
    - 4: reviewed_procedure
    - 5: draft_context
    - 6: archive              # preserved but deprioritized

  stale_runtime_data:
    action: re_probe_before_consequential_use
    reason: state changes; cached observation is observation-of-the-past, not now

  default_visibility:
    high_priority: hot_memory + warm_memory
    default: cold_memory + reviewed archive
    deprioritized: unverified drafts, agent self-narrative
```

When uncertain, the system retrieves from higher-priority layers first and falls back only on miss or contradiction.

## 6 · Forgetting Hierarchy (6 Levels) — KCP-002 CORE

```yaml
forgetting:
  levels:
    - HOT_MEMORY:    current task, live state, active constraints
                     lifecycle: session-scoped, expire at session close
    - WARM_MEMORY:   recent validated decisions, reusable procedures
                     lifecycle: 7-30 days active, then demote
    - COLD_MEMORY:   historical evidence, old incidents, past research
                     lifecycle: long-term, accessible on demand
    - ARCHIVE:       preserved but excluded from default retrieval
                     lifecycle: indefinite, retained for audit + lineage
    - TOMBSTONE:     record that something existed + why removed/superseded
                     lifecycle: permanent marker; successor_reference required
    - PURGE:         authorized irreversible deletion
                     lifecycle: exceptional; F13_verified_authorization required

  default_action: archive_then_deprioritize
  hard_delete:
    requires: F13_verified_authorization
    receipt: required (who/when/what/why)
  supersession:
    requires:
      - successor_reference
      - reason
      - timestamp
      - retained_provenance
    tombstones:
      always_retained: true
```

**Rule:** Forget from default retrieval before deleting from evidence storage. Archive is the default forgetting action; delete is exceptional.

**Binding on arifOS memory promotion:** the 6-level forgetting hierarchy applies to `arifosmcp.runtime.memory_store` rows from the moment of write. Tier=ephemeral maps to HOT_MEMORY; tier=session to WARM; tier=canon to COLD. Tier=sacred is **out of KCP-002 scope** (sacred is governed by F1 immunity and the VAULT999 seal discipline, not forgetting).

## 7 · Retention Defaults by Material Type (UNCHANGED)

| Material | Default fate | Reason |
|---|---|---|
| Raw source evidence (files, probes, logs) | Preserve/immutable, access-controlled | Future agents may need raw form for verification |
| Verified decision | Cold Memory, high priority | Decision is reusable; preservation mandatory |
| Validated procedure / skill | Cold Memory | Reusable; may be promoted to skill canon via Phoenix-72 |
| Cached observation (state at t) | Re-probe before use | State changes; cached value is observation-of-the-past |
| Agent self-narrative (interpretations) | Archive after 7d, deprioritize on retrieval | High inflation; low reusability unless 4-gate promoted |
| Draft / unverified claim | Archive immediately on demotion | Default = witness only, not memory |
| Constitutional / F-floor definition | **OUT OF KCP-002 SCOPE** (F1 immunity) | Sacred tier; F13 sovereignty |

## 8 · Authority Boundary (UNCHANGED)

```yaml
authority:
  F13_required_for:
    - canon_promotion
    - constitutional_change
    - irreversible_deletion        # PURGE
    - external_publication
    - production_mutation
    - persona / agent identity claim ratification

  agent_may:
    - write to workspace
    - supersede with successor_reference
    - archive with tombstone
    - deprioritize via retrieval config
    - re-probe to refresh staleness

  agent_may_NOT:
    - mint canon
    - mint F13_decision
    - perform irreversible deletion without F13 ack
    - claim F13 identity
```

## 9 · Retention Equation (UNCHANGED)

$$
R = f(\text{authority}, \text{evidence}, \text{reusability}, \text{recency}, \text{sensitivity}, \text{cost})
$$

Where:
- high **authority** → high retention
- strong **evidence** → high retention
- recurring operational **reuse** → high retention
- **staleness** → low default retrieval priority (but does not destroy)
- high **sensitivity** → low access (NOT necessarily low preservation)
- storage/retrieval **cost** → encourages compression or archival

The final retention decision remains policy + human authority, not a number.

## 10 · Overlap with Existing Ratified Doctrine (RESOLVED)

| Existing artifact | Status | Relation to KCP-002 (RESOLVED) |
|---|---|---|
| `evidence-discipline.md` (F13 2026-08-10) | BINDING | KCP-002 7-class taxonomy is **memory-lifecycle-scoped**; the 4-class subset (OBS/DER/INT/SPEC) remains binding for evidence packets. The 3 new classes (POLICY/HYPOTHESIS/UNKNOWN) are non-overlapping — they describe *forgetting decisions*, not truth labels. MEASURED is admitted as a refinement of OBSERVED for memory purposes. No silent override. |
| `memory-promotion-gate.md` (F13 2026-09-11) | BINDING | KCP-002 §6 forgetting hierarchy implements the gate's "if not memory, witness only" outcome: default = archive, not memory. |
| `PHOENIX-72-COOLING-DOCTRINE-2026-09-26` | BINDING | 72h clock + 4 promotion gates interact with KCP-002 §6: a candidate that fails 4-gate lands in WARM_MEMORY with TTL=72h, then demotes to ARCHIVE (tombstone with `suppression_reason`). |
| `human-memory-compartmentalization.md` (F13 2026-09-18) | BINDING | STORY-class material is OUT OF KCP-002 §6 (never enters default memory; held separately). |
| `APEX-ZEN` (F13 2026-09-12) | BINDING | "Evidence before narrative" → KCP-002 §4 typed_record mandatory. |

## 11 · Promotion Path (EXECUTED 2026-10-07)

```
external_advisory_draft                            (2026-09-24, KCP-002-DRAFT)
       │
       │  F13 sovereign review via TURN 123 ("123" message)
       │  Resolution of §10 conflict (4-class binding subset preserved)
       ▼
canon/operating/memory-lifecycle-forgetting-policy.md   ← THIS FILE
       │
       │  SEAL: arif_seal invocation (system: arifOS 8088) by FI-005 on behalf of F13
       │  (Receipt pending kernel SCT path; if blocked → stamp at /root/VAULT999/seals/)
       ▼
SEAL
```

## 12 · Writer Authority Statement (updated for ratification)

```yaml
writer:
  agent_id: FI-003 (Qwen Code, anonymous session)   # DRAFT original
promoted_by:
  agent_id: FI-005 (Codex CLI)                       # ratification
  actor_verified: true
  f13_authorization: "TURN 123 message: 123"        # explicit sovereign approval
  session_id: 01a1120c-e752-7422-9acc-ec0717ee5df8
  band: SOVEREIGN_BY_DELEGATION
  f13_standing: VERIFIED_THIS_TURN

constitutional_status:
  f1_amanah: satisfied (reversible artifact + F13 ack)
  f2_truth: explicit evidence-class schema + §0 conflict resolution
  f4_clarity: entropy reduction target via 6-level forgetting hierarchy
  f11_audit: this file IS the audit + ratification receipt
  f12_injection: not_applicable
  f13_sovereign: RATIFIED (2026-10-07)

companion_artifact:
  ARC-001: /root/AAA/instructions/observation-retrieval-contract-DRAFT.md  (still DRAFT; may be promoted separately)
  audit_report: /root/AAA/reports/memory-lifecycle-promotion-receipt-2026-10-07.md
```

## 13 · Receipt Index

This RATIFIED version supersedes KCP-002-DRAFT-2026-09-24.

- `OBS-KCP2-20261007-001` — DRAFT self-audit read (line 100-110 of DRAFT)
- `OBS-KCP2-20261007-002` — evidence-discipline.md cross-check (line 84 binding)
- `OBS-KCP2-20261007-003` — F13 verbal authorization (TURN 123)
- `OBS-KCP2-20261007-004` — §10 conflict resolved (path b chosen, line 17-22 of this file)
- `OBS-KCP2-20261007-005` — file path moved DRAFT → canon location

---

DITEMPA BUKAN DIBERI ⚒️

`#KCP-002-RATIFIED-2026-10-07`
