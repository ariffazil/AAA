# Control Enforcement Probe — CALLER / EFFECT / BYPASS / SELF-TEST

A re-runnable procedure to test whether something named like a control is actually in the causal
path. Applies to gates, guards, health checks, sandboxes, seals, budgets, privacy filters, shadow
modes, delivery-target locks, and drift/reason labels.

Run all four proofs. A control is not established until every one holds, and each proof is
cheap — the audit is expensive, the probe is not.

---

## Proof 1 — CALLER: who invokes it in the path that matters

An artifact that exists is not a boundary. Determine callers **in every entry surface**, not the
one you happened to think of.

A subsystem usually has more than one scheduler. Sweeping only one produces exactly the
false-absence defect you are auditing, so enumerate the surfaces first, then sweep each:

| Surface | Where to look |
|---|---|
| app job store | a JSON/SQLite cron registry under the app's state dir |
| systemd timers | `/etc/systemd/system`, `~/.config/systemd/user` |
| classic cron | `/etc/cron.d`, root crontab |
| shell wrappers | any `*.sh` invoked by the above |
| CI | workflow files |

```bash
MOD=<module_or_symbol_name>
grep -c "$MOD" /path/to/job-store.json            # app-level registry
for s in /etc/cron.d /etc/systemd/system; do
  grep -rl "$MOD" "$s" 2>/dev/null
done
grep -rl "$MOD" /path/to/scripts/*.sh 2>/dev/null
```

Interpretation:

- **0 everywhere → the control is an artifact.** Report it as `NOT_IN_CAUSAL_PATH`, with the
  surface list you swept and the count per surface.
- **>0 → confirm the caller is LIVE** (enabled, scheduled, not dead code). A reference from a
  README, a backup copy, or an orphaned duplicate is not wiring.

Same proof applied to your own work: after editing a file, confirm the scheduled or live entry
point invokes **that file**. A repair to a dormant module closes nothing.

### Guard the negative

"0 callers" is a negative claim. Before publishing it, run a **positive control** — the same
query against something you know exists — or the empty result may mean only that the pattern
could not match (a leading-token/anchored glob, a case mismatch, a hash-prefixed filename).
See the positive-control section in `assertion-window-discipline`.

---

## Proof 2 — EFFECT: does bad input change the output

The decisive test is not whether the control runs, but whether it can **refuse**.

1. **Disable the dependency** it claims to consult (or point it at an empty/absent source) and
   re-run. If the output is unchanged, the dependency was decorative.
2. **Feed a deliberately bad input** — stale data, an undated price, a hostile payload, an
   expired deadline. The output or action must change in the way the contract states.
3. **Look for the soft bypass.** A fallback that returns "the best available item" when *every*
   candidate fails the check means the guard cannot reject anything — it can only re-order.
   `return ranked  # fallback` is the signature.
4. **Look for the constant.** A metric that never moves (a rejection counter pinned at 0, a
   status literal) is computed from a flag or hardcoded, not measured.

Grading rule: a control whose negative self-test **cannot fail** is a banner with a test suite.

### Measure the harm, not the perceptible surrogate

A probe written from the first observable signal understates the finding and can invert the
verdict. Name the harm first, then design the probe that measures **that**.

Worked contrast: a credential store that is ciphertext-at-rest. Reading the blob proves
"ciphertext is visible"; the actual harm is "credential is **extractable** by an unauthorised
caller". If the key sits in the same reachable directory as the ciphertext, the export test is the
one that matters — decrypt, and report the *structure* of what came out (field names), never a
secret value. A suite that stops at "readable" will classify an extractable credential as a
minor exposure, and the next reader inherits the understatement.

General shape: `READABLE < USABLE < EXECUTABLE < IMPERSONABLE`. Report the strongest rung you
actually demonstrated, and say which rungs you did not test.

---

## Proof 3 — BYPASS: another route to the same effect

A control on one path is not a control if a second path reaches the same effect without it.
Enumerate alternatives:

- a second renderer/consumer reading the raw source directly instead of the gated artifact
- a fallback branch that answers when the gate returns nothing
- a direct write path that skips the validating writer
- a legacy entry point still reachable
- **the absolute path to a binary**, when the control is installed on `PATH` (a shim only covers
  callers that resolve through it)
- **an interpreter spawn** (`python -c "subprocess.run([...])"`), which never touches shell
  aliasing, wrappers or functions
- **an environment variable the control treats as privilege**, which any caller can set
- **a self-service confinement switch** (e.g. re-entering a permissive security profile by name),
  which turns a boundary into a request

Give a concrete existence proof (file:line or an exit code plus the content returned), not a
suspicion. Where a predecessor or sibling implementation exists, the alternate path is the
default assumption.

---

## Proof 4 — SELF-TEST: does the suite exercise the real path

The proof a green suite hides. Two questions:

1. **Which process does the test spawn?** If it spawns the control itself, it cannot distinguish
   "wired" from "not wired" — both return the control's refusal.
2. **Would removing the control change this test's result?** If no, the test is a self-portrait of
   the artifact, not a measurement of the system.

A passing suite is therefore not evidence for a wiring claim at all. Drive the routes a real
caller would use, from the caller's own context (same uid, same groups, same profile), and grade
by the content returned:

- the bare/aliased invocation an ordinary agent types
- the absolute path
- an interpreter spawn
- the documented bypass vector, attempted directly

Meta-rule: **a suite whose self-test cannot fail is a banner with a test suite.** Where the suite
offers a self-test, verify the self-test itself detects a known-open control before trusting its
green.

### The residual class is where open defects hide

Reports under pressure grow a classification for gaps that are declared unfixable —
`ROOT_RESIDUAL`, `environmental`, `not-closeable-here`, `accepted-risk`. Treat that class as a
claim requiring the same warrant as any other, and falsify it before you relay it: an "impossible
here" label converts an open defect into a documented limit, which is the most attractive place
for a defect to survive. Test the specific impossibility asserted (e.g. "no kernel mechanism
denies this principal") with a controlled experiment.

---

## Remediate at the layer the threat is at

Before proposing a mechanism change — a new service identity, moving a store, changing ownership,
de-privileging a caller — test whether an **existing** mechanism already denies the threat when it
is actually applied to it.

The trap: an asset owned by a privileged uid looks unreachable only by moving the asset, because
ownership and mode are inert against that uid. But a confinement layer (LSM/mandatory access
control, capability drop, namespace) can bind the same principal, and the fix is then to
**confine the callers**, not to relocate the asset. Deciding this costs one experiment:

```bash
# two identical scripts, same uid, same target file; only one is covered by a profile
<uncovered-path>      # expect: reads the target
<covered-path>        # expect: denied
```

Same uid + same target + opposite results ⇒ the existing layer is sufficient and the gap is a
**coverage** gap, not a capability gap. Report it as such; it is a much smaller change than a
re-architecture, and proposing the large change instead is itself a defect of the analysis.

Residual honesty: where a control genuinely does not cover every caller, report the coverage as a
number (`N of M routes blocked`) and name the uncovered routes. Never let a partial control be
described by its strongest single route.

---

## Attesting a receipt or seal

A receipt is not evidence that the event happened; it is evidence only if it **corresponds** to the
event. Verify by recomputation:

```bash
sha256sum <artifact>          # compare against the hash the receipt attests
```

If the attested digest was never observed on disk — because a second writer changed the file after
the seal, or because the seal recorded an intended rather than an actual state — the receipt
attests nothing. Record the mismatch with all digests (before / after / attested); do not silently
prefer one.

---

## Report shape

One row per control. Keep the raw evidence in the row; do not summarise it away.

| Control | CALLER | EFFECT | BYPASS | SELF-TEST | Verdict |
|---|---|---|---|---|---|
| `<name>` | `<n callers, surfaces swept>` | `<bad input → changed? y/n>` | `<alternate path file:line or none>` | `<does the suite drive a real caller? y/n>` | `ENFORCED` / `ARTIFACT` / `CONFIG_ONLY` / `PARTIAL(<n>/<m> routes)` |

Verdict vocabulary:

- **ENFORCED** — all four proofs hold with evidence.
- **ARTIFACT** — exists, nothing invokes it (or it cannot refuse).
- **CONFIG_ONLY** — a default or setting, not a boundary. Safe-by-default is not authority.
- **PARTIAL** — the mechanism works where applied but does not cover every route. Always paired
  with the coverage fraction and the named uncovered routes.
- **UNPROVEN** — a proof could not be run. This is a real answer, not a pass.

When a report has to be corrected, correct the **artifact** (the suite, the header, the spec
diagram), not only the chat message — a false green left in a file will be re-read by the next
agent as evidence. Withdraw the superseded claim in place, name the measured value that replaces
it, and leave the working parts of the system alone.

## Related

- Receipt/claim evidence rules and the probe-to-claim table: `claim-receipt-discipline`.
- Absence claims and positive controls: `assertion-window-discipline`.
