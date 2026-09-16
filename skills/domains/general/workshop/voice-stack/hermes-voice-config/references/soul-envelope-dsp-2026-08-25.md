# Soul Envelope DSP Path (2026-08-25)

## Proven working path for "soul of Melayu" voice work without impersonation.

### When to use this path

- Arif says "build the soul" of a Malay voice reference (Siti Nurhaliza, humble genius Melayu, etc.).
- F9 anti-hantu compliance required — no clone of living person's waveform.
- F13 consent NOT available — no recorded voice of named person to clone from.
- Arif explicitly rejects voice_design from prompt alone (proven 2026-08-25).

### Why this path exists

MiniMax voice_design with carefully crafted qualia prompt was tested 2026-08-25:

| Prompt dimension | Value |
|---|---|
| Qualia description | "Perempuan Melayu muda, lembut sopan, gemersik, sebut jelas" |
| F0 target | 237.3 Hz |
| Pitch setting | +6 |
| **Resulting F0** | **247 Hz (+4.1% from target)** |
| Acoustic metrics | All passed (voiced 82%, spectral centroid 1356 Hz) |
| **Arif verdict** | **"faill. nope. revert back"** |

Metrics landed. Soul did not. Voice_design synthesizes from prompt alone — no real human foundation underneath. The output passes every acoustic test but reads as AI-generated, not human.

### Working path components

#### 1. Base: `edge-tts ms-MY-YasminNeural`

Microsoft's Malay-specific neural model. **Key differentiator vs MiniMax/Qwen for Malay soul work**: native BM corpus, NOT Chinese-backbone with Malay adapter.

```bash
# Three prosody variants for testing
edge-tts --voice ms-MY-YasminNeural \
  --text "Salam Arif. Sistem arifOS dah sedia." \
  --rate=-15% --pitch=-5Hz --volume=+5% \
  --write-media /tmp/sopan.mp3    # soft_sopan variant (recommended base)
```

#### 2. DSP shaping: `soul_envelope_dsp.py`

Location: `/root/AAA/engines/soul_envelope_dsp.py`

Four-stage envelope (sopan santun qualia matrix):

| Stage | Parameter | Value | Acoustic effect |
|---|---|---|---|
| Attack | Sigmoidal ramp | 60 ms | Sopan entry, no abrupt glottal transient |
| Bandpass | Highpass + Lowpass | 80 Hz + 12 kHz | Clean signal, remove rumble + above-band noise |
| Singer's formant | Bandpass + additive | +3 dB @ 2.9–3.1 kHz | Gemersik clarity, voice cuts through |
| Breath floor | RMS gate | -40 dB | Tenang, no hiss in silence |
| Release | Cosine decay | 180 ms | Gentle landing |

```bash
python3 /root/AAA/engines/soul_envelope_dsp.py \
  /root/AAA/audio/processed/i-arif-v8-yasmin-soft_sopan.mp3 \
  /root/AAA/audio/processed/i-arif-soul-v1.wav
```

Output: 16-bit PCM WAV with sopan-santun envelope locked in.

#### 3. Verify before delivery

```bash
# F0 check (expect 200-260 Hz band for female Penang register)
python3 -c "
import librosa, numpy as np
y, sr = librosa.load('/root/AAA/audio/processed/i-arif-soul-v1.wav', sr=16000)
f0, _, _ = librosa.pyin(y, fmin=50, fmax=500, sr=sr)
f0v = f0[~np.isnan(f0)]
print(f'F0 median: {np.median(f0v):.1f} Hz')
print(f'Voiced: {100*np.sum(~np.isnan(f0))/len(f0):.0f}%')
"

# Spectral centroid check (expect 1200-2200 Hz for vocal range)
python3 -c "
import librosa, numpy as np
y, sr = librosa.load('/root/AAA/audio/processed/i-arif-soul-v1.wav', sr=16000)
print(f'Centroid: {np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)):.0f} Hz')
"

# OGG compression for Telegram voice bubble
ffmpeg -y -i /root/AAA/audio/processed/i-arif-soul-v1.wav \
  -c:a libopus -b:a 96k -ac 1 -ar 48000 \
  /tmp/i-arif-soul-v1.ogg
```

### Why Path C over Paths A and B

- **Path A (clone real audio → DSP):** Best quality, soul present. BUT requires F13 consent from the source. Use ONLY if Arif provides recorded voice of the named person.
- **Path B (voice design from prompt):** F9 clean, no consent needed. BUT Arif rejected on first listen — metrics hit, soul missing.
- **Path C (synthetic BM base + envelope shaping):** F9 clean, no consent needed, soul present via envelope qualia (sopan entry, gemersik formant, tenang breath floor). **This is the default.**

### V8 still production

Soul envelope path is an ADDITIONAL path, not a replacement. V8 (`i-ARIF-20260819T084602`) remains the production voice for personal continuity — cloned from makcik-padded.wav with DSP-stabilized F0 237 Hz. Soul envelope path is for when Arif wants "soul of Melayu" qualia WITHOUT cloning a specific person.

### Files this path touches

- `/root/AAA/engines/soul_envelope_dsp.py` — DSP engine
- `/root/AAA/audio/processed/i-arif-v8-yasmin-{baseline_solo,soft_sopan,measured_rasa}.mp3` — prosody variants
- `/root/AAA/audio/processed/i-arif-soul-v1.wav` — envelope-shaped output
- `/tmp/i-arif-soul-v1.ogg` — OGG for Telegram

### Future iterations

If Arif wants to refine:
- More sopan: increase attack ramp (80ms) + reduce breath gate floor (-50dB)
- More gemersik: increase singer's formant strength (+6dB instead of +3dB)
- Different base register: try `edge-tts --voice ms-MY-YasminNeural` with `--pitch=+5Hz` (closer to 237 Hz without post-DSP pitch shift)

Never escalate to Path B (voice design) without consent evidence from Arif that the metrics-hit-but-soul-missing pattern has resolved.