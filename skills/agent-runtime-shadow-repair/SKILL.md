---
name: agent-runtime-shadow-repair
description: "Use when stabilising a live agent/MCP runtime surface."
version: 1.0.0
owner: curator
risk_tier: low
floor_scope: [F2, F4, F7, F11]
autonomy_tier: T1
tags: [mcp, runtime, audit, shadow, repair, conformance, agent]
capability_tier: fed-reasoning-heavy
ecology_state: WARM
owned_by: curator
authority_of: AAA
---

# Agent Runtime Shadow Repair

When the sovereign says *"refine and stabilise the runtime / MCP tools, resources, prompts"*, the task is
not a feature request. The surface already claims more than it does. Stabilising means **removing the
lies**, not adding organs.

## The one test that decides scope

> Does this change make the system tell the truth about itself?

If yes — it belongs in this job. If it only makes the system *do more*, it is a different job and needs its
own authority. A runtime that is wrong but honest can be corrected by the next reader; a runtime that is
reliable in appearance cannot, because nobody goes looking. **Apparent reliability is the expensive defect.**

Corollary, and the standing preference: repair the agent's honesty, never clamp the human's output. A
filter that strips, truncates, retires or narrows what a human said is itself the defect class — the fix
is to stop deleting substance, not to write a better deleter.

## The four defect classes to hunt

### 1. Retired in prose, still enforced in code

The comment above a guard says `RETIRED`, `disabled`, `no longer applied`. The predicate still returns the
enforcing value. Every reader of the diff believes it stopped; the behaviour never did.

```python
# "F13 retired the forced clamp" — but the guard below still fires
if _lane_should_clamp(lane) and mode != "light":
    mode = "light"          # still deletes content from every group lane
```

Retirement is real only when (a) the predicate returns a constant, **and** (b) the callers were updated.
Grep the function body, never the changelog. Repair by making it a **named no-op whose docstring states its
retirement** — deleting the symbol erases the audit trail, leaving it executable preserves the defect.

### 2. A gate whose threshold reads a value that was later withheld

A scalar gets nulled out so it stops being falsely precise. Every `(value or 0.0) >= threshold` downstream
becomes permanently false. The output stays structurally clean, the suite stays green if it only asserts
structure, and **the most serious alarm goes dark while the tool reports healthy**.

Withholding a number is a **schema change to every boolean that consumes it**. Before calling a withhold
done:

```bash
grep -n '<field_name>' <module>.py | grep -E 'or 0|or 1|or "|>=|<=|min\(|max\('
```

Re-derive each dependent predicate from the axes that DO ship. Never resurrect the withheld number to make
a boolean work — that re-imports the false precision the withhold existed to prevent.

### 3. Declared surface ≠ served surface

A `/health` counter, a declared tuple and the wire can disagree three ways. Counters are display surfaces.
Enumerate live over the real transport and set-diff **both directions**:

```python
async with Client("http://127.0.0.1:<port>/mcp") as c:
    live_r = sorted(str(r.uri) for r in await c.list_resources())
    live_t = sorted(t.name for t in await c.list_tools())
    live_p = sorted(p.name for p in await c.list_prompts())
served_not_declared = [x for x in live_r if x not in DECLARED]
declared_not_served = [x for x in DECLARED if x not in live_r]
```

A server that declares 42 and serves 46 reports `healthy`. Fix the **declaration**, not the counter — the
counter derives from it. Then re-probe and show both directions empty.

### 4. A suite with a permanent red is a muffled alarm

Tests pinned to a frozen literal — a version string, a directory layout, a band name — fail forever after a
legitimate change. The run gets read as "the usual noise", and a real defect landing in the same summary is
never seen.

Repair by **retargeting the assertion to the invariant**, never by pasting the new value:

| Frozen | Invariant |
|---|---|
| `VERSION == "<literal>"` | `VERSION == pyproject.version` |
| "file X inlines section Y" | "X's pointer to Y resolves and the canonical carries it" |
| `band in {MATERIAL, SEVERE}` | `band == WITHHELD_KEYWORD_HEURISTIC and warrant is non-empty` |

Updating the literal only resets the clock. And when a change makes an old assertion honest-but-different
(a scalar deliberately withheld, a layout deliberately moved) — **re-answer the test's original question**
rather than deleting the test: asserting that the *warrant* ships is a stronger contract than what it
replaced.

## Procedure

1. **Baseline the suite first**, unfiltered: `python3 -m pytest tests/ -q` from the package root. Record the
exact pass/fail count before touching anything — a later "106 passed" is only meaningful against a known
starting number, and the failures you are about to fix usually sit in the same output as stale, unread
assertions nobody has looked at in weeks.
2. **Enumerate the live surface over the transport** (not by importing the package — the import path and the
served path are different witnesses), and diff both directions against the declared constants.
3. **Read the body of every control-shaped symbol** on the human-facing path: `_gate`, `_clamp`,
`_should_*`, `_enforce_*`, `_apply_*`. Grade each by whether bad input changes its output.
4. **Fix the predicate**, not the projection. One owner per rule; every derivative follows.
5. **Re-probe live.** Restart the service and re-read `/health` plus a real tool call — a module edit that
is not loaded proves nothing. Compare live against declared and show both diffs empty.
6. **Full suite again**, unfiltered. Target: the stale red are gone because the assertions now test the real
invariant, and no new red appeared.
7. **Commit through the lane gate** (`/root/scripts/git-lane <lane> commit -m "..."`), with a message that
names each defect as a defect class, not as an incident narrative.
8. **State the residue in one line.** A live gateway/service that would kill the command that restarts it
cannot be restarted from inside its own process — say so plainly and give the single command the human
runs. Do not claim the change is live when only the module is.

## Pitfalls

- **`/health` is a claim, the wire is the measurement.** A health payload that prints counts is computing
them from the declaration it is supposed to be checking. Never quote a health count as surface truth.
- **Importing the module is not probing the server.** The installed path, an editable `.pth`, and a stale
service process can all disagree. Prove it with a client call over the transport after a restart.
- **`x or 0.0` silently coerces "withheld" into "failed the threshold".** Any place a falsy merge sits
between a nullable measurement and a boolean is a place an alarm can die quietly.
- **Do not add a filter to fix a filter.** When a clamp has been deleting human-facing content, the repair is
to remove the clamp, not to add a narrower one that deletes less. New guards need a named defect class
behind them, or they are just the old bangang wearing better manners.
- **A pinned literal in a test is the same defect as a hardcoded value in code** — it converts a real
invariant into a fact about one afternoon, then punishes every later afternoon.

## Human-edge conduct (when the surface emits reads of a person)

A human-facing runtime needs one rule the mechanical repairs do not cover: **the feeling belongs to the
person having it.** Describe, ask, hold, return — never author, correct, prescribe a replacement, or narrate
it back as a finding. Deliver structure, not a verdict on someone's interior. Full form, plus the
language-paradox and two-channel rules: `references/human-edge-conduct.md`.

## Support files

- `references/human-edge-conduct.md` — the custody rule, why a verbal map can never be a read of interior
  state (the instrument is made of the measured), and the two-channel minimum for any claim about a person.
