---
name: travel-intelligence-standard
description: "Canonical 3-Layer Travel Intelligence Protocol for arifOS. Generates machine-grade spatial travel artifacts optimized for human execution in the field. Activates when: planning any trip, refreshing live itinerary, or updating travel data. Layer 1 = Executive Summary (driver-ready), Layer 2 = Day Narrative (on-the-road cards), Layer 3 = Machine Appendix (audit/spine)."
category: travel
tags: [spatial, itinerary, map-grade, human-execution, arifOS]
version: 2026.05.08
seal: 999
---

# CANONICAL TRAVEL INTELLIGENCE STANDARD
## 3-Layer Travel Intelligence Protocol — arifOS F1-F13

**DITEMPA BUKAN DIBERI** — SEAL 999

---

## ARCHITECTURE

```
Raw Spatial Data (Places API / OSRM / Nominatim)
    ↓
arifOS Spatial Compute Engine
    ↓
Constraint Scoring (halal · stroller · nap · weather · fatigue · budget)
    ↓
3-LAYER FORMATTING ENGINE
    ↓
Layer 1: HUMAN SUMMARY (top 20%) — driver-ready, low entropy
Layer 2: DAY NARRATIVE (middle 60%) — actionable cards per stop
Layer 3: MACHINE DATA (bottom 20%) — audit trail, drill-in only
```

---

## LAYER 1: HUMAN SUMMARY

### Trip Overview Card
Format:
```
| Field | Value |
|---|---|
| Route | [Origin] → [Stop 1] → [Stop 2] → ... → return |
| Group | [Count] adults + [Baby name] ([age]) |
| Base | [Hotel name] ⭐[rating] |
| Budget | [currency] [min]–[max] / pax |
| Timezone | [UTC offset] |
```

### Safety and Emergency Card
Always include:
- Nearest clinic (name, rating, distance from base)
- Baby supplies source (name, rating, distance)
- Border buffer time (if applicable)
- Abort triggers per day

### Critical Decision Box
Highlight with F1 Protocol when:
- Fatigue load exceeds threshold for group composition
- Reversibility is low (irreversible once committed)
- Multiple conflicting constraints (heat + baby + distance)

Format:
```
⚠️ CRITICAL DECISION: [Short Title]
[Constraint math — e.g., "78 min driving + 2-3 hrs zoo + lunch = 6-9 hrs"]
*Verdict:* [DO/DO NOT] [action] with [baby/constraints]

Option A (Recommended): [description]
Option B: [description]
```

---

## LAYER 2: DAY NARRATIVE

### Per-Day Structure
1. **Morning Brief**: Theme + one-line summary + departure time
2. **Stop Cards** (one per stop):
   - Departure time window
   - Drive time + distance
   - Key facts (halal, AC, hours verified)
   - Baby notes (nap fit, stroller fit)
   - Abort rule (when to skip/cut short)
   - Fallback option
3. **Evening Prep**: 3–5 bullet action items for next day

### Stop Card Format
```
📍 STOP — [Name] (ID)
| | |
|---|---|
| Hours | [verified hours] |
| Halal | [status] |
| Parking | [available/limited/none] |
| Baby | [fit score as plain language + emoji] |
| Time here | [min]–[max] min |
| Abort if | [condition] |
| Fallback | [alternative stop] |
```

### Abort Rules
Always tag per-day critical aborts:
- Rain / heat advisory
- Time boundary violations (e.g., "must exit zoo by 4:15PM")
- Fatigue threshold exceeded
- Venue closure / crowd overflow

---

## LAYER 3: MACHINE DATA

### Place Graph Table
Columns: ID · Canonical Name · Place ID · Lat/Lng · Rating · Reviews · Open Status · Hours · UTC offset

### Route Intelligence Table
Columns: Leg · From → To · Mode · Distance · Duration · Risk Note

### Constraint Scoring Matrix
Columns: Stop · Halal · Stroller · Nap Fit · Weather · Detour Cost · AGI Verdict

### Epistemic Tags
| Tag | Meaning |
|-----|---------|
| VERIFIED | API confirmed |
| PLAUSIBLE | Domain inference |
| UNVERIFIED | No API data |
| HYPOTHESIS | Human assumption |

---

## GENERATION PROMPT TEMPLATE

When user says "plan trip to [location]":

```
You are producing a family travel itinerary for [TRIP NAME].

Output must have THREE LAYERS:

1. HUMAN SUMMARY (top 20%)
   - Trip card: who, when, where, budget, risks
   - Safety card: nearest clinic, baby supplies, abort conditions
   - Decision points: where family must choose (tag F1)

2. DAY NARRATIVE (middle 60%)
   - Morning brief per day
   - Stop cards: depart window, ETA, halal, baby notes, abort, fallback
   - Evening prep bullets
   - Plain language, active voice, direct instructions

3. MACHINE DATA (bottom 20%)
   - Place graph with verified IDs
   - Route table with distances/durations
   - Constraint scores and evidence
   - Epistemic tags: VERIFIED / PLAUSIBLE / UNVERIFIED / HYPOTHESIS

NEVER:
- Dump tables without narrative context
- Hide critical decisions in data sections
- Use scores without plain-language verdicts
- Bury safety/abort info below fold

ALWAYS:
- Lead with actionable summary
- Tag uncertainty clearly
- Promote safety to top
- Structure for scanning while driving
```

---

## APPLY TO: Hat Yai 2026

**Locked Context IDs (2026-05-08 session):**

| ID | Name | Place ID | Lat/Lng |
|----|------|----------|---------|
| P01 | Lamoon Villa | ChIJYQKhMfUpTTARXmkX3NQpeyA | 7.0128, 100.5408 | ⚠️ PLAUSIBLE — address `9 Tienjawuthit 1 Rd` not OSM-indexed; coordinate derived from CentralFestival spatial relationship (8-min walk north) |
| P02 | Municipal Park | ChIJH2dajhQpTTARwYer740Ezc8 | 7.0031, 100.4667 |
| P04 | Songkhla Zoo | ChIJbU7VQqcyTTARDwPrrYKMWXE | 7.1595, 100.6190 |
| P05 | Wat Hat Yai Nai | ChIJbYpzmW4oTTARiDHJTTPsJbY | 7.0225, 100.5500 |
| P06 | Central Hatyai | ChIJCZ0eezMoTTARCFlwdoY1Z9w | 7.0089, 100.5327 |
| P08 | R&R Halal Sadao | ChIJV8qjN-q5TDARYewG8HwVYrQ | 6.7250, 100.4450 | ✅ USER-PROVIDED |
| P09 | ISDU Premium Songkhla | ChIJW9c_hPgzTTARyYCgTcE8CwM | ~7.1864, 100.6005 | ⚠️ PLAUSIBLE — prior session data, not independently verified |
| P10 | Friendly Health Massage | ChIJ1fGExespTTARzfItRCtapi0 | ~7.0083, 100.5299 |
| P11 | Malika Beauty Massage | ChIJ...(near P06) | ~7.0111, 100.5411 |

**Route Legs:**

| Leg | From → To | km | min |
|-----|-----------|---|-----|
| L01 | Border → R&R Sadao | 3.0 km | 5 min |
| L02 | R&R Sadao → Lamoon Villa | 42.2 km | 49 min |
| L03 | Lamoon Villa → Municipal Park | 10.7 km | 23 min |
| L04 | Municipal Park → Night Market | 10.7 km | 22 min |
| L05 | Lamoon Villa → ISDU Songkhla | 25.3 km | 33 min |
| L06 | ISDU → Songkhla Zoo | 4.1 km | 7 min |
| L07 | Zoo → Lamoon Villa | 27.9 km | 33 min |
| L08 | Lamoon Villa → Massage | 1.4 km | 3 min |
| L09 | Massage → Dinner | 0.6 km | 2 min |
| L10 | Lamoon Villa → Wat | 4.2 km | 6 min |
| L11 | Wat → Malika Massage | 3.4 km | 6 min |
| L12 | Malika → Central Hatyai | 1.2 km | 3 min |
| L13 | Central Hatyai → Border | 42.6 km | 54 min |

**Day 2 Fatigue Math:**
- Driving: 78 min total
- Zoo walking: 2-3 hrs
- Lunch + massage: 2-4 hrs
- Total: 6-9 hrs active time
- With baby (8 months): HIGH fatigue load → split group recommended

**Safety IDs:**
- Nearest clinic: Health Link International ~1.5 km
- Baby supplies: Central Hatyai supermarket (ground floor)
- Emergency pharmacy: B&T Pharmacy 5 stars 1.8 km (Central Hatyai G-05)

---

## VPS Deployment Notes (arifOS Travel Artifact)

### Google Share Links
**CRITICAL LIMITATION:** `vision_analyze` CANNOT resolve Google Share links (`share.google.com/...`). These redirect through Google's sharing infrastructure and do not expose raw content.
**Workaround:** Ask user to provide: (1) place name, (2) Place ID from URL (format: `ChIJ...`), or (3) coordinates from URL (format: `@lat,lng`). Then use OSM Nominatim or direct Google Maps Place ID.

### VPS Web Root Map
Different routes serve from different roots on `root@72.62.71.199`:
| URL Pattern | Web Root |
|------------|----------|
| `arif-fazil.com/*` | `/var/www/arif-fazil.com/` |
| `*.arif-fazil.com` (subdomains) | `/var/www/html/` |

**Correct rsync for main domain artifacts:**
```bash
rsync -av /root/arif-sites/output/{file}.html root@72.62.71.199:/var/www/arif-fazil.com/
```

**Verify after deploy:**
```bash
curl -s "https://arif-fazil.com/{file}.html" | grep -c 'unique-content-string'
```

**Cloudflare cache issue:** If URL returns wrong page after deploy, Cloudflare is serving stale cached content. Fix: purge via CF dashboard or API. Temporary bypass: add `?refresh=1` to URL.

### PDF Generation
```bash
/root/.hermes/venv/bin/weasyprint /root/arif-sites/output/{name}.html /root/arif-sites/output/{name}.pdf
```
WeasyPrint runs from Hermes venv, not system-wide. Known quirk: `@media (max-width: 400px)` without space before parenthesis causes "invalid media type" warning — safe to ignore.

### Email PDF via Gmail SMTP
**Use `terminal()` with inline Python reading password from file** — `execute_code` sandbox cannot see `/root/AAA/secrets/email.env` env vars.
```python
python3 << 'EOF'
# Read password directly from file (bypasses sandbox env-var issue)
password = None
with open('/root/AAA/secrets/email.env') as f:
    for line in f:
        if 'GMAIL_APP_PASSWORD' in line and '=' in line:
            password = line.strip().split('=', 1)[1].strip()
            break
# Then smtplib.SMTP("smtp.gmail.com", 587) with starttls() + login
EOF
```

---

*DITEMPA BUKAN DIBERI — 999 SEAL*
*Generated by arifOS Travel Intelligence Protocol v2026.05.08*
