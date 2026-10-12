---
name: persona-voice-note-render
description: "Use when rendering a persona voice note for a lane."
version: 1.0.0
tags: [voice, tts, telegram, minimax, sado]
---

# Persona Voice Note — headless render + QC + delivery

Use when the principal asks for a reply "in <persona> voice" (e.g. "Bagi voice Siti Nurhaliza", "SS", "suara PMX", "suara aku"). Deliverable = an audio file that lands in the chat as a voice bubble, not a description of one.

## Steps

1. **Write the spoken script to a file** (`/root/.hermes/cache/scratch/<name>.txt`) — prose, paragraphs, no markdown, no bullets. Human language only: no F-numbers, no receipts, no internal vocabulary.
2. **Render** with a stdlib runner (no venv/requests needed):

```python
# /root/.hermes/cache/scratch/siti_call.py  (template — change voice_id only)
import os, json, urllib.request, sys
key  = os.environ["MINIMAX_API_KEY"]
base = os.environ.get("MINIMAX_API_HOST", "https://api.minimax.io")
text = open(sys.argv[1], encoding="utf-8").read()
payload = {"model":"speech-2.8-hd","text":text,"stream":False,
  "voice_setting":{"voice_id":"SSSiti20260926v1","speed":1.0,"vol":1.0,"pitch":0},
  "audio_setting":{"sample_rate":24000,"bitrate":128000,"format":"mp3"},
  "language_boost":"Malay"}
req = urllib.request.Request(base+"/v1/t2a_v2", data=json.dumps(payload).encode(),
  headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"})
r = json.load(urllib.request.urlopen(req, timeout=180))
assert r["base_resp"]["status_code"] == 0, r["base_resp"]
open(sys.argv[2],"wb").write(bytes.fromhex(r["data"]["audio"]))  # HEX, not base64
```

Voice IDs: Siti/SS = `SSSiti20260926v1` · Arif = `iarif-sovereign-v9` (NOT V8 — it injects a banned greeting) · fallback male = `Indonesian_BossyLeader`. Never mix personas in one lane.
3. **QC — mandatory.** `ffprobe` the duration (expect ~13 chars/s of script; a 200-char script rendering 0.2s is truncated) and round-trip through Groq whisper `language=ms`. On any suspicious take read `no_speech_prob` from `verbose_json`: >0.5 means there was no speech to transcribe. Sign-off boilerplate ("Terima kasih kerana menonton") or a one-word transcript on a short clip = silence/noise, not Malay — say "no speech in this clip" instead of inventing content.
4. **Deliver** as two lines in the reply: `MEDIA:/abs/path.mp3` then `[[audio_as_voice]]` on its own line. Add at most one short line of text saying what landed and how long it runs; never attach a menu of follow-ups.

## Audio format for Telegram voice bubbles (headless MiniMax path)

When the rendered clip is `.wav` (the default from `bash /root/AAA/engines/iarif_tts_pipeline.sh`), Telegram will NOT render it as a native voice bubble. It arrives as a generic audio file attachment — the user has to tap to play. To get a native bubble:

1. Convert to MP3 with ffmpeg (32000 Hz mono is the engine default, 128 kbps is plenty):
   ```bash
   ffmpeg -y -i input.wav -codec:a libmp3lame -b:a 128k output.mp3
   ```
2. Deliver as `MEDIA:/abs/path/output.mp3` followed by `[[audio_as_voice]]` on the next line.

Don't cite the `/tmp` or scratch path to the principal — just send the artifact.

## Duration floor (do not skip the verify step)

`iarif_tts_pipeline.sh` enforces a 2.0s render floor on the MiniMax lane. A clip shorter than that triggers **three auto-retry attempts, then abort — no success returned.** This bites hard on short utterances like a one-line persona reply ("Haha", "Yeah", "Wey sedap", "Setuju"):

```text
attempt 1: duration 1.405s < floor 2.0s — re-render
attempt 2: duration 1.184s < floor 2.0s — re-render
attempt 3: duration 1.311s < floor 2.0s — re-render
duration guard FAILED after 3 attempts — abort, do NOT return success
```

**Fix:** extend the script to a minimum ~25 chars (one full sentence in BM) so the TTS pauses naturally to clear the floor. Do NOT patch the floor lower — the floor exists because sub-2s renders truncate phonemes in unpredictable ways and downstream Whisper round-trips become hallucinated. The persona line plus a register-fitting follow-up ("Wei sedap. Cheese + ham cukup protein — gym full send lepasni.") clears the floor on attempt 1.

```python
# Pre-flight length check — never invoke the pipeline on a script below ~24 chars
text = open(text_file).read().strip()
if len(text) < 24:
    raise SystemExit(f"script too short ({len(text)} chars) — pad to ≥24 chars or pipeline will refuse")
```

## Pitfalls

- `data.audio` is a hex string — decode with `bytes.fromhex`, never base64.
- Pacing is ~2.1–2.3 words/s with paragraph pauses; a 500-word script lands ~3.5–4 min. For a deep answer expect ~4 min and say so in the delivery line.
- `status_code 0` alone proves nothing — always check duration + round-trip.
- Dead lanes as of 2026-09-29: Z.AI `glm-asr-2512` (`1113 insufficient balance`), DashScope intl `qwen3-asr-flash` (`AllocationQuota.FreeTierOnly`). Working ASR: Groq whisper (curl) and local `whisper` CLI.
- The voice only carries the message; it does not license softening. If the ask is medical/legal analysis, the script must BE the finished analysis.
- Voice-registry resolution is fail-closed: `iarif_tts_pipeline.sh` resolves `<voice>` → canonical alias → provider id by reading `/root/.AAA/audio/voice-registry.json`. A REVOKED voice id (e.g. `i-arif-v8-deprecated`) or an unknown id aborts before any audio is sent. The pipeline will not let you route around the V8 contamination hole via env-var override — this is by design. To use a non-default persona voice in a lane, look up the alias (`aliases.<alias>.casefold()`) before invoking the script.

## Delivery — the moment of truth (Anti-Bangang LAW 1 + LAW 6)

The artifact is rendered; the file path is known; `ffprobe` says it is audio. At this moment there is exactly one correct next move: **send it**. Any text generated before, during, or after delivery that asks the principal to choose between options is a defect.

**Permitted:**
- One short line of text naming the artifact and its duration ("Syed, 1m08s, ping KSCC pukul 5 — protein baru cerita"). That line is the receipt.
- `MEDIA:/abs/path.mp3` then `[[audio_as_voice]]` on the next line.

**Forbidden at delivery time:**
- "Hang nak dengar sebagai suara ke fail?" — formats already ask before render.
- "mp3 ke ogg?" — format already chosen by pipeline.
- "Mana satu hang nak?" — there is no menu after the file is rendered.
- "Saya hantar ke chat ni ke group Syed?" — destination already in `origin`.
- A 4-question audit checklist asking the principal to confirm what the system just produced.

**Why this rule is absolute:** the moment the audio is on disk, the principal's attention budget is finite. A menu at delivery costs more than a missing option later. If something is genuinely ambiguous (rare), fix it before render — not after. A render followed by a permission menu is the loudest possible "talk is cheap, work is expensive" — the defect Anti-Bangang LAW 1 ("Kalau benda tu tambah kerja manusia, ia bukan improvement") and LAW 6 ("Jika Arif perlu baca 1,000 perkataan untuk tahu satu keputusan mudah") were written to prevent.

**Receipt vs narrative:** receipt = artifact + one line. Narrative = prose explanation of why the artifact is what it is. The principal did not ask for the narrative at the moment of asking for the voice note. Render, send, stop.

## Federation role split (binding — do not collapse)

When the principal asks for a voice note and an execution channel exists, route execution to the right organ before any rendering begins:

| Domain | Organ | Does what |
|---|---|---|
| Memory · Learning · Context · Voice | **HERMES** | Decides what to say, who says it, which voice_id, in which persona. Returns the spoken script + chosen voice_id + delivery channel. |
| Execution · Tools · Mutation · Render | **OPENCLAW / IRFANclaw** | Calls `iarif_tts_pipeline.sh` / `siti_render.py` / MiniMax API. Returns the file path + md5 + duration. Does not choose words or voice_id. |
| Delegation · Interoperability | **A2A** | Wraps the request envelope (intent + claim + proof_obligations) and returns witness bundle (commit_sha + diff_stat + latency_ms). |
| Governance · Authority | **arifOS** | Authorises whether a voice_id may be used; F13 gates voice creation. |

Merge them and you get a department store clerk who is also the cashier, the shelf-stocker, and the security guard — capable of nothing efficiently. Bind them through authority-controlled delegation and each organ does the one job it was forged for. **Voice-lane is execution — never re-decide voice_id or script in the execution lane.**
