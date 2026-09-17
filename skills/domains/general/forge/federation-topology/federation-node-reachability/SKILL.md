---
name: federation-node-reachability
description: Use when a federation node cannot reach another node.
risk_tier: medium
tags:
- federation
- tailscale
- headscale
- ufw
- diagnostics
floor_scope:
- F02
- F11
- F13
---

# Federation Node Reachability

Class: "node X cannot reach organ Y on node Z". Two independent layers decide the answer and both must pass. Editing the wrong one burns a change and a restart for nothing.

## Layer model

1. **Tailnet ACL (headscale)** — decides whether node A may talk to node B *at all*, per tag/group and port. Read `/etc/headscale/acl.yaml` (or `acl.json`).
2. **Host firewall (UFW on the target)** — decides whether a specific TCP port is accepted *after* the tailnet already allowed it. Default policy is typically `deny (incoming)`.

The common wrong turn: assuming the ACL blocks when it already grants broad access (`group:admins → *:*`) and the real gap is a missing per-port firewall rule on the target.

## Ladder (all read-only)

```bash
# 1. Is the node in the tailnet, and with which tag?
tailscale status                       # on the node; note tags and 100.64.x.x address
headscale nodes list                   # on the headscale host; shows tag per node

# 2. What does the ACL actually allow?
sed -n '1,200p' /etc/headscale/acl.yaml    # find src group/tag -> dst *:*

# 3. On the TARGET: is the port listening, and on which interface?
ss -tlnp | grep -E ':(8081|18082|18083|18085|7072)\b'
ss -tlnp | grep '<target-tailnet-ip>'

# 4. On the TARGET: does the firewall admit that port?
ufw status numbered

# 5. On the CONSUMER: which address does it actually call, and does that address answer?
tr '\0' '\n' < /proc/<consumer-pid>/environ | grep -iE '<DEP>.*(BASE_URL|HOST|PORT)'
ss -lntp | grep ':<port>'          # note WHICH interface each listener sits on
```

Organ ports typically appear as `tailscaled` listeners bound to the tailnet IP. A listener there means the service is reachable **if** the firewall permits it — the listener alone proves nothing about reachability.

## Pitfalls

- **A `127.0.0.1`-only bind is invisible remotely.** If a service binds loopback, a remote probe times out and reports it DOWN while it is perfectly healthy. Check `ss -tlnp` for which interface the port sits on before treating a timeout as an outage.
- **A tailnet-IP-only bind makes *loopback* probes fail — the mirror case, and the more deceptive one.** `bind 100.64.0.2:<port>` alone answers every remote peer while a loopback probe returns connection-refused. A co-located consumer configured for `http://127.0.0.1:<port>` then reports its own dependency DOWN, and that false outage propagates into kernel health, tracing, and any peer monitor reading the same field. Probe **both** addresses before believing either result.
- **Read the consumer's configured address from its live process, not from docs.** The env in `/etc/…`, a README, and a peer's memory all drift from the process actually running:
  ```bash
  tr '\0' '\n' < /proc/<pid>/environ | grep -iE '<DEP>.*(BASE_URL|HOST|PORT)'
  ```
  Mask values before printing — `sed -E 's/(KEY|TOKEN|SECRET)=.*/\1=<redacted>/I'`.
- **Read the ACL, never infer it.** Presence in a config file is not a rule. Quote the actual accept/deny lines you found.
- **Port-to-organ mapping drifts.** Confirm which service owns a port (`ss -tlnp` → PID → `ps -p <pid> -o cmd`) before reporting an organ as down; detectors, docs, and dashboards all go stale independently.
- **A listener the firewall blocks is not "down".** Report it as unreachable-by-policy; the distinction changes who fixes it.
- **An address is not an identity — probe the peer's `hostname` before you trust a route.** A
  Tailscale IP, an `~/.ssh/config` alias, a fleet-table row, and your memory of "0.4 = that box" are
  all *claims about identity*; only the far side's own `hostname` output witnesses it. Precede any
  cross-host operation with `ssh <target> "hostname; ip -4 addr show | grep 100.64"` and read the
  answer, not the alias you typed.
- **A misresolved alias is self-consistent, so N checks through it are ONE observation.** Every
  re-probe returns the same *wrong* machine, which feels like corroboration while carrying no new
  information. When a peer contradicts you about what is on a node, suspect the route before the
  peer — the disagreement is itself the finding, and neither side is lying.
- **Close a cross-host transfer on the receiver's probe, never the sender's.** `scp`/`rsync` exit 0,
  the sender's `ls`, and the sender's own `sha256sum` read-back all live on the sender's side of the
  boundary; they attest the send, not the landing. State `host + sha256 + byte count` and have the
  other side report what *it* sees. One-sided verification is not verification.
- **Prefer a pull-able lane for anything another node must witness.** `git push` to the shared origin,
  then the peer `git fetch` + `checkout`, yields a hash-addressed artifact both nodes resolve
  independently and neither can author unilaterally. Ad-hoc `scp` plus an in-thread paste is the shape
  that burns a working thread on one file. A large paste into a chat channel is **not** a delivery —
  content over a few KB can arrive split or dropped and the sender cannot see that; ask the receiver
  to confirm the bytes.
- **Name the host whenever you claim an artifact exists.** "It's on disk" with no host is not a
  falsifiable claim. "On `<host>`, `sha256 <hash>`, `<n>` bytes" is the claim a peer can act on.
- **Firewall edits roll back cheaper than an ACL restart.** A per-port allow is removed with `ufw delete <n>`; an ACL change needs a headscale restart. Prefer the smaller blast radius unless the ACL is genuinely wrong.

## Fix shape

Scope each allow to the tailnet CIDR, one rule per port, commented with the consumer:

```bash
ufw allow from 100.64.0.0/10 to any port <port> proto tcp comment "<service> for <consumer>"
```

This fleet also exposes an IPv6 tailnet range that may need its own rule — check for an existing `fd7a:…::/48` style entry before assuming the v4 rule covers traffic.

## Presenting options

When the fix has real tradeoffs, rank the candidate paths against **latency / risk / complexity / reversibility** and state a recommendation with the axis that drove it. The tradeoff table is the artifact the sovereign decides from — a bare recommendation without the table makes them re-derive it.

## Bind-address mismatch: pick the smaller blast radius

When a service is healthy on one interface and a co-located consumer is configured for
another, two fixes exist:

- **Widen the listener** — add the missing `bind` line to the frontend/proxy. One change,
  fixes *every* consumer on that path including ones you have not found yet, and touches
  no consumer config.
- **Edit each consumer's env** — one change per consumer, each needing its own restart, and
  the next consumer added inherits the same trap.

Prefer widening the listener; keep a timestamped backup beside the config, validate before
reload (`haproxy -c -f <cfg>`, `nginx -t`), revert automatically if validation fails, then
probe **both** addresses to prove the repair. A graceful reload (`systemctl reload`) keeps
existing connections alive; a restart does not — and a restart of a unit other sessions are
hosted in kills them.

Confirm the payoff by field name, not by status word: the dependency's own report
(`provider_status.*_healthy`, `last_fallback_reason`) going from a named failure to `null`
is the receipt that the address was the whole fault. Do that *before* reporting the repair
— and if the line turns out to have been already present, report that you verified rather
than applied it.

## Reachability vs authority

Treat any firewall, ACL, or public-port mutation as F13 territory: stage it, show the diff,
and wait for the sovereign's word. Reachability *diagnosis* is read-only and needs no gate —
report findings and the candidate fixes, then hold.
