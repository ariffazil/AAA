# Gemini Provider Integration — Session Findings (2026-08-09)

## Integration Architecture Confirmed

Arif locked in the following provider integration doctrine on 2026-08-09:

```
GEMINI_API_KEY → vault only (kunci-mas.env line 138)
├── FED seats: gemini-flash / gemini-pro / fed/image-gen / fed/vision(secondary)
│     OpenAI-compat or native gemini/ → single-turn, vision, image
├── hermes-asi / opencode / codex / agi-333
│     NO Gemini (tool loops need MiMo/Qwen + reasoning_content pad)
└── Future: gemini-interactions sidecar
      store + previous_interaction_id → real multi-tool Gemini
```

## Commits

- A-FORGE `5b93df5c` — stripped Gemini from agi-333/opencode/codex, created new seats
- AAA `8dd9738f` — updated CALL_MAP and GEMINI_INTEGRATION.md docs

## Smoke Test Results (post LiteLLM boot)

| Seat | Result |
|------|--------|
| `gemini-pro` → PONG | ✅ |
| `hermes-asi` → PONG | ✅ |
| `gemini-flash` → HTTP 200, empty content | ⚠️ (thinking model parks text in reasoning at minimal effort — seat is registered) |
| Interactions API → INTERACT_OK | ✅ |

## Full Model Pricing Table (Aug 2026)

| Model | Input/M tokens | Output/M tokens | Context | Notes |
|-------|---------------|----------------|---------|-------|
| Gemini 3.1 Pro | $3.00 | $12.00 | 2M | Flagship, paid only |
| Gemini 3.6 Flash | $1.50 | $7.50 | 1M | Good value for agents |
| Gemini 3.5 Flash | $1.00 | $4.00 | 1M | Budget balanced |
| Gemini 3.5 Flash-Lite | $0.40 | $0.40 | 1M | Cheapest high-volume |
| Gemini 2.5 Flash | $0.075 | $0.30 | 1M | Cheapest reasoning |
| MiMo (current hermes-asi primary) | ~$0.14 | $0.28 | 1M | Cheapest overall by ~10x |

## LiteLLM Config Locations

- **litellm-config.yaml:** `/root/A-FORGE/litellm-config.yaml`
- **API keys:** `/root/.secrets/kunci-mas.env` (GEMINI_API_KEY line 138, GEMINI_BASE_URL line 139)
- **FED seats:** All Gemini models use `os.environ/GEMINI_API_KEY`

## Existing Gemini Seats in litellm-config.yaml (as of session)

| Seat | Model | api_base | Order |
|------|-------|----------|-------|
| `agi-333` | `openai/gemini-3.6-flash` | Google OpenAI-compat | 1 |
| `opencode` | `openai/gemini-3.6-flash` | Google OpenAI-compat | 1 |
| `codex` | `openai/gemini-3.6-flash` | Google OpenAI-compat | 1 |
| `fed/image-gen` | `openai/gemini-3-flash-preview` | Google OpenAI-compat | 0 |

Note: After Arif's 2026-08-09 fix, Gemini was STRIPPED from agi-333/opencode/codex tool loop paths. New seats `gemini-flash` and `gemini-pro` were created as single-turn alternatives.

## Antigravity Managed Agent Deployed

- **Agent ID:** `federation-agent`
- **Base agent:** `antigravity-preview-05-2026`
- **Model:** `gemini-3.6-flash`
- **Created via:** `client.agents.create()` REST API
- **Files mounted:** `.agents/AGENTS.md` (arifOS constitution) + `.agents/skills/apex-theory/SKILL.md`
- **Verified:** HTTP 200 on interaction call
- **Note:** `"environment": "remote"` is REQUIRED in every interaction or you get 400 error

## Key Pitfalls Discovered

1. **Google's OpenAI-compat endpoint** (`generativelanguage.googleapis.com/v1beta/openai`) is the stable path. Native `gemini/` route has LiteLLM bug #14771 (Vertex AI credential confusion).

2. **Gemini thinking models return empty content** when reasoning is parked in thought blocks at minimal effort. This breaks tool loops. Use MiMo/Qwen for tool-loop seats.

3. **Interactions API requires `"environment": "remote"`** field or returns 400. This is mandatory for managed agents.

4. **agy CLI requires TTY** — does not work in non-interactive terminal. Use REST API directly for headless operations.

5. **Free tier is gutted** (Feb 2026) — many models return `429 with "limit: 0"`. Paid billing required for most production workloads.

## GENESIS Documents Forged (2026-08-09)

During this session, Arif forged two constitutional GENESIS documents:

1. **LAYER_SEPARATION_DOCTRINE.md** — "AAA bukan protocol. AAA adalah constitutional state."
   - Path: `/root/arifOS/GENESIS/LAYER_SEPARATION_DOCTRINE.md`
   - Git: `38cac609e`
   - Three strata: Immutable (L4-L6), Replaceable (L2-L3), Disposable (below L2)

2. **AUTHORITY_LAYER_DOCTRINE.md** — did:web=identity, ACT=authority, F1-F13=constitution, VAULT999=evidence
   - Path: `/root/arifOS/GENESIS/AUTHORITY_LAYER_DOCTRINE.md`
   - Git: `b33d0a2d3`
   - Separation of powers: 333=propose, 555=verify, 888=judge, A-FORGE=execute, VAULT999=witness

Both documents are sealed to GENESIS and referenced by the AGENTS.md pointer system.
