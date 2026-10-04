# Model Picker Architecture — Duplicate & Dead Provider Diagnosis (2026-08-09)

> Session-derived codebase knowledge for diagnosing model picker issues in Hermes Agent.
> All paths verified against `/usr/local/lib/hermes-agent/` source.

## Component map

| Component | File | Role |
|---|---|---|
| `CANONICAL_PROVIDERS` | `hermes_cli/models.py:1053` | Master list of provider slugs + display labels + TUI descriptions |
| `PROVIDER_GROUPS` | `hermes_cli/models.py:1139` | Display-only fold: groups related slugs under one picker row |
| `_PROVIDER_MODELS` | `hermes_cli/models.py:191` | Curated model lists per provider slug |
| `list_authenticated_providers()` | `hermes_cli/model_switch.py:1496` | Core: detects which providers have credentials, returns picker rows |
| `list_picker_providers()` | `hermes_cli/model_switch.py:2463` | Wrapper called by Telegram `/model` command |
| `probe_api_models()` | `hermes_cli/models.py:3548` | Probes `GET /v1/models` — exists but NOT used for picker filtering |
| `_handle_model_command()` | `gateway/slash_commands.py:1402` | Telegram `/model` slash command handler |
| `send_model_picker()` | `plugins/platforms/telegram/adapter.py:4846` | Builds inline keyboard for Telegram |
| Provider auth registry | `hermes_cli/auth.py` | `PROVIDER_REGISTRY` — ProviderConfig entries with `api_key_env_vars` |

## Credential check flow (current — 2026-08-09)

```
list_authenticated_providers()
  │
  ├─ Section 1: models.dev mapped providers
  │   has_creds = any(os.environ.get(ev) for ev in env_vars)
  │   if not has_creds: skip
  │   → emit picker row with curated model list
  │
  ├─ Section 2: Hermes overlay providers (nous, codex, copilot, etc.)
  ├─ Section 3: user-configured providers.<slug> blocks
  └─ Section 4: custom_providers (user-defined endpoints)
```

**Key limitation:** `has_creds` only checks that the env var **exists** — not that
the key is valid, has quota, or the endpoint is reachable. A key set but
expired/rate-limited/out-of-credit still shows in the picker. This is the
root cause of "I see the provider but it doesn't work when I select it."

## Duplicate provider diagnosis

### Alibaba (two rows)

| Slug | Endpoint | Env vars checked | Why it shows |
|---|---|---|---|
| `alibaba` | `dashscope-intl.aliyuncs.com/compatible-mode/v1` | `DASHSCOPE_API_KEY` | Key set ✅ |
| `alibaba-coding-plan` | `coding-intl.dashscope.aliyuncs.com/v1` | `ALIBABA_CODING_PLAN_API_KEY`, **`DASHSCOPE_API_KEY`** (fallback) | Same key triggers fallback ✅ |

**Root cause:** `alibaba-coding-plan` ProviderConfig in `auth.py:328` lists
`DASHSCOPE_API_KEY` as a fallback env var. When only `DASHSCOPE_API_KEY` is set
(no `ALIBABA_CODING_PLAN_API_KEY`), both providers match → two rows.

**Fix option A (display fold):** Add Alibaba to `PROVIDER_GROUPS` in `models.py`:
```python
"alibaba": ("Alibaba / Qwen Cloud", "DashScope + Coding Plan endpoints",
            ["alibaba", "alibaba-coding-plan"]),
```
This folds both under one "Alibaba / Qwen Cloud ▸" row, same as Kimi.

**Fix option B (logic gate):** Only show `alibaba-coding-plan` when
`ALIBABA_CODING_PLAN_API_KEY` is explicitly set. The fallback to
`DASHSCOPE_API_KEY` is useful at runtime, just not for picker display.

### Kimi (already grouped — not a bug)

Kimi IS in `PROVIDER_GROUPS`:
```python
"kimi": ("Kimi / Moonshot", "Coding Plan, Moonshot global & China endpoints",
         ["kimi-coding", "kimi-coding-cn"]),
```
`kimi-coding-cn` requires `KIMI_CN_API_KEY` (separate env var). If not set,
only `kimi-coding` shows — as a group row with one member. Not a duplicate.

### Duplicate model names across providers

`_PROVIDER_MODELS["kimi-coding"]` and `_PROVIDER_MODELS["alibaba-coding-plan"]`
both list `kimi-k2.7-code` and `kimi-k2.5` — the Alibaba Coding Plan endpoint
supports third-party models (Kimi, MiniMax, GLM) alongside Qwen. This is
correct (same model available from multiple providers), but confusing in the
picker if both providers show the same model name.

## Health-probe filter design (proposed, not yet implemented)

**User vision (Arif 2026-08-09):** "Only show the model that working and have
quota and limit and credit still working only. Kalau x dak, x payah menyemak."

**Approach:** After credential check passes, probe each provider's
`GET /v1/models` endpoint (2s timeout, parallel via ThreadPoolExecutor).
Cache results 5 min TTL.

| HTTP response | Picker action |
|---|---|
| 200 OK | ✅ Show provider |
| 401 / 403 | ❌ Hide (key invalid/expired) |
| 429 | ⚠️ Show with rate-limit badge |
| 402 | ❌ Hide (payment required / out of credit) |
| Timeout / connection refused | ❌ Hide (endpoint unreachable) |

**Existing infra:** `probe_api_models()` in `models.py:3548` already does the
HTTP probe — it just isn't called during picker construction. The patch point
is `list_authenticated_providers()` in `model_switch.py:1496`, after the
`has_creds` check and before the row is appended to `results`.

**Tradeoff:** First `/model` call adds ~2s latency (parallel probes). Cached
for 5 min so subsequent calls are instant.

**Limitation:** This verifies key validity + endpoint reachability. Actual
quota/credit remaining requires provider-specific billing APIs (most don't
expose them — see `qwen-token-plan-quota.md` for the Qwen example). 429/402
status codes are the closest signal for "out of quota." This is the same
"validity ≠ usability" doctrine from the SKILL.md — applied to the picker UI.

## Provider group registry (current state)

```python
PROVIDER_GROUPS = {
    "kimi":     ("Kimi / Moonshot",      ["kimi-coding", "kimi-coding-cn"]),
    "minimax":  ("MiniMax",              ["minimax", "minimax-oauth", "minimax-cn"]),
    "xai":      ("xAI Grok",             ["xai", "xai-oauth"]),
    "google":   ("Google Gemini",        ["gemini"]),
    "openai":   ("OpenAI",               ["openai-codex", "openai-api"]),
    "opencode": ("OpenCode",             ["opencode-zen", "opencode-go"]),
    "copilot":  ("GitHub Copilot",       ["copilot", "copilot-acp"]),
}
```

**Missing:** Alibaba (`alibaba` + `alibaba-coding-plan`), Qwen OAuth (standalone).

## Plugin auto-extension

Plugins in `plugins/model-providers/<name>/` auto-extend `CANONICAL_PROVIDERS`
at import time (`models.py:1093-1107`). Providers with `auth_type` in
`{oauth_device_code, oauth_external, external_process, aws_sdk, copilot, vertex}`
are skipped (need bespoke picker UX). All `api_key` auth providers auto-inject.

## Key env vars observed (2026-08-09, aaa-hermes profile)

```
DASHSCOPE_API_KEY     → triggers alibaba + alibaba-coding-plan (duplicate root cause)
KIMI_API_KEY          → triggers kimi-coding
FIREWORKS_API_KEY     → triggers fireworks (current active provider)
QWEN_API_KEY          → triggers qwen-oauth
ANTHROPIC_API_KEY     → triggers anthropic
```
