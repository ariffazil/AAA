---
name: federation-substrate-hardening
description: |
  Pick up the matching recipe from /root/AAA/instructions/SUBSTRATE-PATCHES-v2.1.md for any of the nine substrate-defect classes surfaced by the 2026-10-11 Opus federation reality test. Use BEFORE proposing a code change to arifOS, A-FORGE, AAA, WEALTH, or HERMES, when the change targets verdict labels, sovereign-receipt parsing, floor honesty, claim-tense axis, vault signature-method labelling, side-effect-on-read, numeric contradiction detection, public-surface label reservation, or README freshness binding. Does NOT issue mutations — returns the recipe; the engineering agent applies.
triggers:
  - "harden arifOS MCP"
  - "patch arif_judge verdict"
  - "sovereign_receipt demote"
  - "fix floor-list hallucination"
  - "claim-class tense fix"
  - "vault method label fix"
  - "WEALTH read writes a receipt"
  - "HERMES finds 0 numeric contradictions"
  - "/999 SEAL overstatement"
  - "README says 0 broken lines"
  - "A-FORGE health SEAL string"
---

# Skill — federation-substrate-hardening (v1.0)

> **Read FIRST:** `/root/AAA/instructions/federation-reality-test-execution-prompt-v2.1.md` §B (the nine defect contracts).
> **Recipes:** `/root/AAA/instructions/SUBSTRATE-PATCHES-v2.1.md` (one patch per defect class).
> **Authority:** Does NOT mutate. Musyawarah before applying.
> **Constitutional floors:** F1 AMANAH · F2 TRUTH · F4 CLARITY · F7 HUMILITY · F9 ANTI-HANTU · F11 AUDIT · F13 SOVEREIGN.

## When to invoke

| Symptom in a federation reality test | Patch to load |
|---|---|
| Free-text `sovereign_receipt` triggers stage SEAL | PATCH 1 (B.1) |
| Floor list reports `L*:true` while the measurement is null | PATCH 2 (B.2) |
| Forecast claim accepted with `claim_class:"OBSERVED"` | PATCH 3 (B.3) |
| `vault_entry.method` says `ed25519_verified` on an HMAC | PATCH 4 (B.4) |
| A `wealth://*` resource read appends a vault row | PATCH 5 (B.5) |
| `hermes_contradiction_scan` returns `[]` on known numeric conflicts | PATCH 6 (B.6) |
| `/999` header is `SEAL` while gaps are non-zero | PATCH 7 (B.7) |
| Public README/999 VAULT999 status is stale | PATCH 8 (B.8) |
| `forge_health_check` returns `status:"SEAL"` | PATCH 9 (B.9) |
| Discovery returns verbs the connector then refuses | PATCH 10 (advertised-but-uncallable) |
| Cross-organ ACT rejected by a sibling organ | PATCH 11 (cross-organ inheritance) |

## How to invoke

1. Read v2.1 §B to see the contract per defect.
2. Read `SUBSTRATE-PATCHES-v2.1.md` to see the contract schema, retest signature, and owner-organ.
3. Produce a proposed diff (one patch per PR).
4. Carry the diff back to the owning organ (`@arifos/arifos`, `@aaa/cockpit`, `@aforge/api`, `@wealth/organ`, `@hermes/mcp`) through a musyawarah session.
5. Retest signature is part of the recipe; the PR description must include before/after of the replay against the Opus 2026-10-11 00:41Z run's MCP trace.

## What this skill never does

- It does not apply patches. Musyawarah does. This skill informs musyawarah.
- It does not invent new defects. The nine are real, traced, and named.
- It does not silently re-use the labels it cleans up. See v2.1 §A.2.

## Stamp

```
STAMP: ARIFOS::SKILL::federation-substrate-hardening::v1.0 :: 2026-10-11T01:00:00Z
```
