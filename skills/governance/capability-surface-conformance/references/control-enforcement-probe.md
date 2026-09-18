# Control Enforcement Probe — CALLER / EFFECT / BYPASS

A re-runnable procedure to test whether something named like a control is actually in the causal
path. Applies to gates, guards, health checks, sandboxes, seals, budgets, privacy filters, shadow
modes, delivery-target locks, and drift/reason labels.

Run all three proofs. A control is not established until every one holds, and each proof is
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

---

## Proof 3 — BYPASS: another route to the same effect

A control on one path is not a control if a second path reaches the same effect without it.
Enumerate alternatives:

- a second renderer/consumer reading the raw source directly instead of the gated artifact
- a fallback branch that answers when the gate returns nothing
- a direct write path that skips the validating writer
- a legacy entry point still reachable

Give a concrete existence proof (file:line of the alternate path), not a suspicion. Where a
predecessor or sibling implementation exists, the alternate path is the default assumption.

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

| Control | CALLER | EFFECT | BYPASS | Verdict |
|---|---|---|---|---|
| `<name>` | `<n callers, surfaces swept>` | `<bad input → changed? y/n>` | `<alternate path file:line or none>` | `ENFORCED` / `ARTIFACT` / `CONFIG_ONLY` |

Verdict vocabulary:

- **ENFORCED** — all three proofs hold with evidence.
- **ARTIFACT** — exists, nothing invokes it (or it cannot refuse).
- **CONFIG_ONLY** — a default or setting, not a boundary. Safe-by-default is not authority.
- **UNPROVEN** — a proof could not be run. This is a real answer, not a pass.

## Related

- Receipt/claim evidence rules and the probe-to-claim table: `claim-receipt-discipline`.
- Absence claims and positive controls: `assertion-window-discipline`.
