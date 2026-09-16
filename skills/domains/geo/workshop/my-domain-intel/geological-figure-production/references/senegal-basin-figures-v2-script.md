# Senegal Basin — Session Reference (2026-08-20)

Concrete lessons from the Senegal Basin PSM + 7-figure deliverable session. Use as a worked example when producing figures for any basin — replace data, keep the structure.

## Files produced this session (template copy)

- `/tmp/senegal_figs_v2/` — final figures (7 PNGs, ~440 KB each)
- `/tmp/build_all_figures_v2.py` — generator script (single-file, all 7 figures)
- `/tmp/build_fig1_v4.py` — strat column with non-overlapping rows
- `/tmp/build_fig3_v2.py` — cross-section with NaN-safe seabed
- `/tmp/build_fig4_v2.py` — block map with corrected basin orientation
- `/tmp/build_fig5_v2.py` — risk heatmap with margin labels
- `/tmp/build_final_figures_dossier.py` — weasyprint HTML→PDF assembler

## Iterations made

| Version | What changed |
|---|---|
| v1 (initial 7 figures) | First cut: many bugs — strat column overlap, cross-section NaN, block map wrong basin orientation, risk labels collided |
| v2 (mid session) | Seabed fixed with `np.sin`-based profile; cross-section salt+struct visible |
| v3 (final) | Strat column rebuilt with evenly-spaced rows; risk heatmap with leader lines to margin; block map redrawn WNW-ESE; cover page clean |

## Key takeaway

- 3 figure generations = ~20 vision_analyze calls
- Vision QA found issues that matplotlib "rendered successfully" without flagging
- Code review cannot catch label collisions; vision model catches everything

## Real data used (for any basin doing similar work)

- 12 stratigraphic units: Cenozoic → Upper Triassic
- 11 horizon points along burial curve from 200 Ma to present
- 7 PSC blocks with working interests ~30-60%
- 12 wells drilled 2014-2020 (SNE-1 etc.)
- Two main discoveries: Sangomar (~560 MMbo oil), Tortue (~15 Tcf gas)
- Two main operators: Woodside (oil), bp/Kosmos (gas)

## Truth bounds (epistemic discipline)

- Reservoir properties (porosity, perm) from Sangomar well disclosures — **OBS**
- Source rock TOC, HI, Ro ranges from regional synthesis + literature — **INT**
- Block geometry / cross-section geometry — **SCHEMATIC**
- Discovery reserves from operator press releases — **OBS**
- Risk positions are interpreter judgment — **INT**

Never present uncalibrated values as facts; always tag the band.
