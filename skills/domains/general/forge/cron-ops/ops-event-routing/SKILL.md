---
name: ops-event-routing
description: Use when routing cron or monitor output to a chat channel.
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Ops Event Routing

Route automated job output to the right destination. **Cron is timing; the event bus is
meaning.** A chat channel is an append-only execution ledger, not a notification feed.

## The rule

Every scheduled job must have an accountable result *somewhere*. That does not mean every
run talks in chat.

- **Producers stay silent.** A detector job writes its finding to a log/ledger and exits.
- **A bridge posts.** A separate job reads the producer's output a minute later and decides
  whether to publish.
- **Gate on change, not on schedule.** Posting unchanged content on a fixed cadence trains
  the reader to ignore the channel; the one real alert is then missed.

## Lanes

| Lane | Purpose | Channel behaviour |
|---|---|---|
| P0 interrupt | security, data-loss, sovereignty, production outage | post immediately; one thread / dedupe key |
| P1 receipt | a system action changed verified state | post one compact receipt after verification |
| P2 digest | trend or governance context, no intervention needed | batch daily/weekly |
| P3 telemetry | routine measurement, clean checks, run start/end | log only — never chat |

## Delta gate

Hash the content (sha256, truncated) and compare with the last posted hash for that source.

- Unchanged → exit 0 and print nothing. This is the noise floor; a clean day is zero messages.
- Changed → append a structured record to the authoritative event log, then project a
  human-readable message to the channel.
- Write the new hash only after the send succeeds, so a failed send retries next run.

The event log is authoritative; the channel is a projection of it. Never treat the channel
as the ledger.

## Scope every claim

A node-local observation stated as a federation claim is a truth-floor violation. Every
posted event carries `host_id` and `scope: node|federation`. Never send "X is gone" or "Y is
clean" without node qualification — the downstream reader otherwise concludes "nothing to
do" and misses a real finding on the other box.

## Suppress outright

"Working" / progress / timer pings, clean-check results, successful routine housekeeping
(backup, prune, cert renewal, reaper), raw agent deliberation transcripts, repeated failure
notices for the same incident, and proposals that were never executed or approved.

## Pitfalls

- **Schedule the bridge AFTER its producer.** It reads the producer's output, so it runs at
  producer-time + 1 minute. Replacing a producer's own notify with a bridge and forgetting
  to schedule the bridge silently drops all alerting for that source.
- **A fixed-cadence digest is not a bridge.** Several daily posts at fixed clock times is a
  dashboard. An unresolved standing condition should become an incident with an escalation
  policy, not a repeated FYI.
- **Idempotence is required.** Bridges must be safe to re-run; dedupe by content hash, not
  by "did I already run today".
- **Bridges are additive.** Deleting their schedule lines returns every producer to
  log-only behaviour with no producer change — keep rollback that cheap.
- **A channel's own history is not proof of delivery.** Verify the send result, then write the
  hash; otherwise a failed post is silently treated as published.
- **`attach_to_session: true` is a second, hidden surface.** Cron output that injects into the
  user's active session log — alongside direct prompts — reads as "interruption" even when the
  cron delivered fine. The user sees `[response interrupted]` for their own killed direct reply,
  then `Cronjob Response: ...` adjacent in time, and attributes the disruption to the cron. It
  wasn't the cron; their own `/restart` killed the direct reply. Diagnostic: read `last_status`
  and `failure_streak` first. If both are clean, the artefact is `attach_to_session`, not a cron
  failure. Fix: `attach_to_session: false`. The cron keeps delivering to its `deliver` target
  exactly as before; it stops appearing in the session log.

## Reference
- `references/event-bus-routing.md` — event envelope, state machine, per-job inventory policy.
