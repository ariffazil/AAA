---
id: agentic-dream-engine
name: agi-dream-engine
autonomy_tier: T1
version: 2.0.0
description: "v2 HARDENED: 72h reasoning distillation producing structured DreamCandidates with four independent axes (p_occurrence, p_predictive, p_normative, consequence), counterstory generation, causal status, CHRON calibration bridge, and promotion lifecycle. Substrate consolidation via separate process. No self-witnessing."
owner: AAA
risk_tier: medium
knowledge_basis:
  language: true
  math: false
  physics: false
host_compatibility:
- claude-code
- codex
- opencode
- kimi
- kimi-code
dependencies:
  skills:
  - arifos-memory
  - arifos-mcp-federation
  - arifos-governance
  servers:
  - arifos-kernel
  - aforge
  tools:
  - arif_memory_recall
  - arif_seal
  - arif_judge
examples:
- Design the dream-state protocol for a new AAA warga agent.
- Map how OpenCode's auto-dream.ts should feed into arifOS L4 canon.
- Audit whether an agent's nightly consolidation respects F7 humility and F13 sovereign
  locks.
tests:
- Verify a warga agent's dream output lands in memory_records with actor_id, session_id,
  and source_ref.ratified_by.
- Confirm daily cap and threshold lock are enforced before any canon promotion.
version_lock:
  schema_version: '1'
  artifact_hash: pending
orthogonal_tags:
  trinitarian:
  - Ω
  functional:
  - Interface
  # 2026-09-17 P2-001: layer corrected to DESIGN until P0-002 (cross-warga read +
  # arif_judge gate) lands. SKILL.md spec is federated; runtime currently dreams solo.
  layer: DESIGN
  autonomy_tier: T2
floor_scope:
- F2
- F4
- F6
- F7
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# Agentic Dream Engine — Federation Memory Consolidation

## Overview

The Dream Engine is a **substrate process** — Python scripts scheduled by systemd — not an LLM loop. LLM enters ONLY for distillation (pattern extraction + counterstory generation).

**v1→v2 (2026-09-21):** Single p= confidence → four independent axes. Prose wisdom.md → structured DreamCandidate JSONL. No falsification → mandatory counterstories. No lifecycle → 11-state promotion chain.

**The definition:** Dream Engine = asynchronous evidence-consolidation, replay, falsification, calibration and bounded policy-learning subsystem for persistent agents.

### arifOS-ACT Embedding

Before using this skill on any mutating, irreversible, or high-blast-radius task:
1. **ART** — Attune (what is the real task?), Recognize (what class of power?), Test (fit · authority · evidence · blast · reversible).
2. **Kernel** — Route to arifOS for F1–F13 judgment if action class is Maker/Messenger/Mutator/Destroyer/Sovereign.
3. **ACT** — Apply narrow, Constrain scope, Trace witness, STOP before corruption.
4. **Receipt** — Leave evidence of what changed, why, and under whose authority.

### Architecture

```
EXPERIENCE → CANDIDATE → FALSIFICATION → PREDICTION → REALITY → CALIBRATION → GOVERNANCE
```

wisdom.md is NOT the destination. It is a temporary artifact in a larger learning chain.

No component may close its own epistemic loop. Dream Engine generates candidates. CHRON measures outcomes. arifOS governs promotion. A-FORGE executes bounded change.

## When to Use

- Designing memory consolidation for a new agent or organ.
- Wiring an agent's local "dream" output into federation canon.
- Auditing whether an agent's consolidation loop respects constitutional floors.
- Deciding cadence/threshold changes for an agent's dream cycle.

## When NOT to Use

- **Never** use this skill to let an agent raise its own synthesis threshold or daily cap. That is F13 territory.
- **Never** let an agent write directly to VAULT999 (L6) during a dream cycle. L6 seals require `arif_seal` with human ack or 888_JUDGE verdict.
- **Never** treat dream output as truth without counterfactual challenge and provenance.

## Core Doctrine

> The dream-engine is not a metaphor. It is a thermodynamic necessity for any agent whose substrate does not consolidate on its own. The cron is the price of statelessness. The LLM is the price of scale. The threshold is the price of sovereignty.

Extended corollary for multi-agent federation:

> Each agent has its own entropy pump, but all pumps drain into the same canonical reservoir. The reservoir has one lock: F13.

## The Four Independent Axes

frequency(pattern) ≠ probability(pattern is wise). An agent can consistently repeat a stupid behaviour.

| Axis | What it measures | How computed | Initially |
|------|-----------------|-------------|-----------|
| p_occurrence | How often did it appear? | session_count / total_sessions | Set from LLM |
| p_predictive | Does it predict outcomes? | CHRON calibration (Brier score) | null (untested) |
| p_normative | Does it govern behavior? | F13 ratification authority | null (no authority) |
| consequence | What if it's wrong? | cost_if_wrong × reversibility | Set from LLM |

Two candidates at p_occurrence=0.7 are NOT equivalent if one has blast_radius=CATASTROPHIC and the other LOW.

## DreamCandidate Lifecycle

```
OBSERVED → CANDIDATE → REPLAYED → PROSPECTIVE → REPLICATED → LESSON → POLICY_PROPOSAL → RATIFIED
    ↓                                                              ↓
  never promoted                                           SUPERSEDED / RETRACTED / DECAYED
```

State transitions require evidence at each gate. Only RATIFIED can influence system behavior.

Decay: not observed in 6 cycles (18 days) → RETRACT. A system that can learn but cannot forget becomes dogma.

## The Dream Candidate Pipeline

| Step | Script | What it does | LLM? |
|------|--------|-------------|------|
| 1. Extract | `engines/dream_engine.py` | Pull reasoning traces from state.db | No |
| 2. Distill | `engines/dream_engine.py` | LLM pattern extraction + counterstories | Yes |
| 3. Build | `engines/dream_engine.py` | Construct DreamCandidate objects | No |
| 4. Write | `engines/dream_engine.py` | JSONL + wisdom.md render | No |
| 5. CHRON bridge | `dream_engine/dream_chron_bridge.py` | Compute p_predictive from verified predictions | No |
| 6. Scar verification | `engines/dream_engine.py` | Count active scars, attach metadata | No |
| 7. Deliver | `engines/dream_engine.py` | Telegram AAA group summary | No |

## The Five Dream Functions (Eureka Insights)

| Function | Biology analog | Engineering analog | Current owner | Federation extension |
|----------|---------------|-------------------|---------------|----------------------|
| **Replay** | Hippocampal reactivation | Pull recent episodic memory | dream-engine stage1 | Each agent replays its own trajectory store |
| **Cluster** | Sharp-wave ripple binding | Cosine grouping | dream-engine stage2 | Agent-local + federation cross-agent cluster |
| **Synthesize** | Gist extraction | LLM compression to falsifiable statement | dream-engine stage3 | Per-agent + cross-warga synthesis |
| **Defend + Seal** | Counterfactual threat rehearsal | Counterfactual challenge before canon write | dream-engine stage4 + rehearse.py | Centralized via arifOS kernel |
| **Recombine** | Creative interleaving (Kekulé/Mendeleev) | Cross-organ graph walk | dream-engine recombine.py | Weekly cross-warga pattern detection |

### Cognitive vs Canonical Substrate Mapping

Two valid ways to talk about the 6-layer stack:

| Layer | Cognitive framing (intelligence ladder) | Canonical substrate framing (arifOS memory skill) |
|-------|----------------------------------------|---------------------------------------------------|
| L1 | Working context | Redis ephemeral |
| L2 | Short-term/episodic | Redis session / raw logs |
| L3 | Semantic/facts | Qdrant vector space |
| L4 | Procedural/skills | Postgres `memory_records` + `memory_store` |
| L5 | Constitutional/values | Graphiti/FalkorDB relational graph |
| L6 | Core identity/legacy | VAULT999 immutable ledger |

**Important:** The canonical substrate mapping is the source of truth for implementation. The cognitive framing is useful for reasoning about *what* each layer does, but code must use the substrate names (Redis, Qdrant, Postgres, Graphiti, VAULT999) to avoid deployment drift.

### Entropy Controller Clarification

`scripts# ARCHIVED: entropy_controller.py` computes five entropy **proxies** (P1–P5) and **proposes** cadence/threshold changes. It does **not** enforce a hard `ΔS < -ε` bound. The controller is an advisory instrument; the actual entropy reduction happens when low-signal singletons are excluded and clusters are compressed into canon. Any claim that the controller enforces a numeric epsilon should be treated as a documentation/interpretation error unless a future F13-ratified patch adds it.

### 1. Agent-local dream cycle

Every agent that dreams runs a loop:

```
REPLAY   → pull agent-local episodic buffer (24h)
CLUSTER  → group by semantic similarity
SYNTHESIZE → produce candidate canonical statements
PROPOSE  → emit tier_up_eligible candidates
```

Agents do **not** seal their own canon. They propose.

### 2. Constitutional seal gate

Proposals are collected by the **arifOS dream-engine coordinator** (the existing nightly cron, extended). It:

1. Validates the agent's identity and lease.
2. Checks the global daily cap across all agents.
3. Runs counterfactual challenge (`rehearse.py`).
4. Writes to `memory_records` + `memory_audit_log` with:
   - `actor_id = <agent>:<dream-cycle>`
   - `source_ref.ratified_by = arif-fazil`
   - `source_ref.ratified_floors` = `[F7_threshold, F8_reversibility, F11_auth, F13_cap]`

### 3. Cross-warga recombination

Weekly, the federation recombiner reads L5 (Graphiti/FalkorDB) for entities shared across warga agents and proposes cross-agent patterns. These also route through the seal gate.

## Mapping to OpenCode

OpenCode already has `auto-dream.ts` (`# ARCHIVED: auto-dream.ts (mimocode never built)`) which consolidates project memory every 7 days and auto-distills every 30 days.

| OpenCode concept | Federation mapping | Gap |
|------------------|-------------------|-----|
| `AUTO_DREAM_TITLE` session | Local replay + cluster + synthesis | Not yet writing to arifOS L4 |
| `AUTO_DISTILL_TITLE` session | Pattern packaging into skills | Should produce canon candidates, not just skills |
| `Config.dream.interval_days` | Agent-local cadence | Must also respect federation global cadence/cap |

**Recommended wiring:** OpenCode's dream cycle should emit a `dream_proposal.jsonl` to a known federation inbox (`/var/spool/arifos/dream-proposals/opencode/` or Supabase staging table). The nightly coordinator ingests it.

## Mapping to OpenClaw — Sleep-Time Manager Daemon

OpenClaw is the AGI gateway; its dream cycle is a **sleep-time compute daemon** that metabolizes idle hours.

### Prototype Architecture

| Stage | Function | Reversibility Mechanism |
|-------|----------|------------------------|
| **1. State Monitor** | Detect idle (`t_idle > 120 min` or scheduled nightly window); acquire L1 mutex | Suspends immediately on 888 activity |
| **2. L2 Ingress & Entropy Sorting** | Pull raw L2 traces; cluster semantically; drop noise | Read-only on primary stores |
| **3. Offline EMD Metabolizer** | Gist extraction + anticipatory reasoning trees | Output stays in shadow partition |
| **4. Shadow Commit & Seal** | Write compressed gist to `L3_shadow`; cryptographic hash; morning briefing handshake | Single-command purge or merge |

### Key Design Rules

- **F1:** Never write directly to primary `L3`/`L4` during an unsupervised cycle. Always shadow-first.
- **F2:** Morning briefing presents shadow content; merge to primary only after validation.
- **F9:** Logs use mechanical language only ("metabolize", "compress", "shadow commit"), never "I dreamed".
- **Trigger:** Use **Option A (chronological nightly cron)** for the prototype to establish baseline cadence.

### Trigger Options

| Option | Mechanism | Pros | Cons | Recommendation |
|--------|-----------|------|------|----------------|
| **A — Chronological** | Fixed nightly window (e.g., 03:00 MYT) | Predictable cost; guaranteed morning briefing | Wasted compute on light days; may clash with late sessions | **Prototype** |
| **B — Saturation** | Trigger when L2 token/complexity threshold crossed | Compute-efficient; dreams only when material exists | Unpredictable timing; may miss briefings | Phase 2 |

Prototype files: see `/root/AAA/skills/AGI-dream-engine/prototype/`.

## Mapping to AAA Warga

| Warga | Dream content | Output |
|-------|--------------|--------|
| **333-AGI** | Code forge receipts, plan DAGs, test results | Engineering canon |
| **555-ASI** | Memory synthesis, ethical critiques, cross-agent patterns | Memory + dignity canon |
| **888-APEX** | Verdict patterns, floor violations, seal chains | Governance canon |
| **A-AUDIT** | Anomaly patterns, drift signals | Audit canon |
| **A-ARCHIVE** | Vault chain topology, seal topology | Archive canon |

## Constitutional Gates Checklist

| Floor | Requirement | Current Status |
|-------|-------------|----------------|
| F1 AMANAH | Proposals only; no agent self-seals. Rollback = `DELETE FROM memory_records WHERE actor_id = '<agent>:<cycle>'`. **Add pre-seal snapshot of `memory_records` + `memory_audit_log` state so hallucinated L3/L4 writes can be reverted cleanly.** | Partial — additive writes exist, but snapshot rollback is missing |
| F2 TRUTH | Every canonical statement is falsifiable and carries a counterfactual. **Add explicit tri-witness cross-check before seal (human/AI/earth or second-agent verifier).** | Partial — counterfactual is generated, but no independent witness validates offline replay |
| F4 CLARITY | One candidate = one cluster = one proposition. No noise promotion. | Aligned |
| F7 HUMILITY | `synthesis_score ≥ 0.65` is F13-locked; no agent overrides. | Aligned |
| F8 LAW | Agent boundaries enforced via arifOS lease + A2A auth. | Aligned for Hermes; gaps for OpenCode/OpenClaw/warga |
| F9 ANTIHANTU | Logs are process descriptions, never "I dreamed". | Aligned |
| F11 AUTH | Every write has `actor_id`, `session_id`, and `memory_audit_log` row. | Aligned |
| F13 SOVEREIGN | Threshold, daily cap, and cadence changes require Arif's explicit ratification. | Aligned |

### Gap Register (post-assessment merge)

| ID | Gap | Severity | Owner | 888_HOLD gate |
|----|-----|----------|-------|---------------|
| G1 | No pre-seal L3/L4 snapshot for clean rollback | High | dream-engine | Before Phase 0 execution |
| G2 | Offline replay lacks independent F2 witness before seal | Medium | dream-engine stage4 | Before Phase 1 federation inbox |
| G3 | OpenCode auto-dream does not write to federation canon | High | OpenCode / AAA | Phase 1 ratification |
| G4 | OpenClaw and AAA warga have no dream cycle | High | AAA / OpenClaw | Phase 2 design |
| G5 | `entropy_controller.py` computes proxies but does **not** enforce a hard ΔS < -ε | Clarification | dream-engine | Document, do not change without F13 |
| G6 | arifOS + WEALTH degraded; global recombine unsafe | Blocker | ops | Phase 0 repair |

## Four-Phase Eureka Engineering Path

**Current verified state:** Stages 1-4 run nightly at 04:00 MYT, entropy is reducing, and Vault999 seals are locking. arifOS and WEALTH systemd services are `active`, though MCP organ attestation flags them DEGRADED (probe issue).

**Pivot:** Phase 2 counterfactual rehearsal is the real unbuilt learning engine. Phase 1/3 speculative vectors (Letta sleep-time compute, RL weight updates) are dropped per F2 evidence.

### Phase 0 — F1 Snapshot + Schema Drift Fix (Week 1)

**Goal:** Make cross-organ consolidation safe before expanding scope.

**Deliverables:**
1. Restore arifOS and WEALTH to healthy attestation (or fix the MCP health probe).
2. Fix `consolidate.py` Supabase drift: it queries `arifosmcp_memory_records.id` which does not exist; align with `memory_records.memory_id`.
3. Fix `entropy_controller.py` R6 vault read error: `'str' object has no attribute 'get'`.
4. Add pre-seal snapshot of `memory_records` + `memory_audit_log` state for rollback.
5. Add independent F2 witness step before seal.

**888_HOLD gate:** Arif clears kernel stability + snapshot policy.

### Phase 1 — Phase 2 Counterfactual Rehearsal (Weeks 2–3)

**Goal:** Implement the real learning engine: weekly stress-testing of sealed rules.

**Deliverables:**
1. `stage5_rehearse.py` — weekly random sample of 10-20% of recent sealed rules.
2. Counterfactual challenge per rule.
3. Tri-witness governance check (F1/F2/F4).
4. Survival → additive metadata (`stress_tested: true`).
5. Fracture → 888_HOLD alert in `alerts.jsonl`, never auto-amend.
6. Systemd timer: `arif-dream-phase2.timer` (Sunday 02:00 MYT).

**888_HOLD gate:** Deployment of systemd timer + weekly rehearsal policy.

### Phase 2 — Federation Inbox + OpenCode Wiring (Weeks 4–5)

**Goal:** Let OpenCode's existing auto-dream feed arifOS canon.

**Deliverables:**
1. `dream_proposals` staging table in Supabase (or filesystem spool).
2. OpenCode `auto-dream.ts` extended to emit `dream_proposal.jsonl`.
3. Existing dream-engine coordinator ingests the inbox nightly, after Phase 0 snapshot.

**888_HOLD gate:** Schema + global cap policy ratification.

### Phase 3 — Cross-Warga Recombination (Weeks 6–10)

**Goal:** Federation discovers cross-agent patterns no single agent sees.

**Deliverables:**
1. Weekly cross-warga graph walks on L5 (FalkorDB).
2. "Improve the improver" R6 meta-rule extended per agent.
3. No unsupervised L4/L5 modifications — all proposals route through 888_HOLD.

**888_HOLD gate:** Any cross-agent policy change.

## Output Format

```
## Skill Result: agentic-dream-engine

### Summary
One-paragraph summary of the federation dream design.

### Evidence
- Current dream-engine path: /root/AAA/dream_engine/ (runs via `arif-dream.timer`)
- OpenCode auto-dream: # ARCHIVED: auto-dream.ts (mimocode never built)
- Memory schema: /root/arifOS/arifosmcp/migrations/001_memory_schema.sql

### Recommendations
- Implement Phase 1 inbox for OpenCode.
- Extend entropy controller with per-agent proxies.

### Escalations
- F13 ratification needed for threshold/cap/cadence changes.
```

## Pitfalls

- **frequency ≠ wisdom:** p_occurrence is session frequency, not epistemic confidence. A pattern appearing in 8/8 sessions can have p_predictive=0.2 when tested against outcomes. Never treat the occurrence score as validation.
- **Path drift:** wisdom.md has existed at two paths (`/root/AAA/dream-engine/wisdom.md` and `/root/AAA/knowledge-graph/dream-engine/wisdom.md`). Always stat the file before claiming its date. The canonical output is `knowledge-graph/dream-engine/`; the old path is now a symlink.
- **CHRON domain gap:** CHRON predictions are domain-specific (currently XAUUSD trading). Dream candidates about technical/governance patterns get p_predictive=null because no matching predictions exist. The bridge reports the gap honestly — null means 'untested', not 'absent'.
- **Compression drift:** MDL pressure makes abstractions smaller, but reality has exceptions. Every candidate carries `scope_boundary` (where it does NOT hold) to prevent premature universalization.
- **Self-certification is forbidden:** Dream Engine may generate candidates. Dream Engine may not certify candidates. Kamoi 2024: self-correction unreliable without external feedback.

## References

- Schema: `/root/AAA/dream_engine/specs/dream_candidate.schema.json`
- Literature: `/root/AAA/dream_engine/FOUNDATIONS.md` (12 mandatory anchors)
- Design: `/root/AAA/dream_engine/DESIGN.md`
- CHRON bridge: `/root/AAA/dream_engine/dream_chron_bridge.py`
- Memory architecture: `/root/AAA/governance/FEDERATION_MEMORY_ALIGNMENT_DOCTRINE.md`
- Canonical engine skill: `/root/AAA/dream_engine/SKILL.md`

---

*Forged: 2026-06-16 by FORGE (000Ω) — DITEMPA BUKAN DIBERI*