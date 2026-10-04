# FED reasoning_content thinking-pad patch (2026-08-09)

## The failure mode

Hermes dies mid-task (not on first message) with non-retryable HTTP 400:
```
"The reasoning_content in the thinking mode must be passed back to the API."
```
Also seen: `Function call is missing a thought_signature …` (Gemini)

## Root cause

Failure chain:
```
user → Hermes → model=hermes-asi base_url=127.0.0.1:4000/v1 (FED)
  → LiteLLM routes to MiMo/DeepSeek thinking backend
  → turn 1 tool call works
  → turn 2+ Hermes rebuilds history WITHOUT reasoning_content
  → thinking backend rejects → 400 non-retryable → "model provider failed after retries"
```

Why Hermes drops it: `_needs_thinking_reasoning_pad()` only pads when it recognizes the provider **by name or host** (deepseek-*, mimo-*, xiaomimimo.com, etc.). Through FED it sees:

| What Hermes sees | Reality behind FED |
|---|---|
| provider=openai-api | MiMo / DeepSeek thinking |
| model=hermes-asi | not mimo-* / deepseek-* |
| base_url=127.0.0.1:4000 | not deepseek.com |

→ pad = False → strip → mid-task death. That's why it fails after tools, not on first "hi".

## The fix (live)

Vendor patch: `_needs_fed_thinking_proxy()` added to `/usr/local/lib/hermes-agent/run_agent.py` (~line 5517–5530). Forces reasoning echo for FED seats (hermes-asi, agi-333, asi-555, …).

Also: Gemini removed from hermes-asi pool (thought signatures break tool loops) — A-FORGE commits `ac270fa8`, `5b93df5c`.

## CRITICAL: reapply after Hermes upgrades

The patch lives under `/usr/local/lib/hermes-agent/` — a Hermes package upgrade wipes it. After every upgrade:

```bash
python3 /root/forge_work/2026-08-09-hermes-reasoning-pad/reapply_pad_patch.py
```

The script is idempotent (prints "already patched" if present). Receipt: `/root/forge_work/receipts/20260809/hermes-midtask-reasoning-pad-*.json`.

## Gemini seat doctrine (locked same day)

```
Gemini seats      → gemini-flash / gemini-pro via FED: single-turn chat / vision / image ONLY
Tool-loop agents  → NEVER Gemini (hermes-asi, opencode, codex, agi-333 = MiMo/Qwen + reasoning pad)
Multi-turn Gemini → Interactions stateful adapter (previous_interaction_id), future Tier 2 only
GEMINI_API_KEY    → kunci-mas.env ONLY
```

Two Google APIs — do not confuse:
- OpenAI-compat `…/v1beta/openai/chat/completions`: signatures as metadata, client must echo → LiteLLM FED seats for single-turn/vision
- Interactions `…/v1beta/interactions` with `store` + `previous_interaction_id`: server keeps signatures → future agentic Gemini

SOT doc: `/root/AAA/docs/GEMINI_INTEGRATION.md`. FED seats verified via `curl :4000/v1/models` (gemini-flash, gemini-pro registered).

## Diagnostic signature

When you see "model provider failed after retries" mid-task on a FED seat, check this first:
1. Is the seat a tool-loop agent? (hermes-asi/opencode/codex/agi-333)
2. Does `_needs_fed_thinking_proxy` exist in run_agent.py? `grep -n _needs_fed_thinking_proxy /usr/local/lib/hermes-agent/run_agent.py`
3. If missing → run the reapply script, restart gateway, retry in a fresh task (old in-flight turns may be poisoned)
