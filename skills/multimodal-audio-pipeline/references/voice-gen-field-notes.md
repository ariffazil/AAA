# Voice Gen Field Notes — 2026-08-13 session

## Proven winning voices (user-approved this session)

The user (Arif) asked for an "abang sado cocky voice" — deep Malay male, confident, arrogant-smirk energy. **5 candidates were generated; the user chose Gemini voice `Charon`.**

| Candidate | Source | Result |
|---|---|---|
| gemini_cocky_Charon.mp3 | Gemini TTS, voice `Charon` | ✅ **WON — "this is nice"** |
| edge_alphamale.mp3 | edge-tts Osman, pitch -60Hz | solid backup |
| gemini_cocky_Aoede.mp3 | Gemini voice `Aoede` (female) | backup |
| edge_deep.mp3 | edge-tts Osman, pitch -40Hz | backup |
| Sky | Gemini voice `Sky` | rejected — invalid voice name |

## The winning Charon instruction

```
Deep masculine voice, confident cocky alpha male. Tone like a dominant
bodybuilder speaking with an arrogant smirk. Slow, deliberate, commanding.
Not shouting — quiet confidence.
```

Charon produced a slow, deep, deliberate masculine delivery despite the same
text on all candidates — the voice name + instruction pairing is what sells it.

## Text that worked (Malay, cocky)

> "Tengok ni. Bukan hang nak tengok — aku bagi tengok je. Kalau belum cukup yakin, tunggu sampai aku kata 'boleh'."

## Video + audio sync technique

Charon audio was 11.47s, source video 8.00s. Rather than cutting the voice,
**slow the video to match** (`setpts=PTS*1.434` for 11.41/8.00) so the full
line plays over slow-motion footage — preserved the cocky delivery and looked
intentional.

```bash
ffmpeg -y -i src.mp4 -i voice.mp3 \
  -filter:v "setpts=PTS*1.434" \
  -map 0:v:0 -map 1:a:0 \
  -c:v libx264 -preset fast -crf 22 -c:a aac -shortest -movflags +faststart \
  out.mp4
```

## Keys reality check (this box)

- GEMINI_API_KEY — works, but **rate-limits after ~7 rapid calls**; also vision frames hit 401 on repeated frames (batch ≤3, 2s delay).
- No ElevenLabs key in `kunci-mas.env` (confirmed by grep count = 0).
- MiMo TTS endpoint returns openresty 404 on `api.xiaomimimo.com/v1` — base URL wrong or provider inactive.
- OpenAI `VOICE_TOOLS_OPENAI_KEY` resolved as literal placeholder `${OPENAI...}` — NOT a real key. Skip unless confirmed.
- Qwen Token-plan key quota-exhausted; DashScope websocket blocked by this box's firewall. Both non-functional as of this session.

## F9 / governance note

Voice cloning (ElevenLabs) = F13 HOLD — needs sovereign consent + real source speaker's consent. Stylized TTS generation (Charon etc.) = no consent needed, it's a synthetic voice not a real person's clone.