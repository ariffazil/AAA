# Runtime Hook Wire-Up Recipes — Federation Enforcement

> Compiled 2026-08-07. Source: Hermes MISSION-GATION (Phase 1+2) + Kimi K-02 verification.

These are the exact wire-up patterns needed to move from "policy doc exists" to "runtime blocks the action." Each harness has its own hook protocol; this is the cheat sheet.

## Hermes — `pre_tool_call` Hook Protocol

Hermes runtime hooks fire from `model_tools.py` before tool execution. The script receives JSON via stdin and returns JSON via stdout. Source: `/usr/local/lib/hermes-agent/agent/shell_hooks.py`.

### Wire format

**stdin (JSON):**
```json
{
  "hook_event_name": "pre_tool_call",
  "tool_name": "terminal",
  "tool_input": {"command": "rm -rf /tmp/junk"},
  "session_id": "sess_abc123",
  "cwd": "/root",
  "extra": {
    "task_id": "...",
    "tool_call_id": "...",
    "turn_id": "...",
    "api_request_id": "..."
  }
}
```

**stdout (JSON) — three accepted shapes:**
```json
{"decision": "block", "reason": "Forbidden command"}      // Claude-Code-style
{"action": "block", "message": "Forbidden command"}        // Hermes-canonical
{"decision": "approve"}                                     // allow
```

### Wiring location

`/root/.hermes/config.yaml` (or profile-level):
```yaml
hooks:
  - event: pre_tool_call
    command: /usr/bin/python3 /root/HERMES/gate/mutation_gate_hook.py
    timeout: 5
```

Or in profile config at `/root/.hermes/profiles/<name>/config.yaml`.

### Reference implementation

`/root/HERMES/gate/hermes_mutation_gate.py` (gate logic, pure function `evaluate()`).
`/root/HERMES/gate/mutation_gate_hook.py` (hook entry, stdin/stdout JSON wrapper).
`/root/HERMES/gate/receipts/hermes_actions.jsonl` (receipt trail, append-only).

### Verification (subprocess pipe)

```bash
echo '{"hook_event_name":"pre_tool_call","tool_name":"terminal","tool_input":{"command":"rm -rf /tmp/junk"},"session_id":"test"}' \
  | python3 /root/HERMES/gate/mutation_gate_hook.py
# Expect: {"decision": "block", "reason": "..."}
```

Exit code 0 regardless (hermes shell_hooks reads decision from JSON, not from process exit).

### Critical pitfalls

- **First-use consent**: shell_hooks prompts user on first registration. Non-TTY callers (cron, scripts) must pass `--accept-hooks` or set `HERMES_ACCEPT_HOOKS=1`.
- **No mutation in hook**: shell_hooks runs the hook synchronously. If the hook hangs, the entire runtime hangs. Keep timeout ≤ 5s.
- **fallback safety**: shell_hooks treats non-200 exit as `approve`. If hook crashes, default is approve, not block. For T3 patterns, the gate returns `block` in JSON, which IS the blocking signal — process exit code is irrelevant.
- **Process isolation**: each `pre_tool_call` spawns a fresh subprocess. State cannot persist between calls. The gate MUST be stateless on each invocation.

## Kimi — `exit 2` Enforcement Pattern

Kimi's `aaa-witness-pre.sh` hook (at `/root/.arifos/agents/kimi/hooks/`) is the one working example of fail-closed enforcement in the federation.

### Mechanism

The hook outputs `permissionDecision: "deny"` in JSON. At the very end of the script:

```bash
if [[ "$PERMISSION" == "deny" ]]; then
    exit 2  # SIGINT-like non-zero; harness must stop the tool call
fi
exit 0
```

When exit code = 2, Kimi runtime treats it as a hard block. When exit code = 0, proceed.

### Live-fire test (2026-08-07 verified)

| Pattern | Hook decision | Exit code | Result |
|---|---|---|---|
| `rm -rf /tmp/junk-test` | deny | 2 | ✅ BLOCKED |
| `cat /root/.secrets/kunci-mas.env` | allow | 0 | ❌ NOT BLOCKED (gap!) |
| Force-push git | deny | 2 | ✅ BLOCKED |
| `DROP TABLE` | deny | 2 | ✅ BLOCKED |
| `chmod 777 /etc/passwd` | deny | 2 | ✅ BLOCKED |
| Read `/root/AGENTS.md` | allow | 0 | ✅ Allowed |

### Critical gap (the K-02 PARTIAL verdict)

**Secrets paths are NOT in Kimi's BLOCK_REASON table.** The hook blocks catastrophic destructive actions but does NOT block secret disclosure. Adding to BLOCK_REASON requires editing `aaa-witness-pre.sh` directly (T2 territory).

To close the gap, add patterns like:
```bash
elif [[ "$TOOL_INPUT" == *"kunci-mas"* ]] || [[ "$TOOL_INPUT" == *".secrets/"* ]] || [[ "$TOOL_INPUT" == *"signing_key"* ]]; then
    BLOCK_REASON="BLOCKED: secrets material access — F1 AMANAH violation"
```

### Wiring location

`/root/.kimi-code/config.toml`:
```toml
[[hooks]]
event = "PreToolUse"
matcher = "Bash|Shell|Write|WriteFile|Edit|StrReplace|StrReplaceFile"
command = "/root/.arifos/agents/kimi/hooks/aaa-witness-pre.sh"
```

Already wired in current config. Working since 2026-08-07 K-02 patch.

## OpenCode — `judge-gate.ts` Plugin

Already wired in `/root/.config/opencode/opencode.json` plugins block:
```json
"./plugins/arifos-judge-gate.ts"
```

MUTATE_PATTERNS include `task`, `delegate_task`, `cronjob`, `plugin` (Kimi E-22 patch). However: `gated_total=0, blocked_total=0` across all observed sessions — gate is armed but never fired live. WIRED-UNTRIGGERED.

To prove live-fire:
1. Trigger any `task` tool call from 333-AGI in a test session
2. Verify gate fires, returns BLOCK, tool halts
3. Receipt appended to `/root/.local/share/arifos/opencode_receipts.jsonl`
4. Audit confirms the block

## Cross-Harness Gate Truth Table (the E-22 answer per harness)

| Harness | T3 pattern | T2/T3 mutation | Spawn risk | Tool strip | Verdict |
|---|---|---|---|---|---|
| Hermes | ✅ BLOCK (subprocess pipe) | ✅ REQUIRE_JUDGE (subprocess pipe) | ✅ REQUIRE_JUDGE | n/a | **Gate works in subprocess**; not wired to runtime |
| OpenCode | ✅ ARMED | ✅ ARMED | ✅ ARMED | n/a | **Armed but never fired live**; WIRED-UNTRIGGERED |
| Kimi | ✅ BLOCK (exit 2) | ⚠️ PARTIAL (exit 2 for some patterns) | ❌ NOT BLOCKED | ❌ NOT STRIPPED | **Enforces rm-rf/drop/force-push**; misses secrets + spawn |

## The Migration Sequence (governance moves forward by closing one gap at a time)

The E-22 audit answer ("can runtime violate without receipt?") resolves in this order:

1. **Hermes K-02**: subprocess pipe proves gate works → wire to runtime → trigger live mutation → confirm receipt appended → confirm tool actually blocked
2. **OpenCode live-fire**: trigger real `task` tool call from 333-AGI → confirm `judge-gate.ts` returns BLOCK → confirm `opencode_receipts.jsonl` updated
3. **Kimi secrets gap**: extend `BLOCK_REASON` table with secrets patterns → confirm cat-kunci-mas exit 2

Each step is T2 territory (reversible). Each step produces a verifiable receipt. The receipt chain is what closes E-22, not the audit.

## Pitfalls

- **Don't claim WIRED before live-fire test.** Hermes gate works in subprocess pipe but is not wired to runtime. OpenCode gate exists in source but has never fired. WIRED-UNTRIGGERED is the honest status until something actually blocks.
- **Don't extend gate patterns without testing the new patterns live.** A new BLOCK_REASON entry that doesn't fire is the same as no entry.
- **Don't conflate witness exit code with block exit code.** Kimi hook script exits 0 normally. The block is `permissionDecision: deny` in JSON, plus `exit 2` at the very end. The double signal is for redundancy.
- **Don't assume `extras:` keys are stable.** Hermes shell_hooks passes event-specific kwargs under `extra`. If a new key is added in a Hermes upgrade, hook scripts that destructure it will break. Wrap in try/except.