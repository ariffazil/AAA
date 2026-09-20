# EUREKA — Automation runtime substrate (12 organs → 14 subsystems)

> **Class:** guidance (not constitution)
> **Status:** CANDIDATE — AWAITING F13
> **Binding:** false until ratified
> **Author:** F13 articulation (target map) · FI-007 clerk (live census)
> **Date:** 2026-09-21
> **Does not supersede:** APEX-ZEN-CANONICAL-COMPRESSION.md · ARIF_FLOW_METABOLIC_PLANE.md · CHRON canon · event-bridge
> **This file adds:** the wajib execution organs as a *runtime* map, scored against live KVM8, and the APEX-ZEN path (repair joins, do not buy a 13th scheduler).
>
> **Census (counts, hops, live SHAs):** `/root/work/AUTOMATION-REALITY-CENSUS-2026-09-21.md` generated_utc `2026-09-20T17:23:38Z`. Do not treat the 00:30 MYT table below as current numbers.
>
> **Delta 01:23 MYT (same night, FI-007 re-probe):**
> - BUS join **partially closed**: `aaa-ops-bus-worker` + durable consumer `aaa-ops-fabric` on `arifos.floor.>`. Canary hop 4ms ok. Stream now also matches `arifos.floor_breach`. Retract “governance last persist 2026-09-01”.
> - LEARNING is no longer “lessons.jsonl empty”: 1 row exists, and it is a **sentinel lesson about `UNKNOWN`**, not a real lesson. `VERIFIED → LESSON | NO_LESSON_REASON` is still the unpaid invariant.
> - 12 organs under-count the target. Split **PROVENANCE**, **LEARNING**, **ATTENTION** out of MEMORY/CHRON/HUMAN EDGE. Target set is 14: TIME EVENT QUEUE STATE WORKFLOW AUTHORITY EXECUTION WITNESS RECONCILIATION PROVENANCE MEMORY LEARNING HUMAN-EDGE ATTENTION.
> - Remaining P0 is still JOIN, not missing NATS, and now also **state ontology**: HEALTH × CONVERGENCE. Deploy-reconciler already HOLDs unpushed labor; `/health` still says `degraded`. HOLD ≠ FAIL.

## The law (target)

Cron wakes. Event bus announces. Queue assigns. State machine decides what state is legal. Hooks connect boundaries. Workflow remembers progress. Witness proves what happened. Human authority decides what machines must not decide.

Do not collapse everything into cron.

## 12 organs

| Organ | Question | Live posture (KVM8, 2026-09-21 ~00:30 MYT) |
|---|---|---|
| CLOCK | when? | **OVER-LIVE** — systemd timers + `/etc/cron.d` + root crontab + Hermes jobs.json. Three substrates, overlapping metabolism. |
| BUS | what happened? | **PARTIAL** — NATS JetStream up. Four streams. **01:23 MYT:** `aaa-ops-fabric` (governance floor.>) and `kabarkan-worker-fresh` are live. Organ-heartbeat consumers still never pulled (~34k unprocessed). `agent_memory` still has no consumer. Dual subjects (`floor.breach`/`floor_breach`, `arifos`/`arifOS`) remain. |
| QUEUE | who works? | **PARTIAL** — `aaa:hold_queue` exists in a2a-server Redis code. `niat_proposals.json` is a file queue (11 PENDING). Floor-breach handler does not enqueue. No DLQ. |
| STATE | what is true now? | **PARTIAL** — kernel `/health` degraded (source≠built). Envelope schema exists. LLM text still routinely treated as transition. |
| WORKFLOW | what comes next? | **PARTIAL** — Grok Rhai workflows, niat executor, no durable multi-day engine. **Do not install Temporal to fill this.** |
| AUTHORITY | who may cause it? | **PARTIAL** — F1–F13 kernel, niat binary approve, 888_HOLD payload. Not bound to every transition. |
| EXECUTOR | change reality | **LIVE** — A-FORGE, systemd, FI seats. |
| WITNESS | did it happen? | **PARTIAL** — VAULT999, FRAME `:18085` ok, arifFlow receipts. APEX-ZEN loop cannot append VAULT999 (EPERM). |
| RECONCILER | does reality still match? | **LIVE / noisy** — deploy-reconciler, drift-detector, aaa-drift-check, auditor-drift-check, surface-guard. Many clocks, one truth. |
| MEMORY | what survives? | **PARTIAL** — carry_forward, CHRON episodes. `agent_memory` stream has no consumer. |
| LEARNING | expected vs actual | **PARTIAL** — CHRON MCP live; calibration 2/2 accuracy 0.5. One lesson row is a sentinel about `UNKNOWN`. Policy-candidate gate not live. |
| CHRON | what does time mean? | **PARTIAL** — meaning organ exists (predictions, verify timers, loop-closer). Linux cron still fires the bodies. Bind-before-attention still the scar. |
| HUMAN EDGE | machine meets human | **PARTIAL** — Hermes Telegram + APA email/gmail/calendar/gws bridges live. Event-bridge is still a cron delta-gate. Kill-switch is a runbook not a below-LLM tripwire. |
| ATTENTION | who is allowed to be bothered | **PARTIAL** — envelope has `NEXT_ACTOR` and refuses Arif DM as default. `HUMAN_REASON` closed set is skill-only, not on the wire. A0–A3 not a live classifier. |
| PROVENANCE | where did this fact come from | **PARTIAL** — kernel `software_release` hashes; CHRON birth snapshots. Ops envelope `causation_id=null`. arifFlow rows often lack `trace_id`. |

Under every organ: identity, provenance, idempotency, time, retry, cancellation, observability, reversibility. Those are physics, not products.

## The measured hole (P0)

A safety event that cannot traverse **detector → durable bus → consumer that does work → receipt → FRAME → acknowledgement** does not exist operationally.

Live tonight (OBS):

1. Surface-guard detected A-FORGE DOWN, consecutive ≥2, published `arifos.floor_breach` at 00:21:45 MYT. Journal: `888_HOLD alert published`.
2. a2a-server (pid 2253605) **received** it and `console.log`'d twice. That is not a queue, not a human, not a receipt.
3. **00:30 MYT (RETRACTED at 01:23):** JetStream did not persist `arifos.floor_breach` (underscore vs `arifos.floor.>`). **01:23 MYT:** stream subjects include both; last `floor_breach` is seq 57946; last `floor.breach` is seq 57948; last canary seq 57951 hop 4ms. Persist is no longer the hole. Consume-without-queue still is.
4. Organ stream `arifos-organs` is live (heartbeats every ~9s) with four pull consumers whose last delivery is **never** and ~34k unprocessed.
5. Event-bridge is a cron delta-gate to Telegram, not the NATS nervous system. It did not record the 00:21 HOLD.
6. Prior open-loop “NATS client missing” is **RETRACTED**. Module loads from `/root/A-FORGE`. The remaining hole is **join**, not dependency.
7. Extra OBS from independent census: heartbeat publishes `arifOS.verdicts` while A2A subscribes `arifos.verdicts` (NATS is case-sensitive). `flow-event.sh` greps stdin, so under cron it always skips the digest. `nats-storm-guard.sh` is not on crontab. arifFlow live JSONL rows often have `previous_receipt_hash: null` and no `trace_id`. CHRON `e2e_proof.json` verify/learn stages are SIMULATED.

`/health` green + a log line ≠ delivery works.

**Canary (MEASURED 2026-09-21 00:36:47 MYT, reversible pub):** `nats pub arifos.floor.canary` → JetStream `arifos-governance#57944` in 616ms. Control: `arifos.floor_breach` still “no message found”. a2a did not log the canary (it only core-subscribes `floor_breach`). So: **dot-token subjects persist; underscore-token alerts do not.** The live HOLD path is the one that cannot be replayed.

## APEX-ZEN path (not a shopping list)

Industry 2026 (Temporal, Restate, DBOS, Inngest) all say the same thing this map already said: long-lived agent work cannot live in one LLM context; cron is not a workflow; bus ≠ queue. **Buying Temporal would be a 13th organ.** This box already has NATS + Postgres + systemd + CHRON + arifFlow. Import the *invariant*, not the product.

1. **P0 canary** (no new cron — hook an existing timer). Emit `arifos.floor.canary` (subject that matches the stream). Durable consumer. Receipt. FRAME. If any arrow fails → DEGRADED, not healthy.
2. **Fix the subject** so alerts persist: `arifos.floor.breach` *or* add `arifos.floor_breach` to the stream. Then make the a2a handler call `queueTask` instead of `console.log`.
3. **Do not add clocks.** Clock is already the over-provisioned organ. Compress later; repair joins first.
4. **CHRON keeps meaning; systemd keeps wake.** That split is already the doctrine. Keep it.
5. **Learning stays gated.** Outcome → lesson candidate → cooling → test → human/constitutional gate → canary → keep/rollback. An empty lesson file can be honest. A lesson whose `error_type` is the classifier's own sentinel (`UNKNOWN`) is not. Invariant: `VERIFIED → LESSON | NO_LESSON_REASON`.
6. **Split HEALTH from CONVERGENCE on every `/health`.** `HEALTHY + INTENTIONAL_HOLD` is legal (unpushed source, deploy HOLD). Today that shape is published as `status=degraded`. UNKNOWN ≠ OK, HOLD ≠ FAIL, DRIFT ≠ FAILURE.

## External research (2026-09-21, does not change the path)

Cited report: session workflow `deep-research` scratch `report.md` (status Partial).

- Temporal / Restate / DBOS = journal replay. Inngest / Cloudflare = named-step memoization. LangGraph = node restart. **NATS JetStream and Kafka are buses, not workflows.** A JetStream PubAck means stored, not consumed. Neither broker atomically commits a DB write + a publish; that is still the outbox.
- Durable sleep exists in Temporal/Restate/Inngest/Cloudflare. That is CLOCK meaning (CHRON + durable timer), not a reason to install a 13th organ.
- MCP cancel is SHOULD/cooperative. A2A cancel is protocol, not F1–F13. Kill-switch remains a runbook until it is below the LLM.
- Local scar still open: `arif_seal` retry-after-timeout can duplicate a VAULT999 row (idempotency key on session+nonce). That is the same join class as `floor_breach` console.log.

Nothing here authorises buying Temporal. It authorises repairing joins.

## What this is not

Not a seal. Not a new organ. Not authority to install Temporal/Kafka/Restate. Not a request to add cron.

Bus persist + self-consume canary is now MEASURED (4ms, `aaa-ops-fabric`). The remaining hole is EVENT → QUEUE → OWNER → OUTCOME → FRAME: ACK is not a job, envelope `next_actor` is hardcoded, `HUMAN_REASON` is not on the wire, and `/health` still collapses INTENTIONAL_HOLD into `degraded`.
