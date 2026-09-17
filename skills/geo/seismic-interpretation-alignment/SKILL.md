---
name: seismic-interpretation-alignment
id: seismic-interpretation-alignment
version: 1.0.0
description: Use when interpreting seismic or claiming AI picks.
owner: Hermes (curator-managed)
risk_tier: medium
floor_scope: [F1, F2, F7, F9, F11]
autonomy_tier: T1
tags: [seismic, interpretation, geox, structural-geology, avo, horizons, faults, coverage]
---

# Seismic Interpretation Alignment

Load when tasked with interpreting seismic, wiring an agent to an interpretation lane, or when anyone is about to
claim that an AI "interpreted" a section, picked a horizon, or identified a fault or trap.

The whole discipline is one sentence: **the model proposes falsifiable geometry, physics gates it, the Earth witnesses
it, and only a human seals it.** Everything below elaborates that sentence.

## 1. Establish what the lane actually reads before claiming anything

Before describing what an interpretation tool did, find out what data it consumed. Pixel-based and trace-based lanes
produce different epistemic classes of result and must not be described interchangeably.

- If the lane loads a raster image, extracts amplitude from channel arithmetic or inverted intensity, and detects
  boundaries in that array, the output is **image interpretation** — an observation about a picture.
- If the lane ingests SEG-Y, audits trace headers, checks geometry, preserves amplitude and estimates wavelet phase,
  the output is **seismic interpretation** — an observation about a measurement.

Image-derived picks can be correct and still not be seismic interpretation. Say which one you have. When a session
reports "the AI interpreted the seismic", the audit question is: which lane, and was a real volume loaded?

## 2. Three transitions, three gates

Never skip a transition. Each has a gate that returns a verdict rather than a number.

**Transition 1 — Pixel → rock.** Is this a reflector, a multiple, or a migration artifact?
Gate on amplitude preservation, wavelet phase (mixed phase ⇒ lower every pick's confidence), tuning thickness (λ/4 at
 the dominant frequency constrains the minimum resolvable bed), and an explicit imaging-artifact screen.

**Transition 2 — geometry → structure.** Fault or stratigraphic edge? Is the dip consistent with the regional stress
field, and does throw stay continuous along strike?
Gate on structural restore metrics plus correlation of the feature across lines. A feature seen on one line only is a
hypothesis, not a fault.

**Transition 3 — structure → charge.** Is closure real, seal intact, and did charge arrive before or during trap
formation?
Gate on the petroleum-system events sequence. Trap and charge synchrony is the favourable case; state it when you have it
and say so when you do not.

## 3. Iron rules

- The interpretation organ proposes geometry; it never states geology. Any field meaning "the preferred answer" stays
  null from the organ. Sealing belongs to the kernel, not the interpreter.
- The local maximum is a **qualified candidate**. Never report it as a conclusion.
- Gate verdicts include an UNMEASURED state. **UNMEASURED is not a pass.** Never upgrade it in transit, and never
  average it away.
- Carry at least three competing hypotheses for every pick. Collapsing to one before testing is the core failure mode.
- Confidence is capped below 1.0 (humility floor). A pick at maximum confidence is a red flag, not a good result.
- Report **coverage** alongside confidence. Confidence without coverage is invalid — a high-confidence pick supported
  by almost no data is a hypothesis wearing a number. If the lane's schema has no coverage field, say so rather than
  omitting the caveat.
- Cite the evidence receipt and artifact id the lane emits. An uncited pick is not auditable.
- Scalars sourced from a health endpoint are echoed, not computed locally. Do not report them as organ output.

## 4. Depth, seal and volume — state the gap, do not paper over it

- **Depth conversion.** Without an interval-velocity model or well-tie depth grid, depth is a mapped assumption.
  Report an error per horizon. Never carry a single global depth error, and never quote a depth without saying how it
  was converted.
- **Fault seal.** Without shale-gouge-ratio and juxtaposition analysis, fault seal capacity is unmeasured. Do not
  describe a fault as "sealing" on geometry alone.
- **Volume vs 2-D.** Fault correlation across lines requires a 3-D volume. On 2-D data, cross-line correlation is not
  available and every fault pick is single-line evidence.
- **Authority.** Prospect-evaluation verbs typically require an elevated authority class and will return an authority
  gate / HOLD from a default read-only session. Raise authority before promising prospect numbers.

## 5. Reporting language

Use: "the lane returned a qualified candidate", "the gate returned UNMEASURED", "coverage for this pick is low",
"uncertainty in depth conversion is ±X m for this horizon".

Never use: "the seismic shows", "the fault is", "the prospect contains" — those assert geology the interpreter is not
entitled to assert.

## 6. Supporting files

`references/geox-seismic-lane.md` — the live GEOX interpretation surface: mode list, argument contracts that cause
avoidable failures, and the known gaps of that specific implementation.
`references/basin-dossier-from-public-literature.md` — how to answer a basin/field dossier request when no proprietary
volume exists in the federation: organ coverage-gap read, literature sweep, full-text extraction, and the provenance
labels the deliverable must carry.

## 7. When the organ holds no data for that basin — say so, then build the honest artifact

`geox_basin` resolves against a catalog. A basin outside it returns `Basin data not found` for every basin_name you
try, including lat/lng-only calls (which are rejected earlier for an empty `basin_name`).

- **A coverage gap is not a tool failure.** Do not announce the lane is down, and do not keep re-querying different
  spellings. Catalog absent = this organ cannot witness this basin. Report that, then use the fallback in
  `references/basin-dossier-from-public-literature.md`.
- **After three rejections the GEOX server pauses (~48 s) and rejects again regardless of content.** Change the
  approach or the lane — never re-issue a variant of the same call to "check".
- **A dossier assembled from published papers is a literature synthesis, not an interpretation.** State that in the
  artifact itself, and list the proprietary inputs you did not have (SEG-Y volume, LAS well logs, Petrel picks,
  interval-velocity model, well ties). A reviewer will ask a question that only the volume can answer; the deliverable
  must not imply it can.
- **Never synthesise a pick, depth, or volume figure to fill a gap.** A fabricated number in a review pack is worse
  than an admitted unknown — it survives to the slide and dies under cross-examination, taking the author with it.

---

*DITEMPA BUKAN DIBERI — a pick is a hypothesis until the Earth agrees.*

---

## Related

**`basin-charge-screening`** (category `geo`) — load when the question is whether a basin can charge or cook.
Transition 3 above gates on the petroleum-system events sequence; that skill carries the arithmetic, the minimum
dataset, and the two independent failure modes. A charge question is settleable from published thickness, crust
and gradient data *without* seismic — do not stall it waiting for an interpretation lane.
