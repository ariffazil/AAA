# arifOS Security Intelligence — Knowledge Graph

> **Status:** F13_UNSEALED_DRAFT (2026-09-17)
> **Author:** FI-003 (Qwen Code) + F13 sovereign cybersecurity synthesis
> **Purpose:** Authoritative map linking all security domains, enforcement modules, doctrine, tests, scars, and memory across the arifOS Federation.
> **Maintenance:** Update on every security-relevant mutation. This file is the SOT for "where does security knowledge live."

---

## How to Read This File

- **Sections 1–7** = the 7 security layers, each with doctrine → enforcement → test → scar → memory links.
- **Section 8** = cross-layer linkages (the knowledge graph edges).
- **Section 9** = the 15 classical cybersecurity invariants mapped to arifOS.
- **Section 10** = the 12 AGI-grade authority kernel invariants (agent-graph-specific).
- **Section 11** = known gaps and next actions.
- **Every `[link:...]`** = a file path or memory reference that can be followed for depth.

---

## 1. IDENTITY

### Doctrine

| File | Concept |
|------|---------|
| [link:/root/AAA/instructions/identity-continuity.md] | Identity binding to cryptographic key, never name-string |
| [link:/root/arifOS/docs/IDENTITY_VERIFICATION.md] | ActorSource enum: ed25519_verified / sovereign_directive / jwt_verified / kernel_evaluated / self_report |
| [link:/root/AAA/instructions/consequence-bearing-identity.md] | 5-layer identity architecture (Label/Behavior/Motivation/Identity/Meaning) |
| [link:/root/AAA/governance/WP-01-IDENTITY-CONVERGENCE-DELIVERABLES.md] | Cross-source identity convergence (6 sources) |
| [link:/root/AAA/canon/ACTOR_SURFACE_DOCTRINE.md] | Actor/Surface/Contract layers; identity ≠ implementation |
| [link:/root/AAA/docs/BOOT_ATTESTATION_CLARITY.md] | Boot attestation clarity |
| [link:/root/AAA/canon/EUREKA-IDENTITY-METABOLISM-2026-09-09.md] | Closed-loop identity metabolism |

### Enforcement

| Module | Lines | What It Does |
|--------|-------|--------------|
| [link:/root/arifOS/arifosmcp/runtime/crypto_auth.py] | 1130 | Ed25519 challenge-response, single-use nonces (120s TTL), 5 key sources |
| [link:/root/arifOS/arifosmcp/runtime/session_auth.py] | 442 | Trust tier → authority band (ELDER=sovereign, VERIFIED=operator, etc.) |
| [link:/root/arifOS/arifosmcp/runtime/dpop_auth.py] | 192 | RFC 9449 proof-of-possession, prevents bearer replay |
| [link:/root/arifOS/arifosmcp/runtime/jwt_auth.py] | 760 | Supabase RS256 + internal HS256, configurable enforcement modes |
| [link:/root/arifOS/arifosmcp/runtime/f13_gate.py] | 110 | Non-delegable sovereign gate — blocks F13 delegation |
| [link:/root/arifOS/scripts/hooks/commit-msg/identity_guard.py] | — | Git commit identity validation |
| [link:/root/AAA/auth/sign_agent_card.py] | 218 | Ed25519 sign/verify A2A Agent Cards |
| [link:/root/A-FORGE/src/interfaces/middleware/operatorAuth.ts] | — | Operator auth middleware |

### Tests

- [link:/root/arifOS/tests/test_crypto_auth_ceremony.py]
- [link:/root/arifOS/tests/test_auth_continuity_file_secret.py]
- [link:/root/arifOS/tests/test_auth_continuity_open_mode.py]
- [link:/root/arifOS/tests/runtime/test_dpop_auth.py]
- [link:/root/arifOS/tests/runtime/test_oauth_flow.py]
- [link:/root/arifOS/conformance/kernel/test_authority.py]

### Scars & Memory

- `transport-authorization-parity.md` — different credentials OK, different authorization NOT
- `sct-programmatic-relay.md` — tokens corrupt when hand-copied
- `model-inhabitant-doctrine.md` — identity ≠ implementation, silent redirect scar
- `federation-identity-zen-closure.md` — C1-C10 chaos closed, 53→51 cards
- `p06-pydantic-literal-mismatch.md` — silent ValidationError → OBSERVE_ONLY

---

## 2. AUTHORITY

### Doctrine

| File | Concept |
|------|---------|
| [link:/root/AAA/instructions/authority-envelope.md] | Complete Mediation reference monitor. 10-field tuple. TOCTOU binding. EnforcementCoverage trinity. |
| [link:/root/arifOS/docs/AUTHORITY_MODEL.md] | How power flows — 6-arrow chain verification |
| [link:/root/AAA/docs/SEAL_AUTHORITY_DOCTRINE.md] | Authority bands: SOVEREIGN / FULL / LIMITED_MUTATE / OBSERVE_ONLY / ANONYMOUS |
| [link:/root/AAA/docs/SOT_AUTHORITY_TRUST.md] | Identity proof + authority band = mutation permission |
| [link:/root/AAA/docs/ACT_AUTHORITY_LAYER.md] | A2A = how to talk, DID = who, ACT = what may |
| [link:/root/AAA/instructions/epistemic-operating-rules.md] | Authority_out ≤ Authority_in + Evidence_new (R0-R5 gradient) |
| [link:/root/AAA/instructions/escalation-boundary.md] | T0-T3 tiers, 888 Lanes, zero-budget autonomy |
| [link:/root/AAA/canon/EUREKA-2026-09-13-CONSTRAINT-OVER-INTELLIGENCE.md] | Constraint > Intelligence; R-BAP Authority Clamp |
| [link:/root/AAA/canon/APEX-ZEN-CANONICAL-COMPRESSION.md] | BUILD→VERIFY→JUDGE→SEAL→ACT→WITNESS; Capability ≠ Authority |
| [link:/root/AAA/canon/APEX_FEDERATION_ALIGNMENT_v1.md] | Reality-constrained decision architecture |
| [link:/root/AAA/canon/REASON_BOUNDED_AUTHORITY_CANON_2026-09-16.md] | Reason-bounded authority |

### Enforcement

| Module | Lines | What It Does |
|--------|-------|--------------|
| [link:/root/arifOS/arifosmcp/runtime/authority.py] | 721 | Central authority state, DID registry, mtime caching, F1 fail-closed |
| [link:/root/arifOS/arifosmcp/runtime/authority_gate.py] | 215 | 7 axioms, authority smuggling detection, free-text verdict vocabulary gate |
| [link:/root/arifOS/arifosmcp/runtime/authority_middleware.py] | 296 | Single-writer middleware — eliminates 64 competing emission paths |
| [link:/root/arifOS/arifosmcp/runtime/act_token.py] | 1290 | ACT wire format, HMAC-SHA256, 7 bands, 8h TTL, legacy SCT dual-accept |
| [link:/root/arifOS/core/shared/authorize_mutation.py] | 320 | Tamper-proof execution tokens, TOCTOU-resistant, hash-bound |
| [link:/root/A-FORGE/src/domain/governance/execution-authority.ts] | 370 | 6-class action ladder (OBSERVE→DRAFT→MUTATE→EXECUTE_REVERSIBLE→EXECUTE_HIGH_IMPACT→IRREVERSIBLE) |
| [link:/root/A-FORGE/src/domain/governance/McpPolicyGate.ts] | 1237 | 5-layer boundary: Identity→Server→Tool→Argument→Verdict |
| [link:/root/A-FORGE/src/domain/governance/FloorEnforcer.ts] | 407 | F1-F13 unified dispatcher, VOID > HOLD > SABAR > SEAL |
| [link:/root/A-FORGE/src/domain/governance/mcpFloorEnforcer.ts] | 250 | Wraps every MCP tool call in FloorEnforcer.checkAll() |
| [link:/root/AAA/governance/tool_authority_registry.py] | — | Runtime authority band resolution, never trust arguments["action_class"] |
| [link:/root/arifOS/arifosmcp/arifos_policy/rego/mutation_policy.rego] | 63 | OPA/Rego sovereign-only mutations |
| [link:/root/arifOS/arifosmcp/arifos_policy/rego/lease_policy.rego] | 63 | Lease authority |
| [link:/root/arifOS/arifosmcp/arifos_policy/rego/tool_policy.rego] | 118 | Tool authority by lane |

### Tests

- [link:/root/arifOS/tests/invariants/test_no_self_authorization.py]
- [link:/root/arifOS/tests/invariants/test_service_health_not_execution_authority.py]
- [link:/root/arifOS/tests/test_f13_adversarial.py]
- [link:/root/arifOS/tests/test_f13_no_hold_to_seal.py]
- [link:/root/arifOS/tests/test_cross_organ_sct_propagation.py]
- [link:/root/arifOS/tests/runtime/test_wealth_auth.py]
- [link:/root/arifOS/tests/constitutional/test_authority_state_v1.py]
- [link:/root/arifOS/conformance/delegation/test_authority_attenuation.py]
- [link:/root/arifOS/conformance/execution/test_mutation_gates.py]

### Scars & Memory

- `apex-zen-worker-cell-doctrine.md` — 7 rules for bounded execution cells
- `aforge-p0-act-scope-fix.md` — ACT per-request scope fix (OBSERVE→MUTATE bypass)
- `c3-authority-override-fix.md` — 3rd authority-override bug in init path
- `seal-casual-ratification-decline.md` — self-SEAL = constitutional violation
- `hook-not-judge-enforcement-membrane.md` — hooks are sensors, not judges
- `empty-deny-list.md` — kernel is safety layer, not vendor approval prompts

---

## 3. INTERPRETATION BOUNDARY (DATA ≠ CODE ≠ AUTHORITY)

### Doctrine

| File | Concept |
|------|---------|
| [link:/root/AAA/canon/HERMES_PROMPT_INJECTION_MEMBRANE_v1.md] | Sealed canon — prompt injection defense membrane for Hermes |
| [link:/root/AAA/canon/HERMES_DATA_CLASSIFICATION_ROUTING_v1.md] | SECRETS = NEVER enters Hermes context |
| [link:/root/arifOS/static/arifos/floors/F12_INJECTION.md] | F12 injection floor specification |
| [link:/root/arifOS/static/arifos/floors/F10_ONTOLOGY.md] | F10 ontology floor specification |
| [link:/root/arifOS/docs/SECURITY.md] | Cypher injection vulnerability documented and fixed |

### Enforcement

| Module | Lines | What It Does |
|--------|-------|--------------|
| [link:/root/arifOS/core/shared/guards/injection_guard.py] | 377 | Pattern-based injection detection, score 0-1, threshold 0.85, input normalization |
| [link:/root/arifOS/arifosmcp/core/enforcement/f10_ontology_guard.py] | 522 | SABAR→888_HOLD→VOID escalation, Redis-backed counter, BM+EN patterns |
| [link:/root/arifOS/arifosmcp/runtime/fed_guard.py] | 300 | SEA-Guard 11-category safety filter, fail-closed on unavailability |
| [link:/root/arifOS/arifosmcp/tools/self_authorize_guard.py] | 116 | SELF_APPROVE / BYPASS_JUDGE / AUTO_FORGE / SELF_MODIFY_CONSTITUTION / GRANT_SOVEREIGNTY detection |
| [link:/root/arifOS/arifosmcp/core/niat_guard.py] | 160 | Al-Kahf intent fabrication blocker — refuses "I know what you want" patterns |
| [link:/root/arifOS/arifosmcp/core/seal_token_guard.py] | 371 | Disambiguates "seal" across domains (geological/constitutional/vault/trap) |
| [link:/root/A-FORGE/src/infrastructure/code-mode/sandbox/SecurityScanner.ts] | 455 | AST-based static analysis — disallowed identifiers, modules, shell patterns |
| [link:/root/AAA/gateways/mcp_constitutional_gateway/gateway.py] | 680 | 8 pre-flight checks, dangerous keyword scanning in tool descriptions |
| [link:/root/AAA/contracts/haram_enforcement_map.yaml] | 177 | HARAM-class prohibited behaviors for all agents |

### Tests

- [link:/root/arifOS/tests/constitutional/test_f10_ontology_guard.py]
- [link:/root/arifOS/tests/adversarial/test_10_gates.py]

### Scars & Memory

- `forge-search-f12-overtrigger.md` — F12 regex-greedy scanner
- `external-ai-restricts-capabilities.md` — external AIs propose restrictions; kernel is safety layer
- `self-validation-degenerates-into-recursive-hallucination.md` — self-referential validation failure

---

## 4. EXECUTION CONTROL

### Doctrine

| File | Concept |
|------|---------|
| [link:/root/AAA/instructions/anti-haram-behavior-canonical.md] | Prohibited behaviors for all agents |
| [link:/root/AAA/instructions/human-zero-visibility-invariant.md] | Anti-HARAM spine (F2 Reality / F7 Ego / F13 Power) |
| [link:/root/AAA/instructions/CANON-LOCK-PROTOCOL.md] | chattr +i immutable trees, single legal mutation path |
| [link:/root/AAA/instructions/vault999-writer-discipline.md] | Kernel owns ledger, agents never append directly |
| [link:/root/AAA/instructions/autonomous-execution-seal.md] | Federation binding for autonomous execution |
| [link:/root/AAA/instructions/state-transition-discipline.md] | Never collapse a transition into a Boolean |
| [link:/root/A-FORGE/docs/MCP-HANDLE-SECURITY.md] | MCP handle security model (HMAC-SHA256, 256-bit) |

### Enforcement

| Module | Lines | What It Does |
|--------|-------|--------------|
| [link:/root/A-FORGE/src/interfaces/mcp/shell/arifJudge.ts] | 395 | 3-class shell classification: ALLOW/GATE/DENY. DENY = destructive patterns. GATE = irreversible. Default = GATE (fail-closed). |
| [link:/root/arifOS/arifosmcp/runtime/guard.py] | 125 | Irreversibility guard — markers in protected domains → HOLD |
| [link:/root/arifOS/arifosmcp/runtime/state_machine_guard.py] | 180 | 9-stage metabolic loop (000→111→333→444→555→666→777→888→999) — prevents skipping/reversing |
| [link:/root/arifOS/arifosmcp/runtime/amendment_guard.py] | 293 | 7-day cooling period for constitutional amendments |
| [link:/root/arifOS/arifosmcp/runtime/godel_lock_gate.py] | 336 | phi_external < 0.5 → HOLD; self-certification blocked regardless of tier |
| [link:/root/arifOS/arifosmcp/runtime/enforcer.py] | 710 | HARD STOP — query classification BEFORE tool invocation, immutable audit log |
| [link:/root/arifOS/arifosmcp/constitution/degradation_policy.py] | 351 | Asymmetric degradation: observe=permissive, mutate=deny |
| [link:/root/arifOS/core/enforcement/auth_continuity.py] | 281 | L11 Amanah Handshake — HMAC-chained session context across tool calls |
| [link:/root/A-FORGE/src/domain/containment/SandboxPolicy.ts] | 203 | bwrap/firejail/docker containment — filesystem, network, resources |
| [link:/root/A-FORGE/src/domain/forge/CapabilityLease.ts] | 311 | Time-bounded, resource-limited permits. 24h max. Agent creates CAPABILITY, never creates AUTHORITY. |
| [link:/root/A-FORGE/src/infrastructure/secrets/SecretBrokerPolicy.ts] | 273 | Never-return-host, TTL auto-revoke, SHA-256 audit (never plaintext) |
| [link:/root/A-FORGE/src/domain/governance/AutonomousForgeGate.ts] | 272 | Self-evolution gate: PROPOSE→STAGE→MESA_SCAN→TRI_WITNESS→APEX→TRUST→FORGE_SEAL→PROMOTE→EXECUTE |
| [link:/root/A-FORGE/src/domain/governance/TrustTierEnforcer.ts] | 342 | UNTRUSTED→STAGED→REVIEWED→TRUSTED matrix with APEX binding |
| [link:/root/arifOS/arifosmcp/runtime/lease_engine.py] | — | Lease lifecycle management |
| [link:/root/A-FORGE/src/domain/governance/GitDiffGuard.ts] | — | Git diff guard for code review |

### Tests

- [link:/root/arifOS/tests/test_seal_e2e.py]
- [link:/root/arifOS/tests/test_vault999_isolation_guard.py]
- [link:/root/arifOS/tests/runtime/test_no_inline_auth.py]

### Scars & Memory

- `arif-seal-hold-constitutional-not-failure.md` — HOLD = constitution working, not failure
- `decommissioned-surface-respects.md` — sovereign deletion ≠ pause
- `t2-announce-discipline.md` — 10s veto window for T2 mutations
- `writer-governance-ownership.md` — every SOT file needs a writer registry
- `codex-cli-trust-flag-f13-only.md` — hook trust cannot be pre-set by agents
- `aaa-picker-no-auto-sync.md` — AAA writes SOT, does NOT auto-sync to pickers

---

## 5. ISOLATION & BLAST RADIUS

### Doctrine

| File | Concept |
|------|---------|
| [link:/root/arifOS/docs/constitutional.llms.txt] | blast_radius: LOCAL / ORGAN / FEDERATION / EXTERNAL / IRREVERSIBLE |
| [link:/root/arifOS/docs/SOVEREIGN_FABRIC_SPEC.md] | Wajib layers (5 of 8 implemented) |
| [link:/root/arifOS/docs/LOCALHOST_IS_PASSWORD.md] | Localhost services no-auth, UFW blocks external (ADR-001, 2026-06-04) |
| [link:/root/AAA/canon/GODEL_LOCK.md] | No system is final authority on own reality |
| [link:/root/AAA/instructions/constitutional-separation.md] | Constitutional separation enforcement |

### Enforcement

| Module | Lines | What It Does |
|--------|-------|--------------|
| [link:/root/A-FORGE/src/domain/containment/SandboxPolicy.ts] | 203 | Filesystem (readOnly/denied), network (denyAll/allowedDomains), resource limits |
| [link:/root/A-FORGE/src/domain/forge/CapabilityLease.ts] | 311 | Filesystem scope, network scope, resource limits, credential scoping |
| [link:/root/A-FORGE/src/infrastructure/egress/EgressPolicy.ts] | 109 | Profile-based egress: default/direct/mubeng/corp-proxy/tor; unknown = "unavailable" |
| [link:/root/arifOS/arifosmcp/runtime/ssrf_guard.py] | — | IP classification, DNS resolution, fail-closed |
| [link:/root/arifOS/arifosmcp/runtime/remote_proxy_auth.py] | 379 | Organ proxy auth, authority capped to OBSERVE_ONLY for Path-B |
| [link:/root/arifOS/core/enforcement/auth_continuity.py] | 281 | HMAC-chained session context — prevents session hijacking across tool calls |
| [link:/root/arifOS/arifosmcp/runtime/wealth_auth/authorize.py] | 142 | Single gate for WEALTH organ — signature, issuer, audience, expiry, jti replay, capability grants |

### Scars & Memory

- `container-kill-dependency-verify.md` — never kill containers by name alone
- `arifos-three-way-code-split.md` — probe which copy is live before editing
- `symlink-trap-preflight-mv.md` — pre-flight for destructive ops (mv/rm/chmod)
- `systemd-protecthome-blocks-root-symlink.md` — ProtectHome=yes blocks symlinks

---

## 6. INTEGRITY & PROVENANCE

### Doctrine

| File | Concept |
|------|---------|
| [link:/root/AAA/instructions/vault999-writer-discipline.md] | JSONL invariant, chattr +a, kernel owns ledger |
| [link:/root/AAA/instructions/claim-receipt-binding.md] | Atomic receipt and handle law |
| [link:/root/AAA/governance/.archive-2026-08-29/CLAIM_PROVENANCE_LAYER.md] | Provenance tracking specification (25KB) |
| [link:/root/AAA/instructions/epistemic-operating-rules.md] | R0-R5 authority gradient; TEXT ≠ EVIDENCE |
| [link:/root/arifOS/docs/spec/TOOL_LINEAGE_CONTRACT.md] | Tool lineage injection per invocation |
| [link:/root/AAA/docs/CRYPTO_ATTESTATION.md] | Signed verdict capsule spec |
| [link:/root/AAA/canon/WITNESS_SUBSTRATE_V1-2026-09-10.md] | Witness as constitutional function |
| [link:/root/AAA/canon/EUREKA-WITNESS-MEMBRANE-2026-09-09.md] | W1 before action, W2 after action, W3 human witness |
| [link:/root/AAA/instructions/witness-zen-doctrine.md] | Witness > Projection, shadow acknowledgment |
| [link:/root/AAA/instructions/evidence-discipline.md] | Evidence packages to 888-APEX |
| [link:/root/AAA/canon/WITNESS_OBJECT_SPEC_v1.md] | Witness object specification |
| [link:/root/AAA/canon/CONTRADICTION_LEDGER.md] | Max 3 active contradictions |
| [link:/root/AAA/canon/FALSIFICATION_REGISTER.md] | Falsification tracking |

### Enforcement

| Artifact | What It Does |
|----------|--------------|
| [link:/root/VAULT999/outcomes.jsonl] | 29MB, 67K+ records, hash-chained, chattr +a |
| [link:/root/VAULT999/seal_chain.py] | Ed25519 signature chain to genesis statement |
| [link:/root/VAULT999/vault_chain_verify.py] | Chain verification script (21KB) |
| [link:/root/VAULT999/seal_law.py] | Seal enforcement (23KB) |
| [link:/root/scripts/chain_walk.py] | Walks outcomes.jsonl, classifies chain integrity |
| [link:/root/arifOS/arifosmcp/runtime/evidence_guard.py] | 65 | Requires evidence_state for nontrivial claims |
| [link:/root/arifOS/arifosmcp/runtime/seal_chain.py] | 275 | Seal chain validator — Ed25519 signature verification |
| [link:/root/A-FORGE/src/domain/governance/mcp-surface-guard.ts] | 716 | Schema fingerprinting + drift detection |
| [link:/root/A-FORGE/duties/security-disclosure-watch.py] | 321 | 72-hour ack clock for vulnerability reports |
| [link:/root/AAA/scripts/supply_chain_gate.py] | 127 | Fails closed on unpinned installs |
| [link:/root/scripts/vault999_verify.py] | — | VAULT999 chain verification |
| [link:/root/scripts/audit_receipt_integrity.py] | — | Receipt integrity verification |
| [link:/root/scripts/external_witness_probe.py] | — | External witness probe |

### VAULT999 Ledger Inventory

| Ledger | Size | Purpose |
|--------|------|---------|
| outcomes.jsonl | 29MB | Main immutable audit trail |
| SEALED_EVENTS.jsonl | 1.8MB | Kernel-owned sealed events |
| rsi_ledger.jsonl | 3.7MB | RSI audit trail |
| apex-zen-receipts.jsonl | 9.8MB | Governance receipts |
| apex-zen-witness.jsonl | 10.5MB | Witness records |
| arifflow_sealed.jsonl | 12MB | Metabolic audit trail |
| receipts_v2.jsonl | — | V2 receipt ledger |
| session-seals.jsonl | — | Session seal records |
| local_seals.jsonl | — | Local seal chain |
| outcomes.sig.jsonl | — | Signed outcome records |

### Scars & Memory

- `witness-tamper-evidence-discipline.md` — 6 requirements for operational immutability
- `seal-chain-append-only-attribute.md` — chattr cycle requirement for seal_chain.jsonl
- `audit-epistemic-honesty.md` — OBS/DER/INT/SPEC labels, trace dataflow before filing
- `geox-restoration-admissibility.md` — 5-axis consistency (geometry/chronology/physics/uncertainty/provenance)
- `audit-error-not-governance-success.md` — correcting errors proves witness, not governance
- `audit-severity-rating-inversion.md` — "Critical" often false positive, "Low" hides real bugs

---

## 7. OBSERVABILITY & RECOVERY

### Doctrine

| File | Concept |
|------|---------|
| [link:/root/AAA/instructions/witness-zen-doctrine.md] | Witness > Projection, shadow acknowledgment, void guard |
| [link:/root/AAA/canon/HERMES_KILL_SWITCH_PROCEDURE_v1.md] | Kill / isolate / restart procedure |
| [link:/root/AAA/governance/.archive-2026-08-29/ZERO_DAY_SENTINEL_ARCHITECTURE.md] | DEFENSIVE_ONLY constitutional exposure auditor |
| [link:/root/AAA/governance/A4-BOUNDARY-REMEDIATION-PLAN-v0.md] | Enforcement boundary failure analysis |
| [link:/root/AAA/instructions/probe-before-panic.md] | Capability declared "down" only after inventory sweep + alternate-lane test |
| [link:/root/AAA/instructions/sovereign-attention-preservation.md] | Sovereign attention = ultimate cost |

### Enforcement

| Module | Lines | What It Does |
|--------|-------|--------------|
| [link:/root/A-FORGE/src/domain/agents/mesa-detector/MesaDriftDetector.ts] | 378 | Statistical drift detection: chi-square, KL divergence, z-score; detects hidden objectives |
| [link:/root/A-FORGE/src/domain/governance/mcp-surface-guard.ts] | 716 | Schema fingerprinting — hash-pins at init, re-verifies on every call, delta = 888_HOLD |
| [link:/root/A-FORGE/duties/security-disclosure-watch.py] | 321 | Gmail OAuth inbox check, 72-hour ack clock, scar-derived from SSRF disclosure |
| [link:/root/AAA/scripts/supply_chain_gate.py] | 127 | Fails closed on missing registry, unpinned npx/uvx |
| [link:/root/scripts/doctor.sh] | — | Single-command federation health check (organs + memory + skills + vault + drift) |
| [link:/root/scripts/federation-sot-check.sh] | — | Federation SOT drift detection |
| [link:/root/scripts/scan_entropy.py] | — | Entropy scanner |
| FRAME `:18085` | — | Independent observer, drift detection, evidence gathering |
| arifFlow `:7073` | — | FQ monitoring, receipt ingestion, metabolic ledger |

### Recovery Infrastructure

| Artifact | What It Does |
|----------|--------------|
| [link:/root/scripts/federation-backup.sh] | Nightly encrypted snapshot (AES256 via GPG) |
| [link:/root/scripts/vault999-backup.sh] | VAULT999 backup |
| [link:/root/scripts/vault999-push-replica.sh] | VAULT999 replica push |
| [link:/root/A-FORGE/src/infrastructure/secrets/SecretBrokerPolicy.ts] | TTL auto-revoke, credential rotation |
| [link:/root/A-FORGE/governance/KEY_ROTATION_POLICY.md] | Key rotation policy |
| forge_sandbox_pause/resume | Container state persistence + resume |

### Scars & Memory

- `probe-before-panic.md` — "down" requires proof
- `capability-layered-reachability.md` — Declared ≠ Reachable ≠ Healthy ≠ Routable
- `metabolism-cron-verified-but-dead.md` — code CAN run ≠ DOES run
- `convergence-after-unblinding.md` — convergence after unblinding is baseline, not evidence
- `n1-not-load-bearing.md` — n=1 latency sample is not "verified"
- `verify-active-surface-before-referring.md` — verify active surface before naming "this session"

---

## 8. CROSS-LAYER LINKAGES

```
IDENTITY ──────────→ AUTHORITY
  │                    │
  │ crypto_auth.py     │ act_token.py (HMAC, 8h TTL)
  │ session_auth.py    │ authority_gate.py (7 axioms)
  │ identity-continuity│ authority-envelope.md (10-field tuple)
  │                    │
  ▼                    ▼
INTERPRETATION ────→ EXECUTION CONTROL
  │                    │
  │ injection_guard    │ ArifJudge.ts (3-class)
  │ f10_ontology_guard │ enforcer.py (HARD STOP)
  │ fed_guard (SEA)    │ state_machine_guard (9-stage)
  │ McpPolicyGate      │ degradation_policy (asymmetric)
  │ self_authorize_guard│ authorize_mutation (TOCTOU)
  │                    │
  ▼                    ▼
ISOLATION ─────────→ INTEGRITY & PROVENANCE
  │                    │
  │ SandboxPolicy      │ VAULT999 (67K+ records)
  │ CapabilityLease    │ seal_chain (Ed25519)
  │ EgressPolicy       │ evidence_guard
  │ ssrf_guard         │ claim-receipt-binding
  │ remote_proxy_auth  │ tool_lineage_contract
  │                    │
  ▼                    ▼
OBSERVABILITY & RECOVERY
  │
  │ MesaDriftDetector (statistical)
  │ mcp-surface-guard (schema fingerprinting)
  │ FRAME (independent observer)
  │ arifFlow (metabolic ledger)
  │ Zero-Day Sentinel (exposure scanner)
  │ security-disclosure-watch (72h ack)
  │
  └──→ feeds back to IDENTITY (witness validates identity)
       and to AUTHORITY (reality contracts authority)
```

---

## 9. THE 15 CLASSICAL CYBERSECURITY INVARIANTS → arifOS MAPPING

| # | Invariant | arifOS Enforcement | Status |
|---|-----------|-------------------|--------|
| 1 | Identity ≠ authority | `arif_init` + `arif_judge` separate tools | ✅ Enforced |
| 2 | Complete mediation | Authority Envelope (10-field tuple, TOCTOU binding) | ✅ Enforced |
| 3 | Least-privilege, scoped, temporary | ACT bands + CapabilityLease (8h TTL) | ✅ Enforced |
| 4 | DATA ≠ CODE ≠ AUTHORITY | injection_guard + self_authorize_guard + Cypher fix | ✅ Enforced |
| 5 | Representation ≠ referent | FastMCP URL-decode fix + seal_token_guard | ✅ Enforced |
| 6 | Post-transform validation | authority_middleware (single-writer, TOCTOU-resistant) | ✅ Enforced |
| 7 | Default deny, fail closed | degradation_policy (asymmetric) + enforcer (HARD STOP) | ✅ Enforced |
| 8 | Secrets must be secrets | 5-R Protocol + SecretBrokerPolicy + mode-600 | ✅ Enforced |
| 9 | Isolation survives compromise | 3-node mesh + SandboxPolicy + per-organ authority | ✅ Enforced |
| 10 | Blast radius bounded | canonical.llms.txt (5 levels) + CapabilityLease scope | ✅ Enforced |
| 11 | Integrity has provenance | VAULT999 (67K+) + seal_chain (Ed25519) + chattr +a | ✅ Enforced |
| 12 | Controls are attack surfaces | Dead mock-OAuth fixed + mcp-surface-guard fingerprinting | ✅ Monitored |
| 13 | Observation ≠ truth | FRAME (evidence, never verdict) + 555 independent witness | ✅ Enforced |
| 14 | Observability after the fact | arifFlow receipts + VAULT999 + security-disclosure-watch | ✅ Enforced |
| 15 | Recovery is part of security | sandbox pause/resume + AES256 backups + key rotation | ✅ Enforced |

---

## 10. THE 12 AGI-GRADE AUTHORITY KERNEL INVARIANTS

See companion file: [link:/root/AAA/instructions/agi-grade-authority-kernel-invariants.md]

---

## 11. KNOWN GAPS & NEXT ACTIONS

### Gap 1: MCP Tool Description Poisoning
**Evidence:** CVE-2025-49596, CVE-2026-30615 (Reddit intelligence 2026-08-26)
**Problem:** arifOS has 5+ MCP servers, 200+ tools. Tool descriptions are injected into context BEFORE the kernel sees them. `injection_guard` runs on user input, not MCP tool descriptions.
**Proposal:** Extend `mcp_constitutional_gateway` to scan tool descriptions at registration time.
**Status:** OPEN

### Gap 2: Authority Graph Acyclicity
**Evidence:** `godel_lock_gate.py` blocks self-certification but delegation chain acyclicity is not mechanically verified.
**Problem:** A→B→C→A authority chains could theoretically escalate.
**Proposal:** Authority graph cycle detector — verify delegation chains terminate.
**Status:** OPEN

### Gap 3: Postcondition Coverage Incomplete
**Evidence:** `forge_seal_run` + VAULT999 verify postconditions for sealed actions.
**Problem:** Not every mutation path has mandatory postcondition verification. The "Reality Boundary" needs mechanical enforcement at every mutation, not just sealed ones.
**Proposal:** Extend postcondition verification to all Class C+ mutations.
**Status:** OPEN

### Gap 4: External Red-Team Assessment
**Evidence:** 2026-09-16 external security report found 4 issues (all fixed in dev tree).
**Problem:** No external auditor has done a full red-team assessment of the authority model.
**Proposal:** Commission external security review of the authority envelope + ActToken system.
**Status:** OPEN

### Gap 5: Enforcement Boundary Failure
**Evidence:** `A4-BOUNDARY-REMEDIATION-PLAN-v0.md` — every FI harness runs as root.
**Problem:** Actor-becomes-authorizer incidents; boundary vs discipline.
**Proposal:** Per-harness user namespaces + capability bounding.
**Status:** DRAFT_AWAITING_F13

---

## 12. CI/CD SECURITY GATES

| Workflow | Repo | What It Does |
|----------|------|--------------|
| `secrets-audit.yml` | AAA | Secrets scanning gate |
| `gitleaks.yml` | AAA | Gitleaks secret detection |
| `sentinel-premerge-gate.yml` | AAA, arifOS | Sentinel pre-merge gate |
| `governance-gate.yml` | AAA, arifOS | Governance enforcement gate |
| `floor_gate.yml` | arifOS | Constitutional floor gate |
| `surface-gate.yml` | arifOS | MCP surface gate |
| `03-secrets-gate.yml` | arifOS | Secrets scanning |
| `a-forge-boundary-guard.yml` | A-FORGE | Boundary guard CI |
| `act-integration.yml` | AAA | ACT integration |
| `external-witness.yml` | AAA | External witness |
| `federation-abi-conformance.yml` | AAA | ABI conformance |
| `repo-hygiene-weekly.yml` | AAA | Weekly repo hygiene |

---

## 13. SECURITY SKILL INVENTORY

| Skill | Security Domain |
|-------|-----------------|
| [link:/root/AAA/skills/security/security-disclosure-handling/] | Vulnerability disclosure procedure |
| [link:/root/AAA/skills/forge-act-federation-ingress/] | ACT token mint/validate (65-case matrix) |
| [link:/root/AAA/skills/authority-reality-grounder/] | Anti-shadow architecture validator |
| [link:/root/AAA/skills/sanctuary-boundary-enforcer/] | Human dignity/privacy protection |
| [link:/root/AAA/skills/enforcement-coverage-audit/] | Control effectiveness measurement |
| [link:/root/AAA/skills/verify-gate/] | 5 gates: authority + evidence + reversibility + lineage + REALITY |
| [link:/root/AAA/skills/aaa-skill-governor-runtime/] | 6-gate pre-load + lifecycle governance |
| [link:/root/AAA/skills/forge-secret-hygiene/] | Secret leak audit |
| [link:/root/AAA/skills/forge-infra-guardian/] | Caddy/Cloudflare/SSL/DNS validation |
| [link:/root/AAA/skills/forge-telegram-audit/] | TREE777 Telegram bot security |
| [link:/root/AAA/skills/asi-agentic-governance/] | Compact agent operating constitution |
| [link:/root/AAA/skills/forge-mcp-testing/] | MCP protocol conformance |
| [link:/root/AAA/skills/kernel-bind/] | Constitutional binding before action |
| [link:/root/AAA/skills/seal-discipline/] | SEAL vs RECEIPT vs SABAR disambiguation |
| [link:/root/AAA/skills/forge-esm-require-guard/] | ESM/CommonJS interop guard |
| [link:/root/AAA/skills/a2a-task-delegator/] | A2A precondition contracts + attestation |
| [link:/root/AAA/skills/hermes-coding-gateway/] | Governed multi-CLI coding fabric |
| [link:/root/AAA/skills/aaa-musyawarah-execution/] | Authority star — no agent proposes+executes same irreversible step |
| [link:/root/AAA/skills/audit-repo-reality/] | STUB/ORPHAN/SHIM/REALITY_LEAK detection |
| [link:/root/AAA/skills/capability-telemetry-audit/] | Demonstrated capability audit |
| [link:/root/AAA/skills/learning-loop-verification/] | Learning loop closure verification |
| [link:/root/AAA/skills/first-party-evidence-audit/] | Claims vs first-party records |
| [link:/root/AAA/skills/forge-vss-verifier-suite/] | Post-generation visual verification |
| [link:/root/AAA/skills/arifos-kernel-zen-audit/] | Kernel zen audit (includes sovereign auth, seal architecture) |

---

> **DITEMPA BUKAN DIBERI** — Forged, Not Given. This knowledge graph is a living document. Update it on every security-relevant mutation.
