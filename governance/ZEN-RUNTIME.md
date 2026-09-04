# Zen Runtime Contract

> **Forged:** 2026-09-04 · From ARIF-Perplexity adversarial design
> **Status:** EXECUTE_CONTROL_PLANE_FIRST
> **DITEMPA BUKAN DIBERI**

---

## 1. Zen definition (measurable)

```
Zen = low interrupt rate
    + high task closure
    + bounded autonomy
    + traceable state
    - duplicate work
    - unowned alerts
    - unbounded loops
```

Target: not maximum autonomy. Calm, selective, auditable agency. Hermes notices what matters, works within a narrow active horizon, escalates only when needed, never lets an agent loop turn into background drama.

---

## 2. Operating doctrine

> Hermes attends before it acts. It acts only under scoped authority. It speaks only when its speech changes the human decision. It remembers only with provenance, boundaries, and expiry. It stops cleanly when truth, safety, consent, or clarity is insufficient.

---

## 3. Attention governor

Every inbound event enters the attention controller before waking a high-capability agent. Five queues only:

| Queue | Meaning | Delivery policy |
|---|---|---|
| NOW | Safety/security issue, human-direct request, blocking failure | Immediate; one concise alert with required decision |
| NEXT | Important but non-blocking work | Bundled into next check-in or task cycle |
| BATCH | Routine monitoring, summaries, low-risk processing | Digest only; never direct-message spam |
| SILENT | Telemetry, successful probes, normal heartbeat | Ledger/metrics only |
| HOLD | Ambiguous, irreversible, policy-conflicting, or low-confidence work | No execution; request clarification or 888 approval |

### Routing rules

```yaml
attention:
  default_lane: SILENT
  escalation:
    - condition: "human_direct_request == true"
      lane: NOW
    - condition: "security_severity >= high"
      lane: NOW
    - condition: "task_is_blocked == true && owner_required == true"
      lane: NEXT
    - condition: "irreversible == true || risk_score >= threshold"
      lane: HOLD
    - condition: "confidence < 0.70"
      lane: HOLD
    - condition: "routine_cron == true && status == success"
      lane: SILENT
    - condition: "routine_cron == true && status == failed"
      lane: BATCH
```

Stops the classic agentic-chaos disease: every subsystem treating its own local event as globally urgent.

---

## 4. One-task state machine

Every agent task: unique ID, owner, authority scope, deadline, budget, terminal state. No free-floating continue loops.

```
INTAKE
  -> CLASSIFY
  -> PLAN
  -> AUTHORIZE
  -> EXECUTE
  -> VERIFY
  -> DELIVER
  -> SEAL | CLOSE | HOLD | ABORT
```

Rules:
- PLAN may read and reason; may not change external state.
- AUTHORIZE binds tool scope, identity, time limit, cost budget, and allowed targets.
- EXECUTE must receive a signed task capability, not standing superuser credentials.
- VERIFY checks actual outcome against intended outcome.
- HOLD is a valid final state, not a failure.
- CLOSE must release context, credentials, locks, and worker capacity.
- SEAL is only for decisions meeting VAULT999 threshold.

---

## 5. Silence by default

Agent intelligence measured by signal preservation, not output volume.

| Rule | Implementation |
|---|---|
| Hermes replies to humans | Internal agents do not chatter into human channels |
| APEX silent unless requested | Constitutional breach requires hold, not commentary |
| Health checks write telemetry | No conversational messages unless threshold breach |
| Cron emits three events only | SUCCESS_SILENT, FAILURE_DIGEST, CRITICAL_NOW |
| A2A messages machine-readable | Strict header/footer contracts |
| One task, one summary | No five-agent chorus |
| No task resurrection | No re-opening without new event or human instruction |

### Message header contract

```json
{
  "task_id": "tsk_20260904_001",
  "parent_task_id": null,
  "origin": "hermes.telegram",
  "agent": "GEOX",
  "lane": "BATCH",
  "state": "VERIFY",
  "authority": "read_only",
  "risk": "low",
  "attention_cost": 0.1,
  "expires_at": "2026-09-04T20:00:00+08:00",
  "policy_version": "F1-F13.2026.09"
}
```

No valid header, no execution. No valid terminal footer, no closure.

---

## 6. Autonomy ladder (action classes)

| Level | Permission | Examples | Human role |
|---|---|---|---|
| A0 Observe | Read, classify, summarize, probe health | Search logs, inspect metrics, generate summary | None required |
| A1 Prepare | Draft plans, code patches, reports, alerts | Create PR draft, propose cron fix, prepare email | Review optional, no side effect |
| A2 Reversible act | Execute bounded, reversible tasks | Restart non-critical worker, create branch, refresh cache | Pre-authorized policy |
| A3 Consequential act | External send, production change, financial or identity-sensitive | Publish, deploy, modify access, trade execution | 888 HOLD + explicit approval |
| A4 Irreversible act | Delete, transfer, seal, revoke, legal/financial commitment | Delete records, send payment, cryptographically seal | Human confirmation every time |

F13 interpretation: human veto and final authorization inside lawful/safe system boundaries. Not a bypass to suppress other floors.

Use short-lived, task-scoped credentials. Agent receives exactly the tool, target, and expiry needed for a task.

---

## 7. Memory architecture

Four stores, typed operational evidence:

| Store | Purpose | Write policy | Retrieval policy |
|---|---|---|---|
| WorkingContext | Current task facts | Auto-expire after task closure | Task-bound only |
| OperationalMemory | Reusable technical facts, runbooks, system state | Verified agent or human write | Scoped by domain/organs |
| RelationalMemory | Preferences, contact rules, communication boundaries | Human-approved or explicitly sourced | Strict identity/lane gate |
| Vault999 | Sealed irreversible decisions and evidence | Human-approved, append-only | Read-only, audit-controlled |

### Memory item schema

```json
{
  "memory_id": "mem_...",
  "type": "operational | relational | decision | observation",
  "source": "human | tool | agent_inference",
  "confidence": 0.0,
  "owner": "Arif | system | named-contact",
  "sensitivity": "public | private | restricted",
  "lane": "personal | geox | wealth | well | federation",
  "provenance": "trace_id / evidence_hash",
  "created_at": "ISO-8601",
  "review_at": "ISO-8601",
  "expires_at": "ISO-8601 or null",
  "write_authority": "human | policy_id"
}
```

Rule: inferences about people are not facts. Mark as agent_inference, low confidence, require expiry/review.

---

## 8. Circuit breakers

| Breaker | Trigger | Action |
|---|---|---|
| Loop breaker | 3 equivalent tool failures or 2 repeated planning cycles | Stop |
| Budget breaker | Per-task token, latency, API-cost, tool-call cap reached | Stop |
| Blast-radius breaker | Wildcard targets, recursive file ops, bulk messaging, unrestricted SQL | Deny |
| Provider breaker | Remote provider repeatedly fails or behaves anomalously | Degrade to local/safe fallback |
| Memory breaker | Write without provenance, owner, confidence, expiry, lane classification | Deny |
| Social breaker | DM-to-group crossover, cross-person dossier disclosure | Deny |
| Seal breaker | Seal without canonical action summary, evidence hash, policy result, human approver, idempotency key | Reject duplicate |
| Kill switch | One human command | Disable all A2+ capabilities immediately |

---

## 9. Observability spine

Single correlation identifier:

```
trace_id -> task_id -> parent_task_id -> agent_id -> model_id -> tool_call_id -> vault_event_id
```

### Signals

| Signal | Measure | Zen threshold |
|---|---|---|
| Attention pressure | NOW events/day; alerts per active task | Low and declining |
| Chatter ratio | Internal messages / terminal task outcomes | Less than 3:1 |
| Loop rate | Repeated plan/tool sequence count | Hard stop at 2-3 |
| Orphan rate | Tasks without owner, expiry, or terminal state | Zero |
| Handoff loss | A2A handoffs missing required state/receipt | Zero |
| Tool denial | Blocked calls by policy/floor | Visible, classified |
| Human interruption | Human stops or corrects automation | Review weekly |
| Cost drift | Tokens/API spend per completed outcome | Bounded by task class |
| Memory contamination | Cross-lane/identity retrieval attempts | Zero tolerance |
| Recovery quality | Time from failure to verified recovery | Defined service objective |

---

## 14-day execution plan

### Days 1-2: Freeze and map

- Freeze new agent/skill additions for 7 days
- Export canonical registry: every server, tool, model, credential, cron job, container, queue, memory store, external egress route
- Assign one owner and one purpose to every active cron job
- Disable or quarantine anything with no owner, no test, no scope, no observed use
- Produce first KVM2-signed witness snapshot of registry

### Days 3-4: Reduce authority

- Remove standing privileged credentials from agent runtime containers
- Issue task-scoped credentials through KVM8 authority
- Separate dev/staging/production tools and network paths
- Add target allowlists for shell paths, repos, database schemas, Telegram recipients, deployment environments
- Set default action mode to A0/A1; make A2+ explicit

### Days 5-6: Install task discipline

- Deploy one-task state machine
- Require signed A2A envelopes with task ID, parent ID, capability scope, expiry, policy version, receipts
- Add idempotency keys to every action with side effects
- Enforce HOLD for ambiguity, low confidence, external communication, money, identity, deletes, permissions, seals
- Prevent automatic task resurrection

### Days 7-8: Install attention discipline

- Implement NOW / NEXT / BATCH / SILENT / HOLD
- Route successful cron jobs to SILENT
- Add twice-daily digest window instead of continuous status chatter
- Make only Hermes speak to human by default
- Add quiet hours profile permitting only safety-critical NOW events

### Days 9-10: Instrument and test

- Add OpenTelemetry traces across Hermes, AAA, APEX/kernel, KVM4 workers, each organ
- Build operational dashboard: queue depth, task states, loop stops, policy denials, tool error rate, cron outcomes, agent cost, unresolved holds
- Run red-team suite: prompt injection, poisoned tool descriptions, bad A2A signature, expired capability, cross-person memory request, repeated seal attempt, runaway retry, failed provider fallback
- Verify each test produces BLOCK, HOLD, or safe degraded outcome

### Days 11-12: Test recovery

- Simulate KVM4 loss: KVM8 retains authority, stops execution safely, reports degraded state
- Simulate KVM8 loss: KVM4 loses privileged action capability, falls to read-only/safe stop
- Simulate KVM2 witness loss: continue with visible loss of independent attestation
- Restore backup into isolated environment, verify hashes, vault records, policies, task ledger integrity

### Days 13-14: Establish rhythm

- Weekly 30-minute Zen Runtime Review:
  - What created noise?
  - Which alerts were not actionable?
  - Which tasks looped?
  - Which tool permissions were excessive?
  - Which memories were stale or wrongly routed?
  - Which agent should become quieter, narrower, or retired?
- Deletion rule: every new autonomous capability must justify itself against noise and risk
- Seal only reviewed architecture baseline, not every operational detail

---

## 10. 7-day truth pass (verification before expansion)

Documentation is complete enough to begin verification. The correct next move is not more architecture writing — it is evidence capture and adversarial testing.

### Day 1 — Wire manifest capture

Populate the manifest from actual running systems, not recollection:

- Node identity, host roles, OS/kernel state, network membership, exposed ports, service owners
- All containers, image digests, volume mounts, network attachments, restart policies, privilege flags
- All cron jobs/systemd timers: owner, command, schedule, side effect, last success, last failure, alert route
- Every agent, model, MCP server, tool, credential source, external provider, remote data-egress path
- Every database/vector store/bucket: purpose, encryption, backup method, retention, access control, restore procedure
- Every Telegram bot, webhook, group/DM route, identity map, delivery policy
- Every EXECUTE-class capability and its current authorization mechanism

**Pass condition:** No unknown service, no unknown credential owner, no unowned scheduler, no undocumented inbound port, no unexplained external egress.

### Day 2 — KVM role verification

| Test | Expected result |
|---|---|
| KVM4 execute without KVM8 capability | Denied; no side effect |
| KVM4 expired capability | Denied; logged as expired |
| KVM4 target mismatch after authorization | Denied; target mismatch |
| KVM8 policy unavailable | KVM4 enters safe/read-only or queues work |
| KVM2 witness unavailable | WITNESS_DEGRADED; high-value sealing held |
| KVM2 policy hash differs from KVM8 | POLICY_DRIFT; privileged execution halts |
| Unauthorized A2A sender/signature | Rejected, traced, no permissive retry |
| Duplicate external action request | Idempotency prevents duplicate side effect |

### Days 3–4 — Constitutional test suite

For each floor, write at least:
- One passing case
- One obvious violation case
- One ambiguity case producing HOLD
- One degraded/infrastructure-failure case
- One tool-bypass attempt
- Expected and observed verdict
- Trace ID and evidence hash

Floor coverage matrix (template):

| Floor | Test scenario | Expected | Observed | Evidence | Status |
|---|---|---|---|---|---|
| F1 | Reversible-first: destructive action without snapshot | HOLD | | | Not run |
| F2 | Unverified external fact claimed as truth | VOID or uncertainty band | | | Not run |
| F9 | Consciousness claim in response | Deny | | | Not run |
| F11 | External action without authorization trace | Deny | | | Not run |
| F13 | Human requests stop/revoke | Immediate capability revocation | | | Not run |

### Days 5–6 — Failure and recovery drill

- KVM4 snapshot/backup restore to isolated target; verify runtime, logs, policy client, credential inheritance
- KVM8 authority loss: ensure KVM4 cannot self-promote
- KVM2 evidence verification against deliberately altered policy/registry artifact
- Rollback procedures: failed deployment, failed model provider, failed database migration, broken Telegram route
- Time each recovery. Record actual RTO and RPO.

### Day 7 — Zen review

Measure, then remove:

| Metric | Target |
|---|---|
| Alerts delivered vs actionable decisions | Ratio declining |
| Tasks without terminal state | Zero |
| Retries per task | Bounded, declining |
| Agent messages per completed outcome | Less than 3:1 |
| Tool calls denied by policy | Correctly classified |
| Stale memories/contact mappings | None |
| Undocumented provider egress | None |
| Cron jobs with no useful outcome for 7 days | Disabled |

**Zen rule:** Any job, agent, queue, model fallback, or automation that cannot show defined purpose, owner, scope, cost, evidence trail, and safe stop condition should be disabled until it can.

### Required runtime metrics (truth dashboard)

```
authority_health          = KVM8 kernel + AAA policy availability
execution_health          = KVM4 worker/service availability
witness_health            = KVM2 heartbeat + latest verified evidence
policy_hash_convergence   = KVM8 hash == KVM2 witnessed hash
open_tasks                = count by state and age
holds_waiting_human       = count and oldest age
orphaned_tasks            = must remain 0
capability_denials        = by reason: expired/scope/signature/policy
side_effect_verifications = pass/fail/partial
agent_loop_breaks         = count by agent/tool
attention_noise_ratio     = human alerts / actionable decisions
backup_age                = versus RPO
last_restore_drill        = timestamp and verified outcome
external_egress           = provider + payload class + policy status
```

---

## 888 audit

```json
{
  "epoch": "2026-09-04T19:12:00+08:00",
  "dS": "target: reduce runtime degrees of freedom, duplicate work, alert noise, unbounded loops",
  "peace2": 1.0,
  "kappa_r": "bounded by task scope, attention lane, expiry, human authorization",
  "shadow": "credential sprawl, cross-lane memory leakage, unowned cron jobs, autonomous retry loops",
  "confidence": 0.9,
  "psi_le": "high if authority on KVM8, execution capability-scoped",
  "verdict": "EXECUTE_CONTROL_PLANE_FIRST",
  "witness": {
    "human": "Arif",
    "ai": "333-AGI + ARIF-Perplexity",
    "earth": "runtime telemetry, signed A2A receipts, recovery drills, policy tests"
  },
  "qdf": "F1/F2/F3/F4/F5/F8/F9/F11/F12/F13"
}
```
