# Gemini API — Live Probe 2026-08-09

## Key
- `GEMINI_API_KEY` set in kunci-mas.env (prefix `AIzaSy...`, 39 chars)
- `GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai` (OpenAI-compat)
- Provider config: `auth.py:235`, `api_key_env_vars=("GOOGLE_API_KEY", "GEMINI_API_KEY")`

## Models available (50 total via GET /v1beta/models?key=KEY)

### Chat models (supports generateContent)
- gemini-2.5-flash ✅ (but 429 — free tier exhausted)
- gemini-2.5-pro (likely same 429)
- gemini-2.0-flash (deprecated June 2026)
- gemini-2.0-flash-001
- gemini-2.0-flash-lite-001
- gemini-2.5-flash-lite
- gemini-2.5-flash-image
- gemini-3-pro-preview
- gemini-3-flash-preview ✅ (WORKS — best free option)
- gemini-3.1-pro-preview
- gemini-3.1-flash-lite-preview
- gemini-3.1-flash-lite
- gemini-3.5-flash
- gemini-flash-latest
- gemini-flash-lite-latest
- gemini-pro-latest
- gemma-4-26b-a4b-it
- gemma-4-31b-it

### Non-chat (image/audio/embed/etc)
- gemini-2.5-flash-preview-tts
- gemini-2.5-pro-preview-tts
- gemini-3-pro-image-preview
- gemini-3-pro-image
- gemini-3.1-flash-image-preview
- gemini-3.1-flash-image
- gemini-3.1-flash-lite-image
- nano-banana-pro-preview

## Free tier limits (August 2026)

| Model | RPD | RPM | Notes |
|---|---|---|---|
| gemini-2.5-pro | 5 | 2 | Extremely tight |
| gemini-2.5-flash | 20 | 10 | Exhausts within one session |
| gemini-3-flash-preview | Higher | TBD | Preview quota — works reliably |
| gemini-3.5-flash | TBD | TBD | New, untested |

RPD = requests per day, RPM = requests per minute.
Resets at midnight Pacific Time.
Free tier data may be used to improve Google's models.
Not for EU/EEA/UK/Switzerland production use.

## Working probe commands

```bash
source /root/.secrets/kunci-mas.env

# Native Gemini API (works):
curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"Say hello"}]}]}'
# → ✅ "Hello! How can I help you today?"

# OpenAI-compat endpoint (also works):
curl -s "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions" \
  -H "Authorization: Bearer $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gemini-3-flash-preview","messages":[{"role":"user","content":"Say hello"}],"max_tokens":20}'
# → ✅ 200, valid response

# gemini-2.5-flash (rate limited):
curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"Say hello"}]}]}'
# → 429: "You exceeded your current quota"
#   quotaId: GenerateRequestsPerDayPerProjectPerModel-FreeTier
#   quotaValue: 20
#   retryDelay: 23s
```

## Hermes integration

- Provider already wired: `gemini` in `CANONICAL_PROVIDERS` at `models.py:1070`
- `_PROVIDER_LABELS["gemini"] = "Google AI Studio"`
- `PROVIDER_GROUPS["google"] = ("Google Gemini", ..., ["gemini"])` — grouped under "Google Gemini ▸"
- Curated models: `models.py:294` — missing `gemini-3-flash-preview`
- To use: `/model gemini-3-flash-preview --provider gemini --global`
- Or add to curated list in `_PROVIDER_MODELS["gemini"]`

## Deprecation schedule

| Model | Deprecation | Replacement |
|---|---|---|
| gemini-2.0-flash | June 1, 2026 | gemini-3.1-flash-lite |
| gemini-2.5-flash | Oct 2026 (est) | gemini-3.6-flash (GA Jul 2026) |
| gemini-2.0-flash-lite | June 1, 2026 | gemini-3.1-flash-lite |

## Cost (paid tier)

- gemini-2.5-flash: $0.30/1M input, $2.50/1M output
- gemini-2.5-pro: $7.00/1M input, $14.00/1M output (approx)
- Enable billing in Google AI Studio console
