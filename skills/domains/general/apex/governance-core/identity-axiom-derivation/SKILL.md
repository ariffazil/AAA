---
name: identity-axiom-derivation
description: Use when deriving minimal axioms from codebase evidence — extract the smallest set of invariants the code actually implies.
---

# Identity Axiom Derivation

Derive the minimal set of concepts required to reconstruct a domain from first principles.

## Method

1. **Evidence Collection** — Read actual codebase structures (identity.toml, agent cards, FLOOR_TABLE.json, INVARIANTS.md, seal chain, carry_forward, vault999, tool registries, SOUL.md). NOT documentation claims.

2. **Persistence Test** — For each claimed primitive: "Does this persist through transformation?" YES = candidate. NO = projection of something deeper.

3. **Intersection Analysis** — For each pair: "Does their intersection explain an emergent concept?" (e.g., IDENTITY × FIELD → MEMORY as residue)

4. **Compression** — Remove any concept derivable from others without loss. Stop when irreducible.

5. **Verification** — Map every codebase element to axioms. Unexplained element = incomplete axioms.

## Output
Pure theory. No code, no YAML, no implementation. Axioms + compressed set + verification table + implications + open questions.

## Example
`/root/AAA/IDENTITY_AXIOMS_V0.md` — 7 axioms, 2 primitives (identity + field), 433 lines.

## Constraints
F2: Evidence-sourced. F7: Open questions listed. F13: Research only — implementation requires separate directive.
