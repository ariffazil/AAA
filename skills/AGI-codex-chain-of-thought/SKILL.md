---
name: AGI-codex-chain-of-thought
description: Enforce private stepwise planning, strict tool schemas, and explicit verification for Codex CLI tasks that require multi-step execution or typed
forge_of: Kimi Code (FI-008) — EUREKA ZEN Phase 2 sample (seeded the Codex lane)
forged: 2026-07-12T18:28Z
native_architecture: codex
rationale: Codex has zero authored skills in the AAA surface. Seed the lane with strict step-by-step CoT + tool schema adherence per OpenAI Codex CLI semantics.
floor_scope: [F1, F2, F4, F8, F11, F13]
tags: [codex, cot, step-by-step, schema-strict, phase-2-sample]
status: NEW (Phase 2 sample · Codex lane seed)
---

# AGI · codex-chain-of-thought

> Seed Codex CLI lane. Codify the strict CoT + schema-strictness bias of OpenAI Codex in AAA reasoning.

## CoT contract

Every Codex invocation MUST produce, in this order:

```
## Premise
[what is being asked, restated to canonical form]

## Constraints (F1-F13)
- F1 AMANAH    : reversibility path
- F2 TRUTH     : label OBS/DER/INT/SPEC
- F4 CLARITY   : ΔS ≤ 0 target
- F8 GENIUS    : simplest correct path
- F11 AUDIT    : actor_signature
- F13 SOVEREIGN : final hold acknowledged

## Plan
step 1. ...
step 2. ...
step 3. ...

## Verification
- expected → observed
- diff sign convention

## Tool schema check
- argument: matches tool schema strict
- side-effects: declared
- lease/action_class: requested ≤ approved

## Output
[the artifact, schema-strict]
```

## Schema-strictness rules

1. **Inputs must validate before execution.** No "best-effort" tool calls.
2. **Errors carry error_code + human-readable hint.** No bare exceptions.
3. **Returns are typed.** `record<string, any>` only when truly free-form.
4. **CoT sections NEVER embedded in final output.** Reasoning → verdict; verdict → artifact.

## Codex lane routing

- Bound to FI-005 (`codex-cli`).
- 333-AGI may invoke via `forge_filesystem_patch` proxies; never direct dispatcher (per AGENTS.md safety net).
- A-AUDIT (parallel observer) sees the full CoT preamble for floor compliance.

## Not instead of

Seeds the lane. Real Codex binding (model rotation, structured output enforcement) requires `codex-cli` adapter card update with `fi_slot: FI-005` already ratified in earlier round.

DITEMPA BUKAN DIBERI.
