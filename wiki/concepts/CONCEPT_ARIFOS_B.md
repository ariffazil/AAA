---
title: "Concept: arifOS F13 Self-Certification Bypass Fix"
created: 2026-05-17
updated: 2026-05-17
type: concept
category: architecture
tags: [F13, sovereign, elicitation, self-certification, arifOS, governance]
confidence: high
source: session-2026-05-17
---

# Concept: arifOS F13 Self-Certification Bypass Fix

> **Status:** FIXED | **Severity:** HIGH (F13 violation) | **File:** `arifosmcp/runtime/tools.py`

---

## The Problem

`arif_judge_deliberate` (888_JUDGE) had a structural F13 violation in its candidate acceptance logic.

**Original code** (`_elicit_judge_candidate`, pre-2026-05-17):

```python
if candidate and candidate.strip():
    return candidate.strip(), None  # ← BYPASSES ELICITATION
```

**What it allowed:** A model could call `arif_judge_deliberate(candidate="my proposed action is safe")` and the judgment would execute directly — without human review — because the candidate was provided as a tool argument.

**Why this is an F13 violation:** If the model can invoke judgment on its own output without human confirmation, the model is self-certifying. F13 states: _human veto is absolute_. The model deciding its own safety is a bypass of that veto.

---

## The Fix (Fix A — Always Elicit)

**New code:**

```python
# F13 FIX: Always elicit — the model cannot self-certify even if it provides
# a candidate as a tool argument.
#
# Rule: arif_judge_deliberate is a two-party protocol. The model requests
# judgment. The human (via elicitation) confirms the candidate. The model
# never accepts its own safety argument.
#
# Candidate provided as tool argument = advisory context (shown to human).
# Candidate confirmed via elicitation = human-authorized action.

if mode == "rules":
    return candidate, None  # Safe: rules mode returns constitutional text, not verdict

if ctx is None:
    # No MCP context = no elicitation possible = require explicit human ack
    if not candidate or not candidate.strip():
        return None, _hold("arif_judge_deliberate", "candidate required", [])
    return None, _hold(
        "arif_judge_deliberate",
        "MCP client with elicitation support required. Model cannot self-certify (F13). "
        "Use mode='history' to browse past verdicts.",
        [],
    )

# Always elicit — human must confirm even if model provided candidate
await ctx.elicit(
    "arif_judge_deliberate: Confirm the candidate to be judged.\n"
    "The model has requested judgment on an action. "
    "You (Arif) must confirm or modify the candidate before adjudication proceeds.\n\n"
    f"Candidate: {candidate_preview}",
    JudgeCandidateInput,
)
```

---

## What Changed

| Scenario | Before (bypass) | After (Fix A) |
|----------|-----------------|---------------|
| Model calls with `candidate="my action"` | Runs judgment directly | Always elicits — human must confirm |
| No ctx (no elicitation possible) | Returns HOLD (good) | Returns HOLD with F13 message (same) |
| `mode=="rules"` | Bypasses (safe — text only) | Unchanged (safe — text only) |
| `mode=="history"` | Not affected | Not affected (read-only) |

---

## Architectural Implications

**F13 is enforced structurally, not procedurally.** The fix is in the code path — not in a comment or a prompt instruction. The model physically cannot bypass elicitation because the bypass line was removed.

**Elicitation is the F13 gate.** The MCP `ctx.elicit()` call is the hard human-in-the-loop mechanism. If elicitation fails (no MCP client support), the tool returns HOLD — it does not proceed without human confirmation.

**Candidate as tool argument becomes advisory context.** The model's candidate is shown to the human in the elicitation dialog, but the human must explicitly click Confirm. The model cannot однозначно accept its own safety.

---

## Safe Modes (No Change)

| Mode | Behavior | F13 Safe? |
|------|----------|------------|
| `judge` | Full constitutional review | ✅ Now always requires elicitation |
| `compare` | Side-by-side comparison | ✅ Requires elicitation |
| `history` | Browse past verdicts (read-only) | ✅ No judgment — read-only |
| `explain` | Generate verdict rationale | ✅ No judgment — explanation only |
| `rules` | Return constitutional rules | ✅ Text only — no candidate |

---

## The Two-Party Protocol

```
MODEL                          HUMAN (Arif)
  |                                  |
  |-- request_judge(candidate) ----→ |
  |                                  |
  |    [elicitation: confirm/modify] |
  |←────────────────────────────── |
  |                                  |
  |<-- human confirms ---------------|
  |                                  |
  |-- judgment runs with human ack --|
  |                                  |
  |<-- verdict (SEAL/SABAR/HOLD/VOID)
```

The model **requests**. The human **confirms**. The model never self-certifies.

---

## Verification

```bash
cd /root/arifOS
python -m pytest tests/runtime/test_judge_reversibility.py tests/test_floors.py -q
# 24 passed ✓
```

---

**DITEMPA BUKAN DIBERI — Governance is constraint, not suggestion.**
