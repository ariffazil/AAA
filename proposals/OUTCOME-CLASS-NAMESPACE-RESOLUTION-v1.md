# outcome_class Namespace Collision — Resolution Proposal v1

> **Status:** PROPOSED_HELD_FOR_F13 (2026-09-25) · FI-003 (BUILD lane)
> **Companion law:** FATWA K1 (`AAA/instructions/namespace-fatwa-k1.md`) — same pattern, new instance
> **Origin:** 2026-09-25 morning session verification of L13 — flagged as F13 binary #5

## The collision

Two federation organs independently minted the name `outcome_class` with
**different value sets and different planes**:

| Plane | Owner | Shape | Ratified by |
|---|---|---|---|
| **Actuator receipt field** (code enum) | A-FORGE executor, `src/executor/types.ts:79` | 5-state: SUCCEEDED / FAILED / DEGRADED / UNKNOWN_OUTCOME / (NEUTRAL) — F13-ratified L13 spec (UNKNOWN_OUTCOME closes the false-binary defect) | F13 2026-09-25 ("execute L11 and L09 too" line) |
| **Consequence record field** (wire field) | arifFlow RG-7, `mcp/arifflow-mcp.py` | 3-value: recovery \| regression \| neutral — the Reality Graph's consequence taxonomy | RG-7 doctrine (2026-09-12 line) |

Same name, disjoint semantics. A future join (executor receipt → RG-7
consequence edge) will silently mis-map unless the namespaces are marked now.

## Proposed resolution (K1 pattern — markers, not renames)

**Ruling 1 — No rename.** Both fields are load-bearing in ratified surfaces.
Renaming either breaks live consumers for zero capability gain.

**Ruling 2 — Coordinate markers (the actual fix).** In any artifact where both
appear (dashboards, joins, cross-organ schemas, VAULT999 records):

- A-FORGE enum ⇒ write `executor:outcome_class`
- arifFlow RG-7 field ⇒ write `rg7:outcome_class`

Bare `outcome_class` in a cross-organ context becomes a naming violation (F10),
exactly like bare `999` post-K1.

**Ruling 3 — One SOT per coordinate.**
- Executor enum SOT: `A-FORGE/src/executor/types.ts` (+ spec `A-FORGE UNKNOWN_OUTCOME v1`)
- RG-7 field SOT: `/root/arifFlow` RG-7 consequence records

**Ruling 4 — If a join is ever built** (executor receipt → consequence edge):
the bridge owns the translation table and must publish it as
`OUTCOME_CLASS_BRIDGE` with an explicit mapping (5-state → 3-value is
lossy: UNKNOWN_OUTCOME maps to no RG-7 value — it must HOLD, not coerce).
This rule exists to prevent silent lossy coercion at a future seam.

## What this does NOT decide

- Whether the two taxonomies should eventually unify (that is a doctrine
  question, 888-lane, not a namespace question).

## F13 binary

SAH this proposal as-is, or reject with direction. No code changes are
required by Rulings 1–3 beyond documentation adoption at the next natural
edit of each surface.
