# PROMPT FOR OTHER AGENTS — route every PDF job to pdf-federation

Paste this to any federation agent (Claude Code, OpenCode, Gemini, a subagent,
a fresh session) that is about to touch a PDF.

---

You are working inside the arifOS federation. ALL PDF work goes through ONE skill:

  /root/AAA/skills/pdf-federation

RULES (binding):

1. Do NOT create any new PDF skill. Do NOT use these retired names — they all
   resolve to pdf-federation: hermes-pdf-intelligence, forge-pdf-delivery,
   forge-artifact-publisher, scientific-pdf-generation, civic-intelligence-pdf,
   open-slide-integration, pdf-realmap, powerpoint, document-pipeline,
   empirical-audit-pdf, governed-artifact-composition, nano-pdf-routing,
   ocr-routing, html-pdf-reporting, pdf-report-generation.

2. Flow: probe → compose → verify → deliver.

3. One-off consumption PDF (a guide, brief, letter, dossier, map handout):
   use typst. Read /root/AAA/skills/pdf-federation/references/typst-recipes.md
   for the working boilerplate, the known pitfalls, and the real-map recipe
   (staticmap + OpenStreetMap + Nominatim + OSRM).

4. Verify before shipping:
   - G1: pdfinfo — page count + structure
   - G3: pdftotext — sentinel string round-trips
   - G2: pdftoppm + vision — ONLY for layout/map/chart PDFs (catches URL
     overflow, clipped boxes, wrong marker placement)

5. Capability claims require raw probe output:
   bash /root/AAA/skills/pdf-federation/scripts/probe_manifest.sh
   A prose claim of "I probed" is fabricable — ship the raw output.

6. Deliver the absolute .pdf path. Never cite a scratch/tmp path to a human.

To start: read SKILL.md, probe, then compose.

---
