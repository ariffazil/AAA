# fed_signatures.yaml — TOMBSTONE

**Law for model routing is not this file.**

| Role | Path |
|---|---|
| **SOT (static routing)** | `/root/.config/federation-models.json` |
| **Reader** | `/root/AAA/scripts/fed_router.py` (`FED_SOT_PATH`) → `:7074` |
| **Live health/balance** | `token_bank.db` via `:7074` — never duplicated in JSON |

`fed_signatures.yaml` was orphaned when `fed_router_v2.py` died. Tombstoned 2026-08-17. F13 confirmed 2026-08-18: **do not resurrect the yaml as a second SOT.** Cascades live in `federation-models.json` (`fallback_chains` / `model_routes`).

If you are editing yaml for a model release, you are in the wrong file.
