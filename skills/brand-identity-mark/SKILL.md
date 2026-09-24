---
name: brand-identity-mark
description: "Design marks with specific typography. Use for logo briefs."
version: 1.0.0
owner: Hermes
risk_tier: low
tags: [logo, monogram, wordmark, badge, agent-identity, brand, svg, heraldic, image-gen]
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# Brand Identity Mark — Hand-Crafted Path

For any request to design a logo, monogram, badge, emblem, or identity mark that must contain
**specific letters or a specific wordmark**. Covers shields, wings, crests, and freeform heraldic —
not circular Arabic marks (see `circular-mark-and-arabic-typography`).

## The one rule

**Diffusion image-gen cannot honour exact letterforms.** `mmx image generate --model image-01`,
DALL·E, Stable Diffusion all treat the prompt as a mood-board; they pick plausible-looking letters,
not specified ones. Across three iterations of the same prompt with the same seed, ARIF + IRFAN
came back as "ATPF", "TAR", or partial "AR" with N missing. The model will trade unspecified
elements (claws, star, accent colour) to fit the substituted letters.

**Default to hand-crafted SVG for any mark with specific typography.** Use diffusion only when
the brief is mood/illustration and the letters are decorative, not literal.

## Procedure

### Step 1 — Identify the typography contract

Before drawing, name the exact letters that must appear in the mark:
- Monogram (1–3 letters, e.g. AI, AR)
- Shared-letter merge (e.g. ARIF + IRFAN → I, R, F, A shared; N hinted)
- Wordmark (full name + accent, e.g. "arifOS")
- Sub-wordmark (small caption under the mark)

Write the contract as a checklist before any prompt or SVG.

### Step 2 — Pick the rendering path

| Brief | Path |
|---|---|
| Literal letters/wordmark required | Hand-craft SVG → `rsvg-convert` |
| Mood/atmosphere only, letters decorative | `mmx image generate` with `--seed` for reproducibility |
| Mix (e.g. abstract background + literal monogram) | SVG for the literal parts, compose with image-gen for the background |
| Iteration count expected > 3 | SVG from the start; image-gen will not converge on letterforms |

### Step 3 — SVG composition for shields / crests / wings

**Shield path** (anchor with cubic curves):

```svg
<path d="M 256 64
         C 360 64, 432 80, 432 80
         L 432 280
         C 432 380, 360 432, 256 448
         C 152 432, 80 380, 80 280
         L 80 80
         C 80 80, 152 64, 256 64 Z"
      fill="#1a2747" stroke="#4a5568" stroke-width="6"/>
```

**Clipping interior elements** so stripes do not bleed past the rim:

```svg
<defs>
  <clipPath id="shieldClip">
    <path d="...same shield path..."/>
  </clipPath>
</defs>
<g clip-path="url(#shieldClip)">
  <!-- diagonal stripes, claws, etc. -->
</g>
```

**Wings** as 3 stacked tapered strokes per side (top/middle/bottom feather), swept outward at
increasing angles. Each stroke = `<path>` with two cubic curves meeting at a point. Wings rendered
this way stay recognisable at 64 px; anatomically-detailed feathers disappear.

**Monogram letters** as explicit `<rect>` and `<line>` primitives:

```svg
<!-- I: vertical bar + top/bottom serifs -->
<rect x="-12" y="-130" width="24" height="220" fill="#fafaf5"/>
<rect x="-44" y="-138" width="88" height="14" fill="#fafaf5"/>
<rect x="-44" y="74" width="88" height="14" fill="#fafaf5"/>

<!-- A: two legs + crossbar -->
<line x1="-40" y1="0" x2="0" y2="-50" stroke="#ff7849" stroke-width="14" stroke-linecap="round"/>
<line x1="40" y1="0" x2="0" y2="-50" stroke="#ff7849" stroke-width="14" stroke-linecap="round"/>
<line x1="-26" y1="-22" x2="26" y2="-22" stroke="#ff7849" stroke-width="10" stroke-linecap="round"/>
```

For R/F/N as smaller accent glyphs, anchor with `<g transform="translate(x,y)">` and use
`<line>`/`<path>` primitives.

**Wordmark below the mark:**

```svg
<text x="256" y="490"
      font-family="Helvetica, Arial, sans-serif"
      font-size="42" font-weight="700" letter-spacing="6"
      text-anchor="middle" fill="#1a2747">arifOS</text>
```

Keep wordmark as one line for marks below 512 px wide. `letter-spacing="6"` to `"8"` reads as
distinctive at small sizes; `"12"`+ feels like a marketing deck.

### Step 4 — Render to PNG

```bash
rsvg-convert -w 1024 -h 1024 input.svg -o output.png
```

Sub-second, pixel-exact. Output is the SVG as-authored. No model interpretation.

### Step 5 — Verify

The SVG source is the truth — `<text>` content is exact by construction; `<rect>` coordinates
are deterministic. Use `vision_analyze` only for **composition** judgements (centring, clipping,
colour readability at small size). Do **not** trust vision's reading of *which* letter is where
when the SVG primitives are small — vision pattern-matches strokes into plausible glyphs and
will report "ATPF" for an I+A+R+F+N composition.

If the brief required exact typography, the verification is: SVG source matches the contract
checklist from Step 1. Not what vision says it sees.

### Step 6 — File under identity versioning

Path: `~/.hermes/identity/logos/<name>-v<n>.svg` and `<name>-v<n>.png`.

Older versions are provenance, not litter. A future session asking "what was the original logo
for X" gets the history, not a single canonical file. When a name changes (e.g. agent rename),
keep the old version files; the rename is the history, not the file.

## Pitfalls

- Believing the model will follow letterform specs after one prompt. It will not. After three
  prompts with stricter language, the model drops other specified elements to fit the substituted
  letters. Stop and switch to SVG.
- Trusting `vision_analyze` for *which* letters are in an SVG-rendered mark. Use it for
  composition only; assert the SVG source for typography.
- Putting thin calligraphic strokes in a 64 px target. Fatten with `stroke-width` ≥ 8 for
  small-letter accents.
- Centring by visual eye instead of measured mass centre. For non-symmetric marks (wings, claws),
  measure and adjust.
- Renaming / deleting old logo files when the identity changes. Keep them as provenance.
- Forgetting to clip interior elements to the shield. Stripes bleed past the rim and the mark
  loses its heraldic containment.

## Deliverable set

Per mark, produce:
1. SVG source — canonical, versioned.
2. PNG render at 1024 px (primary) and 512 px (platform standard).
3. Optionally: 256 px and 64 px renders for app-icon / avatar use.

Send one PNG and the SVG. Not six near-identical variants. Name the recommendation.
