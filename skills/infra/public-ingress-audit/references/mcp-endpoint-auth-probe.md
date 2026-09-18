# Probing a public MCP endpoint's auth posture

Goal: establish whether an internet-reachable MCP surface requires credentials — **without
credentials, and without invoking a single tool.** This is read-only reconnaissance.

## Step 1 — initialize, sending no credential

```bash
curl -s -D /tmp/h.txt -o /tmp/i.txt --max-time 20 \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"audit","version":"1"}}}' \
  https://<host>/<path>/mcp
head -1 /tmp/h.txt; head -c 300 /tmp/i.txt
```

If it returns a `result` carrying `serverInfo` **plus** an `mcp-session-id` response
header, the surface accepted an unauthenticated client and issued a session. That is the
finding — write it down before doing anything else.

## Step 2 — enumerate, still sending no credential

```bash
curl -s --max-time 25 -D /tmp/h2.txt -o /tmp/t.json \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H 'mcp-session-id: <id>' \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' \
  https://<host>/<path>/mcp
```

The body is SSE-framed, so parse the `data:` line rather than JSON-decoding the whole file:

```python
import json, re, collections
raw = open('/tmp/t.json').read()
d = json.loads(re.search(r'data: (\{.*\})', raw, re.S).group(1))
tools = d['result']['tools']
print(len(tools), dict(collections.Counter(t['name'].split('_')[0] for t in tools)))
```

Group by name prefix to see which organ each tool belongs to, then flag the risk class:
`shell|exec|filesystem|git|postgres|cron|seal|deploy|write`. Report the **count** of
risk-class tools and the owning organ — not the full list.

## Interpreting responses

| Response | Meaning |
|---|---|
| `result` with `serverInfo` + session header | unauthenticated; the client was accepted |
| `401` / `403` | auth-gated — endpoint is up, and this is the good outcome |
| `400 Missing session ID` on a bare `GET` | transport wants a POST `initialize` first — **not** an auth failure; re-probe with POST |
| `404` on a sibling path | that path is unrouted; says nothing about the MCP path itself |

Do not read a transport error as a security control. A gateway answering `400` to a
malformed request is answering, which is a different claim from "it is gated".

## Pitfalls

- **Parsing the session header.** Grepping the header block case-insensitively for
  `session-id` matches the `access-control-allow-headers` line, which lists
  `Mcp-Session-Id` among the allowed *request* headers — you capture the CORS list, not
  the value. Anchor on the exact lowercase response header:
  `grep -i '^mcp-session-id:' /tmp/h.txt | tr -d '\r' | awk '{print $2}'`.
- **SSE framing.** `tools/list` returns `event: message` + `data: {...}`, not bare JSON.
  A direct `json.load` on the response file fails with an unhelpful parse error.
- **Never call a tool to test a gate.** `tools/list` is observation; invoking
  `*_execute`, `*_shell`, `*_filesystem`, `*_git*`, or `*_postgres` is an irreversible
  production side effect. If you cannot prove a gate from read-only surfaces, report
  UNKNOWN — an untested gate is not a closed gate.
- **Note whether the surface sets `Access-Control-Allow-Origin: *`.** That lets any web
  origin drive the endpoint from a victim's browser, and it is reported separately from
  missing auth.
- **Check the vhost logs before claiming no one has called it.** Many proxy blocks carry
  no `log` directive, which makes the caller history unrecoverable. "No log entries" is
  cannot-witness, never all-clear.
