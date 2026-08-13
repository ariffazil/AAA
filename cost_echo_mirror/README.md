# cost-echo

A read-only CLI organ for the arifOS federation. It measures **human
relational energy asymmetry** — energy given vs energy returned — across
human↔human and human↔agent relationships recorded in the Hermes state
database, and emits green/yellow/red signals.

**ADVISORY ONLY — F13 decides. Never auto-act.**

cost-echo is a mirror, not a hand. It never writes, never notifies, never
acts on any relationship. It exists so the human sovereign (F13) can *see*
where energy flows out and does not return.

## Governance note

- **Advisory only.** Signals are observations for F13, not triggers.
- **F13-bound.** The human sovereign reads the mirror; no agent may act on
  its output autonomously.
- **Sovereign data.** The underlying data is human-relational. It stays
  sovereign-owned; cost-echo opens the source DB strictly read-only
  (SQLite URI `immutable=1` when supported) and writes nothing outside its
  own directory.
- **Deterministic.** Output is sorted (`drain_score` desc, then actor) and
  contains no timestamps unless `--with-timestamp` is passed.

## What it measures

Per actor (a distinct `(chat_id, user_id)` pair authoring user messages):

| metric | meaning |
|---|---|
| `tokens_given` | word count of messages the actor authored (energy out) |
| `messages_given` | count of authored messages |
| `tokens_received` | words in replies to the actor (energy back) |
| `response_latency_s` | median seconds from an actor message to the next reply |
| `closure_rate` | fraction of the actor's messages answered within 30 min |
| `asymmetry` | `tokens_given / max(tokens_received, 1)` |
| `drain_score` | `asymmetry * (1 - closure_rate)` — higher = more drain |

Replies are detected two ways: (a) messages starting with `[Replying to:`
from another actor in the same chat (Telegram convention), and (b)
assistant-role messages in sessions where the actor is the user.

## Signals (defaults, CLI-configurable)

- **green** — `drain_score < 0.8` AND `closure_rate >= 0.6`
- **yellow** — `drain_score < 2.0`
- **red** — otherwise

## Usage

```bash
./cost-echo ledger --min-messages 5 --table      # aligned text ledger
./cost-echo ledger --chat-id -1003815535761      # JSON ledger, one chat
./cost-echo signal --table                       # green/yellow/red + reason
./cost-echo report                               # full markdown report
python3 -m cost_echo.cli --db /path/to/state.db ledger   # custom DB path
./cost-echo --green-drain 1.0 --yellow-drain 3.0 signal  # custom thresholds
```

## Development

Python 3.10+ stdlib only for the package (pytest for tests). Tests build
their own temporary SQLite fixture mimicking the real schema — they never
touch the real DB.

```bash
python3 -m pytest tests/ -q
```
