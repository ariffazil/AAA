---
name: media-content-extraction
description: "Extract IG/YouTube content and generate images."
version: 1.0.0
author: 333-AGI
capability_tier: fed-multimodal-vision
ecology_state: WARM
---

# Media Content Extraction

## When to use
User shares IG reel link, YouTube video link, or requests an image/poster.

## Instagram Reels

```bash
timeout 60 yt-dlp --no-warnings -o "/root/.hermes/workspace/ig_reel.%(ext)s" "https://www.instagram.com/reel/REEL_ID/"
```

- Works WITHOUT cookies from cloud IPs (yt-dlp 2026-08-19+)
- Extract frames: ffmpeg -v quiet -i ig_reel.mp4 -vf fps=1 -frames:v 8 /tmp/ig_frames/f_%02d.jpg -y
- Metadata: yt-dlp --skip-download --print uploader|title|description|duration URL

**Pitfall:** If yt-dlp returns 429, try --cookies-from-browser chrome.
**Pitfall:** Extract at 2fps for reels >15s. Text overlays need multiple frames.

## YouTube Transcripts

```bash
uv pip install youtube-transcript-api 2>/dev/null
uv run python /root/.hermes/skills/media/youtube-content/scripts/fetch_transcript.py URL --text-only
```

**Pitfall:** YouTube BLOCKS cloud IPs. Fallback: web_extract for title only, web_search for summaries. NEVER fabricate content.

## Image Generation (Pollinations API)

Free, no auth. Use for posters, concept art, not real photos.

```python
import requests, urllib.parse
encoded = urllib.parse.quote("descriptive prompt here")
url = f"https://image.pollinations.ai/prompt/{encoded}?width=1920&height=1080&model=flux&nologo=true"
resp = requests.get(url, timeout=120, stream=True)
```

**Pitfall:** AI-generated = NOT real photos. Always caveat.
**Pitfall:** First attempt sometimes 500. Retry once after 5s.
**Pitfall:** NSFW rejected. Verify output with vision_analyze before sending.

## Always-on rules
- Verify all content with vision_analyze before sending
- YouTube transcripts: check extraction success before answering
- Fallback chain: tool fails → search reviews → caveat honestly
- Vision analyze intermittent; use subagent delegation as backup
- IG metadata + frame analysis sufficient even without full transcript

## Reference
- see references/pollinations-patterns.md for API quirks