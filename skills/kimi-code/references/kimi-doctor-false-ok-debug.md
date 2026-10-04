# kimi doctor False-OK — Strict vs Salvage Validation Debug

> Compiled 2026-08-14. Source: live debugging of kimi-code 0.36 config validation failure.

## The Problem

`kimi doctor` reports `OK config.toml` while `kimi login` fails with:
```
Cannot change settings while /root/.kimi-code/config.toml is invalid
— fix it first (run kimi doctor for details).
```

This is a diagnostic dead end: the fix instruction points to the tool that says everything is fine.

## Root Cause: Two Validation Paths

Kimi Code has **two config parsing paths**:

| Path | Function | Used by | Behavior on invalid keys |
|------|----------|---------|--------------------------|
| **Salvage** | `salvageConfigData()` | `kimi doctor`, runtime boot | Drops invalid entries silently, reports success |
| **Strict** | `parseConfigData()` → `KimiConfigSchema.parse()` | `kimi login`, config writes | Throws `CONFIG_INVALID` on first error |

The salvage path works by looping: it parses, finds errors, deletes the offending entries from a copy, and retries until it either succeeds (returning `dropped: [...]`) or runs out of things to drop.

The strict path is used by `readConfigFileForUpdate()` — any operation that reads-merges-writes config (login, model change, setting change). It explicitly does NOT salvage, because a salvaged base would silently drop the user's broken-but-fixable sections on rewrite.

## Binary Reverse-Engineering Technique

The kimi-code binary is a native ELF (Single Executable Application). The JS is bundled inside but not extractable as files. Use `strings` to read schema definitions:

```bash
# 1. Find the HOOK_EVENT_TYPES enum
strings /root/.kimi-code/bin/kimi | grep -A20 'HOOK_EVENT_TYPES\$1 ='
# Output (0.36.0):
#   HOOK_EVENT_TYPES$1 = [
#     "PreToolUse", "PostToolUse", "PostToolUseFailure",
#     "PermissionRequest", "PermissionResult",
#     "UserPromptSubmit", "Stop", "StopFailure", "Interrupt",
#     "SessionStart", "SessionEnd",
#     "SubagentStart", "SubagentStop",
#     "PreCompact", "PostCompact", "Notification"

# 2. Find which schemas use .strict()
strings /root/.kimi-code/bin/kimi | grep -B2 -A8 'Schema.*\.strict()'
# HookDefSchema$1 is .strict() — unknown keys/enum values cause hard failure

# 3. Find KimiConfigSchema fields
strings /root/.kimi-code/bin/kimi | grep -A40 'KimiConfigSchema = object'
```

## The transformTomlData Pipeline

Config keys go through a snake_case → camelCase transform before validation:

```
config.toml → TOML parse → transformTomlData() → snakeToCamel keys → KimiConfigSchema.parse()
```

`snakeToCamel` replaces `_x` with `X` (e.g., `max_context_size` → `maxContextSize`). Special transforms exist for `providers`, `models`, `permission`, `services`, `loopControl` sections.

Non-strict zod schemas (most of them) silently strip unknown keys. Only `HookDefSchema` uses `.strict()`.

## Schema Reference (0.36.0)

### KimiConfigSchema (top-level)
- `providers`, `defaultProvider`, `defaultModel`, `models`, `thinking`
- `planMode`, `yolo`, `defaultPermissionMode`, `defaultPlanMode`, `permission`
- `hooks`, `services`, `mergeAllAvailableSkills`, `extraSkillDirs`, `extraAgentDirs`
- `loopControl`, `background`, `subagent`, `secondaryModel`
- `mcp`, `image`, `modelCatalog`, `experimental`, `telemetry`, `raw`

### HookDefSchema (.strict!)
- `event`: must be in `HOOK_EVENT_TYPES` enum
- `matcher`: optional string
- `command`: required string (min 1)
- `timeout`: optional int (1-600)

### ModelAliasBaseSchema
- `provider`, `model` (required strings)
- `maxContextSize`: required int ≥ 1
- `maxInputSize`, `maxOutputSize`: optional int
- `capabilities`: optional string array
- `displayName`, `reasoningKey`, `protocol`, `adaptiveThinking`
- `supportEfforts`, `defaultEffort`, `offEffort`, `betaApi`, `baseUrl`

### ProviderTypeSchema enum
`anthropic`, `openai`, `kimi`, `google-genai`, `openai_responses`, `vertexai`

### PermissionRuleScopeSchema enum
`turn-override`, `session-runtime`, `project`, `user`

## Known Version Breaking Changes

### 0.35 → 0.36 (2026-08-13)
- **Removed hook events:** `TurnStarted`, `UserPromptQueued` — were valid in 0.35, removed from enum in 0.36.
- **Symptom:** Config with `[[hooks]] event = "TurnStarted"` passes doctor (salvaged) but fails login (strict).
- **Fix:** Comment out or delete the `[[hooks]]` blocks using removed events. The hook scripts are fine — only the event registration is rejected.

## Debugging Checklist

1. **Version check:** `kimi --version` — did it auto-update? Check `/root/.kimi-code/updates/rollout.log`.
2. **Hook events:** Compare `grep '^event = ' config.toml` against the `HOOK_EVENT_TYPES` enum from `strings`.
3. **Strict schemas:** Only `HookDefSchema` uses `.strict()`. If hooks are clean, the issue is elsewhere.
4. **Enum values:** Verify all enum-typed fields (`type`, `scope`, `decision`, `event`) match the current schema.
5. **Type mismatches:** `experimental` must be `record(string, boolean())` — any non-boolean value fails.
6. **Doctor diff:** If you have a known-good backup config, `diff` to find what changed.
