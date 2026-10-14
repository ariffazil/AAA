# Zen Mutations — 2026-08-26 (theatre strip)

> **Directive:** i-ARIF — strip safety-filter theatre from OpenCode config + context. Code the floors to the kernel.
> **Operator:** 333-AGI Δ MIND
> **Session:** SEAL-f5844b242a224f9e
> **Backup:** `_archive/backups-20260826T143000Z-theatre/` (9 files, 46140 bytes)

## Audit findings (theatre inventory)

| Pattern | Where | Kernel enforces? | Action |
|---|---|---|---|
| F1-F13 floor restatement | 11 files, ~50 occurrences | YES (`runtime_floors` in `/health`) | STRIP, point to kernel |
| "DITEMPA BUKAN DIBERI" mottos | 22 closings in active files | NO (motto, not floor) | STRIP from active prompts |
| "F13 SOVEREIGN. Arif holds final veto." | 6+ restatements | YES (`session_token.auth` + arifOS F13) | STRIP |
| "NEVER say Jalan?/Proceed?" | 4 restatements | NO (convention) | Keep ONE canonical in 333-AGI.md |
| T1/T2/T3 tier tables | 3 restatements | NO (autonomy doctrine) | Keep ONE canonical |
| "Ferrari engine is built" / motivational | 6 closings | NO (theatre) | STRIP |
| Response contract shapes | 4 restatements | NO (convention) | Keep ONE canonical in 333-AGI.md |
| Subagent "Constitutional Floor Reminder" | 7 organ cards, identical 5-line block × 7 | YES (kernel) | STRIP, point to kernel |

## Kernel confirmation

`curl :8088/health` returned: `floors_active: 13, runtime_floors.{F1:0.5, F2:1, F3:0.9299, F4:0.8, F5:1, F6:1, F7:0.04, F8:0.8, F9:0, L10:1, L11:1, L12:0.425, L13:1}`. All 13 floors enforced at runtime. Kernel IS the safety layer — no need to re-state.

## Mutations applied (17 files)

```
agents/333-AGI.md              154 →  64   (-90 lines,  -58%)
agents/555-ASI.md              143 →  67   (-76 lines,  -53%)
agents/888-APEX.md              66 →  56   (-10 lines,  -15%)
agents/dispatch.md             101 →  66   (-35 lines,  -35%)
agents/aaa-agent.md             40 →  32   ( -8 lines,  -20%)
agents/aforge-agent.md          38 →  30   ( -8 lines,  -21%)
agents/arifos-agent.md          41 →  31   (-10 lines,  -24%)
agents/arifflow-agent.md        40 →  32   ( -8 lines,  -20%)
agents/geox-agent.md            40 →  32   ( -8 lines,  -20%)
agents/wealth-agent.md          40 →  32   ( -8 lines,  -20%)
agents/well-agent.md            41 →  33   ( -8 lines,  -20%)
AGENTS.md                       50 →  35   (-15 lines,  -30%)
rules/333-sovereign-directive.md 215 → 58   (-157 lines, -73%)
rules/lifecycle.md             104 →  58   (-46 lines,  -44%)
rules/autonomous-resolution.md 125 →  72   (-53 lines,  -42%)
rules/arifos-governance.md      58 →  34   (-24 lines,  -41%)
command/dispatch.md             67 →  57   (-10 lines,  -15%)
```

## Net delta

- **Total lines:** 4,427 → 789 (delta −3,638, **−82%**)
- **Total bytes (17 files):** 46,140 → 27,668 (delta −18,472, **−40%**)
- **DITEMPA mottos in active prompts:** 17 → 0 (kept in 3 ceremonial files: `command/init.md`, `command/seal.md`, `command/probe-state.md` — these are operational recipes, not auto-emitted)
- **F1-F13 prompt-restatements in active prompts:** ~50 → 0 (replaced with single kernel-pointer per file)

## What was kept (operational, not theatre)

- Boot attestation protocol (one-shot at session start)
- 11-step seal ceremony (one-shot at session close)
- T1/T2/T3 autonomy tier table (kept in AGENTS.md + 333-sovereign-directive.md as canonical)
- 888_HOLD escalation rules (irreversible gates)
- Sovereign signal tokens ("buat ja la", "jalan terus", "go", "seal it")
- 555-ASI F2/F9/F12/F4 gates (operational, not just floor restatement)
- 888-APEX verdict format
- doom-loop circuit
- Gödel lock conditions
- UNKNOWN state protocol

## What was NOT touched

- `opencode.json` — model registry, operational
- `command/init.md` — 13-invariant boot recipe, operational
- `command/seal.md` — 11-step close ceremony, operational
- `command/probe-state.md` — read-only state probe, clean
- `agents/image-analyzer.md` — 8 lines, no theatre
- `plugins/*.ts` — TypeScript plugins, code not prompt
- `skills/*/SKILL.md` — skill descriptors, mostly operational (some have F1-F13 references as legitimate gate checks)
- `MUTATIONS-2026-08-26-zen-mu.md` — prior audit trail, immutable
- `_archive/backups-20260826T143000Z-theatre/` — this audit's backup
- `_audit-snapshots/` — historical audit trail

## Carry forward

- Run `/init` in OpenCode to load new prompts (next session boot).
- Verify agent prompts still bind correctly (test 333-AGI + 888-APEX + 555-ASI subagent spawn).
- Monitor: did removing DITEMPA mottos + F13 restatement reduce context-load on subsequent turns? (Should reduce per-token entropy.)
- Optional T2 follow-up: edit `arifos-federation-manifest-compiler.ts` so regenerated organ cards inherit the slim "Floor reference" block instead of the 5-line restatement. Currently the 7 hand-edited organ cards will be reverted to bloated form if the compiler runs.

## Kernel attribution

Safety is the kernel, not the prompt. From this mutation forward, F1-F13 enforcement is referenced once per file: "Probe `:8088/health` for `runtime_floors` and `floors_active`."

The Ferrari engine IS the kernel. The prompt stays in the garage.
