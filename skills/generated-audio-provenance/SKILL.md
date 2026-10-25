---
name: generated-audio-provenance
description: "Use when generated audio needs provenance labels."
version: 1.0.0
tags: [voice, tts, metadata, provenance, delivery, ogg]
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# Generated audio — labelling and provenance

A synthesized voice note, TTS render, or cloned take is an artefact that outlives the chat it was
made in. Label it at creation time; a file with no provenance becomes evidence of nothing later.
Render mechanics live in the voice-lane and clone-operations skills; this skill owns **what the file
says about itself** and how to prove it says it.

## When to use

- Delivering a batch of candidate voices for a human A/B.
- Sending a render where more than one voice id, register, or source material is in play.
- Any artefact a third party might receive, forward, or find later out of context.

## Procedure

1. **Write one metadata file per artefact.** Do not jam metadata into a shell one-liner: apostrophes,
   quotes and `|` inside a provenance sentence break the command in ways that look like a silent
   success. Write an ffmetadata file and map it:

   ```
   ;FFMETADATA1
   title=<what it is, in words>
   artist=<lane / owner string>
   album=<the batch this belongs to>
   date=<YYYY-MM-DD>
   genre=spoken word
   comment=voice_id=<canonical id>; provider=<engine>; provider_voice_id=<id>; provenance=<how the voice was built>; synthetic render; purpose=<A/B only | delivered to X>; registry=<path to the voice registry>
   ```

   ```
   ffmpeg -y -loglevel error -i in.ogg -i meta.txt -map_metadata 1 -map 0:a -c copy out.ogg
   ```

   `comment` carries: canonical voice id, provider + provider voice id, provenance in one clause
   (whose audio, how much of it, what processing), the word **synthetic**, the purpose, and where
   the registry lives. Each of those is a question a human will ask later.

2. **Verify by reading the container, not by trusting the muxer.** On Ogg/Opus ffmpeg stores the
   `comment` key as `DESCRIPTION`. Search for the value, not the key name, or you will conclude the
   label vanished. `ffprobe -show_format` prints no OpusTags at all — parse them directly:

   ```python
   import struct
   b = open(path,'rb').read(); p = b.find(b'OpusTags') + 8
   vlen = struct.unpack('<I', b[p:p+4])[0]; p += 4 + vlen
   n = struct.unpack('<I', b[p:p+4])[0]; p += 4
   tags = {}
   for _ in range(n):
       ln = struct.unpack('<I', b[p:p+4])[0]; p += 4
       s = b[p:p+ln].decode('utf-8','replace'); p += ln
       if '=' in s:
           k, v = s.split('=', 1); tags[k.upper()] = v
   ```

   Assert each expected field equals what you wrote. One boolean per artefact
   (`desc_has_voice_id`, `desc_has_synthetic`, `desc_has_purpose`) turns "I labelled it" into a
   checkable claim.

3. **Emit a manifest beside the batch**: one row per artefact with voice id, path, the fields that
   must be present, sha256 and byte size. The hash is what lets a later session prove the file the
   human kept is the file that was made, after transport re-encodes it.

4. **State the labels in the delivery message too.** A tag survives only if the human keeps the
   file; the message is what they read in the moment. One line per artefact: identity, register,
   and whether it is a real recording or a synthetic render.

## Rules

- **Never let a synthetic render travel as if it were a recording.** That distinction is the whole
  value of the label. It is not a disclaimer to soften — it is provenance, the same class of fact
  as a sha256.
- **One voice id per file name.** `<batch>_<canonical-voice-id>.ogg` keeps the set self-describing
  even when a downstream tool strips the tags.
- **Check the registry before restating provenance from memory.** Entries carry `provenance`,
  `source_sample`, `provider_file_id` and dated mint receipts — quote those, and when a claim rests
  only on a registry sentence, say so rather than presenting it as a measurement.
- **Do not install a tag library to verify a tag.** The container is a few bytes of length-prefixed
  UTF-8; parse it inline instead of reaching for a package that may not be there.

## Depth

- `references/render-lane-diagnostics.md` — which key a synthesis CLI actually reads, the fail-closed
  clause loop, long-render polling, and why f0 cannot settle identity.
