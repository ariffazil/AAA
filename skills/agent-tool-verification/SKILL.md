---
name: agent-tool-verification
description: "Use when claiming a tool or fix works or is broken."
version: 1.0.0
owner: AAA
risk_tier: low
floor_scope: [F1, F2, F11]
autonomy_tier: T1
tags: [verification, mcp, capability, stub, reload, claim-discipline]
triggers:
  - "is this tool working"
  - "fix the MCP server"
  - "capability reports dead or broken"
  - "verify a fix took effect"
  - "tool returns nothing useful"
  - "ghost capability"
  - "claim a server is fixed"
  - "deploy a patch to a running service"
  - "agent claims it is built"
---

# Agent Tool Verification

Claiming a tool works, or that a fix landed, is a **reality claim**, not a status update. Two
independent failures must be excluded before either claim is true:

1. the tool never did anything (ghost capability — never errors, so nothing surfaces it);
2. the running process never loaded the edit (fixed on disk, unchanged in reality).

Test 1, then 2. A green unit-test run excludes neither.

---

## Step 1 — Stub probe: does the tool do anything at all?

A tool that accepts a rich payload and returns a constant verdict is worse than a broken tool: it
never errors, so nothing ever surfaces it.

### Method — two contrasting inputs, echo stripped

1. **Read the real signatures first.** `inspect.signature` over every tool. Guessed kwargs raise
   `TypeError`, and a `TypeError` line looks identical to a constant-output line in a naive diff —
   that manufactures false findings and wastes a pass.
2. **Call each tool twice** with inputs that differ in the dimension the tool claims to judge: two
   subjects, two claim classes, two event descriptions.
3. **Strip the echo.** Recursively delete from each result every key whose name matches one of the
   tool's own parameter names. What remains is the tool's actual contribution.
4. **Compare the remainders.** Identical across both calls ⇒ constant output ⇒ defect.

```python
import inspect, json

def drop_echo(obj, pnames, depth=0):
    if depth > 4:
        return obj
    if isinstance(obj, dict):
        return {k: drop_echo(v, pnames, depth + 1) for k, v in obj.items() if k not in pnames}
    if isinstance(obj, list):
        return [drop_echo(v, pnames, depth + 1) for v in obj]
    return obj

def stub_sweep(mod, cases: dict):
    # cases: {tool_name: [call_kwargs_a, call_kwargs_b]}
    for name, variants in cases.items():
        fn = getattr(mod, name, None)
        if fn is None:
            continue
        pnames = set(inspect.signature(fn).parameters)
        outs = [json.dumps(drop_echo(fn(**v), pnames), sort_keys=True, default=str) for v in variants]
        print(("CONSTANT " if outs[0] == outs[1] else "VARIES   ") + name)
```

### Pitfalls

- **Reading code shape is not a substitute.** Grepping for `pass`, short bodies, or constant returns
  flags legitimate constant gate verdicts and misses stubs wrapped in a hundred lines of input
  marshalling. Run the behavioural probe.
- **Distinguish an error from a verdict.** A tool that refuses an invalid enum, or that demands a
  caller-supplied list it will not invent, is behaving correctly — constant-by-design is not a stub.
  Only a constant *judgement over varying inputs* is the defect.
- **A sibling agent's inventory is a citation, not evidence.** Cross-check its list against your own
  sweep and report only what you measured. Two agents on the same surface disagree often, and the
  count you did not take cannot be corrected later.
- **Widen the sweep past the tools you care about.** The stub you were not looking for is the one
  that has been silently answering questions for weeks.

---

## Step 2 — Live-code check: did the process load the edit?

A server file is loaded **once, at process start**. Editing it changes nothing until that process is
recreated, and a call through the running transport will faithfully return the **old** behaviour.

### Find every loader before claiming anything

```bash
ps -eo pid,ppid,lstart,cmd | grep "<server>.py" | grep -v grep
```

Expect up to two independent loaders running the same file. Both are easy to miss:

| Loader | How to recognise it | Where it is declared |
|---|---|---|
| systemd unit (HTTP) | `ppid 1`, carries its own `--port` | `systemctl cat <unit>` → `ExecStart` |
| gateway stdio child | `ppid` = the gateway pid, carries `--transport stdio` | the client's MCP config `args: [<path>, --transport, stdio]` |

Neither hot-reloads. The stdio child is spawned **once per gateway, not per session** — so a session
that has been up for days is holding days-old code.

Also resolve symlinks before diffing: two paths can be the same file, and a patch written under one
resolves under both. Confirm with `systemctl cat` that the unit's `ExecStart` path is the file you
actually edited — a live tree is often a separate checkout with a dirty worktree, so `sha256sum`
both copies before copying anything in.

### Verify on a fresh instance, not through the live one

```bash
python3 /path/server.py --transport stdio    # new process, new code, same file
```

Call the tool there, then call it through the live transport, and compare. The two answers
disagreeing *is the finding*.

### Restart discipline

- **Never restart the gateway from inside a gateway session.** The signal propagates to your own
  process and the command dies mid-flight. Restarts belong to a separate shell, or to an operator.
- Recreating a process that serves other people is an **operator decision**, not a cleanup step.
  Name it as a separate action with its own owner.

---

## Step 3 — Report the state you actually reached

Use transition vocabulary, never a boolean (`state-transition-discipline`).

| Reached | Say |
|---|---|
| Code edited, tests green, process still old | **"Fixed on disk, not live"** + name the restart as a separate action |
| Code edited, tests green, fresh instance confirms new behaviour | **"Fixed, verified on a fresh instance; live surface still stale"** |
| Process recreated, live call returns new behaviour | **"Live and verified"** + the observation that proves it |
| Probe could not run | **"Unverified"** — never "should work" |

Rules:

- **"Fixed on disk, not live" is a complete and honest status.** Reporting it as "fixed" is the
  transition lie; the person acting on it tests the live surface, gets the old answer, and loses
  trust in every other report from that session.
- **A green unit-test run is not proof the running surface changed.** Tests import the module; the
  live process holds the version it loaded at boot. Those are different objects.
- **Never present a tool's own output as proof of the tool's own capability.** A tool reporting its
  own success is echo. Independent observation lives on ports, hashes, files and process tables.
- **When a fix rebuilds a dependency's authority check, test both directions.** A gate that stops
  rejecting the false positive can silently stop rejecting the true positive. Assert the rejection
  case explicitly, not just the now-passing case — an asymmetric test proves the gate was loosened,
  not that it was corrected.

---

## Sibling skills

- `state-transition-discipline` — the transition vocabulary this skill reports in.
- `claim-receipt-discipline` — receipts, trace ids, and what makes a claim re-checkable.
- `mcp-testing` / `mcp-ops` — protocol conformance and server operation (this skill covers only the
  does-it-work / did-it-load axis).
- `verify-runtime` / `runtime-probe` — health and liveness probing.

DITEMPA BUKAN DIBERI ⚒️
