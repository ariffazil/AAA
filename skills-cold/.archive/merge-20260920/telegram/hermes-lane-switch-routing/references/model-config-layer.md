# Model Config Layer — Reality (2026-08-19)

## Quick answer

`config.yaml` → `model.default` is the **sole source** of the default LLM model.
FED `fed_route` handles capability-based task routing.
There is **no** `model_override` in `lanes.yaml`.
There is **no** `gateway_routing` config file.

## What actually exists

| Thing | Exists? | Where |
|---|---|---|
| `model.default` | ✅ Yes | `config.yaml` line 2 |
| `custom_providers[].models` | ✅ Yes | `config.yaml` lines 99-107 |
| FED `fed_route` task routing | ✅ Yes | MCP tool, routes by capability signature |
| Session-level `/model` switch | ✅ Yes | Runtime only, not persisted to config |
| `model_override` per-lane | ❌ No | Not in `lanes.yaml` or anywhere |
| `gateway_routing` config | ❌ No | Zero hits across `/root/HERMES/` |

## The actual routing chain

```
Telegram message → lane_switch resolves lane
                 → model.default from config.yaml (i-arif)
                 → FED fed_route may upgrade to agi-333/asi-555 for heavy reasoning
                 → LLM responds
```

## Common false assumption

"I put `model_override: i-arif` in my lane so it should use that model."

**Reality:** `lanes.yaml` has NO `model_override` field. The lane_switch plugin injects memory/soul/voice/capability context — it does NOT select the LLM model. Model selection is config.yaml → FED routing.

## How to verify

```bash
# 1. What does config say?
grep "default:" /root/HERMES/profiles/aaa-hermes/config.yaml | head -1

# 2. What was it before the last change?
grep "default:" /root/HERMES/profiles/aaa-hermes/config.yaml.pre-*

# 3. Does model_override exist anywhere?
grep -r "model_override" /root/HERMES/lanes/ /root/HERMES/profiles/ --include="*.yaml"

# 4. Does gateway_routing exist?
find /root/HERMES -name "*gateway_routing*" 2>/dev/null
```

## Drift diagnosis pattern

When someone says "the model should be X but it's acting like Y":

1. Read `config.yaml` → `model.default`
2. Check pre-upgrade backup (`config.yaml.pre-*`) for the previous value
3. Note: runtime `/model i-arif` changes session header ONLY, not config
4. Search for `model_override` / `gateway_routing` → confirm they don't exist
5. FED `fed_probe` + `fed_route` to verify the routing chain is healthy

## Recommended default for Telegram

`model.default: i-arif` — the human edge bridge model. Reads SOUL.md, speaks BM Penang, follows The One Rule.

`agi-333` / `asi-555` stay available through FED `fed_route` for deep reasoning tasks — FED auto-selects based on capability signature (`fed-reasoning-heavy`, `fed-agent-subagent`, etc.).
