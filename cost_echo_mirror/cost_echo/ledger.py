"""Energy ledger for cost-echo.

For each actor (distinct (chat_id, user_id) pair authoring user messages)
compute energy-given vs energy-returned metrics from message traffic.

Reply detection (two paths, per spec):
  (a) messages whose content starts with '[Replying to:' authored by a
      DIFFERENT actor in the same chat;
  (b) assistant-role messages in sessions where the actor is the user.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from statistics import median
from typing import Any, Iterable

REPLY_PREFIX = "[Replying to:"
CLOSURE_WINDOW_S = 1800.0  # 30 minutes


@dataclass(frozen=True)
class LedgerRow:
    chat_id: str
    actor: str
    display_name: str
    messages_given: int
    tokens_given: int
    tokens_received: int
    response_latency_s: float | None
    closure_rate: float
    asymmetry: float
    drain_score: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _words(text: str | None) -> int:
    if not text:
        return 0
    return len(text.split())


def _is_reply_marker(content: str | None) -> bool:
    return bool(content) and content.lstrip().startswith(REPLY_PREFIX)


def _actor_label(user_id: Any, session_id: str) -> str:
    return str(user_id) if user_id is not None else f"session:{session_id}"


def compute_ledger(
    messages: Iterable[dict[str, Any]],
    chat_id: str | None = None,
    min_messages: int = 1,
) -> list[LedgerRow]:
    """Compute ledger rows from message dicts (see db.fetch_messages).

    Deterministic: sorted by drain_score desc, then actor asc.
    """
    # Group messages by chat.
    chats: dict[str, list[dict[str, Any]]] = {}
    for m in messages:
        cid = str(m.get("chat_id") or "")
        if chat_id is not None and cid != str(chat_id):
            continue
        chats.setdefault(cid, []).append(m)

    rows: list[LedgerRow] = []
    for cid, msgs in chats.items():
        # Actors: distinct (chat_id, actor) authoring user-role messages.
        actors: dict[str, dict[str, Any]] = {}
        for m in msgs:
            if m["role"] != "user":
                continue
            label = _actor_label(m.get("user_id"), m["session_id"])
            entry = actors.setdefault(
                label,
                {"display_name": m.get("display_name") or label, "count": 0},
            )
            entry["count"] += 1
            if m.get("display_name"):
                entry["display_name"] = m["display_name"]

        for actor, meta in actors.items():
            if meta["count"] < min_messages:
                continue
            rows.append(_compute_actor(cid, actor, meta["display_name"], msgs))

    rows.sort(key=lambda r: (-r.drain_score, r.actor, r.chat_id))
    return rows


def _is_reply_for(actor: str, m: dict[str, Any]) -> bool:
    """Reply-class message relative to `actor` (spec paths a and b)."""
    if m["role"] == "assistant":
        # Path (b): assistant message in a session where the actor is the user.
        return _actor_label(m.get("user_id"), m["session_id"]) == actor
    if m["role"] == "user":
        # Path (a): '[Replying to:' marker authored by someone else.
        author = _actor_label(m.get("user_id"), m["session_id"])
        return author != actor and _is_reply_marker(m.get("content"))
    return False


def _compute_actor(
    chat_id: str, actor: str, display_name: str, msgs: list[dict[str, Any]]
) -> LedgerRow:
    given = [m for m in msgs if m["role"] == "user"
             and _actor_label(m.get("user_id"), m["session_id"]) == actor]
    tokens_given = sum(_words(m.get("content")) for m in given)

    tokens_received = sum(
        _words(m.get("content")) for m in msgs if _is_reply_for(actor, m)
    )

    # Latency + closure: for each actor message, the next reply-class message
    # in the same chat ordered by time.
    ordered = sorted(msgs, key=lambda m: (m["ts"], m["message_id"]))
    reply_flags = [_is_reply_for(actor, m) for m in ordered]
    given_idx = [
        i for i, m in enumerate(ordered)
        if m["role"] == "user"
        and _actor_label(m.get("user_id"), m["session_id"]) == actor
    ]

    latencies: list[float] = []
    threads = 0
    closed = 0
    for i in given_idx:
        threads += 1
        t0 = ordered[i]["ts"]
        for j in range(i + 1, len(ordered)):
            if reply_flags[j]:
                dt = float(ordered[j]["ts"]) - float(t0)
                latencies.append(dt)
                if dt <= CLOSURE_WINDOW_S:
                    closed += 1
                break

    closure_rate = (closed / threads) if threads else 0.0
    latency = float(median(latencies)) if latencies else None
    asymmetry = tokens_given / max(tokens_received, 1)
    drain = asymmetry * (1.0 - closure_rate)

    return LedgerRow(
        chat_id=chat_id,
        actor=actor,
        display_name=display_name,
        messages_given=len(given),
        tokens_given=tokens_given,
        tokens_received=tokens_received,
        response_latency_s=round(latency, 1) if latency is not None else None,
        closure_rate=round(closure_rate, 4),
        asymmetry=round(asymmetry, 4),
        drain_score=round(drain, 4),
    )
