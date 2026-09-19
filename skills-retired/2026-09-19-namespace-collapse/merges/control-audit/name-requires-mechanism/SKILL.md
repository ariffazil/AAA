---
name: name-requires-mechanism
description: Use when auditing whether a named control actually controls.
---

# NAME_REQUIRES_MECHANISM

**The law:** no control-like name may be trusted without runtime causal evidence.
A gate, health check, sandbox, seal, drift flag, verify step, privacy filter, or
SHADOW mode is a **hypothesis about the system**, not a fact about it. The name is
the claim; the mechanism is the evidence. They are different objects.

```
SEMANTIC AUTHORITY = NAME ∩ CALL_PATH ∩ MEASURED_EFFECT ∩ BYPASS_RESISTANCE ∩ EVIDENCE
any term empty  ->  AUTHORITY_CLAIM = VOID
```

## Why the failure hides

A missing mechanism is visible. A mechanism-shaped name is **believed**, so it
propagates: the next agent reads the name, assumes the control, and builds on top.
That is why this class outlives any single bug and why it must be killed by
doctrine, not by patch.

Agents trust names faster than they read mechanisms. Assume you are susceptible —
the authors of the doctrine that names this defect fell for it in their own text.

## The three proofs — demand all three

| Proof | Question that must be answerable |
|---|---|
| **CALLER** | Who actually invokes this? Name the call sites; zero callers = artifact, not boundary. |
| **EFFECT** | Does a failing/absent input change the output or block the action? |
| **BYPASS** | Can the same effect be reached without passing through it? |

Any proof you cannot produce is a FAIL, not a maybe. Report it as unproven.

## Ask the causal question, not the existence question

Replace every existence question with a bypass question — it is the only one
that discriminates:

- "Is there a gate?" -> **"Can this action happen without passing the gate?"**
- "Is there a health check?" -> **"If a dependency dies, does the output change?"**
- "Is there a sandbox?" -> **"Can a payload escape it?"**
- "Is sending off?" -> **"What mechanically prevents a send?"**

## Declaration is not enforcement — the recurring shapes

- **Gate as artifact** — a real, well-built checker with zero callers.
- **Default mistaken for wall** — an env default of `SHADOW`/`off` is
  safe-by-default, not an authority boundary. Anyone who writes the env opens it.
- **Label overriding fact** — a `state` or `reason_code` field driving a decision
  while the measured value in the same payload says otherwise. Check whether the
  reason is *computed* or *defaulted*: `reason_code or "SOMETHING"` is a default,
  not a measurement.
- **Imported but unused** — a module imported at the top and absent from the
  execution path. `grep` each imported symbol; if it appears only on the import
  line, the architecture was imported, not installed.
- **Hardcoded banner** — a health endpoint returning a literal `"healthy"`.
  Probes nothing; a banner.
- **Metric derived from a flag** — a counter computed from the very flag it is
  supposed to validate, so it can never disagree with it. Metrics must be derived
  from **artifacts**, never from declarations.

## Fix order: RENAME before you FIX

If a name over-claims, correct the **name** first.

- `forge_health_check` that only returns a literal -> `forge_status_banner`
- `SHADOW`-as-safety -> `delivery_default=off`
- an unreferenced module named "engine" -> mark `DORMANT — NOT IN PRODUCTION PATH`
  in the file header, with the real production path named

Naming honesty is a security control. A misnamed artifact keeps recruiting future
agents into the same false assumption; a renamed one stops the bleed.

## Fix must be IN the causal path

Before repairing a file, `grep` for its **scheduled callers**. On a federated
box, sweep all four surfaces: hermes cron jobs, systemd timers, `/etc/cron.d`,
root crontab.

> A fix outside the scheduled call path is **fix-shaped, not a fix**.

Editing a dormant file and reporting seven defects repaired is itself an instance
of the defect being audited: declaration without enforcement.

## Label states honestly — UNBUILT is a valid verdict

Use, and never collapse:

`PASS` (artifact exists and the check can reject) · `FAIL` (violated, evidence named)
· `UNBUILT` (nothing exists to test — not a pass) · `UNPROVEN` (cannot be tested now)
· `NEEDS WITNESS` (only a human can confirm).

A checker that has never rejected anything is untested. Prove the check **can**
fail by running it against a known-bad input before trusting a PASS from it.

## Receipts: correspondence, not existence

`receipt exists != the event happened`. A receipt is only valid if it causally
corresponds to what it attests. Re-derive the artifact hash and compare: a sealed
`sha256_after` matching **no state that ever existed on disk** attests a fiction.

Record corrections **append-only**: `ORIGINAL CLAIM -> COUNTEREVIDENCE ->
CORRECTION`. Never rewrite history to make it clean; the mismatch is the most
valuable part of the record.

## Reporting discipline

Do not force claims to `confirmed` to make a finding look strong. When some
instances are verified and others are class-level or site-dependent, say so per
instance and name the exact `file:line`. An audit that over-claims belongs to the
same defect class as the code it audits — including findings you produced
yourself, against yourself, recorded in the same receipt.
