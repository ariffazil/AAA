# Qwen Image API Discovery — 2026-08-25 Session

## Problem
Token Plan image generation (`$QWEN_BASE_URL`) returned 404 on the multimodal generation endpoint.

## Root Cause
`$QWEN_BASE_URL` = `https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`

The skill template appends `/api/v1/services/aigc/multimodal-generation/generation`, creating:
```
/compatible-mode/v1/api/v1/services/aigc/multimodal-generation/generation
```
This double-path does not exist — 404.

## Working Fix
Use `$QWEN_PAYG_BASE_URL` = `https://ws-wlab8klalfojzq7i.ap-southeast-1.maas.aliyuncs.com`

No `/compatible-mode/v1` prefix needed. Full working path:
```
${QWEN_PAYG_BASE_URL}/api/v1/services/aigc/multimodal-generation/generation
```

## Working Models (PAYG)
- `qwen-image-2.0` — natural, slightly softer output
- `qwen-image-2.0-pro` — higher quality, slower
- `wan2.7-image-pro` — cinematic, warm-tone

## MiniMax API (separate endpoint)
- Base: `https://api.minimax.io/v1/image_generation`
- Response shape: `{data: {image_urls: ["https://..."]}}` — note `image_urls` (plural array), NOT `image` (singular)
- Auth: `Authorization: Bearer $MINIMAX_API_KEY`

## Size Parameter
- Qwen: `"size":"768*1024"` (asterisk separator)
- MiniMax: `"aspect_ratio":"3:4"` (colon separator)
