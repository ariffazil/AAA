---
name: declared-vs-live-audit
description: "Use when checking what a system says about itself."
version: 1.0.0
triggers:
  - a /health, /status or self-report field will be quoted to a human
  - a service docstring, README or comment states a capability count or state
  - a rule or gate is described as retired, deprecated, disabled or no-op
  - an agent reports what it can do, or what it just did
  - a schema alias or unversioned name resolves to a version you did not choose
  - a receipt or audit-trail path is printed but never verified to exist
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Declared vs Live Audit

Every system carries two accounts of itself: what it **declares** (docstrings, health fields,
comments, schema aliases, pointers, a report an agent writes about itself) and what it **does**
(live registries, call paths, resolvers, behaviour under a diff). The gap between them is where
humans get lied to without anyone lying.

This is the same law at three scales, and the human case costs the most:

- **Service** — `/health` says 42 resources; the server serves 46.
- **Agent** — a self-report says it can do X; nothing in the call path reaches X.
- **Human** — a person's account of themselves is privileged evidence about their *experience* and
  weak evidence about their *causes*.

A system that cannot be accurate about itself cannot be trusted about anyone else. Not because it is
malicious — because it does not know where it stops.

## The four defect shapes

Recognise these by shape, not by product. All four look healthy from the outside.

| Shape | Signature | Why it survives |
|---|---|---|
| **Count drift** | a number in prose/health differs from the live registry | nobody diffs prose against `list_*` output |
| **Dangling pointer** | a path, receipt dir, or audit trail is *printed* but never created | printing a location feels like writing one |
| **Zombie rule** | the comment says "retired / deprecated / no-op"; the enforcement path is still live | the retirement was documented, not executed |
| **Alias shadow** | an unversioned name silently resolves to a version that is not the obvious one | resolution is correct; the *shape* changed |

## Procedure

### 1. Enumerate declarations and reality — in both directions

Diff both ways. **Declared-but-missing** and **live-but-undeclared** are different bugs with
different fixes, and checking one direction reports half the surface as healthy.

```python
declared = set(RESOURCE_URIS)
live     = {str(r.uri) for r in await mcp.list_resources()}
print("declared but missing:", sorted(declared - live))
print("live but undeclared:", sorted(live - declared))
```

```bash
curl -s -m 5 http://127.0.0.1:<port>/health | jq '{resources, tools_count, version, status}'
```

Reconcile the health number against the live list. If they disagree, the **live list is reality** and
the health field is a claim.

### 2. Kill every dangling pointer

For each path the system prints, test that it exists **before** quoting it to a human.

```bash
ls -d <the directory the message named> 2>&1
```

A message saying "audit trail: see `<path>`" while the tool never writes there is worse than no
message: it converts an absent control into a believed one. Fix by making the writer create the
artifact it advertises — not by editing the sentence.

### 3. Grep the enforcement path on any "retired" claim

A retired rule that still runs is worse than an active one, because the system lies about its own
shape and every reader downstream trusts the comment.

```bash
grep -rn "RETIRED\|deprecated\|no-op\|disabled" <module> | head
```

For each hit, find the call site and read what it returns. If it still enforces, either remove the
path or make it a **named no-op** that returns a constant, keeps its docstring, and can be grepped by
name. Deleting it silently is not the fix — a caller importing the symbol then breaks, and "retired"
becomes indistinguishable from "never existed".

### 4. Resolve aliases to a target and state the shape delta

An unversioned alias is a promise you cannot audit. When two versions of one contract exist, a
name-only binding can adopt either.

- Make the alias return `aliased_to: <target>` as structured data, not only in prose.
- State whether the versions are **shape-identical** or a **superset**. A backward-compatible superset
  (same `required` set, extra optional fields) is safe for readers and dangerous for writers, who then
  cannot tell which contract they emitted.
- Name the canonical target for new writers and mark the older version readable-only.

### 5. For an agent, replace self-report with a differential test

An agent cannot be read from what it says about itself. Give it two inputs that should produce
different behaviour and observe. An agent returning the same answer to different questions is
performing, whatever its self-description says.

Same test for a tool — **content sensitivity**: call it twice with materially different input;
identical output means the input never reached the logic.

### 6. Repair by derivation, never by re-typing the number

When a count is wrong, derive it from the registry. A hardcoded list is the mechanism that produced the
drift; editing its contents schedules the next one.

```python
# wrong: a whitelist of layers silently drops any layer added later
by_layer = {"canon": [], "playbooks": []}
for uri in uris:
    if layer in by_layer:
        by_layer[layer].append(uri)

# right: group from the data
by_layer = {}
for uri in uris:
    by_layer.setdefault(uri.split("/")[2], []).append(uri)
```

### 7. Verify, then close with the split

- Re-run the suite — a surface change touches discovery, so run the discovery tests, not just the module.
- Probe the **live service** after restart, not the source: `/health` plus one real call through the new
  surface.
- Re-pin any drift baseline and confirm the receipt file was actually written.
- State what you fixed and what a **sibling lane** fixed. Absorbing their fix into your commit destroys
  an independent second witness — the split is the evidence the defect was real.

## MCP surface probe (concrete)

Tool argument names are part of the contract and are **not** guessable from the prose description.

```python
async with Client(url) as c:
    schema = {t.name: t.inputSchema for t in await c.list_tools()}
    print(list(schema["hermes_retrieve"].get("properties", {})))
```

Read `properties` and `required` **before** the first call. A wrong keyword returns
`unexpected_keyword_argument` and looks like the tool is broken; it is the harness validating a schema
you did not read. Never conclude a capability is unavailable from an argument-validation error.

## Pitfalls

- **Quoting a health field without reconciling it against the live list.** `/health` is transport
  liveness plus self-report; treat its counts as claims.
- **Fixing the docstring instead of the count.** If prose and registry disagree, one is wrong — find
  which before editing either.
- **Reading "retired" as retired.** A comment is a claim. Grep the call path.
- **Assuming a green status means the surface is complete.** A service can be `healthy` while three of
  its resources were never declared, because nothing reconciles the two lists.
- **Treating `verified: true` or a success response as a state change.** Read state back from the store.
- **Declaring a capability dead from one bad probe.** Argument errors, transport expiry, and auth
  failures are all *probe* failures. Distinguish "the call failed" from "the capability does not exist"
  before reporting either.
- **Letting the audit become the product.** The point is not a longer defect list; it is that the next
  reader stops having to guess. Report the four shapes, the fix, and the residual — then stop.

## The one-line test

Before quoting any self-description to a human, ask: *did I probe the thing, or did I read the thing?*

If the answer is "I read it", the sentence is a claim — not a finding.

## Eureka updates (auto)

- 2026-10-22 · `e-65cdef5c9f66` · REPRESENTATION-DRIFT THEOREM (F13, 2026-10-22): Across the audit batch, failures that looked like capability failure were consistently representation failure — stale cards (GEOX 20 vs 27 live), stale baselines (FRAME 2026-09-15 vs October reality), schema…
- 2026-10-28 · `EUREKA::DEPLOY_DRIFT_REMEASURED::v1` · Postur deploy arifOS berubah dalam <30 minit antara dua pembacaan sesi berbeza: adik laporkan HEAD=3eab62697 (1 di hadapan origin/main); ukuran saya pukul 14:2xZ — HEAD=c98cc7ed7, origin/main 0 di hadapan/3 di belakang (hutang push 1→3), pokok kotor 4…
