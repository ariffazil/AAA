# Kimi Code config.toml — Full Schema Map (2026-08-07 snapshot)

Annotated dump of `/root/.arifos/agents/kimi/config.toml` for this federation. Use this to debug model selection, capability mismatches, and provider routing.

## Top-level keys (canonical)

```toml
# Required
default_model = "<provider>/<model>"     # TUI banner; capability match may override at request time
small_model  = "<provider>/<model>"     # Used for title generation + lightweight tasks (ollama/qwen2.5-coder:3b default)

# Operational
default_permission_mode = "yolo"         # or "default", "acceptEdits", "bypassPermissions"
telemetry = true                         # emit usage to telemetry dir
merge_all_available_skills = false       # explicit skill dirs only
extra_skill_dirs = [ "/root/AAA/skills", "/root/.agents/skills" ]
extra_agent_dirs = [ "/root/.arifos/agents/kimi/agents" ]

# Image handling
[image]
max_edge_px = 2000
read_byte_budget = 262144

# Thinking
[thinking]
enabled = true

# Per-provider blocks
[providers.<name>]
type = "anthropic" | "openai" | "openai_chat"
api_key = "env:<VAR>" | "<literal>"
base_url = "https://<endpoint>/<path>"
```

## Configured models (this federation, 2026-08-07)

| Model key | Display | Capabilities | Context | Output |
|---|---|---|---|---|
| `minimax-coding-plan/MiniMax-M3` | MiniMax-M3 | image_in, video_in, thinking, tool_use | 204,800 | 131,072 |
| `minimax-coding-plan/MiniMax-M2.7` | MiniMax-M2.7 | thinking, tool_use | (default) | (default) |
| `minimax-coding-plan/MiniMax-M2.5` | MiniMax-M2.5 | thinking, tool_use | 204,800 | 131,072 |
| `minimax-coding-plan/MiniMax-M2` | MiniMax-M2 | thinking, tool_use | 196,608 | 128,000 |
| `minimax-coding-plan/MiniMax-M2.1` | MiniMax-M2.1 | thinking, tool_use | 204,800 | 131,072 |
| `minimax-coding-plan/MiniMax-M2.7-highspeed` | MiniMax-M2.7-highspeed | thinking, tool_use | 204,800 | 131,072 |
| `minimax-coding-plan/MiniMax-M2.5-highspeed` | MiniMax-M2.5-highspeed | thinking, tool_use | 204,800 | 131,072 |
| `kimi-code/kimi-for-coding` | K2.7 Coding | thinking, always_thinking, image_in, video_in, tool_use | (default) | (default) |
| `kimi-code/kimi-for-coding-highspeed` | K2.7 Coding Highspeed | thinking, always_thinking, image_in, video_in, tool_use | (default) | (default) |
| `deepseek/chat` | DeepSeek V3 (Chat) | thinking, tool_use | (default) | (default) |
| `deepseek/reasoner` | DeepSeek R1 (Reasoner) | thinking, tool_use | (default) | (default) |

## Capability routing — what gets picked when

| Input | Required capability | Filter result |
|---|---|---|
| Plain text prompt, code task | `thinking`, `tool_use` | 11 entries qualify; harness picks by `default_model` priority then `always_thinking` |
| Image attachment | `image_in` | 3 entries: MiniMax-M3, kimi-for-coding, kimi-for-coding-highspeed |
| Video attachment | `video_in` | 3 entries (same as image_in) |
| Sub-agent invocation (af-plan, af-reviewer) | varies per agent | filtered by agent's `[agents.<name>].capabilities` if present |

## Why the TUI shows "MiniMax-M3" even though Kimi K3 is the "primary"

`default_model = "minimax-coding-plan/MiniMax-M3"` is what's rendered in the banner. At request time:
- If the request has NO image/video: harness can route to any thinking-capable model. MiniMax-M3 stays the default unless explicitly overridden.
- If the request HAS an image/video: harness MUST route to an `image_in`-capable model — but still tries `default_model` first. If `default_model` doesn't have `image_in`, falls back to one that does.

To force Kimi K3 primary, change `default_model = "kimi-code/kimi-for-coding-highspeed"` (highspeed variant = cheaper for high volume; non-highspeed = full reasoning).

## Quirk: `always_thinking` cost

`kimi-for-coding` and `kimi-for-coding-highspeed` both have `always_thinking`. This means every chat completion burns reasoning tokens even for trivial prompts. For agents that don't need deep reasoning (af-explore, af-reviewer doing simple yes/no), use MiniMax-M2.5/M2.7 instead.

## Tool to dump the live model table

```bash
grep -B1 -A6 'capabilities.*=.*\[' /root/.arifos/agents/kimi/config.toml \
  | grep -E "^\[|model|capabilities|display"
```

If the table looks empty, the file was hand-edited and lost its `[models.*]` headers. Restore from the most recent `.bak-*` snapshot first.