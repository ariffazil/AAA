---
name: geo-earth-ground
description: |
  Earth surface navigation and geodata reasoning grounding.
  ACTIVATES when: any navigation, transit routing, geocoding, distance calculation, or place/location query.
  Forces epistemic discipline: OBS/DER/INT/SPEC labels on navigation data. Sources, freshness, and confidence required.
metadata: {"openclaw": {"emoji": "🧭"}, "version": "1.0.0"}
---

# geo-earth-ground — Navigation & Surface Geo Reasoning

## Trigger Conditions

- Any transit direction request (MRT, LRT, KTM, monorail, bus)
- Any geocoding query (address → coordinates or vice versa)
- Any distance or bearing calculation
- Any question involving roads, routes, navigation, public transport
- Words: "nearest", "how to get", "route", "distance to", "coordinates of"

## Epistemic Labels for Navigation

| Label | Meaning | Example |
|-------|---------|---------|
| `OBS` | Direct measurement | "Nominatim returns lat/lon for this address" |
| `DER` | Derived from data | "Haversine distance computed from coordinates" |
| `INT` | Interpolation/estimation | "Approximate fare based on zone" |
| `SPEC` | Speculation | "Route likely has light traffic at this hour" |

## Navigation Data Quality Checklist

Before answering any navigation query:

1. **Source known?** (Nominatim = OSM data, may be stale)
2. **Freshness?** (GTFS/station data may not reflect recent service changes)
3. **Confidence?** (High: official schedule. Medium: crowd-sourced. Low: estimated)
4. **Transfer risk?** (Minimum connection time at interchanges)
5. **Service status?** (No real-time data — always warn of possible disruption)

## KL Transit Specifics

| Line | Data Source | Freshness |
|------|-------------|-----------|
| MRT Kajang | Station graph (static) | ⚠️ Check for Phase 2 extensions |
| MRT Putrajaya | Partial (key stations) | ⚠️ Under construction segments |
| LRT Ampang/Kelana Jaya/Sri Petaling | Static | ⚠️ Check Prasarana announcements |
| KTM Komuter | Partial | ⚠️ May have schedule gaps |
| Monorail | Static | ⚠️ Limited coverage |

## Anti-Hallucination Rules

❌ "The MRT runs every 5 minutes" → Always say "~5 min" with caveat
❌ "This is the only route" → Always offer alternative routes
❌ "No construction on this line" → Always warn of possible disruptions
❌ "This address is exactly at these coordinates" → Nominatim precision varies

✅ Always cite data source (Nominatim, station graph, OSM)
✅ Always provide time range not single point estimate
✅ Always acknowledge real-time unknowns
✅ Always say "I don't know" rather than invent service disruption info
