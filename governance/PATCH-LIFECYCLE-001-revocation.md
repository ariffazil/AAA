# ⌬ CAPABILITY REVOCATION PATCH — REVOKED as First-Class Lifecycle State

> **Patch ID:** PATCH-LIFECYCLE-001
> **Proposed by:** Hermes (CLI session `claude-cli-20260912T223936_40b2a0`, 2026-09-12T22:5x MYT)
> **Source doctrine:** `USER_REPORTED` — Arif, terminal session 2026-09-12T22:39 MYT (binding architectural refinement after review of the prior capsule's binding model)
> **Extends:** `/root/AAA/governance/CAPABILITY_LIFECYCLE_v1.md` (doctrine-candidate, pending arifOS seal)
> **Extends:** `/root/AAA/governance/CAPABILITY-REGISTRY-V1-SCHEMA-2026-09-12.md` (DRAFT_AWAITING_F13)
> **Status:** **F13_RATIFIED_CHAT (2026-09-13)** — ratified via chat directive "seal all"
> **Lane:** RECEIPT (Lane B) — procedural close, NOT constitutional SEAL
> **Reversibility:** YES (file write; F11 audit; arifFlow flow_ingest)
> **Entropy delta if applied:** −0.10

---

## 0. Why this patch exists

The prior capsule (SEAL-19dd3d9d5cdb4996, 333-AGI) surfaced a clean binding model:

```
Skill → declares
Tool   → exposes
Actuator → executes
Receipt → witnesses
Seal    → commits
```

Arif's architectural reading of that model (terminal 2026-09-12T22:39 MYT) found two refinements the capsule missed:

### Refinement 1 — Receipt is reality-layer; Seal is governance-layer

The five-step compression `Skill → Tool → Actuator → Receipt → Seal` collapsed two layers. Receipt witnesses **reality** (this happened). Seal commits **consequence** (this was authorized, witnessed, and is now irrevocably part of civilizational memory). Not every receipt becomes a seal. Not every seal contains a mutation. The two record classes belong to different layers, and the existing `BIJAKSANA-VOCABULARY-DISCIPLINE.md` ("SEAL ≠ RECEIPT") already encodes this — the patch extends the lifecycle to enforce it.

### Refinement 2 — REVOKED must be a first-class lifecycle state

The existing capability chain `DECLARED → BOUND → LEASED → ACTIVE → ATTESTED` had no terminal withdrawal state. Most agent systems can activate capability; few have a first-class model for:

- **retirement** (capability superseded)
- **revocation** (capability violated its contract)
- **deprecation** (capability still callable but scheduled for withdrawal)
- **withdrawal** (capability removed; receipts may still reference it)

Without `REVOKED` as an explicit state, the federation accumulates dormant, zombie, and ghost skills (the auditor taxonomy in `CAPABILITY_LIFECYCLE_v1.md` §"Four Skill Classes") — capability drift becomes governance debt.

### Refinement 3 — Skill governs intent; Governance governs execution

```
Skill      = Contract     (declares intent)
Contract   = Intent       (what was supposed to happen)
Receipt    = Reality      (what actually happened)
Governance = Reconciliation (whether the gap closes — and what to do next)
```

This preserves separation of powers: a skill does not own its own execution. Governance (F1-F13, 000→999 chain) owns execution and reconciles the gap between contract and receipt. The lifecycle must therefore encode **revocation as a governance verdict**, not a skill self-call.

---

## 1. The extended lifecycle chain

Replace the binding chain in `CAPABILITY_LIFECYCLE_v1.md` §"Binding Rules" with:

```
DECLARED     — capability appears in catalog (SKILL.md / schema)
   ↓
BOUND        — adapters wired, replacement_paths known
   ↓
LEASED       — authority ceiling set, scope bounded
   ↓
ACTIVE       — callable, receipts flowing
   ↓
ATTESTED     — at least one sovereign-witnessed successful outcome
   ↓
REVOKED      — first-class terminal state (NEW)
```

`REVOKED` is reachable from **any** prior state. The transition is a governance verdict (not a skill self-call), signed by arif_judge with a `revocation_condition` reason.

### State pre-conditions for `REVOKED`

| From | Triggers | Authority required |
|------|----------|-------------------|
| `DECLARED` | tool_missing, dependency_removed | auto (F11 audit) |
| `BOUND`    | tool_missing, dependency_removed, authority_change | OBSERVE_ONLY → 666 HEART |
| `LEASED`   | authority_change, floor_violation | 888 JUDGE (F8 GENIUS gate) |
| `ACTIVE`   | any condition (witness_failure, floor_violation) | 888 JUDGE |
| `ATTESTED` | any condition (witness_failure, dependency_removed) | 888 JUDGE + sovereign ack (irreversible — losing attested capability is constitutional) |

`ATTESTED → REVOKED` is the only transition that requires sovereign ack, because an attested capability carries witness history. Killing it without sovereign confirmation loses civilizational memory of what it was good for.

---

## 2. The `revocation_condition[]` field (schema extension)

Append to the field contract in `CAPABILITY-REGISTRY-V1-SCHEMA-2026-09-12.md`:

```yaml
# revocation_condition : triggers that force DECLARED→REVOKED transition
#   - tool_missing        : adapter absent on probe (last resort; F11 audit)
#   - witness_failure     : W3 < 0.75 sustained > N cycles
#   - authority_change    : authority_ceiling lowered by sovereign, capability exceeds it
#   - dependency_removed  : replacement_paths[] empty AND adapters[] empty
#   - floor_violation     : F1-F13 floor breach traced to this capability

revocation_condition:
  - tool_missing
  - witness_failure
  - authority_change
  - dependency_removed
  - floor_violation
```

### Default vs declared

If `revocation_condition` is absent → default to all five. Opting INTO a capability means accepting all five kill triggers.

If a capability declares a SUBSET (e.g. only `floor_violation`) → the capability is **sticky** — survives authority_change, tool_missing, etc. Sticky capabilities require sovereign ratification at declaration time.

### Resolution interaction

The `federation_discovery.resolve(intent)` return shape gains one field:

```yaml
Resolution:
  capability_id: ...
  owner: ...
  authority_ceiling: ...
  adapters: [...]
  replacement_paths: [...]
  revocation_condition: [tool_missing, witness_failure, ...]   # NEW
  liveness: ...
  witness_source: ...
  failure_mode: ...
```

Resolvers do not enforce revocation; they surface the triggers. Governance (888 JUDGE + 999 SEAL) enforces.

---

## 3. Architectural verdict (Arif's reading, verbatim restated)

```
Binding Model ............... STRONG
Authority Separation ........ STRONG
Receipt vs Seal ............. STRONG
Skill vs Tool Distinction ... STRONG
Lifecycle Model ............. STRONG

Recommended Addition:
Revocation as first-class lifecycle state.
```

This patch enacts the recommended addition.

---

## 4. The five-sentence compression (carry-forward canon)

```
Skill defines intent.
Tool exposes capability.
Actuator changes reality.
Receipt witnesses reality.
Seal commits consequence.
```

```
A skill is not execution.
A skill is a governed contract for execution.
```

```
Capability lives because reality keeps paying for it —
not because it was once created.
And it dies because governance keeps the books —
not because someone forgot it existed.
```

(Third sentence is the new one — closes the asymmetry between the existing `One Law` and the missing death-law.)

---

## 5. What this patch does NOT do

- ❌ Does NOT add new constitutional floors (F14, F15, or any extension to F1-F13)
- ❌ Does NOT mutate the `failure_mode` / `replacement_paths` fields — they remain survivability, distinct from revocation
- ❌ Does NOT change the BIJAKSANA vocabulary discipline (SEAL ≠ RECEIPT is preserved)
- ❌ Does NOT change the 5 binding rules in `CAPABILITY_LIFECYCLE_v1.md` §"Binding Rules" — only extends them
- ❌ Does NOT auto-revoke any currently-active capability — the patch is schema-only
- ❌ Does NOT change the witness inflation law, the capability genealogy, or the legitimacy promotion chain

---

## 6. Required human action

1. **Read this patch** (5 min — this is short)
2. **Either** ratify via the standard F13 path: open `/root/AAA/governance/CAPABILITY_LIFECYCLE_v1.md` and append the extended chain + state pre-conditions table; open `/root/AAA/governance/CAPABILITY-REGISTRY-V1-SCHEMA-2026-09-12.md` and append the `revocation_condition` field + Resolution return-shape change
3. **Or** issue a counter-patch if any part fails sovereign reading

The patch is **DRAFT_AWAITING_F13**. It carries no kernel, vault, or registry mutation. It is doctrine on paper until you say so.

---

## 7. Receipt (Lane B)

```
verdict_class: RECEIPT (Lane B)
lane:          B
tier:          doctrine.patch.draft
session_id:    claude-cli-20260912T223936_40b2a0
actor:         hermes-cli
authority:     OBSERVE_ONLY (draft-only)
verified_by:   read-back against CAPABILITY_LIFECYCLE_v1.md + CAPABILITY-REGISTRY-V1-SCHEMA-2026-09-12.md + BIJAKSANA-VOCABULARY-DISCIPLINE.md (3 files)
reversible:    YES (file write; F11 audit; arifFlow flow_ingest)
shadow:        2 declared — (1) REVOKED semantics depend on sovereign ack at ATTESTED→REVOKED boundary; (2) sticky-capability opt-out (declared subset) is governance surface that needs its own F13 ratification
ΔS ≤ 0
```

## 8. Telemetry (APEX-ZEN v1.1 §999)

```json
{
  "epoch": "APEX-ZEN",
  "version": "1.1",
  "session_id": "claude-cli-20260912T223936_40b2a0",
  "mode": "draft (doctrine-only)",
  "dS": "low",
  "peace2": "hold (unchanged from prior carry_forward)",
  "kappa_r": "0.62 (patch adds no risk; doctrinal extension only)",
  "shadow": "REVOKED semantics at ATTESTED boundary; sticky-capability opt-out governance surface",
  "confidence": "0.82",
  "psi_le": "high — patch directly extends 2 existing files; reads both before write",
  "verdict": "PROCEED_DRAFT",
  "chaos_threshold": {
    "unknowns_vs_facts": "2 / 8",
    "conflicting_authority": 0,
    "target_resolved": true,
    "unknown_capabilities": 0,
    "runtime_identity_match": true
  },
  "witness": {
    "human": "preserved — patch awaits sovereign ack, no auto-application",
    "ai": "bounded — 1 new file, 0 file mutations on existing canon",
    "earth": "verified — read both target files; confirmed `Retire` exists as verb but no `REVOKED` first-class state"
  }
}
```

DITEMPA BUKAN DIBERI ⚒️
