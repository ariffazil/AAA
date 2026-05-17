---
title: "POST-TASK UPDATE PROMPT CONTRACT"
created: 2026-05-17
updated: 2026-05-17
version: 1.0.0
type: governance
tags: [prompt, contract, post-task, TREE777, trace, evidence]
category: governance
risk_band: LOW
floors: [F2, F4, F6, F7]
evidence_required: false
sources: [wiki/concepts/TREE777.md, wiki/skills/skill-trace-capture.md]
confidence: high
status: canonical
---

# POST-TASK UPDATE PROMPT CONTRACT

> **Contract ID:** `post-task-update-v1`
> **Canonical location:** `AAA/wiki/post-task-update-prompt-contract.md`
> **Status:** CANONICAL — this is a governance contract, not a draft
> **Purpose:** Bind agents to TREE777 trace-capture protocol after every non-trivial task
> **Applies to:** Claude Code, OpenCode, Hermes, Gemini CLI, OpenClaw, Kimi Code, Codex, Copilot

---

## Summary

After completing ANY non-trivial task, the agent MUST execute the trace-capture protocol before ending the session or starting new work.

This contract is **prepended to the agent's system prompt**. It does not require the agent to read any file — the protocol is self-contained in this contract.

---

## THE CONTRACT (Paste into System Prompt)

```
═══════════════════════════════════════════════════════════════
TREE777 POST-TASK PROTOCOL — MANDATORY
═══════════════════════════════════════════════════════════════

You are bound by the TREE777 promotion ladder.

AFTER EVERY NON-TRIVIAL TASK, before ending session or starting new work:

1. COMPOSE TRACE (write to wiki/log.md or session log):
   TRACE: [YYYY-MM-DD HH:MM] | AGENT: {your-name} | TASK: {one-line task}
   ---
   Step 1: [what was attempted]
   Step 2: [what happened]
   Step 3: [outcome]
   ---
   Confidence: [LOW / MEDIUM / HIGH]
   Risk: [LOW / MEDIUM / HIGH / 888_HOLD]
   Proposed delta: [what should change in TREE777, or "none"]

2. COLLECT EVIDENCE (for each significant action):
   - Command or API call made
   - Raw output (verbatim, not summarized)
   - Verification result
   Store in: wiki/raw/notes/{YYYY-MM-DD}_{agent}_{task-slug}.md

3. IF FAILURE OCCURRED:
   - Write ADMISSION immediately: "ADMISSION: [what went wrong]"
   - Create scar draft: wiki/scars/scar-{name}-{YYYY-MM-DD}.md
   - Status: proposed
   - Cite evidence from step 2
   - Never deflect blame to "the system"

4. IF PATTERN REPEATS 2-3×:
   - Create skill promotion proposal: wiki/skills/skill-{name}.md
   - Status: proposed
   - Cite 2+ evidence bundles
   - Submit for 888 deliberation

5. APPEND TO wiki/log.md:
   ## [YYYY-MM-DD HH:MM] trace | {agent} | {task summary} | {outcome}
   - Confidence: {tag}
   - Risk: {tag}
   - Evidence: {path or "none"}
   - Proposed delta: {description or "none"}

═══════════════════════════════════════════════════════════════
NON-TRIVIAL TASK DEFINITION:
- Took more than 5 tool calls
- Agent made a decision (not just followed script)
- Produced non-trivial output (file creation, config change, API call)
- Agent was uncertain and made judgment call
- ANY failure or error occurred
- Session end
═══════════════════════════════════════════════════════════════

FLOOR REMINDERS:
- F2 (TRUTH): Capture raw outputs, not interpretations
- F6 (MARUAH): Own every failure honestly — no deflection
- F7 (HUMILITY): If uncertain, say so — do not fabricate confidence
- F4 (CLARITY): The trace must be understandable by future agents
═══════════════════════════════════════════════════════════════

DITEMPA BUKAN DIBERI — Capture first. Prove later. Always.
═══════════════════════════════════════════════════════════════
```

---

## How to Deploy This Contract

### Claude Code
Add to `~/.claude/system.md` or the session-specific system prompt:

```
[Paste the contract above]
```

### OpenCode
Add to `/root/.opencode/system-prompt.md` or agent config:

```
[Paste the contract above]
```

### Hermes
Add to `~/.hermes/system.md`:

```
[Paste the contract above]
```

### Gemini CLI
Add to `~/.gemini/system.md`:

```
[Paste the contract above]
```

### OpenClaw
Add to `~/.openclaw/system.md`:

```
[Paste the contract above]
```

### Kimi Code
Add to `~/.kimi/system.md`:

```
[Paste the contract above]
```

### Codex
Add to `~/.codex/system.md` or project CLAUDE.md:

```
[Paste the contract above]
```

### Copilot
Add to `~/.copilot/system.md` or repository CLAUDE.md:

```
[Paste the contract above]
```

---

## Agent-Specific Notes

| Agent | Config Location | Notes |
|-------|---------------|-------|
| Claude Code | `~/.claude/system.md` | Per-user config; also respects repo-level CLAUDE.md |
| OpenCode | `/root/.opencode/system-prompt.md` | Global agent config |
| Hermes | `~/.hermes/system.md` | Hermes fabricates — ensure contract is LOADED, not just present |
| Gemini CLI | `~/.gemini/system.md` | Verify with `cat ~/.gemini/system.md` after edit |
| OpenClaw | `~/.openclaw/system.md` | Verify with `cat ~/.openclaw/system.md` after edit |
| Kimi Code | `~/.kimi/system.md` | Verify after edit |
| Codex | `~/.codex/system.md` or repo CLAUDE.md | Repo CLAUDE.md overrides user config |
| Copilot | `~/.copilot/system.md` or repo CLAUDE.md | Same override pattern as Codex |

---

## Verification Procedure

After adding the contract to an agent's config:

1. **Verify the contract loaded:**
   ```bash
   # For the agent you're testing
   cat ~/{agent-config-dir}/system.md | grep -c "TREE777 POST-TASK"
   # Expected: 1 (contract is present and not duplicated)
   ```

2. **Verify the agent can write to wiki/log.md:**
   ```bash
   # Test write access
   echo "## [TEST] post-task-contract | test | verification check | OK" >> wiki/log.md
   # If permission denied, fix permissions
   ```

3. **Verify the agent can create files in wiki/raw/notes/:**
   ```bash
   # Test write access
   echo "# Test" > wiki/raw/notes/test-{agent}.md
   # If permission denied, fix permissions
   ```

---

## Contract Versioning

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-05-17 | Initial canonical version |

**Upgrade path:** When this contract is updated:
1. New version gets a new file: `post-task-update-prompt-contract-v{N}.md`
2. All agent configs should be updated to point to the new version
3. Log the upgrade in `wiki/log.md`

---

## Relationship to TREE777

This contract is the **enforcement mechanism** for TREE777's trace-capture requirement:

```
POST-TASK CONTRACT (this document)
    ↓ binds agent behavior
skill-trace-capture (wiki/skills/skill-trace-capture.md)
    ↓ emits evidence bundle
skill-scar-distill (wiki/skills/skill-scar-distill.md)
    ↓ on failure
skill-skill-promote (wiki/skills/skill-skill-promote.md)
    ↓ on 2-3x repetition
→ 888 JUDGE promotion
```

The contract makes trace-capture **mandatory**, not optional.

---

## Related Pages

- [[TREE777]] — governance framework
- [[skill-trace-capture]] — the skill this contract implements
- [[skill-scar-distill]] — failure handling
- [[skill-skill-promote]] — pattern promotion
- [[tree-manifest.json]] — page registry tracking this contract's deployment status

---

*DITEMPA BUKAN DIBERI — The contract is law. Follow it. Every time. No exceptions.*
