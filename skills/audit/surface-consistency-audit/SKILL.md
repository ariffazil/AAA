---
name: surface-consistency-audit
description: "Use when surfaces of one system disagree on a value."
version: 1.0.0
tags: [audit, consistency, multi-surface, wire-protocol, conflation]
---

# Surface Consistency Audit

> Trigger: a live system reports different values for the same thing on different surfaces —
> wire protocols, an HTTP projection, and the declared source of truth on disk.

A running system is not one source of truth. It is **many surfaces**, each read by a different
protocol, each able to be internally consistent and mutually contradictory — with no cache, no
stale replica, and no deployment skew needed to explain it.

## The law

**When two competent witnesses disagree about the same system, suspect the system first.**
Both readings are frequently correct *for their surface*. The divergence is the defect, not
noise around the defect.

Corollary: never let a shared name prove a shared identity. Two surfaces agreeing on the
*label* while disagreeing on the *semantics* passes every name-level check while being broken.
A hash over names certifies nothing.

## Step 1 — Enumerate every surface, through its own protocol

Never infer one surface from another. Query each natively and record protocol + source:

```bash
curl -s :PORT/tools                          # HTTP convenience projection
# native wire protocols — do NOT infer one from another:
#   tools/list     via JSON-RPC   → capability surface
#   prompts/list   via JSON-RPC   → prompt/template surface
#   resources/list via JSON-RPC   → resource surface
grep -rn '<value>' <repo>/<declared-canon>   # declared source of truth on disk
```

A finding is only actionable once you can say *which* surface says what, and through which
protocol you read it.

**Compare schemas, not just names.** Enumerating the surfaces is only half the job — the diff *is*
the audit. A name-set diff is the weakest possible comparison and it goes green while the system is
broken. Diff the per-object key sets, and the serialized byte size of one representative object,
across every surface:

```
names identical across wire / /tools / /tools.json : True   <- green light, means nothing
tool object bytes, same name, per surface         : 7407 / 4948 / 5048
key sets, same name, per surface                  : {annotations,_meta,...} vs {canonical,stage,...}
```

Names identical while field sets and byte sizes differ means the same object is published several
ways. Then ask of every field: *which* surfaces expose it? A field present on a manifest or
declared canon but absent from the wire is a field no real client ever reads — a declared control
that never reaches the caller. Confirm the names appear on the live wire before blaming a client,
and confirm the *fields* appear there before trusting the control.

## Step 2 — Look for duplicated constants, not a single stale file

The usual cause is two source files each hardcoding the same concept and never importing one
another. Check coupling before blaming deployment:

```bash
grep -n '^import\|^from' <surface_module>    # does it import the canon module? no import = duplicated
git log -S'<value>' -- <canon file>          # when the value moved, and whether the other file followed
```

An unowned second definition can diverge for months, because nothing compares the two. Same
package, same build, same mtime — and still contradictory.

## Step 3 — Separate the axes before calling a value wrong

Contradictory values are often **two different concepts sharing one field name**. Collect every
field that reports the concept, then ask what each could mean other than your reading:

- machine health vs caller authority
- a number on ladder A vs the same number on ladder B
- advertised vs registered vs callable
- a receipt vs a seal
- transport success vs postcondition success
- an agent name that looks like a stage number
- source-vs-built drift vs artifact-vs-built drift (two axes flattened into one boolean)
- advertised count vs dispatching count vs handler count
- a zero that means "at zero" vs a zero that means "never measured"

If two readings are each true on their own axis, the finding is **unqualified namespacing**. The
fix is qualification (`tool:666` / `cog:888`) or splitting the field — not "correcting" one value
to match the other. Expect this class to dominate: in one audit it accounted for most findings.

When a number is overloaded, state which ladder it belongs to whenever you quote it, or the
next reader resolves it against the wrong one and reports a contradiction you never had.

The converse also occurs, and it defeats the "which axis?" framing — so check for it explicitly.

### The shadowed field: one concept, emitted twice, from two computation stages

Not every contradiction is two concepts. Sometimes it is **one concept written twice in the same
payload**, where a dict spread re-emits a pre-transformation value *after* the corrected value has
already been used to compute a verdict:

```python
val = pre_transform()                        # e.g. artifact-vs-build
val = val or second_signal()                 # OR'd with a second axis
verdict = "DRIFT" if val else "VERIFIED"     # verdict reads the POST-transform value
payload = { "verdict": verdict, **_stale }   # spread re-emits the PRE-transform field  <- defect
```

Symptom: a single response carrying `drift=false` **and** `DRIFT_DETECTED` **and** `status=degraded`
— all three, simultaneously, from one builder. Both fields are correct in isolation; the payload is
the defect.

Read the payload builder before theorising. Search for a `**spread` and check whether any key it
carries is *also* computed locally — the spread wins because it is applied later. A neighbouring
field already patched for the same class is a strong tell: when a fix note in the code says "status
and X now agree", check the **next field over**, which is usually still shadowed.

Full axis inventory and the four naming shapes that qualify a status field:
`references/status-field-axes.md`.

## Step 4 — Two-call isolation (cheap, decisive)

To decide whether a field reports the world or echoes the request: call the *same* tool twice,
seconds apart, same session and actor, changing ONE input.

```
call A: mode=<irreversible op>  → verdict=HOLD,          substrate=DEGRADED
call B: mode=<safe/audit op>    → verdict=OBSERVE_ONLY,  substrate=HEALTHY
```

The machine did not change between calls. Any field that moved is **derived from the input**,
not measured from the world. This converts a suspicion into a controlled observation in two
calls, and it is usually the fastest route from "this looks wrong" to a defensible root cause.

## Step 5 — Check the control is engaged, not merely present

A guard in the source is not a guard in force. Config-disabled controls fail silently:

- `X = os.environ.get("GUARD_USER","")` with `if X:` skips the whole block when the variable is unset
- `except ImportError: pass` skips it again when the dependency is absent
- `logger.warning("deprecated…")` followed by executing the action is a **bypass**, not a warning
- a **self-consistency checker that subtracts its suspect set by name** before comparing:
  `internal_only = all_names - exposed - ABSORBED` structurally cannot report the absorbed names.
  The control is installed, wired, and blind to exactly the defect class it exists to catch.

Probe the configuration (unit env, process env, drop-ins) — not just the code path. Then read the
layers together: one disabled layer among several intact ones is a much narrower finding than
"the control is broken", and the precise statement is what makes it actionable.

For any checker, ask what it **filters out** before it compares, not only whether it runs. A
`CONSISTENT` verdict from a scope-narrowed comparator is not evidence — name the set the comparator
subtracted, or the verdict is unearned. The same move applies to every "all-clear": read the
allow-list, because the allow-list is where the blind spot is.

## Pitfalls

- **A client-side cache is not a server defect.** Before calling an advertised surface broken,
  confirm the names appear on the live wire. Names that exist nowhere live came from a stale
  client, not the server — and the two failure modes look identical in a bug report.
- **A convenience HTTP projection is often written independently** of the wire protocol and
  drifts silently. Treat it as its own surface with its own author, not as a view of the protocol.
- **A gate's own advice must be validated.** When a tool returns a list of legal or safe values,
  intersect it with the schema enum before acting. A list longer than the enum is a false
  affordance — and it can sit inside the very gate that guards irreversible operations.
- **A recorded finding the verdict never reads is not a finding.** Check that the divergence list
  actually feeds the verdict. Measured: `any_divergence = len(divergences) > 0` was computed and
  then omitted from the `if/elif` chain — so the checker could record a divergence and still print
  `CONSISTENT`.
- **Subtracting the suspects before comparing is the defect wearing the fix's clothes.** A
  consistency check that removes the known-bad names (`- ZEN_ABSORBED`) from the set it audits
  cannot report on them, by construction. Report the excluded set explicitly, and assert an
  invariant over it, rather than deleting it from view.
- **"Absorbed" must mean unreachable, not unspelled.** A name retired into another tool can still
  dispatch. Compare reachability across surfaces (`tools/list`, registry, advert cards), not names.
- **A refusal is a result.** When an authority gate declines an operation, record the refusal as
  the correct outcome and read what it offered instead; then validate *those* alternatives against
  the schema before using them.
- **Do not attempt the sensitive operation to test it.** Read the code and the configuration.
  Minting a credential or exercising a signing path to "check" is itself the mutation.
- **"Listed but dead" and "hidden but live" are both invisible to a name diff.** Enumerate the
  advertised set, then *dispatch* each ambiguous name using the cheapest read-only mode it offers
  and record the result — a name on no discovery surface can still execute, and a name advertised
  on three surfaces can answer `Unknown tool`. Only read-path modes are fair game; record anything
  mutation-capable as `UNTESTED` and read its disposition from source instead. Corollary: a count
  field claiming to number "callable" tools usually counts the *advertised* surface — read the
  field's own semantics string before quoting the number.
- **A negative claim carries the same burden as a positive one.** A lagging replica reports
  missing whatever is newer than its last sync; an absence claim carries node + path + copy-age
  or it is a rumour.

## Verdict contract

Report per surface, with protocol and source:

```
surface → value → protocol → file/endpoint
```

State the divergence, the coupling check, and the axis separation. Do not collapse to a single
winner unless the evidence actually settles it — **"both surfaces are live and contradictory"**
is a complete and useful verdict, and often the one that changes the system.

## Delivery surfaces — the audit does not end at the value

When the divergence has to be *fixed*, the source tree is not the last surface. Enumerate the
delivery path as its own set of surfaces, through their own protocols, before editing anything:

```bash
ls -la <venv>/lib/*/site-packages/<pkg>/   # COPY or symlink? readlink -f, compare inodes
python -c "import pkg; print(pkg.__file__)" # under the TARGET interpreter, not yours
systemctl cat <deploy-unit>; journalctl -u <deploy-unit> -n 30
```

Measured (arifOS MCP, 2026-09-21): the running kernel imported a **copy** in `site-packages`, not
the repo — and the scheduler meant to keep them aligned compared `git rev-parse HEAD` to
`origin/main`. With a feature branch checked out, `HEAD != origin/main` is permanent, so the
reconciler held on every tick, forever, while printing a success-looking line. Two defects in one
place:

- **A guard can be deadlocked by state it does not control.** The gate never failed; it never
  satisfied its own precondition again. Check whether the compared refs can ever become equal.
- **A log line printed unconditionally is not evidence.** The script printed
  `fast-forwarded to <sha>` after *any* successful pull step, including a no-op. Read the
  condition that wraps the message, not the message.

Also: the deploy script derived its source from its own location (`$(dirname $0)/..`) and deployed
the **checked-out branch**, so production can carry unpushed branch code while the scheduler
believes it is guarding against exactly that. Verify which tree the deploy actually reads — do not
infer it from the unit's description.

When delivery is blocked, the complete verdict names the chain position, not a boolean:
`PRODUCED → COMMITTED → PUSHED(ref) → DEPLOYED → OBSERVED`, and for each un-reached state, the
owners and the exact blocked operation. "Fixed" with no deployed commit is PRODUCED.

## Relationship to other audits

Narrative-vs-state probing and multi-writer auditing are a separate discipline (see the
user-owned `live-probe-audit-pattern`). This skill covers the case where the *system itself*
reports inconsistently across its own surfaces — no human narrative involved. For claim
labelling (OBS/DER/INT, negative-claim burden), see the user-owned `arifos-evidence-policy`.
