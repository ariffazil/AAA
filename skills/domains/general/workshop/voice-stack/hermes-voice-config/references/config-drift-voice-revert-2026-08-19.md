# Config Drift Voice Revert — 2026-08-19

## What happened

Arif reported voice output did not sound like Siti Nurhaliza. Audio F0 analysis: 174 Hz median — confirmed V5 (designed voice, retired), not V8 (production clone, 239 Hz).

## Root cause chain

1. `tts.provider` was `minimax` (direct API call), not `i-arif-sovereign` (pipeline). The pipeline with V8 + DSP was completely bypassed.
2. `tts.minimax.voice_id` was `iarif-sovereign-v5` (retired designed voice, F0 170 Hz), not `i-ARIF-20260819T084602` (V8).
3. Pipeline script had `set -uo pipefail` — the `set -u` (nounset) interacted with env file forward-references (`BAILIAN_TOKEN_PLAN_API_KEY` referencing `QWEN_INDIVIDUAL_API_KEY` before it was defined), causing the pipeline to fail silently before Stage 1.

## How did config drift happen?

The V5 voice_id and `provider: minimax` were set during the voice_design session (2026-08-19 15:10 MYT). When V8 was sealed later (2026-08-19 16:07 MYT), the pipeline script was updated to default to V8, but `config.yaml` was never re-patched to switch `tts.provider` to `i-arif-sovereign`. The config and pipeline diverged.

**This is a systemic risk.** Any session that sets `tts.provider` or `tts.minimax.voice_id` for testing/development creates drift if not explicitly reverted.

## Prevention

- After ANY change to `tts.provider` or `tts.minimax.voice_id`, verify the full chain: provider → pipeline → voice_id → DSP → F0 output.
- The canonical production state is documented in `hermes-voice-config` SKILL.md under "Canonical unified default."
- Config drift detection: the F0 fingerprint table in `hermes-voice-config` provides a quick reality check. If audio F0 doesn't match expected band, check config first.

## Files changed in fix

| File | Change |
|---|---|
| `~/.hermes/config.yaml` line 807 | `provider: minimax` → `provider: i-arif-sovereign` |
| `~/.hermes/config.yaml` line 831 | `voice_id: iarif-sovereign-v5` → `voice_id: i-ARIF-20260819T084602` |
| `/root/AAA/engines/iarif_tts_pipeline.sh` line 16 | `set -uo pipefail` → `set -o pipefail` |
| `/root/AAA/engines/iarif_tts_pipeline.sh` lines 25-30 | Added `set +u` / `set -u` wrapper around env source |

## Verification

Post-fix pipeline test: F0 median 243.8 Hz (target band 225–255 Hz). Confirmed V8 through full pipeline.

---

## Second incident — 2026-08-19 23:30 MYT (voice.tts_provider_default drift)

### What happened

Arif reported voice output still doesn't sound like Siti Nurhaliza, hours after the first fix. Investigation revealed a **second routing path** that was never fixed.

### Root cause

The first fix (2026-08-19 16:46 MYT) corrected `tts.provider` and `voice_id` in the `tts:` section. But auto-voice-reply reads `voice.tts_provider_default` (a SEPARATE config key in the `voice:` section), which was still set to `minimax`. This routed auto-voice-reply to the built-in MiniMax handler → `tts.minimax.voice_id: iarif-sovereign-v5` (old V5, never updated).

**Key insight:** `tts.provider` and `voice.tts_provider_default` are independent. The first controls agent-initiated `text_to_speech` calls; the second controls the gateway's auto-voice-reply. Both must point to `i-arif-sovereign`.

### Additional factor: gateway not restarted after config change

Last gateway start: 14:29 MYT. V8 seal: 16:46 MYT. The gateway was never restarted, so even if `tts.provider` had been corrected in config.yaml, the running gateway process would still use the old config. Config is read at boot only.

### Evidence trail

- Audio file: 1,038,580 bytes (1014 KB) for 181s = ~5.7 KB/s (raw MiniMax, no DSP compression)
- Compare: V8 pipeline output ~49 KB for short clip (DSP-processed WAV is denser)
- Gateway logs: no TTS entries after 15:37 (log buffer not flushed, but `voice.tts_provider_default: minimax` confirmed in config)
- Pipeline test: V8 pipeline works correctly (F0 median 242.8 Hz, in-band)

### Fix required

1. Change `voice.tts_provider_default: minimax` → `voice.tts_provider_default: i-arif-sovereign` in config.yaml
2. Restart gateway to pick up both changes
3. Verify: auto-voice-reply should now route through the pipeline

### Prevention update

After ANY voice config change, check BOTH:
```bash
grep -E 'tts_provider_default:|^  provider:' ~/.hermes/config.yaml
```
And restart gateway after config changes (config is read at boot only).
