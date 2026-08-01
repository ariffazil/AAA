---
id: RSI-recursive-improvement
name: RSI — Recursive Self-Improvement Protocol
version: 2.0.0
description: Mandatory recursive self-improvement at session boundaries and phase transitions. Diagnoses bottlenecks, installs fixes, writes to RSI ledger, and carries forward to next session. The federation learns from every session or it stagnates.
owner: 333-AGI
risk_tier: low
floor_scope: F2, F4, F7, F11
autonomy_tier: T1
trigger_when: session_end, phase_boundary, repetition_alert, bottleneck_detected
---

# RSI — Recursive Self-Improvement Protocol

> **Doctrine:** DITEMPA BUKAN DIBERI — Forged, not given.
> **SOT:** `/root/AAA/prompts/INIT.md` §3 (canonical reference)
> **Script:** `rsi-cycle.py` (Phase 1-4 executor + ledger writer)
> **Ledger:** `/root/.local/share/arifos/rsi-ledger.jsonl`
> **Zen:** Every session must teach the next one something. If you finished without learning, you stagnated.

## When to Run RSI (MANDATORY — not optional)

```
ALWAYS RUN:
  ├── Session end (before /seal)
  ├── Phase transition (observe→reason→plan→execute→seal)
  ├── After 3+ retries of the same approach
  └── Any HOLD or VOID verdict

OPTIONALLY RUN:
  ├── Mid-session bottleneck detection (stuck for >5 min on same problem)
  ├── Complex multi-phase work (≥3 distinct cognitive stages)
  └── After any tool produced an unexpected error
```

## The 5-Phase Protocol

### Phase 0 — CONFIGURE TRACE
At session start or phase boundary:
- Record `session_id`, `actor_id`, `task_description`
- Set checkpoint markers for each phase
- Declare known unknowns (Ω₀ ∈ [0.03, 0.05])

### Phase 1 — TRACE
What did I actually do vs what I planned?
```json
{
  "tool_calls": {"total": N, "success": N, "failed": N},
  "files_changed": [{"path": "...", "reason": "..."}],
  "evidence_labels": {"OBS": N, "DER": N, "INT": N, "SPEC": N},
  "subagents_spawned": 0,
  "errors_encountered": 0
}
```

### Phase 2 — DIAGNOSE
Find exactly ONE bottleneck. Check in priority order:

| Priority | Bottleneck | Detection Method |
|----------|-----------|-----------------|
| 1 | REPETITION | Same tool/approach called 3+ times |
| 2 | EVIDENCE_GAP | F2 TRUTH violated — assertion without source |
| 3 | TOOL_DRIFT | Used wrong tool (ART bypass) |
| 4 | SCOPE_CREEP | Task expanded beyond declared intent |
| 5 | OVERCONFIDENCE | Confidence > 0.90 at any point |
| 6 | SKILL_BLOAT | Loaded skills not used |
| 7 | ABANDONED_PATH | Approach started then abandoned |
| 8 | ORPHAN_RESULT | Output produced but not sealed or returned |
| 9 | RECURRENCE | Same bottleneck as prior session (check ledger) |
| 10 | ENTROPY_GAIN | ΔS > 0 (workspace worse than found) |

### Phase 3 — REMEDIATE
Install ONE fix. Must be:
- **Immediate** — takes effect this session or before next
- **Reversible** — can be undone with one command (F1 AMANAH)
- **Singular** — one fix per bottleneck, not five
- **Evidence-backed** — tied to a specific trace observation

### Phase 4 — LEDGER
Execute the cycle script:
```bash
python3 /root/.agents/skills/RSI-recursive-improvement/rsi-cycle.py \
  --session-id "<session_id>" \
  --actor-id "<actor_id>" \
  --phase "session_end" \
  --trace-json '<Phase 1 trace as JSON>' \
  --bottleneck "<DIAGNOSED_BOTTLENECK>" \
  --bottleneck-detail "<one-line explanation>" \
  --fix "<what was installed>" \
  --delta-entropy <float: -1.0 to 1.0> \
  --next-session-hint "<what next session should watch for>"
```

This writes to `/root/.local/share/arifos/rsi-ledger.jsonl` and emits a receipt.

### Phase 5 — SEAL
If session produced a meaningful artifact:
- Include RSI receipt in seal payload
- Reference `next_session_hint` in carry_forward.json

## Anti-Patterns (NEVER do these)

```
❌ RSI without a trace — memory is not evidence
❌ Fixing artifacts but not cognition — patch the thinking, not just the output
❌ RSI that runs but results are ignored — ledger must be read next session
❌ RSI only at session end — bottlenecks compound during the session
❌ RSI that produces new tools instead of using existing ones — use less, not more
❌ Multiple bottlenecks per cycle — focus on the ONE root cause
```

## Recurrence Detection

Before diagnosing, check if the bottleneck is recurring:
```bash
# Check last 5 RSI entries for same bottleneck type
tail -5 /root/.local/share/arifos/rsi-ledger.jsonl | \
  python3 -c "
import json, sys, collections
bottlenecks = collections.Counter()
for line in sys.stdin:
    d = json.loads(line)
    bottlenecks[d.get('bottleneck','?')] += 1
for b, c in bottlenecks.most_common():
    print(f'  {b}: {c}x in last 5 sessions')
"
```

If a bottleneck appears 2+ times, escalate from REMEDIATE to ARCHITECTURAL FIX.

## Integration Points

| Trigger Point | What RSI Does |
|---------------|---------------|
| `/seal` Step 2 | RSI cycle runs BEFORE seal — seal includes RSI receipt |
| `/init` carry_forward | Last 3 RSI entries loaded into session context |
| EUREKA777 | If paradox resolved, RSI records it as the fix |
| Reality Loop VERIFY stage | RSI feeds improvement signals back to ENCODE stage |
| arifFlow FQ | Low FQ triggers mid-session RSI check |

## Floor Alignment

| Floor | RSI Obligation |
|-------|---------------|
| F2 TRUTH | Trace must match reality — no fabricated tool counts |
| F4 CLARITY | ΔS ≤ 0 — fix must reduce entropy, not add complexity |
| F7 HUMILITY | Declare what you didn't know. Ω₀ in [0.03, 0.05] |
| F11 AUDIT | Every cycle written to ledger. No silent fixes. |

## The Zen

> Every session that doesn't teach the next one is a dead session.
> The RSI ledger is the federation's learning spine.
> If you can't name what you learned, you didn't learn.
