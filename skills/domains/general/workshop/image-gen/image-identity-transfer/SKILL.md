---
name: image-identity-transfer
description: Preserve a face from one image into a new composition.
trigger: User asks to swap a face from one reference into another.
version: 1.0.0
owner: 333-AGI
risk_tier: T1
floor_scope: F1, F2, F4, F7, F9
autonomy_tier: T1
capability_tier: fed-multimodal-vision
ecology_state: WARM
forged: 2026-08-28
author: Hermes
license: arifOS
metadata:
  hermes:
    tags: [vision, image-generation, identity-transfer, face-consistency, image-edit, f2, f4, f9]
    related_skills:
      - creative/photorealistic-human-image-gen
      - creative/minimax-cli
      - capabilities/media/AAA-voice-cloning-mimo-minimax
      - forge-vision-densify
      - forge-vss-verifier-suite
---

# Image Identity Transfer — Face Consistency Across Compositions

> **The hardest image-edit problem in the federation: keep the face, change everything else.**
> Without the right model, the agent silently fabricates a new face and tells you the swap worked.

## When to Use

- User provides 2 images and asks to put the identity (face + body type) of one into the composition of the other.
- User asks for a "face swap", "identity transfer", "replace person in image A with person in image B", or "preserve face, change everything else."
- User wants the same person rendered in a new pose, setting, or lighting.

**Do NOT use** for: text-driven new image generation (use `photorealistic-human-image-gen`), text editing inside an existing image (use `image-text-editing`), inpainting a specific region, or video identity preservation (much harder, no working stack yet).

## The One Rule (F2 TRUTH)

When the user asks for an "identity swap" / "replace person in image A with person in image B", the result has only two acceptable states:

1. **True identity transfer** — the rendered face matches the reference person's face (identity preserved).
2. **Honest fallback** — the agent tells the user upfront: "I don't have a tool that does true identity transfer right now; the model will invent a new face. Do you want me to proceed and you pick the best one?"

The forbidden third state is: **silently deliver a fabricated face and call it a swap.** That's an F2 violation — the output does not match the user's claim.

## Tool Selection — True Transfer vs Invention

| Model | API/tool | True identity transfer? | When to use |
|---|---|---|---|
| `wan2.7-image-pro` (DashScope) | QwenCloud image.py `--model wan2.7-image-pro` with `reference_images` | **YES** — multi-image subject consistency, best on the federation | First choice if available |
| `qwen-image-2.0-pro` (DashScope) | QwenCloud image.py `--model qwen-image-2.0-pro` with `reference_images` | **YES** — fused generation + editing | Alt if wan2.7 unavailable |
| `qwen-image-edit-max` | QwenCloud image.py | YES — 1-6 output variations | When you need multiple options from one call |
| `wan2.5-i2i-preview` | QwenCloud image.py `--model wan2.5-i2i-preview` (async only) | YES — single-image edit | Lightweight alternative |
| MiniMax `image-01` MCP | `mcp__minimax_media__text_to_image` | **NO** — text-to-image only, no `reference_images` parameter | Last resort, only after telling user the model will invent |
| `mmx image generate` | mmx CLI | **NO** — pure T2I | Last resort |
| Pollinations FLUX/SANA | Pollinations API | **NO** | Last resort |

## Failure Mode: Model Fabricated a New Face

This is the failure pattern that happens when an agent uses a T2I model for an identity-swap request:

- User provides 2 images, asks for identity swap.
- Agent uses `MiniMax image-01` MCP (text-to-image only).
- Model receives a text description of a "young Southeast Asian Malay male" — it has never seen the reference face.
- Output: a different but plausible face. The composition, pose, lighting, and background match. The face does not.
- Agent delivers the image saying "swap done." User notices the face is wrong. F2 violation + trust damage.

**The agent must catch this before it happens**, not after.

## The Honest-Disclosure Protocol (F2 + F4)

When the user asks for an identity swap:

1. **Probe tool availability first.** Can I see both reference images? Does the model accept `reference_images`? Is the quota healthy?
2. **If true transfer model available (wan2.7-image-pro or qwen-image-2.0-pro)** — proceed normally, generate n=2 variations, deliver with brief note on what was preserved.
3. **If only T2I model available** — BEFORE generating, tell the user clearly:
   > "I don't have a tool that preserves face identity in image edits right now. The model I'll use will invent a new face from the text description — pose, lighting, background preserved, but the face will be a guess. Want me to proceed so you can pick the best match, or wait until I have a proper identity-transfer model?"
4. **If true transfer attempted but failed (quota, 403, model error)** — fall through to T2I AND disclose: "I tried the identity-preserving model, it failed with [error]. I can either (a) generate T2I approximations and you pick, or (b) wait and retry once the upstream is fixed. Which?"
5. **Never deliver a fabricated face as "swap complete"** — even if the result is compositionally beautiful, the face is not the user's reference.

## Reference Prompt Construction (For True Transfer Models)

For `wan2.7-image-pro` or `qwen-image-2.0-pro` with `reference_images`:

```json
{
  "prompt": "Identity edit: place the subject from the first image (description with concrete details) into the exact composition of the second image (pose, lighting, background). Preserve pose, sheen, lighting, framing, and background exactly. Render hyperrealistic skin texture, natural body proportions, no AI artifacts.",
  "reference_images": [path/to/identity_source.jpg, path/to/composition_source.jpg],
  "n": 2,
  "size": "1024*1024",
  "negative_prompt": "blurry, distorted face, extra limbs, extra fingers, deformed body, plastic skin, AI artifacts, low resolution, watermark, text, logo, two people, crowd",
  "prompt_extend": true,
  "watermark": false
}
```

Two reference images, in order: identity first, composition second. The model needs both to perform the transfer.

## Provider Quota & Auth Pitfalls (seen 2026-08-28)

- DashScope `DASHSCOPE_API_KEY` defaults to free tier. After quota exhaustion, even `DASHSCOPE_PAYG_API_KEY` returns `403 AllocationQuota.FreeTierOnly` until the console setting "use free tier only" is disabled. Fix: `https://dashscope-intl.aliyuncs.com` → account → disable the free-tier-only toggle. The error itself tells the user where to fix it.
- The QwenCloud skill sets `QWEN_PROVIDER=bailian-token-plan` in the vault. The skill's provider registry only ships `dashscope`. Override at invocation: `export QWEN_PROVIDER=dashscope QWEN_BASE_URL=https://dashscope-intl.aliyuncs.com/api/v1` before calling the script.
- `mmx auth status` shows "Not authenticated" if `MINIMAX_API_KEY` is not exported. Set it before running `mmx image generate`.

## When NOT to Use This Skill

- User wants a new image from a text description (not an identity swap) → use `photorealistic-human-image-gen`.
- User wants to add/replace text in an existing image (screenshot, document) → use `image-text-editing` (PIL).
- User wants inpainting of a specific region → that's a separate model class, not covered here yet.
- User wants a video of the new identity → see `minimax-cli` video section; identity preservation in video is even harder than in stills.

## Verification After Render

After a true transfer render, do a visual identity check:
1. Compare face shape, jawline, eye spacing, skin tone, hair line, distinguishing features between reference 1 and output.
2. Compare pose, lighting, background, framing between reference 2 and output.
3. If face match is below ~70% (subjective, but obvious miss = wrong person), say so — don't deliver a fabricated result as success.

## Related Skills

- `creative/photorealistic-human-image-gen` — generating new human images from prompts (no identity transfer)
- `creative/minimax-cli` — mmx CLI for MiniMax T2I (no identity transfer)
- `capabilities/media/AAA-voice-cloning-mimo-minimax` — voice cloning (different modality, same "preserve source identity" pattern)
- `forge-vision-densify` — prompt-densification governance for any vision tool
- `forge-vss-verifier-suite` — post-generation visual verification

## Session Notes

- `references/2026-08-28-dashscope-quota-and-mcp-fallback.md` — first session that exposed the F2 trap. Concrete transcript of the DashScope `FreeTierOnly` 403, the `mcp__minimax_media__text_to_image` no-`reference_images` limitation, and the honest disclosure protocol that was deployed.
