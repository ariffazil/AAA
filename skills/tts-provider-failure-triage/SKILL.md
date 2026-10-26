---
name: tts-provider-failure-triage
description: "Use when a TTS provider errors on credit or 404."
version: 1.0.0
author: Hermes
license: arifOS
tags: [tts, provider, credentials, diagnostics]
metadata:
  hermes:
    category: audio
    tags: [tts, provider, credentials, diagnostics]
    related_skills: [chunked-tts-render-integrity, voice-render-verification, voice-lane]
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# TTS Provider Failure Triage

## When to Use

- A TTS CLI reports `insufficient credit` and you are about to top up or swap accounts.
- A TTS CLI reports a bare `HTTP 404`.
- A render fails while the same account appears to have credit elsewhere.

A synthesis failure is usually one of four layers: which key is being read, what URL it is sent to,
which voice id is named, or the wallet. Diagnose in that order — cheapest first, and never re-mint a
voice to fix a billing or routing problem.

## 1. Which key is the CLI actually reading

Wrappers commonly resolve credentials from their own config file (for `mmx`: `~/.mmx/config.json`)
and ignore the shell environment entirely. A stale key in that file fails with `insufficient credit`
while a live key for the same provider sits exported and unused. Changing the env var does nothing.

Compare without ever printing a secret:

```bash
python3 - <<'EOF'
import json, os, hashlib
cfg = json.load(open('/root/.mmx/config.json'))
def h(k): return hashlib.sha256(k.encode()).hexdigest()[:12] if k else None
print('config', h(cfg.get('api_key','')), len(cfg.get('api_key','')))
for n in ('MINIMAX_API_KEY','MINIMAX_PLUGIN_API_KEY'):
    v = os.environ.get(n,'')
    print(n, h(v), len(v), 'same', v == cfg.get('api_key',''))
EOF
```

Different hashes mean the CLI and the shell are on different keys/accounts. Confirm which key has
credit with a direct call, then back the config up, write the working key in, `chmod 600`, and probe
with one short line before re-running the full script.

## 2. Endpoint shape — the fake 404

CLI wrappers take the **host only**; the direct call needs the full path:

- wrapper `--base-url`: `https://api.minimax.io`
- direct endpoint: `POST https://api.minimax.io/v1/t2a_v2`

Passing the full path to the wrapper doubles the path and the provider answers `HTTP 404`. That reads
like a dead route or a missing voice, and the natural (wrong) next move is to re-mint a clone — costing
the identity match already verified.

```bash
curl -s -X POST https://api.minimax.io/v1/t2a_v2 \
  -H "Authorization: Bearer $MINIMAX_API_KEY" -H "Content-Type: application/json" \
  -d '{"model":"speech-2.8-hd","text":"ujian","voice_setting":{"voice_id":"<id>","speed":0.95}}' \
  | head -c 200
```

A `data.audio` field means key, endpoint and voice id are all good — the fault is downstream (the
render loop, the gate, or delivery).

## 3. Read the error text literally

- `insufficient credit` → which key is being read (§1), then the wallet.
- bare `HTTP 404` → endpoint shape (§2), then a wrong path prefix.
- `voice not found` → wrong `provider_voice_id`: read the registry entry, do not re-mint.
- empty output with exit 0 → the wrapper swallowed the error; check whether the output file exists
  before trusting success.

## 4. After the fix, re-verify

A provider fix is not proven by the absence of an error. Render one short line, confirm the file
exists, confirm its duration, and only then re-run the long script — a chunked render that starts on a
half-fixed lane wastes minutes and can still ship truncated.
