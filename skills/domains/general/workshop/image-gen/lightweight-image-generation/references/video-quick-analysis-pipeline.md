# Video Quick-Analysis Pipeline

**Captured:** 2026-08-29 (Mr. Enrich On The Go event recording, SADO group)

Use this when user drops a short video (under ~2 min) and asks "what do you
see" or wants quick visual + audio breakdown. The deliverable is
**understanding what's in the video**, not a polished edit.

## Pipeline (3-4 terminal calls, sequential)

### Step 1: Probe metadata + extract

```bash
ffprobe -v quiet -print_format json -show_format -show_streams /path/to/video.mp4 \
  | head -60

# Frames every 2 seconds (good for short clips, fast)
mkdir -p /tmp/video_frames
ffmpeg -i /path/to/video.mp4 -vf "fps=1/2" -y /tmp/video_frames/frame_%02d.jpg 2>&1 | tail -3

# Audio (mono 16kHz WAV — fastest for whisper)
ffmpeg -i /path/to/video.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 \
       -y /tmp/video_audio.wav 2>&1 | tail -3
```

Key metadata to capture: duration, dimensions, framerate, audio codec,
audio sample rate. Useful for "is this portrait?" / "how long?" / "is it
worth transcribing?" decisions.

### Step 2: Vision-analyze key frames (not all)

Don't analyze every frame. Pick frames at **evenly distributed timepoints**
plus any frame where something visibly changes. For 11s clip, 6 frames at
2s intervals is plenty. For 60s clip, 8-10 frames.

```bash
# vision_analyze per frame — describe what's there
vision_analyze(image_url="/tmp/video_frames/frame_01.jpg",
               question="Describe what's in this frame: who, what, where, text?")
```

### Step 3: STT — prefer faster-whisper over openai-whisper CLI

**Pitfall**: `openai-whisper` CLI hangs 5+ minutes on model load (downloads
fresh each invocation in some configs). Use **faster-whisper** Python:

```python
python3 -c "
from faster_whisper import WhisperModel
model = WhisperModel('tiny', device='cpu', compute_type='int8')
segments, info = model.transcribe('/tmp/video_audio.wav', language='en', beam_size=1)
print(f'Detected: {info.language} (prob {info.language_probability:.2f})')
for seg in segments:
    print(f'[{seg.start:.1f}-{seg.end:.1f}] {seg.text.strip()}')
"
```

For Malay, set `language='ms'` or omit language to auto-detect.

### Step 4: Synthesize report

Combine frame descriptions + STT transcript into structured chat reply:

```
**Visual:**
- Bullet list of what's in each distinct frame

**Audio:**
- Transcript of dialogue/cues

**Round/context diagnosis** (if applicable):
- What event/category this is
- Athletes/people involved (without ID — describe, don't name unless source)
```

## Why this works (vs polling frame-by-frame or running full STT first)

- Frames at 2s intervals + vision_analyze is fast enough that you can
  describe a 60s video in 4-5 tool calls instead of 20+
- Audio extracted first = if video has no speech (e.g. just music),
  you can skip STT entirely and save 60+ seconds
- faster-whisper tiny on CPU = ~10s for 11s of audio, near-realtime

## Pitfalls

| Pitfall | Fix |
|---------|-----|
| `openai-whisper` CLI hangs forever on model load | Use faster-whisper Python (above). Tiny model = ~40MB download first time, then cached. |
| Video has no audio stream | Skip STT. vision_analyze frames covers it. |
| Frames look identical (static video) | Drop frame count to 3 (0s, mid, end). Don't waste calls. |
| Video portrait 9:16 (phone recording) | vision_analyze still works — frames are 540x1280 or similar. |
| Audio ambient noise only (no speech) | STT will return empty or single garbled tokens — that's fine, mention "no clear dialogue" in report. |
| User wants FULL detailed analysis (>2 min video) | Skip this pipeline — use full delegate_task or video tools. This pattern is for quick "what's in this clip" reads. |

## Output to user

Don't dump technical details (frame rates, codec names). Speak human:

**BAD:** "ffprobe shows 548x1280 H.264 11.5s, faster-whisper detected 'Play it!'"

**GOOD:** "Ni 11.5 saat vertical phone recording. Visual: 2-3 athletes on
stage, transition between front/rear pose rounds. Audio cuma single cue
'Play it!' — emcee call for next segment. Standard competition flow."

## When NOT to use this

- User wants to **edit** the video (use ffmpeg script + subagent)
- User wants **frame extraction for poster/collage** (separate pattern)
- Video >5 minutes (use delegate_task to subagent for thorough work)
- User asks "summarize this meeting" with 60+ min video (delegate_task)