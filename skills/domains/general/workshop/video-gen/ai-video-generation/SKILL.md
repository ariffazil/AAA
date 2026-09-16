---
name: ai-video-generation
description: "Use when generating or verifying AI video of a person."
version: 1.0.0
tags: [minimax, mmx, video, image-to-video, verification, ai-generated-media]
metadata:
  hermes:
    category: creative
    requires: [mmx-cli]
    related: [mmx-h3-video, video-prompt-engineering, photorealistic-human-image-gen]
---

# AI Video Generation — Still-First, Verified, Honestly Labelled

Class-level procedure for producing a generated video clip of a subject (reel, mood piece, scene) and for the companion question of putting the user himself in the frame. Tools: the `mmx` CLI — MiniMax image model for the frame, Hailuo/H3 for motion — plus `ffmpeg` and `vision_analyze` for proof.

For H3-specific API detail (region recovery, reference modes, core limits) use the `mmx-h3-video` skill; this skill owns the end-to-end workflow including the paths H3 cannot serve. For directing the still frame itself, see `photorealistic-human-image-gen`.

---

## 1. Still first, motion second

A clip is one verified base frame plus one motion. Text-to-video surrenders all control of the subject — for a person it is not an option.

```bash
# base frame — subject, pose, props, lighting, lens, film grain, natural body proportions
mmx image generate --prompt "<photography prompt>" --aspect-ratio 9:16 --seed <n> --out /root/.hermes/workspace/<name>.jpg

# animate the frame (default model — reachable on standard plans)
mmx video generate --prompt "<one camera move + one subject motion>" \
  --image /root/.hermes/workspace/<name>.jpg --download /root/.hermes/workspace/<name>.mp4
```

- Read the base frame with `vision_analyze` before spending on video: count people, ask for anatomy errors, melted objects, garbled text. Re-seed and regenerate rather than animating a frame you have not looked at.
- Direct the frame with photographer language (camera body + focal length + aperture, lighting direction and colour temperature, culturally specific props, spatial description of pose). Generic prompts return digital art.
- On H3-capable keys add `--model MiniMax-H3 --duration <4-15> --ratio <ratio>`.
- **Direction without H3: supply both ends of the move.** A single `--image` only says where
the clip starts. Generate a second still as the intended *end state* and pass it as
`--last-frame` with no `--model`, and the CLI switches to the two-frame interpolation lane —
the two frames carry the continuity that the unavailable `--duration`/`--ratio` flags would
otherwise have given you. Reach for this whenever the request names where the motion should
*arrive* (a push-in that lands on a body region, a turn that ends on a held gaze), not just
where it begins.
- **Read the `[Model: ...]` line the CLI prints on success** (`[Model: MiniMax-Hailuo-02]`,
`[Model: MiniMax-Hailuo-2.3]`) and report that. The legacy output geometry follows the source
frame and the tier (observed 1364x768 @ 24fps, ~6s) — confirm with `ffprobe` rather than
assuming the lane you asked for.

---

## 2. Model and flag fallbacks — never abandon the request

| Symptom | Move |
|---|---|
| Error `2013` / Token-Plan refusal on the H3 series | Fall back to the default `MiniMax-Hailuo-2.3` i2v on the same base frame. The gate is on H3, not on video. |
| `2013` on H3 **and** the move needs an end state | Two-frame interpolation: pass `--image` + `--last-frame`, omit `--model`, let it auto-select Hailuo-02. Costs one extra still and buys back the direction control the H3 flags would have carried. |
| `require --model MiniMax-H3` | `--duration`, `--ratio`, `--reference-image/-video/-audio` are H3-only. Drop the flags, keep the model. |
| Resolution seems wrong for the request | Hailuo output follows the source frame. Read the file with `ffprobe` instead of assuming 2K or 9:16. |
| `unexpected EOF while looking for matching '` | The prompt contains an apostrophe. Build the command with `shlex.quote(prompt)` in Python, not hand-rolled quotes. |
| Clip too short for the idea | Add shots, do not stretch one take. A single beat is enough for 5–6 seconds. |

---

## 3. Verify before delivering (mandatory)

A file that downloaded is not evidence that the intended camera move happened or that the anatomy held.

```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,duration,nb_frames,r_frame_rate -of default=nw=1 <out.mp4>

# filmstrip: first→last across one sheet
ffmpeg -v error -i <out.mp4> -vf 'fps=1,scale=360:-1,tile=4x1' -frames:v 1 /tmp/sheet.jpg -y

# individual frames, evenly spaced
ffmpeg -v error -i <out.mp4> -vf 'fps=4/<clip_seconds>,scale=480:-1' /tmp/f_%02d.jpg -y
```

Then `vision_analyze` the filmstrip — "does the camera move the prompt asked for actually happen across the frames?" — and the final frame alone — "clean anatomy; any melted skin, fused hands, extra limbs, garbled text?".

- Move absent → the prompt stacked too many actions. Cut to one camera move + one subject motion, regenerate.
- Lettering or props melted → regenerate from a cleaner base frame with `no text, no signage` and less background clutter.
- Both checks pass → deliver.

---

## 4. Self-insert without a reference photo

When the user asks for an image or clip with **himself** in it and no reference photo of him exists on the box:

1. Render him as a **back-of-head silhouette in the foreground** — dark, slightly out of focus, back of head and shoulder at the doorway or window edge, the actual subject beyond it, sharp. The viewer stands where he stands.
2. Or ask for one clear face photo and route through an identity-preserving model before generating.

Never invent a face and present it as him, and never let a generated human deliverable go out unlabelled.

The silhouette is usually the stronger composition anyway: the unseen body at the edge is what makes the frame read as a point of view rather than a portrait, so the honest option costs nothing.

---

## 5. Delivery

- Say plainly that the output is AI-generated, not a photograph or recording of a real person.
- Offer concrete variants — slower push, tighter crop, alternate angle, tighter framing on a named body region — rather than asking a vague "how is it?".
- Change one variable per re-generation so the comparison stays meaningful.
