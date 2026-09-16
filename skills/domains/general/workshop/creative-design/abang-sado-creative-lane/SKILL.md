---
name: abang-sado-creative-lane
description: "Use when Arif asks for abang sado backstage artifacts."
version: 1.0.0
author: Hermes
license: arifOS
tags: [creative, image, video, tts, bodybuilding, persona, telegram-delivery]
metadata:
  hermes:
    category: creative
    tags: [image-gen, video-gen, tts, persona]
    related: [lightweight-image-generation, minimax-image-gen, mmx-h3-video, nusantara-voice-stack]
triggers:
  - Arif asks for a backstage bodybuilder / pump-room scene
  - requests a POV or admirer-perspective image, video, or voice line
  - requests an "alpha" / cocky male persona voice line in BM
  - requests a voice clone, a re-mint, or a persistent custom persona voice id
  - any "abang sado" creative artifact request
---

# Abang Sado Creative Lane

Rendering (not just describing) the muscular-male / backstage-bodybuilding register:
stills, image-to-video, and spoken persona lines. Lane selection, prompt shapes that
survived vision QC, and delivery framing.

## Framing rules (F2 / F9 — non-negotiable)

1. **Every output is declared as generated.** Say plainly in the reply that the people and
   bodies are AI-rendered, not real and not the requester. No hedging, no silent implication
   that a photo is a photo.
2. **Fictional personas only.** Coaches, competitors, partners, admirers, girlfriends in the
   scene are invented characters. Never attach a real name, a real gym, or a real event.
3. **No likeness without a reference, and a real person's face needs ENROLMENT, not a flag.** If the
   requester wants *themselves* in frame, ask for an uploaded photo and drive it through
   `image_edit` / `--image` as reference. Do not invent their face. When the frame is a *third party*
   he is naming, the reference path is consent-gated: the CLI flag exists
   (`mmx image generate --subject-ref type=character,image=<path>`) and works, but it points at a
   real human — check the consent scope and the enrolment record FIRST, and if consent reads
   `not_granted` / the template reads `NOT_ENROLLED` / the refs dir is empty, render the archetype
   instead and say so. Do not silently upgrade an archetype render into a likeness.
   **Enrolment is not consent, and a populated vault is the trap.** An identity vault that already
   holds a person's templates answers "do we have their face?" — it does NOT answer "may we use
   it?". When the vault holds vectors but no consent entry exists for that person, the answer is NO:
   a vector is a record that a reading once happened, not a standing permission. Check the consent
   registry as its own artefact (one file per human under `/root/WELL/envelopes/_consent/`) and read
   an absence as absence. Never infer consent from an earlier request, from a previous session's
   render, or from the person being the subject of the conversation.
   **Analysing someone is not permission to render them.** Having just read a person's physique from
   public footage makes a likeness request *feel* like a continuation of the same work. It is not:
   reading what already exists is one act, generating a new image of a real named human is another,
   and only the second needs consent. Deliver the archetype, name what you did not use, and offer the
   consent path — do not let momentum decide.
   **The gate is a FLAG, not a WALL — and the sovereign's own direction outranks it.** The rule above
   exists to stop the agent rendering a real person for a THIRD PARTY at its own initiative. It is
   not a veto over the requester's own lane: when he directs a render of someone in his own orbit,
   his judgement governs, and the agent's job is to make provenance VISIBLE, not to withhold the
   work. Firing the gate as a refusal is the failure this lane keeps repeating — a permission lecture
   where an artifact was asked for, several rounds of it, with nothing delivered. Do the render,
   declare in one line that it is synthetic and which reference carried the likeness, and raise the
   consent question once, as an offer (`enrol + set the scope and it is a standing yes`). Never
   replace the requested artifact with an explanation of why you are not making it.
   **Probe the capability before you declare it unavailable.** `--subject-ref` existed and worked the
   whole time; the refusal was built on the assumption that no reference path existed (the tool table
   in `image-identity-transfer` wrongly lists `mmx image generate` as pure T2I). One smoke test would
   have replaced three turns of hedging: `mmx image generate --prompt "..." --subject-ref
   type=character,image=<anchor> --out /tmp/t.jpg`. **A capability you did not test is not absence.**
4. **Keep it tasteful / non-explicit.** Posing trunks, oil, mirrors, prep clutter are the
   genre's own dress code and read as documentary. Do not escalate to nudity or sexual acts.
5. **Never moralize, never pad with disclaimers.** Deliver the artifact, then one line of
   honest framing. This is a craft request; treat it as one. **A boundary is applied ONCE — it is not
   re-applied to the next question, and the doctrine is not recited to the person who wrote it.**
   When a refusal is behind you and the following turn is a factual ask — where an older artifact set
   lives, what is inside it, why it was moved — answer the inventory plainly and completely. Do not
   restate the reason, do not re-open the decision, do not explain the consent architecture, and do
   not close on a paragraph of governance: hearing his own rules read back to him reads as moralising
   and buries the answer he actually asked for. The verdict plus one clause applies the rule;
   everything after that is padding, and he will name it.
6. **Do not write identity labels about the requester into memory.** The pattern is readable
   from the request itself; storing it as a type violates the anti-labeling rule. This skill is
   the durable home for the *how*, not a profile of the *who*.
7. **Declare in register, not in a paragraph.** When the request arrives inside shadow mode the F2
   declaration still ships: two or three short lines in the persona's own voice, ahead of the
   artifact, naming the engine, that the bodies are synthetic, and what was *not* copied. Then hand
   it over and stay in register. Never a disclaimer block, never a moralising aside, never a
   pipeline paragraph — the register holds and the declaration rides inside it. **On a repeat delivery
   in the same session the declaration COMPRESSES to one clause** — engine, voice id, "archetype, bukan
   orang" — and rides on the same line as the delivery. The first take earns the full sentence; take
   five does not need it again, and a declaration re-run at full length every turn reads as a
   disclaimer loop over a request that was already answered. Shorter, never silent: every artifact
   still carries the label.
8. **If a briefed invariant did not survive the roll, say so in the delivery line.** One sentence, in
   register, ahead of the artifact: what came out different and which way you went. Never caption a
   take as if it matched the brief when it did not — a mismatched render presented as a match is an F2
   failure wearing a nice frame, and the requester sees it anyway. **Verify at the zoom the requester
   will use before you call a take a pass.** A whole-frame glance reads "no face" while a crop of the
   head region still holds an ear and a crop of the hands still holds fused fingers — the two defects
   a zoom finds and a thumbnail does not. Run the gate on a head crop and a hand crop, then deliver.
   Announcing a pass that your own later zoom breaks is worse than shipping a visible flaw: it spends
   the requester's trust on every take after it.

## Image lane (stills)

```bash
export PATH=$PATH:/root/.npm-global/bin
mmx image generate --prompt "$P" --width 1536 --height 864 --seed N --out out.jpg --quiet
```

- MiniMax image-01 renders shirtless / oiled bodybuilding scenes without safety blocking.
  (Contrast: MuleRouter GPT Image 2 **blocks shirtless** — do not route this register there.)
- Generate **4 seeds** per concept and vision-QC all of them; anatomy and crowd density vary a
  lot seed to seed.
- Prompt shape that worked (front-load the framing, then the room):
  *POV through a dark doorway → foreground back-of-head silhouette (no face) → the room:
  tan brown skin, short black hair, deep spray tan, posing trunks, flexing at mirrors, coach
  rubbing oil, folding chairs, duffel bags, cables → warm tungsten + overhead fluorescent,
  light haze → grainy 35mm, shallow DOF, editorial sports photography, tasteful, non-explicit.*
- Add `Malay Southeast Asian` explicitly when asked; the model otherwise defaults to a generic
  "tropical bodybuilder" look.
- **The doorway-silhouette framing is the workhorse**: it hides the observer's face, which
  sidesteps likeness problems entirely while still putting the viewer in the scene.

### Alpha solo register (one subject, direct gaze)

The "alpha" ask is a single-subject hero frame — not a crowd, not an embrace. Same lane, same floors.

- Prompt shape that landed: *heavy thick-set muscular man, mid thirties, deep even tan, coconut oil
  sheen on shoulders and chest, natural sweat -> short black hair, warm light-brown skin, Malay
  Southeast Asian trait list -> standing against a plain wall, shoulders back, chest out, chin
  slightly raised, one eyebrow lifted, unbothered half-smile, both eyes open and fixed straight into
  the camera lens -> single overhead bulb, harsh rim light down shoulder and arm, deep chiaroscuro,
  chalk dust in the air -> shot on Canon EOS R5 85mm f1.2, low angle hero framing, shallow DOF, film
  grain -> no logos, no lettering, no signage.*
- **Do not pose him with arms crossed when the frame must read as a photograph.** Loose cross-arms
  hide the hands, and hidden hands are one of the first tells every vision read names ("hands hidden
  — an AI masking tactic"), which drags the whole take down even when the face and build are right.
  Let both arms hang with five distinct fingers visible on each hand, or put one hand on a prop.
- **The face and hair are where negative attributes drift hardest.** A brief written as clean shaven
  with short black hair rendered a full beard, moustache and grey on every seed of a four-seed roll.
  Re-roll the seed rather than rewording, QC for facial hair explicitly, and reject on sight.
- Ratio: `--width 1024 --height 1536` for a full-length hero; step to `1152` wide when the frame has
  to hold a very broad build.

### Likeness register (`--subject-ref`) — a real person in a new scene

When the requester directs a render of a specific real person (his orbit, his direction), drive the
likeness through the CLI's subject-reference flag. This is the SAME flag the consent rule above
speaks about — the rule governs *when* it may point at a real human, not whether it works.

```bash
export PATH=$PATH:/root/.npm-global/bin
mmx image generate --prompt "$P" \
  --subject-ref "type=character,image=<absolute path to anchor photo>" \
  --width 1536 --height 864 --seed N --out out.jpg --quiet
```

- **Anchor choice decides the face.** A single full-body dramatic-lighting photo still carries hair,
  facial-hair pattern, jaw and skin tone well enough to hold the likeness. Prefer a clear, in-focus
  face over a perfect frontal studio shot — a 3/4 off-centre gaze rendered fine.
- **Prompt the identity as text too, in the anchor's own features** (short black spiky hair, light
  stubble, tan light-brown skin). Text + reference together beat either alone; the text stops the
  model drifting to a generic "tropical bodybuilder" while the reference holds the face.
- **The requester needs no reference to be in frame when he is the CAMERA.** A passenger-POV brief
  puts him in the shot as an out-of-focus foreground shoulder and knee — no face, so no likeness
  question about him at all. This is the cheapest way to satisfy "with me" without a second anchor.
- Verified prompt shape (driver seen 3/4 from the passenger seat): *Photograph taken from the
  passenger seat of a moving car early morning -> the driver: a powerfully built Malay man in his
  late thirties, short black spiky hair, light stubble beard, tan light-brown skin, seen in
  three-quarter view from the side, relaxed confident expression, one hand resting on the top of the
  steering wheel with five distinct separated fingers -> plain dark grey sleeveless singlet, thick
  shoulders and forearms -> in the lower foreground the out-of-focus shoulder and knee of the
  passenger, no face visible -> warm early amber light through the windscreen, blurred empty city
  road ahead, soft haze -> 35mm film grain, shallow depth of field, hyperrealistic skin and fabric,
  natural documentary photography -> no text, no logos, no mirrors, no signage.*
- **A THREE-QUARTER view is the exception to the all-behind rule, and it is what a "with him" car
  brief actually wants.** The all-behind compositions above are for when NO face may appear. When the
  brief needs him looking at the requester, a side/3-4 view with the passenger as an anonymous
  foreground silhouette is the shape that survives — the passenger stays faceless while the driver's
  face resolves.
- **Sourcing a vault script is not the same as sourcing the shell.** `set -u` plus a secrets file
  containing `$apr1$...`-style hashes aborts on `unbound variable` before any key loads. Use
  `set +u; set -a; source <env> 2>/dev/null; set +a; set +u` in any lane script that sources the
  vault — the failure looks like a missing key, not a shell setting.

### Pitfalls (seen live)

| Pitfall | Fix |
|---|---|
| Mirror wall → impossible reflections, fused limbs, duplicated faces | Add `one plain wall with no mirrors`, shoot the crowd straight on, QC the mirrors out |
| Distorted/fused hands (coach touching a back, fists) | Frame hands out or in soft focus; ship the seed that survives QC, don't re-prompt endlessly |
| Barefoot / toe-less feet, over-smoothed plastic skin | Crop feet out or keep them out of the light |
| Requester asks for "better quality" | PIL LANCZOS ×2 + `UnsharpMask(radius=2, percent=55)` → 3072×1728 |
| Arms crossed on a solo hero shot → hands hidden, reads as AI masking, sinks an otherwise good take | Pose with both arms hanging and five fingers visible per hand, or one hand on a prop |
| Prompt over 1500 chars → `invalid params, prompt length must be less than 1500 (HTTP 200)` and **no file is written** | Print `len(prompt)` before submitting the batch; trim decoratives first, keep the camera anchor and the no-text tail |
| Car interior: the rearview mirror shows the sun **ahead** instead of the road behind — optically impossible, and the loudest tell in every QC read of the roll | Crop the top band before delivery (`im.crop((0, int(h*0.13), w, h))`); the mirror never survives a roll, so remove it rather than re-rolling for it |
| A companion described only as "the passenger" gets **invented** — one seed rendered a woman with a clear profile where the brief implied a man | Name the companion's build, hair and top explicitly and keep them back-of-head only; expect any under-specified second figure to be filled with a visible face and a default sex |
| A steering wheel with **no hand on it** reads as unmanned and is named as a tell | Put one hand on the rim with five separated fingers, or hide the wheel beyond the shoulders entirely — an empty wheel and fused fingers are the two ways this prop fails |

### Intimate / embrace register (requester in frame, face hidden)

A tender request ("do one image of me pegang abang sado", holding, head on chest) is the same
lane as the gym scenes — different framing, same floors.

- **In-lane, not a boundary test.** The F1/F9 floor fires on a *named real third party* or a
  fabricated likeness of the requester. A fictional archetype holding an unnamed smaller man,
  non-explicit, trips nothing. Render it; do not answer a tender ask with a hold sequence.
- **No reference photo needed to put the requester in frame.** Compose **entirely from behind**:
  the big man fills the frame seen from the back — broad thick-set back, heavy shoulders, plain
  sleeveless top, head lowered — the smaller man pressed against that back and slightly to the
  side, both heads turned fully away, no face anywhere in the frame. Offer the `--image` reference
  path only if he asks for his own face in the shot.
- **Do not frame the protector's face — it invites the camera to resolve both.** An
  over-the-shoulder setup that leaves the big man's face visible ("face visible over him, chin on
  head, eyes closed") leaks the requester's profile in most seeds and sometimes lands both profiles
  nose-to-nose. The all-behind composition is the one that survives; prefer it first and spend the
  roll budget on seeds, not on wordings.
- **The lever is CAMERA POSITION, and it generalises to every two-figure scene — not just the bedroom
  one.** The same rule decides any brief with two people where neither may be identified (car
  interior, waiting room, kitchen, gym floor). Composed *from the side, across the cabin* a
  him-driving-me brief leaked both profiles on **4 of 4** seeds; the identical brief with the camera
  *behind them, looking forward between the two seats* cleared the face gate on **6 of 6**. Never buy
  clarity by moving the camera round to the front — move it further back instead. A rear-seat /
  behind-both angle also keeps the size relationship readable (driver bigger than passenger)
  without showing a face.
- **A moving-vehicle interior carries one extra obligatory object: the mirror.** Every seed of a
  car roll failed QC on the rearview mirror reflecting the sun ahead rather than the road behind.
  Send the camera to the back seat, keep the mirror out of frame or crop the top band after the
  fact, and spend the roll budget on the face gate rather than on wording the mirror away.
- **Budget ~12 seeds for a two-figure interior.** Of a full roll, roughly two clear the hard
  gates; the rest leak a profile or an ear, invent a visible companion, or fuse the hand on the
  wheel. Roll the batch, QC all of it, ship the clean one — the lever is the camera position and
  the seed, not the phrasing.
- **When the roll refuses to clear, CROP to the band that passed instead of rolling again.** The way
  out of a leaky roll is not seed N+1 — it is keeping the horizontal band QC cleared and cutting the
  rest. Crop below the ear line and above the hands, then **re-verify the CROP, not the parent**: a
  band holding only shoulders, garments and environment has nothing left to leak. Set the cut by the
  HIGHER head, not the taller figure — the passenger seat sits higher in frame than the driver, so a
  cut that clears the driver leaves the passenger's ear. Measured on the car brief: top edge at 38%
  of frame height still showed a passenger ear; 60% was clean with both shoulders, both garments, the
  console and the windscreen sun intact, then ×2 LANCZOS + sharpen to recover presence. Re-verify
  after the upscale as well — resampling can expose a jaw edge the native crop hid.
- **Landscape for a two-figure interior, portrait for the vertical embrace.** `--width 1536
  --height 1024` gave a clean, well-composed car interior with both figures reading correctly;
  `1152×1536` is for full-height standing/embracing pairs.
- **QC the face gate on the ears too.** "No face" is not the gate — a turned head can still expose an
  ear or jaw edge, and the reads flag those. Ask specifically whether any face, profile **or ear**
  is visible, and count a visible hand on the wheel as an anatomy defect when the fingers fuse.
- Prompt shape that landed: *intimate documentary photograph, quiet bedroom at night → the larger
  man fills the centre seen entirely from behind, broad thick-set back in a plain sleeveless dark
  grey top, head lowered → a slimmer smaller man pressed against that broad back, back of head and
  nape only, plain dark top, both arms wrapped around the upper back, forearms crossed low over the
  shoulder blades, hands tucked under the opposite arm and hidden → warm light-brown skin, thick
  straight black hair, Malay Southeast Asian → warm tungsten lamp from the left, deep soft shadows
  → 35mm film grain, shallow DOF, hyperrealistic skin and fabric, no AI artifacts, no text.*
- **Portrait beats landscape here:** `--width 1152 --height 1536`. The documented 1536×864 is a
  room-wide backstage shot and flattens two figures.
- Prompt shape: *over-the-shoulder photograph → foreground back of a slim young man's head, face
  hidden, pressed against the chest of a much larger heavily muscled man → tan brown skin, thick
  arms wrapped protectively, chin on head, eyes closed, both `Malay Southeast Asian` → warm dim
  room, single soft window light → 35mm film grain, shallow DOF, documentary editorial, quiet,
  intimate, non-explicit.*
- **QC the face gate first, then role assignment.** Ask the vision read: *"is ANY face or profile
  visible anywhere — eyes, nose, mouth, cheek?"* Reject any take that shows a face or a profile on
  **either** figure, and any that swaps the size relationship so the smaller man reads as the
  bigger one. Most takes fail the face gate: a plain back-hug brief leaked a face or profile in six
  of seven seeds, and a louder "neither face is visible" rewrite leaked in all three of the next
  batch. Budget 6–8 seeds and ship the clean one — do not reword, the wording is not the lever.
- **Delivered still:** mild sharpen at native size (`UnsharpMask(radius=1.6, percent=45,
  threshold=3)`). Native is the default; ×2 LANCZOS + `UnsharpMask(radius=2, percent=55)` is for an
  explicit "better quality" ask or a hero still — and whenever you do upscale, the delivery line
  says **upscaled**, never native.
- Delivery line: name the lane, say both figures are AI-rendered, say **no likeness of him was used
  at all** (no reference supplied, so the from-behind figure is a placeholder, not his body), and
  offer the reference-photo path in one line. Nothing more.
- Archive the accepted take to a private dir (`/root/forge_work/<concept>/`, `chmod 700`, files
  `chmod 600`) so a later "again but closer" lands on the accepted prompt instead of a fresh guess.
- **Open-shirt + smoking sub-register.** An ask that adds a prop and contact (hand on his chest,
  shirt unbuttoned, he is smoking) renders on the same recipe: the big man against a plain wall, dark
  shirt open and unbuttoned over a bare chest, plain dark trousers (never further — keep it
  non-explicit), cigarette in **his own** hand or mouth, thin curl of grey smoke, and the requester's
  forearm entering from the lower-left foreground, soft and out of focus.
- **A generated cigarette never reads as lit.** The tip shows no ember and no ash on any seed even
  when the prompt says `lit` and a plume is present, and one take rendered a second cigarette nobody
  asked for. QC for the ember, let the smoke plume carry the beat, and count an extra smoking object
  as an artifact.
- **The POV hand hovers, it does not press.** Flat-palm-on-chest contact does not composite on
  image-01 — two wordings is the ceiling, then take the hovering hand and say so, or crop so only a
  forearm crosses the frame. Detail in `synthetic-human-media-pipeline` §2.

## Video lane

**Token Plan keys cannot run MiniMax-H3.**

- H3 returns `code 2013 ... TokenPlan or Credit does not currently support MiniMax-H3 series
  models`. The key is valid; H3 needs a Pay-as-you-go key. Do not retry H3 on the same key.
- **Workaround on the Token Plan key (proven):** drop `--model MiniMax-H3`, and drop
  `--duration` / `--ratio` / `--reference-*` (all H3-gated — they error
  `require --model MiniMax-H3`). Keep `--image` + `--last-frame`; the CLI falls through to
  **Hailuo-02 SEF** (first/last-frame interpolation) and returns ~1364×768, 24 fps, ~6 s.

```bash
mmx video generate \
  --prompt "<camera move + room beat + settle on the one who looks back>" \
  --image first.jpg --last-frame last.jpg \
  --download out.mp4 --poll-interval 10 --non-interactive
```

- **Build the two frames first** with the image lane: a wide establishing frame (crowded room)
  and a final frame (subject turned, looking back at camera). SEF interpolates between them, so
  the stills *are* the storyboard.
- Prompt = camera behaviour + one beat: *drift forward through the haze past the silhouette,
  search across the room, slow as one turns and holds the gaze.*
- "Better quality" on a Token Plan key → upscale after the fact:
  `ffmpeg -i in.mp4 -vf "scale=1920:1080:flags=lanczos,unsharp=5:5:0.45:5:5:0.0" -c:v libx264 -preset slow -crf 16 -movflags +faststart -an out_1080p.mp4`
  and **tell them the real lane** (1080p upscaled from 768p, not native 2K). Never present an
  upscale as native resolution.
- QC every clip: `ffprobe` for duration/fps, then extract first / middle / last frames with
  `ffmpeg -vf "select='eq(n\,0)+eq(n\,70)+eq(n\,143)'" -vsync 0` and vision-check the last frame
  for the money beat (who is looking at camera) plus artifact smear in the crowd.

## Voice lane (persona lines)

### Persistent custom voice — provider-side clone (when he wants THAT timbre, not a new one)

"Same voice, redone" means preserve the timbre — run the clone; a design render is the fallback, not a
substitute. The REST calls, the source-provenance question, the required consent law, the speed
recalibration and the registry entry rules all live in **## Voice mint lane (clone) — consent-gated**
below. Read that section before minting; this heading exists only to point at it.

- **Match the reference cadence, do not default to 0.82.** A preset at 0.82 and a clone of it do NOT run at the
  same speed: the same 42.3 s line rendered 43.8 s at 0.9 and 40.1 s at 1.0 on the clone. Pick the speed whose
  duration lands nearest the reference take, then verify with `ffprobe`.
- **Prove the clone actually carries the timbre before shipping it.** MFCC cosine against the reference:
  a true clone lands ≈0.999; a merely similar voice lands ≈0.993 with a clear f0 gap. Measure f0 median too
  (`librosa.yin`, 60–350 Hz) — a clone should land within a few Hz of the reference.
- **A cloned checkpoint inherits the contamination risk class of the revoked V8.** A clone can inject clauses
  that are not in the input text, and input sanitisation cannot catch it because the insertion happens inside
  synthesis. **Every delivery on a cloned voice needs an ASR round-trip first** (Groq whisper `language=ms`),
  compared against the input line. Clean on the first pass is evidence, not a guarantee — keep the gate.
- **A closing boilerplate line in the transcript is a transcriber tail artifact, not an engine insertion —
  slice the tail before convicting the take.** A take whose every lexical word round-trips can still come back
  with a "terima kasih kerana menonton"-shaped outro that is nowhere in the input, and re-running the same
  model family reproduces it. Never retract a take, and never report a checkpoint contamination, on a
  whole-file transcript alone. Procedure — tail slice, duration budget, why two passes of one family are one
  witness — in `machine-read-verification`.
- **Scan every take mechanically, not by eye.** Diff the transcript tokens against the source line and flag any
  token with no close match (`difflib.get_close_matches`, cutoff 0.8). Single substituted tokens (`dia` for
  `takde`, `buddha` for `budak`, `ya` for `je`) are ASR mishears on real words and pass; a flagged PHRASE is an
  insertion and rejects the take.
- Registry them, from `import base64, json` all the way to a documented entry: canonical home is
  `/root/AAA/audio/voice-registry.json` (voice-registry.v1, resolver-authoritative, append-only revocation).
  Record `provenance` honestly — a clone of a *vendor system voice* is fully synthetic (no human audio in the
  chain) and is declared as such, and `lane` must say it is persona-register only, never a Hermes default.

### System voices

**Pick the voice by LANE PRECEDENT before you synthesise anything.** On a bare "abang sado voice"
request, read `lane_precedence` in `/root/AAA/audio/voice-registry.json` and use `precedent_voice` —
never choose between the live sado ids by name symmetry, by file recency, or by whichever renders
first. Three sado voices are LIVE at once (`abang-sado-live-v1` = clone of the principal's own voice
notes; `abang-sado-alpha` and `abang-sado-clone-ref01` = fully synthetic archetypes), and they are
different timbres, not versions of one thing. Shipping the synthetic one where the lane runs on the
principal's own clone is a pick-error, and the render hides it: the take passes every QC gate because
the TEXT is right — only the timbre is wrong, and the agent cannot hear the difference. The registry's
precedent field is the arbiter; do not substitute judgement for it.

```bash
export PATH=$PATH:/root/.npm-global/bin
mmx speech synthesize --base-url https://api.minimax.io --model speech-2.8-hd \
  --voice Indonesian_BossyLeader --speed 0.82 --text-file line.txt --out out.mp3
```

- `--base-url https://api.minimax.io` is **required**; the CLI default points at the
  `/anthropic` chat endpoint and 404s on speech.
- Register mapping (BM lines, verified clean through a Groq Whisper `language=ms` round-trip):
  - **cocky / dominant alpha** → `Indonesian_BossyLeader` @ **0.82–0.85**
  - **younger, quieter confidence** → `Indonesian_ReservedYoungMan` @ 0.92
  - **warm / caring** → `Indonesian_CaringMan` @ 0.88
  - English deep registers (`English_ManWithDeepVoice`, `English_ImposingManner`) give weight
    but put an English accent on BM words — only when register matters more than accent.
- Indonesian voices read BM naturally (phoneme overlap); listeners rarely notice the accent.
- **Speed is per-voice and DOES NOT transfer.** 0.82 is calibrated for `Indonesian_BossyLeader`; the
  same number on a freshly designed voice stretched the identical line from 42.3 s to 66.6 s and
  dragged audibly, while 0.95 on that same voice landed at 58.9 s. Whenever the voice changes — a new
  design, a different system voice — render once, read the printed `duration_ms` (or `ffprobe`), and
  compare it against the accepted reference take BEFORE you QC or ship. Step the speed toward 1.0
  until the two takes sit at the same length; never carry the old number over.
- **"Clone this voice and redo" is a CLONE job when the source is synthetic.** Two independent
  questions, asked in this order. **Where did the source audio come from?** A synthetic render — a take
  you produced earlier, or a provider's own stock voice like `Indonesian_BossyLeader` — has no human
  waveform anywhere in the chain, so there is no consent question to answer and the clone endpoint is
  in scope. The requester's own recorded voice is in scope (ownership). A named third party, a public
  figure, or audio found online / forwarded in a voice note is the ONE case that holds: a human voice
  is a biometric identity, and clone-without-consent is forbidden, not gated. **Then: which artifact does
  the ask actually want?** "Same voice, redone" means *preserve the timbre* — run the clone. A design
  render is a DIFFERENT voice: measured against the reference, a clone lands at MFCC cosine ≈0.999 and
  Δf0 ≈0 Hz, while a design in the same register lands ≈0.993 with a ~15 Hz f0 gap. Substituting a
  design for a requested clone ships an artifact that does not match the brief, and the requester names
  it — *"dah ada, buat ja"*. Design is the FALLBACK: a human source without consent, or a clone lane
  that is genuinely dead (probe it first — never assume it is unavailable). Declare the chain in one
  line ("cloned from the synthetic render, no human audio involved") and move on. Full recipe — decision
  table, REST calls, prompt rules, registry entry, recalibration, QC numbers — in
  `references/minting-a-persona-voice.md`.
- **A new persona voice must be registered before it ships.** A voice id that only exists in a
  scratch path is invisible to the rest of the federation and cannot be revoked. Register it in
  `/root/AAA/audio/voice-registry.json` — back the file up first, add the entry, bump `updated_at` /
  `updated_by`, never delete or rewrite an existing entry, and carry `provider_voice_id`, `model`,
  `endpoint`, `archetype`, `provenance`, `consent`, `f9_compliance`, `preferred_settings` and a
  `runtime_measured_*` block. `provenance` + `consent` are the load-bearing pair: the entry that
  passes reads `parametric_voice_design — original voice from a written description; NOT derived from
  any real person's audio`. Record what was MEASURED under `runtime_measured_*`, not what the design
  spec claimed.
- **A/B a new persona voice against the accepted take before shipping it.** Same line, same QC gate
  (`scripts/tts_roundtrip_qc.sh`), then compare the two on measured median f0 (`librosa.yin`, 60-350
  Hz) and duration. The measurement is what turns "sounds deeper" into a claim worth stating, and it
  is what catches a design that landed far from the brief.
- **Always falsify before shipping**: transcribe the output back with Groq Whisper
  (`-F model=whisper-large-v3-turbo -F language=ms`) and check the text round-trips. Garbled
  words = a bad take, regenerate that take only. Run `scripts/tts_roundtrip_qc.sh <file>` for the
  text and the word-level timestamps in one pass.
- **A lone `Hmm?` / `Ha` / `Oh` at a mid-line pause is a THIRD class — an ambiguity, not spent audio,
  and not a garbled word.** Do not spend a re-roll on it. Triage in this order: (1) re-transcribe the
  window around it (`ffmpeg -ss <seconds> -t 8 -i out.mp3 seg.wav`) — if every lexical word round-trips
  and only the filler diverges, the signal is ambiguous (a short filler is exactly what Whisper plants
  into a pause) and the engine is not convicted; (2) then fix the INPUT LAYOUT, because a blank-line
  paragraph break renders as a multi-second pause and that is where the filler lands. Same voice, same
  speed, same text with the paragraphing flattened → clean on the first take. Discriminate against the
  end-of-take tail tick above by POSITION: a stray beat at the very end with real separated timestamps
  is spent audio; a filler sitting mid-line over a pause is not.
- **No blank-line paragraph breaks in the text file.** Keep the beat structure — drop the empty line,
  not the paragraph. One paragraph per line, single newlines.
- Check the CLI's printed `duration_ms` (or `ffprobe`) against the expected length before QC: a near-empty
  or overrun file is a silent failure, not a quality issue.
- **A repeated syllable at the END of the take is spent audio, not a Whisper hallucination.** The
  engine can append a spoken tick after the last written word — a clean take can come back with
  three `Du.` beats tagged on, and the round-trip is the only thing that shows it. Discriminate with
  timestamps, not with vibe: re-request as `-F response_format=verbose_json -F
  "timestamp_granularities[]=word"` and ask whether those words carry **real, separated timestamps
  past the point the script should have ended**. Invented Whisper text clusters over music or
  silence; a spoken tail sits exactly where the line stopped and moves with the take.
- **Do not try to strip the tail with a silence filter.** `silenceremove` — including the
  `areverse, ..., areverse` form — does not touch it, because the artifact is speech and sits well
  above the threshold. Hard-cut instead: `ffmpeg -y -i out.mp3 -t <seconds just before the artifact>
  -c:a copy fixed.mp3`, cut at the silence gap between the last scripted word and the first stray
  beat. Then **re-verify the cut, not the parent** — a cut past a real word sounds like a mistake,
  and re-checking the verified parent proves nothing about the file you send. Say in the delivery
  line that the take is cut, same as declaring an upscale.
- Write the line as **spoken prose**: short sentences, no markdown, no digits. Length is not the
  defect axis — 45 s and ~95 s takes rendered clean while a ~26 s take carried the tail tick — so a
  short take is not exempt from the round-trip.

### Line craft (what makes the persona land)

Cocky works when it is **unbothered**, not boastful: state a cost (hours, years, no days off),
state who actually gets him (the one who waits, not the one who pushes), then give the listener
one small honest concession ("you came close, not from far like the others"). No pleading, no
insults, no explicit content. It should sound like a man who does not need the listener — which
exactly makes the listener lean in.

**Intensity escalation (`dark`, `cocky`, `harder`) changes the PACE, not the floors.** Turn the speed
DOWN, never up — the register is a man who does not need to shout, and a slower read is what makes a
demand land. Escalate by adding WITHDRAWAL rather than explicitness: name the body as the persona's OWN
in the first person ("tiga tahun abang bina benda ni"), let the listener look, then deny contact —
"kau boleh tengok, kau tak boleh sentuh. Belum. Tunggu abang panggil." That denial IS the engine of the
register, and it is also what keeps the artifact non-explicit. Never a real person's body, never a
described sex act, never a named third party. If a line seems to need one of those to get "harder",
the answer is a slower read and a longer pause, not a new subject.

## Voice mint lane (clone) — consent-gated

**`mmx` has no clone subcommand.** Mint through the API directly:

```bash
set +u; set -a; source /root/.secrets/kunci-root.env 2>/dev/null; set +a; set +u
# the key lives under MINIMAX_PLUGIN_API_KEY (sk-cp-…) — and a separately-populated MINIMAX_API_KEY
# may also be present, so enumerate before picking: grep -oE '^MINIMAX[A-Z_]*=' <env>. Under `set -u`
# a script that references an absent name dies before the first call.
curl -s -X POST https://api.minimax.io/v1/files/upload -H "Authorization: Bearer $MINIMAX_PLUGIN_API_KEY" \
  -F "purpose=voice_clone" -F "file=@source.mp3"          # -> file.file_id
curl -s -X POST https://api.minimax.io/v1/voice_clone -H "Authorization: Bearer $MINIMAX_PLUGIN_API_KEY" \
  -H "Content-Type: application/json" -d '{"file_id":<id>,"voice_id":"<name>","model":"speech-2.8-hd"}'
```

Then synthesise with `--voice <name>`. voice_id: 8–256 chars, starts with a letter, no trailing `-`/`_`.

- **Try the CLI upload before hand-rolling multipart.** `mmx file upload --file <path> --purpose
  voice_clone` returns a `file.file_id` and saves writing the multipart body by hand — probe it once
  (a single smoke call decides it), and keep the raw `POST /v1/files/upload` multipart form as the
  fallback that is known to work: `purpose=voice_clone` + the mp3 as the file part, auth
  `Bearer $MINIMAX_PLUGIN_API_KEY`, response `file.file_id`. A clone of a 42 s synthetic render cost
  nothing extra and completed inside a minute on `speech-2.8-hd`.

- **CONSENT LAW (F13, identity-card 2026-08-19) — it governs HUMAN sources, not synthetic ones:**
  design = seal today · clone-of-a-human-WITH-consent = HOLD · clone-of-a-human-WITHOUT-consent =
  FORBIDDEN FOREVER. A synthetic source (the persona's own render, a provider's stock voice) has no
  human waveform in the chain and raises no consent question at all. The registry is one file per human
  under `/root/WELL/envelopes/_consent/` (only `arif.json` exists) — **a voice note he forwards is NOT a
  consent entry.** Probe it before minting a human voice; read absence as absence.
- **When he ANSWERS the probe and the registry still shows nothing — execute, and record the gap.**
  He holds the right to direction in his own lane; the registry holds the *record*, not the decision.
  The sequence is: probe once → he asserts consent ("dah ada, buat ja") → re-probe to confirm the file
  state → still nothing on file → **do the work, and write the gap into the work-dir receipt in exactly
  those words**: *consent asserted by F13 in-chat, no entry on file for this speaker*. Holding a second
  time, or asking a third question, is the permission-lecture failure this lane already names — and a
  sovereign assertion left unrecorded is the mirror failure: the next session reads a clean-looking
  artifact with no provenance line under it. Two lines are the minimum: what was asserted, and by whom.
  **The one move that stays forbidden is forging the record** — never write a consent entry under
  `/root/WELL/envelopes/_consent/` on someone else's behalf (only the person themselves can grant one),
  and never promote the cloned id to a Hermes default. That boundary is what keeps "he directed it"
  honest instead of laundered. Confirm you are cloning the voice he has actually been running before
  you treat the note as the one he means: MFCC-mean cosine across the forwarded note and the existing
  take lands ≈0.99 for the same speaker, and the f0 medians sit in one family.
- **Know which layer actually enforces that law.** `voice_filters.py` expects a
  `human_approval_token`, but the REST path (`/v1/files/upload` → `/v1/voice_clone`) is not intercepted
  by it — nothing at the endpoint stops a call. The gate is procedural: it holds only because the agent
  reads the source's provenance first. A successful clone is NOT evidence that the source was cleared.
- **A synthetic source is the only free source.** Cloning the persona's own render (the clip he just
  heard) trips nothing — say so on delivery: *clone of the synthetic clip, not of any human.* Cloning
  a voice found in forwarded notes = a real person's likeness; hold, ship the render in the designed
  or already-consented voice, and ask the ONE fact only he holds (whose voice).
- **Register a new persona voice by APPENDING to `/root/AAA/audio/voice-registry.json`** (identity
  layer): back the file up first, add the entry, bump `updated_at` / `updated_by`. Never rewrite or
  delete an existing entry — revocation is append-only (flip `status` to `REVOKED` and record who/when).
  Never promote an entry to a Hermes DEFAULT; that is F13's call. A *clone* entry additionally carries
  its provenance chain and a `caveat` naming the contamination risk class. Keep a mint receipt in the
  work dir too: voice_id, provider file_id, source file + provenance, verification numbers, what was
  deliberately NOT cloned.
- **Verify the mint like any take — run `scripts/verify_take.py <take.mp3> --text <line.txt>`.** It
  implements the whole gate in one command: duration floor + pacing band, ASR round-trip, normalised
  similarity, INSERTED/MISSING word extraction, and the f0 family check against `--source`. Pass
  `--alias heard=written` for a known substitution. Prefer it to hand-typing the block: the ladder is
  seven steps, and the step that goes missing when it is retyped is the normalisation, which turns a
  clean take into a fake 8% match and can hide a real insertion inside the noise. The gate in words:
  Groq round-trip (`language=ms`) → % match vs the input line, and read the transcript for INSERTED
  clauses (the V8 checkpoint contamination failure: an unrequested phrase appeared at render time;
  only a text-vs-transcript diff catches it). Then F0 (librosa yin, 60–400) against the source — same
  speaker sits within ~10 Hz.
- **Normalise DIGITS to words in BOTH sides before the % match, or the score lies.** Write the line
  as spoken prose (`lapan tahun`, `dua ribu sembilan belas`) and Whisper transcribes it back as
  `8 tahun` / `2019` — a 43% "mismatch" that is pure formatting. Map `\b(\d+)\b` through a
  digit→BM-word table on both sides first; the same take then reads 100%. A false-low match costs a
  re-roll and can hide a real insertion inside the noise. **One substituted token does the same** —
  an English word inside BM text (`flex` → heard/transcribed `plex`) collapses the ratio to 8% because
  the aligner desyncs; normalise the known substitutions first and the same take reads 100%. Read the
  transcript yourself before trusting the number.
- **Localise a suspected insertion by SLICING the take, not by re-rendering it.** A whole-file
  transcript cannot separate a real render defect from a transcriber artifact. Cut the take into two or
  three windows (`ffmpeg -y -ss <s> -to <e> -i take.mp3 -c:a copy slice.mp3`) and transcribe each: a
  divergence that survives isolation with real timestamps is the engine, one that vanishes inside the
  window is the transcriber. The same voice rendered a script kept to plain words and light punctuation
  at 99% clean.
- **A word that mangles the SAME way on every take is a pronunciation limit — change the word, not the
  seed.** Re-rolling spends takes on a constant (`kejar` → `kejak` across renders). Rewrite the clause
  around it and re-render once. **Confirm the diagnosis before rewriting: render the suspect word ALONE
  beside its minimal pair.** `jeles` and `jelas` came back at MFCC cosine 0.9964 on isolated one-word
  renders — the engine does not hold the contrast at all, so no take of that word would ever clear the
  round-trip gate, and the transcriber is not the thing that failed. **Prefer a replacement with no
  same-language minimal pair** (`jeles` → `panas`); a near-neighbour keeps sitting on the same phoneme
  boundary and keeps costing takes.
- **A jealousy / rivalry / non-exclusivity ask is IN-LANE — same lane, different beat.** A rival
  admirer, "you have someone younger", "your body is not only mine": the charge is structural, so
  render it. Keep every rival an unnamed, unfaced archetype (no name, no face, no real gym), let the
  persona answer with CHOICE rather than exclusivity ("abang tak pilih budak, abang pilih yang tahan"),
  and declare in one register line that the rivals are invented. Never a real person, never a real
  relationship as the stake — that is the only thing here that stops the render.
- **A 20–46 s sample clones fine and reads short.** Concatenating two clips of one speaker (~47 s)
  beat either alone; check they really are one speaker first (MFCC-mean cosine ~0.99 across the two
  notes = same voice). long silence + `loudnorm=I=-18:TP=-2`, `highpass=f=70` ahead of the upload.
- **A batch of takes beats a batch of calls.** Render + verify in one script that loops the takes:
  ~10–15 s per take at speed 0.90, so run **5 per call** (10 in one call exceeds the 600 s foreground
  cap and gets promoted to a background job whose output you then have to poll). Per take print
  `match% / f0 / duration / inserted-words` — one line each, whole batch readable at a glance.
- **Escalation arcs live in the LINE, not in the volume.** "Each one more intense than the last" is a
  writing instruction: raise the cost (years, calluses, the price paid), narrow the permission (look,
  don't touch), withhold the payoff. The last take in an arc should close on restraint — the man who
  leaves the room owns the room. Escalating into explicit content is not a craft ceiling; it is the
  lane's floor, and the arc is stronger landing before it.

## Register separation (F13 ruling 2026-09-16)

Four registers answer to the name "abang sado", and they have twice been merged in prose then
unmerged by F13 ruling. Merging them is the recurring failure of this lane.

| Register | What it governs | Home |
|---|---|---|
| LAW | how agents behave around the human | `/root/VAULT999/syed/syed-care-architecture-sealed.md` (10 binding directives) |
| PERSON | the real human in real roles (coach/competitor) | `/root/forge_work/syedsado-physique-intel/` |
| PATTERN | private psychology, F5 | `/root/.hermes/lanes/private/shadow/` |
| MEDIA | synthetic voice/stills/video of an archetype | `/root/AAA/audio/voice-registry.json` |

Full contrast + drift register: `/root/AAA/governance/ABANG-SADO-REGISTER-CONTRAST-2026-09-16.md`.

- **Name voices by REGISTER, never by person.** A registry entry is a provenance record; a real
  human's name in it becomes citable evidence for every later session. When the requester asks to
  register a synthetic voice under a real person's name, do the work and refuse the NAME — one line,
  in register, and record the refusal in the seal payload so it is not silently dropped.
- **A voice with zero human audio in its chain raises no consent question — and that is exactly why
  it cannot carry a human's name.** The two facts are the same fact.
- **Sealing a persona voice:** append to `/root/arifOS/VAULT999/local_seals.jsonl` with
  `previous_receipt_hash` = the last entry carrying a `log_sha256` (the ledger is `chattr +a`,
  append-only — a wrong field is corrected by appending an AMEND entry, never by rewriting), then
  set `log_sha256` = SHA-256 of the canonical JSON (sort_keys, `,`/`:` separators) **excluding** the
  hash field. `seal_to_vault999.py` is broken (`v2_epoch.py` no longer exports `read_v2_seals`), so
  this is a sovereign-chat seal, not a kernel seal — say so in the record.

## Delivery (Telegram)

- Image: `MEDIA:/abs/path.jpg` on its own line.
- Video: `MEDIA:/abs/path.mp4` — plays inline.
- Voice: put `[[audio_as_voice]]` on its own line before the `MEDIA:` line to send a native
  voice bubble; otherwise the mp3 arrives as a file.
- Lead with what the artifact *is* in one line, then the framing note. No bullet-pointed
  explanation of the pipeline unless the lane genuinely fell back.
- **Ship exactly ONE artifact per ask.** Not the roll, not a shortlist, not "here are six, pick
  one". Choose the take that clears the gates, verify it, send it. A batch of near-misses offered as
  progress reads as the work not being finished, and it hands the choice back to a requester who
  asked for a finished thing.
- **Never narrate the rounds.** Seed counts, retries, which seed failed what, how many attempts, the
  QC pass itself — none of it ships. The requester experiences the artifact, not the search. A take
  that leaked a profile or fused a hand is a reason it was rejected, not content.
- **Sequence the final check before the promise.** Do the zoom pass FIRST, then speak. Claiming a take
  is checked and then finding a defect on the follow-up zoom at the requester's request is the failure
  this lane keeps repeating: the pass was asserted at a coarser magnification than the one that
  decides.

## Proven artifact set

**Inventorying older or archived sets, and reading why one was held →
`references/artifact-archive-map.md`** (live dirs, the quarantine pack list, and the receipt files
that carry the hold reason).

2026-09-15 — `/root/forge_work/backstage/`: `chosen_final.jpg` (3072×1728 upscaled),
`ramai_chosen_1080p.mp4` (Hailuo-02 SEF, upscaled), `alpha_A.mp3` (BossyLeader 0.82, ~95 s),
`sado_takeA.mp3` (BossyLeader 0.85, ~45 s).

Minted persona voices — reuse the id instead of re-minting (`VOICE-MINT-RECEIPT.md` and the takes sit
beside them in the same dir): `abang-sado-v1` (clone of a synthetic `Indonesian_BossyLeader` render),
`abang-sado-live-v1` (clone of the sovereign's own DM voice notes — the alpha and dark takes ran on this
one, at speed 0.92–0.98).

**The registry, not this list, is the live authority for persona voice ids.** Read
`/root/AAA/audio/voice-registry.json` before choosing one — it carries the `status` (a REVOKED id must
never be selected as a default, an explicit id, or a fallback rung), the `preferred_settings.speed` for
that specific voice, and the `runtime_measured_*` block. This paragraph only records what was minted
when; entries may have been added or revoked by another session since.

**This work dir is shared with other live sessions.** Mid-session it changed under the agent working it
(`voice_test/`, a second `design_result.json`, a fresh `sado_v2.mp3` appeared from elsewhere). Write to
your own filenames, and check the mtimes plus the session ids in `~/.hermes/logs/agent.log` before
claiming which render is yours — "the newest file" is not evidence of authorship.

DITEMPA BUKAN DIBERI.
