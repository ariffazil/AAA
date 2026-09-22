---
name: "qwen-token-plan-team-edition"
description: "Use when handling Qwen Token Plan seat configuration or capability URL resolution. Qwen Token Plan seats — capability & OSS URL handling."
version: 1.0.0
author: hermes-curator
license: MIT
metadata:
  hermes:
    category: devops
    tags: [qwen, token-plan, team-edition, aliyun, multimodal, oss]
    related_skills: [token-plan-image, happyhorse-video-api, tokenrouter-guide]
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

## When to Use

- Qwen Token Plan Team Edition returns an unexpected error code (404, 200-empty, 429) and the bundled `token-plan-image` doesn't cover it (Nous Research bundles that as protected, not patchable from this profile)
- Multimodal calls (image / TTS / vision) mysteriously fail even though the model name appears in `/models`
- Downloads from generation endpoints come back as 463-byte XML files instead of PNG/MP4 (OSS signed URL expiry pitfall)
- Comparing quota states across the 4 Team seats (OWNER / Individual / arifOS / ariffazil)
- Wiring `QWEN_*` env vars correctly into agent configs and you need to know which seat actually does what
- A vision LLM call (`qwen-vl-max`) returns `model_not_found` and you need the rename map

## When NOT to Use

- Pure chat completion routing → use `tokenrouter-guide`
- OpenAI/Anthropic API compatibility patterns → see `tokenrouter-guide`
- Local ollama sovereign anchor → not Token Plan territory

# Qwen Token Plan Team Edition — Operational Reality

> **Authored:** 2026-08-18. Fills gaps the bundled `token-plan-image` (Nous Research protected) cannot cover.
> **Scope:** Seat permission model, OSS signed URL handling, vision LLM model renames, multimodal capability matrix for the four Qwen Token Plan Team seats.
> **Out of scope:** Endpoint URLs (already in bundled skills), chat completion patterns (use `tokenrouter-guide`).

## The 4 Seats — What Each Actually Grants

The bundled docs and `kunci-root.env` comments treat seats as interchangeable keys with different quotas. They are not. Each seat has **different capability grants**:

| Seat env key | Display name | Image gen | Vision LLM | TTS | Chat | Status 2026-08-18 |
|---|---|---|---|---|---|---|
| `QWEN_INDIVIDUAL_API_KEY` | qwen-token-plan-individual | ✅ enabled | ✅ enabled | ✅ enabled | ✅ | quota exhausted, resets 21 Aug 03:30 UTC |
| `QWEN_TEAM_OWNER_API_KEY` (= `QWEN_BAILIAN_KEY`) | qwen-token-plan-team (aliyun, Owner · Advanced) | ✅ LIVE — `wan2.7-image-pro` via `/api/v1/services/aigc/multimodal-generation/generation` verified 2026-08-18 | ❌ blocked | ❌ blocked | ✅ LIVE 36288/61291 used |
| `QWEN_API_KEY` (= `QWEN_OPENCODE_API_KEY` = `QWEN_ARIFOS_API_KEY`) | qwen-token-plan-arifos (Admin · Advanced) | ❌ blocked | ❌ blocked | ❌ blocked | ❌ DEAD 0/100000 |
| `QWEN_HERMES_API_KEY` | qwen-token-plan-ariffazil (Admin · Standard) | ❌ blocked | ❌ blocked | ❌ blocked | ❌ DEAD 0/25000 |

### Why the gap?

`/v1/models` lists the model catalog. Seat-level IAM decides which models fire. Even if a seat's `/models` lists `wan2.7-image-pro`, that seat cannot call it without image generation enabled at the seat tier. The Individual seat carries the multimodal grant; the Team Owner seat was originally text-only Advanced but gained image gen access by 2026-08-18.

**Key discovery (2026-08-18):** The Owner seat (`QWEN_BAILIAN_KEY`) returns `wan2.7-image-pro` in its `/models` listing AND successfully generates images via `/api/v1/services/aigc/multimodal-generation/generation`. The old assumption that "Owner seat = text-only" was wrong — it was based on the `/compatible-mode/v1/images/generations` endpoint returning 404, but the correct endpoint for image gen is the multimodal-generation endpoint, not the OpenAI-compatible images endpoint.

### Diagnosis recipe — what does THIS seat actually allow?

```bash
curl -s "https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/models" \
  -H "Authorization: Bearer $KEY" \
  | python3 -c "
import json, sys
d = json.load(sys.stdin)
print([m['id'] for m in d['data'] if any(k in m['id'] for k in ['image','wan','tts','audio','vl'])])
print('Total chat models:', len(d.get('data', [])))
"
```

If the list excludes `wan2.7-image-pro`, `qwen-image-2.0-pro`, `qwen-audio-3.0-tts-plus`, that seat **cannot** do multimodal. Switch to the Individual seat (or wait for quota reset / topup at https://home.qwencloud.com/billing/subscription/token-plan).

### Failure signatures (canonical map)

| HTTP | Body code | Meaning | Fix |
|---|---|---|---|
| 401 | `invalid_request_error: No API-key provided` | Env var empty or unset | `set -a && source /root/.secrets/kunci-root.env && set +a` then re-check `${KEY:0:6}` |
| 401 | `InvalidApiKey` | Key expired or placeholder (`PASTE_HERMES...` style) | Rotate in qwencloud.com → API keys |
| 429 | `Throttling.AllocationQuota` / `insufficient_quota` | Seat quota exhausted (may be weekly or monthly) | Wait for reset OR topup pack |
| 404 | `model_not_found` on `/v1/images/generations` | Wrong endpoint — `/compatible-mode/v1/images/generations` is NOT the image gen API | Use `/api/v1/services/aigc/multimodal-generation/generation` instead (see token-plan-image skill) |
| 200 | `content: []` (empty array on chat-completions) | Model listed in /models but seat doesn't grant it | Same as 404 — switch seat |

## OSS Signed URL Pitfall — Downloads 463-byte XML Errors

Image and video generation endpoints (`/api/v1/services/aigc/multimodal-generation/generation`, `/api/v1/services/aigc/video-generation/video-synthesis`) return Aliyun OSS signed URLs in their `output.choices[*].message.content[*].image` / `output.video_url` fields.

**URL format:** `https://dashscope-<id>.oss-accelerate.aliyuncs.com/...?Expires=<unix-ts>&OSSAccessKeyId=<key>&Signature=<sig>`

**Expiry:** ~1 hour from generation. The signature is HMAC-SHA1 over `(Expires, OSSAccessKeyId, path)` using a temporary access key the API server hands out. Once expired, the server returns:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Error>
  <Code>AccessDenied</Code>
  <Message>Request has expired</Message>
  <Expires>...</Expires>
</Error>
```

— exactly 463 bytes. If you save this as `<file>.png` / `.mp4`, `file img.png` reports `XML 1.0 document, ASCII text` instead of `PNG image data`.

**Symptom chain (recognized 2026-08-18):**
1. Response contains URL with `Expires=` parameter
2. User curls the URL directly with hardcoded signed params from the response
3. URL has already expired (or signature was consumed by an earlier download)
4. Curl writes 463-byte XML body to `<file>.png`
5. `file <file>.png` says XML, not PNG
6. Vision QC fails because vision models can't read XML

**Correct download pattern:**

```python
import urllib.request, os, time

# After generation response:
urls = []
for choice in resp["output"]["choices"]:
    for item in choice["message"]["content"]:
        if "image" in item:
            urls.append(item["image"])

# Download each via urllib — handles signed URL natively
for i, url in enumerate(urls, 1):
    outp = f"/root/.hermes/cache/images/gen_{int(time.time())}_v{i}.png"
    req = urllib.request.Request(url, headers={"User-Agent": "curl/7.81.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    with open(outp, "wb") as f:
        f.write(data)
    print(f"v{i}: {len(data)} bytes -> {outp}")
```

**Forbidden pattern:**

```bash
# ❌ DO NOT — extracts signed URL params from one response, hardcodes in another curl
curl -sL -o "generated.png" "https://dashscope-463f.oss-accelerate.aliyuncs.com/.../...png?Expires=1787073242&OSSAccessKeyId=LTAI5t...&Signature=2x6k3R8w9F4t7Y1n2M5p8Q0s3J6k9L2m"
# ^ signature expired → 463-byte XML written as .png
```

If terminal-only is unavoidable, save the URL list to a text file IMMEDIATELY after the generation response arrives, then download in the same shell session before the expiry hits:

```bash
echo "https://dashscope-.../gen.png?Expires=..." > /tmp/gen_urls.txt
curl -sL -o /root/.hermes/cache/images/gen.png "$(cat /tmp/gen_urls.txt)"
# ^ within seconds of generation, before 1-hour expiry
```

## Vision LLM Renames — `qwen-vl-max` is Dead

`qwen-vl-max` returns HTTP 404 `{"code":"model_not_found"}` on all four Team seats as of 2026-08-18. The model has been renamed. Use:
- `qwen3-vl-plus` (if listed in seat's `/models`)
- A multimodal chat model with `attachment: true` (e.g. `qwen3.8-max`) for image inputs through chat-completions

When in doubt, list the seat's actual vision-capable models:
```bash
curl -s "https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/models" \
  -H "Authorization: Bearer $KEY" \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print([m['id'] for m in d['data'] if 'vl' in m['id'] or 'vision' in m['id']])"
```

## Quota Reset Windows

Different seats reset on different cycles:

| Seat | Cycle | Proven reset time |
|---|---|---|
| Individual (DIIYD...) | Weekly | 21 Aug 03:30 UTC (next reset from 2026-08-18 03:30 UTC) |
| Team Owner (IEHM...) | Monthly / per-pack | Tracks seat tier |
| Team arifOS (DIEXP...) | Monthly (Admin · Advanced 100K) | Reset date not yet verified |
| Team ariffazil (IPRH...) | Monthly (Admin · Standard 25K) | Reset date not yet verified |

Probe reset timing by triggering a 429 and reading the error message body — most Qwen quota errors include `quota will reset at <timestamp>`.

## Fallback Ladder (proven 2026-08-18)

For multimodal work when Token Plan seats are quota-exhausted:

1. **Image gen** → Use Owner seat (`QWEN_BAILIAN_KEY`) via `/api/v1/services/aigc/multimodal-generation/generation` with `wan2.7-image-pro` or `qwen-image-2.0-pro`. Proven working as of 2026-08-18 with 15K+ credits remaining. ⚠️ This does NOT work via `/compatible-mode/v1/images/generations` (returns 404) — must use the multimodal-generation endpoint.
2. **Image gen fallback** → Individual seat (`QWEN_INDIVIDUAL_API_KEY`) when available (weekly reset). Has broader multimodal grant (TTS, vision LLM, image gen all enabled).
3. **Text chat** → use Team Owner seat (always alive, 36K/61K used) or opencode.ai/zen/go (26 chat models, flat-rate subscription)
4. **Video** → happyhorse-1.1-t2v via Individual seat (no i2v — i2v needs dress-the-frame workaround documented in `happyhorse-video-api`)
5. **TTS** → edge-tts `ms-MY-OsmanNeural` (free, no API key, Malay voice) — independent fallback for voice
6. **Sovereign anchor** → ollama local models (qwen2.5-coder:3b) for text

## Reference Files

- `references/seat-quota-snapshot.md` — snapshot of seat quota states with timestamps (append-only history)
- `references/oss-signed-url-lifecycle.md` — full HMAC signing explanation, error body catalog, expiry timing math

## Pitfall — Don't Trust `/models` Listing for Capability

A seat's `/v1/models` returning `["wan2.7-image-pro", ...]` is necessary but not sufficient. The seat may have image-listed but **seat tier denies image generation**. Always probe with a real call (1 token max) before wiring an agent into a workflow:

```bash
curl -s "https://token-plan.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"wan2.7-image-pro","input":{"messages":[{"role":"user","content":[{"text":"test"}]}]},"parameters":{"size":"1024*1024","n":1}}'
```

If response contains `{"code":"AccessDenied","message":"seat not authorized"}` or 403 — pick a different seat. If quota 429 — topup. Only HTTP 200 means go.

DITEMPA BUKAN DIBERI.