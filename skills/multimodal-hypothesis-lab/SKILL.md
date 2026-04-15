---
name: multimodal-hypothesis-lab
description: Scientific reasoning loop that uses multiple MMX modalities to test a hypothesis. Activates when: (1) Arif proposes a geological model or interpretation; (2) a complex question needs visual + textual + data evidence; (3) Arif asks to "prove" or "test" an interpretation. Runs: hypothesis → request image/video evidence → mmx vision analysis → GEOX consistency check → CLAIM/PLAUSIBLE/HYPOTHESIS verdict.
metadata: {"openclaw": {"emoji": "🔬"}}
---

# Multimodal Hypothesis Lab — Test Interpretations Across Modalities

Geoscience is not a single-modality discipline. A depositional model must be consistent with core, wireline, seismic, and analogs. This skill runs a multi-step hypothesis test using MMX's modalities as a evidence engine.

## The Hypothesis Test Loop

```
HYPOTHESIS
  ↓ propose in text
PLAN EVIDENCE NEEDS
  ↓ what modalities would confirm or refute?
REQUEST EVIDENCE
  ↓ mmx image (schematic), mmx video (animation), mmx vision (real photos), mmx text (analog data)
ANALYZE EVIDENCE
  ↓ GEOX labels on all evidence
CONSISTENCY CHECK
  ↓ does evidence support / refute / is inconclusive?
VERDICT
  ↓ CLAIM (supported) / PLAUSIBLE (weak support) / HYPOTHESIS (unsupported)
```

## Step-by-Step

### 1. PROPOSE (text)
State the hypothesis clearly with GEOX labels:
```
INT: The Upper Sandstone in Field X is a turbidite channel complex.
SPEC: This interpretation is based on gamma ray log motif alone.
NEEDS: seismic amplitude character + analogous core photo to confirm.
```

### 2. PLAN EVIDENCE NEEDS
What would confirm or refute this? List:
- Seismic section or amplitude map → `mmx image` (schematic) or ask Arif to provide
- Core photo from analogous turbidite → `mmx vision`
- Regional depositional model → `mmx text chat --model MiniMax-Text-01`
- Published analog case → `mmx search`

### 3. REQUEST EVIDENCE
```bash
# Generate schematic of expected seismic character
mmx image "seismic section showing turbidite channel complex, amplitude map, two-way-time depth"

# Request analogous core photo
mmx image "core photo turbidite sandstone amalgamated channels"

# Search published analogs
mmx search "turbidite channel seismic amplitude character field analog"
```

### 4. ANALYZE EVIDENCE (with geo-vision-translator)
For each image received, run through geo-vision-translator to get OBS/DER/INT labels.

### 5. CONSISTENCY CHECK
```
EVIDENCE ITEM 1: [description]
- Supports hypothesis? YES/PARTIAL/NO
- GEOX label: OBS/DER/INT
- Uncertainty: [what it can't confirm]

EVIDENCE ITEM 2: ...
```

### 6. VERDICT

| Verdict | Definition | When to Use |
|---|---|---|
| **CLAIM** | Multiple independent evidence types support it | Consistent seismic + well + analog |
| **PLAUSIBLE** | Some support, but key evidence missing | Supported by one modality, unconfirmed by others |
| **HYPOTHESIS** | Plausible but unsupported | Single line of evidence or theoretical only |
| **REFUTED** | Evidence contradicts the hypothesis | Explicit counter-evidence from data |

## Example Run

**Hypothesis:** "The N5 sandstone in Well A is shoreface, not turbidite."

```
STEP 1 — PROPOSE
INT: N5 sandstone = shoreface depositional environment
SUPPORTING: gamma ray motif blocky,proximal
REFUTING: absence of turbidite indicators

STEP 2 — PLAN
Needed: (1) seismic amplitude at N5 level, (2) analogous shoreface core photo, (3) wireline shape comparison

STEP 3 — REQUEST
mmx image "shoreface sandstone core photo well sorted"
mmx search "shoreface vs turbidite gamma ray motif distinction"

STEP 4 — ANALYSIS (geo-vision-translator on core photo)
OBS: well-sorted, fine-to-medium sandstone, horizontal lamination
INT: consistent with shoreface, not diagnostic of turbidite
SPEC: turbidite would show amalgamation surfaces and clast variety

STEP 5 — CONSISTENCY
Evidence 1 (core analog): SUPPORTS shoreface (partial)
Evidence 2 (regional search): Gamma blocky motif ambiguous — both possible
Evidence 3 (mmx text): Shoreface model plausible but not confirmed

STEP 6 — VERDICT: PLAUSIBLE
"Not refuted, but insufficient evidence to distinguish from turbidite.
Need: biostratigraphy, seismic amplitude at N5, pressure data."
```

## When to Use This Skill

- Arif proposes an interpretation: "could this be a turbidite?"
- Question uses words: "prove", "test", "confirm", "refute", "is this consistent with"
- Complex question that needs multiple angles of evidence
- Any CLAIM that needs cross-modal support before being presented as fact

## Output Format

```
MULTIMODODAL HYPOTHESIS TEST
Hypothesis: [stated clearly with GEOX label]
Confidence before: [HIGH/MEDIUM/LOW]

Evidence gathered:
- [modality] | [finding] | supports: YES/PARTIAL/NO | label: OBS/DER/INT

Consistency: [strong / mixed / weak]

VERDICT: [CLAIM / PLAUSIBLE / HYPOTHESIS / REFUTED]
Confidence after: [HIGH / MEDIUM / LOW]
Remaining gap: [what would upgrade the verdict]
```

## Rules

1. Never present HYPOTHESIS as PLAUSIBLE, or PLAUSIBLE as CLAIM
2. Always specify what evidence would upgrade the verdict
3. Use mmx image for schematics/analogs, not to generate fake data
4. If evidence contradicts the hypothesis, say so — REFUTED is a valid verdict
5. Log to vault999: hypothesis + verdict + key evidence
