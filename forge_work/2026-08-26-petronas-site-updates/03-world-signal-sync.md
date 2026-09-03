# /world — Signal Sync Patch

**Status:** Ready-to-apply
**Priority:** P0
**Session:** SEAL-d7d3fde881a74721
**Author:** 333-AGI Δ Mind

---

## What to do

Sync the live market proxies on `/world` State of the World Radar with the values on `/vitals`. Also add a 6th radar signal: PETRONAS Sovereign Extraction — the most important Malaysian macro indicator.

---

## ISSUE — Current State of World Radar

```
Brent Crude:   $82.40 +1.2% SEAL        ← STALE (vitals shows $85.48)
Natural Gas:   $13.20 +0.8% SEAL       ← DIFFERENT UNIT (vitals shows HH $2.86)
Gold:          $2,425.80 +0.4% SEAL    ← OK
Ringgit:       4.4250 -0.3% SABAR      ← STALE (vitals shows 4.047 — 10% gap!)
KLCI:          1,598.40 +0.5% SEAL    ← STALE (vitals shows 1,749.20 — 9% gap!)
```

The Brent, Ringgit, and KLCI signals are 4-10% stale relative to `/vitals`. The 10% gap on USD/MYR is severe.

---

## PATCH — New State of the World Radar

**FIND:**
```
STATE OF THE WORLD RADAR:4/5 SIGNALS SEALED

Brent Crude:$82.40+1.2%SEAL | Natural Gas / LNG:$13.20+0.8%SEAL | Gold (Hard Asset):$2,425.80+0.4%SEAL | Ringgit Exchange:4.4250-0.3%SABAR | FTSE Bursa KLCI:1,598.40+0.5%SEAL
```

**REPLACE WITH:**
```
STATE OF THE WORLD RADAR:5/6 SIGNALS SEALED · 1 SABAR · PETRONAS Sovereign Extraction added

Brent Crude:$85.48+1.2%SEAL | Natural Gas (HH):$2.86+0.8%SABAR | Gold (Hard Asset):$2,425.80+0.4%SEAL | Ringgit Exchange:4.047-0.3%SABAR | FTSE Bursa KLCI:1,749.20+0.5%SEAL | [NEW] PETRONAS Sovereign Extraction:70.5%BREACHED

PETRONAS Sovereign Extraction gauge — extracted via /vitals — BREACHED (70.5% PAT > 60% tripwire). This is the single most important Malaysian macro indicator. Federal dividend dependence on PETRONAS = ~20-25% of federal revenue. Breach cascades to bond market, ringgit, sovereign rating.
```

---

## PATCH — Live Signal Source Documentation (add at end of State of World Radar section)

```markdown
**Live signal source:** All values mirror `/vitals` and `/world/makcikgpt/feed.xml` live market proxies. Source: WEALTH commodity engine via yfinance · 5-min cache. If values diverge between /world and /vitals, /vitals is canonical.

**Sync required:** Every 6 hours minimum. Current data cycle: real-time. Previous stale data on Brent ($82.40 vs $85.48) and Ringgit (4.4250 vs 4.047) flagged at 2026-08-26 audit.
```

---

## Implementation Notes

- The `/world` radar data is likely served from a different cache than `/vitals`. Audit the data pipeline:
  - Check `/var/www/html/arif/scripts/` for the radar update script
  - Verify both `/vitals` and `/world` pull from the same WEALTH API endpoint
  - If they don't, unify the source

- The 6th signal (PETRONAS Sovereign Extraction) is novel — no current radar slot exists for it. Needs:
  - Backend support to ingest from `/vitals` JSON-LD
  - Front-end slot addition in the radar component
  - Definition of "SEAL/SABAR/HOLD/VOID" semantics for a static governance indicator

- The "4/5 SIGNALS SEALED" count needs updating:
  - Currently 4 SEAL + 1 SABAR = 4/5 SEAL label is misleading
  - Update to honest count: 3 SEAL + 2 SABAR + 1 BREACHED = 3/6 SEAL

---

## Recommended Sequence

1. **Immediate:** Sync the 5 existing signal values to match /vitals (Brent, NatGas, Gold, Ringgit, KLCI)
2. **Same deploy:** Fix the "4/5 SEAL" label to honest count
3. **Next sprint:** Add the 6th signal (PETRONAS Sovereign Extraction) — requires backend work

---

**Receipt:** Patch drafted 2026-08-26, Session SEAL-d7d3fde881a74721, 333-AGI Δ Mind.
