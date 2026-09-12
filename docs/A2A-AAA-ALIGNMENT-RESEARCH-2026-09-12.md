# A2A Protocol Deep Research — AAA Federation Alignment

**Research Date:** 2026-09-12
**Researcher:** Hermes (ASI Human Bridge) + ARIF-PERPLEXITY audit
**Requested by:** Arif (F13 Sovereign)
**Spec Version Analyzed:** A2A v1.0.0 (latest released)
**Classification:** OBS/DER/INT — evidence from spec, derivation from AAA topology
**Audit Status:** 888 HOLD — protocol compliance claims require test-backed evidence before documentation
**Round 2 (2026-09-12):** roadmap normalized to P0–P9 + acceptance-gate column; security-invariants table and threat model extended (applied in-tree).
**Verification pass (333-AGI, 2026-09-12 14:57 MYT):** residual §3 compliance claims disarmed; §2 counts synced to observed (20 routes / 10 targets); acceptance-gate detail expanded; section numbering normalized (7, 8, 9 in order).
**Evidence state:** Research and design artifact — not a protocol conformance claim.
**Runtime validation:** Pending P0 conformance evidence (§5 acceptance gates).
**Canonical version status:** Drift detected across four surfaces — root README `A2A v1.0.0` · agent-card `protocolVersion: "1.2"` (schema ref v1.0) · wire-manifest `meta.protocol: "A2A v1.2"` · server header `A2A-Version: 1.0`. Decision pending (§5 P0). Evidence packet: `docs/a2a-evidence-2026-09-12.json`.

---

## 1. What Is A2A? — The Real Specification

A2A (Agent2Agent) is an open protocol (v1.0.0, backed by Google + 50+ partners) for agent-to-agent communication. It is NOT just a messaging standard — it is a complete interaction framework with discovery, task lifecycle, streaming, push notifications, and extension mechanisms.

### Core Architecture — 3 Layers

```
Layer 1: Canonical Data Model    (proto-defined, binding-agnostic)
  → AgentCard, Task, Message, Part, Artifact, Extension

Layer 2: Abstract Operations     (what agents MUST support)
  → SendMessage, SendStreamingMessage, GetTask, ListTasks,
     CancelTask, SubscribeToTask, PushNotification CRUD,
     GetExtendedAgentCard

Layer 3: Protocol Bindings       (how it's transported)
  → JSON-RPC 2.0 (primary), gRPC, HTTP/REST
```

The normative source is `spec/a2a.proto` — all SDKs must regenerate from this.

### Core Data Objects

| Object | Purpose | Key Fields |
|--------|---------|------------|
| **AgentCard** | Discovery — published at `/.well-known/agent-card.json` | name, description, url, version, capabilities, skills, securitySchemes, supportedInterfaces, extensions |
| **Task** | Stateful unit of work | id, contextId, status (state+message), artifacts[], history[] |
| **Message** | A communication turn | role (user/agent), parts[], taskId?, contextId?, referenceTaskIds[] |
| **Part** | Smallest content unit | text, file, data, form — with mimeType |
| **Artifact** | Task output | id, name, parts[], metadata |
| **Extension** | Extra functionality beyond core spec | uri, required, params{} |

### Task Lifecycle (v1.0)

```
SUBMITTED → WORKING → INPUT_REQUIRED → WORKING → COMPLETED
                                   ↘ FAILED
                                   ↘ CANCELED
                                   ↘ REJECTED (NEW in v1.0)
```

Terminal states: COMPLETED, FAILED, CANCELED, REJECTED
Interrupted states: INPUT_REQUIRED, AUTH_REQUIRED

### Operations Summary

| Operation | Purpose | Delivery |
|-----------|---------|----------|
| SendMessage | Initiate interaction | Sync (wait for terminal) or async (return immediately) |
| SendStreamingMessage | Initiate with SSE stream | SSE events: TaskStatusUpdateEvent, TaskArtifactUpdateEvent |
| GetTask | Poll task state | REST/JSON-RPC |
| ListTasks | Paginated task listing | Cursor-based pagination |
| CancelTask | Request cancellation | Idempotent |
| SubscribeToTask | Stream updates for existing task | SSE |
| Push Notification CRUD | Webhook-based async delivery | HTTP POST to registered webhook |
| GetExtendedAgentCard | Authenticated detailed card | Requires OAuth/bearer |

### Multi-Turn Interactions

- **contextId**: Groups related tasks/messages into a conversation
- **INPUT_REQUIRED**: Agent pauses mid-task, requests human/agent input
- **ReferenceTaskIds**: Explicit cross-referencing between tasks
- **Context Inheritance**: New tasks in same context can inherit prior state

### Extension System

Extensions are URI-identified, with `required` flag and `params` dict. This is where AAA's governance can plug in — the spec explicitly supports this pattern.

### A2A vs MCP — The Key Distinction

| Dimension | MCP | A2A |
|-----------|-----|-----|
| Connects | Agent → Tool/Resource | Agent → Agent |
| Interaction | Stateless tool calls | Stateful multi-turn collaboration |
| Discovery | tools/list | AgentCard at /.well-known/ |
| Content | Structured I/O | Rich modalities (text, files, forms, streams) |
| Autonomy | Tool executes as directed | Agent reasons, negotiates, delegates |

**Both are needed.** MCP is the wrench. A2A is the conversation between mechanics.

---

## 2. AAA's Current A2A State — Evidence

### What Exists (UNVERIFIED — file existence ≠ protocol compliance)

1. **Agent Card** (`/root/AAA/dist/.well-known/agent-card.json`)
   - Schema reference: `https://a2a-protocol.org/schemas/agent-card/v1.0` — UNVERIFIED against actual schema
   - Protocol binding: JSONRPC v1.0 declared
   - Capabilities: streaming, pushNotifications, extendedAgentCard declared
   - Extensions: sovereignty, verdict-grammar, governed-identity, federation-gateway, governance, metadata, federation-prompts, kernel-skills
   - Security: OAuth2 + bearer_auth declared
   - Signatures: Ed25519 with DID:web

2. **Routing Manifest** (`/root/AAA/a2a-server/A2A_LIVE_WIRE_MANIFEST.json`)
   - 20 routes across 10 routing targets (counted 2026-09-12; runtime dispatch UNVERIFIED)
   - Task lifecycle: SUBMITTED→WORKING→INPUT_REQUIRED→COMPLETED/FAILED/CANCELED
   - Receipt required on every handoff
   - Circuit breaker: 3x failure → HOLD

3. **Agent Lifecycle** (`/root/AAA/a2a-server/agent_lifecycle.js`)
   - Lifecycle states observed 2026-09-12: REGISTERED→PROVISIONED→AUTHORIZED→EXECUTING→AUDITING→STOPPED→DEPROVISIONED (+ governance: HELD, DEGRADED)
   - VAULT999 logging on every transition

4. **Status** (`/root/AAA/dist/a2a/status.json`)
   - Federation status: `discovery-live`
   - Message ingress: `888_HOLD` — POST handler NOT implemented

5. **Legacy Agent Cards** (archived)
   - Multiple agent cards for retired/deprecated agents
   - Identity cards for i-ARIF, i-AZWA

### What's Missing / Gaps

| Gap | Severity | Description |
|-----|----------|-------------|
| **Message Ingress** | CRITICAL | `POST /a2a/message` returns 888_HOLD — no actual task processing |
| **Task State Machine** | HIGH | A2A v1.0 has 7 states; AAA has 6 (missing REJECTED) |
| **contextId Support** | HIGH | No evidence of context grouping implementation |
| **Streaming (SSE)** | MEDIUM | Capability declared but no SSE endpoint found |
| **Push Notifications** | MEDIUM | Capability declared, webhook broker skill exists, but no implementation |
| **GetExtendedAgentCard** | LOW | Capability declared but not implemented |
| **ListTasks** | MEDIUM | No evidence of task listing/pagination |
| **SubscribeToTask** | LOW | Depends on SSE infrastructure |
| **Proto Normative Source** | INFO | AAA uses JSON Schema, not proto — acceptable for non-SDK use |

---

## 3. Alignment Map — A2A v1.0 ↔ AAA Federation

### 3.1 Discovery Layer

| A2A Concept | AAA Implementation | Gap |
|-------------|-------------------|-----|
| `/.well-known/agent-card.json` | Published at this path (existence verified 2026-09-12) | Schema conformance UNVERIFIED |
| AgentCard.name | "AAA A2A Gateway" | None |
| AgentCard.skills | 8 skills declared | Could add more per-organ skills |
| AgentCard.capabilities | streaming, pushNotifications, extendedAgentCard | Declared; none runtime-verified |
| AgentCard.supportedInterfaces | JSONRPC v1.0 at /a2a (declared) | UNVERIFIED against live runtime |
| AgentCard.securitySchemes | OAuth2 + bearer_auth (declared) | Runtime flows not implemented |
| AgentCard.extensions | 8 custom extensions | AAA-specific; governance-critical classification pending (§6) |

**Verdict:** Discovery surface exists and is structurally aligned; conformance UNVERIFIED until P0 (schema pin + CI gate) passes. The extension system is where AAA's constitutional governance would live.

### 3.2 Identity & Authentication

| A2A Concept | AAA Implementation | Gap |
|-------------|-------------------|-----|
| OpenID Connect | OAuth2 flows declared in securitySchemes | Needs runtime implementation |
| Bearer tokens | arifOS session tokens (SCT) | Maps conceptually — runtime binding UNVERIFIED |
| DID:web | `did:web:arif-fazil.com` with Ed25519 signatures (declared) | Beyond A2A baseline — resolver/key-rotation/token-validation posture unverified |
| Extended Agent Card | Declared capability | Not implemented |

**Verdict:** AAA DECLARES DID:web + Ed25519 beyond the A2A baseline. Do not overstate as complete mitigation — protection depends on resolver behavior, trust anchors, key rotation, DNS/HTTPS posture, and token validation.

### 3.3 Task Lifecycle

| A2A State | AAA State | Mapping |
|-----------|-----------|---------|
| SUBMITTED | SUBMITTED | 1:1 |
| WORKING | WORKING | 1:1 |
| INPUT_REQUIRED | INPUT_REQUIRED | 1:1 |
| AUTH_REQUIRED | (none) | **GAP** — AAA has no explicit AUTH_REQUIRED |
| COMPLETED | COMPLETED | 1:1 |
| FAILED | FAILED | 1:1 |
| CANCELED | CANCELED | 1:1 |
| REJECTED | (none) | **GAP** — AAA has no REJECTED state |

AAA has additional states not in A2A:
- AGENT_REGISTERED, AGENT_PROVISIONED, AGENT_AUTHORIZED — agent lifecycle, not task lifecycle
- AGENT_HELD, AGENT_DEGRADED — governance states

**Key Insight:** AAA's agent lifecycle (agent-level states) and A2A's task lifecycle (task-level states) are DIFFERENT LAYERS. They don't conflict — they compose. An agent can be AUTHORIZED while its tasks flow through SUBMITTED→WORKING→COMPLETED.

### 3.4 Messaging

| A2A Concept | AAA Implementation | Gap |
|-------------|-------------------|-----|
| SendMessage | Routing manifest defines `sendTask` | Message handler at /a2a/message is 888_HOLD |
| SendStreamingMessage | Capability declared | Not implemented |
| Message.role | N/A | Not yet processing messages |
| Message.parts | N/A | Not yet processing messages |
| contextId | N/A | Not implemented |

**Verdict:** This is the critical gap. AAA has the routing manifest but no actual message processing pipeline.

### 3.5 Extensions — AAA's Advantage

AAA's custom extensions are exactly what A2A v1.0's extension system was designed for:

| Extension URI | Purpose | A2A Alignment |
|---------------|---------|---------------|
| `.../ext/sovereign` | F13 sovereignty + DID:web binding | Custom, well-formed |
| `.../verdict-grammar/v1` | SEAL/HOLD/SABAR/VOID verdicts | Custom, maps to governance |
| `.../governed-identity/v1` | Internal registry identity | Extends AgentCard identity |
| `.../federation-gateway/v1` | Organ map + routing flags | Core federation capability |
| `.../governance/v1` | F1-F13 floors + injection defense | Constitutional governance |
| `.../metadata/v1` | Provenance + doctrine | Metadata extension |
| `.../federation-prompts/v1` | Zen prompt catalog | Domain-specific |
| `.../kernel-skills/v1` | Kernel skill dependencies | Domain-specific |

**Key Insight:** AAA's extensions are NOT violations of A2A — they ARE the A2A extension mechanism in action. The spec explicitly says extensions provide "additional functionality or data beyond the core A2A specification."

### 3.6 The tenant Field — Interface Selection (CORRECTED)

A2A v1.0 added a `tenant` field to many operations. Per the spec, this is an optional opaque routing identifier that must match the selected `AgentInterface.tenant` in the Agent Card.

**CORRECTION:** Tenant is NOT an organ routing mechanism. It is an interface-selection input. AAA must NOT overload it with authority or organ dispatch.

**Correct handling:**
```
A2A tenant → selects/validates declared AgentInterface
AAA policy → decides which internal organs are eligible
arifOS → decides whether a consequential proposed action may proceed
```

Effective route = authenticated_principal ∩ tenant/interface_policy ∩ allowed_capability_set ∩ task_classification ∩ federation_state ∩ arifOS_verdict (when consequential)

**NEVER allow:** tenant="A-FORGE" → direct executor access. Tenant is untrusted routing input, not authorization.

### 3.7 A2A ↔ MCP Complementarity in AAA

AAA already uses both:
- **MCP** for organ-to-tool communication (7 MCP servers on KVM8)
- **A2A** for agent-to-agent routing (routing manifest)

This is exactly the pattern A2A recommends: MCP for tools, A2A for agents.

The missing piece: A2A's message/task processing pipeline. Currently, inter-agent communication goes through MCP tool calls (forge_kernel, forge_execute, etc.) rather than through A2A's native task lifecycle.

---

## 4. What AAA Does That A2A Doesn't

This is the important part. A2A provides the plumbing. AAA provides the governance that makes the plumbing trustworthy.

### A2A Has No Concept Of:

| AAA Concept | Why A2A Doesn't Have It |
|-------------|------------------------|
| **Constitutional Floors (F1-F13)** | A2A is protocol, not governance |
| **Verdict Grammar (SEAL/HOLD/SABAR/VOID)** | A2A has task states, not judgment states |
| **Tri-Witness Consensus** | A2A assumes opaque agents, not witnessed ones |
| **Scar-Weight Entity Propagation** | A2A has no concept of historical cost |
| **VAULT999 Immutable Ledger** | A2A has no persistence layer |
| **Sovereign Veto (F13)** | A2A has AUTH_REQUIRED but not human veto |
| **Injection Defense (F12)** | A2A has auth but not semantic injection defense |
| **Receipt on Every Handoff** | A2A doesn't mandate audit trails |
| **Circuit Breaker (3x → HOLD)** | A2A doesn't specify resilience patterns |
| **Edge Observes, Center Executes** | A2A is symmetric; AAA has authority asymmetry |

### The Core Insight

A2A says: "Here's how agents talk."
AAA says: "Which agent should receive this, with what bounded context?"

```
A2A = interoperability and collaboration protocol
AAA = federation ingress, identity, routing, task correlation, and policy-aware control
arifOS = judgment
A-FORGE = execution
VAULT999 = evidence and receipt witnessing
```

A2A is the postal protocol. AAA is the federation gateway and traffic controller. arifOS is the policy judge. A-FORGE is the executor. VAULT999 is the evidence witness.

**AAA routes. AAA does not judge, certify, or execute consequential action.**

---

## 5. Implementation Roadmap — Corrected Priority Order

**CORRECTION from audit:** Do not implement ingress before defining the security and authority contract. A working unaudited ingress is worse than a static Agent Card.

| Priority | Work Item | Acceptance Gate |
|----------|-----------|-----------------|
| **P0** | Agent Card schema validation + exact A2A version pin | Card validates against pinned proto/schema; CI gates on drift |
| **P1** | Threat model + authority contract | Task-to-identity/tenant/route binding tested for all scenarios in Section 8 |
| **P2** | Query/analysis-only `sendMessage` ingress | Valid A2A task creates traceable AAA record; no query route reaches A-FORGE |
| **P3** | A2A ↔ governance state-machine correlation contract | A2A task states never masquerade as arifOS verdicts; correlation record is auditable |
| **P4** | `contextId`, durable task store, `GetTask`, authorized `ListTasks` | Cross-tenant access denied; cursor behavior tested |
| **P5** | Governed proposal path to arifOS | A2A output classified as proposal → canonical proposal → arif_judge; no execution yet |
| **P6** | A-FORGE dispatch only through valid scoped/unexpired SEAL | A-FORGE independently verifies arifOS provenance; any mismatch = refusal |
| **P7** | SSE streaming with task authorization | Event ordering, reconnect, cancellation, terminal-state closure tested |
| **P8** | Push notification support (if justified) | SSRF controls, allow-list, signing, retry, cancellation tested |
| **P9** | Extended Agent Card (least-privilege only) | No topology/telemetry leakage; approval from F13 |

### P2 Detail: Query/Analysis Ingress

**Gap:** POST /a2a/message is 888_HOLD
**Action:** Implement A2A v1.0 SendMessage handler at the AAA gateway for **analysis and query tasks only**.
1. Receives SendMessageRequest
2. Validates A2A envelope + schema
3. Binds authenticated principal to task
4. Classifies intent (query/analysis vs proposal vs execution)
5. Routes query/analysis tasks to appropriate organ
6. Returns task with correlation IDs
7. For proposals: creates canonical proposal → arifOS arif_judge

**A-FORGE dispatch requires arifOS SEAL — no exceptions.**

### P3 Detail: Non-Equivalence of A2A and Governance States

A2A task states and arifOS verdicts are SEPARATE state machines. Never equate them.

| A2A State | AAA Mapping | Governance Meaning |
|-----------|-------------|-------------------|
| SUBMITTED | RECEIVED | No approval |
| WORKING | ROUTED/PROCESSING | No approval |
| INPUT_REQUIRED | HOLD_FOR_INPUT | NOT equivalent to arifOS HOLD |
| AUTH_REQUIRED | AUTH_ESCALATION | NOT equivalent to F13 sovereign approval |
| COMPLETED | TASK_COMPLETED | Output may be proposal; NEVER automatic SEAL |
| FAILED | TASK_FAILED | No approval |
| CANCELED | TASK_CANCELED | No approval |
| REJECTED | TASK_REJECTED | NOT equivalent to arifOS VOID |

**Critical rule:** A2A `COMPLETED` never equals arifOS `SEAL`. A completed task produces an output. That output may CONTAIN a proposal. The proposal still needs separate arifOS judgment.

### Governance Lifecycle (separate from A2A task lifecycle)

```
OBSERVED → ROUTED → PROPOSAL_CANONICALIZED → JUDGMENT_PENDING
  → SEAL | HOLD | SABAR | VOID
  → EXECUTION_LEASED [SEAL only]
  → EXECUTED / EXPIRED / REVOKED
  → RECEIPT_WITNESSED
```

Never infer one from the other. AAA binds them through a correlation record, not by derivation.

### P9 Detail: Extended Agent Card (CORRECTED)

Extended card should expose ONLY least-privilege capability detail. Do NOT publish internal telemetry.

**SAFE to expose:**
- Additional permitted skills for authenticated client
- Allowed content types and rate-limit tier
- Supported task modalities
- Public key references
- Availability class (AVAILABLE/DEGRADED/MAINTENANCE)

**NEVER expose by default:**
- KVM/server names, internal ports, topology
- Scar pressure, lease counts, vulnerability details
- Active execution queue pressure
- Internal agent roster, provider model details
- VAULT999 paths, receipt IDs (enables enumeration)

### Acceptance Gates — Definition of Done (Round 2)

**P0 — Agent Card truthfulness:** card validates against an exact pinned schema/proto model; advertised protocol version matches tested server behavior; advertised capabilities are implemented; unsupported operations absent or explicitly marked unsupported; CI fails on schema/capability/endpoint drift. (Note: `A2A_LIVE_WIRE_MANIFEST.json` currently declares `meta.protocol: "A2A v1.2"` while this analysis targets v1.0.0 — exact-version pinning is precisely what P0 exists for.)

**P1 — Identity & authority:** authenticated subject bound to A2A task ID and AAA session ID; tenant/interface selection cannot bypass routing policy; cross-principal read/resume/cancel/replay denied; delegation cannot increase privilege, TTL, scope, spend, or data access; direct A-FORGE invocation without a valid arifOS-issued SEAL fails closed.

**P2 — Query/analysis ingress:** valid A2A task creates a traceable AAA record carrying task ID, session ID, actor/principal, parent lineage, trace ID, expiry, and route-receipt reference; invalid schema/auth/replay rejected; no query or analysis route can reach A-FORGE.

**P6 — Consequential execution:** A-FORGE independently verifies arifOS provenance (signature/hash, task ID, actor identity, scope hash, target, nonce, expiry, operation class); seal single-use where required; any mismatch, missing field, timeout, or unavailable verifier ⇒ refusal; VAULT999 records the complete causality chain.

---

## 6. The AAA A2A Thesis (CORRECTED)

A2A v1.0 solves the interoperability problem. AAA is the federation's A2A-aware control plane — NOT the governance judge, NOT the executor, NOT the evidence ledger.

**Corrected thesis:** A2A should make AAA more interoperable, not more powerful. A2A is the network language; AAA is the traffic controller; arifOS is the policy judge; A-FORGE is the executor; VAULT999 is the witness.

Current state: AAA has an Agent Card (UNVERIFIED schema compliance) and a routing manifest (UNVERIFIED against live runtime). Message ingress is 888_HOLD.

Target state: AAA becomes a tested A2A v1.0 edge with:
- Schema-validated Agent Card
- Threat-model-reviewed authority contract
- Query/analysis ingress with trace binding
- Consequence classifier (query vs proposal vs execution)
- Governance correlation (A2A task ↔ arifOS verdict ↔ A-FORGE operation ↔ VAULT999 receipt)
- A-FORGE rejects any request without valid, scoped, unexpired arifOS SEAL

The A2A extensions in the current Agent Card need classification. AAA distinguishes optional interoperability extensions from governance-critical extensions.

An external peer may ignore an extension ONLY when its absence does not weaken identity binding, task lineage, authorization, evidence integrity, verdict scope, or execution safety.

If an extension is required to safely interpret a task, preserve provenance, or participate in a governed execution flow, AAA must either:
1. Mark the extension as `required: true` and reject peers that cannot support it; or
2. Downgrade the interaction to analysis/query-only mode with no consequential execution path.

Unknown or unsupported governance-critical extensions must fail closed.

**One-line:** A2A is the protocol. AAA is the institution that runs on the protocol.

---

## 7. Non-Negotiable Security Invariants (ADDED from audit)

### Identity is not authority

An authenticated external A2A agent is NOT automatically permitted to:
- Submit privileged action proposals
- Read sensitive internal memory
- Access internal federation topology
- Delegate authority onward
- Trigger A-FORGE
- Override an arifOS HOLD, SABAR, or VOID

```
DISCOVERED ≠ AUTHENTICATED ≠ TRUSTED ≠ AUTHORIZED ≠ JUDGED ≠ EXECUTABLE
```

| State | Meaning | Grants execution? |
|-------|---------|------------------|
| Discovered | Agent Card located | No |
| Authenticated | Credential/token verified | No |
| Trusted | Local trust domain accepts identity | No |
| Authorized | Route/capability scope permitted | No |
| Judged | arifOS evaluated a canonical action proposal | No, unless verdict is valid SEAL |
| Executable | A-FORGE independently validates SEAL scope and lease | Yes, only within bound scope |

### Capability advertisement is not permission

```
EffectiveCapability =
  ClaimedCapability
  ∩ AAAAllowedCapability
  ∩ SessionScope
  ∩ arifOSVerdictScope
```

### No verdict laundering

Never map: A2A task = "completed" → arifOS verdict = "SEAL"

These are unrelated state machines. A completed A2A task produces output. Output may contain a proposal. Proposal requires separate arifOS judgment.

### Delegation depth must be bounded

No delegated child may have greater authority, longer TTL, broader capability, or wider data access than its parent.

### Provenance chain must be complete for consequential actions

```
a2a_task_id → aaa_session_id → aaa_route_receipt_id
→ arifOS_proposal_id → arifOS_verdict_id / decision_hash
→ a_forge_lease_id → a_forge_operation_id
→ vault999_chain_id / receipt_id
```

If any link is missing, execution must fail closed for consequential actions.

---

## 8. Threat Model (ADDED from audit)

| Threat | Mitigation |
|--------|------------|
| Forged Agent Card | Schema validation + DID:web verification + trust scoring |
| Task ID replay | Idempotency keys + nonce binding |
| Cross-tenant task access | Tenant isolation + authorization scoping |
| Confused deputy routing | Capability allow-list independent of Agent Card claims |
| Verdict substitution | A-FORGE verifies arifOS signature, hash, expiry, scope |
| Artifact mutation after judgment | Content hash binding at judge time |
| Delegation escalation | Max-depth + capability attenuation per hop |
| Direct A-FORGE invocation without SEAL | A-FORGE rejects any request without valid arifOS provenance |
| Streaming race conditions | Event ordering + terminal-state closure |
| Extended Agent Card info disclosure | Least-privilege field set, no topology/telemetry |
| A2A state masquerading as governance | Separate state machines, correlation record not derivation |
| Token audience confusion (cross-service token accepted) | Strict issuer/audience/subject/nonce/expiry/client binding |
| SSRF through push callback (internal URL injected) | Allow-list callback origins; block RFC1918/loopback/link-local; sign callbacks |
| Agent Card substitution / DNS confusion (wrong card fetched) | HTTPS + hostname policy + signed identity linkage |
| Resource exhaustion (message/stream/artifact floods) | Size caps; concurrency quotas; delegation-depth limits; rate limits; cancellation TTL |
| Data exfiltration through artifacts (sensitive references returned) | Content-type policy; artifact scanning; access-controlled storage; redaction boundary |

---

## 9. Risk Conditions (Counterfactual Obligation)

This alignment analysis would FAIL if:

1. **A2A v1.0 adds mandatory governance primitives** — If a future A2A version mandates verdict-like semantics that conflict with AAA's SEAL/HOLD/SABAR/VOID, the extension mechanism would need to adapt. Current v1.0 has no such mandate.

2. **The proto normative source diverges from JSON Schema** — AAA uses JSON Schema for its Agent Card; the proto is the normative source for SDKs. If AAA ever builds an A2A SDK, it must regenerate from proto.

3. **Google deprecates A2A in favor of a competing standard** — A2A has 50+ partners (Salesforce, SAP, Atlassian, etc.) and is an open standard under a Linux Foundation-style governance. Deprecation risk is low but non-zero.

---

*DITEMPA BUKAN DIBERI — Forged, Not Given*
*arifOS F1-F13 · A2A v1.0.0 · 2026-09-12*
