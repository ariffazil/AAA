# FED live state baseline — 2026-08-08

> Snapshot probed via `fed_status` (MCP), `:7074/health`, and `token_bank.db`.
> Re-probe before any SEAL-grade claim (F2 / Dynamic-State: T0 evidence is only T0 evidence).

## Health
- `:7074/health` → healthy, ADVISORY_ONLY, 5 tools advertised (fed_route, fed_status, fed_probe, fed_contrast, fed_health)
- `fed-router.service` active since 2026-08-05 11:44 UTC, ~89.5M RSS

## token_bank.db schema (6 tables)
`providers` · `sqlite_sequence` · `shadow_ledger` · `route_latency` · `route_health` · `token_bank_spend`

**FED's only write path:** `log_spend()` → INSERT into `token_bank_spend` (provider, model, agent, tokens_in/out, estimated_cost_usd, called_at). Provider/health/latency tables are read-only from the MCP surface.

## Providers (live, token_bank.db)
| provider | track | balance_usd | conf | notes |
|---|---|---|---|---|
| deepseek | A | 12.54 | 1.0 | API-probed |
| flame | A | 0.00 | 1.0 | FREE mesh :18901 |
| qwen-token-plan-team | A | 0.00 | 1.0 | credits EXHAUSTED (reset 2026-09-01); non-qwen models still route |
| bailian-token-plan | B | 25.00 | 1.0 | |
| mimo-platform | B | 10.00 | 1.0 | |
| minimax | B | 0.00 | 0.95 | monthly plan, NOT PAYG — don't read as dead |
| mulerouter | B | 49.93 | 0.99 | ARCHIVED (orphaned) |
| openrouter | B | 0.50 | 0.60 | ARCHIVED (near-empty) |
| tokenrouter | B | 59.94 | 0.98 | PARKED — SHADOW-TR-001 gateway contamination |

## Route health & latency
- 17 LIVE / 1 RATE_LIMITED (qwen-token-plan-team qwen3.6-flash)
- deepseek-v4-pro: p50 615ms / p95 865ms / n=4 → flagged INSUFFICIENT_TELEMETRY (<10 samples)
- MiniMax-M3: p50 1811ms / p95 3378ms / n=5
- qwen3.6-flash: p50 225ms / p95 428ms / n=2
- flame internal tools (hermes_fact_check, hermes_epistemic_check, hermes_plan_review): n=120–150, ~3–6ms (local)

## Spend ledger (total tracked ≈ $0.07)
Recent: hermes→flame $0.0008 · apex-888→deepseek $0.0039 ×3 · 333-AGI→deepseek $0.00675 · hermes→mulerouter $0.0076

## LiteLLM federation consumers (litellm-config.yaml — 27 entries / 9 aliases)
hermes-asi ×5 · opencode ×5 · agi-333 ×4 · asi-555 ×4 · openclaw ×3 · apex-888 ×2 · dispatch ×2 · asi-555-audio ×1 · asi-555-video ×1

Key chains:
- apex-888: MiniMax-M3 (order 1) → deepseek-v4-pro (order 2) — both constitutional-eligible
- agi-333: deepseek-v4-pro → mimo-v2.5-pro → MiniMax-M3 → qwen3.8-max
- asi-555: deepseek-v4-flash → mimo-v2.5-pro → MiniMax-M3 → qwen3.8-max
- hermes-asi: mimo-v2.5 → deepseek-v4-flash → MiniMax-M3 → qwen3.8-max → qwen3.6-flash

## Route engine mechanics (fed_router.py v3.1 — confirmed from source)
10 steps: effort dial → filter DEAD → health gate (skip DEGRADED / demote RATE_LIMITED +8) → rank (direct > gateway > shadowed) → vision boost → constitutional degrade (≥666 direct only) → balance gate → latency gate (p95>5s +3) → telemetry gate (<10 samples +2, n=0 → NO_TELEMETRY) → cost surface → top-3 return with `reason`.

- Balance gate: Track A hard <$1.00 (+10, LOW_BALANCE_HARD); Track B soft <$5.00 (+5, LOW_BALANCE_SOFT); conf<0.50 or balance None → UNVERIFIABLE flag, NEVER demoted
- Effort dial: low→flame-free (0.3×, 0 passes); medium/high/ultra→deepseek-v4-pro (1.0/2.5/6.0×, 0/1/2 passes); tier ≥666 forces deepseek-v4-pro regardless of dial
- `CONSTITUTIONAL_ALLOWED`: 666/999 → {"direct"} only; 333/555/0 → direct+gateway
- 666/999 constitutional allowlist (federation-models.json): **deepseek-v4-pro, glm-5.2, qwen3.8-max, MiniMax-M3**

## Known issues (as of 2026-08-08)
- `fed_probe` MCP tool fails FastMCP validation (`Unexpected keyword argument 'provider'`) — advertised but signature broken; use `fed_status` for full state. Re-verify signature before relying on it.
- qwen-token-plan-team native models 429 until 2026-09-01 credit reset (deepseek/GLM/kimi routes unaffected — direct API keys)
- Static balances in `federation-models.json` are PURGED by design (2026-08-05) — the file's own `_meta` says any balance_usd there is STALE/FALSE. Live source = FED :7074 only.
