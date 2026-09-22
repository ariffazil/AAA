---
id: dashscope-video-generation
description: "Use when generating video via DashScope Wan or HappyHorse."
name: dashscope-video-generation
version: 1.0.0-2026.09.22
owner: curator
capability_tier: fed-multimodal-vision
ecology_state: WARM
---

# DashScope Video Generation

Two model families, two endpoints, two input contracts. Mixing them up is the #1 error.

## Endpoints (MUST match model family)

| Family | Synthesis endpoint | Poll endpoint | Auth key |
|--------|-------------------|---------------|----------|
| **HappyHorse** | `POST https://token-plan.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis` | `GET .../api/v1/tasks/$TASK_ID` (same host) | Token Plan seat key (`QWEN_BAILIAN_KEY`, `QWEN_INDIVIDUAL_API_KEY`, etc.) |
| **Wan** | `POST https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis` | `GET .../api/v1/tasks/$TASK_ID` (same host) | `DASHSCOPE_API_KEY` from kunci-root.env |

Both require header `X-DashScope-Async: enable`.

Wan models do NOT appear in `/v1/models` listing. Verify by submitting a cheap 3s t2v task.

## Models & Input Contracts

### HappyHorse (token-plan)
| Model | Mode | Input |
|-------|------|-------|
| `happyhorse-1.1-t2v` | t2v | `input.prompt` |
| `happyhorse-1.1-i2v` | i2v | `input.prompt` + `input.media` (list of `{type: "first_frame", url: ...}`) |

### Wan (dashscope-intl)
| Model | Mode | Input |
|-------|------|-------|
| `wan2.6-i2v-flash` | i2v | `input.prompt` + `input.img_url` (string, NOT list) |
| `wan2.6-i2v` | i2v | `input.prompt` + `input.img_url` |
| `wan2.5-i2v-preview` | i2v | `input.prompt` + `input.img_url` |
| `wan2.6-t2v` | t2v | `input.prompt` |
| `wan2.5-t2v-preview` | t2v | `input.prompt` |
| `wan2.2-t2v-plus` | t2v | `input.prompt` |
| `wan2.1-t2v-plus` | t2v | `input.prompt` (200s free quota) |
| `wan2.1-t2v-turbo` | t2v | `input.prompt` (200s free quota) |
| `wan2.2-animate-move` | animate | `input.prompt` + `input.img_url` |
| `wan2.2-animate-mix` | animate | `input.prompt` + `input.img_url` |

## Critical: i2v Input Field

- **HappyHorse** i2v: `input.media` = `[{"type": "first_frame", "url": "data:image/png;base64,..."}]`
- **Wan** i2v: `input.img_url` = `"data:image/png;base64,..."` (a plain string)

Using the wrong field returns `InvalidParameter`. HappyHorse rejects `img_url`. Wan rejects `media` list.

## Image Constraints (Wan i2v)

- Dimensions: 240–8000 pixels on each side
- If image exceeds 8000px (e.g. panoramic geological sections), resize with PIL before submitting
- Format: base64 data URI or HTTPS URL

## Common Parameters

```json
{"resolution": "720P", "duration": 5}
```
Resolution: 480P, 720P, 1080P. Duration: 3–10 seconds.

## Workflow

1. Load key: `DASHSCOPE_API_KEY` for Wan, seat key for HappyHorse
2. Encode image to base64 if i2v
3. Submit with correct endpoint + correct input field
4. Poll `GET .../tasks/{task_id}` every 15–20s
5. On `SUCCEEDED`: download `video_url` immediately (OSS URLs expire ~1 hour)
6. Save to target path, verify with `ffprobe`

## Pitfalls

- **Endpoint mismatch**: Wan on token-plan = `Model not exist`. HappyHorse on dashscope-intl = same error. Each family has its own endpoint.
- **Input field mismatch**: Wan i2v with `input.media` = `Field required: input.img_url`. HappyHorse i2v with `input.img_url` = `Field required: input.media`.
- **Image too large**: Wan rejects images >8000px per side. Resize with `PIL.Image.open(path).resize()` before base64 encoding.
- **OSS URL expiry**: Download video immediately after poll returns SUCCEEDED. URLs expire in ~1 hour.
- **Quota exhaustion**: `AllocationQuota.FreeTierOnly` = free tier gone, not lane death. Seat quotas rotate daily.
- **Key parsing**: kunci-root.env uses `export KEY=VALUE` format. Strip `export ` prefix before splitting.
- **Poll timeout**: Use bounded loop (max 40 iterations × 20s), never `while true`.
- **T2V slower than i2v**: T2V takes 2–5 min vs i2v 30–60s. Set timeout accordingly.

## Free Quota Budget (Token Plan, expires Sep 29)

- `wan2.1-t2v-plus`: 200s (highest quality t2v)
- `wan2.1-t2v-turbo`: 200s (fastest t2v)
- `wan2.6-i2v-flash`: 50s (fastest i2v)
- 8 other models: 50s each

## Cross-reference

- `happyhorse-video-api` — original HappyHorse-only skill (user-owned)
- `minimax-cli` — MiniMax direct API fallback
- `token-plan-image` — image generation (not video)
