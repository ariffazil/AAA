---
name: temporal-awareness
description: "Temporal anchor for every agent session — run `now` before answering any time/date/day question. Provides UTC + MYT + day + ISO week + AED FQ + all 8 organ health. One command, always fresh, never cached. The single time SOT for the federation."
tags: [time, now, temporal, anchor, federation-health]
version: 1.0.0
triggers:
  - User asks "what time", "what day", "what date", "pukul berapa", "hari apa"
  - Any time-related question in any language
  - Session start (boot anchor)
  - Before SEAL or timestamp-sensitive operations
  - Cron job timestamp verification
related_skills:
  - arifos-federation-ops
  - arifos-machine-wellness
---

# Temporal Awareness

## The Rule

> **Every AAA warga agent answering time-related questions MUST first run `now`.**
> **Never answer "what time/day/date" without `now` first.**

This is NOT optional. Time perception is a first-class cognitive function (000 OBSERVER).

## Commands

```bash
# Full anchor — timestamp + federation health + FQ + vault status
now

# One-liner — for context windows, cron prompts, carry_forward
now --brief

# Machine-readable — for JSON pipelines
now --json
```

### `now` (full output)

```
⏰  NOW        2026-08-09 19:23:03 MYT (Sunday)
             UTC: 2026-08-09T11:23:03Z
             Unix: 1786274583  · ISO week 32  · day 221
             ☀️  active hours

👑  SOVEREIGN  Arif (F13 SOVEREIGN)

🌐  FEDERATION
             ✅arifOS ✅A-FORGE ✅A-FORGE-MCP ✅arifflow ✅AAA ✅GEOX ✅WEALTH ✅WELL
             AED FQ: 🟢 0.0 (threshold 5.0)

📦  VAULT999    2952 records · 0 broken · append-only=✅
🪪  AAA         2f2bd195 · 0 dirty files

⏭   NEXT CRON  (none)
             at (unknown) (None min from now)

🧠  SESSION CARRY
             last: SEAL-22c6011cabe54c9d
```

### `now --brief` (one-liner)

```
now=2026-08-09 19:23:04 MYT (Sunday) utc=2026-08-09T11:23:04Z dow=Sunday iso_wk=32 aed_fq=0.0
```

Use this in cron prompts, session carry_forward, and anywhere you need a fast timestamp without federation health.

## What `now` provides

| Field | Source | Why |
|-------|--------|-----|
| MYT timestamp | system clock | Local time for Arif (UTC+8) |
| UTC timestamp | system clock | Universal reference |
| Unix epoch | system clock | Machine-readable |
| ISO week | computed | Week-boundary awareness |
| Day of year | computed | Seasonal context |
| Day/night indicator | sunset calculation | Quiet-hours awareness (23:00–07:00 MYT) |
| Federation health | live port probes | Ground truth for organ status |
| AED FQ | journalctl AED service | Flow Quotient — operational readiness |
| VAULT999 status | filesystem | Receipt count + integrity |
| AAA repo state | git status | Dirty files detection |
| Next cron | jobs.json | Upcoming scheduled work |
| Session carry | carry_forward.json | Last sealed session |

## When to use

| Scenario | Which form |
|----------|------------|
| User asks "what time/day" | `now` (full) |
| Cron prompt timestamp | `now --brief` |
| JSON pipeline | `now --json` |
| Session boot anchor | `now` (full) |
| Pre-SEAL timestamp | `now` (full) |
| Quiet-hours check | `now` (full) — check ☀️/🌙 indicator |
| FQ gate decision | `now` (full) — check AED FQ value |

## Quiet Hours Doctrine

- **Quiet hours:** 23:00–07:00 MYT
- **Rule:** No Telegram pings during quiet hours (except VOID/breach/data loss/public surface down)
- **Budget:** ≤3 immediate pings/day; overflow → evening-zen-brief (22:30 MYT)
- **Check:** `now` output shows ☀️ (active) or 🌙 (quiet) based on sunset/sunrise in MYT

## Pitfalls

- **`now --brief` does NOT include federation health.** Use `now` (full) when organ status matters.
- **AED FQ may show `?`** if AED service hasn't logged recently — this is NOT an error, it means FQ is unmeasured.
- **`now` reads live state.** Every call probes federation ports. Do NOT cache `now` output for decision-making — re-run when freshness matters.
- **Timezone is always MYT (UTC+8).** If the user asks for a different timezone, use `date` with TZ or the `maps` skill timezone feature.
- **The `now` binary** lives at `/usr/local/bin/now`. The brief script is at `/root/HERMES/scripts/zen/now_brief.py`.
- **Stale reply-chain timestamps override correct time.** Telegram UI injects `[Replying to:]` blocks from prior sessions carrying old timestamps. If a reply chain says "4:48 pagi" but `now` says 12:48 PM — trust `now`, silently ignore the reply chain. Never echo a timestamp you didn't compute yourself. (Discovered 2026-08-10.)

## Integration with other skills

- **arifos-machine-wellness:** `now` + machine wellness = full operational picture
- **arifos-federation-ops:** `now` gives live organ health; federation-ops can drill into any ❌ organ
- **arifos-morning-pulse:** `now` provides the temporal anchor for the daily 06:00 MYT pulse
- **cron-jobs:** Every cron prompt should start with `now --brief` for temporal grounding
