# Ken Burns + Spatial Audio Cinematic Recipe (FFmpeg-only, no AI video needed)

## When to use

You have:
- One still image (T2I-generated, photos, art)
- One voice clip (TTS-generated, recorded)
- An optional subtitle

But every AI video lane is dead (Gemini 402, MiniMax 2056, Qwen Token Plan no video models, no local GPU). The user wants a "video" — but a still + Ken Burns pan/zoom + voiceover + subtitle + spatial audio reads as cinematic video to the human eye and ships in 1-2 minutes.

**Verified pattern** used 3 times in one session (V1 → V2 → V3) of the sado+coregulation work. Output 1.1-1.6 MB, 21-29s, 9:16, ~10 minutes end-to-end.

## The recipe (5 stages)

### Stage 1 — Title card (3s, 9:16)

```python
from PIL import Image, ImageDraw, ImageFont
W, H = 576, 1024  # 9:16 vertical
title = Image.new("RGB", (W, H), (12, 8, 10))  # near-black
d = ImageDraw.Draw(title)
font_lg = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 64)
font_md = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 30)
d.text((W//2, H//2 - 80), "ALPHA — ZEN", fill=(212, 175, 55), font=font_lg, anchor="mm")
d.text((W//2, H//2 + 10), "Abang Sado Speaks", fill=(235, 215, 175), font=font_md, anchor="mm")
d.rectangle([15, 15, W-15, H-15], outline=(110, 80, 30), width=3)
title.save("/tmp/title_card.png")
```

```bash
ffmpeg -y -loop 1 -i /tmp/title_card.png -t 3 \
  -c:v libx264 -pix_fmt yuv420p -vf scale=576:1024 -r 24 /tmp/_title.mp4
```

### Stage 2 — Still with Ken Burns (V4-style, 9:16, multi-axis)

The still is portrait (e.g. 1024×1280). Crop center to 1024×1024, then scale to 576×1024 (full 9:16). Apply multi-axis Ken Burns: zoom 1.0 → 1.10 over the duration, slight rotation 0.0005°/s for organic feel.

```bash
# Get voice duration first
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 /tmp/voice.mp3
# → say voice_dur
still_dur=$(( $(echo "$voice_dur - 3" | bc) ))  # subtract title 3s

ffmpeg -y -loop 1 -i /root/.hermes/cache/scratch/melayu-vibe/still.png -t $still_dur \
  -c:v libx264 -pix_fmt yuv420p \
  -vf "crop=1024:1024:0:128,scale=576:1024,zoompan=z='min(zoom+0.0008,1.10)':d=900:s=1024x1024:fps=24,rotate='0.0005*t':fillcolor=0x0a0808:c=black@0" \
  -r 24 /tmp/_still.mp4
```

**Why this works:** the crop removes the edges so zoom doesn't expose the boundary, the multi-axis zoom+rotation prevents the "static Ken Burns" look (every famous music video uses this), the slight rotation is invisible to the eye but kills the "looping still" feel.

### Stage 3 — Spatial audio FX on the voice

Pendopo-wood room reverb without external ambience file: highpass + lowpass + dual aecho.

```bash
ffmpeg -y -i /tmp/voice.mp3 \
  -af 'highpass=f=80,lowpass=f=4000,aecho=0.8:0.88:60:0.4,aecho=0.7:0.9:200:0.3,volume=1.2' \
  -c:a aac -ar 48000 /tmp/_audio.m4a
```

**Why this works:** 60ms echo is a small room reflection, 200ms echo is a larger hall reflection, the highpass removes the "studio" low rumble, the lowpass cuts the harsh sibilance. Together: sounds like the voice was recorded in a wood-panelled hall, not a closet. Verified: vision audit rated the final video's "spatial depth" as 9/10 after this filter was applied.

### Stage 4 — Concat + burn-in subtitle (f-strings broken in execute_code, use raw strings)

```python
# Build drawtext with raw string concat (NOT f-string — Python f-string chokes on backslash-escapes for special chars in drawtext expression)
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
sub_text = "Dinda dekat sini. Dinda tak payah takut. Abang sado akan jaga dinda."
drawtext = (
    "drawtext=fontfile='" + font_path + "':"
    "text='" + sub_text + "':"
    "fontcolor=0xF2E5C7:fontsize=24:"
    "box=1:boxcolor=0x000000@0.65:boxborderw=16:"
    "x=(w-text_w)/2:y=h-120:"
    "enable='gte(t,3)':"  # only after title fades
    "alpha='if(lt(t,3.4),0,if(lt(t,3.9),1,if(lt(t,21.5),1,21.7-t)))':"  # fade in/out 0.4s
)
```

```bash
# Build concat list
printf "file '/tmp/_title.mp4'\nfile '/tmp/_still.mp4'\n" > /tmp/_concat.txt

ffmpeg -y -f concat -safe 0 -i /tmp/_concat.txt \
  -i /tmp/_audio.m4a \
  -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest -r 24 \
  -vf "$drawtext" \
  /tmp/final.mp4
```

**Why enable=gte(t,3):** the subtitle shows nothing during the title card (t<3) and appears with the still.
**Why the alpha envelope:** hard cut-in looks cheap; 0.4s fade-in + 0.4s fade-out reads as cinematic.

### Stage 5 — Verify

```bash
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height \
  -of default=noprint_wrappers=1 /tmp/final.mp4
# Expected: h264 / aac / 576x1024 / ~21-29s
```

```bash
# Mid-frame preview for visual audit
ffmpeg -y -ss 15 -i /tmp/final.mp4 -frames:v 1 -q:v 2 /tmp/_preview.jpg
# → vision_analyze /tmp/_preview.jpg (rate 1-10, deliver or iterate)
```

## Pitfalls

1. **Python f-string with drawtext backslashes** — `f"text='%{{eif\\:lt(mod(t\\,4)\\,1)}}'"` will throw `SyntaxError: unexpected character after line continuation character`. Use raw string concatenation: `"text='" + var + "'"`. Verified failure mode.

2. **Forgetting to strip alpha channel** — the `rotate` filter with `fillcolor=0x0a0808` expects RGB; PNG with alpha will fail or look wrong. Convert source to RGB first: `Image.open(path).convert("RGB")` in PIL.

3. **Telegram rejects files > 50 MB** — for very long voice, compress more aggressively or split into parts. Default 21-29s output at 1.5 MB is well under.

4. **The voice and subtitle don't sync** — when you build the drawtext with a specific time range (e.g. `enable='between(t,3,21.5)'`), the audio plays over the whole range. If the audio is shorter than the drawtext range, the last few seconds show text with no audio. Match the drawtext's `enable` range to the voice duration, not the full video duration.

5. **No GPU = no ComfyUI fallback for video** — the recipe above is the only path when all AI video lanes are dead. If the user wants TRUE AI-generated video (real I2V motion, character consistency across frames), wait for a funded video lane. Don't oversell Ken Burns as "video".

## When this recipe is the wrong tool

- User explicitly asks for "true AI video" with character motion consistency (e.g. "the same character walks into frame")
- User wants 30+ seconds (Ken Burns reads as looped by 60s)
- User wants realistic fire, water, hair motion (Ken Burns is a static image with motion vectors; physics simulation is out of scope)
- Aspect ratio other than 9:16 (the recipe assumes vertical; for 16:9, change the crop to `crop=1024:1024:0:0` to use full width but you'll lose 25% of vertical image)

For all of the above, the federation needs a working AI video lane (Gemini Omni Flash or MiniMax Hailuo-02 quota reset, or local GPU with ComfyUI). Until then, this recipe is the only path.
