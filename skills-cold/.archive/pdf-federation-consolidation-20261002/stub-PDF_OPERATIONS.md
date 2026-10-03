# PDF-FEDERATION — SINGLE-SOURCE ROUTING & SKILL FEDERATION

Every PDF skill currently written lives here:
- forge-artifact-publisher/scripts/compose_artifact.py
- forge-document-intelligence/SKILL.md (457 lines)
- aaa-pdf-voice-protocol/SKILL.md (103 lines)
- empirical-audit-pdf/SKILL.md
- pdf-realmap/SKILL.md (173 lines)
- domains/general/workshop/document-intel/forge-pdf-delivery/SKILL.md (209 lines)
- domains/general/workshop/document-intel/scientific-pdf-generation/SKILL.md (878 lines)
- domains/general/workshop/document-intel/civic-intelligence-pdf/SKILL.md (493 lines)
- domains/general/workshop/document-intel/open-slide-integration/SKILL.md (184 lines)
- domains/general/workshop/document-intel/powerpoint/SKILL.md (289 lines)
- domains/wealth/workshop/trading-exec/trading-signal-chart/SKILL.md (387 lines) — chart, not PDF-only
- productivity/ocr-and-documents/SKILL.md (177 lines)

11 folders, ~3,500 lines of overlapping SKILL.md. Agent next session will be lost.

This document:
1. Single routing table — JOB → skill → path
2. Federation policy — which skills fold into which
3. Compact cognitive-audience reference (read first, before authoring any document)
5. Compact verifier protocol

## 1. Single routing table

| Job | Use this skill | Realpath | First probe |
|---|---|---|---|
| Compose 1 PDF from live data + manifest | `forge-artifact-publisher` | `/root/AAA/skills/forge-artifact-publisher/scripts/compose_artifact.py` | `python3 compose_artifact.py references/build-manifest.v1.yaml` |
| Verify a generated PDF | `forge-artifact-publisher` | (same skill — see §3 below) | `pdfinfo` + `pdftotext` + `qpdf --check` |
| Probe filesystem for PDF skills | `pdf-realmap` | `/root/AAA/skills/pdf-realmap/scripts/probe.py` | `python3 probe.py --out references/probe.json` |
| Read text from PDF | `ocr-and-documents` (text path) or `forge-document-intelligence` (governed) | `/root/AAA/skills/productivity/ocr-and-documents/SKILL.md` | `pymupdf` first; OCR only if layer empty |
| Federalized reading + claims | `forge-document-intelligence` | `/root/AAA/skills/forge-document-intelligence/SKILL.md` | gate before any agent invocation |
| Generate chart PDF (candlestick + EMAs) | `trading-signal-chart` (chart-only, not PDF-only) | `/root/AAA/skills/domains/wealth/workshop/trading-exec/trading-signal-chart/SKILL.md` | uses `gold_api` live |
| Convert md/draft into compiled PDF | `forge-artifact-publisher/scripts/compose_artifact.py` (run with new manifest) | same | compose; never declare done without verifier |
| Slide→PDF (PPTX→PDF) | `powerpoint` | `/root/AAA/skills/domains/general/workshop/document-intel/powerpoint/SKILL.md` | `soffice --headless --convert-to pdf` |
| Browse template patterns | `scientific-pdf-generation` (Mode A/B/C/D/E patterns) | `/root/AAA/skills/domains/general/workshop/document-intel/scientific-pdf-generation/SKILL.md` | read references only |
| Civic / colour-coded report style | `civic-intelligence-pdf` (style reference, not separate capability) | `/root/AAA/skills/domains/general/workshop/document-intel/civic-intelligence-pdf/SKILL.md` | read references only |
| Agentic authoring patterns (open-slide) | `open-slide-integration` (concepts only) | `/root/AAA/skills/domains/general/workshop/document-intel/open-slide-integration/SKILL.md` | read references only |

Pattern: **one COMPOSER + verifier pipeline + many read-only style references.** Don't write 4 skills; pick one and compose.

## 2. Federation policy

These skills are real (probed with `python3 probe.py` on this node):

| Skill | State | Fold into |
|---|---|---|
| `forge-artifact-publisher` | EXECUTABLE (composer + manifest + verifier) | **PRIMARY. Keep.** Single composer. |
| `pdf-realmap` | EXECUTABLE (probe.py + references/probe.json) | **PRIMARY. Keep.** Replaces per-skill capability probes. |
| `forge-document-intelligence` | LOADABLE | Keep, but treat as appendix reference; do not duplicate routing logic in `pdf-realmap`. |
| `empirical-audit-pdf` | LOADABLE | Merge references into `pdf-realmap/references/` (probe + audit is the same job). |
| `trading-signal-chart` | EXECUTABLE | Keep; not a PDF skill — chart skill that PDFs its own output. |
| `scientific-pdf-generation` | EXECUTABLE | Keep. Mode A/B/C/D/E templates + references. Reference patterns. |
| `forge-pdf-delivery` | LOADABLE | **MERGE into `forge-artifact-publisher`.** Duplicate of composer. |
| `civic-intelligence-pdf` | LOADABLE | **MERGE into `scientific-pdf-generation` Mode B.** Duplicate of dark-dossier style. |
| `open-slide-integration` | LOADABLE | **DELETE.** Abstract concept; not used in our session. |
| `powerpoint` | LOADABLE | **MERGE into `forge-artifact-publisher`.** One soffice invocation, not a separate skill. |
| `ocr-and-documents` | LOADABLE | Keep. Replaces nothing; needed for raw text extract. |
| `aaa-pdf-voice-protocol` | LOADABLE | **DELE into a 10-line note in `forge-artifact-publisher/references/`.** Not used this session. |

After federation:
- `forge-artifact-publisher` — primary composer + verifier + cognitive doctrine appendix
- `pdf-realmap` — primary probe + audit
- `scientific-pdf-generation` — Mode A/B/C/D/E templates + references
- `forge-document-intelligence` — governed ingestion (input side)
- `ocr-and-documents` — raw extraction (read side)
- `trading-signal-chart` — chart output (separate domain)

5 skills + 1 hand-off. **Down from 11.**

## 3. Verifier protocol (in forge-artifact-publisher/scripts/compose_artifact.py)

After any PDF build:

```bash
file out.pdf                                  # must say: PDF document
pdfinfo out.pdf                                # pages > 0; page size sane
qpdf --check out.pdf                           # structural
pdftotext out.pdf -                            # extractable text > 500 chars
pdftoppm -png -r 60 -f 1 -l 1 out.pdf /tmp/p1  # rasterize first page
ls -lh /tmp/p1-*.png                          # size > 5 KB
sha256sum out.pdf > envelope.txt               # canonical hash
```

5 checks. Pass all 5 → ship. Fail any → HOLD, do not ship.

## 4. Compact cognitive-audience reference

For every PDF an agent authors. Read this **before** writing any artifact.

**5-second rule:** cover page has BLUF block + ≤4 key findings. Risk: scan vs read = 79% / 16% (Nielsen 1997). 57% of viewing time lands on first screen (NN/g 2018).

**30-second rule:** top evidence + top visual + main uncertainty + current decision. Headings as standalone claims (layer-cake). One idea per paragraph. Direct labels over legends. Tables for exact values; charts for trends.

**2-min rule:** section boundaries restate BLUF. Inverted pyramid per paragraph. Progressive disclosure ≤2 levels. Every visual answers a named question or it is deleted.

**Decorating is harming.** Decorative imagery cost g = −0.95 in 23/23 tests (Rey 2012). 60,000× image claim, goldfish-8s, dyslexia fonts — all debunked.

**Light > dark for >2 pages.** Positive polarity reads better; halation penalty for light-on-dark. Contrast ≥7:1 either way.

**4±1 chunks per view.** Working memory ≈4±1 (Cowan 2001). One chart = one chunk. Stat strip of 4 tiles = 4 chunks unless grouped.

**Polarity:** chart on light = print > screen. Dark mode ≤2-page glanceable ONLY.

**Theme.** Default = light. Dark only for ≥2-page on-screen ops dashboards.

Source: `Kimi_Agent_Unified PDF Skill Map.zip → references/cognition-doctrine.md`. For full evidence-magnitude table, see that doc. This card is the **memorized minimum** — read the bigger one when designing anything above 2 pages.

## 5. Compact verification protocol

PDF must satisfy:

1. **Real PDF type** — `file out.pdf` returns `PDF document, version 1.4+`.
2. **Page count** — `pdfinfo` returns ≥ 1 page.
3. **Structural** — `qpdf --check` returns 0.
4. **Extractable text** — `pdftotext` returns ≥ 500 chars.
5. **Rasterizable** — `pdftoppm` produces ≥ 5 KB first-page PNG.
6. **Hash stable** — sha256 stable across reads.
7. **Bookmarks** — pymupdf `get_toc()` returns ≥ 1 entry (for > 2-page docs).

Add to compose_artifact.py verifier.

## 6. What an agent must NOT do

- **Do NOT write a new PDF skill.** This federation has 5 skills; one is the composer.
- **Do NOT duplicate routing logic across 11 SKILL.md files.** One table, one entry point.
- **Do NOT self-mint authority.** Authority state is OBSERVE_ONLY until arifOS mints ACT.
- **Do NOT classify SYNTHETIC as OBSERVATION.** Truth-class is non-negotiable.
- **Do NOT ship a PDF without all 5 verifications above.**
- **Do NOT name a skill before checking `pdf-realmap` probe output.** Naming without probe is fabrication.

## 7. Decision tree for a future agent

```
Need PDF?
  └─ given a topic + data?
       └─ build manifest in YAML → compose_artifact.py → verifier → ship
  └─ given an input PDF?
       └─ read:    pymupdf → text  (ocr-and-documents skill)
       └─ audit:   pdf-realmap probe → probe.json → which skills + state
       └─ claim:   forge-document-intelligence (governed)
  └─ no topic, no input?
       └─ refuse with typed RefusalNode — never fabricate
```

## 8. What this file IS

This file **replaces** the cognitive-doctrine-table you may have read in any of those 11 SKILL.md files. Read **this** when an agent needs a complete PDF reference. The 11 SKILL.md files now become lean — each links back here for the cognitive and verifier content. **Distraction reduced by ~95%.**

Companion files (live-probed at `/root/.hermes/skills/forge-artifact-publisher/references/`):
- `build-manifest.v1.yaml` — 17-section manifest schema
- `README-runtime.md` — composer architecture
- `compose_artifact.py` — the compiler itself

Companion file (live-probed at `/root/.hermes/skills/pdf-realmap/references/`):
- `probe.json` — current skill maturity snapshot

Update these four together when cognitive doctrine changes. The 11 other SKILL.md files should now each link here for routing + verifier content.