#!/bin/bash
# A/B: base F5-TTS vs mesolitica Malaysian-F5-TTS-v3 finetune
# Same reference, same ref_text, same gen_text. ONLY the checkpoint differs.
set -a; source /root/.secrets/kunci-root.env 2>/dev/null; set +a

cd /root/AAA/engines/f5tts || exit 1
REF="/root/AAA/engines/f5tts/reference-10s.wav"
REFTXT="Pergi apa lagi? Pergi-pergi berangga? Memanglah suri rumah yang suka membeni Tapi, menang memakai tak? Bukanlah, pakai tu"
GENTXT="Kami sembang pasal kerja, pasal anak, pasal kampung. Nyanyi lagu lama, syukur masih ada."
OUT="/root/AAA/engines/f5tts/ab_test"
CKPT="/root/AAA/engines/f5tts/checkpoints/bm_v3_infer_ema.pt"   # clean ema-only, 1.35GB, built 2026-09-29
mkdir -p "$OUT"
echo "$GENTXT" > "$OUT/gen_text.txt"

echo "############ PHASE 1: BASE F5-TTS (SWivid F5TTS_v1_Base) ############"
date -Is
./venv/bin/python f5_local_render.py "$REF" "$REFTXT" "$GENTXT" "$OUT/base.wav" 32 2>&1 | tail -20
echo "BASE_EXIT=$?"

echo
echo "############ PHASE 2: V3 Malaysian-Emilia finetune ############"
date -Is
F5_CKPT="$CKPT" ./venv/bin/python f5_local_render.py "$REF" "$REFTXT" "$GENTXT" "$OUT/v3.wav" 32 2>&1 | tail -25
echo "V3_EXIT=$?"

echo
echo "############ PHASE 3: VERIFY ############"
date -Is
for f in base v3; do
  echo "--- verify $f.wav"
  ./venv/bin/python /root/AAA/engines/voice_render_verify.py \
      --audio "$OUT/$f.wav" --text "$OUT/gen_text.txt" --ref "$REF" --json 2>&1 | tail -25
  echo "VERIFY_${f}_EXIT=$?"
done

echo
echo "############ FILES ############"
ls -la "$OUT"
date -Is
echo "AB_TEST_DONE"
