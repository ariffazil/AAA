# Qwen Individual Token Plan Refresh — Live Probe 2026-08-08

## Context
Arif refreshed the individual Qwen token plan. Asked to "try test sat." FED `fed_status` still showed stale notes from earlier that day.

## Probe sequence (real data)

### 1. Direct upstream (qwen3.6-flash) — anomaly

```
endpoint: https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1
model: qwen3.6-flash
HTTP: 200
time: 26.1s
total_tokens: 3573 (of which reasoning_tokens: 3545, text_tokens: 3557)
finish_reason: stop
```

**Verdict:** HTTP 200 (key works), but the model enters a massive reasoning loop
for trivial prompts ("say hello in 5 words"). 26 seconds, 3.5K tokens for a
5-word answer. This is a model-side behavior, not an API failure.

### 2. Direct upstream (qwen3.8-max) — clean

```
endpoint: same
model: qwen3.8-max
HTTP: 200
time: 1.6s
total_tokens: 99 (reasoning: 16, text: 28)
finish_reason: stop
content: "2 + 2 = 4"
```

**Verdict:** Flagship model works clean. 1.6s, 99 tokens. Use qwen3.8-max for
all validation probes when testing the Qwen individual plan.

### 3. LiteLLM :4000 (hermes-asi) — alias resolves to qwen3.8-max

```
model: hermes-asi → openai/qwen3.8-max (via litellm-config.yaml)
HTTP: 200
time: 0.9s
total_tokens: 96 (reasoning: 6, text: 9)
finish_reason: stop
content: "OK."
```

**Verdict:** Federation path works. Note: `system_fingerprint: fp_a18b46594c_prod0820_fp8_kvcache_20260402`
confirms DashScope Aliyun upstream. 192 cached prompt tokens (system prompt).

### 4. LiteLLM :4000 (agi-333) — same alias, same upstream

```
model: agi-333 → openai/qwen3.8-max (same cascade entry as hermes-asi)
HTTP: 200
time: 1.6s
total_tokens: 32 (reasoning: 20, text: 12)
finish_reason: stop
```

**Verdict:** Works. Different fingerprint (fp_9954b31ca9) — may be a different
DashScope pod.

### 5. LiteLLM :4000 (fed/vision) — vision path

```
model: fed/vision → openai/qwen3.8-max
HTTP: 200
time: 1.9s
total_tokens: 100 (reasoning: 26, text: 33)
finish_reason: stop
content: "vision_ok"
```

**Verdict:** Vision path works but doesn't actually test vision (text-only
prompt). Needs a real image to verify the multimodal path.

### 6. max_tokens budget trap demonstration

```
model: hermes-asi via LiteLLM
max_tokens: 20
prompt: "Say OK only."
HTTP: 200
finish_reason: length  ← ALL 20 tokens used on reasoning
content: "" (empty)     ← ZERO output tokens
```

This is the max_tokens trap: HTTP 200 + empty content = misdiagnosed as broken.

### 7. Fallback chain stale state

`fallback_providers` in config.yaml lists:
- `qwen-token-plan-standard` → qwen3.8-max → **429 (team pool exhausted)**
- `qwen-token-plan-team-owner` → qwen3.8-max → **429 (team pool exhausted)**
- `minimax` → MiniMax-M3 → **works**
- `groq` → llama-3.3-70b-versatile → **works (FREE)**

The first two fallbacks are dead. If the primary FED path fails, the first
two fallback attempts waste 60s (2 × 30s timeout) before hitting live seats.

## Summary table

| Test | Layer | Model | HTTP | Latency | Tokens | Verdict |
|---|---|---|---|---|---|---|
| 1 | direct | qwen3.6-flash | 200 | 26.1s | 3573 | ⚠️ reasoning loop |
| 2 | direct | qwen3.8-max | 200 | 1.6s | 99 | ✅ |
| 3 | LiteLLM | hermes-asi | 200 | 0.9s | 96 | ✅ |
| 4 | LiteLLM | agi-333 | 200 | 1.6s | 32 | ✅ |
| 5 | LiteLLM | fed/vision | 200 | 1.9s | 100 | ✅ |
| 6 | LiteLLM | hermes-asi (max20) | 200 | — | 20 | ⚠️ empty (budget) |

## Key config state at time of probe

- `/root/A-FORGE/litellm-config.yaml`: `hermes-asi`, `agi-333`, `asi-555`, `dispatch`,
  `openclaw` all route to `openai/qwen3.8-max` as primary entry
- `qwen3.6-flash` appears in `asi-555` and `asi-555-vision` cascade entries but NOT
  in `hermes-asi` or `agi-333`
- FED `fed_status` balance for `qwen-token-plan-individual`: `balance_usd: 0` (credit-based),
  notes confirmed "LIVE 2026-08-08T06:48Z", needs manual re-probe after refresh
