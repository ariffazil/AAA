---
name: runtime-control-registration
description: "Use when a control exists but its runtime never loads it."
---

# Runtime Control Registration

> A control is not in the path because it exists. It is in the path when the runtime that dispatches
the work has been told its name.

Scope: the **registration layer** only — whether an already-written control is loaded, on which
interception surface, and whether it has ever fired. For the layers either side of it use
`enforcement-coverage-verification` (can a caller route around it) and `chokepoint-enforcement-audit`
(can the actor acquire the capability anyway). Do not duplicate those here.

## When this applies

- A module, plugin, middleware or policy file exists, is tested, and is described as enforced.
- A doctrine or spec was ratified and someone wants to know whether it does anything yet.
- An audit must say which surfaces of a runtime are gated and which are bare.
- A repo already carries a remedy for the failure class under investigation.

## Procedure

### 1. Read the runtime's own registration config, not the control's manifest

```bash
grep -n -A15 '^plugins:' <runtime-config>   # authoritative enabled/disabled registry
grep -n -A10 '^hooks:'   <runtime-config>   # the stages that actually dispatch
```

A directory present under the plugins path but absent from the enabled list is inert: deployed,
possibly tested, never loaded. A `hooks:` list in the module's own metadata registers nothing — it is
a request to be wired. Report which file the control is missing from.

### 2. Enumerate interception surfaces and report per stage

| Stage | Intercepts | Typical state |
|---|---|---|
| tool-call | outbound capability use | most often the only stage with a gate |
| model-call (pre) | request assembly, identity/context injection | frequently observer-only |
| output / dispatch (post) | what actually reaches a human | frequently bare; mistakes here are unrecallable |

A live gate on the tool stage licenses **no** claim about the output stage. Weight the verdict by
*which* surface is gated, never by how many gates exist — the bare surface is usually the one whose
errors cannot be retracted.

### 3. Read the control's own state line before its receipt

```bash
sed -n '1,30p' <control-file>   # STAGED / NOT_WIRED / ADVISORY / 'blocks nothing on its own'
```

The header is written by whoever built it and describes the wire. A deployment receipt describes an
intention, and is often produced by the same session that deployed the file. When they disagree, the
artifact is what runs.

### 4. Sensor or gate — audit what it records

An advisory verdict that blocks nothing on its own can only be audited for its recording:

```bash
ls -la <telemetry-or-holds-file>    # absent  -> never fired
wc -l  <telemetry-or-holds-file>    # static  -> died after the first run
tail -1 <telemetry-or-holds-file>   # timestamp -> last time it actually ran
```

Green bench self-test plus an absent or frozen output artifact is the standard shape: the logic was
exercised, the wire never was. Call it a sensor, not a gate.

### 5. Run the same probes on any existing remedy

Grep the repo for an already-ratified control covering the same failure class, then run steps 1–4
against it. A remedy that is itself unregistered means the failure class is *recurring*, and the dead
remedy — not the original instance — is the headline.

### 6. State the rung, per surface

```
doctrine ratified -> module written -> bench green -> registered in config -> fired on live traffic
```

Partial credit across these rungs is what turns "it is deployed" into a false green. Anything not
probed is `UNCHECKED`; a control with no registration and no caller is `ENFORCER_ABSENT`, not
`ENFORCING`.

## Pitfalls

- **A truncated sweep reads as absence.** A recursive grep over a live tree full of caches, archives
  and vendored copies hits its time budget or result cap and returns partial output *with no error* —
  and the write-up then states a negative universal the sweep never tested. Scope to specific subtrees
  and exclude the noise (`--exclude-dir=__pycache__ --exclude-dir=build --exclude-dir=.git
  --exclude-dir=_archive --exclude-dir=backups`), and prefer several targeted sweeps over one broad
  one. An incomplete sweep yields `UNCHECKED`, not `absent`.
- **A receipt for the file is not a receipt for the behaviour.** `DEPLOYED_AND_VERIFIED` beside a
  header reading `STAGED` is a contradiction, and the artifact is the one that runs.
- **Do not propose a second control to fix a reach problem.** A missing wire is a wire, not a new
  registry, spec or doctrine file — a parallel artifact restating the first is a duplicate, not
  coverage. Name the missing registration and the surface it belongs to.
- **Config-registered controls still need a restart.** A long-running host loads its plugin set once at
  start; editing the enabled list or the module on disk changes nothing until the process is restarted
  and the surface re-probed.
- **Rank findings by irreversibility, not gate count.** A gate protecting an unrecallable human-facing
  channel outranks a gate on a reversible internal step.

## Reporting shape

1. **What is registered and firing** — config entry plus a non-frozen output artifact, with the surface.
2. **What exists but is not registered** — file, self-declared state line, the config entry it lacks.
3. **Which surfaces are bare** — per stage, and the consequence of the bare one.
4. **The remedy's own reach**, when a ratified remedy for the same failure class exists.

Close on the missing wire and the surface it belongs to. Enabling a control on a human-facing surface
is a behaviour change to that surface: stage it and let the owner enable it rather than flipping it on
during an audit.
