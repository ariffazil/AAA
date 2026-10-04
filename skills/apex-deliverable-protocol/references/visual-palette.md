# Apex visual palette — semantic colour mapping

One colour = one meaning. No exceptions across the document.

## Core palette

| Colour | Hex | Meaning | Use |
|---|---|---|---|
| Navy | `#0e1a2b` | Observed data | Bar fills, primary data lines, heading accents |
| Gold | `#c9a227` | Derived model / median | Scenario median lines, model output, KPI accents |
| Red | `#c0392b` | Risk threshold / invalidation | Invalidation lines, risk zones, failure paths |
| Green | `#1e8449` | Upside scenario | Upside scenario lines, positive fills, confidence ≥60% |
| Orange | `#e67e22` | Adverse countercase | Failure scenario lines, countercase box borders, confidence <60% |
| Grey | `#7f8c8d` | Neutral context | Source notes, axis labels, baseline references |

## Rules

1. Same colour must never mean different things across charts in the same document.
2. Chart titles encode falsification tests inline. Title = [ClaimID] [epistemic tag] · topic · Falsify: test.
3. Confidence ≥60% → green chip. <60% → orange chip. No yellow middle ground.
4. Backgrounds: verdict boxes = navy with gold text; countercase boxes = orange-tinted with orange border; three-lane blocks = gold (signal), blue (evidence), red (implication).
