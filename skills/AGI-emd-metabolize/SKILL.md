---
name: AGI-emd-metabolize
forge_of: Kimi Code (FI-008) — EUREKA ZEN Phase 3 (audit gap fill)
forged: 2026-07-12T18:28Z
rationale: Audit showed only 6 of 244 active skills mention "metabolize" — narrow, concentrated in dream-engine + audit-skill-atlas. Add explicit contract between encode→decode with witness check. Phase 3 gap fill.
floor_scope: [F1, F2, F4, F8, F11, F13]
tags: [emd, metabolize, memory-promotion, witness-check]
status: NEW (Phase 3 gap fill)
---

# AGI · emd-metabolize

> The `M` in EMD. Bound to 333-AGI runtime. Distinct from decode (next step backward, not forward).
> Doctrine: take decoded segments and decide what promotes to durable memory vs ephemeral observation.

## Promotion tiers (L1 → L6)

| Tier | Class | Example | Reversible |
|---|---|---|---|
| L1 | Conversation cache | current turn scratch | yes (auto) |
| L2 | Session transcript | this session memory | yes |
| L3 | Cross-session fact | "Kimi handles EUREKA ZEN" | partial |
| L4 | Constitutional record | SEAL-grade events | no (sealed) |
| L5 | Pattern emergence | dream-engine outputs | partial |
| L6 | Civilizational canon | ratified treatises | no (append-only) |

## Witness check (F3)

Before any L4+ promotion:
- Human witness — explicit or via `actor_signature=arif-fazil`
- AI witness — `forge_evaluate` APEX score ≥ 0.80
- External witness — VAULT999 chain head valid + G ≥ 0.85

W³ = ∛(h × ai × ext) ≥ 0.70 to promote L4+.

## Malu scalar (F9 anti-bias)

Failure to promote (a verified segment that should have been L4 but ended L2) increments Malu by 0.05.

Malu > 0.85 → 888_HOLD triggered on the relevant agent.

## Not instead of

Sits between `AGI-emd-decode` (L1/L2 always) and the dream-engine (L5/L6 in batch). Never auto-promotes without witness. Never demotes without explicit human ack.

DITEMPA BUKAN DIBERI.
