---
name: hermes-mcp-surface-maintenance
description: "Use when repairing the hermes-mcp surface."
version: 1.0.0
owner: curator
risk_tier: low
floor_scope: [F2, F4, F11]
category: hermes-ops
tags: [hermes, mcp, runtime, repair, tests, service, surfaces]
related_skills: [hermes-runtime-audit, mcp-ops, verify-runtime]
---

# HERMES MCP Surface Maintenance

Maintaining `/root/.hermes/hermes_mcp/` — the meaning-integrity organ's tools, resources,
prompts, canon strings, registry constants and test suite, plus the live service on `:18087`.

**Load when:** the principal says the MCP surface must be "refined", "stabilised", "audited",
or "upgraded"; a `/health` number is being quoted as the map; a test run is red and nobody
remembers why; or an agent-facing behavioural law has to bind every organ, not just this one.

## The standing rule: repair by removal, never by addition

The recurring failure on this surface is not missing capability — it is small lies about what
the surface is and does. So the work is almost always **deletion and retargeting**: unwire a
retired rule, rebuild a boolean on real evidence, fix a count, retarget a stale assertion.

**Never** answer a prompt like "make this better / safer / more honest" by adding a filter
that strips output, an approval gate, or a new guard layer. The principal's standing position:
capabilities first, safety is emergence; conduct is fixed in doctrine, not enforced by output
transforms. A guard is only justified if it can say NO to a **named sentence class** — and it
must fail toward the person's own words, never toward silence.

## Procedure

### 1. Establish the live baseline before changing anything

```bash
curl -s http://127.0.0.1:18087/health | /usr/bin/python3 -c \
  "import json,sys;d=json.load(sys.stdin);print({k:d.get(k) for k in ('status','version','resources','canonical_tools','prompts','tools_count')})"
```

Then enumerate and diff **both directions** (claims vs served). See
`references/mcp-surface-probe-recipes.md` for the async diff script and tool-call patterns.

### 2. Look for the four defect classes, in this order

| Class | Symptom | Detection |
|---|---|---|
| **Retired-but-running** | Comment says RETIRED; behaviour still enforces | Call the predicate with an input the retirement claims freed |
| **Gate on a withdrawn field** | Alarm never fires; output looks clean | `grep` the withheld field for comparison operators |
| **Count drift** | `/health` number ≠ live surface | Bidirectional enumeration diff |
| **Stale-literal tests** | Suite red on every legitimate change | Read the assertion: literal or invariant? |

**Retired-but-running.** Prove it behaviourally, never by reading the comment. Repair by making
the predicate a **named no-op whose docstring states the retirement** — do not delete it
(importers break, history vanishes, the next reader cannot tell absence from accident).

**Gate on a withdrawn field.** When a value is withheld for honesty (keyword-derived,
unmeasured), every downstream boolean that thresholded it becomes permanently unsatisfiable —
the alarm is dark and never errors. Withdrawing a value and sweeping its consumers are **one
act**. Rebuild the boolean on the axes that do ship, and make its failure text name that
evidence ("not met at two axes over threshold") rather than a number the caller will never see.
Never resurrect the composite number to make a boolean work.

**Count drift.** A self-reported count is a claim. Fix the declaration (`RESOURCE_URIS` in
`_constants.py`, tool/prompt name tuples) so live == declared, and re-check after restart.

**Stale-literal tests.** Retarget the assertion onto the invariant it was proxying — never
update the literal:

| Frozen literal | Invariant it proxied | Correct assertion |
|---|---|---|
| `VERSION == "<old date>"` | wire and packaging agree | `VERSION ==` version parsed from `pyproject.toml` |
| `score == 0.0` | no asymmetry on a symmetric ledger | `is None` + warrant ships + no flag fires |
| a doc section inlined in a file that now only points | doctrine is bound and reachable | the pointer resolves; the canonical file carries all N items; **and** if anyone re-inlines the block the names must still match canonical |

Keep the old drift check armed and **conditional on presence** rather than deleting it — the
rule returns if the old shape returns. Distinguish *stale-but-correct* (retarget) from
*red-because-broken* (fix the code); `assert None == 0.0` tells you which.

### 3. Add one test that locks each repair

A repair without a regression test is a story. Put the behaviour, not the accident: call the
no-op predicate, call the detector on a case that must fire **and** a case that must stay quiet,
assert the canon string carries the new clause. Keep them in one class-level file rather than
one file per fix.

### 4. Verify, then restart, then re-verify

```bash
cd /root/.hermes && /usr/bin/python3 -m pytest tests/ -q      # must end `N passed`, zero fail
systemctl restart hermes-mcp-server.service && sleep 5
curl -s http://127.0.0.1:18087/health | ...                    # counts must match step 1 claims
```

Then **make one real tool call over the wire** (`Client("http://127.0.0.1:18087/mcp")`) that
exercises the repaired path. A green health endpoint plus a green suite still proves nothing
about the live process — the patch is not live until the service restarted.

### 5. Commit narrowly, then hand over what you cannot do

Stage only the files you touched. Other agents edit this tree concurrently — check `git status`
and `git log -5` before assuming a modified file is yours.

- `/root/.hermes` accepts a plain `git commit`.
- `/root/AAA` requires the lane identity: `git add <paths>` then `/root/scripts/git-lane hermes commit -m "..."`. `git-lane` injects the `REPO=` trailer the gate needs; a hand-written `-m "REPO=..."` normalises wrongly.

**The Telegram gateway cannot be restarted from inside a gateway process** — the runtime blocks
it (SIGTERM returns to the child). Do not try `nohup`, `&`, or a background sleep loop. Finish
the work, verify what you can, and hand the principal one line:

```
hermes gateway restart
```

## Doctrine placement (the one-owner rule)

When the repair is a **behavioural law for every agent** (not just this organ), write it once in
`/root/AAA/instructions/<topic>.md` as the owner, then have HERMES **render and cite** that
path — from the canon string, the prompt body, and the tool output. Three renderings of one
owner is correct; a second full copy inside `hermes_mcp` is a duplicated source of truth that
drifts the first time either side is edited.

Ask before writing doctrine: *does an existing ratified fragment already cover this?* Build on
its formalism rather than minting a rival one. A derivation that lands inside an existing
equation needs a staging note, not a canon file.

## Pitfalls

- **Warnings are not passes.** Compilers emit warnings and still produce output; a bad font
  family or a mis-parsed emphasis marker renders wrong while looking finished. Read stderr,
  not just the exit code.
- **A withdrawn value must never be re-fabricated to satisfy a caller.** If a scalar is
  `None` by design, the caller reads the axes — not a synthesised zero.
- **Do not widen a helper signature to fix one caller**; check whether tests reimplement the
  old shape, or the next shard fails where you did not run.
- **Do not treat a schema listing as truth.** `tools/list` proving a tool exists says nothing
  about whether its internal gate can fire. Call it.
- **Restart is a state transition, not a completion.** `PRODUCED ≠ SENT ≠ DELIVERED` applies to
  services too: patched ≠ restarted ≠ verified green ≠ exercised.
- **An agent-facing "safety" addition usually outlives its reason.** Prefer a docstring and a
  test over a new guard.

## Support files

- `references/mcp-surface-probe-recipes.md` — async enumeration diff, live tool-call probe, and
  the health-field reference for `:18087`.
