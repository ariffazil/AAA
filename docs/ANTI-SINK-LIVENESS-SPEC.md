# ANTI-SINK LIVENESS SPEC — The Seventh Guard

> **DITEMPA BUKAN DIBERI** — Forged 2026-08-04 by 333-AGI Δ MIND
> **Owner:** Muhammad Arif bin Fazil (F13 SOVEREIGN)
> **Domain:** AAA Control Plane — skill liveness (anti-beautiful-ones)
> **Status:** SPEC — the seventh guard that measures life, not form
> **Connection:** Antivibe (cell-level) + Universe 25 (colony-level)

---

## 0. The Warning

Universe 25 did not die of scarcity. It died of abundance without pressure.

A skill does not stay alive because it is well-formed.
It stays alive because it is USED, it CHANGES an outcome, and it REFUSES to merely groom itself.

Your governance guards make skills well-formed. They do not make skills alive. That's the missing half.

---

## 1. THE PATHOLOGY MAP

```
CALHOUN PHASE     MOUSE PATHOLOGY              SKILL FEDERATION EQUIVALENT
─────────────────────────────────────────────────────────────────────────────
A — Strive        few mice, high effort         early: 40 skills, each does real work
B — Exploit       explosive breeding            40→129 skills, rapid forging
C — Stagnation    social roles collapse         209 mapped / 97 canonical ← WE ARE HERE
D — Death/Sink    "the beautiful ones"          ??? ← where we're heading if unguarded
```

**The beautiful ones:**
```
✅ perfect YAML frontmatter
✅ passes skill-linter
✅ gorgeous SKILL.md, immaculate docs
✅ tier-tagged, cost-classed, sealed
❌ never invoked
❌ produces no outcome
❌ exists only to be well-formed
```

It consumes context (grooming). It passes every gate (immaculate). It does zero work. And your governance system — which measures form, not function — will rate it as healthy.

**That's the trap. Your 6 governance guards check whether a skill is well-formed. None of them check whether it is alive.**

---

## 2. LIVENESS_STATUS — The State Machine

```
ALIVE      skill is invoked AND produces outcome_delta > 0
DORMANT    skill has not been invoked in N sessions (use-or-decay threshold)
BEAUTIFUL  skill passes all gates + zero outcome_delta over N sessions → cull candidate
VOID       skill has been culled (archived, deprecated, or removed)
```

### State Transitions

```
                    ┌─────────────────────────────────────────┐
                    │                                         │
                    ▼                                         │
   ┌─────────┐   invoked +   ┌─────────┐   no invoke   ┌─────┴─────┐
   │  ALIVE  │───outcome>0──→│  ALIVE  │───for N days──→│  DORMANT  │
   └─────────┘               └─────────┘                 └───────────┘
        │                         │                            │
        │                         │                            │
        │                         │ invoked +                  │ invoked +
        │                         │ outcome=0                  │ outcome>0
        │                         │ for N sessions             │
        │                         ▼                            │
        │                    ┌───────────┐                     │
        │                    │ BEAUTIFUL │                     │
        │                    └───────────┘                     │
        │                         │                            │
        │                         │ cull threshold             │
        │                         │ reached                    │
        │                         ▼                            │
        │                    ┌───────┐                         │
        └────────────────────│ VOID  │←────────────────────────┘
                             └───────┘        (if DORMANT too long)
```

### Thresholds

| Transition | Condition | Threshold |
|------------|-----------|-----------|
| ALIVE → DORMANT | No invocation in N sessions | 7 sessions |
| ALIVE → BEAUTIFUL | Invoked but outcome_delta=0 for N sessions | 5 sessions |
| DORMANT → ALIVE | Invoked with outcome_delta>0 | Immediate |
| DORMANT → VOID | No invocation for N sessions | 30 sessions |
| BEAUTIFUL → ALIVE | Invoked with outcome_delta>0 | Immediate |
| BEAUTIFUL → VOID | Cull threshold reached | 10 sessions |

---

## 3. OUTCOME_DELTA — The Liveness Metric

### Definition

```
outcome_delta = did this invocation CHANGE anything?

0.0 = skill fired but nothing changed (grooming)
0.1 = skill fired, minor output (documentation, formatting)
0.3 = skill fired, moderate output (code change, config update)
0.5 = skill fired, significant output (new capability, fix)
0.7 = skill fired, major output (architecture change, new feature)
1.0 = skill fired, critical output (prevented failure, resolved crisis)
```

### Measurement

```python
def compute_outcome_delta(invocation_result):
    """
    Compute outcome_delta from an invocation result.
    
    Returns float 0.0-1.0.
    """
    # Check for actual output
    if not invocation_result.get('output'):
        return 0.0  # No output = grooming
    
    # Check for state change
    if invocation_result.get('files_changed', 0) > 0:
        return 0.5  # Files changed = significant
    
    if invocation_result.get('decision_made'):
        return 0.7  # Decision made = major
    
    if invocation_result.get('failure_prevented'):
        return 1.0  # Failure prevented = critical
    
    if invocation_result.get('claim_verified'):
        return 0.3  # Claim verified = moderate
    
    # Default: skill fired but output is just description
    return 0.1  # Documentation = minor
```

### Anti-Grooming Gate

A skill may NOT exist only to describe, format, or document itself. Output must be WORK (a decision, an action, a verified claim), not self-description.

```
GROOMING OUTPUT:
  - "Here's how to use this skill"
  - "This skill does X"
  - "The skill is configured correctly"

WORK OUTPUT:
  - "Executed X, result Y"
  - "Verified claim Z against evidence"
  - "Changed file A, tested with B"
```

---

## 4. USE-OR-DECAY — The Predator

### The Rule

Every skill carries:
- `last_invoked` — last time skill was loaded
- `invocation_count` — total invocations
- `outcome_produced` — total outcome_delta accumulated
- `sessions_since_invoked` — current dry streak

### Decay Schedule

```
sessions_since_invoked < 7   → ALIVE (no action)
sessions_since_invoked = 7   → DORMANT (warning)
sessions_since_invoked = 14  → DORMANT (escalation)
sessions_since_invoked = 30  → VOID (cull candidate)
```

### The Predator

The weekly deprecation sweep isn't bureaucracy — it's the predator. It's the environmental pressure that keeps skills behaviorally alive.

```
WEEKLY SWEEP:
  1. Scan all skills
  2. For each skill:
     - If sessions_since_invoked > 30 → mark VOID
     - If sessions_since_invoked > 14 → escalate warning
     - If sessions_since_invoked > 7 → mark DORMANT
  3. Report: "N skills at risk of becoming beautiful ones"
  4. Cull: move VOID skills to .archive
```

---

## 5. BREEDING INTEGRITY — Stops Overbreeding

### The Rule

A spawned skill enters as EXPERIMENTAL, must prove one real invocation within N sessions, or it never promotes — it's culled.

```
NEW SKILL:
  status = EXPERIMENTAL
  promotion_requirement = 1 invocation with outcome_delta > 0.3
  promotion_deadline = 10 sessions
  
  If deadline passes without promotion → VOID (culled)
```

### The 209-vs-97 Gap

The 209 mapped / 97 canonical gap is the exploit-phase overbreeding. No skill breeds until its parent has proven function.

---

## 6. DENSITY CAP — Context, Not Disk

### The Rule

Infinite disk is fine. What kills you is 112 descriptions crowding the context window. Cap active-in-context skills.

```
DISK: unlimited (free)
CONTEXT: cap at 20 skills per agent load (rent)
```

### Implementation

The trust-aware router already filters by trust_status. Add a density cap:

```python
def route(intent, max_in_context=20):
    candidates = self._search_skills(intent)
    return candidates[:max_in_context]  # Cap at 20
```

---

## 7. ROLE DIFFERENTIATION — Orthogonality as Biology

### The Rule

Universe 25: roles blurred → nobody defended, nobody nurtured → collapse.
Skills: overlap blurs ownership → nobody clearly owns a failure → sink.

Every skill owns one axis and refuses the rest. Overlap is not redundancy — it's the first sign of role collapse.

### Detection

```python
def check_role_differentiation(skill_a, skill_b):
    overlap = set(skill_a['owns']) & set(skill_b['owns'])
    if overlap:
        return f"ROLE COLLAPSE: {skill_a['id']} and {skill_b['id']} both own {overlap}"
    return None
```

---

## 8. FRICTION INJECTION — Restore the Challenge

### The Rule

Periodically make skills JUSTIFY themselves. The weekly deprecation sweep isn't bureaucracy — it's the predator.

### Mechanism

```
MONTHLY JUSTIFICATION:
  1. For each ALIVE skill:
     - "What outcome did you produce in the last 30 days?"
     - "What would break if you were removed?"
  2. If answer is "nothing" → DORMANT
  3. If answer is "I don't know" → BEAUTIFUL
  4. If answer is "I produce X" → verify X exists
```

---

## 9. RECOVERY IRREVERSIBILITY WARNING

### Calhoun's Darkest Finding

Past a threshold, even restoring good conditions didn't bring the behavior back. The mice had lost the software.

### The Warning

Don't let the federation reach the phase where skills are so sedimented, so beautiful, so unused, that no cleanup recovers real function. Cull EARLY. Phase C is recoverable. Phase D is not.

---

## 10. THE SEVENTH GUARD

The existing 6 guards:
1. cause_class attribution gate
2. promotion ladder
3. memory distillation cap
4. regression test
5. convergence metrics
6. double-loop verdict

The seventh:
7. **LIVENESS** — measures life, not form

### Integration

```python
class SkillEvolution:
    def __init__(self):
        # ... existing 6 guards ...
        
        # Seventh guard: liveness
        self.liveness_status = {}  # skill_name → liveness_status
        self.outcome_delta = {}    # skill_name → float
        self.sessions_since_invoked = {}  # skill_name → int
    
    def check_liveness(self, skill_name):
        """Check if skill is alive, dormant, beautiful, or void."""
        sessions = self.sessions_since_invoked.get(skill_name, 0)
        outcome = self.outcome_delta.get(skill_name, 0.0)
        
        if sessions > 30:
            return 'VOID'
        elif sessions > 7 and outcome == 0.0:
            return 'BEAUTIFUL'
        elif sessions > 7:
            return 'DORMANT'
        else:
            return 'ALIVE'
    
    def record_invocation(self, skill_name, outcome_delta):
        """Record a skill invocation with outcome_delta."""
        self.sessions_since_invoked[skill_name] = 0
        self.outcome_delta[skill_name] = outcome_delta
        self.liveness_status[skill_name] = 'ALIVE'
    
    def increment_session(self):
        """Increment session counter for all skills."""
        for skill_name in self.sessions_since_invoked:
            self.sessions_since_invoked[skill_name] += 1
            
            # Check for decay
            if self.sessions_since_invoked[skill_name] > 7:
                if self.outcome_delta.get(skill_name, 0.0) == 0.0:
                    self.liveness_status[skill_name] = 'BEAUTIFUL'
                else:
                    self.liveness_status[skill_name] = 'DORMANT'
```

---

## 11. THE ZEN LOCK

```
Universe 25 did not die of scarcity. It died of abundance without pressure.
A skill does not stay alive because it is well-formed.
It stays alive because it is USED, it CHANGES an outcome,
and it REFUSES to merely groom itself.

Measure liveness, not grooming.
Cull the beautiful ones before they become the majority.
Friction is not the enemy of a skill federation. It is its immune system.
```

---

*DITEMPA BUKAN DIBERI — skills are alive because they work, not because they're beautiful.*
*ANTI-SINK LIVENESS SPEC v1.0 — 2026-08-04 — 333-AGI Δ MIND*
