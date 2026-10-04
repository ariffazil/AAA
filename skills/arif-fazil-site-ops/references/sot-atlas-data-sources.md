
# SOT Atlas Live-Data Sources

Reference for arif-fazil.com world map / atlas features that consume live APIs.

---

## GDELT DOC 2

**Endpoint:** `https://api.gdeltproject.org/api/v2/doc/doc`

- Auth: none
- CORS: yes (for browser fetches)
- **Rate limit: 1 request per 5 seconds per IP.**
  Exceeding returns HTTP 200 with plaintext error message (not JSON).
- Params: `query`, `format=json`, `maxrecords`, `sort=datedesc`
- Response shape: `{ "articles": [ { "title", "url", "seendate", "domain", "tone": [...], "language", ... } ] }`
- `tone`: array of floats. Negative = conflict/bad news. Positive = economic/good.

**Working pattern (single combined query, 2026-08-06):**
```js
// OR-join all themes in one request, classify post-fetch by keyword on title.
const query = `(conflict|diplomacy|ceasefire|sanctions|...|economy|trade|energy|...|refugee|humanitarian|...) sourcelang:eng`;
const url = `${BASE}?query=${encodeURIComponent(query)}&format=json&maxrecords=60&sort=datedesc`;
// Handle non-JSON rate-limit response:
const text = await res.text();
if (!text.trim().startsWith('{')) return []; // rate-limited, retry on next tick
```

**Geocoding GDELT articles:** Use the `sourcecountry` field (string, e.g. "Syria") matched
against the `world-countries` dataset `name` or `cca3`. GDELT does NOT return lat/lng.

**Host-side timeout issue:** On arifos VPS (2026-08-06), GDELT requests from the server
often timeout. From real user browsers, the same query succeeds. Do NOT conclude the
API is down from `curl` alone — test in a browser if possible.

---

## World Bank API v2

**Endpoint:** `https://api.worldbank.org/v2/country/<CCA3>/indicator/<INDICATOR>?format=json&date=YYYY:YYYY&per_page=1`

- Auth: none, CORS: yes, generous rate limits.
- Response shape: `[ { page, pages, per_page }, [ { indicator, country, date, value, ... } ] ]`
- `value` may be null (no data for year).

**Indicators used in SOT Atlas dossier:**
| ID | Meaning |
|---|---|
| `NY.GDP.MKTP.CD` | GDP (current US$) |
| `NY.GDP.PCAP.CD` | GDP per capita (current US$) |
| `SP.POP.TOTL` | Population, total |
| `SP.DYN.LE00.IN` | Life expectancy at birth |
| `EN.ATM.CO2E.PC` | CO₂ emissions (metric tons per capita) |
| `IT.NET.USER.ZS` | Individuals using the Internet (% of population) |

**Caching strategy:** In-memory map keyed by CCA3, TTL 24h. Six requests per dossier
click; fetch all in parallel with `Promise.all`. No throttling needed.

---

## REST Countries

**Status (2026-08-06): v3.1 (free, no-auth) DEPRECATED.** All v3.1 endpoints now return
`{ success: false, data: null, errors: [{ message: "...please visit v5" }] }`.

**v5:** Requires an account + API key. Free tier exists but is not zero-auth.
**`?fields` param removed** — v5 uses a different response shape.

**Pivot (done):** Embedded `world-countries` npm package at build-time.
- Source: `cdn.jsdelivr.net/npm/world-countries@5.1.0/countries.json`
- Raw size: 1.4 MB (250 countries, includes genealogy, native names, currencies, borders).
- Trimmed for Atlas use: ~74 KB (cca3, cca2, name, capital, region, subregion, population,
  area, latlng, languages, currencies, flag, unMember, independent).

**Trim script:** `scripts/trim-countries-json.cjs` (under this skill's directory).

**Why embedded > live API:**
No auth needed, no CORS issues, no deprecation risk, no rate limits, instant load,
deterministic data. Better for ZEPHTIN (ΔS ≤ 0): one fewer live dependency =
fewer failure modes.

---

## TopoJSON World Geometry

**URL:** `https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json`

- CORS: yes (`Access-Control-Allow-Origin: *`)
- Size: 107 KB (110m resolution — good enough for full-world view, 50m for zoomed detail)
- Used by `react-simple-maps` (`<ComposableMap geography={GEO_URL}>`)
- Country names in the TopoJSON properties sometimes mismatch restcountries (e.g.
  "United States" vs "United States of America"). Handle with an alias map or flexible match.

---

## react-simple-maps

- `react-simple-maps@3.0.0` wraps d3-geo projections for React.
- `ComposableMap projection="geoEqualEarth"` — equal-area, good for SOT atlas (area-accurate).
- `<ZoomableGroup zoom={1} minZoom={1} maxZoom={6} center={[0, 20]}>` — allows pan/zoom.
- Geography lookup: `<Geography geography={geo}>` gives access to `geo.properties.name`
  (country name from the TopoJSON) and `geo.rsmKey` (stable React key).
- `<Marker coordinates={[lng, lat]}>` — places event markers from GDELT.

**Pitfall:** `react-simple-maps` is ~100 KB gzipped; keep it in a separate chunk via Vite
`manualChunks` to avoid loading it on pages without a map.
