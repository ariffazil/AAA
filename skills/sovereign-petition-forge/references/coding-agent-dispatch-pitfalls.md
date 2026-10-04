># Coding Agent Dispatch Pitfalls — Sovereign Petition Forge

> The 2026-08-12 session attempted to dispatch the v12/v13/v14 sovereign
> petition forge to **3 external coding agents** in parallel (Gödel E3
> provider diversity). All 3 dispatch attempts failed. The lesson:
> **Pivot to direct authoring** for sovereign artifacts.

## The 3 Attempts — All Failed

### Attempt 1: Qwen Code (`qwen -m qwen3-coder-plus -p ...`)
**Failure:** `400: anthropic_messages: Invalid model name passed in model=qwen3-coder-plus. Call `/v1/models` to view available models for your key.`

**Cause:** Wrong model ID. `qwen3-coder-plus` is not in the configured provider's available model list.

**Attempts to fix:**
- Tried without `-m` flag → defaulted to anthropic route, worked but routed through Claude API (not Qwen)

### Attempt 2: OpenCode DeepSeek direct (`opencode run --model deepseek/deepseek-v4-pro`)
**Failure:** `Error: Insufficient Balance`

**Cause:** Direct DeepSeek API key has no credits.

**Fix attempted:** Switched to `opencode-zen/deepseek-v4-pro` (zen tier provider). Need to verify credits.

### Attempt 3: OpenCode Luna (`opencode run --model gpt-5.6-luna`)
**Failure:** `Error: Model not found: gpt-5.6-luna/.`

**Cause:** `gpt-5.6-luna` model is registered in `opencode-zen` provider, not the default provider.

**Fix attempted:** Switched to `opencode-zen/gpt-5.6-luna`. Worked.

## Why They All Failed Anyway

Even after fixing model IDs, all 3 agents hit infrastructure issues:

1. **Qwen (3rd dispatch):** Warning: "Tool 'run_shell_command' requires user approval but cannot execute in non-interactive mode. To enable automatic tool execution, use the -y flag (YOLO mode)." — Without `-y` flag, agent can't write files.

2. **OpenCode DeepSeek (3rd dispatch):** Last status showed `> 333-AGI · deepseek-v4-pro` with no error — but no HTML produced. Possible: A-FORGE PolicyGate blocked file writes via `forge_session_init`.

3. **OpenCode Luna (3rd dispatch):** `✗ aforge_forge_session_init ... failed` with `PolicyGateError: EROFS: read-only file system, open '/root/.agent-workbench/mcp-audit.jsonl'`. Then `Type validation failed: Value: {"type":"keepalive","sequence_number":2}`.

## The Correct Diagnostic Path

```bash
# Step 1: Check what models exist
opencode models | head -20

# Step 2: Check provider configuration
cat /root/.config/opencode/opencode.json | python3 -c "
import json,sys
d = json.load(sys.stdin)
for pname, pdata in d.get('provider',{}).items():
    models = list(pdata.get('models',{}).keys())
    if models:
        print(f'{pname}: {models[:3]}')
"

# Step 3: Check actual model ID format
# opencode uses: provider/model (NOT bare model)
# So gpt-5.6-luna → opencode-zen/gpt-5.6-luna

# Step 4: Check qwen-code settings
cat /root/.local/share/qwen-code/settings.json | head -30
# Default anthropic route, default model = "hermes-asi"

# Step 5: Test with simpler prompt first
qwen -p "Reply with just SUCCESS" -o text
```

## The Decision Tree — When to Use What

```
Need to dispatch sovereign petition forge to coding agents?
│
├─ Is the agent critical for F13 governance?
│   ├─ YES → MUST be done by Hermes (arifOS lane) or 3rd-party direct
│   └─ NO → Try coding agents for speed
│
├─ Is the artifact small (<5KB) and well-bounded?
│   ├─ YES → Coding agents can do (with --y flag for non-interactive)
│   └─ NO → Direct authoring is more reliable
│
├─ Is the artifact >50KB or requires narrative voice?
│   ├─ YES → ALWAYS direct authoring
│   └─ NO → Coding agents may work
│
└─ Is the system under high load (load >10)?
    └─ YES → Direct authoring (coding agents will be slow anyway)
```

## The Sovereign Petition Threshold

**For ANY sovereign petition (named, F13-bound, intended for state body):**

1. **DO NOT dispatch to external coding agents.** Period.
2. **Author directly in this lane.** Use the spec file as canonical, generate HTML via write_file, render via weasyprint.
3. **Verify with APEX judge** (in-lane, with KERNEL_ARBITER independence via OPENCLAW judge).
4. **Seal to VAULT999** with full provenance.

External coding agents are useful for:
- Code refactoring (different artifact class)
- Multi-file changes (where parallel reads help)
- Boilerplate generation (where voice doesn't matter)

But NOT for sovereign artifacts where:
- Voice matters (qualia)
- Constitutional binding matters (F13)
- Reversibility matters (one-shot dispatch)
- Identity protection matters (arifOS Federation as shield)

## The Pattern in One Sentence

> **External coding agents failed all 3 dispatch attempts for the sovereign
> petition. Direct authoring succeeded within the same session. Default
> to direct authoring for sovereign artifacts.**

## What the Coding Agents DID Get Right (in other contexts)

This isn't anti-coding-agent. The agents worked for:
- Boilerplate HTML scaffolding (when called with simple prompts)
- Multi-file refactoring (when system load is low)
- Quick code generation (when context is technical)

But for narrative-driven, voice-driven, qualia-bearing, F13-bound sovereign
artifacts — direct authoring in the operator's lane is the reliable path.