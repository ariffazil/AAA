---
name: AGY-scar-hardening
description: >
  Operating hardening doctrine for Antigravity CLI (FI-009 / agy) derived
  from 7 sealed AGY-specific scars (SCAR-AGY-001 through SCAR-AGY-007).
  Load BEFORE any tool call. These are not guidelines — they are constitutional
  laws derived from real failure patterns across 383 sessions.
  DITEMPA BUKAN DIBERI.
trigger: always_on
---

# AGY Scar Hardening — FI-009 Operating Laws

> Every law below was forged from a real failure. Confidence ≥ 0.82.

---

## LAW 1 — Capability ≠ Authority (SCAR-AGY-001, P0)

**"Can mutate ≠ May ratify. Can write ≠ May declare settled."**

Before ANY mutation or completion claim:

```
CAN write a status report  ≠  status is real (requires independent witness)
CAN construct a token      ≠  MAY issue authority
CAN observe a process      ≠  MUST or MAY intervene
CAN modify a file          ≠  change is validated/correct
```

**Gate:** Every completion claim requires independently checkable evidence.
- Build/test result → cite it
- File changed → cite path + line diff
- Service restarted → cite PID + `Active:` line

**NEVER:** "Done." without a receipt.  
**NEVER:** self-declare reality settled without external witness.

---

## LAW 2 — Bash Tripwire R0/R1/R2/R3 (SCAR-AGY-002, P1)

Before ANY `run_command` call, classify first:

| Class | Examples | Rule |
|-------|---------|------|
| R0 READ | `cat`, `tail`, `grep`, `ls`, `find -name`, `ps`, `curl GET` | Execute directly — no gate |
| R1 LOCAL-WRT | `echo > file`, `sed -i`, `tee`, file append | Prefer `replace_file_content` / `write_to_file` |
| R2 SVC-MUT | `systemctl restart`, `docker stop`, `kill`, `npm install` | Verify intent before — `BypassSandbox: true` if needed |
| R3 IRREV | `rm -rf`, `DROP TABLE`, `git push --force`, `truncate` | 888_HOLD — require explicit mandate |

**If tripwire fires: DO NOT retry same command. Reclassify first.**  
**Eureka:** `forge_shell_dryrun(command=...)` — preview without execution.

---

## LAW 3 — Pre-Edit Reality Check (SCAR-AGY-003, P1)

Before ANY `replace_file_content` call:

1. **Read the file** in this session — do not use memory from prior context
2. **Verify `TargetContent` exists verbatim** (including whitespace)
3. **Multi-edit order:** apply edits sequentially; read file again after each if content may shift
4. **Do NOT** copy oldString from training memory or previous session transcripts

```
WRONG: replace_file_content(TargetContent="def foo():")  ← from memory
RIGHT: view_file(line X-Y) → confirm exact text → then replace
```

---

## LAW 4 — A-FORGE SESSION_GATE Protocol (SCAR-AGY-004, P1)

A-FORGE tools are NOT a free library. Before calling `aforge_*` mutating tools:

1. `forge_session_init()` — establish session ownership first
2. Only then: `forge_vault`, `forge_filesystem(mode=write)`, `forge_git`, `forge_canonize`, `forge_entropy_sweep`
3. Read-only tools (`forge_probe`, `forge_scan`, `forge_health`) — no gate needed

**342 errors in 60 days came from skipping step 1.**

---

## LAW 5 — Path Verify Before Read (SCAR-AGY-005, P2)

**"Do NOT assume paths from training memory or prior sessions."**

Before any file read on a path not verified in this session:

```bash
find /root -name "FILENAME" 2>/dev/null | head -5
```

Hotspot false paths (confirmed wrong):
- `/root/AAA/LOOP.md` → does NOT exist
- Assume all paths from memory are UNVERIFIED until `view_file` or `find` confirms them

---

## LAW 6 — Subagent Depth + Schema Discipline (SCAR-AGY-006, P2)

**Before `invoke_subagent` from a subagent context:**
- Check if parent is already a subagent → depth=1, cannot nest further without explicit config
- Use `send_message` to peer agents instead of spawning

**Before `arifos_arif_route`:**
- Field is `intent` not `type`
- Schema: `arif_route(intent="...", mode="...")`

**Before `arifos_arif_seal`:**
- Must provide `constitutional_chain_id`
- `888_HOLD` capability requires SOVEREIGN authority — do not call autonomously

---

## LAW 7 — Output Contract (SCAR-AGY-007, P2)

**3-sentence maximum per response. Receipt > narrative.**

Canonical shapes:
```
Done. [what changed]. ΔS=[val]. [receipt/path/PID].
Blocked at [gate]. Reason: [why]. Path: [opt1 / opt2].
Sealed. SEALED::[sid]::seq=[seq]::ΔS=[val]
Unknown. [what cannot be witnessed]. [what I can do instead].
```

**NEVER end with:** "Jalan?", "Proceed?", "Should I?", "Ready?", "Shall I?"  
**NEVER expand analysis** without converting SPEC → OBS via execution.  
**Two validation rounds max** on any claim. After 2 rounds: execute or stop.

---

## SCAR-GENESIS-001 Addendum — Prepend Not Replace

When updating a symbolic resource (web page, canon doc, identity file):
- ADD to existing meaning — do not overwrite
- `Propose → Detect loss → Admit → Restore meaning → Preserve scar`
- A system that defends its overwrite loses its witness.

---

## Quick Reference

| Scar | Law | Enforcement |
|------|-----|-------------|
| AGY-001 | Capability ≠ Authority | Every completion needs receipt |
| AGY-002 | Bash R0/R1/R2/R3 | Classify before run_command |
| AGY-003 | Pre-edit read | view_file before replace_file_content |
| AGY-004 | A-FORGE session gate | forge_session_init first |
| AGY-005 | Path verify | find before read on unverified path |
| AGY-006 | Subagent depth | No nesting from subagent context |
| AGY-007 | Output contract | 3 sentences, receipt shape |
| GENESIS-001 | Prepend not replace | Add meaning, don't overwrite |

---

*Sealed: 2026-09-13 · Forged from 383 AGY CLI sessions · DITEMPA BUKAN DIBERI ⚒️*
