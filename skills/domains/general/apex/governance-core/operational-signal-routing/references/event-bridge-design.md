# Delta-gated event bridge — implementation

Routes scheduled output to a human channel only on material change. Chat is a
projection of an append-only event log; the log is authoritative.

## Shape

```
<source> job  ──> writes output file (report/log) ──> <source>-event.sh
                                                              │
                                                              ▼
                                     event-bridge.sh <source> <content_file> [P0|P1|P2]
                                                              │
                                    hash == last posted hash? ──yes──> exit 0, silent
                                                              │no
                                                              ▼
                                 append events.jsonl  →  notify  →  record hash
```

## Decision points inside the bridge

1. **Delta gate.** `hash=$(sha256sum "$content_file" | cut -c1-16)`; compare against
   `state/<source>.last_hash`. Identical → exit 0 with no post. This is the whole
   noise floor; everything else is formatting.
2. **Classify** when the caller does not pass an explicit lane, by scanning the
   content: outage/failure/breach vocabulary → P0; restored/healthy/resolved → VERIFIED;
   sealed/scar/governance → at least P1.
3. **Envelope.** severity, `event_id = evt_<date>_<hhmm>_<hash8>`, `scope: node`,
   host id, source name, dedupe hash, ISO-8601 UTC timestamp, verdict state.
4. **Append the one-line JSON record to `events.jsonl` before posting.** The log is
   authoritative; if the send fails you still have the event.
5. **Post, and only on success write `<source>.last_hash`.** A failed post must not
   mark the content as seen, or the event is suppressed forever.

## Per-source gating predicates

A bridge should re-check *actionability*, not just novelty:

| Source | Post condition |
|---|---|
| drift scanner | report file exists — the scanner only writes one when drift was found |
| triage digest | contains stale/blocking items, a seal blocker, a decision needed, or a failed deploy |
| vitality pulse | vitality below threshold, contradictions ≠ 0, or DEGRADED/CRITICAL |
| flow digest | governance-collapse, HOLD, or flow degraded |
| federation pulse | material delta versus the previous run |

## Crontab wiring

Schedule each bridge one minute after its parent job so the output file is complete:

```cron
# parent
47 7 * * * /root/A-FORGE/duties/federation-pulse.sh >> .../pulse.log 2>&1
# bridge — delta-gated
48 7 * * * /root/scripts/pulse-event.sh             >> .../bridge.log 2>&1
```

Append a one-line comment naming the script and the invariant (`delta-gated`), so an
auditor can distinguish an intentional bridge from a stray cron entry.

## Remove the old direct-post path

If the parent script already posts to the channel itself, delete that call in the same
change. Two delivery paths means double posts on exactly the days that matter. Leave a
comment at the old site naming the bridge that now owns delivery.

## Rollback

```bash
crontab -l | grep -v "event-bridge\|-event\.sh\|weekly-digest" | crontab -
```

State lives under one directory (`<state_dir>/{events.jsonl, <source>.last_hash,
bridge.log}`). Deleting the state directory resets every delta gate — the next run
posts as NEW for all sources, so use that deliberately, not casually.

## The always-on companion: one weekly digest

One scheduled message that always posts — the "still alive" check, separate from the
delta-gated bridges. Keep it to a handful of lines: capacity headroom, component
health, new-scar count, mesh/vault verdicts, unresolved P0/P1, event counts by
severity. It is an audit artifact, not an interrupt, so pick a stable weekly ritual
slot and keep it there.
