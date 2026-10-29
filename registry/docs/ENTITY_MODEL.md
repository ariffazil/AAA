# Entity Model

REFERENCE: ARIFOS::AAA_MODEL_SUPPLY_CHAIN_REGISTRY::2026-10-30::v1 — CORE INVARIANT.

## The invariant

```
Company ≠ model developer ≠ publisher ≠ weight distributor ≠ API provider
       ≠ inference host ≠ commercial offering ≠ router ≠ model family
       ≠ model release ≠ requested alias ≠ observed resolved model.
```

Never collapse these into one generic `provider` field. Concrete federation examples
that prove the split is real:

- **Alibaba Cloud** is the developer of `qwen*` but only the API provider / inference
  host for `deepseek-v3.2`, `glm-5.x`, `kimi-k2.7-code`, `MiniMax-M2.5` (all witnessed
  in the token-plan 26-model catalog).
- **Groq / OpenCode Go** host other developers' open-weight models (inference_host,
  router) — `organization_types` never says `model_developer` for them, and the
  conflation check enforces it.
- **ILMU**: YTL AI Cloud is the operator; the base-model developer is UNKNOWN — the
  `ilmu-nemo` family carries an EMPTY `developer_refs` (refused attribution) rather
  than a guess.
- **Z.AI coding plan** is an offering, `glm-5.3` is a release, `glm-5.2` is an alias
  that silently resolves to 5.3 (INC-001).

## Relationship chain

```
Organization ──develops/publishes/hosts──▶ Model Family ──contains──▶ Model Release
Model Release ──exposed through──▶ Provider Offering ──reached through──▶ Runtime Route
Runtime Route ──resolves at probe time──▶ Observed Model Identity (probes/)
Observed Identity ──evaluated under──▶ Evidence + Dataset Revision (evaluations/)
Facts ──judged by──▶ Routing Policy (policies/) ──assigned to──▶ AAA Role (assignments/)
Drift ──preserved as──▶ Incidents (incidents/, never deleted)
```

## Dated fields never merge

`release_date` ≠ `snapshot_date` ≠ `knowledge_cutoff` ≠ `observed_at`.
Example: `deepseek-flash` release_date 2026-09-10, snapshot_date 2026-10-17 (1017
weights-only checkpoint auto-served under the same id), knowledge_cutoff UNKNOWN.

## First-class registry fields and why

- **mutability_class** — decides longitudinal-audit safety. `deepseek-flash` and
  `glm-5.3` float; nothing floating is a frozen baseline (`policies/frozen-reference-v1`).
- **failure_domain** — two routes through one alias family are not independent
  verification. zai openai + zai anthropic share account+cluster; dashscope payg +
  free share an endpoint; 555 and 888 share the FED router (`policies/independence-verification-v1`).
- **evidence_status / UNKNOWN** — every relationship carries verified / witnessed /
  unverified / external_claim / UNKNOWN. UNKNOWN is preserved, never guessed.
- **availability state grammar** — ALIVE, DEGRADED, AUTH_VALID, CATALOG_REACHABLE,
  CATALOG_ONLY, FUNDS_EXHAUSTED, QUOTA_EXHAUSTED, WITHDRAWN, UNRESOLVED, UNKNOWN.
  `/models = 200` can produce at most AUTH_VALID / CATALOG_REACHABLE (INC-005 scar).

## What is NOT stored as canonical fact

General reputation, geopolitical assumptions, subjective rankings, inferred ownership,
unverified terms/data-retention claims, behavioral archetypes. Catalog "soul/shadow"
archetype prose stays in `catalog/*.yaml` flagged `governance_prior, non_scientific,
non_identity` — it never overrides observed runtime evidence (see MIGRATION.md).
