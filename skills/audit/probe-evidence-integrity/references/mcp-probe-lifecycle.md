# MCP Probe Lifecycle

Recipe for probing MCP servers so the result can bear a finding. Companion to
`probe-evidence-integrity` steps 1–6.

## 1. Full lifecycle, one session, in order

```
initialize → notifications/initialized → tools/list → resources/list
```

Stateful streamable-HTTP servers return an **empty** `tools/list` when the handshake is incomplete.
Sending `initialize` without the `notifications/initialized` follow-up **on the same session** is
the most common cause of a false "0 tools" reading.

A server reporting 0 tools while advertising the capability is far more likely mis-probed than
broken. Re-run the full sequence before writing the finding.

Headers for streamable HTTP:

```
Content-Type: application/json
Accept: application/json, text/event-stream
```

Some servers answer with SSE (`text/event-stream`). Parse the `data:` line — the raw body is not
JSON.

## 2. Version negotiation discriminator

Before reporting any protocol-version mismatch, establish whether the server negotiates at all:

```bash
curl -sS --max-time 8 -X POST http://<host>:<port>/mcp \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"9999-01-01","capabilities":{},"clientInfo":{"name":"diag","version":"1"}}}'
```

- Echoes `9999-01-01` back → **not negotiating**; pins/echoes one version. A client pinning that
  version is correct, not broken.
- Returns a supported version → negotiating.

Repeat per endpoint with the version you actually intend to use, then tabulate the fleet. An
advertised supported-version list is itself a claim: probe the versions you will use rather than
trusting the list, and reprobe the health endpoint's list against live behaviour if they disagree.

## 3. Authenticated session probe

Some kernels refuse every verb until a session is minted, returning a session-required error
otherwise. Sequence:

```bash
# 1. mint a session
SID=$(curl -sS -X POST http://127.0.0.1:8088/mcp \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"arif_init","arguments":{"mode":"init","actor_id":"<actor>"}}}' \
  | python3 -c "import sys,json;d=json.load(sys.stdin);print(json.loads(d['result']['content'][0]['text'])['session_id'])")

# 2. every subsequent verb carries the session header
curl -sS -X POST http://127.0.0.1:8088/mcp \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -H "mcp-session-id: $SID" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"arif_observe","arguments":{"mode":"vitals","actor_id":"<actor>","session_id":"'$SID'"}}}'
```

Compare the two responses. An unauthenticated call comes back with the constitution block
`_floor_measurement: "unmeasured"` and `failed_floors: []` — a **measurement gap**, not a floor
violation. The authenticated call returns `substrate_state` and an `actor_verified` flag that tells
you the probe actually bound. Never report a failed control from an anonymous probe.

## 4. Read the schema before calling

Argument names are per-verb and not guessable. Pull `tools/list` (or the client's tool schema)
first and pass only declared parameters. Hand-passing plausible-but-undeclared names yields a
pydantic `unexpected_keyword_argument` error that reads like a broken tool but is caller error.

## 5. Fleet version matrix

Tabulate one row per endpoint: port, service name, and the version returned by its **own**
initialize. Before naming any member as the outlier:

- confirm step 2 (bogus-version control) for each;
- confirm each suspect config entry's **target** matches the endpoint you are blaming.

The finding is the spread plus each member's negotiation mode — not "server X is broken".
