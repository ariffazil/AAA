---
name: seismic-interpretation-alignment
id: seismic-interpretation-alignment
version: 1.2.0
description: Use when interpreting seismic or claiming AI picks.
owner: Hermes (curator-managed)
risk_tier: medium
floor_scope: [F1, F2, F7, F9, F11]
autonomy_tier: T1
tags: [seismic, interpretation, geox, structural-geology, avo, horizons, faults, coverage]
capability_tier: fed-agent-subagent
ecology_state: WARM
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

### The epistemic ladder — never let a claim travel above its tier

The three transitions are also three tiers of certainty. A claim may not be asserted at tier N unless the tier below it
has been measured. Climbing a tier is an **inversion**, not an observation.

- **Kinematics — observed displacement field.** Geometry of faults and horizons, cutoff pairs, throw, dip, curvature,
  vergence, azimuth distribution, cross-cutting order. The strongest thing geometry yields, and still relative:
  band-limited, depth-converted, and dependent on operator picks. Observed ≠ assumption-free. A kinematic snapshot is
  compatible with many mechanisms, so it can never carry a regime on its own.
- **Strain — finite strain and rotation.** Extension/shortening magnitude, block rotation, β. Requires a restoration,
  and therefore inherits its assumptions: plane strain, and a declared balance method (line-length for fault-bend
  folding, area for detachment folding — two methods, two domains, never mixed silently).
- **Dynamics — the stress tensor.** Orientation of σ1/σ2/σ3 plus the shape ratio. This is the weakest and most
  under-determined tier: a reduced stress tensor has **4 parameters against the full tensor's 6**, and the absolute
  magnitude is not recoverable from fault data at all — it must be anchored externally (friction law, borehole, focal
  mechanism). Geometry alone supplies fault *plane* orientation; the slip vector needs cutoff-line separation in 3-D,
  so **2-D data can never enter this tier**.

Consequences to enforce in any tool or report:

- Never present a stress tensor, slip tendency (τ/σn), or fluid-migration-from-strain prediction as if it were read from
  seismic. Those need an input tensor that seismic does not contain.
- **Stress ≠ strain.** Seismic records finite displacement, not the force state that produced it. Crossing from one to
  the other requires a constitutive assumption — state it or do not make the crossing.
- A restoration that fails is a **diagnostic, not an error flag**. Non-balance means structure is missing from the
  section, not that the interpretation is wrong. Never instruct an interpreter the other way; it produces picks bent
  until they balance, at the cost of the correct answer.
- Restoration conservation is **conditional**. Bed length and area are conserved only under plane strain, on a section
  parallel to transport, with no penetrative strain, no erosion across an unconformity, and **no mobile ductile unit in
  section**. Where salt or overpressured shale decouples the section the invariant is NOT_APPLICABLE, not violated —
  running it anyway manufactures a false kill. Balancing is an admissibility test, never a proof of correctness.

## 3. Iron rules

- The interpretation organ proposes geometry; it never states geology. Any field meaning "the preferred answer" stays
  null from the organ. Sealing belongs to the kernel, not the interpreter.
- The local maximum is a **qualified candidate**. Never report it as a conclusion.
- Gate verdicts include an UNMEASURED state. **UNMEASURED is not a pass.** Never upgrade it in transit, and never
  average it away.
- **Falsifier direction rule — the single most important gate invariant.** Two directions, two different powers:
  - **Contradiction** = positive counter-evidence MEASURED → a gate **may return KILL**, and may reject a hypothesis.
  - **Deficit** = an expected signature merely ABSENT ("no growth wedge detected", "no flower structure imaged") →
    **UNMEASURED only. Never KILL.**
  The reason is mechanical, not stylistic: an absence test fires on thin data exactly as readily as on a true negative,
  so wiring deficits into a kill set makes the engine reject true hypotheses whenever the data is poor — confident and
  wrong. Gate deficit tests on a coverage fraction and downgrade to UNMEASURED below it. A sub-resolution feature is
  invisible, not absent: a fault moving slower than sediment supply leaves no growth signature at all.
- **A kill must carry its scope.** Say what the kill applies to, because the same counter-evidence refutes claims of
  different sizes. An expansion index ≤ 1 refutes the *syn-tectonic timing of that interval*, not the existence of
  extension. A failed extension/shortening balance refutes the gravity hypothesis *within that linked system*, never
  basin-wide. An unscoped kill silently upgrades a local refutation into a regional conclusion, and the reader cannot
  tell which was meant.
- **Hunt the deficit-as-pass defect in PRE-EXISTING gates before trusting their verdicts.** The rule above is not only
  for code you write. Shared engines commonly return PASS when their inputs are absent, because a missing key falls
  through every branch to a default. Probe the empty case deliberately — call the gate with `{}` and see whether it
  reports PASS or an UNMEASURED-equivalent. Repairing it is a different objective from the lane you are building and
  changes verdicts other lanes consume: report it, do not silently patch it.
- **Determinism means reproducible, not dimensionally true.** A deterministic algorithm returns the same number every
  run; that says nothing about whether the number is the rock. Never label an output "absolute". Image-derived
  geometry is an observation about a picture — only calibrated, depth-converted geometry is an observation about rock.
- **Never accept an injected confidence score.** A supplied figure like `"reliability": 0.95, P(truth) > 0.99` is
  confidence theatre. A confidence value stays null unless a named, versioned, validated benchmark receipt is attached.
  An external proposal that arrives carrying its own probability is a defect to be corrected, not a design to adopt.
- **Prove a gate discriminates — in both directions.** A gate is decoration unless it is shown to (1) change its
  verdict when the defect is present, and (2) stay quiet on clean input. Build the contaminated/clean synthetic pair
  *before* the gate is trusted, and verify a constraint's own test by **deleting the constraint** and confirming the
  test fails — a test that passes with the constraint removed tests nothing. The failure is symmetric: a gate that
  never fires cannot kill a bad claim, and a gate that fires on clean data gets disabled by its users, which is worse
  than not having one. Where a screen legitimately cannot run on the supplied input, it must report NOT_EVALUATED —
  never a silent pass. (This is the general form; the empty-input probe above is one instance of it.)
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
- **Decompact before any thickness argument.** "Constant thickness" in a pre/syn/post-kinematic division means constant
  in *time*, not in *depth*. Compaction thins parallel beds with zero tectonics, so an un-decompacted isopach shows a
  differential whose cause is lithology — and that differential will be priced as growth. Decompaction is mandatory
  before thickness, expansion index, or growth-wedge evidence is used for anything.
- **Uniformity is non-discriminating, not evidence for the null.** A uniform interval does not mean eustasy: steady
  sediment supply, thermal subsidence, pure strike-slip, and post-depositional sag all produce it. The eustatic test is
  a regionally correlative surface with synchronous onlap — not the absence of thickness change. Record such a result as
  NON-DISCRIMINATING, and never as favouring the null hypothesis.

## 5. Reporting language

Use: "the lane returned a qualified candidate", "the gate returned UNMEASURED", "coverage for this pick is low",
"uncertainty in depth conversion is ±X m for this horizon".

Never use: "the seismic shows", "the fault is", "the prospect contains" — those assert geology the interpreter is not
entitled to assert.

**A deterministic lane emits no probability.** It must not return `confidence`, `reliability`, `probability`,
`p_truth`, `score`, or `certainty` — a geometry or computer-vision algorithm cannot produce a probability about
geological truth, and a field named that way is read downstream as one. Emit **coverage, sample count, and
uncertainty bounds** instead, and let the governance layer derive whatever confidence it is entitled to. Hold the
forbidden names in a module constant and check it at every exit point: a single smuggled `confidence` field re-enters
the pipeline looking authoritative, and nothing downstream can tell it was invented.

The same applies to **classifications**. Dip and curvature are measurable; "listric", "growth", "inverted" are
interpretations. A lane may emit such a label only from a **named rule** whose decision inputs are themselves
MEASURED, with the rule named in the receipt. No rule fired → UNMEASURED with a null value. A pipeline that prints a
bare interpretive adjective from a gradient computation is committing the same defect as a fabricated probability.

## 6. Supporting files

`references/geox-seismic-lane.md` — the live GEOX interpretation surface: mode list, argument contracts that cause
avoidable failures, and the known gaps of that specific implementation.
`references/basin-dossier-from-public-literature.md` — how to answer a basin/field dossier request when no proprietary
volume exists in the federation: organ coverage-gap read, literature sweep, full-text extraction, and the provenance
labels the deliverable must carry.
`references/tectonic-regime-deduction.md` — deducing tectonic regime and deformation timing from horizon geometry:
Andersonian dip families, the regime→geometry map, the confounders that flip a call, the falsifier direction applied
per regime, and what geometry cannot decide at all.
`references/expansion-index-extraction.md` — producing or reviewing the code that measures lateral thickness change
between two picks (the EI / growth-wedge axis that K-GROWTH consumes). The four traps: a slop constraint that can
only ever censor correlation rather than steep geology, a phase screen that must be measured outside the interval,
wavelength estimation that lands on bedding interference, and why a scalar velocity leaves an EI unchanged.

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

## 8. Auditing a supplied structural framework before implementing it

Structural frameworks for regime deduction arrive as prose, tables, and threshold lists — often generated by another
model. Audit before implementing; the errors are systematic and predictable. Work in this order:

1. **Decompose every claim into a tier.** Label each asserted fact kinematic, strain, or dynamic. Mis-tiering is the
   most common defect: a stress tensor or a slip-tendency prediction presented as if geometry produced it.
2. **Check the attribution of every named law.** Frameworks mangle authority routinely (cross-cutting and superposition
   are Steno, not Walther — Walther governs lateral continuity of conformable facies). A right rule on a wrong name dies
   under cross-examination and takes the author's credibility with it.
3. **Check dimensional validity of every equation.** A displayed-velocity correction written with a bare 'V' equates a
   dimensionless ratio to a velocity. Also check that the operator matches the data: migrated and unmigrated dips
   follow different trigonometric relations.
4. **Check for category errors.** A process that *decouples or masks* the regional stress field is not a regime within
   it — salt and mobile shale are the standard example, and they invalidate area/bed-length conservation in the same
   section rather than failing it.
5. **Check the framework against itself.** A document that lists a masking process as a regime and simultaneously claims
   universal conservation has contradicted its own table. Internal contradiction is the cheapest defect to find and the
   most damaging to leave standing.
6. **Check the falsifiers for direction.** Any table phrased as "killed if there is no X" is a deficit battery wired
   into a kill set — see the falsifier direction rule in §3. Convert absences to UNMEASURED and require positive
   counter-evidence for kills.
7. **Check whether the proposal re-introduces a defect the codebase already fixed.** Read the live implementation before
   judging the proposal; the engine may already encode the correction.

Then, **before spawning any implementer: probe the target repo for what already exists.** Grep for the engine, the gate
names, and the primitives the proposal asks for, and report the actual delta. A proposal to "build" a capability that
is already present and merely unwired is an integration task, not a build; dispatching a builder produces a duplicate
implementation of the same doctrine, which is worse than doing nothing. State plainly which parts exist, which are
orphaned, and which are genuinely missing — and say so **before** the agents are sent, not after.

When a delta does need parallel implementers, give each a disjoint file list and say so explicitly, forbid mutating git
commands, and require each to run only its own test file: sibling agents mid-write make a full-suite run meaningless.
Also freeze the interfaces before dispatch. Write the contract file (types, signatures, return envelope) yourself and
tell every implementer it is immutable and that deviations must be *reported*, not absorbed — parallel builders of one
new subsystem otherwise invent mutually incompatible designs and the merge cost exceeds the build. Give each brief a
context block listing the packages verified present and absent, so no two agents guess differently about the stack.

### After the writers stop — re-verify, then record the deltas

An audit that runs **concurrently with writers** produces findings that decay while it is still being written. A
reported blocking gap can be closed by a sibling agent minutes later, and a reader who trusts the map then spends
effort on a non-existent blocker. A stale *negative* ("capability absent") is worse still, because it licenses
rebuilding something that now exists.

- **Re-probe every load-bearing finding once all writers have finished.** Not a re-read of the report — a fresh probe
  of the underlying artifact. Files that appeared mid-audit are the ones most likely to invalidate a finding.
- **Encode each finding as an executable test.** A claim about the repo that no test can fail is a claim that rots
  silently; tests also make the next re-verification cheap. A test that documents a known defect's current (wrong)
  behaviour is legitimate and should say so in its docstring.
- **Append a VERIFIED / STALE / CONFIRMED section; do not rewrite the auditor's findings in place.** The original
  report is evidence of what was true at its snapshot, and the delta since is itself the finding. Rewriting destroys
  the only record that the race happened.
- **Distinguish a race artifact from an analyst error.** A finding invalidated only by timing is not a reasoning
  failure, and saying which it is prevents both false blame and false confidence in the rest of the report.

### Before arming what you built

Built, tested, and **not reachable** is the correct resting state until arming is authorised. Reaching a new
capability usually takes two coupled edits — declare the names on the surface manifest, AND mount the server; both or
neither — and it mutates the public tool surface, which is a governed change rather than a build step. Hold the plan
in an importable function that lists the exact edits and returns an explicit unarmed flag, so the decision is made
against an inspectable diff instead of from memory.

**Then find out why the neighbouring capability is currently off.** A hazard can be inert by accident: a lane may be
mounted but undeclared, and the only thing keeping it from running is a registry gate never intended as a control.
Adding that name to the manifest to "make it work" is then the same edit that makes the hazard live. Before promoting
anything onto the public surface, enumerate what else the promotion makes reachable — the blocking gate may be
load-bearing, and "the tool is blocked" is not the same claim as "the tool is safe".

**Check for an import-time blocker before you write the arming plan.** The reachability of a lane is a chain, and the
chain can break somewhere unrelated to the manifest or the mount. An unguarded *optional* dependency converts "feature
absent" into "package broken": a defensive forward-compatibility import (`import client_v2  # migration`) raises
`ModuleNotFoundError` at import time when the package is not installed, and if that module sits anywhere in the
transitive import graph of the server package, the whole package becomes unimportable — every mount path, not just the
one you were tracing. Two consequences:

- **Guard it, and shim it.** Wrap the optional import in `try/except ModuleNotFoundError` and bind a shim that aliases
the name to the installed library, so the defensive intent survives without a hard failure. A duplicate exception class
inside an `except` tuple is harmless; an unimportable package is not. Fixing only the one module you happened to
traverse leaves the sibling breakages in place — grep the whole tree for the bare import.
- **Test the reachability claim rather than reasoning about it.** `import <server_package>` is a one-line probe that
distinguishes "unmounted" from "unimportable", and they need different fixes. A wiring gap reported from static reading
may be a false blocker covering a real one underneath — and if tests must load a module by file path to exercise it,
that workaround is itself the symptom.

---

*DITEMPA BUKAN DIBERI — a pick is a hypothesis until the Earth agrees.*

---

## Related

**`basin-charge-screening`** (category `geo`) — load when the question is whether a basin can charge or cook.
Transition 3 above gates on the petroleum-system events sequence; that skill carries the arithmetic, the minimum
dataset, and the two independent failure modes. A charge question is settleable from published thickness, crust
and gradient data *without* seismic — do not stall it waiting for an interpretation lane.
