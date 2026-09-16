---
name: youtube-extraction-datacenter-ip
description: Use when YouTube extraction fails from a datacenter IP.
---

# YouTube Extraction From a Datacenter IP

Covers: "Sign in to confirm you're not a bot", bot-check, PO token, yt-dlp blocked on VPS/cloud/proxy IP.

**Do not hand-roll this.** The composed lane lives in the `media-ingest` MCP
(`media_ingest_url`, systemd `mcp-media-ingest`, code `/root/.hermes/tools/media_ingest/media_ingest.py`),
which already walks the ladder below and returns an honest `truth_state` + `content_read`
+ `transcript_state`. Use it; fall back to the raw commands here only when debugging it.

## First: identify which failure you have — and whether it is even permanent

**The bot check is per-request, not a permanent IP stain.** Verified 2026-09-16 on one host:
yt-dlp answered fine for one video ID at 01:39 while the same host was refused
("Sign in to confirm you're not a bot") for another ID at 01:24. So:

1. Re-probe the *specific* URL before declaring the IP flagged (`yt-dlp --simulate <URL>` twice).
2. Only when it fails repeatedly, run the two-failure test below.

```bash
yt-dlp -F "https://www.youtube.com/watch?v=ID" 2>&1 | tail -3
curl -s -m 25 -X POST "https://www.youtube.com/youtubei/v1/player?key=«redacted:AIza…»" \
  -H "Content-Type: application/json" \
  -d '{"videoId":"ID","context":{"client":{"clientName":"WEB","clientVersion":"2.20260701.00.00"}}}' \
  | python3 -c "import json,sys;d=json.load(sys.stdin);print(d['playabilityStatus']['status'], list(d.get('streamingData',{}).keys()))"
```

- `playabilityStatus.status == "LOGIN_REQUIRED"` + empty `streamingData` → **request-level flag**. Stop tuning yt-dlp; take the Firecrawl lane.
- `OK` + formats present but downloads 403 → **GVS PO-token gap**. That is what bgutil fixes.

**Flag signature (verified KVM4, 2026-09):** when it does flag, every `player_client`
(`tv`, `mweb`, `web_safari`, `ios`, `android`, `android_vr`, `web_embedded`, `web_creator`,
`tv_simply`, `tv_embedded`, `web`) returns the same bot check, and the raw watch page HTML
carries `playabilityStatus: LOGIN_REQUIRED` with no `captionTracks` and no `streamingData`.

## Rule: once a request IS flagged, no local tool helps

PO tokens, `--remote-components ejs:npm`/ejs:github, deno/node, `--extractor-args youtube:player_client=…`,
`getpot`, `yt-dlp-getpot-wpc`, `pytubefix use_po_token`, `youtube-po-token-generator`
**all still fail** for that request. The player request is rejected before a token is consulted.
Do not spend time here — switch lane, or retry later (it is transient).

## Solution ladder (ranked)

1. **Firecrawl media — the working lane (2026-09-16).**
   ```bash
   curl -s -X POST "https://api.firecrawl.dev/v2/scrape" \
     -H "Authorization: Bearer $FIRECRAWL_API_KEY" -H "Content-Type: application/json" \
     -d '{"url":"https://www.youtube.com/watch?v=ID","formats":["video"]}'
   ```
   - `formats:["video"]` (~5 credits) → signed GCS **MP4 with both streams** (verified on a
     9m32s video: 69 MB, `duration=PT9M32S` in metadata). One call gives you frames *and*
     audio for whisper. **This is the primary lane** — audio-only can never produce frames.
   - `formats:["audio"]` (~5 credits) → signed MP3; works but is **flaky**:
     `SCRAPE_MEDIA_ACCESS_DENIED` "media host temporarily blocked this request. This is
     transient". Retry with backoff (the composed lane does 3 attempts); never report a
     single transient denial as BLOCKED.
   - `formats:["markdown"]` (1 credit) → metadata block + transcript when captions exist.
   - Firecrawl fetches from its own IPs, so the datacenter check never applies. Its
     `metadata` also supplies `duration`/`uploadDate` that SerpApi's youtube_video engine
     returns as null.
2. **SerpApi** — `engine=youtube_video_transcript`, 250 free/mo. Returns
   `transcript[{start_ms,end_ms,snippet}]` + `chapters` + `available_transcripts`.
3. **yt-dlp for discovery only** — browse/search endpoints are NOT bot-checked even on a
   flagged IP:
   ```bash
   yt-dlp --flat-playlist --print "%(id)s|%(title)s" "https://www.youtube.com/@handle/videos"
   yt-dlp --flat-playlist --print "%(id)s|%(title)s" "ytsearch5:query"
   ```
4. **Residential proxy** — `--proxy "http://user:pass@host:port"`, IPRoyal PAYG $7/GB → $5.25/GB
   @10 GB. Sticky per-video; rotate between videos, never mid-download (GVS URLs are IP-bound → 403).
5. **Burner-account cookies** — last resort; account ban is real. Export from an incognito
   window that visits `youtube.com/robots.txt` in the same tab, then close it. Ship
   `cookies.txt` (Netscape) — `--cookies-from-browser` is impossible headless.
   (`/root/.secrets/yt-cookies.txt` exists on this host and was NOT sufficient on its own.)

## Turning the video into intelligence (frames → vision)

For a visual video (posedown, demo, reel) the pixels are half the payload or more, and
**there may be no speech at all** — a silent audio track is not a licence to report nothing.

```bash
# whole-timeline sampling: fps ≈ target/duration, then de-dup near-identical frames
ffmpeg -v quiet -i media.mp4 -vf "fps=24/DURATION,scale=640:-2" -frames:v 40 -q:v 4 frames/c_%03d.jpg -y
# contact sheet = ONE image a vision model can read in a single call
```
`contact_sheet.jpg` + `frames/` + `visual_read` are produced automatically by the composed
lane. Read order: `visual_read` first (already written), then `media_vision_read([sheet])`
if it is empty, then crop a single frame for a closer read:

```
media_vision_read(images=["/…/contact_sheet.jpg"], question="quote every banner text verbatim")
```

Vision ladder (probed live by `doctor --deep`, never assumed): `zai/glm-4.6v` →
`zai/glm-4.5v` → `qwen/qwen3-vl-plus` → `gemini-2.5-flash`. Gemini/DashScope may be out of
credit; zai is the live rung.

**Vision-lane pitfalls (learned the hard way, 2026-09-16):**

- **Never put base64 stills in `curl` argv.** Three frames exceed `ARG_MAX` and curl dies
  with `OSError [Errno 7] Argument list too long`, which reads like a provider outage.
  Write the JSON body to a file and send `-d @file` (the composed lane now does).
- **A vision model that names a person is wrong.** The governed prompt demands verbatim
  text and forbids naming/placing; keep that shape or you will get confident fabrication.
- Verify with the frame count, not the byte count: a video can download 69 MB and still be
  unread if nothing opened the stills.

## Audio → text pipeline

```bash
ffmpeg -v error -y -i in.mp3 -ar 16000 -ac 1 -b:a 32k out.mp3   # Groq caps uploads at 25 MB
curl -s https://api.groq.com/openai/v1/audio/transcriptions -H "Authorization: Bearer $GROQ_API_KEY" \
  -F "file=@out.mp3" -F "model=whisper-large-v3" -F "response_format=verbose_json"
```

**Guard the output — measure the audio first.** Whisper hallucinates speech on music and
on digital silence; the classic is a repetition loop ("you you you you …"), which is a *long*
string of one token, not a short one. A 9m32s posedown produced 87 chars of it, and the
same "you" on every 25-second window sampled.

```bash
ffmpeg -hide_banner -i media.mp4 -af volumedetect -f null - 2>&1 | grep -E "mean_volume|max_volume"
# a silent track reads: mean_volume: -91.0 dB / max_volume: -91.0 dB  -> there IS no speech
```
Do not run STT to find out what silence says. If the track is silent (or the transcript is
degenerate — one token ≥40% of tokens, <20% unique tokens, or <15 words across >2 min),
report `SUSPECT_DEGENERATE`/no-speech and read the PIXELS instead.

## Dead lanes — do not re-litigate

- **Invidious public instances**: all 5 on the official list returned 403/401/502/530 on
  `/api/v1/videos` and `/api/v1/captions` (checked 2026-09; re-checked 2026-09-16 — same).
- **Piped**: public APIs mostly down; the live one returns
  `SignInConfirmNotBotException` (it is on the same kind of IP).
- **Legacy `video.google.com/timedtext`**: HTTP 200 but empty body.
- **Jina Reader on YouTube**: returns page chrome, not the transcript.
- **`youtube-transcript-api`**: IP-blocked.
- Thumbnails (`https://i.ytimg.com/vi/ID/maxresdefault.jpg`) are NOT blocked and are a cheap
  last-ditch visual — but a thumbnail is one frame, never a content read.

## Keep bgutil installed anyway

It does nothing for a flagged request, but the moment you have a clean IP (proxy or cookie
session) GVS 403s appear and bgutil is what fixes them:
```bash
docker run --name bgutil-provider -d --init -p 127.0.0.1:4416:4416 brainicism/bgutil-ytdlp-pot-provider:latest
mkdir -p ~/.config/yt-dlp/plugins && curl -sL -o /tmp/b.zip \
  https://github.com/Brainicism/bgutil-ytdlp-pot-provider/releases/latest/download/bgutil-ytdlp-pot-provider.zip
python3 -c "import zipfile;zipfile.ZipFile('/tmp/b.zip').extractall('/root/.config/yt-dlp/plugins/bgutil-ytdlp-pot-provider')"
yt-dlp -v --simulate URL 2>&1 | grep pot   # expect: bgutil:http-X (external)
```

## Economics

1 Firecrawl credit ≈ 1 transcript; video/audio formats ≈ 5 credits per call. Standard plan
$83/mo = 100k credits. Cache transcripts — they never change once published. Use
`media_ingest_url(text_only=True)` when you only need captions/page text and no frames.
