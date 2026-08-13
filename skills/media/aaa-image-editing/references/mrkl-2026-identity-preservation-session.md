# Image Edit Session — MR KL 2026 Bodybuilder Identity Preservation (2026-08-12)

## Context
User provided real photos of a muscular Malaysian bodybuilder (Syed Khairuddin,
D'POPEYE GYM KL) and asked to place him in MR KL 2026 championship scenes.

## Reference Photos Used
1. `img_d263e9665711.jpg` — video screenshot, concrete wall background, 956×1280
2. `img_5e48617daf39.jpg` — second screenshot, different angle, 1076×588 (landscape)

## Approaches Tried (all 4)

### Approach 1: MiniMax image-01 (Generation, NOT Edit)
- **Result:** Fabricated different person entirely
- **User reaction:** Not delivered (caught in pre-check)
- **Lesson:** Generation model on a real-person request = guaranteed identity loss

### Approach 2: Gemini 3 Pro Image (img2img edit)
- **Model:** `gemini-3-pro-image` via `/root/HERMES/scripts/gemini-image.py --image`
- **Result:** 6/10 realism. Regenerated face — different person. Over-exaggerated
  muscles (cartoonish). Mirror geometry errors. Hand anatomy glitches.
- **User reaction:** "Nope. X sama macam muka abang Syed hang."

### Approach 3: Qwen wan2.7-image-pro (Bailian PAYG edit)
- **Model:** `wan2.7-image-pro` via Bailian PAYG endpoint
- **Result:** 5/10 realism. Over-idealized anatomy, plastic skin texture.
  Identity completely lost — generic Southeast Asian bodybuilder template.
- **User reaction:** Delivered as part of ensemble. User chose not to use.

### Approach 4: rembg cutout + Pillow composite
- **Tool:** `rembg` (u2net model) + PIL paste onto generated empty backgrounds
- **Result:** "So fake. Dagu hilang." Background removal artifacts cropped chin/jawline.
  No shadow integration, no lighting match. Obviously pasted-on look.
- **User reaction:** "So fake. Dagu hilang. Ni bukan stage mr KL."
- **Lesson:** rembg loses fine details (chin, ears, hair edges) on muscular subjects
  with complex poses. Composite without relighting = instant fake detection.

### Approach 5: Gemini 2.5 Flash Image ("nano banana") — WINNER
- **Model:** `gemini-2.5-flash-image` via `/root/HERMES/scripts/gemini-image.py --image`
- **Result:** 6/10 realism but BEST identity preservation of all models tried.
  User explicitly requested this model: "Now hang regenerate pakai Gemini nano banana"
- **Key observation:** Flash preserved the spiky bad-boy hairstyle and jawline better
  than Pro or Qwen. Scene felt more natural/photographic.
- **User accepted these outputs** — delivered 3 variants (backstage, stage, winner).

## Model Comparison Summary

| Model | Identity Preserve | Realism | Scene Quality | User Verdict |
|---|---|---|---|---|
| MiniMax image-01 | 0/10 (wrong person) | N/A | N/A | Not delivered |
| Gemini 3 Pro | 3/10 (face regenerated) | 6/10 | Good atmosphere | Rejected |
| Qwen wan2.7 | 2/10 (template bodybuilder) | 5/10 | Decent | Rejected |
| rembg composite | 4/10 (chin lost) | 2/10 (obviously fake) | Poor | Rejected |
| **Gemini Flash** | **5/10 (closest)** | **6/10** | **Best stage feel** | **Accepted** |

## What the User Actually Wanted
"Abang sado Syed paling sado" — the MOST muscular, dominant competitor. Not just
placed in a scene — the alpha. The prompt had to emphasize dominance:
"most muscular, most shredded, everyone else looks small next to him."

## Key Prompt That Worked Best (Gemini Flash)
```
Place this man at [SCENE]. Keep his face and body exactly as shown.
[Scene description]. Same short spiky hair, same jawline, same person.
[Scene details]. Photorealistic. No text.
```

## Open Questions (Unresolved)
- No current API model on this box achieves >6/10 identity preservation for
  muscular subjects. The ceiling is real.
- `qwen-image-edit-2511` (character consistency specialist) returned 404 on both
  endpoints — may need DashScope integration or self-hosting.
- FLUX.2 [klein] edit support not yet deployed on this box.
- Local GPU (RunPod ComfyUI) with IPAdapter/ControlNet could achieve better
  identity preservation but requires setup.
