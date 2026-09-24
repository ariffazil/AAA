# KCP-002 — Memory Lifecycle and Forgetting Policy (DRAFT)

> **Status:** `external_advisory_draft` — awaiting F13 ratification
> **Companion to:** `observation-retrieval-contract-DRAFT.md` (ARC-001, this session)
> **Writer:** FI-003 anonymous session, `actor_verified=false`, `OBSERVE_ONLY`
> **Authority required for promotion:** F13-verified human (Arif, Muhammad Arif bin Fazil)
> **Canonical standing:** **NONE** — advisory artifact only
> **Mutability:** Reversible (rm/edit by sovereign direction)

---

## 1. Principle

```
Evidence is preserved.
Claims are contestable.
Memory is fallible.
Canon is scarce.
Authority remains human.
```

The wise system is not "remember everything" or "forget everything". It is **selective institutional memory** — high retention on authority/evidence/reusability, deprioritized retrieval on staleness, restricted access on sensitivity, and F13-gated irreversibility.

---

## 2. The Five Questions (Policy Contract)

The policy answers only five questions. Anything that cannot answer one of these is out of scope.

```text
1. What may enter memory?
2. In what form: evidence, claim, decision, entity, procedure, or archive?
3. Who may create, revise, supersede, or delete it?
4. When does it leave default retrieval?
5. What requires F13 authorization before irreversible removal or canon promotion?
```

---

## 3. Intake

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

---

## 4. Consolidation (Typed Record Required)

```yaml
consolidation:
  requires:
    - typed_record (with declared schema)
    - provenance_reference (who/where/when)
    - evidence_class:
        class: OBSERVED | MEASURED | DERIVED | INTERPRETED | POLICY | HYPOTHESIS | UNKNOWN
        confidence: CONFIRMED | DERIVED | SPECULATIVE | OPINION
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

A good prose passage is not canon. A confident answer is not authority. Retrieval is not validation. Promotion to canon requires F13.

---

## 5. Retrieval Priority Order

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

---

## 6. Forgetting Hierarchy (6 Levels)

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

---

## 7. Retention Defaults by Material Type

| Material | Default fate | Reason |
|---|---|---|
| Raw source evidence (files, probes, logs) | Preserve/immutable, access-controlled | Future disputes need original grounding |
| Live runtime observations | Expire quickly, retain summarized receipt | State changes rapidly |
| Failed hypotheses | Archive with falsification outcome | Prevent repeated dead ends |
| Superseded policy | Archive + successor link | Historical lineage matters |
| Duplicate generated drafts | Deprioritize; retain canonical hash reference | Reduce retrieval noise |
| Sensitive private artifacts | Restrict or delete by explicit retention policy | Privacy and dignity outrank curiosity |
| Human decisions / F13 records | Preserve with strong integrity | Authority history is load-bearing |
| Agent self-narrative / persona text | Low retention unless encodes approved rule | Prevent identity theatre |

---

## 8. F13 Authority Boundary

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

---

## 9. Retention Equation (Operational, Not Deterministic)

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

---

## 10. Overlap with Existing Ratified Doctrine

This DRAFT **extends** the existing evidence discipline and must not silently override it.

| Existing artifact | Status | Relation to KCP-002 |
|---|---|---|
| `/root/AAA/instructions/evidence-discipline.md` (F13-ratified 2026-08-10, binds 333-AGI) | BINDING | KCP-002 adds MEASURED / POLICY / HYPOTHESIS / UNKNOWN as new evidence classes; uses full names OBSERVED/DERIVED/INTERPRETED.evidence-discipline.md explicitly says "do not invent EVIDENCE/INTERPRET/UNKNOWN". KCP-002 must either (a) be promoted by F13 with explicit extension approval, or (b) be re-scoped to treat existing 4-class as binding subset and propose additions as separate proposal. |
| ARC-001 DRAFT (this session) | external_advisory_draft | Companion — observation/retrieval contract. KCP-002 is the memory-lifecycle/forgetting counterpart. |
| APEX-ZEN canonical (F13-ratified 2026-09-12) | BINDING | KCP-002 implements the ZEN principle "Evidence before narrative" via typed records + provenance. |

**Action items before F13 review:**

1. Reconcile 4-class (evidence-discipline.md) vs 7-class (KCP-002). Either:
   - (a) Promote 7-class with explicit F13 extension approval, OR
   - (b) Rescope KCP-002 to treat OBS/DER/INT/SPEC as binding subset, and propose MEASURED/POLICY/HYPOTHESIS/UNKNOWN as a separate layered addition.
2. Confirm retention defaults in §7 against any existing retention policy (none found in instructions/ at probe time — UNKNOWN if any exists outside instructions/).
3. Confirm F13 authority boundary in §8 matches current constitutional baseline.

---

## 11. Promotion Path

```
external_advisory_draft                                 (current state)
       │
       │  F13 sovereign review via verified session
       ▼
draft_for_f13_ratification
       │
       │  Arif approval, exact artifact + exact mutation declared
       ▼
canon/operating/memory-lifecycle-forgetting-policy.md
       │
       │  constitutional seal via arif_seal (requires kernel SCT path healed)
       ▼
SEAL
```

Until promoted:

- ✓ May be referenced as an advisory policy proposal
- ✓ May be used to inform workspace-level retention decisions
- ✗ Is **not** binding doctrine
- ✗ Is **not** enforced by `mcp_guard`
- ✗ Is **not** ratifiable without F13 sovereign authority
- ✗ Does **not** override `evidence-discipline.md` (2026-08-10, F13-ratified)

---

## 12. Writer Authority Statement

```yaml
writer:
  agent_id: FI-003 (Qwen Code, anonymous session)
  actor_verified: false
  authority_band: OBSERVE_ONLY
  f13_standing: NONE
  role_in_this_artifact: external_advisory_draft_author
  ratification_path: requires_verified_arif_session

constitutional_status:
  f1_amanah: satisfied (reversible artifact)
  f2_truth: explicit evidence-class schema + confidence tiers
  f4_clarity: entropy reduction target via forgetting hierarchy
  f11_audit: this file IS the audit
  f12_injection: not_applicable
  f13_sovereign: pending (sovereign ratification required for promotion)

companion_artifact:
  ARC-001: /root/AAA/instructions/observation-retrieval-contract-DRAFT.md
  audit_report: /root/AAA/reports/observation-mechanism-audit-2026-09-24.md
```

---

## 13. Receipt Index

This DRAFT cross-references the following live-probed receipts (captured this session):

- `OBS-KVM8-20260924-2143-001` — arifOS kernel health
- `OBS-KVM8-20260924-2143-002` — federation ports
- `OBS-KVM8-20260924-2143-003` — arifFlow FQ / vector
- `OBS-KVM8-20260924-2143-004` — VAULT999 head / last seal
- `OBS-KVM8-20260924-2143-005` — MCP process count
- `OBS-KVM8-20260924-2200-006` — evidence-discipline.md content (this turn)

---

DITEMPA BUKAN DIBERI — Advisory draft, awaiting F13 ratification if promotion is desired.

`#KCP-002-DRAFT-2026-09-24`
