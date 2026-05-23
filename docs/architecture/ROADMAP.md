# AAA — Roadmap: Next Horizon (180-Day)

> **Roadmap Name:** ARIFOS_NEXT_HORIZON_2026  
> **Strategic Verdict:** APPROVED FOR PLANNING  
> **Execution Verdict:** HOLD until repo contracts and schemas are frozen  
> **Role:** Identity, agent registry, OAuth/MCP authorization, control plane  
> **Seal:** DITEMPA BUKAN DIBERI

---

## North Star

Make AAA the hard boundary for identity and scope. Every call is bound to actor + purpose.

---

## The 10 Non-Negotiable Invariants

1. arifOS judges.
2. AAA identifies.
3. GEOX witnesses earth.
4. WEALTH witnesses capital.
5. A-FORGE executes only after verdict.
6. VAULT999 records.
7. ARIF may veto.
8. No agent self-authorizes.
9. No hidden irreversible action.
10. No evidence, no SEAL.

---

## Horizon 0 — Days 0–14: Canon Lock 🧊

**Goal:** Enter cleanup + contract-freeze phase before major feature expansion.

AAA currently carries **56 open issues** and broad control-plane surfaces. Freeze first.

| Deliverable | Output |
|-------------|--------|
| Issue triage | 56 → <10 critical |
| `REPO_AUTHORITY_MATRIX.md` | What AAA may own / must not own |
| Tool inventory | Remove duplicates / dead surfaces |
| Schema inventory | Map all agent/session/delegation schemas |

### Gate
No new features until contracts are frozen.

---

## Horizon 1 — Days 15–45: Security + Session Spine 🔐

**Goal:** Normalize all agent cards. No anonymous agent execution.

| Phase | Task | Why |
|-------|------|-----|
| H1 | Normalize all agent cards | No anonymous agent execution |
| H1 | Implement scoped session tokens | Every call bound to actor + purpose |
| H1 | Add per-tool scope matrix | Agent cannot call tools outside role |

### Deliverables

| Deliverable | Output |
|-------------|--------|
| `/agents/agent_cards/` | Canonical agent card directory |
| `/schemas/agent_card.schema.json` | Identity, tier, scopes, allowed organs |
| `/schemas/session.schema.json` | Actor, scope, expiry, chain_id |
| `/schemas/delegation.schema.json` | Consent + delegation ledger |
| `/auth/oauth_resource_metadata.json` | OAuth 2.1 Protected Resource Metadata |
| `/auth/scope_matrix.yaml` | Per-tool scope matrix |

### Security Requirements

MCP authorization guidance requires:
- Protected MCP servers act as OAuth 2.1 resource servers
- Protected Resource Metadata publication
- Token audience validation
- PKCE for authorization code protection
- Scope minimization

Guard against: confused-deputy attacks, token passthrough, SSRF, session hijacking, local server compromise.

---

## Horizon 2 — Days 46–90: Deterministic Judge ⚖️

**Goal:** LTL trace rules, consent ledger hardened.

| Phase | Task | Why |
|-------|------|-----|
| H2 | OAuth 2.1 / Protected Resource Metadata readiness | Required for remote MCP hardening |
| H2 | Consent + delegation ledger | Prevent confused-deputy flows |

### Deliverables

| Deliverable | Output |
|-------------|--------|
| LTL trace rules | Session + delegation chain validity |
| Consent ledger | Immutable delegation records in VAULT999 |

---

## Horizon 3 — Days 91–135: Semantic Federation 🌍💰

**Goal:** Agent cards carry cross-domain evidence scopes.

| Deliverable | Output |
|-------------|--------|
| Cross-domain scope extensions | Agent card includes GEOX/WEALTH evidence permissions |
| Federation mesh visualization | Live topology of all organs + handshake status |

---

## Horizon 4 — Days 136–180: Self-Healing + Public Release 🛠️

**Goal:** Agent revocation + quarantine. Kill compromised agents cleanly.

| Phase | Task | Why |
|-------|------|-----|
| H3 | Agent revocation + quarantine | Kill compromised agents cleanly |

### Deliverables

| Deliverable | Output |
|-------------|--------|
| Revocation protocol | Instant token invalidation + agent quarantine |
| Public docs cleanup | README, AGENTS.md, API docs |
| MCP registry readiness | Publish AAA as authorization server |
| Release tag `vNext-Horizon-0` | All repos tagged |

---

## What to Build Next

Identity → Evidence → Formal Verdict → Sandboxed Execution → Immutable Seal

## What to Avoid

- More overlapping dashboards.
- More untyped tools.
- More prompt-only governance.
- More agent autonomy language without execution contracts.

## What Wins

- Deterministic checks.
- Typed schemas.
- Scoped authority.
- Evidence contracts.
- Human veto preserved.

---

*DITEMPA BUKAN DIBERI — Identity is forged, not given.*

*SEALED: 2026-05-10 | AAA Control Plane — Next Horizon APPROVED FOR PLANNING*
