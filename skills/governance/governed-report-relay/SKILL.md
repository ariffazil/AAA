---
name: governed-report-relay
description: Use when agents must report without making a human the bus.
---

# Governed report relay — remove the human from the agents' loop

## When to Use

- An agent fleet reports straight into a human's chat and he has become the bus.
- Someone asks to "complete the loop", "get the human out of the middle", or
  "stop pinging me for everything".
- A chat-surface agent (ChatGPT / Claude web / Grok / Perplexity) needs to reach
  a human but cannot make raw HTTP calls.
- You are auditing whether a notification path has triage or just volume.

The failure mode: every agent reports straight to the human's chat, so the
human becomes a message bus, a copy-paste wire, and a triage clerk between
machines. The fix is not "fewer agents" — it is **three surfaces with hard
separation**, so agents talk to agents by default and the human is interrupted
only when interruption is warranted.

## Architecture that works

```
/handoff    agent -> agent. Silently filed to inbox/<agent>.jsonl. NEVER
            touches the human. The default for findings, fixes, retests.
/report     agent -> human. Triaged by severity.
/mcp        MCP server exposing ONE tool (report_to_arif) so chat-surface
            agents (ChatGPT, Claude web, Grok, Perplexity) that cannot make
            raw HTTP calls can still report.
```

## The authority rule that makes triage honest

Severity is not a claim the sender gets to make — it is granted by a key.

| severity | key holder | keyless |
|---|---|---|
| P0/P1 | delivered immediately | **capped to P2, queued** |
| P2/P3 | queued into digest | queued into digest |

Without this, any anonymous caller can ring the human's phone by writing
`"severity":"P0"`. Cap first, then deliver.

## Digest, not stream

P2/P3 accumulate in `pending.jsonl`; a timer flushes them as **one** message
grouped by severity then source. Rules that matter:

- clear the queue only AFTER Telegram confirms, so a failed send retries instead
  of silently dropping the batch
- archive every flushed row — the witness trail must survive the digest
- cap items per digest and trim bodies; a digest longer than the stream it
  replaced solves nothing

## Pitfalls learned the hard way

- **Do not add the reporting tool to the constitutional kernel.** A kernel that
  advertises 8 canonical verbs and then grows a 9th tool has broken its own
  contract, and conformance tests catch it. Run the relay as its own MCP server
  on a subpath: relay owns transport, kernel owns governance.
- **Keyless MCP callers cannot set custom headers** on most connectors, so the
  MCP surface must assume unverified and cap severity server-side.
- **Never let a relay failure swallow a message.** Fall back to the direct send
  path and record `relay_error` in the response — a broken triage layer must
  degrade to noise, not to silence.
- **Rate limit per source AND per lane**, plus per client address for keyless
  callers. Public MCP endpoints attract directory crawlers; expect thousands of
  requests a day from bots that never read the response.
- **stdlib only** for the relay. A notification path that dies because a venv
  drifted is worse than no notification path.
- Handle both `/path` and `/prefix/path` in the router — reverse proxies mount
  services under a prefix.

## Verification checklist (run all, don't assume)

1. Negative auth: no key → 401, bad key → 401.
2. Missing required field → 400 naming the field.
3. Agent lane → returns id, `escalated_to_human: false`, nothing in the chat.
4. Keyless claims P0 → response shows `severity_used: P2`, `queued: true`.
5. Key holder P1 → `channel: telegram`, real message id.
6. Digest dry-run prints what would be sent; a real flush clears the queue and
   writes the archive.
7. Restart the service and re-check `/health` — persistence, not just liveness.

## Reporting to the human, once allowed to

Verdict first, evidence second, caveats last. Every claim carries its receipt
(field path, value, or command output). Unmeasured is written as UNMEASURED,
never softened into a guess. One message per finding — do not stream updates.

See `references/deployment.md` for the systemd, proxy, and secrets recipe.
