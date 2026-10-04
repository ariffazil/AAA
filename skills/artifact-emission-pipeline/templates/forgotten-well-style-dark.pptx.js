// Template: Dark scar-document PPTX style
// Use: A reflection/essay-grade artifact with petroleum-human-reality framing
// Source: "The Cost of a Forgotten Well" — forged 2026-08-13

// AAA is an ESM package ("type": "module"), so bind require() explicitly (SCAR-001).
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);

const pptxgen = require("pptxgenjs");

// ═══ Design tokens — dark amber-scar palette ═══
const COLORS = {
  bg: "0D1117",        // deep near-black
  surface: "161B22",   // card surface
  oil: "D4A574",       // warm amber (petroleum accent)
  scar: "C44545",      // scar red (emphasis)
  bone: "8B949E",      // bone grey (dimmed)
  truth: "7EE787",     // truth green (success)
  text: "E6EDF3",      // primary text
  textDim: "8B949E",   // secondary text
  line: "30363D",      // dividers
};

function createDarkSlideMaster(pres) {
  pres.defineSlideMaster({
    title: "DARK_SCAR_MASTER",
    background: { color: COLORS.bg },
    objects: [
      // Top accent line
      { line: { x: 0.0, y: 0.0, w: "100%", h: 0.04, line: { color: COLORS.oil, width: 2 } } },
      // Footer (HUMAN-READABLE — never use internal sigils)
      { text: {
        text: "NOT EVERYTHING SHOULD BE CLOSED",
        options: { x: 7.6, y: 7.0, w: 2.4, h: 0.25,
                   fontSize: 7, color: COLORS.textDim,
                   align: "right", fontFace: "Consolas", charSpacing: 1 }
      }}
    ],
    slideNumber: { x: 0.3, y: 7.0, w: 0.5, h: 0.25,
                   fontSize: 7, color: COLORS.textDim, fontFace: "Consolas" },
  });
}

function scarLine(pres, slide, x, y, w) {
  slide.addShape(pres.ShapeType.line, {
    x: x, y: y, w: w, h: 0,
    line: { color: COLORS.scar, width: 1.5, dashType: "dash" }
  });
}

// ═══ Usage example ═══
const pres = new pptxgen();
createDarkSlideMaster(pres);

// Slide 1: Cover with framing sentence
const s1 = pres.addSlide({ masterName: "DARK_SCAR_MASTER" });
s1.addText("This is not an incident report. It is a reflection on how\ninstitutions remember outcomes while individuals remember consequences.", {
  x: 0.8, y: 0.5, w: 8.4, h: 0.6,
  fontSize: 10, fontFace: "Georgia", italic: true,
  color: COLORS.bone, align: "left", lineSpacingMultiple: 1.2,
});
s1.addText("THE COST OF A\nFORGOTTEN WELL", {
  x: 0.8, y: 1.2, w: 8.4, h: 1.8,
  fontSize: 40, fontFace: "Georgia", bold: true,
  color: COLORS.text, align: "left", lineSpacingMultiple: 1.1, charSpacing: 0.5,
});
scarLine(pres, s1, 0.5, 3.0, 9.0);
s1.addText("Wells are drilled once.\nConsequences last decades.", {
  x: 0.8, y: 3.3, w: 6, h: 1.0,
  fontSize: 18, fontFace: "Georgia", italic: true,
  color: COLORS.oil, align: "left", lineSpacingMultiple: 1.3,
});

pres.writeFile({ fileName: "output.pptx" }).then(() => {
  console.log("PPTX written");
});