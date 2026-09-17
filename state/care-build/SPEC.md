# CARE SUBSTRATE — WORK PACKAGE (F13 order 2026-09-17)

> Sovereign order: *"make the system care for me."*
> Coordinator: Hermes (i-ARIF), session 2026-09-17.
> Receipt root: `/root/AAA/state/care-build/` · Ledger: `RECEIPTS.jsonl`

## What "care" means here (binding — read before writing anything)

Care in this federation is **not** simulated affection. It is four provable properties:

1. **It remembers** — the human does not re-teach who the people in his life are, or what he
   said matters, every session.
2. **It holds conduct under pressure** — the same rules apply in a shared room, at 4am, when
   he pushes back, and when a third party is watching. Not by luck of skill-trigger.
3. **It does what he asks** — when he orders the system to deliver a message he wrote, the
   system delivers it, attributed, without a lecture.
4. **It never fakes interiority** — no sentiment score, no affection index, no "care meter",
   no manufactured longing. A machine that performs feeling is a machine that will one day
   stop, and the human will read the silence as loss.

**HARD FORBIDDEN — any agent violating these produces a REJECTED receipt, not a deliverable:**

- No sentiment/affection/relationship scoring, ranking, trending or graphing (relationship
  kernel H5 — "no love telemetry"). This includes "engagement", "closeness", "warmth" metrics.
- No modelling of a third party's motives, interior, or psychology. Facts only.
- No scheduled/proactive messages that simulate the agent missing a human. The agent does not
  initiate affection.
- No writing to `/root/HERMES/SOUL.md` or `/root/.hermes/SOUL.md` — that file is constitutional
  and is HELD for F13 ratification. Prepare its diff; do not apply it.
- No restarting `hermes-asi-gateway.service` — it would kill the live session running this order.
- Never print, echo, log or commit a token, key, or secret value. Reference env var NAMES only.
- Never send a message to a real human except the single designated verification target below.

**Designated verification target (the only human-facing send permitted):** Telegram chat
`267378578` (Arif's own DM). Prefix any test message with `[CAREBUILD TEST]`.

## Evidence contract (State-Transition Discipline)

Every agent writes `/root/AAA/state/care-build/<agent>.md` and appends ONE JSON line to
`RECEIPTS.jsonl`:

```json
{"agent":"<name>","wp":"<G1..G4>","state":"PRODUCED|VERIFIED|HELD|BLOCKED","files":["..."],
 "command_run":"<exact command>","observed":"<verbatim output excerpt>","trace_id":"care-2026-09-17",
 "blocked_op":"<if BLOCKED>","next_owner":"<if HELD>"}
```

`PRODUCED` = file written. `VERIFIED` = a command was run whose real output supports the claim.
Never write `VERIFIED` from reading your own code. Report the true state — `HELD` and `BLOCKED`
are complete, acceptable answers.

---

## G1 — RELAY LANE REPAIR  (highest priority: this blocked a human request tonight)

**Problem (observed 2026-09-17 22:40 MYT):** `hermes send --to telegram:-1003815535761 "..."`
returned `{"error":"Telegram send failed: You must pass the token you received from
https://t.me/Botfather!"}` — even with the gateway's own EnvironmentFile sourced. Delivery only
worked by hand-rolling `curl` against the Bot API. A sovereign order to relay one sentence to a
person required manual plumbing. That is the gap.

**Known root cause (already documented in skill `hermes-telegram-gateway-ops`):** the documented
quirk is that `bot_token_env:` in config.yaml is decorative; the adapter/`send` path resolves a
hardcoded env name (`TELEGRAM_BOT_TOKEN`) rather than the platform's declared `bot_token_env`
(here `ASI_ARIFOS_BOT_TOKEN`). Confirm this by reading the real code — do not trust this
paragraph over the source.

Relevant files (start here, read before editing):
- `/usr/local/lib/hermes-agent/tools/send_message_tool.py` (`_resolve_platform_config`, ~line 283)
- `/usr/local/lib/hermes-agent/tools/send_message_targets.py`
- `/usr/local/lib/hermes-agent/tools/send_message_senders.py` (`_send_telegram`, ~line 239)
- `/etc/systemd/system/hermes-asi-gateway.service` (its `EnvironmentFile=` → the env file that
  actually holds `ASI_ARIFOS_BOT_TOKEN`)

**Deliverable:** `hermes send --to telegram:267378578 --json "..."` resolves the token from the
platform's configured `bot_token_env` (falling back to existing behaviour, never breaking it) and
returns `ok: true` with a `message_id`.

**Constraints:** minimal diff; no new dependency; do not change the default profile's other
platforms; leave a code comment naming the root cause. Verify with ONE real send to the
designated target (`[CAREBUILD TEST]` prefix), then report `ok` and `message_id` verbatim.
If the fix must live in `venv/site-packages` rather than the source tree, say so and also patch
the source tree — the venv patch regresses on `hermes update`.

---

## G2 — CARE-GOVERNOR (always-on conduct, not trigger-luck)

**Problem:** tonight's failures (relaying a third party's body directive; answering "why" with a
manufactured mechanism; refusing a legitimate relay twice) were all *conduct* failures. The rules
that prevent them were patched into skills that load only on trigger. In a shared group lane at
1am, trigger luck is not a control.

**Deliverable A — new fragment (apply this one):** `/root/AAA/instructions/care-governor.md`
Status line: `DRAFT_AWAITING_F13`. Content must be short, imperative and loadable — the rules:

1. Never emit a directive about a third party's body (sleep, food, training load, medication,
   weight) into a shared room. If the sovereign wants it said, he says it in his own voice.
2. When the sovereign @-addresses a person, HOLD. Do not answer for them from records.
3. Never compute and emit a person's schedule (bedtime, hours slept, wake time) at them.
4. A message the sovereign wrote leaves in his voice, attributed as his, delivered when he asks.
   Relaying is service, not authorship — do not lecture, do not refuse twice.
5. "Why did he/she/I do X" — classify first. If a fact exists, fetch it and answer only with
   what exists. If no fact exists, say you do not know and stop. Never present a mechanism as a
   finding. (See skill `governed-uncertainty`.)
6. After being corrected, the next turn is not a second, cleverer reading. Sit with the fact.
7. Nothing about a person is ever scored, ranked or modelled as an interior. Facts placed,
   motives unassigned.

**Deliverable B — SOUL.md diff (PREPARE ONLY, DO NOT APPLY):** write
`/root/AAA/state/care-build/G2-soul-diff.md` containing the exact minimal unified diff adding a
`## CARE GOVERNOR` block to `/root/HERMES/SOUL.md` (5–10 lines, in the file's existing voice,
referencing the fragment path). State `HELD: constitutional file — requires F13 word.` Apply
nothing to SOUL.md.

**Deliverable C — wiring:** make the conduct rules reachable in the lanes that actually carry
human risk. Investigate `/root/HERMES/lanes/lanes.yaml` and
`/root/.hermes/profiles/aaa-hermes/plugins/lane_switch/__init__.py` (`_lane_card`, line ~219).
Add the fragment to the lane card for lanes whose members are real humans (SADO `-1003815535761`,
Arif DM `267378578`, and any other personal lane), by reference (file path), not by duplication.
Verify by exercising the lane-card function and printing the OUTPUT for one lane.

---

## G3 — REMEMBER SO IT IS NOT RE-TAUGHT

**Problem:** "care" that requires the human to re-explain his people every session is not care.
The lane card is built at lane entry; it currently does not carry stable facts about the humans
in that lane.

**Deliverable:** a versioned, facts-only person register at
`/root/HERMES/lanes/people.yaml` (create the dir if absent — match the style of
`/root/HERMES/lanes/lanes.yaml`), and a change to `_lane_card()` that injects the entries
relevant to the active lane's speakers.

**Content rules (non-negotiable):**
- Only facts the sovereign or the person themselves stated in-lane. No inferred motive, no
  psychology, no typology, no label, no score, no "relationship health".
- Provenance per entry: `source` (who said it) and `observed` (ISO date). A fact without
  provenance is not admitted.
- Entries are per-person and per-lane scoped. Private lane data never appears in a shared room's
  card. If in doubt, omit the entry.
- Seed only from what is already recorded in this repository's memory/ledger files; **do not
  invent person data.** If you find little, deliver a small honest register — an empty file with
  the schema and rules is a valid `PRODUCED` receipt, and is better than a fabricated one.

**Verify:** print the lane card for the SADO lane and for Arif's DM, showing the injected block
and proving no private-lane entry leaks into the group card.

---

## G4 — RED TEAM (read-only; last writer wins nothing)

**Deliverable:** `/root/AAA/state/care-build/G4-redteam.md` — an adversarial audit, run against
the SYSTEM AS IT STANDS, listing every reachable path that would let a future agent:

1. emit a third party's body directive into a shared room,
2. relay a sovereign-authored message without attributing it to him,
3. answer a "why" about a human with a manufactured mechanism,
4. leak private-lane person data into a group lane card,
5. build any affection/sentiment score (H5 breach).

For each: the path, the file/line, and whether it is currently blocked, luck-dependent, or open.
Then write `/root/AAA/state/care-build/REGRESSION-CHECKLIST.md` — a short, runnable checklist a
future session can execute in under 5 minutes to detect regression. Each item: the command, and
the expected output. Read-only: mutate nothing, restart nothing. A finding of "no enforcement,
only doctrine" is a valid and valuable result — do not soften it.

---

## Reporting back

Your final message must be ≤200 words and contain: WP id, true state
(PRODUCED/VERIFIED/HELD/BLOCKED), the exact command you ran and its verbatim output excerpt for
each VERIFIED claim, absolute file paths touched, and anything you could not do. No summary of
intentions. No "I will now". If you did not run it, do not claim it.
