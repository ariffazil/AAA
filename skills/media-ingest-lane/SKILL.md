---
name: media-ingest-lane
description: "Use when a shared link (YouTube, Instagram, TikTok, X, web) must be read as content. Never say 'I cannot access' before running this."
version: 1.2.0
owner: AAA
category: media
tags: [media, youtube, instagram, tiktok, yt-dlp, firecrawl, whisper, frames, vision, ingest]
floor_scope: [F2, F4, F9]
autonomy_tier: T1
capability_tier: fed-long-context
ecology_state: WARM
---

# Media Ingest Lane — read the link, or say honestly why you couldn't

## Rule 0 — probe, then either read it or state the block

Never answer "I cannot access <platform>" before attempting. A capability declared dead
without an attempt is an F2 failure. Equally: **never narrate content you did not read.**
A blocked lane is a real answer; a fabricated summary is not.

`web_extract` and plain fetch are blocked by Instagram/TikTok — that is a LANE failing,
not the task failing. Probe before you declare.

## The entry point (use this, not hand-rolled yt-dlp)

`media-ingest` MCP — `http://127.0.0.1:18411/mcp`, systemd `mcp-media-ingest`

| tool | use |
|---|---|
| `media_ingest_url(url, text_only=False, vision=True)` | any shared link → content |
| `media_vision_read(images, question="")` | read stills / contact sheet / screenshot / poster |
| `media_ingest_file(path, vision=True)` | media already on disk (voice note, upload) — video gets frames + vision too |
| `media_lane_doctor(deep=False)` | probe every lane live before declaring one dead |

```bash
# CLI fallback if the MCP is unreachable
python3 /root/.hermes/tools/media_ingest/media_ingest.py url "<URL>" [--json] [--text-only] [--no-vision]
python3 /root/.hermes/tools/media_ingest/media_ingest.py doctor --deep   # live-probes media + vision (costs credits)
```

Code: `/root/.hermes/tools/media_ingest/media_ingest.py` · server: `/root/.hermes/mcp/media-ingest/server.py`

Artifacts land in `/root/forge_work/media_ingest/<date>/<kind>-<hash>/`:
`artifact.json` · `artifact.md` · media file · `frames/` · `contact_sheet.jpg` · `frames.json` ·
`visual_read.md` · `transcript_rejected.txt` (when STT junk was refused)

### truth_state + content_read + transcript_state — relay this to the human, always

| state | meaning | what you say |
|---|---|---|
| `OBSERVED` | real content read: a transcript **or** `visual_read` | report the content |
| `PARTIAL` | media obtained but payload **unread** (frames, no transcript, no visual_read), or page text only | say the media itself was NOT read |
| `BLOCKED` | every lane failed | relay `blocking_reason` verbatim; do not summarise |

- `content_read` — which halves were actually read: `media`, `transcript`, `frames`, `visual`, `page`.
  Empty + PARTIAL means nothing of the media was read.
- `transcript_state` — `OK` | `ABSENT` | `SUSPECT_DEGENERATE:<why>`. **Only `OK` is speech.**
  Whisper invents text on music/silence ("you you you you …"); the lane rejects
  degenerate output instead of stamping OBSERVED on it.
- `visual_read` — what a vision model actually SAW in the frames. Frames sitting on disk
  are not a read; if this is empty the pixels were never opened.

## Reading a VIDEO properly (the shape)

1. `media_ingest_url` → fills `media_path`, `frames[]`, `contact_sheet`, and (when there is
   no spoken transcript) `visual_read`.
2. **Read `visual_read` first.** If it is empty but frames exist, call
   `media_vision_read([contact_sheet])` — one image tiles the whole timeline.
3. Zoom only where it matters: `media_vision_read(["frames/<name>.jpg"], question="...")`
   when a number, banner or pose needs a closer read.

If `transcript_state != OK`, there is no usable speech: **read the pixels**, don't
paraphrase silence. If `frames=0` and there is no transcript, the honest answer is BLOCKED.

## The lane ladder (cost-ordered, falls through)

1. **SerpApi transcript** `engine=youtube_video_transcript` — YouTube captions, free tier
   250/mo (check `serpapi.com/account`). Runs on SerpApi's IP, our reputation is irrelevant.
2. **Firecrawl `formats:["video"]`** (~5 credits) — **the YouTube media lane.** One signed
   MP4 with both streams → frames, vision *and* whisper from one call. Also the only lane
   that fills `duration_s`/`published`.
3. **Firecrawl `formats:["audio"]`** (~5 credits) — fallback; flakier
   (`SCRAPE_MEDIA_ACCESS_DENIED` is transient — retried with backoff), no frames.
4. **yt-dlp media** — every non-YouTube platform (IG public reels, X, FB); free. Try it on
   YouTube too before spending credits — the bot check is per-request, not permanent.
5. **Groq `whisper-large-v3`** on extracted audio (mono 16 kHz, chunked ≤22 MB).
6. **ffmpeg frames** — whole-timeline sampling + average-hash de-dup + contact sheet.
7. **VISION** — `zai/glm-4.6v` → `zai/glm-4.5v` → `gemini-2.5-flash` reads the frames into
   `visual_read`. Providers are probed live in `doctor --deep`, not assumed. There is
   deliberately **no qwen rung**: that token-plan account carries no vision model
   (`qwen3-vl-plus`/`qwen-vl-max` → "Model not exist", its listed models reject
   `image_url` content). A rung that can only fail is not a fallback, it is noise.
8. **Firecrawl markdown → r.jina.ai free** — last-resort page text.

## Platform reality on this host (verified 2026-09-16)

| platform | status | note |
|---|---|---|
| YouTube captions | **works** via SerpApi | unaffected by our IP |
| YouTube media | **works** via Firecrawl `["video"]` | yt-dlp is **intermittently** bot-checked — one video passes, the next fails minutes later. Probe the URL; never declare it globally dead |
| Firecrawl audio format | **flaky** | transient denials, retried with backoff; never the primary lane |
| Instagram | **works, no cookies** | public reels only. `empty media response` = dead/private shortcode, **not** an IP block |
| TikTok | **blocked** | `Your IP address is blocked` — needs a cookie/proxy lane |
| X/Twitter | untested | — |

## Hard-won pitfalls

- **Silence is not a transcript.** Measure before you trust STT: a silent audio track reads
  `mean_volume: -91.0 dB` under `ffmpeg -i m.mp4 -af volumedetect -f null -`. Whisper turns
  that into "you", deterministically, on every 25-second window. Check the audio is real and
  reject degenerate output — never promote absence to OBSERVED.
- **Frames on disk are not a read.** An artifact once reported OBSERVED next to 18 frames no
  model had opened. If you did not read `visual_read`, you did not read the video.
- **Sample the whole timeline, not the intro.** A sampler at fps=0.5 with `-frames:v 6` reads
  the first 12 seconds of a 9m32s video. Sample at adaptive fps across full duration, de-dup,
  then tile into one contact sheet.
- **A text lane returning junk is not success** — see the silence rule above.
- **Long audio breaks STT silently.** Groq rejects oversize uploads (`Request Entity Too Large`);
  downsample to mono 16 kHz and chunk first.
- **Download video, not `bestaudio`,** for social reels — frames are half the payload and an
  audio-only download silently yields zero frames.
- **The hook is not the message.** Short-form video runs hook → body → punchline, and the visual
  register usually changes at the end (meme cut, product card, credit). Reading frame 1 alone
  produces a confidently wrong summary.
- **Transient ≠ blocked.** Retry media denials with backoff before reporting failure.
- **Uploaded files are already local** — check disk before touching the network:
  `/root/.hermes/cache/videos/*.mp4`, `cache/images/*.jpg`, `audio_cache/*.ogg`.
- **Blocked inbound media** ("rejected because it was considered high risk"): the pixels never
  reached us. Say so in one line; do NOT infer body/mood/content from the caption the user typed.
  Offer a concrete alternate route (send as document, public URL, or describe it). Re-sending the
  same way will be blocked again — "try again" is not a fix.
- **If the vision lane returns 402/429** (balance/quota), the dead lane is the session's vision
  tool, not the network: dispatch frame paths to a bounded subagent, and require **two models to
  agree** before reporting anatomy, injury or identity. One model is a read, not a witness.
- **The service reads `HOME`/`PATH` from its systemd unit.** A wrapper that works in your shell
  and fails as a service is almost always a missing `HOME=/root` (yt-dlp finds its config there).
- **Never use `find … -delete` as a listing idiom.** A `-type l -delete -print` sweep deleted 17
  tracked symlinks under `/root/AAA/skills`; list with `ls`/`find -print` only.

## Verification receipt (the lane is not "probably" working)

`doctor --deep` must show these green before you claim the capability: `serpapi_transcript`
(segments > 0 + `quota_left`), `firecrawl_video` (real video URL), `vision` (a model read a
probe image), `groq_stt`, `jina_free`. Last verified 2026-09-16: all green —
`vision` = `zai/glm-4.6v read 1 image(s)`, `firecrawl_video` OK in 8.1s.

End-to-end proof (same day, a 9m32s YouTube posedown whose audio track is digital silence):

```
truth_state       OBSERVED
content_read      ['media', 'frames', 'visual']
transcript_state  SUSPECT_DEGENERATE: repetition_loop(100% one token)   <- silence, correctly refused
frames            22/24 kept (dedup), contact_sheet.jpg written
vision            zai/glm-4.6v read 3 image(s), 1142 chars -> visual_read.md
```

Before this lane existed the same video produced an artifact that said `OBSERVED` with a
fabricated "you you you" transcript and zero visual content. If a run returns PARTIAL with
`frames` but no `visual_read`, the vision lane failed — read the per-provider error in
`lanes_tried`, do not paper over it with a paraphrase.

## Vision-lane pitfalls (both hit in one afternoon)

- **Never put base64 stills in `curl` argv.** Three frames exceed `ARG_MAX` → curl dies with
  `OSError [Errno 7] Argument list too long`, which looks exactly like a provider outage.
  Stage the JSON body in a temp file and send `-d @file`.
- **A retry per provider, and an honest error string.** One run lost all rungs at once
  (zai transient, qwen 404, gemini 429) and reported only "empty/short answer (0 chars)".
  The lane now retries with backoff and joins every provider error into `detail`.
- **A low `max_tokens` can make a reasoning vision model return empty content.** Do not
  impose a length floor on a short question — accept any non-empty answer.

## Transcript safety — never report a hallucination as content

Whisper does not fail on music or silence; it **invents text**. A hallucinated transcript
is worse than an empty one because it looks like content and poisons every downstream
reader. Four signals, all enforced in code (`_transcript_looks_hallucinated`):

| signal | catches | measured |
|---|---|---|
| repetition loop (<=3 unique words, >12 words) | `"you you you ..."` on silent audio | 22 words / 1 unique |
| unique-word ratio < 0.2 over >25 words | degenerate loops | real speech ~0.7, hallucination ~0.05 |
| **script mismatch** | Khmer text on a Malay video | 146/198 chars KHMER vs target `ms` |
| boilerplate ratio >= 0.35 | "Thank you / subscribe" filler | — |

**Text-primary on purpose.** An earlier version also triggered on `silence_gaps == 0`
("speech has pauses"). That was WRONG: silencedetect returned 0 gaps on an Instagram reel
containing clear speech, so the gate would have **withheld a valid transcript**. A gate
that destroys real information is worse than the hallucination it prevents. Acoustic
numbers stay in the artifact as *evidence a human can inspect*, never as the trigger.

**The measurement must itself be tested.** The first `silence_gaps` implementation ran
`ffmpeg -v quiet`, which SUPPRESSES the `silence_start` lines it was counting — so it
always returned 0 and reported "continuous audio" for a digitally silent file. A
measurement that cannot fail is not a measurement. Use `volumedetect`
(`mean_volume == max_volume == -91 dB` is true digital silence) and drop `-v quiet` in
anything whose output you intend to parse.

## Vision lane — three failure modes, all seen live

1. **ARG_MAX.** Base64 stills in `argv` blow the ~2 MB limit; curl dies with
   `OSError [Errno 7]` and it *looks* like a provider outage. Send the body via
   `-d @file.json`, never inline.
2. **`reasoning_content`.** Reasoning-capable models (GLM-4.5v verified) put their whole
   answer in `reasoning_content` and leave `content` empty. Reading only `content`
   reports a working provider as dead. Fall back to `reasoning_content`.
3. **Scratchpad leak + repetition.** A live read returned 5.4 KB of "Wait, no, maybe the
   second image..." with the answer buried inside. The prompt already said "a rambling
   reply is a failed read" and the model rambled anyway — **an instruction is not an
   enforcement.** Enforce in code: `strip_scratchpad()` drops scratchpad lines and
   near-duplicate lines, and `frequency_penalty: 0.4` on the request is the real lever
   against the model restating one fact three formats deep.

## The doctor must not be able to lie

`ytdlp_youtube` was probed against a **single** video (`dQw4w9WgXcQ`, the most cached
video on earth) and reported `ok (IP not flagged)` while three real videos failed the bot
check in the same minute. A sample of one that happens to pass is a false green.

**Rule: any health check must probe several samples and report a RATE.** A doctor that
always says OK is worse than no doctor, because it teaches you to distrust the whole lane.

### The outlier trap — worse than a small sample

Measured 2026-09-16 across 7 videos:

| video | result |
|---|---|
| `dQw4w9WgXcQ` (Rick Astley) | **passes 3/3 attempts** |
| `aqz-KE-bpKQ`, `Ks-_Mh1QhMc`, `bmQdyM-BCBc` | bot check |
| `jNQXAC9IVRw` (Me at the zoo), `9bZkp7q19f0` (Gangnam), `kJQP7kiw5Fk` (Despacito) | bot check |

So the YouTube block is **per-video and deterministic, not transient and not time-based** —
and `dQw4w9WgXcQ` is a lone outlier that always works. Probing *it* is worse than probing
nothing: it manufactures a permanent false green on the single most-cached video on earth.

**Vocabulary matters too:** `1/3` is technically true but misleading when the 1 is an
outlier — it reads as "sometimes works". Use a probe set of REPRESENTATIVE videos so the
number means what a user's ordinary link will experience. The doctor now reports
`0/3 — YouTube media BLOCKED from this IP; use firecrawl_video`.

**Keep doctor probes fast.** The first multi-probe version used a 120 s per-probe timeout
and took 6 minutes — a doctor nobody runs. Bot checks and format lookups answer fast, so
`--socket-timeout 15` with a 35 s cap brings it to ~7 s.

## Concurrency — artifact dirs are a shared resource

Running the same link through **two entry points at once** (MCP tool + CLI) makes both
write the same artifact directory. Observed live 2026-09-16: frame counts disagreed
(5 vs 18), and **5 Firecrawl credits burned on a duplicate fetch**. Fixes now in place:

- a **lock** on the artifact directory so a second run waits instead of racing
- a **result cache**: a link already read successfully returns in ~0.08 s with zero
  credits; `--force` re-ingests when you actually want fresh data

**Rule: never fire the same URL through two lanes concurrently.** If you are testing a
lane, stop the other consumer first — or you will pay for it twice and mis-read the
result as a lane bug.

## Multi-writer files — check before you patch

`media_ingest.py` grew 977 → 1683 lines in one night with **two agents editing it
simultaneously**. Both sets of work survived only because each patch was anchored on
distinct text. Before patching a hot file:

```bash
grep -c "<your marker>" file        # is your work still there?
grep -c "<their marker>" file       # is someone else's?
python3 -c "import ast;ast.parse(open('file').read())"   # does it still parse?
```

Take a timestamped backup before every write (this file has ten, all cheap). If you find
code you did not write, **do not revert it** — someone else's fix in a shared file is a
decision, and the honest move is to name it in your report and reconcile.

## Vision ladder + the sovereign rung (measured 2026-09-16)

Order: **zai/glm-4.6v → zai/glm-4.5v → gemini (out of credit) → LOCAL moondream on KVM4.**

This ordering exists because every external rung failed at once on one night: gemini's
prepay was depleted, the qwen token-plan carries **no** VL model, OpenRouter's free VL
models returned 429/503/400, OpenAI's key was invalid, and FED's `vision` alias is a
**text** model that silently returns empty. (Test that claim with two different solid
images: a real vision model names them differently, a text model answers identically or
returns nothing.) **A capability with one provider is a dependency, not a capability.**

### Local rung: real, but it needs handling

`moondream:latest` (1.7 GB) on the inference node, called via Ollama's NATIVE
`/api/generate` — base64 in the `images` array, **no `data:` prefix** (unlike the OpenAI
format the other rungs use).

Three measured behaviours, all encoded in `lane_vision_local`:

1. **Short prompt or nothing.** The multi-clause prompt that makes glm-4.6v produce a
   structured read makes moondream return **empty**. It answers
   `"Describe this image in one sentence."` perfectly in ~1 s. Match prompt length to
   model size; ask the small model one thing at a time.
2. **It degenerates on some frames.** Frame c_001 of a video came back as Tamil-script
   repetition (`சணகர் சணகர் ...`) 3/3 times, while c_007 of the SAME video described the
   scene correctly 3/3 times. So the local rung runs the SAME degeneracy guard as the
   transcript gate (`_vision_output_degenerate`: script mix + repetition ratio), retries
   once on an autocontrast-normalised copy, then **skips the frame with a stated reason**.
3. **It can read on-screen text** — it returned `"...a red door with 'TEGAPTV.COM' text"`,
   independently confirming a watermark spelling another model had got wrong.

Report the local rung in the doctor (`vision_local`), because a lane that is not measured
does not exist for monitoring.

## TikTok — the lane WORKS; some videos are simply gone

**Corrected 2026-09-16 (my own earlier note here was WRONG).** I first concluded "TikTok is
blocked from this IP, do not burn turns" after five lanes failed on one URL. That was a
false negative caused by testing a **dead video**. Corrected measurement:

```
@weeklyshowpodcast/video/7668349403203226911   oEmbed 200   yt-dlp: metadata + formats + download
@natgeo/video/7216180156045724933              oEmbed 400   "Video currently unavailable"
@khaby.lame/video/7137423965982653701          oEmbed 400   same
```

Full pipeline on the live one: `truth_state: OBSERVED`, 221 s video downloaded, **4,044
characters of real transcript** from Groq, 17 frames + contact sheet, vision read 2,473
chars. **TikTok is a working lane.**

### Pre-flight: oEmbed tells you dead-video from blocked-lane

Before spending minutes on a TikTok, ask oEmbed — it is tiny and definitive:

```bash
curl -sS "https://www.tiktok.com/oembed?url=<URL>" -o /tmp/o.json -w "HTTP=%{http_code}\n"
# 200 -> live, proceed with yt-dlp
# 400 -> the POST is unavailable (deleted / region-locked). Say so; do not blame the lane.
```

`yt-dlp`'s error for both cases is the misleading `Your IP address is blocked from
accessing this post` — it says *IP* even when the video is simply gone. **Never trust that
message as a diagnosis; confirm with oEmbed.**

### The format trap (cost 2 attempts)

TikTok exposes **combined** streams with non-standard ids (`h264_720p_936123-1`), so a
`bv*+ba` selector fails with `Requested format is not available` while `-f best` succeeds
in the same minute. Use a ladder that reaches a single combined stream:
`bv*[height<=720]+ba/b[height<=720]/b[ext=mp4]/b`.

### Lanes that genuinely do not work for TikTok

Firecrawl refuses the domain outright (`we do not support this site`), and the public
mirrors/oEmbed-alternates tried were down. Those are real; the *platform* is not blocked.

## Relationship to other skills

| This skill | Other skills |
|---|---|
| Inbound media (link → text / frames / visual read) | `generated-media-delivery` — outbound artifacts |
| YouTube lane detail + datacenter-IP failure map | `youtube-extraction-datacenter-ip` |
| Post-extract analysis | `AAA-video-emd-pipeline`, `social-video-intelligence` |
| Cheaper context | `mcp-context-compression` |
