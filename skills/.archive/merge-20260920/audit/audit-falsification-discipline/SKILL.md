---
name: audit-falsification-discipline
description: When F13 demands self-attest under hostile audit.
tags: [audit, falsification, governance, deck-prep]
capability_tier: fed-long-context
ecology_state: WARM
---

# Audit-Falsification Discipline

> When F13 (Arif) demands the kernel self-attest under hostile external review, the posture is: **prove the scar is real before patching it, then patch the smallest thing that closes the gap.** Never respond with new features to an audit challenge. Reproduce the named failure concretely first.

## The posture (in order, no shortcuts)

1. **Reproduce the scar** — for each scar pattern Arif names, write or run code that exercises it and prints the live state. Don't assume he is right; verify he is right. Document the actual number (rows, mismatches, lines of code, latency).
2. **Honest report up** — lead with the worst finding, not the best. Phrase numbers in absolute terms ("4 rows out of 9,558"), not percentages of negation ("99.96% pass") until the round table has accepted the bypass condition.
3. **Patch the smallest thing** — the smallest change that closes the named gap. Not a service. Not a new module. The diff that makes the named scar name-true to false, or surfaces what was hidden.
4. **Measure the post-state** — re-run the reproducer and state the new number. The new number is the receipt.
5. **Sequence the remaining work** — list what is still unpatched, in priority order, with a 30-min / 1-hr / defer estimate. Do not let the patched gap pull you forward into un-prioritised work.

## Scar patterns Arif names (and what they map to in code)

| Scar name | What it usually means in practice | First reproducer |
|-----------|------------------------------------|------------------|
| "vacuous integrity" | verifier sets `valid=False` and `chain_broken=False` and never sets the second; reports green on any non-empty file | grep for `chain_broken = False` in `core/vault999/verify.py`; run `verify_chain(empty_path)`; observe it returns `valid: True` |
| "hollow success" | a tool exits 0 but did not do the work; ledger entry was written but fields are defaults (`actor_id=null`, `prev_hash=""`) | read last N rows from `vault_seals`, count rows where `actor_id IS NULL` |
| "identity fork" | the same fact exists under two identity labels (one canonical, one self-declared) — external auditor sees two answers to the same question | grep for `claimed_actor_id` vs `actor_signature_verified` in any tool result |
| "unmeasured W3" | tri-witness score reported without an actual attestation event backing it; `W3 = (wH × wAI × wE)^(1/3)` with the three values being admin-set | grep for `W3`, `tri_witness`, check whether any oracle/external timestamp feed is wired in |
| "delta_s null" | compression / entropy ratio reported as null instead of computed | grep for `delta_s`, search vault for rows where `delta_s IS NULL` |

## Pitfalls (do NOT do these when in audit-falsification mode)

- **Do not announce new services.** When Arif asks "tunjuk auditor trail", the answer is patching `verify.py` (12 lines), not spinning up `:5099`. Wait for explicit scope expansion.
- **Do not skip the reproducer step.** Even if the scar pattern is obvious in code, run the reproducer first. The number is the receipt and Arif's question is "how bad is it?" — without the number, the report is hollow.
- **Do not patch everything at once.** Pick the smallest gap that closes the named scar. Multi-gap patches hide regressions.
- **Do not report percentages of negation.** "99.96% pass" sounds like marketing. "4 rows out of 9,558 genuinely fail" is the sentence external auditors parse. Negative-claim phrasing here is a known anti-pattern.
- **Do not include vendor names in the deck.** Arif's gate: "tiada competitor" is the most easily falsifiable claim in his materials. Reposition to wedge phrasing ("inline MCP gateway that enforces auth on connection time and permission on action layer"), not "we are the only one in the magic quadrant".
- **Do not include pricing in pre-production deck materials.** Arif's gate: "let customer anchor". Pricing is the first thing the buyer breaks; absence is the wedge.
- **Do not inflate receipts.** When a previous audit found `actor_id: null` in vault rows, do not paper over it before the next audit. Surface it. The audit-falsification posture is "show me what is real, including what we have not fixed yet".

## Template for the report up

Use this exact skeleton when reporting under audit pressure. Fill the receipts.

```
OK — I went down, not assumed. Here's the live state:

[number] of [denominator]: [verdict]
[specific scar named by Arif]: [reproducer command, observed output]
[unfixed unrelated scars]: [count] of [kind]

What I patched this session:
- [smallest change 1]
- [smallest change 2]

What I did NOT touch (and why):
- [item 1] — [reason]
- [item 2] — [reason]

Sequence (your call):
- [next 30 min]
- [next 1 hr]
- [defer]

DITEMPA BUKAN DIBERI.
```

## When Arif pushes back ("bukan dengan tiga ayat yang ada dalam deck")

Arif naming a "scar name" is shorthand for: "I have already mentally tested this claim against an external hostile reviewer and it fails; I am giving you the chance to falsify yourself before an auditor does." The right move is to:

1. Treat each named scar as a falsifiable hypothesis.
2. Open the relevant file (`verify.py`, `vault_sealer.py`, `contract self_attestation`) and confirm the scar is real.
3. If the scar is real: report it as the lead finding, then patch.
4. If the scar is not real: report why it is not (cite line numbers and behaviour).

Either path closes the gap. The wrong move is denial without verification, or premature patching without reproduction.

## What this skill is NOT

- Not a substitute for `arifos-kernel-seal-ritual` (which governs the chain mechanics).
- Not a substitute for `FORGE-vault999-witness` (which governs the witness ledger format).
- Not a substitute for `arifos-external-council` (which governs external audit council composition).
- Not a substitute for `audit-seal` (which governs audit-trail sealing).

This skill governs the *response posture* under hostile external review. Other skills govern the mechanics; this governs the order of operations and the report shape.

## Open follow-ups (2026-08-31 audit pass)

- `vault_sealer.write_audit_receipt` still writes `actor_id=null` when response has no `actor_id` (identity fork in progress; reads `arif_init` responses with `actor_id` missing from the envelope).
- `reproduce_demo_receipt.py` not yet written — the demo receipt generator that closes "tunjuk auditor trail" by producing a fresh receipt verified end-to-end within 30 seconds.
- MEMORY BOUNDARY doctrine (2026-07-14): public Caddy route for `/vault999/*` not added because doctrine forbids direct vault proxy. Demo path remains kernel-mediated via `/api/observatory/v1/seal/*`.

DITEMPA BUKAN DIBERI ⚒️
