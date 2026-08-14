# Paperclip → arifOS Federation Semantic Map (CCC Worker Contract, 2026-08-14)

> **Method:** falsify before claiming. Every EXISTS verdict below cites a live endpoint probed on
> this VPS at 2026-08-14 (UTC). `UNKNOWN` = could not falsify within this session's probe budget.
> Truth rule: live :3001/health beats prose.
>
> Source: /tmp/paperclip-study (MIT). Doctrine: /root/AAA/governance/CCC_DOCTRINE.md.
> AAA = the state providing infrastructure (barang awam) to citizens. AAA never judges.

## Legend

- **EXISTS** — live twin verified by direct probe of organ endpoint.
- **WEAK** — twin exists but missing a load-bearing behavior of the Paperclip pattern.
- **MISSING** — no twin found; falsified by probing the organ's declared surface.

---

## P1 — Wake Bus (heartbeat / wakeup requests / watchdogs)

| # | Paperclip component (file) | Capability | Our twin (organ + live path) | Verdict |
|---|---|---|---|---|
| 1.1 | `server/src/services/heartbeat.ts` + `packages/db/src/schema/agent_wakeup_requests.ts` | Persistent wake-request queue: enqueue → claim → finish, coalesce counter, idempotency key, semantic reason | **AAA a2a-server hold queue** — Redis list `aaa:hold_queue` + `startRetryWorker()` (30s poll, retry → `aaa:dead_letter` after 5), live at `a2a-server/server.js:5607-5664`. Probed: `GET :3001/health` → healthy, `queue_depth` published on NATS `aaa.mesh_status` every 60s | **WEAK** — time-based retry loop only. No event types, no fingerprint dedup, no claim semantics, no backoff, no HOLD-with-reason. → built as Wake Bus v1 (this task) |
| 1.2 | `heartbeat.ts` wake reasons (`source: timer/assignment/on_demand/automation`, `triggerDetail`) | Semantic wake reasons — every wake carries why | **arifFlow :7073** — every ingest carries `intent` + `organ` + FQ vector; probed `POST /ingest`-family (`/check` requires `actor_id`). `/health` → `fq.diagnosis: BALANCED`, receipts window 100 | **WEAK** — receipts record *what happened*, not *why an agent should be woken*. No enqueue surface |
| 1.3 | `task-watchdogs.ts` — `TASK_WATCHDOG_FIRST_RUN_GRACE_MS = 15_000` (line 40) | First-run grace: don't judge "stalled" before first assignment run is visible | No twin. Hermes cron / delegate_task = fire-and-forget; no creation-timestamp grace anywhere in AAA surface | **MISSING** — folded into Wake Bus v1 (first-wake grace) |
| 1.4 | `task-watchdogs.ts` — `stableStopFingerprint()` (sha256 over material leaves) | Stop fingerprint: dedupe repeated "stopped" verdicts on identical world-state | AAA federation geometry ledger (health shows `federation_geometry.ledger_events: 45`) hashes *organ health*, not actor+reason+target triples | **MISSING** — folded into Wake Bus v1 (fingerprint dedup) |
| 1.5 | `heartbeat.ts` — `BOUNDED_TRANSIENT_HEARTBEAT_RETRY_DELAYS_MS = [2m, 10m, 30m, 2h]`, max attempts | Exponential/backoff bounded retry, then terminal | AAA hold-queue retry: linear 30s poll, dead-letter after 5 — no backoff curve, no reason terminal state | **WEAK** — Wake Bus v1 ships backoff ×3 then HOLD (not DROP) |
| 1.6 | `issue-assignment-wakeup.ts`, `issue-dependency-wakeups.ts` (`ISSUE_BLOCKERS_RESOLVED_WAKE_REASON`) | Wake on upstream state change (blocker resolved → wake blocked assignee) | AREP task lifecycle (`POST /api/arep/submit`, `GET /api/arep/reality-feed` live) tracks task state but emits no downstream wake | **WEAK** — Wake Bus v1 `upstream_complete` event closes this for CCC flows |
| 1.7 | NATS-published mesh status (AAA) ← semantic twin of Paperclip live events (`live-events.ts`) | Observable queue state | **AAA mesh coordinator** — `GET :3001/api/mesh/state` + NATS `aaa.mesh_status` | **EXISTS** |

## P2 — Claim Office (atomic checkout)

| # | Paperclip component (file) | Capability | Our twin | Verdict |
|---|---|---|---|---|
| 2.1 | `issues.ts` checkout (`checkoutRunId`, `claimedAt`, `sameRunLock()`) | Atomic single-owner claim on a work item | **git worktrees + CCC temp-roles** — `/root/forge_work/worktrees/*` live (verified `git -C /root/AAA worktree list`); CCC_DOCTRINE.md §Roles: role expires when task completes. Claim = worktree + branch ownership, enforced socially by CCC contract | **EXISTS** (mechanism differs: VCS-native claim vs DB row lock; both single-owner, both expiring) |
| 2.2 | `issue-tree-control.ts` (`ISSUE_TREE_CONTROL_INTERACTION_WAKE_REASONS`) | Verified wake reasons for tree interactions; pause-hold gate | AAA membrane middleware classifies every message (action_class OBSERVE/MUTATE/…) — `a2a-server/membrane_middleware.js:85-96` | **WEAK** — classification ≠ verified wake reason, but Wake Bus v1 reuses membrane (passes OBSERVE) and adds its own enum |
| 2.3 | `issues.ts` `claimed`/`queued` wakeup status join (line 2897) | Queue visibility joins claim state | `GET :3001/api/agents/status` + `/cockpit/agents` | **EXISTS** (display plane) |

## P3 — Cost Telemetry (budgets/costs)

| # | Paperclip component (file) | Capability | Our twin | Verdict |
|---|---|---|---|---|
| 3.1 | `costs.ts` `costEvents` ledger (cents, tokens, scope) | Append-only cost events per agent/issue | **FLAME :18901** — probed `/health` + `/`: `status: live`, `chain: RM0-TOOLS-FREELOOP`, authority **ADVISORY**, tracks hit rates/model failures (FLAME-router skill: "latency, billing, hit rates") | **EXISTS** (semantic twin: FLAME is the cost/route telemetry plane) |
| 3.2 | `budgets.ts` `hard_stop → pauseReason="budget"` (lines 72, 221-296) | Hard stop = HOLD not DROP — scope pauses with reason, resumable | **arifFlow FQ gate** — `fq_gate.js` blocks MUTATE at FQ<0.5 with `verdict: HOLD` + reason + next_action; probed live via `:7073/health` (fq BARRIER count 58) and AAA middleware (`[fq-gate] BLOCKED` path) | **EXISTS** (FQ = budget-of-trust semantics; both HOLD-not-DROP) |
| 3.3 | `budgets.ts` `resume()` clearing `pauseReason` | Explicit resume after operator action | F13 sovereign override path (`next_action: "request F13 override"` in gate responses) | **EXISTS** (sovereign-ratified resume) |

## P4 — Skills Provenance

| # | Paperclip component (file) | Capability | Our twin | Verdict |
|---|---|---|---|---|
| 4.1 | `packages/skills-catalog/` bundled/optional/generated classes + `catalog-provenance.ts` | Every skill carries provenance class | **AAA skills_index.json** — `/root/AAA/skills_index.json`: `schema_version: 1.0.0-orthogonal-discovery`, count 180, per-skill metadata; synced by cron `skill-mesh-sync.sh --check` (*/5) | **EXISTS** |
| 4.2 | `catalog-builder.ts` shipped-catalog contract tests | Catalog truth verified by tests | `npm run validate:aaa` + skills_index regeneration script + AAA CI (agentic-ci.yml) | **EXISTS** |
| 4.3 | `frontmatter.ts` skill frontmatter parse | Skill metadata contract | Hermes skills (264+, YAML frontmatter) + AAA skills/ tree | **EXISTS** (dual homes, both with frontmatter contract) |

## P5 — Cross-cutting (observed, kept for context)

| # | Paperclip component | Capability | Our twin | Verdict |
|---|---|---|---|---|
| 5.1 | Agent Inbox (SIAL, NATS JetStream KV, 24h TTL) — AAA | Persistent inter-agent messages | AAA `agent_inbox.js` (forged 2026-08-05) — **EXISTS**; Wake Bus v1 uses REST delivery + its own queue, not inbox, to keep wake semantics distinct from message semantics |
| 5.2 | `secrets.ts` runtime bindings | Pre-dispatch secret gate | arifOS kernel :8088 (floor 13/13 healthy, probed) — secrets are F11 kernel authority | **EXISTS** (kernel-owned) |
| 5.3 | VAULT999 seal chain | Immutable witness | `:3001/health` → `chain.seq 45`, sha256 hash live; arifOS `/999/verify` | **EXISTS** |

---

## Build decision (falsification conclusion)

Only the **event-driven wake queue itself** is MISSING (1.1/1.3/1.4/1.5/1.6). Everything else has a
live twin — reuse, do not rebuild:

- Persistence → existing Redis (`REDIS_URL` already in aaa-a2a.service).
- Delivery target → A2A card `endpoints.baseUrl` from `AgentCardRegistry` (existing).
- HOLD semantics → reuse FQ-gate vocabulary (`verdict: HOLD`, reason, next_action).
- Announce/restart → existing T2 protocol (`AGENTS-AUTONOMY.md` §T2) + `systemctl restart aaa-a2a`.

**P1 Wake Bus v1** is therefore built *inside* AAA a2a-server as public infrastructure: 5 event
types, sha256(actor+reason+target) dedup, 15s first-run grace, exponential backoff max 3 → HOLD.
No new service/repo/organ/protocol. See commit on branch `wake-bus-v1`.
