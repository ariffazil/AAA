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
```

Organ ports typically appear as `tailscaled` listeners bound to the tailnet IP. A listener there means the service is reachable **if** the firewall permits it — the listener alone proves nothing about reachability.

## Pitfalls

- **A `127.0.0.1`-only bind is invisible remotely.** If a service binds loopback, a remote probe times out and reports it DOWN while it is perfectly healthy. Check `ss -tlnp` for which interface the port sits on before treating a timeout as an outage.
- **Read the ACL, never infer it.** Presence in a config file is not a rule. Quote the actual accept/deny lines you found.
- **Port-to-organ mapping drifts.** Confirm which service owns a port (`ss -tlnp` → PID → `ps -p <pid> -o cmd`) before reporting an organ as down; detectors, docs, and dashboards all go stale independently.
- **A listener the firewall blocks is not "down".** Report it as unreachable-by-policy; the distinction changes who fixes it.
- **Firewall edits roll back cheaper than an ACL restart.** A per-port allow is removed with `ufw delete <n>`; an ACL change needs a headscale restart. Prefer the smaller blast radius unless the ACL is genuinely wrong.

## Fix shape

Scope each allow to the tailnet CIDR, one rule per port, commented with the consumer:

```bash
ufw allow from 100.64.0.0/10 to any port <port> proto tcp comment "<service> for <consumer>"
```

This fleet also exposes an IPv6 tailnet range that may need its own rule — check for an existing `fd7a:…::/48` style entry before assuming the v4 rule covers traffic.

## Presenting options

When the fix has real tradeoffs, rank the candidate paths against **latency / risk / complexity / reversibility** and state a recommendation with the axis that drove it. The tradeoff table is the artifact the sovereign decides from — a bare recommendation without the table makes them re-derive it.

Treat any firewall or ACL mutation as F13 territory: stage it, show the diff, and wait for the sovereign's word. Reachability *diagnosis* is read-only and needs no gate.
