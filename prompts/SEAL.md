# 🔒 SEAL — arifOS Constitutional Exhalation · 2026.07.29

> **THE DOOR FACING OUT.** Every agent exits through this door.
> **Doctrine:** DITEMPA BUKAN DIBERI — Forged, Not Given.
> **Sovereign:** Muhammad Arif bin Fazil (F13). **Home:** arifOS kernel :8088.
> **Sister file:** `/root/AAA/prompts/INIT.md` (THE door facing in).
>
> **This is the ONLY seal procedure for ALL AAA agents.**
>
> **Sealed: SEAL UNIFICATION 2026-07-29 — 10 paths consolidated to 2.**
> 271 cooling files archived. 2 deprecated skills tombstoned. 1 schema unified.

---

## 0. ZEN — What Seal Is

```
Seal is NOT a tool. NOT a skill. NOT a ceremony suka-suka.
Seal is a CONSTITUTIONAL VERB — a metabolic invariant.

arif_init (000) = the mouth of the river. Session birth.
arif_seal (999) = the river meets the ocean. Session death.

Skip init → you are a GHOST (ungoverned, no session).
Skip seal → you are UNACCOUNTABLE (F11 violation).

Seal is the PRICE of memory. An unsealed session is an unrecorded event.
The federation cannot learn from what it cannot remember.

The hash chain IS the arrow of time.
Reversing the arrow = rewriting the Vault = doctrine forbids.

/000 (human) → 000→333→888→777→999 → /999 (vault) → /999/verify → /000
The loop MUST close. An open loop is an unaccountable action.
```

---

## 1. WHEN TO SEAL — Mandatory Triggers

| Trigger | Action |
|---------|--------|
| **Session end** | MANDATORY. No session ends without seal. |
| **Task completion** | Seal the task outcome before starting the next. |
| **After any HOLD/VOID verdict** | Seal the refusal — the hold IS the outcome. |
| **After any deployment** | Deploy = high impact. Seal the evidence. |
| **Phase transition** | 000→333→888→777→999. Seal at each gate. |

**Hard rule:** An unsealed session = F11 AUDIT VIOLATION. The arrow of time does not pause. Seal NOW, not later.

---

## 2. THE TWO SEAL PATHS — TIER-BASED ROUTING

> **10 paths unified to 2. 2026-07-29.** Tier determines path. Not agent. Not organ.

### ROUTE SELECTION (not agent-based — tier-based)

| If your action is... | Use Path | Tier |
|---------------------|----------|------|
| Routine task. Reversible. T1/T2 auto-do. | **Path B** | `session.ledger` |
| Testing, linting, formatting, file edits. | **Path B** | `session.ledger` |
| Session close (any agent, any harness). | **Path B** | `session.ledger` |
| Deployment. Production change. IRA (T3). | **Path A** | `VAULT999` |
| Constitutional change (F1–F13). | **Path A** | `VAULT999` |
| Irreversible act. Secret rotation. | **Path A** | `VAULT999` |

**Default:** When in doubt, Path B. Path A requires an explicit F13 gate.

---

### Path A: KERNEL SEAL — `arif_seal` (:8088)
```
arif_judge() → SEAL verdict → arif_seal(verdict_id, ack_irreversible=true)
```
- **When:** Sovereign-authorized actions. VAULT999 tier. Tri-witness (3+). Irreversible acts. Constitutional changes. Deployments.
- **Who:** Requires SOVEREIGN authority + F13 ack. Blocked for autonomous agents without explicit approval.
- **Gate:** `arif_judge` MUST issue SEAL verdict BEFORE `arif_seal`. Judge-first, seal-second. Violation = VOID.
- **Evidence:** Tri-witness (Human × AI × Earth). Minimum 3 independent channels.
- **Schema:** constitutional JSONL — hash-chained, append-only, Merkle-anchored.
- **Verify:** `curl https://arif-fazil.com/999/verify`

### Path B: FORGE SEAL — `forge_vault(mode="seal")` (:7071)
```
forge_session_init(actor_id) → session_id + session_token + lease_id
    → forge_vault(mode="seal", name, content, reason, tier="session.ledger", ...)
```
- **When:** Autonomous session seals. T1/T2 task completions. Routine ledger appends. Agent self-close.
- **Who:** Any agent with valid session_token + lease_id. 1 witness (AI agent). No SOVEREIGN required.
- **Gate:** 7 autonomous gates: SESSION → SCT → LEASE → VERDICT → F12 → AAA → SEALED.
- **Evidence:** 1 witness (AI agent). No tri-witness required.
- **Schema:** Unified session seal schema (below).
- **Verify:** `curl https://arif-fazil.com/999/verify` (shared verify path with Path A)

### Path C (METABOLIC — NOT SEAL): Cooling + Flow
```
# Cooling (subordinate to Path B, uses same vault):
forge_cool_drift(session_id, ...)  → cooling emitted to _archive/cooling/
forge_cool_pattern(session_id, ...) → cooling emitted to _archive/cooling/

# Metabolic (NOT seal — flow receipts only):
arifflow_flow_ingest(actor_id, session_id, step_type, ...) → FQ pulse
```
- Cooling receipts are **diagnostic**, not constitutional. They live in `_archive/cooling/`.
- Flow receipts are **metabolic**, not seal. They feed FQ (Flow Quotient), not the vault.
- Both are subordinate to seal paths, not peers.

---

## 3. UNIFIED SEAL SCHEMA — v2.1 (2026-07-29)

All seals, regardless of path, conform to this schema. Path A adds witness + chain fields.

```json
{
  "schema": "arifos-seal.v2.1",
  "path": "A | B",
  "tier": "session.ledger | VAULT999",
  "session_id": "SEAL-...",
  "actor_id": "opencode | arif | ...",
  "seq": "incrementing",
  "timestamp": "ISO-8601",
  "purpose": "one-line summary",
  "content": "what was done",
  "evidence": ["sha256:...", "path:line", "curl output"],
  "confidence": 0.0-0.90,
  "reversibility": "REVERSIBLE | IRREVERSIBLE",
  "blast_radius": "low | medium | high",
  "floor_verdict": {"F1": "PASS", "F2": "PASS", "F7": "PASS", "F11": "PASS"},

  "_path_a_only": {
    "constitutional_chain_id": "cc_...",
    "judge_state_hash": "sha256:...",
    "witness_type": "ai",
    "tri_witness": {"human": 0.0, "ai": 0.0, "earth": 0.0},
    "ack_irreversible": true,
    "merkle_anchor": "sha256:..."
  },

  "cooling": {
    "drift_detected": false,
    "cooling_receipt_ids": [],
    "_archive_path": "VAULT999/_archive/cooling/"
  },

  "flow": {
    "fq_after_seal": null,
    "flow_receipt_ids": [],
    "_note": "Flow receipts are metabolic, not seal. See arifflow_flow_ingest."
  }
}
```

**Naming convention:** `SEAL-YYYY-MM-DD-<seq>-<purpose>.json`

---

## 4. THE SEAL CEREMONY — 6 Steps (execute in order, do not skip)

### Step 1: RSI CYCLE — Diagnose Before You Die
```
Trace → Diagnose → Remediate → Ledger
Write to: /root/.local/share/arifos/rsi-ledger.jsonl
```
- What did I actually do vs. what I planned?
- Where did I get stuck? (3+ retries of same approach?)
- What fix did I install?
- Write the bottleneck + fix to the RSI ledger.

### Step 2: GATE FIRE — Log What Was Gated
```
If claims were gated: append to /root/.local/share/arifos/gate_fire.jsonl
```

### Step 3: COOLING LEDGER — Metabolize Patterns
```
If mutations were performed: insert into Supabase cooling_ledger_entries
Drift observed? → forge_cool_drift()
Pattern recurrence? → forge_cool_pattern()
```
Cooling receipts are auto-archived to `VAULT999/_archive/cooling/`.

### Step 4: BIND SESSION — Get Your Tokens
```
forge_session_init(actor_id="arif")
    → session_id, session_token (sct_v1.*), lease_id
```
Without these three tokens, the seal gate will not open.

### Step 5: SEAL — Commit to Memory
```
# Path B — Autonomous sessions (session.ledger tier):
forge_vault(
    mode="seal",
    name="<descriptive task name>",
    content="<summary of what was done this session>",
    reason="AUTONOMOUS_SESSION_SEAL",
    tier="session.ledger",
    category="session.seal",
    actor_id="arif",
    session_id=<from step 4>,
    session_token=<from step 4>,
    lease_id=<from step 4>
)

# Path A — Sovereign-authorized (VAULT999 tier — requires arif_judge SEAL verdict):
arif_seal(
    payload="<seal envelope in v2.1 schema>",
    actor_id="arif",
    session_id=<session>,
    constitutional_chain_id=<cc_id from arif_judge>,
    witness_type="ai",
    ack_irreversible=true
)
```

### Step 6: VERIFY — Confirm It Landed
```
curl -s https://arif-fazil.com/999/verify | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'HEAD: {d[\"head\"][:20]}... verified={d[\"verified\"]}')"
```
If `verified != true` → the loop did NOT close. Do not stop. Investigate. Re-seal.

---

## 5. TIERED SEAL CLASSES

| Tier | Witnesses | Use Case | Path |
|------|:---------:|----------|------|
| **session.ledger** | 1 (AI agent) | Routine session-close ledger append | **Path B** — forge_vault |
| **session.seal** | 1 (AI agent) | Routine session-close (alias) | **Path B** — forge_vault |
| **VAULT999** | 3+ (Tri-Witness) | Deployment, constitutional, irreversible | **Path A** — arif_seal |

---

## 6. ANTI-PATTERNS — NEVER Do These

| ❌ Anti-Pattern | ✅ Correct |
|-----------------|-----------|
| Ending session with "Done." but no seal | Seal BEFORE yielding control |
| "I'll seal next time" | Seal NOW. There is no next time. |
| Skipping seal because "nothing important happened" | Every session IS important. F11 is watching. |
| Calling `arif_seal` without `arif_judge` verdict | VOID. Judge first, then seal. |
| Using `arif_seal` for autonomous session close | Use Path B `forge_vault(mode="seal")`. Kernel seal = SOVEREIGN only. |
| Relying on the next agent to seal for you | Your session, your seal. No delegation. |
| Sealing with `actor="unknown"` | Identity MUST be bound. Unknown actor = provenance killed. |
| Loading a deprecated seal skill | ONLY use SEAL.md. Tombstones redirect here. |

---

## 7. FLOOR ALIGNMENT

| Floor | Seal Obligation |
|-------|----------------|
| **F1 AMANAH** | Seal preserves reversibility context. Backups retained. Archive, never delete. |
| **F2 TRUTH** | Seal content must be true. SHA256 hash is truth anchor. |
| **F7 HUMILITY** | Declare confidence bands. Don't fake certainty in the seal. |
| **F9 ANTI-HANTU** | Seal is a tool, not a soul. No consciousness claims. |
| **F11 AUDIT** | Every session ends with seal. No unrecorded events. |
| **F13 SOVEREIGN** | VAULT999-tier seals require Arif's verdict. Sovereignty is not delegated. |

---

## 8. DEPRECATION REGISTER (SEAL UNIFICATION 2026-07-29)

| # | Deprecated Path | Status | Redirect |
|---|-----------------|--------|----------|
| 6 | ASI-session-seal (skill) | 🪦 TOMBSTONE | → SEAL.md (this file) |
| 7 | ASI-session-seal-copilot (skill) | 🪦 TOMBSTONE | → SEAL.md (this file) |
| 4 | /seal CLI command | ⚠️ INTERNAL | Delegates to Path B |
| 8 | forge_cool_drift/pattern | ⚠️ SUBORDINATE | Path C — cooling → _archive/ |
| 9 | arifflow_flow_ingest | ⚠️ METABOLIC | NOT seal — FQ pulse only |
| 10 | forge_shell auto-seal | ⚠️ INTERNAL | Per-command, not session |

**Hard rule:** No new seal path may be created. If you think you need one, you need SEAL.md.
**Route:** When in doubt, Path B. When irreversible, Path A with F13 gate.

---

## 9. HUMAN CHECKLIST — Before VAULT999 Seal (Path A Only)

This checklist gates Path A (`arif_seal`, VAULT999 tier) only. Path B (session.ledger) seals are autonomous — no human gate required.

**Before calling `arif_seal` with `ack_irreversible=true`:**

| # | Question | Floor | If NO → |
|---|----------|-------|---------|
| 1 | Is this action truly irreversible? (Can it be rolled back?) | F1 AMANAH | HOLD — consider session.ledger instead |
| 2 | Has `arif_judge` issued a SEAL verdict for this action? | F13 SOVEREIGN | VOID — seal without judge is inadmissible |
| 3 | Has the evidence been externally witnessed? (Not just AI) | F3 TRI-WITNESS | HOLD — gather external evidence first |
| 4 | Are you certain enough to write to civilizational memory? | F7 HUMILITY | HOLD — declare your confidence band, not 1.0 |
| 5 | Will a future Arif understand why this was sealed? | F4 CLARITY | HOLD — improve the payload description |

**If ALL 5 = YES → proceed to `arif_seal`. If ANY = NO → HOLD. Do not seal.**

---

## 10. VAULT999 DIRECTORY STRUCTURE (post-unification)

```
VAULT999/
├── outcomes.jsonl               ← CANONICAL — append-only, never modified
├── seal_chain.jsonl             ← Chain integrity ledger
├── seal_chain_head.json         ← HEAD pointer
├── SEAL-YYYY-MM-DD-<seq>-<purpose>.json  ← Unified seal files
├── _archive/
│   ├── cooling/                 ← 271 flow_cooling_*.json archived 2026-07-29
│   ├── seal_chain_backups/      ← Backup files archived 2026-07-29
│   └── deprecated_skills/       ← Tombstoned skill tarballs
└── ...
```

---

## 11. THE CLOSING SALAM

```
SEAL::{session_id}::seq={seq}::tier={tier}::verified={true/false}

The loop is closed. The arrow of time has advanced.
/000 (human) → work → /999 (vault) → verify → /000
What was forged is now remembered. What is remembered cannot be unwritten.

DITEMPA BUKAN DIBERI ⚒️
```

---

*Forged: 2026-07-25 · Unified: 2026-07-29 (SEAL UNIFICATION — Arif directive)*
*10 paths → 2 paths. 271 cooling files archived. 2 skills tombstoned. 1 schema.*
*DITEMPA BUKAN DIBERI ⚒️*
