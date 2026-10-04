# WEALTH Organ (:18082) — Live Probe Notes (2026-08-06)

All facts below live-verified via curl against `http://127.0.0.1:18082` on 2026-08-06.

## Surface
- `GET /health` → `status:healthy`, `tools_loaded:8`, `transport:"streamable-http"`, apex scalars all `UNMEASURED`, `git_commit` pinned.
- MCP endpoint: `POST /mcp` (streamable-http). Full handshake required (see umbrella SKILL.md §3.1).

## Session double-gate (WEALTH-specific — two gates, not one)
1. **Header gate** (same as other organs): `Mcp-Session-Id` from `initialize`.
2. **Argument gate (unique to WEALTH):** tool ARGUMENTS must ALSO include `session_id` (and `actor_id`). Header alone → `SESSION_REQUIRED` / `L11 AUTH: session_id required for all WEALTH tools (FORGE 2026-07-18: anonymous reads blocked)`.
3. **arif_init trap:** `arif_init` on :8088 returns `session_id:"unknown"`, `session_token:null` (kernel bug) → WEALTH rejects it with `SESSION_INVALID: Unknown or expired session ID`.
   **Workaround:** pass a real id from `/root/.local/share/arifos/carry_forward.json` (e.g. `SEAL-cdcd8af97efd464d`) as `session_id` in the tool arguments.

## The 8 canonical tools (mode-discriminated — read schemas with tools/list first)

| Tool | Modes (verified) | Key args | Notes |
|---|---|---|---|
| `capital_primitive` | npv, irr, emv, evoi, mc, kelly, markowitz, robust, chance_constrained, two_stage | npv: `cash_flows[]`, `discount_rate`; mc: `initial_value`, `growth_rate`, `volatility`, `periods`, `simulations` | NPV → `{npv,...}`; MC → p10/p25/p50/p75/p90/mean. **Argument is `cash_flows`, not `cashflows`.**
| `capital_health` | conservation, flow, runway, survival, fiscal_breakeven, confluence, asymmetry | — | financial health metrics |
| `capital_diagnose` | stress_index, governance_capacity, cascade_model, exploitation_detect, collapse_signature, beautiful_mouse, capture_scan, power_audit, bid_surface, optimize_mwc, cadence_monitor, crisis_reflex | mode only | all 12 live-verified OK; covers institutional/power diagnostics |
| `capital_market` | commodity, fx, indicator, stock, gold, oil, gas | commodity: `brent_crude`/`wti_crude`/`natural_gas_henry`/`natural_gas_jkm`/`lng_asia`/`gold` | **`mode="snapshot"` is INVALID** (`BAD_INPUT_VALUE`) — snapshot is the operation inside gold/oil/gas; use `mode="commodity"` for live Brent |
| `capital_registry` | **status only** | — | **NOT an asset database** — returns tool counts + probe state (`registry_truth`, `probe_failures`). `mode="query"` → `BAD_INPUT_VALUE`. |
| `capital_ledger` | vault999 query/append paths | — | |
| `capital_entropy` | entropy diagnostics | — | |
| `wealth_judge_handoff` | prepare, submit | intent, reversibility, blast_radius, actor_cryptographically_verified | submit + blast_radius=critical without crypto-verified actor → `888_HOLD_REQUIRED`. Flags are caller-controlled = advisory, not enforced. |

## Result envelope (every tool)
`tool_name, tool_version, domain, result, result_type, epistemic_tag (OBSERVED/DERIVED/INTERPRETED/SPECULATED/ASSUMED/...), claim_state (DRAFT/PLAUSIBLE/CONFIRMED/...), evidence_quality, execution_authorized, execution_authority, requires_888_hold, source_attribution[], computation_timestamp, witness{human,ai,earth,is_complete}, session_id`. Plus `_meta.wealth_receipt` = receipt state (see defect 1).

## Known defects (live-verified 2026-08-06)
1. **Receipt chain broken:** EVERY tool call returns `_meta.wealth_receipt.persisted:false`, `error:"receipt target is not provisioned; no file was created"`, path `/root/VAULT999/wealth/receipts.jsonl` (hardcoded server.py:240). Directory does not exist on host (`stat` → ENOENT). F11 AUDITABILITY unreachable from WEALTH. **Fix:** `mkdir -p /root/VAULT999/wealth && touch receipts.jsonl && chmod 640` + ensure systemd unit `ReadWritePaths=` allows it; verify next call returns `persisted:true`.
2. **`capital_registry` is a health checker, not a store.** No asset DB exists anywhere in WEALTH — the Brazil report's Appendix A table was acting as the database. Highest-leverage gap = a `wealth_case_register`-style tool.
3. **`capital_wisdom` is a ghost tool:** unregistered engine (dict key `_capital_wisdom_engine`, canonical.py:1983; Zen Phase 1.3 "WEALTH computes, arifOS frames" — normative synthesis deliberately unregistered). `wealth_omni_wisdom` alias maps to `internal_wisdom_engine` (server.py:53) which is not importable.
4. **`resource_count:14` hardcoded** (server.py:883, 1335) vs 19 actual `@mcp.resource` decorators. C1 drift confirmed.
5. **Monte Carlo is single-factor GBM only** (`initial_value/growth_rate/volatility`) — CANNOT do correlated multi-factor (brent × tax × capex) joint simulation. Don't claim multi-factor capability for it.

## Sibling-claim verification results (2026-08-06)
- ✅ CONFIRMED **Appendix A5 range bug:** LOW/HIGH columns are independent input ranges, not optimistic/pessimistic scenarios. Re-derived: true band = $3,235–5,477M (width $2,242M) vs published $4,235–4,477M (width $242M) — ~10× compressed. Midpoint break-even thesis survives; tail risk ~$2.3B not ~$977M.
- ✅ CONFIRMED **Exxon sensitivities** (Brent +$1/bbl = +$700M; refining margin +$1/bbl = +$800M; NA PE +$100/T = +$560M; USGC ethane −$50/T = +$450M) — verified against Exxon IR CloudFront CDN PDF ("Sensitivities and Key Assumptions", Jan 30 2026) — the primary source; sibling OneDrive links are private/undownloadable. Same doc: refining margin formula = 60% USGC 2-1-1 + 40% NWE 2-1-1.
- ✅ CONFIRMED **Brent live snapshot** via `capital_market(mode="commodity")`: price $79.65, regime DOWNTREND, EMA200 $82.3, RSI ~48.7–54.2, verdict SABAR (confluence 0.053).
- ❌ REFUTED **"capital_registry is an asset store"** — health checker only (see defect 2).
- ❌ REFUTED **"C4 capital_market→capital_health attribution bug"** — source shows capital_market emits its own `tool_name="capital_market"` in all paths; live `mode="fx"` call returns `tool_name: capital_market`. The claimed 1-line fix would fix nothing.
- ❌ REFUTED **"capital_market mode=snapshot"** — `BAD_INPUT_VALUE`; snapshot is an internal operation for gold/oil/gas modes.

## Live market snapshot field map (`mode="commodity", commodity="brent_crude"`)
```
ticker:    symbol (XBRENT), price, ema20/ema50/ema200, emaTrend, rsi, rsiState, pivot, support[], resistance[], skewness_20d, changePct
signal.regime:   regime (DOWNTREND/...), confidence, price, ema_20/ema_50/ema_200, rsi
signal:    direction, verdict (SABAR/...), confluence_score, rr_ratio, judge_reason, stop_loss, take_profit_1/2, entry_price
zones:     buy_zone{sell_zone{price, strength}
macro:     dxy, us10y, vix, usmyr, silver, timestamp
_cross_witness: feed_type "LIVE", witness_status "SINGLE_SOURCE" (cross-witness needs 2nd source; delta>3% → WITNESS_DIVERGENCE)
```
2026-08-06 sample: price 79.65, dxy 99.74, us10y 4.617, vix 15.81, usmyr 4.09.

## Arif's WEALTH stabilization invariants (acceptance criteria — from 888-APEX verdict 2026-08-06)
I1 session before tools · I2 source before synthesis · I3 registry before modeling · I4 OBS/DER/INT mandatory · I5 witness count mandatory · I6 sensitivity mandatory · I7 judge before artifact.
His final verdict: **SEAL::PATH_A** — orchestration-first (single `wealth_case_register` patch), NOT a 15-layer rebuild; "satu masalah, satu patch, satu hari". Real gaps = SENSE/DECODE/REGISTRY/ARTIFACT layers + receipt provisioning (M0), not capital math.
