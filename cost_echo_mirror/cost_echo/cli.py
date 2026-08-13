"""argparse CLI for cost-echo.

Subcommands:
  ledger  — print ledger rows (JSON default, --table for aligned text)
  signal  — per-relationship green/yellow/red with one-line reason
  report  — full markdown report (ledger + signals + top-5 most asymmetric)

All output is deterministic. No timestamps unless --with-timestamp is given.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from . import __version__
from .db import DEFAULT_DB_PATH, fetch_messages
from .ledger import LedgerRow, compute_ledger
from .signal import Thresholds, Signal, classify_all

ADVISORY_HEADER = "ADVISORY ONLY — F13 decides. Never auto-act."

_LEDGER_COLS = [
    ("actor", "ACTOR"),
    ("chat_id", "CHAT"),
    ("messages_given", "MSG"),
    ("tokens_given", "GIVEN"),
    ("tokens_received", "RECV"),
    ("response_latency_s", "LAT(s)"),
    ("closure_rate", "CLOS"),
    ("asymmetry", "ASYM"),
    ("drain_score", "DRAIN"),
]


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="cost-echo",
        description=(
            "Read-only human relational energy asymmetry mirror. "
            + ADVISORY_HEADER
        ),
    )
    p.add_argument("--version", action="version", version=f"cost-echo {__version__}")
    p.add_argument("--db", default=DEFAULT_DB_PATH, help="SQLite DB path (read-only)")
    p.add_argument("--green-drain", type=float, default=0.8,
                   help="green if drain_score below this (default 0.8)")
    p.add_argument("--green-closure", type=float, default=0.6,
                   help="green also needs closure_rate >= this (default 0.6)")
    p.add_argument("--yellow-drain", type=float, default=2.0,
                   help="yellow if drain_score below this (default 2.0)")

    sub = p.add_subparsers(dest="command", required=True)

    pl = sub.add_parser("ledger", help="print energy ledger rows")
    pl.add_argument("--chat-id", default=None)
    pl.add_argument("--min-messages", type=int, default=1)
    pl.add_argument("--table", action="store_true", help="aligned text output")
    pl.add_argument("--with-timestamp", action="store_true",
                    help="include generated-at timestamp in output")

    ps = sub.add_parser("signal", help="green/yellow/red per relationship")
    ps.add_argument("--chat-id", default=None)
    ps.add_argument("--min-messages", type=int, default=1)
    ps.add_argument("--table", action="store_true")
    ps.add_argument("--with-timestamp", action="store_true")

    pr = sub.add_parser("report", help="full markdown report")
    pr.add_argument("--chat-id", default=None)
    pr.add_argument("--min-messages", type=int, default=1)
    pr.add_argument("--with-timestamp", action="store_true")
    return p


def _thresholds(args: argparse.Namespace) -> Thresholds:
    return Thresholds(
        green_drain=args.green_drain,
        green_closure=args.green_closure,
        yellow_drain=args.yellow_drain,
    )


def _load(args: argparse.Namespace) -> list[LedgerRow]:
    msgs = fetch_messages(args.db)
    return compute_ledger(
        msgs, chat_id=args.chat_id, min_messages=args.min_messages
    )


def _stamp(args: argparse.Namespace) -> dict[str, Any]:
    if getattr(args, "with_timestamp", False):
        import datetime

        return {
            "generated_at": datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat()
        }
    return {}


def _print_table(rows: list[LedgerRow]) -> None:
    data = []
    for r in rows:
        d = r.to_dict()
        d["response_latency_s"] = (
            "-" if d["response_latency_s"] is None else d["response_latency_s"]
        )
        data.append(d)
    widths = []
    for key, header in _LEDGER_COLS:
        w = max([len(header)] + [len(str(d[key])) for d in data]) if data else len(header)
        widths.append(w)
    print("  ".join(h.ljust(w) for (_, h), w in zip(_LEDGER_COLS, widths)))
    for d in data:
        print("  ".join(str(d[k]).ljust(w) for (k, _), w in zip(_LEDGER_COLS, widths)))


def _cmd_ledger(args: argparse.Namespace) -> int:
    rows = _load(args)
    if args.table:
        _print_table(rows)
    else:
        payload = {"advisory": ADVISORY_HEADER, **_stamp(args),
                   "rows": [r.to_dict() for r in rows]}
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def _cmd_signal(args: argparse.Namespace) -> int:
    rows = _load(args)
    signals = classify_all(rows, _thresholds(args))
    if args.table:
        for s in signals:
            print(f"{s.level.upper():6s}  {s.display_name} ({s.actor}) "
                  f"[chat {s.chat_id}] — {s.reason}")
    else:
        payload = {"advisory": ADVISORY_HEADER, **_stamp(args),
                   "signals": [s.to_dict() for s in signals]}
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    if not signals:
        print("no relationships found", file=sys.stderr)
    return 0


def _md_table(headers: list[str], body: list[list[Any]]) -> list[str]:
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join("---" for _ in headers) + "|"]
    for row in body:
        out.append("| " + " | ".join(str(c) for c in row) + " |")
    return out


def _cmd_report(args: argparse.Namespace) -> int:
    rows = _load(args)
    signals = classify_all(rows, _thresholds(args))
    stamp = _stamp(args)

    lines: list[str] = [
        "# cost-echo report",
        "",
        f"**{ADVISORY_HEADER}**",
        "",
        "Read-only mirror of human relational energy asymmetry "
        "(energy given vs energy returned). Advisory only; data is "
        "human-relational and stays sovereign-owned.",
        "",
    ]
    if stamp:
        lines += [f"Generated: {stamp['generated_at']}", ""]

    counts = {"green": 0, "yellow": 0, "red": 0}
    for s in signals:
        counts[s.level] += 1
    lines += [
        "## Signal summary",
        "",
        f"- green: {counts['green']}",
        f"- yellow: {counts['yellow']}",
        f"- red: {counts['red']}",
        "",
        "## Signals",
        "",
    ]
    lines += _md_table(
        ["level", "actor", "chat", "reason"],
        [[s.level, s.display_name, s.chat_id, s.reason] for s in signals],
    )
    lines += ["", "## Ledger", ""]
    lines += _md_table(
        ["actor", "chat", "msgs", "given", "received", "latency_s",
         "closure", "asymmetry", "drain"],
        [[r.display_name, r.chat_id, r.messages_given, r.tokens_given,
          r.tokens_received,
          "-" if r.response_latency_s is None else r.response_latency_s,
          r.closure_rate, r.asymmetry, r.drain_score] for r in rows],
    )
    top = sorted(rows, key=lambda r: (-r.asymmetry, r.actor, r.chat_id))[:5]
    lines += ["", "## Top 5 most asymmetric relationships", ""]
    if top:
        lines += _md_table(
            ["actor", "chat", "asymmetry", "drain", "closure"],
            [[r.display_name, r.chat_id, r.asymmetry, r.drain_score,
              r.closure_rate] for r in top],
        )
    else:
        lines.append("_none_")
    lines += ["", "---", f"_{ADVISORY_HEADER}_"]
    print("\n".join(lines))
    return 0


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    handler = {
        "ledger": _cmd_ledger,
        "signal": _cmd_signal,
        "report": _cmd_report,
    }[args.command]
    return handler(args)


if __name__ == "__main__":
    sys.exit(main())
