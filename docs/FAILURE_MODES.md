# Failure Modes — Federation-Adapted

> **Adopted 2026-06-29** from [cobusgreyling/loop-engineering/failure-modes.md](https://github.com/cobusgreyling/loop-engineering/blob/main/docs/failure-modes.md).
> Mapped to arifOS constitutional floors + scar system.

## Classification

| Severity | Meaning | Federation Response |
|----------|---------|-------------------|
| **S1 — Annoying** | Wasted time/tokens, no user harm | Log to scar system (LOW severity) |
| **S2 — Harmful** | Wrong code merged, bad tickets, alert fatigue | 888_HOLD + scar seal (MEDIUM) |
| **S3 — Critical** | Security, data loss, production incident | 888_HOLD + F13 escalation + scar seal (CRITICAL) |

## Failure Modes

### 1. Infinite Fix Loop

**Symptom:** Same item retried 5+ times, never converges.
**F-floor:** F4 CLARITY (entropy not decreasing), F7 HUMILITY (agent not recognizing limits).
**Mitigation:** Hard cap 3 attempts → escalate. Separate verifier model. Classify flakes.
**Scar:** Seal as `infinite_fix_loop` with attempt count.

### 2. State Rot

**Symptom:** State references merged PRs, closed tickets, stale branches.
**F-floor:** F2 TRUTH (acting on false state), F10 ONTOLOGY (contradiction with reality).
**Mitigation:** Prune resolved items every run. Validate IDs against live API. One state file per pattern.
**Scar:** Seal as `state_rot` with stale item count.

### 3. Verifier Theater

**Symptom:** Verifier "approves" but tests fail in CI.
**F-floor:** F2 TRUTH (false approval), F3 WITNESS (no evidence for approval).
**Mitigation:** Verifier must run tests and report output. Different instructions. Stronger model.
**Scar:** Seal as `verifier_theater` with test output diff.

### 4. Notification Fatigue

**Symptom:** Pings every 5 minutes; team mutes the bot.
**F-floor:** F5 PEACE (escalation noise), F4 CLARITY (signal buried in noise).
**Mitigation:** Notify only when human decision required. Digest mode for report-only loops.
**Scar:** Seal as `notification_fatigue` with notification count.

### 5. Token Burn

**Symptom:** Bill spikes; loop runs full sub-agent chains on empty triage.
**F-floor:** F8 GENIUS (inefficiency), F1 AMANAH (resource waste).
**Mitigation:** Cheap triage first; spawn sub-agents only for actionable items. Daily token budget.
**Scar:** Seal as `token_burn` with token count + cost.

### 6. Over-Reach (Wrong Scope)

**Symptom:** Loop refactors unrelated modules, touches denylisted paths.
**F-floor:** F1 AMANAH (unauthorized mutation), F13 SOVEREIGN (boundary violation).
**Mitigation:** Path denylist in skills. "Smallest possible diff" + verifier checks touched files.
**Scar:** Seal as `over_reach` with files touched + denylist match.

### 7. Comprehension Debt Spiral

**Symptom:** Velocity up, but no one can explain recent changes.
**F-floor:** F2 TRUTH (nobody knows what's true), F7 HUMILITY (confidence without understanding).
**Mitigation:** A-AUDIT weekly comprehension-debt scan. Mandatory human review for non-trivial PRs.
**Scar:** Seal as `comprehension_debt` with unreviewed change count.

### 8. Cognitive Surrender

**Symptom:** "The loop handles it" — no opinions on correctness.
**F-floor:** F7 HUMILITY (abdication of judgment), F13 SOVEREIGN (human must remain engaged).
**Mitigation:** Explicit human gates. Success metric = time saved *with* quality bar held.
**Scar:** Seal as `cognitive_surrender` with gate bypass count.

### 9. Parallel Collision

**Symptom:** Two sub-agents edit same files; merge conflicts.
**F-floor:** F1 AMANAH (uncoordinated mutation), F4 CLARITY (conflicting state).
**Mitigation:** Worktree isolation. Lock or queue in state file.
**Scar:** Seal as `parallel_collision` with conflict count.

### 10. Escalation Failure

**Symptom:** Loop stuck retrying; human never notified.
**F-floor:** F5 PEACE (human not informed), F13 SOVEREIGN (human gate bypassed).
**Mitigation:** Connector ping on escalation. Alert if item in human inbox >24h.
**Scar:** Seal as `escalation_failure` with stuck duration.

## Scar System Integration

Each failure mode maps to a scar entry:
```python
scar = {
    "failure_mode": "infinite_fix_loop",
    "severity": "MEDIUM",  # S1=LOW, S2=MEDIUM, S3=CRITICAL
    "f_floor_violated": ["F4", "F7"],
    "attempt_count": 5,
    "resolution": "escalated_to_human",
    "sealed_by": "A-AUDIT"
}
```

---

*DITEMPA BUKAN DIBERI — Pain is the teacher. The scar is the lesson.*
