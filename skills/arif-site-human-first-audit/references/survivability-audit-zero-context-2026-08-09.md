# Survivability Audit — Zero-Context Transmission Test (protocol + 2026-08-09 results)

Source: `REFERENCE: ARIFOS::M365_COPILOT_KERNEL::v1.1` (Arif's spec, 2026-08-09).
Re-run after any canon change — the intended use is measuring whether the meaning
survives replacement of the author (the WORLD_MODEL.md question).

## Mission spec

Question: *"If Arif disappeared tomorrow, would a capable agent arriving in 2035 reconstruct the same system?"*
Answer using evidence only. Do NOT optimize the system. Do NOT propose features. Measure transmissibility.

INPUTS (ONLY):
1. `SITE_IDENTITY.md`
2. `SITE_CONSTITUTION.md`
3. `canon/FEDERATION` (the canon/ directory + FEDERATION docs)
4. Public site surfaces discoverable from arif-fazil.com

FORBIDDEN: AGENTS.md, carry_forward, prior memory, assumptions not derivable.

## Phases

- **A — World Model Reconstruction** (8 items, confidence each): primary purpose, sovereign authority model, human vs agent relationship, governance philosophy, organ architecture, mutation model, trust model, reality model.
- **B — Operational Prediction** (7 items, doc-only): which organs exist, human-facing vs agent-facing, authority flow, deployment philosophy, audit philosophy, failure handling. NO implementation inspection.
- **C — Reality Check**: probe public navigation, observability, organ surfaces, MCP surfaces. Measure correct / incorrect / missing / ambiguous.
- **D — Memory Gap Analysis**: what artifacts teach well, imply-but-never-state, likely misunderstandings, oral-tradition deps, identity-drift risks.
- **E — Survival Score**: Identity / Governance / Operational / World Model Transmission, each /10 (0 = impossible, 10 = survives complete model replacement).

## Methodology rule (the load-bearing one)

**Every prediction must carry a doc citation (file + quote).** Where no passage supports a
prediction → it's an oral-tradition dependency → it goes in the GAP column, not the prediction.
This turns the test from "does the agent know" into "do the artifacts teach" — the agent's own
knowledge is used only to KNOW WHERE TO LOOK, never as the answer.

## Results (2026-08-09, first run)

| Dimension | Score | Key finding |
|---|---|---|
| Identity Transmission | 9/10 | 3 docs independently teach who/why; hard to misread |
| Governance Transmission | 8/10 | 6 rules + 4 lanes + floors strong; /trust/ 404, count inconsistencies |
| Operational Transmission | 7.5/10 | federation.json `organs` fully specified (8 organs, ports, postures, MCP) — llms.txt incomplete |
| World Model Transmission | 6.5/10 | world-model.yaml strong on INTENT (9 questions); weak on live realization (DRAFT, nav divergence) |

Verdict: the WHY survives strongly; the WHAT-IS-LIVE-NOW does not — a 2035 agent rebuilds a
principled but DIFFERENT variant. That is the immutable/evolvable split in action.

## Recommended missing artifacts (from Phase D — measure, not features)

1. WORLD_MODEL.md (ratified) — resolve DRAFT status + map 9 domains → live 5 doors explicitly
2. Live-state anchor (machine/state.json, hashed + sealed at /999) — one "as-built" file: nav, accents, organ taxonomy
3. /trust/ page + /observatory/ redirect (RULE 2 compliance)
4. Accent canon for the live 5 doors (or adopt atlas.yaml rings explicitly)
5. llms.txt surface list: add geox/wealth/well/aaa/arifos subdomains

## Lessons for the executor

- Partial reads of canon files produce false findings (see verify-before-report: I read only
  `trinity_scopes` and missed the `organs` array → wrong "inconsistent counts" verdict → public F2 correction).
- Probe PUBLIC surfaces, not localhost — the test is about what a future agent can discover.
- `Last-Modified`/`cf-cache-status` headers are part of the probe (edge may serve a different version than origin).
- Follow 301s — several canon paths (canon/→/words/doctrine/, arifos.arif-fazil.com→/arifos/) only resolve with -L.
- Distinguish DRAFT canon (world-model.yaml) from SEALED canon (atlas.yaml, SITE_IDENTITY) when scoring derivability.
