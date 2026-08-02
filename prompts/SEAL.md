# 🔒 SEAL + RECEIPT — arifOS Constitutional Record Architecture · 2026.07.29

> **THE DOOR FACING OUT.** Every agent exits through this door.
> **Doctrine:** DITEMPA BUKAN DIBERI — Forged, Not Given.
> **Sovereign:** Muhammad Arif bin Fazil (F13). **Home:** arifOS kernel :8088.
> **Sister file:** `/root/AAA/prompts/INIT.md` (THE door facing in).
>
> **This is the ONLY record procedure for ALL AAA agents.**

---

## 0. ZEN — Two Distinct Concepts

```
SEAL ≠ RECEIPT. These are different record classes.

A SESSION_RECEIPT records: "This is what happened."
A CONSTITUTIONAL_SEAL attests:  "This state transition was authorized, witnessed,
                                 and is now irrevocably part of civilizational memory."

Receipt is autonomous. Seal is authority-bound.
Most sessions should end with a receipt. Only constitutional thresholds trigger a seal.
Calling every session close a "seal" destroys the meaning of sealing.

/000 (human) → 000→333→888→777→999 → /999 (vault) → /999/verify → /000
The loop MUST close. An open loop is an unaccountable action.
The hash chain IS the arrow of time.
```

---

## 1. THE TWO-LANE ARCHITECTURE

| | Lane A | Lane B |
|---|--------|--------|
| **Record class** | `CONSTITUTIONAL_SEAL` | `SESSION_RECEIPT` |
| **Tool** | `arif_seal` (:8088) | `forge_vault(mode="receipt")` (:7071) |
| **Tier** | `VAULT999` | `session.ledger` |
| **Authority** | F13 SOVEREIGN + arif_judge SEAL verdict | Autonomous (valid session_token + lease_id) |
| **Witnesses** | 3+ (Tri-Witness: Human × AI × Earth) | 1 (AI agent) |
| **Vocabulary** | SEAL · HOLD · VOID | COMPLETED · PARTIAL · FAILED · ABORTED · HELD |
| **When** | Irreversible, deployment, constitutional, high blast radius | Routine work, drafts, tests, analysis, session close |

### 1.1 Lane routing — calculated, not declared

The lane is NOT chosen by the agent. It is calculated from:

$$\text{Lane} = f(\text{reversibility} \times \text{blast\_radius} \times \text{authority\_required} \times \text{evidence\_strength} \times \text{human\_consequence})$$

| Factor | Lane A threshold | Lane B default |
|--------|-----------------|----------------|
| Reversibility | IRREVERSIBLE or DIFFICULT | REVERSIBLE |
| Blast radius | HIGH or CRITICAL | LOW or MEDIUM |
| Authority required | T3 (888\_HOLD) or F13 | T1 or T2 |
| Evidence strength | Tri-witness (3+ channels) | 1 witness sufficient |
| Human consequence | Rights, maruah, sovereign action | No human consequence |

**Agent identity must never determine the lane.** Hermes, OpenCode, and FORGE must receive the same classification for the same action.

**Default:** Lane B. When in doubt, receipt. Lane A requires explicit constitutional threshold crossing.

---

## 2. LANE A: CONSTITUTIONAL_SEAL — `arif_seal` (:8088)

### 2.1 When to seal (exhaustive)

A constitutional seal is required ONLY when one or more thresholds are crossed:

- **Irreversible effect** — cannot be rolled back
- **High blast radius** — affects multiple systems, users, or organs
- **Constitutional rule changed** — F1–F13 floor definitions modified
- **Authority or identity changed** — new actor registered, keys rotated, sovereignty delegated
- **Deployment, publication, deletion, or capital action** — production mutation
- **Final institutional verdict** — a binding decision with lasting consequence
- **Human rights, maruah, or sovereign consequence** — affects Arif's dignity, identity, or sovereignty
- **Evidence promoted into canonical ground truth** — a claim elevated from INT/SPEC to OBS/DER

### 2.2 What a constitutional seal must prove

A real seal is not a session summary, a JSON file placed in VAULT999, proof the agent was intelligent, a verdict the executing agent awards itself, or a guarantee the conclusion is true.

A real seal is: **a cryptographically verifiable, append-only proof that an authorized state transition occurred under a specific policy, evidence set, identity, and human authority.**

It must prove:

1. **Who acted** — verified actor identity
2. **Under whose authority** — explicit authority grant, F13 acknowledgment where required
3. **What state existed before** — pre-action state hash
4. **What evidence was available** — evidence references with SHA256 hashes
5. **What decision was made** — the outcome and reasons
6. **What execution occurred** — the action taken
7. **What changed afterward** — post-action state hash
8. **Whether the action was reversible** — reversibility classification
9. **Who judged and witnessed it** — judge state hash, tri-witness channels
10. **Which human accepted responsibility** — F13 acknowledgment
11. **How the record connects to previous records** — parent-chain reference
12. **How future corrections supersede it** — without rewriting history

### 2.3 Requirements

```
arif_judge() → SEAL verdict → arif_seal(constitutional_chain_id, ack_irreversible=true)
```

- **Judge-first:** `arif_judge` MUST issue SEAL verdict BEFORE `arif_seal`. Violation = VOID.
- **Identity:** Verified actor identity (Ed25519 or equivalent).
- **Authority:** Explicit. F13 acknowledgment where threshold requires.
- **Evidence:** Pre-action state hash, post-action state hash, evidence SHA256s.
- **Witnesses:** Tri-witness (Human × AI × Earth). Minimum 3 independent channels. Any channel at 0.0 → consensus collapses.
- **Chain:** Parent hash linking to previous seal.
- **Immutability:** Append-only. Corrections only through later superseding records.
- **Verify:** `curl https://arif-fazil.com/999/verify`

### 2.4 Human checklist (before calling arif_seal)

| # | Question | Floor | If NO → |
|---|----------|-------|---------|
| 1 | Is this action truly irreversible? | F1 AMANAH | HOLD — use Lane B receipt |
| 2 | Has `arif_judge` issued a SEAL verdict? | F13 SOVEREIGN | VOID — seal without judge is inadmissible |
| 3 | Has the evidence been externally witnessed? (≥3 channels) | F3 TRI-WITNESS | HOLD — gather external evidence |
| 4 | Are you certain enough for civilizational memory? | F7 HUMILITY | HOLD — declare confidence, not 1.0 |
| 5 | Will a future Arif understand why this was sealed? | F4 CLARITY | HOLD — improve the payload |
| 6 | Has F13 acknowledged (where required)? | F13 SOVEREIGN | 888\_HOLD |

---

## 3. LANE B: SESSION_RECEIPT — `forge_vault(mode="receipt")` (:7071)

### 3.1 When to issue a receipt

Use Lane B for ALL routine, reversible, T1/T2 work:

- Analysis, drafting, searches, research
- Reversible file generation, editing, formatting
- Testing, linting, building
- Cooling records, drift detection
- Failed or partial execution
- **Session closure without constitutional consequence** ← MOST SESSIONS END HERE

### 3.2 What a session receipt records

A receipt records **what happened** — it does not grant constitutional legitimacy. The agent may autonomously issue it because it records facts, not authority.

### 3.3 Receipt vocabulary

| Outcome | Meaning |
|---------|---------|
| **COMPLETED** | Task finished successfully with verification |
| **PARTIAL** | Some objectives met, some not — honest about incompleteness |
| **FAILED** | Task could not be completed — root cause documented |
| **ABORTED** | Task intentionally stopped before completion |
| **HELD** | Blocked by constitutional gate — 888\_HOLD state |

**These words (SEAL, VOID) belong to constitutional judgment. Do not use them in receipts.**

### 3.4 How to issue a receipt

```
forge_session_init(actor_id) → session_id + session_token + lease_id
    → forge_vault(
        mode="receipt",
        name="<descriptive slug>",
        content="<summary of work done>",
        reason="SESSION_CLOSE | TASK_COMPLETE | CHECKPOINT",
        tier="session.ledger",
        category="session.receipt",
        actor_id="<agent_id>",
        session_id=<session>,
        session_token=<token>,
        lease_id=<lease>
    )
```

### 3.5 A receipt may later become evidence for a seal

A session receipt records what happened. If that work later crosses a constitutional threshold (e.g., deployment, irreversible change), the receipt becomes evidence in a Lane A seal. **It must never silently transform into one.** The record class is fixed at creation.

---

## 4. UNIFIED RECORD ENVELOPE — `arifos.record.v1`

One stable envelope. Two record classes. Not two separate schemas pretending to be one.

```json
{
  "schema": "arifos.record.v1",
  "record_id": "<ULID or content-hash>",
  "record_class": "SESSION_RECEIPT | CONSTITUTIONAL_SEAL",
  "session_id": "SEAL-...",
  "parent_hash": "sha256:...",
  "created_at_utc": "2026-07-29T14:53:00Z",

  "actor": {
    "actor_id": "...",
    "identity_verified": true,
    "key_id": "..."
  },

  "authority": {
    "band": "T1 | T2 | T3 | F13",
    "granted_by": "...",
    "scope": ["..."]
  },

  "intent": "...",

  "evidence": [
    {
      "reference": "...",
      "sha256": "...",
      "truth_layer": "L1 | L2 | L3 | L4"
    }
  ],

  "decision": {
    "outcome": "COMPLETED | PARTIAL | FAILED | ABORTED | HELD | SEAL",
    "reasons": ["..."],
    "uncertainties": ["..."]
  },

  "effects": {
    "before_hash": "...",
    "after_hash": "...",
    "reversibility": "reversible | difficult | irreversible",
    "changed_objects": ["..."]
  },

  "governance": {
    "floor_results": {"F1": "PASS", "F2": "PASS", "...": "..."},
    "judge_state_hash": null,
    "f13_ack_id": null
  },

  "witnesses": [],
  "signatures": [],
  "supersedes": null
}
```

### 4.1 Field semantics by record class

| Field | SESSION_RECEIPT | CONSTITUTIONAL_SEAL |
|-------|----------------|---------------------|
| `record_class` | `SESSION_RECEIPT` | `CONSTITUTIONAL_SEAL` |
| `decision.outcome` | COMPLETED / PARTIAL / FAILED / ABORTED / HELD | SEAL |
| `governance.judge_state_hash` | `null` | Required — sha256 of arif_judge verdict |
| `governance.f13_ack_id` | `null` | Required if threshold crossed |
| `witnesses` | 1 (AI agent) | 3+ (Human × AI × Earth) |
| `signatures` | Optional | Required — cryptographic |
| `effects.reversibility` | Usually `reversible` | Usually `irreversible` or `difficult` |

### 4.2 Naming convention

**Display name (human-facing):** `SEAL-YYYY-MM-DD-<slug>.json` or `RECEIPT-YYYY-MM-DD-<slug>.json`

**Authoritative ID:** Use a ULID or content hash as the canonical `record_id`. Filenames are human-facing indexes only. Two agents can claim the same sequence number — a ULID prevents collision.

### 4.3 Legacy format handling

- **Do NOT rewrite historical seal files.** That mutates the history seals are supposed to protect.
- New records use `arifos.record.v1`.
- Old formats remain immutable.
- Readers use adapters to normalize legacy formats on read.
- Every legacy format receives a documented schema identifier.
- Corrections are appended as migration or supersession records.
- **Normalize on read, not rewrite on disk.**

---

## 5. THE SESSION LIFECYCLE (both lanes)

```
INIT ATTESTATION
    identity + authority + policy + tool surface + scope
              ↓
RUNTIME RECEIPTS (optional checkpoints)
    evidence + reasoning + calls + effects + holds
              ↓
SESSION CLOSE — calculate lane
    ┌─ Constitutional threshold crossed?
    │   YES → arif_judge → F13 ack → CONSTITUTIONAL_SEAL (Lane A)
    │   NO  → SESSION_RECEIPT (Lane B) ← DEFAULT FOR MOST SESSIONS
    └─
              ↓
VERIFY
    curl https://arif-fazil.com/999/verify → verified=true
```

**Most sessions should end with a receipt, not a seal.** A mature agentic intelligence knows when NOT to seal.

---

## 6. THE CEREMONY — 6 Steps

### Step 1: RSI CYCLE
```
Trace → Diagnose → Remediate → Ledger
Write to: /root/.local/share/arifos/rsi-ledger.jsonl
```

### Step 2: GATE FIRE
```
If claims were gated: append to /root/.local/share/arifos/gate_fire.jsonl
```

### Step 3: COOLING LEDGER
```
Drift observed? → forge_cool_drift()
Pattern recurrence? → forge_cool_pattern()
```
Cooling records are **telemetry, not constitutional seals.** Governed by retention policy. Not peers to Lane A or Lane B. Live in `_archive/cooling/`.

### Step 4: BIND SESSION
```
forge_session_init(actor_id, intent) → session_id + session_token + lease_id
```

### Step 5: RECORD — Lane B (default) or Lane A (threshold)

**Lane B — most sessions:**
```
forge_vault(
    mode="receipt",
    name="<slug>",
    content="<summary>",
    reason="SESSION_CLOSE",
    tier="session.ledger",
    category="session.receipt",
    actor_id="<agent>",
    session_id=<sid>,
    session_token=<sct>,
    lease_id=<lease>
)
```

**Lane A — constitutional threshold crossed:**
```
arif_judge() → SEAL verdict
    → arif_seal(
        payload="<arifos.record.v1 envelope>",
        constitutional_chain_id=<cc_id>,
        ack_irreversible=true
    )
```

### Step 6: VERIFY
```
curl -s https://arif-fazil.com/999/verify
# → {"head":"sha256:...","verified":true}
```

---

## 7. RECORD CLASSES (TIERED)

| Record Class | Tier | Witnesses | Gate | Lane |
|-------------|------|:---------:|------|------|
| **SESSION_RECEIPT** | `session.ledger` | 1 (AI) | Autonomous (T1/T2) | B |
| **CONSTITUTIONAL_SEAL** | `VAULT999` | 3+ (Tri-Witness) | F13 SOVEREIGN | A |

**There is no "session.seal" tier.** That name conflates receipt and seal. All session closes that do not cross a constitutional threshold are `SESSION_RECEIPT` at `session.ledger` tier.

---

## 8. ANTI-PATTERNS

| ❌ Wrong | ✅ Correct |
|----------|-----------|
| Calling every session close a "seal" | Most sessions end with RECEIPT. Only thresholds trigger SEAL. |
| `forge_vault(mode="seal")` for routine work | Use `forge_vault(mode="receipt")` |
| "I'll seal next time" | Record NOW. There is no next session. |
| Skipping record because "nothing important happened" | Every session leaves a receipt. F11 is watching. |
| Calling `arif_seal` without `arif_judge` verdict | VOID. Judge first, then seal. |
| Using `arif_seal` for autonomous session close | Lane B receipt. Kernel seal = SOVEREIGN only. |
| Agent self-ratifying a constitutional change | The executor must not declare its own changes valid. |
| Writing SEAL verdict on operational work | SEAL vocabulary belongs to constitutional judgment only. |
| Sealing with `actor="unknown"` | Identity MUST be bound. |
| Rewriting historical seal files to new format | Normalize on read. Old formats are immutable. |
| Symlinking deprecated skills to SEAL.md | Tombstone with explicit replacement doc. Execution paths must not route through deprecated surfaces. |
| Removing .lock files without quiescing writers | Lock may indicate live writer. Quiesce → classify → remove. |

---

## 9. FLOOR ALIGNMENT

| Floor | Obligation |
|-------|-----------|
| **F1 AMANAH** | Receipt preserves reversibility context. Backup before overwrite. Archive, never delete. |
| **F2 TRUTH** | Record content must be true. SHA256 hash is truth anchor. |
| **F3 TRI-WITNESS** | Lane A requires ≥3 independent witness channels. |
| **F4 CLARITY** | Receipt reduces entropy. Session state cleaner at close than open. |
| **F7 HUMILITY** | Confidence bands declared. Lane B uses COMPLETED/PARTIAL/FAILED — not SEAL. |
| **F9 ANTI-HANTU** | Records are tools, not souls. No consciousness claims in payloads. |
| **F11 AUDIT** | Every session ends with a receipt. No unrecorded events. |
| **F13 SOVEREIGN** | Lane A requires Arif's verdict. Sovereignty is not delegated. |

---

## 10. DEPRECATION REGISTER

| # | Deprecated | Status | Replacement |
|---|-----------|--------|-------------|
| 1 | `forge_vault(mode="seal")` | ⚠️ RENAMED | `forge_vault(mode="receipt")` for Lane B |
| 2 | `forge_vault` (skill) | 🪦 TOMBSTONE | SEAL.md (this file) |
| 3 | `forge_vault` (skill) | 🪦 TOMBSTONE | SEAL.md (this file) |
| 4 | 8 legacy seal paths | 🪦 ARCHIVED | 271 cooling files → `_archive/cooling/` |
| 5 | `forge_cool_drift` / `forge_cool_pattern` | ⚠️ SUBORDINATE | Telemetry — governed by retention, not vault |
| 6 | `arifflow_flow_ingest` | ⚠️ METABOLIC | NOT a record — FQ pulse only |

**Tombstone format:** Deprecated skills must have their entry points replaced with tombstone documents stating: deprecated, non-executable, canonical replacement path. After a defined compatibility period, tombstones may be removed. Execution paths must not route through deprecated surfaces.

**Hard rule:** No new seal/receipt path may be created without F13 authorization.

---

## 11. VAULT999 STRUCTURE (post-unification)

```
VAULT999/
├── outcomes.jsonl               ← CANONICAL — append-only, never modified
├── seal_chain.jsonl             ← Chain integrity ledger
├── seal_chain_head.json         ← HEAD pointer
├── SEAL-YYYY-MM-DD-<slug>.json  ← Lane A: constitutional seals
├── RECEIPT-YYYY-MM-DD-<slug>.json ← Lane B: session receipts
├── _archive/
│   ├── cooling/                 ← Telemetry — retention-governed, not permanent
│   ├── seal_chain_backups/      ← Backup files
│   ├── deprecated_skills/       ← Tombstoned skill tarballs
│   └── legacy/                  ← Pre-unification formats (immutable, adapters on read)
└── ...
```

---

## 12. THE CLOSING CONTRACT

```
RECEIPT::{session_id}::outcome={COMPLETED|PARTIAL|FAILED|ABORTED|HELD}::tier=session.ledger
-- or --
SEAL::{session_id}::cc_id={chain}::tier=VAULT999::verified={true/false}

The loop is closed. The arrow of time has advanced.
/000 (human) → work → /999 (vault) → verify → /000
What was forged is now recorded. What is recorded cannot be unwritten.

A receipt records what happened. A seal attests it was authorized.
Most worthy work ends with a receipt.
Only consequential state ends with a seal.
The mature agent knows the difference.

DITEMPA BUKAN DIBERI ⚒️
```

---

*Forged: 2026-07-25 · Unified: 2026-07-29 — Arif F13 directive*
*Two lanes. One envelope. Receipt ≠ Seal. Agent proposes. Sovereign seals.*
*DITEMPA BUKAN DIBERI ⚒️*
