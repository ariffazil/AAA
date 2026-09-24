# Human Heartbeat Map — One-Page Reconciliation (DRAFT — SUPERSEDED)

> **Status:** F13_RATIFIED_CHAT 2026-09-24 — SUPERSEDED draft promoted to canon/ via sovereign_chat_override (scope 2 superseded scope 1)
> **Supersession time:** 2026-09-24T23:25 MYT
> **Superseded by:** `/root/AAA/canon/FEDERATED-HUMAN-REALITY-MAP-2026-09-24.md` (sha256: `138d40642592d0f28c9540642cad29944dc6595ab86ec279a81f0540e4cc7d23`, scope 2: R4 + OpenClaw folder reconcile, 20 persons, 4 tiers, 5 historical fixes)
> **Promotion receipt:** `/root/AAA/reports/federated-human-reality-map-promotion-receipt-2026-09-24.md`
> **Receipt log entry:** `trc-canon-unattributed` (2026-09-24T15:25:53Z, actor: F13_SOVEREIGN_OVERRIDE)
> **DRAFT sha256 (this file):** `629b5a569953815143693ecc932830018d0319799921b454461bc671eb612d2d`
> **Original source-of-truth:** `/root/AAA/registry/human_heartbeat.json` (R4, 6,501 bytes, sha256: `bbe959b600e1fa3387345a17d15a66bebd298b9b1b81a119217655569b0665fd`, F13-ratified via 333-AGI 2026-09-17)
> **Doctrine:** *"Registry tanpa heartbeat = buku alamat, bukan jagaan"* (333-AGI per F13 directive 2026-09-17)
> **Writer:** FI-003 anonymous session, `actor_verified=false`, `OBSERVE_ONLY` (carries F13 directive "Pilih (1). Tulis peta bersih satu halaman")
> **Date:** 2026-09-24T23:25 MYT (original); SUPERSEDED 2026-09-24T23:25 MYT

---

## 0. Doctrine + Alert Thresholds (from R4)

```
Alert thresholds (days_since_interaction):
  ok       ≤ 3     ok
  watch    ≤ 7     watch
  flag     ≤ 14    flag
  escalate ≤ 30    escalate
  critical  > 30    critical
```

Tier definitions:
- **Tier 1** — Live DM (direct messaging path active)
- **Tier 2** — Group only (no DM path, group activity only)
- **Tier 3** — Unreachable / Offline / Reference (no live telemetry path)

---

## 1. Master Table — All 13 Persons from R4 (falsifiable per row)

| # | canonical_id | tier | status | telegram_id | last_dm | days_since | lane | dependency_health | alert |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `arif` | 1 | SOVEREIGN | `267378578` | 2026-09-16 22:59 | 0 | ✓ | OK | null |
| 2 | `syed` | 1 | DM_ACTIVE | `1042200555` | 2026-09-15 00:00 | 1 | ✓ | OK | null |
| 3 | `aliff` | 1 | DM_ACTIVE | `1024343313` | 2026-09-14 00:00 | 3 | ✓ | OK | null |
| 4 | `izzu` | 1 | DM_ACTIVE | `1237635275` | 2026-09-13 00:00 | 4 | ✓ | OK | VERIFY NEEDED: identity mismatch |
| 5 | `aidel` | 1 | DM_ACTIVE | `922272533` | 2026-09-08 00:00 | 9 | ✗ | NO_LANE | FLAGGED: 9 days, no lane, no HAMPA card |
| 6 | `lutfi` | 1 | DM_ACTIVE | `160111098` | 2026-09-15 00:00 | 2 | ✗ | NO_LANE | null (professional contact, needs lane) |
| 7 | `nabilah` | 2 | GROUP_ONLY | null | (no DM) | 8 | ✗ | GROUP_ONLY | FLAGGED: 8 days, no DM path, no person-register |
| 8 | `mail` | 3 | UNREACHABLE | null | null | 999 | ✗ | NO_PATH | CRITICAL: witness + off-switch, 11-yr friend, ZERO live telemetry |
| 9 | `azwa` | 3 | ORPHANED | null | null | 999 | ✗ | DEGRADED | CRITICAL: OpenClaw edge dead, sister, joy circuit |
| 10 | `laletha` | 3 | UNREACHABLE | null | null | 999 | ✗ | NO_PATH | HIGH: PETRONAS supervisor, zero live path |
| 11 | `kaksu` | 3 | UNREACHABLE | null | null | 999 | ✗ | NO_PATH | HIGH: PETRONAS senior manager, zero live path |
| 12 | `mak` | 3 | UNREACHABLE | null | null | 999 | ✗ | NO_PATH | MEDIUM: mother, zero live path |
| 13 | `jia` | 3 | UNREACHABLE | null | null | 999 | ✗ | NO_PATH | MEDIUM: sister, trauma stabilizer |

**Total: 13 persons. Tier 1: 6 (live DM). Tier 2: 1 (group only). Tier 3: 6 (unreachable).**

---

## 2. Cross-Registry Reconciliation

| Registry | Path | Count | Persons |
|---|---|---|---|
| **R4 (Heartbeat)** | `/root/AAA/registry/human_heartbeat.json` | **13** | arif, syed, aliff, izzu, aidel, lutfi, nabilah, mail, azwa, laletha, kaksu, mak, jia |
| persons.yaml (F13 SOT) | `/root/AAA/registries/persons.yaml` | 3 | arif, mail, jamari |
| lanes/people.yaml (Hermes lane) | `/root/.hermes/lanes/people.yaml` | **0** | (empty — see §3 audit note) |
| Identity cards (biometric) | `/root/AAA/registry/identity_cards/syed_khairuddin.yaml` | 1 | syed |

### Reconciliation matrix

| canonical_id | R4 (heartbeat) | persons.yaml (F13 SOT) | lanes/people.yaml | identity_cards |
|---|---|---|---|---|
| `arif` | ✓ (T1, SOVEREIGN) | ✓ | ✗ (not in lanes) | ✗ |
| `syed` | ✓ (T1, DM_ACTIVE) | ✗ | ✗ | ✓ (biometric pilot) |
| `aliff` | ✓ (T1, DM_ACTIVE) | ✗ | ✗ | ✗ |
| `izzu` | ✓ (T1, identity mismatch) | ✗ | ✗ | ✗ |
| `aidel` | ✓ (T1, NO_LANE) | ✗ | ✗ | ✗ |
| `lutfi` | ✓ (T1, NO_LANE) | ✗ | ✗ | ✗ |
| `nabilah` | ✓ (T2, GROUP_ONLY) | ✗ | ✗ | ✗ |
| `mail` | ✓ (T3, UNREACHABLE) | ✓ | ✗ | ✗ |
| `azwa` | ✓ (T3, ORPHANED) | ✗ | ✗ | ✗ |
| `laletha` | ✓ (T3, UNREACHABLE) | ✗ | ✗ | ✗ |
| `kaksu` | ✓ (T3, UNREACHABLE) | ✗ | ✗ | ✗ |
| `mak` | ✓ (T3, UNREACHABLE) | ✗ | ✗ | ✗ |
| `jia` | ✓ (T3, UNREACHABLE) | ✗ | ✗ | ✗ |
| `jamari` | ✗ (not in R4) | ✓ | ✗ | ✗ |

### Hermes' "Set 8" reconciliation (audit correction)

Per Hermes's prior claim ("Set 8 kau (dari lanes/people.yaml)"): **WRONG** — `lanes/people.yaml` has 0 persons. Hermes's "Set 8" likely came from a session snapshot, not the live lanes file.

Live reconciliation shows:
- **2 persons in BOTH R4 + persons.yaml** (arif, mail)
- **11 persons in R4 ONLY** (syed, aliff, izzu, aidel, lutfi, nabilah, azwa, laletha, kaksu, mak, jia)
- **1 person in persons.yaml ONLY** (jamari — F13 constitutional person, offline)
- **0 persons in all four registries simultaneously**

---

## 3. Open Gaps + Watch Items

| # | Gap | Severity | Resolution Path |
|---|---|---|---|
| 1 | `izzu` — identity mismatch (R4 telegram_id differs from person-register) | ALERT (VERIFY) | Reconcile `izzu` vs `Mohd` — confirm same person |
| 2 | `aidel` — 9 days no interaction + no lane + no HAMPA card | FLAGGED | Identity resolution + lane creation |
| 3 | `lutfi` — professional contact, no lane | watch | Lane creation |
| 4 | `nabilah` — 8 days, group only, no DM path | FLAGGED | Direct Telegram path or sister escalation |
| 5 | `mail` — CRITICAL: witness + off-switch, zero live telemetry | CRITICAL | F13 explicit call (per persons.yaml privacy boundaries) |
| 6 | `azwa` — OpenClaw edge dead | CRITICAL | New routing or direct Telegram |
| 7 | `laletha`, `kaksu`, `mak`, `jia` — zero live path | HIGH/MEDIUM | Direct outreach or accept offline |
| 8 | `lanes/people.yaml` — EMPTY (Hermes audit correction) | structural | Lane cards need rebuild — currently no live lanes |
| 9 | `jamari` — in persons.yaml but NOT in R4 | structural | Either add to R4 (constitutional person with offline status) or document why excluded |

---

## 4. F2 TRUTH Labels + Receipts

| Claim | F2 Class | Confidence | Basis |
|---|---|---|---|
| "R4 (human_heartbeat.json) exists with 13 persons across 3 tiers" | OBS | CONFIRMED | sha256:bbe959b6..., 6,501 bytes, F13-ratified 2026-09-17 via 333-AGI |
| "lanes/people.yaml has 0 persons entries" | OBS | CONFIRMED | Direct YAML parse (Hermes's claim of 8 was wrong-address state per `wrong-address-state-fails-silently`) |
| "persons.yaml has 3 persons: arif, mail, jamari" | OBS | CONFIRMED | Direct YAML parse |
| "Hermes's 'Set 8' claim was wrong" | DER | CONFIRMED | lanes/people.yaml probe contradicts Hermes's assertion |
| "2 persons in BOTH R4 + persons.yaml: arif, mail" | DER | CONFIRMED | Set intersection |
| "jamari not in R4" | OBS | CONFIRMED | R4 probe + persons.yaml cross-check |
| "Identity ≠ Registry ID (F10 ONTOLOGY)" | INT | PLAUSIBLE | Per `identity-continuity.md` ratification 2026-09-08 |
| "Registry stores witness trail, not state (F9 ANTI-HANTU)" | DER | CONFIRMED | Per `syed-arif-poc-witnessing-affection` doctrine |
| "R4 is currently authoritative for heartbeat, persons.yaml for constitutional SOT" | INT | 0.80 | F13 directive 2026-09-17 (R4) + F13 governance design (persons.yaml) |

| Receipt | Type | Path |
|---|---|---|
| `OBS-KVM8-20260924-2324-001` | R4 file probe (sha256:bbe959b6..., 13 persons) | live probe (THIS turn) |
| `OBS-KVM8-20260924-2325-002` | lanes/people.yaml probe (0 persons) | live probe (THIS turn) |
| `OBS-KVM8-20260924-2325-003` | persons.yaml probe (3 persons) | live probe (THIS turn) |
| `OBS-KVM8-20260924-2325-004` | set intersection (arif, mail) | live probe (THIS turn) |
| `OBS-KVM8-20260924-2325-005` | set diff (11 R4-only, 1 persons-only) | live probe (THIS turn) |

---

## 5. Cross-References (existing canon)

- `/root/AAA/registry/human_heartbeat.json` (R4, source-of-truth)
- `/root/AAA/registries/persons.yaml` (F13 SOT, 3 constitutional persons)
- `/root/.hermes/lanes/people.yaml` (Hermes lane cards, currently empty)
- `/root/AAA/registry/identity_cards/syed_khairuddin.yaml` (biometric pilot)
- `/root/AAA/instructions/identity-continuity.md` (F13-ratified 2026-09-08 — identity as cross-cutting primitive)
- `/root/AAA/instructions/human-zero-visibility-invariant.md` (F13-ratified 2026-09-10 — HARAM rules)
- `/root/AAA/reports/network-concepts-f13-mapping-audit-v2-2026-09-24.md` (Identity/Relationship/Authority distinction)

---

## 6. Writer Authority

```yaml
writer:
  agent_id: FI-003 (anonymous session)
  actor_verified: false
  authority_band: OBSERVE_ONLY
  f13_standing: NONE
  role: external_advisory_draft_author

doctrine_alignment:
  - "Registry tanpa heartbeat = buku alamat, bukan jagaan" (R4 doctrine)
  - "Witnessing ≠ Claiming" (per syed-arif-poc-witnessing-affection)
  - "Identity ≠ Registry ID" (per identity-continuity.md + F10 ONTOLOGY)
  - "Audit Error ≠ Governance Success" (per audit-error-not-governance-success)

audit_correction:
  wrong_address_failure: Hermes claimed lanes/people.yaml has 8 persons; actual is 0
  correction_classification: WITNESS (data verified), NOT GOVERNANCE
  per: wrong-address-state-fails-silently + audit-error-not-governance-success

canonical_standing: NONE (awaits F13 seal via sovereign_chat_override)
promotion_path: requires_verified_arif_session
```

---

DITEMPA BUKAN DIBERI — One-page heartbeat map, falsifiable per row. 13 persons from R4 (heartbeat) reconciled with persons.yaml (F13 SOT, 3 constitutional persons) + lanes/people.yaml (0 persons — Hermes audit correction) + identity_cards (1 biometric pilot). 5 receipts captured. Awaiting F13 seal.

`#HUMAN-HEARTBEAT-MAP-DRAFT-2026-09-24`
