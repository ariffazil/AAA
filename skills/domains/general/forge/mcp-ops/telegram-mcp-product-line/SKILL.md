---
name: telegram-mcp-product-line
description: "Use when building Telegram-native products on MCP backends."
author: Hermes Agent
license: MIT
version: 1.0.0
metadata:
  hermes:
    tags: [telegram, product, mcp, arifos, bot]
    related_skills: [trading-signal-chart, nasilemak-engine, syedos]
tags: [telegram, product, mcp, arifos, bot, command-surface]
triggers:
  - "real product"
  - "telegram product"
  - "one apps"
  - "satu apps"
  - "mini app"
  - "!gold !nasilemak !body"
  - "MCP backend product"
  - "interface is telegram"
---

# Telegram-MCP Product Line

## When to Use

Use when Arif asks to turn proposals/ideas into real products, or mentions
Telegram as the interface, MCP organs as the backend, or any of the product
lanes (!gold, !nasilemak, !body). This is the architecture for shipping
federation capabilities as Telegram command surfaces.

Arif's product thesis (2026-08-31): *manusia nak SATU apps* — Telegram. "Future is AI agent yang pakai apps tu." So a product = a Telegram command surface on top of MCP organs that ALREADY exist. No new apps unless explicitly asked. No new bot per lane — ONE bot, multiple command lanes.

## The One Rule

Interface = Telegram (existing bot / group). Backend = existing MCP organs. Product = the wiring + delivery pattern, NOT new infrastructure.

## Lane Map (as of 2026-08-31)

| Lane | Command | Backend | Status |
|---|---|---|---|
| Trading / Emas | `!gold` | gold API :3456 + WEALTH :18082 | LIVE — chart pipeline proven |
| Business / Nasi lemak | `!nasilemak` | nasilemak data (optimization_v2.json) | LIVE — 26 days tracked |
| Body / Physique | `!body` | WELL :18083 | BACKEND READY — biometrics MOCK, needs Google Fit OAuth or biometric_inject.sh |

## Delivery Pattern (per product)

1. **Visual FIRST** — chart/image before text ("aku malas nak baca"). MEDIA: PNG (+ PDF for printable), then ≤ 8 lines text.
2. **Real numbers, not narrative** — cite the live source; compute from data files, don't invent.
3. **Honest status** — if data is MOCK/stale/absent, say so plainly (WELL honesty banner: "do not treat as body truth"). Never fake a live score.
4. **Close with ONE decision** — offer the next concrete step (wire command layer / build mini app), not a menu of options.

## Recipes (pointers)

- **Gold live chart:** `trading-signal-chart` skill → "Live Feed Wiring" section (curl :3456 endpoints, map live values into gold_live_weekly_pdf.py, render with bare python3).
- **Nasi lemak snapshot:** `/root/sado/data/optimization_v2.json` — variants + variant_mix + daily_breakdown (26 days). Sum daily_breakdown for totals. NOTE: skill-listed `engine_v4.json` may be ABSENT; optimization_v2.json is the live file.
- **WELL status:** `well_get_triadic_snapshot` + `well_observe_machine` MCP tools. Check snapshot freshness — cron writer can lag (observed 10+ days stale).

## Pitfalls

- **WELL triadic snapshot can be days stale** — check `snapshot_age_seconds` before citing; the hermetic cron writer may not be running.
- **Do NOT build a new bot per product.** Arif's explicit "satu apps" rule. Add command lanes to the existing bot.
- **Data files drift.** Skills list file paths that may not exist (engine_v4.json). Always list the data dir (search_files target='files') and use the newest optimization/parsed JSON.
- **WELL biometrics are MOCK** — honesty_banner is mandatory context; never present WELL score as real body truth.

## References

- `references/build-log-2026-08-31.md` — first real-product pass: endpoints, live values, numbers, decisions
