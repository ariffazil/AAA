---
name: codebase-reality
description: "CLI-first evidence contract for federated code intelligence — revision-pinned repo dossiers, purpose-specific subgraphs, boundary gates, and reality reconciliation across intended/static/observed/verified/unknown."
argument-hint: ["<mode> <repo> [args]", "modes: repo|map|symbol|flow|impact|architecture|before_change"]
capability_tier: fed-multimodal-vision
ecology_state: WARM
---

# /codebase-reality

Executable evidence contract (ratified 2026-09-16, `domain-atlas/code-intel/RATIFICATION-2026-09-16.md`).
Every invocation MUST pin identity and separate evidence classes. Verdicts: CLAIM / PLAUSIBLE / HYPOTHESIS / UNKNOWN / HOLD.

## Core law

> An agent may propose from inference; assert only from revision-pinned evidence; execute only within a bounded capability; promote only with human authority.

Never "visualize the codebase." Always a purpose-bounded subgraph: ingress→write path, changed-symbol→impact path, schema→producer/consumer path, cycle→smallest break path.

## Identity pin (every mode, before anything)

```bash
REPO=<repo>; R=$(git -C /root/$REPO rev-parse --abbrev-ref HEAD); S=$(git -C /root/$REPO rev-parse HEAD)
echo "$REPO $R $S $(date -u +%FT%TZ)"
```

## Modes

### repo — revision-pinned dossier
Languages, package roots (NOT archive dirs — use live views per INDEX.md), entrypoints, CI surfaces, hub files. Adapters: `ls`, manifests, `cgc stats`.

### map — purpose-specific visual
Canonical configs: `/root/AAA/domain-atlas/code-intel/emerge-configs/*.yml`; regen `/root/.tools/emerge-venv/bin/emerge -c <config>` (export dir must pre-exist). Quick graphs: `pydeps <pkg> -o out.svg --max-bacon 3`, `npx --yes madge --extensions ts --ts-config <tsconfig> --image out.svg --circular <src>`. Full-repo GEOX/arifOS views are archive-contaminated — live views only.

### symbol — definitions/references/callers/callees
`cgc query "MATCH (caller)-[:CALLS]->(f:Function {name:'<sym>'}) RETURN caller.name, caller.path"` (also reverse direction; embedded FalkorDB Lite). Serena LSP for type hierarchy. All results carry file:line.

### flow — bounded path trace
Static path via chained cgc CALLS/IMPORTS queries (max_depth declared). If claiming runtime behavior → receipt lookup required, else verdict = PLAUSIBLE.

### impact — blast radius
Changed files → `git diff --name-only <base>..<head>` → for each symbol: callers via cgc → bounded subgraph. Include contracts if schemas touched (HOLD pending compatibility verdict).

### architecture — boundary gate check
Python: `PYTHONPATH=/root/<repo> /root/.tools/emerge-venv/bin/lint-imports --config /root/AAA/domain-atlas/code-intel/importlinter/<repo>/pyproject.toml`
TS: `cd <workdir-with-ts6> && npx depcruise <src> --config <rules.cjs> --ts-config <tsconfig>`
Doctrine: existing violations = baseline debt (record in ledger); FAIL only on NEW. Exceptions need owner+expiry (ledger/exceptions-ledger.json schema).

### before_change — mandatory composite (before any meaningful edit)
repo → architecture → impact → flow → reconcile → plan. Output the evidence-bundle JSON per `schema/code-reality-envelope.v1.json` + `code-reality-reconciliation.v1.json` (drafts in forge_work/2026-09-16-code-intel-phase0/). Verdict READY_TO_PLAN | HOLD | INSUFFICIENT_EVIDENCE.

## Evidence classes (label everything)

INTENDED = /etc/arifos policy/config · STATIC = parser/graph output · OBSERVED = arifFlow/kabarkan receipt (cited, environment+revision-scoped) · VERIFIED = executed checks · UNKNOWN = declared, never hidden.

"No receipt found" is evidence, not failure. "Runs in production" without a receipt = downgrade to PLAUSIBLE.

## Hard stops

- Never assert unobserved execution as fact.
- Never mutate canonical checkout, /etc/arifos, remote FalkorDB facts, or CI blocking from this skill.
- Promotion/merge/push = separate human-authorized act (888).
