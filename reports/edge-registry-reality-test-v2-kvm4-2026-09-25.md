# Edge Registry Reality Test v2 — KVM4 Probe + Triage

> **Status:** `external_advisory_reality_test_v2` (Lane B autonomous, no F13 seal claimed)
> **Writer:** FI-003 anonymous session, `actor_verified=false`, `OBSERVE_ONLY` (per F13 directive "reality test edge registry v2 against kvm4")
> **Date:** 2026-09-25T00:17 MYT

---

## 0. Per `federation-invariant-identification-20260906` + `fail-closed-federation-state`

Reality Test v1 (prior turn) tested KVM8 + KVM2 + arifFlow on :7073. v2 specifically probes **KVM4 (workshop, 100.64.0.5)** for:
- Edge registry equivalent
- persons.yaml drift vs KVM8
- FED-litellm on tailscale IP (not loopback)
- Service state

---

## 1. Reality Test v2 — KVM4 Probes

| Probe | Result | Honest Report |
|---|---|---|
| **FED-litellm :4000 (loopback 127.0.0.1)** | ✗ Connection refused | "**UNKNOWN** — port not bound to loopback" (per `fed-relay-20260829` memory: loopback 127.0.0.1:4000 is DEAD) |
| **FED-litellm :4000 (tailscale 100.64.0.5)** | ✓ ALIVE but 401 auth error | "ALIVE but requires API key — not 0" |
| **lanes/people.yaml on KVM4** | ✗ NOT FOUND | "**UNKNOWN** — KVM8 convention; not propagated to KVM4" |
| **identity_cards/ on KVM4** | ✗ EMPTY (only `.` and `..`) | "**UNKNOWN** — empty registry; cannot determine" (NOT 0) |
| **federated map on KVM4** | ✗ NOT FOUND | "**UNKNOWN** — KVM8-canonical; replicated to KVM2 only" |
| **/var/lib/arifos/edge_assertions.jsonl on KVM4** | ✗ NOT FOUND | "**UNKNOWN** — edge registry is KVM8-only" |
| **/root/AAA/relationships/ on KVM4** | ✗ NOT FOUND | "**UNKNOWN** — no separate tree per memory recommendation" |
| **persons.yaml on KVM4** | ✓ EXISTS (205 lines) | "OLD SCHEMA v1.0 (no edge_references, no Schema v1.1)" |
| **hermes-asi-gateway on KVM4** | inactive | "**UNKNOWN** — per memory: KVM4 = OpenClaw + FED-litellm, NOT Hermes" |
| **fed-litellm.service** | loaded active running | "ALIVE on tailscale IP" |
| **openclaw-gateway.service** | loaded active running | "ALIVE on KVM4" |

---

## 2. CRITICAL DISCOVERY — persons.yaml DRIFT (KVM8 vs KVM4)

```
KVM8 (forge,   Schema v1.1):   sha256: d7344a4c7829428fccad4e0bdd767ff306bf4194cefdc04a1e0b3dcbf4283eaf  (13948 bytes, has edge_references)
KVM4 (workshop, Schema v1.0):  sha256: 9a43d02006c649a428fd7964cc147b3be059617e09ebf6a7447027e349f6505b  (10703 bytes, NO edge_references)

Result: ✗ DRIFT DETECTED
  - KVM4 has older version (Schema v1.0 — pre-Edge-Registry)
  - KVM8 has updated version (Schema v1.1 — with edge_references field)
  - DIFF: 3245 bytes, 72 lines, edge_references field
```

**Per `terminal-guard-before-creation` + `fail-closed-federation-state`:** this is REAL drift, not artifact. The Edge Registry implementation updated KVM8 but didn't propagate to KVM4.

---

## 3. KVM4 Edge Reality — Honest Findings

| Aspect | Finding | Severity |
|---|---|---|
| **Edge registry on KVM4** | ✗ NOT FOUND | HIGH (per `federation-invariant-identification` — invariant violated) |
| **persons.yaml drift** | ✗ OLD VERSION (v1.0) | HIGH (canonical identity record drift) |
| **lanes/people.yaml on KVM4** | ✗ NOT FOUND | medium (HERMES convention is KVM8-only by design) |
| **identity_cards/ on KVM4** | ✗ EMPTY | medium (F13-pilot biometric was KVM8 only) |
| **FED-litellm :4000 (tailscale)** | ✓ ALIVE (needs API key) | low (working as designed) |
| **FED-litellm :4000 (loopback)** | ✗ DEAD | medium (per memory: loopback is intentionally dead) |

**Per memory `kvm-mesh-truth-20260903`:** KVM4 = workshop (OpenClaw + FED-litellm, NOT Hermes). Edge registry not existing on KVM4 is **architectural** (not drift) — Hermes convention is KVM8-only.

**BUT persons.yaml drift is real drift** — should have been replicated to KVM4 when Schema v1.1 was applied.

---

## 4. Four-Bucket Triage (per `fix-optimize-forget-flow-triage`)

### 4.1 — **FIX** (prioritized by leverage and danger)

| # | Item | Severity | Action |
|---|---|---|---|
| 1 | Edge registry not federated invariant (KVM8-only) | HIGH | Add to `canon-replicate` cron (replicate `edge_assertions.jsonl` KVM8 → KVM2; KVM4 doesn't have arifFlow, no replicate target) |
| 2 | persons.yaml drift KVM8 vs KVM4 (Schema v1.1 not propagated) | HIGH | Replicate updated persons.yaml to KVM4 (manual cp via canon-mutate cycle on KVM4, or add to existing replication infrastructure) |
| 3 | FED-litellm :4000 loopback is DEAD (memory says intentional) | low (intentional design) | **FORGET** (verified-frozen per `fed-relay-20260829` — loopback intentionally dead; only tailscale IP works) |
| 4 | FED-litellm on KVM8 HAProxy :4000 TIMEOUT | HIGH | Probe HAProxy on KVM8 (may not be running or routing broken) |

### 4.2 — **OPTIMIZE** (working but backwards/inefficient)

| # | Item | Action |
|---|---|---|
| 1 | Naming convention gap (3 conventions for same entity: HERMES display_name / edge canonical_id / persons.yaml id) | F13 binary needed for canonicalization; recommend `human:<handle>` everywhere (matches edge registry convention) |
| 2 | FED-litellm 401 auth on tailscale | Add API key management (proper key rotation, not hardcoded) |
| 3 | F13 missing-edge binary for mail/jamari edges | Add subject-sealed testimony edges (awaiting F13 direction) |

### 4.3 — **FORGET** (verified-frozen items)

| # | Item | Why FORGET |
|---|---|---|
| 1 | FED-litellm loopback 127.0.0.1:4000 DEAD | Verified per `fed-relay-20260829` memory (2026-09-03): loopback is intentionally dead, tailscale is the live path. Not a bug, a design decision. |
| 2 | hermes-asi-gateway on KVM4 inactive | Per `kvm-mesh-truth-20260903` memory: KVM4 = OpenClaw + FED-litellm, NOT Hermes. Hermes is KVM8-canonical. Not a bug, architecture. |
| 3 | minimax-relay retired | Per `fed-relay-20260829`: retired 2026-08-29, inactive+disabled. Don't restart. |
| 4 | KVM8 litellm-federation :4013 orphan | Per `fed-relay-20260829`: orphan since cutover, stopped 2026-09-03 15:35 MYT (crash-loop NRestarts=140). Permanent disable + haproxy stop = 888_HOLD C-1. |

### 4.4 — **FLOW** (working correctly — keep, don't touch)

| # | Item | Why FLOW |
|---|---|---|
| 1 | Edge registry on KVM8 (9 edges, append-only) | Working — verify-and-keep; replication is the FIX, not redesign |
| 2 | Edge↔persons.yaml linkage (8/8 arif edges) | Working — verified end-to-end this session |
| 3 | Edge subject-sealed testimony pattern | Working — per memory `small-world-helix-linkage-20260924` recommendation |
| 4 | KVM2 witness canon-replicate cron | Working — `canon-replicate.timer` active every 15 min; receipt logged; telegram drift alarm wired |
| 5 | Edge registry as Reality Graph receipts (NOT standalone tree) | Working — per memory; no need for new infrastructure |

---

## 5. F2 TRUTH Labels + Receipts

| Claim | F2 Class | Confidence | Basis |
|---|---|---|---|
| "KVM4 persons.yaml differs from KVM8 (different sha256)" | OBS | CONFIRMED | sha256sum direct comparison |
| "KVM4 persons.yaml is Schema v1.0 (no edge_references)" | OBS | CONFIRMED | grep -c edge_references = 0 |
| "KVM4 has no edge_assertions.jsonl" | OBS | CONFIRMED | direct find probe |
| "KVM4 has no lanes/people.yaml" | OBS | CONFIRMED | direct ls probe |
| "KVM4 has no relationships/ directory" | OBS | CONFIRMED | direct ls probe |
| "FED-litellm on tailscale IP ALIVE (requires API key)" | OBS | CONFIRMED | curl :4000/health → 401 auth error |
| "FED-litellm on loopback 127.0.0.1:4000 DEAD" | OBS | CONFIRMED | curl :4000 refused |
| "hermes-asi-gateway on KVM4 inactive (architectural, not bug)" | DER | CONFIRMED | per `kvm-mesh-truth-20260903` memory |
| "Edge registry is KVM8-local, not federated invariant" | DER | CONFIRMED | per `federation-invariant-identification-20260906` memory |
| "KVM8 HAProxy :4000 TIMEOUT (potential FED gateway issue)" | OBS | CONFIRMED | curl timed out |
| "arifos-node-id.service runs once at boot (normal)" | OBS | CONFIRMED | Active (exited) since 2026-09-02 |

| Receipt | Type | Path |
|---|---|---|
| `OBS-KVM8-20260925-0017-001` | persons.yaml KVM8 sha256 | live probe |
| `OBS-KVM8-20260925-0017-002` | persons.yaml KVM4 sha256 (different) | SSH probe |
| `OBS-KVM8-20260925-0017-003` | KVM4 Schema v1.0 verification (0 edge_references) | SSH probe |
| `OBS-KVM8-20260925-0017-004` | KVM4 lanes/people.yaml NOT FOUND | SSH probe |
| `OBS-KVM8-20260925-0017-005` | KVM4 identity_cards/ EMPTY | SSH probe |
| `OBS-KVM8-20260925-0017-006` | KVM4 federated map NOT FOUND | SSH probe |
| `OBS-KVM8-20260925-0017-007` | KVM4 /var/lib/arifos/edge_assertions.jsonl NOT FOUND | SSH probe |
| `OBS-KVM8-20260925-0017-008` | KVM4 /root/AAA/relationships/ NOT FOUND | SSH probe |
| `OBS-KVM8-20260925-0017-009` | FED-litellm loopback DEAD | SSH probe |
| `OBS-KVM8-20260925-0017-010` | FED-litellm tailscale ALIVE (401) | SSH probe |
| `OBS-KVM8-20260925-0017-011` | KVM8 HAProxy :4000 TIMEOUT | local probe |
| `OBS-KVM8-20260925-0017-012` | arifos-node-id.service state | SSH probe |

---

## 6. Cross-References

- `/root/AAA/canon/EDGE-REGISTRY-PERSONS-YAML-CONNECTION-RECEIPT-2026-09-25.md` — Canonical connection (sha256:e7702c51…)
- `/var/lib/arifos/edge_assertions.jsonl` — Edge registry (KVM8-only, 9 edges, append-only)
- `/root/AAA/registries/persons.yaml` — KVM8 updated Schema v1.1 (with edge_references)
- `/root/AAA/registries/persons.yaml` (KVM4) — old Schema v1.0 (DRIFT, no edge_references)
- `/root/.local/share/arifos/vault999/seal_chain.jsonl` — Governance events
- `/root/.hermes/lanes/people.yaml` — HERMES lane cards (KVM8 convention)
- `/root/AAA/governance/HERMES_RELATIONSHIP_KERNEL.md` — Relationship kernel (conceptual, not edge registry implementation)

---

## 7. Constitutional Status

```yaml
artifact:
  type: reality_test_audit_v2
  status: external_advisory (Lane B)
  canonical_standing: NONE — Lane B audit
  lane: B (autonomous)

constitutional_status:
  f1_amanah: satisfied (reversible audit)
  f2_truth: explicit F2 labels + 12 receipts + fail-closed reporting
  f4_clarity: entropy reduction via 4-bucket triage
  f7_humility: Ω₀ = 0.05 (declared gaps: persons.yaml drift, edge not federated, naming gap)
  f8_genius: simplest correct path — diagnose + triage (no edge mutation)
  f9_anti_hantu: witnessing ≠ claiming (audit doesn't assert federation invariant)
  f10_ontology: substrate ≠ being (KVM8 vs KVM4 hash divergence is REAL drift, not artifact)
  f11_audit: 12 receipts captured, drift honestly reported
  f12_injection: no external content propagated
  f13_sovereign: PROMULGATED via F13 directive "reality test edge registry v2 against kvm4"
```

---

## 8. Writer Authority

```yaml
writer:
  agent_id: FI-003 (anonymous session)
  actor_verified: false
  authority_band: OBSERVE_ONLY
  f13_standing: NONE
  role: external_advisory_reality_test_v2_auditor (Lane B)

test_authority: F13 directive "reality test edge registry v2 against kvm4"
test_scope: KVM4 (workshop) — edge artifacts + persons.yaml drift + FED state
test_methodology: probe + fail-closed reporting per `fail-closed-federation-state` + triage per `fix-optimize-forget-flow-triage`
```

---

DITEMPA BUKAN DIBERI — Reality Test v2 against KVM4 complete per F13 directive. 12 probes, 4-bucket triage. CRITICAL FINDING: persons.yaml drift KVM8 vs KVM4 (Schema v1.1 not propagated). Edge registry KVM8-local only (not federated invariant). FORGET items: FED loopback DEAD, hermes-asi KVM4 inactive (architectural, not bugs). FLOW items: edge registry + linkage + subject-sealed pattern (working, keep). Standing by.

`#EDGE-REGISTRY-REALITY-TEST-V2-KVM4-2026-09-25`
