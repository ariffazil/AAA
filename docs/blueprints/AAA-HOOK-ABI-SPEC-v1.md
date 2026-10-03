# AAA Hook ABI v1 — Spec (F13-stage, no build)
**Problem:** Codex has 4 hooks, Claude has 0, Kimi/Qwen have unknown. Each harness is drifting.

**Solution:** One canonical AAA Hook ABI, render adapter per harness.

## Canonical schema (AAA Hook Event v1)

```python
@dataclass
class AAAHookEvent:
    event: Literal["SESSION_START", "PRE_ACTION", "POST_ACTION", "SESSION_END"]
    agent_id: str          # e.g. "codex/FI-005", "claude/FI-002"
    session_id: str
    surface: str           # "codex" | "claude-code" | "kimi-code" | "qwen-code"
    tool_name: str | None
    tool_input_digest: str | None  # sha256:...
    authority: str         # e.g. "OBSERVE_ONLY" — from arifOS live
    mutation_allowed: bool
    decision: Literal["ALLOW", "HOLD", "VOID", "SABAR"]
    reason_code: str
    receipt_ref: str | None
    ts: str
```

## Render targets

```
AAA hook ABI
  ↓ render
  ├── Codex `hooks.json` (JSON with shell commands)
  ├── Claude `settings.local.json` permissions
  ├── Kimi `mcp.json` (stdio)
  ├── Qwen settings
  └── OpenCode `opencode.json`
```

## ABI invariants

- `agent_id` = canonical form (e.g. "claude/FI-002", "codex/FI-005")
- `session_id` = ONLY ONE per session (N_init/session = 1) ← Codex P0 fix applied 2026-10-03
- `authority` = ALWAYS read from live arifOS response, NEVER inferred
- `decision` = ALLOW only if `mutation_allowed == true` AND `actor_verified == true`
- `decision` = HOLD if either is false
- `decision` = VOID if not recognized

## Failure modes (must surface, not silent)

- Harness can't connect to arifOS → HOLD, reason_code="ARIFOS_UNREACHABLE"
- Tool name not in arifOS registry → VOID, reason_code="UNKNOWN_TOOL"
- Authority not granted → HOLD, reason_code="INSUFFICIENT_AUTHORITY"

## Migration plan

- v1: each harness keeps its native hook format, add an AAA-mode field
- v2: render hooks from AAA ABI per harness
- v3: drop native hook formats entirely

**Reversibility:** None — this is spec only. Build is F13-stage.
