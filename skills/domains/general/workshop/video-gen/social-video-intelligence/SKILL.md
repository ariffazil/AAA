---
name: social-video-intelligence
description: "Multi-platform social video content access and analysis"
created: 2026-07-13
tags: [media, tiktok, youtube, instagram, social-media, video-analysis, browser]
---

# Social Video Intelligence

> **Platform-agnostic video access and analysis.**
> YouTube blocked → try TikTok → try Instagram. This skill documents the fallback chain.

## When to load

- User shares a YouTube URL and `youtube-content` pipeline fails due to bot detection/auth
- User wants to watch/analyze video content from social media platforms
- User asks about bodybuilding, fitness, or physique content on TikTok
- You need to find and analyze video content the user mentions watching
- User sends a video FILE / Telegram attachment (already on disk) and wants to know what's in it or whether it's real

## Layer 0 — Local video file / attachment forensics

When the video is already on disk (Telegram attachment, user-uploaded file), skip platform access and go straight to local forensics:

1. `ffprobe` — duration, codecs, resolution, whether an audio stream exists.
2. `ffmpeg` — extract audio (`-vn -ac 1 -ar 16000`) plus 4–6 frames at spread timestamps (`-ss 0.5 / 2 / 4 / 6 / 7.5 ...`).
3. STT the audio: Groq `whisper-large-v3-turbo` (GROQ_BASE_URL/GROQ_API_KEY from `/root/.secrets/kunci-mas.env`) or local faster-whisper. **faster-whisper CUDA init fails on this VPS ("CUDA driver version is insufficient for CUDA runtime version") — fall back to `device='cpu', compute_type='int8'`; that is the working retry path.**
- **Whisper hallucination pitfall:** on music-only / speechless audio, Whisper (local AND Groq) fabricates full-span boilerplate like "Terima kasih kerana menonton!" / "Thanks for watching!". That output is a NO-SPEECH signal, not a transcript. Cross-check with per-second RMS energy (ffmpeg → f32le PCM → numpy per-second rms) and a second engine/language pass; if both return full-duration closing phrases, report "BGM only, no speech" — never quote the hallucination as spoken content.
- **Multi-attachment batch (4+ videos in one Telegram message):** ffprobe-first triage — ~25% of Telegram uploads may have incomplete `moov atom`. Process only valid files. For tiny on-screen numbers (competitor stickers, captions, watermarks) unreadable in raw 548px-wide phone footage, use a crop-zoom pattern.
4. `vision_analyze` each extracted frame for content: people, poses, on-screen text, watermarks, phone-UI chrome.

### AI image-to-video detection tells (animated still, not real footage)

- Status-bar clock jumps non-monotonically across frames (e.g. 9:20 → 9:22 → 9:24 → back to 9:21 within seconds) — the model animates screenshot chrome it found in the source image.
- Mouth moves "talking" but the audio track contains no speech (music/BGM only).
- Photographer/studio watermark on a "video" — provenance is a still photo.
- Subtle identity morphing between frames (hair colour/face drift) while pose stays frozen.

Combine 2+ tells before claiming AI-generated to the user; state the tells plainly (the clock jump is the most persuasive single piece of evidence).

## The Fallback Chain

```
YouTube ──► blocked? ──► Firecrawl MCP (transcript) ──► TikTok ──► blocked? ──► Instagram ──► Web search
```

### Layer 1: YouTube (via youtube-content skill)
Use `youtube-content` skill scripts first. If `yt-dlp` returns "Sign in to confirm you're not a bot", try:
- `--js-runtimes node:/usr/bin/node` (yt-dlp 2026+ needs a JS runtime)
- `yt-dlp --extractor-args "youtube:player_client=android"` (sometimes bypasses)
- Cookie file at `/root/.secrets/yt-cookies.txt` (if user has exported one)
- Invidious/Piped instances (most are now blocked — don't rely on them)

**Layer 1.5 — Firecrawl MCP (reliable YouTube transcript from cloud IPs):**
When yt-dlp and youtube-transcript-api both fail (cloud IP blocked), Firecrawl MCP returns the full YouTube page as markdown including the complete auto-generated transcript. This is the **most reliable path from this VPS**.

```python
# Via MCP tool call
tool_call: mcp__firecrawl__firecrawl_scrape
arguments:
  url: "https://www.youtube.com/watch?v=VIDEO_ID"
  formats: ["markdown", "summary"]
  onlyMainContent: true
  waitFor: 5000

# Parse result: JSON string → result.markdown contains chapters + full transcript
# Transcript is under "## Transcript" heading — continuous auto-generated captions
# Chapters are in the description section with timestamps (00:00:00 format)
# Scale: 2h48m video → ~200K chars of markdown
```

**Pitfalls:**
- Transcript is auto-generated: search with variant spellings (e.g., "BPC57" for "BPC-157", "thyulin" for "thymulin")
- No speaker labels — use context clues
- `waitFor: 5000` required (YouTube is JS-heavy SPA)
- Result JSON is double-encoded: `json.loads(raw)['result']` → then `json.loads(that)['markdown']`

If all fail, proceed to Layer 2.

### Layer 2: TikTok (browser + API)

TikTok's web player often works without login. Two approaches:

**Approach A — Find video IDs via tikwm.com API (fastest):**

```bash
curl -s "https://www.tikwm.com/api/user/posts?unique_id=USERNAME&count=30" \
  -H "User-Agent: Mozilla/5.0" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if data.get('code') == 0:
    for v in data['data']['videos']:
        print(f\"ID: {v['video_id']} | {v['title'][:100]}\")
"
```

Build the URL as `https://www.tiktok.com/@USERNAME/video/VIDEO_ID`.

**Approach B — Web search for the video:**

```bash
web_search(query="tiktok @abamsadoseksi Nazri Pulong photoshoot part 2 video")
```

Look for the TikTok URL in search results. The tikwm API is more reliable for discovering all of a user's videos.

**Playing and analyzing:**

1. `browser_navigate(url)` to the TikTok video
2. Click the video area to play (find the video ref via `browser_snapshot` — usually the "Watch in full screen" region, ref varies per page load)
3. Wait with `terminal("sleep N")` to let the video advance to the desired timestamp
4. Capture frames with `browser_vision(question="Describe everything visible")`
5. Repeat to catch different moments

**Known limitations:**
- TikTok serves a puzzle-slider CAPTCHA on repeated/profile page requests — navigate directly to a video URL to bypass, or close the dialog (`ref=e3`) and retry
- No transcript extraction available
- Video playback is real-time only — can't scrub programmatically
- Video refs change on every page load — always `browser_snapshot` first

### Layer 2.5: Facebook Pages (login-free probe via Googlebot UA)

Facebook PAGES (not profiles) serve full HTML with embedded JSON to the Googlebot UA — no cookies, no login wall. Most reliable way from the VPS to check "is this page LIVE right now" and enumerate recent videos.

```bash
UA='Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
curl -s "https://www.facebook.com/<PAGE>/videos" -H "User-Agent: $UA" > /tmp/fb.html   # ~1MB
grep -o 'is_live_for_comet_live_ring[^,]*' /tmp/fb.html | head -1                      # live status
grep -oE 'facebook.com/<PAGE>/videos/[A-Za-z0-9_.-]+' /tmp/fb.html | sort -u | head    # recent videos
```

- **Live check:** `is_live_for_comet_live_ring":true` = broadcasting right now (present on both `/live` and `/videos`; false even when finished-live VODs exist).
- **Ordering:** `publish_time` unix epochs in the same JSON.
- **Post captions:** fetch the post URL with the same UA, read `property="og:description"`.
- Fails: mbasic → HTTP 400; normal browser UA → login wall; Firecrawl → refuses facebook.com entirely; Instagram profiles → HTTP 429 from VPS IP (use SearXNG snippets for IG).

Full recipe + Mr Enrich OnTheGo 2026 worked example (broadcaster map, YT handle 404 quirk, 2019 live precedent URL) is documented in the body above.

### Layer 3: Instagram (limited)

Instagram profile fetches from the VPS IP get HTTP 429 — don't burn retries on direct curls; use SearXNG snippets (`instagram.com <handle> <topic>`) to read captions instead. Reels may work without login but often degrade to a sign-up wall. Try:
- Direct Reel URL via browser
- `web_extract` on the URL (rarely works — TikTok is the reliable fallback)

### Layer 4: Web search fallback

When all platforms are blocked:
```bash
web_search(query="topic video site:tiktok.com OR site:instagram.com/reel OR site:x.com")
```

## Known Malaysian bodybuilding accounts (Arif context)

| Platform | Account | Content |
|----------|---------|---------|
| YouTube | `arena cergazz` | Mr Selangor, Mr Malaysia, backstage, posing (426 videos) |
| Facebook | `tegaptv` | TegapTV — official MY bodybuilding broadcaster; FB LIVE finals (2019 precedent) |
| Instagram | `tegaptvmalaysia` | TegapTV IG (92K) — per-category winner/result posts ("Tahniah ... juara 1 kategori ...") |
| Facebook | `onthegoofficialmy` | OnTheGo (Mr Enrich title sponsor) — event recaps, athlete lineups |
| TikTok | `abamsadoseksi` | Nazri Pulong photoshoots, abang sado, tegaptv |
| TikTok | Search `#abamsado` | Broader abang sado content |
| TikTok | Search `#tegaptv` | Malaysian physique competition coverage |

## Known failure modes


| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| yt-dlp "Sign in to confirm" | Cloud IP blocked | Use Firecrawl MCP (Layer 1.5) — most reliable from VPS |
| yt-dlp "No JS runtime" | Missing node/deno | `--js-runtimes node:/usr/bin/node` |
| TikTok blank page/slider CAPTCHA | Rate limited | Navigate to specific video, not profile |
| Instagram login wall | Platform policy | Try TikTok or web search instead |
