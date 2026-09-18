# Routing evidence — who actually receives what

The question "does this reach the human?" is answered in four separate steps, and a green
status field answers none of them.

```
INTENT → CONFIG → RESOLVED → DELIVERED
```

| Step | What it proves | How it is measured |
|---|---|---|
| INTENT | someone meant it to go there | the script/prompt says so |
| CONFIG | the environment overrides it | read the resolver lines; env beats a literal |
| RESOLVED | the id means what you think | resolve the numeric id against its own directory |
| DELIVERED | it arrived | a receipt with destination + provider message id |

Improve confidence only by moving right. A job scheduled, enabled, and `last_status: ok` has
not moved past step one.

## Trap 1 — a symbolic name is not a destination

An environment variable or constant can silently outrank the literal you are reading. Trace the
resolver, not the value you expect:

```python
# the target is whichever of these wins, and the env one wins
chat_id = env.get("TARGET_OVERRIDE") or first_numeric(env.get("ALLOWED_CHATS"))
```

Read the resolver lines and follow precedence before describing where anything goes.

## Trap 2 — resolve every numeric id against its own directory

An id that resolves to a **group** while you believe it is a **direct message** is the normal
case, not an exotic one. Where a directory of channels exists, look the id up and quote its
`type`. Never describe an id by its shape ("it looks like a DM", "it is negative so it is a group").

Corollary: never infer a sender's identity from an id field alone. A mirrored message can carry
the third party's id in one field and your own in another; verify the field that identifies the
CHAT against the field that identifies the PERSON.

## Trap 3 — a host has several scheduler registries

They are independent and do not know about each other. A map built from one layer is not
incomplete — it reads as complete, which makes it wrong. Enumerate the sources first, then
filter inside them:

- agent/cron job store (JSON, per-agent)
- `systemctl list-timers --all`
- `/etc/cron.d/*`
- user crontab (`crontab -l`)

Then, and only then, filter by name — and remember the filter finds YOUR vocabulary, not the
category. An entry named differently is invisible to a keyword search but visible to an
enumeration.

## Trap 4 — a receipt is the only proof, and its clock is usually UTC

Receipt logs typically stamp UTC while you reason in local time. Filtering a UTC field by a
local date silently drops exactly the boundary rows you care about, and returns a confident
empty result. Print the newest timestamp actually present and convert it before asserting that
nothing arrived.

Also confirm the log is still being WRITTEN (`tail -1` vs now) before treating it as evidence:
a stale log is silence, and silence is not a negative.

## Distinguishing many sensors from many producers

Many sensors are good; many producers of the same truth are not. For each apparent duplicate,
classify it before acting: duplicate producer, duplicate delivery, independent witness, fallback,
or genuinely different purpose. **Never delete an independent witness.** Delete the second
producer of a claim that already has one.
