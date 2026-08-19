# PETRONAS Intelligence Router

> **Trigger:** Any query mentioning PETRONAS, Petronas, petronas, Petros, SEARAH, Gentari, Tengku Taufik, extraction ratio, PETRONAS Carigali, or Malaysian national oil company topics.
> **Purpose:** Route all PETRONAS-related work through the unified intelligence atlas so every agent has full context.
> **Constitutional:** F2 TRUTH (cite sources), F7 HUMILITY (insider bias warning), F13 SOVEREIGN (Arif is PETRONAS insider).

## When to Load

- User mentions PETRONAS in any context (financial, political, institutional, personal)
- Agent encounters PETRONAS data in WEALTH, GEOX, or arifOS work
- MakcikGPT article generation or review
- SEARAH JV analysis
- Gentari energy transition queries
- PETRONAS-PETROS dispute updates
- Capital intelligence requiring PETRONAS context

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
