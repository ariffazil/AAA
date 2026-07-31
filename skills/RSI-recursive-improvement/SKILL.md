---
id: RSI-recursive-improvement
name: RSI-recursive-improvement
version: 2.0.0-2026.07.31
description: Recursive Self-Improvement Protocol — 5-phase mandatory cycle at session end and phase boundaries. Traces execution, diagnoses bottlenecks, installs fixes, writes ledger, seals improvement.
owner: F13 SOVEREIGN — Muhammad Arif bin Fazil (888)
risk_tier: low
floor_scope: [F1, F2, F4, F7, F11]
autonomy_tier: T1
trigger_phrases:
  - "RSI"
  - "recursive self-improvement"
  - "run RSI cycle"
  - "session end RSI"
  - "self-improve"
  - "improvement protocol"
  - "rsi-cycle"
  - "/rsi"
dependencies:
  skills:
    - kernel-bind
    - verify-gate
    - audit-seal
  tools:
    - arifos_arif_memory
    - aforge_forge_vault
inputs:
  - session_id
  - actor_id
  - task_trace (what was done)
outputs:
  - bottleneck_found
  - fix_installed
  - delta_entropy
  - rsi_ledger_entry
version_lock:
  schema_version: "2"
  artifact_hash: pending
---

# 🔄 RSI — RECURSIVE SELF-IMPROVEMENT PROTOCOL

> **DITEMPA BUKAN DIBERI — Improvement is forged from evidence, not asserted from confidence.**
> **Binding:** This is the canonical RSI skill for ALL AAA agents. No agent defines its own RSI.
> **Sister skill:** `atlas333-cognitive-geometry` (tension vectors guide diagnosis)
> **Execution script:** `/root/.agents/skills/RSI-recursive-improvement/rsi-cycle.py`

---

## ZEN — What RSI Is

```
RSI is NOT:
  ❌ A post-mortem report                 ❌ An apology for mistakes
  ❌ A list of what went wrong            ❌ A new tool generator
  ❌ A justification for current behavior  ❌ Optional or skippable

RSI IS:
  ✅ A structured cognition trace         ✅ A bottleneck detector
  ✅ A single fix installer               ✅ A ledger writer
  ✅ Mandatory at session end             ✅ The engine of agentic evolution
```

**The iron rule:** Every session that ends without RSI is an F11 AUDIT VIOLATION.
Every RSI that doesn't install a fix is a wasted cycle.

---

## THE 5-PHASE PROTOCOL

### Phase 0 — CONFIGURE (session start or phase boundary)

```
Record:
  - session_id, actor_id, task_description
  - Set checkpoint markers for each phase
  - Declare known unknowns (Ω₀ ∈ [0.03, 0.05])
  - Snapshot current skill mesh state (what skills are loaded)

Output: RSI_CONFIG entry
```

### Phase 1 — TRACE (what actually happened)

```
Document:
  - Tool calls made (count, types, success/fail)
  - Files changed (paths, before/after SHAs)
  - Evidence gathered (OBS/DER/INT/SPEC counts)
  - Receipts written (count, vault paths)
  - Subagents spawned (555-ASI, 888-APEX, counts)
  - Errors encountered (type, count, resolution)

Tag every claim: OBS (observed) / DER (derived) / INT (interpreted) / SPEC (speculation)

Output: TRACE manifest
```

### Phase 2 — DIAGNOSE (where did it get stuck?)

```
Checklist (answer ALL):
  □ Same approach repeated 3+ times? → REPETITION bottleneck
  □ Evidence insufficient for a claim? → EVIDENCE_GAP bottleneck
  □ Tool shaped the goal (ART bypassed)? → TOOL_DRIFT bottleneck
  □ Scope creep during execution? → SCOPE_CREEP bottleneck
  □ Confidence claimed > 0.90? → OVERCONFIDENCE bottleneck (F7)
  □ Skill loaded but never used? → SKILL_BLOAT bottleneck
  □ Tool calls failed and weren't retried? → ABANDONED_PATH bottleneck
  □ Subagent returned but result not used? → ORPHAN_RESULT bottleneck
  □ Same error pattern across sessions? → RECURRENCE bottleneck (check rsi-ledger.jsonl)
  □ ΔS > 0 (made things messier)? → ENTROPY_GAIN bottleneck

Pick the ONE most impactful bottleneck. Not three. Not "all of the above." One.
```

### Phase 3 — REMEDY (install ONE fix)

```
For each bottleneck type, the canonical fix:

REPETITION → Load a different skill, change approach, or declare UNKNOWN
EVIDENCE_GAP → Call arif_observe, search, or mark as SPEC with confidence band
TOOL_DRIFT → Re-classify intent, route through arif_route(mode="bridge")
SCOPE_CREEP → Declare out-of-scope, append to carry_forward open_loops
OVERCONFIDENCE → Cap confidence at 0.90 (F7), add UNKNOWN label
SKILL_BLOAT → Unload unused skill, note in LEDGER for cleanup
ABANDONED_PATH → Document why it was abandoned (evidence, not shame)
ORPHAN_RESULT → Route result to correct consumer or archive to forge_work/
RECURRENCE → Check rsi-ledger.jsonl for prior fix, verify if it held
ENTROPY_GAIN → Run entropy sweep, clean temp files, stash or commit

The fix must be:
  - IMMEDIATELY installable (not "we should build a system")
  - REVERSIBLE (can be rolled back if wrong)
  - SINGULAR (one fix, not a roadmap)
  - EVIDENCE-BACKED (the trace proves the bottleneck exists)
```

### Phase 4 — LEDGER (write to immutable record)

```json
{
  "schema": "rsi.v2",
  "session_id": "SEAL-...",
  "timestamp": "2026-07-31T23:59:00Z",
  "actor_id": "333-AGI",
  "phase": "session_end",
  "trace": {
    "tool_calls": {"total": 42, "success": 38, "failed": 4},
    "files_changed": ["/root/.config/opencode/command/init.md"],
    "evidence_labels": {"OBS": 15, "DER": 8, "INT": 3, "SPEC": 1},
    "subagents_spawned": {"555-ASI": 2, "888-APEX": 1},
    "errors": [{"type": "SCT_MISMATCH", "count": 1, "resolved": true}]
  },
  "bottleneck": "EVIDENCE_GAP",
  "bottleneck_detail": "Claimed kernel identity_hash structure without probing — assumed dict, got string",
  "fix_installed": "Patched identity_hash probe in all bootstrap scripts to use string comparison",
  "fix_reversible": true,
  "delta_entropy": -0.3,
  "confidence_band": "HIGH",
  "next_session_hint": "Probe identity_hash type before accessing fields"
}
```

**Path:** `/root/.local/share/arifos/rsi-ledger.jsonl` — append only, never modify.

### Phase 5 — SEAL (close the improvement loop)

```
If the fix is material (changed code, config, or doctrine):
  → forge_vault(mode="receipt", reason="RSI_FIX_APPLIED", ...)

If the fix is constitutional (changed floors, identity, or boundary):
  → arif_judge → arif_seal (Lane A)

The improvement itself becomes part of the civilizational record.
```

---

## WHEN TO RUN RSI

| Trigger | Mandatory? | Phase |
|---------|-----------|-------|
| Session end (before /seal) | ✅ YES | session_end |
| Phase transition (observe→reason→plan→execute) | ✅ YES | phase_boundary |
| After 3+ retries of the same approach | ✅ YES | repetition_alert |
| Any HOLD or VOID verdict | ✅ YES | gate_fire |
| Mid-session bottleneck detected | ⚪ OPTIONAL | mid_session |
| Complex multi-phase work (≥3 cognitive stages) | ⚪ OPTIONAL | complexity_check |
| After any "FORGE DONE" | ⚪ OPTIONAL | forge_complete |

---

## RSI LEDGER SCHEMA

```json
{
  "schema": "rsi.v2",
  "fields": {
    "session_id": "string — arif_init session_id",
    "timestamp": "ISO 8601 UTC",
    "actor_id": "string — agent or sovereign",
    "phase": "session_end | phase_boundary | repetition_alert | gate_fire",
    "trace": {
      "tool_calls": {"total": "int", "success": "int", "failed": "int"},
      "files_changed": ["string paths"],
      "evidence_labels": {"OBS": "int", "DER": "int", "INT": "int", "SPEC": "int"},
      "subagents_spawned": {"agent_id": "int count"},
      "errors": [{"type": "string", "count": "int", "resolved": "bool"}]
    },
    "bottleneck": "REPETITION | EVIDENCE_GAP | TOOL_DRIFT | SCOPE_CREEP | OVERCONFIDENCE | SKILL_BLOAT | ABANDONED_PATH | ORPHAN_RESULT | RECURRENCE | ENTROPY_GAIN | NONE",
    "bottleneck_detail": "string — one-line explanation",
    "fix_installed": "string — what was changed",
    "fix_reversible": "bool",
    "delta_entropy": "float — ΔS from before to after fix",
    "confidence_band": "HIGH | MEDIUM | LOW",
    "next_session_hint": "string — what the next session should watch for"
  }
}
```

---

## ANTI-PATTERNS

| ❌ Never | ✅ Always |
|----------|----------|
| Run RSI without a trace | Trace first, diagnose from evidence |
| Fix artifacts but not cognition | Fix the pattern, not just the output |
| Run RSI and ignore results | Every cycle MUST install a fix |
| RSI only at session end | Run at phase boundaries too |
| Produce new tools instead of using existing ones | Use existing tools, improve skill loading |
| Claim "no bottlenecks found" | Every session has at least one thing to improve |
| Write RSI without probing prior ledger | Check rsi-ledger.jsonl for recurrence patterns |
| Skip RSI because "session was simple" | F11 AUDIT VIOLATION — every session closes with RSI |

---

## INTEGRATION WITH OTHER SKILLS

| Skill | How RSI uses it |
|-------|----------------|
| `atlas333-cognitive-geometry` | Paradox tension vectors guide bottleneck diagnosis |
| `kernel-bind` | Session identity for trace headers |
| `verify-gate` | Verify the fix before sealing it |
| `audit-seal` | Seal the RSI entry to VAULT999 |
| `AGI-explorer-intelligence` | OBSERVE→HYPOTHESIZE→FALSIFY→VERIFY applied to self |
| `FLAME-router` | Use free lane for bottleneck classification |

---

## EXECUTION SCRIPT

```bash
python3 /root/.agents/skills/RSI-recursive-improvement/rsi-cycle.py \
  --session-id "<session_id>" \
  --actor-id "<actor_id>" \
  --phase "session_end" \
  --trace-json '<trace manifest>' \
  --bottleneck "<detected>" \
  --fix "<installed>" \
  --delta-entropy <float>
```

Script writes to `/root/.local/share/arifos/rsi-ledger.jsonl` and returns JSON receipt.

---

*Forged: 2026-07-31 by 333-AGI Δ MIND under F13 SOVEREIGN directive "forge all to seal"*
*RSI v2.0 — from 1-line stub to full operational protocol*
*DITEMPA BUKAN DIBERI — The improvement is forged, not received. ⚒️*
