---
name: site-traffic-reality
description: "Use when counting site visitors or auditing traffic claims."
version: 1.0.0
owner: Hermes
risk_tier: T1
floor_scope: [F1, F2, F4]
triggers:
  - "how many visitors do we have"
  - "any analytics data"
  - "site traffic numbers"
  - "page views / uniques question"
  - "enable access logging"
  - "is anyone reading my site"
tags: [analytics, access-logs, caddy, cloudflare, observability, evidence]
capability_tier: fed-long-context
ecology_state: WARM
---

# Site Traffic Reality

Answering "how many people visit this site" honestly. The honest answer is often *nobody knows,
and here is why* — which is more useful than a fabricated number and more actionable than silence.

## Procedure

1. **Check whether logging exists at all — never infer traffic from its absence.** A vhost logs
   only if it carries a `log` directive. No directive means **zero history**, not a small one.
   `grep -nE '^\s*log(\s|\{)'` the vhost config, and list `/var/log/caddy/`. Say plainly which
   periods are unmeasured. Do not extrapolate backwards into them.

2. **If a sibling subdomain logs, that log is your only sample of real traffic shape.** It is a
   different surface, so its absolute numbers do not transfer — but its *composition* (machine vs
   human vs self-probe) usually does, and it is worth analysing while you wait for fresh data.

3. **Enable logging when asked, with the standard safety ritual:** backup → edit the one vhost →
   validate → reload in-process (zero downtime) → re-probe every major route and compare status
   codes BEFORE vs AFTER → report a single-command rollback recipe. Never touch `trusted_proxies`
   or security headers as part of a logging change.
   Rotate by size, keep ten files, expire after thirty days — never by a timer that could lose the
   window you are about to analyse:
   ```
   log {
       output file /var/log/caddy/<site>-access.log {
           roll_size 50MiB
           roll_keep 10
           roll_keep_for 720h
       }
       level INFO
       format json
   }
   ```
   `level INFO` is the server default and has no functional effect — keep it to minimise churn
   against whatever a concurrent agent already wrote.

4. **Classify, don't just count.** Buckets that carry signal: `OWN_INFRA` (self-probes — the
   host's own watchers, and requests whose source is the host's own public IP), `BOT`
   (bot/crawl/spider/probe/httpx/curl/wget/headless/scrapy tokens plus MCP and agent-framework
   client strings), `DATACENTER_IP` (known cloud prefixes), `HUMAN_CANDIDATE` (everything left).
   **Disclose the overlaps** — a request can be bot-UA *and* datacenter-IP, and a partition that
   hides that reads as four independent categories when it is not.

5. **Separate scanner traffic explicitly, and count beyond your own pattern list.** Requests for
   credential files, version-control metadata, CMS login paths, path-traversal and
   cloud-metadata SSRF shapes are exploitation attempts on a public host, not visitors. The
   enumeration is never exhaustive — measure outside it too, and state that true scanner volume is
   **higher** than your enumerated count.

6. **Distinguish page-like from asset/API requests** (exclude health endpoints, version endpoints,
   bundled assets and static extensions) or the number is dominated by script chunks loaded once
   per session.

7. **Report the coverage window with every number** — first and last record timestamp. And let a
   fresh log accumulate before interpreting: minutes of traffic containing only your own smoke
   tests will read as silence, and silence misread as signal is its own error.

## What these counts CAN and CANNOT establish

**CAN:** exact request counts per day, per path, per status, per User-Agent over the window; the
machine/human composition; which content is genuinely fetched once probes are stripped out.

**CANNOT: a visitor count.** No cookie, no session id, no authenticated user, no fingerprint —
nothing joins a request to a person, so no arithmetic over these rows yields people. State that
instead of presenting a "visitors" figure. Two traps inflate the raw number:

- **Hits are not people.** One reader loading a page twenty times is twenty requests. Without
  sessions they cannot be folded.
- **User-Agent is trivially spoofable.** Browser-shaped strings with stale version tokens are
  scrapers wearing a costume, and a large slice of page-like requests may carry **no UA at all**.
  A log analyser's "unique visitors" metric is IP+UA+day arithmetic — a tool printing the word does
  not make it a human count.

Where a number cannot be computed, write UNKNOWN. Expect the machine share to dominate — that is a
finding, not a measurement failure, and it is usually the interesting one.

## Behind a tunnel: the real client address

When the origin sits behind an outbound tunnel connector, the connector dials the origin over
**loopback**, so the logged client address is 127.0.0.1 in 100% of records. A standard reverse proxy
rewrites the client address from the forwarded-for header only when the peer address is in its
trusted-proxy list; loopback is not in that list.

Confirm the topology before theorising: check which process listens on the TLS port (only the web
server, no local front), list running containers, and read the tunnel's ingress config to see which
hostnames map to the loopback origin.

- **Prefer the CDN-written client header** where one exists — a visitor cannot forge it.
- **Treat the forwarded-for header as advisory only.** It is client-supplyable; never promote it to
  identity or to a unique-visitor key.
- **Do NOT "fix" this by trusted-listing the loopback address.** That lets anything able to connect
  locally forge the client address. It is a trust-boundary change, not a logging tweak, and it needs
  the owner's explicit decision.

## Historical data lives upstream, and is usually gated

Origin logs cannot recover the past — they did not exist. Retroactive zone-wide numbers exist only
in the CDN's own analytics API. Access is scope-gated; a zone-scoped token with read-only
permissions on zone, settings and DNS typically returns a permission error naming the missing
`analytics.read` scope on every analytics query. Adding that scope is an **account mutation by the
owner** — an F13-class binary. Report the exact missing permission string, stay read-only (no write
verbs, no settings changes, no DNS edits), and never hunt for other credentials.

A CDN-side real-user-monitoring setting can report itself enabled and editable while the beacon is
still unprovisioned. Verify by fetching the beacon endpoint and grepping the served HTML for the
injected script — a setting is not an injection. Moot when the site is served through a static path
that the CDN's automatic injection does not reach.

## Handling credentials while doing this work

When a gate blocks a tool call because a protected path appears literally in its arguments —
including inside a subagent prompt — the fix is to **resolve the file at runtime through a shell
variable and never paste the literal path**. Read the value into an environment variable once, pass
it to the API client from the environment rather than as a visible argument, and never echo, log,
write or report the value or any substring of it. Report only whether a credential was found and
whether it was accepted.

A redaction helper that splits lines on an equals sign will leak any line lacking one — comment
lines are the usual culprit. Print key names and value **lengths**, never values.

## Pitfalls

- **Analysing the log is separate from deploying the analysis.** Keep it read-only: never truncate,
  rotate or delete a log you are reading. If the live log grows during your run, that is the server
  serving traffic, not your script.
- **A "new" log appearing mid-session may not be yours.** On a host with concurrent agents, check
  mtimes and ownership before claiming a file as your output — and check whether someone else is
  mid-edit on the same config before you write to it.
- **Cross-check your analyser against a second tool** and reconcile any delta explicitly. An
  unexplained difference means one of them is wrong; an explained one (a single oversized record a
  parser rejects) is evidence both work.
- **Record-per-line logs with a console prefix often need a normalisation step** before a standard
  analyser accepts them, because the text prefix breaks JSON parsing. Disclose every field you
  synthesise during normalisation.
