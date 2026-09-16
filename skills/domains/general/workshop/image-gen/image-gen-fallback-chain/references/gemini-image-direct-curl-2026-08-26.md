# Gemini 2.5 Flash Image — Direct Curl Recipe

**Discovered:** 2026-08-26
**Status:** Working (production-ready for alpha-male / muscular / worship POV framing)
**Why this lane matters:** Strong photorealistic human rendering with Malaysian/Malay phenotype support, handles fine details like cigarette smoke + sweat + hand-on-chest composition well.

## Endpoint

```
POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent
Headers:
  x-goog-api-key: <GEMINI_API_KEY>
  Content-Type: application/json
```

`GEMINI_API_KEY` lives in `/root/.secrets/kunci-root.env`. Auth method: API key header (NOT OAuth).

## Working Body Schema

```json
{
  "contents": [
    {"parts": [{"text": "<prompt>"}]}
  ],
  "generationConfig": {
    "responseModalities": ["IMAGE"],
    "imageConfig": {"aspectRatio": "3:4"}
  }
}
```

Aspect ratios supported: `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `9:16`, `16:9`, `21:9`. Output is inline base64 PNG (NOT JPEG — response_modalities IMAGE always returns PNG; do not request jpeg).

## Response Shape

```json
{
  "candidates": [
    {
      "content": {
        "parts": [
          {"inlineData": {"mimeType": "image/png", "data": "<base64>"}}
        ]
      }
    }
  ]
}
```

Extract via:
```bash
curl ... | jq -r '.candidates[0].content.parts[] | select(.inlineData) | .inlineData.data' > /tmp/img_b64.txt
base64 -d /tmp/img_b64.txt > /root/media/<path>.png
```

Output dimensions: 864×1184 for 3:4 ratio (consistent across calls).

## Strengths (verified 2026-08-26)

- Malay/Malaysian male phenotype: brown skin, stubble, jawline, short hair — renders correctly without explicit "Malay" keyword
- Cigarette + thin smoke wisp: works
- POV hand-on-chest composition: hand reads as separate subject, palm pressed flat works
- Sweat/sheen on skin: rendered as glossy highlights, looks natural
- Chiaroscuro rim lighting: model interprets "rim light" + "chiaroscuro" + "warm tungsten" — but sometimes interprets as cyber-neon instead of pure tungsten (monitor the lighting in delivery)
- Film grain / Canon EOS R5 anchor: model respects camera language

## Pitfalls (verified 2026-08-26)

- **Pose drift:** "chest flex" can render as "vacuum tuck" or "hands clasped below belly" instead of pure peak most-muscular. Specify the exact body position (e.g. "arms up, hands clasped overhead, chest pushed out toward camera") if you need a specific pose.
- **Lighting drift:** "warm tungsten" + "chiaroscuro" sometimes comes out cyber-neon blue/magenta. If you need pure tungsten, push harder: `"single warm tungsten bulb overhead, NO neon, NO cyan"`.
- **Single subject bias:** like SANA, Gemini occasionally drops one element of a multi-subject prompt. For first-person hand-on-chest, the viewer arm usually survives because it's in the foreground (priority bias).
- **Quotas:** `api_key_in_product_not_authorized` means the free-tier Gemini API key does not authorize that specific model. Image gen usually works; Veo 3.1 video typically does not (separate auth tier).

## Cost/Quota

Counts against Google AI Studio free-tier quota for `gemini-2.5-flash-image`. Generous limits for image gen (no observed exhaustion in 3-call session).

## When To Use

- After `mmx image generate` 404 (fall through)
- For Malay/SEA male phenotype where MiniMax would normally be first choice but is misbehaving
- For cigarette/smoke details that other models fumble
- For POV framing with viewer limb in foreground