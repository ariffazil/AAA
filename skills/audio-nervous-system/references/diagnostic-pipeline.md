# Diagnostic Pipeline — Audio Nervous System Setup & Verification

> Forged 2026-08-13 by Hermes Bridge. Deterministic probes for verifying all layers of Telinga architecture.

## Prerequisites Installation

```bash
# Core librosa (Python 3.13 compatible)
pip install librosa soundfile numpy scipy

# A-FORGE parselmouth layer (separate from core)
pip install parselmouth

# FFmpeg for audio I/O
apt-get install -y libsndfile1-dev ffmpeg
```

### Critical: Numba Segfault Workaround

On Python 3.13 + numpy 2.4.6, these librosa functions CRASH via numba extension modules:
- `onset_detect()` → Segmentation fault
- `peak_pick()` → Segmentation fault
- `chroma_cqt()` → Segmentation fault
- `beat_track()` → Segmentation fault

**Safe paths to use:**
- `librosa.pyin()` for pitch estimation (F0)
- `librosa.feature.rms()` for energy
- `librosa.feature.zero_crossing_rate()` for speech rate proxy
- `librosa.feature.spectral_centroid()` for brightness/timbre
- `librosa.load()` for audio loading/decoding

Never use onset_detect or peak_pick in production. They will crash with `core dumped`.

## Layer 1 Verification Script

```python
"""Verify voice_state.py extraction works on sample audio."""
import sys
sys.path.insert(0, '/root/hermes-agent-dev')
from tools.voice_state import extract_voice_state
import os

test_files = [
    "/usr/local/lib/hermes-agent/profiles/aaa-hermes/cache/audio/audio_34d3639cab5e.mp3",
    "/tmp/tts-bench/osman_deeper.ogg",
]

for path in test_files:
    if not os.path.exists(path):
        print(f"SKIP: {path} not found")
        continue
    
    features = extract_voice_state(path)
    
    if isinstance(features, dict) and len(features) > 0:
        expected_fields = ["pitch_mean_hz", "energy_rms_mean_db", "pause_density"]
        missing = [f for f in expected_fields if f not in features]
        
        if missing:
            print(f"⚠️ {path}: Missing fields: {missing}")
        else:
            print(f"✅ {path}: {len(features)} features extracted")
            for k, v in sorted(features.items()):
                if isinstance(v, float):
                    print(f"   {k}: {v:.6f}")
    else:
        print(f"❌ {path}: Failed to extract features")
```

Run: `python3 verify_voice_state.py`
Expected: All test files show ✅ with 14 features each.

## Layer 2 Verification Script

```python
"""Verify A-FORGE audio ingest chain works end-to-end."""
import os
import json

checks = []

# Check 1: forge_audio_ingest.py exists and imports
try:
    sys.path.insert(0, '/root/A-FORGE')
    from tools.forge_audio_ingest import ingest_audio_event
    checks.append(("forge_audio_ingest import", True))
except ImportError as e:
    checks.append(("forge_audio_ingest import", False))
    print(f"FAIL: forge_audio_ingest import: {e}")

# Check 2: state_aware_tts.py exists
if os.path.exists("/root/A-FORGE/audio/state_aware_tts.py"):
    checks.append(("state_aware_tts.py exists", True))
else:
    checks.append(("state_aware_tts.py exists", False))

# Check 3: audio_watcher.py exists
if os.path.exists("/root/A-FORGE/audio/audio_watcher.py"):
    checks.append(("audio_watcher.py exists", True))
else:
    checks.append(("audio_watcher.py exists", False))

# Check 4: Qdrant collection arifos_audio_memory accessible
try:
    from qdrant_client import QdrantClient
    client = QdrantClient("localhost", port=6333)
    collections = client.get_collections()
    has_collection = any("arifos_audio_memory" in c.name for c in collections.collections)
    checks.append(("Qdrant arifos_audio_memory accessible", has_collection))
    if has_collection:
        print(f"✅ Qdrant collection 'arifos_audio_memory' exists with {collections.collections[0].points_count} points")
    else:
        print("⚠️ Qdrant running but arifos_audio_memory collection not found")
except Exception as e:
    checks.append(("Qdrart accessible", False))
    print(f"FAIL: Qdrant connection: {e}")

# Print summary
print("\n=== LAYER 2 VERIFICATION ===")
for name, passed in checks:
    status = "✅" if passed else "❌"
    print(f"{status} {name}")
```

Run: `python3 verify_layer2.py`
Expected: All four checks pass ✅.

## Config Drift Detection

STT providers wired in Python source but missing from config.yaml is a recurring pattern. Fix:

```bash
# Check what STT providers exist in Python source vs config
echo "=== SOURCE CODE STT PROVIDERS ==="
grep -r "stt\." /root/hermes-agent-dev/tools/transcription_tools.py | grep -oP '\w+(?=STT|\bsend_request\b)' | sort -u

echo "=== CONFIG.YAML STT PROVIDERS ==="
grep -A 20 "^stt:" /usr/local/lib/hermes-agent/profiles/aaa-hermes/config.yaml | grep -E '^\s+\w+:' | head -10
```

Fix missing entries by adding to config.yaml under `stt:` section:
```yaml
stt:
  enabled: true
  provider: openai
  groq:
    model: whisper-v3-turbo
  xai:
    model: grok-stt-v1
```

## Deployment Safety Protocol

A-FORGE has automated deployment pipeline that overwrites on-disk edits. SAFETY CHECKS:

1. **Always commit to git first**, then deploy. Manual disk edits WILL be wiped.
```bash
cd /root/A-FORGE
git add -A
git commit -m "feat(audio): [description]"
git push origin main  # triggers deployment pipeline pickup
```

2. **Check deployment status after changes:**
```bash
docker ps | grep aforge  # confirm container running
tail -f /var/log/aforge-deploy.log  # watch for deployment activity
```

3. **Post-deploy verification:** Verify critical files survived the deploy cycle.
```bash
ls -la /root/A-FORGE/tools/forge_audio_features.py
ls -la /root/A-FORGE/audio/audio_event_bridge.py
```

If files are gone after deploy → they weren't committed to source tree before deploy ran. Commit → wait for next deploy cycle.

## Voice Note Delivery Test

Generate and deliver test voice note through full stack:

```python
"""End-to-end test: generate voice note → process through stack → receive response."""
import asyncio
import edge_tts
import requests
import os

# Step 1: Generate test audio
text = "Woi hang dengar ni sikit nak tengok siapa suara paling real Arif pilih satu"
comm = edge_tts.Communicate(text, "ms-MY-OsmanNeural", pitch="-10Hz", rate="-5%")
await comm.save("/tmp/test_voice.mp3")

# Step 2: Verify it plays correctly (duration > 0)
import subprocess
result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", 
                        "-of", "default=noprint_wrappers=1:nokey=1", "/tmp/test_voice.mp3"],
                       capture_output=True, text=True)
duration = float(result.stdout.strip())
assert duration > 0, f"Generated audio has zero duration"

# Step 3: Send as Telegram voice note
bot_token = os.environ.get("ASI_ARIFOS_BOT_TOKEN")
chat_id = "267378578"  # Arif DM
api_base = f"https://api.telegram.org/bot{bot_token}"

with open("/tmp/test_voice.ogg", 'rb') as f:
    r = requests.post(f"{api_base}/sendVoice",
                      data={'chat_id': chat_id, 'caption': '[🎤] Test Voice'},
                      files={'voice': ('test.ogg', f, 'audio/ogg')})

assert r.status_code == 200, f"Telegram API failed: {r.status_code}"
print("✅ E2E voice note delivered successfully")
```

## Known Troubleshooting Cases

| Symptom | Cause | Fix |
|---|---|---|
| `Segmentation fault (core dumped)` on librosa | numba crashes on Python 3.13 + numpy 2.4.6 | Use only pyin, rms, zcr, spectral_centroid paths. Avoid onset_detect(), peak_pick() |
| `_load_mono_stereo() returned temp file deleted` | TemporaryDirectory context exited before parselmouth read | Keep all file operations inside same `with TemporaryDirectory()` block |
| `ModuleNotFoundError: audio` | sys.path missing parent directory | Add `Path(__file__).resolve().parent.parent / "tools"` to sys.path |
| On-disk edits vanish after redeploy | A-FORGE pipeline resets from main branch | Always commit to git first, then deploy |
| `NoAudioReceived` from edge_tts | Invalid pitch/rate parameters | `-10Hz pitch` + `-15% rate` may fail on some texts; try `-8Hz` + `-10%` |
| STT works in Python but not in config.yaml | Source code and config misaligned | Run config_drift_detection script above, add missing entries |
| VoiceState features not reaching WELL | Consumer wire not implemented yet | Gap 1 remains — implement `wire_voice_to_well(event)` in gateway/run.py |

## References
- Source skill: `/root/hermes-agent-dev/tools/voice_state.py`
- Wiring point: `/root/hermes-agent-dev/gateway/run.py` ~line 22340
- A-FORGE tools: `/root/A-FORGE/tools/`, `/root/A-FORGE/audio/`
- Config: `/usr/local/lib/hermes-agent/profiles/aaa-hermes/config.yaml`
