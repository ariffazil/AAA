# Veo 3.1 API Reference (verified 2026-08-10)

## Endpoint

```
POST https://generativelanguage.googleapis.com/v1beta/models/veo-3.1-generate-preview:predictLongRunning
```

## Auth

**CRITICAL:** Use `x-goog-api-key` HEADER, NOT `?key=` query param.

```bash
-H "x-goog-api-key: $GEMINI_API_KEY"
```

## Request Body

```json
{
  "instances": [{
    "prompt": "YOUR_PROMPT_HERE"
  }]
}
```

**⚠️ NO `config` field.** Returns `INVALID_ARGUMENT: Unknown name "config"` if included.
Duration/aspect default to 8s 16:9. Use Python SDK for full parameter control.

## Response (poll until done)

```json
{
  "done": true,
  "response": {
    "generateVideoResponse": {
      "generatedSamples": [{
        "video": {
          "uri": "https://generativelanguage.googleapis.com/v1beta/files/<id>:download?alt=media"
        }
      }]
    }
  }
}
```

## Download

```bash
curl -sL -o output.mp4 -H "x-goog-api-key: $GEMINI_API_KEY" "${VIDEO_URI}"
```

## Capabilities

- 8-second videos at 720p, 1080p, or 4K
- **Native audio** (AAC stereo, 48kHz) — no separate audio track needed
- Portrait (9:16) and landscape (16:9)
- Video extension
- Frame-specific generation (first/last frames)
- Image-based direction (up to 3 reference images)

## Rate Limiting

Gemini prepayment credits can be depleted. Error:
```json
{
  "error": {
    "code": 429,
    "message": "Your prepayment credits are depleted."
  }
}
```

## vs Omni Flash

| Feature | Veo 3.1 | Omni Flash |
|---|---|---|
| Duration | 8s fixed | 10s |
| Quality | Higher | Lower |
| Audio | Native AAC | Included |
| Auth | Header | Query param |
| Polling | Async (predictLongRunning) | Synchronous |
| Cost | Higher | Lower |
