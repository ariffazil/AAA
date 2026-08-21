---
name: FORGE-model-monitor
id: forge-model-monitor
version: 1.1.0
risk_tier: low
description: 'Monitor the model fallback chain. Track latency, billing failures (402),
  cold-start failures, and auto-pause dead models. USE WHEN: "model health", "check
  fallback chain", "model latency", "billing alert".'
owner: A-FORGE
floor_scope:
- F1
- F2
- F4
- F11
- F13
autonomy_tier: T0
---
# Model Fallback Monitor

**Tracks Arif's model federation health. Prevents silent provider failures.**

## INVARIANT — The Method (does not rot)

### Principle
1. **Probe, don't assume.** Every provider status claim must come from a live HTTP probe.
2. **Canonical SOT.** Model-to-agent assignments live at `/root/AAA/registries/models/AGENT_MODEL_MAP.json`. Never hardcode a model name — read the registry.
3. **Governance.** Provider pool assignments live at `/root/.config/opencode/rules/arifos-governance.md`. Read, don't embed.
4. **History.** `/root/.openclaw/workspace/skills/model-fallback-monitor/check.sh` (if exists) contains the cron script.

### Probe Pattern (invariant)
```bash
# Generic provider health check — substitute provider URL from live config
curl -s -o /dev/null -w "%{http_code}" --max-time 10 \
  <PROVIDER_API_URL> 2>/dev/null

# DeepSeek balance check
curl -s -X POST https://api.deepseek.com/v1/models \
  -H "Authorization: Bearer $DEEPSEEK_KEY" \
  --max-time 10

# Ollama local check
curl -s --max-time 5 localhost:11434/api/tags

# Latency test (generic)
start=$(date +%s%N); <probe>; echo "$(($(date +%s%N) - $start))ns"
```

### Known Failure Modes (invariant taxonomy)
| Signal | Meaning |
|---|---|
| HTTP 402 | Insufficient balance — provider needs top-up |
| HTTP 429 | Rate limit — throttle or rotate |
| HTTP 401/403 | Auth failure — key expired or invalid |
| > 30s response | Cold start or overload — warm up or skip |
| Config mismatch | Model ID in config doesn't match provider's available models |

### Dynamic State — Read Live, Never Embed
- **Which model is primary for which agent?** → Read `/root/AAA/registries/models/AGENT_MODEL_MAP.json`
- **Which provider pool serves which agent?** → Read `/root/.config/opencode/rules/arifos-governance.md`
- **Current DeepSeek balance?** → Probe `https://api.deepseek.com/v1/models` with live key
- **Is MiniMax alive?** → Probe `https://api.minimax.chat/v1/models` with live key
- **Which Ollama models are loaded?** → `curl localhost:11434/api/tags`
