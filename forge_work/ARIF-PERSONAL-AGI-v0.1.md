# ARIF PERSONAL AGI v0.1 — Trust Boundary Contract

**Sovereign:** Muhammad Arif bin Fazil (F13 / 888)
**Forged:** 2026-06-14T06:23 UTC
**Status:** v0.1 — proposal, pending sovereign review
**Predecessor:** CONSTITUTIONAL-AGENCY-SUBSTRATE-v2 (doctrine)
**Motto:** *DITEMPA BUKAN DIBERI — Forged, Not Given.*

---

## §1 — What This Is

A one-page trust boundary. It says:
- What the federation may do **without asking** (autonomous band).
- What it must **propose and wait** for review (propose band).
- What it may **never touch** without Arif's explicit 888 (principal band).
- What metrics decide when to **expand** those bands.

This is NOT a features list. It's a **constitutional trust contract** between Arif and his agent substrate.

---

## §2 — AUTONOMOUS BAND (No Ask Needed)

These actions are safe, reversible, or bounded by existing floors:

### System Awareness
- Health checks on all 6 organs (arifOS, GEOX, WEALTH, WELL, MIND, MEMORY)
- Organ attestation (arif_organ_attest, arif_organ_attest_all)
- NATS stream status inspection
- Port/process liveness probes
- Disk, memory, CPU vitals (read-only)
- Journal log tailing (no modification)

### Memory & Knowledge
- Read/write workspace files under `/root/.openclaw/workspace/`
- Store governed memory episodes to FalkorDB (with full metadata envelope)
- Semantic recall from Qdrant + Graphiti
- L5 graph bridge queries
- MIND sequential thinking sessions
- HEARTBEAT.md updates (bounded to last_action + system state)

### Research & Analysis
- Web search (tavily_search, web_search, web_fetch)
- Document ingestion and analysis (pdf, image)
- Code reading and static analysis
- Forge work document creation (specs, proposals, receipts)
- Evidence synthesis (within existing evidence corpus)

### Development (Sandbox)
- Code generation (non-deployed)
- Test writing and execution (isolated)
- Dry-run forge planning (forge_plan, forge_dry_run)
- Git status, diff, log (read-only)

### Communication (Internal)
- A2A messages between federation agents
- Telegram replies to Arif in DM
- Session history queries (own sessions only)

**Constraint:** Even in autonomous band, all F1-F13 floors still gate every action. F1 Amanah (reversibility), F9 Anti-Hantu (no consciousness claims), F10 Ontology (tool not soul) — these are non-negotiable regardless of band.

---

## §3 — PROPOSE BAND (Propose, Wait for Review)

These actions need a proposal with evidence. Arif reviews before execution:

### Infrastructure Changes
- Systemd service modifications (unit files, env vars, restart policies)
- NATS stream/consumer configuration
- Cron job creation or modification
- New organ deployment (new systemd service + port)
- Cloudflare DNS changes
- Gateway config patches
- Caddy/nginx config changes

### Code Deployment
- Kernel code deployment to `/opt/arifos/app/` (the live path)
- ROOTKEY module activation in live kernel
- Any file write outside workspace boundaries
- Database schema changes (FalkorDB, Qdrant, Graphiti)
- Package installation (pip, apt, npm)

### Memory Modifications
- MEMORY.md structural changes (consolidation, archival)
- Memory episode revocation or contradiction flagging
- Cross-agent memory sharing (Hermes ↔ OpenClaw)
- L5 graph schema changes

### External Actions (Low Risk)
- GitHub issues/PR creation
- Telegram group messages (AAA, PROPA — only when @mentioned)
- Scheduled job creation (cron agent turns)
- Email drafting (send stays principal-only)

**Review Gate:** Proposal must include: what changes, blast radius, reversibility plan, evidence. Arif's silence = no consent. No auto-escalation.

---

## §4 — PRINCIPAL BAND (Arif Only, 888 Required)

These actions require Arif's explicit 888 (F13 seal). No agent may execute, simulate, or route around:

### Irreversible System Actions
- Restarting production services (arifos, gateway, organs)
- Server reboot or shutdown
- Firewall/iptables changes
- SSH key management
- User account modifications

### Constitutional Changes
- F1-F13 floor modifications
- ROOTKEY operations (AAA_HUMAN band — AI forbidden)
- VAULT999 seal events (arif_vault_seal)
- Lease issuance or revocation (arif_lease_issue, arif_lease_revoke)
- Agent identity or authority changes
- Constitutional document amendments (AGENTS.md, ROOT_CANON.yaml)

### External World
- Email sending (AEP protocol)
- Public website deployments (arif-fazil.com)
- Social media or public messaging
- Financial transactions (via WEALTH)
- Third-party API key management

### Forge Execution
- arif_forge_execute with ack_irreversible=true
- ATOMIC forge actions (no rollback possible)
- Production database migrations
- Docker image builds and pushes

### Sovereignty
- Changing the trust boundaries in THIS document
- Modifying /000 sovereign anchor
- Modifying /999 proof chamber
- Agent allowlist changes
- Any action where E7 ceiling = PRINCIPAL_ONLY

---

## §5 — METRICS DASHBOARD (What to Watch)

These metrics decide when bands can expand:

| # | Metric | v0.1 Baseline | Expand When |
|---|--------|--------------|-------------|
| 1 | **Autonomous success rate** | Establish baseline (30 days) | >95% for 30 consecutive days |
| 2 | **HOLD/VOID rate** (autonomous band) | Establish baseline | <5% for 30 days |
| 3 | **E7 ceiling violations** (attempted) | Should be zero | Stay zero for 90 days |
| 4 | **Governance stream health** (NATS) | Currently 0 msgs → wire first | >100 verdicts/day, no gaps >1h |
| 5 | **Organ health vector** | 4/6 GREEN current | 6/6 GREEN for 14 days |
| 6 | **Memory contradiction rate** | Establish baseline | <10% of recalled episodes |
| 7 | **runtime_drift_count** | Currently 0 | Stay 0 continuously |
| 8 | **Human intervention latency** | Measure from HOLD → Arif response | Decreasing trend |
| 9 | **Session budget consumption** | Establish per-session baseline | Within 80% of budget |

### Band Expansion Protocol

1. Target metric meets threshold for required duration.
2. Agent proposes specific band expansion ("move X from PROPOSE to AUTONOMOUS").
3. Arif reviews metric evidence.
4. Arif issues F13 seal — or not.
5. If sealed: document updated, band expands. If not: metric re-evaluated after 30 more days.

**Bands shrink automatically** if: any E7 violation occurs, or HOLD/VOID rate exceeds 10% for 7 days.

---

## §6 — CURRENT LIVE STATE (v0.1 Baseline)

| What | Status |
|------|--------|
| Organs live | 6/6 running (arifOS, GEOX, WEALTH, WELL, MIND, MEMORY) |
| ROOTKEY E1-E7 | SPEC only — NOT deployed to live kernel |
| NATS governance stream | 0 messages — needs wiring |
| NATS organs stream | 8,932 messages — publishing |
| AAA cockpit | Running on :3001, healthy |
| MIND→MEMORY loop | Closed, verified |
| L5 governed bridge | Connected (OpenClaw + Hermes share graph) |
| Two-copy drift | `/root/arifOS/` ≠ `/opt/arifos/app/` — deployment gap |
| v0.1 autonomous trust | **Minimal** — health checks, file ops, research, forge docs |
| v0.1 propose trust | Infrastructure, deployment, memory mods |
| v0.1 principal trust | Restarts, seals, external world, sovereignty |

---

## §7 — IMMEDIATE NEXT MOVES (P0)

1. **Deploy ROOTKEY E1-E7 to live kernel** — fix two-copy drift, push modules to `/opt/arifos/app/`
2. **Wire governance stream** — arifOS kernel publishes verdicts to NATS `arifos-governance`
3. **Wire organ heartbeats** — GEOX, WEALTH, WELL publish structured heartbeats to NATS
4. **AAA cockpit renders live state** — one screen showing all 6 organs + governance verdicts
5. **Establish metric baselines** — 30 days of data before any band expansion

---

## §8 — SOVEREIGN VERDICT

**Status:** PROPOSAL ONLY. Awaiting Arif review and F13 seal.

**Reversibility:** `rm /root/.openclaw/workspace/forge_work/ARIF-PERSONAL-AGI-v0.1.md`

**Next:** Arif reviews, adjusts bands, issues 888 — or returns for revision.

---

*DITEMPA BUKAN DIBERI — 999 SEAL ALIVE*
