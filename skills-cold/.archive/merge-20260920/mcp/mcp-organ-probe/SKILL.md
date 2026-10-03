---
name: mcp-organ-probe
description: "Probe an MCP organ before believing a 'broken' verdict."
version: 1.0.0
owner: AAA
category: governance
tags: [mcp, probe, handshake, capability, surface, verdict, conformance, f2, f11]
floors: [F2, F4, F11]
autonomy_tier: T1
triggers:
  - "is this tool broken"
  - "tool not callable"
  - "SESSION_MISSING"
  - "Unknown tool"
  - "registry drift"
  - "advertised but unreachable"
  - "probe this organ"
  - "surface truth"
  - "declared vs callable"
  - "check the organ"
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# MCP Organ Probe

**One line:** most "organ X is broken" findings are probe-method artifacts. Complete the lifecycle,
name the exact tool, and count all four surface states before reporting a defect.

## The law

> **When a probe returns a protocol or lifecycle error, suspect the probe before reporting the
> target as broken.**

An organ-failure report is a claim with a *method* attached. A skipped handshake, a near-miss tool
name, or an unread lifecycle message produces an error that *looks* like a capability defect and will
be escalated as one — often into a remediation plan that "fixes" a contract that already works.

## Step 0 — the handshake, before any interpretation

A streamable-HTTP / SSE MCP server answers only after a 3-step lifecycle. A raw `curl` that skips it
receives a protocol error, and that error is **correct server behaviour** — not a broken contract, not
a dead lane, not a guard.

```
1. POST initialize                 -> capture `Mcp-Session-Id` from the RESPONSE HEADER
2. POST notifications/initialized  -> 202, EMPTY body, and NO `id` field
                                      (send it WITH the captured session header)
3. POST tools/list | resources/list | tools/call  -> now returns real data
```

Headers on **every** call: `Content-Type: application/json` and
`Accept: application/json, text/event-stream`.

```bash
for p in 8081:geox 18082:wealth 18083:well; do
  port=${p%%:*}; name=${p##*:}
  hdr=$(curl -s -D - -o /dev/null --max-time 10 -X POST "http://127.0.0.1:$port/mcp" \
    -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" \
    -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"probe","version":"1"}}}')
  sid=$(echo "$hdr" | grep -i '^mcp-session-id:' | tr -d '\r' | awk '{print $2}')
  [ -n "$sid" ] || { echo "$name: NO SESSION HEADER"; continue; }
  curl -s -X POST "http://127.0.0.1:$port/mcp" \
    -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" \
    -H "Mcp-Session-Id: $sid" -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'
done
```

For a full multi-call client (session tracking, expiry, the empty-202 body trap), use
`live-probe-audit-pattern` -> `references/mcp-sse-session-lifecycle.md`.

### The three misreadings, verbatim

| Raw probe returned | What it actually is | What it is NOT |
|---|---|---|
| `SESSION_MISSING: Mcp-Session-Id header required` | the server asking for the documented handshake | an unsatisfiable contract |
| `Missing session ID` / `MCP_LIFECYCLE: tools/call rejected until client sends notifications/initialized` | step 2 never sent | a runtime guard blocking the tool |
| `Unknown tool: '<name>'` | the name was never advertised | an advertised-but-unreachable tool |

## Step 1 — four numbers, never one

```bash
curl -s :PORT/tools        # DECLARED   — what the REST surface advertises
# handshake + tools/list   # EXPOSED    — what a client can enumerate
# handshake + tools/call   # CALLABLE   — prove end-to-end; a list entry proves nothing
#                          # AUTHORIZED — does an envelope permit the call
```

- Report the four separately. Do not average them, and never quote one as another.
- **DECLARED and EXPOSED can disagree in either direction, and a one-entry gap is a finding.**
- `callable: 0` on a tool you never handshaked is not a finding — it is an unfinished probe.

## Step 2 — exact-name check before any "broken" verdict

Grep the advertised list for the tool's **exact** name first. A tool that was never advertised
returning `Unknown tool` is a name error in the probe. Near-miss names differ only by a suffix
(`*_registry_status` vs `*_system_registry_status`) and fail identically to a real defect.

```bash
<handshake> … | grep -o '"[a-z_]*_[a-z_]*"' | sort -u | grep -i <fragment>
```

## Step 3 — one organ label may be several surfaces

A single organ name can resolve to multiple MCP ports with **disjoint** tool sets. Enumerate every
listening port before declaring "organ X's registry is clean / broken":

```bash
ss -tlnp 2>/dev/null | grep python3
```

A verdict on one surface says nothing about the others, so two auditors comparing different surfaces
will disagree with neither being wrong. Always state **which port** a verdict came from.

## Step 4 — use the installed instrument, not a hand count

If the federation ships a census/gate script for the thing you are counting, run it and quote *its*
number. An ad-hoc count that disagrees with the wired instrument is wrong until the instrument is
proven wrong.

This extends past skills to any inventoried surface: report the instrument's figure and name the
method you used, both. A count derived by comparing two directory shapes answers a different question
than "what can actually be loaded", and the two diverge widely.

## Pitfalls

- **A value computed but absent from the payload is dropped downstream of its builder.** Do not report
  "the field is missing, the builder must be broken" — invoke the builder directly in the **deployed**
  interpreter and see whether it returns the field. If it does, the loss is in a projection/mapping
  layer, not in the logic. See `references/layer-drop-diagnosis.md`.
- **A repair aimed at the projection layer cannot restore a value that was never populated.** Adding a
  field name to a keep-list / allow-list / verbosity set only works if the value is present upstream of
  it. Verify the value exists at the payload boundary before patching the projection.
- **A receipt whose reversal command cannot run is not a receipt.** If a ledger records `mv A B` for an
  operation that never happened, the reverse fails with `cannot stat`. Execute (or dry-run) the reversal
  of at least one row before trusting the ledger's claim about how many operations it performed.
- **Check inbound dependents before moving or archiving anything.** A directory that looks empty may be
  the live body behind a symlink elsewhere; removing it breaks every link pointing at it, silently and
  with no error on any surface. Resolve inbound links first, then move, then re-run the census.
- **Never read an exit status through a pipeline.** `cmd | tail; echo $?` prints the *last* command's
  status, not `cmd`'s. Capture to a file and check separately.
- **`pgrep -f` / `pkill -f` match the shell running them.** A pattern that appears in your own command
  line makes the tool kill or count itself. Use a bracket in the pattern (`pgrep -cf 'name[x]'`) so the
  running command line does not match.
- **Memory of a probe is not a probe.** A capability may only be declared down after a live sweep at
  the time of the claim; a verdict from an earlier hour is a claim with a timestamp, not a reading.

## Output contract

For each organ and each capability:

```
organ | port | DECLARED n | EXPOSED n | CALLABLE n | first failing transition | verdict
```

Name the **first failing transition** (`declared->exposed`, `exposed->callable`,
`callable->authorized`) rather than a bare Boolean. "Not callable" does not tell the reader what to
fix; "declared but not exposed on port N" does.
