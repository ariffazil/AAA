# MuleRouter API Reference — Verified Endpoints

> Base: `https://api.mulerouter.ai`
> Auth: `Authorization: Bearer $MULEROUTER_API_KEY`
> OpenAI-compatible: `/vendors/openai/v1` — NOT bare `/v1`

---

## Chat / Text

| Model | Endpoint | Verified |
|---|---|---|
| deepseek-v4-flash | `POST /vendors/openai/v1/chat/completions` | ✅ |
| qwen3-max | `POST /vendors/openai/v1/chat/completions` | ✅ |
| qwen3-omni-flash | `POST /vendors/openai/v1/chat/completions` | ✅ |
| deepseek-v4-pro | `POST /vendors/openai/v1/chat/completions` | ✅ |

Standard OpenAI chat format. `model` field selects the model.

## Vision

Same as chat — multi-modal models accept `image_url` in message content.

| Model | Speed | Use Case |
|---|---|---|
| qwen3-omni-flash | ~1030ms | Fast vision perception |
| qwen-vl-max | ~1883ms | Best quality vision |
| qwen3-vl-plus | ~2282ms | High quality |

## Image Generation (GPT Image 2) ✅

```
POST /vendors/openai/v1/gpt-image-2/generation
GET  /vendors/openai/v1/gpt-image-2/generation/{task_id}
```

```json
{
  "prompt": "A red circle on white background",
  "quality": "high",  // high | medium | low | auto
  "size": "1024x1024",
  "n": 1,
  "format": "png"     // png | jpeg | webp
}
```

Response: `task_id` → poll GET until `status: "completed"` → `images[]` with URLs.

## Text-to-Speech (MiniMax) ✅

### HD (higher quality)
```
POST /vendors/minimax/v1/speech-2.8-hd/text-to-speech/generation
GET  /vendors/minimax/v1/speech-2.8-hd/text-to-speech/generation/{task_id}
```

### Turbo (faster, lower quality)
```
POST /vendors/minimax/v1/speech-2.8-turbo/text-to-speech/generation
GET  /vendors/minimax/v1/speech-2.8-turbo/text-to-speech/generation/{task_id}
```

```json
{
  "prompt": "Text to speak",
  "voice_setting": {
    "voice_id": "Wise_Woman",
    "speed": 1.0,
    "vol": 1.0,
    "pitch": 0
  },
  "output_format": "url"
}
```

Known voice IDs: `Wise_Woman`, `male-qn-qingshu` (verify others)

## Async Task Pattern

All generation (image, TTS, video, music) uses the same async pattern:
1. `POST` → returns `{task_info: {id, status: "pending"}}`
2. Poll `GET /.../{task_id}` until `status: "completed"` or `"failed"`
3. Completed response contains the result (images[], audios[], etc.)

## Models List

```
GET /vendors/openai/v1/models
```

## Notes

- `/vendors/openai/v1` prefix is required — bare `/v1` returns 404
- Industry-specific aliases like `/v1/chat/completions` → `/vendors/openai/v1/chat/completions` may NOT work
- All non-chat endpoints are async (task-based)
- Image gen supports up to 4K resolution, 4 images per request
- TTS supports 128kbps MP3 output