---
name: public-ingress-audit
description: "Use when a proxy route change must be audited for exposure."
owner: HERMES (ASI bridge)
risk_tier: T0
floor_scope: [F1, F2, F4, F11, F13]
autonomy_tier: OBSERVE_ONLY
forged_from: unacknowledged proxy ingress change surfaced by a config drift watcher
capability_tier: fed-long-context
ecology_state: WARM
---

# Public Ingress Audit

Resolve a route, vhost, or port change to **upstream identity, auth posture, and blast
radius** — then hand the keep-or-close decision to the sovereign.

USE WHEN: "drift watch fired", "caddy config changed", "vhost mutated", "is this
exposed", "new route added", "who can reach this port", "public endpoint audit",
"should I close this door".

> A reverse-proxy route is a **capability grant**, not a config detail. Editing one
> changes what the open internet can do to your organs. Audit it as an authority
> change, never as a syntax change.

## The One Law

```
CONFIG DELTA FIRST. IDENTITY SECOND. EXPOSURE LAST.
Validate is not audit — a config can be perfectly valid and still publish an execution organ.
Listing a tool is observation. Calling one is an irreversible production side effect.
The audit produces evidence. The keep-or-close decision is sovereign-class.
```

Run `scripts/ingress_audit.sh <vhost>` for the read-only reconnaissance pass (it never
edits config and never reloads Caddy), then complete the auth probe in
`references/mcp-endpoint-auth-probe.md` if the upstream speaks MCP.

---

## Procedure

### 1. Read the assembled config, not the dispatcher

A root Caddyfile is often just a dispatcher (`import /etc/caddy/vhosts/*.conf`). Judging
the change from the dispatcher alone will read as "nothing changed" while a whole route
was added underneath it.

```bash
grep -rn 'reverse_proxy\|try_files\|respond' /etc/caddy/vhosts/*.conf
/usr/bin/caddy validate --config /etc/caddy/Caddyfile 2>&1 | tail -3
```

`caddy validate` is safe and belongs in the audit. `caddy reload` is **T3** — never run
it as part of an audit, only under a sovereign directive or live incident repair.

### 2. Establish what the added block actually says

A drift report gives you `oldhash -> newhash`. That tells you *that* something changed
and nothing about *what*. Resolve it to the added lines before you report anything.

```bash
ls -t /etc/caddy/vhosts/<vhost>.conf.bak* 2>/dev/null | head -1   # pick the baseline
```

`scripts/ingress_audit.sh` prints the delta between that baseline and the live file
(read-only, computed in Python — it never writes). The `*.bak-*` files are your baseline
set. Read every added block, because that block is the finding.

### 3. Resolve the upstream to a live process and unit

```bash
ss -ltnp | grep -E ':<port>\b'
ps -o pid,lstart,etime,cmd -p <pid>
systemctl show <unit> -p ExecStart -p FragmentPath -p ActiveEnterTimestamp
```

Elapsed time separates a long-resident organ from one started minutes ago. A unit that
started immediately before the ingress patch is evidence of a deliberate rollout.

### 4. Establish whether the upstream was public **before**

This is the step that carries the finding. Search every live and backup vhost for the port.

```bash
grep -l '<port>' /etc/caddy/vhosts/*.conf*
```

A port that appears in **no older vhost** has crossed from local-only to
internet-reachable for the first time. That transition — not the hash change — is what
you report.

### 5. Test the auth posture from the public side, with no credentials

Handshake the public endpoint unauthenticated. If it issues a session or returns data,
it is unauthenticated. Procedure and interpretation: `references/mcp-endpoint-auth-probe.md`.

Read-only enumeration only. **Never invoke a mutation tool to discover whether it is
gated** — that is an irreversible side effect on production. Leave it UNKNOWN and say so.

### 6. Check whether the vhost logs at all

```bash
grep -nE '^\s*log\b' /etc/caddy/vhosts/<vhost>.conf
```

Most blocks carry none by default. This step decides whether the caller history is
answerable at all.

### 7. Find the introducing change

```bash
git log --oneline -- <source path>     # in the repo that owns the upstream
```

Typical ordering on this host: **source written → unit started → ingress patched.**
Ingress that follows both is deliberate. Deliberate is not the same as authorized —
say which one you proved and which you did not.

---

## Pitfalls

- **No `log` directive means you cannot witness callers.** "No entries" is *cannot
  witness*, never *nobody called*. Never report an unlogged public endpoint as clean —
  state plainly that the caller history is unrecoverable. This is the Void Guard applied
  to logs.
- **A proxy route bypasses the host firewall by design.** The localhost-bind + UFW
  posture (`LOCALHOST_IS_PASSWORD`) holds only while the organ stays local. A
  `reverse_proxy 127.0.0.1:<port>` republishes that trust to the internet and the
  firewall never sees the request. When an upstream leans on localhost-trust, *exposure
  itself* is the risk — not any individual tool.
- **Never probe a gate by calling through it.** Enumerate, count, classify. Do not invoke.
- **Count tools and group by owning organ before judging severity.** On a federated MCP
  surface the blast radius is the *highest-risk* tool, not the average one. Group by
  prefix, then flag risk class by name (shell, execute, filesystem, git, postgres, cron,
  seal, deploy) and report the count of each.
- **`Access-Control-Allow-Origin: *` is a separate finding from missing auth.** It means
  any web origin can drive the endpoint from a victim's browser. Report the two
  independently.
- **Never advance or replace a drift baseline yourself.** The baseline file *is* the human
  acknowledgement artifact. Clearing it silences a correctly-firing watchdog and forges
  consent you do not hold. A recurring alert in a shared thread is the system working as
  designed — let it fire until the sovereign decides.
- **Re-verify a reported route failure against the actual path before chasing it.** A
  one-character slug difference serves a different page, or a fallback shell, and reads
  as a live regression. Confirm the exact path exists in the served tree first.

---

## Decision handoff

The audit ends in a ranked choice, not a recommendation to act:

- **Close the route** — drop the ingress block, reload under directive. Reversible,
  fastest, kills exposure while leaving the organ alive on localhost.
- **Keep the route, add auth first** — a token, `basic_auth`, or `forward_auth` ahead of
  it. Design work, not a one-line fix.
- **Accept and record** — advance the baseline deliberately, with the risk stated.

Present the options with the **failure condition of each** (e.g. closing may break another
agent mid-task on that route). Then stop and name the decision as sovereign-class.

Also name what you could not resolve — an unknown owner, an unproven self-gate, an
unlogged window. State it as UNKNOWN rather than folding it into a clean verdict.

## Evidence output

Produce, in order: the config delta vs baseline · `ss`/`ps`/`systemctl` identity of the
upstream · the prior-exposure grep result · the unauthenticated probe transcript · the
introducing commit · and an explicit list of UNKNOWNs. Never convert an unwitnessed
surface into a clean one.
