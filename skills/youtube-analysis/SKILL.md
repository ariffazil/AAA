---
name: youtube-analysis
description: "Deep visual analysis of YouTube videos when transcript is unavailable (music-only or non-spoken content). Covers preview-thumb frame extraction, oEmbed plus Wayback CDX metadata recovery, no-captions pivot, poster-vs-content mismatch, and multi-frame vision analysis for physique, exercise, and scene identification."
tags: [youtube, vision, frames, analysis, fallback, video, DEPRECATED]
related_skills:
  - youtube-multimodal  # UNIFIED entry point (replaces manual routing)
  - youtube-content   # primary acquisition router (cascade S0-S8)
  - youtube-eureka    # 11-part digest contract (uses transcript)
triggers:
  - User asks for video analysis but youtube-content router returns empty transcript
  - User shares a YouTube link where video is music-only or non-verbal (gym reel, music video, ASMR)
  - User asks for "deep analysis" or "frame analysis" on a YouTube URL
  - Transcript cascade (S0-S8) returns all-fail with "No transcript available"
  - User asks to "feel" or "describe" the visual content of a video
version: 1.1.0
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# YouTube Deep Visual Analysis

When transcript or caption extraction fails (music-only, montage, non-spoken content), the bundled `youtube-content` router reaches end-of-cascade. This skill covers the **pivot path**: visual analysis via preview thumbnails, metadata recovery, and multi-frame vision inspection.

**Complements** the bundled `youtube-content` skill (handles S0-S8 transcript cascade). This skill picks up where S8 ends with "No transcript available."

---

## 1. The No-Captions Pivot

When the transcript router returns `{ok:false}` with stage S8 or S2 reporting "No transcript available" or "No caption track":

1. Diagnose. This means the video has no ASR or human captions, NOT quota or auth failure. Gym reels, music videos, and montages commonly have zero transcript tracks.
2. Do not retry transcript stages. The video has no spoken content; no retry changes the truth.
3. Extract preview thumbnails (Section 2) and proceed to visual analysis (Section 4).

### S8 diagnosis shortcut

- S8 "No transcript available" => no caption track, pivot to frames
- S8 "HTTP 404" => video ID invalid or removed
- S8 "HTTP 408 timeout" => transient, retry once
- S8 "unexpected response" => API schema changed, check payload

---

## 2. Preview Thumbnail Frame Extraction

YouTube auto-generates preview frames at 25%, 50%, 75% of video duration. These are NOT the custom thumbnail; they are actual video frames.

**All frames are free and never bot-walled** (served from `i.ytimg.com`, separate CDN from YouTube main).

### Frame URLs

```bash
# YouTube preview frames (actual video content at ~25%, 50%, 75% marks)
curl -sf "https://i.ytimg.com/vi/{VIDEO_ID}/hq1.jpg" -o frame_25pct.jpg
curl -sf "https://i.ytimg.com/vi/{VIDEO_ID}/hq2.jpg" -o frame_50pct.jpg
curl -sf "https://i.ytimg.com/vi/{VIDEO_ID}/hq3.jpg" -o frame_75pct.jpg

# Resolution variants (higher quality, same content)
curl -sf "https://i.ytimg.com/vi/{VIDEO_ID}/maxresdefault.jpg" -o hero.jpg
curl -sf "https://i.ytimg.com/vi/{VIDEO_ID}/sddefault.jpg" -o hero_sd.jpg
```

### Resolution and size comparison

- `hq1.jpg`, `hq2.jpg`, `hq3.jpg` (11-15 KB, medium quality): actual video frames at 25%, 50%, 75%
- `maxresdefault.jpg` (140-180 KB, high quality): custom thumbnail, may differ from video
- `sddefault.jpg` (40-55 KB, medium quality): resized custom thumbnail
- `default.jpg` (3-4 KB, low quality): YouTube default thumbnail

### Verification: are frames from the actual video?

A quick `ls -la *.jpg` confirms files downloaded. Then:

- hq1/hq2/hq3 = real video frames (different poses, angles, scenes)
- maxresdefault = poster or thumbnail (often a posed shot, may not appear in actual video)
- hq1 equal to maxresdefault in size = the video reuses the thumbnail as one of its frames (low-effort edit)

---

## 3. Metadata Recovery (when yt-dlp is bot-walled)

Even when yt-dlp fails with "Sign in to confirm you're not a bot", rich metadata is still recoverable.

### Method 1: YouTube oEmbed (always works, instant)

```bash
curl -sf "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={VIDEO_ID}&format=json"
```

Returns: `title`, `author_name`, `author_url`, `thumbnail_url`. Limited fields but never blocked.

### Method 2: Wayback CDX API (historical metadata)

```bash
# Step 1: Check if archived
curl -sf "https://web.archive.org/cdx/search/cdx?url=youtube.com/watch?v={VIDEO_ID}&output=json&limit=20&filter=statuscode:200"

# Step 2: Get the timestamp of latest snapshot
curl -sf "https://archive.org/wayback/available?url=youtube.com/watch?v={VIDEO_ID}"

# Step 3: Fetch archived page (raw, not parsed)
curl -sfL "https://web.archive.org/web/{TIMESTAMP}id_/https://www.youtube.com/watch?v={VIDEO_ID}" -o archived.html

# Step 4: Extract metadata from archived HTML
grep -oE '"lengthSeconds":"[0-9]+"' archived.html
grep -oE '"viewCount":"[0-9]+"' archived.html
grep -oE '"uploadDate":"[^"]+"' archived.html
grep -oE '"keywords":\[[^]]+\]' archived.html
grep -oE '"shortDescription":"[^"]{20,2000}"' archived.html
```

Key fields: duration, view count (at archive time), upload date, tags, full description.

### Method 3: Wayback Machine raw (with decompression)

Wayback serves `id_/` URLs as gzip-compressed. If you see binary output:

```bash
curl -sfL "https://web.archive.org/web/{TIMESTAMP}id_/https://youtube.com/watch?v={VID}" | gunzip > page.html 2>/dev/null || curl -sfL "https://web.archive.org/web/{TIMESTAMP}https://youtube.com/watch?v={VID}" > page.html
```

---

## 4. Multi-Frame Visual Analysis

After extracting hq1, hq2, hq3, plus maxresdefault, run `vision_analyze` on each frame independently.

### Analysis template per frame

For each frame, extract:

- Exercise or Action: what is the person doing? (lateral raise, lat pulldown, posing, etc.)
- Muscle group focus: primary mover plus secondary stabilizers
- Physique: conditioning estimate (BF%), muscle separation, symmetry, vascularity
- Pose type: mandatory pose, mid-rep, casual, or editorial
- Equipment: barbells, dumbbells, machines, cables, identify specific type
- Setting: gym type, lighting, background elements
- Watermark or OCR: channel branding, text overlays

### Exercise identification rules

- Arms extended laterally with motion blur = lateral raise (delt focus)
- Seated with arms overhead on machine handles = shoulder press (delt plus tricep)
- Seated with overhead bar and cable = lat pulldown (lat focus)
- Standing with bar on chest and back arched = squat or clean
- Arms or back shot with lats visible = posing or lat spread

### Physique classification framework

- Body fat: ab visibility, serratus, vascularity. Range 8% (stage) to 15% (fit) to 20% (normal).
- Conditioning: striations (chest, shoulder), dryness. Contest-ready vs off-season vs recreational.
- Symmetry: left-right balance, proportional development. Even vs lagging body part.
- Vascularity: vein prominence on arms, shoulders, chest. Minimal (off-season) to pronounced (stage-ready).
- Fullness: muscle belly roundness vs flatness. Pumped vs flat vs depleted.

---

## 5. Poster-vs-Content Mismatch Pitfall

The thumbnail (maxresdefault) may not represent actual video content. Common patterns:

| Poster shows | Video actually shows | Why |
|--------------|---------------------|-----|
| Shirtless posing shot | Full-clothes workout | Promotional poster is not content |
| One athlete alone | Multiple athletes in gym | Thumbnail crops to single person |
| Competition-stage photo | Gym training footage | Poster from competition, video is training |
| Dramatic lighting | Flat gym fluorescents | Poster is studio-quality, video is handheld |

**Rule**: always analyze hq1, hq2, hq3 (actual video frames) before characterizing content. Never infer video content from thumbnail alone. The thumbnail is a marketing asset, not a content sample.

### Worked example (this skill's origin session)

The poster for `EVjOukIg_bQ` shows Syed Khairuddin shirtless in a low-rise-jeans editorial pose against a weathered wall, a fitness-model poster. The actual video frames (hq1-hq3) show him in a yellow tank top performing dumbbell lateral raises, machine shoulder press, and lat pulldowns, a gym workout session. A first-pass analysis based only on the thumbnail would have incorrectly called this a posing video.

---

## 6. Identity Verification Pitfall (namesakes)

When video content features someone with the same name or surname as a person in memory, **do not conflate without evidence**.

Probe before claiming identity:

1. Does the video subject's physique and age match the person in memory?
2. Does the video timestamp align with the person's known timeline?
3. Does the location match?
4. Is there any direct identifier (IC, full name confirmation, photo match)?

In this skill's origin session: video features Syed Khairuddin Morktarudin at D'Popeye Gym (2020). Memory has a Syed Khairuddin (2026, SADO group, sambal business). Same first name plus same gym brand equals possible but not confirmed. Always state the match probability honestly (30-50%) rather than asserting identity.

---

## 7. Sibling-Report Verification (when analyzing YouTube)

When a sibling or friend agent has produced a report on the same video, verify before trusting:

- `kappa_r=0.96, tri_witness=0.97` with no frame extraction run = fabricated self-report metrics
- "visual frame telemetry" claimed but no `hq1`, `hq2`, `hq3` files on disk = prose without evidence
- Timeline with specific timestamps when transcript is empty = predicted, not observed
- "mandatory bodybuilding poses" when poster shows casual editorial = thumbnail assumption, not video observation
- Same `@VID v6.0 Epoch33Ω` template as another report = nested echo, not independent analysis

**Rule**: a witness that didn't probe isn't a witness. Count actual frames analyzed and actual tools run, not self-reported confidence scores.

---

## 8. Complete recovery recipe (when transcript fails)

```bash
VIDEO_ID="<extract from URL>"

# 1. Metadata (works even when bot-walled)
curl -sf "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=${VIDEO_ID}&format=json" | python3 -m json.tool

# 2. Preview frames (always free, no auth)
mkdir -p /tmp/yt_frames
for i in 1 2 3; do
  curl -sf "https://i.ytimg.com/vi/${VIDEO_ID}/hq${i}.jpg" -o "/tmp/yt_frames/hq${i}.jpg"
done
curl -sf "https://i.ytimg.com/vi/${VIDEO_ID}/maxresdefault.jpg" -o "/tmp/yt_frames/poster.jpg"

# 3. Verify files exist and differ
ls -la /tmp/yt_frames/

# 4. Vision analysis on each frame
# Run vision_analyze on hq1.jpg, hq2.jpg, hq3.jpg independently
# Then vision_analyze on poster.jpg to compare poster vs content

# 5. Report: poster vs actual content, physique assessment, exercise ID, timestamp estimates
```

---

## 9. YouTube video categories where transcript fails

- Gym/bodybuilding reels: no transcript (music-only). Use preview frames and exercise identification.
- Music videos or lyric videos: no transcript. Use frames for visual narrative, oEmbed for song info.
- Cooking ASMR: no transcript. Use frames for recipe steps, OCR for text.
- Nature or landscape drone: no transcript. Use frames for location identification.
- Short-form vlog with speech: usually has transcript. Use youtube-content S0-S8 first.
- Long-form documentary: usually has transcript. Use youtube-content S0-S8 first.
- Podcast clip: usually has transcript. Use youtube-content S0-S8 first.

**Default assumption**: if youtube-content S8 says "No transcript available," the video is non-verbal. Pivot immediately to frame analysis rather than retrying transcript stages.

---

## Related skills

- `youtube-content` (bundled): S0-S8 transcript cascade. Use first; if it returns empty, pivot to this skill.
- `verify-nested-sibling-reports`: when multiple agents report on the same video, verify each before trusting.
- `frontier-model-audit-verification`: when a frontier model (Claude, Gemini) produces a YouTube analysis, treat as self-report requiring reproduction.