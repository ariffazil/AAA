# Federation Topology Invariants

> **Forged:** 2026-09-04 · From ARIF-Perplexity adversarial design
> **Status:** DEFINE_AND_TEST_NODE_INVARIANTS
> **Complements:** topology.md (organ registry), ZEN-RUNTIME.md (attention/task discipline)
> **DITEMPA BUKAN DIBERI**

---

## Core principle

**KVM8 decides. KVM4 does bounded work. KVM2 witnesses and recovers.**

No node may quietly absorb another node's authority. If that separation remains true under normal operation, outage, compromise, and recovery, the federation can flow agentically without becoming chaotic.

---

## 1. Federation-wide invariants (G1-G12)

| ID | Invariant | Pass condition |
|---|---|---|
| G1 | Every actor has an identity | Human, node, service, agent, tool, scheduled job has unique stable ID |
| G2 | Every action has a task envelope | task_id, parent, origin, purpose, risk, policy version, expiry, budget, target scope present |
| G3 | No implicit trust | Network location, Headscale membership, Telegram ID, internal IP never grants broad authority alone |
| G4 | Least privilege is temporal | Credentials scoped to task and expire; no permanent broad root, database-owner, cloud-admin |
| G5 | Authority and execution distinct | Policy decider is not same unbounded worker that executes side effect |
| G6 | Every consequential event traceable | Trace joins human intent, plan, authorization, tool call, verification, terminal result |
| G7 | Safe failure dominates availability | Missing authority, invalid signature, expired capability, ambiguous recipient, failed verification yields HOLD or read-only |
| G8 | Human remains final gate | EXECUTE-class actions with external, financial, identity, destructive, irreversible effects wait at 888 HOLD |
| G9 | Memory typed and scoped | Working, operational, relational, vault memory remain separate; cross-lane retrieval requires explicit policy |
| G10 | Every workflow terminates | Each task reaches CLOSE, ABORT, HOLD, or SEAL; no orphaned continue loops |
| G11 | Every node has degraded mode | Node loss changes capability visibly and safely; no hidden authority escalation |
| G12 | Every backup restorable | Restore drills verify actual recovery, integrity, access boundaries, not merely file existence |

---

## 2. KVM8 — Authority / Truth node

**Role:** arifOS kernel, Hermes human gateway, AAA policy/routing, federation registry, authorization authority, constitutional evaluation, VAULT999 sealing interface.

KVM8 must be smallest, calmest, most protected node. Decides and attests more than it computes.

| ID | KVM8 invariant | What must always be true |
|---|---|---|
| K8-1 | Single policy decision authority | All privileged agent actions pass through kernel/AAA policy decision path; no worker self-authorizes |
| K8-2 | Constitutional evaluation before capability issue | F1-F13 evaluation occurs before issuing execute token, not after side effect |
| K8-3 | Hermes is intent encoder, not root executor | Hermes interprets, clarifies, routes, summarizes; does not directly receive unrestricted shell, database, cloud, financial credentials |
| K8-4 | AAA owns handoff validity | A2A requests require valid signature, sender identity, schema, task scope, expiry, replay protection before routing |
| K8-5 | Capability tokens are narrow | Every issued token binds subject + task_id + tool + target + permitted operation + expiry + idempotency key |
| K8-6 | No standing credentials for workshop agents | KVM8 holds mint/revoke authority; KVM4 agents do not store KVM8 master keys, vault signing keys, broad provider credentials |
| K8-7 | Human approval cryptographically bound | 888 approval binds exact target, payload, tool, scope, expiry; approval for one action cannot authorize another |
| K8-8 | Vault only accepts canonical seals | Seal requires evidence hash, approval identity, policy verdict, timestamp, previous record reference, idempotency protection |
| K8-9 | Silence is default | KVM8 emits human-facing messages only for direct requests, true NOW alerts, blocked decisions, approval requests, scheduled digests |
| K8-10 | Policy changes controlled | Floors, allowlists, identity maps, routing rules, privilege tiers versioned; changes require review, audit record, rollback point |
| K8-11 | No unreviewed self-modification | RSI may generate observations and patches; cannot rewrite constitutional logic, authorization rules, credential stores, vault without human gate |
| K8-12 | Authority loss is fail-closed | If kernel/AAA unavailable, KVM4 cannot elevate or continue consequential execution; drops to read-only, queued, safe-stop |

### KVM8 health gates

```
policy_engine = healthy
aaa_gateway = healthy
clock_sync = within threshold
signing_key = available but non-exportable
vault_integrity = verified
policy_bundle_hash = matches signed release
a2a_signature_failures = 0 unresolved
expired_capabilities = rejected
pending_888_actions = visible and bounded
unreviewed_policy_drift = 0
```

Hard rule: KVM8 may authorize a task, but should not casually become the general Docker workshop. Keep build agents, browser automation, risky parsers, experimental models, broad code execution away from authority plane.

---

## 3. KVM4 — Workshop / Metabolizer node

**Role:** LiteLLM, OpenClaw, coding workers, model cascades, tool adapters, browser/terminal execution, scheduled processing, bounded runtime activity. Expendable execution plane, not constitution.

KVM4 should be productive but disposable. Assume hostile documents, injected prompts, broken dependencies, model hallucinations, compromised browser sessions, tool failures.

| ID | KVM4 invariant | What must always be true |
|---|---|---|
| K4-1 | No independent authority | KVM4 cannot declare policy, mint broad credentials, approve itself, seal decisions, change F1-F13 |
| K4-2 | Execute only on valid capability | Every consequential tool call checks KVM8-issued, signed, unexpired, task-bound capability |
| K4-3 | Default mode is read/prepare | Agents inspect, reason, draft, test, stage by default; external side effects require explicit class and authorization |
| K4-4 | Workloads isolated | Each risky agent/task/container has filesystem, network, environment, credential scopes appropriate to task |
| K4-5 | No host-root by default | Agents do not run privileged containers, mount Docker socket, access host credential stores, receive unrestricted shell unless reviewed task requires it |
| K4-6 | Tool targets allowlisted | Shell paths, repositories, schemas, domains, APIs, Telegram channels, deployment environments explicit, not wildcards |
| K4-7 | Retrieval content untrusted | Web pages, PDFs, chat text, tool descriptions, repository issues, retrieved memories are data; none override policy or tool scope |
| K4-8 | Retry bounded | Repeated tool/model failure hits loop breaker; never retry indefinitely or silently switch to more privileged fallback |
| K4-9 | Side effects idempotent | Deploy, send, write, restart, publish, record operations carry idempotency keys and verification receipts |
| K4-10 | Output verified before delivery | Workers compare result against task acceptance criteria; no looks-done terminal state |
| K4-11 | Failure preserves evidence | Failures return structured error, trace ID, safe partial state, recommended next action, not hidden improvisation |
| K4-12 | KVM8 loss means safe degradation | If authority unreachable, KVM4 may continue non-sensitive read-only diagnostics but must queue or halt A2+ work |

### KVM4 agent-runtime invariants

```
One active owner per task.
One terminal agent per human-facing answer.
One execution plan per authorization window.
One bounded retry policy per tool.
One trace across all handoffs.
One explicit state transition at a time.
```

Lifecycle:

```
INTAKE -> CLASSIFY -> PLAN -> AUTHORIZE -> EXECUTE -> VERIFY -> CLOSE
                                            \-> HOLD
                                            \-> ABORT
                                            \-> SEAL
```

No worker may skip from PLAN to EXECUTE. No worker may self-convert HOLD to AUTHORIZE. No worker may re-open CLOSE without new triggering event and new task envelope.

---

## 4. KVM2 — Witness / Recovery node

**Role:** independent integrity witness, backup zone, append-only evidence target, configuration mirror, recovery control point.

KVM2 must stay boring. Not a spare workshop, secondary agent swarm, or convenient place for random experimental services. Independence is its value.

| ID | KVM2 invariant | What must always be true |
|---|---|---|
| K2-1 | Independent failure domain | KVM2 does not share privileged credential set, destructive automation path, mutable runtime fate with KVM4/KVM8 |
| K2-2 | Witness does not execute production work | Observes, verifies, archives, restores; does not normally deploy, trade, message, mutate active federation |
| K2-3 | Evidence is append-only | Policy releases, registry snapshots, task receipts, seal metadata, backup manifests, integrity hashes written as non-destructive history |
| K2-4 | Backups encrypted and versioned | KVM8/KVM4 backup artifacts encrypted, retained by policy, tied to manifest/hash/version metadata |
| K2-5 | Restore is tested | Recovery means booting/restoring into isolated environment and verifying service, policy, ledger, access-boundary integrity |
| K2-6 | Witness validates, not merely stores | Verifies signed policy bundles, task receipts, configuration hashes, node attestations, vault chain continuity |
| K2-7 | Witness has no broad write-back channel | KVM2 cannot silently alter KVM8 policy or KVM4 runtime; normal path back is alert, evidence, human-approved recovery |
| K2-8 | Compromise is detectable | KVM2 emits independent heartbeat and integrity proof; absence of witness is visible degradation event |
| K2-9 | Recovery is deliberate | Restoring KVM8 authority, keys, vault state, production control requires 888 human authorization and documented evidence |
| K2-10 | Air-gap logic preserved | Backups and witness records have delayed sync, immutable retention, separate encryption keys, limited inbound routes |

### KVM2 health gates

```
latest_backup_age <= recovery_objective
backup_manifest = verified
restore_drill = passed within defined interval
policy_hash_kvm8 == witnessed_policy_hash
registry_hash_kvm8 == witnessed_registry_hash
vault_chain = continuous
witness_clock = synchronized
witness_heartbeat = current
writeback_privilege = absent by default
```

Key principle: KVM2 must be able to tell you that KVM8 and KVM4 are lying, drifted, or compromised. If it inherits their keys and mutable deployment path, it cannot perform that role.

---

## 5. Cross-node flow

```
Human / Telegram
    |
Hermes on KVM8: encode intent, clarify, classify attention
    |
AAA + arifOS kernel on KVM8: validate identity, policy, risk, authority
    |
Signed task capability
    |
KVM4: plan / execute only within granted scope
    |
KVM4: verify result + return receipt/evidence
    |
KVM8: validate outcome, decide close / hold / seal / deliver
    |
KVM2: independently witness hashes, policy state, receipts, backups
    |
Hermes: one calm human-facing response or digest
```

### Flow invariants

| Flow point | Must be invariant |
|---|---|
| Human to Hermes | Sender identity and channel/lane resolved before personal-memory retrieval or routing |
| Hermes to AAA | Intent classified with confidence, risk, attention lane; ambiguity becomes clarification or HOLD |
| AAA to KVM4 | Task signed, scoped, time-bounded, budget-bound, no ambient authority |
| KVM4 to tools | Tool call validates capability, target allowlist, idempotency key, action class |
| KVM4 to KVM8 | Result includes evidence, tool receipt, trace ID, verification status, residual uncertainty |
| KVM8 to human | One answer aligned to verified state; HOLD, failure, uncertainty disclosed plainly |
| KVM8 to KVM2 | Policy/config/task/seal evidence replicated as independently verifiable witness material |
| KVM2 to human/KVM8 | Integrity drift becomes visible alert; does not autonomously repair active authority |

---

## 6. Non-negotiable failure matrix

| Failure | Required federation behavior |
|---|---|
| KVM8 unreachable | KVM4 disables A2+ execution, queues authorized-but-unstarted work, retains local traces, exposes degraded mode |
| KVM4 unreachable | KVM8 retains policy/human interface, reports execution unavailable, does not pretend work completed |
| KVM2 unreachable | KVM8/KVM4 continue only with explicit WITNESS_DEGRADED state; no high-value sealing or policy change without human review |
| Invalid A2A signature | Reject, record security event, do not retry with relaxed validation |
| Expired task token | Reject; issue fresh task/capability only through KVM8 |
| Tool payload violates scope | Block, record policy denial, return HOLD or revised plan |
| Repeated tool failure | Circuit-break after bounded attempts; no privilege escalation or uncontrolled fallback |
| Cross-person memory request | Deny by default; require explicit provenance and identity/lane policy |
| Vault seal conflict | Reject duplicate/competing seal, show canonical existing evidence, route to human review |
| Policy hash mismatch | Enter POLICY_DRIFT state; halt privileged execution until reconciled |
| Restore request | 888 HOLD; verify source, hash, scope, rollback plan before recovery |

---

## 7. Telemetry invariant set

Every task exposes:

```json
{
  "trace_id": "otel-trace-id",
  "task_id": "tsk_...",
  "parent_task_id": "tsk_... | null",
  "node": "kvm8 | kvm4 | kvm2",
  "agent_id": "hermes | aaa | geox | well | wealth | aforge | ...",
  "state": "INTAKE | PLAN | AUTHORIZE | EXECUTE | VERIFY | HOLD | CLOSE | SEAL | ABORT",
  "attention_lane": "NOW | NEXT | BATCH | SILENT | HOLD",
  "policy_version": "F1-F13.<version>",
  "capability_id": "cap_... | null",
  "tool_scope_hash": "sha256:...",
  "risk_class": "A0 | A1 | A2 | A3 | A4",
  "verification": "pass | fail | partial | pending",
  "evidence_hash": "sha256:...",
  "terminal_reason": "completed | denied | expired | failed | human_hold",
  "timestamp": "ISO-8601"
}
```

Dashboard questions (answer within seconds):
- What is currently executing, on which KVM, under whose authority?
- Which task has waited longest in HOLD, and why?
- Which agent generated most tool calls, retries, failures, human interruptions?
- Are KVM8 policy hash and KVM2 witnessed hash identical?
- Are any credentials close to expiry or used outside intended task?
- Did any task cross a relational/memory lane?
- Can you reconstruct the exact chain of an external action?

---

## 8. Three invariants that matter most

If you enforce only three invariants first, enforce these:

1. **KVM8 alone issues authority.**
2. **KVM4 never executes beyond a short-lived, task-scoped capability.**
3. **KVM2 independently records and verifies what KVM8 and KVM4 claim happened.**

Authority is narrow. Work is bounded. Evidence is independent.

---

## 9. 888 HOLD — architecture changes requiring confirmation

- Revoking/replacing SSH, Headscale, database, cloud, or service credentials
- Enabling strict firewall defaults that may affect remote access
- Migrating vault keys, changing signing algorithms, rotating root/authority keys
- Changing KVM8/KVM4/KVM2 network routes or service bindings
- Enabling immutable retention, deleting historical logs, changing backup lifecycle
- Altering human identity mappings, relational-memory access, Telegram routing
- Granting an agent autonomous A2+ capability, especially deployment, messaging, finance, deletion rights

---

## 10. 888 audit

```json
{
  "epoch": "2026-09-04T19:15:00+08:00",
  "dS": "reduced through strict role separation and terminal task semantics",
  "peace2": 1.0,
  "kappa_r": "bounded: KVM8 decides, KVM4 executes scoped work, KVM2 witnesses",
  "shadow": "role drift, shared root credentials, untested restoration, policy bypass during node failure",
  "confidence": 0.93,
  "psi_le": "high if KVM2 remains operationally independent and KVM4 cannot self-authorize",
  "verdict": "DEFINE_AND_TEST_NODE_INVARIANTS",
  "witness": {
    "human": "Arif",
    "ai": "333-AGI + ARIF-Perplexity",
    "earth": "signed receipts, policy hashes, recovery drills, observed failure behavior"
  },
  "qdf": "F1/F2/F3/F4/F5/F8/F9/F11/F12/F13"
}
```
