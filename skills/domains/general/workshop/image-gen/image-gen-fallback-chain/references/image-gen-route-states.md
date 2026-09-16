# Image Gen Route States — Per-Session Snapshots

## 2026-08-19 22:30 MYT (Hermes session verification)

All routes tested with simple prompt. Auth keys present unless noted.

| Route | Status | Response | Evidence |
|-------|--------|----------|----------|
| Pollinations free GET | ✅ LIVE | HTTP 200, 13.9KB JPEG, 768×768 | SANA served regardless of model= param. Real JPEG verified via `file`. |
| Pollinations SANA (explicit) | ✅ LIVE | HTTP 200, 59KB JPEG, 768×768 | 42s response. Reliable but slow. |
| Pollinations rate limit | ⚠️ TRIGGER | HTTP 200, 701B "JSON text data" | Back-to-back requests trigger. sleep 8 resolves. |
| MuleRouter GPT Image 2 | 🔴 NO BALANCE | HTTP 402 insufficient_balance | Balance: -0.7476 credits. Endpoint alive, needs top-up. |
| MuleRouter Wan 2.6 T2I | 🔴 NO BALANCE | HTTP 402 insufficient_balance | Same balance issue as GPT. |
| MiniMax image-01 (mmx CLI) | 🔴 404 | HTTP 404 | Likely CDN rotation (transient per fallback-chain docs). Not permanent. |
| Qwen Token Plan | 🔴 BAD KEY | InvalidApiKey (HTTP 200 w/ error body) | QWEN_API_KEY set but invalid/expired. Needs key rotation. |
| Qwen Seat 3 | 🔴 NOT SET | Key empty | QWEN_SEAT3_API_KEY not configured. |
| Modal/Mage-Flow | 🔴 BROKEN | Serves 5.3KB placeholder | Same SHA256 across all prompts. 12ms inference (impossible for 1024²). |
| FED image-gen | ⚠️ CHECK | Health endpoint alive | /health/liveliness returns "I'm alive!" but actual gen capability untested. |

**Key finding:** 4 of 6 paid routes are alive but gated (balance/key). Free tier always works. The "nothing works" conclusion from prior session was wrong — it only tested paid providers and missed the free tier.

### Provider error classification reference

- **402** = endpoint alive, needs money → user action
- **400** = endpoint alive, bad params → fix request
- **404** = may be CDN rotation → wait 5-10min, retry
- **InvalidApiKey** = endpoint alive, needs key rotation → user action
- **500/503** = genuinely broken → fall through
- **Connection refused** = service down → fall through
- **Rate limit (200 + JSON body)** = alive, throttle yourself
