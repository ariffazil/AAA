# Codex CLI 0.147 Config Fix — 2026-08-14

## Context

Codex was upgraded to 0.147.0. On next invocation, it refused to start with
a cascade of config errors. Two config files needed fixing:
- `~/.codex/config.toml` — deprecated `wire_api` values
- `~/.codex/model-catalog.local.json` — schema violations

The errors surface one at a time (fix one → restart → next error), so the
diagnosis required ~6 iterations. This file captures all fixes in one batch.

## config.toml Fixes

All `[model_providers.*]` blocks with `wire_api = "chat"` must change to
`wire_api = "responses"`. In the arifOS federation, two blocks had it:

- `[model_providers.minimax-direct]` — `wire_api = "chat"` → `"responses"`
- `[model_providers.zai-coding]` — `wire_api = "chat"` → `"responses"`

Search command:
```bash
grep -n 'wire_api.*"chat"' ~/.codex/config.toml
```

## model-catalog.local.json Fixes

The catalog had ~15 model entries; 7 were non-conformant. Violations found,
in the order they surfaced:

1. `input_modalities` contained `"video"` — only `text`, `image`, `audio` valid
2. `visibility` was `"hidden"` — valid values are `list`, `hide`, `none`
3. `supported_reasoning_levels` was `["low","medium","high"]` (strings) —
   must be list of objects: `[{"effort":"low","description":"..."}]`
4. `truncation_policy` was `"auto"` (string) — must be object:
   `{"mode":"bytes","limit":10000}` (mode must be `bytes` or `tokens`)
5. Missing `supported_reasoning_levels` field entirely
6. Missing many other required fields (sparse entries vs first model's full schema)

### Batch-Fix Script

This script normalizes ALL model entries to match the schema of the first
complete model. Run after each `failed to parse` error to catch the next
violation:

```python
#!/usr/bin/env python3
"""Batch-fix model-catalog.local.json for Codex 0.147+ compat."""
import json

CATALOG = "/root/.codex/model-catalog.local.json"

with open(CATALOG) as f:
    data = json.load(f)

first = data["models"][0]
valid_vis = {"list", "hide", "none"}
valid_mods = {"text", "image", "audio"}

# Template for supported_reasoning_levels (struct format)
template_levels = [
    {"effort": "low", "description": "Fast responses"},
    {"effort": "medium", "description": "Balanced"},
    {"effort": "high", "description": "Deep reasoning"},
]

fixed = 0
for m in data["models"]:
    # 1. Fix visibility
    v = m.get("visibility")
    if v not in valid_vis:
        m["visibility"] = "hide" if m.get("deprecated") else "list"
        fixed += 1

    # 2. Fix input_modalities (remove invalid, keep valid)
    mods = m.get("input_modalities", [])
    bad = [x for x in mods if x not in valid_mods]
    if bad:
        m["input_modalities"] = [x for x in mods if x in valid_mods]
        fixed += 1

    # 3. Fix supported_reasoning_levels (string → struct)
    srl = m.get("supported_reasoning_levels")
    if isinstance(srl, list) and srl and isinstance(srl[0], str):
        m["supported_reasoning_levels"] = template_levels
        fixed += 1
    elif "supported_reasoning_levels" not in m:
        m["supported_reasoning_levels"] = template_levels
        fixed += 1

    # 4. Fix truncation_policy (string → struct)
    tp = m.get("truncation_policy")
    if isinstance(tp, str):
        m["truncation_policy"] = {"mode": "bytes", "limit": 10000}
        fixed += 1
    elif isinstance(tp, dict):
        if tp.get("mode") not in ("bytes", "tokens"):
            m["truncation_policy"] = {"mode": "bytes", "limit": 10000}
            fixed += 1

    # 5. Fill in any missing fields from the first complete model's schema
    #    (use sensible defaults per field type)
    field_defaults = {
        "input_modalities": ["text", "image", "audio"],
        "experimental_supported_tools": ["function_call"],
        "shell_type": "default",
        "codex_lanes": [],
        "codex_escalation": "",
        "truncation_policy": {"mode": "bytes", "limit": 10000},
        "effective_context_window_percent": 100,
        "supports_image_detail_original": True,
        "base_instructions": "",
        "support_verbosity": False,
        "supports_parallel_tool_calls": True,
        "supports_reasoning_summaries": False,
        "selection_reason": "",
    }
    for k, dv in field_defaults.items():
        if k not in m:
            m[k] = dv
            fixed += 1

with open(CATALOG, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Fixed {fixed} field violations across {len(data['models'])} models")
```

## Provider Override (No --provider Flag)

Codex 0.147 removed the `--provider` flag. Use `-c` config override:
```bash
codex exec -c model_provider="litellm-federation" --sandbox danger-full-access "task"
```

## Session Notes

- The arifOS federation's FED middleware at :4010 was also down during this
  session (connection refused). LiteLLM at :4000 was up but all upstream
  providers were rate-limited/exhausted (MiniMax 429, Gemini 429, DeepSeek 402).
  The config fixes here are durable; the provider exhaustion is transient.
- After fixing config, verify with: `codex --version` (should print version
  without errors) then `codex exec "echo hello"` for a quick model-agnostic test.
