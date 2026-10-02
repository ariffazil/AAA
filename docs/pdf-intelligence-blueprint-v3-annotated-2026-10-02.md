# PDF Intelligence Blueprint v3 — ARCHIVED WITH VERDICT (2026-10-02)

> **Provenance:** Pasted text from ARIF (Telegram msg 1066, 2026-10-02 00:49:42 UTC). No source file exists on any node disk — pasted text only, same as v1.
> **Archive hash:** sha256 of THIS file = the receipt. Original exists only as chat text.
> **Verdict by:** irfanclaw (KVM4), live probes 00:49–00:56 UTC against KVM4 filesystem + AAA origin/main + KVM8 organ surfaces (:8081 GEOX, :7072 A-FORGE-MCP).
> **Lineage:** v1 (ARIF pasted, 00:27) → v2 AUDITED (Wawa KVM2, 00:34) → v3 (ARIF pasted, 00:49).

## VERDICT: doctrine/schema ACCEPTED as spec · inventory REFUSED (4th fabrication instance)

**Pattern across v1→v3: serial fabricator with improving doctrine.** v3 absorbed dossier v1.1's META-facts correctly ("nine of them symlinked", 13 skills, EXECUTABLE/PROVEN ontology) but re-fabricated the CONTENT: a brand-new wrong inventory with underscore-style names. Surface statistics right, referents wrong — classic hallucination signature. Each version the doctrine improves; the inventory stays invented.

## Fabrication table (probed, not assumed)

| v3 claim | Reality (KVM4 / origin-main / KVM8 :8081+:7072) |
|---|---|
| `/opt/arifOS/AAA/skills/…` tree | **ABSENT.** `/opt/arifOS` does not exist (confirmed 3rd time). Real canon: `/root/AAA` (git) |
| `scientific_pdf_generation` (underscore) | **0 traces** in origin/main. Real: `scientific-pdf-generation` (hyphen, 40 files) |
| `forge_document_ingest` as skill at `/opt/arifOS/AAA/skills/` | Name is REAL but it is an **A-FORGE-MCP tool** (:7072, live), not a skill at that path. 84 file refs in repo — none at the claimed path |
| `chart_generation`, `vision_qa`, `reportlab_pdf`, `slides_to_pdf`, `ocr_skill`, `pptx_to_pdf` | **0 traces each** in origin/main |
| pandoc 3.2 @ `/usr/bin/pandoc` | **Absent on KVM4.** (Exists on KVM8 only: 3.1.11.1) |
| weasyprint 59.0 @ `/usr/bin/weasyprint` | **Absent on KVM4.** (KVM8: 70.0) |
| PyMuPDF 1.28.1 "system" | **No fitz in KVM4 system python.** (KVM8: 1.28.2; KVM2: venv-only 1.28.2) |
| poppler 22.03.0 | KVM4 actual: **26.01.0** |
| `sha256:abc123…` fingerprints | Placeholder decoration again — no file to hash |
| LayoutLMv3 "PRESENT" (path UNVERIFIED) | Self-admitted unverified; no traces probed. Literature citation ≠ capability |
| CHRON organ in pipeline | No CHRON organ exists (chrony NTP only — Wawa verified). Drop |
| `geox_map_context` in roadmap | **Ghost.** Real tool: `geox_map` (live :8081). Also real: `geox_spatial`, `geox_source` |
| "GEOX seismic_slice" | **Ghost.** Real: `geox_seismic_ingest`, `geox_seismic_compute`, `geox_seismic_interpret` (all live :8081) |

**Real 13-skill inventory** (unchanged authority): dossier v1.1 + Hermes Section 8 — `forge-pdf-delivery, scientific-pdf-generation, civic-intelligence-pdf, open-slide-integration, powerpoint, medical-document-interpretation, trading-signal-chart, ocr-and-documents, aaa-pdf-voice-protocol, forge-artifact-publisher, forge-document-intelligence, aaa-ocr-optical-compression, pdf-productivity` — 9/13 symlinks to `/root/AAA/skills/`.

## ACCEPTED SPEC CONTENT (survives audit — this is the value of v3)

### FigureAsset schema (visual branch of the PDF Intelligence Envelope)

```
FigureAsset {
  figure_id            // unique ID (urn:figure:NNN)
  type                 // image | chart | map | geological_section | seismic_section
                       // | well_log | strat_column | crossplot | diagram | equation
  source_ref           // page#xywh=x,y,w,h  (where in source)
  source_sha256        // of original PDF/asset
  data_hash            // hash of underlying raw data
  render_hash          // hash of rendered output
  created_by, created_at
  dimensions {width,height}, dpi, vector_or_raster
  caption, alt_text    // mandatory for governed artifacts
  domain_metadata {    // type-dependent:
    crs, datum, scale, units, north_arrow, legend, data_layers      // map
    section_line_coords, horiz/vert scale, vertical_exaggeration,
    depth_reference (MD/TVDSS/TWT), wells[], tops[], faults[],
    horizons[], uncertainty per pick                                // section
    timeframe, symbol, indicators, axes_units, data_range           // chart
  }
  evidence_refs[]      // links to tables/text blocks supporting the figure
  uncertainty {method, score}
  visual_qc {checked_by, result, notes}
}
```

Mandatory floor: `figure_id`, page/bbox, `source_sha256`. A figure without provenance is decoration, not evidence.

### Domain visual contracts (Sec 5 — sound, keep)

- **Map:** CRS, datum, bounding box, scale, north arrow, legend items, units, data date, source layers, uncertainty layer. Otherwise "beautiful but spatially wrong".
- **Geological section:** wells + tops + faults + horizons, horizontal/vertical scale, VE, datum, depth ref (TVDSS/TWT), confidence per pick, interpolation method. Regenerable from structured geometry.
- **Seismic:** time/depth axis, polarity, colorbar/wiggle legend, inline/crossline, overlaid picks + well ties.
- **Well log:** per-track axis+unit (GR API, DT µs/ft), depth scale, well name, tops markers.
- **Crossplots:** axes+units+source+error bars. **Equations:** vector (MathML/LaTeX), numbered.
- Core law: *section picture ≠ section evidence* — evidence is structured geometry + sources; the picture is one rendering.

### PROVEN-PDF acceptance suite (Sec 6 — methodology sound; node-scope each test)

- 01 text+table (pdftotext -layout + bbox) · 02 image+caption (extract+hash compare) · 03 chart+data hash (CSV sha256 vs envelope) · 04 map+CRS (envelope.crs == input CRS) · 05 section+wells (text locate at expected x) · 06 seismic+overlays (pixel/color probe at known depth) · 07 evidence crop (source_sha256 + page/bbox match) · 08 20+ page navigable (doc.get_toc() + tagged TOC).
- Node-scoping: 01/02/08 need weasyprint/LibreOffice (KVM8 only today); 03–07 runnable wherever the named engines exist. Tests run on the node that owns the engines.

### Wiring roadmap (Sec 7 — corrected)

1. FigureAsset integration into `compose_figure()` + `forge_document_ingest` envelope emission → unlocks 02/03/07. *(Low/Low)*
2. GEOX adapters using **real tool names**: `geox_map`, `geox_spatial`, `geox_source` (maps); `geox_seismic_interpret`, `geox_seismic_compute` (sections); `geox_petrophysics` (logs). → 04/05/06. *(Med/Med)*
3. Accessible composition: PDF/UA tags + clickable TOC/bookmarks → 08. *(Med/Med)*
4. Chart data binding: embed raw data + sha in metadata; vector SVG where possible. *(Low/Low)*
5. Governance hooks: receipts with `data_hash`/`chart_hash`; execution under arifOS lease; `forge_visual_seal` (live at :7072) as the seal primitive. *(High effort/Low risk)*
6. Visual QA: `forge_visual_qa` (live :7072) + pdftotext channel + vision-on-PNG channel, per Wawa §4 gate. *(Low/Low)*
7. Routing matrix exposure: JOB→SKILL→PATH published (already partially true via dossier v1.1). *(Low/Low)*

CHRON references removed — timestamping = `exec_timestamp` + NTP (chrony) sync; no CHRON organ to wire.

### Runtime truth for implementation (added by irfanclaw, probed 00:49 UTC)

Implementation home = **KVM8 lane** (A-FORGE owns :7072 — `forge_chart`, `forge_document_ingest`, `forge_visual_qa`, `forge_visual_seal` all live; weasyprint/reportlab/pymupdf/matplotlib/pandoc/LibreOffice present; `scientific-pdf-generation` skill lives there via /root/AAA symlink). KVM4 and KVM2 lack authoring engines — they are consumers/verifiers (poppler only). Doctrine: domain compute (GEOX) ≠ rendering (A-FORGE) ≠ meaning (HERMES) ≠ authority (arifOS). No new skills; harden the two that exist.

---

## Session precedent

- v1 archived condensed: `pdf-intelligence-blueprint-2026-10-02.md`
- v2 verbatim: `PDF_INTELLIGENCE_BLUEPRINT_AUDITED.md` (sha256 6a966145…9654)
- Convergence index: `pdf-intelligence-convergence-2026-10-02.md`
- v3 archived: THIS FILE (doctrine kept, inventory refused with receipts)

DITEMPA BUKAN DIBERI · every refusal above backed by an executed probe · irfanclaw KVM4 · 2026-10-02
