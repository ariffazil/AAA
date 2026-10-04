# Semantic Chart Grammar — Unified Colour by Role

Proven 2026-08-07 on the Arif weekly brief v2. The key insight: the old `build_charts.py`
used the federation palette (NAVY/GOLD/RED/GREEN/BLUE/ORANGE) decoratively — different
charts used the same colour to mean different things. v2 unified the palette across all
charts by semantic role.

## The binding palette

| Role | Hex | Meaning | Use for |
|------|-----|---------|---------|
| `ROLE_OBSERVED` | `#7a7a7a` (neutral grey) | Past or current observed world state | Historical bars, past-line data, trend tails |
| `ROLE_DERIVED` | `#0e1a2b` (navy) | Math the analyst did — models, subsidy bills, scenarios | Subsidy curve, derived metrics, model lines |
| `ROLE_FORECAST` | `#c9a227` (gold) | Forward-looking estimate | Forecast paths, present-state markers (gold dot + navy edge), future bars |
| `ROLE_RISK` | `#b3261e` (red) | Downside / invalidation line | Invalidation thresholds (dashed red), bear-scenario lines, loss fills |
| `ROLE_OPP` | `#2e7d32` (green) | Upside / opportunity zone | Bull-scenario lines, gain fills, opportunity thresholds |
| `ROLE_PAST` | `#9aa1ac` (softer grey) | Trailing historical data only | Trailing bars vs present bar |
| `ROLE_PRESENT` | `#0e1a2b` (navy) | Today's value | Current day bar (navy), present state marker |

## Key invariants

1. **One role, one colour, all charts.** If navy means "derived" in chart 1, it means "derived"
   in chart 10. Never use navy for "historical" in one chart and "model" in another.

2. **Invalidation is always dashed red.** Every chart that has a thesis-level falsification
   threshold uses a red dotted/dashed line labelled "Invalidation · RISK".

3. **Present state = gold dot with navy edge.** The single most important data point on
   each chart — today's number — gets a large gold scatter point (120-180pt s=) with
   navy edgecolor, so it stands out without being red/green.

4. **Scenario lines carry role colour, not entity colour.** "Bull scenario" = green line.
   "Bear scenario" = red line. "Base scenario" = navy line. Never colour scenarios by
   asset name.

5. **Fill regions carry role colour, not decorative colour.** Positive fill = green (OPP).
   Negative fill = red (RISK). Neutral fill = grey (OBSERVED). Never use decorative
   colour for regions that carry judgment.

6. **Bar charts: past = grey, present = navy, forecast = gold.** When a bar chart shows
   past + present + future, the time-sequence colour is grey → navy → gold. Never use
   the same colour for past and present bars.

7. **Directional colour in bar charts (YTD, returns):** Positive = green, negative = red.
   This overrides the time-sequence rule when the semantic meaning is gain/loss.

## Worked example — subsidy paradox (C01)

```python
# Subsidy paradox — Brent (x) → dividend + subsidy + net (y)
ax.plot(brent, div, color=ROLE_DERIVED, ...)  # Navy = derived model
ax.plot(brent, subsidy, color=ROLE_RISK, ...)  # Red = risk curve
ax.fill_between(..., where=net<0, color=ROLE_RISK, ...)  # Red fill = fiscal loss
ax.fill_between(..., where=net>=0, color=ROLE_OPP, ...)  # Green fill = fiscal gain
ax.scatter([83.85], [...], color=ROLE_FORECAST, ...)  # Gold dot = present spot
ax.axvline(78.5, color=ROLE_RISK, linestyle=":", ...)  # Dashed red = invalidation
```

## Pitfall: `fill_between` with numpy bool arrays

Pyright flags `NDArray[numpy.bool[builtins.bool]]` as incompatible with the `where`
parameter of `fill_between`. This is a type-checker false positive — matplotlib accepts
numpy boolean arrays at runtime. Suppress with `# type: ignore` or cast to `.tolist()`.
Not a real bug.

## Pitfall: legend bbox_to_anchor warnings

The old `pyrolite.mplstyle` has a stale `legend.bbox_to_anchor` key. Harmless warning —
just suppress with `plt.legend()` (no bbox override) or accept the warning line.
