# MiniMax image-01 Direct Curl (bypass mmx CLI)

**Discovered:** 2026-08-26
**Status:** Working
**Symptom that triggered:** `mmx image generate` returns `{"error":{"code":1,"message":"API error: HTTP 404 (HTTP 404)"}}` for every prompt, even after `mmx auth login --api-key $MINIMAX_API_KEY`.

## Root Cause

`mmx 1.0.22` CLI internally POSTs to `https://api.minimax.io/anthropic/v1/image_generation` (Anthropic-format path), which is a wrong/stale endpoint mapping. The real MiniMax image gen endpoint is `/v1/image_generation` and works with the same `$MINIMAX_API_KEY`.

`mmx auth status` reports `authenticated: true` after login — the key is fine, the routing is wrong.

## Working Recipe

```bash
curl -sX POST https://api.minimax.io/v1/image_generation \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "image-01",
    "prompt": "<prompt text>",
    "aspect_ratio": "3:4",
    "response_format": "url"
  }'
```

Returns JSON: `{"data":{"image_urls":["<signed OSS URL>"]}, ...}`. Download the signed URL with `curl -sL`.

Aspect ratios: `1:1`, `3:4`, `4:3`, `9:16`, `16:9`. Multiple images via `"n": N`. Seed for reproducibility: `"seed": <int>`.

## When To Use

- Any time `mmx image generate` returns 404 — DO NOT retry the CLI, bypass immediately
- When mmx CLI hangs on the spinner without output (also a routing symptom)
- When `mmx auth status` says authenticated but every call 404s

## When NOT To Use

- If you don't have `$MINIMAX_API_KEY` set in env (source `/root/.secrets/kunci-root.env` first)
- For video gen — different endpoint family (`/v1/video_generation`)

## Cost/Quota

Hits the same `general` quota as mmx CLI would have. ~15-25s per call. Verified at ~93% general quota remaining (2026-08-26).