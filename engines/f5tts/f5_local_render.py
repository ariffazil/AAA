#!/usr/bin/env python3
"""F5-TTS local zero-shot clone render — NO API KEY, runs on CPU.

Usage: f5_local_render.py <ref_audio> <ref_text> <gen_text> <out_wav> [nfe_steps]

Why this file exists: the lane was declared (f5tts_pipeline.sh) but unbuildable —
the venv it sourced (/root/venv) did not exist and f5_tts was installed nowhere,
so the "offline clone" was a ghost capability. This is the runnable form.
Model weights are already cached at ~/.cache/huggingface (SWivid/F5-TTS).
"""
import os
import sys
import time

import soundfile as sf

os.environ.setdefault("HF_HOME", "/root/.cache/huggingface")


def _shim_torchaudio_load() -> None:
    """torchaudio>=2.9 delegates audio decoding to TorchCodec, which is only
    built against one exact torch build. On this box (8-CPU VPS, torch 2.11
    CPU wheel) the shipped torchcodec .so cannot load, so torchaudio.load()
    raises at call time. f5-tts only ever loads a local .wav reference, so a
    soundfile-backed load() is a complete substitute and removes the ABI
    coupling entirely."""
    import numpy as np
    import soundfile as sf
    import torch
    import torchaudio

    def load(path, *args, **kwargs):
        data, sr = sf.read(path, always_2d=True, dtype="float32")
        return torch.from_numpy(np.ascontiguousarray(data.T)), sr

    torchaudio.load = load


def main() -> int:
    if len(sys.argv) < 5:
        print(__doc__)
        return 2
    ref_audio, ref_text, gen_text, out_wav = sys.argv[1:5]
    nfe = int(sys.argv[5]) if len(sys.argv) > 5 else 32

    _shim_torchaudio_load()

    from f5_tts.api import F5TTS

    # Optional fine-tuned checkpoint (e.g. mesolitica/Malaysian-F5-TTS-v3).
    # Base F5-TTS is English/multilingual-dominant, so it carries English phonology into
    # BM — the reason the base-model BM render "does not feel Malay". A Malaysian-Emilia
    # finetune is the fix; it is an OPTION here, never a silent default swap.
    ckpt = os.environ.get("F5_CKPT")
    vocab = os.environ.get("F5_VOCAB")
    f5_kwargs = {"device": "cpu"}
    if ckpt:
        f5_kwargs["ckpt_file"] = ckpt
        if vocab:
            f5_kwargs["vocab_file"] = vocab

    t0 = time.time()
    tts = F5TTS(**f5_kwargs)
    t_load = time.time() - t0
    print(f"CKPT={ckpt or 'BASE(F5TTS_v1_Base from HF cache)'}")
    print(f"VOCAB={vocab or 'BASE'}")

    t1 = time.time()
    wav, sr, _ = tts.infer(
        ref_file=ref_audio,
        ref_text=ref_text,
        gen_text=gen_text,
        speed=1.0,
        nfe_step=nfe,
    )
    t_gen = time.time() - t1
    sf.write(out_wav, wav, sr)
    dur = len(wav) / sr
    print(f"MODEL_LOAD_S={t_load:.1f}")
    print(f"GEN_S={t_gen:.1f}")
    print(f"AUDIO_S={dur:.1f}")
    print(f"RTF={t_gen / dur:.1f}x_realtime_on_8cpu")
    print(f"OUT={out_wav}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
