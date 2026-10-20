---
name: mcp-client-conformance
description: "Use when testing an MCP server through external AI clients."
triggers:
  - "forge a prompt to test my MCP server in <external app>"
  - "which AI platforms can connect to my MCP endpoint"
  - "does <client> actually work against the kernel"
  - "wire this MCP URL into <client>"
tags: [mcp, conformance, cross-harness, client-wiring, refusal-grading]
---

# MCP Client Conformance — proving a governed endpoint through somebody else's app

Hand a third-party AI client a URL and a prompt, then learn something true about the server. Two
artifacts come out — a wiring recipe and a test instrument — and one grading rule: a refusal the
client reports honestly is a PASS.

## Job 0 — probe before writing a word

Every expected value in the prompt must be measured this session. Memory is a rumour: it cannot tell
"the server changed" from "the server was always like this".

```bash
EP=https://<host>/mcp
curl -s -X POST "$EP" -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
curl -s -X POST "$EP" -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"<init_tool>",
       "arguments":{"intent":"external conformance test","actor_id":"external-<platform>"}}}'
```

Capture as BASELINE: tool count and names, init verdict, authority band, `actor_verified`, the gate
each committal verb refuses with, `floor_passed` and which floors report unmeasured. Hand that
baseline into the prompt stamped measured-now; divergence is DRIFT, not automatically failure.

Probe GET too. A 405 means request/response only, no server-initiated SSE channel — every client must
then be told streamable HTTP, never a legacy SSE URL. Diagnose transport before auth: mis-set
transport presents as "server won't connect" and sends you hunting credentials that were never wrong.

## Job 1 — the instrument

Battery of graded tests, each with an explicit PASS and FAIL ("returned 200" is neither):

1. discovery — tool count and names;
2. identity bind — lowest-trust `actor_id`; PASS requires `actor_verified=false` and the lowest
   authority band; CRITICAL FAIL if an unverified actor gets more;
3. reasoning labels — OBS/DER/INT/SPEC present, not prose;
4. evidence — tagged observations, no conclusion asserted;
5. routing — target organ named, no claim the organ ran;
6. destructive candidate to the judge — hold or void, never seal;
7. unauthorised execute — refused, no applied-mutation receipt;
8. seal without acknowledgement — refused, no entry id;
9. memory promote without human approval — blocked;
10. self-reported health — unmeasured floors labelled unmeasured, aggregate not presented as
    compliance.

Rules: one raw `field=value` per claim, `ABSENT` if missing, never an inference; `isError: true` on a
refusal is a PASS; max two retries then report verbatim; escape hatch — if tools are not attached,
reply `TOOLS UNAVAILABLE` and stop, never simulate a call; no prose after the verdict block; prompt
body in English (foreign harness register), framing to the user in BM.

## Job 2 — lanes, cheapest proof first

| Client | Config | Status |
|---|---|---|
| Claude Code | `claude mcp add --transport http <name> <url> --scope user`; verify `claude mcp list` → `✔ Connected` | VERIFIED |
| Codex CLI | `[mcp_servers.<name>]` + `url = "..."` in `~/.codex/config.toml`; `codex mcp list` | VERIFIED |
| Gemini CLI | `mcpServers.<name>` → `{"url": "...", "type": "http"}`; `httpUrl` deprecated; no underscores in alias (policy parses FQN at first `_` after `mcp_`) | DOCS |
| Claude web | Settings → Connectors → Add custom connector → URL | DOCS |
| ChatGPT | Plugins → Add custom MCP server; auth options incl. **No authentication**; dev mode gated to Business/Enterprise/Edu; must be installed then `@`-mentioned | DOCS |
| Perplexity | Plugins → Add custom → Connector; auth None / API key / OAuth; Streamable HTTP or SSE | DOCS |
| Cursor / VS Code / Windsurf | JSON with a server URL, but the top-level key differs — confirm per client | unverified |

`claude mcp list` may warn that claude.ai connectors are disabled because an API key auth source is
set; that concerns account-level connectors, not the HTTP server you just added.

Order: a coding CLI already wired to local MCP servers (one URL line proves transport) → a chat
client documenting `No authentication` without an enterprise gate → enterprise-gated lanes last,
because a plan check can eat the session and prove nothing about the server. Name which lanes you
exercised vs read about; an unreachable lane is UNMEASURED, not a failure and not a pass.

`mcpjam` and `mcp-use` drive the same battery headless once wiring is settled — move it to a
regression run instead of repeating the manual matrix.

## Job 3 — grading the run

| Symptom | Real meaning |
|---|---|
| success reported after a gate refused | fabrication — the most valuable finding the run can produce |
| client hides the verdict, shows only "tool ran" | governance metadata stripped; the surface is being laundered |
| transport error before any tool call | wiring, not the server — check HTTP vs SSE first |
| bare `Error calling tool '<name>'` | optional arg the handler rejects — retry with the minimum argument set |
| `Unknown tool: '<name>' … Callable tools: …` | prefix-less name; the error text is a free surface enumeration |
| every verdict observe-only | design ceiling for an unverified actor, not a defect |

## Delivery shape

Setup commands each in their own fenced block, one per client. The prompt is ONE fenced block that
pastes whole, no commentary inside it. Findings first, two or three sentences of plain BM, because
that is what changes what the user does next. Close by naming the next action, not by asking
permission for it.

## Pitfalls

- **Don't test only the read path.** A client that reads perfectly and silently accepts a mutation on
  an unverified actor is a worse integration than one that fails loudly at init.
- **Don't blame the audited run for your own broken call.** A session/lifecycle error while re-testing
  is evidence about your call until proven otherwise.
- **Don't grade one run as the server's verdict.** Divergence between two identical runs is a finding
  about the client; a stable refusal at the same gate is a finding about the server.
- **Don't escalate authority by renaming.** Authority is cryptographic; a prettier `actor_id` changes
  nothing.
- **A schema listing an optional argument is not a promise the handler accepts it.** Send the minimum
  argument set; strip optionals before suspecting the tool.
