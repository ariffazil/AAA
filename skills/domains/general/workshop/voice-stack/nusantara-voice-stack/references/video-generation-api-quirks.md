# MiniMax Video Generation API Quirks (2026-08-18)

## mmx CLI vs raw curl

`mmx video generate` can return HTTP 404 when the CLI's upstream provider map is stale. This is a routing failure, NOT quota or safety. Raw curl to the API works fine.

```bash
source /root/.secrets/kunci-root.env
curl -s "https://api.minimax.io/v1/video_generation" \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MiniMax-Hailuo-2.3",
    "prompt": "your prompt here",
    "duration": 10
  }'
```

## Model naming (critical)

| Guess | Works? |
|---|---|
| `Hailuo-2.3` | ❌ 404 |
| `MiniMax-Hailuo-2.3` | ✅ |
| `MiniMax-H3` | ❌ Not on Token Plan |

H3 model (2K, reference-audio/video/image) is NOT available on Token Plan.

## Supported durations

`MiniMax-Hailuo-2.3`: **6s and10s only**. Other durations return `invalid params`.

## Quota

- Daily: 3 videos/day
- Weekly:21/week
- Separate from general model quota
- Exhausted = `Token Plan usage limit reached` (status_code 2056)
- Check: `mmx quota show` → `model_name: "video"` entry

## H3-only flags (useless on Token Plan)

These require `--model MiniMax-H3` which returns 404 on Token Plan:
- `--reference-image`, `--reference-video`, `--reference-audio`
- `--duration`, `--ratio`

Working without H3:
```bash
mmx video generate --prompt "..." --download /tmp/out.mp4           # T2V
mmx video generate --prompt "..." --image start.jpg --download /tmp/out.mp4  # I2V
```

## ffmpeg cinematic fallback

When AI video quota is exhausted, create motion video from image + voiceover:

```bash
ffmpeg -y \
  -loop 1 -i /path/to/image.jpg \
  -i /path/to/voiceover.mp3 \
  -filter_complex "
    [0:v]scale=1200:2134,
    crop=720:1280:'480*t/DURATION':'(854-640)*t/DURATION',
    vignette=PI/4,
    format=yuv420p[v]
  " \
  -map "[v]" -map "1:a" \
  -c:v libx264 -preset ultrafast -crf 23 \
  -c:a aac -b:a 128k \
  -shortest \
  -movflags +faststart \
  /tmp/output.mp4
```

Replace `DURATION` with audio length in seconds. Creates Ken Burns zoom-pan + vignette.

**Performance pitfall:** `zoompan` filter on1024x1024→1080x1920 times out (>120s). Use `crop` animation instead — renders in seconds.
