#!/bin/bash
set -e

echo "[✓] DSP Pre-processing i-ARIF V9 (Siti Sopan Formant Lock)..."
mkdir -p /root/AAA/audio/processed

for f in /root/AAA/audio/raw_sample*.ogg /root/AAA/audio/raw_sample*.wav; do
    [ -e "$f" ] || continue

    base=$(basename "$f")
    out="/root/AAA/audio/processed/clean_${base%.*}.wav"

    echo "[*] Processing $base → $out"

    # Bandpass (100Hz - 7.5kHz), Attack Smoothing & Dynamic Normalization
    # Note: Using pad to ensure attack/release envelopes match the design spec
    sox "$f" "$out" \
        remix 1 \
        highpass 100 \
        lowpass 7500 \
        compand 0.3,1 6:-70,-60,-20 -5 -90 0.2 \
        norm -3 \
        pad 0.08 0.08

    # Audit Noise Floor / RMS Level - Fixed regex to match SoX stat output
    rms=$(sox "$out" -n stat 2>&1 | grep "RMS amplitude" | awk '{print $3}')
    echo "    -> Cleaned. RMS Level: $rms"
done

echo "[✓] DSP pre-process selesai. Ready for DashScope Voice Enrollment."
