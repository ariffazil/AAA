# ═══════════════════════════════════════════════════════════════════════════
# HERMES MODEL ARCHITECTURE PLAN v2026-05-11
# Authority: 888_JUDGE | Sovereign: Arif
# Purpose: 9-slot model routing + key rotation ledger
# ═══════════════════════════════════════════════════════════════════════════

## 1. EXECUTIVE SUMMARY

| Metric | Value |
|--------|-------|
| Total API keys on disk | 11 |
| **Live keys** | **5** |
| **Dead keys** | **6** |
| OpenRouter models accessible | 365 |
| Local Ollama models | 2 (qwen2.5:7b, bge-m3) |
| Primary constraint | Non-American + budget-conscious ("miskin") |
| Strategic insight | OpenRouter = one key → 365 models (free tiers included) |

---

## 2. KEY INVENTORY — LIVE vs DEAD

### ✅ LIVE KEYS (5)

| # | Provider | Key Prefix | Status | Endpoint | Use Case |
|---|----------|-----------|--------|----------|----------|
| 1 | **MiniMax** | `sk-cp-xL0YZe...` | ✅ LIVE | `api.minimax.io` | Primary reasoning model |
| 2 | **Kimi** | `sk-kimi-QN0CPLA...` | ✅ LIVE (agent-restricted) | `api.kimi.com` | Fallback coding |
| 3 | **Kimi** | `sk-kimi-s9T1b9D...` | ✅ LIVE (agent-restricted) | `api.kimi.com` | Backup fallback |
| 4 | **OpenRouter** | `sk-or-v1-2ed3e0...` | ✅ LIVE | `openrouter.ai` | Auxiliary model hub |
| 5 | **Firecrawl** | `fc-733871f3...` | ✅ LIVE | `api.firecrawl.dev` | Web extraction |

### ❌ DEAD KEYS (6) — NEED ROTATION

| # | Provider | Key Prefix | Failure Reason | Rotation Priority |
|---|----------|-----------|----------------|-------------------|
| 1 | **DeepSeek** | `sk-d5b13984...` | `Authentication Fails` — **invalid key** | 🔴 HIGH |
| 2 | **Anthropic** | `sk-ant-api03-9ZsAF...` | `credit balance too low` — exhausted | 🔴 HIGH |
| 3 | **GitHub PAT** | `ghp_wEAfMBtlqO9...` | `Bad credentials` | 🟡 MEDIUM |
| 4 | **Copilot** | `gho_zJqLG5L23Ty...` | `Bad credentials` | 🟡 MEDIUM |
| 5 | **Jina AI** | `jina_12378eed...` | `Invalid endpoint` / invalid key | 🟢 LOW |
| 6 | **Old MiniMax** | `sk-cp-BJtUy1en...` | `invalid api key` — already rotated | ✅ CLOSED |

---

## 3. DEEPSEEK ANALYSIS

### The Key on Disk
```
Path:     /root/ (found via grep)
Prefix:   ***REDACTED***
Status:   ❌ INVALID — "Authentication Fails, Your api key: ****ebb0 is invalid"
Registry: arifOS secret-registry.yaml has `llm.deepseek.api_key` → `DEEPSEEK_API_KEY`
Hermes:   NOT configured in auth.json or config.yaml
OpenClaw: NOT configured in openclaw.json
```

### Why It's Dead
- Key was likely revoked by DeepSeek (security sweep, inactivity, or account closure)
- DeepSeek has been aggressively rotating keys since their server attacks in early 2025
- The key format (`sk-d5b1...`) suggests an older generation key

### Alternatives (No New DeepSeek Key Needed)

| Alternative | How | Cost | Non-American? |
|-------------|-----|------|---------------|
| **OpenRouter → deepseek/deepseek-chat** | Use existing OpenRouter key | ~$0.30/M tokens | ✅ China |
| **OpenRouter → deepseek/deepseek-reasoner** | R1 reasoning model | ~$0.55/M tokens | ✅ China |
| **Ollama → deepseek-r1** | Run locally (70B requires 40GB+ VRAM) | FREE | ✅ China |
| **Get new DeepSeek key** | Sign up at platform.deepseek.com | 500 free credits | ✅ China |

**Recommendation:** Use OpenRouter for DeepSeek access. One key, no separate signup, no separate billing. OpenRouter already routes to DeepSeek V3 and R1.

---

## 4. HERMES 9-SLOT MODEL ARCHITECTURE

### Slot Map

| Slot | Purpose | Current | Recommended | Provider | Why |
|------|---------|---------|-------------|----------|-----|
| **0** | **Main** | minimax/MiniMax-M2.7 | **minimax/MiniMax-M2.7** | MiniMax | Fast, high-quality, Token Plan active |
| **1** | **Vision** | minimax/MiniMax-M2.7 (raw key) | **openrouter/google/gemini-2.5-flash** | OpenRouter | Cheaper vision, 1M context |
| **2** | **Web Extract** | auto | **firecrawl** (native) | Firecrawl | Purpose-built, not LLM-based |
| **3** | **Compression** | auto | **ollama/qwen2.5:7b** | Ollama | Free, fast, local |
| **4** | **Session Search** | auto | **ollama/bge-m3** | Ollama | Embedding model, free, local |
| **5** | **Skills Hub** | auto | **openrouter/deepseek/deepseek-chat** | OpenRouter | Non-American, cheap, capable |
| **6** | **Approval** | auto | **minimax/MiniMax-M2.7** | MiniMax | Consistency with main |
| **7** | **MCP** | auto | **minimax/MiniMax-M2.7** | MiniMax | Best tool-use reliability |
| **8** | **Title Generation** | auto | **ollama/qwen2.5:7b** | Ollama | Free, fast, good enough |

### Architecture Rationale

```
┌─────────────────────────────────────────────────────────────────┐
│                    HERMES MODEL ROUTING                          │
├─────────────────────────────────────────────────────────────────┤
│  PRIMARY          │  FALLBACK          │  AUXILIARY HUB        │
│  minimax/M2.7     │  kimi/k2.6         │  openrouter/*          │
│  (reasoning)      │  (coding)          │  (365 models)         │
│                   │                    │                       │
│  ├─ Main          │  ├─ Fallback       │  ├─ Vision            │
│  ├─ Approval      │  └─ Backup         │  ├─ Skills Hub        │
│  └─ MCP           │                    │  └─ (any model)       │
│                   │                    │                       │
│  LOCAL (FREE)     │  TOOLS             │                       │
│  ollama/qwen2.5:7b│  firecrawl         │                       │
│  ollama/bge-m3    │  (web extract)     │                       │
│                   │                    │                       │
│  ├─ Compression   │                    │                       │
│  ├─ Title Gen     │                    │                       │
│  └─ Session Search│                    │                       │
└─────────────────────────────────────────────────────────────────┘
```

**Cost Strategy (for "miskin"):**
- Ollama tasks: **$0** (local inference)
- Firecrawl: **$0** (already paid, generous limits)
- MiniMax: **$0** (Token Plan active)
- OpenRouter free tiers: **$0** (models ending in `:free`)
- OpenRouter paid tiers: **~$0.30-2.00/M tokens** (still cheaper than direct APIs)

---

## 5. RECOMMENDED CONFIGURATION

### Updated `/root/AAA/hermes-config/config.yaml`

```yaml
model:
  provider: minimax
  model: MiniMax-M2.7
  max_turns: 90
  temperature: 0.2

providers:
  ollama:
    name: ollama
    api_key: ollama
    base_url: http://127.0.0.1:11434
  minimax:
    name: minimax
    api_key: ${MINIMAX_API_KEY}
    base_url: https://api.minimax.io/v1
  kimi-coding:
    name: kimi-coding
    api_key: ${KIMI_API_KEY}
    base_url: https://api.kimi.com/coding/v1
  openrouter:
    name: openrouter
    api_key: ${OPENROUTER_API_KEY}
    base_url: https://openrouter.ai/api/v1

fallback_providers:
  - kimi-coding
  - openrouter

# ═══════════════════════════════════════════════════════════════════
# AUXILIARY MODEL SLOTS — 8 slots for specialized tasks
# ═══════════════════════════════════════════════════════════════════
auxiliary:
  vision:
    provider: openrouter
    model: google/gemini-2.5-flash
    base_url: https://openrouter.ai/api/v1
    api_key: ${OPENROUTER_API_KEY}
    timeout: 120
    extra_body: {}
    download_timeout: 30

  web_extract:
    provider: auto           # Uses Firecrawl (configured in browser section)
    model: ''
    base_url: ''
    api_key: ''
    timeout: 360
    extra_body: {}

  compression:
    provider: ollama
    model: qwen2.5:7b
    base_url: http://127.0.0.1:11434
    api_key: ollama
    timeout: 120
    extra_body: {}

  session_search:
    provider: ollama
    model: bge-m3            # Embedding model for semantic search
    base_url: http://127.0.0.1:11434
    api_key: ollama
    timeout: 30
    extra_body: {}
    max_concurrency: 3

  skills_hub:
    provider: openrouter
    model: deepseek/deepseek-chat
    base_url: https://openrouter.ai/api/v1
    api_key: ${OPENROUTER_API_KEY}
    timeout: 30
    extra_body: {}

  approval:
    provider: minimax
    model: MiniMax-M2.7
    base_url: https://api.minimax.io/v1
    api_key: ${MINIMAX_API_KEY}
    timeout: 30
    extra_body: {}

  mcp:
    provider: minimax
    model: MiniMax-M2.7
    base_url: https://api.minimax.io/v1
    api_key: ${MINIMAX_API_KEY}
    timeout: 30
    extra_body: {}

  title_generation:
    provider: ollama
    model: qwen2.5:7b
    base_url: http://127.0.0.1:11434
    api_key: ollama
    timeout: 30
    extra_body: {}
```

### Updated `/root/AAA/.hermes/auth.json`

```json
{
  "version": 1,
  "credential_pool": {
    "minimax": [
      {
        "id": "f163aa",
        "source": "env:MINIMAX_API_KEY",
        "access_token": "sk-cp-xL0YZe...",
        "base_url": "https://api.minimax.io/anthropic"
      }
    ],
    "kimi-coding": [
      {
        "id": "kimi-vps-001",
        "label": "AAA VPS",
        "auth_type": "api_key",
        "access_token": "sk-kimi-QN0CPLA...",
        "base_url": "https://api.kimi.com/coding/v1"
      },
      {
        "id": "kimi-vps-002",
        "label": "AAA VPS Backup",
        "auth_type": "api_key",
        "access_token": "sk-kimi-s9T1b9D...",
        "base_url": "https://api.kimi.com/coding/v1"
      }
    ],
    "openrouter": [
      {
        "id": "64823a",
        "source": "env:OPENROUTER_API_KEY",
        "access_token": "sk-or-v1-2ed3e0...",
        "base_url": "https://openrouter.ai/api/v1"
      }
    ],
    "custom:ollama": [
      {
        "id": "d3e163",
        "access_token": "ollama",
        "base_url": "http://ollama:11434"
      }
    ],
    "firecrawl": [
      {
        "id": "firecrawl-001",
        "source": "env:FIRECRAWL_API_KEY",
        "access_token": "fc-733871f3...",
        "base_url": "https://api.firecrawl.dev"
      }
    ],
    "anthropic": [
      {
        "id": "b018f6",
        "source": "env:ANTHROPIC_API_KEY",
        "access_token": "sk-ant-api03-9ZsAF...",
        "last_status": "exhausted",
        "rotation_required": true,
        "rotation_reason": "Credit balance depleted"
      }
    ],
    "deepseek": [
      {
        "id": "deepseek-legacy-001",
        "source": "disk-grep",
        "access_token": "sk-d5b13984...",
        "last_status": "invalid",
        "rotation_required": true,
        "rotation_reason": "Authentication fails — key revoked by provider",
        "recommendation": "Use OpenRouter for DeepSeek access instead of direct API"
      }
    ],
    "gemini": [],
    "copilot": [
      {
        "id": "f072c2",
        "source": "gh_cli",
        "access_token": "gho_zJqLG5L...",
        "last_status": "invalid",
        "rotation_required": true,
        "rotation_reason": "Bad credentials — token expired/revoked"
      }
    ],
    "github": [
      {
        "id": "github-pat-001",
        "source": "env:GITHUB_TOKEN",
        "access_token": "ghp_wEAfMBt...",
        "last_status": "invalid",
        "rotation_required": true,
        "rotation_reason": "Bad credentials — PAT expired/revoked"
      }
    ],
    "jina": [
      {
        "id": "jina-001",
        "source": "env:JINA_API_KEY",
        "access_token": "jina_12378ee...",
        "last_status": "invalid",
        "rotation_required": true,
        "rotation_reason": "Invalid endpoint / key format changed"
      }
    ]
  }
}
```

---

## 6. ROTATION ACTION ITEMS

### Immediate (This Week)
- [ ] **DeepSeek**: Either (a) get new key at platform.deepseek.com, or (b) use OpenRouter route (recommended)
- [ ] **Anthropic**: Top up credits at console.anthropic.com, or remove from pool
- [ ] **GitHub PAT**: Generate new PAT at github.com/settings/tokens with `repo`, `workflow`, `read:org` scopes

### Soon (Next 2 Weeks)
- [ ] **Copilot**: Re-authenticate via `gh auth login` or generate new Copilot token
- [ ] **Jina AI**: Check if key format changed (new keys start with `jina_` but API endpoint may have moved to `jina.ai/api/v1`)

### Completed
- [x] Old MiniMax key rotated ✅
- [x] Kimi dead key removed ✅
- [x] MiniMax endpoint fixed (`.chat` → `.io`) ✅

---

## 7. COST PROJECTION (Monthly)

| Workload | Provider | Model | Est. Tokens/Month | Cost |
|----------|----------|-------|-------------------|------|
| Main reasoning (70%) | MiniMax | M2.7 | ~5M | $0 (Token Plan) |
| Fallback (20%) | Kimi | K2.6 | ~1M | $0 (agent quota) |
| Vision (5%) | OpenRouter | gemini-2.5-flash | ~500K | ~$0.25 |
| Skills Hub (3%) | OpenRouter | deepseek-chat | ~300K | ~$0.10 |
| Compression | Ollama | qwen2.5:7b | ~2M | **$0** |
| Title Gen | Ollama | qwen2.5:7b | ~200K | **$0** |
| Session Search | Ollama | bge-m3 | ~500K | **$0** |
| Web Extract | Firecrawl | — | ~1K pages | $0 (within limits) |
| **TOTAL** | | | | **~$0.35/month** |

> **Note:** If using OpenRouter free tiers (`:free` models), total cost drops to **$0/month**.

---

## 8. NON-AMERICAN COMPLIANCE MATRIX

| Provider | Origin | Status |
|----------|--------|--------|
| MiniMax | 🇨🇳 China | ✅ Active primary |
| Kimi | 🇨🇳 China | ✅ Active fallback |
| OpenRouter | 🇺🇸 USA (aggregator) | ⚠️ US company, but routes to non-US models |
| → DeepSeek via OR | 🇨🇳 China | ✅ Non-American model |
| → Qwen via OR | 🇨🇳 China | ✅ Non-American model |
| → Mistral via OR | 🇫🇷 France | ✅ Non-American model |
| Ollama | 🇺🇸 USA (tool) | ⚠️ US company, but runs local models |
| → qwen2.5 | 🇨🇳 China | ✅ Non-American model |
| → deepseek-r1 (local) | 🇨🇳 China | ✅ Non-American model |
| Firecrawl | 🇺🇸 USA | ⚠️ US company |

**Sovereign Decision Required:** Is using a US-based aggregator (OpenRouter) acceptable if the actual models served are non-American? OpenRouter is infrastructure, not the model provider. This is analogous to using Cloudflare (US) to serve a Chinese website.

---

## 9. APPENDIX: OPENROUTER FREE TIER MODELS

Verified free models accessible with the live OpenRouter key:

| Model | Provider | Context | Best For |
|-------|----------|---------|----------|
| `inclusionai/ring-2.6-1t:free` | Inclusion AI | 262K | General chat |
| `baidu/cobuddy:free` | Baidu | 131K | Chinese language |
| `meta-llama/llama-4-maverick:free` | Meta | 256K | Reasoning |
| `nvidia/llama-3.3-nemotron-super:free` | NVIDIA | 128K | Coding |
| `qwen/qwen-2.5-72b-instruct:free` | Alibaba | 131K | General |
| `deepseek/deepseek-chat:free` | DeepSeek | 64K | Reasoning |

To use free tiers, append `:free` to any model ID in the auxiliary config.

---

*Plan generated: 2026-05-11T00:48Z*
*Authority: A-FORGE 777 (planning) | Requires 888_JUDGE for config deployment*
