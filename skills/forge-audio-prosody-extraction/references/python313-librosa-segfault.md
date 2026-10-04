# python313-librosa-segfault — Full Debug Transcript

## Context
Session: TELINGA P1 prototype (extract VoiceState from user voice note)
Python version: 3.13 (Ubuntu system Python)
librosa version: latest via pip --break-system-packages
Platform: Linux x86_64

## Symptoms
`librosa.onset_detect()` triggers segfault in numba JIT compilation. Crashes ENTIRE pipeline.

## Stack trace (abbreviated)
```
Fatal Python error: Segmentation fault
Current thread (most recent call first):
  numba/np/ufunc/gufunc.py line 263 in __call__
  librosa/util/utils.py line 1352 in peak_pick
  librosa/onset.py line 191 in onset_detect
```

## Root cause
Numba JIT compiler incompatible with Python 3.13 C API changes. Segfault during extension module init (`numba._helperlib`). Known issue across scipy-based audio libraries.

## Functions affected on Python 3.13
| Function | Status | Reason |
|---|---|---|
| `librosa.onset_detect()` | FAILS | Calls numba JIT |
| `librosa.feature.chroma_stft()` | FAILS | Uses numba internally |
| Any librosa function importing numba | FAILS | Extension load failure |
| `librosa.pyin()` | WORKS | Pure scipy backend |
| `librosa.feature.rms()` | WORKS | Pure scipy |
| `librosa.feature.zero_crossing_rate()` | WORKS | Pure scipy |
| `librosa.feature.spectral_centroid()` | WORKS | Pure scipy |
| `librosa.get_duration()` | WORKS | Pure CFFI |

## Workaround confirmed
All features work correctly when using ONLY scipy-backed librosa functions. No numba-dependent calls. Produces complete prosodic analysis minus onset/burstiness metrics.

## Verification script
Run this before any extraction attempt:
```bash
python3 -c "import librosa; Y,S=librosa.load('test.mp3'); print('pyin:',len(librosa.pyin(Y,sr=S)[0])); print('OK')"
```
Exit 0 = safe. Exit 139 = blocked on numba.

## Alternative if onset needed
Use Python 3.12 venv instead of 3.13 where numba works:
```bash
uv venv --python 3.12 .venv && uv pip install librosa && ./venv/bin/python script.py
```

## Session evidence
- Failed script: `/tmp/hermes_sandbox_w924y3ks/script.py`
- Numba loaded extensions: 142 total at crash time
- Platform: Linux x86_64 Ubuntu 24.x