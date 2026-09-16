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

### An activation phrase is a request, not a mode switch

"Activate voice <persona> <name>" asks for a take. The persona's *register* has its own activation gate
and that gate is doctrine — do not widen it to fit the phrasing, and do not refuse the artifact for want
of an exact phrase. Deliver the take.

When the phrase attaches a real person's name to the voice, the artifact ships and the **name** does not:
a registry entry is a provenance record, and a real name in one becomes citable evidence for every later
session. Name by register, one clause, move on.

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
