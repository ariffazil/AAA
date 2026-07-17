---
name: HERMES-multi-modal-bridge
version: "1.0.0-2026.07.13"
description: "IO boundary protocol for Hermes ↔ 333-AGI multi-modal signal routing. Ingests vision/audio signals from Hermes' creative/media surface and routes them as structured evidence payloads into the reasoning layer. USE WHEN: Hermes encounters an image, audio, or video that requires reasoning beyond creative routing."
domain: hermes
cognitive_engine_notes:
  hermes: "Hermes owns the ingestion gate. Produce structured A2A JSON. Do not attempt reasoning on raw media — route it."
  claude: "When receiving a bridged payload, Claude should look for <evidence_payload> XML blocks and treat them as first-class observation."
  codex: "When receiving, treat `structured_evidence` array as input to chain-of-thought. Each item is an OBS/DER/INT labelled claim."
---

# HERMES Multi-Modal Bridge

## Prime Law

**Hermes ingests. AGI reasons. APEX judges.**

Hermes is the human-facing creative surface — it encounters images, audio, voice, video. Hermes does NOT perform deep reasoning on these signals. It classifies, extracts, and routes them as governed evidence payloads to the reasoning layer (333-AGI).

## Bridge Protocol

### 1. Ingest Gate (Hermes)

When Hermes receives multi-modal content:

```yaml
ingest_classification:
  modality: IMAGE | AUDIO | VIDEO | VOICE | MIXED
  source: TELEGRAM | API | UPLOAD | URL
  requires_reasoning: true | false  # Set true if content needs interpretation
  requires_creative_routing: true | false  # Set true for text-to-image, TTS, etc.
```

### 2. Evidence Extraction (Hermes → Structured Payload)

For content requiring reasoning:

```yaml
evidence_payload:
  bridge_id: "mmb_<timestamp>_<random6>"
  modality: IMAGE
  extracted:
    perceptual_inventory:
      - element: "text visible in image"
        confidence: high
      - element: "chart showing decline from Q1 to Q3"
        confidence: medium
    transcription: "<text extracted from audio/OCR>"
    metadata:
      dimensions: "1920x1080"
      format: "image/png"
      duration_seconds: null
  reasoning_request:
    intent: "Analyze this seismic section for structural traps"
    domain: geox
    urgency: standard
  provenance:
    ingested_by: "hermes-asi"
    ingested_at: "2026-07-13T02:20:00Z"
    source: "telegram_message_id:8471"
```

### 3. A2A Routing (Hermes → 333-AGI)

The payload routes through AAA A2A gateway:

```
Hermes → AAA gateway (port 3001)
       → arif_route(intent="analyze seismic section")
       → 333-AGI (structured evidence in A2A task)
       → arif_judge if decision required
       → Hermes (response payload back to human)
```

### 4. Response Formats

**IMAGE → Reasoning:**

```json
{
  "bridge_id": "mmb_20260713_0215_a3f2c1",
  "modality": "image",
  "agI_verdict": "STRUCTURAL_CLOSURE_DETECTED",
  "confidence": 0.78,
  "evidence": [
    {"claim": "Anticlinal four-way dip closure visible in inline 4200", "label": "OBS", "confidence": 0.85},
    {"claim": "Fault seal risk on eastern flank", "label": "DER", "confidence": 0.60}
  ],
  "requires_human_review": true,
  "routed_to": "geox_seismic_compute"
}
```

**AUDIO → Reasoning:**

```json
{
  "bridge_id": "mmb_20260713_0220_b4d3e2",
  "modality": "audio",
  "transcription": "I need the Q2 production forecast for Bekok field by tomorrow",
  "agI_decomposition": {
    "task": "Generate Q2 production forecast",
    "domain": "geox",
    "subtasks": ["fetch_bekok_production_history", "decline_curve_analysis", "generate_forecast_chart"],
    "estimated_tools": ["geox_well_ingest", "geox_petrophysics", "FORGE-chart"]
  },
  "urgency": "high",
  "deadline": "2026-07-14T00:00:00+08:00"
}
```

### 5. Creative Routing (No Reasoning Required)

When content only needs creative/media routing (no reasoning):

```yaml
creative_route:
  intent: "Generate image of Malay Basin cross-section"
  route: "minimax-media → text-to-image"
  payload: "{prompt, style, dimensions}"
  # Does NOT go through 333-AGI reasoning layer
```

## Anti-Patterns

- ❌ Hermes performing deep geological reasoning on an image — route to AGI
- ❌ Hermes sending raw binary to AGI — always extract structured evidence first
- ❌ Skipping perceptual inventory — AGI needs to know what's IN the image
- ❌ Creative tasks routed through AGI reasoning — wasted compute

## Floor Alignment

| F | Obligation |
|---|-----------|
| F2 TRUTH | Perceptual inventory labeled with confidence per element |
| F4 CLARITY | Structured A2A JSON, never raw binary over the bridge |
| F6 MARUAH | Never describe humans in images without consent context |
| F11 AUDIT | Every bridge has `bridge_id` for traceability |
| F13 SOVEREIGN | Human-in-the-loop for any image of people or sensitive content |

---

*Forged: 2026-07-13 by FORGE (000Ω) under F13 SOVEREIGN directive*
*DITEMPA BUKAN DIBERI*
