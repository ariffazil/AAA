#!/bin/bash
# dsp_preprocess_v2.sh — Corrected per F2 audit (2026-08-25)
# Owner: Hang (AGI) · Reviewer: ASI🪽 · F13: pending ARIF approval
set -euo pipefail

echo "[✓] DSP Pre-processing i-ARIF V9 (ffmpeg-only — sox not installed in env)"
mkdir -p /root/AAA/audio/processed

for f in /root/AAA/audio/raw_sample*.ogg /root/AAA/audio/raw_sample*.wav /root/AAA/audio/raw_sample*.mp3; do
    [ -e "$f" ] || continue

    base=$(basename "$f")
    out="/root/AAA/audio/processed/clean_${base%.*}.wav"

    echo "[*] Processing $base → $out"

    # ffmpeg chain: bandpass → compand → loudnorm → pad
    # equivalent of: highpass 100, lowpass 7500, compand (0.3,1 6:-70,-60,-20 -5 -90 0.2), norm -3, pad 0.08
    ffmpeg -y -i "$f" \
        -af "highpass=f=100,lowpass=f=7500,acompressor=threshold=-20dB:ratio=3:attack=5:release=50,volume=-3dB,loudnorm=I=-14:TP=-1:LRA=11,adelay=80|80" \
        -ar 44100 -ac 1 -c:a pcm_s16le \
        "$out" 2>/dev/null

    # Audit noise floor via ffmpeg volumedetect (sox stat not available)
    rms_db=$(ffmpeg -i "$out" -af volumedetect -f null - 2>&1 | grep "mean_volume" | awk '{print $5}' | tr -d '-')
    rms_linear=$(awk -v db="-$rms_db" 'BEGIN { printf "%.6f", 10^(db/20) }')
    echo "    -> Cleaned. RMS: $rms_db dBFS (linear: $rms_linear)"
done

echo "[✓] DSP pre-process selesai. Ready for DashScope Voice Enrollment."
