---
name: AAA-OCR-optical-compression
license: MIT
description: OCR as optical context compression. Converts documents/images to structured markdown using a VLM cascade (qwen3-omni-flash → Tesseract → RapidOCR). Use when processing scanned documents, tables, charts, or images containing text. Includes F2/F4/F9/F12 constitutional gates. Trigger phrases include "OCR", "extract text from image", "document to markdown", "parse table from image", "scan document".
floor_scope:
- F2
- F4
- F9
- F12
---

# AAA-OCR — Optical Compression Pipeline

> **EUREKA777::OCR_COMPRESSION · 2026-07-31**
> **Insight:** OCR is not text extraction — it's optical context compression.
> **Source:** DeepSeek-OCR paper (arXiv:2510.18234), architecture adapted for af-forge (no GPU).
> **DITEMPA BUKAN DIBERI**

---

## 1. The Insight

DeepSeek-OCR reframes OCR as **context compression**: a vision encoder compresses an image into tokens, the language model decodes those tokens into structured text. The key is that structure (tables, headings, figures, layout) survives the compression.

Before this insight, OCR meant "extract characters from pixels." After: OCR means "compress visual context into token-efficient structured text."

### What This Changes

| Dimension | Old (Tesseract) | New (VLM OCR) |
|-----------|----------------|---------------|
| Output | Raw text blob | Structured markdown |
| Tables | Lost/garbled | Preserved as markdown tables |
| Figures/Charts | Ignored | Described in context |
| Layout | None | Headings, sections, reading order |
| Confidence | None | Per-section confidence scores |
| Injection risk | Low (binary extraction) | High (model can hallucinate) → needs F9 gate |

---

## 2. Cascade Architecture

```
Document/Image Input
       │
       ▼
  555-ASI-VISION (classify)
       │
       ├── Document/PDF → VLM OCR (qwen3-omni-flash)
       ├── Chart/Figure  → VLM Describe (qwen3-omni-flash)
       ├── Simple text   → Tesseract (local, fast)
       └── Ambiguous     → RapidOCR (fallback)
       │
       ▼
  555-ASI (F12 INJECTION scan)
       │
       ▼
  Structured Markdown → 333-AGI
```

### Model Tier

| Tier | Model | Cost | Use |
|------|-------|------|-----|
| 1 (VLM) | `mulerouter/qwen3-omni-flash` | $0.0001/1K | Documents, tables, charts |
| 2 (Local) | Tesseract 5.5.0 | FREE | Simple text, fast batch |
| 3 (Local) | RapidOCR 3.9.1 | FREE | Chinese/mixed scripts |

---

## 3. OCR Prompt Templates

Based on DeepSeek-OCR's prompt patterns, adapted for qwen3-omni-flash:

### Document → Markdown (primary)
```
<|grounding|>Convert this document to markdown. Preserve all headings, tables, lists, and reading order. For any figures or charts, describe them briefly. Output ONLY the markdown — no preamble.
```

### Free OCR (text-only, no layout)
```
Free OCR this image. Extract all visible text. Do not describe images.
```

### Figure/Chart Parsing
```
Parse this figure. Describe what it shows — axes, trends, data points. Be specific about numbers.
```

### Table Extraction
```
Extract all tables from this document as markdown tables. Include all rows and columns.
```

---

## 4. Constitutional Gates (555-ASI)

Every OCR output passes through these before reaching 333-AGI:

| Floor | Gate | Action |
|-------|------|--------|
| **F2 TRUTH** | Epistemic label | Every section tagged OBS (machine-read text) or DER (model-described figure) |
| **F4 CLARITY** | Structure check | Output must be valid markdown. Raw blobs rejected. |
| **F9 ANTI-HANTU** | Hallucination scan | "The document says X" — but is X actually in the pixels? Low-confidence DER must be flagged. |
| **F12 INJECTION** | Adversarial scan | Text extracted from images scanned for prompt injection patterns. |

---

## 5. Integration Points

### 5.1 Hermes (Telegram)

When Arif sends an image to Telegram:
1. Hermes receives image → classifies as OCR-needing
2. Routes to 555-ASI-VISION with document prompt
3. Returns structured markdown
4. F12/F9 gate before response

### 5.2 OpenCode (A-FORGE)

`forge_document_ingest` upgrade:
1. Detect document type (PDF → PyMuPDF extract pages as images → VLM OCR)
2. Simple images → VLM OCR directly
3. Fallback to Tesseract if VLM fails

### 5.3 All AAA Agents

Any agent can call `555-ASI-VISION` with OCR prompt. The output is always gated through 555-ASI before reaching reasoning.

---

## 6. Non-Goals

- NOT self-hosting DeepSeek-OCR (no GPU on af-forge)
- NOT replacing Tesseract — it's the fast local fallback
- NOT adding new MCP tools — this is a routing upgrade, not a new surface

---

## 7. Test Criteria

```
1. Send document image → get structured markdown back (not raw text)
2. Table in document → markdown table in output
3. Chart in document → described in output, not ignored
4. Adversarial text hidden in image → F12 injection scan catches it
5. Low-quality image → confidence < 0.70 → output flagged as DER, not OBS
```

---

*Forged from DeepSeek-OCR (arXiv:2510.18234) · Adapted for af-forge CPU-only VPS*
*Cascade: VLM (qwen3-omni-flash) → Tesseract → RapidOCR*
*Gate: 555-ASI F2/F4/F9/F12*
