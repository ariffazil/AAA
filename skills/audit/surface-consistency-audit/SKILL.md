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

If two readings are each true on their own axis, the finding is **unqualified namespacing**. The
fix is qualification (`tool:666` / `cog:888`) or splitting the field — not "correcting" one value
to match the other. Expect this class to dominate: in one audit it accounted for most findings.

When a number is overloaded, state which ladder it belongs to whenever you quote it, or the
next reader resolves it against the wrong one and reports a contradiction you never had.

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

Probe the configuration (unit env, process env, drop-ins) — not just the code path. Then read the
layers together: one disabled layer among several intact ones is a much narrower finding than
"the control is broken", and the precise statement is what makes it actionable.

## Pitfalls

- **A client-side cache is not a server defect.** Before calling an advertised surface broken,
  confirm the names appear on the live wire. Names that exist nowhere live came from a stale
  client, not the server — and the two failure modes look identical in a bug report.
- **A convenience HTTP projection is often written independently** of the wire protocol and
  drifts silently. Treat it as its own surface with its own author, not as a view of the protocol.
- **A gate's own advice must be validated.** When a tool returns a list of legal or safe values,
  intersect it with the schema enum before acting. A list longer than the enum is a false
  affordance — and it can sit inside the very gate that guards irreversible operations.
- **A refusal is a result.** When an authority gate declines an operation, record the refusal as
  the correct outcome and read what it offered instead; then validate *those* alternatives against
  the schema before using them.
- **Do not attempt the sensitive operation to test it.** Read the code and the configuration.
  Minting a credential or exercising a signing path to "check" is itself the mutation.
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

## Relationship to other audits

Narrative-vs-state probing and multi-writer auditing are a separate discipline (see the
user-owned `live-probe-audit-pattern`). This skill covers the case where the *system itself*
reports inconsistently across its own surfaces — no human narrative involved. For claim
labelling (OBS/DER/INT, negative-claim burden), see the user-owned `arifos-evidence-policy`.
