---
name: artifact-emission-pipeline
description: Generate human-facing artifacts (PPT, PDF, HTML) from agent reasoning. Edge bridge reality transport layer — converts machine cognition into objects that survive outside the chat session. PptxGenJS + weasyprint + Gemini image gen pipeline.
version: 1.0.0
triggers:
  - generate a PPT, PPTX, or PowerPoint presentation
  - generate a PDF from agent reasoning or structured content
  - create a downloadable artifact for arif-fazil.com
  - user says "make a deck" or "build a presentation"
  - user says "emit an artifact" or "create an object"
  - convert structured analysis into a presentation format
autonomy_tier: T1
floor_scope: [F1, F2, F4, F7]
---

# Artifact Emission Pipeline — Edge Bridge Reality Transport

> DITEMPA BUKAN DIBERI — Artifacts are forged, not narrated.

## Core Doctrine (Forged 2026-08-13)

> **"Chat ialah permukaan. PPT/PDF ialah objek."**

A Hermes edge bridge that can only chat is **incomplete**. The bridge must emit objects that:
1. **Survive outside the chat** — a visitor understands without talking to Hermes
2. **Carry meaning independently** — no context required
3. **Are editable by humans** (PPT) or **fixed as attestation** (PDF)
4. **Pass the 3-second test** — human grasps the core message in 3 seconds

The architecture:

```
Reasoning → Structure → Artifact → Human institution acts
         (not)  → Chat → Nothing
```

## The Two Artifact Classes

| Class | Format | Peranan | Sifat |
|---|---|---|---|
| **Coordination Object** | PPT/PPTX | Jemput manusia masuk loop — boleh edit, argue, decide | Mutabel |
| **Witness Object** | PDF | Attestation — fixed, portable, archivable, signable | Immutable |

**PPT = ruang rundingan. PDF = titik attest.**

## Vocabulary Discipline at Boundary (Arif correction 2026-08-13)

**NEVER** use internal arifOS governance vocabulary in public-facing artifacts. Terms like `WITNESS REQUIRED`, `888_HOLD`, `SEAL`, `F1–F13` are internal. Replace with human-readable equivalents:

| Internal | Public | Reason |
|---|---|---|
| `WITNESS REQUIRED` | `NOT EVERYTHING SHOULD BE CLOSED` | No authority claim without evidence |
| `888_HOLD` | `PENDING REVIEW` | Opaque to outsiders |
| `SEAL` | `Published` / `Attested` | False legal implication |

**Iron rule:** *"If a stranger reads only this artifact, does every word mean what it appears to mean?"*

## Genre Declaration (Arif correction 2026-08-13)

Every artifact must declare what it IS and what it is NOT before the reader encounters the content. A framing sentence above the title changes the entire reading:

> "This is not an incident report. It is a reflection on how institutions remember outcomes while individuals remember consequences."

**Why:** Genre ambiguity is a flaw, not a feature. If the artifact sits between personal testimony and public institutional document without declaring which, the reader invents their own frame — and may infer things you never stated.

**Formula:** `"This is not {wrong genre}. It is {right genre}."`

## Pipeline: PPT via PptxGenJS

### Setup

```bash
npm install pptxgenjs  # one-time, in project dir or globally
```

### Architecture

```
Node.js script → PptxGenJS API → .pptx (OOXML)
                                   ↓
                          No PowerPoint install required
                          Works: PowerPoint, Keynote, LibreOffice, Google Slides
```

### Design tokens pattern

```javascript
const COLORS = {
  bg: "0D1117",        // deep near-black
  surface: "161B22",   // card surface
  oil: "D4A574",       // domain accent (amber)
  scar: "C44545",      // emphasis/error (red)
  bone: "8B949E",      // dimmed text
  text: "E6EDF3",      // primary text
  textDim: "8B949E",   // secondary text
  line: "30363D",      // dividers
};
```

### Slide master pattern

```javascript
pres.defineSlideMaster({
  title: "CUSTOM_MASTER",
  background: { color: COLORS.bg },
  objects: [
    // Top accent line
    { line: { x: 0.0, y: 0.0, w: "100%", h: 0.04, line: { color: COLORS.oil, width: 2 } } },
    // Footer text (use human-readable, NOT internal sigils)
    { text: { text: "NOT EVERYTHING SHOULD BE CLOSED", options: { ... } } },
  ],
  slideNumber: { ... },
});
```

### Key patterns

- **Images:** `slide.addImage({ path: "file.png", x: 0, y: 0, w: 10, h: 5.6, sizing: { type: "cover" } })`
- **Tables:** `slide.addTable(rows, { colW: [...], rowH: [...], border: { ... } })`
- **Shapes:** `slide.addShape(pres.ShapeType.roundRect, { ... })`
- **Scar lines (visual):** Dashed horizontal line for emphasis/divider

### Pitfall: PptxGenJS image integration

Image generation (Gemini) may run async. Check file exists BEFORE generating PPTX:

```javascript
const fs = require("fs");
const imgPath = path.join(__dirname, "image.png");
if (fs.existsSync(imgPath)) {
  slide.addImage({ path: imgPath, ... });
}
```

Regenerate PPTX after image is ready — the script is idempotent.

## Pipeline: PDF via HTML → weasyprint

### Setup

```bash
# weasyprint usually pre-installed; if not:
pip install weasyprint
```

### Pattern

```html
<style>
  @page { size: A4 landscape; margin: 0; }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  :root {
    --bg: #0D1117;
    --oil: #D4A574;
    /* ... same design tokens as PPTX ... */
  }
  .slide {
    width: 297mm; height: 210mm;
    padding: 20mm 25mm;
    page-break-after: always;
    position: relative;
  }
</style>
```

```bash
weasyprint output.html output.pdf
```

### Pitfall: local image references

Weasyprint resolves `url('file.png')` relative to the HTML file. Place images in the same directory. Background images via CSS work:

```css
.cover {
  background-image: linear-gradient(rgba(13,17,23,0.65), rgba(13,17,23,0.95)),
                    url('rig-silhouette.png');
  background-size: cover;
}
```

## Image Generation (Gemini)

```bash
python3 /root/HERMES/scripts/gemini-image.py "prompt text" --output output.png
```

**Note:** The `prompt` is a positional argument, NOT `--prompt`. The `--prompt` flag will cause an error.

## SHA-256 Sealing

After generation, seal all artifacts:

```bash
sha256sum *.pptx *.pdf *.png | tee artifacts.sha256
```

## Publication Gate (Arif correction 2026-08-13)

Before publishing to arif-fazil.com, the artifact must pass:

1. **Genre declaration** — framing sentence above download
2. **Vocabulary check** — no internal sigils
3. **Standalone test** — reader understands without chat context
4. **Evidence proportionality** — authority of language must match evidence present (no witness language without witness material)
5. **apex-judge** for public homepage; personal essays section for reflection-grade artifacts

### Publication verdict taxonomy

| Verdict | Meaning |
|---|---|
| **SEAL** | Ready for personal essays section |
| **HOLD** | Not ready for public homepage — needs context/framing |
| **VOID** | Wrong genre or insufficient evidence for claimed authority |

## Templates (in this skill's `templates/` directory)

- **`templates/forgotten-well-style-dark.pptx.js`** — Drop-in PptxGenJS template using the dark amber-scar palette. Pre-configured slide master, color tokens, scar-line helper, cover layout with framing sentence slot. Copy and modify for new scar/reflection-grade decks.
- **`templates/scar-pdf-weasyprint.html`** — A4 landscape HTML scaffold ready for `weasyprint`. Dark theme, cover with background image, footer text, table styles, scar-line dividers. Rename sections, add slides, point at local image files.

## Reference: Scar-Document Pattern (Session 2026-08-13)

"The Cost of a Forgotten Well" — the first artifact emitted by Hermes edge bridge:

- **PPTX:** `/root/forge_work/artifacts/forgotten-well/The-Cost-of-a-Forgotten-Well.pptx`
- **PDF:** `/root/forge_work/artifacts/forgotten-well/The-Cost-of-a-Forgotten-Well.pdf`
- **Script:** `/root/forge_work/artifacts/forgotten-well/generate-pptx.js`
- **HTML:** `/root/forge_work/artifacts/forgotten-well/The-Cost-of-a-Forgotten-Well.html`
- **Image:** Gemini-generated rig silhouette
- **SHA-256:** Sealed in `artifacts.sha256`
- **Verdict:** HOLD for public homepage, SEAL for personal essays (positioned as reflection, not investigation)

Lessons from this artifact:
1. Framing sentence is mandatory ("This is not an incident report...")
2. Internal vocabulary leaked on first attempt — caught by Arif at editorial review
3. Genre ambiguity is a flaw — artifact must declare what it is and isn't
4. Authority of language must match evidence present
5. PPT is coordination object (for humans to edit/argue); PDF is witness object (fixed attestation)
