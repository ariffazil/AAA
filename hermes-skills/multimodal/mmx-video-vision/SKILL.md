---
name: mmx-video-vision
description: Analyze video content using MMX vision for any URL yt-dlp supports
auto_trigger: false
---

# MMX Video Vision Pipeline

Use when: user shares a video URL (YouTube, Facebook, TikTok, Instagram, any yt-dlp-compatible site) and wants content analyzed, summarized, or understood.

## Why this pipeline?

MMX vision (mmx vision describe) only accepts image files, not video. Solution: extract key frames at 1fps using ffmpeg, then analyze them individually.

## Step-by-step

### Step 1 — Extract metadata (no download)
```bash
yt-dlp --no-download --dump-json "<video_url>"
```
Returns: title, uploader, view count, duration, direct video/audio URLs, thumbnail.

### Step 2 — Download video
```bash
yt-dlp -f "<format_id_video>+<format_id_audio>" --merge-output-format mp4 "<url>" -o "output.mp4"
```
Use format IDs from Step 1. Common pattern: video+audio format IDs merged into mp4.

For Facebook share links (/share/v/), yt-dlp automatically follows redirects to the canonical reel URL. No auth needed.

### Step 3 — Extract frames with ffmpeg
```bash
ffmpeg -i input.mp4 -vf "fps=1" -q:v 2 frames_%03d.jpg
```
- fps=1 = 1 frame per second. For 5-min video = ~300 frames.
- For shorter videos (<2 min): fps=2 to get more coverage.
- -q:v 2 = high quality JPEG.

### Step 4 — Analyze frames with MMX vision
Pick 3-5 representative frames:
- Frame 001 = start
- Frame at ~25% duration = early content
- Frame at ~50% = middle
- Frame at ~75% = late content
- Last frame = ending

```bash
mmx vision describe /path/to/frame_001.jpg
mmx vision describe /path/to/frame_xxx.jpg
mmx vision describe /path/to/frame_last.jpg
```

### Step 5 — Combine findings
Synthesize the frame analyses into a coherent summary. Note any text overlays, scenes, people, context.

## Trick: Direct video URL from yt-dlp JSON

From Step 1 output, the url field in any format entry is the direct CDN URL. Can also download that URL directly with curl/wget if yt-dlp fails.

## Pitfalls

1. MMX does not support .mp4 - always extract frames first
2. Facebook /share/v/ links - yt-dlp handles the redirect automatically
3. Very long videos (>10 min) - sample at fps=0.5 instead to keep frame count manageable (max ~300 frames)
4. No audio track in format - yt-dlp downloads video-only + audio-only separately and merges with --merge-output-format mp4
5. DASH formats (manifest_url) - separate video/audio streams; always pick one video + one audio format ID

## Verification

After download:
```bash
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 input.mp4
```

After frame extraction:
```bash
ls frames_*.jpg | wc -l  # should equal duration in seconds (for fps=1)
```
