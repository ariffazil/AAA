# Gemini Integration — arifOS Federation

> **SOT:** Google [Thinking](https://ai.google.dev/gemini-api/docs/thinking) · [Interactions API](https://ai.google.dev/gemini-api/docs/interactions-overview) · [OpenAI compat](https://ai.google.dev/gemini-api/docs/openai)  
> **Vault:** `GEMINI_API_KEY` in KUNCI-MAS only  
> **Forged:** 2026-08-09  

## Doctrine (one line)

> Gemini thinking models **require thought signatures** across multi-turn tool work.  
> FED may call Gemini for **chat / vision / image**. Hermes multi-tool seats **must not** land on Gemini until a client preserves signatures (or uses Interactions stateful mode).

## Two Google APIs (do not confuse)

| API | Signature handling | Use in federation |
|-----|--------------------|-------------------|
| **OpenAI-compat** `…/v1beta/openai/chat/completions` | Signatures as metadata on parts / `provider_specific_fields`; **client must echo** | LiteLLM seats for single-turn & vision |
| **Interactions** `…/v1beta/interactions` | **Stateful (recommended):** `store` + `previous_interaction_id` — server keeps signatures | Future thin adapter for agentic Gemini tools |
| **generateContent** | Signatures on any part (incl. `functionCall`) | Native SDK paths |

### Thought steps (Interactions)

| Field | Required | Role |
|-------|----------|------|
| `signature` | Yes | Encrypted reasoning state — **must** be preserved (server does this in stateful mode) |
| `summary` | No | Human-readable thought; may be empty |

Stateless Interactions: resend every `thought` block unchanged.  
Stateful: pass `previous_interaction_id` — **do not manage signatures yourself**.

## Secrets (5-R)

```bash
# only in kunci-mas.env
GEMINI_API_KEY=...
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai
make -f /root/.secrets/Makefile vault-generate
systemctl restart litellm-federation
```

LiteLLM unit: `EnvironmentFile=/root/.secrets/kunci-mas.flat.env`.

## FED seats (current policy)

| Seat | Route | Allowed |
|------|--------|---------|
| **`gemini-flash`** | `gemini/gemini-3.6-flash` (+ 2.5 fallback) | Explicit chat / vision one-shot |
| **`gemini-pro`** | `gemini/gemini-3.1-pro-preview` | Deep multimodal reasoning (non-tool or Interactions later) |
| **`fed/image-gen`** | Gemini + Wan | Image generation |
| **`fed/vision`** | Qwen/MiMo primary; Gemini order 50 | Image Q&A secondary |
| **`hermes-asi` / `opencode` / `codex` / `agi-333`** | **No Gemini** | Tool loops — MiMo/Qwen/DeepSeek/MiniMax only |

Call via FED:

```bash
curl http://127.0.0.1:4000/v1/chat/completions \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gemini-flash","messages":[{"role":"user","content":"ping"}],"max_tokens":16}'
```

## Hermes / OpenClaw rule

- Primary: `model=hermes-asi` → FED → **non-Gemini** thinking backends + `_needs_fed_thinking_proxy` (reasoning_content pad for MiMo/DeepSeek).
- **Never** re-add `openai/gemini-*` to hermes-asi pool without thought_signature round-trip in Hermes.
- Direct `providers.gemini` in Hermes config is catalog-only until Interactions adapter exists.

## Interactions API (agent-grade Gemini — future / opt-in)

When multi-turn tools + Gemini are required:

```python
from google import genai
client = genai.Client()  # GEMINI_API_KEY in env

# Turn 1 — stateful
i1 = client.interactions.create(
    model="gemini-3.6-flash",
    input="…",
    # store defaults true in stateful usage
    generation_config={"thinking_level": "low"},
)

# Turn 2 — server holds signatures
i2 = client.interactions.create(
    model="gemini-3.6-flash",
    input="…",
    previous_interaction_id=i1.id,
)
```

Federation placement: thin **A-FORGE or HERMES sidecar** (`gemini-interactions` service), not generic OpenAI chat completion through Hermes loop.

## Pricing note

Billable = **output tokens + thought tokens** (`total_thought_tokens`). Prefer `thinking_level: minimal|low` for simple tasks.

## Smoke checklist

1. `curl` AI Studio OpenAI `/models` with `GEMINI_API_KEY` → model list  
2. `POST /v1beta/interactions` → `status=completed`  
3. FED `model=gemini-flash` → 200  
4. FED `model=hermes-asi` multi-tool → **no** Gemini 400 thought_signature  
5. Hermes journal: no `thought_signature` errors after tool turns  

## Related

- Hermes mid-task pad: `/root/forge_work/2026-08-09-hermes-reasoning-pad/`  
- CALL_MAP: `/root/AAA/docs/CALL_MAP.md`  
- LiteLLM config: `/root/A-FORGE/litellm-config.yaml`  

DITEMPA BUKAN DIBERI.
