---
name: control-integrity-audit
description: "Use when auditing whether a control really enforces."
version: 1.0.0
license: MIT
---

# Control Integrity Audit

> A control-like name requires a runtime causal mechanism. Where the mechanism is absent, the name is
> a claim about intent — and intent is not enforcement.

## When to use

Any time a control is claimed to be in force: a gate, validator, health check, sandbox, seal, drift
detector, shadow mode, authority check, privacy filter, or promotion ladder. Also load before
*repairing* anything described as a guard, and before trusting a label a guard produced.

## The one question

Not "does it exist?" and not "is it configured?". Ask:

> **Can an action reach the protected effect without passing through this control?**

If yes, it is not a boundary.

## The three proofs — all three required

| Proof | Question | How to obtain it |
|---|---|---|
| CALLER_PROOF | What actually invokes this? | Sweep every invocation surface (agent/cron job store, systemd units, `cron.d`, crontab, shell wrappers, loader imports). Name the call site with path:line. Zero callers = artifact, not boundary. |
| EFFECT_PROOF | Does a bad input change the outcome? | Feed it a deliberately failing input and observe a changed output or a blocked action. A control that cannot fail is a banner. |
| BYPASS_PROOF | Can the same effect be reached another way? | Enumerate alternate paths — another handler, raw shell, a direct DB or file write, a second producer for the same output. One unguarded path voids the control. |

Partial coverage is the normal case. Report **which** of the three are proven and which are not. Never
upgrade `PARTIAL` to `ENFORCED` because the code reads correctly.

## STOP RULE — check causal-path membership before auditing or repairing

Run CALLER_PROOF **first**. If nothing invokes the artifact:

- auditing it yields true findings with **no consequence**;
- "fixing" it leaves the delivered behaviour identical;
- the finding is real but the *impact* is zero.

Label it by what it is and stop: **DORMANT** (exists, correct in isolation, zero callers) or **DECOY**
(named like a control, called zero times). A repair outside the causal path is fix-shaped, not a fix.
Verify the sweep query can actually match — see the null-result rule in `agent-exploration-discipline`.

## Classification vocabulary

One state per control, stated explicitly:

| State | Meaning |
|---|---|
| DECLARED | Name/contract exists; runtime mechanism not proven |
| PARTIAL | Mechanism exists; coverage or bypass resistance unproven |
| ENFORCED | Causal path and measured effect demonstrated |
| VERIFIED | Enforced + bypass test + evidence lineage all pass |
| CONTRADICTED | Claim conflicts with observed runtime facts |
| UNBUILT | Nothing exists yet to check — honest, and **NOT** a pass |
| DORMANT | Exists, correct in isolation, zero callers |
| DECOY | Named like a control, called zero times |

**UNBUILT and DORMANT must never be reported as PASS.** A rule that holds only because nothing exists
to violate it is a vacancy, not a control. Vacancies are treacherous: several fail simultaneously on
the day the governed thing is finally built, and nothing was installed to catch it. Say plainly which
protections hold *by vacancy* rather than by strength.

## Evidence hierarchy — the dispute resolver

```
RAW OBSERVATION  >  MEASURED FACT  >  DERIVED STATE  >  REASON CODE  >  NARRATIVE LABEL
```

When two elements of one payload disagree, the higher tier wins. A derived state label must never
override a measured fact beside it, and a defaulted reason code is the weakest tier — it cannot justify
blocking anything. An inverted hierarchy is the same defect as a false name, expressed as an **ordering
violation** rather than a naming violation. Look for it wherever a specific-sounding reason is produced
by `value or "SOME_CAUSE"`: that string impersonates a diagnosis nobody measured.

## Attestation validity and sole-writer discipline

An attestation binds a digest to an instant. It is stale the moment anything writes the subject —
including your own follow-up edit and a parallel agent's.

- **Before attesting:** confirm you are the sole writer of every path in scope.
- **Before fanning work out to several agents:** partition by **disjoint file sets** and record one owner
  per path. Two writers on one path is a defect of the plan, not of the agents.
- **When a digest no longer matches:** check whether the attestation was correct when written and a
  second writer moved the target. Blame the second writer, not the seal.
- **Reconcile append-only:** `ORIGINAL CLAIM → COUNTEREVIDENCE → CORRECTION`, with the causal chain.
  Never rewrite a signed record to match current state — that destroys the audit trail it exists to be.
- Re-verify *all* digests in an attestation, not just the suspect one. A single mismatch does not mean
  the whole attestation is false.

## Reporting

1. Count controls by state; report **UNBUILT and DORMANT separately** from PASS.
2. Report the **false-assurance count** — controls that look enforced but are only DECLARED. A false name
   is worse than an absence, because absence is visible and a name is believed.
3. Name the **counterexamples too**. A control that records both success and failure with a verifiable
   identifier, an API that returns a refusal verdict on a missing required field, and a self-test that
   proves each of its checks can reject are all genuine enforcement. The accurate finding is usually
   **uneven control integrity**, not universal failure.
4. State one condition under which your audit would be wrong.

## Pitfalls

- **Auditing the name instead of the mechanism.** Finding the implementation correct proves the code is
  correct, not that anything runs it. CALLER_PROOF is not optional.
- **Treating configuration as enforcement.** A permissive-by-default setting is safe-by-accident, not
  safe-by-design; whoever can write the setting can open it. Default ≠ wall.
- **Repairing a dormant artifact and reporting impact.** The edit is real, the effect is nil. Say so.
- **Accepting a metric whose value is a constant or flag.** A rejection counter derived from config
  rather than from events will read as a working control forever.
- **Generalising to "everything here is fake".** That conclusion is itself a false claim, and it hides
  the genuinely working controls an operator needs to keep trusting.
- **Letting a guard fall back to the permissive branch.** "If every check fails, return the top-ranked
  item anyway" means the gate can reorder but never refuse. Verify the denial path exists.

## Support files

- `references/decoy-catalogue.md` — observed decoy shapes with the specific probe that exposes each.
