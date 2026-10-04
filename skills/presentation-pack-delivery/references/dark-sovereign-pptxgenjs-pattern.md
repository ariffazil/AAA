# Dark Sovereign — PptxGenJS + WeasyPrint Pattern (Verified 2026-08-13)

Proven on "The Cost of a Forgotten Well" — 6-slide scar-ledger deck, 1540 KB PPTX + 1.3 MB PDF.

## Design Tokens (PptxGenJS)

```javascript
const COLORS = {
  bg: "0D1117",        // deep near-black
  surface: "161B22",   // card surface
  oil: "D4A574",       // warm amber (petroleum/accent)
  scar: "C44545",      // scar red (semantic: unresolved, risk)
  bone: "8B949E",      // bone grey (dimmed, secondary)
  truth: "7EE787",     // truth green (positive state)
  text: "E6EDF3",      // primary text
  textDim: "8B949E",   // dimmed text
  line: "30363D",      // divider/border
};
```

Palette family: GitHub-dark. Swap `oil` accent per organ if needed (WEALTH=gold, GEOX=teal, arifOS=amber).

## Slide Master Pattern

```javascript
pres.defineSlideMaster({
  title: "SOVEREIGN",
  background: { color: COLORS.bg },
  objects: [
    // Top accent line
    { line: { x: 0.0, y: 0.0, w: "100%", h: 0.04, line: { color: COLORS.oil, width: 2 } } },
    // Bottom-right watermark — HUMAN-LANGUAGE, not internal governance sigils
    { text: { text: "NOT EVERYTHING SHOULD BE CLOSED", options: {
      x: 7.6, y: 7.0, w: 2.4, h: 0.25,
      fontSize: 7, color: COLORS.textDim, align: "right", fontFace: "Consolas", charSpacing: 1
    }}}
  ],
  slideNumber: { x: 0.3, y: 7.0, w: 0.5, h: 0.25, fontSize: 7, color: COLORS.textDim, fontFace: "Consolas" },
});
```

### ⚠️ Boundary Vocabulary Translation (Forged 2026-08-13)

**Never use internal arifOS governance sigils in human-facing artifacts.** The first version of this pattern used `"WITNESS REQUIRED"` — an arifOS internal command for the agent governance layer. To a human reader it reads as authoritative attestation language on an artifact that contains no evidence. That is *false authority*.

| Internal sigil | Human meaning | What the reader infers |
|---|---|---|
| WITNESS REQUIRED | "someone must attest this" | Official investigation with evidence |
| HOLD | unresolved governance state | Something is being covered up |
| SEAL | constitutional closure | Legal-grade attestation |

**Rule:** Translate every internal term at the boundary. If the artifact is a reflection, the footer should say so in human language — not in agent language that implies a different genre.

Arif's verdict: *"WITNESS REQUIRED" without evidence = implied accusation.*

## Scar Line Helper

```javascript
function scarLine(slide, x, y, w) {
  slide.addShape(pres.ShapeType.line, {
    x, y, w, h: 0,
    line: { color: COLORS.scar, width: 1.5, dashType: "dash" }
  });
}
```

## Cover Image Embedding (PptxGenJS)

```javascript
const fs = require("fs");
const rigImg = path.join(__dirname, "rig-silhouette.png");
if (fs.existsSync(rigImg)) {
  s1.addImage({ path: rigImg, x: 0, y: 0, w: 10, h: 5.6, sizing: { type: "cover", w: 10, h: 5.6 } });
}
// Semi-transparent overlay to keep text readable
s1.addShape(pres.ShapeType.rect, {
  x: 0, y: 0, w: 10, h: 5.6, fill: { color: COLORS.bg, transparency: 35 }
});
```

## WeasyPrint Cover with Background Image

HTML/CSS technique for PDF cover slides with embedded imagery:

```css
.cover {
  background-image:
    linear-gradient(rgba(13,17,23,0.65), rgba(13,17,23,0.95)),
    url('rig-silhouette.png');   /* relative path — must be in same dir as HTML */
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}
```

**Pitfall:** WeasyPrint ignores `print-color-adjust: exact` — suppress the CSS property or live with the warning. It does NOT break rendering.

## A4 Landscape @page for WeasyPrint

```css
@page { size: A4 landscape; margin: 0; }
```

No margin on slide pages. Set padding in `.slide` class instead for edge control.

## SHA-256 Attestation Pattern

```bash
sha256sum The-Cost-of-a-Forgotten-Well.pptx The-Cost-of-a-Forgotten-Well.pdf | tee artifacts.sha256
```

Always seal artifact hashes. Prevents silent mutation if served from a web surface.

## File Sizes (verified)

| Artifact | Size | Notes |
|---|---|---|
| PPTX (6 slides, 1 embedded image) | 1.6 MB | OOXML bundle |
| PDF (6 slides, 1 embedded image) | 1.3 MB | WeasyPrint output |
| HTML source | 9 KB | Readable, maintainable |
| rig-silhouette.png | 1.4 MB | Gemini-generated |

## Full Script

Source: `/root/forge_work/artifacts/forgotten-well/generate-pptx.js`
HTML: `/root/forge_work/artifacts/forgotten-well/The-Cost-of-a-Forgotten-Well.html`
