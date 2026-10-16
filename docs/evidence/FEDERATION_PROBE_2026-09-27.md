# Federation probe — observed 2026-09-27T00:52Z
> **Moved verbatim from README.md** during the AGENTIC-README-DOCTRINE v1 restructure
> (2026-10-16). This is a historical observation, **not a standing score**. Re-probe
> before quoting any row. Source archive: `docs/archive/README-2026-10-16-pre-doctrine.md`.

| Surface | Probe |
|---|---|
| AAA `:3001` | healthy. A2A card and `agent/getCard` answer. |
| arifOS `:8088` | healthy. 13 floors. |
| A-FORGE `:7072` | healthy. |
| arifFlow `:7073` | up. Diagnosis `HEURISTIC_ADVISORY`. The word `OPTIMAL` in the payload is a legacy label. |
| FED router `:7074` | healthy. Advisory only. |
| Model proxy `:4000` | liveliness answers. This is not the FED router. |
| GEOX `:8081` | process healthy. Kernel verdict `HOLD`. |
| WEALTH `:18082` | healthy. |
| WELL `:18083` | answers `degraded`. Telemetry not verified. Floors not violated. |
| FRAME `:18085` | ok. |
| CHRON `:18102` | ok. |
| HERMES `:18087` | healthy. Relay only. |
| kabarkan `:18902` | reports healthy and `consumer_missing` at the same time. |
| FLAME `:18901` | no answer. |
| Work ledger | `/root/work/tasks.json` is the queue. `/root/work/ledger.jsonl` is absent. |

For current state, re-probe `:3001/health` and the AAA surfaces — see the README's
"Current verified state" section.
