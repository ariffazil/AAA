# Edge Registry ↔ persons.yaml Connection Receipt (Lane B Audit)

> **Status:** `external_advisory_connection_receipt` (Lane B autonomous, no F13 seal claimed)
> **Writer:** FI-003 anonymous session, `actor_verified=false`, `OBSERVE_ONLY` (per F13 directive "link persons.yaml to edge registry")
> **Date:** 2026-09-25T00:10 MYT

---

## 0. Per `small-world-helix-linkage-20260924` + Identity Continuity doctrine

Per memory recommendation:
> "relationship assertions ride the Reality Graph as receipts ... with testimony staying in H/P-axis files (subject-sealed wins)"

**Subject-sealed = the SUBJECT's identity record holds the testimony about edges where they're involved.**

This implementation links persons.yaml (P-axis — Person registry) to edge_assertions.jsonl (Reality Graph receipts).

---

## 1. Implementation Summary

| Component | Path | Status |
|---|---|---|
| **persons.yaml** | `/root/AAA/registries/persons.yaml` | ✓ UPDATED (Schema v1.1, edge_references field added) |
| **Edge registry** | `/var/lib/arifos/edge_assertions.jsonl` | ✓ LIVE (9 edges, append-only) |
| **Query tool** | `/root/AAA/instructions/query_edges.py` | ✓ LIVE (executable) |

---

## 2. persons.yaml Updates

```
File:    /root/AAA/registries/persons.yaml
Before:  10703 bytes, 205 lines
After:   13948 bytes, 277 lines (+3245 bytes, +72 lines)
Header:  Added Schema v1.1 annotation (edge_references field documented)
Schema:  v1.0 → v1.1 (backward-compatible — old consumers ignore new field)
```

### 2.1 — arif entry (F13 SOVEREIGN)

```yaml
edge_references:
  # 8 edges total — 6 where arif is subject, 2 where arif is object
  - edge_id: "edge:human:arif:employed_by:org:petronas"
    layer: relationship
    role: subject (employed_by petronas)
    confidence: 1.0
    witness: human:arif
    sensitivity: private
  - edge_id: "edge:human:arif:knows:human:syed_khairuddin"
    layer: relationship
    role: subject (knows syed)
    confidence: 0.95
    witness: human:arif
    sensitivity: F5_PROTECTED
    note: "Chosen familial figure (BM Abang = older brother, but chosen, not biological)"
  - edge_id: "edge:human:arif:family_of:human:jia"
    layer: relationship
    role: subject (jia's brother)
    confidence: 1.0
    witness: human:arif
    sensitivity: F5_PROTECTED
  - edge_id: "edge:human:arif:family_of:human:azwa"
    layer: relationship
    role: subject (azwa's brother)
    confidence: 1.0
    witness: human:arif
    sensitivity: F5_PROTECTED
  - edge_id: "edge:human:arif:family_of:human:nabilah"
    layer: relationship
    role: subject (nabilah's brother)
    confidence: 1.0
    witness: human:arif
    sensitivity: F5_PROTECTED
  - edge_id: "edge:human:arif:family_of:human:mak"
    layer: relationship
    role: subject (mak's son)
    confidence: 1.0
    witness: human:arif
    sensitivity: F5_PROTECTED
  - edge_id: "edge:org:petronas:influences:human:arif"
    layer: authority
    role: object (petronas influences arif)
    confidence: 0.85
    witness: public_knowledge
    sensitivity: private
  - edge_id: "edge:corporate_decision:may_affect:human:arif"
    layer: consequence
    role: object (corporate decisions affect arif)
    confidence: 0.85
    witness: public_knowledge
    sensitivity: private
```

### 2.2 — mail entry (placeholder, no edges yet)

```yaml
edge_references:
  # Currently empty — F13 binary needed to add Mail↔Arif witness testimony edge
  - placeholder: true
    status: awaiting_F13_binary_for_Mail_testimony_edge
    sensitivity: F5_PROTECTED
    note: "Mail is witness/off_switch_holder per privacy_boundaries above"
```

### 2.3 — jamari entry (placeholder, no edges yet)

```yaml
edge_references:
  # Currently empty — F13 binary required (consent_status: none per privacy_boundaries)
  - placeholder: true
    status: awaiting_F13_binary_for_Jamari_testimony_edge
    sensitivity: F5_PROTECTED
    note: "Jamari has consent_status: none; HIGH PRIVACY PERSON; edges deferred per F13 ack only"
```

---

## 3. Cross-Reference Verification

```
Query: arif's edges in edge registry
  edge:human:arif:employed_by:org:petronas ✓
  edge:human:arif:knows:human:syed_khairuddin ✓
  edge:human:arif:family_of:human:jia ✓
  edge:human:arif:family_of:human:azwa ✓
  edge:human:arif:family_of:human:nabilah ✓
  edge:human:arif:family_of:human:mak ✓
  edge:org:petronas:influences:human:arif ✓
  edge:corporate_decision:may_affect:human:arif ✓

Reference: arif's edge_ids in persons.yaml
  edge:human:arif:employed_by:org:petronas ✓
  edge:human:arif:knows:human:syed_khairuddin ✓
  edge:human:arif:family_of:human:jia ✓
  edge:human:arif:family_of:human:azwa ✓
  edge:human:arif:family_of:human:nabilah ✓
  edge:human:arif:family_of:human:mak ✓
  edge:org:petronas:influences:human:arif ✓
  edge:corporate_decision:may_affect:human:arif ✓

Match: 8/8 (100%)
```

---

## 4. Schema (backward-compatible)

| Field | Type | Required | Description |
|---|---|---|---|
| `edge_references` | array of edge objects | per-person | Subject-sealed testimony — links to Reality Graph edge receipts |
| `edge_references[].edge_id` | string | required | Unique edge ID (must match /var/lib/arifos/edge_assertions.jsonl) |
| `edge_references[].layer` | string | required | relationship \| authority \| consequence \| reality |
| `edge_references[].role` | string | required | subject \| object (per edge's subject/object position) |
| `edge_references[].confidence` | float | required | 0.0-1.0 (per Reality Graph receipt) |
| `edge_references[].witness` | string | required | Witness canonical_id (per receipt) |
| `edge_references[].sensitivity` | string | required | public \| private \| F5_PROTECTED |
| `edge_references[].note` | string | optional | Human-readable context |
| `edge_references[].placeholder` | bool | if empty | Marker: this person has no edges yet (awaiting F13 binary) |
| `edge_references[].status` | string | if placeholder | Status of pending edge work |

---

## 5. F2 TRUTH Labels + Receipts

| Claim | F2 Class | Confidence | Basis |
|---|---|---|---|
| "8/8 arif edges match between registry and persons.yaml" | OBS | CONFIRMED | grep cross-reference verified |
| "mail + jamari edge_references are placeholders (no edges yet)" | OBS | CONFIRMED | grep -A5 verification |
| "Schema v1.1 added edge_references field (backward-compatible)" | INT | CONFIRMED | Header annotation present |
| "Subject-sealed testimony: subject's record holds edge references" | DER | CONFIRMED | Per memory `small-world-helix-linkage-20260924` |
| "Witnesses for mail + jamari edges awaiting F13 binary" | INT | CONFIRMED | privacy_boundaries + consent_status constraints |

| Receipt | Type | Path |
|---|---|---|
| `OBS-KVM8-20260925-0010-001` | persons.yaml probe (Schema v1.0) | live probe |
| `OBS-KVM8-20260925-0010-002` | arif entry boundaries (37-64) | live probe |
| `OBS-KVM8-20260925-0010-003` | mail entry boundaries (65-120) | live probe |
| `OBS-KVM8-20260925-0010-004` | jamari entry boundaries (121+) | live probe |
| `OBS-KVM8-20260925-0010-005` | Edge registry arif count (8) | live probe |
| `OBS-KVM8-20260925-0010-006` | persons.yaml arif edge_ids count (8) | live probe |
| `OBS-KVM8-20260925-0010-007` | Match check (8/8) | live probe |

---

## 6. Cross-References

- `/root/AAA/registries/persons.yaml` — P-axis (Person registry) — UPDATED (Schema v1.1)
- `/var/lib/arifos/edge_assertions.jsonl` — Reality Graph receipts (append-only)
- `/root/AAA/instructions/query_edges.py` — Query tool
- `/root/AAA/canon/REALITY_GRAPH_5_LAYER_DOCTRINE-2026-09-24.md` — 5-layer doctrine (just promoted this session)
- `/root/AAA/canon/REALITY_GRAPH.md` — Reality Graph doctrine (parent_assertion_ids pattern)
- `/root/AAA/instructions/identity-continuity.md` — Identity as cross-cutting primitive (F13-ratified 2026-09-08)

---

## 7. Constitutional Status

```yaml
artifact:
  type: connection_receipt
  status: external_advisory (Lane B)
  canonical_standing: NONE — backward-compatible schema evolution
  lane: B (autonomous)

constitutional_status:
  f1_amanah: satisfied (reversible — added field, not deleted)
  f2_truth: explicit F2 labels + 7 receipts + cross-reference check
  f4_clarity: entropy reduction via subject-sealed cross-references
  f7_humility: Ω₀ = 0.05 (declared gaps: mail + jamari edges awaiting F13 binary)
  f8_genius: simplest correct path (extend existing schema, no new artifact)
  f9_anti_hantu: witnessing ≠ claiming (edges are receipts, not state claims)
  f10_ontology: substrate ≠ being (canonical_id ≠ person; edge_id ≠ relationship)
  f11_audit: receipt + append-only + cross-reference check
  f12_injection: external content not propagated (only existing canon referenced)
  f13_sovereign: PROMULGATED via F13 directive "link persons.yaml to edge registry"
```

---

## 8. Writer Authority

```yaml
writer:
  agent_id: FI-003 (anonymous session)
  actor_verified: false
  authority_band: OBSERVE_ONLY
  f13_standing: NONE
  role: external_advisory_connection_author (Lane B)

connection_authority: F13 directive "link persons.yaml to edge registry"
connection_path: persons.yaml (P-axis) ←edge_references→ edge_assertions.jsonl (Reality Graph)
promotion_required: NO (backward-compatible schema evolution, no F13 seal needed)
```

---

DITEMPA BUKAN DIBERI — Edge Registry linked to persons.yaml per F13 directive. Schema v1.1 (backward-compatible). Subject-sealed testimony per memory recommendation. 8/8 arif edges referenced + 2 placeholders for mail/jamari (awaiting F13 binary). 7 receipts captured.

`#EDGE-REGISTRY-PERSONS-YAML-CONNECTION-RECEIPT-2026-09-25`
