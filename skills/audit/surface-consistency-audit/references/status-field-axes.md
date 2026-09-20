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

## Sibling-surface sweep

When one organ of a multi-service system publishes a qualified shape and another flattens the same
concept, that is the fastest available evidence for which shape is correct *inside one codebase*.
Read every sibling's status endpoint before proposing a fix; adopt the best-qualified naming already
in the fleet rather than inventing a new one, and record which siblings are the reference
implementation, which are unqualified, and which carry the field not at all.
