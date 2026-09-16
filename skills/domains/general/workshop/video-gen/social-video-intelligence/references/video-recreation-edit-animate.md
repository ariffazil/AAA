# Video Recreation — Edit Frame → Animate (Token Plan)

Verified 2026-08-15. Use after Layer-0 forensics when the user wants to re-animate an
analyzed video, or insert a new person/object into it ("add someone worshipping him",
"now with two guys", etc.).

## Pipeline

1. **Source frame**: `ffmpeg -y -ss 1 -i <video>.mp4 -frames:v 1 -q:v 3 frame.jpg`
   (pick a clean early frame; 0.5–1s usually avoids motion blur).
2. **Edit the frame** — `wan2.7-image-pro` image-edit, same endpoint as
   `token-plan-image` skill:
   `POST .../services/aigc/multimodal-generation/generation`
   payload: `input.messages[0].content = [{"image":"data:image/jpeg;base64,<b64>"},{"text":"<edit prompt>"}]`,
   `parameters: {"size":"720*1280","n":1}` (match source aspect; 720*1280 for 9:16).
   Edit-prompt pattern that preserves the original: "Keep the existing <subject>, his
   pose, and the entire scene exactly as they are. Add <new element>... Same lighting,
   same background, same photorealistic style, vertical composition."
   Response image URL: `output.choices[0].message.content[0].image` (OSS URL, ~24h expiry).
3. **Animate** — `happyhorse-1.1-i2v`, endpoint
   `POST .../services/aigc/video-generation/video-synthesis` with `X-DashScope-Async: enable`.
   Payload (async, then poll `/tasks/<task_id>`):

   ```json
   {
     "model": "happyhorse-1.1-i2v",
     "input": {
       "prompt": "<motion prompt: gaze shift, breathing, breeze, light shimmer; natural subtle motion only>",
       "media": [{"type": "first_frame", "url": "<OSS image URL from step 2>"}]
     },
     "parameters": {"resolution": "720P", "duration": 8}
   }
   ```

   **The field is `input.media`, NOT `input.img_url`.** Wrong field → first poll returns
   `{"code":"InvalidParameter","message":"Field required: input.media"}`.
   Pass the step-2 OSS URL straight into `media[].url` — do not download and re-base64 it.
   `duration` supports 3–10; match the original video's length for a seamless swap.
4. **Verify before delivering**: extract 2–3 frames from the output (`ffmpeg -ss`) and
   `vision_analyze` them (character count, pose consistency, artifacts). Only then send
   the file to the user.

## Quota seat ladder (applies to BOTH edit and i2v submits)

`Throttling.AllocationQuota` = seat exhausted, not fatal. Walk the same endpoint with the
next key: `QWEN_TEAM_OWNER_API_KEY` → `QWEN_API_KEY` → `QWEN_INDIVIDUAL_API_KEY` →
`QWEN_HERMES_API_KEY` (source `/root/.secrets/kunci-mas.env`). Keep the key that returned
`task_id` for polling too. Observed 2026-08-15: first two seats exhausted on both calls;
individual key carried both.

## Green Net (content moderation)

Shirtless-but-tasteful fitness framing PASSED both wan2.7-image-pro edit and happyhorse
i2v on first try (2026-08-15). If `DataInspectionFailed` appears, soften per the
token-plan-video skill's retry pattern (clothed-but-fit, friendly-respectful beats).
