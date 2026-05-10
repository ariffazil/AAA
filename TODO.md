# TODO — AAA Control Plane

> **Roadmap:** ARIFOS_NEXT_HORIZON_2026  
> **Execution Status:** HOLD until contracts frozen  
> **Last Updated:** 2026-05-10  
> **Seal:** DITEMPA BUKAN DIBERI

---

## ✅ Embodiment Attestation (Completed Earlier Today)

- [x] A2A agent cards pushed to `.well-known/`
- [x] Caddy routing updated for `/a2a`, `/tasks`, agent-card
- [x] arifOS embodiment contracts deployed

---

## 🔴 P0 — Horizon 0: Canon Lock (Days 0–14)

**Gate: No new features until contracts are frozen.**

### Issue Triage
- [ ] **56 open issues → <10 critical** — highest priority action in federation
- [ ] **Categorize:** P0 (HALT) / P1 (CRITICAL) / P2 (HIGH) / P3 (MEDIUM) / P4 (LOW)
- [ ] **Identify unknown failure modes** — A2A handshake, session loss, token races
- [ ] **Close/consolidate duplicates**

### Authority Freeze
- [ ] **Create `REPO_AUTHORITY_MATRIX.md`** — what AAA may own / must not own
- [ ] **Tool inventory** — remove duplicates / dead surfaces
- [ ] **Schema inventory** — map all agent/session/delegation schemas
- [ ] **Auto-deploy pipeline** — GitHub Action for VPS static host (still manual rsync)

---

## 🟠 P1 — Horizon 1: Security + Session Spine (Days 15–45)

**Gate: No execution without actor, scope, verdict, trace.**

### Agent Cards
- [ ] **Normalize all agent cards** — no anonymous agent execution
- [ ] **Create `/schemas/agent_card.schema.json`** — identity, tier, scopes, allowed organs
- [ ] **Create `/agents/agent_cards/`** — canonical directory

### Session & Scope
- [ ] **Create `/schemas/session.schema.json`** — actor, scope, expiry, chain_id
- [ ] **Create `/schemas/delegation.schema.json`** — consent + delegation ledger
- [ ] **Implement scoped session tokens** — every call bound to actor + purpose
- [ ] **Add per-tool scope matrix** — agent cannot call tools outside role

### OAuth / MCP Security
- [ ] **Create `/auth/oauth_resource_metadata.json`** — OAuth 2.1 Protected Resource Metadata
- [ ] **Create `/auth/scope_matrix.yaml`** — per-tool scope matrix
- [ ] **Token audience validation** — validate tokens for intended audience
- [ ] **PKCE for authorization code protection**
- [ ] **Guard against confused-deputy attacks**
- [ ] **Guard against token passthrough, SSRF, session hijacking**

---

## 🟡 P2 — Horizon 2: Deterministic Judge (Days 46–90)

**Gate: Consent + delegation ledger hardened.**

- [ ] **OAuth 2.1 readiness** — Protected Resource Metadata full implementation
- [ ] **Consent + delegation ledger** — immutable records in VAULT999
- [ ] **LTL trace rules** — session + delegation chain validity
- [ ] **Session continuity across reboot** — persist to VAULT999 before stage transition

---

## 🟢 P3 — Horizon 3: Semantic Federation (Days 91–135)

**Gate: Agent cards carry cross-domain evidence scopes.**

- [ ] **Cross-domain scope extensions** — agent card includes GEOX/WEALTH evidence permissions
- [ ] **Federation mesh visualization** — live topology + handshake status
- [ ] **MCP Endpoint Registry v2.0** — unified namespace, collision detection

---

## 🔵 P4 — Horizon 4: Self-Healing + Release (Days 136–180)

**Gate: Kill compromised agents cleanly.**

- [ ] **Agent revocation protocol** — instant token invalidation
- [ ] **Agent quarantine** — isolated sandbox for compromised agents
- [ ] **Public docs cleanup** — README, AGENTS.md, API docs
- [ ] **MCP registry readiness** — publish AAA as authorization server
- [ ] **Release tag `vNext-Horizon-0`**

---

**DITEMPA BUKAN DIBERI — Identity is forged, not given.**
