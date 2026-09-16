# Physique Topography Invariants

> How to model a human body so a future photo/video can be *corroborated* against them — without ever
> letting a body become an identity. Forged 2026-09-16.

## The layers, in extraction order

```
frame selection        (whole-timeline sample, de-duplicated)
  → person detection
  → pose keypoints
  → pose normalisation     ← pelvis origin, robust long-bone scale
  → relation extraction    ← ratio catalogue
  → evidence classification ← RATIO_INVARIANT | STATE_OBSERVATION | UNUSABLE
  → cross-session compare  ← corroboration only
  → topography record      (append-only, per subject, separate from identity)
```

Only the `RATIO_INVARIANT` family is comparable across sessions. Everything else is a dated state
observation and must be recorded with its date.

## The normalisation recipe (and the correction that matters)

The widely-copied recipe divides by **shoulder width**. On a physique subject that is the pair that
moves MOST with lat spread, flexion, pump and camera elevation — so it injects pose noise into *every*
derived ratio.

Instead: translate so the **pelvic midpoint** is the origin, rotate so the shoulder axis is
horizontal, and divide by the **median of the usable long-bone lengths** (hips→knees, knees→ankles,
shoulders→elbows, elbows→wrists). A single bad landmark then perturbs one term and the median absorbs
it. Exclude shoulder breadth and neck from the scale for exactly the reason above.

If the pelvis is occluded, fall back to the shoulder midpoint and record that as a warning — do not
silently pretend the origin is the same.

## Invariant catalogue

| Invariant | Class | Note |
|---|---|---|
| `arm_span_to_torso` | RATIO_INVARIANT | needs both arms extended or symmetrically flexed |
| `upper_to_lower_arm` | RATIO_INVARIANT | the most clothing-blind limb relation |
| `femur_to_tibia` | RATIO_INVARIANT | unusable under a long-shorts crop |
| `torso_to_femur` | RATIO_INVARIANT | a standing-height proxy needing no calibration object |
| `shoulder_to_hip` | STATE_OBSERVATION | the V-taper proxy; the most pose-variable pair |
| `neck_to_shoulder` | STATE_OBSERVATION | head tilt and camera elevation dominate it |
| `*_height_delta`, `*_reach_delta` | accumulate only | bilateral asymmetry, mirrored axes |

Ratios of **sums of bone lengths** beat two-point ratios: one bad landmark then perturbs only one term.
Use shared dimensions (2D or 3D) when the estimator supplies depth, and degrade to UNUSABLE rather
than raising on a partial frame — a half-occluded frame is a normal input, not an error.

## Coverage groups — why a half-body read must abstain

Split the invariant catalogue into an UPPER group (arm span/torso, upper/lower arm) and a LOWER group
(femur/tibia, torso/femur). A read is only cross-session comparable when it has an anchor in **both**
groups.

This was found by a test that failed: with the whole lower body cropped, the implementation still
reported a quality pass, because 2 of 4 invariants are upper-body-only and the 50 %-coverage rule was
satisfied by the upper body alone. Arms-and-torso-only is the *ordinary* gym framing, so that false
pass would have been the common case, not an edge case. A half-body read degrades to FAIR and abstains
upward.

## Excluded from identity-class evidence (permanently)

Pumped volume, leanness/body-fat state, posture under load, clothing, tan, hairstyle and beard length,
jewellery, temporary marks, background/equipment, watermark, location, camera focal length, crop and
mirroring, and any exercise-specific pose (overhead press, curl, cable pull, lat spread).

**Test to apply:** "would this still hold in a different photo, six months later?" If no →
STATE_OBSERVATION, never identity.

## Asymmetry — record it, do not correct it away

Keep left/right values separate before deriving any symmetry figure, and keep the raw bilateral
deltas. A single frame's asymmetry is usually scapular position, unilateral loading or perspective; it
only becomes evidence when it repeats across independent sessions. Never "correct" asymmetry during
normalisation — that deletes the one signal that might be genuinely identifying.

## Gates binding on any caller

1. **Corroborate, never identify.** The compare step returns CORROBORATES / DIVERGES / AMBIGUOUS /
   INSUFFICIENT. There is no MATCH verdict, because naming requires the face witness **plus** the
   permanent name/history/relations witnesses under quorum.
2. **Abstain upward.** Occlusion, foreshortening, half-body coverage or too few scale segments →
   abstain. Never estimate through it.
3. **No single witness is authority** — quorum ≥3; a modality mismatch escalates.
4. **Consent before template**, for any third party, the same as biometrics.
5. **No 1:N, ever.**
6. **Templates, not photos.** Derived values + provenance; delete raw media after extraction.
7. **Provenance is mandatory.** A ratio without its acquisition conditions is not comparable to the
   same ratio measured another way. Carry source, framing and extractor version with every read.

## Traps when implementing

- **Shoulder width as the scale reference** — the single most common error; see the recipe above.
- **Anterior-only frames passing as good** — the coverage-group rule exists because this failed live.
- **Fixtures that couple the wrong joints.** A test fixture whose hip width tracked shoulder width made
  a scale-contamination test fail for the *wrong* reason. Fixtures must vary one anatomical quantity at
  a time, or they hide real bugs behind fake ones. When a test fails, decide first whether the
  expectation or the implementation is wrong — then fix that one, not the test that complains.
- **A gate that cannot fail is not a gate.** A measurement implementation whose own output was being
  suppressed (e.g. parsing log lines the tool was told not to print) returned a constant and looked
  healthy. Verify a measurement against a known-negative input before trusting it.
- **A doctor that samples one case reports a false green.** A health check probed against a single
  conveniently-cached sample will pass while the real workload fails. Probe a representative set and
  report a **rate**, and never let the single easy sample be the probe.
- **Gait needs walking video.** Deliberate lifting poses are non-cyclic and load-dependent; gym footage
  cannot supply gait. Omit the modality rather than stretching it.
- **Never carry an ID across photos by association.** Context priors set the candidate list; only an
  anchor comparison produces a name.

## Evidence discipline

A real diagnosis of a real body, from real frames, is a *diagnosis* — not a prescription and not a
verdict. State what was read ("anterior-only, gym lighting, legs cropped"), state what follows from
it, state what does not, and never let a body read stand in for a name or a placing.
