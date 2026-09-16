# Video Lane Selection, Flag Gating & Delivery

Concrete depth for the video half of generated-media-delivery, written against the `mmx` CLI
(MiniMax). The lane logic generalises; the flags and the verify/QC/upscale commands are exact.

## 1. Lane table

| Need | Model flag | Accepts | Key class |
|---|---|---|---|
| Text-to-video, plain | default `MiniMax-Hailuo-2.3` | `--prompt` | Token Plan ok |
| Animate a still (I2V) | default or `-Fast`, `--image` | `--prompt --image` | Token Plan ok |
| Move from composition A to composition B | default + `--image --last-frame` (auto `MiniMax-Hailuo-02`) | `--prompt --image --last-frame` — **no duration, no ratio** | Token Plan ok |
| 2K, 4–15 s, explicit duration/ratio, multimodal reference image/video/audio | `--model MiniMax-H3` | `--duration --ratio --reference-image/‑video/‑audio` | **pay-as-you-go / credit only** |
| Keep one face/character across shots | `--subject-image` (auto `S2V-01`) | `--prompt --subject-image` | Token Plan ok |

Highest-fidelity-first is the wrong default: the legacy lane accepts the credential the federation
usually holds. Reach for the top lane only when the request genuinely needs 2K, a non-default
duration, or multimodal references **and** the right key class is available.

## 2. Flag compatibility is not additive

`--duration`, `--ratio`, `--reference-image`, `--reference-video`, `--reference-audio` belong to the
newer model only. Adding any of them to a default-model call fails before submission:

```
{"error": {"code": 2, "message": "--reference-image, --reference-video, --reference-audio,
 --duration, and --ratio require --model MiniMax-H3."}}
```

So the first/last-frame lane is a **legacy** lane: keep it to `--prompt --image --last-frame
--download`, omit duration and ratio, and expect a fixed aspect around 1364×768 @ 24 fps, ~6 s.
Do not "fix" the error by adding the newer model reflexively — that swaps the key requirement too.

## 3. Model-series key gating

- A subscription / Token-Plan credential against the H3 series returns a model-series gate: the
  series is not entitled to that credential class. Nothing is submitted, so no task is in flight and
  no retry is owed.
- Correct response order: report the gate, check for a pay-as-you-go key already injected as an env
  var, save it once if present (`mmx config set --key api_key --value "$MINIMAX_API_KEY" --quiet`),
  then re-run the same request **unchanged** on the newer model.
- Never retry the identical command, never submit a second paid task, never ask the user to paste a
  key into chat, never quote a key in a transcript.
- Region fallback is only for a pre-submission region/endpoint/routing failure where no task ID came
  back. A model-series gate is not a region problem.

## 4. Long waits

Blocking calls with `--download` exceed the foreground command cap. Launch as a tracked background
process and wait on that same session; a missing final path while the session is alive is not a
failure. The failure to avoid is a duplicate paid submission after an interrupted wait.

## 5. Verify → QC → upscale

1. **Verify the artifact.**
   ```bash
   ffprobe -v error -select_streams v:0 \
     -show_entries stream=width,height,r_frame_rate,nb_frames \
     -show_entries format=duration -of default=noprint_wrappers=1 out.mp4
   ```
2. **Read frames back before showing anything** (first / middle / last) through `vision_analyze`:
   ```bash
   ffmpeg -y -v error -i out.mp4 -vf "select='eq(n\,0)+eq(n\,70)+eq(n\,143)'" -vsync 0 qc/f_%02d.png
   ffmpeg -y -v error -sseof -0.08 -i out.mp4 -frames:v 1 qc/f_last.png
   ```
   Check the invariants the request named (framing, focal beat, which subjects landed, garbled text,
   melted hands, mirror geometry). Absent beat → regenerate, never narrate.
3. **Upscale when the ask is "better quality" and the top lane is unreachable.**
   ```bash
   ffmpeg -y -v error -i out.mp4 \
     -vf "scale=1920:1080:flags=lanczos,unsharp=5:5:0.45:5:5:0.0" \
     -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -movflags +faststart -an out_1080p.mp4
   ```
4. **State which lane rendered**, and offer the re-render once the right key class is in place.

## 6. Prompt shape

One camera behaviour per clip. A single continuous move (``the camera drifts slowly forward through
the haze past him, then settles on ...``) lands; multi-action direction and cuts do not. Most
important element first, payoff beat last. Reference-frame mode and multimodal-reference mode cannot
be mixed, and frame interpolation needs both an opening and a closing composition at the same aspect
ratio.
