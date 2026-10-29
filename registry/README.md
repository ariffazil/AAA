# AAA Model Supply-Chain Registry

> REFERENCE: ARIFOS::AAA_MODEL_SUPPLY_CHAIN_REGISTRY::2026-10-30::v1 — authority ARIF (Human Sovereign).

## Source-of-truth declarations (read first)

1. **AAA repository = canonical registry SOT.** The normalized objects under `registry/` are the hand-governed source.
2. **`registry/generated/` = deterministic projections.** Produced by `registry/compile.py`; never hand-edit; never write back.
3. **arifOS-model-registry = optional downstream/public projection, NOT a concurrent authority.**
4. **Runtime behavior is observed by probes.** `registry/probes/` holds append-only four-field receipts.
5. **Catalog claims ≠ runtime truth.**
6. **HTTP 200 ≠ verified model identity.** A `/models` 200 yields `AUTH_VALID`/`CATALOG_REACHABLE` at most — never inference-ALIVE.
7. **Model capability ≠ execution authority.** `assignments/` + `policies/` govern use; the registry stores facts.
8. The live federation config (`/root/.config/federation-models.json`) remains the runtime SOT for routing; this registry is the normalized, evidence-bounded map OF that supply chain. Registry metadata changes never mutate production routing.

## Canonical object directories

| Directory | Object | One line |
|---|---|---|
| `organizations/` | Company / lab / platform | who exists and in WHICH roles (developer ≠ API provider ≠ host ≠ router) |
| `families/` | Model lineage | never inferred from naming similarity |
| `releases/` | One model / snapshot | release_date ≠ snapshot_date ≠ knowledge_cutoff ≠ observed_at |
| `offerings/` | Commercial plan | a plan is not a model |
| `routes/` | Credential → endpoint path | mutability_class + failure_domain + route_freshness |
| `aliases/` | Resolution contracts | silent remaps become machine-testable states, not notes |
| `probes/` | Append-only runtime receipts | requested / resolved / http_status / output_validity |
| `evaluations/` | Scope-bound performance | dataset revisions pinned, never floating `main` |
| `policies/` | How facts may be used | frozen-reference, independence, verdict grammar |
| `assignments/` | Role → model/route/task | separation of powers + independence state |
| `incidents/` | Durable drift history | never deleted because current behavior is healthy |
| `schema/` | JSON Schemas | machine-validatable contracts per object |
| `catalog/` | Legacy compatibility projection | 9 profiles preserved; canonical owner is the normalized set |
| `compiled/` | Legacy generated views | shape unchanged for existing consumers |

## Commands

```bash
python3 registry/compile.py                 # validate + emit generated/ + compiled/ (deterministic)
python3 registry/update.py discover         # inventory + SOT coverage gaps
python3 registry/update.py probe --route zai-coding-openai --model glm-5.3 --marker PONG
python3 registry/update.py reconcile        # declared vs catalog vs requested vs resolved
python3 registry/update.py validate         # schemas, refs, duplicates, conflation, secrets
python3 registry/update.py propose          # patch preview — AUTHORIZATION IS NEVER SELF-ISSUED
python3 registry/update.py witness          # post-publish push-parity + hash verification
python3 -m pytest tests/registry_supply_chain/test_supply_chain.py -q
```

Docs: `docs/ENTITY_MODEL.md` · `docs/AGENTIC_UPDATE_LOOP.md` · `docs/PROBE_CONTRACT.md` · `docs/SOT_AND_PROJECTIONS.md` · `docs/MIGRATION.md`

DITEMPA BUKAN DIBERI — Forged, Not Given.
