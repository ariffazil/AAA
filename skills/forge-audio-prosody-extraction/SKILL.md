---
name: forge-audio-prosody-extraction
id: forge-audio-prosody-extraction
autonomy_tier: T1/T2
version: 1.0.0
description: "Prosody extraction for WELL. Trigger: prosody extract."
owner: AAA
risk_tier: low
knowledge_basis: {language: true}
platforms: [linux]
floor_scope: [F2, F7, F6, F9]
metadata:
  hermes:
    tags: [audio, prosody, extraction, wellbeing, voice-state]
    related_skills: [ai-media-generation-ops, well-assess-homeostasis]
license: MIT
author: Hermes / FI-008
---

# forge-audio-prosody-extraction

## When to Use
- Input: raw audio file (.mp3/.wav/.ogg) — transcript already produced by STT
- Need: physiological proxies (fatigue, urgency, stress_load, arousal) for WELL bridge
- Context: user sent voice note; system needs VoiceState metadata without running full TTS
- NOT for: TTS generation, music creation, audio editing, STT transcription

## Architecture Rule
Audio has TWO lanes in this federation:
1. **SENSING lane** (this skill): extract features FROM audio -> VoiceState -> WELL
2. **ACTUATION lane** (ai-media-generation-ops): generate TTS/music FROM audio -> Telegram/bot

NEVER mix sensing extraction with actuation generation. They serve different organs.

## Prerequisites
```bash
apt-get install -y ffmpeg libopus0   # audio decoding
pip install --break-system-packages -q librosa numpy         # acoustic analysis
# OR inside venv: /path/to/venv/bin/pip install librosa numpy
```

## Numbered Steps

### Step 1 - Validate input
Run: `ffprobe -v error -show_entries format=format_name,duration,bit_rate -of json <file>`
Verify format supported. Duration >0. Sample rate >= 8000 Hz.

### Step 2 - Load audio with librosa
```python
import librosa, numpy as np
Y, SR = librosa.load(filepath, sr=None)  # None preserves native sample rate
DURATION = len(Y) / SR
```

### Step 3 - Extract safe features (no numba-dependent calls)
```python
# Pitch (f0) - uses scipy only, no numba
f0 = librosa.pyin(Y, fmin=librosa.note_to_hz('C2'), 
                  fmax=librosa.note_to_hz('C7'), sr=SR)[0]
f0_clean = f0[~np.isnan(f0)]
pitch_mean = float(np.mean(f0_clean)) if len(f0_clean) else 0
pitch_std = float(np.std(f0_clean)) if len(f0_clean) else 0
pitch_range = float(max(f0_clean) - min(f0_clean)) if len(f0_clean) else 0

# Energy (RMS) - pure scipy
rms = librosa.feature.rms(y=Y)[0]
energy_max = float(np.max(rms))
energy_avg = float(np.mean(rms))

# Zero-crossing rate - pure scipy
zcr = librosa.feature.zero_crossing_rate(Y)[0]
zcr_mean = float(np.mean(zcr))
zcr_var = float(np.var(zcr))

# Pause density - pure numpy threshold comparison
threshold = energy_max * 0.1
pause_ratio = float(np.sum(rms < threshold) / len(rms))

# Spectral centroid - pure scipy
centroid = librosa.feature.spectral_centroid(y=Y, sr=SR)[0]
centroid_mean = float(np.mean(centroid))
```

### Step 4 - Map to semantic proxies
| Raw metric | Semantic proxy | Epistemic cap | Source |
|---|---|---|---|
| pitch_mean > 180 Hz | male register | INT 0.70 | acoustics |
| pitch_std > 50 Hz | moderate emotion | INT 0.65 | inference |
| energy_max/energy_avg > 3x | dynamic range | INT 0.70 | measurement |
| pause_ratio > 0.30 | deliberate pacing | INT 0.50 | inference* |
| zcr_mean > 0.15 | bright/tense speech | INT 0.60 | inference |

*\*pause ratio alone cannot distinguish cognitive deliberation from TTS breath-pauses. Cross-reference with transcript before WELL decisions.*

### Step 5 - Output JSONL
Each line must include: `event_id`, `timestamp`, `source_file`, `sha256_hash`,
all raw metrics, all semantic_proxies, and `confidence` per field.

### Step 6 - Store
Hash original audio -> SHA256. Store hash in VAULT999. Store VoiceState vector in Qdrant.
NEVER store the raw audio file itself - only the hash (F1 AMANAH).

## Pitfalls

### CRITICAL: Python 3.13 + numba segfault
`librosa.onset_detect()` segfaults on Python 3.13 due to numba JIT failure. Crashes ENTIRE pipeline.

Workaround - do NOT use any numba-dependent functions:
- ❌ `librosa.onset_detect()` - segfault
- ❌ `librosa.feature.chroma_stft()` - segfault  
- ❌ Any function importing numba internally
- ✅ `librosa.pyin()` - works (scipy-only)
- ✅ `librosa.feature.rms()` - works
- ✅ `librosa.feature.zero_crossing_rate()` - works
- ✅ `librosa.feature.spectral_centroid()` - works
- ✅ `librosa.get_duration()` - works

Full debug transcript in `references/python313-librosa-segfault.md`.

### STOPRULE: Paralinguistic claims are INT, never OBS
Paralinguistic inference from prosody is NEVER ground truth. Epistemic label `INT` with confidence cap 0.70. Cross-speaker inference cap is 0.50. Never treat extracted features as diagnostic indicators (medical, legal, etc.).

### F9 ANTI-HANTU: Don't claim empathy from audio
Detecting "stress" or "fatigue" in audio != performing empathy. Do NOT say "I hear you're stressed." That IS the dark pattern F9 forbids. Log `stress_proxy=high` in VoiceState payload; route to WELL for human-aware response instead.

## Verification Checklist
- [ ] ffprobe validates file before loading
- [ ] All extracted fields present in output
- [ ] Confidence caps applied correctly (0.70 max self, 0.50 cross-speaker)
- [ ] No numba-dependent functions called
- [ ] SHA256 computed for original file
- [ ] Output is valid JSONL

## Integration Points
- Wells bridge: VoiceState -> well_assess_homeostasis biometric overrides
- FED routing: activate asi-555-audio as audio-sense model alias
- Carry-forward: append extraction summary to carry_forward.json under open_loops

## See Also
- `ai-media-generation-ops` - actuation lane (TTS/music generation)
- `forge-audio-tts-routing` - TTS provider selection logic

DITEMPA BUKAN DIBERI - extraction ditempa, bukan diberi.