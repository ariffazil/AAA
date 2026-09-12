# EFFECT-IDEMPOTENCY CONVENTION v1 — external effects under U12

> **Status:** ACTIVE convention (2026-09-12) — operationalizes U12 of FEDERATION-CONSTITUTIONAL-INVARIANTS-v1.1 (F13_RATIFIED_CHAT) · Gate-2 item 5, additive layer
> **Tool:** `scripts/effect_guard.py` — check / register / replay (append-only registry at `~/.local/share/arifos/effect_registry.jsonl`)
> **Protocol source:** v1.1 ambiguous-commit clause — durable intent before effect, idempotency identity, terminal outcome, UNKNOWN + reconciliation, never blind retry.

## The field

Any receipt for an EXTERNAL effect (Telegram send, API mutation, deploy, payment, vault seal) carries:

```json
"effect": {"kind": "<class>", "target": "<id>", "idempotency_key": "<stable-key>"}
```

`idempotency_key` = stable function of (intent + target + parameter digest). Same intent retried → same key.

## Discipline (agents, tonight onward)

1. **Before** firing an external effect after any ambiguity/timeout/retry: `effect_guard.py check --key K` — rc=2 means a committed prior exists: DO NOT re-fire, reconcile against external state instead (U13).
2. **Before firing** (where feasible, per v1.1): register `--status attempted`.
3. **After outcome**: register terminal status — `committed` / `denied` / `unknown`.
4. `replay --window-h N` reconstructs the effect timeline merged with AAA commit history — read-only, commits pinned at their historical SHAs (policy state at effect time, not current HEAD).

## Scoped to owner lanes (NOT tonight, per UL-007 do-not-cascade)

- Kernel: `effect` as first-class ingest field; idempotency enforcement at the arifFlow boundary.
- Hermes lane: Telegram send path calls `check` before send + registers after (the highest-volume external surface).

## Acceptance test (falsifier)

Register a real effect → `check --key` must return rc=2 (blocked); replay must show it annotated with the policy commit in force; no test may fire an external effect.
