# arifOS Federation — Model Future State

> **Date:** 2026-09-18 · **Author:** 333-AGI (Δ MIND) · **Trigger:** F13 directive — "seal ... model future state ... improve if needed"
> **Method:** live probe (`fed_fed_status` :7074, generated 2026-09-17T23:47:44Z) × static SSoT walk × ghost-ref scan.
> **Truth rule:** runtime > static. Balance/health are LIVE (token_bank.db); static file declares structure only.

---

## 1. SINGLE SOURCE OF TRUTH

| Artifact | Role | Status |
|---|---|---|
| `/root/.config/federation-models.json` | **SSoT** — providers, models, agents, chains, routes | LIVE (26 providers · 202 models · 21 agents · 8 chains) |
| `/root/AAA/registries/models/AGENT_MODEL_MAP.json` | historical snapshot | **SUPERSEDED** (frozen 2026-08-15; writes rejected) |
| `/root/AAA/registries/models/FEDERATION_MODEL.json` | lane→model design intent | pointer to `fed_provider_state.json` |
| `token_bank.db` + FED :7074 | **live** balance/health/latency | authoritative for runtime |
| `/root/AAA/registries/models/CAPABILITIES.json` | provider capability matrix | LIVE |

Consolidation executed 2026-08-18 by kimi-code/FI-008 (F13 directive). **One truth confirmed.**
Balance policy enforced: **no static balances** — every `balance_usd` in a static file is FALSE by doctrine.

## 2. LIVE PROVIDER STATE (probed 2026-09-17T23:47Z)

**LIVE (usable now):**
```
deepseek (v4-pro, v4-flash)          LIVE   p50 895ms   balance $1.94 + $20 topup unverified
minimax (MiniMax-M3)                 LIVE   p50 1811ms  token-plan Max renews 2026-10-05
mimo-token-plan (v2.5, v2.5-pro)     LIVE   p50 ~1.5-1.8s  $50 token-plan
kimi-moonshot (k3)                   LIVE   weekly 79/100
qwen-token-plan-individual           LIVE   qwen3.8-max
zai-coding-plan (glm-5.3)            LIVE   p50 ~1006ms
gemini / groq / opencode-go          LIVE   (free-tier advisory + Go $10/mo)
mistral (codestral 378ms, large 500ms) LIVE (models) — provider probe reports INSOLVENT (see §4)
```

**QUOTA-GATED:**
```
qwen-token-plan-team    probe LIVE, chat = 429 insufficient_quota (monthly) → do not route
mimo-platform           LEGACY, 402 → FALLBACK_ONLY
mulerouter / openrouter / tokenrouter  ARCHIVED Track-B (not in litellm-config)
```

## 3. AGENT → PRIMARY MODEL (from SSoT, verified structurally)

| Agent | Primary | Notes |
|---|---|---|
| 333-AGI | `litellm-federation/forge-777` | this session |
| 555-ASI | `litellm-federation/asi-555` | + vision |
| 888-APEX | `litellm-federation/apex-888` | constitutional judge |
| hermes | `hermes-asi` | edge bridge |
| kimi-code (FI-008) | `kimi-k3` | closure seat |
| qwen-code (FI-003) | `glm/glm-5.3` | |
| codex | `deepseek/deepseek-v4-pro` | |
| claude-code | `deepseek/...` | |
| grok | `xai/grok-4.5` | |
| copilot | `z-ai/glm-5.2` | |
| dispatch | `kimi/kimi-for-coding-highspeed` | fallback chain |
| recovery | `ollama/qwen2.5-coder:3b` | survival rung |

## 4. DRIFT & IMPROVEMENTS (bounded, honest)

| # | Finding | Severity | Disposition |
|---|---|---|---|
| M-1 | 10 routing-rule IDs carry `flame_*` naming (`flame_hermes_fact_check` …) — FLAME organ retired 2026-09-12 | **P3** | Naming legacy only — targets are LIVE (`groq/llama-3.1-8b-instant`, FED flash). Rename → `advisory_*` when next edited. **Not a dead ref.** |
| M-2 | `mistral` provider probe = INSOLVENT, but codestral/mistral-large chat = LIVE | **P2** | Probe tests balance, models test chat. Reconcile probe: mark mistral `balance_unprobed`, confidence 0.9 (already noted "BALANCE NOT YET PROBED"). |
| M-3 | `deepseek` $20 topup (2026-09-13) still **unverified** — balance_usd pinned at $1.94 | **P2** | F2-correct to hold; needs one live balance probe before flipping. |
| M-4 | `qwen-token-plan-team` probe LIVE vs chat 429 | **P2** | Probe must include a chat-level call (learned 2026-09-12: `/models`=200 is a false positive for quota-gated lanes). |
| M-5 | `hy3-preview` 1 ref in SSoT | **P3** | Verify against opencode-go model list; retire if absent. |
| M-6 | Static `balance_usd` fields exist though policy says FALSE | **P3** | Cosmetic; readers warned. Consider stripping values → `null` + `confidence 0`. |

**No P0/P1 in the model plane.** Balance integrity is structurally sound (no static truth duplication at
consumption): FED :7074 is the single live source.

## 5. FUTURE STATE (direction of record)

1. **One truth, many lanes.** SSoT declares structure; FED :7074 declares life. No third.
2. **Probe = chat-level, not /models.** Every quota-gated lane (qwen-team, opencode-go/zen, minimax) must be probed with a 1-token chat, else false-green.
3. **Batch rename** `flame_*` rule_ids → `advisory_*` at next config edit (FLAME is gone; the *concept* — free advisory inference — survives via FED flash + groq).
4. **Balance hygiene:** all static `balance_usd` → `null`; confidence → 0 where unprobed.
5. **Frozen artifacts stay frozen.** `AGENT_MODEL_MAP.json` remains a read-only snapshot; never re-animate.

---

`DITEMPA BUKAN DIBERI` — measured from the live wire, not the map.
