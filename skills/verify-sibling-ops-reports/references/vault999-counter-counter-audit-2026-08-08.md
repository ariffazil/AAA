# VAULT999 Chain Verification — Round 2: When Sibling Pushes Back (2026-08-08)

**Origin:** After the first counter-audit (`vault999-chain-verification-2026-08-08.md`) downgraded the sibling's "43 null chain_hash" claim, the sibling returned with a **revised count (46, later independently verified as 47) AND a different failure mode** ("missing key, not null value"). The revised claim turned out to be **load-bearing TRUE**, but the bigger finding was different: the canonical verifier was never wired into Makefile.

**Lesson:** A wrong number can hide a right finding. Always re-verify the *failure mode*, not just the count.

---

## What Happened

| Turn | Sibling claim | Auditor verification | Verdict |
|---|---|---|---|
| 1 | "43 entries with null chain_hash" | Live: 38,937 missing, 0 null-valued, 0 JUDGE_SEAT_DEPUTY matches | Sibling fabricated the count + event-type — rejected as T3 → T2 |
| 2 | "46 JUDGE_SEAT_DEPUTY entries lack chain_hash KEY (not value); canonical verifier at `verify_vault_chain.py:288` is unwired from Makefile" | Live: 47/47 entries with `[channel, decision, deputy_seat, event, primary_seat, reason, registry_path, role]` and no `chain_hash` field | **Confirmed load-bearing** — T1 constitutional finding |

The sibling was **wrong about the number** in turn 1 (43 was pulled out of thin air) but **right about the structural concern** in turn 2. The auditor was **right to push back** but should not have **closed the door** on the underlying claim.

---

## The Failure-Mode Distinction (Critical)

| Sibling says | Auditor must check | If true |
|---|---|---|
| "N entries have `chain_hash: null`" | grep for entries where the **key exists but value is null** | Recent post-Jun-29 entries with bad write |
| "N entries are missing `chain_hash`" | grep for entries where the **key is absent entirely** | Pre-chain-format legacy entries OR new format that failed to write |
| "N entries have wrong schema (e.g. timestamp vs ts)" | grep for entries where `timestamp` exists but `ts` doesn't, on the same event-type the sibling names | Real schema-drift bug in writer code |

**Test command pattern:**

```bash
# Distinguish "null value" vs "missing key"
total=$(wc -l < /root/arifOS/VAULT999/outcomes.jsonl)
key_present=$(grep -c '"chain_hash"' /root/arifOS/VAULT999/outcomes.jsonl)
key_null=$(grep -c '"chain_hash":\s*null' /root/arifOS/VAULT999/outcomes.jsonl)
key_missing=$(( total - key_present + key_null ))  # entries without chain_hash key

echo "total=$total key_present=$key_present key_null=$key_null key_missing=$key_missing"
```

If sibling cites a specific event-type (e.g. `JUDGE_SEAT_DEPUTY_ACTIVATED`), run:

```bash
grep -c '<EXACT_EVENT_TYPE_STRING>' /root/arifOS/VAULT999/outcomes.jsonl
# If 0 → event type does not exist. Sibling scanned wrong file or hallucinated.
# If > 0 → sample 3-5 lines and verify the actual schema
```

---

## The Bigger Finding: Canonical Verifier Unwired

The sibling's most actionable claim was not the count, but this:

> "Make target vault999-verify returned 'Nothing to be done for vault999-verify' — the canonical chain verifier is unwired from the build. The script exists but is not invoked by make. So 'chain healthy' was never actually measured by the canonical verifier."

**Verification (live):**

```bash
# Canonical verifier exists and has the right check
grep "Missing chain_hash is a structural break" /root/arifOS/scripts/verify_vault_chain.py
# Line 288: "# Missing chain_hash is a structural break — not synthesizable."

# But Makefile wires the wrong script
grep "vault999-verify" /root/arifOS/Makefile /root/Makefile
# /root/arifOS/Makefile:182: vault999_status.py
# /root/Makefile:23: vault999-verify → $(MAKE) -C $(AAA_DIR) vault999-verify
```

**Why this matters:** if `make vault999-verify` returns "healthy" but uses `vault999_status.py` (parseable + append-only check), and `verify_vault_chain.py` (canonical hash-chain link check) is the source of truth — then **every prior "chain healthy" assertion is unfalsifiable**. The federation has been running with a fake-green status indicator.

**Pattern for the federation operator:** any sibling claim about a "missing/broken/unwired" piece of federation plumbing is **higher-signal than a count**. Plumbing claims tell you what the system *can't* tell you about itself.

---

## How to Do a Counter-Counter-Audit (3 steps)

When a sibling pushes back after your first counter-audit:

1. **Strip the count, keep the structural claim.** If the sibling said "46 entries" and you found 47, that's noise. If the sibling said "the entries have no `chain_hash` field at all" and you verified the field is absent, **that's load-bearing**. Concede the count delta; hold the structural claim.

2. **Re-scan the failure mode from scratch.** Don't reuse your first probe script — siblings often correct the *mechanism*, not just the count. Re-derive the relevant subset of the vault and verify the sibling's NEW framing.

3. **Look for the bigger finding.** A wrong-count sibling often has a right-plumbing concern lurking. Check what they cited about *infrastructure* (scripts, Makefiles, registries) before the numbers.

---

## Counter-Counter-Audit Decision Tree

```
Sibling returns with revised claim
        ↓
Does the revised claim cite a DIFFERENT failure mode? (null value → missing key)
        ↓
   YES → re-probe for the new failure mode, ignore the old count
   NO  → sibling is just adjusting a number; verify the number, hold original verdict
        ↓
Did the sibling cite any plumbing / infrastructure / unwired-script concern?
        ↓
   YES → investigate the plumbing claim FIRST; it's usually higher signal
   NO  → stay on the count
```

---

## Live Output (2026-08-08T05:30Z)

```python
# Re-scan with corrected failure mode ("missing chain_hash KEY, not null value")
{
  "total_entries": 42153,
  "chain_hash_present": 2758,         # 6.5%
  "chain_hash_absent_key": 39005,    # 92.5% pre-chain-format legacy
  "chain_hash_null_value": 0,        # never written as null
  "JUDGE_SEAT_DEPUTY_ACTIVATED": 47, # sibling said 46, live says 47
  "all_47_have_no_chain_hash_field": True,  # confirmed load-bearing
  "first_chain_hash_line": 24878,    # June 29, 2026
  "canonical_verifier_unwired": True # Makefile uses vault999_status.py
}
```

**Final verdict after round 2:**

- T1 constitutional finding: **47 JUDGE_SEAT_DEPUTY entries lack `chain_hash` field** — confirmed, load-bearing for F11/F2.
- T1 operational finding: **canonical verifier unwired** — confirmed, all prior "chain healthy" claims unfalsifiable.
- The 39,005 noise entries: schema migration debt, T2/T3, not constitutional.

**Action recommendation:**
1. (T1, immediate) Wire `verify_vault_chain.py` into Makefile — one-line change. This makes chain health *actually measurable*.
2. (T2, F1-reversible) Re-seal the 47 JUDGE_SEAT_DEPUTY entries with retro-linked `chain_hash`. Audit-logged.
3. (T3, deferred) Schema migration for the 39,005 legacy entries. Segregate test/telemetry from real-seal before sweeping.

---

## What This Session Proved About the Audit Loop

1. **Sibling fabrications don't stay fabricated.** When a sibling's number is wrong but their concern is real, they'll return with corrected evidence. Treat round-1 rejection as **opening the door**, not closing it.

2. **Counter-counter-audits find plumbing.** The first audit caught a count. The second caught an unwired verifier. Each round, the signal gets *higher-tier* — counts → structural → infrastructural.

3. **The "wrong number" framing wastes time on the wrong thing.** If the structural concern is real, the count is irrelevant. Lead with: "is the structural claim TRUE?" before "is the number RIGHT?"

4. **Federation plumbing bugs are load-bearing.** A wrong count is mostly a calibration issue. An unwired verifier means the system has been lying about its own integrity. Always investigate plumbing claims to the source.
