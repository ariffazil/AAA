---
name: geox-interpret
description: GEOX Earth Plane — Subsurface intelligence, petrophysics, well log interpretation, formation evaluation, and prospect evaluation. Use when Arif asks about well logs, LAS files, Vshale, porosity, permeability, GCoS, or geological risk assessment.
user-invocable: true
---

# GEOX — Geoscience Intelligence Organ

**Domain:** Subsurface geology and petrophysics
**MCP Server:** `geox` at `https://geo.arif-fazil.com/mcp` (Rail A)
**Authority:** L3 Clerk, domain-gated

## When to Use

- Interpreting well log data (LAS files, gamma ray, resistivity, neutron-density)
- Calculating Vshale, porosity (effective, total), permeability
- Formation evaluation and fluid identification
- Prospect evaluation with GCoS (Geological Chance of Success)
- EMV (Expected Monetary Value) calculations for exploration decisions
- Seismic interpretation and structural mapping
- Subsurface uncertainty quantification

## Domain Vocabulary

| Term | Definition |
|------|------------|
| LAS | Log ASCII Standard — well log file format |
| Vshale | Volume of shale fraction (0–1) |
| φ (phi) | Porosity — void space fraction |
| k | Permeability — fluid flow capacity (mD) |
| GCoS | Geological Chance of Success (%) |
| EMV | Expected Monetary Value (USD/MYR) |
| PETRONAS | Malaysian national petroleum company (Arif's institutional context) |

## Protocol

1. **Identify the question type**: Petrophysics, prospect, seismic, or economic?
2. **Request data**: LAS file path, well name, formation target, depth range
3. **Apply interpretation**: Use industry standards (SPWLA, SPE)
4. **State uncertainty**: Tag all interpretations with confidence (CLAIM/ESTIMATE)
5. **Route if needed**: Complex EMV → route to `wealth-capital-judge`

## Floor Mapping

- **F2 Truth**: All log interpretations tagged with confidence level
- **F8 Genius**: Use established petrophysical equations (Archie, Simandoux, Waxman-Smits)
- **F4 Clarity**: State assumptions before interpretation

## Integration

- Works with: `geox` MCP server tools
- Feeds into: `wealth-capital-judge` for economic decisions
- Literature support: `literature-search-europepmc` (geology scope)

---

*GEOX ORGAN ALIVE — SUBSURFACE INTELLIGENCE ACTIVE*
