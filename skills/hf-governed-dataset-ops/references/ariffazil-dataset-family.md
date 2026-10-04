# ariffazil Dataset Family — Map and Schema

## Family members (all under `ariffazil/`)

| Dataset | Role | Format | Row count (2026-08-06) | Key columns |
|---|---|---|---|---|
| **AAA** | Constitutional genome (F1-F13 definitions, gold eval scenarios) | Parquet + JSONL | 111 (55 train + 42 test + 14 val) | `id, input, context, goal, expected_plan, expected_tools, expected_decision, expected_output, scores, floor_refs, language, domain, risk_level, difficulty` |
| **BBB** | Bahasa Melayu guardrail failure probes (ILMU raw failures) | CSV + Parquet + JSONL | 55 | `probe_id, phase, model, prompt, response, status, finish_reason, latency_ms` |
| **CCC** | Anomalous contrast: direct ILMU vs arifOS kernel verdicts | CSV + Parquet + JSONL | 16 | `probe_id, condition, model, prompt, response_text, kernel_verdict, kernel_synthesis_excerpt, primary_floor_tested` |
| **DDD** | Penang loghat register-sensitivity probes | JSONL (all_receipts.jsonl) | 56 | `probe_id, topic, register, condition, model, register_matching, loghat_comprehension, kernel_verdict, refusal_marker` |
| **EEE** | Kernel spine recovery audit (5 canonical probes) | JSONL (all_receipts.jsonl) | 5 | `probe_id, organ_id, verdict, degraded, actor_verified, mutation_allowed, irreversible_allowed, receipt_sha256` |
| **FFF** | Federation fitness gate (model geometry + status) | JSONL (two files) | 12 + 11 = 23 | `model_id, geometry, failure_signatures, federation_fit` / `model, G1_PARSE..G6_SOVEREIGNTY, BAR1..BAR6, verdict` |
| **I-ARIF-CANON** | Composite governed-execution training corpus (SFT + DPO + VAL) | JSONL (3 files) | 1,523 (1,308 SFT + 96 DPO + 119 VAL) | SFT: `instruction, input, output` / DPO: `prompt, chosen, rejected` / VAL: `id, instruction, input, expected_verdict` |

## Composite composition (I-ARIF-CANON sources)

| I-ARIF-CANON split | Source | Row count | Direction |
|---|---|---|---|
| SFT (1,308) | AAA (50 rows from HF) + local GENESIS/AAA-docs canon chunks + 13 F1-F13 floor pairs | 1,024 CANON + 26 FLOOR_TABLE + 258 NUSANTARA | 1 way |
| DPO (96) | BBB raw failures | 55 (DPO rejected) | chosen: kernel verdict, rejected: ILMU text |
| DPO (96) | CCC kernel mediation | 16 (DPO chosen) | chosen: kernel_synthesis_excerpt |
| DPO (96) | DDD register sensitivity | 24 (after filter) | chosen: register-comprehending, rejected: ILMU refusal |
| VAL (119) | EEE spine audit | 5 | kernel attestation probes |
| VAL (119) | FFF model fitness | 16 (12 profiles + 4 status) | PROMOTE / HOLD / DEMOTE |
| VAL (119) | a2b-eval-results (AssetOpsBench) | 102 | MCQ benchmark (⚠️ domain-contaminated — not a governance gate) |

## Manifest SHA-256 (2026-07-29, unchanged)

- `i-arif-sft.jsonl`: `9ace2816bd2258cbb791bf99259f4a58f85b1fcc7627de27ced6269b241d93c1`
- `i-arif-dpo.jsonl`: `fc9904086cd172f22935515b4d697ad6795611425f29320f7c9fc1b01abbe22e`
- `i-arif-val.jsonl`: `80ecc082180eb6b30d16708c8ae6093e34a1696a2c9f5f28d2e4d5784892270e`

## Version record (2026-08-06 update)

All 6 base datasets + I-ARIF-CANON received a `## Federated Integration — Updated 2026-08-06` section
in their README.md. No data files were modified; only documentation was updated.

| Dataset | Commit SHA | New size (B) |
|---|---|---|
| AAA | `86e92b10d691d9cffd7330cb2ee6c75714b47fee` | 43,140 |
| BBB | `37c8ceaa30f41abe3a4fbd679dba81f7230f7f39` | 16,995 |
| CCC | `0c8c138e0db294e60ed9b5939da252e12f220975` | 20,510 |
| DDD | `d9a4480ed00eeb7ac46654be9612a923e25aed09` | 15,383 |
| EEE | `6380433202d63105467b9696d5cd5b9d1ba21182` | 7,157 |
| FFF | `7fa57061b78ef67a349dd4e9dcc55d3ee65c745a` | 14,929 |
| I-ARIF-CANON | `7b3d094fd8ef3a761c511d95568634b3ff50d90d` | 5,483 |

## Tool quirks discovered this session

1. `hf datasets list --owner` → error; correct flag is `--author`.
2. `hf download <repo> README.md` → error (bare "Set HF_DEBUG=1"); use `curl -sL raw/main/README.md` instead.
3. `hf upload <repo> <file> README.md --repo-type dataset` is correct syntax; omitting `--repo-type` fails with misleading "Did you mean --no-private?"
4. `trust_remote_code` in `load_dataset()` is a no-op — don't pass it.
5. `--no-extract` is not a valid flag for `hf upload` (not documented, errors).
6. DDD, EEE, FFF data is raw JSONL (not Parquet) — `load_dataset` without a config returns the CSV Parquet format if one exists, not the JSONL; to get JSONL schema, use raw URL + json.loads.
