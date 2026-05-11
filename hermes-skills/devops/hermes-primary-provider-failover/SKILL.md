---
name: hermes-primary-provider-failover
description: Diagnose Hermes Telegram silence caused by broken upstream model auth, then fail over primary model safely.
trigger:
  - Hermes Telegram connected but not replying
  - Kimi/Moonshot key suspected broken
  - switch Hermes primary provider
  - gateway looks healthy but inference is failing
  - Hermes appears deaf in groups
version: 1.1.0
---

# Hermes Primary Provider Failover & Full Diagnostic

Use this when Hermes looks alive on Telegram but replies are failing, especially when `config.yaml` points at `kimi-coding` / Moonshot.

## Key lesson

`gateway_state.json` showing Telegram `connected` does **not** mean Hermes can actually answer. Transport can be healthy while the primary inference provider is dead or unauthorized.

Also, Hermes has two different config concepts that are easy to confuse:
- `model.fallback` is a display/legacy routing hint
- actual automatic provider failover is driven by `fallback_providers:` (or legacy `fallback_model:`)

If you want real failover, populate `fallback_providers:` with explicit `{provider, model}` entries. Do not rely on `model.fallback` alone.

One more gotcha: Copilot and MiniMax credentials may already exist in `~/.hermes/auth.json` under `credential_pool` even when `providers: {}` is empty in `config.yaml`.

---

## Phase 1 — Full Diagnostic Chain

### 1) Confirm Telegram transport first
```bash
python3 - <<'PY'
import json, os
p=os.path.expanduser('~/.hermes/gateway_state.json')
print(json.load(open(p)))
PY
```
If Telegram is `connected`, move on to provider auth. Do **not** stop at transport health.

### 2) Inspect current model + provider config
```bash
python3 - <<'PY'
import yaml, os
p=os.path.expanduser('~/.hermes/config.yaml')
cfg=yaml.safe_load(open(p))
print("model:", cfg.get('model'))
print("providers:", cfg.get('providers'))
print("toolsets:", cfg.get('toolsets'))
print("fallback_providers:", cfg.get('fallback_providers'))
PY
```

Watch for these bad patterns:
```yaml
# Bad: provider exists but no matching block under `providers:`
model:
  provider: kimi-coding
# Bad: fallback points to a provider that isn't configured
  fallback: openai/gpt-4o
# Bad: only 2 toolsets enabled
  fallback: minimax/MiniMax-M2.7
```

### 3) Test ALL provider API keys live

Run this single script to test every key in `.env`:

```bash
python3 - <<'PY'
import os, requests

def test_key(name, key, url, headers):
    if not key or len(key) < 10:
        print(f"{name}: EMPTY/MISSING")
        return
    try:
        r = requests.get(url, headers=headers, timeout=10)
        print(f"{name}: {r.status_code} {'OK' if r.status_code == 200 else 'FAIL'}")
    except Exception as e:
        print(f"{name}: ERROR {e}")

env = lambda k: os.popen(f'grep ^{k}= ~/.hermes/.env | cut -d= -f2').read().strip()

test_key("Kimi/Moonshot", env("KIMI_API_KEY"), "https://api.moonshot.cn/v1/models",
         {"Authorization": f"Bearer {env('KIMI_API_KEY')}"})

test_key("MiniMax", env("MINIMAX_API_KEY"), "https://api.minimax.chat/v1/models",
         {"Authorization": f"Bearer {env('MINIMAX_API_KEY')}"})

test_key("Anthropic", env("ANTHROPIC_API_KEY"), "https://api.anthropic.com/v1/models",
         {"x-api-key": env("ANTHROPIC_API_KEY"), "anthropic-version": "2023-06-01"})

test_key("OpenAI", env("OPENAI_API_KEY"), "https://api.openai.com/v1/models",
         {"Authorization": f"Bearer {env('OPENAI_API_KEY')}"})

test_key("OpenRouter", env("OPENROUTER_API_KEY"), "https://openrouter.ai/api/v1/auth/key",
         {"Authorization": f"Bearer {env('OPENROUTER_API_KEY')}"})
PY
```

Interpretation:
- `200 OK` → key is valid, provider is usable
- `401` / `403` → key expired or revoked → remove or rotate
- `EMPTY/MISSING` → `.env` has no value → remove from config or get new key

### 4) Check Ollama local fallback
```bash
curl -s --max-time 5 http://ollama:11434/api/tags 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print('models:', len(d.get('models',[])))" || echo "ollama unreachable"
```
If Ollama is unreachable and it's configured as a fallback, local inference is dead.

### 5) Check Hermes Docker container health
```bash
docker inspect hermes-agent --format='{{.State.Health.Status}} {{.State.Status}}' 2>/dev/null || echo "no hermes-agent container"
```
If `unhealthy`, the container may be a ghost process interfering with the gateway.

### 6) Audit `.env` for dead keys
```bash
python3 -c "
import os
keys = ['KIMI_API_KEY','MINIMAX_API_KEY','OPENROUTER_API_KEY','ANTHROPIC_API_KEY','OPENAI_API_KEY']
for k in keys:
    v = os.popen(f'grep ^{k}= ~/.hermes/.env | cut -d= -f2').read().strip()
    print(f'{k}: length={len(v)}, status={\"VALID\" if len(v)>20 else \"EMPTY/DEAD\"}')
"
```

Remove dead keys:
```bash
sed -i '/^KIMI_API_KEY=/d' ~/.hermes/.env
sed -i '/^MINIMAX_API_KEY=/d' ~/.hermes/.env
sed -i '/^MINIMAX_BASE_URL=/d' ~/.hermes/.env
sed -i '/^MINIMAX_API_HOST=/d' ~/.hermes/.env
```

---

## Phase 2 — Failover to a Working Provider

### Pick the healthy provider

| Provider | Config model value | Provider block name | Base URL |
|----------|-------------------|---------------------|----------|
| Anthropic Claude | `claude-sonnet-4` | `anthropic` | `https://api.anthropic.com/v1` |
| OpenAI GPT | `gpt-4o` | `openai` | `https://api.openai.com/v1` |
| OpenRouter | `openai/gpt-4o` or `anthropic/claude-sonnet-4` | `openrouter` | `https://openrouter.ai/api/v1` |
| Kimi | `kimi-k2.6` | `kimi-coding` | `https://api.kimi.com/coding/v1` |
| MiniMax | `MiniMax-M2.7` | `minimax` | `https://api.minimax.io/v1` |

### Patch `config.yaml`

Example: switching from dead Kimi to working Anthropic with OpenAI fallback:

```yaml
model:
  provider: anthropic
  model: claude-sonnet-4
  fallback: openai/gpt-4o
  max_turns: 90
  temperature: 0.2
providers:
  anthropic:
    name: anthropic
    api_key: ${ANTHROPIC_API_KEY}
    base_url: https://api.anthropic.com/v1
  openai:
    name: openai
    api_key: ${OPENAI_API_KEY}
    base_url: https://api.openai.com/v1
```

Critical: **every provider referenced in `model:` or `fallback:` MUST have a matching block under `providers:`.** A valid key alone is not enough.

### Enable critical toolsets

If `toolsets:` only shows `[hermes-cli, brave-search]`, expand it:

```yaml
toolsets:
- hermes-cli
- brave-search
- terminal
- file
- web
- browser
- vision
- github
- gmail
```

Without `terminal` and `file`, Hermes cannot run shell commands or read files.

---

## Phase 3 — Verify after patch

### 1) Validate config syntax
```bash
python3 - <<'PY'
import yaml, os
p=os.path.expanduser('~/.hermes/config.yaml')
cfg=yaml.safe_load(open(p))
m = cfg.get('model', {})
print("provider:", m.get('provider'))
print("model:", m.get('model'))
print("fallback:", m.get('fallback'))
print("providers configured:", list(cfg.get('providers', {}).keys()))
print("toolsets:", cfg.get('toolsets', []))
PY
```

### 2) Restart gateway
```bash
kill $(cat ~/.hermes/gateway.pid) 2>/dev/null
# Or if no PID file:
ps aux | grep "hermes gateway" | grep -v grep | awk '{print $2}' | xargs kill -9 2>/dev/null

# Start fresh
hermes gateway run
```

### 3) Confirm Telegram reconnected
```bash
sleep 5
cat ~/.hermes/gateway_state.json | python3 -c "import json,sys; d=json.load(sys.stdin); print('state:', d.get('gateway_state')); print('telegram:', d.get('platforms',{}).get('telegram',{}).get('state'))"
```

---

## Phase 4 — Telegram group gotcha

Even after provider fix, Hermes can still appear silent in groups if `TELEGRAM_ALLOWED_USERS` does not include the group chat ID or if BotFather privacy mode is enabled.

Check allowlist:
```bash
grep '^TELEGRAM_ALLOWED_USERS=' ~/.hermes/.env
```

For full group listen (no mention required), set it blank:
```bash
TELEGRAM_ALLOWED_USERS=
```

Check BotFather privacy:
```bash
curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getMe" | python3 -c "import json,sys; d=json.load(sys.stdin); print('can_read_all_group_messages:', d.get('result',{}).get('can_read_all_group_messages'))"
```
If `false`, send `/setprivacy` to @BotFather and **Disable**.

---

## Pitfalls

1. `Telegram connected` != model healthy. Always test provider auth directly.
2. Broken Kimi/MiniMax auth can masquerade as Telegram silence.
3. `TELEGRAM_ALLOWED_USERS` can block a group even when the bot is connected.
4. A valid key in `.env` is useless without a matching `providers:` block in `config.yaml`.
5. Leaving dead keys in `.env` causes future confusion and security risk.
6. Fallback model strings like `openai/gpt-4o` require the `openai` provider block to exist.
7. Missing `terminal`/`file` toolsets means Hermes cannot execute tools even if the model works.
8. Unhealthy `hermes-agent` Docker container may be a ghost eating resources — consider stopping it.

## Outcome pattern

If Kimi returns `401 Invalid Authentication`, Anthropic returns `200`, OpenAI returns `200`, but OpenRouter is empty, the correct recovery is:
1. Remove dead keys from `.env`
2. Switch primary provider to `anthropic` with `openai` fallback
3. Add matching `providers:` blocks for both
4. Enable `terminal`, `file`, `web` toolsets
5. Restart gateway
6. Verify Telegram reconnects
