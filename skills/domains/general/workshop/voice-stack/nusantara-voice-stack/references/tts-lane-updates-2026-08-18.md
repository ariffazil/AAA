# TTS Lane Updates (probed 2026-08-18)

## mmx speech base-url fix

`mmx config` default `base_url=https://api.minimax.io/anthropic` makes `mmx speech synthesize`, `mmx speech voices`, and `mmx quota show` return HTTP 404. Not quota, not auth — routing misconfig. Fix: `--base-url https://api.minimax.io` on the command.

```bash
mmx speech synthesize --base-url https://api.minimax.io --model speech-2.8-hd \
  --voice English_ManWithDeepVoice --speed 0.9 --text "..." --out v.mp3 --non-interactive
```

~8s clip in ~5s wall. Deep/dominant male picks: `English_ManWithDeepVoice` (verified), `English_magnetic_voiced_man`, `English_ImposingManner`, `English_MatureBoss`. Mixed BM+EN text speaks fine. This is the "berat/dominan" lane — for persona weight, NOT for Malay realism (edge-tts ms-MY-OsmanNeural still owns BM realism per §1 ceiling doctrine).

## Qwen qwen-audio-3.0-tts-plus — no Malay

Token-plan seat model has NO Malay voice; Chinese (Mandarin) + English only. Voice params are lowercase-no-underscore:
- male flagship: `longanlufeng` (bright cheerful) — verified working on team-owner seat
- female flagship: `longanlingxin`
- FAIL with `[cosyvoice:]Engine error [411]`: old CosyVoice names (longxiaochun, longshu, longlaotie), Qwen3-TTS names (Cherry, Ethan, Serena, Chelsie), v3.6-suffixed voices (longchuanshu_v3.6, loongjohn — flash-only)
- Catalog: https://docs.qwencloud.com/api-reference/speech-synthesis/qwen-audio-tts/voice-list (the qwen-tts/voice-list page is the Qwen3-TTS catalog — different model family)

## Seat quota flavours

`Throttling.AllocationQuota` 429 on `BAILIAN_TOKEN_PLAN_API_KEY`/`QWEN_ARIFOS_API_KEY` (same key) can be WEEKLY (message names reset datetime) while `QWEN_TEAM_OWNER_API_KEY` still has pool. Same for image gen and TTS. Ladder before declaring dead.
