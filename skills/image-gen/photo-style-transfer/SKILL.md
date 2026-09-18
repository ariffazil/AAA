---
name: photo-style-transfer
description: "Use when restyling a photo into another aesthetic."
version: 1.0.0
tags: [image-editing, style-transfer, image-to-image, dashscope, qwen-image-edit, multimodal]
---

# Photo Style Transfer (restyle an existing photo)

## Route first: generate vs edit

Two different requests look alike in chat and need opposite tooling:

| Request shape | Lane |
|---|---|
| "buat gambar X" / "imagine a scene of X" | text-to-image generation |
| "buat gambar **ni** jadi X" / "restyle this photo" / attached image + style name | **image-to-image (this skill)** |

A text-to-image model given "restyle this photo as <style>" without the source pixels in hand returns
a *new* picture that merely resembles the description — the subject is gone. Confirm which direction
the user means before spending a call.

## Procedure

1. **Locate the source.** Chat attachments land under the cache images dir; copy to a working path so
   the filename extension yields the right mime type.
2. **Read the source with vision once** if you need to name what is in it (who, what they wear,
   setting). Do not guess details you cannot resolve — see *Resolution floor* below.
3. **Send the edit request** (see *Request*) — one call, source as a base64 `data:` URI.
4. **Download the returned URL** to a local file immediately; the link is short-lived.
5. **Convert to JPG** for chat delivery and send with `MEDIA:<abs-path>`.
6. **Read the result back with vision before claiming success** — confirm the style landed and the
   subject survived. Report what you saw, not what you asked for.

Runnable implementation: `scripts/photo_style_transfer.py <src> <out> [prompt-file]`.

## Request

```
POST https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
Authorization: Bearer $DASHSCOPE_API_KEY
Content-Type: application/json

{
  "model": "qwen-image-edit",
  "input": {"messages": [{
    "role": "user",
    "content": [
      {"image": "data:image/jpeg;base64,<...>"},
      {"text": "<restyle instruction>"}
    ]
  }]},
  "parameters": {"watermark": false}
}
```

Result URL lives at `output.choices[].message.content[].image`. Image-*to*-image lives on the
**multimodal-generation** path; the OpenAI-compatible `/images/generations` route is text-to-image and
returns 404 for models that only exist on the multimodal path — that is a wrong-API-shape signal, not
a dead model. Do not abandon the lane; switch the path.

## Prompt shape

Name the target aesthetic **and** pin what must survive:

> Restyle this photograph into a classic <style> illustration. Keep the same person, pose, clothing
> and composition, but redraw everything in the <style> aesthetic: <line quality, texture, palette,
> lighting specifics>. Remove photorealism entirely.

The preservation clause is load-bearing. "Keep the same person, pose, clothing and composition" is
what stops the model inventing a substitute subject; without it the output is a stranger in the right
costume.

Add "remove photorealism entirely" when going photo → illustrated, or the result lands as a filter
overlay rather than a redraw.

## Verification before delivery

Read the output with vision and check, in order:

1. **Subject survived** — same person, pose, framing as the source.
2. **Style actually shifted** — illustrated/stylised, not the original with a colour grade.
3. **No artifacts** — mangled hands, duplicated limbs, garbled background geometry, invented text.
4. **No fabricated lettering.** Generated images invent plausible-looking text. Describe the artwork
   as containing calligraphic marks; never transcribe them as if they were legible signage.

If it fails, change one variable (usually the preservation clause) and re-run once. Never describe a
restyle you have not looked at.

## Pitfalls

- **Never put base64 image data in a shell argument list.** Large bodies exceed argv limits and the
  request dies with an `Argument list too long` error that reads like a provider outage. Build the
  JSON body inside a script and send it from the body.
- **Output dimensions follow the source aspect ratio**, not any requested ratio. Check the actual
  size instead of assuming the aspect you asked for.
- **A models list is not a capability.** Do not advertise a lane until a real edit has returned a
  file. Probe with one small image when quota is uncertain.
- **Do not restyle a real, identifiable person into an intimate or defamatory framing.** Style
transfer is fine; do not generate content about a real person that they would not consent to.

## Resolution floor — do not read past it

Identifying details in the *source* has a hard limit. Below roughly 640×360, lettering across a chest
is about 10px tall. Iterating crops and zoom factors does not converge: successive vision calls return
**different** confident words for the same garment. The tell is disagreement between attempts; the fix
is not another attempt.

Zoom once at native resolution. If the letters do not resolve, report **UNREADABLE** and ask for a
better frame. Report what the resolution *does* support — colours, trim, band shape, garment type,
number of subjects — as lower-confidence facts, kept separate from anything unreadable. Never put a
guessed word in the same sentence as a verified one.

## Related skills

- `image-gen-fallback-chain` — text-to-image provider ladder and route states.
- `image-identity-transfer` — carrying a face into new compositions (likeness over restyle).
- `poster-vision-extraction` — reading text out of images without guessing.
