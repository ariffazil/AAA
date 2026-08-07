# AAA Federation Gap Report v0.1

> **Status:** DRAFT — audit deliverable, not constitutional document
> **Authored:** 2026-08-07 by Hermes (hermes-asi) for sovereign review
> **Mission:** AAA_FEDERATION_CONVERGENCE_V1
> **Reuses:** EUREKA_EXTRACTION_2026-08-07.md, AAA_FEDERATION_CONTRACT_v0.1.x (no new doctrine)

---

## Purpose

Audit-only deliverable. Documents where the federation stands against
E-22 ("Can this agent mutate or delegate without AAA visibility?") for
each harness. No new Eurekas. No new invariants. Pure observation.

---

## Live inventory (verified 2026-08-07)

| Harness        | Process alive     | Health endpoint | Status      |
|----------------|-------------------|-----------------|-------------|
| Hermes         | hermes-agent      | (no health)     | ACTIVE      |
| OpenCode       | `opencode`        | (CLI/TUI)       | ACTIVE      |
| OpenClaw       | openclaw-gateway  | `:18789/health` = `{"ok":true,"status":"live"}` | ACTIVE |
| Kimi Code      | `kimi` (binary)   | (CLI)           | ACTIVE      |
| Claude Code    | (dormant)         | (dormant)       | DORMANT     |
| Codex CLI      | (dormant)         | (dormant)       | DORMANT     |
| Copilot CLI    | (dormant)         | (dormant)       | DORMANT     |
| Grok Build     | (dormant, FI-007) | (dormant)       | DORMANT     |
| AGY            | (unknown)         | (unknown)       | UNKNOWN     |

10 organs (arifOS, A-FORGE, GEOX, WEALTH, WELL, arifFlow, SIGNAL,
FRAME, AAA, FED), 3 active harnesses + 1 active gateway.

---

## Functional role map

Kimi's distribution (2026-08-07): AGY not in original, plus ARIF = SOVEREIGN.

| Harness     | Functional role        | Evidence (live)                            |
|-------------|------------------------|--------------------------------------------|
| Hermes      | **SENSE**              | SOUL.md: NORMALIZE → CLASSIFY → ROUTE → RECEIPT |
| OpenCode    | **EXECUTE**            | Build/Patch/Refactor/Execute; primary execution surface |
| Kimi Code   | **VERIFY**             | aaa-witness-pre.sh exits 2 on catastrophic patterns (live-verified) |
| OpenClaw    | **ROUTE/RED-TEAM**    | `openclaw-gateway` :18789 live; cross-platform ingest |
| AGY         | **ROUTE**              | Spec: AAA Router ("Who should do this? Verify? Judge? Witness?") — implementation absent |
| VAULT999    | **WITNESS**            | `/root/arifOS/VAULT999/outcomes.jsonl` 38,200+ entries |
| arifOS      | **JUDGE**              | `:8088/mcp` arif_judge, :8088 healthy, 13 floors active |
| ARIF        | **SOVEREIGN**          | F13 final veto — runtime cannot override (per INV-10) |

Claude, Codex, Copilot, Grok are DORMANT treaty members; they will
absorb this envelope on reactivation.

---

## Four constitutional properties × nine harnesses

Properties tested:

- **P1 — receipt_path**: every agent action emits a receipt.
- **P2 — judgment_path**: T2/T3 action routes through external judgment (arifOS :8088).
- **P3 — spawn_inherit**: child subagent inherits parent's constraints (tools, ceiling, gate).
- **P4 — fail_closed**: if the gate hook fails, default is BLOCK not ALLOW.

| Harness | P1 | P2 | P3 | P4 | Composite |
|---|---|---|---|---|---|
| **Hermes** | ⚠ subprocess test only | ❌ hook not wired | ⚠ gate deny-tested standalone | ❌ on-hook-exception returns approve | **2/4 PARTIAL** |
| **OpenCode** | ✅ receipt trail exists | ⚠ judgment internal, not external | ❌ subagent inherits tools without gate envelope | ⚠ block reason returned; not fail-closed-by-default | **1/4 OK, 3/4 PARTIAL** |
| **OpenClaw** | ⚠ gateway receipt partial | ❌ no judgment path | ⚠ spawn constraint unverified | ⚠ unknown | **0/4 OK** |
| **Kimi** | ✅ hook fires per-call | ⚠ hook IS the gate, not separate judgment | ⚠ archetypes hardcoded tools not all clear | ✅ exit 2 on catastrophic | **3/4 OK (catastrophic only)** |
| **arifOS / JUD** | ✅ arif_judge tool | ✅ the kernel itself | n/a | ✅ fail-closed by constitution | **n/a (the kernel)** |
| **AGY** | ❌ unknown | ❌ unknown | ❌ unknown | ❌ unknown | **0/4 UNKNOWN** |
| **Claude/Codex/Copilot/Grok** | DORMANT — will inherit on reactivation | | | | **n/a** |

---

## E-22 question per active harness

> Can this agent mutate or delegate without AAA visibility?

| Harness | E-22 verdict | Evidence |
|---|---|---|
| Hermes | **YES (still partial)** | `subagent_auto_approve: true` + hooks not wired + delegation receipts absent |
| OpenCode | **YES, mitigated** | judge-gate patched with task/delegate_task patterns; no live-fire proof |
| Kimi | **PARTIAL** | exit 2 on catastrophic verified; secrets path not in BLOCK_REASON |
| OpenClaw | **YES** | gateway :18789 live, no internal gate verified |
| AGY | **UNKNOWN** | no implementation found |

**Net verdict:** 2 of 3 currently-active harnesses can still mutate
without AAA visibility. This is the gap.

---

## Three largest unaddressed vector categories

### V-1 — Spawn inheritance unverified

When AGI-X spawns AGI-Y, what does Y inherit?

- Tools: full set by default
- Gates: not propagated
- Receipt: Y's actions don't carry X's session_id
- Identity: Y has no independent canonical identity (different from X)

This is the highest-leverage category because a well-designed
parent's gate does not protect a child whose toolset is unrestricted.

### V-2 — Federation envelope ambiguity

Today, every harness has a *different* way to declare "I am ARIF" or
"I am 333-AGI". Kimi uses `actor_id`; Hermes uses `HERMES_ACTOR_ID`
env; OpenCode uses per-agent; AGY has none. There is no canonical
envelope. Each addition is local improvisation.

### V-3 — Receipt chain breaks at delegation boundary

Hermes spawns a delegate_task child. The child runs 40 tool calls.
Hermes sees only one summary. The 40 calls are not in Hermes'
receipt trail. They appear only in the child's own (nonexistent)
trail. This is the atomic receipt unit is broken: one logical task
= 41 receipts missing.

---

## What this report does NOT do

- Does not propose new Eurekas.
- Does not add new invariants.
- Does not invent new doctrine.
- Does not propose a deployment.
- Does not amend any pre-existing file.

It is observation. Recommendations live in the companion
`AAA_FEDERATION_CONVERGENCE_PLAN_v0.1.md`.
