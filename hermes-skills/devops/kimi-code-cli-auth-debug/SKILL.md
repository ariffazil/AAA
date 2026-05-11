---
name: kimi-code-cli-auth-debug
description: Debug and fix Kimi Code CLI (Moonshot AI) authentication failures — OAuth token expiry vs static API key confusion
triggers: kimi code cli, kimi login, api key invalid, moonshot auth
category: devops
last_updated: 2026-05-07
---

# Kimi Code CLI — Auth Debug Skill

## How Kimi Code CLI Auth Works (Critical)

**Kimi Code uses OAuth browser login, NOT a static API key.**

The config may show `api_key = "sk-kim...Pqby"` but this is either:
1. A stale Moonshot global API key from a previous auth session, OR
2. Part of the OAuth flow — the real auth is the `access_token` in `~/.kimi/credentials/`

**Two auth paths:**
```
Path A (Kimi Code /login):  OAuth → access_token + refresh_token stored in credentials/
Path B (Moonshot Global):   Static sk-... API key in config.toml provider block
```

## Diagnostic Steps

### Step 1 — Check if OAuth token is valid
```python
import json, time
with open('/root/.kimi/credentials/kimi-code.json') as f:
    d = json.load(f)
print('expires_at:', d['expires_at'])
print('current_ts:', time.time())
print('token_valid:', time.time() < d['expires_at'])
# If False → token expired, needs re-login
```

### Step 2 — Check credentials structure
```bash
cat ~/.kimi/credentials/kimi-code.json
```
**Expected keys:** `access_token`, `refresh_token`, `expires_at`, `expires_in`
**NOT expected:** `api_key` (that's only in config.toml)

### Step 3 — Check config.toml provider
```bash
python3 -c "
import toml
c = toml.load('/root/.kimi/config.toml')
p = c['providers']['managed:kimi-code']
print('type:', p.get('type'))
print('base_url:', p.get('base_url'))
print('api_key_set:', bool(p.get('api_key')))
print('oauth_storage:', p.get('oauth', {}).get('storage'))
"
```

### Step 4 — Direct API test (if you have a real Moonshot global key)
```bash
curl -s -X POST https://api.kimi.com/coding/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"kimi-for-coding","messages":[{"role":"user","content":"hi"}],"max_tokens":5}'
# 200 = key works; 401 = key invalid/expired
```

## Fixes

### Fix A — Re-run OAuth login (for Kimi Code platform)
```bash
kimi /login
# CLI outputs a URL → open in browser → complete OAuth → CLI auto-reloads
```

### Fix B — Use Moonshot AI Global API key directly
Edit `~/.kimi/config.toml`:
```toml
[providers.moonshot-global]
type = "kimi"
base_url = "https://api.moonshot.ai/coding/v1"
api_key = "sk-YOUR-REAL-MOONSHOT-KEY"

[models."moonshot-global/k2"]
provider = "moonshot-global"
model = "moonshot-v1-128k"
capabilities = ["thinking", "image_in"]
```

Then set as default:
```toml
default_model = "moonshot-global/k2"
```

### Fix C — Check lock file (can block re-auth)
```bash
cat ~/.kimi/credentials/kimi-code.lock
# If non-empty, delete it:
rm ~/.kimi/credentials/kimi-code.lock
```

## Key Files
```
~/.kimi/config.toml              # Provider config, model settings
~/.kimi/credentials/kimi-code.json  # OAuth tokens (access, refresh, expiry)
~/.kimi/credentials/kimi-code.lock  # Lock file (delete if blocking re-login)
~/.kimi/oauth/kimi-code/        # OAuth artifacts (may be empty dir)
```

## Known Failure Modes

| Error | Cause | Fix |
|-------|-------|-----|
| `"The API Key appears to be invalid or may have expired"` | OAuth token expired OR static key rotated | Re-run `/login` or update static key |
| OAuth token `expires_at` in past | Token expired | `kimi /login` |
| `api_key = "sk-kim...Pqby"` in config | Masked stale key | Use real Moonshot Global key or re-OAuth |
| Config shows key but `credentials/` empty | OAuth was used, key never persisted | `kimi /login` |

## Kimi Code CLI vs Kimi API Platform

- **Kimi Code CLI** (`kimi` command): Agentic coding CLI, OAuth-based auth via `/login`
- **Moonshot AI Platform** (`platform.moonshot.ai`): Direct `sk-...` API key, no OAuth
- **Moonshot AI China** (`moonshot.cn`): Separate China-region endpoint

The `api.kimi.com/coding/v1` endpoint is Kimi Code's own backend — accepts OAuth tokens from `/login` OR static API keys from Moonshot Global.
