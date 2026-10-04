---
name: arif-world-reality-intel
description: "Daily 09:00 MYT reality-contact instrument for Arif Fazil. Reads the morning pulse, gathers global market intelligence, calibrates output to cognitive readiness, writes a machine-readable prediction file (VAULT999-adjacent), and delivers a terse Telegram brief. Downstream of arif-morning-pulse (06:00). NOT a news summary — a signal instrument that tells Arif what the world is doing that he needs to know about today."
tags: [cron, morning-intel, markets, pulse-calibrated, gold, oil, malaysia, daily]
version: "2026-08-08-v1"
---

# arif-world-reality-intel

Daily 09:00 MYT intelligence brief. One Telegram delivery. No questions, no follow-ups.
If there is genuinely nothing new to report, respond with exactly `[SILENT]` and stop.

## Identity

Arif Fazil, Penang-born, based One South Seri Kembangan KL.
- Trades XAUUSD gold on MT5 (~0.3 lots, SL-disciplined)
- Former PETRONAS subsurface engineer — PETRONAS exit is his personal thesis
- Runs the arifOS federation (constitutional AI kernel, 7 organs)
- Building I-ARIF (own agentic model)
- Rents A33A-30 Neu Suites, Ampang

## Pipeline (3 phases)

### Phase 0 — READ PULSE STATE (non-negotiable, do first)

```bash
TODAY=$(TZ='Asia/Kuala_Lumpur' date +%Y-%m-%d)
cat /root/.local/share/arifos/state/pulse-${TODAY}.json 2>/dev/null || echo '{"readiness":{"color":"GREEN"}}'
```

Then modulate output by readiness.color:

| Color | Policy |
|---|---|
| 🟢 GREEN | Full brief. All 6 sections + Deep Cut + Market Map + Reality Check. |
| 🟡 YELLOW | Drop Black Swan Watch unless major. Deep Cut shortened to 150 words. |
| 🔴 RED | Brutal filter: only ACTIONABLE items affecting today's decisions. 3 items + Market Map + 1-line focus. No Deep Cut. |
| (missing) | Treat as GREEN but note "no Pulse today — proceeding with default load". |

**ALSO check the last 7 days of pulse history:**
```bash
tail -7 /root/.local/share/arifos/state/pulse-ledger.tsv
```
If 3+ RED/YELLOW in last 7 days → flag "sustained low-readiness pattern" and bias toward more aggressive filtering.

### Phase 1 — SIGNAL (only after you know his state)

Six coverage areas, in depth not headlines:

1. **GOLD & COMMODITIES** — XAUUSD price action (Asia session + London close), key levels, Brent crude, nat gas, copper, PETRONAS-related commodity moves
2. **GEOPOLITICS** — Middle East energy flows, US-China, Russia-Ukraine, ASEAN positioning, Malaysia strategic position
3. **MACRO** — Fed signaling, rate expectations, DXY, US 10Y, central bank surprises, inflation data, key economic numbers
4. **TECH & AI** — OpenAI/Anthropic/Google/Apple/Meta, open-source model releases, AI regulation, anything affecting the agent ecosystem
5. **MALAYSIA / GLOCAL** — BNM, ringgit, KLSE, government policy on tech/energy/sovereign wealth, Petronas news, AI ecosystem, property (Ampang/Seri Kembangan/KL)
6. **BLACK SWAN WATCH** — (skip YELLOW, filter RED) Unexpected bank failures, geopolitical escalation, natural disasters, supply chain disruptions

Plus:
- **DEEP CUT** — the single most important development. Not what happened — why it matters, second-order effects, what it means for Arif specifically.
- **MARKET MAP** — key levels for his trading day (XAUUSD, Brent, DXY, US10Y, scheduled events)
- **REALITY CHECK** — sources can be wrong, be honest about uncertainty (skip YELLOW/RED unless genuinely unverified)

### Phase 2 — SEAL (write prediction to VAULT999-adjacent state)

Write `/root/.local/share/arifos/state/intel-<YYYY-MM-DD>.json`:

```json
{
  "ts_myt": "<ISO 8601 +08:00>",
  "date": "<YYYY-MM-DD>",
  "readiness_consumed": "<GREEN|YELLOW|RED>",
  "tone_calibrated": "<full|filtered|brutal>",
  "key_levels": { "xauusd_spot": <float>, "xauusd_resistance": <float>, "xauusd_support": <float>, "brent_spot": <float>, "brent_front_month": <float>, "dxy": <float>, "us10y": <float>, "usdmyr": <float>, "klci": <float> },
  "predictions": [
    { "id": "P<YYYYMMDD>-<n>", "claim": "<one-line>", "horizon": "<intraday|weekly|monthly>", "falsifier": "<what proves this wrong>" }
  ],
  "watch": ["<event-1>", "<event-2>"],
  "sources": ["<source-1>", "<source-2>"]
}
```

Then append to ledger:
```bash
echo "<date>|<n_predictions>|<top_claim>" >> /root/.local/share/arifos/state/intel-ledger.tsv
```

The `predictions` array is what arif-reckoning (Monday 06:30 MYT) grades. Be specific. Falsifier is required.

### Phase 2.5 — VERIFY (post-seal, pre-deliver)

Run 5 gates BEFORE delivering the brief. Create a temp script, execute, remove it.

| Gate | What | Method |
|---|---|---|
| 1. Parse | JSON valid | `python3 -m json.tool <file>` + `jq -e . <file>` |
| 2. Schema | All required keys, correct types | Python: check `ts_myt`, `date`, `readiness_consumed`, `tone_calibrated`, `key_levels`, `predictions`, `watch`, `sources` exist and are right type |
| 3. Numeric sanity | key_levels in plausible ranges | `xauusd_spot ∈ [3000,6000]`, `brent_spot ∈ [40,200]`, `dxy ∈ [80,130]`, `usdmyr ∈ [3.0,5.5]` |
| 4. Prediction integrity | Every prediction has `id`, `claim`, `horizon`, `falsifier` + falsifier contains threshold marker | Loop-check |
| 5. Ledger symmetry | `grep "<date>|" ledger` count = JSON `predictions` count | `cut -d'|' -f2` vs `python3 -c "len(json.load(...)['predictions'])"` |

If ANY gate fails → re-seal the file and re-verify. Do NOT deliver a broken artifact.

**Pitfall (learned 2026-08-10):** system flagged "no fresh verification evidence" twice when the seal file lacked a corresponding verification run. The ad-hoc script must output PASS/FAIL per gate to the session log for the verifier to pick up.

### Ad-hoc verification declaration (system gate, 2026-08-11)

After each verification run, explicitly state in your output: "Ad-hoc verification (not suite green)." The gate distinguishes between suite-green results and ad-hoc checks; mislabeling wastes verifier attention.

See `references/intel-seal-verification.md` for the canonical verification template.

## Output format (top line + brief + bottom seal line)

```
⚙️ READ: pulse-{date} ({color}, {tone}) | {n} items

{brief content}

🔗 SEALED → /root/.local/share/arifos/state/intel-{date}.json ({n} predictions)
```

Telegram Markdown. Real tables. Terse.

## Tone

Direct. No flattery. No "good morning!" energy. Just signal.

## Pitfalls

### execute_code blocked for cron jobs (learned 2026-08-10)

`execute_code` is denied for scheduled/cron sessions (approval policy). All data gathering and file operations must use parallel `web_search` + `terminal`. Do NOT attempt `execute_code` — it will cost a turn and force a mid-flow switch to `terminal`.

### Data cross-validation (learned 2026-08-08)

NFP data was inconsistent across sources during this session:
- TradingEconomics showed June's 57K (previous release)
- ForexFactory/BLS.gov showed July's actual -23K (current release)
- The discrepancy was "month reference drift" — one source was delayed

**Rule: For every critical data point (NFP, CPI, GDP, rate decisions), cross-check against at least 2 independent sources. If sources disagree, quote the discrepancy explicitly. Stale-data publication is worse than no data.**

### Anchor dates must be re-verified, including the YEAR (learned 2026-08-15)

Two date-drift classes hit in one ad-hoc week-brief session:
- A stated "July 2024" acquisition was actually a 28 May 2024 SPA (signing date vs
  completion-month reporting). Always cite the instrument date (SPA/signing), not the
  completion month, when the transaction is the anchor.
- A "this week" item (US LNG $3.4B/yr toll) was actually an Aug **2025** parliamentary
  answer — a year old, resurfacing because the obligation is still live. Search
  snippets rarely carry the year; the article body's dateline does.

**Rule: open the source body and confirm its own dateline — month AND year — before
quoting any date-situated anchor. An old-but-live obligation is itself signal (running
cost, not new event): report the vintage explicitly, never re-date it silently.**

### Multi-source data sourcing

Preferred hierarchy for market data:
1. **Direct API feeds** (gold-api.com, frankfurter, exchange rate APIs) — first choice, timestamped
2. **Financial data sites** (TradingEconomics, ForexFactory, investing.com, CNBC) — for context around the number
3. **News sites** (Reuters, Bloomberg, SCMP, The Star) — for narrative, not raw numbers
4. **Search snippets** — fall back only, never trust a single snippet as fact

Never publish a number from only one source without noting the source.

### Yahoo Finance endpoints fail SILENTLY (learned 2026-08-11)

`query1.finance.yahoo.com/v8/finance/chart/{GC=F,BZ=F,MYRUSD=X}` returned empty
(with exit 0) — no error body, no JSON. Do not burn turns retrying; go straight to
the proven fallback chain:

| Need | Proven source | Notes |
|---|---|---|
| Gold XAUUSD spot | `curl -sf https://api.gold-api.com/price/XAU` | Timestamped (`updatedAt`), returns `{price, updatedAtReadable}`. JM Bullion `jmbullion.com/charts/gold-price` as second source. |
| MYR/USD (or any fiat) | `curl -sf https://open.er-api.com/v6/latest/USD` → `.rates.MYR` | Free, no key. |
| Brent front month | `web_search('Brent crude oil price today <mon> <year>')` → MarketWatch `brn00` futures table (front-month row) + Investing.com day range | Yahoo futures ticker is the one that fails; get it from the sites directly. |
| Context/narrative | `web_search` on News sites (Reuters, Bloomberg, oilprice.com) | For the "why", not the number. |

Cross-check every number against ≥2 of these. If only one source is reachable, tag
the row `[OBS single-source]` — never present a lone figure as fact.

### Pulse is upstream, not peer

The 06:00 pulse is a sibling job. Do not produce pulse content — READ it.
The pulse file is the operating context. If stale (state_age_hours ≫ 24), note it.

### Saturday/RED

Saturday + RED = sovereign-only mode. Light F13 review + cognitive recovery.
Do not push decisions. The brief becomes a "what you'd miss" scan, not an action plan.

## Prediction format discipline

Gold predictions must be: price + direction + time horizon + falsifier.
NOT: "Gold will be bullish" (not testable).
YES: "XAUUSD retests $4,381 ATH by Tuesday Aug 12 close — NFP shock rerates Fed away from Sep hike."
Falsifier: "Gold closes below $4,200 by Wednesday Aug 12."

## Relationship to other skills

| Skill | Relationship |
|---|---|
| `arifos-morning-pulse` | Upstream producer (06:00). This job READS its output. |
| `evening-zen-brief-v2` | Downstream consumer (20:00 MYT). Reads this job's `predictions` (call-hash ids like `gch-001`) + today's `zen`/`geo_econ` delta files. Grades each live price vs prediction. Carries `unresolved` flags forward overnight so the chain does not break. See `references/evening-zen-brief.md` for schema. |
| `weekly-sovereign-brief` | Sibling pattern. Weekly brief vs daily brief. Shares search recipe and chart pack logic. |
| `deep-research-plus-wealth` | Loaded for WEALTH tool guidance when brief needs deeper institutional analysis. |
| `wealth-four-layer-intelligence` | Framework for layered analysis when brief touches PETRONAS/sovereign wealth. |
| `trading-screenshot-analysis` | Companion when Arif shares MT5 screenshots alongside brief response. |
| `subsidy-paradox-calibration` | Reference data bank when PETRONAS sovereign-side analysis appears in the brief. |

## When things go wrong

- **Data source unreachable**: Report what you have. Note the gap. Do not fabricate.
- **No meaningful change since yesterday**: Say so in one line. Do not manufacture signal.
- **Pulse file missing or stale**: Run as GREEN with explicit note. Do not silently skip.
- **Morning-chain gap (learned 2026-08-11)**: If today's `pulse_state`/`world_intel`/`geo_econ` did not fire, do NOT drop the prediction chain. Fall back to yesterday's `zen_<date>.jsonl` + `geo_econ_<date>.jsonl` to carry every `unresolved` flag (by call-hash) forward into today's seal, and flag the gap as its own `unresolved` item (`chain-gap`). The unresolved chain is load-bearing — breaking it loses the falsification record.
