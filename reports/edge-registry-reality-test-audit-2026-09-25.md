# Edge Registry — Reality Test Audit (Lane B)

> **Status:** `external_advisory_reality_test` (Lane B autonomous, no F13 seal claimed)
> **Writer:** FI-003 anonymous session, `actor_verified=false`, `OBSERVE_ONLY` (per F13 directive "reality test edge registry against federation")
> **Date:** 2026-09-25T00:14 MYT

---

## 0. Per `federation-invariant-identification-20260906`

The Edge Registry exists locally on KVM8 (`/var/lib/arifos/edge_assertions.jsonl`). A reality test must validate against actual federation data, not just internal consistency.

**Per the memory's split-brain test:** *a component must be federated as an invariant iff two nodes can silently disagree about it at the same moment.*

This audit probes 3 nodes + cross-registry sources to detect silent disagreement.

---

## 1. Federation Data Sources Probed

| Source | Node | Path/Endpoint | Status | Receipts |
|---|---|---|---|---|
| **arifFlow KVM8** | KVM8 forge | `:7073/health` | ✓ ALIVE | 1000 (v3-vector) |
| **arifFlow KVM4** | KVM4 workshop | `:7073/health` | ✗ NOT REACHABLE | — (port refused) |
| **arifFlow KVM2** | KVM2 witness | `:7073/health` | ⚠ PARTIAL (0 receipts, 0 actors) | 0 (UNMEASURED verdict) |
| **HERMES lanes (KVM8)** | KVM8 forge | `/root/.hermes/lanes/people.yaml` | ✓ LIVE | 7 lane names |
| **persons.yaml** | KVM8 forge | `/root/AAA/registries/persons.yaml` | ✓ UPDATED | 3 constitutional + 8 edge_refs |
| **Edge registry** | KVM8 forge | `/var/lib/arifos/edge_assertions.jsonl` | ✓ LIVE (append-only) | 9 edges |
| **seal_chain** | KVM8 vault | `/root/.local/share/arifos/vault999/seal_chain.jsonl` | ✓ LIVE | 40+ entries (seq 40 confirmed) |
| **VAULT999** | symlink | `/root/VAULT999 → /root/arifOS/VAULT999` | ✓ resolved per `VAULT999 is a symlink` memory |

---

## 2. Per `fail-closed-federation-state` — fail-closed reporting

| Probe | Result | Honest Report |
|---|---|---|
| KVM8 arifFlow | OK, 1000 receipts | "OK 1000" |
| KVM4 arifFlow | connection refused on :7073 | "**UNKNOWN** — port refused" (NOT 0) |
| KVM2 arifFlow | alive but 0 receipts | "**UNKNOWN** — empty state plane, cannot determine" (NOT 0) |

---

## 3. Cross-Reference: Edge Registry ↔ HERMES Lanes ↔ persons.yaml

| Edge registry subject (canonical_id) | HERMES lane display_name | Match? |
|---|---|---|
| `human:arif` | Arif (sovereign) | ✓ MATCH |
| `human:syed_khairuddin` | Syed (Abang Sado) | ✓ MATCH (name variant) |
| `human:jia` | Jia | ✓ MATCH |
| `human:azwa` | Azwa (adik Arif) | ✓ MATCH |
| `human:nabilah` | (not in lanes) | ✗ NOT IN LANES |
| `human:mak` | (not in lanes) | ✗ NOT IN LANES |
| `org:petronas` | (not in lanes — org not person) | n/a |
| `corporate_decision` | (not in lanes — abstract) | n/a |
| (edge registry has no entry for these) | PAAN (kelas sado) | ✗ MISSING FROM EDGE REGISTRY |
| (edge registry has no entry for these) | Ahmad Lutfi bin Muhd Khadri | ✗ MISSING FROM EDGE REGISTRY |
| (edge registry has no entry for these) | Faqwan | ✗ MISSING FROM EDGE REGISTRY |

**Net:** 4 of 7 HERMES names have edge coverage (arif, syed, jia, azwa). 3 names missing (PAAN, Lutfi, Faqwan). 2 edge names missing from HERMES (nabilah, mak).

---

## 4. Edge ↔ persons.yaml Cross-Reference

```
Arif edges in edge registry:        8
Arif edge_ids in persons.yaml:       8 (Schema v1.1 edge_references field)
Match: 8/8 (100%)
```

**Per receipt:** `edge-registry-persons-yaml-connection-receipt-2026-09-25.md` (canonical, sha256:e7702c51…)

---

## 5. Naming Convention Gap (Honest Disclosure)

HERMES lane uses display_name ("Syed"); edge registry uses canonical_id ("human:syed_khairuddin"). This is a **naming convention gap** — both refer to the same entity but with different identifier conventions.

**Per `naming-doctrine`:** kata nama am vs khas — display names are common nouns (Syed, Jia, Azwa), canonical_ids are proper nouns (human:syed_khairuddin). Both layers have their use.

**Resolution path:** Edge registry's `human:*` prefix should match persons.yaml's `id:` field format. Currently:
- HERMES uses: `Syed` (display_name)
- Edge registry uses: `human:syed_khairuddin` (canonical_id)
- persons.yaml uses: `syed_khairuddin` (id, no human: prefix)

→ 3 different conventions for the same entity. F13 binary needed for naming canonicalization.

---

## 6. seal_chain.jsonl — Governance Event Layer

Path: `/root/.local/share/arifos/vault999/seal_chain.jsonl` (447,447 bytes, append-only)

| Field | Sample (seq 40, latest probed) |
|---|---|
| `actor` | arif (F13 SOVEREIGN) |
| `actor_verification.actor_verified` | true |
| `actor_verification.method` | ed25519_verified |
| `authority_state` | SOVEREIGN |
| `decision_reference` | SOV-3278ad34e404 |
| `verdict` | SEAL |
| `reversibility` | IRREVERSIBLE |
| `signature` | verified (or hmac-sha256) |

**Reality Test result:** seal_chain captures GOVERNANCE EVENTS (seals, decisions), not RELATIONSHIP EDGES. Edge schema differs from seal_chain schema. They are LAYERED, not duplicate.

---

## 7. KVM4/KVM2 Reality Test Gaps (Fail-Closed Reporting)

| Node | Reality Test Status |
|---|---|
| **KVM8** | ✓ FULL — edge registry LIVE, 9 edges, queryable, linked to persons.yaml, cross-referenced to HERMES lanes |
| **KVM4** | ✗ **UNKNOWN** — arifFlow :7073 connection refused; cannot determine if KVM4 has equivalent edge registry |
| **KVM2** | ⚠ **UNKNOWN** — arifFlow alive but 0 receipts; KVM2 is witness-pending per memory `kvm-mesh-truth-20260903` |

**Per `terminal-guard-before-creation` + `federation-invariant-identification-20260906`:** Edge Registry is NOT yet federated as invariant. KVM4 + KVM2 may silently disagree with KVM8.

**Honest disclosure per `audit-error-not-governance-success`:** file existing (KVM8) ≠ federation invariant. The Edge Registry is currently KVM8-local; cross-node replication would require `canon-replicate`-style infrastructure.

---

## 8. F2 TRUTH Labels + Receipts

| Claim | F2 Class | Confidence | Basis |
|---|---|---|---|
| "KVM8 edge registry has 9 edges" | OBS | CONFIRMED | `wc -l` + JSON parse |
| "KVM4 arifFlow unreachable on :7073" | OBS | CONFIRMED | `curl --max-time 5` failed |
| "KVM2 arifFlow has 0 receipts" | OBS | CONFIRMED | live health probe |
| "8/8 arif edges match between registry and persons.yaml" | OBS | CONFIRMED | grep cross-reference |
| "HERMES has 7 lane names; edge registry covers 4 of them" | OBS | CONFIRMED | regex extraction |
| "Naming convention gap: HERMES display vs edge canonical vs persons id" | INT | CONFIRMED | 3-way regex |
| "Edge Registry is KVM8-local, NOT yet federated invariant" | DER | PLAUSIBLE | per `federation-invariant-identification-20260906` |
| "seal_chain captures governance events (not relationship edges)" | INT | CONFIRMED | schema diff (governance vs relationship) |

| Receipt | Type | Path |
|---|---|---|
| `OBS-KVM8-20260925-0014-001` | arifFlow KVM8 health probe (1000 receipts) | live probe |
| `OBS-KVM8-20260925-0014-002` | arifFlow KVM4 connection refused | live probe |
| `OBS-KVM8-20260925-0014-003` | arifFlow KVM2 health (0 receipts) | live probe |
| `OBS-KVM8-20260925-0014-004` | HERMES lanes/people.yaml (7 names) | live probe |
| `OBS-KVM8-20260925-0014-005` | persons.yaml edges (8 arif) | live probe |
| `OBS-KVM8-20260925-0014-006` | Edge registry (9 edges, append-only) | live probe |
| `OBS-KVM8-20260925-0014-007` | seal_chain.jsonl (447K bytes, 40+ entries, seq 40 verified) | live probe |
| `OBS-KVM8-20260925-0014-008` | VAULT999 symlink resolved | live probe (per `VAULT999 is a symlink` memory) |
| `OBS-KVM8-20260925-0014-009` | HERMES lane name cross-reference (4/7 coverage) | live probe |

---

## 9. Cross-References

- `/root/AAA/canon/EDGE-REGISTRY-PERSONS-YAML-CONNECTION-RECEIPT-2026-09-25.md` — Connection receipt (canonical, promoted)
- `/var/lib/arifos/edge_assertions.jsonl` — Edge registry (live, append-only)
- `/root/.local/share/arifos/vault999/seal_chain.jsonl` — Governance events
- `/root/AAA/registries/persons.yaml` — Identity registry (Schema v1.1, linked)
- `/root/.hermes/lanes/people.yaml` — Lane cards (HERMES convention)
- `/var/lib/arifflow/receipts.jsonl` — arifFlow receipts (KVM8)
- `/var/lib/arifos/replication_receipts.jsonl` — canon-replicate cron receipts (KVM8 → KVM2)
- `/root/forge_work/2026-09-24-FI-003-small-world-helix-realitygraph-linkage.md` — Edge Registry research recommendation (same session, FI-003)
- `/root/AAA/canon/REALITY_GRAPH_5_LAYER_DOCTRINE-2026-09-24.md` — 5-layer doctrine (canonical)
- `/root/AAA/canon/REALITY_GRAPH.md` — Reality Graph doctrine (parent_assertion_ids pattern)

---

## 10. Constitutional Status

```yaml
artifact:
  type: reality_test_audit
  status: external_advisory (Lane B)
  canonical_standing: NONE — Lane B audit, not canon
  lane: B (autonomous)

constitutional_status:
  f1_amanah: satisfied (reversible audit)
  f2_truth: explicit F2 labels + 9 receipts + fail-closed reporting per `fail-closed-federation-state`
  f4_clarity: entropy reduction via 3-node split-brain test
  f7_humility: Ω₀ = 0.05 (declared gaps: KVM4 unknown, KVM2 unknown, naming convention gap)
  f8_genius: simplest correct path (probe + report — no edge mutation)
  f9_anti_hantu: witnessing ≠ claiming (audit doesn't assert federation invariant)
  f10_ontology: substrate ≠ being (HERMES display ≠ edge canonical ≠ persons id)
  f11_audit: 9 receipts captured, cross-references documented
  f12_injection: no external content propagated; fail-closed used for missing data
  f13_sovereign: PROMULGATED via F13 directive "reality test edge registry against federation"
```

---

## 11. Writer Authority

```yaml
writer:
  agent_id: FI-003 (anonymous session)
  actor_verified: false
  authority_band: OBSERVE_ONLY
  f13_standing: NONE
  role: external_advisory_reality_test_auditor (Lane B)

test_authority: F13 directive "reality test edge registry against federation"
test_scope: 3-node federation + cross-registry sources
test_methodology: probe + fail-closed reporting per `fail-closed-federation-state` memory
```

---

DITEMPA BUKAN DIBERI — Reality Test complete per F13 directive. KVM8 verified FULL (8/8 arif edges, 9 total edges, linked to persons.yaml, cross-ref to HERMES). KVM4 + KVM2 fail-closed reported as UNKNOWN (not 0). Naming convention gap documented honestly. seal_chain layer distinguished from edge layer. 9 receipts captured. Honest gaps surfaced for F13 binary.

`#EDGE-REGISTRY-REALITY-TEST-AUDIT-2026-09-25`
