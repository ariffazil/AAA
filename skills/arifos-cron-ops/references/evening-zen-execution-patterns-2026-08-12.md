# Evening-Zen-Brief Execution Patterns — 2026-08-12

Session log and durable patterns from evening-zen-brief-v2 run on 2026-08-12 (Wed, 20:00 MYT).

## What happened

1. **STEP 0 reads all returned empty** — the evening-zen prompt reads from JSONL paths (`pulse_state_YYYYMMDD.jsonl`, `world_intel_YYYYMMDD.jsonl`) that upstream jobs do NOT write to. Upstream jobs write to `/root/.local/share/arifos/state/` with different naming conventions.

2. **Fallback read succeeded** — session directory paths (`/usr/local/lib/hermes-agent/profiles/aaa-hermes/cron/output/<job_hash>/`) contained the session history markdown files, and `/root/.local/share/arifos/state/pulse-YYYY-MM-DD.json` and `intel-YYYY-MM-DD.json` contained the actual machine-readable state.

3. **Market data fetched via direct APIs** — Tavily returned HTTP 432. Used gold-api.com, Yahoo Finance v8, currency-api as fallbacks.

4. **Kernel probe OK** — arifOS :8088 healthy, drift=aligned, 7/7 organs alive.

5. **Previous day's zen file corrupted** — `zen_20260811.jsonl` has two JSON objects on one line (19:17 + 20:02 re-seals concatenated).

6. **New zen file written clean** — single JSON object, single line, validated.

## Correct read paths for evening-zen (canonical)

```bash
# Pulse state (today)
cat /root/.local/share/arifos/state/pulse-$(TZ='Asia/Kuala_Lumpur' date +%Y-%m-%d).json 2>/dev/null

# Intel state (today)
cat /root/.local/share/arifos/state/intel-$(TZ='Asia/Kuala_Lumpur' date +%Y-%m-%d).json 2>/dev/null

# Previous zen (yesterday, for continuity)
ls -t /usr/local/lib/hermes-agent/profiles/aaa-hermes/cron/output/zen_*.jsonl 2>/dev/null | head -2 | tail -1 | xargs cat 2>/dev/null | tail -1

# Alt: session history directories for raw output
ls -lt /usr/local/lib/hermes-agent/profiles/aaa-hermes/cron/output/*/  2>/dev/null | head -20
```

## Verification pattern for JSONL zen output

When verifying a `.jsonl` artifact (not code — no linter/test applies):

1. **Parse validity** — `json.loads()` on the content, assert no exception
2. **Schema parity** — keys match previous day's zen (ts, deltas, unresolved, tomorrow_first)
3. **Field presence** — ts has `+08:00`, unresolved is a list with id+claim per item, tomorrow_first is non-empty
4. **Plausibility** — market values in sane ranges (Gold $4300-4600, Brent $70-110, MYR 4.0-4.3)
5. **Chain continuity** — check that unresolved flag IDs from yesterday appear (carried forward) or are explicitly retired with reason

## Market data sources (when Tavily is down)

| Data | Source | URL pattern |
|---|---|---|
| XAU/USD | gold-api.com | `https://api.gold-api.com/price/XAU` → `.price` |
| Brent | Yahoo Finance | `https://query1.finance.yahoo.com/v8/finance/chart/BZ=F?interval=1d` → `.chart.result[0].meta.regularMarketPrice` |
| USD/MYR | currency-api | `https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/usd.json` → `.usd.myr` |

## Cron constraints for this job

- `execute_code` blocked — no user present
- Use `python3 -c "..."` with single quotes for inline JSON parsing
- `terminal()` foreground only — no `&`, no `| python3` (security scan)
- `write_file` always overwrites — correct for clean re-seals
