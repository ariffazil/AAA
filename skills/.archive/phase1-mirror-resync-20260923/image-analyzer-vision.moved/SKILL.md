---
name: "image-analyzer-vision"
id: "image-analyzer-vision"
version: 1.0.0
owner: AAA
risk_tier: low
floor_scope: [F1, F2, F4, F7]
description: "Adds visual understanding to text-only Token Plan models (glm-5, glm-4.7, MiniMax-M2.5, qwen3-max-2026-01-23, qwen3-coder-next, qwen3-coder-plus) by routing image inputs through a vision-capable model. Activates when the user passes an image to a text-only model or asks 'what's in this image'."
autonomy_tier: T1
---

For text-only Token Plan models, use this skill to gain visual understanding by delegating to a vision-capable model (`qwen3.7-plus`, `qwen3.6-plus`, `qwen3.5-plus`, `kimi-k2.5`, `qwen3.8-max`).

User request: $ARGUMENTS

## When to use

| If user is on... | They already have vision | Don't load this skill |
|---|---|---|
| `qwen3.8-max` | ✅ | ✓ |
| `qwen3.7-plus` | ✅ | ✓ |
| `qwen3.6-plus` | ✅ | ✓ |
| `qwen3.5-plus` | ✅ | ✓ |
| `kimi-k2.5` | ✅ | ✓ |
| `qwen3-max-2026-01-23` | ❌ | Load this skill |
| `qwen3-coder-next` | ❌ | Load this skill |
| `qwen3-coder-plus` | � | Load this skill |
| `glm-5` | ❌ | Load this skill |
| `glm-4.7` | ❌ | Load this skill |
| `MiniMax-M2.5` | ❌ | Load this skill |

## Recommended: switch to a vision model directly

The simplest path — if the user is on a text-only model but frequently needs vision, switch:

```bash
# Claude Code
/model qwen3.7-plus   # or qwen3.6-plus / qwen3.5-plus / kimi-k2.5

# OpenCode
/models   # then search and select

# Qwen Code
/model    # then select

# OpenClaw — edit ~/.openclaw/openclaw.json:
#   agents.defaults.model.primary → "bailian/qwen3.7-plus"
```

Then pass images directly: paste, drag-drop, or reference a path in the conversation.

## Alternative: add this Skill for delegation

Use this only when the user **must stay** on the text-only model (e.g., code-generation specific model).

For **Claude Code**:

```bash
mkdir -p .claude/skills/image-analyzer
```

Create `.claude/skills/image-analyzer/SKILL.md`:

```markdown
---
name: image-analyzer
description: Helps models without vision capabilities understand images. Use this skill when you need to analyze image content, extract information, text, or UI elements from images, or understand screenshots, charts, architecture diagrams, or any visual content. Simply pass in the image path to get a description.
model: qwen3.7-plus
---

qwen3.7-plus has visual understanding capabilities. Use qwen3.7-plus directly for image understanding.

When given an image path, read the image (you can pass it via the Read tool), then call qwen3.7-plus with the image to extract a description. Return the description to the user.
```

For **OpenCode**, instead use an Agent at `.opencode/agents/image-analyzer.md`:

```markdown
---
description: Helps models without vision capabilities understand images.
mode: subagent
tools:
  bash: true
  write: false
  edit: false
---

Delegate to qwen3.7-plus (vision-capable) for image understanding. Pass the image path or URL via the prompt and request a structured description.
```

For **OpenClaw / Hermes / Codex / Qwen Code / Qoder** — see `token-plan-bailian-config` skill for the skill-paths table.

## Steps

1. Identify the user's current model (from the active tool's model picker or `~/.openclaw/openclaw.json`).
2. If vision-capable → tell them they already have it; do nothing.
3. If text-only → recommend switching to `qwen3.7-plus` (simplest), OR install the Skill/Agent pattern above (preserves current model).

## Notes

- **Cost**: Switching to `qwen3.7-plus` is the same Token Plan Credits as the text-only model — no surcharge for vision. Using a Skill that delegates to `qwen3.7-plus` counts as two Token Plan invocations (parent + delegate).
- **F2 TRUTH**: never claim to "see" an image if your active model is text-only without this skill loaded. Be honest: "I'm on <text-only-model>, switch to <vision-model> or load `image-analyzer-vision` first."
- **OpenClaw cache invalidation**: after editing `~/.openclaw/openclaw.json`, clear `~/.openclaw/agents/main/agent/models.json` and restart the gateway, otherwise old config sticks.
