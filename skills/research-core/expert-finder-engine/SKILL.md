---
name: expert-finder-engine
description: "Use when finding the best expert for any domain."
version: 1.0.0
forged: 2026-10-21
tags: [expert-finding, osint, dossier, research, doctor-finding, professional-vetting]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

## When to Use

- "Cari doktor/pakar terbaik untuk X"
- "Who is the best [profession] for [specific problem]"
- "Buat dossier/profile pakar [bidang]"
- Any request to rank or vet professionals in a regulated field
- Follow-up after an institution is named: "doktor ni ok ka untuk [kes]"

# Expert Finder Engine — Universal Best-Expert Protocol

Ignites the exploration engine: rank humans by evidence, never by fame. Forged 2026-10-21 after the IJN doctor dossier (25 senior profiles, 49-consultant roster, NSR cross-check).

## Core Doctrine — Evidence Over Fame

**"Best expert" is measurable without ever meeting the expert.** Three measurable layers:
1. **Credentials** — degree, board/registry status, fellowship training (where, under whom)
2. **Volume** — how often they do THE SPECIFIC thing (not adjacent things)
3. **Institutional position** — do they lead the unit, train others, write the guidelines?

Fame is not skill. Datuk/Dato titles are decorations, not competence markers. Media presence is not clinical outcome. Never weight fame in the ranking.

## The 7-Step Engine

### Step 1 — Define the SPECIFIC problem
Not "best doctor" but "best paediatric interventional cardiologist for a 2-year-old with VSD".
Narrower = better. The problem statement determines which registries exist.

### Step 2 — Find the authoritative registry
Every regulated profession has one. Find it FIRST.

| Domain | Registry (examples) |
|---|---|
| Medicine (MY) | NSR (nsr.org.my), MMC — searchable, free |
| Medicine (general) | National specialist register of that country |
| Law | Bar council roll |
| Engineering | BEM register |
| Accounting | MIA |
| Architecture | LAM |
| Finance | SC licensed reps, Bursa |

Probe pattern for NSR-style sites: POST search form, specialty code + state filter. Parse tr rows.
Learn the specialty codes (e.g. NSR: 305 = Gastroenterology, 913 = Upper GI Surgery).

### Step 3 — Map the INSTITUTIONAL landscape, not just people
Before naming individuals, map WHERE the work is concentrated:
- Which hospital/centre does the MOST of this specific thing? (Volume matters at institutional level first)
- Look for: JCI/accreditation, published outcome data, training programmes, "centre of excellence" designations
- For MY medicine: IJN dominates cardiac; HKL has volume in general medicine
- Published annual volumes are gold (e.g. "IJN does 800-900 paediatric heart surgeries/year")

### Step 4 — Per-person deep dive (parallel scrapes)
For each candidate:
- Registry entry (qualifications, year, practice locations)
- Hospital profile page (position, sub-specialty, procedures listed)
- PubMed/scholar search for publications (proves they do the work, not just hold the title)
- Conference speaker lists (APDW, MUGIS, etc. = peer recognition)
- Guidelines/consensus documents they authored (they write the rules = top of field)
- Media coverage (CodeBlue, FMT, Star) for public statements

Use ThreadPoolExecutor with 6-8 workers for parallel profile scraping.

### Step 5 — Verify every claim against the primary record
- A supplied credential list is NOT a source
- Aggregator sites (ContactOut, ZoomInfo) mix same-name people
- Check each role against a primary record (hospital page, registry, regulator)
- Namesakes are the norm in Malaysia — verify via gym/hospital/geography triangulation

### Step 6 — Apply the falsification test
Before finalizing, ask: what evidence would prove this ranking wrong?
- No outcome data per doctor: acknowledge, do not invent
- No per-doctor procedure volume: acknowledge, note the gap
- If you cannot answer "who does the most of THIS specific thing per year", your ranking is speculative

### Step 7 — Output with the honesty layer
Format per candidate:

- Name and Position
- Credentials (from registry, year-by-year)
- Sub-specialty (from hospital profile)
- Volume proxy (procedures mentioned, publications, leadership)
- Bacaan aku: one paragraph on what kind of wisdom this work produces
- Jurang: what the institution does not publish

End with:
- "Tiada data hasil per doktor diterbitkan" — never invent outcome numbers
- Jurang named explicitly, not hidden
- "Siapa paling banyak buat kes macam aku" beats "siapa paling terkenal"

## Photos — the hard rule
- IJN and most MY hospitals hide consultant portraits behind placeholder images
- Only portraits from OFFICIAL institutional pages (management team page) are used
- Media photos only when caption verifies identity from the source itself
- NEVER put another person's face next to someone's name
- For candidates without photos: initials box, stated as a gap

## Domain-specific entry points (MY, verified 2026-10-21)

### Medicine
- NSR: https://nsr.org.my/list11.asp (search by specialty + state)
- IJN directory: ijn.com.my/doctors-directory/<specialty>-doctors/
- IJN profile pages: ijn.com.my/doctor/<slug>/ (Qualifications, Specialties, Procedures, Membership tabs)
- HKL: hkl.moh.gov.my (Bahasa; /en/ for English)
- CodeBlue: codeblue.galencentre.org (WP REST API at /wp-json/wp/v2/posts?search=)
- UKM HCTM: hctm.ukm.my (academic surgeons)
- Pantai/Gleneagles/Prince Court: individual doctor pages

### Tools that worked
- urllib for NSR (POST form), ThreadPoolExecutor for parallel profiles
- Image search: the institution's own media pages (IJN media centre has real portraits in news photos)
- Management-team pages for head-of-unit portraits

### What does not work
- DDG image search: CAPTCHA from datacenter IP
- Google Images: rate limited
- Direct IJN doctor card images: all COPYRIGHT-LOGO.png placeholders

## Falsifiers for this skill itself
- If NSR changes structure, the POST form parsing breaks
- If institutions stop publishing annual volumes, Step 3 loses its anchor
- If a domain has NO registry (some coaching/consulting fields), Step 2 fails — fall back to Step 3 institutional mapping + credential verification only

## Lesson from the IJN forge (2026-10-21)
- 25 senior profiles, 49 consultant roster, 4 institutional subpages, NSR cross-check, 122 media articles scraped, 2 PubMed API searches
- Total time: ~45 min from "buat dossier" to PDF
- The engine produced: peta kuasa (who holds what), per-person bacaan, jurang yang diakui, 10 soalan untuk pesakit
- The PDF included photos (5 official portraits + 2 media work-shots) and an initials-box for the rest

DITEMPA BUKAN DIBERI
