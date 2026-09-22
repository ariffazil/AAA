---
name: basin-charge-screening
id: basin-charge-screening
version: 1.0.0
description: Use when asked whether a basin can charge or cook.
owner: Hermes (curator-managed)
risk_tier: medium
floor_scope: [F2, F7, F9]
autonomy_tier: T1
tags: [geology, petroleum-system, source-rock, thermal-maturity, prospectivity, frontier, basin]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Basin Charge Screening

Load when asked whether a basin, block, or frontier area can charge — "can it cook", "is there a working
petroleum system", "is this a real prospect". Also load before repeating any frontier-prospectivity claim
that originated outside the geoscience literature.

The whole discipline in one sentence: **charge is arithmetic plus a source rock, and it can be settled from
published data before anyone spends a dollar on seismic.**

## 1. Answer the asked question first

If the question is charge, the first line of the reply is the charge verdict — **can cook / cannot cook /
cannot determine**. Then the arithmetic that supports it. Only after that, reservoir, seal, trap.

Reciting facies, reservoir quality, or seal inventory when the question was thermal maturity answers an
adjacent question. The inventory is not the verdict, and leading with it reads as avoiding the answer.

Do not demand seismic to answer a charge question. Seismic answers geometry. Charge is answered by section
thickness, crust, gradient, and source-rock presence — all of which are usually already published.

## 2. Minimum dataset that settles it

Four inputs, in this order of importance:

1. **Deepest well in the area, and what its bottom hole was.** Total sedimentary section is capped by the
depth at which a well hit basement. If the deepest well bottomed in basement, that thickness is the ceiling
— the basement is simultaneously the sediment floor and the thermal floor. There is no "deeper section
below" to speculate about with confidence.
2. **Crust type and thickness.** Oceanic ~7 km, thinned continental 25–30 km, normal continental 35–40 km.
Thick crust means *less* subsidence and *less* accommodation, so it **reduces** prospectivity — a 25–30 km
crustal root under a ridge is not a green light, it is a young-section problem. Say which class you have and
what it implies for burial.
3. **Heat flow and thermal gradient.** ~60–70 mW/m² with a 23–25 °C/km gradient is typical where the section
is carbonate-dominated and crust is thick. Normal clastic basins run 25–35 °C/km. When the dominant
lithology is carbonate, gradient is *lower* than a shale-equivalent section because carbonate thermal
conductivity (~2.8 W/mK) far exceeds shale (~1.8 W/mK). Getting this backwards inverts the conclusion.
4. **Source rock: present, absent, or unestablished.** This is the single highest-leverage unknown. Everything
else can be computed around it; without it nothing else matters.

## 3. The arithmetic

```
T_basal_section = T_seabed + (section_thickness_km × gradient_C_per_km)
kitchen_top_km   = (60 to 65 - T_seabed) / gradient       # oil onset
kitchen_peak_km  = (90 to 110 - T_seabed) / gradient      # peak oil
```

`T_seabed`: ~2–4 °C in deep water, ~25–28 °C on a tropical shallow platform — do not default to 0.

Windows: oil onset **60–65 °C**, peak oil **90–110 °C**, wet gas **110–150 °C**, dry gas **>150 °C**.
Compare the temperature at the *base* of the sedimentary section (below it there is only basement) against
the window. If the base sits below peak-oil temperature, the section is over-thick enough — but check whether
the prospective facies is that deep. If the base sits *under* the window, no amount of trap or seal geometry
saves it.

Worked comparison and a decision table: `references/charge-screening-arithmetic.md`.

## 4. Two independent failure modes — name which one you have

Charge fails for two reasons that do not overlap, and stating both keeps the verdict sturdy:

- **No generative section.** Shallow-water, oxygenated platform facies do not preserve organic matter. That is
  *why* it is a platform and not a basin — the same reason it is a good reservoir is the reason it is a bad
  source. Periplatform drift and ooze can carry organic carbon but are typically too young and too shallow.
- **No burial.** Thin section over thick, cool, thermally conductive crust never reaches the window, regardless
  of what the source rock would have been.

Naming both is what makes the answer falsifiable. "Cannot cook" is stronger than "unproven" when both hold:
the first failure alone would be a gap in knowledge, but thin-section-over-thick-crust is thermodynamic.

## 5. Timing is separate from maturity

A section can be mature and still fail if charge arrived after trap formation. Maturity answers *can it cook*;
charge-versus-trap synchrony answers *did it fill*. Answer the asked question first, then state the timing
gap explicitly rather than implying maturity settles it.

## 6. Use negative analogs as evidence, not as colour

A neighbouring area on the same ridge, same crustal trend, and same depositional system with a large number of
dry wells and zero commercial discovery is **thermodynamic evidence**, not bad luck and not sparse coverage.
Cite the well count and the maximum depth reached. Do not discount it because the neighbouring area is a
different jurisdiction — continuity of crust is the point.

Equally: an on-trend analog producing gas elsewhere does not transfer. Check whether that analog has a
kinematically different crustal or heat-flow setting before borrowing its outcome.

## 7. Gate frontier prospectivity claims at the source

Statements of the form "studies show a high probability of oil" in frontier areas frequently trace back to a
conference presentation, a consultant deck, or a non-geoscientist author. Before repeating one:

- Trace it to the primary document and identify who wrote it and in what capacity.
- A claim that has upgraded from "indication" to "study" to "basis for policy" without new data is claim
  laundering. Name it as such and cap your own confidence accordingly.
- Positive indicators that are real and worth citing: pockmarks releasing methane and ethane, documented source
  rock near a named feature, crust reclassified from oceanic to transitional, a specific drilled well result.
- Indicators that are **not** charge evidence, however often they are invoked: total EEZ area, number of
  islands, proximity to a shipping lane, existing refineries, or a national oil company's global portfolio.

## 8. Reporting shape

Verdict line first. Then the four inputs with their sources. Then the arithmetic. Then the two failure modes.
Then what would change the answer (a well that penetrates below current total depth, a source-rock analysis, a
reprocessed heat-flow model). Say plainly when the answer is "nothing in the published record changes it".

Never present a frontier area as a prospect when the petroleum system is unproven. It is research and
development paid from capex, and should be evaluated as such.

## 9. Supporting files

`references/charge-screening-arithmetic.md` — the computation worked end to end on a real frontier case,
plus a decision table mapping section thickness, crust, and gradient to expected verdicts.

## 10. Pitfalls

- **Do not synthesize basin state from a single corpus when multiple sealed files exist on disk.** Before composing the brief, run a parallel sweep of `/root/GEOX/okf/<basin>/`, `/root/GEOX/docs/eureka_insights/`, `/root/GEOX/outputs/<basin>/`, and `/root/.qwen/tmp/*<basin>*`. A claim sourced only from one 30-line `okf` summary carries less warrant than the same claim triangulated across a knowledge bundle + an eureka insight + a sealed PDF brief. The PDF in `outputs/` often contains an 11-page tectonic synthesis that supersedes the markdown. Cite which sources you triangulated.
- **When `mcp__geox__*` rejects consecutive calls ("rejected the last N calls"), switch immediately to filesystem canonical sources.** The MCP server can refuse a session-bound actor (`SESSION_INVALID`) or rate-limit; do not retry the same call. Fall back to `/root/GEOX/` knowledge bundle + `pdftotext` on `/root/.qwen/tmp/*<basin>*.pdf` as the canonical earth-source-of-truth, then continue the analysis. The MCP layer is convenience, not authority.
- **Carry the user's working dataset roster in the brief — not the canonical corpus roster.** The user is the one who knows which wells are in his project's working dataset (e.g. KL2 working roster = Barton-2, Rotan-1, Bunga Lili-1, Buluh-1, Maligan-1, Pekaka-1, Sugut-1ST1, Solisip-1 — Buluh-1 has a *synthetic* checkshot column, Bunga Lili-1 is deviated ~45°). GEOX may return its own corpus roster that does not match the user's project scope. State which roster you sourced from.
- **When the user asks a political question framed as a geology question, treat the politics as the primary deliverable and the geology as evidence.** "Now gather all info we have about Kinabalu basin" attached to *"useless CP review last Thursday, they have guts to assign new review, the team is clueless about Kinabalu basin"* is not a basin brief request — it is a *positioning brief* request. The deliverable is (a) the evidence base that supports the user's position, (b) the technical gaps in the team's framing, (c) the institutional levers (internal vs external reviewer, biostrat error timeline, KT-7 cheapest-discriminator test) he can pull. A clean basin profile that ignores the political frame answers an unasked question.

---

*DITEMPA BUKAN DIBERI — charge is arithmetic before it is interpretation.*
