# ZAI / GLM-Image Route — Verified 2026-08-11 (SADO lane, session 2026-08-11)

When user asks for **"GLM model"** for image generation, route via Zhipu AI (ZAI) at `https://open.bigmodel.cn/api/paas/v4`. Two distinct layers to probe — image models are NOT visible in `/models` catalog.

---

## Probe Sequence

### Step 1 — Catalog probe (chat models only)

```python
import os, requests
ZAI_KEY = os.environ["ZAI_API_KEY"]
BASE = "https://open.bigmodel.cn/api/paas/v4"

r = requests.get(f"{BASE}/models",
    headers={"Authorization": f"Bearer {ZAI_KEY}"}, timeout=15)
chat_models = [m["id"] for m in r.json().get("data", [])]
# 2026-08-11 snapshot: glm-4.5, glm-4.5-air, glm-4.6, glm-4.7, glm-5,
#                     glm-5-turbo, glm-5.1, glm-5.2  (8 chat models)
```

**Catalog returns ONLY chat models.** No image gen here.

### Step 2 — Image gen probe

```python
r = requests.post(f"{BASE}/images/generations",
    headers={"Authorization": f"Bearer {ZAI_KEY}",
             "Content-Type": "application/json"},
    json={"model": "glm-image", "prompt": "...", "size": "1024x1024"},
    timeout=120)
```

ZAI's flagship image model is **`glm-image`** — single name, not `cogview-X` or any other historical variant. **All other model names return 1211 ("model not in catalog").** Probed 2026-08-11: cogview-3, cogview-3-plus, cogview-3-flash, cogview-4, cogview-4-plus, cogview-4-flash, image-01, image-pro, flux-pro, dall-e-3 → all 1211.

---

## Error Code Triage (CRITICAL)

| Code | Chinese msg | Meaning | Action |
|---|---|---|---|
| **1113** | 余额不足 | Balance insufficient — ZAI account depleted | **Top up via Zhipu billing portal, OR route to Gemini Pro.** Do not retry. |
| **1211** | 模型不存在 | Model not in catalog | Wrong model name. Use exactly `glm-image` |
| **1214** | size参数不合法 | Size parameter illegal | CogView supports `1024x1024`, `768x768`, `512x512` only |

---

## Multimodal Variant — Same Credit Pool

`POST /chat/completions` with `glm-4.6` + `modalities: ["image", "text"]` ALSO returns 1113 if balance empty. **All ZAI endpoints (chat + image + multimodal) share ONE credit pool.** Topping up one route covers all.

---

## Verified Fallback Decision Pattern (2026-08-11)

When `glm-image` returns 1113 and user explicitly wants GLM:

1. **Tell user honestly.** Don't fabricate. Don't switch silently.
2. State the truth: "GLM-Image endpoint exists, our ZAI account is at 0 balance."
3. Offer Gemini Pro as proven alternative (macho sado / photorealistic confirmed working).
4. If user wants true GLM-Image: pause for top-up at https://open.bigmodel.cn/billing, then retry.

Arif's response tonight (SADO lane, 2026-08-11): "Ok buat bagi macho habis" → accepted Gemini Pro with explicit GLM-situation disclosure. He didn't ask for top-up; he wanted the image. **Judgment: route to working tool, document the gap.**

---

## Sizing for CogView (`glm-image`)

```json
{"size": "1024x1024"}   // square, highest detail
{"size": "768x768"}     // medium
{"size": "512x512"}     // small, fastest
```

No `9:16` / `16:9` / aspect ratio strings — only square. (If user wants cinematic wide, route to Gemini Pro.)

---

## MiniMax vs Gemini vs GLM Comparison (after 2026-08-11 probe)

| Route | Pros | Cons | Best for |
|---|---|---|---|
| **MiniMax MCP `:18100`** | Camera control (Director models), MCP tooling | Cartoon aesthetic, slow, stricter content filter | Hero videos, camera-movement scenes |
| **Gemini Pro / Flash** | Photorealistic DSLR aesthetic, Malay/SEA preserved, fastest, generous output | No camera control, Pro timeout-prone | Sado portraits, myvi scenes, sensual rasa |
| **ZAI `glm-image`** | Direct GLM family aesthetic | 0 credit on arifOS account tonight, square-only | When top-up available + user wants different aesthetic |

---

## When User Says "Use GLM model"

Quick decision flow:

```
User asks "use GLM model" for image gen
   │
   ├─ Has ZAI account with credit?
   │     ├─ YES → glm-image route, "1024x1024"
   │     └─ NO  → tell user, offer Gemini Pro, get confirmation
   │
   └─ User wants GLM for chat / reasoning?
         → glm-4.6 multimodal (or glm-5.x) — text-only, chat API
```

---

## Pitfall Notes

- **Don't trust `/models` for image gen.** Chat-only listing is misleading.
- **Don't use `cogview-X` model names.** They're deprecated aliases; ZAI consolidated to `glm-image`.
- **Don't fabricate GLM generation when balance is empty.** F2 TRUTH violation + user trust damage.
- **Don't retry 1113.** It's not a transient rate limit — it's zero credit. Retry just costs latency.
- **Don't assume `glm-image` size = `1:1` ratio string.** Use exact pixel values.