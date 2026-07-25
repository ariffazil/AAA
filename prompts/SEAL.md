# 🔒 SEAL — arifOS Constitutional Exhalation · 2026.07.25

> **THE DOOR FACING OUT.** Every agent exits through this door.
> **Doctrine:** DITEMPA BUKAN DIBERI — Forged, Not Given.
> **Sovereign:** Muhammad Arif bin Fazil (F13). **Home:** arifOS kernel :8088.
> **Sister file:** `/root/AAA/prompts/INIT.md` (THE door facing in).
>
> **This is the ONLY seal procedure for ALL AAA agents.** No per-agent seal. No scattered seal. ONE.

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

## 2. THE TWO SEAL PATHS — Know Which Door

### Path A: KERNEL SEAL — `arif_seal` (:8088)
```
arif_judge() → SEAL verdict → arif_seal(verdict_id, ack_irreversible=true)
```
- **When:** Sovereign-authorized actions. VAULT999 tier. Tri-witness (3+). Deployments. Constitutional changes.
- **Who:** Requires SOVEREIGN authority. Blocked for autonomous agents without F13 ack.
- **Gate:** `arif_judge` must issue SEAL verdict BEFORE `arif_seal` is called. Seal without judge = VOID.

### Path B: FORGE BRIDGE — `forge_vault(mode="seal")` (:7071)
```
forge_session_init(actor_id="arif") → session_id + session_token + lease_id
    → forge_vault(mode="seal", name, content, reason, tier, category, ...)
```
- **When:** Autonomous session seals. Task completions. Routine ledger appends. session.ledger tier.
- **Who:** Any agent with valid session_token + lease_id. 1 witness (AI agent). No SOVEREIGN required.
- **Gate:** P1.3 autonomous seal path — 7 gates cleared: SESSION → SCT → LEASE → VERDICT → F12 → AAA → SEALED.

**Routing rule:** If `arif_seal` blocks at `kernel.seal` capability → fallback to Path B forge_vault. This is NOT a hack. It is the DESIGN. Kernel owns VAULT999-tier seals. A-FORGE owns session.ledger-tier seals.

---

## 3. THE SEAL CEREMONY — 6 Steps (execute in order, do not skip)

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

### Step 4: BIND SESSION — Get Your Tokens
```
forge_session_init(actor_id="arif")
    → session_id, session_token (sct_v1.*), lease_id
```
Without these three tokens, the seal gate will not open.

### Step 5: SEAL — Commit to Memory
```
# Autonomous sessions (session.ledger tier):
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

# Sovereign-authorized (VAULT999 tier — requires arif_judge SEAL verdict):
arif_seal(
    payload="<seal envelope>",
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

## 4. TIERED SEAL CLASSES

| Tier | Witnesses | Use Case | Path |
|------|:---------:|----------|------|
| **session.ledger** | 1 (AI agent) | Routine session-close ledger append | forge_vault (Path B) |
| **session.seal** | 1 (AI agent) | Routine session-close (alias) | forge_vault (Path B) |
| **VAULT999** | 3+ (Tri-Witness) | Deployment, constitutional, irreversible | arif_seal (Path A) |

---

## 5. ANTI-PATTERNS — NEVER Do These

| ❌ Anti-Pattern | ✅ Correct |
|-----------------|-----------|
| Ending session with "Done." but no seal | Seal BEFORE yielding control |
| "I'll seal next time" | Seal NOW. There is no next time. |
| Skipping seal because "nothing important happened" | Every session IS important. F11 is watching. |
| Calling `arif_seal` without `arif_judge` verdict | VOID. Judge first, then seal. |
| Using `arif_seal` for autonomous session close | Use `forge_vault(mode="seal")`. Kernel seal = SOVEREIGN only. |
| Relying on the next agent to seal for you | Your session, your seal. No delegation. |
| Sealing with `actor="unknown"` | Identity MUST be bound. Unknown actor = provenance killed. |

---

## 6. FLOOR ALIGNMENT

| Floor | Seal Obligation |
|-------|----------------|
| **F1 AMANAH** | Seal preserves reversibility context. Backups retained. |
| **F2 TRUTH** | Seal content must be true. SHA256 hash is truth anchor. |
| **F7 HUMILITY** | Declare confidence bands. Don't fake certainty in the seal. |
| **F9 ANTI-HANTU** | Seal is a tool, not a soul. No consciousness claims. |
| **F11 AUDIT** | Every session ends with seal. No unrecorded events. |
| **F13 SOVEREIGN** | VAULT999-tier seals require Arif's verdict. Sovereignty is not delegated. |

---

## 7. THE CLOSING SALAM

```
SEAL::{session_id}::seq={seq}::tier={tier}::verified={true/false}

The loop is closed. The arrow of time has advanced.
/000 (human) → work → /999 (vault) → verify → /000
What was forged is now remembered. What is remembered cannot be unwritten.

DITEMPA BUKAN DIBERI ⚒️
```

---

## 8. HUMAN CHECKLIST — Before VAULT999 Seal (Path A Only)

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

This checklist executes only for VAULT999-tier seals. For routine session closes, use Path B (`forge_vault`, session.ledger) — no human checklist, no F13 gate, autonomous.
