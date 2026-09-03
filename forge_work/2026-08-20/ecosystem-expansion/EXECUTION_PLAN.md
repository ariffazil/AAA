# Ecosystem Expansion — 5-Phase Execution Plan

> **STATUS:** DRAFT — proposal only. Awaiting per-phase SEAL.
> **DRAFTED:** 2026-08-20
> **REFERENCES:** `ARIFOS::ECOSYSTEM_EXPANSION::v1`, charter at `/root/AAA/instructions/ecosystem-expansion.md`

---

## Global Constraints (apply to every phase)

| Constraint | Rule |
|---|---|
| Authority gate | Each phase requires explicit per-phase SEAL (Arif decree + Hermes deploy) |
| Separation of powers | No phase mutates production state without Hermes on VPS |
| Reversibility | Phase 1 = additive (revertable). Phase 2 = additive. Phase 3-5 = partial reversibility, requires rollback plan |
| Blast radius declaration | Required before each phase SEAL |
| Trust gate | Low trust → HOLD. High trust → Eligible. Trust Engine (Phase 2) gates downstream |
| Memory | VAULT999 internal only. Adapters read from governed surfaces, never write direct |
| MCP Sampling | `888_HOLD` until identity proven + observability complete + trust active |
| Marketplace | DEFERRED until Phase 1-4 operational |
| Capability without witness | NOT permitted. Every adapter action must emit Trace → Receipt → Witness |

---

## Phase 1 — DISCOVERY (READY TO SEAL)

**Goal:** arifOS becomes discoverable as a federation ecosystem.

### Deliverables
- [x] DRAFT: `/root/AAA/forge_work/2026-08-20/ecosystem-expansion/drafts/arifos.json` (federation manifest)
- [x] DRAFT: `/root/AAA/forge_work/2026-08-20/ecosystem-expansion/drafts/agent-json-evolution-proposal.md` (kernel card evolution)
- [x] DRAFT: charter at `/root/AAA/instructions/ecosystem-expansion.md`
- [ ] DEPLOY: `arifos.json` to `https://arif-fazil.com/.well-known/arifos.json`
- [ ] VERIFY: all `.well-known/*` paths return 200 with valid signatures/JSON

### Prerequisites (already met)
- ✅ Existing SEAL-signed agent.json and agent-card.json
- ✅ DID document signed
- ✅ 5 organ cards (arifos, a-forge, geox, wealth, well)
- ✅ arifos.json schema drafted and cross-walked

### Blast radius
- **Surface:** `arif-fazil.com/.well-known/arifos.json` (new public file)
- **Severity:** LOW — additive, no existing card touched
- **Rollback:** delete file from web root (1 command)
- **Auth impact:** NONE — discovery is read-only

### Trust gate before next phase
- [ ] arifos.json publicly resolvable from at least 3 vantage points
- [ ] No Caddy/Cloudflare auth gate on `/.well-known/*`
- [ ] JSON validates against draft schema
- [ ] No secrets in any draft file

### Hermes handoff envelope
```bash
# On VPS (72.62.71.199:22888)
cp /root/AAA/forge_work/2026-08-20/ecosystem-expansion/drafts/arifos.json \
   /var/www/arif-fazil.com/.well-known/arifos.json
chmod 644 /var/www/arif-fazil.com/.well-known/arifos.json
# Verify Caddy: ensure /.well-known/* is public
curl -I https://arif-fazil.com/.well-known/arifos.json
# Seal to VAULT999
arif_seal --mode=seal --payload="phase1-discovery-deployed" --ack_irreversible=true
```

### Authority required
- Arif: "Phase 1 SEAL"
- Hermes: VPS deploy
- 333 PROPOSAL → 555 VERIFY → 888 JUDGE → A-FORGE EXECUTE → VAULT999 WITNESS

---

## Phase 2 — TRUST (BLOCKED until Phase 1 sealed)

**Goal:** Trust Engine operational. Every federation surface emits a trust score.

### Deliverables
- [ ] Trust Engine implementation (location TBD: arifOS kernel extension vs new service)
- [ ] Metrics wiring: identity, uptime, auditability, mutation_risk, witnessability
- [ ] Trust score emitted per organ to arifFLOW
- [ ] Trust policy: low → HOLD, high → Eligible

### Prerequisites
- ⏳ Phase 1 SEAL verified
- ⏳ Observability baseline (Phase 3 in parallel, minimum: Prometheus + FRAME observer working)

### Blast radius
- **Surface:** Trust Engine code, arifFLOW schema extension, NATS subject additions
- **Severity:** MEDIUM — adds policy layer, can be disabled by config flag
- **Rollback:** config flag → `trust_engine.enabled: false` (1 env var)
- **Auth impact:** INDIRECT — gates which organs can be reached for what capability

### Trust gate before next phase
- [ ] Trust Engine emits scores for all 5 organs
- [ ] LOW-trust organs cannot reach downstream services (e.g. WELL REFLECT_ONLY stays REFLECT_ONLY)
- [ ] High-trust organs get capability expansion (e.g. arifOS FULL authority)
- [ ] No false positives (a low-trust organ must never be marked high)

### Hermes handoff envelope
- Deploy Trust Engine container
- Wire NATS subject `arifos.federation.trust.*`
- Run calibration sweep against historical seals
- SEAL receipt

### Authority required
- Arif: "Phase 2 SEAL"
- Hermes: VPS deploy
- Pre-flight: independent Trust Engine audit (separate verifier)

---

## Phase 3 — OBSERVABILITY (parallel to Phase 2)

**Goal:** OpenTelemetry integration. Every action emits Trace → Receipt → Witness.

### Deliverables
- [ ] OTel collector wired into arifOS kernel
- [ ] Trace export to Prometheus/Grafana/Loki
- [ ] arifFLOW becomes canonical witness layer (replaces ad-hoc metabolism)
- [ ] Per-organ instrumentation: arifOS, A-FORGE, GEOX, WEALTH, WELL

### Prerequisites
- ⏳ Phase 1 SEAL verified
- ⏳ Trust Engine (Phase 2) at minimum 80% signals wired

### Blast radius
- **Surface:** OTel collector, Prometheus scrape configs, Grafana dashboards
- **Severity:** MEDIUM — adds observability, no functional change
- **Rollback:** disable OTel exporter (1 env var)
- **Auth impact:** NONE — telemetry is outbound only

### Trust gate before next phase
- [ ] Trace → Receipt → Witness chain verifiable end-to-end
- [ ] arifFLOW can replay any trace from last 7 days
- [ ] No PII leakage in traces (verify with FRAME observer)

### Hermes handoff envelope
- Deploy OTel collector container
- Wire NATS subject `arifos.federation.observability.*`
- Update Prometheus scrape configs
- Create Grafana dashboards
- SEAL receipt

### Authority required
- Arif: "Phase 3 SEAL"
- Hermes: VPS deploy
- Pre-flight: trace chain integrity test

---

## Phase 4 — COMPOSITION (BLOCKED until 2 + 3 operational)

**Goal:** Composition Bus. Cross-system execution becomes governed.

### Deliverables
- [ ] Composition Bus implementation (extends A-FORGE `forge_orchestrate`)
- [ ] Plan → Select Organ → Select Adapter → Execute → Collect Receipts → Return Result
- [ ] Single Receipt per composition (atomic execution record)
- [ ] Adapter framework for organs 03/04/05/06 (COMMS, STORAGE, WORK, BACKUP)

### Prerequisites
- ⏳ Phase 2 (Trust) operational
- ⏳ Phase 3 (Observability) operational
- ⏳ ORGAN_08_AUTH broker operational (BLOCKER for organs 03/04/05)

### Blast radius
- **Surface:** A-FORGE execution path, NATS subject schema, VAULT999 schema
- **Severity:** HIGH — multi-system execution atomicity is non-trivial
- **Rollback:** Composition Bus can be disabled, falls back to direct organ calls
- **Auth impact:** INDIRECT — adapters broker credentials via ORGAN_08_AUTH

### Trust gate before next phase
- [ ] Atomic execution test (start, kill mid-flight, rollback, verify consistency)
- [ ] Receipt replayability test (can a sealed receipt be re-executed deterministically?)
- [ ] Adapter isolation test (one adapter failure cannot cascade)

### Hermes handoff envelope
- Deploy Composition Bus container
- Wire A-FORGE forge_orchestrate → Composition Bus path
- Deploy ORGAN_08_AUTH broker
- First adapter: OneDrive (STORAGE) — least sensitive credential surface
- SEAL receipt

### Authority required
- Arif: "Phase 4 SEAL"
- Hermes: VPS deploy
- Pre-flight: 3-agent adversarial test (correctness, security, perf)

---

## Phase 5 — STREAMING (BLOCKED until 4 operational)

**Goal:** Event subscriptions. arifFLOW receives events in real-time.

### Deliverables
- [ ] NATS JetStream subscription model for incidents, tickets, messages, telemetry, receipts
- [ ] Per-subject ACLs (F12 injection defense)
- [ ] Webhook broker for external subscribers (OAuth-gated)
- [ ] Streaming A2A tasks support (extending agent-card capabilities.streaming = true)

### Prerequisites
- ⏳ Phase 4 (Composition) operational
- ⏳ ORGAN_08_AUTH broker operational
- ⏳ At least 1 production adapter from Phase 4 (proves the path)

### Blast radius
- **Surface:** NATS JetStream streams, webhook broker, A2A protocol extensions
- **Severity:** MEDIUM-HIGH — streaming exposes new async surface
- **Rollback:** Disable stream subjects, fall back to polling (degraded but functional)
- **Auth impact:** MEDIUM — webhook subscribers need OAuth tokens

### Trust gate before finalization
- [ ] Stream replay test (subscribe, replay last 24h, verify integrity)
- [ ] Webhook signature verification (every webhook has Ed25519 sig)
- [ ] ACL test (F12 injection defense holds under load)

### Hermes handoff envelope
- Enable NATS JetStream durability classes
- Deploy webhook broker
- Configure ACLs per subject
- SEAL receipt

### Authority required
- Arif: "Phase 5 SEAL"
- Hermes: VPS deploy
- Pre-flight: load test (10k events/sec sustained)

---

## Phase 6+ — ADAPTERS (DEFERRED, post-Phase 5)

After Phase 5 operational:

| Organ | Adapter Priority | Trust Gate |
|---|---|---|
| ORGAN_03_COMMS | Email (IMAP), Calendar | AUTH broker |
| ORGAN_03_COMMS | Telegram, Gmail, Outlook | AUTH broker |
| ORGAN_04_STORAGE | OneDrive, Google Drive | AUTH broker |
| ORGAN_05_WORK | GitHub Issues (already informal), Linear, Jira | AUTH broker |
| ORGAN_06_BACKUP | Restic (local), Velero, snapshots | Identity proven |
| ORGAN_07_DNS_CDN | Cloudflare (already informal), Route53 | F13 grant per action |

Each adapter is its own sealed phase. No adapter proceeds until the parent organ's expansion is approved.

---

## Critical Path Summary

```
Phase 1 (DISCOVERY)     → ~2-4 hours drafting + Hermes deploy
Phase 2 (TRUST)         → ~1-2 weeks (Trust Engine + calibration)
Phase 3 (OBSERVABILITY) → ~1-2 weeks (OTel + arifFLOW canonical)
Phase 4 (COMPOSITION)   → ~2-4 weeks (Composition Bus + first adapter)
Phase 5 (STREAMING)     → ~1-2 weeks (NATS streams + webhooks)
Phase 6+ (ADAPTERS)     → continuous, per-adapter
```

---

## Success Criteria (final state, post-Phase 5)

- [ ] Discovery surfaces return 200 from 5+ vantage points
- [ ] Trust Engine emits scores, low-trust surfaces are gated
- [ ] OTel traces flow into arifFLOW, replayable
- [ ] Composition Bus executes multi-organ plans with atomic receipts
- [ ] Streaming webhooks deliver events with Ed25519 sigs
- [ ] No adapter proceeds without Trust Engine green-light
- [ ] VAULT999 unchanged (still internal canonical memory)
- [ ] MCP Sampling transitions from 888_HOLD → controlled enablement
- [ ] Skill Marketplace opens (gated by all of the above)

---

*Drafted by 333-PROPOSAL. Awaiting per-phase SEAL via 888 JUDGE.*