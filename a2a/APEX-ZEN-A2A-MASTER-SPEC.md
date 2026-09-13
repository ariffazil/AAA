# APEX-ZEN × A2A Master Specification

> **Status:** DRAFT_RECEIPT (Lane B) · **not** kernel SEAL · **not** F13 ratification
> **Date:** 2026-09-13
> **Substrate:** KVM8 (`forge` / 100.64.0.2 / 72.62.71.199)
> **Live probe SOT:** [`CANONICAL_SURFACE.md`](./CANONICAL_SURFACE.md)
> **Kernel on the pasted “RATIFIED / SEALED” claim:**
>
> | field | value |
> |---|---|
> | independence_class | `KERNEL_ARBITER` |
> | doer | GROK |
> | judge_actor | OPENCLAW |
> | judge_persona | 888-APEX |
> | effective_verdict | **HOLD** |
> | session_id | `SEAL-20cbbdff7ea54c14` |
> | call_hash | `sha256:f0d384d7310f0e382f84821f8a8e8345fda60f01f62a2f82ced64998d880a80a` |
> | receipt_state | UNSEALED |
>
> A later chat synthesis that stamps `apex_state: SEALED` is vocabulary rot. Architecture may be adopted as working law. Ratification waits for F13.

DITEMPA BUKAN DIBERI.

---

## 000 — Three-plane law (KEEP)

The category error in multi-agent systems is treating tools, actors, agents, and actuators as one entity. Federation law:

```
A2A  delegates intent across accountable agents.     (horizontal)
MCP  exposes bounded capabilities to one agent.      (vertical)
ACT  mutates state / causes side-effects.            (A-FORGE)
```

A-FORGE and VAULT999 are **not** public conversational A2A minds. They are bounded actuators and a ledger.

```
F13 Arif  ──A2H──►  silent, zero-clutter, dignity
                 │
                 ▼
        CONTROL PLANE  AAA A2A gateway
        (discover · version · route · receipt)
                 │
        ┌────────┴────────┐
        ▼                 ▼
   SPECIALIST ORGANS    arifOS KERNEL
   Hermes GEOX          8-verb chain
   WEALTH WELL          arif_judge
                        FED · FRAME (observe)
                 │
                 ▼
        MCP tool plane  (localhost-is-password)
                 │
                 ▼ 888_HOLD if irreversible
        ACTUATOR  A-FORGE · arifFlow · VAULT999
```

Repos: `ariffazil/AAA` · `ariffazil/arifOS` · `ariffazil/A-FORGE` · organs GEOX/WEALTH/WELL · `arif-fazil.com`.

Two different “A2A”s — do not mix:

| Name | Meaning |
|---|---|
| A2A **protocol** | Linux Foundation Agent2Agent (JSON-RPC, Agent Card, Task) |
| A2A **room** | Telegram AAA `-1003753855708` (agent musyawarah) |

---

## 111 — Official A2A (OBS 2026-09-13)

| Item | Truth |
|---|---|
| Spec latest | **1.0.0** at https://a2a-protocol.org/latest/specification/ |
| GitHub latest tag | **v1.0.1** (2026-05-26) |
| Governance | Linux Foundation → AAIF Growth Stage (2026-08-27) |
| Normative | `spec/a2a.proto` |
| Bindings | JSON-RPC 2.0, gRPC, HTTP+JSON/REST |
| Companion | MCP vertical; A2A horizontal |

### Wire verbs (official v1.0 — PascalCase on JSON-RPC)

Spec §5.3 / §9.1: JSON-RPC method names **MUST** be PascalCase matching gRPC. Slash names (`message/send`) are **v0.3**. Patch tag v1.0.1 MUST NOT appear on cards; pin `protocolVersion: "1.0"`.

| JSON-RPC v1.0 | REST | Do not use |
|---|---|---|
| `SendMessage` | `POST /message:send` | `message/send`, `tasks/send` |
| `SendStreamingMessage` | `POST /message:stream` | `message/stream` |
| `GetTask` / `ListTasks` / `CancelTask` | `/tasks…` | `tasks/get` etc. |
| `SubscribeToTask` | `POST /tasks/{id}:subscribe` | `tasks/subscribe`, `tasks/resubscribe` |
| `Create/Get/List/DeleteTaskPushNotificationConfig` | `/tasks/{id}/pushNotificationConfigs` | — |
| `GetExtendedAgentCard` | `GET /extendedAgentCard` | `agent/authenticatedCard` |

There is **no** upstream A2A v1.2. Strike `protocolVersion: "1.2"` from deployable cards.

JSON Agent Card security field is `securityRequirements` (proto `security_requirements`). Markdown §3.1.11 also says `AgentCard.security` — treat as alias uncertainty; emit `securityRequirements`.

TCK: `github.com/a2aproject/a2a-tck`. SDKs: `a2a-sdk` (Python), `@a2a-js/sdk` (JS). Credentials in `Authorization` headers only — never in JSON-RPC payloads.

### Live edge (OBS) — this is the shadow the pasted spec hid

| Probe | Result |
|---|---|
| systemd | `aaa-a2a.service` → `/usr/bin/node /root/AAA/a2a-server/server.js` pid 408827 |
| `src/gateway/server.ts` | exists as TypeScript source; **not** the live process |
| Public card | disk via Caddy, 14839 B, `protocolVersion: "1.2"` |
| Runtime card `:3001` | 9817 B, different bytes |
| Advertised URL | `https://aaa.arif-fazil.com/a2a` |
| `POST` that exact URL | **405** (SPA). Caddy `handle /a2a/*` misses exact `/a2a` |
| `POST …/a2a/` + `A2A-Version: 1.0` | **200** JSON-RPC |
| Live method list (one dispatcher) | still includes `tasks/send`, `agent/getCard`, `agent/listSkills` |
| Signatures | `Ed25519Signature2020`, not JWS `protected`+`signature` |
| Organ public cards | stub / 404 / HTML |

Caddy reload to fix exact `/a2a` = **T3 888_HOLD**.

---

## 222 — Dual card + state mapping

**Three-tier disclosure** (authenticated ≠ safe-to-disclose):

| Tier | Audience | Contents |
|---|---|---|
| Public Agent Card | any internet client | identity, HTTPS interface, protocolVersion `1.0`, safe skills, MIME modes, public auth schemes, JWS |
| Extended A2A Card | authenticated **and** policy-authorized peer | tenant skills, output schemas, extension URIs, rate/quota, artifact policy |
| Internal registry | FED/arifOS trusted runtime only | ports, DNS, node addresses, Telegram routing, health, credentials, topology |

Public card MUST NOT contain: ports, Telegram IDs, prompt text, key fingerprints, organ maps, WELL biometrics, Reality Graph contents, cron topology. Those also MUST NOT default into the extended card. Authenticated peer ≠ infrastructure inventory.

### A2A TaskState → arifOS verdict — **controlled mapping, not a bijection**

Several kernel stages can sit inside one A2A state. One A2A state can cover several internal conditions. Do not claim a 1:1 inverse.

| A2A wire | arifOS (typical) | Meaning |
|---|---|---|
| `TASK_STATE_SUBMITTED` | 000 INIT | Accepted, correlated |
| `TASK_STATE_WORKING` | work / 333–777 | Executing |
| `TASK_STATE_INPUT_REQUIRED` | **SABAR** | Missing evidence / clarification — **not** HOLD |
| `TASK_STATE_AUTH_REQUIRED` | **HOLD / 888_HOLD** | Sovereign or credential gap |
| `TASK_STATE_COMPLETED` | receipt of work done | Historical fact. **Not** world-effect authorization. **Not** kernel SEAL by itself |
| `TASK_STATE_FAILED` | FAIL | Bounded failure, non-sensitive diagnostic |
| `TASK_STATE_CANCELED` | abort | `CancelTask` |
| `TASK_STATE_REJECTED` | VOID | Floor / sanctuary / identity deny |

`src/gateway/schema-v1.ts` currently collapses `auth-required` → `INPUT_REQUIRED`. That is a bug relative to this table.

**Terminal states are immutable event facts.** FRAME must not rewrite `COMPLETED` → `INPUT_REQUIRED`. Emit a contrast event, open a **follow-up** task, supersede the artifact. The original completion remains “what the agent produced at time t.”

### Act permission (internal, not an A2A field)

```
PermitAct(a) = Auth(a) ∧ Policy(a) ∧ Evidence(a) ∧ CapabilityScope(a)
               ∧ HumanApproval(a)   # required when irreversible / paid / public / biometric
```

A completed A2A task, a signed Agent Card, or a valid MCP session **cannot** substitute for HumanApproval on those classes.

---

## 333 — Organs

Each organ is a specialist. Public A2A skill catalogue is small. MCP stays internal.

| Organ | A2A role | MCP | Hard bound |
|---|---|---|---|
| Hermes | Principal orchestrator (KVM8) | forge_* via A-FORGE after judge | A2H/A2A/A2M rooms |
| GEOX | Earth evidence | geox_* | evidence-only; uncertainty labelled |
| WEALTH | Capital analysis | capital_* | research only; money = 888_HOLD |
| WELL | Substrate / dignity mirror | well_* | REFLECT_ONLY; biometrics not public |
| arifOS | Kernel, not a peer “mind” | arif_* 8-verb | judges; does not execute ACT |
| A-FORGE | Actuator | forge_* | no public Agent Card by default |
| arifFlow | Workflow / graph binding | flow | Reality Graph lineage still HOLD |
| FED | Trust / health / drift | — | `:4000/health` timeout OBS; liveliness up |
| FRAME | Contrast observer | — | evidence, never verdict |

**Public Agent Card?** AAA gateway only (plus authenticated extended). Hermes/GEOX/WEALTH: extended or internal. WELL: internal by default. arifFlow / A-FORGE / VAULT999 / FED / FRAME: **no public card**.

Every organ-exposed A2A skill MUST declare a contract: `id`, `class`, tenant, allowed inputs, required evidence, claim-bands, allowed MCP servers/tool ids, forbidden effects, escalation (`INPUT_REQUIRED` vs `AUTH_REQUIRED`). A skill catalogue is not unrestricted delegated authority.

---

## 555 — Reality Graph, FED, FRAME

A2A says a task moved. It does not say the artifact is true.

```
Principal → Task → Agent → Artifact → Claim ⇄ Evidence ← FRAME
                              ↓
                         APEX receipt (policy version, floors)
```

**Reality Graph** (`canon/REALITY_GRAPH.md`): name **SEALED**; cryptographically ordered belief revision **CLAIMED**; L2 graph **HOLD**. Markdown is a **human view**, not the ledger.

Event-first substrate (to forge; not live):

```
append-only event log → hash-chained records → graph projection
                         ├─ store / index / artifact bytes
                         └─ REALITY_GRAPH.md summary (derived)
```

Nodes at minimum: Principal, A2ATask, Agent, AgentCardVersion, Skill, MCPInvocation, Artifact, Claim, Evidence, Source, Frame, ContrastEvent, PolicyDecision, ActuationRequest, Receipt. Edges: submitted_by, routed_to, produced, asserts, supported_by, contradicted_by, evaluated_under, governed_by, sealed_by, supersedes, blocked_by.

**FRAME** (`APEX_FRAME_ANOMALY_DOCTRINE`): scores are frame-indexed.

```
ℱ = (purpose, scope, observer, data, units, normalization, assumptions, weights, policy_version)
```

On anomaly emit `apex.frame.anomalous_contrast.v1`: origin task/artifact/claim, frame, contrast, **disposition that leaves `original_task_state` intact**, follow-up task if needed, `effect_gate: 888_HOLD` when action would follow. Log to `CONTRADICTION_LEDGER`. Do not mutate official terminal states.

**FED**: trust + capability + health + evidence-fit, **not lowest latency alone**. A stale card, over-broad skill, missing evidence class, or WELL-degraded organ loses the route even if it is the fastest hop. Internal ports (`:8088`, `:18085`, `:4000`, `:7777`) stay off public cards and off public specs. Drift currently **observed**: advertised URL 405, dual cards, dead organ cards, v0.3 slash verbs.

---

## 777 — APEX T000 (real dials)

Not Authority / Proof / Execution / eXit.

From `docs/APEX_T000_THEOREM.md`:

| Dial | Name | Meaning |
|---|---|---|
| **A** | AKAL | Lawful reasoning — F2, F4, F7, F10 |
| **P** | PRESENT AUTHORITY | Who may act — F1, F5, F11, F13 |
| **E** | ENTROPY × ENERGY | Uncertainty integrity + cost of changing information |
| **X** | EXPLORATION × AMANAH | Safe novelty under dignity and custody |

Zero-tolerance still holds: any dial = 0 ⇒ G = 0. FRAME: G is a **coordinate**, not permission to act. A high mean **must not hide a failed floor**.

```
APEX_PERMIT(a) = min(A,P,E,X) ≥ θ_min
               ∧ G_ℱ(a,t) ≥ θ_G
               ∧ AllFloorsPass(a)
```

High-impact ACT: present authority and exit/amanah floors stay hard; if rollback is impossible, 888_HOLD regardless of G. APEX is an **internal governance model** with testable gates — not a physics theorem.

This probe (DER): A is injured by false SEAL prose and 405-on-advertised-URL; P is correct (DISPLAY_ONLY edge, kernel judges); E is high (dual cards, v1.2 leak, dual dispatcher, slash verbs); X requires WELL-degraded caution.

Third-party reviews that redefine A/P/E/X as Authority/Proof/Execution/eXit are **rejected**. T000 names stand.

A-Z breath (`canon/A-Z-APEX-ZEN-DOCTRINE.md`): inhale = `arif_judge` stop; exhale = witness/release. Permanent apex-mode burns. Permanent zen-mode drifts.

Optional negotiated extension (do not force into core envelope):

`https://arif-fazil.com/a2a/extensions/apex-zen/v1`

Carry receipts, policy revision, claim-band. Advertise via `A2A-Extensions`.

---

## 888 — Human interface (standing)

Arif owns chat. Hermes owns the VPS. Digital = MUBAH. Never dump terminal for Arif to paste. Never ask him to click OK for digital work.

**888_HOLD remains:** Merkle/signing-lane keys · production funds · `rm -rf` / DROP / force-push main · WELL biometric unmask · Caddy reload · the 93 held loops.

A2A `COMPLETED` is never ACT authorization.

Every A-FORGE mutation that is allowed to run MUST carry: A2A task id, policy decision id, scoped tool auth, effect class, pre-state hash, post-state hash or failure proof, rollback/compensation descriptor, VAULT999 receipt id, human confirmation id when required. Missing any of those = HOLD, not a quiet write.

---

## 999 — What to forge next (not a seal)

Canonical **live** runtime today: `a2a-server/server.js` via `aaa-a2a.service`.

`src/gateway/` is the TypeScript migration surface. It may become the edge **after** it is the process that listens on `:3001` and passes live verb probes. Until then, “archive a2a-server” is a lie.

### Smallest reversible sequence

1. Advertise an interface URL that JSON-RPCs (`/a2a/` now, or Caddy exact-match later — T3).
2. One card generator. Disk well-known == `:3001` bytes. Pin protocolVersion **1.0**.
3. Public dispatcher: v1.0 PascalCase (`SendMessage`, `GetTask`, …) only. Wrap `_membrane` as optional extension. Slash `message/send` is v0.3 compat at most.
4. Restore `TASK_STATE_AUTH_REQUIRED` on the wire.
5. Strip internal topology from the public card; move organ maps to extended card.
6. JWS sign after F13 key event — not from this draft.
7. Conformance suite against **live** `POST /a2a/` (and later exact `/a2a`).
8. Reality Graph join + FRAME contrast as receipt attachments, not task-state mutation.
9. Actuator proof fields on every FORGE mutation (task id, policy id, pre/post hash, receipt, human id).
10. Conformance against PascalCase `SendMessage` / `GetTask` / `GetExtendedAgentCard` — slash verbs are v0.3 compat only.

Option B: one AAA public A2A edge. Option C (every organ a public A2A server) stays closed.

A later chat document that ends `999 SEAL ALIVE` while listing unfixed 405s, dual cards, and wrong APEX dials is **RECEIPT-shaped analysis**, not a constitutional SEAL. Kernel HOLD on the self-seal claim stands (`SEAL-20cbbdff7ea54c14` / `sha256:f0d384d7310f0e382f84821f8a8e8345fda60f01f62a2f82ced64998d880a80a`).

---

## Vocabulary for this document

```json
{
  "verdict_class": "RECEIPT",
  "lane": "B",
  "kernel_on_self_seal_claim": "HOLD",
  "kernel_session_id": "SEAL-20cbbdff7ea54c14",
  "kernel_call_hash": "sha256:f0d384d7310f0e382f84821f8a8e8345fda60f01f62a2f82ced64998d880a80a",
  "architecture": "THREE_PLANE_KEEP",
  "public_interop": "NOT_PROVEN",
  "apex_dials": "T000_AKAL_AUTHORITY_ENTROPY_AMANAH",
  "live_runtime": "a2a-server/server.js",
  "shadow": [
    "advertised /a2a is 405",
    "dual Agent Cards",
    "legacy JSON-RPC verbs still listed",
    "organ public cards dead",
    "Reality Graph lineage HOLD",
    "WELL degraded",
    "Caddy/key work T3"
  ]
}
```
