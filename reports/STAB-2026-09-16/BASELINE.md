# BASELINE — STAB-2026-09-16
> Captured: 2026-09-16 ~13:40 UTC · Two independent clients (Hermes + OpenClaw)

## Organ Health

| Organ | Health | Commit (built/deployed) | Drift | Verdict |
|---|---|---|---|---|
| arifOS | 200 | 58e5740 / 58e5740 | false | OK |
| A-FORGE | 200 | 17db70d / 17db70d | — | OK |
| AAA | 200 | 9cc4129 / — | — | OK |
| GEOX | 200 | 4128750 / 4128750 | — | OK |
| WEALTH | 200 | e446f92 / e446f92 | — | OK |
| WELL | 200 | 9f71af2 / 9f71af2 | — | OK |
| arifflow | 200 | — / — | — | OK |

## arif_init (session SEAL-4de3dde08a4a473a)

- actor: arif-fazil → canonical "arif", verified=true
- authority_band: LIMITED_MUTATE, seal_allowed=false
- substrate: HEALTHY
- built_commit == deployed_commit, drift=false
- canon: 2026.09.16-58e5740, 3/3 verified
- VPS: load=4.8, mem=62.7%, disk=77.7%

## Seal Ledger (arif_seal mode=verify)

- ledger_size: 1761
- chain_length: 1357
- canonical_entries: 56
- unlinked_seal_entries: 959
- integrity: GAPS_FOUND
- canonical chain verified: true
- Three counts disagree → K8 CONFIRMED (cross-verified: two clients, same numbers)

## Public /999/verify

- head_seq: 39
- last_seal: 2026-09-16T03:39:07.013968Z (not null, fresh)
- verified_at: 2026-09-16T13:41:22.589082Z

## Registry Status

| Organ | Intended | Registered | Exported | Callable | Verdict |
|---|---|---|---|---|---|
| WELL | 10 | 40 | 19 | 10 | REGISTRY_DRIFT (9 unexpected public) |
| WEALTH | 12 | 12 | 12 | 12 | PASS |
| GEOX | — | 31 tools | — | — | OK (surface count = 31) |

## Apex Scalars

- G: 0.5 (runtime) / 0.4689 (kernel_baseline, n=18958)
- C_dark: 0.1588
- W3: 0.94
- h: 0.913
- nine_signal: SELAMAT (init) / RETAK (entropy observe — verdict_monotonicity degradation, not floor failure)

## Port Map (truth)

| Service | Port | Source |
|---|---|---|
| arifOS | 8088 | STAB + live |
| A-FORGE | 7071 | STAB + live |
| AAA | 3001 | live /health |
| GEOX | 8081 | STAB + live |
| WEALTH | 18082 | STAB + live |
| WELL | 18083 | STAB + live |
| arifflow | 7073 | STAB + live |
| signal (Kabarkan) | 18084 | live /health |
| FRAME | 18085 | OpenClaw witness |
| hermes-mcp | 18087 | memory |

## OpenClaw Witness Notes

- Two clients, same time window, exact match on K8 numbers
- Authority middleware consistent: LIMITED_MUTATE via identity, no leakage
- Substrate contradiction found: constitutional_check says DEGRADED vs result.substrate says HEALTHY (same envelope)
