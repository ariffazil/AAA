# TODO — AAA Control Plane

> **Last Updated:** 2026-05-10  
> **Session:** Governance Attestation + Federation Mesh Hardening  
> **Seal:** DITEMPA BUKAN DIBERI

---

## ⚠️ CRITICAL NOTE

The previous `TODO.md` in this repo contained **GEOX content** (GEBCO WMS, seismic layers, etc.) — a clear copy-paste error from an earlier session. That file has been replaced with the actual AAA task list below.

---

## ✅ Completed This Session

- [x] **AAA frontend deployed** to `/var/www/aaa.arif-fazil.com/` via rsync
- [x] **A2A agent cards** pushed to `sites/aaa.arif-fazil.com/.well-known/`
- [x] **Caddy routing** updated for `/a2a`, `/tasks`, `.well-known/agent-card.json`
- [x] **arifOS embodiment contracts** deployed — AAA benefits from kernel-level tool gating

---

## 🔴 P0 — Critical (Before Next Session)

### 56 Open Issues Triage
The AAA repo has **56 open issues** — the highest-risk surface in the federation.

- [ ] **Categorize** all 56 issues into P0–P4
- [ ] **Identify unknown failure modes** — A2A handshake, session state loss, token refresh races, MCP discovery inconsistency
- [ ] **Create reproduction steps** for every P0/P1 — no reproduction = not P0
- [ ] **Target:** 56 → <10 critical within 30 days

### Auto-Deploy Pipeline
Current AAA frontend deploy is **manual rsync**. This is error-prone and violates F3 Witness.

- [ ] **CI/CD for VPS static host** — GitHub Action that builds `npm run build` + rsyncs to `/var/www/aaa.arif-fazil.com/`
- [ ] **Build verification** — health check after deploy
- [ ] **Rollback path** — preserve last N dist/ backups

**Blocked by:** Needs sovereign approval for GitHub Actions secrets (server SSH key).

---

## 🟠 P1 — High (Next 7 Days)

### A2A Mutual Authentication v1.1
Current A2A uses token-based auth. Needs mTLS + capability attenuation.

- [ ] **mTLS transport** — client certificates signed by AAA CA, rotated every 24h
- [ ] **Capability attenuation** — token includes `allowed_tools: string[]` claim
- [ ] **Scope validation** — A-FORGE validates tool call against token scope before execution
- [ ] **arifOS 888_JUDGE issues scoped tokens** — sovereign authority over delegation boundaries

### Command Center Retest
The Command Center GUI was not retested after the identity registry fixes.

- [ ] **Session init flow** — verify cockpit can create and validate sessions
- [ ] **Tool orchestration** — verify 13 canonical tools are callable via UI
- [ ] **Health dashboard** — verify `/health` data maps correctly to cockpit widgets
- [ ] **Embodiment visualization** — show agent_card, lane, tier, risk leash in UI

### Session Continuity Across Reboot
AAA must persist in-flight session state to VAULT999.

- [ ] **Persist session state** before every stage transition
- [ ] **Reconstruct on restart** — read VAULT999 for active sessions
- [ ] **Checkpoint schema:** session_id, current_stage, verdict_so_far, floor_scores, pending_messages

---

## 🟡 P2 — Medium (Next 30 Days)

### Federation Mesh Visualization
- [ ] **Topology map** — live graph of all federation nodes (arifOS, GEOX, WEALTH, WELL, A-FORGE, HERMES)
- [ ] **Health overlay** — color nodes by health status (green/yellow/red)
- [ ] **A2A handshake status** — show which agents have verified treaties
- [ ] **Latency matrix** — round-trip times between all node pairs

### Operator Override Latency
F13 veto path must complete in <2 seconds.

- [ ] **Latency budget per segment:**
  - Telegram → OpenClaw: 200ms
  - OpenClaw → arifOS: 300ms
  - arifOS F13 evaluation: 500ms
  - arifOS → A-FORGE kill: 200ms
  - A-FORGE halt: 300ms
- [ ] **Total target:** <1500ms (500ms headroom)

### MCP Endpoint Registry v2.0
Unified namespace for all federation tools.

- [ ] **Namespace convention:** `<organ>_<noun>_<verb>`
- [ ] **Collision detection** in CI
- [ ] **Deprecation path** for tool renames
- [ ] **Reconcile tool counts:** arifOS 13, WEALTH 48, WELL 45, GEOX 15

---

## 🟢 P3 — Backlog (H2 2026)

### Operator Panel Governance
- [ ] **Multi-operator panel** — aggregate readiness across panel members
- [ ] **Response aggregation** — unanimous / majority / consensus modes
- [ ] **Unavailability handling** — graceful degradation when operators offline

### Third-Party Organ Conformance
- [ ] **Standardized A2A + MCP conformance tests**
- [ ] **Certification gate** — third-party organs cannot join without passing

---

## Risk Register

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| 56 issues block federation hardening | High | High | Triage session this week |
| A2A handshake unknown failures | Medium | Critical | mTLS + capability attenuation |
| Manual deploy causes downtime | High | Medium | Auto-deploy pipeline |
| Session continuity fails on reboot | Medium | High | VAULT999 checkpointing |

---

**DITEMPA BUKAN DIBERI — Control plane sovereignty is forged, not given.**
