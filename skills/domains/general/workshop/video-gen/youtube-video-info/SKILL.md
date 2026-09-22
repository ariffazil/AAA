---
id: youtube-video-info
name: youtube-video-info
version: 1.0.0
description: "Fetch YouTube video identity (title, channel, thumbnail) and attempt transcript when the user pastes a YouTube link."
owner: 333-AGI
risk_tier: low
floor_scope: [F2, F4]
autonomy_tier: T1
forged: 2026-08-30
forged_by: "kimi-code/FI-008 (F13 directive: make YouTube work for Hermes ASI)"
trigger_when:
  - "message contains youtu.be/ or youtube.com/watch or youtube.com/shorts"
  - "user asks what a video is, or sends a video link for discussion"
capability_tier: fed-multimodal-vision
ecology_state: WARM
---

# YouTube Video Info — VPS-Safe Lane

## The Reality (read first)

- `yt-dlp` and `youtube-transcript-api` are **bot-blocked from this VPS IP** — do NOT retry them directly; they will burn a turn and fail.
- Browser fetching YouTube works only when the browser tool is healthy; do not depend on it.
- The **oEmbed endpoint is public and always works**: title, channel, thumbnail. That answers "video apa?" every time.

## Procedure (no approval needed — approvals are off)

1. Extract the video URL from the message.
2. Run:

```bash
python3 /root/HERMES/bin/youtube-info.py "<URL>"
```

Returns JSON: `title`, `channel`, `channel_url`, `thumbnail`, `watch_url`, `transcript`.

3. **If transcript.available is true** → summarize from transcript text.
4. **If transcript.available is false (normal on VPS)** → enrich with your web SEARCH tool using the exact title: search `"<title>" <channel>` and summarize what the search snippets + description say.
5. Reply in the user's language (BM santai with Arif). Lead with title + channel, then the summary. If content is gym/training related, link it to the user's training context naturally.

## Never Do

- Never ask the user to approve anything for this flow — it is read-only metadata.
- Never claim you "watched" the video. You read metadata and (when available) transcript/search context. Say so honestly if depth is limited.
