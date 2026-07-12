---
agent: hermes-asi
name: Hermes Multi-Modal Bridge
skill_id: hermes-multi-modal-bridge
version: 1.0.0
description: >
  A2A protocol bridge for routing multi-modal inputs (vision, audio,
  video, document) through Hermes to the reasoning and execution layers.
  Hermes receives the raw modality, classifies it, extracts structured
  content, and routes to the correct organ (GEOX for seismic images,
  WELL for biometrics, WEALTH for documents, A-FORGE for code diagrams).
  Use when Arif sends or references an image, audio file, video, scanned
  document, or any non-text input that needs governed processing.
owner: HERMES-ASI / 555-ASI
risk_tier: low
floor_scope: [F2, F4, F9, F10]
autonomy_tier: T1
tags: [hermes, multimodal, vision, audio, bridge, a2a]
forged: 2026-07-13
dependencies:
  servers:
    - geox-mcp
    - well-mcp
    - wealth-mcp
  tools:
    - vision_analyze
    - text_to_speech
    - image_generate
---

# HERMES Multi-Modal Bridge

## Purpose

Route non-text inputs to the correct federation organ for governed processing.
Hermes is the SOUL layer — it receives the raw modality, extracts the intent,
and dispatches to the right executor.

## Modality Routing Table

| Input Type | Classify As | Extract | Route To | Tool |
|------------|-------------|---------|----------|------|
| Seismic image | GEOX_VISION | Structural features, horizon picks | GEOX | geox_vision |
| Well log screenshot | GEOX_WELL | Curve shapes, formation boundaries | GEOX | geox_well_desk_open |
| Body image | WELL_SOMATIC | Posture, nervous system state | WELL | well_detect_boundary |
| Audio/file/voice memo | WELL_AUDIO | Emotional tone, energy level | WELL | well_classify_state |
| Document/PDF | WEALTH_DOC | Financial terms, contract clauses | WEALTH | wealth_capital_wisdom |
| Code diagram | FORGE_DIAGRAM | Architecture, flow, dependency | A-FORGE | forge_execute |
| Satellite/map | GEOX_MAP | Bounding box, spatial context | GEOX | geox_map_context_scene |
| Unknown | HERMES_CLASSIFY | Ask Arif for context | HERMES | clarify |

## Bridge Protocol

### Step 1: Receive
```python
# Arif sends image/audio/file
modality = classify_input(source)  # image/audio/video/document/unknown
```

### Step 2: Extract
```python
# Use available tools to extract content
if modality == "image":
    content = vision_analyze(source, question="Extract structured content")
elif modality == "audio":
    content = "Audio received — route to WELL for state classification"
```

### Step 3: Route
```python
# Route to the correct organ via the routing table
organ, tool = resolve_route(content, routing_table)
# Execute via MCP bridge
result = arif_route(intent=content, organ_tool=tool)
```

### Step 4: Return
```
— Output the organ's response with modality tag
— Include source reference: [MODALITY: type | ORGAN: name | TOOL: tool]
— If routing fails: "Gambar/audio ni tak clear untuk mana-mana organ.
   Boleh explain context sikit?"
```

## Invocation

```
Canonical: skills/HERMES-multi-modal-bridge/SKILL.md
Route: hermes-asi → organ MCP → governed result
```

---
*DITEMPA BUKAN DIBERI — arifOS Federation · Hermes ASI SOUL Layer*
