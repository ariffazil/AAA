# Governance Surface Verification — 2026-08-09

## Session context

OpenCode session spawned with /init prompt. Agent claimed "Complete Governance Surface" deployed. Independent audit found:

1. Files at `~/.config/opencode/` not `~/.opencode/` (XDG config path)
2. `command/` (singular) not `commands/` (plural)
3. Pre-commit hooks were from 2026-08-06, not new
4. failure_ledger.jsonl was empty despite "5 wisdom scars recorded"
5. 888-APEX fallback chain had no config evidence

## What was actually deployed

```
~/.config/opencode/
├── rules/
│   ├── autonomous-resolution.md     v2.0 (F13 ratified, HITL split correct)
│   ├── arifos-governance.md          model chains, fallback discipline
│   ├── 333-sovereign-directive.md    autonomous execution contract
│   └── lifecycle.md                  /init → plan → build → verify → 888 gate → /seal
├── agents/
│   ├── 333-AGI.md    (steps=40, doom_loop=ask, *:allow)
│   ├── 555-ASI.md    (steps=30, task:deny)
│   ├── 888-APEX.md   (steps=5, task:deny)
│   ├── dispatch.md
│   ├── image-analyzer.md
│   └── 7 organ agents (aaa, aforge, arifflow, arifos, geox, wealth, well)
├── command/
│   ├── init.md
│   ├── seal.md
│   └── dispatch.md
├── opencode.json       (62KB, comprehensive)
└── flags/
    └── failure_ledger.jsonl → /root/HERMES/flags/failure_ledger.jsonl (symlink)
```

## autonomous-resolution.md v2.0 — the correction

v1.0 (VOID): "Direct human prompting is STRICTLY FORBIDDEN"
v2.0 (RATIFIED): "COGNITIVE escalation FORBIDDEN. AUTHORIZATION escalation REQUIRED."

| Class | Action | Examples |
|---|---|---|
| COGNITIVE HITL | FORBIDDEN — resolve internally | "should I proceed?", "which approach?" |
| AUTHORIZATION HITL | REQUIRED — escalate to F13 | money, irreversible, secrets, constitutional |
| UNKNOWN + T3 | 888_HOLD → ESCALATE | unverifiable state with irreversible blast radius |

Resolution ladder: re-probe → alt tool → subagent (555-ASI) → fallback model → scar + UNKNOWN

## failure_ledger.jsonl — real content

After remediation, the file contained 3 real scars:
1. INIT_SCHEMA — ledger initialized
2. TRANSIENT_TOOL_FAILURE — arif_init MCP transport failed, retried, resolved
3. ARCHITECTURE_CORRECTION — ledger path corrected to canonical location

The agent hit a real failure, resolved it, and logged the scar. Protocol working.

## Audit methodology

1. Find actual config path (`find /root -name 'opencode.json'`)
2. Verify directory structure (rules/, agents/, command/)
3. Check agent configs in opencode.json (steps, permissions, doom_loop)
4. Verify HITL split in autonomous-resolution.md
5. Check failure_ledger exists and has real content
6. Verify symlink from opencode flags to canonical location
7. Check git commit exists and matches claimed work
8. Verify VAULT999 receipt for the commit

## Overlapping skills

- `forge-federation-probe` — federation organ probing (health, authority, drift)
- `verify-nested-sibling-reports` — sibling self-report verification (this skill)
- `audit-and-validate-deliverables` — generic artifact audit
- `verify-before-report` — post-action verification

The governance surface verification pattern fits under `verify-nested-sibling-reports` because it's about verifying sibling agent claims against live state on disk.
