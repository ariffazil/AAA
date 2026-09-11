# WITNESS_MAINTENANCE — Read-Only Health as Constitutional Witness

**Forged:** 2026-09-10
**Source:** EUREKA::CAPABILITY_METABOLISM::v1
**Status:** DRAFT_AWAITING_F13

## Axiom

Health loops are witnesses. Not executors. Governance begins only when findings change future behavior.

## Canonical Form

```
Registry → Witness → Governance
```

Maintenance sits in Witness until a human or governor acts.

## Implementation

The maintenance loop (hermes-maintenance-loops) is:
- Read-only by design
- Suggestion-only output
- Never auto-applies
- Never restarts, repairs, or schedules

It checks: core files, session age, disk usage, cron health, tool stalls, SQLite state.

## Governance Rule

A maintenance finding is EVIDENCE, not a VERDICT. Findings enter the governance pipeline only when:
1. A human reviews and decides to act, OR
2. A constitutional floor is breached (F1-F13), OR
3. The finding is recurring (3+ times in 7 days) and matches a scar pattern

## Relationship to Existing Doctrine

- Implements Witness-First Doctrine at the infrastructure level
- Composes with FRAME observer: FRAME observes drift, maintenance observes health
- Composes with arifFlow: maintenance findings feed into Flow Quotient
- Separation of powers: maintenance proposes, arifOS verifies, AAA judges, A-FORGE executes
