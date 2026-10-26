---
name: faceless-subject-rendering
description: "Use when a rendered person must be unidentifiable."
version: 1.0.0
tags: [image-generation, privacy, cropping, vision-verify, persona]
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# Faceless Subject Rendering

For asks where the body carries no identity — faceless torso, anonymous
physique shot, "muka tak ada" — do NOT try to talk the image model out of
rendering a face. It will not comply dependably, and each retry costs a full
generation. Build the crop into the pipeline from the start.

## Procedure

1. **Generate normally.** Direct body, light, props and camera as usual
   (photorealistic human-image lane for prompt structure). Include the
   faceless intent in the prompt anyway — it sometimes helps composition —
   but treat it as a wish, not a control.
2. **Read the render with a vision pass before anything else.** Three
   questions in one call: is the face visible · is there nudity or exposed
   genitalia · is there any text or watermark. Do not skip this to save a
   step; you cannot see the pixels, and a plausible prompt is not a receipt.
3. **Measure the crop line, don't guess it.** Ask the vision pass for image
   width/height and the pixel y of the bottom of the chin / top of the neck.
   Cropping at a fixed fraction of image height lands on the chin or leaves a
   sliver of jaw — both read as an accident rather than a composition.
4. **Crop in post** with the measured line (`PIL.Image.crop`), then re-run the
   vision pass on the cropped file asking narrowly: "is any part of the face,
   chin or jaw visible now, and what appears at the very top edge?" Cropping
   "below the chin" by eye leaves the chin. Verify the second time.
5. **Deliver the verified crop and say what it is** in one short line: a
   rendered body, not this person and not anyone they know.

## Pitfalls

- **Prompted framing is not obeyed.** "Head cropped out of frame", "framing
  starts below the chin", "faceless anonymous subject" survive the prompt and
  lose to the model's portrait prior. Count on the crop.
- **Vision descriptions drift toward interpretation.** The same image reads as
  "face fully visible" in a wide pass and "lower face visible at the top edge"
  in a zoomed pass. Ask the narrow positional question (which body part sits at
  the top edge), never "describe the image".
- **A crop that removes the face can also remove the shot.** Jaw-down crops
  often clip the shoulders at the sides. Re-frame by choosing the crop
  rectangle; do not regenerate to fix framing.
- **Keep the source file.** Save the uncropped original beside the crop so a
  later request for a different framing needs no new generation.

## Boundaries

Consenting adults only. No named third parties, no claim that the subject is a
specific real person, no underage framing in any register. If the request adds
a non-consensual or real-person-harm axis, hold that axis and offer the
anonymous composition — do not refuse the whole scene.
