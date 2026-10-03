---
name: media-link-ingest
description: "Use when a shared link's media must be fetched and read."
version: 1.0.0
owner: AAA
category: media
tags: [media, ingestion, yt-dlp, instagram, youtube, ffmpeg, vision, telegram]
floor_scope: [F2, F4, F9]
autonomy_tier: T1
capability_tier: fed-long-context
ecology_state: WARM
---

# Media Link Ingest

When a user shares a **link** instead of a file, nothing lands on disk and the gateway has nothing to route — the agent must fetch it. When inbound media is **blocked**, the agent must say so rather than describe what it cannot see.

This skill exists because both failure modes were hit repeatedly: declaring "I cannot access Instagram" before trying, and narrating an image that never arrived.

Sibling: `generated-media-delivery` owns the **outbound** lane — artefacts you synthesise and send
(renders, posters, plates). This skill is only about media coming *in*.

## Rule 0 — probe first, and prefer the MCP entry point (2026-09-16)

**Call `media_ingest_url` (media-ingest MCP, `127.0.0.1:18411`) before hand-rolling
`yt-dlp`.** It walks the whole lane ladder, writes artifacts to
`/root/forge_work/media_ingest/<date>/<kind>-<hash>/` (media file + frames +
`artifact.md`), and returns a `truth_state` you can relay honestly:

| truth_state | meaning | what to tell the human |
|---|---|---|
| `OBSERVED` | a lane returned real content | report the content |
| `PARTIAL` | only page text/metadata | say the media itself was NOT read |
| `BLOCKED` | every lane failed | relay `blocking_reason` verbatim; do not summarise |

`media_lane_doctor` probes every lane live — run it before declaring any media
capability dead. Never answer "I cannot access <platform>" without it.

## Rule 0b — the lane ladder, in order (cheapest first)

1. **YouTube transcript → SerpApi** `engine=youtube_video_transcript`. LIVE and
   unaffected by IP reputation because it runs on SerpApi's side. Free plan =
   250 searches/month (check `serpapi.com/account` — `total_searches_left`).
   `engine=youtube_video` gives metadata (title, channel, views, description).
2. **yt-dlp metadata probe** — tells you the truth about this IP for this platform.
3. **yt-dlp media download → Groq whisper-large-v3** (`stt.provider=groq`, configured
   in `~/.hermes/config.yaml`). Fast, Malay-capable, no local GPU needed.
4. **ffmpeg frame sampling → vision** — the visual half of short-form video.
5. **Firecrawl → r.jina.ai free tier** — page text as the last resort.

## Step 1 — Instagram Reels / posts (validated, no cookies)

Works from this cloud IP **without cookies** — but only for genuinely public reels.
A non-existent or deleted shortcode returns `Instagram sent an empty media response`,
which is a **dead-link signal, not an IP block**. Confirm the post exists in a
browser before concluding the lane is down.

```bash
yt-dlp --no-warnings -o "/root/.hermes/workspace/ig.%(ext)s" "https://www.instagram.com/reel/<ID>/"
```

Download **video** (not `bestaudio`) for social reels — frames are half the payload,
and an audio-only download silently produces zero frames.

## Step 0 — check disk first

Uploaded *files* are already local. Check the hinted path before touching the network:

- `/root/.hermes/cache/videos/*.mp4`
- `/root/.hermes/cache/images/*.jpg`
- `/root/.hermes/audio_cache/*.ogg`

If the inbound message says the media was **rejected as high risk**, jump to "Blocked inbound media" below — there is nothing on disk to read.

## Step 1 — Instagram Reels / posts (validated, no cookies)

```bash
yt-dlp --no-warnings -o "/root/.hermes/workspace/ig.%(ext)s" "https://www.instagram.com/reel/<ID>/"
```

Metadata only — often the fastest route to the meaning, because a talking-head reel's caption IS the punchline:

```bash
yt-dlp --no-warnings --skip-download \
  --print "%(uploader)s|%(title)s|%(description)s|%(duration)s|%(like_count)s" "<URL>"
```

Works from a cloud IP without cookies. If a shared short link 404s, retry the canonical `https://www.instagram.com/reel/<ID>/` form.

## Step 2 — frames + audio

```bash
ffmpeg -v quiet -i in.mp4 -vf "fps=1" out_%02d.jpg -y    # sample the WHOLE clip
ffmpeg -v quiet -i in.mp4 -vn -acodec libmp3lame -q:a 4 out.mp3 -y
```

Then read the **first, a middle, and the LAST frame** — not frame 1 alone.

**Pitfall — the hook is not the message.** Short-form video runs hook → body → punchline, and the visual register usually changes at the end (meme cut, product card, joke, credit). A clip that opens on an interview question can end on a Call-of-Duty meme with a joke caption; reporting the opening frame as the content produces a confidently wrong summary the user will have to correct. `fps=1` across the whole timeline is cheap — do it.

## Step 3 — YouTube

**Primary lane: `media_ingest_url` / SerpApi transcript** (see Rule 0b). The peer-review
finding stands: `web_extract` and `youtube-transcript-api` are both IP-blocked from a
datacenter IP (`RequestBlocked` / `IPBlocked`), so treat them as one lane failing, not
the task failing.

**yt-dlp caveats on this host (verified 2026-09-16):**

- JS-challenge (`n`-sig) failures — `Requested format is not available` — are fixed by
  `--remote-components ejs:npm` in `~/.config/yt-dlp/config`. **If yt-dlp works in your
  shell but not under systemd, the cause is a missing `HOME=/root`** in the unit file:
  yt-dlp looks for its config under `$HOME/.config/yt-dlp/`. Add it before debugging anything else.
- Video download from this IP still hits `Sign in to confirm you're not a bot`.
  Captions come from SerpApi, so the transcript lane is unaffected; only raw media bytes need cookies.
- TikTok is hard-blocked from this IP (`Your IP address is blocked from accessing this post`).
  Do not burn turns re-trying it; route TikTok through a cookie/proxy lane or say so.

**Pitfall — the helper's own invocation.** Plain `uv run python <helper>` aborts with `youtube-transcript-api not installed` even after `uv pip install` (the script runs in an ephemeral env). Use `--with`: `uv run --with youtube-transcript-api python <helper> "<URL>"`. A dependency error is not an IP block — do not read it as "this video has no transcript".

## Step 4 — when the vision lane is out of balance

If the primary vision lane returns 402 (balance) or 429 (quota), do not report the image unreadable. The dead lane is the **session's** vision tool, not the network — dispatch the frame paths to a bounded subagent, whose own session reaches the endpoints directly, and require **two models to agree** before reporting anatomy, injury, or identity detail:

- `inclusionai/ling-3.0-flash-vl:free`
- `nex-agi/nex-n2.5-pro:free`

Two-model agreement is the bar for any claim about a person's body or identity. One model is a read, not a witness.

## Blocked inbound media ("rejected because it was considered high risk")

When the inbound media arrives as a rejection notice, **the pixels never reached the model**. There is no transcript and nothing to analyse.

1. Say so in ONE line — the media was blocked before it reached you.
2. Do **not** narrate what it "probably" shows, and do **not** infer body, mood, or content from the caption the user typed alongside it. A guessed description of blocked media is fabrication.
3. Offer a concrete alternate route: send as a document/file, share a public URL (then ingest per Steps 1-3), or describe it in words.
4. The gate is on the inbound path, not on the vision model — re-sending the same file the same way will be blocked again. "Try again" is not a fix.

## Reporting shape

State which artefacts you actually read (video downloaded? frames? caption? transcript?). Keep OBSERVED (what a frame literally shows) separate from INFERRED (what it means). Never present a partial read as a full one, and never let a third party's caption stand in for content you did not read.
