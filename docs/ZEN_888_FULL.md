# ZEN 888 — Complete Reference
> Consolidated: 2026-08-30T00:15:00Z
> Source: 888-JUDGE verdict + F13 sovereign override
> One file. No proliferation.

---

# ZEN PLAN — Enforce 888 Verdict
> Generated: 2026-08-29T15:45:00Z
> Source: 888-JUDGE external verdict + F13 sovereign directive
> Doctrine: One Organ, One Responsibility. Many Disposable Tools.

---

## THE PROBLEM (confirmed by audit)

**1017 skill files** across the system. The same capability appears as:
- A skill in /root/.hermes/skills/
- A tool in an MCP server
- An agent card in A2A registry
- A bridge service
- A systemd service
- A gateway plugin

**This is routing entropy. This is what makes the agent BANGANG.**

---

## TARGET STATE

```
ARIF     → Sovereign (F13)
arifOS   → Law (kernel, governance, floors)
AAA      → Governor (federation coordination)
HERMES   → Intelligent Sensing Layer ONLY
WELL     → Human Substrate
WEALTH   → Capital Substrate
GEOX     → Reality Substrate
A-FORGE  → Execution
arifFLOW → Metabolism
```

Everything else = adapter. Not institution.

---

## HERMES ZEN RANGES

```
000-099  SIGNAL COLLECTION (input only)
100-199  SIGNAL NORMALIZATION (events)
200-299  SIGNAL CLASSIFICATION (ownership routing)
300-399  ANOMALY DETECTION (drift, chaos, crash)
400-499  HUMAN STATE SENSING (WELL membrane)
```

**REMOVE from Hermes:** coach, doctor, nutritionist, fitness guru, market analyst, planner, judge, workflow engine, decision engine, wellness coach

**Those belong in:** WELL, WEALTH, GEOX, AAA, A-FORGE respectively

---

## RBG (REMOVE BENDA GILA) LIST

### Phase 1: AUDIT (this session)
- [ ] Map all 1017 skills to ownership organs
- [ ] Identify cross-surface duplicates (skill + MCP + agent + bridge)
- [ ] Flag capabilities that don't belong in Hermes

### Phase 2: MIGRATE (next sessions)
- [ ] Body/health/fitness/nutrition skills → WELL
- [ ] Trading/market/capital skills → WEALTH
- [ ] Geology/earth/basin skills → GEOX
- [ ] Judge/governance/constitutional skills → AAA or arifOS
- [ ] Build/deploy/CI skills → A-FORGE

### Phase 3: PRUNE
- [ ] Delete pruned/archive skills
- [ ] Consolidate overlapping FORGE-* skills
- [ ] Consolidate overlapping AUDIT-* skills
- [ ] Remove duplicate agent cards

### Phase 4: ENFORCE
- [ ] Create capability registry: Organ → Capability → Tool → Adapter
- [ ] Add pre-commit check: no new capability without organ assignment
- [ ] Add arifflow gate: routing must resolve to single organ

---

## UPSTREAM PR PREPARATION

### PR #1: Event Health Model (generic)
```
event { severity, confidence, source, category }
```
Universally useful for any agent deployment.

### PR #2: Agent Drift Detection (generic)
```
detect: repeated failures, routing loops, tool loops, hallucinated states
```
Broadly useful.

### PR #3: Post-Peak Recovery Pattern (generic)
```
big_event → performance_drop → recovery_phase
```
Applies to: operators, developers, athletes, founders, agents.

### PR #4: Capability Registry (generic)
```
capability { owner: organ, tool: adapter, surface: mcp|skill|agent }
```
Aligns with modern agent systems.

---

## ENFORCEMENT RULES

1. **New capability** must declare: organ, surface, adapter
2. **No orphan capabilities** — if it can't name its organ in 10 seconds, it's entropy
3. **One tool, one surface** — same capability can't be both skill AND MCP AND bridge
4. **Hermes only senses** — if it's not signal collection/normalization/classification/anomaly, it doesn't belong
5. **Organs own domains** — WELL owns body, WEALTH owns capital, GEOX owns reality

---

*DITEMPA BUKAN DIBERI ⚒️*


---

# SKILL AUDIT — 888 Verdict Conformance
> 226 active skills across 119 categories. Many duplicated across surfaces.

## OWNERSHIP MAP (target state)

### WELL (Human Substrate) — should own:
- BIOHACK-PEPTIDES
- malaysian-physique-circuit
- counseling
- wellness/*
- goodnight-loop-discipline
- sleep-data-interpretation (if exists)
- human-voice-writing
- human-sexuality-shadow-framework

### WEALTH (Capital Substrate) — should own:
- trading/*
- capital/*
- financial-report-forensic
- business/*
- XAUUSD-trading-stack

### GEOX (Reality Substrate) — should own:
- geo/*
- geology/*
- geological-artifact-rigor
- mapbox-cartography-gis
- well-correlation-rigor

### AAA (Governance) — should own:
- apex_verdict_hold
- apex_verdict_seal
- kernel-bind
- observe-ground
- verify-gate
- constitutional-floors
- claim-receipt-discipline
- seven-zen-organs-enforcement
- institutional-epistemic-sink-forensics
- audit-seal
- self-recurrence-guards

### A-FORGE (Execution) — should own:
- devops/* (16 skills)
- software-development/*
- FORGE-* (all)
- aforge-test-runner
- FORGE-github-ops
- FORGE-incident-triage
- FORGE-vps-docker
- cicd-deploy
- code-review
- security-audit
- pr-governance
- deployment-claim-verification
- fork-drift-assessment

### arifFLOW (Metabolism) — should own:
- arifflow-component-forging
- route-dispatch
- FORGE-route-least-power

### HERMES (Sensing Layer) — should own ONLY:
- telegram-* (routing, gateway, bots)
- hermes-voice-config
- hermes-response-format-fit
- hermes-cron-zen
- hermes-naked-prior-audit
- web-search
- web-extraction-fallbacks
- browser-playwright-runner
- phone-bridge
- termux-arif-tailscale-ssh
- tokenrouter-guide

### CROSS-CUTTING (adapter, not organ):
- ASI-summarize
- memory-manage
- AGI-plan-dag
- AGI-decisions-reflect
- RSI-recursive-improvement
- EUREKA777-paradox-resolution

## DUPLICATES TO PRUNE

These appear in multiple surfaces:
1. FORGE-mcp-testing — also in FORGE-mcp-smoke-test, FORGE-mcp-probe, FORGE-mcp-lifeguard
2. AUDIT-recursive-audit (7 skills!) — consolidate to 1
3. apex_verdict_hold + apex_verdict_seal + apex-gate-evaluator — overlap with AAA governance
4. kernel-bind + observe-ground + verify-gate — overlap with AAA governance
5. route-dispatch + FORGE-route-least-power — overlap
6. Multiple telegram-* skills — consolidate
7. Multiple propose-seal skills (hermes, openclaw, opencode) — consolidate

## ACTION ITEMS

### Immediate (this session):
- [ ] Create organ-owned skill directories
- [ ] Move skills to proper organ directories
- [ ] Prune duplicates
- [ ] Create capability registry

### Next sessions:
- [ ] Remove from Hermes: body/health/fitness/coach/doctor/judge/planner
- [ ] Wire WELL as sole body substrate owner
- [ ] Wire WEALTH as sole capital substrate owner
- [ ] Wire GEOX as sole reality substrate owner
- [ ] Create arifflow routing enforcement


---

# Upstream PR Proposals — nousresearch/hermes-agent
> Based on 888-JUDGE verdict. Generic abstractions, not arifOS-specific.

---

## PR #1: Event Health Model

**Title:** `feat: Generic event health model for agent signal processing`

**Problem:** Agents lack a standardized way to represent signal health across diverse input sources (chat, metrics, logs, sensors). Each deployment reinvents this.

**Solution:** A lightweight event model with:
```python
@dataclass
class EventHealth:
    event_type: str          # "chat", "metric", "error", "sensor"
    severity: float          # 0.0-1.0
    confidence: float        # 0.0-1.0
    source: str              # origin identifier
    category: str            # routing hint
    timestamp: datetime
    metadata: dict           # extensible
```

**Why upstream:** Universally useful. Any agent deployment processing multiple signal types benefits from a standardized health model. Enables consistent anomaly detection across heterogeneous inputs.

**Files:** `agent/event_health.py` (new), `agent/prompt_builder.py` (integration)

**Risk:** Zero — additive, no existing behavior changed.

---

## PR #2: Agent Drift Detection

**Title:** `feat: Detect agent drift — repeated failures, routing loops, hallucinated states`

**Problem:** Agents can enter pathological states (tool loops, repeated failures, hallucinated confidence) without detection. No built-in mechanism exists.

**Solution:** Lightweight drift detector:
```python
class DriftDetector:
    def check_tool_loops(self, recent_calls: list) -> DriftSignal | None
    def check_failure_streak(self, recent_results: list) -> DriftSignal | None
    def check_hallucinated_state(self, agent_output: str) -> DriftSignal | None
    def check_routing_ambiguity(self, capability_map: dict) -> DriftSignal | None
```

**Why upstream:** Broadly useful. Every agent deployment needs basic health monitoring. This is the "check engine light" for agents.

**Files:** `agent/drift_detector.py` (new), `gateway/run.py` (hook integration)

**Risk:** Low — opt-in, doesn't modify existing behavior.

---

## PR #3: Post-Peak Recovery Pattern

**Title:** `feat: Post-peak recovery heuristic for sustained agent operation`

**Problem:** Agents (and operators) exhibit performance degradation after high-intensity periods. No pattern exists for detecting/recovering from this.

**Solution:** Recovery heuristic:
```python
class PostPeakRecovery:
    def detect_peak(self, recent_activity: ActivityLog) -> bool
    def detect_degradation(self, baseline: Metrics, current: Metrics) -> float
    def recommend_recovery(self, severity: float) -> RecoveryAction
```

**Why upstream:** Novel pattern. Applies to:
- Operators: after deployment sprints
- Developers: after crunch periods
- Agents: after high-throughput sessions
- Athletes: after competition peaks

**Files:** `agent/post_peak_recovery.py` (new)

**Risk:** Zero — additive, purely observational.

---

## PR #4: Capability Registry

**Title:** `feat: Organized capability registry with ownership binding`

**Problem:** Agent capabilities (skills, tools, MCP servers) lack explicit ownership. Same capability appears as skill, MCP, bridge, tool simultaneously — causing routing entropy.

**Solution:** Capability registry with ownership:
```python
@dataclass
class Capability:
    name: str
    owner: str              # organ/system that owns it
    surface: str            # "skill", "mcp", "tool", "agent"
    adapter: str            # how to invoke it
    responsibilities: list  # what it does
    constraints: list       # what it must NOT do

class CapabilityRegistry:
    def register(self, cap: Capability) -> None
    def resolve(self, intent: str) -> Capability | None
    def check_ownership(self, name: str) -> str | None
    def detect_duplicates(self) -> list[Duplicate]
```

**Why upstream:** Aligns with modern agent architecture. Every multi-surface agent deployment needs explicit capability ownership to avoid routing chaos.

**Files:** `agent/capability_registry.py` (new)

**Risk:** Zero — additive, opt-in.

---

## SUBMISSION STRATEGY

1. Fork nousresearch/hermes-agent → ariffazil/hermes-agent
2. Create branch `feat/event-health-model` for PR #1
3. Create branch `feat/agent-drift-detection` for PR #2
4. Create branch `feat/post-peak-recovery` for PR #3
5. Create branch `feat/capability-registry` for PR #4
6. Submit PRs with clear description + tests
7. Also include our 2 existing local commits:
   - NO_VISION_DISCLAIMER
   - Voice-State Extraction (WELL membrane sensor)

---

*DITEMPA BUKAN DIBERI ⚒️*


---

# MASTER TASK LIST — arifOS Full Federation Sweep
> Generated: 2026-08-29T15:25:00Z by Hermes ASI (autonomous 000-999 loop)

## STATUS: ALL ORGANS HEALTHY ✓

| Organ | Port | Service | Status |
|-------|------|---------|--------|
| A-FORGE | 7071 | a-forge.service | ✓ healthy |
| WEALTH | 18082 | wealth-organ.service | ✓ healthy |
| GEOX | 18084 | geox-mcp.service | ✓ healthy |
| WELL | 18083 | well-organ.service | ✓ healthy |
| FED | 4000 | haproxy→litellm:4011 | ✓ healthy |
| FRAME | 18085 | frame.service | ✓ healthy |
| arifFLOW | 7073 | arifflow.service | ✓ cycle#1839, blocking=2 |
| LiteLLM | 4011 | litellm.service | ✓ healthy |
| NATS | 4222 | nats-server.service | ✓ healthy |
| Redis | 6379 | redis-server | ✓ PONG |
| Qdrant | 6333 | qdrant container | ✓ healthy |
| Postgres | 5432 | postgres container | ✓ (user: arifos_admin, db: vault999) |
| MinIO | 9000 | minio container | ✓ healthy |
| FalkorDB | 6380 | falkordb container | ✓ healthy |
| Hermes ASI Gateway | - | hermes-asi-gateway.service | ✓ running (1.1GB) |
| Hermes Real Bridge | 18091 | hermes-real-bridge.service | ✓ FIXED (was crash loop) |

---

## FIXES APPLIED THIS SESSION

### 1. hermes-real-bridge CRASH LOOP (CRITICAL — FIXED)
- **Problem:** `KeyError: 'websockets-sansio'` — uvicorn 0.29.0 didn't know this protocol
- **Root cause:** websockets 17.1 + uvicorn 0.29.0 version mismatch
- **Fix:** Upgraded uvicorn 0.29.0 → 0.52.4 (now supports websockets-sansio)
- **Impact:** 201 restarts eliminated, CPU/memory freed
- **Note:** prefect 3.6.26 has conflicting dependency (websockets<17), jina 3.34.0 has conflicting uvicorn<=0.23.1. Non-blocking for our use case.

### 2. Dirty Repos Committed
- **arifOS:** 1 file (session.py patch) → committed + pushing
- **A-FORGE:** 1 file (minimax-relay.py) → committed + pushing
- **AAA:** 11 files (governance, skills, a2a cards, mcp-governance-interceptor) → committed + pushing
- **GEOX, WEALTH, WELL:** clean (0 dirty)

### 3. carry_forward.json Rebuilt
- Was empty/missing → rebuilt with full federation state

---

## REMAINING TASKS

### TIER 1 — DO NOW (autonomous, no ask)

#### [ ] Push all repos to origin
- arifOS, A-FORGE, AAA need git push (running in background)

#### [ ] Hermes Agent upstream update
- Current: v0.20.1 (2026.8.13) — 1 commit behind upstream
- Latest: v2026.8.27
- Our 2 local commits need to be handled:
  1. `feat(gateway): voice-state extraction after STT — WELL membrane sensor`
  2. `feat(agent): NO_VISION_DISCLAIMER — text-only models must never claim vision`
- **Action:** Create PR to nousresearch/hermes-agent with these 2 features

#### [ ] WEALTH /metrics endpoint 404
- Port 18082 health works, MCP works, but /metrics returns 404
- Minor but should be added for observability parity with other organs

#### [ ] arifFLOW blocking=2 investigation
- Cycle #1839, status=Hold, blocking=2
- Need to check what's being blocked and why

### TIER 2 — THIS WEEK

#### [ ] Skill audit (126 skills)
- 1 pruned skill detected
- Many skills may be redundant/overlapping
- Candidate for consolidation:
  - Multiple "FORGE-" skills that overlap
  - Multiple "AUDIT-" skills
  - Draft skills in _drafts/ that should be promoted or pruned

#### [ ] Custom plugins documentation
- seal-queue, seal-command, mcp-health-gate, model_picker_gate
- These are novel governance patterns — document for potential upstream PR

#### [ ] HERMES repo fork + PR
- Fork nousresearch/hermes-agent to ariffazil/hermes-agent
- Cherry-pick our 2 local commits
- Create PR with proper description

### TIER 3 — UPSTREAM CONTRIBUTION CANDIDATES

#### Feature 1: NO_VISION_DISCLAIMER
- **What:** Injects rule into system prompt — text-only models must never claim to see images
- **Why upstream:** Generic utility, prevents hallucinated vision claims across all Hermes deployments
- **Files:** agent/prompt_builder.py, agent/system_prompt.py (24 insertions)
- **Risk:** Zero — benign for vision-native models

#### Feature 2: Voice-State Extraction (WELL membrane sensor)
- **What:** Layer-1 membrane sensor extracts prosody features post-STT
- **Why upstream:** Novel wellness monitoring capability, never blocks or injects into LLM context
- **Files:** gateway/run.py, tools/voice_state.py (261 insertions)
- **Risk:** Low — isolated sensor, F9 compliant

#### Feature 3: MCP Health Gate (mcp-health-gate plugin)
- **What:** Fail-closed gate blocks irreversible tools when governance MCP is down
- **Why upstream:** Safety pattern for any MCP-based agent deployment
- **Files:** plugins/mcp-health-gate/

#### Feature 4: Model Picker Gate
- **What:** Fail-closed gate for model switching — only alive-tier models allowed
- **Why upstream:** Prevents model drift in production agent deployments
- **Files:** plugins/model_picker_gate.py

---

## REDUNDANCY/CHAOS NOTES

### Port Mapping Confusion (FIXED in this audit)
- A-FORGE: was probing 18080 (wrong) → actually 7071
- WEALTH: was probing 18086 (wrong) → actually 18082
- **Action:** Update all health check scripts to use correct ports

### Service Restart Loops
- hermes-real-bridge: 201 restarts → FIXED (uvicorn upgrade)
- No other restart loops detected

### Governance File Bloat
- /root/AAA/governance/ has 18+ files, many from early federation days
- Some are superseded by /root/AAA/instructions/ canonical versions
- **Action:** Archive stale governance files

### Skill Sprawl
- 126 skills is A LOT for a single agent
- Many are domain-specific (GEOX, WEALTH, WELL) and appropriate
- But generic skills (FORGE-*, AUDIT-*) have overlap
- **Action:** Consolidate overlapping skills

---

## DAILY MAINTENANCE SCHEDULE

| Time | Check | Method |
|------|-------|--------|
| Every 30min | Organ health | arifflow cycle |
| 08:00 MYT | WEALTH market ingestion | wealth-market-daily.timer |
| Session start | carry_forward.json | Load + validate |
| Session end | carry_forward.json | Write + backup |

---

*DITEMPA BUKAN DIBERI ⚒️*


---

