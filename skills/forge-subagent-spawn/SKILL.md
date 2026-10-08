---
id: subagent-spawn-template
name: FORGE-subagent-spawn
version: 1.0.0
description: "Standard contract for spawning bounded, auditable sub-agents — input contract, output schema, evidence requirements."
owner: AAA
risk_tier: medium
floor_scope: [F1, F2, F11]
autonomy_tier: T1
tags: [subagent, spawn, contract, template]
capability_tier: fed-agent-subagent
ecology_state: WARM
owned_by: AAA
authority_of: AAA
---

# Sub-Agent Spawn Template — OpenClaw

## Purpose
Standard contract for spawning bounded, auditable sub-agents. Every sub-agent gets the same input contract, output schema, and evidence requirements. Replaces ad-hoc "do this thing" spawning.

## Input Contract (Required)

Every sub-agent spawn call MUST include:

```yaml
task_name: "stable-lowercase-identifier"   # e.g. "audit-wealth-endpoints"
task_description: |
  Clear, bounded description of what to do.
  Include: scope, constraints, what NOT to touch.
output_schema:
  type: object
  required: ["status", "findings", "evidence"]
  properties:
    status: {type: string, enum: ["DONE", "BLOCKED", "ERROR"]}
    findings: {type: array, items: {type: object}}
    evidence: {type: array, items: {type: string}}
    recommendation: {type: string}
time_budget_minutes: 15
evidence_required: true          # Attach URLs, tool outputs, file paths
autonomy_band: "PROPOSE_ONLY"    # AUTONOMOUS | PROPOSE_ONLY | NEVER (must match E7)
tools_scope:                     # Explicit tool allowlist
  - "exec"
  - "read"
  - "web_fetch"
rollback_plan: "rm output_file"  # How to reverse ALL changes
```

## Behavior Rules

### 1. Time Budget Enforcement
- Sub-agent MUST return within `time_budget_minutes`.
- If blocked, return `BLOCKED` with reason before timeout.
- Never spawn a sub-agent without a time budget.

### 2. Output Schema Compliance
- Every sub-agent response MUST match the declared `output_schema`.
- If schema can't be met, return `ERROR` with reason.
- Structured JSON only. No prose-only responses.

### 3. Evidence Attachment
- If `evidence_required: true`: every finding MUST be backed by at least one evidence item (URL, file path, tool output snippet).
- Evidence items must be verifiable — live URLs, absolute file paths, or inline tool output.

### 4. Autonomy Band
- `AUTONOMOUS`: Safe read-only tasks (health checks, file reads, research).
- `PROPOSE_ONLY`: Changes proposed but NEVER auto-executed. Returns plan for 888 review.
- `NEVER`: Must fail closed. Any execution attempt = ERROR.

### 5. Rollback
- Every sub-agent spawn MUST include a `rollback_plan`.
- Rollback must be a single shell command or file operation.
- "No changes made" is a valid rollback plan if read-only.

## Example: Spawning a Code Auditor

```
task_name: "audit-arifos-drift"
task_description: |
  Read /root/arifOS/arifosmcp/runtime/tools.py and 
  /opt/arifos/app/arifosmcp/runtime/tools.py.
  Compare them. Report all differences.
  Do NOT modify any files. Read-only.
output_schema:
  type: object
  required: ["status", "findings", "evidence"]
  properties:
    status: {type: string}
    findings: {type: array}
    evidence: {type: array}
time_budget_minutes: 10
evidence_required: true
autonomy_band: "AUTONOMOUS"
tools_scope: ["read", "exec"]
rollback_plan: "No changes — read-only"
```

## Example Output

```json
{
  "status": "DONE",
  "findings": [
    {
      "severity": "IMPORTANT",
      "description": "tools.py differs at line 147: arif_observe has mode=vitals logic in /root/ but not in /opt/",
      "file_1": "/root/arifOS/arifosmcp/runtime/tools.py",
      "file_2": "/opt/arifos/app/arifosmcp/runtime/tools.py"
    }
  ],
  "evidence": [
    "diff -u /root/arifOS/arifosmcp/runtime/tools.py /opt/arifos/app/arifosmcp/runtime/tools.py"
  ],
  "recommendation": "rsync /root/arifOS/arifosmcp/ → /opt/arifos/app/arifosmcp/ then restart arifos. Mark 888_HOLD."
}
```

## Integration with OpenClaw

OpenClaw spawns sub-agents via `sessions_spawn`. The template fields map:

| Template Field | sessions_spawn Param |
|---------------|---------------------|
| `task_description` | `task` (string) |
| `time_budget_minutes` | Included in `task` string + manual timeout |
| `tools_scope` | Native sub-agents inherit parent tools |
| `output_schema` | Included in `task` string as "Return ONLY valid JSON matching schema: ..." |
| `autonomy_band` | Enforced by E7 in arifOS kernel |

## Pitfalls

- **Treat silent zero-result as a failure, not a quiet success.** When `delegate_task` returns no
  transcript, no commit, no output file by `time_budget_minutes`, the sub-agent died silently — not
  finished cleanly. Recover with an in-context branch+commit probe (`git log <branch> --oneline`,
  `git diff main..<branch> --stat`); if the work landed, claim it; if empty, take over directly.
  "Nothing returned" ≠ "all good" — verify the filesystem, not the runtime's exit.

- **Multi-imperative ask = parallel, not sequential.** When a user message contains two or more
  imperatives ("Spawn Y, then exercise Z" / "do A and show me C"), do NOT invent a confirmation gate
  between them. Both are part of the same ask — execute them in the same turn. Treating them as a
  pipeline (do A, then ask "OK now?", then do B) burns user attention and signals a comprehension
  failure.

- **Partial names + confident date slots fabricate, not remember.** When the user names a person by
  partial identifier (surname only, surname + role, no organisation) and the turn requires a tenure
  or date claim, do not populate the slot from parametric memory. Probe-first via `zai_search`
  before rendering any number. If the probe returns zero hits, label the candidate `UNVERIFIED` and
  ask the user for the full identifier — do not paper over with a plausible-looking date.

## Recovery Checklist (silent-drop)

1. `delegate_task` returns empty / no transcript / not in active children list.
3. Do not retry the same sub-agent spawn — same inputs, same defect.
4. `git log <branch> --oneline` — does the work exist on the named branch?
5. `git diff main..<branch> --stat` — has anything actually changed?
6. `git status --short` in the target workdir — any uncommitted work?
7. If yes on any of 4-6: claim the landed work and report "subagent surfaced via prior commit".
8. If no on all of 4-6: take over in-context. Read the wiring points the sub-agent would have
   read, write the patch yourself, commit Arif-author.
9. Report what the runtime says ("subagent silent-drop recovered via in-context") — not "all good".

## F2 Note
This template does not enforce constraints programmatically — it's a contract for human + agent behavior. The arifOS kernel enforces autonomy bands via E7. OpenClaw enforces via constitutional discipline.
