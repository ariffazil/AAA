# Sovereign Sound Stabilizer — Architecture & Pitfalls

**Forged:** 2026-08-19 · Engine: pyworld (WORLD vocoder)

## Architecture

Two-stage DECODE pipeline for i-ARIF voice:
1. **Stage 1 (Seed):** MiniMax speech-2.8-hd produces raw audio from voice_id (clone or design)
2. **Stage 2 (Lock):** WORLD vocoder decomposes → modifies F0 → re-synthesizes

```
raw.mp3 → ffmpeg f64le → WORLD dio+stonemask (F0 extraction)
                         → WORLD cheaptrick (spectral envelope sp)
                         → WORLD d4c (aperiodicity ap)
         → F0 rescale (median → target, default 239 Hz)
         → terminal pitch lift (+35 Hz, log-normal shape, last ~450ms)
         → WORLD synthesize (modified F0 + original sp + ap)
         → coda truncation (40ms amplitude ramp)
         → ffmpeg pcm_s16le → locked.wav
```

## Why NOT numpy/scipy

The naive DSP approach has two fatal flaws:

1. `output = filtered * envelope * sin(phase_mod)` — this REPLACES the speech waveform with a pure sine wave. All phonetic identity, all formant structure, all speaker identity is destroyed. The output is a tone, not a voice.

2. A bandpass filter `300–3400 Hz` removes the glottal source above 3 kHz and strips high formants. The voice loses consonant clarity, breath quality, and "presence."

WORLD correctly separates:
- **f0** (fundamental frequency / pitch) — what we modify
- **sp** (spectral envelope / formants) — what we preserve (speaker identity)
- **ap** (aperiodicity / noise component) — what we preserve (breath, consonants)

This is the LF (Liljencrants-Fant) glottal model family.

## Measured Results

| Seed source | Raw median F0 | After lock | In band? | STT |
|---|---|---|---|---|
| voice_design v6b | 205.7 Hz | 237.3 Hz | YES (225–255) | clean |
| voice_clone v7 (Arif self) | 170.7 Hz | 240.6 Hz | YES | perfect |
| MiniMax existing v4 | 218.4 Hz | 238.5 Hz | YES | clean |

## Terminal Pitch Lift (Northern Cadence)

Log-normal shaped envelope over last ~450ms of voiced speech:
```python
shape = exp(-((log(s + 0.08) + 1.2)^2) / 1.8)
```
Slow build, steep finish — pitch rises only at clause end.

## Coda Truncation

Final 40ms amplitude ramp: `ramp = linspace(1, 0, n_cut) ** 2`
Simulates abrupt glottal closure [ʔ]. Squared ramp avoids clicks.

## Install Pitfall

```bash
pip install pyworld --break-system-packages  # PEP 668 on this VPS
```

## Fail-Open Design

If Stage 2 crashes, raw MiniMax audio is delivered unchanged — voice presence > F0 precision.
