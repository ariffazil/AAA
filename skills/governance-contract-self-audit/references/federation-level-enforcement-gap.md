# Federation-Level Enforcement Gap

> Compiled 2026-08-07. Source: golden-test of Hermes delegation-context.md + cross-harness audit of OpenCode / Kimi Code / Hermes / Codex / Copilot / Claude / Gemini / Cursor / Aider / Qwen.

## The Core Insight

Three harnesses (OpenCode, Kimi Code, Hermes) independently converged on:
- The same **star topology** (primary at center, no nesting, max_spawn_depth=1)
- The same **A1-A7 spawn contract shape** (spawn_reason + risk_tier + archetype + structured return + adversarial + judgment coverage + provenance + entropy gate)
- The same **authority split** (subagent = witness, primary = judge)

But none of them **enforce** their contracts programmatically. This is the federation-level enforcement gap.

## Why Enforcement Fails Last

| Stage | Effort | Status |
|---|---|---|
| Write policy doc | Low | ✅ Done in all 3 harnesses |
| Write spec | Low | ✅ Done (spawn_enums.json, A1-A7) |
| Write docs | Low | ✅ Done (Section 5, changelogs) |
| **Write validator code** | **Medium** | **❌ Missing** |
| **Wire hooks at spawn point** | **Medium-High** | **❌ Missing** |
| **Strip tools per-archetype at runtime** | **High** | **❌ Missing** |
| **Verify enforcement is actually running** | **High** | **❌ Missing** |

Each layer is more expensive than the last. Policy can be 10 lines of YAML. Enforcement is a runtime hook that must survive concurrent spawns, partial failures, and the spawner bypassing itself.

## The Three Layers of AAA Alignment

### 1. Identity alignment
- SOUL.md / AGENTS.md / SYSTEM.md present
- F13 binding declared
- Invariant (not dynamic) content only
- Cross-harness name consistency (hermes-asi vs 555-ASI naming collision known)

**Current:** OpenCode ✅, Kimi Code ✅, Hermes ✅. Others ❌ or registry-only.

### 2. Authority alignment
- Capability ceilings declared (OBSERVE_ONLY / EXECUTE_REVERSIBLE / DISPATCH_ONLY, etc.)
- Per-archetype toolset binding (which tools each archetype can use)
- Risk tier routing (T1 auto / T2+ route to arif_judge)
- Judge gate at mutation point (programmatic, not prompt-memory)

**Current:** OpenCode has `arifos-judge-gate.ts` (real hook). Kimi Code declares ceilings but doesn't strip tools. Hermes self-judges. Others undefined.

### 3. Receipt alignment
- Per-spawn telemetry (8 fields: mutations, recommendations, conclusions, risky_actions, verdicts, coverage, debt, seal_status)
- Aggregate derived-only (never canonical)
- Tri-state seal status (SEALED / UNSEALED_INFRA / FAILED_VALIDATION)
- VAULT999 chain (parent_spawn_hash → receipt_hash chain)
- Provenance per-claim (claim / source / transformation)

**Current:** Schema exists in `spawn_enums.json`. Storage backend undefined. Cross-harness aggregation undefined.

## The Federation Invariant (Arif-ratified)

> **Governance is measured per spawn, never solely per task.**

Aggregate telemetry may summarize for dashboard. Aggregate telemetry may not replace spawn-level telemetry.

Why this matters: a parallel-spawn session might look 0.8 covered on average, but spawn_2 might be at 0.4 (governance leak). Aggregate hides the leak. Per-spawn makes it visible.

## Per-Spawn Telemetry (canonical schema)

```yaml
spawn:
  id: <uuid>
  parent_spawn_id: <uuid or null>
  archetype: <from archetype_ceilings>
  spawn_reason: <from spawn_reason enum>
  risk_tier: [T1 | T2 | T3]
  expected_entropy_reduction: <string>

telemetry:
  mutations_taken: int
  recommendations_made: int
  conclusions_reached: int
  risky_actions_taken: int         # mutations + recommendations + conclusions
  apex_verdicts_sought: int        # restricted to T2+T3
  judgment_coverage: float         # clamped [0.0, 1.0]
  judgment_debt: int               # raw, not clamped

seal:
  status: [SEALED | UNSEALED_INFRA | FAILED_VALIDATION]
  vault_receipt_id: <sha256-hex or null>

receipt:
  parent_spawn_hash: <sha256-hex or null>
  receipt_hash: <sha256-hex>
```

## Tri-State Seal Status

| Status | Meaning | Action |
|---|---|---|
| `SEALED` | Constitutional seal applied, receipt in VAULT999 | Normal path |
| `UNSEALED_INFRA` | Receipt valid but vault unavailable (downtime, quota) | Retry when vault recovers. **NOT** a governance leak. |
| `FAILED_VALIDATION` | Receipt rejected by constitutional validation | **IS** a governance leak. Investigate. |

Rule: **Do not punish governance for infrastructure failure.** Audit must distinguish the two.

## Cross-Harness Alignment Checklist

For each harness, verify:

### Identity
- [ ] SOUL.md / AGENTS.md / SYSTEM.md present
- [ ] F13 binding declared
- [ ] Invariant-only (no dynamic state)
- [ ] Cross-harness name documented (lane vs model alias collision resolved)

### Authority
- [ ] Capability ceilings declared per archetype
- [ ] Toolset binding per archetype (which tools allowed)
- [ ] Risk tier routing (T1 auto / T2+ judge)
- [ ] Judge gate at mutation point (real hook, not prompt-memory)

### Receipts
- [ ] Per-spawn telemetry emitted
- [ ] Aggregate derived-only (never canonical)
- [ ] Tri-state seal status used
- [ ] VAULT999 chain (parent_spawn_hash → receipt_hash)
- [ ] Provenance per-claim (claim / source / transformation)

### Enforcement
- [ ] Validator code for spawn_request schema
- [ ] Pre-spawn gate enforces missing fields → NO SPAWN
- [ ] Post-spawn gate enforces malformed returns → INVALID RETURN
- [ ] Tool stripping at runtime per archetype
- [ ] Verification that enforcement is actually running

## Current Status (2026-08-07)

| Harness | Identity | Authority | Receipts | Enforcement |
|---|---|---|---|---|
| OpenCode | ✅ | ✅ judge-gate.ts | ⚠️ partial | ⚠️ partial |
| Kimi Code | ✅ | ⚠️ declared | ⚠️ partial | ❌ |
| Hermes | ✅ | ❌ self-judging | ❌ | ❌ |
| Codex | ⚠️ registry | ❌ | ❌ | ❌ |
| Copilot | ⚠️ registry | ❌ | ❌ | ❌ |
| Claude Code | ⚠️ registry | ❌ | ❌ | ❌ |
| Gemini CLI | ❌ | ❌ | ❌ | ❌ |
| Cursor | ❌ | ❌ | ❌ | ❌ |
| Aider | ❌ | ❌ | ❌ | ❌ |
| Qwen Code | ❌ | ❌ | ❌ | ❌ |

## What Next?

To move from "docs say X" to "AAA level":
1. **Build mechanical validator** for `spawn_request` schema (A1) in at least 1 harness
2. **Wire PreToolUse hook** for `task` tool in Kimi Code (`.kimi-code/config.toml`)
3. **Strip tools at runtime** per archetype (af-explore shouldn't have `terminal`)
4. **Verify enforcement** by attempting to bypass and confirming failure

None of these are T1 work. All are T2 with sovereign review. The current docs are sufficient to draft them; the implementation requires sustained engineering work.

## Pitfalls

- **Don't assume docs = enforcement.** Repeated trap. A policy doc that no code reads is decoration.
- **Don't promise enforcement you can't verify.** Say "drafted, not implemented" — Kimi protocol v0.1.0 PARTIAL-SEAL+, not SEAL.
- **Don't confuse "supported by harness" with "enforced by harness."** OpenCode supports subagent `mode`, but the runtime may not bind it.
- **Don't ship v0.1.0 with enforcement hooks unverified.** Spec is cheap, enforcement is expensive.