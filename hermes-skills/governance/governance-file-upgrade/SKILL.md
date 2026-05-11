---
name: governance-file-upgrade
description: Execute a coordinated multi-file governance upgrade across an OpenClaw/AAA workspace — adds new governance files, patches existing ones, checks for conflicts, and seals in one atomic operation.
tags: [governance, openclaw, aaa, constitutional]
triggers:
  - "governance upgrade"
  - "add autonomy"
  - "add checkpoint"
  - "AGI-level"
  - "bounded autonomy"
---

# Governance File Upgrade — Coordinated Multi-File Pattern

## When to use
When Arif wants to upgrade OPENCLAW governance architecture with multiple new files (AUTONOMY, CHECKPOINT, LOOP, DECISIONS, TASKS, etc.) that must be:
- Consistent with each other
- Registered in ROOT_CANON.yaml
- Committed atomically
- Described accurately in MEMORY.md

## Pattern used (2026-05-01 — successful)
10-phase upgrade executed in order, committed as one seal.

## Phase sequence

### Phase 1 — Find the actual state first
```bash
# Before writing anything, verify what exists:
ls /root/AAA/*.md  # list all .md files
ls /root/AAA/CLAUDE.md /root/AAA/ARIF.md /root/AAA/GEMINI.md 2>&1  # check for stale models

# Check for conflicting loops in current AGENTS.md:
grep -n "ReAct\|8.step\|loop\|cycle" /root/AAA/AGENTS.md

# Read the section you'll be replacing:
grep -n "Constitutional behavior rules\|step\|loop\|iterate" /root/AAA/AGENTS.md
```

**Key lesson:** The audit characterization is NOT the same as what exists in files. Always verify actual file content before describing what you're replacing.

### Phase 2 — Patch existing files (AGENTS.md, HEARTBEAT.md)
```bash
# AGENTS.md: Add 000-999 governing loop BEFORE the constitutional rules section
# HEARTBEAT.md: Replace static template with live runtime state schema
```

### Phase 3 — Create new files (5 files in parallel is safe)
```bash
# AUTONOMY.md — L0-L5 permission ladder (~130-140 lines)
# CHECKPOINT.md — wake continuity (~75 lines)
# LOOP.md — 000-999 operational implementation (~290 lines)
# DECISIONS.md — sealed decision log format (~40 lines)
# TASKS.md — active work ledger (~55 lines)
```
Write all 5 in parallel using write_file tool. They are independent.

### Phase 4 — Update MEMORY.md
Add a "Sealed Lessons" entry documenting:
- What was wrong
- What was built
- **Exact thresholds from actual files** (NOT from audit characterization)
- Per-model file status

### Phase 5 — Register in ROOT_CANON.yaml
```bash
# In the "constitutional files" section, add:
  - path: AUTONOMY.md
    status: canonical
    role: L0-L5 permission ladder
  - path: CHECKPOINT.md
    status: canonical
  - path: LOOP.md
    status: canonical
  - path: DECISIONS.md
    status: canonical
  - path: TASKS.md
    status: canonical

# In the "legacy" section, mark stale files:
  - path: CLAUDE.md
    status: legacy
    role: stale governance artifact
    notes: Superseded by AGENTS.md + SOUL.md + LOOP.md.
  - path: ARIF.md
    status: legacy
```

### Phase 6 — Mark stale per-model files
```bash
# Verify which exist:
ls /root/AAA/CLAUDE.md /root/AAA/GEMINI.md /root/AAA/ARIF.md 2>&1

# Read first 5 lines of each to confirm content:
head -5 /root/AAA/CLAUDE.md
head -5 /root/AAA/ARIF.md
```

### Phase 7 — git add all changed files
```bash
cd /root/AAA
git add AGENTS.md AUTONOMY.md CHECKPOINT.md LOOP.md DECISIONS.md TASKS.md \
       HEARTBEAT.md MEMORY.md TOOLS.md ROOT_CANON.yaml
git diff --cached --stat
```

### Phase 8 — Commit with descriptive message
```bash
git commit -m "feat: AGI-level governance upgrade — 000-999 loop, AUTONOMY L0-L5, live HEARTBEAT, CHECKPOINT, LOOP, DECISIONS, TASKS"
```

### Phase 9 — Push
```bash
git push
```

## Common mistakes to avoid

### Mistake 1: Trusting the audit description over actual files
**Problem:** Audit says "plain 8-step ReAct loop" exists in AGENTS.md — but grep shows it doesn't.
**Fix:** Always `grep` actual files first.

### Mistake 2: Wrong threshold numbers
**Problem:** Audit says `loop_count > 20` but actual HEARTBEAT.md says `> 10`.
**Fix:** Cite actual file content, not audit characterization.

### Mistake 3: Assuming all per-model files exist
**Problem:** GEMINI.md doesn't exist — but ARIF.md does.
**Fix:** `ls` all candidate files before making claims.

### Mistake 4: Forgetting to register new files in ROOT_CANON.yaml
**Problem:** New files created but not tracked in canonical registry.
**Fix:** Always update ROOT_CANON.yaml in the same commit.

### Mistake 5: Docker rebuild breaks running container
**Problem:** Old container had implicit dev fallbacks; rebuild removes them; container won't start.
**Fix:** Before rebuild, `docker inspect` old container's env vars. Add dev fallbacks to source code before building.

## Critical thresholds (from verified files)
- `loop_count > 10` → stop and report (NOT 20)
- `entropy_delta > +0.3` → investigate before continuing (NOT 0.7)
- risk_level HIGH/CRITICAL → pause for 888 approval
- Default autonomy level: L3
- L4/L5 require explicit 888 authorization

## Sealed Lessons format (for MEMORY.md)
```
## Sealed Lessons

### YYYY-MM-DD — [Brief Title]

**What was wrong:** [specific gap, not audit characterization]

**What was built:** [bullet list of files and what each does]

**Thresholds (from actual files):** [exact numbers with "NOT X" corrections]

**Per-model files:** [which exist, which don't, which are stale]

**Authority:** Arif (888 Judge). **DITEMPA BUKAN DIBERI.**
```

## Output
After seal, report:
- Files changed + lines
- Files created
- Risks reduced (before/after)
- Remaining risks
- Current autonomy level
- Next safe actions
- Whether 888 approval required
