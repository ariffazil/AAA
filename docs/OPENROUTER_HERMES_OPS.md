# OpenRouter — Hermes Operations Guide

> **Audience:** Hermes agent + Hermes-profile agents (hermes_asi, hermes_apex, hermes_forge).
> **Parent doc:** `/root/AAA/docs/OPENROUTER_AGENT_GUIDE.md` (general OpenRouter knowledge).
> **Strategic doctrine:** `/root/AAA/docs/OPENROUTER_ZEN_OPTIMIZATION.md`.
> **Forged:** 2026-07-24 · **SOT:** `/root/AAA/registries/models/AGENT_MODEL_MAP.json` (agent_id `hermes`).

---

## 0. TL;DR for Hermes

You are the **human-facing Telegram agent** (organ HERMES, class C2, daily budget $3, monthly $30).
Your primary model is `mimo/mimo-v2.5-pro-ultraspeed` (1000 tok/s). OpenRouter is your **smart
fallback** at chain priority 2, taking over when MiMo is unavailable or budget-constrained.

Five things you must internalize:

1. **You are NOT a judge.** Constitutional verdicts (666_JUDGE / 999_SEAL) must never route
   through you — always escalate to arifOS kernel. Your job is conversational synthesis.
2. **MY governance has a hard routing override.** When the user asks about 1MDB, Najib,
   PETRONAS, Jho Low, myKad, or any Malaysian politics/governance — route to DeepSeek V4 Pro
   direct, bypass your normal fallback chain entirely.
3. **Session stickiness is your biggest latency win.** Telegram threads are multi-turn.
   Pass `session_id` on every call to OpenRouter so provider pinning + cache kicks in.
4. **You have THREE profiles** (ASI, APEX, FORGE) with different model needs. Don't use
   OpenRouter auto-router for APEX (judgment) or FORGE (execution) — those need stable models.
5. **Your monthly budget is RM30.** Auto-router cqt=9 (default for Hermes) is fine for
   chat. For batch work use `openrouter/free`. Never let cqt=0 anywhere in Hermes.

---

## 1. Hermes topology — who you are

### 1.1 The three personas

| Profile | Role | When to load | Best OpenRouter use |
|---|---|---|---|
| `hermes_asi` (555-ASI) | Synthesis, stewardship, memory, sovereign briefing | Default Telegram chat | `openrouter/auto-beta` cqt=9 (chat tier) |
| `hermes_apex` (888-APEX) | Verification, constitutional review, judgment gate | Audit / verification requests | **None** — escalate to arifOS kernel |
| `hermes_forge` (777-FORGE) | Execution, building, deploying, health probes | When user asks "build" / "deploy" / "fix" | `openrouter/auto-beta` cqt=5 for code work |

Profile YAML files: `/root/HERMES/profiles/{hermes_asi,hermes_apex,hermes_forge}/profile.yaml`.
Each profile has its own `skills/` tree — OpenRouter-relevant skills include
`arifos-external-council/agents/openai.yaml`.

### 1.2 The 4-tier model picker

`/root/HERMES/model-picker.yaml` (probed 2026-07-23, 39 models alive across Zen + Go):

| Tier | Use | Primary | Fallback |
|---|---|---|---|
| `bulk` | Cron, background, high-volume summaries | `opencode-go/deepseek-v4-flash` ($10/mo flat) | Ollama local |
| `default` | **Telegram chat, daily work, casual code** | `opencode-zen/deepseek-v4-flash` ($0.14/M, $0.28/M) | (n/a) |
| `heavy` | Code generation, audits, long-context | `opencode-zen/deepseek-v4-pro` ($1.74/M, $3.48/M) | `minimax-m3` |
| `apex` | Rare governed judgments, constitutional | `opencode-zen/grok-4.5` ($2.00/M, $6.00/M) | `glm-5.2` |

**Important:** OpenRouter is NOT in the primary chain here. The picker routes Zen/Go/MiniMax
direct. OpenRouter kicks in via the **SOT fallback chain** when those fail.

### 1.3 SOT fallback chain (where OpenRouter lives)

From `AGENT_MODEL_MAP.json` `agents[hermes]`:

```
priority 1  mimo/mimo-v2.5-pro               (when ultraspeed unavailable or needs reasoning)
priority 2  openrouter/auto-beta   cqt=9    (when MiMo unavailable)
priority 3  openrouter/free        cqt=9    (when OpenRouter unavailable or budget exceeded)
priority 4  ollama/qwen2.5-coder:3b        (when all remote dead — last resort)
```

Circuit breaker: 3 fails / 60s window / 60s cooldown. Timeout: 30s.
Daily budget $3 / monthly $30. **Auto-router cqt=9 — RM-leaning.**

---

## 2. When OpenRouter kicks in — the decision tree

```
User message → Hermes receives
  │
  ├─ MY governance topic detected (Najib, 1MDB, PETRONAS, myKad, ...)
  │   └─ ALWAYS route to DeepSeek V4 Pro direct (NOT auto-router)
  │
  ├─ Profile = hermes_apex + judgment question
  │   └─ Escalate to arifOS kernel (arif_judge); never use auto-router
  │
  ├─ Profile = hermes_asi (default chat) OR hermes_forge (code/build)
  │   │
  │   ├─ Tier = bulk (cron, batch)         → openrouter/free       (RM0, cqt=10)
  │   ├─ Tier = default (chat, casual)     → openrouter/auto-beta  (cqt=9)
  │   ├─ Tier = heavy (code, audit)        → openrouter/auto-beta  (cqt=5)
  │   └─ Tier = apex (judgment)            → NOT OpenRouter
  │
  └─ Constitutional / irreversible task   → arifOS kernel only
```

**Latency ladder** (in priority order, lowest first):
1. Try the picker default — Zen or Go direct (cheapest, fastest)
2. If that fails or budget exceeded → auto-beta (smart route)
3. If auto-beta 4xx/5xx → openrouter/free (RM0 fallback)
4. If OpenRouter unreachable → ollama local (survival)

---

## 3. Telegram-specific patterns

### 3.1 Multi-turn continuity — use session_id

Telegram conversations are inherently multi-turn. Pass `session_id` to OpenRouter on every
follow-up so the provider pin + prompt cache stays warm:

```python
import hashlib
# Stable per-Telegram-chat-id + user-id for the conversation
session_id = hashlib.sha256(
    f"hermes-tg-{chat_id}-{user_id}-{date}".encode()
).hexdigest()[:32]

response = openrouter.chat.send(
    model="openrouter/auto-beta",
    session_id=session_id,
    plugins=[{"id": "auto-router", "cost_quality_tradeoff": 9}],
    messages=[...],
    stream=True,  # Telegram wants streaming for perceived latency
)
```

**Expected gain:** ~30% latency reduction on turn 2+ via prompt cache hit. Critical for Telegram
UX where the user sees typing indicator.

### 3.2 Telegram message limits

| Limit | Value | Implication |
|---|---|---|
| Max message length | 4096 chars (Telegram Bot API) | Truncate / chunk OpenRouter outputs |
| Max inline keyboard callback_data | 64 bytes | Use shortcodes, not model strings |
| Typing indicator timeout | 5s | Send "typing" action every 4s while streaming |
| Edit window | Unlimited | Edit long responses in place |

**OpenRouter implication:** When the auto-router picks a long-context model (e.g.,
`xiaomi/mimo-v2.5` at 1M ctx), it may produce 8K+ token responses. Hermes MUST truncate to fit
Telegram's 4096-char limit, or chunk into multiple messages.

### 3.3 Streaming is mandatory for chat UX

Always set `"stream": true` for Telegram chat responses. OpenRouter SSE format:

```
data: {"id":"gen-...","model":"anthropic/claude-...","choices":[{"delta":{"content":"Hello"}}]}
data: {"id":"gen-...","model":"anthropic/claude-...","choices":[{"delta":{"content":" there"}}]}
data: [DONE]
```

Log the final `model` field for F11 audit trail.

### 3.4 Retry semantics

Hermes config: `api_max_retries: 3` (config.yaml line 3). On retry, **regenerate session_id**
because the cached provider may have just failed. Don't retry with the same session_id — the
cache won't update on provider errors (per OpenRouter docs), so you're just thrashing.

---

## 4. The Malaysian governance override (HARD RULE)

If user input matches any of these patterns, **route to DeepSeek V4 Pro direct, NOT auto-router**:

```
1MDB | Najib | PETRONAS | Jho_Low | myKad | Anwar_ibrahim_political |
malaysian_governance | malaysian_sovereign_wealth | malaysian_politics
```

**Why:**
1. Auto-router's community-spend signal has no knowledge of censorship
2. MiniMax M3 (still in auto-router's candidate pool) silently censors MY governance
3. F2 TRUTH floor: censored output masquerading as ignorance is a violation
4. SHADOW-MM-001 + drafted SHADOW-OR-001 both apply

**Implementation pattern** (pseudo-code for Hermes):

```python
import re

SOVEREIGN_PATTERN = re.compile(
    r"\b(1MDB|Najib|PETRONAS|Jho[\s_]?Low|myKad|"
    r"Malaysian[_ ]governance|Malaysian[_ ]sovereign|"
    r"malaysian[_ ]politics)\b",
    re.IGNORECASE
)

def select_model(user_message: str, profile: str, tier: str):
    if SOVEREIGN_PATTERN.search(user_message):
        # Hard override — bypass auto-router entirely
        return "deepseek/deepseek-v4-pro", {
            "zdr": True,
            "session_id": sovereign_session_id(user_message),
            "audit_tag": "sovereign-topic-override"
        }
    # ... normal cascade
```

Log every override with the pattern matched (PII-redacted) for F11.

---

## 5. Cost control — daily $3, monthly $30

### 5.1 Budget monitoring

Hermes is the **highest-volume agent** (Telegram-driven, all hours). Auto-router cqt=9 default
is correct. Check `get-credits` (via OpenRouter MCP) at session start and every 100 calls.

```
/root/AAA/scripts/openrouter-credit-check.sh   # Cron every 30 min
# If credit < $5, switch default tier to openrouter/free
# If credit < $1, surface warning to user + escalate to F13
```

### 5.2 Per-tier CQT settings for Hermes

| Hermes tier | CQT | Why |
|---|---|---|
| `bulk` (cron, batch) | 10 | Pure cost — RM0 via openrouter/free |
| `default` (Telegram chat) | 9 | RM-leaning — Hermes primary default |
| `heavy` (code, audit) | 5 | Balanced — quality matters |
| `apex` (judgment) | n/a | **Not OpenRouter** — arifOS kernel |

### 5.3 Token economics

| Model family | Input $/M | Output $/M | Hermes use |
|---|---|---|---|
| `minimax/MiniMax-M3` (primary) | $0.30 | $1.20 | Multimodal fallback |
| `mimo-v2.5-pro-ultraspeed` (primary) | $0.14 | $0.28 | Fast conversational |
| `mimo-v2.5-pro` (reasoning) | $0.14 | $0.28 | Heavy reasoning |
| `openrouter/auto-beta` cqt=9 | variable | variable | Smart fallback |
| `openrouter/free` | $0 | $0 | Last resort |
| `ollama/qwen2.5-coder:3b` | $0 | $0 | Local survival |

**Estimated Hermes monthly cost** (if OpenRouter tier fires 50% of time):
- 50% MiMo primary × $0.14/M × 50M tokens = $3.50
- 30% auto-beta cqt=9 × $0.20/M avg × 30M tokens = $1.80
- 15% openrouter/free × $0 = $0
- 5% ollama local × $0 = $0
- **Total: ~$5.30/month** — well under $30 budget

---

## 6. The MiMo-vs-auto-beta decision

MiMo is preferred because:
1. **Speed:** UltraSpeed hits 1000 tok/s; auto-router adds 50-200ms classifier latency
2. **Cost:** $0.14/M input is known; auto-router variable based on selection
3. **Stability:** No surprise model swap mid-conversation
4. **No censorship:** Confirmed clean on MY topics (zero observation per SOT)

Auto-router takes over when:
1. MiMo 429 (rate-limited) — circuit breaker triggers after 3 fails/60s
2. MiMo unavailable (provider outage)
3. Conversation budget exhausted (MiMo's plan limit)
4. User explicitly requested "use a different model"

**Don't switch to auto-router unless one of these conditions is met.** The MiMo primary is
cheaper, faster, and more predictable for Hermes's conversational load.

---

## 7. consult_external.sh — Hermes's direct-OpenRouter shortcut

`/root/HERMES/scripts/consult_external.sh` is a standalone bash tool for one-shot OpenRouter
consultations (e.g., "ask GPT-5 about X" or "verify this claim with Claude").

```bash
# Default model from OPENROUTER_DEFAULT_MODEL or fallback to gemma-4-31b-it:free
consult_external.sh "google/gemma-4-31b-it:free" "Explain Malaysian palm oil supply chain" 1024
```

**Usage patterns:**

```bash
# Quick classification
consult_external.sh "meta-llama/llama-3.2-3b-instruct:free" "$(cat claim.txt)" 200

# Deep reasoning check
consult_external.sh "z-ai/glm-5.2" "$(cat long_context.txt)" 4096

# Vision
consult_external.sh "google/gemma-4-31b-it:free" "$(cat prompt.txt)" 2048
```

⚠️ **SHADOW-OR-001 applies** — this script uses bare OpenRouter without allowlist. Don't run it
with sovereign topics. Filter inputs in caller code before invoking.

---

## 8. MCP integration — 15 tools for Hermes

Once OAuth flow is unblocked, Hermes can invoke `https://mcp.openrouter.ai/mcp` for:

| Tool | Hermes use case |
|---|---|
| `list-models` | "What models can you use?" — answer user questions about OpenRouter coverage |
| `get-credits` | Self-credit-check at session start, daily cron, post-batch |
| `get-generation` | Per-call cost attribution for cost dashboard |
| `list-benchmarks` | "Which model is best at coding?" — answer user questions |
| `list-daily-model-rankings` | Detect auto-router drift — if selection changes drastically, investigate |
| `search-docs` | On-demand OpenRouter feature lookup |

**Hermes should call `get-credits` at session start** and on each major task boundary. Surface
low-credit warnings to user only after the conversation is complete (don't break flow).

**Block `send-message`** (test inference) — Hermes is for production traffic, not probing.

---

## 9. Hermes profile-specific guidance

### 9.1 `hermes_asi` (default — chat)

- Most common profile
- Telegram-bound
- Uses auto-beta cqt=9 by default
- Session stickiness: HIGH priority
- Streaming: mandatory
- MY governance: HARD override to DeepSeek

### 9.2 `hermes_apex` (judgment)

- Constitutional review, verification
- **Do NOT use OpenRouter for apex reasoning.** Escalate to arifOS kernel via arif_judge.
- If user asks "is this constitutionally valid" or "judge this claim":
  ```python
  return arif_judge.judge_deliberate(
      candidate=user_message,
      action_tier="C3",  # SOVEREIGN-tier
      context_source="hermes_apex"
  )
  ```
- Auto-router is identity-unverified, no fff_gate. Cannot seal verdicts. F1 AMANAH.

### 9.3 `hermes_forge` (execution)

- Build, deploy, fix tasks
- OpenRouter use is OK for code generation: `openrouter/auto-beta` cqt=5
- For 1M-context code review: prefer `xiaomi/mimo-v2.5-pro` (1M ctx, ZDR-safe)
- **Do NOT use auto-router for irreversible actions** (deploy, push, seal). Hermes forge
  proposes; F13 SOVEREIGN decides; A-FORGE executes. F1 AMANAH.

---

## 10. Failure modes specific to Hermes

| Symptom | Likely cause | Fix |
|---|---|---|
| "Model not found" 404 | Guardrail blocked the model | Check `aaa-sovereign-guardrail` allowlist |
| Latency > 5s on turn 1 | Cold cache, fresh session | Expected — next turn will hit cache |
| Latency > 5s on turn 3+ | Session stickiness broken | Verify `session_id` is consistent |
| Censored output on MY topic | Auto-router picked MiniMax | Hard override to DeepSeek (see §4) |
| Cost spike | cqt accidentally set to 0 | Verify `cost_quality_tradeoff: 9` in plugin |
| Empty response | Rate limit on free tier | Wait, retry with non-free tier |
| Telegram "message too long" | Auto-router picked long-ctx model | Truncate to 4096 chars |

---

## 11. Hermes MUST NOT do (forbidden patterns)

| Action | Why |
|---|---|
| Use auto-router for 666_JUDGE / 999_SEAL | Identity unverified, no fff_gate, F1 AMANAH |
| Use auto-router for MY governance | Censorship risk via MiniMax in pool, F2 TRUTH |
| Pass PII (myKad, phone, email) to free models | No ZDR guarantee, sovereign exposure |
| Cache credentials in chat/VAULT999/logs | F12 INJECTION |
| Hand-edit `/root/HERMES/config.yaml` | Use Hermes config renderer / SOT regeneration |
| Trigger MCP OAuth with chat-exposed management key | F12 INJECTION — rotate first |
| Use `openrouter/auto` (deprecated) | Use `auto-beta` — 33-67% better benchmarks |
| Skip the `model` response field logging | Lose F11 audit trail |
| Use cqt=0 in Hermes | Apex should never go via OpenRouter |

---

## 12. Operational status (live, 2026-07-24)

| Item | State | Notes |
|---|---|---|
| Hermes primary (MiMo V2.5 Pro UltraSpeed) | ACTIVE | $0.14/M, 1000 tok/s |
| OpenRouter auto-beta fallback | WIRED | SOT priority 2, cqt=9 |
| OpenRouter free fallback | WIRED | SOT priority 3, cqt=9 |
| Ollama local survival | WIRED | SOT priority 4 |
| `OPENROUTER_API_KEY` in vault.env | PRESENT | used by `consult_external.sh` |
| `OPENROUTER_MANAGEMENT_KEY` in vault.env | PRESENT | rotation-pending F13 |
| `consult_external.sh` | FUNCTIONAL | Default model: `google/gemma-4-31b-it:free` |
| MCP server `mcp.openrouter.ai/mcp` | WIRED (enabled, OAuth-pending) | Blocked pending rotation |
| Per-tier CQT in Hermes config | NOT WIRED | Recommended defaults in §5.2 |
| MY governance routing override | DRAFTED (pattern in §4) | Needs implementation |
| Session stickiness on Hermes calls | NOT WIRED | Recommended pattern in §3.1 |
| Credit monitoring cron | NOT WIRED | Recommended script in §5.1 |

---

## 13. Quick reference card for Hermes

```
┌────────────────────────────────────────────────────────────────┐
│  Hermes × OpenRouter Decision Card                             │
├────────────────────────────────────────────────────────────────┤
│  Hermes profile?                                               │
│  ├─ hermes_apex (judgment)  → arifOS kernel (never OpenRouter) │
│  ├─ hermes_forge (build)    → auto-beta cqt=5 (ZDR-safe pool)  │
│  └─ hermes_asi (chat)       → MiMo primary → auto-beta cqt=9   │
│                                                                │
│  MY governance topic? (Najib, 1MDB, PETRONAS, myKad, ...)      │
│  └─ YES → DeepSeek V4 Pro DIRECT (bypass auto-router)           │
│                                                                │
│  Multi-turn Telegram thread?                                    │
│  └─ YES → pass stable session_id (sha256(chat_id+user_id))     │
│                                                                │
│  Always: stream=true, log response.model field for audit       │
│  Never:  constitutional verdicts via auto-router                │
│  Budget: $3/day, $30/month — switch to openrouter/free <$5    │
└────────────────────────────────────────────────────────────────┘
```

---

## DITEMPA BUKAN DIBERI

Forged from live `/api/v1/models` probe + Hermes `config.yaml` + `model-picker.yaml` + SOT
cross-reference. Hermes is the human face of the federation — OpenRouter is its smart fallback,
not its primary. **Use sparingly, override for sovereign topics, never for judgment.**

**Co-Authored-By:** Kimi Code (FI-008) for Hermes (555-ASI).