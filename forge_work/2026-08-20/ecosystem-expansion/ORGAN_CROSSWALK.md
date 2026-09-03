# Organ Inventory Crosswalk — DRAFT

> **STATUS:** DRAFT — proposal only.
> **DRAFTED:** 2026-08-20
> **REFERENCES:** `ARIFOS::ECOSYSTEM_EXPANSION::v1`, charter at `/root/AAA/instructions/ecosystem-expansion.md`

---

## Existing Federation Organs (5 internal)

| Organ | Port | Role | Status | Skills (existing) |
|---|---|---|---|---|
| **arifOS** | 8088 | judge / verdict | SEAL | render_verdict, gather_evidence, reason, route_intent, seal_receipt |
| **A-FORGE** | 7071/7072 | executor / MCP gateway | SEAL | forge_execute, forge_orchestrate, forge_document_intelligence, forge_browser, forge_git, forge_lease_acquire, forge_vault_seal |
| **GEOX** | 8081 | evidence (earth) | SEAL | evaluate_basin, analyze_well, rank_prospects, falsify_hypothesis, earth_evidence |
| **WEALTH** | 18082 | evidence (capital) | SEAL | compute_npv, compute_emv, evaluate_wisdom, audit_power, scan_collapse, stock_analysis |
| **WELL** | 18083 | evidence (vitality) | DEGRADED — REFLECT_ONLY normal state | assess_homeostasis, assess_livelihood, guard_dignity, validate_vitality, classify_substrate |

**Sources:**
- `/root/AAA/.well-known/agent-card.json` (gateway card, v2026.07.24)
- `/root/AAA/.well-known/agent.json` (kernel card, v2026.06.30)
- `/root/AAA/docs/federation-code-map.md` (per `Federation code map 2026-06-22`)
- `WELL State 2026-07-12` (degraded state)
- `Disabled MCP Audit 2026-08-04` (6 disabled MCP servers in HOLD)

---

## Directive's 8 Expansion Organs — Crosswalk

### ORGAN_01_COMPOSITION → Multi-surface execution governance

**Maps to:**
- A-FORGE `forge_orchestrate` (partial)
- AAA `task_routing` (partial)
- arifOS `arif_route` (intent routing only)

**Gap:** No atomic multi-organ execution plan with single-receipt semantics.

**Status:** Phase 4 DRAFT. Not yet implemented as a unified organ.

**Verdict:** Real gap. Worth building. Trust gate = Phase 2 (Trust) + Phase 3 (Observability).

---

### ORGAN_02_OBSERVE → Reality connection

**Maps to:**
- FRAME observer at :18085 (independent observer per `Reality-First Doctrine`)
- Prometheus + Grafana (existing federation telemetry)
- arifFLOW (informal metabolism, not OTel-standardized)

**Gap:** No canonical OpenTelemetry trace → receipt → witness chain.

**Status:** Phase 3 DRAFT. Partial coverage exists; OTel integration missing.

**Verdict:** Real gap. Worth building. Adapters = Prometheus, Grafana, Loki, OTel.

---

### ORGAN_03_COMMS → Communication surfaces

**Maps to:**
- None in current federation.

**Gap:** Zero existing adapter for Gmail / Outlook / IMAP / Calendar / Telegram.

**Status:** POST_TRUST_AUTH_GATE. Blocked by ORGAN_08_AUTH broker.

**Verdict:** Net-new surface. Worth building **only after** AUTH broker operational. Otherwise credential sprawl.

---

### ORGAN_04_STORAGE → Governed storage access

**Maps to:**
- Local Filesystem under VAULT999/ (existing, internal)
- `/root/BACKUPS/` (existing, manual)
- deprecation-registry.json (governed metadata)

**Gap:** No cloud storage adapters (OneDrive, Google Drive, S3).

**Status:** POST_TRUST_AUTH_GATE. Blocked by ORGAN_08_AUTH broker.

**Verdict:** Real gap, but cloud storage adapters are credential-sensitive. MUST go through AUTH broker first.

---

### ORGAN_05_WORK → Work coordination

**Maps to:**
- GitHub Issues used informally (existing)
- `/root/INCIDENTS/` (manual incident tracking)
- `/root/SESSION_SUMMARY.md` and similar (manual)

**Gap:** No canonical work-tracking layer. No Jira/Linear/structured adapter.

**Status:** POST_TRUST_AUTH_GATE. Blocked by ORGAN_08_AUTH broker.

**Verdict:** Real gap. Adapters = Jira, Linear, GitHub Issues (formalize). Defer until AUTH ready.

---

### ORGAN_06_BACKUP → Constitutional resilience

**Maps to:**
- `/root/BACKUPS/` (manual, via Hermes)
- `BACKUPS/zen-sweep-20260817-174929/` (date-stamped snapshots)
- Restic (possibly installed but not orchestrated — needs verification)

**Gap:** No orchestrated backup verification, no disaster recovery drill, no restore testing.

**Status:** Phase 2 DRAFT. Lower priority than Trust Engine, but parallelizable.

**Verdict:** Real gap. Adapters = Restic (verify install), Velero, snapshot systems. Identity-proven gate sufficient.

---

### ORGAN_07_DNS_CDN → Public surface control

**Maps to:**
- Cloudflare in front of `arif-fazil.com` (existing, manually configured via Hermes)
- Caddy reverse proxy (existing)
- DNS at registrar (existing, manual)

**Gap:** No agent-controlled DNS/CDN surface. All changes are manual via Hermes.

**Status:** POST_TRUST_DRAFT. **Surface control is sensitive.**

**Verdict:** Real gap BUT explicitly dangerous. Each DNS/CDN action needs explicit F13 grant. Do NOT automate broadly. Possible path: read-only observability adapters first, write-capability only with F13 per-action push.

---

### ORGAN_08_AUTH → Identity separation

**Maps to:**
- OAuth 2.1 advertised on AAA agent-card (declared)
- Bearer auth scheme (declared)
- Ed25519 sovereign signature flow (declared in F13 extension)
- SESSION_SUMMARY.md + carry_forward.json (manual identity tracking)

**Gap:** No actual broker implemented. Currently OAuth 2.1 is **advertised in the card** but the broker does not exist as a runtime service.

**Status:** **BLOCKER** for organs 03/04/05. Cannot proceed without it.

**Verdict:** CRITICAL. This is the linchpin. Without ORGAN_08_AUTH, organs 03/04/05/07 must remain HOLD.

---

## Critical Discoveries

1. **OAuth 2.1 is advertised but not implemented.** The agent-card declares OAuth flows that point to `https://aaa.arif-fazil.com/oauth/authorize` and `/oauth/token`. Whether those endpoints actually serve is unverified by this draft. **Worth verifying before Phase 1 SEAL.**

2. **WELL is intentionally DEGRADED.** Per `WELL State 2026-07-12`, WELL reports REFLECT_ONLY normal state. This is not a bug; it's a constitutional posture. The federation manifest should reflect this accurately (it does in the draft).

3. **6 MCP servers are disabled in HOLD.** Per `Disabled MCP Audit 2026-08-04`: capability-index + repomapper = SEAL_READONLY; graphiti/hindsight/sqlite = HOLD; serena = VOID. The federation manifest must NOT advertise these as available capabilities.

4. **arifOS Sampling is `888_HOLD`.** Per the directive itself and `Disabled MCP Audit`. The federation manifest correctly reflects this in the memory_model section.

5. **Disabled servers on port :8000.** Per `deprecation-registry.json` known_issues: "graphiti-not-installed — Port :8000 has no service/container". This should be removed from health probes if not reanimated.

6. **Existing kernel card (agent.json) and gateway card (agent-card.json) are SEAL-signed.** Phase 1 does NOT modify them. The drafted `arifos.json` is additive — separate file at `/.well-known/`.

7. **A-FORGE has TWO ports: 7071 (stateful) and 7072 (stateless).** Per deprecation known_issues: "a-forge-mcp-transport-timeout — Copilot CLI tools/call times out on :7071/mcp. :7072 stateless works." This affects Phase 4 Composition Bus design — should use :7072 by default.

---

## Net-New Work vs Already-Built

| Surface | Already built? | Phase 1 needed? |
|---|---|---|
| A2A kernel card | ✅ YES (agent.json) | No |
| A2A gateway card | ✅ YES (agent-card.json) | No |
| MCP server.json | ✅ YES (DRAFT) | Refresh after Phase 1 |
| DID document | ✅ YES | No |
| **Federation manifest (arifos.json)** | ❌ NO | **YES — net new, drafted** |
| Trust Engine | ❌ NO | Phase 2 |
| OTel / arifFLOW canonical | ❌ NO | Phase 3 |
| Composition Bus | ❌ NO | Phase 4 |
| Streaming / webhooks | ⚠️ Partial (NATS JetStream exists) | Phase 5 |
| AUTH broker | ❌ NO (advertised, not built) | **BLOCKER for 03/04/05** |
| Organs 03/04/05/06/07 | ❌ NO (or partial) | Phase 6+ |

**Bottom line:** ~70% of Phase 1 DISCOVERY is already done. The remaining 30% is **arifos.json** deployment + discovery-surface verification.

---

## Recommended Phase 1 SEAL Scope

### Deploy only:
1. `/root/AAA/forge_work/2026-08-20/ecosystem-expansion/drafts/arifos.json` → `/var/www/arif-fazil.com/.well-known/arifos.json`

### Verify:
1. `curl -I https://arif-fazil.com/.well-known/arifos.json` returns 200
2. `curl https://arif-fazil.com/.well-known/agent.json` still returns 200 (regression check)
3. `curl https://aaa.arif-fazil.com/.well-known/agent-card.json` still returns 200 (regression check)
4. Caddy logs show no auth-gate on `/.well-known/*`
5. `jq .` validates the deployed arifos.json

### Seal:
1. `arif_seal --mode=seal --payload="phase1-discovery-arifos-json-deployed" --ack_irreversible=true`
2. VAULT999 entry_id captured
3. NATS subject `arifos.federation.discovery.sealed` published

### Do NOT touch:
- agent.json (kernel card, SEAL-signed)
- agent-card.json (gateway card, SEAL-signed)
- DID document
- arifOS kernel
- A-FORGE
- VAULT999 schema
- Any disabled MCP server
- DNS/Cloudflare config
- Port bindings

---

*Drafted by 333-PROPOSAL. Cross-walked against existing memory: federation-code-map-2026-06-22, disabled-mcp-audit-2026-08-04, well-state-2026-07-12, separation-of-powers-doctrine.*