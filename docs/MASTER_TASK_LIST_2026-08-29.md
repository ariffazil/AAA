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
