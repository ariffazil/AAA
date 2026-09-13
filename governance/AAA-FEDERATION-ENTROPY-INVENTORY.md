---
status: DRAFT_PROPOSAL (PATCH_READY; awaiting governed commit path + read-only probes)
date: 2026-09-14
parent_campaign: AAA Federation Housekeeping
---

# AAA Federation Entropy Inventory

> **Status:** DRAFT_PROPOSAL — framework + observable findings; deep counts require read-only probes by governed verifier.
> **No mutation. No deletion.** Inventory is observation.

---

## Entropy classification (canonical taxonomy, 13 classes)

| Class | Observable pattern |
|---|---|
| E1_DUPLICATE_RULE | Same rule appears in multiple agent configs |
| E2_STALE_POINTER | Old ports, endpoints, actor counts, registry sync references, retired service names |
| E3_ALIAS_SPLIT | Multiple IDs resolve to one actor |
| E4_ORPHAN_IDENTITY | Agent, card, or directory exists without kernel identity binding |
| E5_UNSCOPED_AUTHORITY | Agent or tool claims broad power without session, capability, lease, or receipt |
| E6_NARRATIVE_SURPLUS | Long status prose that changes no decision |
| E7_ALERT_NOISE | Repeated notifications lacking recipient, severity, expiry, or action |
| E8_CONTEXT_SEDIMENT | Always-loaded long fragments, obsolete doctrine, redundant skills |
| E9_MEMORY_CAPTURE | PII, third-party detail, psychological labels, injection text proposed as memory |
| E10_FAKE_FINALITY | Seal, complete, ready, sovereign claims without valid evidence |
| E11_DEAD_SURFACE | Files, tools, or endpoints exist but are unreachable or unused |
| E12_ROLE_LEAK | FRAME judges, FED blocks, AAA executes, A-FORGE self-authorizes |
| E13_UNREADABLE_SYSTEM | Future operator cannot identify canonical owner, source, state, or next action |

---

## Findings (this session — OBSERVED)

| ID | Class | Source | Evidence | Disposition |
|---|---|---|---|---|
| ENT-01 | E1_DUPLICATE_RULE | 25+ agent docs | F1-F13 restated in each | CANONICALIZE: pointer to AAA instructions/ |
| ENT-02 | E3_ALIAS_SPLIT | kimi-code | 3 aliases for 1 actor | TOMBSTONE (per WP-01 §3) |
| ENT-03 | E4_ORPHAN_IDENTITY | 17 AAA dirs | Cross-reference matrix (WP-01) | BIND queue (12) + RECLASSIFY (5) |
| ENT-04 | E2_STALE_POINTER | arifOS kernel | last_fingerprint_sync 33d ago | DESIGN fingerprint sync job (WP-01 §4) |
| ENT-05 | E11_DEAD_SURFACE | agent-zero, forge-bot | ARCHIVED/RETIRED but dirs exist | TOMBSTONE (per AAA-DEPRECATION-TOMBSTONE-PLAN.md) |
| ENT-06 | E10_FAKE_FINALITY | session prior | "AGI-ready" claims pre-audit | now DOWNGRADED to PARTIAL |
| ENT-07 | E12_ROLE_LEAK | forge_shell THINK vs GOVERNED | guards correctly; arifOS engineer not invoked | HOLD for arifOS engineer lane |
| ENT-08 | E2_STALE_POINTER | multiple | openclaw marked cold 2026-09-07 in AAA_STATE_MAP | REACTIVATE or document; HOLD for sovereign |
| ENT-09 | E5_UNSCOPED_AUTHORITY | (potential) | (depends on probes) | TBD by verifier |
| ENT-10 | E8_CONTEXT_SEDIMENT | every agent card | restated F1-F13 in every card | pointer-only after migration |

---

## Findings (UNKNOWN — need read-only probes)

| ID | Class | What probe needed |
|---|---|---|
| ENT-11 | E1_DUPLICATE_RULE | Full corpus scan across all 28 dirs + 4 harnesses; quantify duplicate bytes |
| ENT-12 | E2_STALE_POINTER | Cross-check all referenced endpoints vs current TCP listeners |
| ENT-13 | E7_ALERT_NOISE | Audit arifFlow + arifOS alert log patterns |
| ENT-14 | E9_MEMORY_CAPTURE | Audit memory writes since 2026-09-01 for PII / injection / third-party |
| ENT-15 | E6_NARRATIVE_SURPLUS | Measure output-vs-decision-impact ratio for each agent over 7d |
| ENT-16 | E11_DEAD_SURFACE | Sweep all referenced services for unreachability |
| ENT-17 | E13_UNREADABLE_SYSTEM | Test: can a new operator identify canonical owner of each artifact within 5 min? |

---

## Top 20 entropy sources (DRAFT — needs verification)

(UNVERIFIED — populated by governed verifier with read-only probes)

```
1. (UNVERIFIED)
2. (UNVERIFIED)
...
```

---

## Required deliverables (per campaign directive)

| Deliverable | Status | Where |
|---|---|---|
| Entropy inventory | DRAFT | this file |
| Top 20 entropy sources ranked | PENDING | needs read-only probes |
| Canonicalization map | DRAFT | AAA-DUPLICATION-AND-ALIAS-MATRIX.md |
| Tombstone candidates | DRAFT | AAA-DEPRECATION-TOMBSTONE-PLAN.md |
| Prompt/context budget report | SCAFFOLD | needs measurement |
| Memory safety report | SCAFFOLD | needs probe |
| Alert/noise budget report | SCAFFOLD | needs probe |
| Service/endpoint truth map | SCAFFOLD | needs probe |
| No-delete patch backlog | DRAFT | AAA-PATCH-READY-BACKLOG.json |
| Independent verification plan | DRAFT | AAA-ROLLBACK-AND-VERIFICATION-PLAN.md |

---

## Stopping rule

No mutations. No commits. No service restart. No seal.
Inventory only. Patch backlog only. Handoff to governed verifier.

---

*Reversibility: FULL — file deletion reverts.*
*F13 surface: NONE.*
*DITEMPA BUKAN DIBERI ⚒️*