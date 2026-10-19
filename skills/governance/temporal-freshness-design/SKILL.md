---
name: temporal-freshness-design
description: Use when a feed must never repeat stale news.
tags: [temporal, freshness, cron, tracker, news, ledger, design]
---

# Temporal Freshness Design

For any system whose job is to tell a human about **events** — a match result, an award, a filing, a price break, a death, a release. The defect this prevents is not "the job ran late"; it is *the job ran on schedule and reported last week's event as today's news*.

## When to load

- Building or repairing a tracker, alert, digest, watchlist, monitoring cron, or "notify me when X happens" loop.
- A user says a report was late, repeats something they already know, or presents old information in a fresh voice.
- A store has `target_date` / countdown / days-remaining fields but no field for *when something happened*.
- A feed announces the same headline twice, or an agent cannot tell "nothing is new" from "I have nothing to say".

## The failure this exists for

Most trackers model **one direction of time**: how long until X. That store has no home for X once it occurs — anything with a negative delta is dropped. So the event survives only inside the job prompt or the agent's memory, where it is re-stated on every fire with no memory of having been said.

The tell: the interval looks wrong ("weekly job, so of course it was late"). The interval is rarely the bug. The store is.

Widening the cadence does not fix it — it just makes stale announcements arrive more often.

## The model

Two axes and one ledger. Nothing more.

| Piece | Rule |
|---|---|
| `occurred_at` | ISO-8601 **with offset**. Absent ⇒ the record can never be news, only a countdown. |
| `delivery_window_hours` | Per-event, with a default. Age beyond it ⇒ `STALE` and must not ship. |
| freshness state | **Computed at read time** from `now − occurred_at` → `FRESH` / `STALE` / `PENDING` (future). Never stored. |
| delivery ledger | Append-only `{event_id, delivered_at, channel, age_at_delivery, state_at_delivery}`. Presence ⇒ already told. |

The definition that makes the whole thing work: **"new" means new to the reader, not new to the file.**

## Procedure — retrofit an existing tracker

1. **Add `occurred_at`** to the event schema and to every existing record that has already happened. Backfill from the best available source; if unknown, leave it null and accept that record can never be announced.
2. **Add `delivery_window_hours`** with a defensible default. Six hours is a good floor for same-day operational news: a result at 22:00 is still news at 07:00; yesterday's result is not.
3. **Write the freshness function** as pure arithmetic: parse → normalise to UTC → `age = now − when` → state. No I/O, no hidden clock read inside.
4. **Add the ledger** (a small JSON file is enough) with an idempotent append that refuses an unknown id.
5. **Expose three verbs**: query-fresh (filter by window AND not-in-ledger, youngest first), mark-delivered, show-ledger.
6. **Make query-fresh exit non-zero when empty.** The caller must be able to honour silence.
7. **Rewrite the job prompt** as: probe fresh → verify against primary source → deliver → mark-delivered. Step 4 is not optional.
8. **Prove it with a self-test** covering: inside window (`FRESH`), past window (`STALE`), a naive timestamp, not-yet-occurred (`PENDING`), and a delivered event never resurfacing.

## Pitfalls

- **Naive timestamps are local, not UTC.** A timestamp with no offset, authored by a human in the operator's zone, must be read in that zone. Treating it as UTC shifts the event forward by the offset, so it never ages and reads `FRESH` forever — the exact bug the freshness axis was added to kill. Normalise naive → operator zone, then convert to UTC.
- **Never store a "this is new" boolean.** It is true when written and false seconds later. Freshness is a function of the clock at read time.
- **Never let an empty result render.** A caller that cannot distinguish "nothing happened" from "nothing to say" will fill the silence with old material. Exit non-zero, and make the prompt state explicitly: no fresh items ⇒ no output.
- **Mark delivered immediately after sending, in the same turn.** Any gap between deliver and mark is a window for a duplicate. If delivery fails, do not mark.
- **Don't mark *before* delivering.** A crash between mark and send loses the event permanently — the opposite failure, and the harder one to notice.
- **A `target_date`-only store silently drops the past.** If the query filters `days < 0`, every occurrence is invisible by construction. Check that filter before blaming the schedule.
- **Freshness is not significance.** A thing can be one hour old and trivial. Do not let "it is fresh" imply "it is worth sending" — that is a separate editorial gate.

## Verification checklist

```
[ ] schema has occurred_at + delivery_window_hours
[ ] freshness() is pure and takes `now` as an argument (testable without freezing the clock)
[ ] query returns [] AND exit != 0 when nothing is fresh
[ ] mark-delivered is idempotent and refuses unknown ids
[ ] self-test proves FRESH / STALE / PENDING / naive-TZ / delivered-once
[ ] job prompt sequences: probe -> verify -> deliver -> mark
[ ] a known past event, replayed through the query, does NOT come back
```

## References

- `references/chron-store-implementation.md` — a worked implementation of this model over a countdown store: field shapes, the three CLI verbs, and the self-test cases that prove each state.
