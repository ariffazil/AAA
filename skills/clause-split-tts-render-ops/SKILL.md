---
name: clause-split-tts-render-ops
description: "Use when a long TTS take must be rendered or repaired."
version: 1.0.0
author: Hermes
license: arifOS
tags: [tts, voice, render, repair, gate, telegram-delivery]
metadata:
  hermes:
    category: audio
    tags: [tts, voice, render-repair, gate]
    related: [persona-arc-scripting, abang-sado-creative-lane, voice-render-verification, multi-voice-note-assembly]
triggers:
  - a 60 s+ TTS take has to be rendered clause-by-clause
  - the round-trip gate returned MISSING or INSERTED on a long take
  - a rendered take came out short, or shorter than the same script rendered before
  - a take needs one clause fixed without spending a full re-render
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# Clause-Split TTS Render Ops

Mechanics for LONG takes (roughly 60 s and up) rendered sentence-by-sentence through a
clause-splitting pipeline. This skill owns the **render work dir, the repair loop, and the gate-flag
triage**. It does not own script structure, act counts, register or delivery shape (that is
`persona-arc-scripting`), it does not own the persona's register or voice selection
(`abang-sado-creative-lane`), and it does not own the verifier's own calibration
(`voice-render-verification`). Load those alongside; this one starts at "the text is written, now
make the audio".

## 1. Resolve the voice from the registry, every time

Read `/root/AAA/audio/voice-registry.json` for the id you were asked for, resolve `aliases` → entry,
and take `provider_voice_id` (a STRING) for the render. Do not take `provider_file_id` (an integer
that only points at the uploaded source audio). The wrong field is accepted at the wire and silently
renders a default voice — the take sounds plausible and only a band/identity check catches it.

## 2. Budget the script for clause-split, not for single-pass

A single-call render runs ≈12 chars/s. Clause-split (`--clause`, gaps of ~0.38 s between sentences)
runs **≈11.5 chars/s at speed 0.90–0.95**, and the loss scales with the number of CLAUSES, not with
length: a 55-clause act loses ~20 s to pure silence.

```
chars ≈ 11.5 × target_seconds      a 3-minute act ≈ 1,900–2,100 chars
```

Do not promise the asked duration. Render, `ffprobe` the file, and state the real number in the
delivery rundown. An act asked at 3 minutes landing at 2:49–3:09 is inside tolerance; an act that
lands 20 s short was under-written, and the fix is more repetition of the command, never new events.

## 3. Fresh work dir, always

```bash
rm -rf "$OUT" && <lane> say script.txt --voice <id> --speed 0.9 --clause --no-deliver --out "$OUT"
```

The renderer keeps `cNN.txt`, `cNN.mp3`, `cNN.wav` inside `$OUT` and concatenates whatever is there.
Two consequences that cost render cycles:

- **Re-rendering into a used work dir can build a truncated take.** Clause files from an earlier
  attempt survive, a failing clause is retried against or replaced by the stale file, and the concat
  joins fewer clauses than the script has. The take is silently short. `rm -rf` before every run.
- **A mixed mtime set (`c*.mp3` older than `c*.wav`) means the dir is dirty** and the take in it is
  not a clean render of the current script. Treat it as suspect even if the gate passes.

## 4. Gate-flag triage — the shape of the flag decides the fix

Read the `heard` line, not the percentage. Then classify:

| Flag shape | What it is | Fix |
|---|---|---|
| MISSING runs from the middle of the take to the last word | **Truncation**, not prose. The transcript stops at a clause boundary | Clear the work dir, re-render whole. Check the reported clause count against `len(clause_split(script))` |
| One MISSING word that appears twice in the script (`panjang-panjang`, a reduplicated pair) | Synthesis elides one copy; the aligner picks the survivor | Rewrite that clause so the target word is not reduplicated. `--alias heard=written` does NOT rescue it |
| One INSERTED short token mid-take (`ni`, `la`) right after a quantity or numeral | Render-time insertion at a clause boundary | Rewrite the clause (drop the numeral, rephrase), then repair that clause only |
| INSERTED closing boilerplate (`terima kasih kerana menonton`) whose `last_end_s` runs past file duration | Transcriber invention over trailing silence, NOT contamination | The tail/EOF discriminator already disproves it. Do not cut, do not re-render |
| `f0 family check SKIPPED` note | The identity check did not run (missing DSP stack) | It is **not** a pass. Do not present a skipped check as verified |

Write quantities the way a speaker says them and keep them out of the shortest clauses. A clause whose
only job is a number attracts insertions and swallows; give it a full sentence with a verb.

## 5. Repair ONE clause, do not re-render the take

A gate flag on a single clause costs ~3 minutes to fix by full re-render and seconds by clause repair.
The render dir has everything needed: `cNN.txt`, the sentence-level wavs, `gap.wav`, and the concat
list.

```bash
WD=/path/to/take            # render work dir: contains cNN.txt / cNN.wav / gap.wav
IDX=17                      # 1-based clause index that failed
TOTAL=48                    # total clauses in this render

printf '%s\n' "New sentence that fixes the seam." > "$WD/c$(printf %02d $IDX).txt"

export PATH=$PATH:/root/.npm-global/bin
cd "$WD"
mmx speech synthesize --base-url https://api.minimax.io --model speech-2.8-hd \
  --voice "<provider_voice_id>" --speed 0.9 \
  --text-file "c$(printf %02d $IDX).txt" --out "c$(printf %02d $IDX).mp3" --quiet
ffmpeg -y -loglevel error -i "c$(printf %02d $IDX).mp3" -ar 44100 -ac 1 "c$(printf %02d $IDX).wav"

rm -f concat2.txt take2.mp3
for i in $(seq -w 1 $TOTAL); do
  echo "file '$PWD/c$i.wav'" >> concat2.txt
  [ "$i" != "$TOTAL" ] && echo "file '$PWD/gap.wav'" >> concat2.txt
done
ffmpeg -y -loglevel error -f concat -safe 0 -i concat2.txt \
  -af loudnorm=I=-18:TP=-2:LRA=11 -ar 44100 -ac 1 take2.mp3
```

Then re-gate `take2.mp3` against the UPDATED script before delivering. Never ship the original take
that the gate refused — a repaired take carries its own verification, a patched transcript does not.

## 6. Re-gate, then encode for delivery

```bash
python3 <lane>/scripts/verify_take.py take2.mp3 --text script.txt   # exit 0 = PASS
ffmpeg -y -loglevel error -i take2.mp3 -c:a libopus -b:a 48k -ar 48000 final.ogg
ffprobe -v error -show_entries format=duration -of csv=p=0 final.ogg
```

Keep the mp3 as the working artifact and ship the opus `.ogg` as a voice bubble. Verify the encoded
file's duration against the mp3 — a resample/encode that drops the tail is a different failure from a
gate flag, and only `ffprobe` on the delivered file shows it.

## 7. Delivery of a re-asked set

- Each take ships as its own bubble: `[[audio_as_voice]]` on its own line, then `MEDIA:/abs/path.ogg`.
- **A bare "give me" / "give" after a delivered set means RE-SEND that set** — same order, no
  re-render, no re-gate, no re-explanation. Re-rendering on that signal changes an artifact the
  requester already accepted.
- When the set is re-sent, a one-line rundown per act plus the real measured duration is enough. Do not
  restate the register, the gate, or the pipeline.
- If the ask names a different register for the same arc, re-render the WHOLE set in that register
  rather than leaving half of it in the old voice.

## Pitfalls

- **Full re-render to fix one clause.** The expensive default; §5 exists because a single clause can be
  repaired in seconds and the evidence (the clause wavs) is already on disk.
- **Trusting a percentage.** Dense dialect BM scores low on clean audio and high on a mangled one; the
  `heard` line is the witness, the ratio is a lead.
- **Reusing a work dir across attempts.** The most reliable way to ship a truncated long take, and
  duration checks do not catch it because the residual silence keeps the file inside the floor band.
- **Splitting the delivery into a status report.** Deliver the audio; one informational line each, not
  a round-by-round account of renders, retries and flags.
