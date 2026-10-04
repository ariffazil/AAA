# SOT Atlas — Data Sources

Verified 2026-08-06.

## GDELT DOC 2

- Endpoint: `https://api.gdeltproject.org/api/v2/doc/doc`
- Rate limit: 1 request per 5 seconds
- From server host (127.0.0.1) it times out; from a real browser (different IP) it works after the stagger.
- Strategy: single combined query covering all 3 axes, post-classify articles by keyword:
  - geo: `\b(conflict|diplomacy|ceasefire|sanction|military|NATO|border|war|troops|missile|attack)\b`
  - econ: `\b(economy|trade|energy|oil|inflation|tariff|recession|GDP|market|stock|export|import)\b`
  - soc: `\b(refugee|humanitarian|migration|disease|health|famine|earthquake|disaster|flood|drought)\b`
- When multiple axis keywords match, use GDELT `tone` array: mean < -3 → geo; > 2 → econ; else → soc.
- Fallback: when GDELT rate-limits, app shows "QUERYING GDELT…" and retries at 5-min refresh.

## World Bank API

- Endpoint: `https://api.worldbank.org/v2`
- No auth required.
- Indicators used per country dossier:
  - `NY.GDP.MKTP.CD` (GDP current US$)
  - `NY.GDP.PCAP.CD` (GDP per capita)
  - `SP.POP.TOTL` (Population)
  - `SP.DYN.LE00.IN` (Life expectancy)
  - `EN.ATM.CO2E.PC` (CO₂ per capita)
  - `IT.NET.USER.ZS` (Internet users %)
- Query pattern: `?format=json&per_page=1&date=2022:2024` (latest available).

## Country metadata

- Source: `mledoze/world-countries@5.1.0` (npm/jsdelivr)
- REST Countries v3.1 deprecated → v5 requires API key → pivoted to embedded dataset.
- Trimmed at build-time (1.4 MB → 74 KB) by `scripts/prepare-data.cjs`.
- Fields kept: `cca3, cca2, name, official, capital, region, subregion, population, area, latlng, languages, currencies, flag, unMember, independent`.

## Map geometry

- Source: `world-atlas@2/countries-110m.json` (107 KB, CDN)
- Used via `react-simple-maps` `<ComposableMap>` + `<Geographies>`.
- Projection: `geoEqualEarth`, scale 165, center [0, 20], zoom 1–6.

## SOT Tension Index math (per axis, 0–100)

- `negTone = max(0, -mean(GDELT tone))`
- `volume = log10(articles.count + 1) * 10`
- `spread = min(20, unique_domains * 1.5)`
- `complexity = mean(min(60, title.length)) / 2`
- `axisScore = negTone * 1.2 + volume + spread + complexity`, clamped [0,100]
- Aggregate: harmonic mean × 1.5 (F1 AMANAH: lowest axis dominates; catastrophic pull).
