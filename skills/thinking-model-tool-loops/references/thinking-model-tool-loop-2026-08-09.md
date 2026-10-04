# Thinking Model Tool Loop Incident — 2026-08-09

## The Incident

Hermes Agent (hermes-asi) repeatedly failed mid-task with:
```
⚠️ The model provider failed after retries. I kept raw provider details out of chat; check gateway logs for diagnostics.
```

## Live Diagnosis

### Step 1: Direct curl probe (control test)
```bash
curl -s -m 15 http://127.0.0.1:4000/v1/chat/completions \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"hermes-asi","messages":[{"role":"user","content":"ping"}],"max_tokens":5}'
```
Result: HTTP 200, `completion_tokens=5`, `reasoning_tokens=4`, empty `content` (reasoning consumed budget).

### Step 2: Gateway log inspection
```bash
journalctl -u litellm-federation --since "45 min ago" | grep -i "error|400|fail"
```
Found the killer error:
```
BadRequestError: The `reasoning_content` in the thinking mode must be passed back to the API.
```
Plus fallback errors:
```
Function call is missing a thought_signature in functionCall parts (Gemini)
Invalid model name passed in model=deepseek-chat (DeepSeek routing issue)
```

### Step 3: Config inspection
```bash
grep -A5 "hermes-asi" /root/A-FORGE/litellm-config.yaml | grep -E "model:|order:|api_base:"
```
Found: `openai/mimo-v2.5` (MiMo primary), `openai/gemini-3.6-flash` (Gemini fallback with wrong prefix).

## Root Cause

Hermes Agent Issue #24443 — Hermes normalizes assistant messages to standard fields and strips `reasoning_content`. MiMo requires this field on all subsequent turns when thinking mode is enabled.

## Fix Applied

1. Disabled thinking mode for MiMo in litellm config
2. Changed Gemini from `openai/` to `gemini/` prefix
3. Added `modify_params: true` to litellm_settings
4. Removed Gemini from tool-loop agent seats (hermes-asi, opencode, codex, agi-333)
5. Created dedicated Gemini seats (`gemini-flash`, `gemini-pro`) for single-turn/vision

## Key Learnings

- 400 error on thinking model after tool call = reasoning state issue, NOT auth
- Gemini prefix (`gemini/` vs `openai/`) determines thought_signature handling
- LiteLLM does NOT cascade fallback on HTTP 400 → silent agent death
- Tool-loop agents should NOT use thinking models until client preserves reasoning state
