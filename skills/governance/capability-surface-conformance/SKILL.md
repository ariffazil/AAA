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
  - "the check exists but does nothing"
  - "empty handler / no-op function"
  - "verification always inconclusive"
  - "fail-open branch"
  - "the comment says it checks but the code does not"
  - "doctrine says it enforces"
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
- a **terminal with an empty body** — a reachable, correctly-wired handler that does nothing
  (`escalate(){ }`, `def handle(x): pass`). Every upstream report says the lane exists; the lane
  ends in a function no input can change. This is the degenerate case of the bad-input test below:
  if nothing you pass alters the output, the control is absent even though its caller is real
- a **predicate hardcoded to one value while the receipt beside it reports the check passed** — a
  verification loop pushing `{criterion, passed: false}` for every criterion, declaring
  `state: "INCONCLUSIVE"`, and emitting `independence_verified: true` in the same return value. Both
  statements live inside one object, so nothing downstream ever resolves the contradiction
- a **fail-open recovery branch** — the credential is decoded, a claim inside it is trusted, and the
  function returns success, with a comment directly above asserting the property that would have
  prevented exactly this. Read the error path as carefully as the happy path: a fallback written to
  unblock a lane is where an authority invariant gets dropped, and the comment records the intent,
  not the shipped code

**A document that describes a gate is not evidence the gate exists.** A ratified doctrine, a spec
section, a header comment and a receipt field all *describe* a control; none of them are the control.
A verdict about whether something enforces, formed from the paper that documents it, is a verdict
about the paper — and it comes out wrong in the flattering direction, because the paper is the
version someone intended. Open the function that runs on the real path and read its body; a symbol
that is defined and never imported is doctrine wearing a filename.

**Grade a control by whether a bad input changes its output — never by its name, its test suite,
or its metadata.** Four proofs, all required:

| Proof | Question | Failing shape |
|---|---|---|
| **CALLER** | Who invokes it, in the path that matters? | grep every scheduler surface returns 0 |
| **EFFECT** | Does bad input change the output or block the action? | guard reorders; a total failure still returns the top-ranked item |
| **BYPASS** | Is there another route to the same effect? | a second renderer reads the raw source directly, skipping the gate |
| **SELF-TEST** | Does the test exercise the real invocation path? | the suite invokes the control itself and asserts the control refused — passes identically whether or not the control is wired |

### A test that invokes the control proves only the control

The SELF-TEST proof is separate from the other three because it is the failure mode an auditor
looking at a **green suite** is least likely to catch. A verification script that runs
`bash <guard_script> gmail ...` and asserts the guard refused has measured the script's behaviour,
not the system's. It returns the same PASS when the guard is wired into every path and when it is
wired into none. **Ask of every test: which process would this test have to spawn for the answer
to change if the control were removed?** If the answer is "the control itself", the test cannot
falsify the wiring claim.

The canonical correct shape drives an **unprivileged, real caller** and grades the CONTENT that
comes back — the exact invocation an ordinary agent would type, plus the absolute path (which
skips `PATH` aliasing), plus an interpreter spawn (which skips the shell). None of those three
routes is the control.

Corollary for the report: a suite's **verdict line is a claim like any other**. When the summary
says a boundary holds while a row in the same run measured it failing — or says a mechanism is
impossible while a row shows it working — the verdict was written, not derived. Re-derive the
verdict from the rows; never relay the summary.

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
8. **A registry that cannot be enumerated cannot be conformed against.** An index that returns
   counts, metadata and descriptions but **no per-skill / per-tool names** forces every client to
   guess — so it hides both staleness and absence. Grade an index by whether a caller can derive
   the complete name set from it alone; if not, that is the first defect to report, ahead of any
   individual missing name.
9. **Dispatch the primitive, do not read a doc — through the FULL protocol lifecycle.** The live
   wire surface is the only authority, but a probe that skips the handshake measures its own
   mistake. Two header gates fail at two different layers, and both read like a dead capability:

   ```
   1. Accept: application/json, text/event-stream   -> transport refusal before any handler runs
   2. initialize  -> session id                      -> arrives in the RESPONSE HEADER, not the body
   3. notifications/initialized
   4. POST methods WITH Mcp-Session-Id               -> else `SESSION_MISSING` / `Missing session ID`
   ```

   Rule 9 in one line: **a refusal that names a lifecycle step is not a capability verdict.**
   `SESSION_MISSING`, `NOT_INITIALIZED`, `must send notifications/initialized`, `client must accept
   text/event-stream` all mean *you are not yet a valid client*. Re-run the handshake before
   reporting anything, and never let one reach a defect list.

   Run `scripts/mcp_session_probe.py` rather than hand-typing curl — it performs the whole
   lifecycle and grades response content.
   ```bash
   python3 scripts/mcp_session_probe.py --port 18083 --list
   python3 scripts/mcp_session_probe.py --port 18083 --call well_registry_status --args '{}'
   python3 scripts/mcp_session_probe.py --scan 8088,7071,8081,18082,18083,7073
   ```

10. **A path that RESOLVES is not necessarily a path the reader can USE.** Grade an alias,
    symlink or projection by the **shape** its target has, not by whether the target exists — the
    loader reads `<name>/SKILL.md` (or a directory entry), so a link pointing at a *file*, or at a
    directory that holds no body, resolves cleanly and yields nothing. The existence check passes
    for every wrong shape; the shape check is the one that finds the defects. Same law as
    advertised-but-uncallable, one layer down: `broken: 0` answers "does the target exist", and
    does not answer "can anything read it".

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
- **`not yet` is not `never`.** A probe that skips a required protocol step measures the probe, not
  the capability. Report the true state — *unverified from this client* — and never promote it to
  "broken", "impossible" or "absent". This is the most expensive false negative in the class
  because it is *confident*: the error message is specific and authoritative-sounding, so it
  survives review and gets written up as a remediation item. Before escalating any negative, ask
  which protocol step your client performed, and re-run the correct sequence once. A defect list
  assembled from an incomplete client is a list about the client.
- **A witness reading a path where the thing does not exist is not a witness.** When two components
  disagree about which code is running, diff the RESOLVED PATHS before adjudicating the verdict —
  and `ls` each one. A verifier pointed at `/usr/local/lib/python3.*/dist-packages/<pkg>` while the
  live package sits at `<venv>/lib/python3.*/site-packages/<pkg>` is not reading a *different*
  revision; it is reading nothing, and every DRIFT/HASH_MISMATCH it emits is a statement about an
  empty target. Tell: the path contains a `*-deprecated` sibling, an editable-install `.pth`, or a
  `src/` with no package — remnants whose presence makes the directory look populated. The remedy is
  one attestation packet naming `import path + interpreter root + PID + manifest hash`, read by both
  witnesses, never two components each inferring the runtime independently. Corollary for any
  drift/parity claim: `source == built == deployed` is a three-way equality, so a fourth path's
  opinion is not a tiebreaker.
- **Alias residue.** A partial compatibility layer is worse than none: some names resolve,
  most do not, and the ones that resolve look healthy while returning the wrong contract.
  Either complete the translation or remove the aliases.
- **A view link whose target is a FILE passes every broken-link test and loads nothing.** An alias
  resolving to `…/<harness>/skills/<name>/SKILL.md` (a file) rather than to a **directory** in the
  canonical store resolves, so `find -L -xtype l` and every existence check report healthy, while
  the loader — which reads `<dir>/SKILL.md` — finds nothing. Detect the shape, not the existence:
  ```bash
  find <view_root> -type l | while read l; do t=$(realpath "$l"); [ -f "$t" ] && echo "FILE-TARGET $l -> $t"; done
  ```
  Measured: 14 such aliases invisible to the canonical census (canonical 850 bodies while the view
  tree offered 703 resolvable), each one a capability the library claimed and the loader could not
  serve. Repair order: **copy** the body into the canonical store under its own name (copy, never
  move — leave the harness copy), then repoint the alias at the canonical **directory**; re-assert
  that aliases-to-file fell and the canonical count rose. A count that does not move means the copy
  landed in a path the loader does not read.
- **A capability whose only copy lives in a harness tree is on loan, not canonicalised.** It is
  absent from the canonical census, outside the store's own governance, and one `git clean` in that
  harness away from vanishing. When a view points into a harness/profile tree the finding is not
  "a broken link" — it is a body that has not been promoted yet.
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
- **A served registry that is a COPY of a live tree drifts monotonically.** Whenever the thing
  you are conformance-checking is materialised — rsync'd, baked into an image, snapshotted into a
  ConfigMap, symlinked from a staging dir — compare `stat` mtime and entry count of the **served**
  root against the **live** root, and name the sync job that is supposed to close the gap. No sync
  job means it is a one-time bake wearing a registry's name. Do not report the individual missing
  entries until the copy itself is named as the cause — otherwise you produce a list of symptoms
  and the next reader re-derives the same list.
- **A guard that passes its own tests can still refuse valid inputs.** A containment/rejection
  control is graded by its stated INTENT, not by its green suite: read what it is defending and
  then count what it rejects. Refusals of legitimate, correctly-shaped inputs are a defect of the
  control, not evidence that the inputs were invalid.
- **A declaration layer that nothing reads is not evidence the capability is unwired.** A config
  block of switch-shaped keys (`*_locked_*`, `*_default`, `ENABLE_*`) can be completely inert — no
  reader anywhere — while the live route sits in a *different* registry one level over: a named
  provider, a dispatch table, a scheduler entry point. Reading the inert layer and concluding "this
  is not wired" is phantom absence wearing a config file, and it is the same defect as a ghost
  capability with the sign flipped. Before any "unwired / not live" claim, enumerate every layer
  that can carry a route (grep the provider or dispatch registry, not only the keys that look like
  the switch), then **dispatch the candidate and grade the CONTENT that comes back**. Corollary:
  when two routes reach the same effect, drive both and diff the artefacts they produce — a shared
  backend can hardcode a setting, so one route is correct in identity and drifted in behaviour, and
  only the side-by-side run exposes the gap. Report the gap; do not silently patch a backend that
  also serves another lane.
- **Framework-inherited advertisement is not the server's claim.** A runtime library can inject a
  capability advertisement unconditionally into every server built on it (a Python MCP framework
  adding an `extensions` block to every `initialize` response, for instance). Before grading an
  advertised-but-unimplemented capability as N per-server conformance defects, find the owner:
  ```bash
  grep -rn '<extension-id>' <venv>/lib/python*/site-packages/<framework>/   # locate the injecting line
  ```
  If the advertisement is framework-wide, the finding is **framework over-advertisement**. The
  remedy lives at framework level (patch upstream, or strip once at the framework) or at host level
  (hosts treat an advertisement as a *hint*, not a promise) — never as N per-server patches, which
  fix the symptom, leave the source, and create N drift points. Note the blast radius before
  proposing a framework patch: it changes the advertisement for every server that imports it.
- **An observation is not a verdict.** "Advertises X, implements nothing" is a CLAIM about observed
  state. Calling it *nonconformant* is a separate verdict needing a normative quote from the spec —
  an inference from a positive example ("the spec shows the implementing pattern") is not that
  quote. Specs commonly mandate that *negotiated* capabilities govern a session without stating
  that advertising an unused extension is a violation. Grade such a class
  `ADVERTISED_NO_BINDING` — observed state, intent unknown, framework-inherited — and hold the
  violation verdict until the normative text is in hand.
- **Re-audit an inventory after the method changes, and diff the two counts.** A sweep built on a
  naming convention (a `systemd` unit-name prefix, a file glob) silently excludes everything not
  following it — the undercount is a METHOD error, not a system finding. When a corrected method
  yields a larger count, say plainly that the first number was method-limited, and carry the
  superseded figure forward as retracted rather than letting both circulate as live.
- **A suite's summary line is a claim; the rows are the measurement.** When a verdict asserts a
  stronger conclusion than its own rows support — a boundary holds though a row measured it failing,
  or a mechanism is impossible though a row demonstrated it working — the summary was written, not
  derived. Recompute the verdict from the rows and relay the recomputed one.
- **A mechanism declared impossible deserves the same falsification as one declared working.**
  "No layer can deny this principal", "not closeable on this host", `ROOT_RESIDUAL`,
  `accepted-risk` — an unfixable classification retires an open defect into a documented limit, so
  it is where defects survive longest. Test the specific impossibility claimed with a controlled
  experiment before repeating it, and test it where the claim was made, not where it is convenient:
  a control proven to refuse in one context is evidence the mechanism exists, which is exactly the
  fact an "impossible" verdict denies.
- **A fix proposed one layer away from the threat is usually the wrong layer.** Where an asset
  looks exposed, the reflex is to relocate it or change its ownership and permissions — all of which
  are inert against a principal that can read anything. Establish first whether the confinement
  layer already binds that principal when applied to it; if it does, the gap is **coverage**
  (the control is not attached to the caller), and the smaller correct remedy is to attach it. Say
  which one it is before proposing either.
- **Correct the artifact, not only the message.** A false green left inside the suite, the header,
  or the spec diagram is re-read as evidence by the next agent, so withdrawing it in chat closes
  nothing. Withdraw the superseded claim in place, name the measured value that replaces it, and
  leave the parts that were verified working untouched — a correction is not a teardown.

## Reference

- `scripts/mcp_session_probe.py` — full-lifecycle probe (initialize → session id →
  `notifications/initialized` → `tools/list` / `tools/call`). Use it instead of hand-typed curl;
  grades response CONTENT, not status codes. Run before reporting any capability as dead.
- `references/arifos-surface-inventory.md` — the concrete projection list, the canonical
  stage-map SOT location, and the known drift sites for the arifOS federation.
- `references/control-enforcement-probe.md` — re-runnable CALLER / EFFECT / BYPASS / SELF-TEST
  procedure: the scheduler surfaces to sweep, the bad-input test, the real-caller routes, the
  harm-vs-surrogate probe design, the controlled confinement experiment, and the report shape.
- `references/measured-constant-probe.md` — when a scalar labelled `MEASURED` never moves: the
  input-provenance table, the falsy-merge pattern that converts absence into a default, and the
  step that matters — enumerating every implementation of one quantity to find which one actually
  SURFACES, since the honest sibling is usually the one wired to nothing.

DITEMPA BUKAN DIBERI.
