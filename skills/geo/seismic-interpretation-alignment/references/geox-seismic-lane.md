# GEOX Seismic Lane — live surface, argument contracts, known gaps

Implementation detail for `seismic-interpretation-alignment`. Verify against the live tool surface before relying on
any of it: when skill and tool surface disagree, the tool surface wins.

## Live modes

`geox_seismic_interpret` exposes: `horizon_contrast`, `fault_sticks`, `track_horizon`, `measure_throw`, `cutoff_throw`,
`structure_validate`, `rsi_pipeline`, `interpret_section`, `interpret`, `segy_slice`, `segy_2d`, `volume_frame`,
`blend`, `render`, `classical_section`, `section_image`.

## Argument contracts that cause avoidable failures

- `horizon_contrast` needs **both** `attribute_data` (dict attr → array) and `depth` (list[float]). It is a 1-D
  multi-attribute boundary detector, not a 2-D section picker. For a section image use `interpret_section` or
  `interpret`.
- `structure_validate` needs `framework` populated with `faults[]` and/or `horizons[]`; called empty it returns
  `EMPTY_FRAMEWORK` rather than defaulting.
- `geox_seismic_compute(mode=avo_forward)` routes to Zoeppritz and requires `theta_deg` plus the two-layer elastic
  triplets (vp/vs/rho per layer).
- `geox_prospect` requires OPERATOR authority; from a default OBSERVE_ONLY session it returns `AUTHORITY_GATE` with a
  HOLD verdict. Raise authority via the kernel init before promising prospect numbers.
- An OBSERVE-only actor can still read basin profiles and compute indicators; only the evaluation verbs are gated.

## Iron rules as implemented (observed in response envelopes)

- `local_verdict: QUALIFIED_CANDIDATE` — the organ never returns a conclusion.
- `preferred_hypothesis` is always null coming out of GEOX.
- Gates return `PASS | WARN | KILL | UNMEASURED` with a receipt hash.
- `claim_tag: HYPOTHESIS` on structural validation output until a higher authority seals.
- `apex_scalars` (G, C_dark, W3, h, QDF) are echoed with `source: arifos.health`; the organ explicitly states it does
  not mint the canonical scalar.
- Every call emits an evidence receipt (sha256) plus an artifact id and an evidence-envelope postcondition verdict.

## Known gaps of this implementation

The interpretation lane reads **image pixels**, not SEG-Y traces. The physical-reality module loads a PNG, extracts
amplitude (R−B for colour seismic, inverted intensity for greyscale), and detects faults and horizons on that array. A
separate trace-level module exists (ingest → header audit → geometry → amplitude preservation → wavelet phase →
attributes) but the interpretation tools do not sit on it.

Consequences to state rather than paper over:

- No depth conversion: no interval-velocity model, no V0-K, no well-tie depth grid.
- No structural restoration engine.
- No shale-gouge-ratio or juxtaposition (fault-seal) calculation — while the regional geology notes for the same
  acreage name fault seal as a primary risk.
- No `coverage_score` in the interpretation output schema, even though the coverage doctrine requires coverage
  alongside confidence.
- No 3-D volume on disk, so `volume_frame` / `segy_slice` cannot correlate a fault across lines.
- Data present is a synthetic section; real volumes must be staged before any interpretation is described as
  volumetric.

## What a useful interpretation response looks like

Given a section image, the honest shape is: the qualified candidates the lane returned, the gate verdict for each
including any UNMEASURED, the count of surviving hypotheses, what coverage exists, what depth-conversion error applies,
and an explicit list of the tests that would discriminate the hypotheses. Then stop — the human seals it.
