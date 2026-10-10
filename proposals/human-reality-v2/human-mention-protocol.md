# HUMAN-MENTION-PROTOCOL v1 — Gateway Preload Tollgate

> **Status:** STAGED for gateway wiring · awaiting F13 "wire"
> **Date:** 2026-10-10 · **Author:** HERMES · **Owner:** F13
> **Data:** `human_reality_register.json` (26 persons, 147 sourced entries) · `name_mention_current_flow.md` (hook anchors) · `infra_live_state.md`
> **Law:** `valence-loss-asymmetry.md` Law 2 (BOUND not COMPUTE) · `human9-spec.md` §9 (retrieval filter) · F5 family privacy · MINOR absolute.

## 0 · Purpose

Any human name/alias in any inbound message, in any lane, passes this chain
BEFORE the LLM generates one token of reasoning. Fail-closed. No exceptions,
no salience override, no valence override.

## 1 · The chain (mandatory physical tollgate)

```
MSG text
  │
  1 RESOLVE    scan text vs people-index (names + aliases + identities)
  │            no hit → pass through untouched, log MISS
  │            hit → canonical person:id (+ confidence)
  │
  2 GATE       scope check (dm/shared, fail-closed on unknown room shape)
  │            F5 family / MINOR → absolute withhold from output surface
  │
  3 VALENCE    read register valence_transitions ONLY (state_before→after+trigger)
  │            no transition on record → UNKNOWN_VALENCE  (never synthesize)
  │            Ω0 < 0.7 → quarantine: facts render, valence does not
  │
  4 TRUST      read domain vectors (gym/emotional/logistics/money) from LEDGERS
  │            empty vector → UNKNOWN (never inferred from text sentiment)
  │
  5 AIRGAP     F13_ONLY invariant layer: read-only to all runtimes.
  │            Mutation path = F13 word only. Schema-enforced (jq-probed).
  │
  6 PRELOAD    bounded projection appended to gateway preload block:
                 MENTIONED: <id> · layers state/strategy only (TTL-checked)
                 · trust domains as UNKNOWN where empty
                 · scope: dm facts withheld in shared rooms
  │
  7 WITNESS    append receipt line (event → id → gate verdicts) to ledger
```

## 2 · Layer TTL (enforced at preload, not by hope)

| Layer | TTL | Expiry behavior |
|---|---|---|
| state | 72h | expired → not preloaded |
| strategy | 60d | expired → downgraded to attractor candidate |
| attractor | 1y | expiry marks RE-VERIFY, not delete |
| invariant | ∞ | F13_ONLY write · always loaded, never mutated by runtime |

A bad mood expires before it can pollute the character model.

## 3 · Hard floors (no chain output may override)

F1 reversibility · F2 truth (UNKNOWN is a valid terminal answer) · F5 family
privacy · MINOR protection · consent scope · no interior computation (H5).
A high-valence or high-salience mention NEVER widens an envelope.

## 4 · Wiring point (measured, not guessed)

Hook **C** — dedicated plugin on the `pre_llm_call` bus
(`name_mention_current_flow.md` §hook C; model: probe-first-reflex
:303-306; enable config.yaml:168-177). Fully isolated from lane_switch.
Fallback hook **A** (`pre_gateway_dispatch` :626, rewrite path wired at
run_inbound.py:95-99) if bus registration is blocked.

## 5 · Fail modes = pass-closed, not pass-open

- Register read fails → `MENTIONED: <raw-name> · REGISTER_UNREACHABLE` + proceed without facts. Never guess identity.
- Ambiguous name (two ids) → preload BOTH ids with AMBIGUOUS flag; runtime must not silently pick one.
- TTL boundary race → older claim wins (STALE marked), newer unverifiable claim never auto-promoted.

## 6 · Falsifier

Protocol fails if: (a) any human mention reaches the LLM without a gate
verdict logged; (b) any synthesized valence/trust value appears in preload;
(c) a scope:dm fact renders in a shared room; (d) the F13_ONLY layer is
mutated by any path other than F13 word.

## 7 · Verification (post-wire, before claim "live")

1. Synthetic probe: message containing "Syed" in a shared lane → preload contains id + shared facts only.
2. dm-scoped fact leak test in shared room → must NOT render.
3. Unknown name "Zulkifli" → REGISTER_MISS logged, zero fabrication.
4. jq probe: F13_ONLY block unchanged after 100 runtime mentions.
5. Ledger receipt count == mention count (no silent drops).
