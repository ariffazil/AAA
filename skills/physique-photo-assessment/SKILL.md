---
name: physique-photo-assessment
description: Use when physique photos or body-fat questions arrive.
category: physique-intel
version: 1.0.0
license: MIT
capability_tier: fed-multimodal-vision
ecology_state: WARM
---

# Physique Photo Assessment

Reading body composition off photos, answering gym questions about it, and rendering
"what would this body look like leaner" without inventing a face.

Companion skills (external, read-only to curation): `BIOHACK-PEPTIDES` for compound
questions, `ped-hormone-advisory` for TRT/prep pharmacology, `gemini-media-gen` for the
generation lanes.

## Procedure

1. **Look at every frame before answering.** When several photos arrive (front, angle,
   close-up), read them together and give ONE verdict. Answering each photo as a
   separate person makes it obvious nobody looked.
2. **Call `vision_analyze` with a clinical question**, one ask per frame: fat range,
   distribution (lower abs / flanks / chest), muscle cues (pecs, delts, arms), and whether
   the lower abdomen is soft or tense. Vision returns confident prose and will invent
   segments that are not there — check the cues it names against what the frame can show.
3. **Answer in a range, then name the distribution**, then what muscle is already developed.
   That order matches how a person thinks about their own body.
4. **Separate mass from definition.** "Sado" is two variables — how much muscle exists and
   how much of it is visible. Grade both. The phrase that lands in gym register is
   *sado basah, bukan sado kering* / "masa ada, cut takda".
5. **Convert the number into kg and weeks.** Stage lean ≈ 5–7%, full visible abs ≈ 10–11%.
   A mid-teens physique is 4–6 kg from stage, 12–16 weeks at a moderate deficit. A number
   with no timeline attached is trivia.
6. **Say what the frame cannot show** — back, legs, side profile, anything under clothing —
   then stop. Offer calliper / DEXA when a precise figure is wanted.
7. **Close on the lever, not the label.** At mid-teens with base muscle, the answer is a
   small deficit, high protein, and keeping the heavy training. Compounds are a different
   conversation (route to `BIOHACK-PEPTIDES`) and rarely the lever at this conditioning.

## Rules that hold every time

- **Range, never a decimal.** One frontal, floodlit phone photo carries ±2–3% error.
  "13–17%, tengah 15%" is honest. "15.0%" is invented and will be tested.
- **Refuse the guess when the body is covered.** Loose overalls, a hoodie, a distance shot,
  a work jumpsuit — there is no data. "Aku tak boleh teka, ini menipu" costs nothing to give.
- **Never let a fat estimate become a muscle verdict.** A thick, strong person can still read
  soft in one lighting condition. Grade the mass on its own evidence.
- **Distribution beats percentage for advice.** Lower abdomen then flanks is the normal male
  pattern and the least responsive early — say so up front, or the first three weeks of a cut
  get read as failure.
- **Anatomy questions deserve anatomy.** A nipple is gland plus smooth muscle: it does not
  shrink on a cut and its size does not track bodyfat. The pad *around* it does. Only a hard
  disc under the areola is a different, clinical story. Name which tissue was pinched.
- **Recovery cannot be bought.** Sleep, protein, and not loading the injured tissue are the
  levers; supplements are marginal. Say that even when the ask is a purchase.
- **No body is mine to keep.** When someone declines to share their body with the agent,
  agree in one line and move on — the read was of a photo, not of a person.

## Rendering "what would he look like at stage condition"

The follow-up ask is almost always a comparison image. It must NOT change the face.

Probe the live scripts first — paths and names differ per host:

```bash
find /root -maxdepth 4 -name 'gemini-image*.py' 2>/dev/null
```

On the KVM8 runtime the working call is `/root/scripts/gemini-image-edit.py`, and its
argument order is **OUT, PROMPT, then reference images** — not prompt-first:

```bash
set -a && . /root/.secrets/kunci-mas.env && set +a   # file uses `export` prefix; plain grep|cut returns garbage
/usr/bin/python3 /root/scripts/gemini-image-edit.py /abs/out.png "<prompt>" /abs/ref.jpg \
  --model gemini-3-pro-image --aspect 4:5
file /abs/out.png   # gemini-3-pro-image writes JPEG bytes under a .png name — expected
```

Prompt-first on that script fails with `IndexError: list index out of range` before any API
call, which reads like a broken script rather than swapped arguments.

Prompt shape that holds identity: name the invariant features (hair cut, eyebrows, facial
hair, jawline, skin tone, expression), enumerate what stays fixed (pose, garment, watch,
background, camera angle, framing), then state the single thing that changes and the
anatomical cues that go with it. Close with `photorealistic, real skin texture, no text,
no watermark, one person only`.

Then verify with `vision_analyze` on BOTH output and reference, describing the face on each
and comparing. A convincing render with a different jawline is the failure you are checking
for. Deliver it as "this is what the cut would give", never as evidence about the real body.

## Pitfalls

- **Vision prose overshoots lean.** It will say "extremely low body fat" on a mid-teens torso
  because abs are faintly visible. Discount the adjectives; keep the structural cues (lower
  abs obscured, flanks soft, sternal line present, vascularity).
- **One frame is one angle.** Do not let a single photo generate confident claims about back
  development, leg size, or posture.
- **Don't grade people nobody asked about.** If a bystander appears in the frame, the
  assessment applies to the subject of the question only.
- **The render is a forecast, not a photo.** Label it in the same message, or it gets read as
  a claim about reality.
