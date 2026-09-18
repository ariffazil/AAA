# Claim gate — verifying named-entity claims before they reach a human

Use before any statement carrying a person's or an institution's name leaves the building: an
outbound message, an article, a brief, a letter signed by the principal.

## The rule the gate encodes

A claim about a **named** institution or person may be published as observed only with an external
source, a retrieval timestamp, and a contradiction check against a **second** external source. A
single well-argued source is still a single source. Own-domain pages and federation-internal URIs do
not witness a claim about themselves.

Separately: claims about a person's **competence, character, motive, trait, behaviour or performance**
are rejected outright, however well sourced. Score structures, never personalities. This is not a
politeness rule — it is the reason an argument about a person survives contact with an audit.

## WEALTH MCP invocation

Tool: `capital_claims`. Any single `HOLD` or `REJECT` blocks the whole batch.

```json
{"session_id": "sess-...", "actor_id": "...", "trace_id": "...",
 "claims": [
   {"claim_text": "...", "category": "career_record",
    "about_entities": [{"name": "...", "type": "institution"}],
    "source_uri": "https://external.example/a",
    "retrieved_at": "2026-01-01T00:00:00Z",
    "contradiction_check": {"status": "CHECKED", "second_source_uri": "https://external.example/b"}}
 ]}
```

Three traps, all of which produce a misleading result rather than an error:

1. **`session_id` is required.** Omit it and every WEALTH tool returns `VOID` / `SESSION_REQUIRED`
   while still looking like a tool that ran.
2. **The keys are `claim_text` and `about_entities`.** Pass a claim under any other key and
   `claim_text` comes back empty, the claim scores `NON_ENTITY` ("no named entities — citation not
   required") and **passes silently** — a batch of malformed claims reports a clean `PASS`. Always
   re-read `verdict_counts` and each claim's echoed `claim_text`; if the echo is blank, the gate never
   saw your text.
3. **Entity `type` decides the person rule.** It fires only when `type == "person"` AND `category` is
   in {`trait`, `behavior`, `character`, `competence`, `performance`, `motive`}.

`HOLD` reasons name the exact gap: `missing_citation`, `self_sourced`, `missing_retrieval_timestamp`,
`contradiction_unchecked`, `invalid_second_source`.

## When the MCP wrapper rejects the call

The deferred-tool schema can be looser than the live server. If argument validation refuses the call,
go to the server directly over JSON-RPC — handshake, capture the session header, then reuse it, and
put the body in a file so nested JSON survives the shell:

```bash
curl -sD - -o /dev/null -X POST http://127.0.0.1:<port>/mcp \
  -H 'content-type: application/json' -H 'accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"hermes","version":"1"}}}' \
  | grep -i mcp-session-id

# then {"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"capital_claims","arguments":{...}}}
# with -H "Mcp-Session-Id: <sid>" and --data-binary @payload.json
```

The payload nests as `result.content[0].text`, itself a JSON string — parse twice. Read the port from
the organ's health endpoint rather than assuming it. Repeated malformed calls trip a short server-side
pause; fix the arguments instead of resending the same shape.

## Non-gate outputs are not clearances

- A scenario engine with no loaded data for its seed case returns `INSUFFICIENT_EVIDENCE` with an empty
  result. That is a coverage gap, not zero risk — report it as a gap.
- A judge-handoff envelope can return `VOID` for a shape it does not accept. `VOID` is not approval.
- `witness` reports `human` / `ai` / `earth`. An incomplete witness set means the verdict is not
  tri-witnessed, however confident the numbers look.

## When no gate is available

Fall back to the same three questions by hand, and say which one you could not answer: does an
external source exist, was it retrieved at a stated time, and did a second source disagree or agree.
Record the answer next to the claim. A claim you cannot source is stated as unsourced — never dropped
silently, and never upgraded by repetition.
