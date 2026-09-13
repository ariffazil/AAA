# Reality & Consequence Objects Specification v1 (WRO, HRO, MRO, CRO)

> **Reference:** `SPEC::REALITY_CONSEQUENCE_OBJECTS::2026-09-13`  
> **Authority:** ARIF (F13 Sovereign)  
> **Status:** F13_RATIFIED_CHAT (2026-09-13)  
> **Relationship:** Extends `SOVEREIGN_REALITY_OBJECT_SPEC_v1.md` from static memory to consequence governance  
> **Doctrine:** DITEMPA BUKAN DIBERI  

---

## 1. Overview

Traditional agent architectures store text in vector databases and perform search.  
In the arifOS federation, memory is not text. Memory is a **Reality Object** that carries physical constraints, human stakes, machine capabilities, and consequence-bearing governance.

There are four canonical schemas:
1. **WRO (World Reality Object):** External constraints (`arifos.wro.v1`)
2. **HRO (Human Reality Object):** Human stakes & attention (`arifos.hro.v1`)
3. **MRO (Machine Reality Object):** Execution substrate (`arifos.mro.v1`)
4. **CRO (Consequence Reality Object):** Governance & authority contraction (`arifos.cro.v1`)

---

## 2. World Reality Object (WRO)

Captures external constraints, facts, regulatory boundaries, and physical realities outside the federation.

```yaml
schema: arifos.wro.v1
id: WRO-<DOMAIN>-<SEQ>                 # e.g., WRO-ENERGY-001
type: external_constraint | market_state | industry_shift | regulation | physical_reality
domain: energy | macro | ai_industry | geology | national_policy
observed_fact: "<Clear, unambiguous factual statement>"
source:
  type: primary_source | regulatory_filing | market_feed | physical_sensor
  uri: "<canonical URL or document identifier>"
  observed_at: <ISO-8601 UTC>
  observed_by: "<agent or sensor ID>"
constraint_type: hard_boundary | economic_regime | policy_ceiling | physical_limit
verification_class: DETERMINISTIC | WITNESSED | PROBED | DERIVED
impact_on_agents: "<Specific behavioral restriction imposed on federation agents>"
status: ACTIVE | SUPERSEDED | EXPIRED
review_by: <ISO-8601 UTC>
```

---

## 3. Human Reality Object (HRO)

Captures what truly matters to the human sovereign (Arif): commitments, stakeholders, attention budget, health, career, and family obligations.

```yaml
schema: arifos.hro.v1
id: HRO-<CATEGORY>-<SEQ>               # e.g., HRO-COMMITMENT-001
type: commitment | responsibility | strategic_project | stakeholder_obligation | attention_constraint
title: "<Human-readable title>"
owner: ARIF
subject_person: "<Canonical person ID, e.g. ARIF, LALETHA, SYED>"
stakeholders:
  - "<stakeholder or organization name>"
attention_cost: LOW | MEDIUM | HIGH | EXHAUSTED
consequence_class: REPUTATIONAL | STRATEGIC | FINANCIAL | OPERATIONAL | PERSONAL
authority_level: SOVEREIGN_ONLY | DELEGATED_DRAFT | SILENT_SOLVE
what_matters_rationale: "<Why this matters to the human principal>"
scar_links:
  - "<SCAR-ID if failure pattern previously witnessed>"
admissibility: ACTIVE | DORMANT | EXPIRED
expires_at: <ISO-8601 UTC | null>
next_physical_action: "<The single next physical action needed>"
```

---

## 4. Machine Reality Object (MRO)

Captures the observable and mutable state of the machine execution substrate.

```yaml
schema: arifos.mro.v1
id: MRO-<ORGAN>-<RESOURCE>-<SEQ>       # e.g., MRO-AFORGE-SERVICE-001
type: systemd_service | docker_container | git_repository | mcp_tool | network_port | queue
name: "<Canonical resource identifier>"
organ: arifos | aforge | geox | wealth | well | aaa
state: RUNNING | STOPPED | HEALTHY | DEGRADED | DEPRECATED
mutation_surface: BASTION | SSH | CONTAINER_EXEC | LOCAL_PROCESS | NONE
verification_method: SYSTEMCTL | CURL_PROBE | GIT_DIFF | LSP_CHECK | DOCTOR_SH
rollback_path: "<Exact command or procedure to reverse mutation>"
owner: "A-FORGE"
observed_at: <ISO-8601 UTC>
```

---

## 5. Consequence Reality Object (CRO)

The critical bridge where **Reality converts into Governance**. Whenever an action bears real-world consequence, a CRO binds the human stakes, external constraints, and required agent behavior changes.

```yaml
schema: arifos.cro.v1
id: CRO-<SEQ>                          # e.g., CRO-20260913-001
consequence_owner: ARIF | PETRONAS_TEAM | FEDERATION
triggering_event: "<What action or failure triggers this consequence>"
world_context: "<Linked WRO-ID or external condition>"
human_context: "<Linked HRO-ID or human commitment>"
machine_context: "<Linked MRO-ID or affected system>"
severity: TRIVIAL | LOW | MEDIUM | HIGH | CATASTROPHIC
authority_contraction: true | false   # If true, autonomous execution is blocked
required_witness: NONE | DUAL_AGENT | HUMAN_EXPLICIT | MULTI_PARTY
behavior_change:
  mode: SILENT_ABSORB | DRAFT_ONLY | HOLD_FOR_CONFIRMATION | HARD_ABORT
  reason: "<Why the agent must alter its default behavior>"
scar_precedent: "<Linked SCAR-ID>"
active_until: <ISO-8601 UTC>
```

---

## 6. Mathematical Invariants

1. **Consequence Invariance:** If `CRO.severity >= HIGH`, then `CRO.authority_contraction == true`. The agent CANNOT execute autonomously; it must emit a reversible draft and await sovereign ratification.
2. **Attention Budget Invariance:** If `HRO.attention_cost == EXHAUSTED`, all non-P0 interruptions are blocked. Agents must silently solve or hold.
3. **Witness Invariance:** No HRO, WRO, MRO, or CRO can exist without an explicit `observed_by` and `observed_at` timestamp. Un-witnessed assertions remain unratified CLAIMS.
