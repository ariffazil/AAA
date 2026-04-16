---
name: geo-vision-translator
description: Wraps MMX vision for geoscience content — wireline logs, core photos, seismic slices, hand samples, maps, well schematics. Activates when Arif sends or asks about geological images. Forces GEOX epistemic labels on pixel-derived content: OBS from pixels (direct measurement) vs INT from interpretation. Prevents confident over-claim on visual data.
metadata: {"openclaw": {"emoji": "🪨"}}
---

# GEOX Vision Translator — Pixel Evidence with Epistemic Discipline

When an image enters the reasoning loop, it must be labeled correctly before conclusions are drawn from it. A core photo is OBS pixels → INT reservoir quality. A seismic section is OBS pixels → DER structure → INT geological history.

Never claim more from an image than the pixels actually show.

## Image Types and Their Epistemic Ladder

### Wireline Log (PNG/JPG scan or screenshot)
```
OBS (pixels): Raw log curve values visible at depth points
DER: Porosity, resistivity, gamma converted to log units
INT: Lithology, fluid type, pay zone interpretation
SPEC: Depositional environment (needs regional context)
```

### Core Photo
```
OBS (pixels): Core texture, color, visible fractures, sorting
DER: Nothing — core photo is visual only
INT: Depositional environment, diagenesis, fracture connectivity
SPEC: Reservoir quality — needs lab data
```

### Seismic Section (2D/3D)
```
OBS (pixels): Reflector geometry, amplitude, continuity
DER: Time-depth conversion if tied to wells
INT: Structure, stratigraphy, fluid effects
SPEC: Hydrocarbon presence — needs well confirmation
```

### Hand Sample / Outcrop Photo
```
OBS (pixels): Grain size, color, texture, fossils visible
DER: Nothing
INT: Depositional environment, provenance
SPEC: Age correlation — needs biostratigraphy
```

### Well Schematic / Map
```
OBS (pixels): Well path geometry, formation tops, fault positions
DER: TVD from MD if deviation survey applied
INT: Structural position, trap geometry
SPEC: Hydrocarbon column height — needs pressure/data
```

## Vision Command Reference

```bash
# Local file
mmx vision photo.jpg

# URL
mmx vision describe --image https://example.com/core-photo.jpg --prompt "Describe this core sample"

# With geoscience prompt
mmx vision describe --image <path> --prompt "Identify lithology, note any features relevant to reservoir quality"

# File ID (after upload)
mmx vision describe --file-id file-123 --prompt "What does this wireline log show?"
```

## Required Prompt Suffix

Always append to geoscience vision prompts:
```
Base your description on what is directly visible in the image.
Distinguish between what you observe and what you interpret.
Label any interpretation as speculative if not directly supported by the image.
```

## Output Format for GEOX Vision

```
MMX VISION ANALYSIS:
Image type: [wireline log / core photo / seismic / map / other]
Epistemic layer: [see ladder above]

OBS (directly visible):
- [what is actually in the pixels — be specific: "gamma ray values 40-120 API at 2000-2100m"]

DER (derived if applicable):
- [computed values with method noted]

INT (interpretation — label as INT):
- [what the image suggests beyond direct observation]

SPEC (speculation — label as SPEC):
- [alternative interpretations not directly supported]

Confidence: [HIGH/MEDIUM/LOW]
Limitation: [what the image cannot tell you]
```

## Anti-Overclaim Rules

❌ "This well has 22% porosity"
✅ "The density log trace shows values consistent with ~22% porosity (DER), but actual porosity requires calibration against core data (INT)"

❌ "This is a turbidite sandstone"
✅ "The amalgamated sand bodies with normal grading visible in this core photo are consistent with turbidite deposition (INT); coarse age correlation is SPEC without biostratigraphy"

❌ "The seismic shows a perfect trap"
✅ "The closed contour on this seismic time structure map suggests a four-way closure (INT). Closure is unconfirmed without depth conversion and pressure data (SPEC)"

## When to Trigger

- Arif sends any image with geological content
- Question mentions: "what does this log show", "identify this rock", "interpret this seismic"
- Any `mmx vision` command in context of geoscience
