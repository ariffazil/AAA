# Public-Surface Probes — does the advertised thing exist, and does it enforce?

Use when a claim, report, or review is about what an **outsider** can reach: a registry entry, a
discovery document, a remote endpoint, a trust page, a proof suite, a quickstart command.

The question is never "is it in the repo". It is: **can an outsider with no credentials reach it,
and does it behave the way the claim says** — including the claim "unauthorized actors are refused".

## Order of operations

1. Enumerate every public surface the document names or silently assumes.
2. Reach each one **unauthenticated** and read its *content*, never the status code alone.
3. Compare counts and names **across** surfaces before comparing prose.
4. Only then weigh the findings.

`200` on a rendered page, `301`, and a working protocol endpoint are three different states. Never
infer a live endpoint from a page that loads, and never score a route dead from one host — check the
sibling hosts the record itself advertises.

## 1. Registry / discovery records

```bash
curl -s "<registry-api>/servers?search=<name>"   # discovery: what exists at all
```

Per record, tabulate `name`, `version`, `repository.url`, `packages[]`, `remotes[]`,
`status.isLatest`. The defects worth finding are **cross-record**, not per-record:

- N records / M distinct names / K hosts for one product ⇒ an outsider cannot tell which is live.
- A namespace that does not match the repository it points at ⇒ provenance split.
- A remote that 404s/301s, or never answers a protocol call ⇒ the record advertises a dead connect path.
- A description naming a capability count that disagrees with the manifest, the docs, or the served
  schema ⇒ three public numbers, one product. In a governance or trust product this is the most
  expensive defect available, and it is invisible to anyone reading a single surface.

Namespace verification: `GET https://<domain>/.well-known/mcp-registry-auth` — absent (404) means no
**domain-verified** namespace, i.e. publishing is bound to whatever account namespace was used rather
than the product's own domain.

## 2. Is the advertised remote actually a protocol endpoint?

The check is a POST `initialize`, not a GET of the URL:

```bash
curl -s -X POST "<remote-url>" \
  -H 'content-type: application/json' -H 'accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"<ver>","capabilities":{},"clientInfo":{"name":"probe","version":"1"}}}'
```

Expect `result.protocolVersion` echoed. `405`/`404` ⇒ the path is not a protocol endpoint (a JSON-RPC
web route can legitimately 405 a GET while its `/mcp` sibling works — probe the exact advertised URL).
An unauthenticated `tools/list` immediately after shows what a stranger sees before any identity bind:
compare the tool **count and names** against the manifest, the registry description, and the docs.

## 3. Discovery documents — read fields, not status codes

`.well-known/agent-card.json` (A2A), `.well-known/did.json`, `server.json`, `llms.txt`,
`security.txt`. A two-field JSON stub answering `200` is a **stub**, not a surface: grade it by field
richness and by whether the identifiers inside it resolve. Record which exist and which do not — the
population reached belongs in the verdict, and so does the list you did not reach.

## 4. Identity enforcement — the negative probe and its control

Two calls, same endpoint, no credentials:

- **(a) novel actor id** → expect a bounded band, not authority (`actor_verified: false`, an
  observe-only band, a session that can read but not mutate).
- **(b) the principal's display name as a plain string** → expect refusal, ideally named.

Read the structured fields, not the prose: `verdict`, `actor_verified`,
`authority_band`/`authority_level`, `session_id`, plus `trace_id` and `call_hash`. A `VOID` carrying a
named `reason_code` (and the laws it cites) *is* the mechanism; a bare `HOLD` may be an unrelated gate,
so **grep the named reason code in the source** and quote the file that holds it before citing the
behaviour as designed enforcement.

**Always run the positive control.** Refusal-only evidence is read by a stranger as "nothing works
here". Pair the refused name with the signed-principal path, or state explicitly that the accept path
was not exercised and is therefore `UNVERIFIED`. If that path has a known gap (a proof the caller must
supply and the wiring does not yet), say so in the same breath — an unqualified "capability ≠
authority" demo is a demo of a wall with no door.

## 5. Reconcile the public numbers

Grep every surface stating a count for the same object — served schema, discovery doc, registry
description, docs, README, website hero — and put them in one column. Publishing one reconciled number
is a smaller job than any build a review proposed, and it is the first thing an evaluator checks.

## 6. The documented first command is a surface too

Run the **exact command string** printed in the quickstart, from a clean environment, before quoting
any install instruction as working. Docs drift from shipped package layout, and that string is where an
outside evaluator either succeeds or stops reading. A doc command that cannot resolve is a funnel
defect with its own severity: the engine underneath may be perfectly fine, which is exactly why
"the engine works" and "the quickstart works" are two separate verdicts.

## Rules

- **Unauthenticated and read-only, always** (observe/light modes; never a mutating verb). Never probe
  with credentials you do not own, and never probe a system you have no standing to test.
- A probe result quoted **without its `trace_id`/`call_hash`** is an event narrative, not a receipt.
- **Absence needs the same warrant as presence**: state host and path actually reached, then list the
  surfaces not reached. "No discovery doc" over three checked paths is a measurement; over one guess
  it is not.
- Expect the remedy to be **publish / prune / reconcile** — same-day work — because this class of defect
  is wiring and consistency, not capability. Say so: a reviewer will have priced it as a build.
