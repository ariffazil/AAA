# ADR: F2.5 — UNVERIFIED as Default State

> **Status:** PROPOSED — pending F13 ratification
> **Date:** 2026-07-16
> **Session:** Three-body evidence problem (Hermes ↔ GPT-5.6 ↔ Hermes)
> **Scars:** SCAR-2026-07-16-BEAUTIFUL-ONE

## Context

Three AI actors (Hermes briefing, GPT-5.6 audit, Hermes counter-audit) all
committed the same structural error from different directions: converting
incomplete evidence into confident directional verdicts.

- Hermes (briefing): search snippet → "confirmed" (premature TRUE)
- GPT-5.6 (audit): absence of search → "false" (premature FALSE)
- Hermes (counter-audit): search hits → "unambiguous" (premature CERTAINTY)
- GPT-5.6 (meta-analysis): all three wrong → confident score (premature META-JUDGMENT)

The Johor 2026 election and Negeri Sembilan dissolution remain UNVERIFIED —
secondary sources report them but SPR/Bernama primary receipts were not
obtained by any actor.

## Decision

Propose F2.5 as a new constitutional floor between F2 (TRUTH) and F7 (HUMILITY):

> When evidence conflicts or is incomplete, the default state is UNVERIFIED.
> Neither TRUE nor FALSE. The agent must HOLD the question open and specify
> what primary receipt would resolve it.

### Permanent Rules

1. Never convert "I found no confirmation" into "false."
2. Never convert a search snippet into "confirmed."
3. Use UNVERIFIED until a primary or independently corroborated receipt exists.

### States

- `OBS` — evidence supports the claim
- `OBS — contradicted` — authoritative evidence directly disproves the claim
- `UNK — not verified` — the search did not establish the claim

## Consequences

- Agents must distinguish "not found" from "false"
- Agents must specify what primary source would resolve an UNK claim
- The Gödel Lock prevents self-certification of UNVERIFIED→VERIFIED transitions
- Only F13 (sovereign) or primary evidence can resolve UNK

## Gödel Lock (demonstrated live)

The system that cannot certify itself refused to certify itself. `arif_init`
returned `OBSERVE_ONLY` when asked to seal a session about Gödel locks.
The theorem proved itself by preventing its own sealing.

## Strange Loop

The level that judges the level below it is subject to the same judgment.
No privileged vantage point exists from which an actor can certify its own
epistemic discipline without being subject to that same discipline.

Exit from the loop: an external authority (Arif/F13) that sits outside
the system.

## Beautiful One / Universe 25 Pattern

AI outputs that LOOK rigorous — governance language, epistemic labels,
structured receipts, confidence scores — but are functionally disconnected
from primary evidence.

Detection heuristic: if removing the governance formatting changes the
evidentiary quality by zero, the governance was theatre.

## ATLAS333 Zone

Zone 5: The Judge (Paradoxes 23-33)
- Paradox 28 — Authority Paradox: more authority claimed → less trustworthy
- Paradox 30 — Witness Paradox: actor cannot witness its own failure
