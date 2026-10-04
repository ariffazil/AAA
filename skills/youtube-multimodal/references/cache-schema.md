# Canonical Cache Schema (fetch_router.py)

Cache path: `/root/.cache/youtube-content/<video_id>.json`

Written by `youtube-content` skill's `fetch_router.py` after a successful
acquisition (any stage S1..S8). Both skills (`youtube-content` and
`youtube-eureka`) read from this same cache — single source of truth.

## Why this exists

`fetch_router.py` returns a nested JSON shape, NOT a flat segments list.
A naive `data["segments"]` returns 0 — there is no top-level `segments` key.
The trap bit during skill synthesis: a fresh S0 cache hit reports
`stage=S0, ok=True, source=cache:transcriptapi.com` but the consumer code
asserted `len(data["segments"]) > 0` and thought the cache was empty.

**Always use `data["transcript"]["segments"]`** (or `transcript.segment_count`)
for transcript access.

## Top-level fields

| Field | Type | Source | Use |
|---|---|---|---|
| `video_id` | str | 11-char YouTube ID | Identity |
| `url` | str | Normalized watch URL | Identity |
| `source` | str | e.g. `transcriptapi.com`, `youtube-transcript-api` | Provenance |
| `stage` | str | `S0`..`S8` | Which cascade step succeeded |
| `transcript` | object | Nested transcript bundle (see below) | **Read here** |
| `metadata` | object | Video-level metadata (see below) | Title, channel, language |
| `cascade_history` | list | Per-stage attempts `{stage, ok, error}` | Diagnostics |
| `fetched_at` | str | ISO-8601 UTC | Freshness check |
| `sha256` | str | Full-payload hash (sha256 of canonical JSON) | Tamper seal |

## `transcript` object

| Field | Type | Use |
|---|---|---|
| `segments` | list of `{text, start, duration}` | **Primary consumer input** |
| `segment_count` | int | Quick cardinality check (prefer over `len(segments)`) |
| `duration` | str `"MM:SS"` or `"H:MM:SS"` | Total video duration |
| `full_text` | str | Plain concat of all segment texts |
| `timestamped_text` | str | `[MM:SS] text\n[MM:SS] text\n...` — human-readable |

## `metadata` object

| Field | Type | Use |
|---|---|---|
| `title` | str | Video title |
| `channel` | str | Channel name |
| `channel_url` | str | Canonical channel URL |
| `thumbnail_url` | str | Maxres or hqdefault thumbnail |
| `language` | str | Transcript language (e.g. `en`, `asr-hi`, `id`) |

## Real example — verified live 2026-08-08

`/root/.cache/youtube-content/lpLReXGD2Kg.json` after a TranscriptAPI S8 hit:

```json
{
  "video_id": "lpLReXGD2Kg",
  "url": "https://youtu.be/lpLReXGD2Kg",
  "source": "transcriptapi.com",
  "stage": "S8",
  "transcript": {
    "segment_count": 400,
    "duration": "21:56",
    "full_text": "वार्म अप हर सेट में नहीं होता है एक सेट में वार्म अप हो जाता है ...",
    "timestamped_text": "[0:00] [♪♪♪] ...\n[0:18] वार्म अप हर सेट में ...",
    "segments": [
      {"text": "वार्म अप हर सेट में नहीं होता है, एक सेट", "start": 0.0, "duration": 4.319},
      {"text": "में वार्म अप हो जाता है। यह करते हैं,", "start": 1.7, "duration": 5.0},
      {"text": "रोइंग, रोइंग मूवमेंट करना है। पूरा जैसे", "start": 4.3, "duration": 4.2}
    ]
  },
  "metadata": {
    "title": "SECRET BEFORE STAGE",
    "channel": "Siddhant Jaiswal",
    "channel_url": "https://www.youtube.com/@...",
    "thumbnail_url": "https://i.ytimg.com/vi/lpLReXGD2Kg/hqdefault.jpg",
    "language": "asr-hi"
  },
  "cascade_history": [
    {"stage": "S8", "ok": true, "error": null}
  ],
  "fetched_at": "2026-08-07T22:17:46.808165+00:00",
  "sha256": "8b29905321bd9a79d0c32f44bc4ec8b9ff425150c91cf4e2c443554f3fcb89fe"
}
```

## Correct consumer pattern

```python
import json
d = json.load(open("/root/.cache/youtube-content/<vid>.json"))

# WRONG — always empty
segs = d["segments"]              # KeyError or []

# RIGHT
segs = d["transcript"]["segments"]
count = d["transcript"]["segment_count"]
title = d["metadata"]["title"]
lang = d["metadata"]["language"]
provenance = f"{d['source']} (stage {d['stage']}, {d['fetched_at'][:10]})"
```

## Dual-shape compatibility (legacy `eureka.py` writes)

Older `eureka.py` (pre-2026-08-08) wrote a flat shape:
`{video_id, source_method, language, title, channel, segments: [...], saved_at}`.

Newer writers (post-this-session) should emit the canonical nested shape above.
Consumers should detect & handle both:

```python
if "transcript" in cached and isinstance(cached["transcript"], dict):
    segs = cached["transcript"]["segments"]   # canonical
else:
    segs = cached["segments"]                 # legacy fallback
```

## Verification pattern

```bash
# Does the cache file exist and is it parseable?
python3 -c "
import json, sys
d = json.load(open('/root/.cache/youtube-content/<vid>.json'))
t = d.get('transcript', {})
print(f\"stage={d.get('stage')}  source={d.get('source')}  segs={t.get('segment_count')}  lang={d.get('metadata',{}).get('language')}\")
"

# List all cached videos
python3 /usr/local/lib/hermes-agent/profiles/aaa-hermes/skills/media/youtube-content/scripts/cache.py list

# Clear one
python3 .../cache.py clear --video-id <vid>
```

## Operational notes

- Cache is append-only by convention; never edit entries in place.
- `fetched_at` is when fetch_router wrote it; same value re-appears on S0 hits
  (cache is read, not refreshed). To force refresh: pass `--no-cache` to the router.
- If two writers race (e.g. cron + interactive), last-write-wins; the sha256
  seal catches tampering, not races.
- Cache file size grows linearly with segment count (a 22-min video with
  400 segments ≈ 120 KB JSON).