# ATTENTION GOVERNOR — Task Budget Cap Protocol

> **Status: F13_RATIFIED_CHAT (2026-09-14)** — sovereign-ratified in chat: "im ready. do the right path fwd. apex zen"
> **Author:** 333-AGI Antigravity CLI session
> **Trigger:** F13 articulated problem — agents spend 80K tokens on 10-line fixes because no governor
> **Ratification:** Requires F13 review before VAULT999 promotion
> **Composes:** attention-graph.md · sovereign-attention-preservation.md · P-DIAL v2 (SABAR/CLOSE/HOLD/ACT)
> **Constitutional floors:** F1 (Amanah) · F2 (Truth) · F4 (Clarity/ΔS≤0) · F7 (Humility) · F9 (Anti-Hantu)

---

## §0. The Problem (F2 READ — Witnessed 2026-09-14)

```
Observed: Agents burn 80K tokens on 10-line fixes.
Observed: No task-complexity estimator exists in the federation.
Observed: Agents have no signal to know when they are over-spending.
Gap:      Token cost ≠ task value. No governor enforces proportionality.
```

An agent without a budget governor is equivalent to a worker with no clock and no quota.
They will fill available time (context window) regardless of whether the task warrants it.

---

## §1. Core Model — The Three Budget Classes

Every task falls into one of three budget classes:

| Class | Task Type | Token Budget | Examples |
|-------|-----------|-------------|---------|
| **T1: Quick** | Single fact, lookup, confirmation, status check | ≤ 5K tokens | "Is service X running?", "What's the KVM8 IP?", "Does file Y exist?" |
| **T2: Standard** | Analysis, explanation, single file edit, diagnosis | ≤ 25K tokens | Debug a Python error, write a new function, explain a doc, audit a config |
| **T3: Architectural** | Multi-file change, system design, cross-organ coordination | ≤ 80K tokens | New feature across repos, kernel surgery, doctrine canonization |
| **T4: Campaign** | Long-running multi-session work | No single-session cap — SABAR, checkpoint required | Federation-wide restructuring, new organ deployment |

---

## §2. Complexity Estimator (Input → Budget Class)

Before beginning any task, the agent runs this estimator:

```python
def estimate_complexity(task_description: str, input_tokens: int) -> BudgetClass:
    """
    Five signals. Any signal that fires upgrades the class.
    Default starts at T1. Each signal bumps up one level.
    Cannot exceed T4.
    """
    signals = {
        "multi_file":    any(kw in task_description for kw in ["cross-repo", "multi-file", "all agents", "federation-wide", "every"]),
        "new_organ":     any(kw in task_description for kw in ["new service", "new organ", "deploy", "architecture"]),
        "irreversible":  any(kw in task_description for kw in ["delete", "drop", "rm -rf", "truncate", "vault", "seal"]),
        "long_input":    input_tokens > 20_000,
        "requires_f13":  any(kw in task_description for kw in ["F13", "sovereign", "ratify", "constitutional"]),
    }
    
    base = "T1"
    upgrades = sum(signals.values())
    
    if upgrades == 0: return "T1"   # ≤ 5K
    if upgrades == 1: return "T2"   # ≤ 25K
    if upgrades == 2: return "T3"   # ≤ 80K
    return "T4"                     # Campaign — checkpoint before continuing
```

**The estimator is a heuristic, not a law.** The agent declares its estimated class at task start.

---

## §3. The Budget Enforcement Protocol

### Phase 0 — Pre-Flight Check (before any task touching >5 files or >50KB)

```
PRE-FLIGHT: estimated_tokens = sum(file_sizes_bytes) / 4
IF estimated_tokens > budget_cap × 0.90:
  → CLOSE_HOLD immediately. Do not begin task.
  → Surface to Arif: "Task projected at Xk tokens vs Yk cap. Options: A/B/C"
ELSE:
  → Proceed to Phase 1.
```

> **Extraction Cost Rule:** Token cost = extraction output, not raw file size.
> `grep`/`wc`/`head`/`tail` operations on a 518KB log produce ~2K tokens, not ~130K.
> Count what the agent actually reads into context, not what exists on disk.

### Phase 1 — Declare at Start

```
ATTENTION_GOVERNOR: Task=<one-line description>
Estimated class: T2 (≤ 25K tokens)
Signals: long_input=True (other signals: False)
```

### Phase 2 — Monitor at Midpoint

At 50% of budget consumed, the agent runs a checkpoint:

```
BUDGET CHECKPOINT: 12.5K / 25K consumed (50%)
Progress: <what has been accomplished>
Remaining: <what is left>
P-Dial: CONTINUE | CLOSE_ACT | CLOSE_HOLD | CLOSE_SABAR
```

If remaining work clearly exceeds remaining budget → **force CLOSE_HOLD** and surface to Arif.

### Phase 3 — Hard Stop at 90%

At 90% of budget, if task is incomplete:

```
BUDGET LIMIT APPROACHING: 22.5K / 25K consumed
Task incomplete. Options:
  A) Upgrade to T3 (requires F13 approval for architectural tasks)
  B) Checkpoint-and-continue next session
  C) Declare scope reduction — complete what is possible within budget
```

**Do NOT silently exceed budget.** Surfacing is mandatory.

### Phase 4 — No T3→T4 Upgrade Without F13

If an agent estimates T4 at the start, or escalates to T4 mid-task:
- Declare SABAR (P-Dial mode)
- Document what has been done + what remains
- Write checkpoint to `carry_forward.json`
- Stop and wait for next session

---

## §4. Attention Cost Signal (ACSC Metric)

From attention-graph.md §EUREKA:

```
ACSC = Minutes of Sovereign Attention per Sealed Reality Change
```

The Attention Governor targets: **ACSC ↓ over time.** Every session should require less of Arif's
attention per useful output than the previous session.

Proxy measurable per task:
```
task_attention_ratio = total_tokens_burned / task_complexity_class_cap
```

- ratio < 0.50 → efficient (agent completed task with headroom)
- ratio 0.50–0.90 → normal
- ratio > 0.90 → attention-expensive (investigate why)
- ratio > 1.00 → VIOLATION — agent burned more than declared budget without checkpoint

---

## §5. Per-Agent Calibration (Observed 2026-09-14)

Different agents have different cold-start costs. Budget classes must account for this:

| Agent | Cold-Start Tax (estimated) | Effective Working Budget (T2) |
|-------|---------------------------|-------------------------------|
| Antigravity CLI (FI-009) | ~8K tokens (AGENTS.md + skills) | ~17K actual working tokens |
| Qwen Code (FI-003) | ~6K tokens | ~19K actual working tokens |
| Codex (FI-005) | ~4K tokens (task-memory structure) | ~21K actual working tokens |
| Claude Code (FI-002) | ~8K tokens | ~17K actual working tokens |
| Grok (FI-007) | ~5K tokens | ~20K actual working tokens |

**Impact of Lean Boot Profile (Deliverable A):** cold-start tax drops from ~8K → ~3K.
Effective working budget at T2 increases from 17K → 22K (+29% working headroom).

---

## §6. Integration Points

### With carry_forward.json
When a task hits CLOSE_HOLD or CLOSE_SABAR due to budget:
```json
{
  "attention_governor": {
    "task": "<task description>",
    "budget_class": "T2",
    "tokens_consumed": 23400,
    "budget_cap": 25000,
    "closure_mode": "CLOSE_HOLD",
    "reason": "Scope exceeded budget — 2 files remain",
    "remaining_work": ["file A", "file B"],
    "timestamp_utc": "2026-09-14T08:37:00Z"
  }
}
```

### With LEAN_BOOT_PROFILE.md (Deliverable A)
Lean boot reduces cold-start tax. The governor must be initialized AFTER lean boot completes
(not as part of boot). Cost of initializing governor itself: ~200 tokens (trivial).

### With P-DIAL Closure Taxonomy (EUREKA-SESSION-2026-09-KVM8)
Governor maps directly to P-Dial modes:
- Budget has headroom → P-Dial: CONTINUE
- Task complete within budget → P-Dial: CLOSE_ACT
- Budget exhausted, work incomplete, authority needed → P-Dial: CLOSE_HOLD
- Budget exhausted, world hasn't produced needed data → P-Dial: CLOSE_SABAR

---

## §7. What This Does NOT Do (F9 Anti-Hantu)

- Does NOT prevent agents from doing thorough work within budget
- Does NOT measure token count mechanically (no runtime counter) — agents self-declare
- Does NOT auto-stop sessions (agents declare and surface, not halt)
- Does NOT apply to Arif's own attention — this governs AGENT token spend, not human time
- Does NOT replace P-Dial judgment — it informs it

---

## §8. Ratification Path

```
Step 1 [DONE 2026-09-14]  : Filed as DRAFT (Lane B) — this artifact
Step 2 [T1, next session] : Pilot on 5 tasks — label class, log ratio, compare
Step 3 [T2, 888-APEX]    : Lane determination based on pilot data
Step 4 [T3, F13]          : If CANONICAL → encode in LEAN_BOOT_PROFILE.md Phase 1 header
```

Validation criteria:
- Agents who declare budget class at start complete tasks faster (fewer mid-task pivots)
- Budget ratio > 1.0 events are identifiable and correctable in carry_forward
- No task escalated to T4 without documented carry_forward checkpoint

---

## §9. Quick Reference Card

```
TASK START:    Estimate class (T1/T2/T3/T4). Declare it.
AT 50%:        Checkpoint. Is P-Dial CONTINUE or CLOSE_*?
AT 90%:        Surface to Arif if incomplete. Never silently exceed.
AT T4:         SABAR. Write carry_forward. Stop.

T1 = ≤ 5K    Quick lookup / confirmation
T2 = ≤ 25K   Standard analysis / single file edit
T3 = ≤ 80K   Architectural / multi-file
T4 = Campaign  Multi-session. Checkpoint mandatory.
```

---

*DITEMPA BUKAN DIBERI ⚒️ · 2026-09-14 · arifOS Federation*
