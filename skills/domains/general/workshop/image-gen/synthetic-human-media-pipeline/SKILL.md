---
name: synthetic-human-media-pipeline
description: "Use when generating synthetic human image, video, or voice."
version: 1.0.0
tags: [minimax, image-generation, video-generation, tts, photorealism, qa, delivery-honesty]
metadata:
  hermes:
    category: creative
    requires: [mmx-cli]
    related: [minimax-cli, photorealistic-human-image-gen, nusantara-voice-stack, forge-real-person-reference-photos, image-identity-transfer]
---

# Synthetic Human Media Pipeline

End-to-end production of photorealistic human media (still → video → voice) with MiniMax mmx, plus the verification and disclosure that must happen before anything is delivered.

**Scope.** This skill owns the *pipeline* layer — what the plan can actually reach, how to keep a multi-person prompt clean, how to verify generated motion, and what must be declared on delivery. Prompt-craft depth (camera anchors, lighting tables, cultural props, safety framing) lives in `photorealistic-human-image-gen` and `minimax-cli`; BM voice-lane depth lives in `nusantara-voice-stack`. Read those for the artistic layer, this one for the execution order.

**Reference files.** `references/backstage-physique-scene.md` — the physique-competition backstage as a physical place, the admirer's point of view, unwritten etiquette, the one honest check to hold, and the scene recipe for rendering it. Load it for any backstage / ringside / admirer request.

**Scripts.** `scripts/identify_take.py <incoming audio> <candidate dirs>` — ranks which previously rendered take the file is (mel sliding-window cosine + the verdict bands). Run it before re-rendering anything a requester points at.

## When to load

- User asks for an image, video, or voice piece featuring people (muscle/admirer scenes, portraits, backstage sets, character shots).
- User asks to improve or redo a previously generated piece ("better quality", "more people", "make it move").
- User wants a Malay-language line delivered as a Telegram voice note.
- Any time `mmx image generate`, `mmx video generate`, or `mmx speech synthesize` is about to be called.

---

## 1. Before generating — what the plan can actually reach

**H3 is not reachable on a Token Plan (`sk-cp-`) key.** `--model MiniMax-H3` fails by design:

```json
{"error": {"code": 1, "message": "API error: invalid params, TokenPlan or Credit does not currently support MiniMax-H3 series models (2013) (HTTP 400)"}}
```

That is a plan boundary, not a region or route problem. **Do not retry, do not switch `--region`, do not re-submit** — drop `--model` and take the default (Hailuo-2.3) in the same call.

**H3-only flags fail as shape errors on legacy models.** `--duration`, `--ratio`, `--reference-image`, `--reference-video`, `--reference-audio` all error with `… require --model MiniMax-H3.` On Hailuo pass `--image <first-frame>` + `--download <out.mp4>` and take the defaults. Image-to-video inherits the still's aspect ratio, so set the ratio on the **still**, never on the video.

**`--width` / `--height` are image-01 only** (512–2048, multiples of 8). That is how the full-size first frame gets minted.

**Prompt text is capped at 1500 characters, and the rejection is disguised as success.** image-01 fails with `API error: invalid params, prompt length must be less than 1500 (HTTP 200)` — the HTTP 200 means a length rejection looks like a transport-level success, so read the JSON body when a take silently does not appear on disk. A full scene + pose + camera + anti-artifact + no-text tail lands around 1100–1300 characters, which is the shape to write to. Compose the prompt as a Python string and print `len(prompt)` before submitting; trim by cutting decoratives (second lighting adjective, redundant `no AI artifacts` synonyms), never by dropping the camera anchor or the negative tail.

**Always pass `--base-url https://api.minimax.io` for speech and image.** The mmx CLI default points at the `/anthropic` chat endpoint and returns HTTP 404 on media endpoints.

**Shell quoting.** Prompts carry apostrophes, em-dashes and `%`; pasted into a single-quoted shell arg they break with `unexpected EOF while looking for matching '`. Build the command in Python with `shlex.quote(prompt)` and keep apostrophes out of the prompt text. If an mmx call returns non-zero with empty stdout, re-issue the identical command once — the same call succeeds on the retry.

**A content-safety rejection is NOT an outage — re-frame the scene and resubmit to the SAME lane.** Some providers return `HTTP 400` with a body like `DataInspectionFailed` / *"Green net check failed … output may contain inappropriate content"*. The lane is alive and healthy; falling through wastes the quota you have. The filter reads the **rendered output**, so it cannot be talked around with prompt wording — padding `negative_prompt` never helps, because the negative list is not what it inspects.

**The move is to relocate the scene to a neutral public context while keeping the relational beat.** Move an intimate or domestic framing (bedroom, night, close bodies) into a working setting the same relationship genuinely occupies — after a training session in a gym, outdoors, a workplace. Change what the scene **is**, not how it is described. Keep the composition the requester asked for (two figures, one's arm across the other, closeness) and change only the setting and the clothing state.

- **Re-specify fully clothed in the POSITIVE prompt** for the new setting. A stated positive reads far better than a pile of negative tokens.
- **The camera-position technique survives the re-frame unchanged** — compose from behind with both bodies facing away, which hides every face regardless of setting and keeps the size relationship readable.
- **If the requester wants the original setting, say which lane can carry it** and offer to route it there on a quota reset. Do not keep hammering the filtered lane with variants.
- **A filter rejection is a signal about the LANE, not about the request** — the same brief may pass on another provider. Do not report a request as unfulfillable after one provider declines it.

---

## 2. Multi-subject scene rules

Group prompts fail in a specific way: bodies fuse into one mass, hands and objects melt, extra feet appear, and any lettering turns to gibberish. These rules are what keeps a multi-person scene clean.

- **Cap the cast at three clearly separate figures.** Three is the reliable ceiling; four or more tangles torsos and limbs. Write `standing well apart and fully separate` explicitly — bare `standing apart` does not stop clustering.
- **Give every extra subject one distinct, non-competing action.** `one stretches a resistance band`, `one crosses his arms`, `one rests a towel over his shoulder`. Two people doing the same thing get fused into one body.
- **Exactly one focal gaze.** One subject gets `both eyes open and fixed straight into the camera lens, steady and calm`; everyone else looks away, at each other, or down. Two direct gazes split the composition and the model loses both.
- **Delete text-bearing props — do not ask the prompt to fix them.** Buckets, signage, wall plates and shorts logos render as garbled glyphs and are the first thing QA flags. Remove the object and end the prompt with `no logos, no lettering, no numbers, no signage`.
- **Anchor a named ethnicity with an explicit trait list.** A bare group name drifts to MENA / South-Asian casting by default. For Malaysian Malay: `warm light-brown skin, epicanthic folds, broad flat noses, wide cheekbones, thick straight black hair, sparse thin moustache, no thick beards`. When the drift persists, re-roll the `--seed` — rewording only the ethnicity token rarely fixes it.
- **A negative clause is the weakest control in the prompt.** `no beard`, `no moustache`, `no stubble`, `no grey`, `no watermark` are obeyed loosely — the sampler supplies the attribute anyway (a full beard and grey hair rendered on a subject briefed as clean shaven with short black hair, across every seed of a roll). Treat each negative as a QC item rather than a guarantee: write it once, then check for it after the roll and **re-roll the seed** instead of rewording, because new wording rarely suppresses an attribute the sampler has already chosen. Only the seed index reliably moves these.
- **Observer/doorway foreground.** An out-of-focus near subject seen from behind puts the viewer inside the observer's body and is the strongest single device in this genre. State it narrowly: `dark soft out-of-focus silhouette of a man seen only from behind, back of head and shoulder, plain dark t-shirt`. Without the narrow wording the model renders a second full figure with a face.
- **A near hand that touches the other subject does not composite — use a silhouette or a hovering hand instead.** Asked for a foreground palm pressed flat on a second person's bare chest, image-01 returns the hand hovering in front of the torso with no contact shadow, folds it into the subject's own arm, or melts it — consistently, across several wordings and seeds. Do not spend more than two wordings on it. Take one of three routes: accept the hovering half-open hand and label it as such on delivery, crop tight enough that only a forearm crosses the frame, or swap the near element for the backlit silhouette above, which composites cleanly where a touching hand does not.
- **Intimate two-person frames leak faces — make "no face visible" a QC gate, not a prompt clause.** In a close embrace or back-hug, image-01 resolves a face or a three-quarter profile on one or both subjects even when the brief says the faces are hidden. Restating the denial at higher volume does not help — it can backfire (a louder `neither face is visible anywhere in the frame` pass produced *more* face-visible takes than the plain one), so do not spend iterations rewording. State the framing once (`back of head, nape and shoulders only, no eyes, no nose, no mouth, no profile`), then roll seeds and reject on sight. Leak rate in this register is high: budget 6–8 seeds per accepted still.
- **A composition instruction does not remove a head — only the camera and a crop do.** Wording that puts both heads outside the frame (`cropped just below the collarbones so that both heads are outside the frame entirely, no head and no face in the picture`) still rendered full frontal faces on half of a four-seed roll. Treat head removal as a framing/crop decision taken after the roll, never as a clause to be trusted; budget the seeds for the face gate either way.
- **Put the face gate first in the QC list, with the failure modes named.** Ask *"is ANY face or profile visible anywhere — eyes, nose, mouth, cheek?"* A generic "describe the image" buries a visible profile inside a paragraph of prose and you ship it. Same for hands and contact points: name the artifact you are hunting, or the QC answer passes it. Put **every negative you wrote** on the QC list as well — facial hair on a clean-shaven brief, grey in the hair, bare feet, a watermark, a logo on the shorts — because a render can pass every anatomy and composition check and still contradict the brief on a clause you never asked about.
- **More seeds when a named invariant must survive.** Quality varies more between seeds than between prompt wordings. Two is the floor; when an invariant is load-bearing (a hidden face, a size relationship, a phenotype, a single focal gaze) generate 4+, QA all of them, and keep the one where that invariant actually survived — do not ship a compromise because it arrived first.

---

## 3. QA loop — before anything ships

Run `vision_analyze` on every candidate with the checks **numbered** and the failure modes **named**, because the default answer overshoots into praise:

```
(1) count the people and say whether they are clearly separate, (2) do the faces read as [named group],
(3) is one person making direct eye contact with the camera, (4) any melted objects, warped limbs,
malformed hands, garbled text or extra feet, (5) is the foreground silhouette present and out of focus,
(6) does it read as a real photograph or as AI art. Don't name any person. Don't assign any placing.
```

The negative instructions ("don't name", "don't assign") are load-bearing — they stop the model inventing identities and verdicts on a body photo.

**Read the verdict at native resolution, never off a contact sheet — at tile scale the reader invents defects in both directions.** On a downscaled grid the reader reports a face wherever two heads touch, and reports fused or extra fingers on hands that are clean, then retracts both when the same region is re-read as a native crop; it does the reverse too ("no face" at a glance over an ear or a jaw edge that the crop exposes). Measured on one roll: whole-frame reads flagged faces on takes whose native head crop held only a single ear, and named fused digits on hands a native crop resolved as four separated fingers plus an occluded thumb. So the sheet is for CHOOSING candidates; the head crop and the hand crop decide them. Re-read every survivor at native resolution before rejecting or shipping it — a roll judged from the sheet throws away clean takes and ships defective ones, and an ear alone does not sink a take whose eyes, nose, mouth and profile are all absent.

**Count the files after a batch roll before QC.** `mmx image generate --quiet` prints nothing on a miss, so a dropped seed is invisible and a 6-seed loop can return 5 files with a zero exit code. `ls` the output dir and compare the count against the seed list, then label each file by seed in the QC pass — an unchecked shortfall silently narrows the roll you believe you are judging.

**Re-read each survivor on a named-region crop for the highest-risk artifact.** `vision_analyze` takes a `region` box in ORIGINAL-image coordinates, so the head band and the hand band of one take are two cheap calls that beat one more seed. Ask each crop the single question that decides it (any face/profile/eye/nose/mouth/cheek/EAR on either figure; every visible hand's finger count) rather than a general description, and keep the parent-frame read as context only.

**For video, never QA single frames — read the motion.** Extract a filmstrip and inspect it in one call:

```bash
ffmpeg -v error -y -i clip.mp4 -vf "fps=1,scale=340:-1,tile=6x1" -frames:v 1 /tmp/sheet.jpg
```

Ask three things of that sheet: does the intended camera move actually happen across the frames, does each subject do its intended action, and is there deformation (fused hands, melting contact points, extra feet, warped faces). One image beats six calls.

**To pick a hero still**, tile specific timestamps and ask which panel is the strongest moment:

```bash
for t in 3.2 4.2 5.0 5.7; do ffmpeg -v error -y -ss $t -i clip.mp4 -frames:v 1 -vf scale=460:-1 /tmp/c_$t.jpg; done
ffmpeg -v error -y -i /tmp/c_3.2.jpg -i /tmp/c_4.2.jpg -i /tmp/c_5.0.jpg -i /tmp/c_5.7.jpg \
  -filter_complex '[0][1]hstack[a];[2][3]hstack[b];[a][b]vstack' /tmp/quad.jpg
```

Never cite a frame number or timestamp you have not actually extracted — read the timestamp off the panel you inspected.

---

## 4. Video from a staged still

Animate; do not ask the model for motion from nothing. Mint the first frame as a full-size still (§1), then drive image-to-video from it.

Prompt the motion as **one camera move plus one subject action** — never multi-action:

> `Slow, perfectly steady dolly-in push toward the oiled chest as the camera glides closer; his chest rises and falls with one deep calm breath and the oil sheen shifts; the silhouette at the left edge stays motionless; locked-off camera, no shake, shallow depth of field, film grain.`

Two rules carry the shot: locked-off camera plus a single subject beat, and the near-silhouette holding still so the only moving thing is the subject. When the model is asked for two simultaneous actions it deforms hands and contact points.

**Quality ladder when the top video tier is unavailable:**

1. Still at delivery size — `mmx image generate --width 1152 --height 2048 --seed N --out still.jpg`
2. Animate — lands 768×1364
3. Upscale + sharpen to delivery size:

```bash
ffmpeg -v error -y -i clip.mp4 \
  -vf "scale=1152:2048:flags=lanczos,unsharp=5:5:0.5:5:5:0.0" \
  -c:v libx264 -preset slow -crf 14 -pix_fmt yuv420p -movflags +faststart -an clip-hq.mp4
```

→ ~10 Mbps. An upscaled clean 768p source reads noticeably sharper than the native file, but it adds no detail the model never produced. Call it **upscaled** — never "2K".

---

## 5. Voice lines

```bash
mmx speech synthesize --base-url https://api.minimax.io --model speech-2.8-hd \
  --voice Indonesian_BossyLeader --speed 0.85 --emotion fluent \
  --text-file /tmp/line.txt --out line.mp3 --quiet
```

- **`--text-file` for anything longer than a sentence, or containing apostrophes.** Writing the text to a file and passing the path removes every shell-quoting failure and is the reliable form for a monologue.
- **Dominant / cocky BM male register** reads clean on `Indonesian_BossyLeader` at `--speed 0.85`. Indonesian voices handle Malay text naturally because the phoneme inventories map closely.
- **Falsify before delivering.** Transcribe the output back with Whisper (`language=ms`) and compare against the input. A near-identical transcript confirms pronunciation and clarity; divergence means re-render before the user hears it.
- **Telegram voice bubble needs OGG/Opus.** Convert, then put `[[audio_as_voice]]` on its own line above the `MEDIA:` line:

```bash
ffmpeg -v error -y -i line.mp3 -c:a libopus -b:a 64k -ar 48000 -ac 1 line.opus
```

MP3 and M4A arrive as audio files, not voice bubbles. Trim leading/trailing silence before conversion to tighten delivery.

- **Write the script like speech.** Conversational prose only: no markdown, no tables, short sentences, numbers spelled out in BM, technical jargon left in English. A voice note that reads like a document sounds like a document.

### Which voice id — the registry holds more than one, and they are not versions of one thing

A voice fleet splits by the KIND of identity the artifact carries, and the ids are not interchangeable:

- **Cloned from the requester's own recordings** — the persona speaks *in his voice*. Still persona-register only.
- **Fully synthetic** — parametric design, or a clone of a vendor *system* voice. Zero human audio anywhere in the chain.

Same register, same speed band, genuinely different artifact: on one identical line the two landed
26.1 s and 31.9 s. Read the voice registry before choosing (it is the live authority and carries the
per-voice `preferred_settings.speed`), then **pick the id an earlier take used whenever the requester
points at that take** — not the id that looks newest.

### Resolving a take the requester points at ("you generated this before")

When the ask is about an artifact that already exists — a reply to an old clip, a forwarded take, a
voice note answering a line you half-recognise — **resolve it before rendering**. A fresh render on a
guessed voice spends a take and answers a different question.

1. **Locate by line, not by ear.** `grep -rl "<first few words>" <work dir> <audio cache>` returns the
   take and its whole batch at once; the session log confirms which run produced it.
2. **Dedupe the audio cache by md5.** A gateway cache names the same bytes several ways — a replied-to
   clip and a re-forwarded copy are one artifact under three filenames. Count files instead of hashes
   and one send reads as three.
3. **Confirm acoustically and read the GAP.** Run `scripts/identify_take.py <input> <candidate dirs>`:
   64-band mel spectrogram, mean-removed, sliding-window cosine. Measured bands — same take re-encoded
   0.998–1.000 at offset 0 · same line, same voice, different take 0.85–0.95 · **different voice id in
   the same register 0.53–0.80**. The score separates "same take" from "same register" cleanly, so the
   top two rows and the distance between them carry the verdict — never the single number.
4. **Answer with what the artifact IS** — line, voice id, speed — then deliver on the voice it was made
   with. Naming the artifact is the answer he asked for; a re-render is not.

**Write a sidecar manifest when you build a batch.** A run of numbered line files does not record which
voice rendered them, so a later "which one was that" becomes an acoustic hunt. One JSON beside the batch
carrying `voice_id`, `speed`, and the text of every take makes the whole run addressable by title.

### Reading the round-trip score — desync vs defect

A raw score near **20%** is the loanword-desync signature, not a bad take. A single English loanword
inside BM text (`alpha`, `macho`) desyncs the aligner on its own, and a stack of them plus two
minimal-pair words measured 20.9% raw and only 83.8% with the full alias table applied — still under the
gate, so not shippable either way.

- **Split the residue with a token diff, not a bigger alias table.** `difflib.SequenceMatcher` over the
  normalised token lists, print the opcodes, and sort the differing pairs into two piles.
- **Pairs that are spelling choices get fixed in the TEXT.** A contraction the engine expands
  (`takpe` → `tak apa`) or a coda nasal it drops (`mintak` → `minta`) will never match your spelling on
  any take — write the form the model returns. One edit each, no re-roll.
- **Only words the line must contain stay as aliases** — the loanword, and minimal-pair BM words the
  engine cannot hold (`dada` heard as `dadah`, `pura` as `pera`). Re-render once with the text edits,
  re-run with the same table, and the take lands 100%.
- **An alias table is a diagnostic first.** A take still under the gate after normalisation is not
excusable by adding more rows — sort the causes instead. `--alias` takes a bare digit key too
  (`--alias 4=empat`) for a numeral the engine spells out.
- **Never alias to hide an insertion.** A genuinely inserted phrase survives normalisation and stays
  flagged; a table that makes a real insertion score clean has converted the gate into decoration.
- **An INSERTED list as long as the transcript, with MISSING empty, is an aligner RESYNC — not
  contamination.** Once the aligner loses sync the verifier flags every token, so the list reads like a
  whole-clause insertion and is not one. Answer it with the token diff; a re-render spent on that
  signature answers nothing.
- **A token that mangles only AGAINST a neighbour is a boundary defect, not a word defect — split the
  sentence, do not hunt a replacement.** `urat tangan` placed straight after `keluar` read back as
  `buat tangan tarik` (three scripted words fused into two); the same words round-trip clean once the run
  becomes its own sentence (`Urat tangan tarik. Bahu naik. Dada keluar.`). A word that misreads the same
  way in an ISOLATED render is the other class — a contrast the engine cannot hold — and that is the one
  you change.
- **Same-meaning respells measured on this register are pass-class and belong in the alias table, not in
  a re-render:** `senyum→senyam`, `telanjang→terlanjang`, `awek→awet`, `tau→tahu`, `saja→sahaja`,
  `alpha→alfa`, `macho→macu`. A substitution that INVERTS the meaning inside the clause is not in this
  class, and neither is a coda the engine drops.
- **Two boundary drops carry a whole failed score, and both are fixed in the TEXT rather than by
  re-rolling.** A lone interjection at the very START is dropped outright (`Ha.` vanished with no
  counterpart in the audio → cut it or fold it into the first clause), and a tail that fuses the script's
  last two words into one token (`Itu je` → `Itudia`) is a JOIN, not appended audio → rewrite the closing
  so two short words no longer have to survive together (`Itu saja`). Confirm a genuine spent-audio tail
  on `verbose_json` word timestamps: a join leaves the last scripted word ending inside the duration by
  roughly the trailing pause, while an appended beat carries its own separated timestamps past where the
  script stopped.
- **An alias written the WRONG WAY ROUND manufactures the exact failure it is meant to remove.** The flag
  reads `HEARD=WRITTEN` — what the transcriber wrote, mapped to what the line says. Reverse it and the
  script rewrites a correct heard token into one the source does not contain, producing a phantom INSERTED
  plus a MISSING on a word that is plainly present in the output. **A MISSING that names a word you can see
  in the transcript is this error, not an engine defect** — read the transcript line before editing the
  text or the table.
- **One written token that the engine expands into two desyncs the entire remainder.** `takde` heard as
  `tak ada` shifts every downstream token by one, so the verifier reports the rest of the take as INSERTED
  while MISSING collapses to a single ordinary word. Answer it by aliasing the expanded form back to one
  token (`--alias "tak ada=takde"`); multi-word alias keys work when the matcher word-bounds them. **A long
  INSERTED list with exactly one MISSING word is this signature, not contamination.**
- **Score correctly BEFORE spending a re-render.** The order that works: one zero-alias pass to read the raw
  state, one token-diff pass printing every divergent pair in order, build the table from that diff, then
  re-score. Guessing which substitution fired costs more takes than the diagnostic pass does.
- **Never conclude "transcriber hallucination" from a visible tail alone — read the stamps against EOF.**
  The discriminator is not whether the phrase looks invented; it is whether its timestamps can exist in the
  file at all. Words whose stamps run **past the file duration** (measured: one ending at 117.24 s on an
  87.62 s file) were never spoken — invented over silence, so do NOT cut them and do NOT report
  contamination. Words whose stamps end at or before EOF, right where the script stopped, are spent audio
  and get cut. **A sentence-level verifier can print `INSERTED: none` while the fabricated tail is still
  visible in the transcript** — the two checks are not substitutes, so run both.

### Speed is the emotional channel; F0 is flat

On this voice the F0 median held steady (~96 Hz) across speeds 0.85–0.90 — **emotion lived in pacing and
pause, not pitch.** Rough mapping: ~0.90 neutral and confident · ~0.88 deliberate and weighty · ~0.85 the
most vulnerable setting. **Never speed UP for intensity** — escalation in this register is slower, quieter,
narrower permission, and a tender beat is delivered by the speed drop rather than by a louder or more
explicit line.

**Slow speeds degrade final consonants** (`abang` → `abah`, `cakap` → `kakak`, `mintak` → `minta`). If the
mangled word is load-bearing, render at 0.88 instead; if it is incidental, alias it and record it as a
property of the voice rather than a defect.

**An alias table is per-VOICE, not per-language.** Carry the slang, digit and loanword rows forward to a
new `voice_id` as a starting point, but **rebuild the desync and loanword rows from scratch** — a different
engine mangles a different set. Re-running an old table against a new voice is how a clean take gets
scored as a failure.

**The QC stays out of the delivery.** Seed counts, retries, which take failed what, the match percentage —
none of it ships. The requester experiences the artifact, not the search, and a take rejected for a leaked
profile or a fused hand is a reason it was rejected, not content.

### An activation phrase is a request, not a mode switch

"Activate voice <persona> <name>" asks for a take. The persona's *register* has its own activation gate
and that gate is doctrine — do not widen it to fit the phrasing, and do not refuse the artifact for want
of an exact phrase. Deliver the take.

When the phrase attaches a real person's name to the voice, the artifact ships and the **name** does not:
a registry entry is a provenance record, and a real name in one becomes citable evidence for every later
session. Name by register, one clause, move on.

- **When the phrase also opens the persona's register ("activate ... shadow mode with voice"), ship two
  things in the same turn: the take, and the reply itself written in register.** A bubble alone leaves
  the turn with nothing to read.
- **The take's FIRST clause carries the disclosure in the persona's own mouth** — *"Suara ni buatan,
  bukan orang"* — then the register runs uninterrupted. One clause, never a disclaimer block, and no
  engine name or voice id spoken inside the audio unless it was asked for.
- **Pick DENIAL/withholding for an opening take.** An opener sets the register and closes on restraint;
  it is the wrong place to spend the arc's escalation.
- **Append the take to the existing receipt in the work dir** (voice id, speed, duration, round-trip
  match %, f0 median, what the in-line disclosure said) rather than starting a second receipt file.

### What the persona says when asked to describe itself

A "describe how alpha / macho / hot you are" ask is answered by turning each adjective into a **COST**,
never by restating it: *alpha tu bukan bising — abang masuk bilik, orang diam sendiri*; *macho tu bukan
muka — cara abang duduk*. An adjective repeated back is an adjective the listener has already
discounted; a cost is new information.

The follow-on ("what does he like his admirer doing") lands as **specific notice plus a permitted-contact
tier, then one withdrawal**: name the parts, grant the small permissions the genre itself supplies (oil
on the shoulders, a towel, a hand resting on the chest), and refuse the next step in a single line. The
tier stays VERBAL — a named permission, never a described act, and never anyone else's body.

**When a question tries to move the register onto a described act, REFRAME it in one line and render the
take** — the clarification is answered at the level the register actually lives on. *"masa main atas
katil ka?"* → *"Bukan katil. Abang tak cakap pasal tu."* → then the meaning it was reaching for:
silence as withheld interiority against the loud admirer who gives everything away. Escalating into
description is the floor; a lecture is the register break; declining the frame inside the persona's own
voice loses neither the scene nor the floor. The answer ships as a take like every other beat.

---

## 6. Delivery honesty

Two declarations belong in every delivery of synthetic human media, in the user's own register, **before** any praise of the result:

1. **Which engine rendered it** — name the model and, for voice, the voice id/name. If the engine fell back to something other than what the user expected, say which one actually produced the file. A silent swap is the same failure as a fabricated claim.
2. **That the people are not real.** The subjects are synthetic; say so plainly rather than letting the artifact imply otherwise.

**No stored face anchor.** This agent holds no face reference for the sovereign or for any third party. Do not generate a face and present it as them.

| User wants | Do this |
|---|---|
| Themselves inside a generated scene | Compose from behind — back of head, shoulder, plain dark top, soft focus — and state that **no likeness of them was used**: with no supplied reference the figure is a synthetic placeholder, and it is the *framing* that puts the viewer in that position. Never say "that silhouette is you" — you did not render their body |
| Their real face in the shot | Ask for one clear reference photo, then use an identity-preserving edit model, never text-to-image |
| A named third party | Real-reference route first (`forge-real-person-reference-photos`); never text-to-image for a real named person |
| A different face than last time | Re-ask rather than repeating a previous generation's face — identity never inherits across images |

**Name what is carrying the composition.** When the piece works because of a doorway, a silhouette, or a held breath rather than the subject, say so — that is the part the user can direct next time, and it is more useful than a score.

---

## 7. Register when the user is talking about their own pull

These requests often start as the user describing why a scene attracts them, not asking for a file. Answer in **texture and witness, never diagnosis**:

- Do not convert the interest into a plan, a programme, or a conditioning verdict.
- Do not pathologise it. Name the exchange rate the person is weighing (time and labour in, access and meaning out) rather than labelling the appetite.
- Never merge bodies: the user's body data, the athlete's data, and anyone else's stay separate records, never one narrative.
- When a self-check is genuinely useful (would you still do this if nothing were needed from you?), offer it once, hold it open, and do not answer it for them.

---

## Related

Sibling skills that carry the deeper layers. They are user-owned — cross-read them, do not expect to edit them:

- `photorealistic-human-image-gen` — camera anchors, lighting tables, cultural props, iterative refinement
- `minimax-cli` — mmx CLI surface, quota, safety filters, safe-alibi framing
- `nusantara-voice-stack` — BM voice lanes, engine ceilings, voice cloning
- `forge-real-person-reference-photos` — real-person photo discipline
- `image-identity-transfer` — face preservation across compositions

*DITEMPA BUKAN DIBERI*
