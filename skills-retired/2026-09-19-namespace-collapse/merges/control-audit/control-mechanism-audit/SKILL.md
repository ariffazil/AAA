---
name: control-mechanism-audit
description: "Use when a named control may not actually enforce."
owner: Hermes
---

# Control Mechanism Audit

> **A representation may never claim to be reality.** The same law applied to controls:
> **a name may never claim a mechanism it does not have.**

## Why this skill exists

An agent trusts a **name** faster than it reads a **mechanism**. `reality_gate`, `health_check`,
`sandbox`, `SEAL`, `drift`, `SHADOW` all read as guarantees. A guarantee-shaped artifact that
enforces nothing is **worse than no control at all**: absence is visible, a false control is
trusted — and it gets *built on* by the next lane.

This is a propagating defect, not a local bug. It crosses hosts, organs, and sessions, because
every layer re-uses the vocabulary without re-checking the mechanism.

## The law

**NAME_REQUIRES_MECHANISM.** Any surface whose name asserts gate / health / sandbox / verify /
seal / drift / secure / shadow / authority / wall must exhibit a runtime mechanism, or it is a
**false name** and the honest label is a different one.

### Reformulate the question before auditing

| Instead of | Ask |
|---|---|
| "Is there a security gate?" | "Can an action reach the protected state **without** passing through it?" |
| "Is there a health check?" | "If a dependency dies, does the output **change**?" |
| "Is there a sandbox?" | "Can a test payload **escape** the containment it claims?" |
| "Is it sealed?" | "Does the seal still **resolve** against the bytes on disk?" |
| "Is it safe?" | "What **physically prevents** the unsafe act — not what discourages it?" |

If the answer is "it is the default", "it is documented", or "it is named that way", there is
no mechanism.

## The three proofs (every control needs all three)

| Proof | Question | Fails when |
|---|---|---|
| **CALLER_PROOF** | Who actually invokes it in the running system? | zero callers → a decoy artifact |
| **EFFECT_PROOF** | Does a failing input change the output or block the action? | can never reject → a sorter, not a gate |
| **BYPASS_PROOF** | Can any alternate path reach the protected state unmediated? | one unguarded path → no security property |

`EFFECTIVE_CONTROL = CALLER ∧ EFFECT ∧ BYPASS` — if any term is empty, the authority claim is VOID.

A control that **never interferes with anyone** is not a control. Interference is the cheapest
positive evidence you will ever get: a gate that blocked your own read command has proven it sits
in the causal path.

## Procedure

1. **Inventory the names.** Collect every surface asserting control in the scope under audit.
2. **CALLER_PROOF — grep every scheduler and dispatch surface, not just one.**
   A capability can be invoked by cron, systemd, crontab, `/etc/cron.d`, a shell wrapper, an HTTP
   route, or another module. Grep them all; a single-surface grep manufactures false dormancy.
   ```bash
   for s in <cron-store>.json /etc/cron.d /etc/systemd/system; do grep -rl "<artifact>" "$s"; done
   grep -rln "<artifact>" --include=*.py --include=*.sh --include=*.service <repo-roots>
   ```
   Zero hits across **all** surfaces = the artifact is DORMANT. Confirm your pattern could have
   matched before trusting the zero (see *False absence*, below).
3. **EFFECT_PROOF — inject a failing input and observe.** Disable the dependency, feed malformed
   data, or attempt the bypass. If the output does not change, the control is decorative.
   A control with no reachable failing state cannot be a control.
4. **BYPASS_PROOF — enumerate alternate paths.** Every mutation path to the protected state must
   pass the check. One shell-level or editor-level path that skips it voids the property entirely.
5. **Decide: rename or repair.** Prefer **rename before fix** (see below).
6. **Record the verdict with its proof**, or mark it `UNPROVEN` — never `PASS` by absence of
   violation. "Nothing violated it yet" is not enforcement.

## Failure shapes (name → the mechanism defect)

- **Decoy control** — the artifact exists and is correct, and nothing calls it.
  *Fix:* wire it, or label it dormant. Do not leave it named like a live gate.
- **Constant metric** — a field that reports a fixed value (`rejections: 0`, `privacy: ok`) because
  it is computed from a **flag** or a literal, never from observed events.
  *Fix:* derive the metric from the thing it describes, or report `NOT_MEASURED`.
  A permanently-zero counter is a claim of safety with no measurement behind it.
- **Label overrides measurement** — the control branches on a *label* while the *fact* in the same
  payload contradicts it. Two fields, same object, opposite meanings.
  *Fix:* branch on the measured fact; treat a label as a hint, never as the decision input.
- **Default mistaken for a wall** — a safe-by-default setting (an env var, a config default) is
  described as a boundary. Anyone able to write config can open it.
  *Fix:* call it `delivery_default = off`, not a wall. A default is a posture; a boundary is a mechanism.
- **Import without use** — the containment/enforcement module is imported and never invoked on the
  execution path.
  *Fix:* trace the actual call path; grep the file for the imported symbol.
- **Stale seal** — a seal/receipt attests a hash that no longer matches disk, because a later writer
  touched the file after sealing.
  *Fix:* see `references/seal-and-delivery-verification.md`. Reconcile with a `supersedes` record —
  never rewrite the sealed history.
- **Configured mistaken for delivered** — a job's `deliver`/`target` field is quoted as proof the
  right party received something.
  *Fix:* read the delivery ledger for a `SENT` event plus a real message id.

## Rename before fix (honest naming IS a control)

The fastest way to kill a false-name family is to make the name true **before** repairing the code:

- A banner that only prints status is a `status_banner`, not a `health_check`.
- A lane that can send if someone edits config is `delivery_default = off`, not `cannot send`.
- A file with zero callers gets a header banner stating it is DORMANT and naming the real path.

Do this even when you cannot fix the code: a truthful name stops the **next** agent from inheriting
the false premise. A misleading artifact name is an unattended trap.

## False absence — proving CALLER_PROOF = 0 honestly

A null result is evidence of absence **only if the query could have returned a hit.**

A pattern can be structurally incapable of matching: searching a store by its visible title
(`-name "Title*"`) when the store renames every artifact to a generated prefix (`doc_<hash>_Title`).
The empty result carries **zero information**, and reporting it as absence fabricates a finding.

**Run a control search first** — the same query shape, aimed at something you know exists:

```bash
find <root> -iname "*known_good_fragment*"   # control: must HIT
find /      -iname "*target*suffix*"        # only then trust a null here
```

- **Anchor on a substring, never a position.** Use `-iname "*token*"` over `-name "Token*"`
  whenever a prefix, hash, or date may be added.
- One control call is cheaper than one retraction.
- If you cannot construct a control that hits, you have not earned the null: report `UNPROVEN`.

## Reporting the verdict

Label each control with the state actually reached — never a boolean:

```
ENFORCED        caller + effect + bypass all proven
UNPROVEN        a proof could not be constructed — not a pass
DORMANT         correct artifact, zero callers
DECORATIVE      reachable but cannot reject
FALSE_NAME      the name asserts a mechanism that does not exist
```

A boundary reported `PASS` because no artifact violated it — when no artifact ever *reached* it —
is the exact false assurance this skill exists to prevent. **Distinguish `UNBUILT` from `PASS`.**

## Seal the pattern, not each bug

Bugs of this family are one defect wearing many names. Fixing them one at a time guarantees the
next one. The durable artefact is the invariant plus an executable check per boundary, where every
check can **REJECT** — a checker that cannot fail is itself a false control.

See `references/seal-and-delivery-verification.md` for the concrete hashes, ledgers, and
per-boundary check recipes.
