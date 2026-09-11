# DOCKET — EUREKA::EVIDENCE_HORIZON (CANDIDATE, NOT RATIFIED)

> **Status:** `DOCKET_COLD` — drafted, awaiting F13 ratification. Per ARIF directive
> 2026-09-12 ~01:11 MYT: *"Catat draft candidate ni dalam working ledger, tapi jangan
> ratify lagi. Biaq dia settle cold. We ratify when the baseline numbers are clean."*
> **Format:** HELIX (mandatory per Wawa binding 2026-09-12) — STRAND_A pattern
> narrative + STRAND_B evidence citations. Without helix this is a claim, not a law.
> **Proposed by:** Arif (F13), from adversarial review of the reality-claim-gate audit.
> **Prior-art check:** RUN — this is the only one of five candidates that survived.
> **Do NOT ratify without reading §5 (what would falsify it).**

---

## STRAND_A — Pattern narrative

A governance organ can only judge the reality it is permitted to observe. Where the
observation surface is bounded — truncated, filtered, sampled, scoped — the organ
rules on a **fraction** of the facts while believing it rules on all of them.

This is a different failure from detection-without-enforcement. Enforcement absence
means the verdict cannot act. **Evidence horizon** means the verdict itself is formed
on incomplete input, and no amount of enforcement authority fixes that. Give the
organ full veto power and it will confidently veto on partial evidence.

Therefore: **governance quality cannot exceed its evidence horizon.**

Operational corollary — the one that changed code tonight: when an organ knows its
own view is truncated, it must **downgrade the severity of its verdict**, not merely
record a caveat. A gate that cannot see the whole artifact has no standing to
refuse. It has standing to warn.

## STRAND_B — Evidence citations

| # | Evidence | Handle |
|---|---|---|
| B1 | `run_turn.py` truncates the hook payload: `"response": (response or "")[:500]` | `/usr/local/lib/hermes-agent/gateway/run_turn.py` **L1476** |
| B2 | Gate therefore never sees chars >500 of any turn — handle evidence there is operationally nonexistent | same file, `_hmwa_post_turn_hooks` L1473-1478 |
| B3 | Coded consequence: `TRUNCATED_PAYLOAD → WARN not BLOCK` — "never BLOCK on evidence we were not allowed to see" | `/root/.hermes/hooks/reality-claim-gate/handler.py` sha256 `ee6330c183692fee1a825729cb423fafca02b855f62ff910c38fbc94bbd81ddf` |
| B4 | Test proving the downgrade fires | `/root/.hermes/hooks/reality-claim-gate/test_phase15.py` sha256 `e821b821bae760d1aed161484fb1b835e3209588cf5388fa0d1bff86cf148a32` — "Truncated payload => WARN not BLOCK" PASS, 14/14 suite |
| B5 | **Tier 1 instance, same night:** three valid measurements of one store (213 / 353 / 351) — each true at its timestamp, each stale on arrival, because the observation window did not include concurrent sibling mutation | `/root/AAA/reports/skill-store-census-2026-09-12.md` + `.json` sha256 `5d0f82d40cc757b184ae073d09c1b6f0ed7fc561dc40b80db14427b08abc2e27` |
| B6 | **My own third artifact, same night:** census v1 keyed by `basename(realpath(dir))`, collapsing 12 distinct skills → reported 339. The method was the horizon. | `/root/AAA/scripts/skill_store_census.py` v1→v2 correction, documented in report §3 |
| B7 | Prior-art grep: term absent from all doctrine surfaces | `grep -rliE 'evidence horizon\|observation window\|evidence_horizon'` over `/root/AAA/instructions/`, `/root/AAA/canon/`, `/root/AAA/governance/`, `/root/.hermes/skills` → **empty** |
| B8 | Prior-art grep: built/loaded/active/effective ladder absent too | `grep -rn -iE 'built.*loaded.*active'` over `/root/AAA/canon/`, `/root/AAA/instructions/` → **empty** |

### Relationship to existing canon (what is NEW vs what is RE-DERIVED)

| Candidate from tonight | Ruling | Prior art |
|---|---|---|
| Detection ≠ Enforcement | **PRIOR ART** (18 days) | `/root/AAA/instructions/gate-promotion.md`, forged 2026-08-25, titled *"Detection Is Debt Until It Can Say NO"*; tiers `OBSERVE_ONLY`/`ANNOUNCE`/`GATE` already defined |
| Hook Paradox (capability on disk ≠ in runtime) | **PRIOR ART** (4 days) | `/root/AAA/canon/EUREKA-ACTIVATION-INERTIA-2026-09-08.md` §1 core law; Kitaran #2 is the same shape (metadata edited in `server.py`, port served by `server.js`) |
| Authority Surface Theory | **DERIVATIVE** of #1/#2 | sharper wording, same mechanism |
| `G = Detection × Authority × Enforcement` | **PRIOR ART shape** | APEX v36Ω `G = (A·P·E·X)^(1/4)`, multiplicative veto: zero in any factor collapses G |
| **Evidence Horizon** | **NEW — survives** | B7 empty |
| built/loaded/active/effective | **AMENDMENT candidate** to ACTIVATION_INERTIA (2 states → 4) | B8 empty |

### The finding that outranked all five

Auditing my own build against `gate-promotion.md`, I found I had **violated canon I
shipped an hour earlier**: the doctrine mandates every observation organ declare
`OBSERVE_ONLY | ANNOUNCE | GATE`. I declared nothing — the limitation lived in a
prose description string no loader reads as a contract.

Fixed, with handles:

    HOOK.yaml L2  enforcement_tier: OBSERVE_ONLY
    sha256        28a5d5b882246dce42827c876b7e45c04d5f2c6150f21ef04a676025346b3be0
    yaml parses   clean; tier reads back; events intact
    tests re-run  14/14 PASS after the edit
    marker        RCG-TIER-OBSERVE_ONLY-DECLARED · chain_hash 7fb65abd1209…

**Doctrine existed. Doctrine was not consulted at the decision point.** Structurally
identical to a hook that exists but is never consulted at delivery — and to the
2026-09-09 curator archiving 37 skills *"tanpa sesiapa tahu."* Third instance of the
same class. This is the strongest support for EVIDENCE_HORIZON: the canon was inside
the search horizon and outside the decision horizon.

---

## 5. Falsification — what would kill it

Per Wawa's binding: a prediction is the real test, not tonight's synthesis.

1. **If a gate with a complete view still rules wrongly** for reasons unrelated to
   observation bounds, the horizon is not the binding constraint.
2. **If truncation is raised from 500 → full response and BLOCK behaviour becomes
   safe** without any other change, that confirms the horizon was load-bearing.
   *This is testable the moment Option A is authorized* — and is a reason to run it
   before, not after, delivery-path enforcement.
3. **If the next 100 scars do not distribute into** Reality Dominance / Structure
   Beats Instruction / External Correction, the meta-eureka framing fails.
   Prediction recorded by Wawa 2026-09-12; testable against
   `/root/.hermes/governance/wisdom_scar_ledger.jsonl` (currently 50 entries).

## 6. Not done, deliberately

- **Not ratified.** No canon file written under `/root/AAA/canon/`. Naming creates
  obligation (`naming-doctrine.md`) and ratification is F13.
- **Not appended to** `/root/AAA/canon/eureka-entries.jsonl` (69 entries) — that is
  the ratified registry, and this is `DOCKET_COLD`.
- **Not sealed.** No `arif_seal`, no `SEALED_EVENTS.jsonl` write (kernel-owned;
  1337 lines, mtime still Sep 11 23:56, plaintext-line count 0).

## 7. Ratification precondition

Per Arif: *"We ratify when the baseline numbers are clean."* Baseline is **not**
clean — 174 untracked `SKILL.md` in `/root/.hermes/skills`, HEAD tracks 162 while
351 exist on disk, and 12 sessions mutate one store with no locking discipline.
Those are Tier 1 open loops §7.1–7.4. Docket stays cold until they close.

DITEMPA BUKAN DIBERI ⚒️
