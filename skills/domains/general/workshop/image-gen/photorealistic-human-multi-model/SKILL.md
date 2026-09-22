---
name: photorealistic-human-multi-model
description: "Compare photorealistic human images across MiniMax and Qwen."
version: 1.0.0
tags: [minimax, qwen, image-generation, photorealism, multi-model, power-dynamics]
metadata:
  hermes:
    category: creative
    related: [photorealistic-human-image-gen, token-plan-image, minimax-cli]
capability_tier: fed-multimodal-vision
ecology_state: WARM
---

# Photorealistic Human — Multi-Model Comparison

When the user wants to compare image models, or when expression/mood isn't hitting right on one model — generate the same prompt across multiple engines and deliver all variants for human selection.

## Why Multi-Model

Different engines interpret the same prompt differently. MiniMax leans stock-photo-clean. Qwen image-2.0 leans natural-realistic. wan2.7-image-pro leans cinematic. Side-by-side comparison lets the user pick the vibe, not guess.

---

## 1. Model Roster (Proven 2026-08-25)

| Model | Engine | Endpoint | Notes |
|---|---|---|---|
| `image-01` | MiniMax | `api.minimax.io/v1/image_generation` | Clean, sharp, stock-photo feel. API key: `$MINIMAX_API_KEY` |
| `qwen-image-2.0` | Qwen PAYG | `$QWEN_PAYG_BASE_URL/api/v1/services/aigc/multimodal-generation/generation` | Natural, slightly softer. Free-ish tier. |
| `qwen-image-2.0-pro` | Qwen PAYG | Same endpoint, model=`qwen-image-2.0-pro` | Higher quality, slower, more detail |
| `wan2.7-image-pro` | Qwen PAYG | Same endpoint, model=`wan2.7-image-pro` | Cinematic, warm-tone, best for noir/mood lighting |

**⚠️ Token Plan endpoint BUG (2026-08-25):** `$QWEN_BASE_URL` already contains `/compatible-mode/v1`. The skill template appends `/api/v1/services/...` creating a double-path that 404s. **Use `$QWEN_PAYG_BASE_URL` instead** — it points to the correct base without the extra path segment.

### MiniMax API Format
```bash
curl -s "https://api.minimax.io/v1/image_generation" \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"image-01","prompt":"...","aspect_ratio":"3:4"}'
# Response: {data: {image_urls: ["https://..."]}}
# NOTE: key is image_urls (plural array), NOT image (singular)
```

### Qwen PAYG API Format
```bash
curl -s -X POST "${QWEN_PAYG_BASE_URL}/api/v1/services/aigc/multimodal-generation/generation" \
  -H "Authorization: Bearer $QWEN_PAYG_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen-image-2.0","input":{"messages":[{"role":"user","content":[{"text":"..."}]}]},"parameters":{"size":"768*1024","n":1}}'
# Response: {output: {choices: [{message: {content: [{image: "https://..."}]}}]}}
```

---

## 2. Expression Style Pitfalls

### ❌ "Cocky smile" generates a laughing grin
Models default to "smile" = teeth showing, mouth open, eyes crinkled. This reads as *happy/friendly*, not *cocky/dominant*.

**Fix — use explicit negative + spatial language:**
```
cold calm arrogant smirk with one slightly raised eyebrow
half-closed eyes looking down
lips closed, expression says you should be grateful I even acknowledge you
NOT laughing, NOT grinning, NOT showing teeth
```

**Proven phrase bank for cocky alpha expressions:**
- `cold calm arrogant smirk with one slightly raised eyebrow`
- `half-closed eyes looking down at camera with quiet supreme arrogance`
- `lips closed, expression says you should be grateful I even acknowledge you`
- `slight smirk with teeth hidden, eyes locked on camera`
- `one corner of mouth raised, chin tilted up`

### ❌ "Dominant" generates a generic power pose
Models read "dominant" as *standing with arms crossed* — correct but boring.

**Fix — add spatial relationship language:**
```
standing over him, chest puffed, arms crossed, looking down
one hand resting on the worshipper's head like a king
taller by a full head, gaze directed downward
```

---

## 3. Worshipper / Power Dynamics Vocabulary

Models respond to **specific spatial language**, not abstract mood words.

| Abstract (weak) | Spatial (strong, proven) |
|---|---|
| "worshipful" | `kneeling at his feet, gazing up with wide reverent eyes` |
| "submissive" | `head tilted back, eyes closed, pressing face against his chest` |
| "arrogant" | `one eyebrow raised, chin tilted up, half-closed eyes` |
| "powerful" | `legs spread wide, one hand on hip, other arm flexed, chin up` |
| "attractive" | `magnetic presence, everyone in the room turned toward him` |

### Worshipper vocabulary (2026-08-25, Arif session)
These specific phrases produced the correct mood:
- `one trembling hand toward his massive forearm` — desire + reverence
- `kneeling at his feet looking up with adoring reverent grateful eyes knowing his place` — hierarchy
- `reaching one hand toward his chest in worship and awe` — physical connection
- `should be grateful I even acknowledge you` — cold dominance from alpha
- `the worshipper knows his place in abang sado heart` — possessive control

---

## 4. Multi-Model Comparison Workflow

When user says "compare", "contrast", "top 3", or "redo with different model":

1. **Write one canonical prompt** — use the expression + worshipper vocabulary above
2. **Fire all models in parallel** — use `execute_code` or sequential `terminal` calls with `wait` for background jobs
3. **Download all images** to `/tmp/contrast_<model>.png`
4. **Send all with MEDIA: tags** — label each with model name + key difference
5. **Let user choose** — "mana satu paling rasa?"

### Quick comparison set (recommended):
- Model A: `wan2.7-image-pro` — cinematic, warm, best for mood
- Model B: `qwen-image-2.0-pro` — natural, detailed, best for realism
- Model C: `MiniMax image-01` — clean, sharp, best for stock-photo feel

---

## 5. Prompt Template (Multi-Model)

```
Ultra photorealistic [SCENE TYPE] in [LOCATION],
[SUBJECT DESCRIPTION] with [ETHNICITY/PHENOTYPE],
[CLOTHING/STATE], [BODY POSITION/POSE],
[EXPRESSION — use proven phrase bank, NOT abstract words],
[SECOND SUBJECT if any] [SPATIAL RELATIONSHIP with worshipper vocabulary],
[ENVIRONMENTAL PROPS — culturally specific],
[LIGHTING SETUP — direction + color + mood],
shot on [CAMERA] [LENS] f/[APERTURE],
[DEPTH OF FIELD], film grain,
hyperrealistic skin pores and texture,
natural body proportions, no AI artifacts,
[STYLE KEYWORD — cinematic/documentary/editorial/noir]
```

---

*Forged: 2026-08-25 · From multi-model Abang Sado comparison session · DITEMPA BUKAN DIBERI*