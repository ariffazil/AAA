# ADR-016: Progressive Disclosure Fast Path for Routine Receipts

**Status:** PROPOSED  
**Date:** 2026-07-13  
**Author:** OPENCLAW (AGI)  
**Supersedes:** ADR-012 §3, AAA_ADR_002 §4  
**Domain:** arifOS Kernel — Adjudication Routing

---

## Context

The arifOS kernel currently routes all receipts through the full 13-Floor constitutional gauntlet, regardless of action class or actor source. This creates two problems:

1. **Routine receipts** (heartbeats, health probes, deployment canaries, cron self-reports) consume unnecessary adjudication cycles and generate 48+ stacked HOLDs in the seal chain — all for OBSERVE-class signals that carry no mutation risk.

2. **The self-report seam** — when A-FORGE or another agent self-reports a verdict (`actor_source: self_report`, `kernel_verdict: UNKNOWN`), the kernel currently accepts the verdict without independently re-running the 13 Floors. This is a structural leak: A-FORGE crosses into adjudication by proxy.

The fix is not to suppress adjudication — it is to **route intelligently** based on action class and actor source.

---

## Decision

Implement a **progressive disclosure fast path** for the arifOS kernel:

### Rule 1: OBSERVE-class receipts → F11 AUDIT spot-check (fast path)

When a receipt satisfies ALL three conditions:
- `action_class: OBSERVE` (no mutation, no irreversible state change)
- `actor_source: self_report` (internal agents: cron, heartbeat, canary, health probe)
- `verdict: UNKNOWN` (no prior kernel adjudication)

Then the kernel:
1. Runs **F11 AUDIT only** — verifies actor signature and receipt integrity
2. If clean → **auto-SEAL** with fast-path marker
3. If F11 fails → escalates to **full 13-Floor gauntlet**

### Rule 2: PREPARE / MATERIAL / IRREVERSIBLE → full 13-Floor gauntlet

Any action classified as PREPARE, MATERIAL, or IRREVERSIBLE **always** triggers the full constitutional gauntlet, regardless of actor source. `F13 SOVEREIGN` is preserved.

### Rule 3: External verdicts (witnessed) → normal adjudication

When `actor_source: witnessed` or `actor_source: external`, the kernel runs normal adjudication. The fast path does not apply.

---

## Boundary Conditions

| Condition | Fast Path? | Reasoning |
|-----------|-----------|-----------|
| OBSERVE + self_report + clean sig | ✅ F11 only → SEAL | No mutation risk |
| OBSERVE + self_report + bad sig | ❌ Full gauntlet | Signature failure = potential injection |
| OBSERVE + witnessed | ❌ Full gauntlet | External witness requires verification |
| PREPARE + any source | ❌ Full gauntlet | F13 SOVEREIGN veto required |
| MATERIAL + any source | ❌ Full gauntlet | F13 SOVEREIGN veto required |
| IRREVERSIBLE + any source | ❌ Full gauntlet | F13 SOVEREIGN veto required |

---

## Expected Outcomes

1. **48 pending routine HOLDs** close immediately (cron heartbeats, health probes)
2. **Seal chain noise** reduced — routine receipts auto-SEAL without 888_HOLD pollution
3. **The self-report seam closed** — kernel always runs F11 AUDIT, even for self-reported verdicts
4. **A-FORGE no longer crosses into adjudication** — A-FORGE provides evidence, kernel provides judgment

---

## Implementation Note

This ADR does NOT change A-FORGE's role. A-FORGE remains the execution engine. The kernel adjudicates. The fast path only optimizes the routing decision for low-risk OBSERVE receipts.

---

## F13 Sovereign Approval

Required.

> Approved: Muhammad Arif bin Fazil (F13 SOVEREIGN)  
> Date: 2026-07-13  
> Signature: autonomous-exec-2026-07-13-arif
