---
name: PETRONAS-intelligence-router
description: "USE WHEN: Any query mentioning PETRONAS, Petronas, petronas, Petros, SEARAH, Gentari, Tengku Taufik, extraction ratio, PETRONAS Carigali, or Malaysian national oil company topics."
version: 0.0.0-untracked
capability_tier: fed-long-context
ecology_state: WARM
---

# PETRONAS Intelligence Router

> **Trigger:** Any query mentioning PETRONAS, Petronas, petronas, Petros, SEARAH, Gentari, Tengku Taufik, extraction ratio, PETRONAS Carigali, or Malaysian national oil company topics.
> **Purpose:** Route all PETRONAS-related work through the unified intelligence atlas so every agent has full context.
> **Constitutional:** F2 TRUTH (cite sources), F7 HUMILITY (insider bias warning), F13 SOVEREIGN (Arif is PETRONAS insider).

> **Trigger:** Any query mentioning PETRONAS, Petronas, petronas, Petros, SEARAH, PRefChem, Gentari, Tengku Taufik, extraction ratio, PETRONAS Carigali, or Malaysian national oil company topics.
> **Purpose:** Route ALL PETRONAS work through the canonical atlas so every agent has full context — internal analysis FIRST, external search second.
> **Canonical atlas:** `/root/AAA/canon/PETRONAS/ATLAS.md` + `KNOWLEDGE_GRAPH.json`
> **Constitutional:** F2 TRUTH (cite sources) · F7 HUMILITY (insider bias) · F13 SOVEREIGN (Arif is PETRONAS insider)
## When to Load

- User mentions PETRONAS in any context (financial, political, institutional, personal)
- Agent encounters PETRONAS data in WEALTH, GEOX, or arifOS work
- MakcikGPT article generation or review
- SEARAH JV analysis
- Gentari energy transition queries
- PETRONAS-PETROS dispute updates
- Capital intelligence requiring PETRONAS context

- Any mention of PETRONAS in any context (financial, political, institutional, personal, geological)
- Agent encounters PETRONAS data in WEALTH / GEOX / arifOS work
- SEARAH JV / Petros dispute / Gentari / PRefChem analysis
## Routing Table

| Intent | Route | Files |
|--------|-------|-------|
| **Financial data** | WEALTH organ → `petronas_vitals.py` | `/root/WEALTH/wealth_core/petronas_vitals.py`, `/data/wealth/petronas_vitals.json` |
| **Institutional analysis** | Atlas → 4 Pillars | `/root/memory/.archive-2026-07/` (Universe25, Crisis Map, Third Axis, Inflection) |
| **Collapse trajectory** | forge_work → charts | `/root/forge_work/petronas-collapse-2026/` (14 charts, V1 vs V2) |
| **SEARAH JV** | Investigation suite | `/root/ariffazil/archive/searah-forge-2026-06-07/`, `/root/AAA/memory/investigations/SEARAH-TRUTH.md` |
| **Public articles** | MakcikGPT suite | `/root/arif-fazil.com/sites/arif-fazil.com/src/data/makcikgpt/` (12 articles) |
| **Open letters** | Surat suite | `/root/forge_work/petronas2025/`, `/root/petronas/04-letters/` |
| **Legal disputes** | Petros-Shell skill | `/root/HERMES/skills/research/petronas-petros-shell-dispute/` |
| **Claims verification** | AAA Claims Ledger | `/root/AAA/artifacts/petronas-leaflet-2026-06-20/CLAIM_LEDGER.yaml` |
| **Constitutional doctrine** | GENESIS | `/root/arifOS/GENESIS/006_PETRONAS_PARADOX.md`, `024`, `062` |
| **VOIDX decay signals** | WEALTH VOIDX | `/root/WEALTH/VOIDX_BENCHMARK.md` |
| **Gentari analysis** | Gentari forge | `/root/forge_work/gentari-v2/`, `/root/forge_work/gentari-v3/` |
| **Brazil sunk cost** | forge_work | `/root/forge_work/2026-08-06/petronas_brasil_sunk_cost_v2_aug2026.pdf` |
| **CEO profile** | Vault dossier | `/root/VAULT999/briefings_backup/briefings/Tengku_Muhammad_Taufik_*` |
| **Knowledge graph** | megamemory | `megamemory_understand("PETRONAS ...")` → 21 concepts, 72+ edges |

## Constitutional Warnings

1. **Insider bias:** Arif is a PETRONAS employee. Every PETRONAS analysis carries insider perspective. F7 HUMILITY: acknowledge this bias explicitly.
2. **Sovereign content:** H5 scars are sovereign memory. Read only when `scar:<id>` explicitly invoked.
3. **F2 TRUTH:** Every claim must cite source (OBS/DER/INT/SPEC). PETRONAS Annual Report, Bernama, Reuters, Companies House UK are primary sources.
4. **F6 MARUAH:** No personal attacks on named individuals. Institutional critique ≠ personal defamation.
5. **Data sovereignty:** PETRONAS internal data NEVER leaves CN/MY jurisdiction. Only public sources for external routing.

1. **Insider bias:** Arif is a PETRONAS employee — every analysis carries insider perspective (F7).
2. **F2 truth:** every claim cites OBS/DER/INT/SPEC; PETRONAS IFR, Bernama, Reuters, Companies House UK are primary.
3. **F6 maruah:** no personal attacks on named individuals; institutional critique ≠ defamation.
4. **Data sovereignty:** PETRONAS internal data never leaves MY/CN jurisdiction; public sources only.
5. **F13:** the exit/stay decision is sovereign — the atlas supplies data, never pressure.
## Key Financial Anchors (FY2025)

| Metric | Value | Source |
|--------|-------|--------|
| Revenue | RM266.1B | PETRONAS IFR FY2025 |
| PAT | RM45.4B (↓17.6%) | PETRONAS IFR FY2025 |
| Dividend | RM20B (↓38% from RM32B) | Board decision Feb 27, 2026 |
| Capex | RM45-50B | Board guidance |
| CFFO | RM85.2B | PETRONAS IFR FY2025 |
| Cash reserves | RM204B | PETRONAS IFR FY2025 |
| Gearing | 20.7% | PETRONAS IFR FY2025 |
| Extraction ratio | 70.5% (dividend/PAT 5yr avg) | WEALTH computation |

## Rightsizing / OD1 Timeline (state as of 2026-09-17)

> **This is the live structural event.** Any PETRONAS career, staffing, or
> org-design query routes here first.

**The cut:** 10% of workforce ≈ 5,000 people of ~52,000. Publicly framed as
"right-sizing", not retrenchment. Target = *enablers* (15,000–16,000 admin/
support roles), whose ratio sits above industry average. Technical core is
not the primary target.

**CEO framing (Tengku Muhammad Taufik):** structural, not cyclical. Industry
margin compressed 40–45% → ~20%, projected 16–18%. "If we don't do it now,
there will be no PETRONAS in 10 years." Read: the cut happened *while profits
were healthy* — this is preparation for permanent margin compression, not
reaction to a loss.

| Event | Date |
|---|---|
| Announcement | Feb 2025 |
| Hiring freeze | until Dec 2026 |
| Rightsizing wave 1 | 2025 |
| Rightsizing wave 2 | Mar 2026 (~1,000 roles) |
| Rightsizing wave 3 | Jul 2026 |
| Complete new org design | Aug 2026 |
| **OD1 (Operating Day 1)** | **Mar 2027** |

**MSS (Mutual Separation Scheme):** offered to permanent staff. Package
exceeds statutory minimum, structured by years of service, varies by
category/eligibility. Includes career coaching, emotional support, upskilling,
financial planning, PERKESO/MyFutureJobs placement. Transition Council +
People Development Committees govern placement. MSS = negotiated individual
deal; VSS = standardised group offer. Signing is voluntary and legally
challengeable in the Industrial Court only where consent was defective
(coercion / no real choice / no time to consider).

**Talent Placement forms** (Career Aspiration, TTS/Executive and above) ask
for: 2–5yr aspirations, development priorities, and a Q6 continuity choice —
*remain until OD1 Mar 2027 and beyond* **or** *register interest in MSS*.
Registering interest ≠ accepting; it signals flight risk to placement panels.

## Portfolio Moves (2026 reshaping)

| Move | Detail | Status |
|---|---|---|
| Searah | 50:50 JV with Eni — selected MY + ID assets, independent entity | Established 8 Jun 2026 |
| EnQuest farm-out | Balingian, SK8, D35 operatorship + PM6/12 non-op | Completing Jan 2027 |
| PRefChem | Saudi Aramco divested 50% to PETRONAS | 2026 |
| Vestigo | Marginal-fields vehicle | Operating |
| RT3 Perak | Regasification terminal approved (FSRU) | Development |
| PETROS dispute | Sarawak — ongoing legal case | Unresolved |

**Strategic direction:** PETRONAS moving from operator → portfolio manager,
with foreign partners funding development of farmed-out PSCs (unencumbers
assets from the PETROS case). Analysts (Kenanga, TA, HLIB) expect upstream
capex weakness through 2HFY26 then **recovery from FY27** — DIALOG and
KEYFIELD named as proxies.

## Key Financial Anchors (1H FY2026, released Aug 2026)

| Metric | Value | Note |
|---|---|---|
| Revenue | RM152.4B | +15% YoY |
| PAT | RM27.2B | +4% YoY — grew slower than revenue |
| Profit attributable | RM22.73B | Down from RM23.64B 1H25 |
| Operating cash flow | RM47.5B | −RM600M YoY |
| Upstream production | 2.34 MMboe/d | Down from 2.40 |
| LNG gross sales | 20.29 MMT / 282 cargoes | +17% YoY — the bright spot |
| Renewables | 9.1 GW installed + under construction | June 2026 |

**Macro (2026-09-17):** Brent ~USD106, USD/MYR 4.10, OPR 2.75%, US10Y 5.01%,
DXY 100.3. High Brent = healthy near-term cash; regime flagged SIDEWAYS.

## Sovereign Eurekas (GENESIS/062, 2026-08-18)

1. **Markets Are Constraint Systems** (WEALTH): Prices are shadows of flows. Flows are shadows of constraints. Constraints are shadows of reality.
2. **Language Is Attestation Layer** (arifOS): Language records reality. Flows reveal reality. Constraints govern reality. Emergence creates reality.

## VOIDX Reading

- Verdict: MIXED (leaning DEPENDENCY)
- Decay score: 0.42
- Strongest signal: dependency concentration
- Decay chain: Incentives drift → Reality diverges → Dependencies concentrate → Optionality shrinks → Fragility rises → Reflexive loops begin → Collapse

## Atlas Location

**Canonical:** `/root/petronas/ATLAS.md`
**Knowledge graph:** `megamemory_understand("PETRONAS")` → `petronas-institutional-knowledge-atlas`
**GENESIS:** `/root/arifOS/GENESIS/006_PETRONAS_PARADOX.md`, `024_PETRONAS_SOVEREIGN_ENERGY_INTELLIGENCE.md`, `062_FOURFOLD_AXIOM_SIGNAL_ARCHITECTURE.md`


## Mandatory First Step

## Mandatory First Step
1. Read `/root/AAA/canon/PETRONAS/ATLAS.md` — the apex-zen single source of truth.
2. **Core model payload:** probe `/root/arifOS/memory/entities/` first for thesis/scenario work (v3 collapse model + `PETRONAS_INTERNAL_ANALYTICAL_GRAPH_2026.md` + `00-EPISTEMIC-HEADER.md` 4-lane routing).
3. Resolve the specific file via `/root/AAA/canon/PETRONAS/KNOWLEDGE_GRAPH.json`.
4. Only then search externally if the atlas does not cover the question.
> **Cross-reference:** the Hermes canonical router `~/.hermes/skills/petronas-knowledge-router/SKILL.md` carries the fuller, live routing table (4-lane doctrine). Both routers point to the same atlas — do not fork them.

## Routing Table (live paths)

## Routing Table (live paths)
| Intent | Route | Canonical file |
|--------|-------|----------------|
| **Everything / first read** | Canonical atlas | `/root/AAA/canon/PETRONAS/ATLAS.md` |
| **Machine graph** | Canonical graph | `/root/AAA/canon/PETRONAS/KNOWLEDGE_GRAPH.json` |
| **Financial data** | WEALTH vitals | `/root/WEALTH/wealth_core/petronas_vitals.py` |
| **Institutional forensics** | sink-forensics refs | `/root/.kimi-code/skills/institutional-epistemic-sink-forensics/references/petronas-*.md` |
| **Crisis / collapse** | memory | `/root/AAA/memory/2026-06-07-petronas-crisis-map.md`, `/root/AAA/memory/deep-research-petronas-third-axis.md` |
| **Taufik-Petros KG (latest)** | memory | `/root/memory/2026-09-07-TENGKU-TAUFIK-PETROS-KNOWLEDGE-GRAPH.md` |
| **SEARAH JV** | investigation suite | `/root/AAA/memory/investigations/SEARAH-TRUTH.md`, `/root/ariffazil/archive/searah-forge-2026-06-07/SEARAH_FILE_MAP.md` |
| **Public articles** | MakcikGPT | `/root/arif-fazil.com/sites/arif-fazil.com/public/makcikgpt-md/petronas-*.md` |
| **Dossiers (BOD/rakyat/site)** | forge_work | `/root/AAA/forge_work/2026-08-26-petronas-*/` |
| **Constitutional doctrine** | GENESIS | `/root/arifOS/GENESIS/{006_PETRONAS_PARADOX,024_PETRONAS_SOVEREIGN_ENERGY_INTELLIGENCE,062_FOURFOLD_AXIOM_SIGNAL_ARCHITECTURE}.md` |

## Key Financial Anchors

## Key Financial Anchors
| Revenue FY2025 | RM266.1B (↓16.8%) | PETRONAS IFR FY2025 |
| PAT FY2025 | RM45.4B (↓17.6%) | PETRONAS IFR FY2025 |
| PAT H1 2026 | RM27.2B (+4%, LNG) | PETRONAS IFR H1 2026 |
| LNG H1 2026 | 20.29 MMT (+17%) | PETRONAS IFR H1 2026 |
| Upstream production H1 2026 | 2.34 MMboed (↓) | PETRONAS IFR H1 2026 |
| Dividend | RM20B (↓ from RM32B) | Board decision |
| Extraction ratio | 70.5% | WEALTH computation |

## Dead paths (do NOT cite)

## Dead paths (do NOT cite)
- `/root/petronas/ATLAS.md` — dir gone (quarantined 2026-09-12)
- `/root/forge_work/petronas-collapse-2026/` — moved
- `megamemory_understand("PETRONAS")` — not verified live