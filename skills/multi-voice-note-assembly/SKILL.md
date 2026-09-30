---
name: multi-voice-note-assembly
description: "Use when one audio artifact must carry several voices."
version: 1.0.0
tags: [audio, tts, assembly, ffmpeg, casting, delivery]
metadata:
  hermes:
    category: audio
    tags: [audio, tts, assembly, casting]
---

# Multi-Voice Note Assembly

Turning several synthesised clips into ONE deliverable artifact — a voice note with a narrator and
two other speakers, a dialogue, a cast reading. Synthesis belongs to the TTS lane; this skill is the
**casting** and the **stitching**, which is where multi-voice work actually fails.

## Procedure

### 1. Cast each speaker from a voice whose provenance fits the seat

- **Provider system voices** (MiniMax ships ~330 — `Indonesian_*`, `English_*`, `Chinese (Mandarin)_*`, ...)
  are fully synthetic: no human waveform anywhere in the chain, so they raise **no consent question**
  and may be cast in any seat, including an antagonist or rival. The `Indonesian_*` set reads BM
  naturally (phoneme overlap) and is the right cast for invented BM-speaking archetypes.
- **A clone of a real human** speaks only with that human's consent and **never** in a rival or
  antagonist seat. A clone of the requester's own voice is fine for the requester's own lines.
- Enumerate what actually exists before choosing an id rather than guessing one: the MiniMax
  `get_voice` endpoint queried with `voice_type: all` returns the full system-voice list. The
  authenticated call pattern lives in the MiniMax voice-cloning binding skill — follow it there
  rather than pasting credential-bearing request lines into a skill body.

Casting table that reads correctly in BM:

| Seat | Voice id | Notes |
|---|---|---|
| Feminine archetype, alluring | `Indonesian_CharmingGirl` | ~0.95 |
| Feminine archetype, soft | `Indonesian_GentleGirl` / `Indonesian_SweetGirl` | ~0.95 |
| Feminine archetype, composed | `Indonesian_CalmWoman` / `Indonesian_ConfidentWoman` | ~0.95 |
| Masculine archetype, younger/quieter | `Indonesian_ReservedYoungMan` | ~0.92 |
| Masculine archetype, warm | `Indonesian_CaringMan` | ~0.88 |
| Masculine archetype, dominant | `Indonesian_BossyLeader` | ~0.82-0.85 |

**Speed is per-voice and does not transfer.** Numbers calibrated on one id drag or clip on another.
Render once, read `ffprobe`, then adjust — never carry a speed across ids.

### 2. Render each clip to its own file

```bash
export PATH=$PATH:/root/.npm-global/bin
mmx speech synthesize --base-url https://api.minimax.io --model speech-2.8-hd \
  --voice <voice_id> --speed <n> --text-file clip.txt --out 01_open.mp3
```

`--base-url https://api.minimax.io` is required; the CLI's default points at the chat endpoint and
404s on speech. Write each clip's text to its own file, and put **one paragraph per line with single
newlines** — a blank line renders as a multi-second pause.

### 3. Normalise EVERY clip to a common target before anything else

This is the step that decides whether the artifact reads as a scene or as a broken file:

```bash
for f in 01_open 02_awek 03_rival 04_close; do
  ffmpeg -v error -y -i $f.mp3 -af "loudnorm=I=-17:TP=-1.5:LRA=11,aresample=32000" \
    -c:a libmp3lame -b:a 128k n_$f.mp3
done
```

### 4. Build real silence gaps

Gaps are what make N voices read as N speakers. One short gap between turns, a longer one before a
closing beat:

```bash
ffmpeg -v error -y -f lavfi -i anullsrc=r=32000:cl=mono -t 0.8 -c:a libmp3lame -b:a 128k gap1.mp3
ffmpeg -v error -y -f lavfi -i anullsrc=r=32000:cl=mono -t 1.4 -c:a libmp3lame -b:a 128k gap2.mp3
```

### 5. Concat, then encode for delivery

```bash
cat > list.txt <<'EOF'
file 'n_01_open.mp3'
file 'gap1.mp3'
file 'n_02_awek.mp3'
file 'gap1.mp3'
file 'n_03_rival.mp3'
file 'gap2.mp3'
file 'n_04_close.mp3'
EOF
ffmpeg -v error -y -f concat -safe 0 -i list.txt -c:a libmp3lame -b:a 128k full.mp3
ffmpeg -v error -y -i full.mp3 -c:a libopus -b:a 64k -ar 48000 -ac 1 full.ogg
```

Encode to Opus `.ogg` and ship it with `[[audio_as_voice]]` on its own line before the `MEDIA:` line
so the platform renders one native voice bubble. Concat-demuxer stitching is only safe because every
clip was levelled to the same sample rate first.

### 6. Verify, then ship ONE artifact

```bash
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 full.ogg
ffmpeg -hide_banner -nostats -i full.ogg -af volumedetect -f null - 2>&1 | grep mean_volume
```

Check the total duration against what you scripted, and re-check each clip's mean volume after
normalising. Deliver the assembled file — **never the stems, never a pick-one shortlist**. A batch of
near-misses offered as progress reads as unfinished work and hands the choice back to someone who
asked for a finished thing.

## Pitfalls

- **Mixing a cloned voice with provider system voices produces a ~6-7 dB level cliff.** Measured on
  identical settings: −17 dB mean for the cloned voice, −24 dB for two system voices. Skip the
  per-clip `loudnorm` and the secondary speakers audibly sit in another room — the take reads as a
  mistake, not as a second character.
- **`-v error` hides `volumedetect`.** The report is emitted at INFO level, so the very line you want
  is suppressed by the flag you habitually reach for. Use `-hide_banner -nostats` and let stderr
  through when measuring volume; keep `-v error` for the render/encode steps.
- **A registry-gated wrapper cannot reach a provider system voice, and that is correct.** A wrapper
  that resolves voice ids through a registry fails closed on ids that are not entries — which is what
  stops a revoked or contaminated checkpoint being routed around. Do not widen the gate to cast a
  stock voice; call the synthesis CLI directly.
- **Do not carry a speed setting between voice ids.** The same number that reads naturally on one
  voice stretches the identical line on another. Render once, `ffprobe`, adjust.
- **A long assembled note is still one deliverable, not a licence to narrate the process.** Seed
  counts, retries, and which clip needed a second pass do not ship; the requester experiences the
  artifact, not the search.

DITEMPA BUKAN DIBERI.
