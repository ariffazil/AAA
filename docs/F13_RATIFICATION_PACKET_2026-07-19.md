# F13 Ratification Packet — T3 WAJIB Actions

> **For:** Arif (F13 SOVEREIGN)  
> **From:** Federation conformance audit  
> **Date:** 2026-07-19  
> **Source:** REALITY_AUDIT_2026-07-19 (58/100, ORANGE, HOLD_EXPANSION)  
> **Status:** AWAITING SOVEREIGN REVIEW  

## What This Is

7 WAJIB actions require changes to the kernel contract — new cryptographic primitives, authority flow restructuring, or constitutional doctrine codification. These **cannot** be auto-executed under ORANGE band. Each requires your review and ratification before code touches the kernel.

## The 7 T3 WAJIBs

### WAJIB 2 — Independent Verification Lane

**What changes:** A new `forge_verify` role that is separate from `forge_execute`. A-FORGE executes; an independent verifier checks the outcome against success criteria.

**Constitutional impact:** Creates a new separation of powers. The executor can no longer self-certify completion.

**New primitives:**
- `verification_request` / `verification_result` schema
- Verifier identity ≠ executor identity enforcement
- Kernel rejection of self-verification

**Risk if wrong:** Low — verification is advisory, not blocking. A bad verifier produces bad reports, not bad mutations.

---

### WAJIB 3 — Normalize Kernel State Semantics

**What changes:** Replace the contradictory `LIMITED_MUTATE`/`OBSERVE_ONLY` fields with a single `effective_state` object. All surfaces derive from this one canonical source.

**Constitutional impact:** Touches `arif_init` response schema. Every consumer of kernel state is affected.

**New primitives:**
- `effective_state: { actor_verified, authority_band, mutation_allowed, seal_allowed, verdict, reason }`
- Conformance test: no surface may describe stronger authority than canonical

**Risk if wrong:** HIGH — if the canonical state is wrong, all downstream decisions are wrong. Must be tested exhaustively before deployment.

---

### WAJIB 4 — Delegation Attenuation

**What changes:** Signed delegation envelope that cryptographically enforces `child_authority ⊆ parent_authority`. OBSERVE parent cannot create MUTATE child.

**Constitutional impact:** Changes how A2A handoffs and child agents work. Creates new invariants that cannot be violated.

**New primitives:**
- `delegation_envelope` schema (parent_session, child_principal, allowed_tools, authority_band, max_blast_radius, expires_at, delegation_depth, redelegation_allowed, kernel_signature)
- 8 adversarial tests (OBSERVE→MUTATE denied, expired denied, revoked denied, etc.)

**Risk if wrong:** MEDIUM — too strict blocks legitimate work; too loose enables authority escape.

---

### WAJIB 5 — Fire-Time Reauthorization

**What changes:** Every deferred mutation (cron, queues, retries, Renovate, long-running tasks) is judged twice: write-time AND fire-time. No grandfathered authority.

**Constitutional impact:** Changes the execution model for all scheduled/queued work.

**New primitives:**
- `deferred_action` envelope
- `reauthorize_at_fire()` kernel verb
- Fire-time checks: identity, lease expiry, current state, blast radius, evidence freshness

**Risk if wrong:** MEDIUM — could break existing cron jobs and automation if too strict. Must be phased.

---

### WAJIB 7 — Organ Disagreement Doctrine

**What changes:** Codified resolution order when GEOX, WEALTH, and WELL disagree: hard veto → blast-radius precedence → Pareto search → F13 escalation. No silent fallback to execution order.

**Constitutional impact:** Formalizes the relationship between domain organs. Creates binding precedence rules.

**New primitives:**
- Domain veto with evidence + release condition
- Blast-radius ownership mapping
- Pareto option search
- Automatic F13 escalation trigger

**Risk if wrong:** LOW (operationally) — the system currently has no resolution, so any doctrine is better than none. Risk is in getting the precedence WRONG and having e.g. WEALTH override WELL safety.

---

### WAJIB 8 — Context-Capture Governance

**What changes:** Every durable context artifact (INIT, NEXT_AGENT_INIT, boot docs, agent definitions) gets a `context_manifest` with classification, authority level, expiry, and approval status. Agents cannot upgrade guidance to policy by placing it in a privileged path.

**Constitutional impact:** Governs what agents can write that influences future agents. Prevents boot-context capture.

**New primitives:**
- `context_manifest` schema (artifact_id, class, author, authority_level, approved_by, binding, expires_at, constitution_compatibility, supersedes, content_hash)
- 6 context classes: Observation, Operational handoff, Guidance, Policy, Constitution, Memory

**Risk if wrong:** LOW — advisory classification doesn't block anything. Risk is in classification disputes.

---

### WAJIB 10 — End-to-End Signed Canary

**What changes:** A single federation-level test that exercises the full lifecycle: ChatGPT → MCP init → identity challenge → arifOS session → AAA route → organ observe → kernel judgment → A-FORGE lease → reversible sandbox mutation → independent verification → RSI record → VAULT999 receipt → rollback → second verification.

**Constitutional impact:** None — it's a test, not a contract change. But it gates the "AGI-substrate ready" claim.

**New primitives:**
- Federation canary test script
- Sealed receipt with all identities, lineage, hashes, evidence, signatures

**Risk if wrong:** NONE — it's a test. It either passes or it doesn't.

---

## Recommended Ratification Order

1. **WAJIB 3** (kernel state) — dependency for WAJIB 2, 4, 5, 8
2. **WAJIB 2** (verification lane) and **WAJIB 8** (context governance) — can be done in parallel
3. **WAJIB 4** (delegation) and **WAJIB 5** (fire-time) — can be done in parallel
4. **WAJIB 7** (disagreement) — independent, but benefits from earlier work
5. **WAJIB 10** (canary) — gates everything

## What Happens If You Defer

The 7 T3 WAJIBs are exactly the gap between the current score (58) and AGI-substrate readiness. Without them:
- The system remains constitutionally designed but not constitutionally proven
- Autonomous agents cannot be trusted with mutation authority
- The "hands never judge" invariant is architectural prose, not enforced code
- Deferred execution (cron, queues) can escape authority through time

**The system remains safe to operate under human supervision.** These WAJIBs are about graduating from supervised to autonomous.

---

*DRAFT — awaiting F13 review and ratification.*  
*DITEMPA BUKAN DIBERI*
