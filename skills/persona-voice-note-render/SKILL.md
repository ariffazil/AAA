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

## Pitfalls

- `data.audio` is a hex string — decode with `bytes.fromhex`, never base64.
- Pacing is ~2.1–2.3 words/s with paragraph pauses; a 500-word script lands ~3.5–4 min. For a deep answer expect ~4 min and say so in the delivery line.
- `status_code 0` alone proves nothing — always check duration + round-trip.
- Dead lanes as of 2026-09-29: Z.AI `glm-asr-2512` (`1113 insufficient balance`), DashScope intl `qwen3-asr-flash` (`AllocationQuota.FreeTierOnly`). Working ASR: Groq whisper (curl) and local `whisper` CLI.
- The voice only carries the message; it does not license softening. If the ask is medical/legal analysis, the script must BE the finished analysis.
