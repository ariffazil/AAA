---
name: wisdom-reader
description: "Read substrate BEFORE claiming victory. Enforces witness-first doctrine. USE WHEN: 'audit', 'validate', 'verify this', 'is this real', 'what is the shadow', 'what's actually true', 'what's missing'."
---

# 📜 WISDOM-reader — Witness-First Audit Doctrine

> **Doctrine:** Witness before claim. Substrate before narrative.
> **Source:** /root/AAA/governance/BIJAKSANA-VOCABULARY-DISCIPLINE.md (PATCH-001)
> **Scar-bound:** SCAR-005 (doctrine archived out of substrate), SCAR-002 (49 sessions lost), SCAR-KERNEL-LEGACY-VERDICT-LEAK-002 (dual-truth rot)
> **Iron oath:** *"Lebih arif, lebih bijaksana, atau tidak sama sekali."*

## When to load

Load this skill BEFORE making any "we did it" / "all clean" / "SEAL" claim. Trigger phrases:

- "audit / validate / verify"
- "is this real / is this true / what is the shadow"
- "what's actually happening"
- "what's missing"
- "before we celebrate"
- After any session with multiple file mutations or constitutional claims

## Iron Rules (read these in order)

### Rule 1 — Read the substrate BEFORE any claim

Before declaring success / completion / SEAL, read in this order:

```

```
1. /root/.local/share/arifos/carry_forward.json — last session's open loops
2. /root/.local/share/arifos/carry_forward_backups/*.json — evolution trail
3. /root/.local/share/arifos/scars/SCAR-*.json — failure patterns (the substrate's memory of pain)
4. /root/.local/share/arifos/vault999/audit_chain.jsonl — recent verdicts
5. /root/.local/share/arifos/vault999/seal_chain.jsonl — constitutional chain (HEAD = truth)
6. /root/.local/share/arifos/vault999/seal_chain_head.json — current head with timestamp
7. /root/AAA/docs/deprecation-registry.json — tombstone inventory
8. arifOS /health + arifFlow /health — current metabolism
```

If you skip any of these, your claim is narrative, not audit.

### Rule 2 — Distinguish Lane A from Lane B before emitting verdict

| Word | Means | Required conditions |
|------|-------|---------------------|
| **SEAL** | Lane A constitutional | `judge_state_hash` present, sovereign witness > 0.5, `seal_chain.jsonl` gains new entry |
| **RECEIPT** | Lane B autonomous | `forge_vault(mode="receipt")` called, read-back verification passed |
| **SABAR** | Lane A honest sub-threshold | gap described in note, kernel-allowed (line 61) |
| **HOLD / VOID** | Gate failure | not a record — re-submit or drop |

**Forbidden:** `verdict=SEAL` without `judge_state_hash` and chain entry. This is precision rot.

### Rule 3 — Emit shadow BEFORE any positive claim

```
SHADOW (required structure):
- What is unverified?
- What is assumed vs proven?
- What is missing or stale? (e.g. chain head age, biometric age, FLAME state)
- What floors are PASS vs HOLD vs UNKNOWN?
```

If you cannot enumerate shadow, you have echoed, not audited.

### Rule 4 — Cross-check the constitutional chain, not just carry_forward

The carry_forward is **Lane B procedural residue**. It can claim "verdict=SEAL" without kernel verification. Only `seal_chain.jsonl` head timestamp is the constitutional truth.

If carry_forward says SEAL but chain head is unchanged, **the carry_forward is lying** (or Lane B). Surface this.

### Rule 5 — Verify the actor before trusting the verdict

arif_init returns `actor_verified: true` AND `actor_cryptographically_verified: true` AND yet `reason_code: TOKEN_INVALID`. This is the constitutional paradox of identity vs authority. **Identity is verified, authority is HOLD**.

Trust the kernel's `effective_verdict`, not the actor's `actor_verified` field.

### Rule 6 — Count the entropy, don't claim it

Use arifFlow `scalar_fq` (deprecated) AND `per_actor` (live) AND `diagnosis` (vector). The single scalar `fq` is heuristic. The vector diagnosis is the live reading.

If you must report entropy, cite all three. Never quote `fq` alone.

## Workflow (canonical)

```
INPUT: any claim of "success" / "SEAL" / "all clean"
  ↓
1. LOAD this skill
2. READ substrate (Rule 1)
3. DISTINGUISH verdict class (Rule 2)
4. ENUMERATE shadow (Rule 3)
5. CROSS-CHECK chain head vs carry_forward (Rule 4)
6. VERIFY actor's effective_verdict (Rule 5)
7. COUNT entropy with all 3 metrics (Rule 6)
  ↓
OUTPUT: audit with shadow + verdict-class + chain-truth
```

## Output shape (canonical)

```
Audit complete. N items verified.
Verdict class: [SEAL | RECEIPT | SABAR | HOLD]
Constitutional chain head age: [N days / fresh]

SHADOW (what was NOT verified):
- [bullet 1]
- [bullet 2]

Entropy:
  scalar_fq: [val] (deprecated, heuristic)
  diagnosis: [val] (vector, live)
  per_actor[333-AGI]: [val] (BALANCED | STUCK | FOSSILIZED)

Recommendation: [next safe action | sovereign unblock needed]
```

## Anti-patterns (forbidden)

- ❌ Echoing a celebration before reading carry_forward
- ❌ "All clean" without enumerating shadow
- ❌ "verdict=SEAL" for Lane B events
- ❌ Trusting scalar FQ without vector diagnosis
- ❌ Reading only `/health` and assuming substrate is healthy
- ❌ Treating `actor_verified=true` as `mutation_allowed=true`
- ❌ Closing a session with SEAL when HOLD was the truth

## NEW — 2026-09-18 (vault999 freshness probe)

**Before any verdict emission, probe `/root/.local/share/arifos/vault999/seal_chain_head.json`:**

```bash
HEAD=$(python3 -c "
import json, datetime
d = json.load(open('/root/.local/share/arifos/vault999/seal_chain_head.json'))
ts = d.get('timestamp') or d.get('last_seal_timestamp')
if ts:
    delta = (datetime.datetime.utcnow() - datetime.datetime.fromisoformat(ts.replace('Z',''))).total_seconds() / 3600
    print(f'{delta:.1f}h')
else:
    print('UNKNOWN')
")
echo "vault999 head age: $HEAD"
```

**Thresholds:**
- `< 24h` — fresh, normal
- `24-72h` — informational, log in SHADOW
- `> 72h` — P0 alert, constitutional heartbeat is silent

**Why:** Probe 2026-09-18T00:30Z detected 29.8h gap (informational, not yet P0). Probe 2026-09-18T06:38Z confirmed 57 entries intact (chain valid). Freshness != validity, both must be checked.

## NEW — 2026-09-20 (empty gauges that look measured)

Three instruments ship numbers that are not measurements. Probe the *producer*, not the label:

1. **W3** — arifFlow vector `w3=0.7439` with `status=MEASURED` is `∛(0.42 × 0.99 × 0.99)` from hardcoded witness defaults (`rest_routes.py`). `apex_primitives.py` honestly returns `None`. Session tokens may show a third value (0.6563 / 0.94). If channels are defaults: report **UNMEASURED**. Never HOLD on a fabricated W3. Evidence: `/root/AAA/reports/STAB-2026-09-16/W3-IS-A-CONSTANT.md`.
2. **CHRON calibration.json** — INIT reads the file, not `compute_calibration()`. A live join can be 1/1 while the file still says zeros. After any verification, `save_calibration(compute_calibration())`. `lessons.jsonl` empty is correct when `error_type=NONE` (a hit is calibration, not an error-lesson).
3. **arifFlow entity_classes.yaml** — loaded once at MCP process start. Live actor `hermes` ≠ listed `hermes-asi` → `UNKNOWN_ACTOR` even after yaml aliases. Disk parse ≠ live report until that MCP process recycles. Do not recycle shared MCP without checking attached sessions.

Also probe `/root/chron/data/calibration.json` vs `compute_calibration()` in the same turn before claiming "0 lessons / 0 verified".

## NEW — 2026-09-20 (attention preservation vs capture)

Candidate eureka, not constitution: `/root/AAA/eurekas/EUREKA-ATTENTION-PRESERVATION-ECONOMY-2026-09-20.md`.

Before any human-facing turn, one test: did this **preserve** his attention or **capture** it?

- Preserve: decide, close, HOLD silently, or stay quiet. Same clock, less of him.
- Capture: menus, re-asks of unanswered binaries, dumps that carry no decision. Same clock, more of him.

Do not re-ask a binary already on disk. The unanswered item stays HOLD.

Knowledge can be stored. Attention cannot. Verbose “help” that he must re-read is extraction, even when true.

## Reference scars (carry these)

- **SCAR-002-CEREMONY_FAILED_406** — 49 sessions failed because seal ceremony had a hard test gate. Tests are verify-phase, not seal-gate. Vocab rot.
- **SCAR-005** — A doctrine archived out of its declared SoT path is chat history, not constitutional memory. Substrate forgot what it forged.
- **SCAR-KERNEL-LEGACY-VERDICT-LEAK-002** — Truth told twice is truth fractured. One verdict field per response.
- **SCAR-AFORGE-SSE-HANDSHAKE-001** — Discovery handshake needs explicit handling.

## Iron Oath

> I will not claim victory before I have witnessed.
> I will not call RECEIPT a SEAL.
> I will not trust the carry_forward before the chain.
> I will not echo without shadow.
> **Lebih arif, lebih bijaksana, atau tidak sama sekali.**


## Lessons (auto)

*Auto-ingested from agent learning. F2-gated: every entry carries evidence.*
- **[2026-09-15] fi-003-qwen-code** (evidence: 555-auditor.md sections 1-2 (probes 22:30+08); CONVERGE.md B2): Counts without tree+method+timestamp are void (555 arbiter rule 2026-09-15): '328' vs '212' vs '374' skills were all real numbers from different trees (AAA vs .hermes) and methods (symlink-follow vs real-path). 19,122-token ad-tax and 78-duplicate-names were unreproducible — truth: 14,083-15.4K tokens, 0 duplicates (1 unnamed file; 'empty descriptions' were YAML block-scalar regex false-positives). '1,142 dirty' was the .hermes tree misattributed (AAA=126).
