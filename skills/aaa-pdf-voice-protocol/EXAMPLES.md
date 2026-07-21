# AAA Voice Protocol — Implementation Examples

Forged 2026-07-21 by FORGE (000Ω) under F13 SOVEREIGN directive.

This file shows the full execution chain — from raw reasoning to published PDF.

## Example 1: Translating the Malay Basin artifact

### Raw reasoning (agent internal — NOT in PDF)

```python
# Internal state machine — uses raw epistemic tags
manifest = ArtifactManifest(
    figures=[
        FigureSpec(
            title="Sundaland EMAG2v3 Magnetic Anomaly + Basin Centres",
            epistemic=[EpistemicLabel.OBS],            # ← raw tag
            caption="EMAG2v3 magnetic anomaly with basin-centre samples. "
                    "geox_falsify(mode='full') returned INCONCLUSIVE for "
                    "the legacy USGS polygons.",
            uncertainty_band={"EMAG2 noise floor": {"central": 0, "sigma_1": 2, ...}},
        ),
    ],
    falsification_refs=[
        {"claim_text": "Sundaland basin architecture from USGS polygons",
         "verdict": "INCONCLUSIVE",                   # ← raw verdict
         "filters": {"passed": 2, "failed": 0, "not_tested": 5}},
    ],
)
```

### After voice_translator.translate_manifest()

```python
# EpistemicLabel.OBS becomes... still an EpistemicLabel enum (backend needs colour)
# But caption text now says:
# "Measured Data: NOAA/NCEI EMAG2v3 magnetic anomaly with basin-centre samples.
#  Regional geophysical validation returned 'requires additional calibration
#  before deployment' for the legacy USGS polygons."
# verdict becomes: "requires additional calibration before deployment"
```

### After compiler filters.enforce_human_cognitive_resonance()

```python
# Any leftover system terms get scrubbed:
#  /root/.cache/geox/emag2/EMAG2_V3_UpCont_DataTiff.tif
#  → (empty)
#  PASS=2 FAIL=0 NT=5
#  → Layers passed: 2 · Layers rejected: 0 · Layers pending data: 5
```

### What the PDF actually shows

> **Figure 1 — Magnetic Anomaly Map of Sundaland with Basin-Centre Measurements**
>
> *Measured Data* · Measured ground-truth evidence from NOAA/NCEI EMAG2v3
>
> *[embedded 1.5 MB magnetic anomaly map with 15 basin-centre samples]*
>
> **Caption.** Magnetic anomaly (NOAA/NCEI EMAG2v3, 2 arc-min global grid) with
> basin-centre measurements overlaid. Malay Basin carries measured ground-truth
> evidence from EMAG2v3 plus the structural framework of Madon (2021). The
> other 14 sampled centres are shown as uncalibrated polygons because no
> subsurface structural model has been built for them in this study.
>
> **Uncertainty Statement (95 % Confidence).** EMAG2v3 noise floor: 0.0 ± 2.0 nT.
> 5×5 pixel smoothing uncertainty: 0.0 ± 5.0 nT.

## Example 2: The 8-check validator at work

```python
v = ClosedLoopVisualValidator()
vresult = v.validate(pdf_path, expected_manifest)

# What runs on every PDF:
#   [1] doc_integrity         — page count, byte ratio
#   [2] epistemic_labels      — OBS/DER/INT/SPEC indicators (raw OR voice)
#   [3] falsification_refs    — verdict text present in render
#   [4] uri_preservation      — declared sources found in render
#   [5] geometry_primitives   — drawing rects within page bounds
#   [6] images                — declared figures vs embedded images
#   [7] constitutional_provenance — actor + session + sovereign anchored
#   [8] human_resonance       — 65 banned terms scanned, none leaked

# If [8] FAILS, validator returns HOLD — Hermes courier blocked.
```

## Example 3: The cost of getting it wrong

If a previous agent had rendered the Malay Basin PDF with:

> "Model B survives with z=0.03 (PASS); Model C is FALSIFIED at z=3.11.
>  Kill Matrix 5/7 NOT_TESTED for Sundaland classification. Source: 
>  /root/.cache/geox/emag2/EMAG2_V3_UpCont_DataTiff.tif. F1 AMANAH verified."

**8th validator result:** `HUMAN_RESONANCE_FAIL` — 7 banned terms detected:
- `z=` (twice), `FALSIFIED`, `Kill Matrix`, `NOT_TESTED`, 
  `/root/.cache/`, `F1 AMANAH`

**Action:** artifact rejected, Hermes courier blocked, agent must rewrite.

That is the architectural guarantee. *Relaks tapi tajam.*
