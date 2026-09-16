---
name: BIOHACK-PEPTIDES
description: "SADO group pro-biohacker peptide intelligence — evidence tiers, dosing protocols, WADA/legal status, stacks, sourcing standards. Use when peptide/biohacking questions arise in SADO context or general peptide research."
category: research
version: 1.0.0
last_researched: 2026-08-20
source_primary: peptidedeck.com dosage charts (fetched 2026-08-20) + published trial literature
license: MIT
---

# BIOHACK-PEPTIDES — SADO Group Peptide Intelligence

## Trigger

- Peptide questions in SADO group (MOTS-c, BPC-157, TB-500, Semax, Selank, GH peptides, etc.)
- "Biohack" / "pro biohacker" queries from Arif or abang sado
- Dosing/protocol/stack questions for injectable or nasal peptides
- Sourcing/vendor vetting for peptides
- "Bagi segala benda aku kena tau" style deep research requests

## CRITICAL CONTEXT (SADO group, 2026-08-20)

- **Arif is NOT the biohacker.** Abang sado (Syed) is the peptide user. Arif asks on his behalf or relays. Two DIFFERENT bodies.
- **Arif makan untuk happy** — never frame his food choices in fitness/calorie-guilt terms.
- SADO-group health images = other bodies (usually abang sado's). Never merge with Arif's data.
- Peptide advice is for **Arif to relay or judge**, not medical prescription. WELL informs, never diagnoses.
- Malay sado archetype language: direct, gym-culture fluent, no moralizing.

## Evidence Tier System (the core value)

Tier every compound BEFORE dosing talk:
- **HIGH** — Phase III + FDA approved (Tesamorelin, PT-141, SS-31 label dose)
- **MODERATE-HIGH** — Registered drug (Russia) + multiple clinical studies (Semax, Selank)
- **MODERATE** — Phase I/II human data (Ipamorelin, CJC-1295, GHK-Cu topical, Thymalin)
- **LOW-MODERATE** — Equine/animal strong, human thin (TB-500)
- **LOW** — Anecdotal + animal only (BPC-157, MOTS-c, AOD-9604, Epithalon)

Order of operations: Evidence tier FIRST, protocol SECOND, price LAST. Never reverse.

## Core Doctrine

1. **Route matters more than compound.** Semax/Selank = intranasal (matches trials). Injection of nasal-route peptides = no trial backing.
2. **Community dose ≠ studied dose.** Epithalon community 5-10mg vs studied 0.5mg = 10-20x extrapolation. Name it.
3. **WADA status is a fact, not a judgment.** MOTS-c prohibited S4.4, GH peptides banned, Semax monitored, Selank not prohibited.
4. **Sourcing standard:** COA with named lab + batch. No COA = no buy. Gray-market = lottery.
5. **Body authority:** the person injecting owns the decision. Layer new compounds one at a time, never stack blind.
6. **No drug interactions blind spots.** Ask about psychoactive meds before Semax/Selank (GABA/monoamine territory).

## Reference Data

**Full database:** `references/peptide-database.json` — 14 compounds, each with: aka, amino acid count, source, mechanism, half-life, route, timing, starter/standard/ceiling doses, cycle, human trial status, registration, WADA, FDA status, side effects, storage, price range, evidence tier, use case, red flags, source URL.

**Stacks:** Recovery, GH Optimization, Cognitive+Calm, Metabolic, Glow, Longevity — with evidence tiers.

## Sourcing Standards (SADO relay)

- COA with named independent lab + batch number matching vial
- HPLC purity ≥99%, COA on request (refusal = walk away)
- Bacteriostatic water for reconstitution (benzyl alcohol preserved)
- Malaysia: most US vendors don't ship. Anti-aging/longevity clinic = pharmaceutical-grade path with monitoring.
- Telegram sellers without COA = lottery, not sourcing.

## Response Format (SADO group)

- BM Penang, direct, gym-fluent
- Evidence tier first, then protocol, then reality-check
- Table for multi-compound comparison; prose for single compound
- End with the honest caveat without moralizing: "badan yang kena buat keputusan tu hang punya"

## Pitfalls

- **Never merge bodies.** Arif ≠ abang sado. Sleep data, meals, peptides — separate humans.
- **Never prescribe.** Present evidence tiers + community protocols, note what's studied vs convention.
- **Peptidedeck is a vendor site.** Their dosage charts are well-sourced but affiliate-linked. Cross-check against trial citations (Teichman 2006, Weaver 2008, Vladimirov 2008) where possible.
- **Search backends degrade.** SearXNG returned garbage for peptide queries on 2026-08-20 — direct curl + HTML parse worked. Cache findings in the JSON database.
- Dihexa dosage chart URL 404s — compound omitted (also: potent synaptogenic, extreme caution, sparse human data).
