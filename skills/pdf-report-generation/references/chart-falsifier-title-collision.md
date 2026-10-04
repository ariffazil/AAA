---
description: Chart title / falsifier text collision pitfall — discovered 2026-08-07 Apex v2 render. Keep titles ≤120 chars; falsifier text goes in HTML chart-caption paragraph.
---

# Chart Title vs Falsifier-Encoding Collision (2026-08-07)

## The problem

When encoding the falsification test into the matplotlib chart title, the long text pushes into the legend area and overlaps — both visually and in WeasyPrint PDF rendering.

**Failed title (too long):**
```
C-01 [OBS base · DER scenarios] · Brent Path — 3-Scenario Fan · Falsify: $60 breach by Sep 1 = demand-collapse base; $95+ by Sep 1 = Iran-strike upside
```
= ~175 chars → legend collisions, title unreadable in PDF.

**Correct title (≤120 chars):**
```
C-01 [OBS] · Brent Path — 3-Scenario Fan
```
= 42 chars. Clean, scannable, no overlap.

## Where falsifier text goes instead

In the **HTML chart-caption paragraph** that sits below the `<img>` in the HTML report:

```html
<div class="chart-section">
  <img src="charts_v2/01_brent_fan.png" alt="Brent 3-scenario fan">
  <div class="chart-caption">
    C-01 / C-02 — Brent path. Falsify marker on each band. Gold line = base path;
    green = upside (Iran re-strike); orange = failure (China demand).
    <strong>Falsify:</strong> $60 breach by Sep 1 = demand-collapse base;
    $95+ by Sep 1 = Iran-strike upside.
  </div>
</div>
```

The caption carries: topic + epistemic tag + claim ID + falsifier. The chart title carries: topic + epistemic tag + claim ID (no falsifier).

## Why this works

The caption is rendered as a separate paragraph after the image — enough vertical space, no overlap with the legend. It's readable in both PDF and HTML. The matplotlib title stays clean.

## Rule

| Element | Contains | Max length |
|---|---|---|
| Matplotlib title | `C-XX [EP] · Topic — Variant` | ≤120 chars |
| HTML chart-caption | `C-XX — detail. Falsifier:` + test + epistemic tag | No limit |
| Chart-label in legend | Series name + weight | 20 chars |

The falsification test belongs to the human-reading path (caption), not the chart-title path (which competes for vertical space with the legend block).
