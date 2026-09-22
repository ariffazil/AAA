# Status-field axes — qualify the name, or the next reader reports a contradiction you never had

Scope: any health / status / report surface that publishes a scalar or boolean standing for "how
this system is doing". The same field name drifts across surfaces when two different questions share
it, and both surfaces then look wrong to whoever resolves the value against the other ladder.

## The axis inventory

Ask which row the field actually answers. Two surfaces can both be correct while disagreeing
because they answer different rows.

| axis | question it answers | evidence that settles it |
|---|---|---|
| source vs built | does the repo head match the compiled artifact? | VCS head, commit marker, commit-map |
| built vs deployed | is the running thing the thing that was built? | deploy marker, image digest, import path |
| deployed vs canonical ref | does the running thing match the *declared target*, or only itself? | the remote ref, not a local copy — see below |
| artifact vs build | did *this* component change, or only something adjacent? | per-component / per-module hashes |
| contract vs registry | does the declared set match the registered set? | enum length vs registry length, per-key diff |
| advertised vs callable | is it published, registered, *and* does dispatch resolve it? | name lists vs a live read-path dispatch |
| proven vs invocable | has it durably succeeded recently, or could it merely be called? | success receipts in a window vs schema presence |
| measured vs unmeasured | is the zero a real zero, or "never observed"? | explicit `status: UNMEASURED` vs a bare `0.0` |

A bare `false`, `0.0`, or missing field is ambiguous across every row. `0.0` is the worst case: it
means at-zero *and* never-measured. Annotate the status, or the ambiguity stays silent.

## Four shapes a status field takes

1. **Qualified namespace — use this.** One parent key per axis, each with its own value and status:
   `deployment_drift{source_commit, built_commit, deployed_commit, drift, status}` and, separately,
   `surface_drift{drift_count}`. The axis is in the name, so no reader can resolve the value
   against the wrong ladder. Prefer this shape; it is the fix for the class.
2. **Flat boolean over two axes — a defect.** One `drift: true` computed as
   `source_vs_built OR artifact_vs_build` cannot be actioned: the reader cannot tell whether to
   redeploy or to rebuild.
3. **Absence — not a pass.** A status surface carrying no drift field at all while reporting
   `healthy` makes a negative claim with no evidence behind it. Report the *missing field* as the
   finding; do not read `healthy` as confirmation.
4. **Shadowed duplicate — a defect.** The same concept emitted twice in one payload, the second
   occurrence written from a pre-transformation value. Both fields are right in isolation; the
   payload contradicts itself. See SKILL.md Step 3.

## Reporting rule

Quote the axis with the value, every time: not "drift is true" but "source-vs-built drift is true
while artifact-vs-build drift is false". If you cannot name the axis, you have not separated the
axes yet — and the contradiction you are about to report may be one you created yourself.

## The comparand can be self-referential — and then there is no external axis at all

A drift field is only as good as the reference it resolves against. Before trusting one, open the
function that computes it and name both sides.

Measured: `deployment_drift_status` was computed as built-vs-live, where *both* sides derived from
the same working tree. It therefore reported `aligned` while the deployment sat six commits ahead of
the canonical remote. The same field had earlier reported drift over a stamp taken from the repo
head — so over one night it produced a false positive and a false negative, from one blind spot.

Two probes settle it:

```bash
# 1. what does the field compare against?  any `origin/`, `remote`, or checksum of the SOURCE artifact?
grep -nE 'origin|remote|rev-parse|sha256' <the_compute_function>
# 2. can the two sides ever become equal?  if it compares a branch head to origin/main,
#    then on a feature branch they NEVER resolve -> permanent HOLD, or a silent `aligned`.
f()  # call it, print every key, read the three commit values side by side
```

If both sides come from the same artefact, the field answers "is this thing consistent with itself"
— which is a real question, but not the one its name claims. Rename it, or add the missing
reference. Never leave the name implying an external comparison that never happens.

## The value vocabulary: check the producer can emit what the consumer compares

When two modules exchange a status string, the consumer's literal is a claim about the producer.

Measured: the producer emitted `"drift_detected"` / `"aligned"`; a consumer in another module
tested `== "drifted"`. That branch was unreachable — always false, in every state, forever — and it
sat inside a vitals roll-up that would therefore report drift only when a *different* field happened
to be populated.

```bash
grep -rn "== *'\?\"\?\(drifted\|degraded\|failed\)" <tree>   # every literal compared
# then, for each, grep the producer for that literal in an EMIT position
```

Two producers and three words is the tell. Enumerate the emitted vocabulary from the producer and
the compared vocabulary from every consumer, and diff them; the unmatched literals are dead
branches that read as guards.

## Sibling-surface sweep

When one organ of a multi-service system publishes a qualified shape and another flattens the same
concept, that is the fastest available evidence for which shape is correct *inside one codebase*.
Read every sibling's status endpoint before proposing a fix; adopt the best-qualified naming already
in the fleet rather than inventing a new one, and record which siblings are the reference
implementation, which are unqualified, and which carry the field not at all.
