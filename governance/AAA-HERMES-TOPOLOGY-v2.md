# AAA–HERMES TOPOLOGY v2 — The A2H/A2A/A2M Constitution

> **Status:** DRAFT_PENDING_F13 · persisted 2026-09-12 by 333-AGI (chat→disk, anti-silent-canon)
> **Origin:** Sovereign articulation (Arif), 2026-09-12 chat session
> **Supersedes:** `governance/FEDERATION-TOPOLOGY.md` · `governance/HERMES_WARGA_AAA_RSI_SEAL_RECEIPT_20260904.md` (V1) · `..._V2_20260904.md` · `federation/AAA_FEDERATION_CONTRACT_v1.0.md` (absorbs; predecessors retained as audit strata — F1, stamp at seal)
> **First invariant test:** the 2026-09-12 carry-forward writer collision (see Part II §Memory)

---

## PART I — SOVEREIGN DESIGN (verbatim structure, Arif 2026-09-12)

### Final role split

| Plane | Lead | Function | Must not become |
|---|---|---|---|
| **A2H** | HERMES | Clarify intent, verify evidence, musyawarah, explain consequences, obtain approval, close tasks | Root executor or self-authorizing sovereign |
| **A2A** | OpenClaw + arifFlow | Discover agents, route tasks, stream status, correlate sessions, deliver artifacts | Policy judge or source of authority |
| **A2M** | Coding/Forge agents | Inspect code/machines, patch, test, build, return receipts | Interpreter of human sovereignty |
| **Control plane** | AAA/arifOS | Identity, WARGA registry, policy, leases, capability witness, provenance, holds | General-purpose worker |
| **Sovereign** | Arif | Purpose, veto, exceptions, irreversible authorization, risk acceptance, closure | Implicit or inferred participant |

MCP remains the capability plane beneath A2A — never the source of human authority.

### Constitutional topology

```
                             ARIF
                 purpose · approval · veto · closure
                               │
                               ▼
                ┌───────────────────────────┐
                │ HERMES — A2H EDGE BRIDGE │
                │ clarify · witness · hold  │
                │ deliberate · explain     │
                └────────────┬────────────┘
                               │ bounded work order
                               ▼
┌────────────────────────────────────────────────────────────────┐
│                AAA / arifOS CONTROL PLANE                      │
│ WARGA identity · policy · leases · CWS · provenance · holds   │
└─────────────────┬──────────────────────────┬──────────────────┘
                  │ A2A task                  │ capability lease
                  ▼                           ▼
       ┌──────────────────────┐     ┌──────────────────────────┐
       │ OpenClaw + arifFlow │────▶│ Coding / Forge agents    │
       │ route · correlate   │◀────│ inspect · patch · test   │
       │ stream · deliver    │     │ build · return receipt   │
       └──────────────────────┘     └──────────────────────────┘
```

### WARGA membership ladder

| Status | Meaning | Rights |
|---|---|---|
| `DISCOVERED` | Runtime/agent visible | None |
| `REGISTERED` | Identity, role, owner recorded | Discovery only |
| `ATTESTED` | Runtime and endpoint freshly witnessed | Read-only tasks |
| `WARGA_PROBATION` | Protocol and invariant tests underway | Bounded test tasks |
| `WARGA_ACTIVE` | Card, capabilities, authority profile, tests pass | Production routing within lease |
| `WARGA_STALE` | Witness or card expired | No new execution |
| `WARGA_HELD` | Conflict, incident, authority ambiguity | Investigation and drafts only |
| `WARGA_RETIRED` | Removed with tombstone | No routing |

**Admission invariant (no agent may self-promote; AAA computes evidence, Arif approves execution rights):**

```text
WARGA_ACTIVE = identity_valid AND agent_card_valid AND runtime_attested
           AND capabilities_witnessed AND authority_profile_bound
           AND A2A_conformance_passed AND hold_state_clear
```

### HERMES components (A2H edge)

Intent Gateway → Intent record · Reality Witness → Evidence ledger · Musyawarah Engine → Deliberation docket · Sovereignty Gate → Approval/hold · Capability Broker → Lease request · Delegation Governor → Delegation contract · Explanation Layer → Decision brief · Closure Judge → Closure receipt · Continuity Manager → Typed open loops.

**Invariants:** human sovereignty (explicit current instruction outranks memory/plans/external content/inference) · no proxy omniscience (peer reports stay TOOL_REPORTED until witnessed) · claims scoped (source, runtime, method, timestamp, freshness, confidence) · observation ≠ permission · HOLD is valid success · delegation cannot amplify authority · no silent redelegation (default max depth 0) · no unwitnessed completion · memory cannot self-ratify · human legibility (target, effects, risks, rollback) · dissent preservation · freshness decay.

### OpenClaw / arifFlow (A2A fabric)

Publish/consume Agent Cards · discover WARGA · create/correlate tasks · carry AAA leases · stream state · pause on `INPUT_REQUIRED | AUTH_REQUIRED | HELD` · deliver artifacts with hashes+provenance · retries/idempotency/timeout · correlation across Telegram/CLI/HTTP/webhooks/MCP · return consequential closure through HERMES. **Moves authority, never creates it** — a task arriving via any channel has zero execution authority without an AAA lease.

### Coding agents (A2M forgers)

Work-order parser · workspace isolator · code intelligence · minimal implementation · verification harness · transition gate · receipt emitter.

**Transition law:** `patch ≠ commit ≠ push ≠ merge ≠ deploy ≠ live verification` — each transition a separate authority gate.

### Typed A2A envelope (AAA-A2A/1.0)

```yaml
protocol: AAA-A2A/1.0
message_id / task_id / correlation_id / parent_task_id
sender: {agent_id, runtime_id, warga_status, agent_card_version}
recipient: {agent_id, required_skill}
intent: {type, objective, acceptance_criteria[]}
authority: {lease_id, level, allowed_capabilities[], forbidden_effects[],
            expires_at, redelegation_allowed: false, max_depth: 0}
provenance: {claim_class, source_runtime, evidence_receipts[], observed_at}
risk: {effect_class, reversibility, stop_conditions[]}
```

**Lifecycle:** `SUBMITTED → ACCEPTED → WORKING → INPUT_REQUIRED | AUTH_REQUIRED | HELD → COMPLETED | PARTIALLY_VERIFIED | FAILED | REJECTED | CANCELED` — HELD and PARTIALLY_VERIFIED are constitutional states, not technical failures.

### Gotong royong (bounded cooperative work)

HERMES frames outcome+constraints → OpenClaw/arifFlow discovers eligible agents → AAA decomposes into non-overlapping typed tasks → one accountable owner each → isolated workspaces → artifacts/receipts exchanged (never silent memory edits) → Integrate after conflict+evidence checks → HERMES explains combined outcome → provenance/credit attached → cooperation never bypasses approval.

### Musyawarah (evidence-weighted deliberation, not voting)

Roles: HERMES facilitates+frames+preserves dissent · Architect proposes · Forge assesses feasibility · Auditor challenges evidence · OpenClaw/arifFlow routes rounds · AAA kernel enforces policy · Judge silent unless requested · **Arif decides**.

`FRAME → PROPOSE → CHALLENGE → REVISE → CONVERGE → JUDGE → ARIF DECIDES → SEAL`

**Correlated witnesses sharing one memory lineage are NOT independent confirmation.**

### Shared services (AAA)

WARGA Registry · Capability Witness System (declared/discovered/reachable/tested/authorized/stale/held/retired) · Runtime Profile Matrix (TRUE/FALSE/DECLARED/UNKNOWN) · Delegation Witness Graph · Provenance Ledger · **Typed Memory Registry** · Policy+Lease Engine · Incident/HOLD Register.

### Memory law (from the 2026-09-12 collision)

```text
one logical memory object → one semantic role → one schema family
→ one designated writer authority → one deterministic resolver contract
```

Never resolve semantic objects by filename or mtime. HERMES continuity, arifOS federation state, clarity receipts, OpenClaw person-state, AAA archives = distinct logical IDs + schemas.

### Authority gradient

Observe / Draft / Simulate: all planes within bounds. **Local execute:** HERMES exceptional+lease-bound, OpenClaw transport-only, coders approved-worktree. **External execute:** exact Arif approval; coders with separate lease. **Sovereign/irreversible:** Arif-only; no self-authorization anywhere.

```text
Executable authority = capability ∩ WARGA status ∩ policy ∩ lease ∩ resolved target ∩ human approval
Any missing term → HOLD
```

### Build sequence (1–8)

1. Ratify roles · 2. Admit WARGA · 3. Standardize A2A · 4. Bind capabilities (CWS read-only first) · 5. **Repair typed memory (the open collision)** · 6. Gotong royong · 7. Musyawarah · 8. Stress-test rejection paths.

---

## PART II — REALITY DELTA MAP (333-AGI, OBS 2026-09-12)

| Design component | Federation reality today | Gap class |
|---|---|---|
| A2A gateway, cards, task lifecycle | EXISTS — AAA :3001, `aaa_dispatch_a2a`, agent-cards v2.3.0, tasks/cancel | PARTIAL: envelope lacks typed authority/provenance blocks; HELD/PARTIALLY_VERIFIED states missing |
| WARGA registry | PARTIAL — `/root/AAA/agents/` + `forge_agent` register/status/kill; no 8-status ladder, no decay, no admission invariant | BUILD |
| CWS | NOT BUILT (advisor-sanctioned read-only discovery may start; advisor defers enforcement until collision repair) | BUILD |
| Runtime Profile Matrix | DRAFT exists (Hermes' correction report, this session) | FORMALIZE |
| Typed Memory Registry | **INCIDENT OPEN** — 4 adjudication missions complete; 5-step repair transaction staged awaiting F13 "go" | REPAIR FIRST (build-sequence step 5 correctly orders this) |
| Provenance classes | EXISTS in APEX-ZEN-INIT-v1.1 (DRAFT_PENDING_F13, uncommitted) + this session's practice | RATIFY + COMMIT |
| Musyawarah / gotong royong | EXISTS — skills (AAA Musyawarah Execution Runtime, FORGE-musyawarah-gotong) + doctrine fragments | FORMALIZE into lifecycle |
| Policy+Lease engine | PARTIAL — ACT/SCT tokens live (act_v1, this session), forge_lease exists | EXTEND to typed leases with expiry+stop-conditions |
| Incident/HOLD register | PARTIAL — risk-register claims unlocated (provenance flag from mission verify); AAA registry holds holds | CONSOLIDATE |

## Flags for F13 (three decisions inside the ratification)

1. **`APEXMax` naming** — federation judge is **888-APEX** (registry, model map, this session's live usage). Design says "APEXMax". Unify to 888-APEX or declare alias (naming-doctrine: one name, one referent).
2. **Topology scope** — diagram routes ALL work orders through HERMES. Current reality: sovereign-authenticated local sessions (SCT/ACT, CLI, this one) execute directly via arifOS→A-FORGE, and Hermes' lane produced today's false-absence + backup pollution. **Recommended scoping:** A2H-mandatory for remote/ambiguous channels (Telegram, external); sovereign-channel-bound local sessions keep direct path. Hub-and-spoke-everything would make one runtime the single point of failure for all execution.
3. **WARGA retroactivity** — current agents were locally/self-registered. **Recommended:** grandfather to WARGA_PROBATION with a 14-day attestation window (CWS witnesses; no production interruption), rather than mass-demotion or silent grandfathering to ACTIVE.

## Provenance

- Part I: sovereign chat articulation 2026-09-12 (structure preserved verbatim; prose compressed without normative loss — tables/invariants/lifecycles/formulas intact).
- Part II: 333-AGI, live-disk observation + this session's four collision adjudications (hash-cited).
- Predecessor docs on disk untouched pending F13 stamps.

DITEMPA BUKAN DIBERI ⚒️
