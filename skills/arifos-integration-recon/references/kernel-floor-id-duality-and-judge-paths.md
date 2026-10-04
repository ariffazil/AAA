# arifOS Kernel Floor-ID Duality & Judge Entry Points (recon 2026-08-06)

State as of the 2026-08-06 recon of `/opt/arifos/app/arifosmcp/`. Some items may be fixed later — re-verify live before relying on any line below.

## Floor ID dual encoding (C1 — architectural)

| Layer | Encoding | Ref |
|---|---|---|
| GENESIS canon | F1–F13 | `/root/arifOS/GENESIS/FLOOR_TABLE.json` |
| `constitutional_map.py` `Law` enum | L01–L13 | constitutional_map.py:46-67 |
| `runtime/law.py` `LAW_DESCRIPTIONS` | L01–L13 | runtime/law.py:178-191 |
| `runtime/tools.py` literals | MIXED | L01≈44 uses, F1≈10 uses |
| `/health` `runtime_floors` | MIXED in one dict | `{F1:0.5,...,F9:0.0, L10:1.0, L11:1.0, L12:0.425, L13:1.0}` |
| `judge.py` `_identity_floors` | `{"L11","F11","L13","F13"}` | judge.py:8421 |

Cross-gate example: `runtime/tools.py:8522` accepts `"L01","L02","F1","F2"` as equivalent. GENESIS floors F1–F13 map 1:1 semantically onto Law L01–L13 (F7 HUMILITY→L07, F9 ANTIHANTU→L09, etc.).

Health payload observed (v2026.08.01): `status=degraded`, `execution_readiness=held`, `floors_active=13`, `floors_enforcement=active`, `final_authority=ARIF`, `last_seal_timestamp=null`, `ml_floors_enabled=false`, `provider.primary=sea_lion`, `ollama_healthy=false`, `deployment_drift_status=drift_detected` (but git_commit matches source — drift is cache/data, not code).

## Judge entry points (C5)

- `runtime/tools.py:23696` — `"arif_judge": arif_judge_facade` (comment: uses kernel facade in tools/judge.py)
- `runtime/tools.py:17255` — `_arif_judge_deliberate`
- `runtime/tools.py:18393` — `_arif_judge_deliberate_tool`
- `tools/judge.py:1023` — `arif_judge` (docstring 888_JUDGE v3)
- `tools/judge.py.bak-20260804-194717` + `tools/session.py.bak.20260801-072815` — backups live beside live files (C2); `diff -q` confirms judge.py vs .bak differ

## Full contradiction set (2026-08-06)

| # | Contradiction | Evidence |
|---|---|---|
| C1 | F#/L## dual encoding | runtime_floors mixed keys in one dict |
| C2 | .bak files in prod tree | diff -q confirms judge.py vs .bak differ |
| C3 | F9=0.0 vs "unmeasured" indistinguishable | no per-floor reason in /health |
| C4 | drift_detected from cache, not code | pyc/VAULT data differ; git_commit matches |
| C5 | 3+ judge implementations | facade + deliberate + tool + .bak |
| C6 | last_seal_timestamp null | key absent while vault chain verifies |

## Stabilization candidates (surfaced, NOT yet executed — await sovereign pick)

- SC5: move .bak out of prod tree (5 min, zero risk)
- SC3: wire last_seal_timestamp from VAULT999 to /health (10 min, zero risk)
- SC4: `0.0` → `null` + `reason=unmeasured` in runtime_floors (30 min, low risk)
- SC6: distinguish cache drift from code drift in deployment_drift_status (1h, low risk)
- SC2: consolidate judge entry points to one path (half-day, medium risk)
- SC1: unify floor IDs to one encoding (full day, highest blast radius — do LAST)

## Repeatable recon recipe that surfaced these

1. `curl -s http://127.0.0.1:8088/health` → save JSON; inspect keys: `runtime_floors`, `execution_readiness`, `floors_active`, `governance.laws_hard_active`, `provider_status`, `ml_floors`, `last_seal_timestamp`, `deployment_drift_status`.
2. `grep -rn "def _compute_canonical_verdict\|def arif_judge\|def _arif_judge"` across `/opt/arifos/app/arifosmcp/`.
3. Count `"F1"` vs `"L01"` literals across `runtime/tools.py` + `tools/judge.py` + `runtime/law.py` to expose dual encoding.
4. `diff -rq /root/arifOS/arifosmcp /opt/arifos/app/arifosmcp` → separate `.pyc`/data drift from real `.py` code drift.
5. `ls tools/*.bak*` → production-tree backups.
6. `python3 -c` over `/root/arifOS/GENESIS/FLOOR_TABLE.json` for canonical F-IDs.
