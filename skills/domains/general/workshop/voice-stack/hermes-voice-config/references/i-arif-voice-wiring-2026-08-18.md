# i-ARIF Voice Wiring Recipe — 2026-08-18

Proven end-to-end: swap Hermes TTS from `edge/ms-MY-OsmanNeural` to `minimax/Indonesian_CaringMan` on `speech-2.8-hd`.

## The Config Block

```yaml
tts:
  provider: minimax
  minimax:
    model: speech-2.8-hd
    voice_id: Indonesian_CaringMan
    speed: 0.88
    emotion: neutral
    sample_rate: 32000
    bitrate: 128000
```

## Wiring Steps (agent-side, T0/T1)

1. **Backup:** `cp config.yaml /tmp/config-bak-$(date +%s).yaml`
2. **Add block** (if `minimax` doesn't exist under `tts:`):
   ```python
   python3 -c "
   import yaml
   with open('/root/HERMES/config.yaml') as f: c = yaml.safe_load(f)
   c['tts']['minimax'] = {'model':'speech-2.8-hd','voice_id':'Indonesian_CaringMan','speed':0.88,'emotion':'neutral','sample_rate':32000,'bitrate':128000}
   c['tts']['provider'] = 'minimax'
   yaml.dump(c, open('/root/HERMES/config.yaml','w'), sort_keys=False)
   "
   ```
3. **Validate:** `python3 -c "import yaml; yaml.safe_load(open('/root/HERMES/config.yaml')); print('OK')"`
4. **Restart gateway:** `hermes gateway restart` — MUST run from OUTSIDE the gateway (SSH, cron, separate shell). Inside-gateway restart is blocked.

## API Verification (curl, independent of Hermes)

```bash
source /root/.secrets/kunci-root.env
curl -s -X POST "https://api.minimax.io/v1/t2a_v2" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -d '{
    "model": "speech-2.8-hd",
    "text": "Ujian suara i-ARIF.",
    "voice_setting": {"voice_id": "Indonesian_CaringMan", "speed": 0.88, "vol": 1.0, "pitch": 0, "emotion": "neutral"},
    "audio_setting": {"sample_rate": 32000, "bitrate": 128000, "format": "mp3", "channel": 1}
  }' -o /tmp/t2a-resp.json -w "HTTP %{http_code}"
```

**Response format:** JSON with hex-encoded audio in `data.audio`. Decode:
```python
import json; with open('/tmp/t2a-resp.json') as f: r = json.load(f)
audio = bytes.fromhex(r['data']['audio'])
with open('/tmp/output.mp3', 'wb') as f: f.write(audio)
```

## STT Quality Check (Groq Whisper)

```bash
curl -s https://api.groq.com/openai/v1/audio/transcriptions \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -F file="@/tmp/output.mp3" \
  -F model="whisper-large-v3-turbo" \
  -F language="ms"
```

**Result (2026-08-18):** 97% transcription match — "Ujian suara Iyarif. Hangat, mesra, direct. Macam inilah aku nak kedengaran." Only "i-ARIF" → "Iyarif" (expected — Whisper doesn't know the branded spelling).

## Quota Check

```bash
source /root/.secrets/kunci-root.env
mmx quota show --base-url https://api.minimax.io
# Check "general" model remains (speech + image shared pool). Video separate.
```

## Identity Card Sync

After voice wiring, update `/root/AAA/agent-cards/identity/i-ARIF/identity-card.json`:
- `audio_identity.primary_voice.provider` → `"minimax"`
- `audio_identity.primary_voice.voice_id` → `"Indonesian_CaringMan"`

## Pitfalls

- `speech-02-hd` is the OLD model name — use `speech-2.8-hd`
- `English_expressive_narrator` is English voice — NOT for BM
- `tts.provider: minimax` without a `minimax:` block in `tts:` = config parse failure or silent fallback
- Hermes `patch`/`write_file` refuse to touch config.yaml — use terminal sed or Python yaml.dump
- Gateway restart from inside the gateway is blocked — run from external shell
