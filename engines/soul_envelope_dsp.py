#!/usr/bin/env python3
"""i-ARIF Soul Envelope DSP — Siti qualia from first principles.

Builds the acoustic envelope of 'sopan santun' from parameters, NOT from
any person's waveform. F9-compliant: reference = documented qualia
(soft attack, high HNR, singer's formant, gentle vibrato), source voice =
original synthetic Malay (YasminNeural base).

Envelope spec (from the qualia matrix):
  - Attack: sigmoidal ramp ~60ms (no abrupt glottal transient) — sopan entry
  - Release: 180ms soft decay
  - HNR polish: gentle high-shelf +3dB @ 2.9kHz (singer's formant clarity)
  - Breath noise floor: -40dB gate on silence regions (clean, tenang)
"""
import sys
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt, sosfreqz

SRC = sys.argv[1] if len(sys.argv) > 1 else "/root/AAA/audio/processed/i-arif-v8-yasmin-soft_sopan.mp3"
DST = sys.argv[2] if len(sys.argv) > 2 else "/root/AAA/audio/processed/i-arif-soul-v1.wav"

y, sr = sf.read(SRC, dtype="float32")
if y.ndim > 1:
    y = y.mean(axis=1)

n = len(y)
t = np.arange(n) / sr

# --- 1. ATTACK: sigmoidal ramp, ~60ms (sopan santun entry) ---
attack_samps = int(0.06 * sr)
attack = np.ones(n)
if attack_samps < n:
    x = np.linspace(-6, 6, attack_samps)
    attack[:attack_samps] = 1.0 / (1.0 + np.exp(-x))

# --- 2. RELEASE: soft 180ms cosine decay ---
release_samps = int(0.18 * sr)
release = np.ones(n)
if release_samps < n:
    release[-release_samps:] = 0.5 * (1 + np.cos(np.linspace(0, np.pi, release_samps)))

# --- 3. HNR POLISH: bandpass 80Hz-12kHz + singer's formant shelf ---
sos_hp = butter(4, 80 / (sr / 2), btype="high", output="sos")
sos_lp = butter(4, min(12000, sr / 2 - 100) / (sr / 2), btype="low", output="sos")
y = sosfilt(sos_hp, sosfilt(sos_lp, y))

# Singer's formant emphasis: gentle resonance at 2.9kHz
sos_f3 = butter(2, [2700 / (sr / 2), 3200 / (sr / 2)], btype="band", output="sos")
f3_band = sosfilt(sos_f3, y)
y = y + 0.35 * f3_band  # +3dB effective in the 2.9-3.1kHz band

# --- 4. BREATH FLOOR: soft noise gate at -40dB (tenang, no hiss) ---
frame = int(0.02 * sr)
env = np.sqrt(np.convolve(y ** 2, np.ones(frame) / frame, mode="same"))
floor = 10 ** (-40 / 20)
gate = np.clip((env - floor * 0.5) / (floor * 2), 0.15, 1.0)
# smooth the gate to avoid clicks
gate = np.convolve(gate, np.ones(frame) / frame, mode="same")
y = y * gate

# --- 5. Apply envelope, normalize to -3dB headroom ---
y = y * attack * release
peak = np.max(np.abs(y))
if peak > 0:
    y = y * (0.707 / peak)

sf.write(DST, y, sr, subtype="PCM_16")
print(f"SOUL DSP OK: {DST} ({n / sr:.1f}s @ {sr}Hz)")
