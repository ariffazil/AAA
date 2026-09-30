---
name: synthetic-voice-scene-rendering
description: "Use when one render carries several synthetic voices."
version: 1.0.0
author: Hermes
license: arifOS
tags: [tts, voice, scene, concat, qc, minimax]
metadata:
  hermes:
    category: audio
    tags: [tts, voice, concat, qc]
    related_skills: [voice-render-verification, voice-lane, persona-voice-binding, nusantara-voice-stack]
triggers:
  - a request casts more than one speaker into one voice artifact
  - a request asks for two or three voices in one file
  - a rival exchange or a dialogue read aloud
  - one file must carry a narrator plus a character
  - a scene needs concatenating from separately rendered segments
---

# Synthetic Voice Scene Rendering

One artifact, several speakers. Casting rules, per-voice speed, concatenation, and the word-level
failures this engine actually produces on colloquial BM.

**Boundaries with sibling skills.** Voice *governance* (which id may be used, consent, registry
writes) belongs to the voice-stack skills. The ASR-diff / identity gate belongs to
`voice-render-verification`. Persona-specific line craft for a named register belongs to the lane
skill for that register. This skill owns only what is unique to a MULTI-SPEAKER artifact: casting,
speed calibration, assembly order, and scene-level QC.

## Always-on rules

1. **Every speaker except the requester's own clone must be fully synthetic** — a parametric design or
   a vendor catalogue voice, with no human waveform anywhere in the chain. A second character or rival
   cast in a cloned human voice is the forbidden case, and it stops the render before it starts. Cast
   before you write a line.
2. **Side speakers talk in the FIRST PERSON.** Never let a character name themselves with a noun; a
   noun the engine mispronounces silently reassigns who is speaking (see section 3).
3. **One artifact per ask.** A scene made of three voices ships as ONE concatenated file — never three
   files, never a shortlist of takes.
4. **Read each voice's calibrated speed BEFORE rendering it.** Speeds do not transfer between voices.
5. **Name every engine used in one delivery clause.** Repeat deliveries in a session get the clause,
   not the paragraph.

## 1 · Procedure — cast, write, render, assemble, verify

**Cast.** List the catalogue, filter in Python (never by eye), one voice per role.

```bash
curl -s -X POST "https://api.minimax.io/v1/get_voice" \
  -H "Authorization: Bearer $MINIMAX_API_KEY" -H "Content-Type: application/json" \
  -d '{"voice_type":"all"}'
```

- `"all"` returns the `system_voice` array. `"system"` returns **zero rows** — an empty success, not an
  outage. Change the value; do not conclude the catalogue is gone.
- A `base_resp.status_code 1004 login fail` here is key selection, not a dead endpoint: switch to the
  other populated `MINIMAX*` variable in the environment before concluding anything.
- Filter on `indonesia|malay` plus the gender token against `voice_id + description`, and drop rows
  matching `child|kid`. Indonesian voices read colloquial BM without an accent a listener notices.
- **Take the speed from the voice's own calibration record, not from a sibling voice.** A parametric
  design, a clone of a preset, and the preset itself are three different cadences; a number that lands
  on one drags on the next.

**Write.** One paragraph per line with single newlines (a blank line renders as a multi-second pause),
no digits, short sentences. Keep a rival's claim to roughly 35 to 50 words — a rival with a paragraph
becomes a second protagonist and the scene loses its shape.

**Render** each segment on its own voice and speed.

```bash
export PATH=$PATH:/root/.npm-global/bin
mmx speech synthesize --base-url https://api.minimax.io --model speech-2.8-hd \
  --voice <id> --speed <calibrated> --text-file <seg>.txt --out <seg>.mp3
```

`--base-url` is required: the CLI default points at the chat endpoint and 404s on speech.

**Assemble** with real silence between speakers.

```bash
ffmpeg -y -loglevel error -f lavfi -t 0.8 -i anullsrc=r=32000:cl=mono \
  -c:a libmp3lame -b:a 128k sil.mp3
printf "file 'a.mp3'\nfile 'sil.mp3'\nfile 'b.mp3'\nfile 'sil.mp3'\nfile 'c.mp3'\n" > list.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i list.txt \
  -c:a libmp3lame -b:a 128k -ar 32000 -ac 1 scene.mp3
```

- **Re-encode, do not `-c copy`.** Segments from different voices can differ by a frame; copy-concat
  leaves a click at the seam.
- Roughly 0.8 s of silence is heard as a speaker change. Longer reads as a dropout in the recording.
- `ffprobe` the total against the sum of the segment durations BEFORE QC. A concat that silently
  dropped a segment is a short file, not an error message.
- **Order the scene so the payoff lands last** — rivals first, the voice that answers them last. A
  scene that opens with the answer has nothing to answer.

**Verify twice.** Run the round-trip on the combined file (one transcript proves every segment landed),
and again on the cloned segment alone — a combined pass can mask a mid-segment defect by scoring it
against a different speaker's words. Then **read the transcript for WHO is speaking**, not only for word
accuracy.

## 2 · The engine's word-level failure modes (colloquial BM)

Measured on `speech-2.8-hd`. A word that fails is a **constant**, not a seed — change the word, never
re-roll the same text.

| Failure | Shape | Fix |
|---|---|---|
| Semantic **flip** | A real word is substituted for its opposite (`tetap buka` to `tak buka`; `kau tetap ada` to `kau tu tak ada`) and the aligner files it as a *replace*, so the gate reports a clean score over inverted meaning | Ban-word it: rewrite the affirmation without it (`kau tak pergi`, `kau masih di situ`). Two different phrases flipped the same way, and one take can render an instance right and another wrong |
| Loanword resolved to the nearest BM word | `blah` renders as `belah`; on another take the ASR read it as `pulak` | Write the word you want HEARD, not the loan. `belah` is a real BM verb and lands every time |
| Pronunciation limit | `reti` returns as `berhenti` on one take and `kerti` on another | Drop the word rather than re-rolling: `susah nak terima`, `tak tahu nak cakap` |
| Body noun behind a verb collapses | `kata bahu` to `kata bahawa`; `complain bahu` to `komplain bahawa` | Restructure the clause. Do not trust a `-hu` token sitting directly behind a verb onset |
| Phrase-initial onset loss | `Budak gym tu` to `Udat gym tu`, while the same word passes mid-clause (`tak pilih budak`) | Change the noun when it opens a clause (`Orang gym tu`). The defect sits mid-file, so the fix is a whole-take re-render, not a splice |

**The score is not the witness.** Substitutions and fusions are filed as *replace* opcodes and sail
through a clean-looking gate; additions and deletions of whole words are what the gate actually catches.
Read the heard line yourself, closing lines first.

**The tail flag fires on margin, not on content.** The verifier flags any gap between the last scripted
word and EOF. With several segments the gap is wider and the flag is noisier still — confirm no
unscripted word carries real separated timestamps past the last scripted one, then ship. Do not cut on
the flag alone, and never re-render on a flag alone.

**Respelled dialect is not a defect.** `awek` to `awik`, `sado` to `saduh`, `ambik` to `ambil`, digits
read back as words — these are the transcriber's spellings of real words. They pass. A flagged PHRASE is
the thing that rejects a take.

## 3 · The naming trap that reassigns a speaker

A character who refers to himself or herself by a noun is one mispronunciation away from a different
sentence. Measured: a rival line opening `Awek nak abang` round-tripped as `Awak nak abang` — `awak` is
"you", so the line silently changes who is speaking, and the gate scores it clean because every word is
real. Rewrite side-speaker lines in the first person (`Aku nak abang`). It removes the ambiguity and is
better craft besides.

## 4 · Delivery

`[[audio_as_voice]]` on its own line, then `MEDIA:/abs/path.mp3`. One line naming every engine used and
stating the speakers are synthetic. Say what the scene IS before the framing note; never narrate the
rounds (segment counts, retries, which take failed what).
