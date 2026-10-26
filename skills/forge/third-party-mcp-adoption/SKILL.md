---
name: third-party-mcp-adoption
description: "Use when adopting an outside MCP server."
version: 1.0.0
tags: [mcp, probe, adoption, integration, reference-server]
risk_tier: low
autonomy_tier: T1
---

# Third-Party MCP Adoption

Probe an outside MCP server on the wire, decide where it belongs, and hand it to the human in
their own language. A link is marketing; the wire is truth.

## USE WHEN

- A URL to an MCP server or MCP directory listing lands in chat with no instructions.
- Deciding whether to wire an external server, borrow its data, or rebuild the capability.
- Auditing what a hosted server really exposes before trusting its listing.

## 1. Read the listing, without getting bot-walled

Directories (`mcpservers.org`, registry mirrors) commonly sit behind a Cloudflare bot check and
return a challenge page to headless browsers. Do not conclude the listing is unreachable — read
it through the search lane instead: `exa web_search_exa` returns page highlights that carry the
endpoint URL, the install command, the registry name and the publisher's own description.

The listing gives you the endpoint and the pitch. It is **not** evidence of the surface — see §2.

## 2. Probe the live wire

Sequence, in order:

1. `initialize` POST with `Accept: application/json, text/event-stream` and an explicit
   browser-like `User-Agent`. Capture `Mcp-Session-Id` from the response headers and echo it on
   later calls when the server issued one.
2. Parse **SSE**, not bare JSON: the body is `event: message` lines followed by `data: {...}`.
   Take only lines starting `data: ` and `json.loads` each — error frames arrive the same way.
3. Enumerate `tools/list`, `resources/list`, `prompts/list`, `resources/templates/list`.
4. Call one cheap real tool. A listing proves a schema exists, not that data comes back.

Re-runnable probe (stdlib only, no install):

```python
import json, urllib.request, urllib.error
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

class Probe:
    def __init__(self, url): self.url, self.sid, self.n = url, None, 0
    def rpc(self, method, params=None):
        self.n += 1
        body = {"jsonrpc": "2.0", "id": self.n, "method": method}
        if params is not None: body["params"] = params
        req = urllib.request.Request(self.url, data=json.dumps(body).encode(), method="POST")
        for k, v in {"Content-Type": "application/json",
                     "Accept": "application/json, text/event-stream",
                     "User-Agent": UA}.items(): req.add_header(k, v)
        if self.sid: req.add_header("Mcp-Session-Id", self.sid)
        try:
            r = urllib.request.urlopen(req, timeout=45)
        except urllib.error.HTTPError as e:
            return {"_http_error": e.code}
        s = r.headers.get("Mcp-Session-Id")
        if s: self.sid = s
        raw = r.read().decode(errors="replace")
        for f in ([ln[6:] for ln in raw.splitlines() if ln.startswith("data: ")] or [raw]):
            try: doc = json.loads(f)
            except json.JSONDecodeError: continue
            return doc.get("result") or {"_rpc_error": doc.get("error")}

p = Probe(URL)
p.rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                     "clientInfo": {"name": "probe", "version": "1"}})
for m, k in (("tools/list", "tools"), ("resources/list", "resources"),
             ("prompts/list", "prompts"), ("resources/templates/list", "resourceTemplates")):
    res = p.rpc(m) or {}
    print(m, len(res.get(k) or []), res.get("_rpc_error", ""))
```

Report: live version, per-surface counts, one real answer, and the honest gap.

## 3. Judge the surface, not the pitch

- **Directory listings lag.** A directory advertised 8 tools at one version while the live
  handshake returned 16 at a newer one. Quote the live handshake for counts, version and
  capabilities; quote the directory only for discovery.
- **No prompt layer is a finding, not a failure.** `prompts/list` answering `-32601 Method not
  found` or an empty `templates` list means the server ships tools and leaves orchestration to
  the caller. Say so — it is usually the opening for what you build on top.
- **Read the tool schemas before the first call.** Argument names come from the live
  `inputSchema`, never from prose. A tool described as "compare two to four topics" took `ids`,
  not `topics`.
- **Read the error text; it often carries the fix.** An unknown id returned
  "no topic with id X — similar: Y", and Y was the correct id.
- **A zero-hit search can surface as a tool error**: a tool with a declared `outputSchema`
  returns `-32602 … has an output schema but no structured content was provided` when nothing
  matched. That is an empty result, not a dead endpoint — retry with another term.
- **Monolingual corpora need the corpus language.** A symptom-style query in the user's own
  language returns zero or nonsense against an index built in another language. Reduce to short
  nouns, translate to the corpus language, and translate back only the fields you report.
- **A 403 from a Cloudflare-fronted host is usually User-Agent filtering**, not downtime — a
  default library UA gets blocked where a browser-shaped request succeeds. Set a real UA and
  retry before telling the human the server is down.

## 4. Decide the home before writing any code

Three different things get confused here; keep them apart.

- **State** — what a substrate IS right now (vitals, readiness, machine health). Goes to the
  organ that mirrors that substrate (WELL, M-WELL), whose resources load at session start.
- **Evidence** — an outside body of knowledge with sources and dates. Its own config entry as a
  reference server, or a small service beside the project surface. Never a substrate organ.
- **Workflow** — what a practitioner does with that evidence. That person's own surface, carrying
  their judgment, not the organ's.

Never annex a large external corpus into a substrate organ. Those resources are ingested at
session start in every lane: the cost lands on every session, the organ splits into two
identities, and other humans' questions get routed through the principal's live state. Keep the
boundary even when hosting is cheap — especially then.

## 5. Reuse the evidence, build the judgment

When an outside party already publishes a scored, sourced catalogue, wire it as a reference
instead of re-deriving the data. What cannot be outsourced is the part that needs local
reality: regional legality, real prices, what actually happened to a real person. Build only
that layer — one structured file beats a sixteen-tool server.

Do not copy the outside server's tool taxonomy. Its names follow its URL structure (`topics`,
`pages`, `episodes`); yours must follow the questions the human actually asks.

## 6. Deliver honestly, in the human's language

State what is real: counts, version, what it refuses (dosing, advice, prices). Name the gaps in
plain words — "it is German first, Malay queries fail, and it takes affiliate money from the
shops it rates" is worth more than a feature list. Never translate a score into a
recommendation it did not make: "high score" means *well studied*, not *good*.
