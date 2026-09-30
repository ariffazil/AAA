#!/bin/bash
set -a; source /root/.secrets/kunci-root.env 2>/dev/null; set +a
cd /root/AAA/engines/f5tts || exit 1
V=./venv/bin/python
CK=/root/AAA/engines/f5tts/checkpoints

echo "### extract NON-EMA weights, wrapped so f5-tts' ema path uses them ###"
$V - <<'PY'
import torch, os
CK="/root/AAA/engines/f5tts/checkpoints"
ck = torch.load(f"{CK}/bm_v3_220000.pt", map_location="cpu", weights_only=True, mmap=True)
sd = ck["model_state_dict"]
# wrap with ema_model. prefix so load_checkpoint's use_ema path strips it back
wrapped = {f"ema_model.{k}": v for k, v in sd.items() if torch.is_tensor(v)}
out = f"{CK}/bm_v3_infer_noema.pt"
torch.save({"ema_model_state_dict": wrapped}, out)
print("entries:", len(wrapped), "bytes:", os.path.getsize(out))
PY
echo "EXTRACT_EXIT=$?"

echo "### render with NON-EMA weights ###"
date -Is
F5_CKPT="$CK/bm_v3_infer_noema.pt" $V f5_local_render.py \
  /root/AAA/engines/f5tts/reference-10s.wav \
  "Pergi apa lagi? Pergi-pergi berangga? Memanglah suri rumah yang suka membeni Tapi, menang memakai tak? Bukanlah, pakai tu" \
  "Kami sembang pasal kerja, pasal anak, pasal kampung. Nyanyi lagu lama, syukur masih ada." \
  /root/AAA/engines/f5tts/ab_test/v3_noema.wav 32 2>&1 | grep -E "CKPT=|VOCAB=|MODEL_LOAD_S|GEN_S|AUDIO_S|RTF=|OUT="

echo "### measure: where is the fundamental? ###"
$V - <<'PY'
import numpy as np, librosa, warnings
warnings.filterwarnings("ignore")
for p,l in [("/root/AAA/engines/f5tts/reference-10s.wav","REF"),
            ("/root/AAA/engines/f5tts/ab_test/base.wav","BASE"),
            ("/root/AAA/engines/f5tts/ab_test/v3.wav","V3-EMA"),
            ("/root/AAA/engines/f5tts/ab_test/v3_noema.wav","V3-noEMA")]:
    y, sr = librosa.load(p, sr=22050, mono=True)
    S = np.abs(librosa.stft(y, n_fft=8192, hop_length=512)); rms=S.mean(axis=0)
    keep = rms >= np.percentile(rms,70); avg = S[:,keep].mean(axis=1)
    fr = librosa.fft_frequencies(sr=sr, n_fft=8192); m=(fr>=60)&(fr<=400)
    band=avg[m]; bf=fr[m]; i=int(np.argmax(band))
    f0,_,_ = librosa.pyin(y, fmin=60, fmax=400, sr=sr)
    v=f0[~np.isnan(f0)]
    print(f"  {l:9} peak={bf[i]:6.1f}Hz  pyin_med={np.median(v):6.1f}  frac>180Hz={np.mean(v>180):.2f}")
PY
echo "NOEMA_TEST_DONE"
