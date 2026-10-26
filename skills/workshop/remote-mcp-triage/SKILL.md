---
name: remote-mcp-triage
description: Probe a pasted third-party MCP live before recommending.
---

# Remote MCP Triage

A pasted `https://.../mcp` link is a **claim**, not a capability. Characterise the
server with four live calls before writing a single sentence about it. Never
describe a hosted MCP from its landing page, its marketing copy, or its README.

## Procedure

1. **POST to the endpoint directly — do not install a client first.**
   Remote Streamable-HTTP MCP servers answer plain JSON-RPC over POST. A stdlib
   probe takes seconds and tells you more than any directory listing. Use
   `scripts/probe_mcp_http.py` (initialize + `tools/list`, optional `--call`).
   Only reach for `mcporter`/`hermes mcp add` once the server is known-good and
   the user actually wants it wired in.

2. **Read the `instructions` field from `initialize`.**
   Well-built servers put their own semantics there — what each score means,
   what the data does *not* prove, and which tool to prefer for a natural
   language question. That text is the server author telling you how to
   represent them honestly; quote its limits, do not invent better ones.

3. **Take one number that only exists inside the server.**
   Corpus size, record count, last-updated date — pull it from a stats/summary
   tool and put it in the answer. It is the receipt that you actually read the
   data and not the promo page.

4. **Spot-check one real query in the domain you will discuss.**
   A server can enumerate 16 tools and return nothing useful. One known query
   proves the lane works end to end before you promise it to the user.

5. **Report in three beats:** what the server is FOR (2-3 sentences, no tool
   inventory), the one load-bearing structural fact about it, and the limits
   that change how it should be used. Tool lists, transport details and version
   strings are for a system audit, not for a human asking "apa benda ni".

## Pitfalls

- **Parse SSE before `json.loads`.** Responses commonly arrive as
  `event: message\ndata: {...}`. Take the last line starting with `data: `.
  Loading the raw body raises a JSON error that looks like a dead server.
- **An error is not an empty result.** A `-32602 output validation error` on a
  search usually means the query did not match the server's corpus language or
  argument shape — not that nothing exists. Translate the query and retry once
  before reporting "tak jumpa". Reporting an error class as absence is a
  fabrication of a negative.
- **Send a browser User-Agent.** Some hosts sit behind Cloudflare and 403 the
  default `Python-urllib/x.y` agent. A 403 with a clean curl is a bot wall, not
  a dead endpoint — retry with a normal UA before concluding anything.
- **`Mcp-Session-Id` is optional on stateless servers.** If the response carries
  the header, echo it on later calls; if not, keep going — absence is not a bug.
- **"Page exists" ≠ "content is live".** Listing and contributor pages routinely
  show a record that is still pending licence review, unpublished, or
  uninstallable. Check for a status line before telling the user their work is
  in the world. Distinguish *profile live* from *content usable*.
- **Relay the server's own disclaimer with its number.** Many scoring or
  evidence servers state that a high score means "much studied", not "safe" or
  "effective". A number quoted without that caveat silently becomes an
  endorsement the server never gave.
- **Do not answer "kita dah ada semua ni kan" from vibes.** When the principal
  asks whether the federation already covers a capability, probe the local
  side (skills, organs, exported artifacts) and answer in three buckets: what
  we have, what only this server has, and what the delta actually costs.
  "Sebahagian saja" with the split named beats either yes or no.

## Delivery

- To F13: prose, one concrete number, and the delta that matters — not a
  feature list.
- To a non-technical friend in the SADO lane: one analogy for the mechanism,
  one sentence on what it is used for, one boundary. Plain BM, no jargon, no
  transport vocabulary.
- If the server is already reachable without install or payment, say so plainly
  and propose using it as an outside reference rather than rebuilding it.

## Support files

- `scripts/probe_mcp_http.py` — stdlib prober: initialize, tools/list, single tool call.
