---
name: governed-artifact-composition
description: "Compose one governed artifact from a build manifest."
version: 1.0.0
forged: 2026-10-02
authority_of: HERMES
---

# Governed Artifact Composition — the manifest + compiler layer

Class-level skill. Use when a user wants **one full multi-section artifact** assembled from several
producers (live data + charts + maps + claims + gaps) and expects it to be **repeatable**, not a
one-off hand-stitch. Trigger phrases: "one final PDF", "full artefact", "compile everything into
one", "the complete picture", "one run", "reproduce it".

This is NOT the markdown→PDF task (`forge-pdf-delivery`) and NOT the single-audit probe→chart task
(`empirical-audit-pdf`). This is the ORCHESTRATION layer above both: many producers, one manifest,
one compiled output.

## The one rule

```
Organ output  ≠  PDF
Organ output  =  a typed node
```

A producer (WEALTH, GEOX, HERMES, CHRON, arifOS) does **not** render pages. It returns a typed
contract — a figure path, a table, a list, a data reading. The compositor reads every node and
writes the single PDF. The moment two producers each write their own PDF, the assembly collapses
back into ad-hoc stitching.

**Why this matters:** without a shared contract, every rebuild re-decides layout, caption shape,
and provenance fields. The manifest fixes those decisions once, so a future session reproduces the
artifact instead of reinventing it.

## Procedure

1. **Write the build manifest** (YAML). Minimum keys:
   ```yaml
   artifact:   { id, title, subtitle, output_path, envelope_path, authority_state }
   sections:   [ { type, producer, caption?, truth_class?, required_fields? }, ... ]
   assets:     { contract: FigureAsset }
   evidence:   { contract: RealityEvidenceEnvelope, fields: [...] }
   verification: { render_all_pages, visual_qa, hash_all }
   compositor: { primary, fallback, figures, no_new_tool: true }
   ```
   Each `section.type` names a render kind (`cover`, `toc`, `live_chart`, `map`, `table`,
   `list`, `authority_view`, `appendix_envelope`, …) and each `section.producer` names the organ.

2. **Run the compiler** — reads manifest, probes live context, dispatches each section to its
   producer, composes one PDF, runs acceptance checks, writes a machine envelope:
   ```bash
   python3 compose_artifact.py build-manifest.yaml            # build + verify
   python3 compose_artifact.py build-manifest.yaml --dry-run  # validate manifest only
   ```

3. **Add a producer** by registering a function that returns
   `ProducerResult(kind, payload, provenance)`. Kinds: `figure_path | table | list | dashboard |
   json | live_data | authority_matrix | unavailable`. The composer's generic renderer handles every
   kind, so a new producer needs **no** change to the composer.

4. **Read the verification output, not the exit code.** The compiler runs five checks — real PDF
   magic, page count, bookmark count, text extractability, hash-stability — and prints per-check
   PASS/FAIL. A log line saying SUCCESS is not sufficient.

5. **Deliver** the artifact path as a `MEDIA:` link with ≤8 lines of chat. The document is the
   deliverable; the chat message is a delivery notice.

## Honest-absence contract (do not violate)

- A section whose producer is missing renders **UNVERIFIED**, never a filled-in guess.
- A figure rendered from server-side defaults carries `data_hash: null` **plus** a
  `data_hash_absent_reason` string. A null hash on a synthetic figure is a correct receipt, not a gap.
- A synthetic demonstration is labelled `truth_class: SYNTHETIC` on the page itself.
- The compiler **does not seal**. Sealing is the kernel's act; a human authorizes.

## Pitfalls (each cost a real failed render)

- **matplotlib 3.11: `ax.scatter()` colour kwarg is `c=`, and `ax.bar()` is `color=`.** Mixing them
  is a trap because the two axes methods disagree: `scatter(..., color=X)` raises
  `ValueError: 'color' kwarg must be a color`, while `bar(..., c=X)` raises
  `AttributeError: Rectangle.set() got an unexpected keyword argument 'c'`. Rule of thumb:
  `bar`/`barh` → `color=`; `scatter` → `c=`. Pass a colour **string**; never pass a reportlab
  `HexColor` object (matplotlib rejects it) and never pass the data dict.
- **`plt.Rectangle` is not exported from `matplotlib.pyplot`.** Import from `matplotlib.patches`.
  Same for `Circle`, `Polygon`, `Wedge`. Lint catches it; runtime fails silently with an empty figure.
- **`Rectangle((x, y), w, h)` takes 3 positional args, not 4.** `Rectangle(x, y, w, h)` raises
  `TypeError: takes 4 positional arguments but 5 were given`.
- **`TableOfContents` and `Frame` are NOT in `reportlab.platypus`.** Import from
  `reportlab.platypus.tableofcontents` and `reportlab.platypus.frames` respectively. The naive
  `from reportlab.platypus import TableOfContents` raises `ImportError`.
- **A PDF outline needs `bookmarkPage` + `addOutlineEntry`, not just a TOC callback.** Overriding
  `afterFlowable` and calling `self.notify("TOCEntry", ...)` populates the on-page table of contents
  but yields **zero** outline entries. Add `self.canv.bookmarkPage(key)` AND
  `self.canv.addOutlineEntry(text, key, level=lvl, closed=(lvl == 0))` in the same block, then build
  with `doc.multiBuild(story)` so the two passes resolve.
- **`file foo.pdf` miscounts pages when the PDF carries an outline.** It can report N+1. Trust
  `pdfinfo` for page count; use `file` only to confirm the magic bytes say `PDF document`.
- **`os.walk` skips symlinked trees by default.** Skill directories are frequently symlinks into
  another tree; `os.walk(path)` returns a near-empty result and silently undercounts. Probe with
  `os.walk(path, followlinks=True)`, and report both the exposed path and `os.path.realpath()` so a
  reader can tell discovery-view from canonical-write location.
- **`pip install --break-system-packages`** is the escape hatch on this VM when PEP 668 blocks a
  system install of reportlab / matplotlib / weasyprint.
- **Set `MPLCONFIGDIR=/tmp/.mpl` and `matplotlib.use('Agg')` before importing pyplot** — headless
  safety plus it silences a non-fatal matplotlibrc warning on every call.

## Reading before answering

When the user hands you a document (a pasted artifact, an attached PDF, a blueprint), **read it
before responding.** Answering from the filename or the surrounding conversation produces confident
claims about content you have not seen — and the correction costs more than the read. If the source
is a PDF, extract its text layer first (`pdftotext -layout`, or pymupdf) and answer from that.

## Do not over-clarify on a build task

Short imperatives from this user — "wow me", "buat ja laaa", "go", "execute all" — mean
**proceed**, not "ask me four questions". One genuine blocking question is fine; a chain of them on
a task where the sensible default is obvious burns the attention the artifact is meant to serve.
When the scope is unclear, pick the most reasonable reading, build it, and say what you assumed.

## Verification checklist

- Compiler acceptance block prints PASS for all five checks.
- `pdfinfo` page count matches expectation; bookmarks > 10.
- Every figure caption carries a SHA prefix and a truth_class.
- Every synthetic figure carries `data_hash: null` + a reason.
- The machine envelope exists alongside the PDF with the artifact SHA-256.

## Related (all external / AAA-owned — recommendation only)

- `forge-artifact-publisher` — declares the artifact TYPES this layer composes.
- `empirical-audit-pdf` — the single-audit probe→chart→assemble pipeline.
- `scientific-pdf-generation` — Mode A–E visual specifications for the render layer.
