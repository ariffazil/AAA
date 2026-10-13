---
name: image-restyle-and-edit
description: "Use when restyling an existing photo (img2img)."
version: 1.0.0
author: hermes
license: MIT
tags: [image-editing, img2img, style-transfer, restyle, dashscope, qwen-image-edit]
metadata:
  hermes:
    category: creative
    related: [image-gen-fallback-chain, minimax-image-gen, photorealistic-human-image-gen]
capability_tier: fed-multimodal-vision
ecology_state: WARM
---

# Image Restyle & Edit (img2img)

Text-to-image **generation** and image **editing** are different lanes with different endpoints.
When the ask is *"buat gambar ni jadi Ghibli"*, *"tukar baju dia jadi X"*, *"jadikan ni poster era 80-an"*
— it is an EDIT of a supplied photo, not a new render. A generation lane cannot do this: it will
silently discard the subject's likeness and hand back a generic stranger.

**Rule: if a source image is supplied and the ask is transformation, use an img2img lane. Never
present a text-to-image result as "your photo, restyled".**

## Lane probe order — probe live, one call each

The image lanes sit on independent accounts. One being dry says nothing about the next.

1. **MiniMax subject reference** — `mmx image generate --subject-ref "type=character,image=<path>"`.
   Keeps the face. Fails with a Token Plan quota message when the plan limit is hit.
2. **Gemini image edit** — `gemini-2.5-flash-image:generateContent` with the source as an inline
   part. The classic "Nano Banana" lane. Fails with `RESOURCE_EXHAUSTED` /
   `prepayment credits are depleted` when billing is empty.
3. **DashScope `qwen-image-edit`** — the lane that works when the paid ones are dry. Recipe below.
4. **Local ComfyUI** — `curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8188/system_stats`.
   Only usable if it answers; it is often not running.

Probe cheaply: one call per lane, read the error signature, fall through. Reshaping the prompt
against a quota-dead lane changes nothing — the rejection is per-account, not per-request.

## Working recipe — DashScope qwen-image-edit

Use the **multimodal-generation** endpoint. `/images/generations` on a Token Plan base URL returns
404 for editing — different host, different path.

```
POST https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
Authorization: Bearer $DASHSCOPE_API_KEY
Content-Type: application/json
```

Body — the source image goes inline as a data URI inside `input.messages[].content[]`:

```json
{
  "model": "qwen-image-edit",
  "input": {
    "messages": [{
      "role": "user",
      "content": [
        {"image": "data:image/jpeg;base64,<B64>"},
        {"text": "<restyle instruction>"}
      ]
    }]
  },
  "parameters": {"negative_prompt": "", "watermark": false}
}
```

The result is a **URL** at `output.choices[].message.content[].image` — download it; do not assume
inline base64. Confirm the file with `os.path.getsize` and convert PNG→JPEG before delivery to keep
the payload small.

## Prompt shape — state KEEP, REDRAW, KILL

Style transfer drifts towards photorealism unless you explicitly kill it. Name all three intents:

> Restyle this photograph into a classic Ghibli hand-painted anime illustration. **Keep** the same
> person, pose, clothing and composition, but **redraw** everything in the Ghibli aesthetic: soft
> cel-shaded character with gentle clean line work, hand-painted watercolour background with visible
> brush texture, warm nostalgic palette, dreamy soft lighting, delicate detail on paving and
> structures. **Remove photorealism entirely.**

The KILL clause is the one that does the work. Without it the model returns a filtered photo.

## Verify before delivering

Run the output through a vision read and confirm the style actually changed and the subject is still
recognisable. A lane can return HTTP 200 with an unchanged or barely-changed image. Check: is it
illustration or photograph? Are the person's clothes, pose and setting still theirs? Only then send.

## Pitfalls

- **`qwencloud` CLI has no image command.** It is an account/usage CLI (models, auth, usage,
  billing). The image lane is the raw DashScope HTTP endpoint. Do not reach for the CLI for pixels.
- **A dry lane is an account condition, not a fact about the tool.** Report which lane served the
  result; do not generalise one quota failure into "image editing is unavailable".
- **Identity loss is the silent failure.** If generation is the only live lane, the output is a new
  person. Say so plainly rather than delivering it as the user's photo.
- **Aspect mismatch.** The edit lane returns roughly 3:4 by default; if the user sent a wide photo
  and expects a wide result, crop-check the output aspect before sending.

## Token Plan vs PAYG keys — probe, don't prose (corrected 2026-10-07)

Three DashScope key flavors live in this environment under different env var aliases
(`DASHSCOPE_API_KEY`, `QWEN_PAYG_API_KEY`, `QWEN_TEAM_OWNER_API_KEY`, etc.). All same family,
just labeled differently per `.env` file.

**Flavor is read by prefix AND endpoint, not env var name alone:**

| Prefix | Account class | dashscope-intl.aliyuncs.com (PAYG base) | token-plan.maas.qwencloudapi.com (Token Plan base) |
|---|---|---|---|
| `sk-ws-` | Workspace / PAYG / free-tier | **200** if budget, **403 `AllocationQuota.FreeTierOnly`** if free quota dry, **429 `Throttling.RateQuota`** if cooldown — route open | **401 `InvalidApiKey`** — this base is not for `sk-ws-` keys |
| `sk-sp-` | Token Plan (Coding Plan) team/individual seat | **401 `InvalidApiKey`** — this base is not for `sk-sp-` keys | **200** — full multimodal-generation route opens; `qwen-image-2.0-pro`, `wan2.7-image-pro`, etc. listed in `/compatible-mode/v1/models` |
| `sk-` (other) | Standard QwenCloud API key | try PAYG; check account status if ambiguous | try Token Plan; check authorization if 401 |

**Discovery recipe (always probe BOTH endpoints, every key flavor):**

```bash
set -a && source /root/.secrets/qwen.env && set +a
PAY_BODY='{"model":"qwen-image-edit","input":{"messages":[{"role":"user","content":[{"text":"x"}]}]},"parameters":{"n":1,"size":"1024*1024"}}'
for V in DASHSCOPE_API_KEY QWEN_PAYG_API_KEY QWEN_HERMES_API_KEY QWEN_TEAM_OWNER_API_KEY QWEN_INDIVIDUAL_API_KEY QWEN_OPENCODE_API_KEY QWEN_ARIFOS_API_KEY; do
  K="${!V:-}"; [ -z "$K" ] && continue
  P="${K:0:5}"
  PAY_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
    "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
    -H "Authorization: Bearer $K" -H "Content-Type: application/json" -d "$PAY_BODY")
  TP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
    "https://token-plan.maas.qwencloudapi.com/api/v1/services/aigc/multimodal-generation/generation" \
    -H "Authorization: Bearer $K" -H "Content-Type: application/json" -d "$PAY_BODY")
  printf "%-32s %-6s pay=%s tp=%s\n" "$V" "$P" "$PAY_STATUS" "$TP_STATUS"
done
```

The matrix output tells you, per key, which base URL actually serves it. Read across
the row, not down the column — a 200 in either column is a working lane.

**The diagnosis mistakes to avoid:**

- Do not write "Token Plan quota exhausted" when a `sk-sp-` key returns 401 at the PAYG base. That's
  not quota — it's the wrong base URL. The Token Plan key class has its own base URL
  (`token-plan.maas.qwencloudapi.com`) where it does return 200. Pointing the user to "top up
  quota" wastes a debug cycle when the real fix is "change the base URL".
- Do not write "PAYG plan needed" when a `sk-ws-` key returns 401 at the Token Plan base. Same fix:
  switch base URL.
- Do not generalize one key's failure to "image editing is broken" without probing at least one
  of each (sk-ws-, sk-sp-) on at least one of each base.

**To list what the Token Plan base exposes for image edit:** hit `GET
https://token-plan.maas.qwencloudapi.com/compatible-mode/v1/models` with the `sk-sp-` Bearer. The
returned list will include `wan2.7-image`, `wan2.7-image-pro`, `qwen-image-2.0`, `qwen-image-2.0-pro`
when Token Plan has the visual lane enabled. If the list is empty or returns 401, Token Plan does
not cover image endpoints for that seat — fall back to a `sk-ws-` PAYG key.

The ready-made script `scripts/probe_visual_lanes.sh` implements the matrix above.

## Source env before testing — naive `os.environ.get` returns shadow

`/root/.secrets/*.env` files are NOT auto-loaded into `os.environ`. A plain
`os.environ.get("DASHSCOPE_API_KEY")` returns `"not set"` even when 8 `.env` files contain the
key. When probing visual lanes, **always `set -a && source /root/.secrets/qwen.env && set +a`
inside the shell call** before checking key status, or you will claim "key absent" while the key
sits unused in a vault file. The probe pattern above uses `source` correctly; copy the pattern
verbatim rather than rewriting it in Python without the source step.

## References

- `scripts/probe_visual_lanes.sh` — non-plaintext diagnostic that sources all `.env` files
  and probes every sk-* key against the multimodal-generation endpoint. Use before claiming
  "lane dead" — distinguishes quota (403/429) from authorization (401) correctly.
