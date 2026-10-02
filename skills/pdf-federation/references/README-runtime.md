# forge-artifact-publisher — RUNTIME ADDITIONS (2026-10-02)

## The Missing Linker: compose_artifact.py

Before this addition, the skill described *how to forge artifact types* (dossier, slide pack, etc.)
but had no **generic assembly protocol**. Each agent composed ad hoc: pick a chart skill, pick a
geology skill, pick a claim skill, manually stitch them into one PDF. That is why the federation
could produce many impressive PDFs but could not reliably produce *the one full mission PDF on demand*.

`scripts/compose_artifact.py` closes that gap.

### Contract

```
BUILD MANIFEST (yaml)
        │
        ▼
compose_artifact.py
        │  reads manifest
        │  probes live context (WEALTH, arifOS, engines, skills)
        │  for each section: calls the named PRODUCER
        │  producers return typed contracts (figure_path / table / list / etc.) — NOT PDFs
        │  composes ONE reportlab PDF
        │  runs acceptance checks
        │  writes: <output>.pdf + <envelope>.json
        ▼
ONE GOVERNED PDF + ONE MACHINE ENVELOPE
```

### Rule (mission §R)

**Organ output ≠ PDF. Organ output = a typed node.**

- WEALTH produces a **live_data** node or a **figure_path** node.
- GEOX produces a **figure_path** node (with CRS/truth_class provenance).
- HERMES produces **table** / **list** nodes (claims, contradictions, gaps).
- CHRON produces a **table** node (temporal state) or gracefully emits UNVERIFIED.
- arifOS produces an **authority_matrix** node.
- A-FORGE is the compositor. It reads all nodes and writes one PDF.

### Files

| File | Purpose |
|------|---------|
| `references/build-manifest.v1.yaml` | The manifest schema + a working 17-section example |
| `scripts/compose_artifact.py` | The compiler. Reads manifest → writes PDF + envelope. |

### Usage

```bash
python3 scripts/compose_artifact.py references/build-manifest.v1.yaml              # build + verify
python3 scripts/compose_artifact.py references/build-manifest.v1.yaml --dry-run    # validate only
python3 scripts/compose_artifact.py references/build-manifest.v1.yaml --no-verify  # skip acceptance
```

### What the compiler guarantees

1. Every section either produces a typed node, or is explicitly marked `UNVERIFIED`.
2. No section invents data to fill a gap. A missing producer → the section says so.
3. Every figure caption carries its SHA prefix and truth_class.
4. Acceptance checks: real PDF / pages > 5 / bookmarks > 10 / extractable text / hash stable.
5. One machine envelope per build: artifact SHA-256, section list, producer calls, figure hashes.

### Adding a new producer

Register it in the `PRODUCERS` dict:

```python
@producer("ORGAN_NAME")
def organ_producer(section, ctx):
    # read section spec, produce a typed node
    return ProducerResult("table", rows)         # or figure_path / list / dashboard / json
```

The composer's generic renderer handles every `ProducerResult.kind`, so a new producer
needs no changes in `build_pdf()`.

### Honest boundaries

- Does **not** generate figures — that remains each producer's job.
- Does **not** invent missing data — renders SYNTHETIC / UNVERIFIED when there is none.
- Does **not** seal — arifOS seals; a human authorizes.

### Proven

2026-10-02 · 17 sections, 16-page PDF, 17 bookmarks, 6 figures tied, ALL PASS on acceptance checks.
Manifest: `references/build-manifest.v1.yaml`
Artifact: `/root/AAA/forge_work/2026-10-02-reality-edge/reality-edge.pdf`
Envelope: `/root/AAA/forge_work/2026-10-02-reality-edge/envelope.json`
