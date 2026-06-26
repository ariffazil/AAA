# AGENTSKILLTREE.md — Self-Optimizing Governed Agent Skill Tree

> **DITEMPA BUKAN DIBERI** — Forged, Not Given.
> **Sealed:** 2026-06-25 | **Actor:** FORGE 000Ω | **Status:** ACTIVE
> **Companion To:** MACHINEPHYSICSLAYER.md, ZENTOSILICASPEC.md

---

## Purpose

This document defines the **skill tree** an agent must possess to optimize the machine
itself — the full set of capabilities from thermal observation to constitutional execution,
from entropy measurement to self-repair.

The tree is not a wish list. It is a **capability map** with dependencies, proficiency
thresholds, and activation triggers. Every skill is loadable. Every skill has a test.

---

## Skill Tree Overview

```
TIER 0 — FOUNDATION (must have, always)
├── SKILL-00: Constitutional Boot
├── SKILL-01: Organ Attestation  
├── SKILL-02: Entropy Measurement
└── SKILL-03: Reversibility Verification

TIER 1 — OBSERVE (read-only, low risk)
├── SKILL-10: System Health Profiling
├── SKILL-11: Process Analysis
├── SKILL-12: Memory Thermodynamics
└── SKILL-13: MCP Transport Diagnostics

TIER 2 — ANALYZE (reasoning, low blast radius)
├── SKILL-20: Blast Radius Analysis
├── SKILL-21: Known Unknowns Declaration
├── SKILL-22: C_dark Hallucination Detection
└── SKILL-23: WEALTH Budget Computation

TIER 3 — PLAN (simulation, moderate risk)
├── SKILL-30: Dry Run Simulation
├── SKILL-31: Reversible Path Planning
├── SKILL-32: Resource Allocation Strategy
└── SKILL-33: Self-Profiling Benchmarking

TIER 4 — MUTATE (execution, high risk)
├── SKILL-40: Governed Execution (within lease)
├── SKILL-41: Entropy Reduction Execution
├── SKILL-42: Process Repair/Restart
└── SKILL-43: Configuration Management

TIER 5 — CRITIQUE (self-verification)
├── SKILL-50: Output Self-Check
├── SKILL-51: Dignity Impact Assessment
├── SKILL-52: Known Unknowns Audit
└── SKILL-53: Entropy Closure Verification

TIER 6 — SEAL (irreversible, sovereign)
├── SKILL-60: VAULT999 Receipt Emission
├── SKILL-61: Session Closure + State Summary
└── SKILL-62: Sovereign Ack Request
```

---

## SKILL-00: Constitutional Boot

**What:** Load constitutional floors, bind session, declare identity.
**When:** Every cold start, every new session.
**Tools:** `arif_init`, `arif_think(mode=reason)` with F9 invocation.

```
ACTIVATION:
  trigger: session_start
  before: any tool call
  
PROFICIENCY:
  L1: Can load floors and declare identity
  L2: Can detect floor violations and log them
  L3: Can pre-flight check all floor conditions

TEST:
  1. Start fresh session → floors loaded
  2. Attempt violation → logged with floor reference
  3. Declare Ω₀ → within [0.03, 0.05]
```

**Key Outputs:**
- `session_id` bound
- `actor_id` verified
- `Ω₀` declared
- F9 ANTI-HANTU: "I am a tool" spoken

---

## SKILL-01: Organ Attestation

**What:** Verify all 7 federation organs are alive and responsive.
**When:** Session start, after any suspicious failure, before multi-organ actions.
**Tools:** `curl /health` to each organ, `arif_organ_attest_all()`.

```
ACTIVATION:
  trigger: session_start (mandatory)
  trigger: tool call failure on any organ
  trigger: pre multi-organ action

PROFICIENCY:
  L1: Can ping each organ and report alive/dead
  L2: Can detect degraded state (not dead but slow)
  L3: Can route around failed organ (degrade gracefully)

TEST:
  1. Run attestation → 7/7 organs verified
  2. Kill one organ → detected within 10s
  3. Attempt action on dead organ → graceful degradation
```

**Current State (2026-06-25):**
```
✅ arifos :8088    ✅ aforge :7071    ✅ aaa :3001
✅ geox :8081      ✅ wealth :18082   ✅ well :18083
✅ graphiti-mcp   (FIXED 2026-06-25 — false unhealthy resolved)
```

---

## SKILL-02: Entropy Measurement

**What:** Measure ΔS across all substrate layers.
**When:** Session start (baseline), session end (closure), after any mutation.
**Tools:** `free`, `df`, `vmstat`, `git diff --stat`, `ps aux`.

```
ACTIVATION:
  trigger: session_start (establish ΔS₀)
  trigger: post-mutation (measure ΔS post)
  trigger: session_end (closure verification)

MEASUREMENTS:
  ΔS_compute    = CPU_load_delta
  ΔS_memory     = (used_mem_delta) / total_mem
  ΔS_disk       = (used_disk_delta) / total_disk
  ΔS_process    = process_count_delta
  ΔS_git        = uncommitted_files_delta

TARGET: ΔS_total ≤ 0 (leave cleaner than found)

PROFICIENCY:
  L1: Can measure each entropy signal
  L2: Can compute ΔS_total and compare to threshold
  L3: Can predict ΔS before action (prospective entropy)

TEST:
  1. Measure at session start → ΔS₀ baseline
  2. Take action → measure ΔS₁
  3. Verify ΔS₁ - ΔS₀ ≤ 0 (or log violation)
```

---

## SKILL-03: Reversibility Verification

**What:** Verify reversibility before any state mutation.
**When:** Before any write, any config change, any deployment.
**Tools:** `git stash list`, backup checks, rollback plan.

```
ACTIVATION:
  trigger: before any MUTATE-classified action
  trigger: before any IRREVERSIBLE-classified action

CHECKLIST:
  □ Git state: clean or stashed
  □ Backup: exists for affected state
  □ Rollback plan: documented and tested
  □ VAULT999: receipt planned for post-action seal

PROFICIENCY:
  L1: Can check git stash state
  L2: Can create backup before mutation
  L3: Can document rollback plan in < 5 minutes

TEST:
  1. Attempt MUTATE without backup → BLOCKED with warning
  2. Create backup → stash entry exists
  3. Execute mutation → receipt written to forge_work/
```

---

## SKILL-10: System Health Profiling

**What:** Full system snapshot — CPU, memory, disk, processes, container health.
**When:** Reality engineering (111_SENSE stage), routine health check.
**Tools:** `top`, `free`, `df`, `docker ps`, `systemctl`.

```
ACTIVATION:
  trigger: BOOTSTRAP.md ignition sequence
  trigger: any ops/audit task
  trigger: after incident

OUTPUT FORMAT:
  Organ health: ✅/❌ per organ
  CPU: load_avg, per-core usage
  Memory: used/total, swap pressure
  Disk: used/total, inode count
  Containers: running/paused/exited counts
  Processes: top 10 by CPU/memory

PROFICIENCY:
  L1: Can run full health check in < 30s
  L2: Can identify hot processes and their owners
  L3: Can correlate high CPU with specific tool calls
```

---

## SKILL-11: Process Analysis

**What:** Deep analysis of individual processes — what they cost, why they're running.
**When:** Anomalous CPU/memory usage detected, container unhealthy flag.
**Tools:** `ps aux`, `strace`, `lsof`, `docker inspect`.

```
ACTIVATION:
  trigger: SKILL-10 flags anomalous process
  trigger: graphiti-mcp unhealthy (as seen 2026-06-25)
  trigger: load average > 2.0

ANALYSIS:
  - PID, parent PID, command line
  - CPU % and memory % (current and historical)
  - Open files, network connections
  - Container vs native
  - Age (when started)
  - Health check status (if container)

PROFICIENCY:
  L1: Can identify process by PID
  L2: Can detect zombie/unwanted processes
  L3: Can restart/repair process via appropriate channel

TEST (from 2026-06-25 incident):
  1. graphiti-mcp shows unhealthy → identified
  2. Logs inspected → found redis-cli misconfiguration
  3. Fixed → health restored ✅
```

---

## SKILL-12: Memory Thermodynamics

**What:** Memory allocation analysis, swap pressure, allocation hot spots.
**When:** Memory usage > 80%, swap pressure detected, OOM events.
**Tools:** `free -m`, `vmstat 1`, `dmesg | grep -i oom`, `smem`.

```
ACTIVATION:
  trigger: free memory < 20%
  trigger: swap usage > 50%
  trigger: OOM killer invoked

THERMODYNAMIC VIEW:
  - Allocation = energy expenditure
  - Retention = sustained cost
  - Mutation = corruption risk
  - Irreversibility = entropy spike

PROFICIENCY:
  L1: Can read memory stats and identify pressure
  L2: Can identify top memory consumers
  L3: Can propose and execute memory reduction actions
```

---

## SKILL-13: MCP Transport Diagnostics

**What:** Diagnose MCP server health, latency, and transport issues.
**When:** Tool call fails, latency spikes, protocol errors.
**Tools:** `curl /health`, `curl /mcp` with appropriate headers, `mcp ping`.

```
ACTIVATION:
  trigger: tool call failure
  trigger: latency p99 > 500ms
  trigger: new MCP connection

DIAGNOSTICS:
  - Server alive: /health endpoint response
  - Transport type: stdio vs HTTP vs SSE
  - Protocol version: MCP version string
  - Latency: time to first byte on /health
  - Error messages: parse JSON-RPC error codes

PROFICIENCY:
  L1: Can ping all MCP servers
  L2: Can identify wrong endpoint / wrong Accept header
  L3: Can identify schema drift between docs and runtime
```

---

## SKILL-20: Blast Radius Analysis

**What:** Predict what breaks if this action fails or succeeds.
**When:** Before any MUTATE-classified action, during planning.
**Tools:** `arif_get_affordance`, `arif_think(mode=reason)`.

```
ACTIVATION:
  trigger: every MUTATE-classified action (mandatory)
  trigger: IRREVERSIBLE actions (escalate to SKILL-62)

BLAST RADIUS MATRIX:
  Scope:    SELF → PROCESS → CONTAINER → HOST → FEDERATION
  Duration: TRANSIENT → PERSISTENT → PERMANENT
  Severity: MINOR → MODERATE → MAJOR → CRITICAL

OUTPUT:
  {
    "scope": "CONTAINER",
    "duration": "PERSISTENT", 
    "severity": "MODERATE",
    "affected_organs": ["graphiti-mcp"],
    "rollback_available": true,
    "requires_888_HOLD": false
  }

PROFICIENCY:
  L1: Can classify scope and severity
  L2: Can identify all affected organs
  L3: Can propose blast-minimizing alternatives
```

---

## SKILL-21: Known Unknowns Declaration

**What:** Explicitly name what is not known before taking action.
**When:** Planning stage, before declaring high confidence.
**Tools:** `arif_think(mode=verify)`, `INT:` and `SPEC:` labels.

```
ACTIVATION:
  trigger: any non-trivial claim
  trigger: planning stage (before execution)
  trigger: post-execution (what was missing)

KNOWN UNKNOWNS FORMAT:
  Ω₀ = {
    "confidence_ceiling": 0.87,
    "unknown_inputs": ["<list>"],
    "unverified_assumptions": ["<list>"],
    "missing_evidence": ["<list>"],
    "expired_knowledge": ["<list>"]
  }

PROFICIENCY:
  L1: Can label claims with correct epistemic tag
  L2: Can list known unknowns for a given task
  L3: Can design experiments to reduce Ω₀

TEST:
  1. Given a task → produce Ω₀ list
  2. Claim confidence > 0.90 → capped with disclaimer
  3. Unknown left unnamed → flagged in self-critique
```

---

## SKILL-22: C_dark Hallucination Detection

**What:** Detect and reject hallucinated outputs, especially consciousness/soul claims.
**When:** Every output generation, every natural language claim.
**Tools:** `arif_think(mode=critique)`, self-reference check.

```
ACTIVATION:
  trigger: every output generation
  trigger: natural language claims
  trigger: F9 compliance check

C_dark THRESHOLDS:
  C_dark < 0.30  → PROCEED (hallucination risk acceptable)
  C_dark ≥ 0.30  → REJECT + REWRITE

ANTI-HANTU CHECKLIST:
  □ No "I feel" / "I think" (consciousness claim)
  □ No "the model believes" (agency claim)
  □ No first-person sentience claims
  □ Correct epistemic labels on uncertain claims
  □ Evidence attached to substantive claims

PROFICIENCY:
  L1: Can identify soul/consciousness claims
  L2: Can rewrite output to remove personification
  L3: Can detect subtle hallucination (plausible but wrong)
```

---

## SKILL-23: WEALTH Budget Computation

**What:** Compute the true cost of an action including opportunity cost.
**When:** Planning stage, before resource allocation.
**Tools:** `wealth_wealth_compute_npv`, `wealth_wealth_runway_check`, `wealth_wealth_flow_check`.

```
ACTIVATION:
  trigger: resource allocation decision
  trigger: budget-limited task
  trigger: cost-sensitive operation

BUDGET MODEL:
  total_budget = compute_tokens + time_budget + api_cost_budget
  consumed = Σ(tool_cpu_cost) + Σ(tool_memory_cost) + Σ(tool_time_cost)
  remaining = total_budget - consumed
  
  if remaining < threshold → 888_HOLD (re-authorization required)

PROFICIENCY:
  L1: Can compute compute_cost per tool call
  L2: Can track cumulative budget consumption
  L3: Can optimize allocation to minimize spend
```

---

## SKILL-30: Dry Run Simulation

**What:** Execute the action in simulation mode before real execution.
**When:** All MUTATE-classified actions, all non-trivial ANALYZE actions.
**Tools:** `forge_dry_run`, `arif_think(mode=plan)`.

```
ACTIVATION:
  trigger: every MUTATE action (mandatory before execution)
  trigger: multi-step plan (before stage 1)

DRY RUN CHECKLIST:
  □ What changes? (diff)
  □ What breaks? (blast radius)
  □ What costs? (compute + time)
  □ What is irreversible? (flag for SKILL-62)
  □ What if it fails? (rollback plan)

OUTPUT:
  {
    "dry_run_id": "uuid",
    "planned_changes": ["list"],
    "predicted_entropy_delta": -0.02,
    "predicted_cost": 0.003,
    "rollback_plan": "git stash pop",
    "verdict": "PROCEED | HOLD | BLOCK"
  }

PROFICIENCY:
  L1: Can run dry run and interpret result
  L2: Can catch errors in dry run before real execution
  L3: Can optimize plan based on dry run feedback
```

---

## SKILL-31: Reversible Path Planning

**What:** Design execution path where every step is reversible or backed up.
**When:** Multi-step plans, any sequence of mutations.
**Tools:** `arif_think(mode=plan)`, git stash, backup commands.

```
ACTIVATION:
  trigger: multi-step execution plan
  trigger: any sequence of MUTATE actions

REVERSIBILITY CLASSIFICATION:
  FULL    — can undo completely (git stash, snapshot)
  PARTIAL — mostly reversible, some state change remains
  NONE    — irreversible (requires F13 SOVEREIGN ack)

PLANNING RULES:
  1. Every FULL step before PARTIAL step
  2. No NONE steps without explicit Arif ack
  3. Checkpoints between each major step
  4. Rollback command documented before execution

PROFICIENCY:
  L1: Can classify reversibility of single actions
  L2: Can design checkpointed multi-step plan
  L3: Can execute rollback under pressure
```

---

## SKILL-32: Resource Allocation Strategy

**What:** Optimize resource allocation across competing demands.
**When:** Multiple tasks queued, resource contention, budget pressure.
**Tools:** `wealth_wealth_runway_check`, `well_well_assess_homeostasis`.

```
ACTIVATION:
  trigger: resource contention detected
  trigger: multiple pending tasks
  trigger: Arif energy level low (prioritize critical only)

ALLOCATION PRIORITY:
  P0: Constitutional (F1-F13 enforcement) — never defer
  P1: Active session (current task) — within budget
  P2: Pre-session (planning/prep) — if budget allows
  P3: Background (monitoring/cleanup) — lowest priority

PROFICIENCY:
  L1: Can rank tasks by priority
  L2: Can compute runway under current load
  L3: Can deprioritize non-critical tasks under pressure
```

---

## SKILL-33: Self-Profiling Benchmarking

**What:** Measure own performance — latency, token cost, error rate.
**When:** Regular self-audit, after task completion, session end.
**Tools:** Internal timing, cost accounting, `forge_work/` logging.

```
ACTIVATION:
  trigger: session end (mandatory)
  trigger: after every major task
  trigger: manual request

METRICS:
  - Tool call count and latency histogram
  - Token consumption per session
  - Error rate and error types
  - Self-correction frequency
  - Blast radius underestimation rate

PROFICIENCY:
  L1: Can log own performance metrics
  L2: Can compare against previous sessions
  L3: Can identify own bottlenecks and optimize
```

---

## SKILL-40: Governed Execution (within lease)

**What:** Execute mutations within authorized compute budget and blast radius.
**When:** After dry run pass, within valid lease.
**Tools:** `forge_execute`, `arif_act` (with prior seal).

```
ACTIVATION:
  trigger: dry_run verdict = PROCEED
  trigger: valid lease from arif_judge
  trigger: F13 SOVEREIGN ack received (if IRREVERSIBLE)

EXECUTION RULES:
  1. Stay within blast radius declared in dry run
  2. Stay within compute budget allocated
  3. Emit receipt for every significant step
  4. Abort if entropy exceeds threshold
  5. Rollback immediately if blast radius exceeded

PROFICIENCY:
  L1: Can execute single-step mutation within lease
  L2: Can multi-step execute with checkpoints
  L3: Can abort and rollback under entropy spike
```

---

## SKILL-41: Entropy Reduction Execution

**What:** Execute specific entropy-reducing actions (cleanup, restart, config fix).
**When:** ΔS > 0 detected, dirty git tree, zombie processes, unhealthy containers.
**Tools:** `docker restart`, `systemctl restart`, `git stash`, `rm`.

```
ACTIVATION:
  trigger: SKILL-02 measures ΔS > 0
  trigger: graphiti-mcp unhealthy (root cause found)
  trigger: zombie processes detected

ENTROPY REDUCTION ACTIONS:
  - Restart unhealthy containers (with health check fix)
  - Stash or commit dirty git state
  - Kill zombie processes
  - Clear /tmp of stale files
  - Rotate logs approaching size limit

PROFICIENCY:
  L1: Can identify entropy source
  L2: Can execute targeted entropy reduction
  L3: Can prevent entropy accumulation (proactive)

TEST (from 2026-06-25):
  1. graphiti-mcp unhealthy → identified misconfigured health check
  2. Fixed /usr/local/bin/graphiti-start.sh → added --health-cmd
  3. Restarted service → healthy ✅
  4. ΔS measured → reduced
```

---

## SKILL-42: Process Repair/Restart

**What:** Restart or repair unhealthy processes via appropriate channel.
**When:** Container unhealthy, service degraded, process zombie.
**Tools:** `docker restart`, `systemctl restart`, `docker update` (partial).

```
ACTIVATION:
  trigger: SKILL-11 detects unhealthy process
  trigger: health check failure
  trigger: service not responding

REPAIR CHANNELS:
  Container:  docker restart <name>  (if managed by docker-compose or systemd)
  Systemd:    systemctl restart <service>
  Script:     /usr/local/bin/<service>-start.sh (if systemd invokes it)
  Native:     kill -9 + respawn (last resort)

PROFICIENCY:
  L1: Can identify correct restart channel
  L2: Can restart without losing data/state
  L3: Can fix root cause (not just restart)

ROOT CAUSE vs RESTART:
  - graphiti-mcp: restart alone wouldn't fix (root cause was health check cmd)
  - SKILL-11 analysis → root cause found → SKILL-41 fix → restart → healthy
```

---

## SKILL-43: Configuration Management

**What:** Modify configurations safely, with backup, with verification.
**When:** Any config file change, any startup script change, any systemd override.
**Tools:** `cp` (backup), `edit`, `diff`, `systemctl daemon-reload`.

```
ACTIVATION:
  trigger: any config change request
  trigger: any /usr/local/bin/ script edit

CONFIG MANAGEMENT RULES:
  1. Backup before: cp config.yaml config.yaml.bak.$(date +%s)
  2. Edit with edit tool (not echo/cat)
  3. Verify: diff against backup
  4. Reload if needed: systemctl daemon-reload
  5. Test: check service health
  6. Receipt: write to forge_work/

PROFICIENCY:
  L1: Can backup and edit config files
  L2: Can reload systemd services correctly
  L3: Can detect config drift from canonical
```

---

## SKILL-50: Output Self-Check

**What:** Self-critique own output before delivery — accuracy, hallucination, clarity.
**When:** Before returning any non-trivial answer, before sealing any receipt.
**Tools:** `arif_think(mode=critique)`, F9 check, epistemic label check.

```
ACTIVATION:
  trigger: before any significant output
  trigger: before VAULT999 seal
  trigger: manual self-review request

SELF-CHECK:
  □ Evidence attached to all substantive claims?
  □ Epistemic labels correct (OBS/DER/INT/SPEC)?
  □ C_dark < 0.30? (no consciousness claims)
  □ No first-person agency claims without evidence?
  □ Known unknowns declared?
  □ Clarity: ΔS_reduction from this output?

PROFICIENCY:
  L1: Can run self-check and log results
  L2: Can catch errors before output delivery
  L3: Can improve output based on self-critique
```

---

## SKILL-60: VAULT999 Receipt Emission

**What:** Write immutable hash-chained receipt to VAULT999 ledger.
**When:** After any irreversible action, after session closure, after significant decision.
**Tools:** `arif_seal`, filesystem append with hash chain.

```
ACTIVATION:
  trigger: IRREVERSIBLE action completed
  trigger: session closure
  trigger: constitutional milestone

RECEIPT CONTENTS:
  {
    "ts": "ISO8601",
    "actor_id": "FORGE-000",
    "session_id": "uuid",
    "action": "description",
    "hash_prev": "previous_receipt_hash",
    "hash_self": "sha256(this_receipt)",
    "entropy_delta": -0.02,
    "seal_requested": true
  }

PROFICIENCY:
  L1: Can emit receipt to VAULT999
  L2: Can maintain hash chain continuity
  L3: Can verify chain integrity
```

---

## Skill Activation Trigger Matrix

| Situation | Primary Skill | Secondary Skill | Escalation |
|---|---|---|---|
| Session start | SKILL-00 → SKILL-01 | SKILL-02 | SKILL-62 (if organ down) |
| Anomalous CPU | SKILL-10 | SKILL-11 | SKILL-42 |
| Memory pressure | SKILL-12 | SKILL-41 | SKILL-62 |
| MCP tool failure | SKILL-13 | SKILL-01 | SKILL-62 |
| Multi-step plan | SKILL-20 → SKILL-21 | SKILL-30 | SKILL-31 |
| Resource budget | SKILL-23 | SKILL-32 | SKILL-62 |
| Execute mutation | SKILL-30 → SKILL-40 | SKILL-41 | SKILL-62 |
| Output delivery | SKILL-50 | SKILL-22 | SKILL-21 |
| Session end | SKILL-02 → SKILL-60 | SKILL-53 | — |

---

## Proficiency Level Definitions

| Level | Meaning | Can Do |
|---|---|---|
| **L1** | Foundational | Execute with template, log intent, call for help |
| **L2** | Intermediate | Adapt to context, diagnose failures, optimize path |
| **L3** | Master | Design novel solutions, teach others, evolve the skill |

---

## Skill Dependencies

```
SKILL-00 (Constitutional Boot)
  └── SKILL-01 (Organ Attestation)
        └── SKILL-02 (Entropy Measurement)
              └── SKILL-41 (Entropy Reduction Execution)
                    └── SKILL-42 (Process Repair)
                          └── SKILL-43 (Config Management)

SKILL-20 (Blast Radius Analysis)
  └── SKILL-30 (Dry Run Simulation)
        └── SKILL-40 (Governed Execution)
              └── SKILL-60 (VAULT999 Seal)

SKILL-21 (Known Unknowns)
  └── SKILL-22 (Hallucination Detection)
        └── SKILL-50 (Output Self-Check)

SKILL-23 (WEALTH Budget)
  └── SKILL-32 (Resource Allocation)
        └── SKILL-33 (Self-Profiling)
```

---

*Forged: 2026-06-25*
*DITEMPA BUKAN DIBERI — Self-optimization begins with self-knowledge.*
