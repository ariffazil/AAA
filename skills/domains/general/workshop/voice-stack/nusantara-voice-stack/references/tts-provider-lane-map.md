# TTS Provider Lane Map — probed 2026-08-14, updated 2026-08-18

All lanes tested for Bahasa Malaysia TTS output on this VPS (Linux 6.17.0, Python 3.13.7, 31GB RAM, no GPU).

## ⚡ LANE STATUS SUMMARY (2026-08-18)

| Lane | Status | Cost |
|---|---|---|
| MiniMax TTS (speech-2.8-hd) | ✅ LIVE | Free (Token Plan quota) |
| MiniMax TTV voice cloning | ✅ LIVE | Free (Token Plan quota) |
| Qwen voice cloning (Singapore) | ✅ LIVE | Free (Token Plan quota) |
| edge-tts ms-MY-OsmanNeural | ✅ LIVE | Free (unlimited) |
| MuleRouter speech | ❌ DEAD (402, -0.75 credits) | N/A |
| Runpod F5-TTS | ⏳ BLOCKED (GPU + license) | ~US$10 |
| Piper TTS | ❌ DEAD (no ms_MY voice) | N/A |

## 1. edge-tts (PROVEN, free, engine-capped)

- **Auth:** none required
- **Installation:** `pip install edge-tts --break-system-packages`
- **Available ms voices:** ms-MY-OsmanNeural (male), ms-MY-YasminNeural (female)
- **Both tagged:** "Friendly, Positive" — formal narration only, no loghat, no fillers, no emotional range
- **Edge-tts CLI pitfall:** `--pitch=-15Hz` works; `--pitch -15Hz` errors "expected one argument"
- **Python API pitfall:** `edge_tts.Communicate(text, voice, rate=..., pitch=...)` — rate/pitch accept string format only (`'+5%'`, `'-8Hz'`)
- **Quota:** unlimited, free forever
- **Verdict:** baseline; engine-level ceiling (2 voices, 1 style)

## 2. MiniMax TTS via Token Plan (PROVEN, RM0 when quota available)

- **Auth:** sk-cp-* Token Plan key (NOT plugin key, NOT Mulerouter key)
- **Correct endpoint:** `https://api.minimax.io/v1/t2a_v2` (global)
- **Wrong endpoint:** `https://api.minimax.chat/v1/t2a_v2` — returns "invalid api key" for Token Plan keys
- **Correct header:** `Authorization: Bearer ***`
- **HTTP 200 + status_code 1004:** auth failure (wrong key format, or wrong endpoint)
- **HTTP 200 + status_code 2056:** Token Plan weekly limit reached — wait for Sunday reset
- **HTTP 200 + status_code 1000:** success, audio in `data` field as base64
- **Model:** `speech-2.8-hd` (latest), `speech-2.6`, `speech-02`
- **GroupId query param:** CN endpoint only; global endpoint takes pure Bearer, no GroupId
- **mmx CLI (FIXED 2026-08-18):** `mmx speech synthesize --base-url https://api.minimax.io` WORKS. Without `--base-url`, CLI defaults to `https://api.minimax.io/anthropic` → HTTP 404. Always pass `--base-url`.
- **Indonesian voices handle BM text naturally** (proven 2026-08-18). Top: `Indonesian_BossyLeader` (speed 0.82-0.85), `Indonesian_CaringMan` (speed 0.9). See SKILL.md §4.
- **Quota:** `general` model pool (shared with image). Check: `mmx quota show --base-url https://api.minimax.io`

**Direct curl template:**
```bash
curl -s "https://api.minimax.io/v1/t2a_v2" \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "speech-2.8-hd",
    "text": "Hai Arif, ujian suara.",
    "stream": false,
    "voice_setting": {"voice_id": "male-qn-qingse", "speed": 1.0, "vol": 1.0, "pitch": 0},
    "audio_setting": {"format": "mp3", "sample_rate": 32000}
  }' | python3 -c "
import json,base64,sys
d=json.load(sys.stdin)
if d.get('data'):
    open('out.mp3','wb').write(base64.b64decode(d['data']))
    print('OK')
else:
    print('ERR', d['base_resp'])
"
```

## 3. MiniMax TTV Voice Cloning (BREAKTHROUGH, FREE, 2026-08-18)

- **Status:** ✅ LIVE on Token Plan — FREE, no Beijing region restriction
- **Voice ID format:** `ttv-voice-YYYYMMDDHHMMSS-*` (e.g., `ttv-voice-2026081809381426-78AFZAgJ`)
- **Invocation:** `mmx speech synthesize --base-url https://api.minimax.io --model speech-2.8-hd --voice "ttv-voice-*" --speed 0.85 --text "..." --out /tmp/output.mp3`
- **Output:** 32kHz, ~200KB per 12s generation
- **Quota:** shared with `general` model pool (same as image + standard speech)
- **Voice creation:** via MiniMax UI (API not yet reverse-engineered)
- **Persistence:** voice ID persists server-side under account; `mmx speech voices` does NOT list custom TTV voices
- **Previously wrong:** documented as "Beijing only, CNY 9.9 unlock fee" — CORRECTED 2026-08-18

## 4. Qwen Voice Cloning (Singapore, FREE, 2026-08-18)

- **Status:** ✅ LIVE — free voice creation + synthesis on Token Plan
- **Model:** `qwen-audio-3.0-tts-flash` (create + synthesize must match)
- **Region:** Singapore (`ap-southeast-1`)
- **Supported input languages:** Chinese, English, Japanese, Korean, Russian, French, German, Portuguese, Thai, Indonesian, Vietnamese, Spanish, Italian, **Malaysian**, Filipino, Arabic
- **Audio requirements:** WAV/MP3/M4A, 10-20s (60s max), ≥ 16kHz, mono, clear speech, no background noise
- **Pitfall:** audio must be accessible via URL (not local file://) — host on temporary HTTP server
- **Seat quota:** QWEN_ARIFOS_API_KEY exhausted (449), QWEN_TEAM_OWNER_API_KEY works
- Full API details: `references/qwen-voice-cloning-2026-08-18.md`

## 5. MuleRouter speech-2.8-hd (❌ DEAD as of 2026-08-18)

- **Auth:** MULEROUTER_API_KEY (separate from Token Plan)
- **Endpoint:** `https://api.mulerouter.ai/vendors/minimax/v1/speech-2.8-hd/text-to-speech/generation`
- **Known voices:** man, woman, Wise_Woman
- **Malay mode:** `--voice man --malay --speed 1.05 --pitch 0` via `mulerouter-tts.py`
- **Status:** ❌ DEAD — HTTP 402, balance -0.75 credits. Separate credit pool from Token Plan. DO NOT RETRY.
- **Script:** `/root/HERMES/scripts/mulerouter-tts.py`

## 6. Runpod GPU — F5-TTS (PENDING — requires F13 GO + balance)

- **Auth:** RUNPOD_API_KEY
- **Target:** Malaysian-F5-TTS-v3 (15,631 hrs, voice cloning)
- **GPU:** RTX 4090 recommended, ~$1.39-2.38/hr
- **As of 2026-08-14:** Runpod balance zero. Blocked until top-up.
- **License:** CC-BY-NC-4.0 — non-commercial only
- **runpodctl pitfall:** deprecated `create pod` form uses `--gpuType`/`--imageName`/`--mem`. Current `pod create` form uses `--gpu-id`/`--image`/`--container-disk-in-gb`. `--mem` does NOT exist on current form.

## 7. Piper TTS (DEAD END for BM)

- Installed: `piper-tts 1.6.1`
- No ms_MY voice exists in rhasspy/piper-voices or any known repo
- Indonesian (id_ID) exists but insufficient for Penang loghat
- **Verdict:** not a BM lane

## 8. Pollinations (DEAD for TTS)

- Legacy text API deprecated for authenticated users
- openai-audio model: 404, migration notice to enter.pollinations.ai
- **Verdict:** not a TTS lane as of 2026-08-14

## 9. FED audio/speech (INTERNAL, partial)

- Endpoint exists at `localhost:4000/v1/audio/speech`
- Returns HTTP 500 "Internal server error" — not wired up for text-to-speech
- fed/audio model available for other purposes but not TTS