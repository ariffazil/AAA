"""CLI entry point for the AAA P2P inner-loop server.

Usage:
    python -m AAA.p2p.run_p2p start 333
    python -m AAA.p2p.run_p2p start 555
    python -m AAA.p2p.run_p2p start 888
    python -m AAA.p2p.run_p2p verify /root/AAA/p2p/audit.jsonl

Stdlib only. Handles SIGINT for graceful shutdown.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import signal
import sys
from pathlib import Path

from .audit import verify_chain
from .protocol import ALLOWED_AGENTS
from .socket_server import P2PServer


def _setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


async def _serve(agent: str, socket_dir: Path, audit_path: Path) -> int:
    received: list[dict[str, object]] = []

    async def on_message(msg: dict[str, object]) -> None:
        received.append(msg)

    server = P2PServer(
        agent=agent,
        socket_dir=socket_dir,
        audit_path=audit_path,
        on_message=on_message,
    )
    loop = asyncio.get_running_loop()

    def _shutdown() -> None:
        server.stop()

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, _shutdown)
        except NotImplementedError:
            # Windows / restricted env — fall back to default behaviour.
            pass

    await server.start()
    return 0


def _cmd_start(args: argparse.Namespace) -> int:
    _setup_logging()
    return asyncio.run(
        _serve(args.agent, Path(args.socket_dir), Path(args.audit_path))
    )


def _cmd_verify(args: argparse.Namespace) -> int:
    ok, detail = verify_chain(args.audit_path)
    if ok:
        print(json.dumps({"ok": True, "path": args.audit_path, "detail": detail}))
        return 0
    print(
        json.dumps({"ok": False, "path": args.audit_path, "detail": detail}),
        file=sys.stderr,
    )
    return 1


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="run_p2p")
    sub = p.add_subparsers(dest="cmd", required=True)

    start = sub.add_parser("start", help="start a P2P server for one agent")
    start.add_argument("agent", choices=sorted(ALLOWED_AGENTS))
    start.add_argument(
        "--socket-dir", default="/tmp/aaa-p2p",
        help="directory for *.sock files (default /tmp/aaa-p2p)",
    )
    start.add_argument(
        "--audit-path", default="/root/AAA/p2p/audit.jsonl",
        help="path to the audit log",
    )
    start.set_defaults(func=_cmd_start)

    verify = sub.add_parser("verify", help="verify the audit hash chain")
    verify.add_argument("audit_path")
    verify.set_defaults(func=_cmd_verify)
    return p


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args) or 0)


if __name__ == "__main__":
    sys.exit(main())