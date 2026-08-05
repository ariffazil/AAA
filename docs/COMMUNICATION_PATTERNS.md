# COMMUNICATION_PATTERNS — Inference vs Delegation

> **Pointer, not constitution.** Canonical: `/root/AGENTS.md`.
> Companion: [`ORGANS_VS_AGENTS.md`](./ORGANS_VS_AGENTS.md) — the boundary question this doc is contingent on.
> Status: doctrine draft, ratified 2026-08-05 in sovereign discussion.

## The rule

```
human ↔ model   = direct inference (LiteLLM)   — 1 hop, 1 call
agent ↔ agent   = delegation (A2A)            — task lifecycle, discovery, artifacts
```

Never put multi-agent coordination machinery between a single user and a single model.
A2A's agent-card discovery, task state machine, and artifact streaming solve
"which of N agents can do this, and how do I track a long-running delegated task" —
neither problem exists on the Hermes CLI → model path.

## The trade-off ledger (the part docs usually gloss over)

| | LiteLLM direct | A2A delegation |
|---|---|---|
| Hops | 1 | 3–5 |
| Latency | inference-bound | + protocol overhead |
| Context cost | conversation only | + protocol metadata |
| Failure modes | simple (timeout/retry) | complex (state machine) |
| **Audit trail** | **none built-in** | **protocol-native (task lifecycle → receipts)** |
| Seal chain | none | writeSeal per task → VAULT999 |

On the chat path you are trading **structured audit trail for latency** — not getting both.
If provenance on the primary chat path is wanted later, it means bolting a receipt
hook onto the LiteLLM path (Lane B `forge_vault(mode="receipt")` exists), not
switching the whole path to A2A.

## The carve-out (and its expiry condition)

"A2A makes sense for delegating to GEOX/WEALTH/WELL because they are a *different
agent*" — this holds **only while organs stay separate services**. If organ tools
collapse into a caller's namespace (the A-FORGE precedent), the "different agent"
disappears and the path collapses to the same "just call the tool" shape as
LiteLLM. A2A's carve-out evaporates with it.

**Therefore this decision is not independent of `ORGANS_VS_AGENTS.md`.**
Resolving "do organs stay services" resolves this one too, in either direction.
