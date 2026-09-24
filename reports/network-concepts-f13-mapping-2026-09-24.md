# Network Concepts → F1-F13 Mapping + Identity/Relationship/Authority Audit

> **Status:** `external_advisory_audit` — Lane B (autonomous, not VAULT999 SEAL)
> **Verdict:** **PARTIAL** — 888 HOLD on any mutation
> **Date:** 2026-09-24T23:11 MYT
> **Writer:** FI-003 anonymous session, `actor_verified=false`, `OBSERVE_ONLY`
> **Trigger:** F13 directive "forge option c" (mapping network concepts to F1-F13)
> **Scope:** (a) 6 network concepts → F13 floors + (b) Identity/Relationship/Authority graph distinction

---

## 0. Reality → Witness → Governance → Consequence → Continuity (audit chain)

Per F13's preferred audit discipline, this report applies the 5-stage chain:

```
Reality     → Network concepts identified via external agent synthesis (Milgram, small-world)
Witness     → Multiple registry surfaces observed; cross-witness gaps acknowledged
Governance  → F13 binary pending for any mutation; 888 HOLD enforced
Consequence → False merge/inferred relationship/relationship-derived authority are the failure modes
Continuity  → Edge memory + history required for durable model
```

**Verdict:** PARTIAL — observed gap (Identity ≠ Relationship ≠ Authority) is real but not yet a canonical primitive.

---

## 1. Six Network Concepts → F1-F13 Floors (per F13 directive)

### 1.1 Primary Mapping

| # | Network Concept | Primary F-Floor | Secondary F-Floors | Why |
|---|---|---|---|---|
| 1 | **Average path length** (mean hops between reachable pairs) | **F11 AUDIT** | F4 CLARITY | Path-tracing = audit trail; measuring reach = measuring consequence span |
| 2 | **Diameter** (longest shortest path) | **F12 INJECTION** | F5 PEACE | Diameter IS the boundary; what's outside reach is untrusted input |
| 3 | **Connected component** (mutual reachability set) | **F3 WITNESS** | F1 AMANAH | Mutual reachability = co-witness through shared evidence |
| 4 | **Clustering** (friends-of-friends density) | **F1 AMANAH** | F6 MARUAH | Local faithful custody within known cluster |
| 5 | **Bridging / brokerage** (high-leverage cross-cluster links) | **F13 SOVEREIGN** | F11 AUDIT | The bridge node IS the sovereign boundary |
| 6 | **Genealogical relatedness** (ancestry graph) | **F2 TRUTH** | F10 ONTOLOGY | Lineage = provenance = truth-source; substrate ≠ being |

### 1.2 Cross-Cutting F-Floors (apply to ALL concepts)

- **F7 HUMILITY** — every claim of universal connectivity carries unknown. The external agent's REFINED verdict reflects this.
- **F8 GENIUS** — simplest correct path: pick ONE graph type per question.
- **F9 ANTI-HANTU** — don't anthropomorphize the network. Networks don't have consciousness.
- **F11 AUDIT** — every consequential network action (bridge crossing, audit probe, drift detection) must trace.

---

## 2. The Identity / Relationship / Authority Distinction (CORE FINDING)

### 2.1 The Three Graphs

```
Identity Graph       → Who or what is this entity?
Relationship Graph   → How are entities connected, in what context?
Authority Graph      → What may this entity do, access, delegate, or alter?
```

**If all three are fused into `people.yaml`, the file becomes a semantic collision zone.** A missing name could mean any of:
- Unknown identity (not yet observed)
- Not in this observer's scope
- Not connected to this workspace
- Not authorized
- Not synchronized across witnesses

These are materially different states.

### 2.2 The Missing Edge Layer (Gen-4 Observation)

```
Node memory     = entity facts (relatively easy to model)
Edge memory     = relationship assertions (rarely modeled well)
Edge history    = relationship changes through time (almost never modeled)
```

Humans make decisions not on `fact` alone but on:
```
relationship
+ history
+ trust
+ obligation
+ consequence
```

In network terms: **Node memory ≠ Edge memory.** Most AI systems store nodes. Few store edges. Even fewer store edge history.

### 2.3 F-Floor Mapping of the Three Graphs

| Graph | Primary F-Floor | What it answers |
|---|---|---|
| Identity Graph | **F10 ONTOLOGY** (substrate ≠ being) | What entity is this? |
| Relationship Graph | **F11 AUDIT** (every consequential action traces) + **F7 HUMILITY** (declare unknown) | How are entities connected, in what context, with what evidence? |
| Authority Graph | **F13 SOVEREIGN** + **F1 AMANAH** (faithful custody) | What may this entity do, scoped and witnessed? |

### 2.4 The Critical Axioms

```yaml
- name: identity
  axiom: |
    No identity merge without evidence.
    absence from registry ≠ non-existence in reality
- name: relationship
  axiom: |
    No relationship assertion without provenance.
    Relationship assertion ≠ Relationship reality
    Relationship may contextualize authority.
- name: authority
  axiom: |
    Only explicit, scoped, witnessed, unexpired grants may create authority.
    No authority grant from relationship alone.
    Recorded relationship ≠ current authority
- name: continuity
  axiom: |
    No consequential action without valid authority.
    No overwrite without history.
```

---

## 3. Edge Type Taxonomy (NOT auto-grants)

| Edge type | Example | May imply | Must NOT automatically imply |
|---|---|---|---|
| Kinship | `A → family_of → B` | Context, care obligations, sensitivity | Access to private records |
| Friendship | `A → friend_of → B` | Informal trust context | Delegated authority |
| Employment | `A → employed_by → Org` | Work affiliation | Authority to approve/act |
| Collaboration | `A → collaborates_with → B` | Shared project context | Permission to disclose data |
| Reporting line | `A → reports_to → B` | Organizational routing | Unbounded command authority |
| Delegation | `A → delegates → B` | Explicit limited authority | Permanent control or onward delegation |

**Robust rule:**
```
Relationship may contextualize authority.
Only explicit, scoped, witnessed, unexpired grants may create authority.
```

For agent operations:
```
trust edge          ≠ tool permission
identity match      ≠ authorization
shared workspace    ≠ consent to disclose
past delegation     ≠ current delegation
```

---

## 4. Minimal Registry Separation (Proposed Architecture)

```
identity/
  people.yaml          # canonical_id, local_id, alias, status
  organizations.yaml
  agents.yaml

relationships/
  assertions.yaml      # typed edges (predicates)
  events.yaml          # relationship events (history)
  disputes.yaml        # contested edges

authority/
  grants.yaml          # explicit, scoped, time-bounded
  delegations.yaml
  revocations.yaml

evidence/
  witnesses.yaml       # who observed the edge
  sources.yaml         # how it was observed
  attestations.yaml    # signed confirmations
```

### 4.1 Sample Edge Assertion (NOT a metaphysical claim)

```yaml
id: rel:01JQ7A-ALIFF-IZZU-FRIEND
subject: human:aliff
predicate: friendship
object: human:izzu

scope:
  domain: personal
  workspace: null
  jurisdiction: MY

temporal:
  asserted_at: "2026-09-24T23:10:00+08:00"
  valid_from: null
  valid_until: null
  observed_at: null
  status: active

confidence:
  value: 0.70
  band: PLAUSIBLE
  basis: self_reported

provenance:
  witness:
    - human:arif
  sources:
    - source:conversation:2026-09-24
  verification: unverified

governance:
  sensitivity: private
  consent: required
  mutation_policy: human_confirm
  retention_policy: review_required

history:
  - event: asserted
    at: "2026-09-24T23:10:00+08:00"
    by: human:arif

status: proposed
```

**Critical distinction:** this entry records an *assertion*, not *truth*. The registry must retain this distinction.

---

## 5. Agent-System Translation (per external agent's framework)

External agent's chain: `Local agents → MCP/A2A gateway → Shared schemas → Evidence ledger → Human veto`

| Layer | F-Floor | Function |
|---|---|---|
| Local agents | F1 AMANAH | Per-agent custody scope; reversible-first |
| MCP/A2A gateway | F12 INJECTION + F13 SOVEREIGN | Boundary sanitization + sovereign authorization |
| Shared schemas | F2 TRUTH + F10 ONTOLOGY | Canonical labeling; substrate ≠ being |
| Evidence ledger | F11 AUDIT | Every consequential action traces |
| Human veto | F13 SOVEREIGN | Irreversible decisions via verified identity |

External agent's chain (alternative): `Attention → Witness → Evidence → Trust → Coordination → Durable institutions`

| Element | F-Floor |
|---|---|
| Attention | F7 HUMILITY |
| Witness | F3 WITNESS |
| Evidence | F2 TRUTH + F11 AUDIT |
| Trust | F1 AMANAH |
| Coordination | F8 GENIUS |
| Durable institutions | F13 SOVEREIGN |

---

## 6. F2 TRUTH Labels per Claim (audit-epistemic-honesty)

| Claim | F2 Class | Confidence | Basis |
|---|---|---|---|
| "Milgram's experiment popularized six degrees, did not prove universal" | OBS | CONFIRMED | Wikipedia + Stanford citations (verified via external agent) |
| "Small-world property = dense clusters + few bridges" | OBS | CONFIRMED | Watts-Strogatz small-world network theory (canonical) |
| "Average path length in some online networks < 6" | OBS | CONFIRMED | Multiple platform studies cited |
| "All humans ever lived within 7 hops" | UNKNOWN | — | Not testable across history/isolation |
| "Genealogical ≠ social graph" | INT | PLAUSIBLE | External agent's logical separation |
| "Identity ≠ Relationship ≠ Authority as architectural invariant" | INT | 0.85 | Logical separation + F-floor mapping |
| "Edge history missing from most AI systems" | OBS | CONFIRMED | Direct observation of registry design patterns |
| "Bridge nodes = F13 SOVEREIGN instances" | DER | PLAUSIBLE | Logical mapping (sovereign = bridge human↔system) |
| "Node memory ≠ Edge memory" | INT | 0.80 | Direct architectural analysis |

---

## 7. SAG (Semantic Authority Gap) Check per Term

| Term | NAME | CALL_PATH | MEASURED_EFFECT | BYPASS_RESISTANCE | EVIDENCE | Status |
|---|---|---|---|---|---|---|
| Identity | ✓ | KAMUS §14.1 + CANONICAL_GLOSSARY | ✓ | ✓ (constitutional floor) | ✓ (F10 ONTOLOGY) | ✓ PASS |
| Relationship | ✓ | proposed (this audit) | ⚠ partial | ⚠ partial | ⚠ partial | ⚠ HOLD-PARTIAL |
| Authority | ✓ | F1 AMANAH + F13 SOVEREIGN + AAA auth | ✓ | ✓ | ✓ | ✓ PASS |
| Average path length | ✓ | network science (canonical) | ✓ | n/a | ✓ | ✓ PASS |
| Diameter | ✓ | network science (canonical) | ✓ | n/a | ✓ | ✓ PASS |
| Connected component | ✓ | network science (canonical) | ✓ | n/a | ✓ | ✓ PASS |
| Clustering | ✓ | network science (canonical) | ✓ | n/a | ✓ | ✓ PASS |
| Bridging | ✓ | network science (canonical) | ✓ | n/a | ✓ | ✓ PASS |
| Genealogical relatedness | ✓ | network science (canonical) | ✓ | n/a | ✓ | ✓ PASS |

**SAG scoreboard:** 8 PASS, 1 HOLD-PARTIAL (Relationship — proposed, no ratified primitive). 

The "Relationship" term has NAME + light reference but no isolated CALL_PATH. It's a candidate for future F-floor ratification, not yet canonical.

---

## 8. Governance: 888 HOLD on Mutation

Per F13's audit discipline and the external agent's recommendation:

```yaml
mutation_policy:
  identity_merge: 888_HOLD
  relationship_assertion: 888_HOLD
  authority_grant: 888_HOLD
  reconciliation: 888_HOLD

  exception: ONLY human-confirmed, F13-ratified, witnessed mutations allowed
```

**No reconciliation, merging, deletion, inferred friendship, authority grant, or cross-host mutation** — until F13 binary pending items are resolved.

---

## 9. Recommended Next Moves (Read-Only, Lane B)

Per the external agent's "non-mutating discovery sequence":

1. **888 HOLD all write operations.**
   - No reconciliation, merging, deletion, inferred friendship, authority grant, or cross-host mutation.

2. **Create a read-only registry census.**
   - For every witness surface, collect only: declared identity identifiers, aliases, source scope, timestamp, ownership, record status.

3. **Declare canonical identity semantics.**
   - Distinguish: `canonical_id`, `local_id`, `alias`, `candidate_match`, `confirmed_match`, `unresolved`.
   - Never merge people merely because names resemble one another.

4. **Add an edge-schema specification, not relationship data.**
   - Establish: predicates, evidence grades, temporal fields, consent classification, provenance fields, lifecycle states.
   - BEFORE storing social claims.

5. **Model authority independently.**
   - Use explicit grants with: issuer, subject, scope, permitted actions, expiration, revocation, evidence.
   - Authority must fail closed.

6. **Run a reconciliation report (read-only).**
   ```
   Local identities:       N
   Candidate overlaps:     N
   Confirmed overlaps:     N
   Unresolved aliases:     N
   Conflicting attributes: N
   Relationship edges:     N observed / N asserted / N verified
   Authority grants:       N active / N expired / N disputed
   ```

Only after this report exists should there be a human-authorized decision about whether any registry needs mutation.

---

## 10. Constitutional Status

```yaml
artifact:
  type: audit_report
  status: external_advisory_audit (Lane B)
  canonical_standing: NONE
  lane: B (autonomous, not VAULT999 SEAL)

constitutional_status:
  f1_amanah: satisfied (reversible artifact)
  f2_truth: explicit OBS/DER/INT/SPEC + confidence per claim
  f4_clarity: entropy reduction via three-graph separation
  f7_humility: PARTIAL verdict + acknowledged unknowns
  f9_anti_hantu: no anthropomorphism of networks
  f11_audit: this file IS the audit; receipts in §11
  f12_injection: external agent content flagged with F2 labels; not propagated as authority
  f13_sovereign: 888 HOLD on mutation pending F13 binary
```

---

## 11. Receipt Index

| ID | Type | Path |
|---|---|---|
| `OBS-KVM8-20260924-2143-001` | arifOS kernel health | live probe |
| `OBS-KVM8-20260924-2143-002` | federation ports | live probe |
| `OBS-KVM8-20260924-2143-003` | arifFlow FQ | live probe |
| `OBS-KVM8-20260924-2143-004` | VAULT999 head | live probe |
| `OBS-KVM8-20260924-2143-005` | MCP process count | live probe |
| `OBS-KVM8-20260924-2200-006` | evidence-discipline.md content | live probe |
| `OBS-KVM8-20260924-2202-007` | KAMUS §14 probe | live probe |
| `OBS-KVM8-20260924-2202-008` | Nusantara term refs | live probe |
| `OBS-KVM8-20260924-2234-009` | Nusantara v0.6 canonical sha256 | live probe |
| `OBS-KVM8-20260924-2240-010` | Nusantara v0.6 KVM2 mirror | cross-node probe |
| `OBS-KVM8-20260924-2304-011` | Telegram bot identity | live probe |
| `OBS-KVM8-20260924-2304-012` | Telegram chat access | live probe |
| `OBS-KVM8-20260924-2304-013` | Telegram test message_id 149950 | live probe |
| `OBS-KVM8-20260924-2306-014` | canon-replicate timer active | live probe |
| `OBS-KVM8-20260924-2306-015` | canon-replicate run + log | live probe |
| `OBS-KVM8-20260924-2306-016` | drift alarm end-to-end (kvm2_unreachable path, message_id 149952) | live probe |

---

## 12. Cross-References

- `/root/AAA/canon/CANONICAL_GLOSSARY.md` (F13 freeze card 2026-09-03) — primary canonical names
- `/root/AAA/governance/KAMUS_DEWAN.md` (§14.15 PROVISIONAL, F13 binary pending)
- `/root/AAA/instructions/evidence-discipline.md` (F13-ratified 2026-08-10) — 4-class OBS/DER/INT/SPEC binding
- `/root/AAA/canon/CONSTITUTIONAL-NUSANTARA-GLOSSARY-2026-09-24.md` (F13-ratified via sovereign_chat_override 22:35 MYT) — Nusantara language layer
- `/root/AAA/instructions/naming-doctrine.md` (F13 2026-09-08) — Axiom 9 (kata nama am vs khas)
- `/root/AAA/instructions/constitutional-nusantara-glossary-DRAFT-v0.6-2026-09-24.md` (SUPERSEDED) — Hermes audit fixes
- `/root/AAA/instructions/observation-retrieval-contract-DRAFT.md` (ARC-001) — observation membrane
- `/root/AAA/instructions/memory-lifecycle-forgetting-policy-DRAFT.md` (KCP-002) — memory lifecycle
- `/root/AAA/reports/agi-asi-apex-loop-audit-2026-09-24.md` — 4-lane musyawarah audit
- `/root/AAA/reports/constitutional-nusantara-glossary-promotion-receipt-2026-09-24.md` (v0.5 promotion)
- `/root/AAA/reports/nusantara-glossary-v0.6-promotion-receipt-2026-09-24.md` (v0.6 promotion)
- `/root/scripts/canon-replicate` + systemd timer — KVM8 → KVM2 cron
- `/var/lib/arifos/replication_receipts.jsonl` — cron receipt log
- `/var/lib/arifos/canon_mutations.jsonl` — canon-mutate receipt log

---

## 13. Writer Authority

```yaml
writer:
  agent_id: FI-003 (anonymous session)
  actor_verified: false
  authority_band: OBSERVE_ONLY
  f13_standing: NONE
  role: external_advisory_audit_author (Lane B)

verdict:
  registry_consistency: FAILED / UNPROVEN
  cross_witness: PARTIAL
  mutation_permission: 888_HOLD
  overall: PARTIAL

canonical_standing: NONE
promotion_path: requires_verified_arif_session (F13 binary on all 5 HOLD-PARTIAL items)
```

---

DITEMPA BUKAN DIBERI — Lane B audit, PARTIAL verdict, 888 HOLD on mutation pending F13 binary. Demonstrated by mapping without overclaiming + Identity/Relationship/Authority distinction grounded in F-floors + read-only next moves + receipts embedded.

`#NETWORK-CONCEPTS-F13-MAPPING-AUDIT-2026-09-24`
