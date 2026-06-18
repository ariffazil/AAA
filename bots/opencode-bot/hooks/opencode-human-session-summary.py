#!/usr/bin/env python3
"""HUMAN SESSION SUMMARY — Plain English recap for Arif."""
from __future__ import annotations

import socket
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import hook_lib as h


def main() -> None:
    event = h.read_event()
    session_id = event.get("session_id", "unknown")
    cwd = event.get("cwd", "/root")
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    summary_file = h.SUMMARY_DIR / f"{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.txt"
    summary_file.parent.mkdir(parents=True, exist_ok=True)
    with summary_file.open("a") as f:
        f.write("\n")
        f.write("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        f.write(f"Session ended: {timestamp}\n")
        f.write(f"Host:         {socket.gethostname()}\n")
        f.write(f"Working dir:  {cwd}\n")
        f.write(f"Session ID:   {session_id}\n")
        f.write("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        f.write("\n")
    print(f"[Human Summary] Session recap saved to: {summary_file}")


if __name__ == "__main__":
    main()
