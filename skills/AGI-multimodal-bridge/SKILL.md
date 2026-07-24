---
name: AGI-multimodal-bridge
description: 'Multi-modal reasoning bridge — unifies text, image, tabular data, and
  geospatial evidence into a single reasoning chain. Routes visual analysis through
  GEOX vision pipeline, tabular data through WEALTH compute, and text through standard
  LLM reasoning. USE WHEN: "analyze this image + data", "combine visual and textual
  evidence", "multi-modal prospect evaluation".

  '
version: 1.0.0
tags:
- multimodal
- reasoning
- bridge
- vision
- data
- F4
- F8
floor_scope:
- F02
- F04
- F08
owner: AAA
---
# AGI-multimodal-bridge

## Purpose
Real-world evidence is multi-modal: seismic images, well logs (tabular), geological descriptions (text), financial projections (structured data). This skill bridges modalities into unified reasoning.

## Modality Pipeline
1. **Detect** — Identify modalities present in input (text, image, table, geospatial)
2. **Route** — Send each modality to its native processor:
   - Text → LLM reasoning (sequential-thinking)
   - Image → GEOX vision pipeline (geox_vision) or native vision model
   - Table → WEALTH compute pipeline or pandas/numpy analysis
   - Geospatial → GEOX map layers (geox_map_layers_list)
3. **Fuse** — Combine processed outputs into unified evidence frame
4. **Reason** — Run cross-modal reasoning chain (observation → signal → narrative)
5. **Label** — Tag each fused claim with epistemic rung and confidence

## Fusion Rules
- Cross-modal corroboration raises confidence (two modalities agreeing > one)
- Cross-modal contradiction triggers F2 TRUTH escalation
- Missing modality is noted, not fabricated (F7 HUMILITY)

## Floors
- F2 TRUTH: Each modality processed with appropriate fidelity bounds.
- F4 CLARITY: Fused output must be clearer than any single modality.
- F8 GENIUS: Cross-modal synthesis must produce insight > sum of parts.
