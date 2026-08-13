# Open-Source Image Edit Models — Landscape (2026-02 / KDnuggets)

Source: https://www.kdnuggets.com/5-open-source-image-editing-ai-models (2026-02-04)

## The 5 Models

### 1. FLUX.2 [klein] 9B — Black Forest Labs
- Unified gen+edit in single 9B architecture
- Sub-second inference on consumer hardware
- Multi-reference editing (multiple input images)
- Undistilled foundation — full control, diversity
- **Use case:** Real-time prototyping, fine control
- **Deployed on our endpoints:** Not confirmed

### 2. Qwen-Image-Edit-2511 — Alibaba Cloud
- **Best for identity preservation** (character consistency)
- Multi-person, multi-reference fusion
- Geometry-aware transformations
- Built-in community LoRAs
- Integrates with Diffusers + Qwen Chat
- **Use case:** Character-consistent edits, multi-person scenes
- **Deployed on our endpoints:** NO — returns 404 `Model not exist` on both
  Token Plan and Bailian PAYG as of 2026-08-12. May need DashScope API or
  self-hosting.

### 3. FLUX.2 [dev] Turbo — Black Forest Labs
- Distilled LoRA adapter for FLUX.2 [dev]
- 8-step inference (ultra fast)
- **Use case:** Speed-critical workflows, rapid iteration
- **Deployed:** Not confirmed

### 4. LongCat-Image-Edit — Meituan
- Instruction-driven editing (CN/EN bilingual)
- Preserves non-edited regions strongly
- Multi-step and reference-guided workflows
- **Use case:** Complex multi-step edits
- **Deployed:** Not confirmed

### 5. (5th model not detailed in extracted content — article was truncated)

## Current Capability Assessment (2026-08-12)

Models we can actually use RIGHT NOW for identity-preserving edits:

| Model | Endpoint | Identity Preserve | Notes |
|---|---|---|---|
| wan2.7-image-pro | Bailian PAYG ✅ | 5/10 | Over-idealized, plastic skin |
| wan2.7-image-pro | Token Plan | — | Hits quota limit frequently |
| Gemini 3 Pro Image | Google API ✅ | 6/10 | Best realistic lighting |
| Gemini Flash ("nano banana") | Google API ✅ | 6/10 | Best stage photo feel |
| MiniMax image-01 | MCP :18100 | N/A | **GENERATION ONLY** — no reference |
| qwen-image-edit-2511 | — | Expected best | **404 on both endpoints** |
| FLUX.2 klein | — | Unknown | Need to check HuggingFace/Serve |

## To Test: qwen-image-edit-2511 on DashScope

```bash
# If someone deploys qwen-image-edit-2511, try:
export DASHSCOPE_API_KEY="..."
curl -s -X POST "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen-image-edit-2511","messages":[{"role":"user","content":[{"image":"data:image/jpeg;base64,..."},{"text":"Edit prompt"}]}]}'
```

## Key Takeaway

**Generation models ≠ edit models.** When the user provides a real photo and
says "place this person in X scene," you MUST use an edit model, not a
generation model. Generation models will fabricate a completely different person.
