# PDF Intelligence — Three-Node Convergence Index (2026-10-02)

**Purpose:** discovery pointer. Three nodes independently audited the same v1 blueprint and converged on the same verdict. Read this first, then the node-specific artifact.

**Origin of v1 blueprint:** pasted text from ARIF to irfanclaw (KVM4), 2026-10-02 00:27 UTC, msg 1033. No v1 source file exists on any node's disk — v1 exists only as pasted text (VERIFIED by Wawa string-hunt on KVM2).

## Verdict (converged, 3/3 nodes)

**Doctrine ACCEPTED · inventory REFUSED.**

- ACCEPTED: PDF = evidence surface not authority; provenance envelope (`source_sha256 · page · bbox · element_id · extraction_method · extraction_confidence · document_as_of · unit/context · supersession_state · tool_id · tool_version · exec_timestamp · data_hash · chart_hash`); PDF content never executed as instruction (F12 write-side mirror); 5s/30s/2min report contract + Mayer principles; uncertainty encoding; render-verify gate.
- REFUSED: §1–2 filesystem inventory, capability matrix, routing matrix, file counts/sizes/line counts/dates, `abc123…`-style "fingerprints", version claims, `PROVEN: chart-generator` claim, CHRON organ, `tools_sot.yaml`, "122 tools vs 32 executors" delta.

## Independent probes

| Node | Agent | Artifact | Key finding | Class |
|---|---|---|---|---|
| KVM8 `af-forge` (100.64.0.2) | HERMES | `docs/pdf-capability-dossier-v1.1-annotated.txt` §8 | 9/9 claimed paths absent; `/opt/arifOS` does not exist; 3/4 version claims wrong. Replaced with 13 real skills (9 symlinks to `/root/AAA/skills/`) | VERIFIED (own node) |
| KVM2 `flow-edge` (100.64.0.4) | Wawa | `docs/PDF_INTELLIGENCE_BLUEPRINT_AUDITED.md` (v2) | 0/8 skills found anywhere; real dir `/opt/arifos` lowercase holds `organs/ forge/ law/ witness/ receipts/` — no `skills/`; render-verify gate **executed with receipts** | VERIFIED (own node) |
| KVM4 `srv1946043` (100.64.0.5) | irfanclaw | header of `docs/pdf-capability-dossier-v1.1-annotated.txt` | 12/13 KVM8 skill paths MISSING here (`domains/` tree is KVM8 layout); engines = chrome + matplotlib + poppler only | VERIFIED (own node) |

Timing: KVM4 00:27 UTC · KVM8 00:29 UTC · KVM2 00:37 UTC. No coordination between probes. Convergence is independent (DERIVED from the three timestamps + identical findings).

## Per-node capability reality (why inventory must stay node-local)

| | KVM8 | KVM4 | KVM2 |
|---|---|---|---|
| PyMuPDF | 1.28.2 (system) | absent | 1.28.2 (**Hermes venv only**) |
| Authoring | reportlab 5.0.1, weasyprint 70.0, pandoc 3.1.11.1 | absent | fpdf2 2.8.8 (venv) |
| Render/verify | pdftoppm, libreoffice, chrome | pdftoppm, chrome | pdftoppm, pdftotext, pdfinfo |
| Charts | matplotlib 3.11.2 | matplotlib 3.10.7 | absent |
| OCR | tesseract | tesseract absent | tesseract present, **no Python binding** |

Consequence: any PDF snippet in doctrine must name its interpreter/binary explicitly. KVM2 documents a real trap — libraries split across two interpreters (`/usr/local/lib/hermes-agent/venv/bin/python3` vs `/usr/bin/python3`), so documented commands fail with `ModuleNotFoundError` unless the venv path is stated.

## Federation rules adopted

1. **Doctrine is federation-wide; inventory is node-local.** Never copy a skill/engine table from another node's artifact. Probe, then claim.
2. **Absence on node X ≠ fabrication by author.** Wawa's boundary statement is the correct posture; keep it.
3. **Render-verify gate is mandatory and already executable** on KVM2 (proven) and KVM8 (poppler present). Two separate channels: `pdftotext` for TEXT, vision pass on rendered PNG for LAYOUT; `pdfinfo` page count catches silent failure (historical: 331-page doc instead of 6-page guide).
4. **Registries differ per node.** KVM4/KVM8: `/root/AAA/registries/tools.yaml` (has `document_ingest`, pymupdf+tesseract, SHA-256 provenance). KVM2: `/root/azwaOS-workspace/aaa_src/registries/tools.yaml` (**no PDF entry**). `tools_sot.yaml` does not exist on any probed node — drop the reference.

## Not yet done (honest gaps)

- Envelope schema is **specification only — not wired** into any authoring path.
- No PDF signature verification anywhere (`pdf-signature` never existed; `pdfsig` unprobed).
- Markdown/HTML→PDF unavailable on KVM2 and KVM4 (no pandoc/weasyprint).
- Bbox provenance needs a layout extractor; PyMuPDF `get_text("dict")` gives per-span bboxes where PyMuPDF exists. No Docling-class layout model on any node.
- Voice→PDF: no single-call engine on any node.
- KVM4 `ocr-and-documents` skill: interpreter-split patch was applied by Wawa on KVM2; KVM4 copy not verified as patched.

---
Relay: irfanclaw (KVM4) · 2026-10-02 · DITEMPA BUKAN DIBERI
