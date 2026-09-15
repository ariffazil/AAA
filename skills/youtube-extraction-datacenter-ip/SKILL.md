---
name: youtube-extraction-datacenter-ip
description: Use when YouTube extraction fails from a datacenter IP.
---

# YouTube Extraction From a Datacenter IP

Covers: "Sign in to confirm you're not a bot", bot-check, PO token, yt-dlp blocked on VPS/cloud/proxy IP.

## First: identify which failure you have

Two different failures look similar. Test BOTH before changing flags:

```bash
yt-dlp -F "https://www.youtube.com/watch?v=ID" 2>&1 | tail -3
curl -s -m 25 -X POST "https://www.youtube.com/youtubei/v1/player?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8" \
  -H "Content-Type: application/json" \
  -d '{"videoId":"ID","context":{"client":{"clientName":"WEB","clientVersion":"2.20260701.00.00"}}}' \
  | python3 -c "import json,sys;d=json.load(sys.stdin);print(d['playabilityStatus']['status'], list(d.get('streamingData',{}).keys()))"
```

- `playabilityStatus.status == "LOGIN_REQUIRED"` + empty `streamingData` → **IP-level flag**. Stop tuning yt-dlp.
- `OK` + formats present but downloads 403 → **GVS PO-token gap**. That is what bgutil fixes.

**IP-flag signature (verified KVM4, 2026-09):** every `player_client` (`tv`, `mweb`, `web_safari`, `ios`, `android`, `android_vr`, `web_embedded`, `web_creator`, `tv_simply`, `tv_embedded`, `web`) returns the same bot check. The raw watch page HTML also carries `playabilityStatus: LOGIN_REQUIRED` with no `captionTracks` and no `streamingData`.

## Rule: on an IP flag, no local tool helps

PO tokens, `--remote-components ejs:npm`/ejs:github, deno/node, `--extractor-args youtube:player_client=…`, `getpot`, `yt-dlp-getpot-wpc`, `pytubefix use_po_token`, `youtube-po-token-generator` **all still fail**. The player request is rejected before a token is consulted. Do not spend time here.

## Solution ladder (ranked)

1. **Firecrawl** — key + MCP tool already wired in the federation.
   ```bash
   curl -s -X POST "https://api.firecrawl.dev/v2/scrape" \
     -H "Authorization: Bearer $FIRECRAWL_API_KEY" -H "Content-Type: application/json" \
     -d '{"url":"https://www.youtube.com/watch?v=ID","formats":["markdown"]}'
   ```
   `formats:["markdown"]` = 1 credit, returns metadata block + full transcript.
   `formats:["audio"]` = 5 credits, returns a signed GCS MP3 URL (valid 1 h) → download → Groq whisper-large-v3.
   Note `metadata.postprocessorsUsed: ["youtube"]` confirms native handling.
2. **SerpApi** — `engine=youtube_video_transcript`, 250 free/mo. Returns `transcript[{start_ms,end_ms,snippet}]` + `chapters` + `available_transcripts`. Sturdier than parsing raw captions.
3. **yt-dlp for discovery only** — browse/search endpoints are NOT bot-checked even on a flagged IP:
   ```bash
   yt-dlp --flat-playlist --print "%(id)s|%(title)s" "https://www.youtube.com/@handle/videos"
   yt-dlp --flat-playlist --print "%(id)s|%(title)s" "ytsearch5:query"
   ```
   Chain the IDs into lane 1. This is the cheap-at-scale pattern.
4. **Residential proxy** — `--proxy "http://user:pass@host:port"`, IPRoyal PAYG $7/GB → $5.25/GB @10 GB. Sticky per-video; rotate between videos, never mid-download (GVS URLs are IP-bound → 403).
5. **Burner-account cookies** — last resort; account ban is real. Export from an incognito window that visits `youtube.com/robots.txt` in the same tab, then close it. Ship `cookies.txt` (Netscape) — `--cookies-from-browser` is impossible headless.

## Audio → text pipeline

```bash
ffmpeg -v error -y -i in.mp3 -ar 16000 -ac 1 -b:a 32k out.mp3   # Groq caps uploads at 25 MB
curl -s https://api.groq.com/openai/v1/audio/transcriptions -H "Authorization: Bearer $GROQ_API_KEY" \
  -F "file=@out.mp3" -F "model=whisper-large-v3" -F "response_format=verbose_json"
```

## Dead lanes — do not re-litigate

- **Invidious public instances**: all 5 on the official list returned 403/401/502/530 on `/api/v1/videos` and `/api/v1/captions` (checked 2026-09). Needs `invidious-companion` + own rotating proxy.
- **Piped**: 3 of 4 public APIs down; the live one returned `subtitles: []` and `audioStreams: 0`.
- **Legacy `video.google.com/timedtext`**: HTTP 200 but empty body.
- **Jina Reader on YouTube**: returns page chrome, not the transcript.
- **`youtube-transcript-api`**: IP-blocked.

## Keep bgutil installed anyway

It does nothing for an IP flag, but the moment you have a clean IP (proxy or cookie session) GVS 403s appear and bgutil is what fixes them:
```bash
docker run --name bgutil-provider -d --init -p 127.0.0.1:4416:4416 brainicism/bgutil-ytdlp-pot-provider:latest
mkdir -p ~/.config/yt-dlp/plugins && curl -sL -o /tmp/b.zip \
  https://github.com/Brainicism/bgutil-ytdlp-pot-provider/releases/latest/download/bgutil-ytdlp-pot-provider.zip
python3 -c "import zipfile;zipfile.ZipFile('/tmp/b.zip').extractall('/root/.config/yt-dlp/plugins/bgutil-ytdlp-pot-provider')"
yt-dlp -v --simulate URL 2>&1 | grep pot   # expect: bgutil:http-X (external)
```

## Economics

1 Firecrawl credit ≈ 1 transcript; Standard plan $83/mo = 100k credits. Cache transcripts — they never change once published.
