---
name: hat-yai-trip-planner
description: Full Hat Yai / Southern Thailand travel planning skill — halal, baby-friendly, with coordinates and Google Maps links. Implements arifOS Canonical Travel Protocol (3-Layer: Summary / Narrative / Data) via travel-intelligence-standard skill. Includes FATIGUE_MATH and SAFETY_CARD frameworks.
triggers:
  - hat yai
  - songkhla
  - sadao
  - thailand road trip
  - malaysia thailand border
  - plan trip
  - travel intelligence
  - trip protocol
---

# Hat Yai Trip Planner — arifOS Travel Intelligence

## Canonical Inheritance
**MUST use `travel-intelligence-standard` skill as the canonical output format.**
This skill provides: coordinates, halal spots, baby notes, and location-specific constraints.
The 3-layer structure (Summary / Narrative / Data) is defined in `travel-intelligence-standard`.

## Sources & Tools
- **Brave Search API** — `https://api.search.brave.com/res/v1/web/search?q={query}`
- **Google Maps Links** — `https://www.google.com/maps/search/?api=1&query={lat},{lon}`
- **GMaps Geocode API** — `https://maps.googleapis.com/maps/api/geocode/json?address={query}&key={API_KEY}`
  - API key: user-provided or from `/root/.hermes/.env`
  - NOTE: Key may be domain/IP restricted — if all geocode returns `NOT FOUND`, fall back to OSM or known coordinates
- **Nominatim OSM** — `https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=1` (rate-limited, 1 req/s)
- **TDAC Portal** — https://tdac.immigration.go.th/arrival-card/

## Halal Verification
- Thai Muslim restaurants = halal ✅ (no pork, no alcohol)
- ISDU Premium Restaurant Songkhla = confirmed halal
- Friendly Health Massage & Malika Beauty Massage = Muslim-friendly, separate rooms
- Always verify via Google Maps reviews when uncertain

## Key Verified Locations (May 2026) — Locked Place IDs

| Place | Place ID (Google) | Lat | Lon | Halal | Notes |
|-------|-------------------|-----|-----|-------|-------|
| Bukit Kayu Hitam Border | — | 6.7025 | 100.4242 | border | Immigration |
| R&R Halal Sadao | ChIJV8qjN-q5TDARYewG8HwVYrQ | ~6.7250 | ~100.4450 | ✅ | Lunch stop |
| Lamoon Villa | ChIJYQKhMfUpTTARXmkX3NQpeyA | 7.0128 | 100.5408 | accommodation | 7 Tienjawuthit Rd |
| Hat Yai Municipal Park | ChIJH2dajhQpTTARwYer740Ezc8 | 7.0031 | 100.4667 | public park | Cable car, 5AM-8PM |
| Lee Garden Night Bazaar | ChIJsTTVaOgpTTARxNF5S30xjPg | 7.0127 | 100.5394 | plausible | ~6PM-11PM |
| ISDU Premium Songkhla | ChIJW9c_hPgzTTARyYCgTcE8CwM | ~7.1864 | ~100.6005 | ✅ | 261/263 ถ.สงขลาพลาซ่า |
| Songkhla Zoo | ChIJbU7VQqcyTTARDwPrrYKMWXE | 7.1595 | 100.6190 | public | 8:30AM-4:30PM |
| Samila Beach | ChIJK3hSmW8zTTAReeb1_maBVGc | 7.2068 | 100.6078 | public beach | Merriman Monument |
| Wat Hat Yai Nai | ChIJbYpzmW4oTTARiDHJTTPsJbY | 7.0225 | 100.5500 | temple | Reclining Buddha, 7AM-6PM |
| Central Hatyai | ChIJCZ0eezMoTTARCFlwdoY1Z9w | 7.0089 | 100.5327 | mall | 10AM-9PM, baby supplies |
| Friendly Health Massage | ChIJ1fGExespTTARzfItRCtapi0 | ~7.0083 | ~100.5299 | ✅ | ~150-250 THB/hr |
| Malika Beauty Massage | ChIJ...(near P06) | ~7.0111 | ~100.5411 | ✅ | ~200-350 THB/hr |

## Day 2 Critical Constraints (F1 — Read Before Departure)

**Fatigue Math:** 78 min driving + 2-3 hrs zoo + lunch + massage = 6-9 hrs total active time
**With Baby Naufal (8 months): HIGH fatigue load — DO NOT execute as single block**

Option A (Recommended): Split group — Azwa+Fizie zoo | Arif+Naazira+baby at AC mall
Option B: Zoo 8:30-11:30AM → beach/AC break → return 3PM → massage 4PM

## Route Intelligence — Locked Legs (Machine-Verified)

| Leg | From → To | km | min |
|-----|-----------|---|-----|
| L01 | Border → R&R Sadao | 3.0 km | 5 min |
| L02 | R&R Sadao → Lamoon Villa | 42.2 km | 49 min |
| L03 | Lamoon Villa → Municipal Park | 10.7 km | 23 min |
| L04 | Municipal Park → Night Market | 10.7 km | 22 min |
| L05 | Lamoon Villa → ISDU Songkhla | 25.3 km | 33 min |
| L06 | ISDU → Songkhla Zoo | 4.1 km | 7 min |
| L07 | Zoo → Lamoon Villa | 27.9 km | 33 min |
| L08 | Lamoon Villa → Friendly Massage | 1.4 km | 3 min |
| L09 | Massage → Ban Phang Nai Dinner | 0.6 km | 2 min |
| L10 | Lamoon Villa → Wat Hat Yai Nai | 4.2 km | 6 min |
| L11 | Wat → Malika Massage | 3.4 km | 6 min |
| L12 | Malika → Central Hatyai | 1.2 km | 3 min |
| L13 | Central Hatyai → Border | 42.6 km | 54 min |

## Day Structure (3-Layer Output Template)

```
DAY 1 (Friday May 9 — Arrival): Border → Sadao lunch → check-in → Municipal Park → night market
DAY 2 (Saturday May 10 — Songkhla): ⚠️ HIGH FATIGUE — split group recommended
DAY 3 (Sunday May 11 — Retreat): Wat → massage → shopping → return
```

## Safety IDs — Locked

- **Nearest clinic:** Health Link International ~1.5 km from Lamoon Villa, 4.9 stars
- **Baby supplies:** Central Hatyai supermarket, ground floor
- **Emergency pharmacy:** B&T Pharmacy 5 stars, 1.8 km (Central Hatyai G-05)
- **Abort: Day 1 rain:** Skip Municipal Park cable car → go direct to Lee Garden Night Market

## Baby-Friendly Notes
- Stroller access: Municipal Park ✅, Samila Beach ✅, Central Festival ✅
- Baby supplies: Central Festival supermarket
- Nap time: Schedule 18:00-20:00 Day 1
- Diapers/milk: Buy at Central Festival Hat Yai

## Pitstop Categories
- ☕ Coffee/Tea: Halal cafes in Sadao area
- 🍰 Dessert: Thai Muslim desserts (avoid gelatin-based unless verified)
- 📸 Photo spots: Hat Yai Municipal Park, Samila Beach, Sadao town, temples
- ⛽ Petrol: 7-Eleven or PETRONAS near highway exits
- 🛒 Convenience: 7-Eleven (abundant in Thailand)

## Budget Template
```
Food (3 days × 4 pax):    3,200-5,000 THB
Massage × 2 sessions:     1,200-2,400 THB
Petrol (round trip):         250-350 THB
Toll Malaysia:                 60-80 MYR
Border vehicle ins:           100-300 THB
Songkhla Zoo (family):       400-600 THB
Misc/buffer:                  1,000 THB
────────────────────────────────────
TOTAL:               ~16,000-27,000 THB
                     (~RM500-830/pax for 4 adults)
```

## Coordinate Acquisition Workflow
1. Try Google Geocode API with key
2. **If ALL results return `NOT FOUND`** → key is domain/IP restricted (common for VPS-based keys). Skip geocode entirely, use known coordinates + OSM fallback
3. If geocode works, verify a few samples manually
4. Compile all into Google Maps search URLs: `https://www.google.com/maps/search/?api=1&query={lat},{lon}`

## HTML Travel Guide Template
Use dark-mode mobile-first HTML. Key design elements:
- Dark background (#0f1923), light text (#e8eaed)
- Color-coded days: Day1=#1a3a2a (green), Day2=#1a2a3a (blue), Day3=#2a1a3a (purple)
- HALAL badge: green pill (#1b5e20 bg)
- Each location: time emoji | title | halal badge | meta | Google Maps tap-link
- Budget grid with 2-column layout
- Baby tips in highlighted box
- Responsive: works on phone while driving

## VPS Static File Deployment
File: `/root/arif-sites/output/{trip-name}.html`

1. **Write HTML** to `/root/arif-sites/output/{filename}.html`
2. **rsync to VPS:**
   ```bash
   rsync -av /root/arif-sites/output/{filename}.html root@72.62.71.199:/var/www/html/
   ```
3. **Verify live:** `curl -s "https://arif-fazil.com/{filename}.html"` → expect HTTP 200
4. **Share link:** `https://arif-fazil.com/{filename}.html`

> VPS serves `/var/www/html/` as static root under `arif-fazil.com`. No Caddyfile change needed.

## PDF Generation (with Hyperlinks!)
WeasyPrint v68+ supports internal AND external hyperlinks in PDF. To include clickable Google Maps links in the PDF:

1. Add a **MAP LINKS APPENDIX section** at the bottom of the HTML with full URLs as `<a href="...">` tags — WeasyPrint renders these as clickable links in the PDF
2. Generate PDF:
   ```bash
   /root/.hermes/venv/bin/weasyprint /root/arif-sites/output/{name}.html /root/arif-sites/output/{name}.pdf
   ```
   WeasyPrint runs from Hermes venv, not system-wide.
3. **Send PDF via Telegram** — `send_message(target="telegram:chatid", message="MEDIA:/path/to/file.pdf")`
   - Telegram renders PDF inline for the recipient
   - Clickable links are preserved when opened in Telegram's PDF viewer

**WeasyPrint quirks discovered:**
- `min-height: 100vh` on body causes "invalid value" warning — use `min-height: 100%` instead
- All URLs in HTML become clickable links in PDF output
- HTML must be well-formed or WeasyPrint may silently skip pages
- Use `--inpsect` flag if pages are missing: `weasyprint -D input.html output.pdf`
