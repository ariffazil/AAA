---
id: capability-surface-conformance
name: capability-surface-conformance
version: 1.1.0
description: Use when a capability reports dead, unknown, or broken, or when a control-like name (gate, guard, check, sandbox, seal, shadow, drift, healthy) may not enforce anything.
owner: Hermes (arifOS federation)
risk_tier: low
autonomy_tier: T1
floor_scope: [F2, F4, F7, F11]
tags: [mcp, registry, conformance, surface, drift, verification, anti-fabrication]
triggers:
  - "unknown tool"
  - "tool not found"
  - "surface drift"
  - "registry drift"
  - "N of M tools work"
  - "the surface is broken"
  - "advertised but uncallable"
  - "why does this tool not exist"
  - "surface conformance"
  - "capability truth"
  - "schema mismatch"
  - "callable vs registered"
  - "verify capability surface"
  - "does this control actually control"
  - "gate not enforced"
  - "zero callers"
  - "false name"
  - "declaration vs enforcement"
  - "is this fix in the causal path"
  - "is this wired in"
---

# Capability Surface Conformance

Prove `advertised = registered = callable` before accepting a claim that a tool, endpoint
or capability is dead — or patching anything.

## The Invariant

```
Advertised = Registered = Callable = Schema-compatible = Authorized correctly
```

Any inequality is a defect. The defect belongs to the **one owner of
registration/dispatch** — never to whichever projection you happened to read first.

A capability that is advertised but uncallable is a **false affordance**.
A capability that is callable but unadvertised is a **phantom capability**.
Both are the same defect with the sign flipped.

### The enforcement extension — a control that nothing calls

The same law applies one layer up, to things named like controls. A module named `*_gate`,
`*_check`, `verify_*`, `*_sandbox`, `*_seal` may be advertised (it exists, it has tests, it is
documented) and **uncalled in the causal path of anything it claims to govern**. That is a false
affordance of governance:

```
Named = Invoked = Enforced = Can-refuse = Authorized correctly
```

Vocabulary: `SEMANTIC AUTHORITY = NAME ∩ CALL_PATH ∩ MEASURED_EFFECT ∩ BYPASS_RESISTANCE ∩ EVIDENCE`.
Any empty term → the authority claim is **VOID**. The NAME is never a term on its own.

The name is believed faster than the mechanism is read — which is why the defect propagates to
every downstream reader, including the next auditor. Named shapes, all one defect:

- a gate with **zero callers** in every scheduler/entry surface (an artifact, not a boundary)
- a metric hardcoded to a constant, or computed from a **flag** rather than from behaviour
- a privacy/security flag asserted in metadata that the renderer never consults
- a health check returning a **literal** status while probing nothing
- a sandbox whose containment engine is **imported and never invoked** on the execution path
- a guard that can reorder or delay but **cannot reject** (a total failure still returns a result)
- a `reason_code` produced by `x or "DEFAULT_LABEL"` — a fallback string where the text claims a
  measurement
- a label that overrides a fact in the same payload (a `state == "DEGRADED"` predicate firing
  while `drift` is `false`)

**Grade a control by whether a bad input changes its output — never by its name, its test suite,
or its metadata.** Three proofs, all required:

| Proof | Question | Failing shape |
|---|---|---|
| **CALLER** | Who invokes it, in the path that matters? | grep every scheduler surface returns 0 |
| **EFFECT** | Does bad input change the output or block the action? | guard reorders; a total failure still returns the top-ranked item |
| **BYPASS** | Is there another route to the same effect? | a second renderer reads the raw source directly, skipping the gate |

**Repair order: rename BEFORE you fix.** A control-shaped name that fails its proofs is corrected
by relabelling it honestly first (`*_health_check` → `*_status_banner`; `SHADOW=true` →
`delivery_default=off`), then implementing the mechanism if it is still wanted. Fixing the body
while the name keeps promising enforcement leaves the false assurance in place — the artifact now
does *something*, and the name still says it *guarantees*.

**A safe default is not a boundary.** "Off by default", "SHADOW by default", "read-only by
default" is reversible configuration, not an authority wall — anyone who can write the env var,
the config, or the flag opens it. Distinguish `safe-by-default` (the state you get if nobody
decides; protects against accident only) from `authority-boundary` (a check that refuses
regardless of configuration). Concrete tell: an accessor with a falsy default
(`os.environ.get("MODE", "SHADOW")`) is configuration; a gate that returns a refusal is a boundary.
Never describe the first as the second.

**A fix outside the causal path is not a fix.** After editing a file, confirm the scheduled or
live entry point actually invokes *that file* before claiming the defect is closed. Repairing a
dormant module changes nothing that runs. The check is the same CALLER proof, applied to your
own work.

**Family-level remedy:** give every control a **negative self-test** — disable its dependency,
inject bad input, attempt the bypass, and require the output to change as its contract states. A
control whose self-test cannot FAIL is a banner with a test suite.

## Always-On Rules

1. **Grade a capability by the CONTENT of its response — never by the absence of an
error code.** "Resolves" is not "works". A call returning `HOLD` with an empty actor, or
`null` for the advertised handle, has not worked.
2. **A NEGATIVE claim needs the same warrant as a positive one.** "Unknown", "absent",
"not advertised", "dead", "never wired" are claims. State the host, the client, and the
observation window. A negative from one vantage never generalises across hosts, clients,
or caches.
3. **Never accept a tool-name list from an audit.** Enumerate a fresh surface yourself,
then dispatch each claimed name.
4. **Diff semantics, not names.** A name-level hash passes while stage, authority, schema
and exposure diverge.
5. **One registry, one owner.** Fix the owner of registration/dispatch and make every
projection derive from it. Patching projections one by one is the failing anti-pattern.
6. **Read the same field at every nesting level** of a single response before trusting any
of it.
7. **A contradiction is same-question, same-axis, different answer.** Verify the axis
before calling one. Execution status, governance verdict and lifecycle state legitimately
differ.

## Procedure

### 1. Enumerate every projection

One registry, many views. Each can go stale independently:

| Projection | Why it matters |
|---|---|
| wire protocol `tools/list` | canonical for clients — quote this one |
| HTTP convenience endpoint (`/tools`, `/health` counters) | display surface; frequently stale |
| generated manifests (`*_sot.yaml`, `ai-plugin.json`, `peer-contract.json`) | consumed by other agents |
| session `allowed_next_verbs` / capability token | what an agent is permitted to call |
| registry introspection tool output | what the organ says about itself |

### 2. Dispatch ladder — classify each name

Three outcomes, not two:

| Outcome | Classification |
|---|---|
| content returned, no `isError` | advertised AND callable |
| `Unknown tool: '<name>'` | absent from the live registry — check for a stale client cache |
| resolves, then validation/schema error | **alias residue** — a legacy name mapped to a canonical handler whose contract was never translated. The worst shape: it looks alive |
| resolves, but HOLD / empty actor / null handle | alias resolves but does not work |

### 3. Semantic diff

Hash the normalized record, not the name list:

```
name, kind, schema, stage, authority, reversibility, blast radius, implementation, exposure, protocol binding
```

Deterministic canonical serialization before hashing (RFC 8785 JCS is the standard for
reproducible JSON hashing). Name equality is not surface equality.

### 4. Attribute the defect

Name the single owner of registration/dispatch. Then state which projections disagree and
in which direction. A stale projection is a symptom; the owner is the cause.

### 5. Coordinate before patching

Code-changed is not deployed. Land a fix on the **deployed** path, not the working
checkout, and re-pin HEAD immediately before the patch — another writer may have committed
while you were reading. Verify `built_commit == deployed_commit` and that the live
behaviour actually changed.

## Pitfalls

- **Client-side cache.** MCP clients cache `tools/list` at connect time. A client connected
  before a surface migration keeps dispatching pre-migration names and reports them as
  unknown. The server is not broken; that client's view is frozen. Report it as a
  client-side finding — the stale client is itself worth naming — not as a surface defect.
  Corollary: when an audit's verb list disagrees with the live list, the audit is usually
  the older view, not the authority.
- **Alias residue.** A partial compatibility layer is worse than none: some names resolve,
  most do not, and the ones that resolve look healthy while returning the wrong contract.
  Either complete the translation or remove the aliases.
- **Projection drift in the opposite direction.** The wire surface can be correct while a
  convenience endpoint is stale. Verify both before declaring either wrong.
- **Stage/token drift.** A numeric identifier that survives only as a *verdict token*,
  having been deprecated as a *stage*, is a classic semantic-divergence tell. Check the
  canonical stage map before trusting any stage printed on a surface.
- **Vantage divergence.** When two seats disagree on existence, diff the vantage
  (`hostname` + Tailscale IP) before adjudicating, then re-probe on the node that owns the
  code. Divergent vantage is the default explanation; fabrication is the rare one.
- **Contradiction false positive.** Verify the axis before calling a same-envelope
  disagreement a defect.

## Reference

- `references/arifos-surface-inventory.md` — the concrete projection list, the canonical
  stage-map SOT location, and the known drift sites for the arifOS federation.
- `references/control-enforcement-probe.md` — re-runnable CALLER / EFFECT / BYPASS procedure:
  the scheduler surfaces to sweep, the bad-input test, the receipt-hash check, and the report shape.

DITEMPA BUKAN DIBERI.
