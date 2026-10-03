---
name: document-pipeline
category: document-intel
description: "Use when producing any PDF or document deliverable."
version: 1.0.0
triggers:
  - "make a pdf"
  - "build a report"
  - "generate a briefing pdf"
  - "which pdf tool"
  - "pdf pipeline"
  - "document deliverable"
capability_tier: fed-long-context
ecology_state: WARM
---

# Document Pipeline — the router

Class-level skill. This is the **entry point** for any document deliverable. It does not replace
the cluster; it routes into it. Load this first, then load only the one or two skills it names.

**Why it exists:** the federation accumulated ~20 document skills with strong individual doctrine and
no map. Every build re-derived the same six steps by hand and forgot a different one each time. The
defects that slipped through were never content defects — they were a skipped gate. On the first run
of the engine below, the path-leak gate caught a real leak that the hand-built pipeline had missed.

## Arif's standing preference — LIGHT, never dark

**Default to a light palette.** White/near-white ground, dark text. He stated this plainly
(2026-09-18): *"I hate black dark background in pdf."* Dark decks are for screen; these artifacts
are for reading. Do not ship a dark-theme document unless he explicitly asks for one.

**This reverses the house style previously recorded in `visual-artifact-delivery` §1**, which
specified a dark base. That file has been corrected. If any older artifact of yours still cites a
dark base as the default, it is stale.

Light palette that works (validated on Edition 001, contrast checked by vision):

| Role | Hex |
|---|---|
| Ground | `#ffffff` |
| Body text | `#1c1c1c` (≈15:1) |
| Heading / table header | `#1a3a5c` navy — white text on it ≈12:1 |
| Accent rule / stamp | `#b02a1f` deep brick |
| Emphasis numbers | `#6b5210` dark bronze — **not** pale gold |
| Zebra row | `#f7f6f4` |
| Muted / footer | `#5f5f5f` |

**Pitfall:** a gold accent that looks right on a dark ground falls to ~3:1 on white — below WCAG AA.
Darken it. Vision inspection caught exactly this on the first light build.

## Layer stack — each layer has an owner

| # | Layer | Owner skill |
|---|---|---|
| 1 | **Audience** — who reads it, what they must retain | `human-facing-artifact-design` |
| 2 | **Content** — sourcing, figures, epistemic tags | `auditable-numeric-artifacts` |
| 3 | **Layout** — pagination, breaks, running furniture | `paged-media-report-layout` |
| 4 | **Render** — the engine | here + `scripts/docbuild.py` |
| 5 | **Audit** — prove content arrived and is legible | `rendered-document-audit` |
| 6 | **Seal** — content hash + artifact hash + chain | `sealed-deliverable-provenance` |
| 7 | **Deliver** | `visual-artifact-delivery` |

Never duplicate an owner's doctrine here. If this file and an owner disagree, the owner wins.

## Two lanes exist — resolved by consolidation, not by running both

Two DIFFERENT implementations of the recurring-briefing deliverable were built on this host on the
same morning (2026-09-18), 30 seconds apart, both scheduled to 09:00 to the same DM. That is a
**defect, not redundancy**: two notifications, and claim history split across two stores so neither
delta is complete. The standing resolution is ONE lane.

| Lane | Location | Engine | Strength |
|---|---|---|---|
| **docforge — THE LIVE LANE** | `/root/AAA/scripts/docforge/` (~1,900 lines) | WeasyPrint, 4 themes incl. `accessible.css` | SQLite claim-state (`CONTESTED`/`OPEN`/`MOVED`/`SETTLED`/`NEW`), `item_id` persists across editions, `first_seen`/`last_seen`/`last_changed`, 32+39 passing tests, producer injected not hardcoded |
| briefing-system — RETIRED | `/root/briefing-system/` | Chrome headless | JSON schema contract + Jinja2 split, ink and path-leak gates, `chain_prev` ledger chaining. Archived editions remain readable as historical input |

**Why docforge won:** the superior state layer. A brief that *learns* needs claim lifecycle and a
stable join key; a list of artifact hashes cannot express "this claim moved". Its transport was then
verified separately (`hermes send -t telegram:<chat_id>` — a bare numeric chat id FAILS with
"Unknown or unregistered plugin platform"; the `telegram:` prefix is required).

**Rules for anyone adding a briefing job:**
- List cron jobs first and check the target timeslot for overlap. Two PDFs to one person on one
  morning is the failure mode.
- On overlap: pick ONE and have the other delegate or retire — never silently leave both live.
- Consolidate onto the stronger engine; do not destroy the losing lane's code, retire its trigger.
- A retired lane must stop being a *source* too, or the survivor waits on output that never comes.
- **`deliver: origin` can silently misroute.** A job created from an agent context can capture the
  BOT'S OWN chat as its origin, not the human's DM — so `origin` looks configured while delivery
  goes somewhere the human never reads. Observed 2026-09-18: origin captured `chat_id 8410138119`
  (the bot's own chat) for a briefing meant for `267378578`. Always set an EXPLICIT target
  (`telegram:<chat_id>`) on a human-facing job and verify it persisted to the job store.
- **Bare numeric chat ids fail in `hermes send`** — `-t 267378578` returns "Unknown or unregistered
  plugin platform". The `telegram:` prefix is required. A transport probe must use the real grammar
  or it reports a false negative.

## Engine matrix — pick by shape, not habit

## Engine matrix — pick by shape, not habit

| Artifact | Engine | Why | Watch out |
|---|---|---|---|
| Multi-page HTML report, tables, CSS layout | **chrome** | Highest fidelity; JS runs; **emits a tagged PDF free (Chrome 85+) — the accessibility baseline** | Not built to be a backend service; `--no-pdf-header-footer` is REQUIRED or it burns `file:///` paths into every page |
| Same, no JS, tight on memory | **weasyprint** | Real CSS-paged-media: `@page` running headers/footers via `counter(page)` | No JavaScript; weaker modern-CSS than Chromium |
| Programmatic, canvas control, embedded plots | **reportlab** | Precise coordinates, matplotlib embedding | Needs a Python build script, not HTML |
| Flat poster, single chart, text over a photo | **PIL** | Fastest; no pagination needed | Measure every string — PIL neither wraps nor raises |
| Slides / deck | fixed-size HTML with a matching page box, or `open-slide-integration` | | Fixed-size divs under a non-zero `@page` margin **split each slide into two pages** |

**Do not adopt `wkhtmltopdf`.** Unmaintained; every 2026 comparison advises against new use.

**Contested — carry it honestly:** the Chromium blog states Chrome generates tagged PDFs;
independent accessibility practitioners report headless-browser pipelines produce **weak or absent**
tag trees. Both are published. Verify the tag tree on your own output rather than trusting either.

## The engine

```bash
python3 ~/AAA/skills/document-pipeline/scripts/docbuild.py \
    --src index.html --out EDITION.pdf \
    --edition 001 --ledger edition-ledger.jsonl \
    --engine chrome
```

One pass: render → page count → ink sweep → text layer → path-leak check → content hash →
artifact hash → sidecar → ledger row. **Exits non-zero on any failure.** Put it in the build
script — a gate that depends on remembering to run it is skipped on exactly the rushed edition
that needs it most.

Embed `{{CONTENT_SHA256}}` where the content hash should print. The engine hashes the template
**before** substitution, injects, renders, then hashes the render. Order is load-bearing: hash a
source that already contains its own hash and the digest describes a document that never existed.

## Reading the gate output

- **ink per page** — every page ≥3 %. A page an order of magnitude below its neighbours is a
  stranded fragment, not design. Healthy example (Edition 001):
  `[5.5, 13.7, 5.1, 12.9, 14.0, 7.1, 14.6, 9.9]`.
- **path leak == 0** — an absolute path in the text layer leaks the build machine.
- **content hash inside ≥ 1**; **artifact hash inside == 0** — a file cannot contain the hash of
  its own bytes. That zero asserts the design constraint, not just the bytes.
- **text layer** — a near-empty layer means a scan or a failed render, not a document.

## Pitfalls

- **A forced page break per section header is the top cause of near-empty pages.** Let the engine
  paginate; reserve one forced break for the cover. Documented at length in
  `paged-media-report-layout`, and it recurs because it feels tidy. Do not defeat this by adding a
  break "for tidiness" mid-document — if a section feels like it needs its own page, that is the
  signal the section is too short, not that it needs a break.
- **An external AI blueprint's specificity is not evidence of implementation.** When the principal pastes an
  external dossier/blueprint for audit, probe every filesystem path, version string and tool name against
  the live system before using any of it. A coherent architecture and a fabricated inventory travel together:
  one pasted blueprint named `/opt/arifOS/forge/skills/pdf-text-extraction` and eight skills that did not
  exist anywhere on disk, while stating `reportlab 3.8.1` against a live `5.0.1`. Take the ideas; replace the
  data with your own probe; label the fabrication explicitly in the deliverable. Carry hash + probe-date per
  claim, never prose confidence.
- **A real map is polygons, not a diagram.** When the principal asks for a "real map", render Natural Earth
  land/admin polygons (`raw.githubusercontent.com/nvkelso/natural-earth-vector/.../ne_50m_land.geojson`) through
  matplotlib — not a schematic. Mark only coordinates you can verify (e.g. KL 3.1390°N, 101.6869°E); label
  virtual/cloud nodes as having no fixed public geography rather than inventing coordinates. Verify the render
  with a vision pass: confirm recognizable coastline geometry before delivery.
- **FigureAsset = the visual branch of the PDF Intelligence Envelope.** When a PDF carries a figure (chart, map,
  geological section, seismic panel, well-log panel, crossplot, equation, photo, 3D snapshot), treat the figure
  as a first-class evidence object, not decoration. The minimum envelope: figure_id, type, source_ref,
  source_sha256, data_hash, render_hash, dimensions, dpi, vector_or_raster, caption, alt_text, domain_metadata
  (CRS, datum, scale, units, vertical_exaggeration, depth_or_time, orientation), evidence_refs[], uncertainty,
  visual_qc. A figure without this envelope is decoration; with it, it is evidence. Domain rendering happens
  in domain organs (GEOX for map/section/seismic/well, WEALTH for chart, HERMES for diagram/equation); PDF
  composition only arranges pre-rendered FigureAssets. Never let PDF skill re-compute domain reality.
- **External doctrine cannot bypass the live probe.** When the principal pastes a long framework blueprint,
  audit every specific tool/path/version claim against the live system before adopting any of it. One pasted
  blueprint cited five GEOX tools (`geox_map_context_scene`, `geox_section_interpret_correlation`,
  `geox_seismic_analyze_volume`, `geox_seismic_well_tie_compute`, `geox_forward_model_synthetic`) — none exist on
  the live surface. The actual GEOX names are shorter (`geox_map`, `geox_basin`, `geox_seismic_compute`,
  `geox_well_ingest`, `geox_seismic_ingest`). Adopt the architecture, replace the names with the live probe.
  Mark the divergence in the deliverable — do not silently propagate the wrong names.
- **FigureAsset origin is a discriminated union, not one schema.** Two grammars, one object:
  `extracted` (from a source PDF → page+bbox+source_sha256 mandatory; e.g. cropped chart, OCR snippet) vs
  `generated` (rendered by domain compute → recipe + input hashes + tool identity mandatory; e.g. map from
  geox_map, cross-section from geox_model). Forcing one grammar over the other yields two failure shapes:
  generated figures become invalid by construction (no page, no bbox), or extracted figures lose provenance.
  Test the discriminator before any field is mandatory.
- **visual_qc is a state, not a boolean.** Verdict ∈ {UNCHECKED, PASS_CANDIDATE, HOLD, SEALED} plus tri-witness
  hash plus seal_ref. `passed: true` is the wrong type — the live visual QA layer
  (`forge_visual_qa`) reports PASS_CANDIDATE / 888_HOLD / SEALED_DEPLOY, never a single boolean. Writing
  `passed: true` either claims authority the QA layer does not have, or misrepresents what the tool said.
  Today every GEOX figure arrives `governance_verdict: HOLD` / `verification_status: PENDING` — no figure
  is SEALED. State that honestly.
- **Hash taxonomy must match what the tool actually returns.** A figure drawn from `geox_map.render_preview`
  carries two hashes that differ (`_evidence_receipt.sha256` vs `_receipt.content_sha256`) — pick one
  consistently and document the mapping. `data_hash` is nullable with a sibling
  `data_hash_absent_reason` and a flag like `server_side_defaults_used`, because some renders happen with
  dataset unseen by the caller (e.g. `geox_model geological_generate` with internal defaults).
  Forcing a hash means fabricating a number — the exact failure the whole exercise is trying to prevent.
- **A QA tool with a DOM payload contract cannot gate a PDF page.** `forge_visual_qa` requires
  `screenshot_path + dom_payload + constraints`. A PDF page has a screenshot but no DOM. Until A-FORGE
  publishes a PDF-page variant of the QA hook, treat visual QA of a PDF as best-effort
  (screenshot diff + ink-coverage sweep), not a SEAL-grade gate. Do not write code that pretends otherwise.
- **Retrieval asymmetry between adapters blocks the pipeline.** `geox_map` returns inline_base64
  (caller-portable), `geox_model` returns a host-local path (caller cannot read). Until the slower
  adapters standardise on inline bytes (or a shared mount), figures from those adapters cannot ship to
  PDF outside the GEOX host. State this in the contract, do not paper over it.
- **Capability state is a chain, never a boolean.** PRESENT (file exists) ≠ LOADABLE (SKILL.md valid) ≠
  EXECUTABLE (runnable assets present) ≠ PROVEN (produced a gated artifact). Marking every skill "LIVE" because
  a SKILL.md exists is a class error. When a dossier must prove addressability, print the absolute canonical
  path ending in `SKILL.md`, the sha256, line count, asset counts and last-modified per skill; mark anything
  unprobed as UNVERIFIED, never inferred.
- **A prose-only dossier is a failed dossier.** When the principal asks for a capability map,
  briefing, or dossier, the deliverable must carry working visuals — charts (matplotlib, light
  ground), code snippets (monospace blocks), and structured tables (real data, not prose in rows).
  Words alone do not demonstrate a capability; the artifact must SHOW the graphs, the snippets, and
  the analytics inside itself. Budget: at least one figure per 2–3 pages, one table per section,
  one code block per technical claim. A dossier that reads as an essay under-delivers regardless of
  how correct its prose is.
- **Fixing a spilling closing block: tighten, do not break.** When the final source/close block
  spills to a near-empty page (ink < 2 %), do NOT add a page break or delete content. Free the last
  ~1 cm by small global tightening — body `line-height` 1.42→1.36, `h2` top-margin 6.5→5 mm,
  table/pre margins −0.5 mm each — then re-render and re-run the ink sweep. Two tightening passes
  are usually enough to pull a 4–5 line block back onto the previous page. Verify with the ink
  sweep, not by eye: a genuine closing page carries ≥600 chars even when its ink is 1.9 %.
- **Patching the PDF instead of the source.** Patched PDFs are unreproducible and hide the diagnosis.
- **Leaving a superseded edition in the chain.** If an error is caught before sealing, rebuild from
  the corrected source and keep the failed build out of the ledger — do not commit it as an ancestor.
- **Adding a generated image that carries text.** Image models render lettering as garbled glyphs;
  ban text in the prompt rather than shipping a corrupted one.
- **Declaring done from a clean exit code.** A generator that writes a failure document still exits 0.
  `%PDF-` header, page count and the ink sweep are the evidence.

## Related

- Engine detail and CSS recipes: `references/engines.md`
- Long-form pagination: `paged-media-report-layout`
- Pre-delivery audit: `rendered-document-audit`
- Seal contract: `sealed-deliverable-provenance`
- Figure discipline: `auditable-numeric-artifacts`
