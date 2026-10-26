---
name: multi-reference-image-edit
description: "Use when 2+ supplied photos go into one frame."
version: 1.0.0
author: Hermes
license: arifOS
tags: [image-edit, multi-reference, identity, gemini, qc, delivery]
metadata:
  hermes:
    category: creative
    tags: [image-gen, image-edit, identity, verification]
triggers:
  - user sends two photos and asks for "both of us together" / "me hugging him" / "put me next to him"
  - a scene needs a specific supplied face AND a second supplied person or product
  - an edit must keep a person while changing pose, setting, or contact
capability_tier: fed-multimodal-vision
ecology_state: WARM
---

# Multi-Reference Image Edit — several supplied photos in one frame

Turning N supplied photos into ONE coherent scene with believable contact. The failure mode is
quiet: the model returns a well-lit, plausible image in which the people are standing apart with a
hand on a shoulder, the hands have fused, and nobody was told.

## Procedure

1. **Locate the working script before assuming the capability is missing.** Paths in older skills
drift:

   ```bash
   find / -name 'gemini-image*.py' -not -path '*/proc/*' 2>/dev/null
   ```

   Two shapes exist and they are not interchangeable: a single-reference generator
   (`PROMPT OUT [MODEL_CHAIN] [ASPECT]`, positional) and a multi-reference editor
   (`PROMPT OUT --image A --image B`, repeatable). Confirm which one you have before composing the
   call.

2. **Prepare one clean figure per reference.** A stacked social post, a two-panel screenshot, or a
   collage gives a CROP, not a person. Slice the panel you want and confirm it:

   ```python
   from PIL import Image
   im = Image.open(src); w, h = im.size
   im.crop((0, 0, w, int(h * 0.5))).save(ref, quality=95)   # top panel of a stacked post
   ```

   Then vision-check the crop: exactly one person, head plus at least mid-torso, nothing cut where
   the new pose will need body. Feeding a two-panel image makes the model average the panels.

   Note the interpreter: on hosts where the default `python3` lacks PIL, `/usr/bin/python3` usually
   has it — try the system python before installing anything.

3. **Generate with every reference as an input part, role-labelled in the prompt.**

   ```bash
   python3 /root/scripts/gemini-image-multi.py \
     "IMAGE 1 = <who this is + the features to keep>; IMAGE 2 = <who this is + features to keep>. <scene>. <contact geometry>. No text, no watermark." \
     /root/forge_work/out.jpg \
     --image /path/ref-a.jpg --image /path/ref-b.jpg \
     --model gemini-3-pro-image,gemini-2.5-flash-image --aspect 4:5
   ```

   Unlabelled references blend into one face. Say `IMAGE 1 =` / `IMAGE 2 =` explicitly, and name the
   features to hold per figure (hair, jaw, build, skin tone, garment).

4. **Verify with a vision read before delivering** — see the checklist below. A whole-frame glance
   passes what a zoom rejects.

## Contact geometry — the rule that costs the re-rolls

A relationship verb is not geometry. *"Giving each other a warm bro-hug"* reliably renders two
people standing apart, chests clear, one hand on a shoulder. The model reads *hug* as a pose label.

Write the body mechanics instead:

> arm wrapped fully around the other's shoulders and back, other arm around the waist, chests and
> shoulders pressed together, heads tilted toward each other, both smiling, bodies touching — not
> posing apart

Expect at least one re-roll even with mechanics spelled out. Judge the result on contact, not on
composition.

## Model tier decides hands and stray lettering

Same brief, same two references, measured in one session:

| Model class | Result |
|---|---|
| flash-class (`gemini-2.5-flash-image`) | upper hand fused into shirt fabric, fingers unreadable; invented gibberish lettering on the waistband seam |
| pro-class (`gemini-3-pro-image`) | five correct fingers on every visible hand, unmarked fabric, no text anywhere |

For frames with two bodies in contact, list the pro model FIRST and keep flash as fallback. Cost of
the pro call is one call; cost of shipping the flash take is the trust on every take after it.

## Verification checklist (run all, in this order)

1. **Contact** — are the two bodies actually touching with arms wrapped, or merely posed near each
   other?
2. **Hands** — five separated fingers on every visible hand; nothing melted into fabric or hair.
3. **Invented text** — any lettering on a waistband, cap, singlet, poster, or sign is fabricated.
   Reject on sight; add `plain unmarked waistband, no lettering anywhere` to the prompt and re-roll.
4. **Both subjects present and correct** — right person on the right side, no third figure invented
   to fill space, no size relationship flipped.
5. **File sanity** — `ls -la` and `file` on the output; a plausible path with zero bytes is the
   classic silent failure.

## Delivery — one clause of honesty

Multi-reference is conditioning, not compositing: the model REGENERATES both faces. Identity lands
close but not pixel-identical, and saying nothing about it is an F2 failure.

- Ship one artifact, not the roll.
- Add the disclosure clause in the same message ("muka bukan pixel-identik — model regenerate, bukan
tampal"), and offer the pixel-exact path — cutout + composite — if the requester needs the face
unchanged.
- Do not narrate the attempts. "I tried three times" is a reason the delivered take is clean, not
  content. One short line that the earlier takes failed the contact/anatomy check is the maximum.

## When NOT to use this

- Single-subject face swap with a pixel-exact requirement → composite (cutout + background + paste),
  accepting the jawline clipping risk.
- A brand-new person who was never photographed → plain text-to-image.
- Text inside an existing image → PIL or an OCR/edit tool, not a generative model.

DITEMPA BUKAN DIBERI.
