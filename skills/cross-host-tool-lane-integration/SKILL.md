---
name: cross-host-tool-lane-integration
description: "Use when a tool server on one host is used from another."
version: 1.0.0
risk_tier: low
floor_scope: [F2, F11]
autonomy_tier: T1
tags: [mcp, stdio, tailnet, proxy, integration, probe, cross-host]
triggers:
  - "failed to start server"
  - "MCP error -32000"
  - "stdin is not writable"
  - "keepalive keeps dropping"
  - "reconnect budget exhausted"
  - "server is up but tools return empty"
  - "copied the file, md5 same"
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Cross-Host Tool Lane Integration

> *Reachable* and *answered* are different states. A lane can be open, authenticated, and return a
> well-formed response containing nothing.

This is the class where a tool server (MCP stdio shim, sidecar, HTTP facade) lives on host A and is
configured for consumption on host B. The failures are almost never "the service is down". They are: the
config names an artifact that does not exist, the artifact exists but is the wrong revision, the transport
works locally and dies at the proxy, or the call fails and the shim reports it as success.

## Procedure

### 1. Read the consumer's real config, not a description of it

Parse the file and print the entry beside its mtime:

```bash
python3 -c "
import json, os, time
c = json.load(open('<config>.json'))
e = c['mcp']['servers']['<name>']
print(json.dumps(e, indent=1))
print('mtime:', time.strftime('%Y-%m-%d %H:%M', time.localtime(os.path.getmtime('<config>.json'))))
"
```

A config that has not been written has not changed, whatever a report says; mtime is the receipt. Read
`command`/`args` (stdio) vs `url`/`transport` (http) and note which shape is actually present — a
half-migrated entry typically carries the env var of the new shape and the transport keys of the old one.

### 2. Resolve the artifact the config actually names

Filename drift is common because these names are hand-typed: one character apart is two different
programs. Before anything else:

```bash
ls -la <dir>/
md5sum <dir>/<named-file> 2>/dev/null || echo "NAMED FILE ABSENT"
stat -c '%y' <dir>/<named-file>
```

Then find what you were probably meant to run, and any newer copies that landed elsewhere:

```bash
find /root -maxdepth 5 -name '<pattern>*.py' | while read f; do
  echo "$(md5sum "$f" | cut -c1-8)  $(stat -c %y "$f" | cut -c1-16)  $f"
done
```

A "copied it already" claim that leaves the destination md5 and mtime unchanged is a **write that landed
elsewhere**. Scoring the destination hash is the only proof of the copy; a source hash says nothing about
the destination, and a hash quoted before an edit described as "+N -M" is stale by construction.

### 3. Spawn exactly as the consumer spawns

Not by importing the module, not by calling the tool function — by subprocess with the resolved command,
args, and **environment from the config**, piping newline-delimited JSON-RPC:

```bash
python3 scripts/mcp_stdio_spawn_probe.py --config <config>.json --server <name> --tool <read-only-tool>
```

The probe reports, per request: whether a result came back, `isError`, and whether the payload carries the
fields the tool promised. Importing the module instead of spawning it hides every problem class in this
skill — the failure lives in the process boundary, the env, and the transport.

### 4. Call the daemon directly and diff the two payloads

This localises the fault. One socket, no wrapper:

```python
s = socket.create_connection((HOST, PORT), timeout=10)
s.sendall(f"GET /health HTTP/1.1\r\nHost: {HOST}:{PORT}\r\nConnection: close\r\n\r\n".encode())
```

If the direct call returns real data and the shim returns a stub, the shim is the defect — regardless of
its `initialize` succeeding. `initialize` proves the process starts, nothing more.

### 5. Exposing a loopback-only service to a tailnet

Keep the service bound to `127.0.0.1` and put the listener on the mesh:

```bash
tailscale serve --bg --tcp <port> tcp://127.0.0.1:<port>
tailscale serve status | grep <port>          # confirm
tailscale serve --tcp <port> off              # reverse
```

`ss -ltnp` then shows two entries: the process on loopback and `tailscaled` on the tailnet address. That is
correct, not a duplicate. Prefer this over changing the application's bind address — it concentrates the
blast radius in one documented place and needs no restart.

## Pitfalls

- **A half-close is fatal through a TCP proxy, and silent.** A client that does `sendall()` then
  `shutdown(SHUT_WR)` to signal end-of-request works on loopback and fails across a proxy: the half-close
  can arrive before the request is forwarded, the proxy tears the connection down, and the caller reads
  **0 bytes**. Read until the response is complete — parse `Content-Length` and stop there, or read to EOF
  without half-closing. Measured on one host pair: with the half-close, 0 bytes; without it, 6527 bytes of
  `HTTP/1.1 200 OK`. Any client written against loopback assumptions must be re-tested before it is
  pointed at a remote daemon.
- **`status=0, body={}` is a fabricated success.** A parser that turns "no response" into an empty dict
  hands the caller a well-formed result meaning nothing. Return a typed error (`RuntimeError: <service>
  unreachable at host:port`) so the failure is visible at the boundary instead of being rendered as data.
  Same for `json.JSONDecodeError` — surface `_unparsed_body`, never `{}`.
- **`isError: false` with a stub payload is a failure.** Inspect the payload's shape, not the flag. The
  giveaway: a top-level object containing only provenance/version/missing-input keys and no data keys.
  Compare against the direct call before calling the lane healthy.
- **A description field is agent-facing documentation and drifts first.** An entry whose description says
  "daemon on 127.0.0.1" while its env points at another host misleads every agent that reads the tool list.
  Fix description and transport in the same edit — same class as a deprecated verdict field still printed
  beside a live one.
- **Hot-reload depends on key scope; test it, never assume it.** Check the consumer's own log rather than
  reasoning about it: `journalctl -u <service> --since "10 minutes ago" | grep -i 'reload\|config change'`.
  A line reading *config hot reload applied (mcp.servers.<name>.description)* is proof for that key and
  only that key. Capture the service start time too — a process older than the config edit runs the old
  copy, whatever the file says.
- **Two revisions of one shim answer with two different formulas.** A shim reporting
  `formula_version: X` while the daemon reports `Y` is version skew, not transport, and a clean
  `initialize` hides it. Print the payload's own provenance/version and diff it against the daemon's.
- **A tool list proves schema registration, not reachability.** `tools/list` is served by the process
  itself. Only a `tools/call` returning daemon data exercises the lane.
- **If the destination host is another operator's, test from a temp copy.** Ship to `/tmp`, probe there,
  delete, report the md5. Do not edit their installed file or restart their service.

## Receipt shape

Report per hop, not as one verdict:

```
config     : <path> mtime=<ts>  shape=stdio|http
artifact   : <path> md5=<8> bytes=<n> mtime=<ts>   (or: NAMED FILE ABSENT)
spawn      : initialize=<ok|fail> tools=<n> call=<tool> isError=<bool> payload_keys=[...]
direct     : <url> keys=[...]        # the baseline
verdict    : which hop is broken
next       : one step   reversibility: one step
```

Script: `scripts/mcp_stdio_spawn_probe.py`.
