# SOT and Projections

## Layer map

| Layer | Path | Role |
|---|---|---|
| Runtime routing SOT | `/root/.config/federation-models.json` | what FED actually routes TODAY (providers, models, routes, agents) — loaded at FED boot |
| **Registry canonical objects** | `registry/{organizations,families,releases,offerings,routes,aliases,probes,evaluations,policies,assignments,incidents}/` | **hand-governed source of the supply-chain map** |
| Deterministic projections | `registry/generated/*.json` | compiled views; byte-identical for identical inputs |
| Legacy projections | `registry/compiled/{FEDERATION_MODEL.json,REGISTRY_INDEX.md,model-state.json,manifest.json}` | shape preserved for existing consumers |
| Legacy catalog | `registry/catalog/*.yaml` (9 profiles) | compatibility projection; canonical owner is the normalized set; never deleted in v1 migration |
| Frozen history | `registry/registries/models/AGENT_MODEL_MAP.json` | SUPERSEDED, frozen 2026-08-15, read-only snapshot |
| Downstream/public | arifOS-model-registry | optional projection, NOT a concurrent authority |

## Determinism contract

`compile.py` derives every timestamp from max(source mtimes) and stamps
`source_commit` from git HEAD — never wall clock. Same inputs → byte-identical
outputs (test-enforced). Generated files declare `generated: true`,
`generator_version`, `source_commit`, `generated_at`, `source_paths`. Generated
output never overwrites canonical sources.

## Projection inventory

| File | Answers |
|---|---|
| `catalog.json` | full normalized entity dump |
| `provider-map.json` | which orgs offer what, through which routes |
| `family-tree.json` | lineage with releases, lifecycle, dates |
| `route-resolution-map.json` | routes + aliases + latest probe verdict per route |
| `agent-assignment-map.json` | role → models/routes with failure domains + independence |
| `freshness-report.json` | family vs route freshness split, stale flags |
| `drift-report.json` | open incidents, floating aliases, unknown-developer families |

## Relationship to runtime

Registry metadata changes NEVER mutate production routing (RCR rule: the registry
describes; FED + pickers act, and pickers are written only by explicit forge steps —
F13 holds the pen). A registry `status` field is an evidence-bounded observation with
`observed_at`, not a live health feed; live balance/latency belongs to FED token_bank.
