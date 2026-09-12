# video-ocr-adapter v0 — Specification

> Next build after video-evidence-packager v0.1.0
> DITEMPA BUKAN DIBERI.

## Purpose

Single-frame OCR/vision adapter that takes a keyframe manifest entry from
`video-evidence-packager v0.1.0` and produces a timestamped visual evidence
segment. Not a narrative engine. Not a video understanding system.

## Input contract

```yaml
vision_request:
  video_asset_id: "local:<sha256-prefix>"
  frame_id: "frame:0012"
  source_pts_seconds: 360.033
  frame_sha256: "<sha256>"
  task: "extract visible text only"  # or "describe visual content"
  output_contract: "visual_ocr_evidence_v0"
```

## Output contract

```yaml
visual_ocr_evidence:
  evidence_id: "ev:<uuid>"
  frame_id: "frame:0012"
  modality: "visual_ocr"
  timestamp_seconds: 360.033
  observation: "..."
  confidence: 0.0
  limitations:
    - "Partial frame or illegible areas may be omitted"
  epistemic_label: "OBS"
```

## Allowed tasks

1. `extract_visible_text_only` — OCR: read text visible in the frame.
2. `describe_visual_content` — Brief observation of visual elements (shapes, colors, layout).
3. `read_table_data` — Structured extraction of tabular data from a frame.

## Forbidden

- Narrative summary of "what the video is about."
- Unsupported factual claims.
- Emotion/intent inference.
- External delivery.
- Cross-frame "story" synthesis.
- Persistent graph write beyond locally reviewable evidence artifact.
- Silent confidence inflation.

## Architecture

```
video-evidence-packager v0.1.0
  → keyframes.json (frame entries with timestamps + hashes)
  → pick one frame entry
  → vision_request (timestamped, hash-bound)
  → OCR/vision adapter (local or API, governed)
  → visual_ocr_evidence (OBS-labeled, timestamped)
  → evidence-segments.jsonl (append)
```

## Engine options (to evaluate)

| Engine | Type | Cost | Status | Notes |
|---|---|---|---|---|
| Tesseract | local OCR | free | always available | Basic, no layout intelligence |
| Qwen2.5-VL (Bailian) | VLM API | ~$0.02/page | ready | Layout-aware, bbox support |
| Unlimited-OCR (HF) | VLM local | free | ready | Via HuggingFace Gradio |
| DeepSeek-OCR | VLM | $0 (future GPU) | proposed | 10-20x compression |

## Acceptance criteria (v0)

1. Takes a single keyframe entry from video-evidence-packager output.
2. Produces a structured evidence segment with frame_id, timestamp, SHA-256, and OBS label.
3. No narrative summary produced.
4. No cross-frame synthesis.
5. Receipt includes engine/version used.
6. Failed OCR produces structured failure receipt, not traceback.
7. No external write, no Telegram, no persistent graph write.
8. Deterministic: same frame + same engine = same evidence text.
9. Output appends to evidence-segments.jsonl (not overwrite).
10. All claims labeled OBS, confidence capped at engine-reported level.

## Decision class

This is a **local, read-only, reversible** build — same class as video-evidence-packager v0.
No F13 hold required for building and testing.
F13 required only for: wiring to HERMES runtime, external delivery, or skill creation.
