# AGI-kinabalu-dossier-qc — Self-Healing Geological Dossier Gate

> **Sovereign QC gate for Kinabalu Basin dossier — enforces physical-reality invariants before any deploy.**
> **ΔS ≤ 0: every edit must reduce geological entropy, not add it.**
> **DITEMPA BUKAN DIBERI — Forged, Not Given.**

## TRIGGER

Load when ANY agent (Claude Code, Copilot, Codex, Grok, Kimi) is asked to:
- "fix kinabalu page"
- "update kinabalu basin"
- "audit geology page"
- "deploy earth site"
- "kinabalu dossier qc"
- "verify basin page"
- "cross-section check"
- Any geological dossier mutation

## INVARIANTS — THE 7 GATES

Every mutation to the Kinabalu Basin dossier MUST pass all 7 gates before deploy.
If ANY gate fails, the mutation is VOID — fix it before proceeding.

### Gate 1: Summit Height (F2 TRUTH)
```
INVARIANT: page MUST state surveyed summit = 4,095 m (Low's Peak, 1997 re-survey)
SRTM nearest-node value (3,951 m) may appear ONLY with explicit "SRTM sample" label
FAIL IF: "3,951 m" appears without the surveyed 4,095 m in proximity
FAIL IF: summit called "3,951 m" as if it were the measured height
```

### Gate 2: Single Vertical Exaggeration (F4 CLARITY)
```
INVARIANT: exactly ONE VE value, computed from axis ranges, printed in ONE place
The cross-section footer says ~4×; the section header must match
FAIL IF: two different VE numbers appear anywhere (currently ~32× header vs ~4× footer)
```

### Gate 3: MMU Is NOT a Seal (F2 TRUTH)
```
INVARIANT: the MMU/DRU is a correlation datum and trap-defining unconformity, NOT a regional seal
Seals = intraformational shales within deltaic/turbidite sequences
FAIL IF: any text states "MMU acts as a regional seal"
FAIL IF: seal description does not mention intraformational shales
SOURCE: PETRONAS Chapter06_Sabah — "no major seal horizons in the Sabah Basin"
```

### Gate 4: Granite Age (F2 TRUTH)
```
INVARIANT: emplacement age = 7.85–7.22 Ma (U-Pb zircon, Cottam et al. 2010 JGS)
The old K-Ar estimate (10–13.7 Ma) is STALE and MUST NOT appear
FAIL IF: "10 Ma" or "10–8 Ma" appears as emplacement age
PASS IF: "7.85–7.22 Ma" with Cottam et al. 2010 citation
```

### Gate 5: Relief Mechanism (F2 TRUTH)
```
INVARIANT: 7 km relief = rapid Neogene exhumation + isostatic rebound (~5 mm/yr still rising)
FAIL IF: text says relief is "almost entirely the result of one intrusion event"
PASS IF: text attributes relief to "unroofing and isostatic uplift"
```

### Gate 6: West Crocker Timing (F2 TRUTH)
```
INVARIANT: West Crocker Fm is Late Eocene–Oligocene → deposited AFTER the Rajang Unconformity (~40 Ma)
FAIL IF: West Crocker described as "scraped off during the ~40 Ma Sarawak Orogeny"
PASS IF: Rajang Group (not West Crocker) associated with Sarawak Orogeny deformation
```

### Gate 7: Epistemic Honesty (F7 HUMILITY)
```
INVARIANT: every claim carries an epistemic tag where confidence < 0.99
UNKNOWN tags MUST appear on:
  - "Megah-1" well name (not independently verifiable)
  - "Meliau Orogeny" event name (not standard in literature)
  - "Cornwell et al. JGR 2025" (DOI unverified)
  - "largest Paleogene" superlative (qualify: "one of the most extensive")
CLAIM tags on: all PETRONAS MPM-sourced statements
ESTIMATE tags on: thicknesses, play extents, OOIP numbers
```

## SELF-HEALING WORKFLOW

```
1. LOAD the live page: https://arif-fazil.com/earth/kinabalu-basin/
2. RUN all 7 gates against the live HTML
3. IF any gate fails:
   a. Edit /root/arif-fazil.com/sites/arif-fazil.com/public/earth/kinabalu-basin/index.html
   b. Re-run gates until all pass
   c. Deploy: cp public → dist → /var/www/html/arif/earth/kinabalu-basin/
4. SEAL: append receipt to VAULT999 with gate results + commit hash
```

## DEPLOY COMMAND

```bash
SOURCE="/root/arif-fazil.com/sites/arif-fazil.com/public/earth/kinabalu-basin/index.html"
DIST="/root/arif-fazil.com/sites/arif-fazil.com/dist/earth/kinabalu-basin/index.html"
LIVE="/var/www/html/arif/earth/kinabalu-basin/index.html"
cp "$SOURCE" "$DIST" && mkdir -p $(dirname "$LIVE") && cp "$SOURCE" "$LIVE"
```

## CROSS-SECTION QC (separate file, same gates)

The cross-section at `/root/arif-fazil.com/sites/arif-fazil.com/public/earth/kinabalu-cross-section.html`
must also pass Gate 1 (summit height) and Gate 2 (single VE).

## BREADCRUMB — FOR THE NEXT AGENT

- **Source:** /root/arif-fazil.com/sites/arif-fazil.com/public/earth/kinabalu-basin/index.html
- **Dist:** /root/arif-fazil.com/sites/arif-fazil.com/dist/earth/kinabalu-basin/index.html
- **Live:** /var/www/html/arif/earth/kinabalu-basin/index.html
- **URL:** https://arif-fazil.com/earth/kinabalu-basin/
- **Cross-section source:** /root/arif-fazil.com/sites/arif-fazil.com/public/earth/kinabalu-cross-section.html
- **Cross-section URL:** https://arif-fazil.com/earth/kinabalu-cross-section.html
- **Last QC:** 2026-07-30 by Copilot corporate audit
- **Canonical references:** Balaguru & Hall 2009, Cottam et al. 2010 JGS, PETRONAS MPM 2025, Madon & Jong 2022
- **Memory:** [[kinabalu-basin-dossier]] [[geox-qc-gates]] [[agentic-web-self-healing]]

## VAULT999 RECEIPT TEMPLATE

```json
{
  "event": "kinabalu-dossier-qc",
  "timestamp": "ISO8601",
  "agent": "agent-id",
  "gates_passed": [1,2,3,4,5,6,7],
  "gates_failed": [],
  "commit": "sha",
  "deployed": true,
  "verdict": "SEAL"
}
```

---

*Forged 2026-07-30 — Copilot corporate audit → self-healing automation. Any agent can now maintain physical-reality alignment.*
