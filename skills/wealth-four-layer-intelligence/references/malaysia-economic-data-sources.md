# Malaysia Economic Data Sources & Live-Probe Recipe

Worked 2026-08-08 answering "apa maksud semua ni" on the VITALS cockpit (sealed 5–6 Aug numbers)
and "deep research DOSM Putrajaya" on GDP/industry. The source map is durable; the numbers are a
dated worked example — re-verify before reuse.

## Live market quotes — fallback chain (2026-08-08)

1. Quick probes that FAILED / got flagged:
   - Stooq CSV (`https://stooq.com/q/l/?s=brent.cmd,xauusd,usdmyr&f=sd2t2ohlcv&h&e=csv`) — returned "page does not exist" (endpoint moved/dead).
   - Yahoo v8 chart API (`query1.finance.yahoo.com/v8/finance/chart/GC=F`) — `curl | python3` pipeline triggers the security scanner (pipe-to-interpreter). If used, fetch to a file first, parse in a separate step.
2. RELIABLE: `web_search` with the pattern `<asset> price today <full date>`:
   - "XAUUSD gold price today August 8 2026"
   - "Brent crude oil price today August 8 2026"
   - "USD MYR ringgit exchange rate today August 8 2026"
   - "DXY dollar index today <date>"
   TradingEconomics / Forbes / Investing.com snippets carry OBS-grade numbers WITH dates
   ("as of August 7, 2026"). Cross-source at least two hits; prefer sources that state the date.
3. Delta table vs a sealed dashboard: quote live value + source date per variable, compute the
   delta yourself, and label BOTH dates in every cell. Never mix sealed and live dates unlabeled.

## DOSM (Putrajaya) source map — Malaysia macro

| Data | URL pattern (dosm.gov.my/portal-main/release-content/) | Cadence |
|---|---|---|
| Advance GDP estimates | `advance-gross-domestic-product-gdp-estimates-q<NN><YYYY>` (e.g. -q22026) | ~17th of month after quarter-end; actual GDP ~1 month later |
| IPI (industrial production) | `index-of-industrial-production-<mmm><YYYY>` (e.g. -may2026) | monthly ~mid-month; open CSV: data.gov.my/data-catalogue/ipi |
| Monthly external trade | `monthly-external-trade-statistics-<mmm><YYYY>` | monthly ~5th–7th |
| Quick aggregates | TradingEconomics: tradingeconomics.com/malaysia/{industrial-production,currency,balance-of-trade,gdp-growth} | daily |

- Chief Statistician Dr. Mohd Uzir Mahidin posts same-day release summaries (12:00pm) on Facebook — useful for exact release date/wording.
- Advance estimates get revised in the actual release — label [OBS advance] vs [OBS actual].
- data.gov.my OpenDOSM (CC BY 4.0) is the machine-readable twin of the release tables.

## Worked example — Q2 2026 snapshot (advance est., released 17 Jul 2026)

- GDP +5.8% Q2 (Q1: 5.4%); QoQ +1.7% (reversing −4.4% Q1). H1 2026 +5.6% vs H1 2025 +4.5%.
- Services +5.4% (WRT, info & comm, transport/storage). Manufacturing +7.5% (E&E/optical; petroleum+chemical+rubber+plastic; non-metallic/basic/fabricated metal). Mining & quarrying +10.2% (natural-gas turnaround from −2.1%). Construction +6.6%. Agriculture −3.7% (oil palm, fishing).
- Trade Jun 2026: exports +45.4% YoY RM177.9B; imports +43.9% RM163.0B; surplus RM14.9B — 74th consecutive monthly surplus (since May 2020). H1 total trade RM1.8T (+22.4%).
- IPI May 2026: +8.4% YoY (strongest since Sep 2022); mining +19.8% (gas +37.4%), manufacturing +6.6%.

## Interpretation anchors (INT, 2026-08 read — re-verify)

- Binding constraint: global semiconductor/E&E cycle — E&E drives the bulk of export growth; a chip demand downturn (cf. 2023) hits Malaysia disproportionately.
- Agriculture contraction (sawit + ikan) hits rural/FELDA/nelayan — headline GDP masks a distribution gap ("GDP 5.8% — untuk siapa?").
- Gas, not oil, is now the mining driver for Malaysia (natural-gas surge) — aligns with PETRONAS CFFO sensitivity in the VITALS engine.
