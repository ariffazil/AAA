# MiniMax Indonesian Voices for BM TTS — Proven 2026-08-18

## Discovery

MiniMax speech-2.8-hd has Indonesian voices that handle BM (Bahasa Malaysia) text naturally. Indonesian and Malay are mutually intelligible — phonemes, rhythm, and intonation map closely enough that Indonesian voices sound natural reading BM text.

This is the first **32kHz, RM0-subscription, no-GPU** path to BM voice that passes the "sounds human" bar. Previously, the only path to engine-level BM realism was F5-TTS on Runpod (CC-BY-NC-4.0, requires GPU, pending F13 GO).

## Working voices (tested live, 2026-08-18)

All voices confirmed working with BM text via `mmx speech synthesize --base-url https://api.minimax.io --model speech-2.8-hd`.

| Voice ID | Vibe | Recommended speed | Best for |
|---|---|---|---|
| `Indonesian_CaringMan` | Warm, caring male | 0.9 | Companion, narration, conversational |
| `Indonesian_BossyLeader` | Dominant, commanding male | 0.85 | Authority, fitness, motivational |
| `Indonesian_DeterminedBoy` | Young, energetic male | 1.0 | Casual, upbeat |
| `Indonesian_ReservedYoungMan` | Quiet, thoughtful male | 0.9 | Reflective, calm |
| `Indonesian_SweetGirl` | Sweet, gentle female | 1.0 | Friendly, warm |
| `Indonesian_CharmingGirl` | Charming, expressive female | 1.0 | Conversational |
| `Indonesian_CalmWoman` | Calm, mature female | 0.9 | Narration, professional |
| `Indonesian_ConfidentWoman` | Confident, assertive female | 0.95 | Business, direct |
| `Indonesian_GentleGirl` | Gentle, soft female | 1.0 | Soothing, caring |

## Invocation

```bash
source /root/.secrets/kunci-root.env
mmx speech synthesize --base-url https://api.minimax.io \
  --model speech-2.8-hd \
  --voice Indonesian_CaringMan \
  --text "Aku nak kau tengok ni. Lagi besar, lagi sado. Badan ni ditempa dengan peluh dan darah." \
  --speed 0.9 \
  --out /tmp/test_bm_indo.mp3 \
  --non-interactive
```

## Critical: mmx CLI base-url

The mmx CLI default `base_url` points to `https://api.minimax.io/anthropic` (configured in `/root/.mmx/config.json`). This is the **text/chat** endpoint. The speech and image endpoints live at `https://api.minimax.io` (no `/anthropic` suffix). Always override:

```bash
mmx speech synthesize --base-url https://api.minimax.io ...
mmx image generate --base-url https://api.minimax.io ...
```

Without `--base-url`, both speech and image return HTTP 404.

## Why this beats edge-tts

| Dimension | MiniMax speech-2.8-hd + Indonesian | edge-tts ms-MY-OsmanNeural |
|---|---|---|
| Sample rate | 32kHz | 24kHz |
| Voice variety | 9 Indonesian voices (5 male, 4 female) | 2 voices (1 male, 1 female) |
| Emotional range | Natural warmth, authority, playfulness | One-style "Friendly Positive" formal |
| BM text | Works directly — phonemes map 1:1 | Works (native) |
| Speed control | Fine-grained (--speed 0.85-1.0) | Rate percentage |
| Cost | RM0 (Token Plan subscription) | Free |

## Why this beats F5-TTS (for production use)

- **Available NOW** — no Runpod GPU, no F13 GO, no US$10 top-up
- **Zero setup** — mmx CLI installed, MINIMAX_API_KEY wired
- **Deterministic** — same text + voice = same output; no reference speaker needed
- **No license issues** — F5-TTS is CC-BY-NC-4.0 (non-commercial)

F5-TTS with Arif's own voice clone remains the ultimate target (see §4 in SKILL.md), but Indonesian voices are the **production-ready interim** that closes the "fake voice" gap TODAY.

## Limitations

- **Not native BM** — subtle accent differences exist (Indonesian "e" pronunciation vs BM, some vowel shifts). Most listeners won't notice; linguists will.
- **No Penang loghat** — "lah", "wei", "habis" pronounced in Indonesian phonemes, not Penang cadence.
- **No code-switch** — English words in BM text get Indonesian-accented English, not Malaysian English.
- **Quota** — MiniMax Token Plan weekly limit applies. HTTP status code 2056 = quota reached (NOT auth failure); resets Sunday.

## Proven prompt patterns for BM

Short, punchy BM text works best. Avoid long sentences without punctuation — the voice needs natural pause points.

**Good:** "Aku nak kau tengok ni. Lagi besar, lagi sado. Badan ni ditempa dengan peluh dan darah. Bukan untuk show-off."

**Bad:** "Aku nak kau tengok ni lagi besar lagi sado badan ni ditempa dengan peluh dan darah bukan untuk show-off sebab aku disiplin tak pernah miss satu sesi pun"

Use periods and commas generously. The Indonesian voices interpret BM punctuation the same way as Indonesian — it works.

## Seat quota

MiniMax Token Plan weekly quota applies. The `MINIMAX_API_KEY` in kunci-root.env authenticates against `api.minimax.io`. If you see `status_code: 2056` or `Token Plan usage limit reached` — quota exhausted, wait for Sunday reset. This is NOT an auth failure.

## Related

- SKILL.md §3 — TTS Provider Lane Map
- SKILL.md §4 — F5-TTS breakthrough path (ultimate target)
- `creative/minimax-cli` — mmx CLI usage
- `media/tts-edge-fallback` — edge-tts fallback when MiniMax quota exhausted
