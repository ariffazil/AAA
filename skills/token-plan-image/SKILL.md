---
name: "token-plan-image"
id: "token-plan-image"
version: 1.1.0
owner: AAA
risk_tier: low
floor_scope: [F1, F2, F4, F7]
description: "Call Qwen Token Plan image models on the Personal allowlist (qwen-image-3.0-pro, wan2.7-image, wan2.7-image-pro). Activate when the user asks to draw, generate, or edit an image via Token Plan."
autonomy_tier: T1
capability_tier: fed-multimodal-vision
ecology_state: WARM
---

Generate or edit an image on **Qwen Token Plan** only. Capability SOT: `CAPABILITIES.json` (`image_out`).

User request: $ARGUMENTS

## Allowlist (exact IDs — do not invent versions)

| Model | When |
|---|---|
| `qwen-image-3.0-pro` | **Default.** Layout, fine text, multilingual fonts, gen+edit, ≤6 outs, 2048² |
| `wan2.7-image` | Faster Wan, ≤2K |
| `wan2.7-image-pro` | 4K t2i, brand color, multi-ref edit (up to 9 images) |

Not on Token Plan Personal allowlist: `qwen-image-2.0`, `qwen-image-2.0-pro`, `z-image-turbo`. Do not call them on this key.

## Steps

1. Prompt + model (default `qwen-image-3.0-pro`) + size (default `1024*1024`).
2. Call Token Plan Singapore (not dashscope-intl pay-as-you-go):

```bash
source /root/.secrets/kunci-root.env
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

3. Image URL from `output.choices[*].message.content[*].image`.
4. Download to `generated_$(date +%Y%m%d_%H%M%S).png`.
5. Return the path.

Edit: `content = [{"image": "<url>"}, {"text": "<edit>"}]`. Prefer `qwen-image-3.0-pro` or `wan2.7-image-pro`.

## Notes

- Credits from Token Plan seat. Video/image burn faster than text.
- `Throttling.AllocationQuota` → seat window exhausted.
- MiniMax media (`minimax-media`) is a different hand. This skill is Qwen Token Plan only.
- Docs: https://docs.qwencloud.com/developer-guides/getting-started/image-models
