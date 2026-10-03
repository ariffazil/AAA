---
name: social-video-extract
description: "Use when a user shares a social video link to analyse."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [Media, Video, Instagram, TikTok, yt-dlp]
    related_skills: [youtube-content]
capability_tier: fed-multimodal-vision
ecology_state: WARM
---

# Social Video Extraction (Instagram / TikTok / X)

## When to use

A user sends a Reel / TikTok / X video link and asks what's in it, wants it analysed, or you would otherwise say "I can't open Instagram." **Try this first** — that claim has already been falsified once.

## The rule

`web_extract` and plain fetch are blocked by Instagram and TikTok. **`yt-dlp` works on Instagram Reels without cookies on this host** — verified end-to-end 2026-09-16 (metadata + video download + Groq whisper transcript + 6 frames). Never report a social video as unreachable before attempting yt-dlp.

Prefer the MCP entry point: `media_ingest_url` (media-ingest MCP, `127.0.0.1:18411`) walks the lane ladder for you, writes the media + frames to `/root/forge_work/media_ingest/`, and returns a `truth_state` (`OBSERVED` / `PARTIAL` / `BLOCKED`) plus a `blocking_reason` you can relay verbatim.

Platform reality on this host (2026-09-16):

- **Instagram** — works without cookies for public reels. `empty media response` = dead/private shortcode, NOT an IP block. Download video (not `bestaudio`) or frames come back empty.
- **TikTok** — hard-blocked from this IP (`Your IP address is blocked from accessing this post`). Needs a cookie or proxy lane.
- **YouTube** — captions come from SerpApi (`engine=youtube_video_transcript`, free 250/mo); yt-dlp *video* download hits the bot check. If yt-dlp works in your shell but fails under systemd, the unit is missing `HOME=/root`.

## Procedure

1. **Download**
   ```bash
   yt-dlp -o "/abs/path/out.%(ext)s" "https://www.instagram.com/reel/REEL_ID/"
   ```
   Pass the bare `/reel/<ID>/` URL — Instagram sometimes breaks on the `?stkn=` token.

2. **Pull metadata — the caption is often the payload**
   ```bash
   yt-dlp --no-warnings --skip-download \
     --print "%(uploader)s|%(title)s|%(description)s|%(duration)s|%(like_count)s" "URL"
   ```
   The full description frequently contains the actual message (a video's text overlay is only half the story). Read it before summarising.

3. **Sample frames for vision**
   ```bash
   mkdir -p frames && ffmpeg -v quiet -i out.mp4 -vf "fps=2" frames/f_%03d.jpg -y
   ```
   Then `vision_analyze` 2–3 spread frames (early = hook, middle = body, last = punchline/twist). Videos often change format at the end (meme insert, caption card).

4. **Audio (optional)** if speech matters
   ```bash
   ffmpeg -v quiet -i out.mp4 -vn -acodec libmp3lame -q:a 4 audio.mp3 -y
   ```

## Pitfalls

- Do not conclude from the thumbnail alone — the final frames often carry the twist.
- Do not paraphrase the caption as your own analysis; quote it, then interpret.
- Videos may be 10–20s only — sample densely (fps=2) so you catch format changes.
- If yt-dlp fails, check version (`yt-dlp --version`) before declaring the platform unsupported.
