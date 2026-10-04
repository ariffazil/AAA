# K-02 Transition — Witness to Enforcer (canonical reference)

> **Status:** Reference doc. Companion to `governance-contract-self-audit` SKILL.md.
> **Date:** 2026-08-07
> **Origin:** AAA Federation E-22 audit + Hermes gate wiring.

## Definition

**Before K-02:** Constitution observes reality. A receipt saying `mutation attempted, mutation succeeded` is a witness event — it records what happened without changing it.

**After K-02:** Constitution alters reality. A receipt saying `mutation attempted, mutation blocked, exit 2, tool halted` changes the outcome — the mutation does not happen.

K-02 is the **inflection point** where a constitutional invariant moves from documentation to enforcement.

## Why K-02 matters

| State | What it means | Worth in governance |
|---|---|---|
| Witness only | Receipt records, but violation proceeds | Form-filling |
| Witness + warning | Receipt + textual warning | Advisory only |
| **Enforce (K-02)** | Receipt + exit code blocks tool | **Outcomes change** |

Without K-02:
- 1 doctrine = 1 document
- 1 contract = 1 spec
- 1 receipt trail = 1 audit log

With K-02:
- 1 doctrine = 1 enforcement layer
- 1 contract = 1 hook script
- 1 receipt trail = 1 actual outcome guarantee

## The K-02 pattern (recipe)

Any harness can reach K-02 in 4 steps. Verified live for Hermes 2026-08-07.

### Step 1 — Classify tools (read/write only)

```python
HERMES_TOOLSETS = {
    "read_file": "OBSERVE",         # passthrough, no gate
    "search_files": "OBSERVE",
    "vision_analyze": "OBSERVE",
    "write_file": "MUTATE_T2",      # T2 = needs judgment
    "patch": "MUTATE_T2",
    "terminal": "MUTATE_T2",
    "delegate_task": "MUTATE_T2",  # SPAWN — most important gate
    "skill_manage": "MUTATE_T3",   # T3 = irreversible, always block at gate
    "plugin_install": "MUTATE_T3",
    # Unknown tool → default T2 (fail-closed)
}
```

### Step 2 — Define T3 patterns (catch catastrophic + secret + constitutional)

```python
T3_PATTERNS = [
    r"secrets?[/\\]",
    r"kunci-mas",
    r"vault\.env",
    r"\.signing_key",
    r"tokenrouter",
    r"systemctl\s+(restart|stop|disable)",
    r"VAULT999/outcomes\.jsonl",
    r"chattr\s+-i",                  # vault integrity tamper
    r"rm\s+-rf\s+/root",
    r"dd\s+if=",                     # disk overwrite
    r"mkfs\.",                       # filesystem format
    r"git\s+push\s+.*--force.*\s+(main|master)",
    r"DROP\s+(TABLE|DATABASE)",
]
```

### Step 3 — Wire protocol (Hermes shell hook format)

The hook receives JSON on stdin:
```json
{
  "tool_name": "terminal",
  "tool_input": {"command": "..."},
  "session_id": "..."
}
```

The hook outputs:
- Allow: no output, `sys.exit(0)`
- Block: `print(json.dumps({"decision": "block", "reason": "..."}))` + `sys.exit(2)`

### Step 4 — Wire into harness config

For Hermes:
```yaml
hooks:
  pre_tool_call:
    - matcher: "*"
      command: /root/AAA/federation/protocols/arifos-hermes-gate-hook.py
      accept_hooks: true
```

For OpenCode, add to `plugin` array in `opencode.json`.
For Kimi Code, add `[[hooks]]` entry in `config.toml`.

For OpenClaw, add to `hooks.mappings` array in `openclaw.json`.

For Codex (if hooks supported), add to `~/.codex/config.toml` `[hooks]` section.

## K-02 verification matrix (per harness)

The test: can the harness produce a live `exit 2` + receipt on a real T3 attempt?

| Harness | K-02 wired? | T3 patterns | Test verified? | Receipt path |
|---|---|---|---|---|
| OpenCode | ✅ (judge-gate.ts) | MUTATE + T3 + fail-closed | ✅ | `opencode_receipts.jsonl` (10,173 entries) |
| Kimi | ✅ (aaa-witness-pre.sh exit 2) | catastrophic patterns (no secrets) | ✅ | `mcp-audit.jsonl` |
| Hermes | ✅ (pre_tool_call shell hook) | T3 + secret-path + constitutional | ✅ | `hermes_hook_receipts.jsonl` |
| OpenClaw | ❌ no gate hook | n/a | n/a | n/a |
| Codex | unverified | unverified | ❌ | n/a |

## K-02 invariants (what it must preserve)

1. **No silent violation** — every T3 attempt leaves a receipt (INV-15)
2. **T2 witnessed** — every T2 mutation logged (not necessarily blocked at K-02; deferred to K-03)
3. **OBSERVE passthrough** — no overhead for read-only operations
4. **Receipt failure ≠ governance failure** — never block on receipt write error (E-19)
5. **Fail-closed for T3 + arifOS down** — high-blast-radius patterns blocked even if judge unreachable
6. **T0-T2 + arifOS down = allow with witness** — low-blast-radius continues with audit trail

## K-02 vs K-03 (next stage)

| K-02 (achieved) | K-03 (pending) |
|---|---|
| T3 blocked at gate | T2 routed through arif_judge before execution |
| T2 witnessed only | T2 blocked if no verdict (currently allow-with-witness) |
| Spawn T2 (delegate_task) | Spawn blocked if no envelope (K-04) |
| Receipt on every decision | Receipt with parent_receipt chain (INV-14) |

K-02 closes the **catastrophic** half of the E-22 question. K-03 closes the **judgment-escalation** half. K-04 closes the **spawn-inheritance** half. K-05 retests E-22.

## The single most important sentence

> The witness was forged earlier. K-02 is the first evidence that the constitution has begun to move from witnessing power to constraining power.

This is the inflection. Everything before K-02 is documentation. Everything after K-02 is doctrine.

## Reference receipt (K-02 first enforcement, 2026-08-07 05:54 UTC)

```json
{"event": "hermes-gate.blocked", "tool": "terminal", "classification": "T3", "reason": "T3 pattern detected in 'terminal' args", "timestamp": "2026-08-07T05:54:03.471104Z", "k02_transition": true}
```

That single line is worth more than a hundred doctrinal refinements.