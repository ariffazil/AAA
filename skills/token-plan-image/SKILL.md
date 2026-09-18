---
name: "token-plan-image"
id: "token-plan-image"
version: 1.0.0
owner: AAA
risk_tier: low
floor_scope: [F1, F2, F4, F7]
description: "Call the Qwen Token Plan text-to-image / image-edit models (qwen-image-2.0, qwen-image-2.0-pro, wan2.7-image, wan2.7-image-pro) to generate or edit images. Activates when the user asks to draw or generate images."
autonomy_tier: T1
---

Call the Qwen Token Plan multimodal-generation API to generate (or edit) an image.

User request: $ARGUMENTS

## Steps

1. Extract prompt (image description), model (default `qwen-image-2.0`), and size (default `1024*1024`) from the user request. If the user explicitly specifies a model (e.g. `model=wan2.7-image` or `use wan2.7-image-pro`), use that model name exactly. Available models: `qwen-image-2.0`, `qwen-image-2.0-pro`, `wan2.7-image`, `wan2.7-image-pro`.

2. Call the API (use bash):

```bash
source /root/.secrets/vault.env
curl -s -X POST "https://token-plan.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
  -H "Authorization: Bearer $QWEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "<MODEL>",
    "input": {
      "messages": [{"role":"user","content":[{"text":"<PROMPT>"}]}]
    },
    "parameters": {"size":"<SIZE>", "n": 1}
  }'
```

3. Extract the image URL from `output.choices[*].message.content[*].image` in the response JSON.

4. Download the image:

```bash
curl -sL -o "generated_$(date +%Y%m%d_%H%M%S).png" "<URL>"
```

5. Display the generated image file path to the user.

## Notes

- Token Plan Team Edition — Credits deducted from seat monthly quota (RM0 marginal).
- `qwen-image-2.0-pro` and `wan2.7-image-pro` are higher quality / slower.
- For image editing (input image + edit prompt), use `wan2.7-image-pro` with `input.messages[0].content = [{"image": "<input_url>"}, {"text": "<edit prompt>"}]`.
- wan2.7-image-pro supports multi-image fusion (up to 9 inputs) + 2K output.
- Base64 payloads MUST go via file (`-d @file.json`), not inline.
- If HTTP 400 `Throttling.AllocationQuota` → seat quota exhausted. Check https://home.qwencloud.com/billing/subscription/token-plan
- If HTTP 200 `InvalidApiKey` → key expired/deactivated. Rotate in /root/.secrets/kunci-mas.env.
