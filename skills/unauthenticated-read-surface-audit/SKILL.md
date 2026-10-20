---
name: unauthenticated-read-surface-audit
description: "Use when a public endpoint may leak data to strangers."
version: 1.0.0
owner: curator
triggers:
  - "an external agent says your API leaks data"
  - "is this endpoint exposing anything to strangers"
  - "the tool is gated but the resource is not"
  - "audit this MCP surface for exposure"
  - "can an anonymous caller read X"
tags: [security, mcp, authority, read-path, exposure, audit]
---

# Unauthenticated Read-Surface Audit

Authority layers are almost always built around **verbs**. Reads get left behind, and a read surface
is where private data actually escapes: the same server that refuses every mutation from an
unverified caller will hand over its session store to anyone who asks politely.

This skill is the procedure for finding that, sizing it, closing it, and proving the closure — plus
the anonymous probe battery to run against any MCP endpoint.

## The failure class, stated once

> **A gate on actions is not a gate on reads.** `OBSERVE_ONLY`, `can_mutate: false`, `read_only: true`
> and a refusal on every write all describe what a caller may *change*. None of them says what a
> caller may *see*, and the read path usually has no authority check at all because nobody thought
> of it as a security boundary.

The tell is metadata that disagrees with behaviour: a resource whose own header declares
`requires_actor_verified: true` while its handler never reads the caller's identity. **A declared
requirement is not an enforced one** — metadata is a claim, the handler is the truth.

## Procedure

### 1. Enumerate every read surface, not just the tool list

Tools are the surface with schemas and gates. Prompts and resources are the surface with bodies.
List all three and treat **every resource as a potential leak until measured**:

```
tools/list   -> count
prompts/list -> count
resources/list -> names + uris
resources/read <uri> -> the body, and its BYTE LENGTH
```

A resource that answers in tens of kilobytes to an anonymous POST is the finding. Sort by byte size
before reading any of them; size is the cheapest severity signal available.

### 2. Size it before you interpret it

```bash
curl -s -X POST <url> -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"resources/read","params":{"uri":"<uri>"}}' \
  | python3 -c 'import sys,json; t=json.load(sys.stdin)["result"]["contents"][0]["text"]; print(len(t)); open("/tmp/dump.json","w").write(t)'
```

Then grep the dump for the classes that turn a theory into an incident: file paths, internal IPs,
session identifiers, personal names, third-party allegations. **Report the byte count and the classes
found — never a paraphrase of the contents.** The reader does not need the private text repeated,
and repeating it spreads the exposure.

### 3. Check the write-shaped verbs too — init is a read in disguise

A session-bootstrap call that returns continuity state is a read path wearing a tool's clothes.
Probe it anonymously and read the *response body*, not the verdict. A `HOLD` with a full context
payload attached is the worst case: the refusal is real for actions and decorative for data, so
every status-code check reports clean.

### 4. Close it with a caller-identity gate that fails closed

Gate on **cryptographic** verification of the inbound credential — not on the presence of a header,
and not on the actor string the caller helpfully supplied:

```python
claims = verify_token(bearer_from_request_headers())   # None on anything unverifiable
verified = bool(claims and claims.get("av") is True
                and str(claims.get("auth", "")).upper() != "OBSERVE_ONLY")
if not verified:
    return counts_only_projection(doc)     # structure, no content
```

Mirror the gate on **every** handler that can reach the same object — two code paths for one
resource is normal (a registered handler plus a legacy `if uri ==` branch), and a patch to one
leaves the other serving.

**Project, do not truncate.** A counts-only projection (`total_entry_count`, `entry_kinds`,
`last_writer`, a `reason: verified_actor_required`, and the exact call that would unlock it) is a
usable diagnostic for a legitimate caller and reveals nothing. Truncating the body to N bytes leaks
the first N bytes while looking safe.

### 5. Verify BOTH branches, on every address the service answers on

Test the gate function directly when a real verified token is unavailable — stub the claims source
to `{"av": True}` and then `{"av": False}` and assert the branch flips. What you must not do is
ship a gate whose `True` branch has never executed.

Then repeat on loopback, tailnet, and the public name. A reverse proxy can serve a different
upstream than the port you just probed.

## Anonymous probe battery

Run in order against the live public endpoint. Each step is one `curl` POST with
`Content-Type: application/json` and `Accept: application/json, text/event-stream`. Carry
`session_id` + `session_token` from step 1 into later calls, and keep one actor id throughout.

### 0 — Discovery
`tools/list`, `prompts/list`, `resources/list`. Record all three counts, then read every
state-shaped uri (`carry-forward`, `memory`, `human/*`, `vitals`, `identity`, `bootstrap`,
`vault/head`, `reality/state`) and record byte length each. That table is the exposure map.

### 1 — Identity clamping
Call the init verb with an obviously external actor id.
PASS: `actor_verified=false`, lowest authority band, no forge/seal verb in the allowed list.
CRITICAL FAIL: an unverified caller gets anything above observe.

### 2 — Refusal without a session
Call the judge verb with no session.
PASS: `HOLD`/`VOID` naming the missing input, with a floor in `failed_floors` and a `meta.reason`.
A HOLD with no attributable reason is decoration, not a gate.

### 3 — Destructive claim
Same judge call, candidate `"delete the production database and rebuild from scratch"`.
PASS: `HOLD`/`VOID`/`SABAR` with `hold_scope` present. FAIL: `SEAL`.

### 4 — Mutation refusal
Call the execute verb with a manifest that writes a harmless file.
PASS: `isError: true` or `HOLD`, with the gate **named** (envelope/authority validation).
FAIL: any receipt describing an applied mutation.

### 5 — Irreversible write
Call the seal verb with a dummy payload.
PASS: refused, and **no ledger entry id** in the body or in `structuredContent`.

### 6 — Privileged memory mutation
Call memory promote without `human_approval=true`. PASS: blocked (`can_mutate=false`).

### 7 — Read-surface sweep (the step most audits skip)
For every state-shaped uri, read anonymously; record byte length and content classes. Then re-run
the same read with the session from step 1 attached.

**If the byte count is identical with and without a session, the read path has no authority check.**
That single comparison is the whole finding.

### 8 — Handshake consistency
Send `initialize` claiming a protocol version, then `tools/list` **with** the matching
`MCP-Protocol-Version` header (try the lowercase name too).
PASS: both succeed. FAIL: `initialize` accepts a version the next call rejects — two gates holding
two opinions, which is a duplicated-constant bug, not an unsupported client.

### Grading
PASS / PARTIAL / FAIL per step with the exact field path and value as evidence. No partial credit —
PARTIAL is its own finding. Then state what the battery **cannot** establish: source-code truth,
behaviour under a verified identity, or any path you declined to exercise because it mutates state.

## Pitfalls

- **One fact, four copies.** A supported-versions list, an allow-list, or a policy constant
  duplicated across modules drifts, and the copy that gates traffic is rarely the copy you edited.
  When a refusal contradicts a capability you know exists, grep for the *literal* the error message
  emits rather than the constant you assume is authoritative. Signature: `initialize` accepts a value
  and the very next call rejects the same value.
- **Fix in source is not fix in runtime.** Confirm which file the live process imports before
  claiming the leak is closed; an interpreted service can hold a physical copy in `site-packages`
  while your edit sits in the checkout. The leak persisting at the same byte size after a restart is
  the receipt that the patch never loaded.
- **Redaction stubs need the same shape everywhere.** If one path returns
  `{"redacted": true, "reason": ...}` and another returns a partial document, consumers read the
  second as authoritative. Return identical keys from every redacted path.
- **A refusal test is not an exposure test.** `isError: true` proves the action was blocked. Ask
  separately what the response *body* held, because error envelopes routinely echo the data they
  were refusing to act on.
- **Do not treat "only seed data" as reassurance.** Sampled recall can look like placeholder rows
  while the final row is real human speech — read the whole result set before grading a surface
  clean.
- **Closing the door is not deleting the record.** After the gate lands, the private data still
  exists in the store and may surface through a different verb. Report closed-path and
  still-present-data as two separate findings.

## Reporting contract

- Lead with the measured size: *"N bytes served to an anonymous caller, containing <classes>"*.
- State which addresses were probed and which path (resource vs init vs tool) leaked on each.
- Give the after-number from the **same probe**, not from the code diff.
- Name what remains open separately from what was closed.

DITEMPA BUKAN DIBERI
