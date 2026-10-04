
# Free Data Sources — API Quirks & Reference

## GDELT DOC 2

### Query syntax
- Boolean operators: `OR`, `AND`, `NOT` (no explicit boolean grouping required, but parenthesise for clarity)
- `sourcelang:eng` filter (or `sourcelang:ara`, etc.)
- `format=json` (not `csv`)
- `maxrecords=60` (reasonable for a dashboard; higher causes 429s faster)
- `sort=datedesc`
- Full query example: `((conflict OR diplomacy) OR (economy OR trade) OR (refugee OR humanitarian)) sourcelang:eng`

### Rate-limit behavior
- From datacenter IPs: HTTP 429 or HTTP 000 (timeout after ~10s). Retry after 6s.
- From user browsers (residential IPs): Usually succeeds. 5s spacing recommended.
- From sandboxed headless browsers: Shares datacenter IP → 429s are normal and do NOT prove the app is broken.
- Rate-limit message (when HTTP 200 but non-JSON): `"Please limit requests to one every 5 seconds..."` — always check `text.trim().startsWith('{')` before parsing.

### Article fields
- `title` (string)
- `url` (string)
- `seendate` (string, format: `YYYYMMDDTHHMMSSZ`)
- `domain` (string, e.g. `bbc.co.uk`)
- `tone` (number array, e.g. `[2.5, -1.2]`; negative = conflict, positive = economic)
- `sourcecountry` (string, e.g. `USA`; NOT always present, sometimes just `actor1country`)
- `socialimage` (string URL, sometimes present)
- No lat/lng fields — must geocode from sourcecountry.

### Post-fetch classification regex
```ts
const AXIS_KEYWORDS = {
  geo: /\b(conflict|diplomacy|ceasefire|sanction|military|NATO|border|war|troops|missile|attack)\b/i,
  econ: /\b(economy|trade|energy|oil|inflation|tariff|recession|GDP|market|stock|export|import)\b/i,
  soc: /\b(refugee|humanitarian|migration|disease|health|famine|earthquake|disaster|flood|drought)\b/i,
};
// Multi-match disambiguation: if 2+ axes match, use tone mean (tone < -3 → geo, > 2 → econ, else soc)
```

## World Bank Indicators

### Endpoint pattern
`https://api.worldbank.org/v2/country/{ISO2}/indicator/{CODE}?format=json&per_page=1&date=2022:2024`

### Common indicator codes
| Code | Meaning |
|---|---|
| `NY.GDP.MKTP.CD` | GDP, current US$ |
| `NY.GDP.PCAP.CD` | GDP per capita, current US$ |
| `SP.POP.TOTL` | Population, total |
| `SP.DYN.LE00.IN` | Life expectancy at birth, total |
| `EN.ATM.CO2E.PC` | CO₂ emissions, metric tons per capita |
| `IT.NET.USER.ZS` | Individuals using the Internet (% of population) |

### Response shape
```json
[
  { "page": 1, "pages": 1, "per_page": 50, "total": 1, "sourceid": "2", "lastupdated": "..." },
  [
    {
      "indicator": { "id": "NY.GDP.MKTP.CD", "value": "GDP (current US$)" },
      "country": { "id": "MY", "value": "Malaysia" },
      "countryiso3code": "MYS",
      "date": "2022",
      "value": 407830525989.553,
      "unit": "", "obs_status": "", "decimal": 0
    }
  ]
]
```
- Data is `json[1][0]` for most recent.
- `value` is null if no data exists → check for null before displaying.

### Common issues
- ISO2 only, not ISO3 — use `c.country.id` (e.g. `MY` not `MYS`).
- Missing data returns `null` in `value` → graceful `-` display.

## REST Countries
- **v3.1 is DEPRECATED (as of mid-2025)**: all endpoints return `{"success":false,"data":null,"errors":[{"message":"This API version has been deprecated..."}]}`.
- **v5 requires API key**: `Authorization: Bearer <key>`. No free tier.
- **No free public fallback exists** (Geonames requires `username=`, Apilayer returns 404).
- **Solution: embed the data.** Use `mledoze/world-countries@5.1.0` (npm, jsDelivr). Trim at build-time.
- **Alternative: World Bank Country API** (preferred for the tier use case — see next section).

## World Bank Country Classification (income tier + lending type)

### Endpoint (THE "WB Tire" artifact)
```
https://api.worldbank.org/v2/country?format=json&per_page=300
```
Returns 295 countries/territories. Each has:
- `id` → ISO3 (e.g. `MYS`)
- `iso2Code` → ISO2 (e.g. `MY`)
- `name` → country name
- `incomeLevel.id` → tier code: `HIC` (high) | `UMC` (upper middle) | `LMC` (lower middle) | `LIC` (low)
- `incomeLevel.value` → "High income", "Upper middle income", etc.
- `lendingType.id` → `IBRD` | `IDA` | `Blend` | `Not classified`
- `latitude` / `longitude` → capital city coords (usable as centroids for map markers)
- `capitalCity` → capital name
- `region.value` → region name

### Build-time fetch recipe
```bash
# One-shot fetch → write to src/data/wb_countries.json
curl -sf "https://api.worldbank.org/v2/country?format=json&per_page=300" -o /tmp/wb.json

# Python to filter + flatten (skip entries with no lat/lon or no income tier)
python3 -c "
import json
raw = json.load(open('/tmp/wb.json'))[1]
out = [
  {'iso3': c['id'], 'iso2': c['iso2Code'], 'name': c['name'], 'capital': c.get('capitalCity',''),
   'region': c['region']['value'].strip(), 'incomeLevel': c['incomeLevel']['value'],
   'incomeTier': c['incomeLevel']['id'], 'lendingType': c['lendingType']['value'],
   'lat': round(float(c['latitude']),3), 'lon': round(float(c['longitude']),3)}
  for c in raw
  if c['incomeLevel']['id'] not in ('NA','INX','') and c.get('latitude') and c.get('longitude')
]
print(len(out), 'countries')
json.dump(out, open('src/data/wb_countries.json','w'), indent=2)
"
# Produces: 211 countries, 4 tiers (HIC/UMC/LMC/LIC), 4 lending types (IBRD/IDA/Blend/Not classified)
```

### Tier-to-color mapping (for choropleth / map overlay)
```ts
const TIER_COLORS: Record<string, string> = {
  HIC: '#4ea77d',  // green
  UMC: '#d4a017',  // amber (matches arifos palette)
  LMC: '#d47a17',  // orange
  LIC: '#e0483e',  // red (matches delta axis)
};
// No tier → '#5c574a' (muted grey — matches text-faint)
```

### How the tier data integrates with the atlas
1. `COUNTRIES` array (the country registry) is the JSON itself — no separate stub needed.
2. Geography fill in `react-simple-maps`: check `findCountry(name)?.incomeTier` and use `tierColor(tier)`.
3. Dossier drawer: render the income tier badge (color-coded border, WB label, lending type).
4. Map mode toggle: `viewMode: 'axes' | 'tier'` — "axes" shows GDELT news markers, "tier" shows the choropleth.
5. Legend in tier mode: list HIC/UMC/LMC/LIC with counts and color dots.

## Trim script sketch (CJS prebuild)
```cjs
// Fetch world-countries once → cache → write trimmed src/data/countries-min.json
// Keep: cca3, cca2, name.common, name.official, capital, region, subregion,
//        population, area, latlng, languages (values only), currencies (keys only),
//        flag emoji, unMember, independent
// Raw 1.4 MB → trimmed ~70 KB (5.3%)
```

## TopoJSON
- `https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json` (107 KB, CORS ✅)
- `properties.name` = country name (NOT cca3 — varies; some use "United States of America" not "United States")
- `properties.id` = ISO-3166-1 numeric code
- react-simple-maps wraps this directly: `<Geographies geography={url}>`

## SOT Index Computation (deterministic, observable)
Per axis 0–100:
- `toneMean`: average of `article.tone` array, `mean = sum / len` (null if array empty)
- `volume`: `Math.log10(articleCount + 1) * 10`
- `spread`: `Math.min(20, uniqueDomains * 1.5)`
- `complexity`: `Math.min(60, avgTitleLength) / 2`
- `raw = negTone * 1.2 + volume + spread + complexity` → clamped 0–100

Aggregate (3 axes):
- Harmonic mean × 1.5, each axis floored at 0.5
- `harmonic = 3 / (1/a + 1/b + 1/c)`, clamped 0–100
- **Design intent: lowest axis dominates** (catastrophic single-axis signal pulls the SOT down; a calm single axis doesn't hide a hot one elsewhere).
