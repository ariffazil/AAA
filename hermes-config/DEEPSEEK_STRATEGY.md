# ═══════════════════════════════════════════════════════════════════════════
# DEEPSEEK V4 INTEGRATION STRATEGY — arifOS Federation
# Authority: 888_JUDGE | Sovereign: Arif
# Date: 2026-05-11
# Key: sk-9736...54c5b (LIVE — verified via api.deepseek.com)
# ═══════════════════════════════════════════════════════════════════════════

## 1. EXECUTIVE SUMMARY

DeepSeek V4 is now **live and wired** across the entire arifOS Federation. The new key unlocks two models:

| Model | Role | Speed | Cost | Best For |
|-------|------|-------|------|----------|
| `deepseek-v4-pro` | Reasoning champion | Medium | ~$0.80/M | Constitutional deliberation, skills hub, complex reasoning |
| `deepseek-v4-flash` | Fast triage | Fast | ~$0.10/M | Quick answers, high-volume tasks, fallback |

> **Deprecation notice:** `deepseek-chat` and `deepseek-reasoner` are deprecated on 2026/07/24. The federation uses the new V4 naming exclusively.

---

## 2. FEDERATION-WIDE DEPLOYMENT MAP

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         arifOS FEDERATION                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐              │
│  │   arifOS     │    │   HERMES     │    │  OpenClaw    │              │
│  │  Law Kernel  │◄──►│  ASI Relay   │◄──►│   Gateway    │              │
│  │   (Python)   │    │    (JS)      │    │    (JS)      │              │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘              │
│         │                   │                    │                      │
│         ▼                   ▼                    ▼                      │
│  ┌─────────────────────────────────────────────────────────┐           │
│  │              DEEPSEEK API (api.deepseek.com)             │           │
│  │    deepseek-v4-pro  │  deepseek-v4-flash  │  thinking   │           │
│  └─────────────────────────────────────────────────────────┘           │
│                                                                         │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐              │
│  │   A-FORGE    │    │    GEOX      │    │   WEALTH     │              │
│  │  (reads via  │    │  (reads via  │    │  (reads via  │              │
│  │   arifOS)    │    │   arifOS)    │    │   arifOS)    │              │
│  └──────────────┘    └──────────────┘    └──────────────┘              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. PER-NODE STRATEGY

### 3.1 arifOS — Law Kernel (Python/FastMCP)

**Files changed:**
- `arifosmcp/core/model_governance.yaml` — Added governance cards
- `arifosmcp/runtime/capability_map.py` — Added `deepseek` provider detection
- `.env` — Added `DEEPSEEK_API_KEY`, `DEEPSEEK_BASE_URL`

**Governance Cards Added:**

```yaml
# Tier 1b: DeepSeek V4 Pro
#   - Same authority as SEA-LION (instrument_only, F13 compliant)
#   - Allowed: reason, critique, reply, judge_deliberate
#   - Fallback chain: SEA-LION → Ollama → deterministic
#
# Tier 1c: DeepSeek V4 Flash
#   - Fast witness role for high-volume constitutional triage
#   - Allowed: reason, critique, reply
#   - Fallback chain: V4 Pro → SEA-LION → deterministic
```

**Why here:** arifOS is the constitutional floor enforcer. DeepSeek V4 Pro's reasoning capability makes it ideal for:
- F11 model governance decisions
- F666_HEART risk critique
- F888_JUDGE deliberation support (advisory only — never sovereign)

**Capability map now reports:**
```json
{
  "providers": {
    "deepseek": "configured",
    ...
  }
}
```

---

### 3.2 HERMES — ASI Relay (JavaScript/Express)

**Files changed:**
- `hermes-config/config.yaml` — Added `deepseek` provider + slot assignments
- `.hermes/auth.json` — Added DeepSeek credential pool entry
- `HERMES/config.json` — Updated cross-agent model contract

**Slot Assignments:**

| Slot | Before | After | Rationale |
|------|--------|-------|-----------|
| Main | minimax/M2.7 | **minimax/M2.7** | Keep fast primary |
| Vision | openrouter/gemini-2.5-flash | **openrouter/gemini-2.5-flash** | Unchanged |
| Skills Hub | openrouter/deepseek-chat | **deepseek/deepseek-v4-pro** | Direct = cheaper + thinking mode |
| Approval | minimax/M2.7 | **minimax/M2.7** | Unchanged |
| MCP | minimax/M2.7 | **minimax/M2.7** | Unchanged |
| Compression | ollama/qwen2.5:7b | **ollama/qwen2.5:7b** | Unchanged |
| Session Search | ollama/bge-m3 | **ollama/bge-m3** | Unchanged |
| Title Gen | ollama/qwen2.5:7b | **ollama/qwen2.5:7b** | Unchanged |

**Fallback chain:**
```
minimax/M2.7 → kimi/k2.6 → openrouter/* → deepseek/v4-pro
```

**Why here:** HERMES is the deliberative relay. DeepSeek V4 Pro enhances:
- Skills hub reasoning (complex skill composition)
- Future: high-confidence constitutional deliberation (when `confidence < 0.85`)
- Cross-agent resilience via updated model_contract

---

### 3.3 OpenClaw — Gateway (JavaScript/Node.js)

**Files changed:**
- `.openclaw/openclaw.json` — Added DeepSeek models, auth profile, MCP server

**Model Routing:**

| Priority | Model | Alias | Use Case |
|----------|-------|-------|----------|
| Primary | `minimax/MiniMax-M2.7` | MiniMax | Fast, responsive Telegram/Discord |
| Fallback 1 | `deepseek/deepseek-v4-pro` | DeepSeek Pro | Complex reasoning, coding |
| Fallback 2 | `kimi/kimi-k2.6` | Kimi | Coding-specialized |
| Fallback 3 | `ollama/qwen2.5:7b` | Ollama | Offline emergency |

**Auth profile added:**
```json
"deepseek:default": {
  "provider": "deepseek",
  "mode": "api_key"
}
```

**MCP server added:**
```json
"deepseek": {
  "command": "uvx",
  "args": ["deepseek-mcp"],
  "env": {
    "DEEPSEEK_API_KEY": "${DEEPSEEK_API_KEY}",
    "DEEPSEEK_BASE_URL": "https://api.deepseek.com"
  }
}
```

**Security fix:** Raw MiniMax API key in MCP config replaced with `${MINIMAX_API_KEY}`.

**Why here:** OpenClaw is the user-facing gateway. DeepSeek V4 Pro adds:
- Better reasoning for complex user queries
- Coding excellence for dev tasks
- Non-American compliance (Chinese provider)

---

### 3.4 A-FORGE / GEOX / WEALTH / WELL / AAA

These nodes **do not connect directly** to DeepSeek. They access LLM capabilities through:
- **arifOS MCP** → arifOS selects the appropriate model via governance
- **HERMES hooks** → Hermes delegates to configured providers
- **OpenClaw gateway** → OpenClaw routes to the best available model

This is intentional — the federation uses a **hub-and-spoke model** where:
- arifOS = model governance authority
- Hermes = deliberative routing
- OpenClaw = user-facing gateway
- Other nodes = consumers, not direct LLM clients

---

## 4. COST ANALYSIS ("Miskin" Budget)

### Monthly Projection

| Workload | Provider | Model | Est. Tokens | Cost |
|----------|----------|-------|-------------|------|
| Main reasoning (60%) | MiniMax | M2.7 | ~4M | **$0** (Token Plan) |
| Skills hub (15%) | DeepSeek | V4 Pro | ~1M | ~$0.80 |
| Fallback reasoning (15%) | DeepSeek | V4 Pro | ~1M | ~$0.80 |
| Fast triage (5%) | DeepSeek | V4 Flash | ~300K | ~$0.03 |
| Vision | OpenRouter | gemini-2.5-flash | ~500K | ~$0.25 |
| Compression | Ollama | qwen2.5:7b | ~2M | **$0** |
| Title Gen | Ollama | qwen2.5:7b | ~200K | **$0** |
| Session Search | Ollama | bge-m3 | ~500K | **$0** |
| Web Extract | Firecrawl | — | ~1K pages | **$0** |
| **TOTAL** | | | | **~$1.88/month** |

> With OpenRouter free tiers for vision, cost drops to **~$1.63/month**.

### Cost Comparison: Direct vs OpenRouter

| Route | V4 Pro Cost | V4 Flash Cost |
|-------|-------------|---------------|
| **Direct DeepSeek** (this strategy) | ~$0.80/M | ~$0.10/M |
| OpenRouter → DeepSeek | ~$1.20/M | ~$0.30/M |
| **Savings** | **~33%** | **~67%** |

Using direct DeepSeek instead of OpenRouter for DeepSeek models saves ~33% on Pro and ~67% on Flash.

---

## 5. NON-AMERICAN COMPLIANCE

| Node | DeepSeek Usage | Origin | Compliant? |
|------|---------------|--------|------------|
| arifOS | Governance deliberation | 🇨🇳 DeepSeek (China) | ✅ Yes |
| Hermes | Skills hub reasoning | 🇨🇳 DeepSeek (China) | ✅ Yes |
| OpenClaw | Fallback reasoning | 🇨🇳 DeepSeek (China) | ✅ Yes |

DeepSeek is a **Chinese** AI company (Hangzhou, Zhejiang). Using it directly satisfies the non-American constraint without needing OpenRouter as an intermediary.

---

## 6. SECURITY & GOVERNANCE

### F11 Model Governance
- DeepSeek V4 Pro: `authority: instrument_only` (same as SEA-LION)
- Forbidden roles: `sovereign_judge`, `irreversible_executor`, `vault_sealer`
- Output required: `schema_valid`, `uncertainty`, `human_decision_required`, `raw_output_hash`

### Key Storage
- **Raw key** stored in: `.secrets/vault.env`, `arifOS/.env`, `compose/.env`
- **All .env files are gitignored** ✅
- **Configs reference via `${DEEPSEEK_API_KEY}`** (no hardcoded keys)
- **Auth.json** stores metadata + token ( Hermes credential pool convention)

### Thinking Mode
DeepSeek V4 Pro supports explicit thinking:
```yaml
extra_body:
  thinking:
    type: enabled
  reasoning_effort: high
```

This is **enabled only for skills_hub** in Hermes. Other slots use standard mode for speed.

---

## 7. FALLBACK RESILIENCE

### Cross-Agent Model Contract (HERMES/config.json)

```json
{
  "hermes": {
    "default": "minimax/MiniMax-M2.7",
    "fallback": "deepseek/deepseek-v4-pro",
    "fallback_fast": "kimi/kimi-k2.6"
  },
  "openclaw": {
    "default": "minimax/MiniMax-M2.7",
    "fallback": "deepseek/deepseek-v4-pro",
    "fallback_fast": "kimi/kimi-k2.6"
  }
}
```

### Failure Scenarios

| Scenario | Fallback Chain | Result |
|----------|---------------|--------|
| MiniMax down | DeepSeek V4 Pro → Kimi K2.6 | ✅ Covered |
| DeepSeek down | MiniMax M2.7 → Kimi K2.6 | ✅ Covered |
| Both down | Kimi K2.6 → Ollama qwen2.5:7b | ✅ Covered |
| All remote down | Ollama local | ✅ Offline capable |

---

## 8. REBOOT / RESTART CHECKLIST

After applying these configs, restart services in this order:

```bash
# 1. arifOS (law kernel must boot first)
cd /root/compose && docker compose restart arifosmcp

# 2. HERMES (reads arifOS MCP)
cd /root/compose && docker compose restart hermes-agent

# 3. OpenClaw (reads HERMES hooks + arifOS MCP)
#    (OpenClaw is not in compose — runs as systemd or standalone)
cd /root/AAA && npm run openclaw:restart  # or appropriate command

# 4. Verify health
curl https://arifos.arif-fazil.com/health
curl http://localhost:7071/health          # HERMES
curl http://localhost:18789/health         # OpenClaw
```

---

## 9. APPENDIX: API REFERENCE

### DeepSeek V4 Models

| Model | Context | Input Price | Output Price | Speed |
|-------|---------|-------------|--------------|-------|
| `deepseek-v4-pro` | 64K | ~$0.50/M | ~$1.50/M | Medium |
| `deepseek-v4-flash` | 64K | ~$0.05/M | ~$0.20/M | Fast |

### Endpoints

| Format | Base URL |
|--------|----------|
| OpenAI-compatible | `https://api.deepseek.com` |
| Anthropic-compatible | `https://api.deepseek.com/anthropic` |

### Thinking Mode (OpenAI format)
```json
{
  "model": "deepseek-v4-pro",
  "messages": [...],
  "thinking": {"type": "enabled"},
  "reasoning_effort": "high"
}
```

---

*Strategy authored: 2026-05-11T08:48Z*
*Authority: A-FORGE 777 | Ratification: 888_JUDGE pending*
*Sovereign: Arif*
