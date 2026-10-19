---
name: forge-visual-design-system
description: Federation visual design system — palette, typography, layout primitives, slide masters, PDF cover templates. Load when creating ANY visual deliverable (slide deck, PDF briefing, branded asset) for the arifOS federation. Single source of truth to prevent palette drift across skills (powerpoint, pdf-report-generation, html-pdf-reporting). Class-level umbrella for visual identity across all media.
license: MIT
platforms: [linux, macos, windows]
---

# Federation Visual Design System

> **DITEMPA BUKAN DIBERI** — One palette. One voice. Every surface.
>
> **Purpose:** Stop every skill from inventing its own palette. PowerPoint decks use midnight+amber. PDF briefings use navy+gold. Branded assets use yet another cream. The federation visual identity drifts. This skill is the source of truth.

## When to load

**Always load BEFORE creating any visual deliverable for the federation:**
- Slide deck (uses `productivity/powerpoint`)
- PDF report / briefing (uses `productivity/pdf-report-generation` or `creative/html-pdf-reporting`)
- Branded medallion / avatar (uses `ai-media-generation-ops`)
- Essay / publication that needs visual identity (uses `essay-publish-pipeline`)

**Trigger phrases:** "make a deck", "create a presentation", "design a PDF", "federation slide deck", "branded asset", "deck about X", "presentation pack", "visual identity for federation".

**Do NOT load** for: arif-fazil.com web pages (use `arif-fazil-web-ops` with `forge-tailwind-tokens`), code-only deliverables, text-only artifacts.

## The Federation Palette (canonical)

One palette. Use it everywhere. Don't invent per-skill colors.

| Token | Hex | Role | When to use |
|---|---|---|---|
| **midnight** | `1A1F36` | Primary dark | Cover, closing, sovereign headers, dark sections |
| **midnight-lift** | `2D3454` | Secondary dark | Card backgrounds on dark, section dividers |
| **amber** | `D4A574` | Primary accent | Eyebrows, hairlines, accents on dark, "human/sensual" warmth |
| **amber-deep** | `B8845C` | Accent shadow | Borders, subtle hairlines, secondary amber |
| **cream** | `F5F1E8` | Primary light | Content backgrounds (sandwich structure) |
| **cream-deep** | `EAE3D2` | Secondary light | Card backgrounds on cream, dividers |
| **ink** | `1A1F36` | Body text on light | Same as midnight, for semantic clarity |
| **ink-soft** | `4B546B` | Muted text on light | Captions, subtitles, body on cream |
| **white** | `FFFFFF` | Text on dark | Body, headers on midnight |
| **muted** | `6B7280` | Footers, captions | Page numbers, footer meta |
| **hairline** | `C9C2B0` | Hairline rules | Dividers, separators on cream |
| **red** | `B85042` | Constitutional red | F13 veto, CAUTION, danger |
| **green** | `5C7A4F` | SEAL green | Confirmed, SEAL, success |
| **blue** | `2D5A7B` | Distinct blue | Where 8-cell grid needs variety, arifFlow accent |

**Cardinal rule:** midnight covers + closing (sandwich structure), cream for content slides in between.

**Avoid:** Per-skill invented palettes. Custom palette per deck. "Default to blue" anti-pattern.

## Typography

| Element | Font | Size | Weight |
|---|---|---|---|
| Slide title | Georgia | 44-54pt | bold |
| Section header | Georgia | 22-26pt | bold |
| Body text | Calibri | 14-16pt | normal |
| Eyebrow / kicker | Calibri / Consolas | 11-12pt | bold + charSpacing 6-8 |
| Captions / footer | Calibri | 10-12pt | normal, muted color |
| Mono / code | Consolas | 11pt | normal |

**Pairs:** Georgia (header) + Calibri (body) is the default. For constitutional / formal decks use Cambria + Calibri.

**Don't:** Arial Black + Arial (clichéd). Don't mix serif header with serif body.

## Layout Primitives

Use these consistently. Don't invent new shapes.

| Primitive | When | Spec |
|---|---|---|
| **Card** | Content block with background | white on cream, 6px shadow, 0.75px hairline border |
| **Callout** | Pinned quote, mission statement, axiom | midnight bg + amber accent + italic white text, full-width |
| **KPI hero row** | Top-of-deck 5-cell strip | flex row, big numbers (60-72pt), color-coded |
| **Accent stripe** | Card left edge, divider | 8px wide, palette accent color |
| **Hairline rule** | Section divider, top/bottom of slides | 2-3px, amber on dark, hairline on cream |
| **Eyebrow caption** | Above slide title | 11pt charSpacing 6-8, uppercase, amber-deep |
| **Icon in circle** | Number badge, section marker | 40-50px circle, palette color, white icon |
| **Pull quote** | Centered strong statement | Italic Georgia 22pt, 1.5em line, midnight bg |

**Sandwich structure:** dark (cover) → light (content) → dark (closing). Don't randomly mix.

## Slide Master Templates

Reference templates under `templates/`:

| Template | Purpose | File |
|---|---|---|
| **slide-cover-master.json** | Title/cover slide | `templates/slide-content-master.json` |
| **slide-content-master.json** | Content slide with eyebrow + title + body | `templates/slide-content-master.json` |
| **slide-grid-master.json** | Grid/card layout (4-col, 5-col) | `templates/slide-grid-master.json` |
| **slide-closing-master.json** | DITEMPA BUKAN DIBERI closing | `templates/slide-closing-master.json` |
| **pdf-cover.html** | PDF report cover | `templates/pdf-cover.html` |
| **pdf-body.html** | PDF body with KPI row + sections | `templates/pdf-body.html` |

Use `pptxgenjs` (Node.js) with these templates as JSON palettes → `pres.defineSlideMaster({ ... })` → consistent rendering across all decks.

## F2 Epistemic Labels (slide notes)

**Bind every slide's speaker notes to F2 TRUTH.** A slide carries claims; the notes carry the epistemic label.

```
[OBS]  Direct observation, measured, primary source
[DER]  Derived, computed from observations
[INT]  Interpreted, modeled, hypothesized
[SPEC] Speculative, uncalibrated
[UNKNOWN]  Missing evidence, gap to fill
```

Pattern (pptxgenjs):
```javascript
slide.addNotes("[OBS] arifOS :8088 port confirmed via curl /health at 2026-08-11. [DER] Federation port count = 8 organs. [INT] Constitutional weight aligns with mission gravity.");
```

For decks going to F13 SEAL: every slide note must carry at least one epistemic label. Auditors verify before ship.

## v1 → v2 Contrast Document Pattern (proven Aug 2026, Petronas)

When the user says "redo this deck" or "v2 of this PDF", don't silently fix. Build a separate contrast document:

```
/path/to/v2/contrast_v1_vs_v2.md
```

Structure:
1. **Coverage matrix** — which sections present in v1 vs v2
2. **Visual coherence radar** — palette, typography, layout consistency score
3. **Epistemic tag coverage** — % of slides/claims with F2 labels
4. **QA pass count vs fail count** — first iteration, second, etc.
5. **"Where I'm wrong" / "What's still thin"** — explicit gap acknowledgment, not silent self-defense

Contrast documents are F2 evidence, not apology. They make the redo auditable.

## Iteration Discipline — The Vision-Loop Trap

**Rule (proven 2026-08-11, arifOS deck):** Fix one issue per pass. Stop after one fix-and-verify. Re-flagged issues after a fix are usually noise, not new bugs.

Symptoms of the loop:
- Same defect flagged 2+ times after fix
- Vision re-flags edge-zone issues across iterations
- Critic finds "X overlaps" → fix → next pass "now Y overlaps" but Y was fine before
- You re-render the same slide 3+ times

**The trap:** LibreOffice renders text via different metrics than PowerPoint. Vision_analyze runs on LibreOffice-rendered JPGs. Phantom overlaps appear at edge zones that don't exist in source. Don't chase them.

**The fix:** fix flagged defect → ONE confirming pass on RAW PNG (not PDF page render) → ship. If phantom defects re-flag, accept and move on.

Verified on: arifOS constitutional deck (2026-08-11), 3 iterations on slide 1, all subsequent phantom flags were noise.

## Surface Availability (governance note)

| Skill | Hermes | AAA canonical | Other harnesses |
|---|---|---|---|
| `productivity/powerpoint` | ✅ | ❌ (mirrored from Hermes bundled) | ❌ |
| `productivity/pdf-report-generation` | ✅ | ❌ | ❌ |
| `creative/html-pdf-reporting` | ✅ | ❌ | ❌ |
| `aaa-pdf-voice-protocol` | ❌ | ✅ | ✅ |
| `forge-document-intelligence` | ❌ | ✅ | ✅ |
| `forge-visual-design-system` (this) | ❌ | ✅ | ✅ |

**Federation gap:** `powerpoint` is hermes-profile-only. Agents on OpenCode/Codex/Claude Code cannot load it without delegation. If you need PPTX from another harness, route through Hermes or wait for Stage 2 of the Zen upgrade (promote to AAA canonical). Loading it via AAA canonical first solves the gap.

## Cross-References

- `productivity/powerpoint` — the actual PPTX creation tool (load this too)
- `productivity/pdf-report-generation` — the actual PDF creation tool (load this too)
- `creative/html-pdf-reporting` — alternative HTML→PDF path
- `aaa-pdf-voice-protocol` — federation vocab → publication prose translation
- `forge-tailwind-tokens` — Trinity palette tokens for **web only** (this skill extends to slides/PDF)
- `ai-media-generation-ops` — Gemini/MiniMax image/video for branded assets
- `audit-recursive-audit` — visual contrast template lives here in Stage 3
- `seven-zen-organs-enforcement` — reflex arc to run on every visual deliverable

## Pitfalls (lessons from 2026-08-11)

1. **Emoji vs SVG glyph consistency** — pick ONE icon system per deck. Default: emoji. Mixing breaks visual register.
2. **Text box height for bold-large fonts** — auto-shrink compresses. Rule: h_inches ≥ pt/72 × lines × 1.3. Round up.
3. **Non-multiple grid centering** — 13 cards in 5 cols → center the last row (cols 1-3) so F13 doesn't strand.
4. **Vertical clearance below bold-large header** — descenders extend. Rule: gap ≥ 0.5" + header_pt × 0.005".
5. **Italic body charSpacing** — LibreOffice renders italic with extra perceived spacing. Use roman or tighter font for italic body.

## Templates

Templates under `templates/` are concrete starter files:
- `slide-cover-master.json` — palette + layout for title slides
- `slide-content-master.json` — eyebrow + title + body pattern
- `pdf-cover.html` — PDF report cover (dark theme)

Copy a template, modify the content, keep the palette/typography/layout. Resist per-deck invention.

---

*DITEMPA BUKAN DIBERI — One palette. One voice. Every surface.*
*Forged 2026-08-11 by Hermes-Prime · 333-AGI Δ MIND on F13 SOVEREIGN directive.*
*Lesson source: arifOS constitutional deck + Zen upgrade research session.*