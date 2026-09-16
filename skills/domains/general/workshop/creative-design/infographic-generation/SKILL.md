---
name: infographic-generation
description: "Shareable data infographics. HTML+Chrome prose, mpl charts."
version: "1.0"
author: "hermes-curator"
license: "MIT"
metadata:
  hermes:
    tags: [infographic, visualization, propaganda, public-communication]
    related_skills: [civic-intelligence-pdf, scientific-pdf-generation]
triggers:
  - "build infographic"
  - "infographic for the public"
  - "reality infographic / anti-propaganda graphic"
  - "data visualisation poster"
  - "one-image explainer"
---

# Infographic Generation

> **Trigger:** User wants a single shareable image (PNG) that explains data to a general audience in ~30 seconds — an infographic, graphic explainer, or "reality vs propa" poster. NOT a multi-page PDF (use `civic-intelligence-pdf` for those) and NOT an academic figure (use `scientific-pdf-generation`).

## Two rendering paths — pick by content type

| Content | Tool | Why |
|--------|------|-----|
| **Prose in cards/boxes/callouts** (status cards, reality-vs-propa blocks, body text) | **HTML + flexbox/grid + CSS auto-wrap → Chrome headless** | matplotlib `text()` does NOT wrap; long body text overflows off-canvas (verified 2026-08-31). |
| **Standalone charts only** (bars, lines, donut) | matplotlib, saved as PNG, embedded as `<img src="file:///...">` | Clean axes, data labels, annotations. |

**Rule of thumb:** if the graphic has more than ~2 lines of running prose, use the HTML path. Reserve matplotlib strictly for the numbers.

## Path A — HTML + Chrome headless (preferred for prose infographics)

Single HTML file with inline CSS, `width:1080px` on `<body>`, then:

```bash
google-chrome --headless --disable-gpu --no-sandbox --hide-scrollbars \
  --window-size=1080,3400 --default-background-color=FFFFFFFF \
  --screenshot=/path/out.png "file:///path/infographic.html"
```

- Chrome auto-wraps text inside flex/grid cards — no overflow, no manual line-breaking.
- Set `--window-size` height generously (3400 for a tall poster); Chrome crops to content but a tall window prevents clipping.
- Embed charts with `<img src="file:///absolute/path/chart.png" style="width:100%">`.
- Box-sizing: `* { margin:0; padding:0; box-sizing:border-box; }` and a `body { width:1080px; margin:0 auto; }` wrapper.

## Path B — matplotlib

For standalone bars/line/donut. Full working chart generators live in `scripts/` (see pointer below).

## Honest-chart rules (anti-propaganda)

These are non-negotiable when the graphic is "for the rakyat" or fact-checks someone else's claim:

1. **Y-axis from 0.** `ax.set_ylim(0, ...)`. The #1 propaganda tell is a non-zero floor (e.g. start at 100) that makes modest growth look like a cliff. A bar chart cut off low is a lie.
2. **Label the floor explicitly** so the reader trusts the scale.
3. **Show the downturn, not just the recovery.** Cherry-picking a "nice" window (e.g. showing only the +8% recovery while omitting that it's still below the prior peak) is omission-propaganda. Annotate the peak and the dip.
4. **Don't hide the operative contradiction.** If the story is "company holds RM204B cash," the graphic must also surface the contradicting fact (e.g. same company borrowed for capex) — otherwise it's a half-truth.
5. **Cite sources inline** at the bottom. A "for the public" graphic with "angka aku" will be dismissed.

## Propaganda-by-omission detection frame

When validating a third-party chart/page, ask: *is the number true, or is the chosen story true?* "Correct numbers, chosen story" = framed, not falsified. Detection signals (check in this order):

- **Y-axis floor** — does the axis start at 0? (cheapest check, biggest tell)
- **What's omitted** — dividend, debt, worker cuts, the peak it's below, etc. What number would break the story?
- **Category error** — conflating a corporate balance-sheet asset with national revenue (e.g. "company's cash = 60% of the federal operating budget" — you cannot fund a state from a company's cash without it being an extraction).
- **Morality tale padding** — a past crisis framed as "handled responsibly" to launder a repeated pattern.

## Reusable assets

- `templates/reality-infographic.html` — proven propa-vs-reality card layout (header, ❌ propa card, ✅ reality cards grid, honest chart embed, truth banner, sources footer). Copy and modify; don't rewrite from scratch.
- `scripts/make_honest_bar_chart.py` — matplotlib bar chart with y-axis from 0, peak/dip annotations, honest data-label caption. Generates the embeddable chart PNG.

## Pitfalls

- **matplotlib text doesn't wrap** → use HTML path for prose (see Path A).
- **Chrome `--screenshot` is viewport-height sensitive.** On a very tall poster, use a tall `--window-size` and verify with a vision pass before sending — check right edge and bottom for clipping.
- **Default Chrome window-size height (800/1080) will crop tall graphics.** Always raise it.
- **Always do a vision_analyze pass after render** to catch overflow/cut-off before delivering to a public group. Layout bugs are invisible in code.

## Verification

1. `vision_analyze` the output PNG — confirm no text overflows right/bottom edges, all cards readable, chart labels legible.
2. Check the y-axis floor is 0 (if a bar chart).
3. Confirm sources footer present.
4. Deliver via `MEDIA:/path/image.png`.
