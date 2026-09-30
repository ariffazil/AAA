---
name: multi-speaker-synthetic-audio
description: "Use when one audio file needs more than one synthetic voice."
version: 1.0.0
tags: [tts, audio, minimax, ffmpeg, persona, telegram-delivery]
metadata:
  hermes:
    category: creative
    tags: [tts, audio-assembly, minimax, ffmpeg]
    related: [voice-lane, nusantara-voice-stack, abang-sado-creative-lane]
---

# Multi-speaker synthetic audio

A scene with two or more speakers — a persona plus an awek / a rival / a narrator — is a **routing
problem plus an assembly problem**, not a synthesis problem. Each speaker renders fine on its own and
the result still sounds wrong, because the clips come out at different loudness and never get joined.

This skill carries the routing, the level-matching and the assembly. The *register* rules (what a
persona may say, which archetypes stay unnamed and unfaced, declaration discipline) live in the
persona-register skills — cross-reference them, do not restate them here.

## Procedure

### 1. Split the script by speaker, one file per speaker

Write one text file per speaker, **one paragraph per line, single newlines, no blank-line breaks** — a
blank line renders as a multi-second pause and that is where transcriber filler lands. Name them in
speaking order (`01_`, `02_`, …) so the concat list stays readable.

### 2. Route each speaker to the right engine

| Part | Engine |
|---|---|
| The persona / a pre-registered clone | the lane's configured TTS provider, **or** `mmx speech synthesize --voice <registry provider_voice_id>` |
| Any speaker using a **provider system voice** | `mmx speech synthesize --voice <MiniMax system voice>` — directly |

**The hard-won bit: a voice-registry-gated pipeline cannot speak a system voice.** A render pipeline
that resolves its voice argument against a voice registry will exit non-zero on any id that is not a
registry entry, and MiniMax *system* voices are not registry entries. Likewise a configured single-voice
provider hardcodes its voice. Both are correct for the persona and useless for a second speaker —
route the secondary speakers straight off the CLI.

```bash
export PATH=$PATH:/root/.npm-global/bin
D=/root/forge_work/<concept>; mkdir -p "$D"; chmod 700 "$D"; cd "$D"

mmx speech synthesize --base-url https://api.minimax.io --model speech-2.8-hd \
  --voice <persona-or-registry-id> --speed 0.92 --text-file 01_open.txt --out 01_open.mp3 --quiet
mmx speech synthesize --base-url https://api.minimax.io --model speech-2.8-hd \
  --voice Indonesian_CharmingGirl --speed 0.95 --text-file 02_a.txt --out 02_a.mp3 --quiet
mmx speech synthesize --base-url https://api.minimax.io --model speech-2.8-hd \
  --voice Indonesian_ReservedYoungMan --speed 0.95 --text-file 03_b.txt --out 03_b.mp3 --quiet
```

- `--base-url https://api.minimax.io` is **required** — the CLI default points at the chat endpoint.
- **Speed is per-voice and does not transfer.** Never carry the persona's speed number onto a system
  voice; render once, read the printed duration, then adjust.

### 3. Level-match every clip BEFORE concatenating

This is the step that gets skipped and it is the one that decides whether the scene works. Measured on
one real three-speaker batch, same model, same speed family:

| Speaker | Mean volume |
|---|---|
| cloned persona voice | **−17.1 dB** |
| system voice A | −23.9 dB |
| system voice B | −24.1 dB |

A ~6–7 dB gap. Concatenated raw, the secondary speakers sound like they are in another room and the
scene reads as one person talking with two echoes. Normalise each clip first:

```bash
for f in 01_open 02_a 03_b 04_close; do
  ffmpeg -y -i $f.mp3 -af "loudnorm=I=-17:TP=-1.5:LRA=11,aresample=32000" \
    -c:a libmp3lame -b:a 128k n_$f.mp3
done
```

### 4. Assemble with silence gaps between speakers

Silence is what makes a speaker change legible; without it the join sounds like a stutter.

```bash
ffmpeg -y -f lavfi -i anullsrc=r=32000:cl=mono -t 0.8 -c:a libmp3lame -b:a 128k gap1.mp3
ffmpeg -y -f lavfi -i anullsrc=r=32000:cl=mono -t 1.4 -c:a libmp3lame -b:a 128k gap2.mp3

cat > list.txt <<EOF
file 'n_01_open.mp3'
file 'gap1.mp3'
file 'n_02_a.mp3'
file 'gap1.mp3'
file 'n_03_b.mp3'
file 'gap2.mp3'
file 'n_04_close.mp3'
EOF

ffmpeg -y -f concat -safe 0 -i list.txt -c:a libmp3lame -b:a 128k full.mp3
ffmpeg -y -i full.mp3 -c:a libopus -b:a 64k -ar 48000 -ac 1 scene.ogg
```

Encode the delivered file as **ogg/opus** so Telegram renders it as a native voice bubble rather than
a file attachment.

### 5. Verify on the FINAL file

```bash
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 scene.ogg
# then, per-clip and on the final file:
ffmpeg -hide_banner -nostats -i scene.ogg -af volumedetect -f null - 2>&1 | grep mean_volume
```

- Duration must equal the sum of the parts plus the gaps — a short file means a clip failed to render
  and the concat silently skipped it.
- **Acceptance bar: every speaker within ~2 dB of the others on `mean_volume`.** A wider spread is the
  tell that one clip skipped `loudnorm`.
- `volumedetect` output is written at INFO level: a `-v error` flag suppresses it and you will read an
  empty result as "no problem". Drop the flag when you run the check.

### 6. Deliver

`[[audio_as_voice]]` on its own line before the `MEDIA:/abs/path.ogg` line. Ship ONE finished file —
not the per-speaker clips. Any per-speaker declaration of what is synthetic belongs in the persona's
own register, in one clause, riding on the delivery line.

## Pitfalls

| Pitfall | Cause | Fix |
|---|---|---|
| Secondary speaker sounds distant / echoey | Clips concatenated at their native loudness; system voices render 6–7 dB quieter than a clone | `loudnorm=I=-17:TP=-1.5` per clip before concat |
| Pipeline aborts with an unknown-voice error | Voice id resolved against a registry that does not contain provider *system* voices | Render that speaker with `mmx speech synthesize --voice` directly |
| Speaker change reads as a stutter | No gap between clips | Insert a generated silence clip between each speaker |
| Delivered file arrives as a document, not a voice bubble | Container is mp3/wav | Re-encode to ogg/opus, and keep `[[audio_as_voice]]` on its own line |
| One clip's audio missing from the final file | A render failed and concat does not error on a missing entry | `ffprobe` the duration against the sum of the parts before delivering |
| Long scene with long pauses inside a speaker's part | Blank-line paragraph breaks in the source text file | One paragraph per line, single newlines only |

## Related

- `voice-lane` / `nusantara-voice-stack` — engine and provider selection, BM voice quality.
- The persona-register skill for the lane in play (e.g. the SADO creative lane) — what the speakers may
  say, which archetypes stay unnamed and unfaced, and the declaration discipline. Those rules are not
  restated here.
