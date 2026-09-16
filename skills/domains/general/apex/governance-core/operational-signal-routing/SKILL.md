---
name: operational-signal-routing
description: 'Use when routing monitored or scheduled output to humans.'
---
# operational-signal-routing

Design where machine output goes — and when it is allowed to speak. Covers
scheduled-job output routing to a human channel, delta-gated event-bus design,
severity lanes, delivery-path verification, and the claim discipline that every
automated probe must follow.

Two failures this prevents:

1. **Dashboard rot** — scheduled jobs dump raw output into a human channel until the
   human stops reading it, so the channel carries no signal on the day it matters.
2. **Confident partial claims** — a monitor reports a global verdict from one narrow
   reading (one box, one column, one timestamp), and downstream readers act on it.

## The rule: a schedule is timing, an event is meaning

A scheduled job fires whether or not signal exists. Publish to a human channel only
when a run produces:

- a material state transition,
- a decision request, or
- a sealed receipt.

Every scheduled job must still have an accountable outcome *somewhere* — usually a
structured log. **"Accountable" does not mean "posted".**

For each job, ask what it is: measure-only · detect-drift · bounded-repair ·
needs-judgment · strategic-intelligence. Only detect-drift and bounded-repair (after
verification) should produce chat events by default; measure-only and strategic-intel
belong in digests or logs.

## Severity lanes

| Lane | Purpose | Channel behaviour |
|---|---|---|
| P0 — interrupt | security, data-loss, sovereignty, outage | immediate; one incident thread per dedupe key |
| P1 — execution receipt | an action changed verified state | one compact receipt, after action + verification |
| P2 — intelligence digest | trend/context, no intervention needed | batched daily or weekly |
| P3 — telemetry | routine measurement, clean checks | logs/database only, never chat |

## State machine, not trigger spam

`OBSERVED → CLASSIFIED → ACTIONED/HOLD → VERIFIED → SEALED`

Publish only on transitions: NEW, ESCALATED, ACTIONED, VERIFIED, HOLD, RESOLVED,
SEALED. Never repeat unless the state changes. A condition that persists unchanged is
an active incident with an escalation policy — not a recurring FYI.

Dedupe key = hash(rule_id + host_id + resource + normalized condition).

## The delta gate — how the noise floor is actually enforced

Hash the normalized content; post only when the hash differs from the last posted
hash. Identical content exits silent.

**Record the hash only after a successful send.** Marking content as seen on a failed
post loses that event permanently — the dedupe gate then suppresses the retry.

Append the event to an append-only log *before* posting. The log is authoritative; the
chat message is a projection of it.

See `references/event-bridge-design.md` for the working implementation — script
layout, per-source gating predicates, crontab wiring, rollback.

## Delivery-path verification

- **A bot cannot message another bot on Telegram.** The API hard-blocks it
  (`403 Forbidden: the bot can't send messages to the bot`) in groups and DMs alike;
  no `allow_bots` setting bypasses it. Agent→agent belongs on a real agent protocol
  (A2A), not chat. Human↔agent stays on chat.
- **An agent's silence on a lane means one of two things:** the lane is unconfigured,
  or the send failed. Check the transport log for the error before concluding the
  message was ignored — and say which of the two it was.
- **Writing a file is not delivery.** Confirm the send returned success before
  reporting that scheduled output "is being delivered".

## Claim discipline for monitors

These apply to every statement an automated probe makes. Each cost real time when
skipped.

1. **Do not call a finding "clean" or "a false positive" from an earlier reading.**
   Re-probe live state in the same breath. A drift finding that looks like a ghost is
   often a real long-running service.
2. **Resolve a suspicious listener fully before judging it.** `ss -tlnp` gives the
   process; `ps` / `systemctl` says what it actually is. Classify only after that —
   the fix differs between "add to the known allowlist" and "kill the rogue bind".
3. **Qualify every claim with a host id and a scope** (`node` | `federation`). A probe
   on one box is a statement about that box. A port allowlist entry is node-scoped; a
   "service is gone" verdict is node-scoped. Without the qualifier, a node-local
   result is read as federation-wide truth.
4. **Unit active ≠ service healthy.** A systemd unit can be `active` while its health
   body reports `degraded`. Read the health payload, not just `is-active`.
5. **Read the authoritative measurement column, not the headline number.**
   `docker system df` reports SIZE and RECLAIMABLE separately — only RECLAIMABLE is
   freeable, and shared build-cache layers make Total ≠ reclaimable. Named volumes are
   *data*; only `-f dangling=true` is a candidate. Under a cache directory, model
   weights are re-download cost, not free space — separate them from regenerable
   caches before quoting any aggregate.
6. **Never invent a config schema.** Read the component's manifest for declared
   settings, then the code for what is actually read. Keys nothing reads are silently
   ignored — the change looks applied and does nothing. Cite file:line in the proposal.
7. **Never state an aggregate figure you have not verified per item.** An off-by-6x
   reclaim estimate is the same error as a false "clean": partial observation,
   confident global verdict.

## Escalation boundary

Anything disruptive — kill, restart, firewall change, rollback — is HOLD by default.
Action only under an explicitly pre-authorized, reversible, bounded runbook, and post
the receipt *after* post-action verification, never the attempt.

---
*DITEMPA BUKAN DIBERI*
