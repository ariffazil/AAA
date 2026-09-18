---
id: capability-surface-conformance
name: capability-surface-conformance
version: 1.0.0
description: Use when a capability reports dead, unknown, or broken.
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

DITEMPA BUKAN DIBERI.
