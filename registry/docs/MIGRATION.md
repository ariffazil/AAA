# Migration Record — 2026-10-30 (v1)

From: `registry/catalog/*.yaml` (9 legacy profiles) + `registry/compile.py` (legacy compiler)
To: normalized 11-object supply-chain registry + deterministic dual projections.

## Preserved (verify against tests)

- All 9 catalog profiles remain in place and loadable (`test_nine_catalog_profiles_accessible`).
- Qwen + Z.AI **freshness split survives**: `family_freshness` lives on families
  (`families/qwen.yaml`), `route_freshness` on routes (`routes/zai-coding-*.yaml`,
  `routes/qwen-tp-*.yaml`) — never merged (`test_freshness_split_family_vs_route`).
- The **four-field probe contract survives** as schema + `verdict_for()` + migrated
  receipts (`probes/`) — catalog `provenance.falsifier.probe_contract` prose became
  machine-checkable state.
- `known_remaps` survive as append-only alias contracts with receipts
  (`aliases/zai_glm-5.2.yaml`, receipt SEAL-d186bb9c9f934225) and as incidents.

## Migrated witnesses (no invention)

Every normalized field traces to an SOT patch note, a catalog record, or a frozen
historical file — see each entity's `evidence_refs`. Where evidence was absent the
field is `UNKNOWN` (e.g. glm release dates, most knowledge cutoffs, opencode corporate
operator). Baseline note: the brief's stated baseline commit `7d28533cf` is the PUBLIC
MIRROR head (filtered-mirror SHAs diverge from the local repo, so it does not resolve
in the local object store — confirmed by the push range `7d28533c..` at publication);
the witnessed LOCAL baseline is `0ce43e47`. Both are true statements about two
different histories: local canonical vs filtered public.

## Field-class decisions

- Catalog "soul/shadow" behavioral archetypes stay in `catalog/*.yaml` as
  `governance_prior, non_scientific, non_identity` — they never populate normalized
  capability fields and never override runtime evidence.
- `knowledge_cutoff` claims without source stay `{value: null, evidence_status: UNKNOWN}`.
- Availability/quota states carry `observed_at` (INC-005 grammar).
- Credentials appear ONLY as env-var names (`credential_env_refs`); secret scan runs
  in the compiler and the test suite.

## Fields that could not migrate cleanly (DEBT)

See the mission report DEBT section — top items: gpt-5.5/claude releases are
route-key-only records; hermes-asi/apex-888 upstream rungs unnormalized; qwen
vl/omni legacy ids and wan/qwen-image multimodal releases unnormalized; MiniMax M2.5
served-only record; gemini/sea-lion/xai/openrouter ecosystems unmapped; evaluations/
empty pending pinned HF dataset revisions.

## Rollback

Single-repo additive change: `git revert` the registry commits restores the prior
state; `catalog/` and legacy `compiled/` shapes were never destructively rewritten.
