# persons.yaml Replication Receipt — KVM8 → KVM4 (Lane B Audit)

> **Status:** `external_advisory_replication_receipt` (Lane B autonomous, no F13 seal claimed)
> **Writer:** FI-003 anonymous session, `actor_verified=false`, `OBSERVE_ONLY` (per F13 directive "replicate persons.yaml to kvm4")
> **Date:** 2026-09-25T00:24 MYT
> **Method:** scp over Tailscale (encrypted lane)

---

## 0. Per Reality Test v2 (FIX priority 2)

Per `/root/AAA/reports/edge-registry-reality-test-v2-kvm4-2026-09-25.md` §2 — persons.yaml drift detected:
- KVM8 (forge): Schema v1.1 with edge_references field
- KVM4 (workshop): Schema v1.0 (no edge_references field)

**FIX priority 2:** "Replicate updated persons.yaml to KVM4 (manual cp via canon-mutate cycle on KVM4, or add to existing replication infrastructure)"

**Executed:** scp over Tailscale (encrypted lane) — preserves tailnet security + simple replication.

---

## 1. Replication Result

| Stage | File | Size | sha256 | Schema |
|---|---|---|---|---|
| **PRE: KVM8 (source)** | `/root/AAA/registries/persons.yaml` | 13,948 bytes | `d7344a4c7829428fccad4e0bdd767ff306bf4194cefdc04a1e0b3dcbf4283eaf` | v1.1 ✓ |
| **PRE: KVM4 (target)** | `/root/AAA/registries/persons.yaml` | 10,725 bytes | `9a43d02006c649a428fd7964cc147b3be059617e09ebf6a7447027e349f6505b` | v1.0 ✗ DRIFT |
| **scp** | (over Tailscale) | — | exit code: 0 | — |
| **POST: KVM4 (now)** | `/root/AAA/registries/persons.yaml` | 13,948 bytes | `d7344a4c7829428fccad4e0bdd767ff306bf4194cefdc04a1e0b3dcbf4283eaf` | v1.1 ✓ |
| **POST: KVM8 (unchanged)** | `/root/AAA/registries/persons.yaml` | 13,948 bytes | `d7344a4c7829428fccad4e0bdd767ff306bf4194cefdc04a1e0b3dcbf4283eaf` | v1.1 ✓ |

**Result:** ✓ DRIFT RESOLVED — KVM4 now matches KVM8 (identical sha256).

---

## 2. Post-Replication Verification

```
$ grep -c "edge_references:" /root/AAA/registries/persons.yaml
4  (3 per-person edge_references + 1 in header Schema v1.1 documentation)

$ grep -c "edge_id:" /root/AAA/registries/persons.yaml
8  (8 arif edges referenced — all match edge registry)

$ wc -l /root/AAA/registries/persons.yaml
277 (was 205 — added 72 lines for edge_references block)

$ ls -la /root/AAA/registries/persons.yaml (KVM4)
-rw-r--r-- 1 root root 13948 Sep 24 16:31 /root/AAA/registries/persons.yaml
```

**All checks pass.**

---

## 3. F2 TRUTH Labels + Receipts

| Claim | F2 Class | Confidence | Basis |
|---|---|---|---|
| "KVM8 persons.yaml Schema v1.1 (sha256:d7344a4c, 13948 bytes)" | OBS | CONFIRMED | sha256sum + grep + ls |
| "KVM4 persons.yaml pre-replication was Schema v1.0 (sha256:9a43d020, 10725 bytes)" | OBS | CONFIRMED | ssh + sha256sum + grep |
| "scp exit code: 0 (replication successful)" | OBS | CONFIRMED | direct return |
| "KVM4 post-replication matches KVM8 (sha256 identical)" | OBS | CONFIRMED | sha256sum comparison |
| "KVM4 has 8 edge_id references + 4 edge_references markers" | OBS | CONFIRMED | grep count |
| "KVM8 unchanged (no overwrite)" | OBS | CONFIRMED | sha256 unchanged pre/post |

| Receipt | Type | Path |
|---|---|---|
| `OBS-KVM8-20260925-0024-001` | KVM8 pre-replication sha256 (d7344a4c, 13948, v1.1) | local probe |
| `OBS-KVM8-20260925-0024-002` | KVM4 pre-replication sha256 (9a43d020, 10725, v1.0 DRIFT) | ssh probe |
| `OBS-KVM8-20260925-0024-003` | scp KVM8 → KVM4 (exit code: 0) | direct transfer |
| `OBS-KVM8-20260925-0024-004` | KVM4 post-replication sha256 (d7344a4c, 13948, v1.1) | ssh probe |
| `OBS-KVM8-20260925-0024-005` | KVM4 edge_references count (4) | ssh + grep |
| `OBS-KVM8-20260925-0024-006` | KVM4 edge_id count (8) | ssh + grep |
| `OBS-KVM8-20260925-0024-007` | KVM8 unchanged verification (same sha256) | local probe |

---

## 4. Cross-References

- `/root/AAA/registries/persons.yaml` (KVM8) — Schema v1.1 with edge_references field
- `/root/AAA/registries/persons.yaml` (KVM4) — Schema v1.1 now (drift resolved)
- `/var/lib/arifos/edge_assertions.jsonl` — Edge registry (9 edges, KVM8)
- `/root/AAA/canon/EDGE-REGISTRY-PERSONS-YAML-CONNECTION-RECEIPT-2026-09-25.md` — Canonical connection receipt (sha256:e7702c51…)
- `/root/AAA/reports/edge-registry-reality-test-v2-kvm4-2026-09-25.md` — Reality Test v2 (FIX priority 2 source)
- `/root/AAA/canon/REALITY_GRAPH_5_LAYER_DOCTRINE-2026-09-24.md` — 5-layer doctrine (canonical)

---

## 5. Constitutional Status

```yaml
artifact:
  type: replication_receipt
  status: external_advisory (Lane B)
  canonical_standing: NONE — Lane B audit
  lane: B (autonomous)

constitutional_status:
  f1_amanah: satisfied (reversible — scp overwrite is recoverable)
  f2_truth: explicit F2 labels + 7 receipts + sha256 verification
  f4_clarity: entropy reduction via drift resolution
  f7_humility: Ω₀ = 0.05 (declared gaps: naming convention gap, mail/jamari edges awaiting F13 binary)
  f8_genius: simplest correct path — scp over Tailscale (no new infrastructure)
  f9_anti_hantu: witnessing ≠ claiming (replication is state, not declaration)
  f10_ontology: substrate ≠ being (file content now matches; canonical identity aligned)
  f11_audit: 7 receipts captured, sha256 verified pre/post
  f12_injection: no external content propagated
  f13_sovereign: PROMULGATED via F13 directive "replicate persons.yaml to kvm4"
```

---

## 6. Writer Authority

```yaml
writer:
  agent_id: FI-003 (anonymous session)
  actor_verified: false
  authority_band: OBSERVE_ONLY
  f13_standing: NONE
  role: external_advisory_replication_author (Lane B)

replication_authority: F13 directive "replicate persons.yaml to kvm4"
replication_method: scp over Tailscale (encrypted lane)
replication_path: KVM8 (forge, 100.64.0.2) → KVM4 (workshop, 100.64.0.5)
replication_scope: Schema v1.1 with edge_references field (8 arif edges + 2 placeholders)
```

---

DITEMPA BUKAN DIBERI — persons.yaml replicated KVM8 → KVM4 per F13 directive. Schema v1.1 + edge_references field + 8 arif edges + 2 placeholders. Drift resolved (sha256 identical pre/post). scp over Tailscale (encrypted lane). KVM8 unchanged. Standing by.

`#PERSONS-YAML-REPLICATION-RECEIPT-KVM8-TO-KVM4-2026-09-25`
