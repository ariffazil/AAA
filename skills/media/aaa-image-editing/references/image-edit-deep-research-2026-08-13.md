# Image Edit Deep Research — Identity Preservation & Prompt Architecture

**Compiled:** 2026-08-13
**Trigger:** Structural audit of `gemini-image.py` image edit workflow

## 1. Semantic Inpainting (Text-Only Masking)

Gemini does NOT expose a binary mask API for `generateContent`. Confirmed from Google docs:
> "There is no documented client-supplied mask/bounding box API for Gemini 2.5 Flash Image."

Instead, use **semantic inpainting** — natural language instructions that describe
what to change and what to lock:

```
Using the provided image, change only the [specific element] to [new element/description].
Keep everything else in the image exactly the same, preserving the original style,
lighting, and composition.
```

## 2. Identity-Preservation Prompt Patterns (Google + community research)

### Identity-locked edit template
```
[Identity lock] → [Edit request] → [Scene detail] → [Technical constraints]
```

Concrete:
```
Place this man at [SCENE]. Keep his face and body EXACTLY as shown.
Same short spiky hair, same jawline, same expression, same person.
[Scene description]. He wears [outfit]. Photorealistic. No text.
```

### Key prompt rules
- Start with "Place this man/woman" — NEVER "Transform into" or "Change to"
- Name specific features: hair texture, jawline, skin tone, expression
- Change ONE variable at a time (outfit OR background OR lighting)
- Every 3-5 edits, re-anchor with the original reference image
- Use concrete nouns not elastic adjectives ("85mm portrait" not "cinematic")
- Hard negatives: "No text, no watermark, no beautification, no skin smoothing"

### Prompt framing taxonomy
| Pattern | Template |
|---|---|
| Identity-locked edit | "Use reference image as identity anchor. Preserve face geometry. Apply only: [changes]." |
| Style transfer | "Preserve facial proportions and identity. Apply [style]. Keep skin texture authentic." |
| Outfit change | "Keep subject identity. Change outfit to [description]. Maintain identical face geometry." |
| Pose/camera | "Maintain identity. Switch to [pose], [camera angle], [lens]. No facial structure changes." |
| Object add | "Preserve identity. Add [accessory]. No changes to facial proportions." |
| Region-bound | "Change only [region]. Foreground subject remains pixel-consistent." |

## 3. Over-Smoothing Root Cause (AAAI 2026 paper)

Generative image models reconstruct the entire image — they don't selectively modify pixels.
Binary masks force "preserve or reconstruct" categories; within reconstruct regions, the
model generates new pixels rather than modifying existing ones. This produces:
- Over-smoothed skin
- Idealized features
- Lost texture (pores, fine lines)

**Our mitigation stack:**
1. Explicit preservation prompts (identity lock at top)
2. Validation reroll (`--validate --check --max-rerolls`)
3. Composite fallback for critical identity
4. `vision_analyze` before every delivery

## 4. Client-Side Compositing (arXiv:2608.02841)

Study tested 6 commercial editing APIs + 1 mask-based inpainting model. Finding:
**client-side masked compositing outperformed all prompt-only approaches** for
identity preservation.

- Median localization ratio: 0.985 (composite) vs 0.538 (prompt-only)
- Mean cost per image: $0.045
- Technique: generate edit on full image, then cut the edited region from the
  response and paste back onto the original photograph through a feathered mask

This validates our composite fallback approach, even though rembg jawline
clipping remains a practical limitation.

## 5. Latent Space Mask Engineering (for diffusion models, reference only)

The dev.to inpainting guide documents two critical rules for mask-based editing:

1. **Feather size:** at VAE downsampling factor f=8, feather < 16px is invisible
   to the model. Working range: 16-32px.
2. **Crop-and-composite:** for sharp results, crop to mask bounding box (25-50%
   padding), generate on crop at native resolution, composite back with pixel-space
   feathered mask. Saves untouched regions as original bytes, not VAE round-trip.

Not directly applicable to Gemini API (no mask input), but informs how we build
composite fallbacks in PIL.

## 6. Model Lineage (as of 2026-08-13)

| Model | Codename | Status | When to use |
|---|---|---|---|
| `gemini-2.5-flash-image` | Nano Banana (legacy) | Active, deprecating | Speed-critical, low-stakes |
| `gemini-3-pro-image` | Nano Banana Pro | Active | Quality-first edits |
| `gemini-3.1-flash-image` | Nano Banana 2 | Recommended successor | General-purpose (not yet in our script) |
| `gemini-3.1-flash-lite-image` | Nano Banana 2 Lite | Fastest+cheapest | High-volume scale |

**Imagen 4** models deprecated Aug 17, 2026 — migrate to Nano Banana family.

## 7. Content Filter Boundary (verified)

| Passes | Gets blocked |
|---|---|
| Cinematic/comedic framing | Explicit sexual acts |
| Suggestive poses, flexing | Graphic content |
| "Movie scene" language | "Make it erotic" language |

Frame as "photorealistic cinematic [dramatic/comedic] scene" to maximize pass rate.
