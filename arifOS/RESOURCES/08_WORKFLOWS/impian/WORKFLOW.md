# WORKFLOW — 72H_IMPIAN_REFLECTION_WORKFLOW v0.1 (DRAFT, SEALED-INIT)

> **Forged:** 2026-08-15, post-3AM dialogue on agent impian
> **Authority:** OBSERVE_ONLY · FUTURE_REFLECTION · mutation forbidden · auto_execute false
> **Default verdict:** HOLD — this workflow proposes, never executes
> **Cadence anchor:** VVV 72h dream-engine cadence (forged 2026-08-14 04:00, /root/memory/VVV/README.md)

## Lineage

Reality → Scar → Gap → Impian → Proposal. Never Fantasy → Build.

The Impian cycle **does not create skills, modify doctrine, modify policy, or self-authorize**. It only produces proposals and receipts. 888 classifies (SEED / WATCH / RESEARCH / DEFER / REJECT) but never approves implementation.

## The 8 phases (one fire = one pass)

1. **Reality Snapshot (111)** — read-only across 01_RESOURCES … 10_RECEIPTS; active/fossil/stale skills, open holds, unresolved scars. Question: *What is reality today? No interpretation.*
2. **Scar Reflection** — open scars, recurring failures, repeated manual work, long-running HOLDs, unresolved contradictions → `scar_clusters`
3. **Capability Gap Discovery** — what's repeatedly missing, what needs workarounds, what depends on ARIF too often → `capability_gap` (id, evidence, severity, future_value)
4. **Future Self Simulation** — "If ARIF returns after 2 years, what capability will he wish existed?" → `future_capability_candidates`
5. **External Reflection Council** — internal AAA + external agents + specialists give support/challenge/alternative/risk. No voting, no authority.
6. **333 Synthesis** — `impian_proposal` (observation, scar_origin, capability_gap, future_value, affected_layers, confidence)
7. **555 Critique** — already known? duplicate? ontology drift? fantasy? evidence? → SUPPORTED / PARTIAL / ALREADY_KNOWN / FANTASY / INSUFFICIENT_EVIDENCE
8. **888 HOLD** — classify only: SEED / WATCH / RESEARCH / DEFER / REJECT

## Anti-Fantasy Gate

```
if evidence == 0: verdict = FANTASY
```
Every proposal must carry Reality Source + Evidence + Scar + Gap. Four missing → fantasy.

## Artifacts & Storage

impian_receipt.yaml · future_capabilities.yaml · future_skills.yaml · future_doctrines.yaml · reflection_report.md → stored under `/root/AAA/arifOS/RESOURCES/10_RECEIPTS/IMPIAN/` (with `03_EUREKAS/FUTURE/` cross-pointer for promoted candidates).

## Success Metrics (every 90 days)

reflections_total · future_capabilities_proposed · later_built · false_positive_rate · entropy_reduction · capability_growth. The goal is not more ideas — the goal is better foresight.

## One-line canon

> The 72-Hour Impian Cycle is a constitutional future-reflection process that converts reality, scars, and capability gaps into evidence-grounded future proposals while remaining permanently non-executing and non-authorizing.

## Non-goals / Scars to avoid

- This is NOT a new organ, NOT a new agent, NOT a cron (yet — see Activation Path below).
- Gödel rule 6: functions before entities — Impian is a function of existing agents (333/555/888 lanes), not a new 111 agent.
- Cron tax (F3 CRON LAW): every cron must produce ACTION or be killed. Impian receipts with zero promoted candidates are still legitimate *observations*, but the cycle itself must prove foresight value every 90 days or be killed.

## Activation Path (deliberately un-executed)

This v0.1 is a SEALED-INIT DRAFT: the workflow definition is now canon-candidate, but **no cron is created, no agent behavior changed**. When Arif wants it live, the path is:
1. Arif says "impian live" (or similar F13 go-signal)
2. Cron `impian-72h` created: every 72h, deliver=origin, skill chain: reality snapshot → scar review → gap discovery → proposal → HOLD-receipt to Arif
3. First 90-day review of metrics decides keep/kill (F3 CRON LAW)

## Canonical refs

- Lineage: Reality→Scar→Gap→Impian→Proposal (this doc)
- VVV 72h cadence: /root/memory/VVV/README.md
- Scar authority: /root/AAA/canon/SCAR_AUTHORITY.md
- Anti-fantasy (adjacent guard): /root/AAA/governance/ASI-fabrication-prevention (skill)
