# Worship-scene recipe — Bailian PAYG wan2.7-image-pro (verified 2026-08-14/15)

Two-subject muscle-worship scenes (sado + smaller admirer). Proven across
multiple sessions when Gemini is rate-limited or identity preservation is not
required (both subjects are generic/fictional, not real people).

## Endpoint + auth

```
POST https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
Authorization: Bearer $BAILIAN_PAYG_API_KEY   (from /root/.secrets/kunci-mas.env)
```

**Key confusion pitfall:** THREE different Qwen keys exist —
`BAILIAN_PAYG_API_KEY` (this route, credit-based) ≠ `BAILIAN_TOKEN_PLAN_API_KEY`
(quota-based Token Plan, different endpoint) ≠ `DASHSCOPE_API_KEY`. For image
gen use BAILIAN_PAYG on dashscope-intl.

## Payload (text-to-image)

```json
{
  "model": "wan2.7-image-pro",
  "input": {"messages": [{"role": "user", "content": [{"text": "<PROMPT>"}]}]},
  "parameters": {"size": "1104*1472", "n": 1}
}
```

- Sizes: `1104*1472` (portrait) / `1328*1328` (square) / `1664*928` (landscape)
- **Response returns a HOSTED URL, not base64.** Read
  `output.choices[0].message.content[0].image` → it's a URL. A
  `binascii.Error: Incorrect padding` when base64-decoding the "image" means
  you are decoding a URL string. Download it with a UA header (`Mozilla/5.0`).
- ~60-90s generation, ~3MB PNG output.
- i2v (happyhorse-1.1) needs `input.media: [{url}]` NOT `img_url`, and the
  input image must be a PUBLIC URL — reuse the OSS URL returned here rather
  than re-uploading.

## Prompt skeleton that works (two-subject worship, gym setting)

```
Two men in a hardcore Malaysian gym (kampung-style zinc-roof gymnasium with
basic iron equipment, a Malaysia flag and worn motivational posters on the
wall). A shirtless muscular Malay bodybuilder in his early 30s, Southeast
Asian Malay features, towers above flexing a massive double biceps pose, huge
vascular pecs. In front of him a slim young Chinese Malaysian boy in his
early 20s, boyish face, wearing a loose white t-shirt, reaches up and presses
his hand flat against the bodybuilder's pec in admiration, gazing up in awe.
Hand clearly on the chest muscle. Dramatic low-angle POV, golden hour light
streaming through open windows mixing with warm amber gym lights, dust
particles in the air, sweat glistening, photorealistic, cinematic color
grade, 85mm, 8k detail.
```

Rules encoded above:
1. **Anchor both subjects with explicit ethnicity + age + build + clothing**
   — wan2.7 drifts both faces toward the same ethnicity if unstated.
2. **Name the physical interaction precisely** ("presses his hand flat
   against the pec", "hand clearly on the chest muscle") — vague "admiring
   touch" renders as hovering hands.
3. **Scale cue** — "towers above" + "low-angle POV" sells the size gap.
4. **Malaysian set-dressing block** (zinc roof, flag, worn posters) is
   copy-pasteable for any gym scene in this genre.
5. wan2.7 ignores angle directives sometimes; qwen-image-2.0-pro obeys
   composition better but wan2.7 wins on muscle/anatomy. Bad hands are a
   known wan2.7 weakness — "anatomically correct hands and fingers" helps.

## Known weakness matrix (2026-08-14 zen)

| Model | Anatomy/muscle | Angle obedience | Hands | Face preserve |
|---|---|---|---|---|
| wan2.7-image-pro | **best** | weak | bad | no |
| qwen-image-2.0-pro | good | **best** | ok | no |
| Gemini flash-image | ok | ok | ok | **best** (i2i) |

For i2i identity-preserving edits (real person's face must survive), Gemini
flash-image is the only route — wan2.7 cannot preserve faces.
