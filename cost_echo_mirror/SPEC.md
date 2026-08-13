# SPEC: cost-echo-mirror v0.1

## What you are building

A read-only CLI organ called `cost-echo` for the arifOS federation. It measures
HUMAN relational energy asymmetry — energy given vs energy returned — across
human↔human and human↔agent relationships, and emits green/yellow/red signals.
It NEVER acts on relationships. It is a mirror for F13 (the human sovereign) to
read. Advisory only.

## Working directory

Build EVERYTHING inside the current working directory (/root/forge_work/cost_echo_mirror).
Do not touch any other directory. Do not modify the source database.

## Input data (READ-ONLY — never write to this file)

SQLite database: /usr/local/lib/hermes-agent/profiles/aaa-hermes/state.db

Tables you need:
- sessions(id, source, user_id, chat_id, chat_type, display_name, started_at)
- messages(id, session_id, role, content, timestamp)
- session_model_usage(session_id, model, api_call_count, input_tokens,
  output_tokens, reasoning_tokens, cache_read_tokens, estimated_cost_usd)

Relationships are inferred by chat: each distinct (chat_id, user_id) pair that
appears in user-role messages is one "actor". Group chats have multiple actors.

## Deliverables

1. `cost_echo/__init__.py` — package
2. `cost_echo/db.py` — read-only SQLite access (URI mode immutable=1 if
   supported, else plain read; never open with write)
3. `cost_echo/ledger.py` — the energy ledger. For each actor and each
   relationship (pair or group), compute from messages:
   - tokens_given: word count of messages authored by the actor (proxy for
     energy output)
   - messages_given: count of authored messages
   - tokens_received: word count of messages that REPLY to the actor.
     Replies are detected two ways:
     (a) messages whose content starts with '[Replying to:' (the Telegram
         reply convention in this DB), and
     (b) assistant-role messages in sessions where the actor is the user.
   - response_latency_s: median seconds between an actor's message and the
     next reply-class message in the same session/chat
   - closure_rate: fraction of an actor's threads (their message followed
     within 30 min by >=1 reply) — proxy for "was I answered, or left hanging"
   - asymmetry = tokens_given / max(tokens_received, 1)
   - drain_score = asymmetry * (1 - closure_rate)  # range 0..N, higher = more drain
4. `cost_echo/signal.py` — thresholds (make them CLI-configurable with
   defaults): green if drain_score < 0.8 AND closure_rate >= 0.6; yellow if
   drain_score < 2.0; red otherwise. Emit per-relationship signal.
5. `cost_echo/cli.py` — argparse CLI named `cost-echo` with subcommands:
   - `cost-echo ledger [--chat-id ID] [--min-messages N]` — print ledger rows
     (default JSON to stdout; `--table` for aligned text)
   - `cost-echo signal [--chat-id ID]` — per-relationship green/yellow/red
     with one-line human-readable reason
   - `cost-echo report [--chat-id ID]` — full markdown report: ledger +
     signals + top-5 most-asymmetric relationships. Header must say:
     "ADVISORY ONLY — F13 decides. Never auto-act."
   All output must be deterministic (sort by drain_score desc, then actor).
6. `cost-echo` — executable shim (bash, `exec python3 -m cost_echo.cli "$@"`)
7. `tests/test_ledger.py` + `tests/test_signal.py` — pytest, using a
   temporary SQLite fixture that mimics the real schema (build it in the
   fixture; NEVER point tests at the real DB). Cover: asymmetry math,
   reply detection both paths, closure_rate edge cases (no replies = 0.0,
   all replied = 1.0), threshold boundaries exactly at 0.8 and 2.0.
8. `README.md` — what it is, governance note (advisory only, F13-bound,
   data is human-relational and stays sovereign-owned), usage examples.

## Constraints

- Python 3.10+ stdlib only for the package itself (pytest allowed in tests).
- No network calls. No writes anywhere except inside the working dir.
- Deterministic output; no timestamps in output unless requested via flag.
- Every module <= 250 lines. If a module grows, split it.
- Handle: empty DB, chat with zero replies, single-actor chats, unicode
  content. No exceptions on real data.

## Definition of done (verify before you finish)

1. `pytest tests/ -q` passes, 100% of the covered edge cases above.
2. `python3 -m cost_echo.cli ledger --min-messages 5 --table` runs against
   the real DB path without error and prints rows.
3. `python3 -m cost_echo.cli report` produces markdown that a human can read.
4. `python3 -m cost_echo.cli signal` exits 0 and prints green/yellow/red
   lines with reasons.
Run all four yourself and paste their actual output in your final answer.
