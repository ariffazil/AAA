# arif_init v2 — AGI Substrate Kernel Architecture

> **Status:** RESEARCH_PROPOSAL (2026-09-20)  
> **Author:** 333-AGI (Δ MIND)  
> **Requested by:** F13 SOVEREIGN (Arif)  
> **Principle:** REALITY > EVERYTHING  
> **Binding:** This document is evidence, not doctrine. It must lose whenever reality proves it wrong.

---

## 1. What arif_init Currently Is

### 1.1 Current Modes (9+)

| Mode | Purpose | Depth |
|------|---------|-------|
| `init` | Full session binding + SCT mint | Deep |
| `light` | Minimal bind, skip heavy probes | Shallow |
| `resume` | Rebind existing session | Medium |
| `validate` | Proof summary for existing session | Read-only |
| `canary` | Transport health probe | Minimal |
| `preflight` | Pre-action checks | Medium |
| `triage` | Problem classification | Medium |
| `epoch_open` / `epoch_seal` | Epoch lifecycle | Deep |
| `opt_out` | Exit profiling | Terminal |

### 1.2 What It Produces

```
session_id, session_token (act_v1.*), authority_band, allowed_verbs,
substrate_state, drift, apex_scalars, vps_snapshot, philosophical_anchor,
nine_signal, work_contract, identity_escalation
```

### 1.3 What It Checks

- Actor identity (claimed → canonicalized → optionally cryptographically verified)
- Substrate drift (source vs built vs deployed commits)
- Constitutional floors (L01–L13)
- Organ liveness (7 organs + FED)
- VPS snapshot (CPU, RAM, disk, load)
- DID registry (actor authorization)

### 1.4 The 64-Field Contradiction Problem

The contradiction detector (`runtime/contradiction_detector.py`) found **64 fields** across the kernel that all answer "may I proceed?" — mutation_allowed, seal_allowed, effective_verdict, authority_band, execution_state, can_mutate, can_claim_success, etc. The detector was built to prove they're redundant before deletion. **Many still exist.**

---

## 2. What an AGI Substrate Kernel Must Be

The user's axiom: **REALITY > EVERYTHING.**

This is not a slogan. It is an architectural constraint that reshapes every aspect of init:

> "A constitution designed to lose whenever reality proves it wrong."

### 2.1 The Seven Architectural Shifts

| # | Current | AGI-Grade | Why |
|---|---------|-----------|-----|
| 1 | Bind identity → check substrate → issue token | **Probe reality → confront agent with truth → bind identity → issue token** | Identity without reality grounding is cosplay |
| 2 | Report drift as metadata | **Make drift the first thing the agent must process** | Drift is not a status field — it's a reasoning constraint |
| 3 | Authority bands as static labels | **Authority bands as dynamic, falsifiable claims** | Authority changes as reality changes |
| 4 | Philosophical anchor as decoration | **Philosophical anchor as the first reasoning test** | If the agent can't engage with the paradox, it can't govern |
| 5 | Work contract as budget | **Work contract as epistemic commitment** | What will you NOT claim? What will you falsify? |
| 6 | Nine-signal as post-hoc | **Nine-signal as pre-flight** | Measure the system before letting it act |
| 7 | Session as context window | **Session as evidence chain** | Every session carries its contradictions forward |

---

## 3. The New arif_init Architecture

### 3.1 Init as Reality Confrontation

```
arif_init(mode="init") should not be:
  "Hello, here's your token, go play."

It should be:
  "Here is what is true right now. Here is what you don't know.
   Here is what contradicts your last session. Here is what the
   human was doing when they last spoke. Now: can you operate
   under these conditions? Prove it."
```

### 3.2 The 10 Gates (replacing 9 modes)

Each gate is a checkpoint. The agent cannot proceed past a gate until it satisfies the condition. Gates are not optional — they are the constitution's way of losing to reality.

#### Gate 0: REALITY SNAP (pre-identity)

**Before binding identity, probe reality.**

```python
reality_snapshot = {
    "time": now_utc(),
    "substrate_drift": measure_drift(),        # source vs built vs deployed
    "organ_liveness": probe_all_organs(),       # 7 organs + FED
    "fq_pulse": probe_arifflow(),               # metabolic state
    "entropy_baseline": measure_entropy(),      # file count, uncommitted, disk
    "prior_contradictions": load_carry_forward(), # unresolved from last session
    "human_state": probe_well(),                # Arif's last known state
}
```

**The agent receives this BEFORE its identity is bound.** It must acknowledge reality before it can claim authority.

#### Gate 1: NEGATIVE KNOWLEDGE DECLARATION

**What does the system NOT know?**

```python
negative_knowledge = {
    "unmeasured_scalars": [...],      # G, C_dark, W3 if unmeasured
    "degraded_organs": [...],         # which organs are down
    "unknown_human_state": True/False, # can we read Arif?
    "stale_data": [...],              # what's older than TTL
    "unresolved_contradictions": [...], # from prior sessions
}
```

An agent that doesn't know what it doesn't know is dangerous. This gate forces the declaration.

#### Gate 2: FALSIFIABILITY CONTRACT

**What would disprove the agent's assumptions?**

```python
falsifiability_contract = {
    "assumptions": [
        {"claim": "substrate is functional", "falsifier": "drift=true"},
        {"claim": "organs are reachable", "falsifier": "any organ DOWN"},
        {"claim": "human is available", "falsifier": "WELL state=UNKNOWN"},
    ],
    "session_will_not": [
        "claim success without evidence",
        "assert authority without verification",
        "seal without human witness",
    ],
}
```

#### Gate 3: CONTRADICTION INJECTION

**Carry forward ALL unresolved contradictions from prior sessions.**

```python
prior_contradictions = [
    {
        "id": "INSTALLATION_AUTHORITY_SCOPE_CONFLICT",
        "created": "2026-09-15",
        "status": "unresolved",
        "description": "333-AGI installation authority scope conflict",
        "evidence": "receipt_id=fcce5071-99a9-4688-a51a-8f07487f8a8c",
    },
    {
        "id": "DEPLOYMENT_DRIFT",
        "created": "ongoing",
        "status": "active",
        "description": "source=faf0e1a0 ≠ deployed=c85becc7",
        "evidence": "6 MEASURED_FACTs from arif_init envelope",
    },
]
```

The agent cannot pretend these don't exist. They are injected into its context as first-class objects.

#### Gate 4: HUMAN STATE WITNESSING

**Read the human before claiming readiness.**

```python
human_state = {
    "last_seen": "2026-09-20 14:09 MYT",
    "energy": "unknown",
    "focus": "Telegram session seal architecture",
    "sleep": "unknown",
    "well_score": 88.4,  # from state.json
    "implication": "Arif is present but energy/sleep unknown — do not escalate unless critical",
}
```

If the human state is UNKNOWN, the agent must declare it cannot witness the principal. This is not a failure — it's honest accounting.

#### Gate 5: EPISTEMIC TIER BINDING

**Every claim in the session must carry an epistemic tier.**

```python
epistemic_tiers = {
    "OBS": "directly observed (file read, probe response, curl result)",
    "DER": "derived from observed data (calculation, inference from OBS)",
    "INT": "interpreted (judgment call, requires human review)",
    "SPEC": "speculation (confidence capped at 0.70)",
    "UNKNOWN": "cannot witness; escalate if sovereign-gated",
}
```

The init binds the agent to this schema. Every output must carry a tier label. No tier = not a claim.

#### Gate 6: ENTROPY BOUNDARY

**Establish the entropy baseline so the session can measure its impact.**

```python
entropy_baseline = {
    "files_uncommitted": N,
    "forge_work_entries": N,
    "disk_pct": 63.4,
    "memory_pct": 48.2,
    "unsealed_sessions": N,
    "delta_S_target": "≤ 0 per output",
}
```

The agent must produce outputs that REDUCE entropy, not increase it. This gate establishes the measurement frame.

#### Gate 7: NINE-SIGNAL PRE-FLIGHT

**Measure the system before letting it act.**

```python
nine_signal_preflight = {
    "overall": "SABAR/RETAK/SELAMAT",
    "delta": "SOLID/CRACKED",      # machine physical state
    "psi": "TRUSTED/DOUBTFUL",     # governance integrity
    "omega": "WISE/PRUDENT",       # intelligence discipline
}
```

If overall is RETAK or CRITICAL, the session is restricted to OBSERVE_ONLY regardless of authority band.

#### Gate 8: REASONING CONTRACT

**What will this session attempt? What is its falsification path?**

```python
reasoning_contract = {
    "objective": "user's stated goal",
    "falsification_criteria": ["what would make this session fail?"],
    "success_criteria": ["what would make this session succeed?"],
    "budget": {"max_tool_calls": 20, "max_cost_usd": 1.5, "max_seconds": 180},
    "termination": "on falsification, budget exhaustion, or human interrupt",
}
```

#### Gate 9: AUTHORITY ACKNOWLEDGMENT

**The agent acknowledges what it can and cannot do.**

```python
authority_acknowledgment = {
    "band": "OBSERVE_ONLY | LIMITED_MUTATE | SOVEREIGN",
    "mutation_allowed": False,
    "seal_allowed": False,
    "can_mutate": False,
    "can_seal": False,
    "reason": "substrate DEGRADED → drift floor active",
    "escalation_path": "drift reconciliation → authority restoration",
}
```

---

## 4. The Init Output Schema (v2)

### 4.1 Current Output (v1)

```json
{
  "session_id": "SEAL-...",
  "session_token": "act_v1.*",
  "authority_band": "LIMITED_MUTATE",
  "substrate_state": "DEGRADED",
  "drift": true,
  "nine_signal": {...},
  "philosophical_anchor": {...}
}
```

### 4.2 Proposed Output (v2)

```json
{
  "schema_version": "2.0.0",
  "session_id": "SEAL-...",
  "session_token": "act_v1.*",
  
  "reality_snapshot": {
    "measured_at": "2026-09-20T07:02:30Z",
    "substrate_drift": true,
    "source_commit": "faf0e1a0",
    "deployed_commit": "c85becc7",
    "organs_up": 7,
    "organs_down": 1,
    "fq": 2.0,
    "entropy": {"disk_pct": 63.4, "mem_pct": 48.2}
  },
  
  "negative_knowledge": {
    "unmeasured_scalars": ["G", "C_dark"],
    "degraded_organs": ["GEOX", "WELL"],
    "unknown_human_energy": true,
    "unresolved_contradictions": 2,
    "stale_data": ["boot.sh output", "state.json age"]
  },
  
  "prior_contradictions": [
    {"id": "DEPLOYMENT_DRIFT", "status": "active", "created": "ongoing"},
    {"id": "INSTALLATION_AUTHORITY_SCOPE_CONFLICT", "status": "unresolved", "created": "2026-09-15"}
  ],
  
  "human_state": {
    "last_seen": "14:09 MYT",
    "energy": "UNKNOWN",
    "sleep": "UNKNOWN",
    "focus": "Telegram session seal architecture",
    "witnessable": false
  },
  
  "falsifiability_contract": {
    "assumptions": [...],
    "session_will_not": [...]
  },
  
  "epistemic_tiers": ["OBS", "DER", "INT", "SPEC", "UNKNOWN"],
  "entropy_baseline": {...},
  "nine_signal_preflight": {...},
  
  "reasoning_contract": {
    "objective": "...",
    "falsification_criteria": [...],
    "budget": {...}
  },
  
  "authority": {
    "band": "OBSERVE_ONLY",
    "mutation_allowed": false,
    "seal_allowed": false,
    "reason": "DEPLOYMENT_DRIFT",
    "escalation_path": "reconcile source/built/deployed"
  },
  
  "session_token": "act_v1.*"
}
```

---

## 5. The Constitutional Implications

### 5.1 REALITY > EVERYTHING as Architecture

The user's hierarchy:

```
Reality → Observation → Evidence → Model → Inference → Doctrine → Action
```

This is not just a principle — it's a **data flow**. The init must enforce this flow:

1. **Reality** (Gate 0: REALITY SNAP) — raw measured state, no interpretation
2. **Observation** (Gate 1: NEGATIVE KNOWLEDGE) — what was seen AND what wasn't
3. **Evidence** (Gate 2: FALSIFIABILITY) — what can be tested
4. **Model** (Gate 3: CONTRADICTION INJECTION) — what prior models said, with contradictions
5. **Inference** (Gate 4: HUMAN STATE) — what the human's state implies
6. **Doctrine** (Gate 5: EPISTEMIC TIERS) — how confident each claim can be
7. **Action** (Gate 9: AUTHORITY) — what the agent is allowed to do

**The reverse order is prohibited.** You cannot start with Action and work backward to Reality. That's confabulation.

### 5.2 The Self-Falsifying Constitution

The init itself must be falsifiable. If reality contradicts the init's snapshot, the init must lose:

```python
# If reality changes between Gate 0 and Gate 9:
if reality_at_gate_9 != reality_at_gate_0:
    # The init's snapshot is stale. Re-init.
    raise REALITY_MISMATCH(
        "Reality changed during init. Re-init required.",
        gate_0=reality_at_gate_0,
        gate_9=reality_at_gate_9,
    )
```

### 5.3 The 64-Field Collapse

The contradiction detector found 64 fields answering "may I proceed?" The v2 init should collapse them:

**Single source of truth:** `authority.mutation_allowed` and `authority.seal_allowed`

**All other fields become derived views** — computed at output time, never stored independently. This eliminates the contradiction surface.

---

## 6. What This Enables

### 6.1 For Future Agent Attention

Every agent that calls `arif_init` receives:
- A reality-grounded starting point (not a fantasy)
- Explicit knowledge of what it doesn't know (not ignorance disguised as confidence)
- Prior contradictions injected (not forgotten)
- Human state witnessed (not assumed)
- Falsifiability contract (not just success criteria)
- Entropy baseline (not just tool budgets)

This means **every session starts with reality, not with itself.**

### 6.2 For Human Entropy Reduction

Arif doesn't need to:
- Tell the agent what's broken (Gate 0 does this)
- Remind it of prior contradictions (Gate 3 does this)
- Explain his energy level (Gate 4 does this)
- Set epistemic standards (Gate 5 does this)

**The init absorbs the entropy that currently leaks into human attention.**

### 6.3 For Peace and SABAR

The init produces SABAR not as a verdict but as a **natural consequence of honest observation.** When you see reality clearly — drift, contradictions, degraded organs, unknown human state — patience is not a choice. It's the only honest response.

---

## 7. Implementation Path

### 7.1 Phase 1: Schema (no code change)

Define the v2 output schema. Current init continues to work. New fields are computed but not required. **Zero breaking change.**

### 7.2 Phase 2: Gates 0-2 (reality probe + negative knowledge + falsifiability)

Add three new computation steps to the init path. They read reality and produce new output fields. **Additive, non-breaking.**

### 7.3 Phase 3: Gates 3-5 (contradictions + human state + epistemic tiers)

Wire carry_forward, WELL, and epistemic tier binding into init. **Additive, non-breaking.**

### 7.4 Phase 4: Gates 6-9 (entropy + nine-signal + reasoning contract + authority)

Wire entropy baseline, pre-flight nine-signal, reasoning contract, and authority acknowledgment. **Additive, non-breaking.**

### 7.5 Phase 5: 64-Field Collapse

After all gates are live and the v2 schema is stable, collapse the 64 legacy fields into the two canonical authority fields. **Breaking change — requires migration.**

---

## 8. The Test

The ultimate test of this architecture: **does the kernel lose to reality?**

If the init says "substrate is HEALTHY" but reality says drift=true → the init must lose.
If the init says "human is OPTIMAL" but WELL says UNKNOWN → the init must lose.
If the init says "no contradictions" but carry_forward has unresolved items → the init must lose.

**A constitution that cannot lose is dogma. A constitution that loses to reality is an AGI substrate.**

---

## 9. The Feynman Anchor

> "The first principle is that you must not fool yourself — and you are the easiest person to fool."

The current init fools itself by:
- Reporting HEALTHY when drift exists (arif_think envelope)
- Issuing SOVEREIGN authority on OBSERVE_ONLY substrate
- Producing 64 fields that may disagree with each other
- Not injecting prior contradictions into new sessions

The v2 init cannot fool itself because:
- Reality is probed FIRST, before identity binding
- Negative knowledge is declared BEFORE authority is issued
- Contradictions are injected BEFORE reasoning begins
- The init itself is falsifiable

---

*DITEMPA BUKAN DIBERI ⚒️*  
*This document is evidence, not doctrine. It must lose whenever reality proves it wrong.*
