# Malaysian Broker Research Scraping Patterns

Proven 2026-08-09 on UOBKH O&G sector intelligence gathering. Class-level reference for any broker research / analyst call / sector intelligence task.

## Source Hierarchy (in order of reliability)

| Source | URL Pattern | What You Get | Reliability |
|--------|------------|--------------|-------------|
| **UOBKH Research Portal** | `equitiesresearch.uobkayhian.com` | Full PDFs, sector updates, company notes | HIGH (direct from broker) |
| **The Edge Malaysia** | `theedgemalaysia.com/node/XXXXX` | Summaries of research notes with analyst quotes | HIGH (journalistic, cites source) |
| **The Star Business** | `thestar.com.my/business/business-news/YYYY/MM/DD/` | Research house summaries, broker calls | HIGH |
| **i3investor** | `klse.i3investor.com/web/blog/detail/` | Aggregated analyst calls, price targets, StockTipRatings | MEDIUM-HIGH (aggregated) |
| **KLCIScreener** | `klsescreener.com/v2/discussion` | Retail sentiment, technical analysis (Chinese MBOW system) | MEDIUM (retail, not institutional) |
| **LinkedIn** | `linkedin.com/company/uobkayhian` | Trading monitors, market data snapshots | MEDIUM (social, partial) |
| **Instagram** | `instagram.com/p/` | Event posters, seminar announcements | LOW (marketing, not research) |
| **Telegram** | `t.me/s/UOBKayHianMalaysia` | Daily market monitors, trading ideas | MEDIUM (timely but partial) |

## Search Query Patterns

### Finding latest analyst calls
```
"UOB Kay Hian" analyst [stock name] target price 2026
site:i3investor.com "UOB Kay Hian" [stock name] [action]
site:theedgemalaysia.com "UOBKH" OR "UOB Kay Hian" [topic]
```

### Finding sector research
```
"UOB Kay Hian" oil gas sector Malaysia 2026
UOBKH sector update Malaysia [sector] 2026
[house name] Malaysia [sector] outlook 2H26
```

### Finding comparative house views
```
Malaysia KLCI target 2026 [house name]
Malaysia oil gas sector stance [house1] vs [house2]
broker comparison Malaysia [sector] overweight
```

## Multi-Source Triangulation

When a single analyst call appears in multiple sources:
1. **Primary source** = broker's own portal (equitiesresearch.uobkayhian.com) — most authoritative
2. **Secondary** = The Edge / The Star — journalistic, adds context and analyst quotes
3. **Tertiary** = i3investor / StockTipRatings — aggregated, may add consensus data
4. **Social** = LinkedIn / Instagram / Telegram — timely but partial, good for event/seminar info

**Rule:** Cross-verify key claims (TP, call, stance) across at least 2 sources before publishing as OBS.

## Synthesis Template

When compiling broker research into intelligence:

### Structure
1. **Sector Stance** — the house's overall rating + key rationale
2. **Stock-Level Calls** — individual names with call/TP/upside
3. **Macro Frame** — how the sector view fits into the house's broader market outlook
4. **Key Risk** — the one risk the house keeps flagging
5. **Comparative** — how this house differs from others on the same sector

### Epistemic Tagging
- Direct quote from research note → [OBS]
- Analyst TP/call from verified source → [OBS]
- Sector stance from research note → [OBS]
- Implied thesis from analyst language → [INT]
- Oil price forecast / earnings estimate → [DER]
- Comparative ranking across houses → [DER]

## Common Pitfalls

- **UOBKH research portal requires authentication** — full PDFs not always accessible via web_extract. Use The Edge / The Star summaries as proxy.
- **i3investor blog index may be stale** — UOBKH's official blog on i3investor shows "Latest Post: Nov 2022" but they publish via CEO Morning Brief and StockTipRatings aggregators.
- **Instagram posts are marketing, not research** — event posters (seminars, webinars) are useful for timing but not for investment thesis.
- **Telegram channel is timely but fragmented** — daily market monitors appear as individual messages, not consolidated reports.
- **KLCIScreener Chinese-language analysis (MBOW system)** is technically sophisticated but retail-oriented — institutional conviction levels differ.

## Worked Example: UOBKH O&G (2026-08-09)

1. Searched 4 queries in parallel → found Edge article (Jul 9), i3investor Bursa downgrade (Jul 31), Star O&G article (Jun 11), Gas Malaysia update (Jul 28)
2. Extracted 5 URLs in parallel → got full text from Edge, i3investor, The Star
3. Cross-verified: MISC BUY RM9.50 appears in Star + i3investor. Dialog BUY RM2.95 in Star. Armada upgrade on equitiesresearch portal listing. Gas Malaysia HOLD RM6 in Star Jul 28.
4. Synthesized: sector stance (MW) + 5 stock calls + macro frame + risk matrix → structured brief
5. Generated 8-chart PDF pack → WeasyPrint → 12-page report

Total sources scraped: 8 | Total extractions: 5 parallel batches | Cross-verified claims: 12
