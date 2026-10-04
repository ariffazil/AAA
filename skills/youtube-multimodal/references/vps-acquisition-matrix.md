# VPS Acquisition Test Matrix (2026-08-08)

Environment: Hostinger VPS, IP 72.62.71.199 (AS47583), Kuala Lumpur, MY.
Video under test: `lpLReXGD2Kg` ("SECRET BEFORE STAGE", Siddhant Jaiswal, ~22 min).
Second sanity video: `dQw4w9WgXcQ` (Rick Astley) — also succeeded via TranscriptAPI (61 segs, en).

## Tested paths — verbatim results

| Path | Result |
|---|---|
| youtube-transcript-api direct | `RequestBlocked` — cloud provider IP |
| youtube-transcript-api + `proxies={}` (none set) | `RequestBlocked` |
| yt-dlp direct | "Sign in to confirm you're not a bot" |
| yt-dlp `player_clients=[ios,android,web_safari,tv]` | Same bot wall |
| curl_cffi impersonate=chrome120 → watch page | HTTP 200, 1.2 MB, but `logged_out=true`, `captionTracks: []` |
| YouTube timedtext API direct | HTTP 200, 0 bytes |
| youtubetranscript.com | "YouTube is currently blocking us from fetching subtitles" |
| transcriptapi.com v2 (no key) | 401 Invalid API key — endpoint live |
| **transcriptapi.com v2 (key + User-Agent)** | **HTTP 200, 44,977 B, 400 segments, 21:56, lang=asr-hi** |
| supadata.ai (no key) | 401 Missing API Key |
| jina r.jina.ai reader | 402 InsufficientBalance (account, not block) |
| Composio v2 `/api/v2/actions/.../execute` | 410 Gone — endpoint retired |
| Composio v3 `/api/v3/tools/execute` | Reachable; list_captions = manifest-only semantics |

## TranscriptAPI.com response shape (verified)

```json
{
  "video_id": "lpLReXGD2Kg",
  "language": "asr-hi",
  "transcript": [{"text": "...", "start": 0.0, "duration": 4.319}, {"text": "...", "start": 1311.28, "duration": 4.8}],
  "metadata": {
    "title": "SECRET BEFORE STAGE",
    "author_name": "Siddhant Jaiswal",
    "author_url": "https://www.youtube.com/@...",
    "thumbnail_url": "https://i.ytimg.com/vi/lpLReXGD2Kg/hqdefault.jpg"
  }
}
```

## Error taxonomy (from ZeroPointRepo/youtube-skills, verified live)

| Code | Meaning | Action |
|---|---|---|
| 401 | Bad API key | Check/re-setup key |
| 402 | No credits | Top up at transcriptapi.com/billing |
| 403 / 1010 | Cloudflare block | Add/fix `User-Agent` header |
| 404 | No transcript | Video likely has captions disabled |
| 408 | Timeout | Retry once after 2s |
| 429 | Rate limited | Wait and retry |

## Auth flow (agent-assisted signup)

- `POST https://transcriptapi.com/api/auth/register-cli` `{"email": "..."}` → response contains `access_token` + email
- Then OTP verify exchange → API key (`sk_...`)
- Disposable emails rejected by server.
- Key persistence: Hermes secret store / `TRANSCRIPT_API_KEY` env; on this box it lives in `/root/.secrets/kunci-mas.env` (mode 600).

## Other repos reviewed

- **JCodesMore/youtube-for-ai-agents** (Apache-2.0) — Node MCP plugin built on `youtubei.js` (InnerTube internal API, anonymous, no key). Clean cookie-validation pattern in `src/lib/cookies.ts` (required cookie names, graceful anonymous→personalized fallback) and error taxonomy in `src/lib/transcript.ts` (disabled / unavailable / language / Too many). InnerTube is unofficial — can break anytime; consider only if hosted APIs fail.
- **ZeroPointRepo/youtube-skills** (MIT) — 12 skill aliases over one TranscriptAPI endpoint; the pattern to copy (User-Agent requirement, error table, free-tier crediting).
- **neuron-core/youtube-ai-agent** — PHP demo (Neuron framework) using Supadata; not transferable.

## Key operational facts

- `User-Agent` header required on EVERY TranscriptAPI request — bare default UA gets Cloudflare 1010.
- 1 credit per successful request; errors are free; free tier = 100 credits/mo, 300 req/min.
- Router implementation: `fetch_router.py` (S0→S8→S1→S2→S4→S5→S6→S7) + `cache.py` in the youtube-content skill dir; cache root `/root/.cache/youtube-content/`.
