# Qwen PAYG Image Generation — Verified Recipe (2026-08-28)

## Context

`/root/AAA/skills/qwencloud-image-generation/scripts/image.py` is the only standard path to Qwen image-edit models (wan2.6-image, qwen-image-2.0-pro, wan2.7-image-pro). The script is NOT usable out of the box from the loaded `/root/.secrets/kunci-mas.env` because the env exports a non-registered provider name.

## What Breaks Without Override

Default `kunci-mas.env` exports:
- `QWEN_PROVIDER=bailian-token-plan` (NOT registered — script only knows `dashscope`)
- `QWEN_BASE_URL=https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` (token-plan base, not dashscope native)
- `QWEN_API_KEY=...` (Coding Plan `sk-sp-` prefix — fails for image)
- `DASHSCOPE_API_KEY=...` (free tier — quota exhausts)

Result: `Error: Unknown provider 'bailian-token-plan'. Available providers: dashscope` exits at script startup.

## Working Recipe (Verified 2026-08-28)

```bash
bash -lc "set -a; source /root/.secrets/kunci-mas.env; set +a; \
  export DASHSCOPE_API_KEY=\"\$DASHSCOPE_PAYG_API_KEY\"; \
  export QWEN_PROVIDER=dashscope; \
  export QWEN_BASE_URL='https://dashscope-intl.aliyuncs.com/api/v1'; \
  export QWEN_REGION=ap-southeast-1; \
  unset QWEN_API_KEY; \
  python3 /root/AAA/skills/qwencloud-image-generation/scripts/image.py \
    --model <MODEL> --file <REQ_JSON> --output <OUT_DIR> --print-response"
```

Critical overrides:
- `QWEN_PROVIDER=dashscope` — forces the built-in provider (the only one registered)
- `QWEN_BASE_URL=https://dashscope-intl.aliyuncs.com/api/v1` — native dashscope base, NOT the token-plan compatible-mode URL
- `unset QWEN_API_KEY` — prevents the script from preferring the Coding Plan key (which 401s for image)
- `DASHSCOPE_API_KEY=\$DASHSCOPE_PAYG_API_KEY` — uses pay-as-you-go key

## Verified Model Status (under DASHSCOPE_PAYG_API_KEY)

| Model | Status | Notes |
|---|---|---|
| `wan2.6-t2i` | ✅ | T2I default, sync mode, 1024×1024 default |
| `wan2.6-image` | ✅ | Image editing with reference_images, n=1–4 |
| `qwen-image-2.0-pro` | ✅ | Fused gen+edit, 1–3 input images, 1–6 outputs |
| `qwen-image-edit-max` | ✅ | Element-level edits, 1–6 outputs |
| `qwen-image-edit-plus` | ✅ | Element-level edits, 1–6 outputs |
| `qwen-image-edit` | ✅ | Single output only |
| `wan2.7-image-pro` | ❌ 403 | FreeTierOnly — account-level toggle needed |
| `wan2.7-image` | ❌ 403 | Same as above |
| `wan2.5-i2i-preview` | ⚠ async | Uses `/api/v1/services/aigc/image2image/image-synthesis` (different endpoint); works but requires async polling |

## Identity-Swap Request Format (F2: identity source + composition source)

For "replace person in image B with person in image A":

```json
{
  "prompt": "Identity edit: place the subject from the first image (<identity desc>) into the exact composition of the second image (<composition desc>). Preserve pose, sheen, lighting, framing, and background exactly. Render with hyperrealistic skin texture, natural body proportions, no AI artifacts.",
  "reference_images": [
    "/root/.hermes/cache/images/img_<identity-source>.jpg",
    "/root/.hermes/cache/images/img_<composition-source>.jpg"
  ],
  "n": 2,
  "size": "1024*1024",
  "negative_prompt": "blurry, distorted face, extra limbs, extra fingers, deformed body, plastic skin, AI artifacts, low resolution, watermark, text, logo, two people, crowd, childlike proportions, anime, painting, cartoon, illustration, NSFW",
  "prompt_extend": true,
  "watermark": false
}
```

Reference image order matters: identity source FIRST, composition source SECOND.

## Honest Verdict on Identity Fidelity (F9, 2026-08-28)

Text-to-image / image-edit models with reference_images deliver **~75% identity likeness, NOT pixel-perfect face lock**. They preserve composition well; face is identity-styled recomposition (model blends features weighted toward identity source but fabricates details).

For tasks requiring true face identity preservation (>90% likeness), the in-federation stack is insufficient. Required:
- InsightFace / ReActor / InstantID (not currently exposed)
- Nano Banana 3.1 Flash (Gemini `gemini-3.1-flash-image`) via `client.interactions` — closest in-stack option for true identity lock (free-tier GCP key authorizes it; see `references/nano-banana-interactions-2026-08-26.md`)

Tell the user the fidelity tier before delivering. Don't present 75% likeness as if it were a true face swap.

## Key Prefix Cheatsheet

| Env Var | Prefix | Use |
|---|---|---|
| `DASHSCOPE_API_KEY` | `sk-` | Free tier (quota exhausts fast) |
| `DASHSCOPE_PAYG_API_KEY` | `sk-ws-` or `sk-cp-` | **Pay-as-you-go — use this for image** |
| `QWEN_INDIVIDUAL_API_KEY` | `sk-sp-` | **Coding Plan — image models NOT authorized** |
| `QWEN_PAYG_API_KEY` | varies | Often `sk-ws-` (same family as PAYG) |
| `QWEN_TEAM_OWNER_API_KEY` | varies | Sometimes expired (401s) |
| `QWEN_HERMES_API_KEY` | varies | Profile-scoped, may be restricted |
| `QWEN_BAILIAN_KEY` | varies | Token-plan lane (Bailian/Aliyun direct) |

## Proven Outputs (Faqwan identity-swap, 2026-08-28)

- `qwen-image-2.0-pro` output: 1 image, identity-styled recomposition, skin tone too pale for Malay phenotype
- `wan2.6-image` n=2: 2 variations, output_2 strongest (warm skin, oil sheen, wall crack pattern preserved, Malay-leaning face)
- `minimax-media.text_to_image` (T2I only, no ref): pose preserved, face fully invented (no identity source)
- Best: `wan2.6-image` output_2 = identity-styled recomposition, but tell user face is ~75% likeness not pixel-perfect

DITEMPA BUKAN DIBERI.
