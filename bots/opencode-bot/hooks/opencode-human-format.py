#!/usr/bin/env python3
"""HUMAN FORMAT — Auto-format after file edits. Silent on failure."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import hook_lib as h


def main() -> None:
    event = h.read_event()
    tool_name = event.get("tool_name", "unknown")
    tool_input = event.get("tool_input", {})
    file_path = h.extract_file_path(tool_input) if tool_name in ("WriteFile", "StrReplaceFile") else ""

    if not file_path or not Path(file_path).exists():
        return

    formatted = False
    msg = ""
    p = Path(file_path)

    if p.suffix == ".py":
        if shutil.which("black"):
            try:
                subprocess.run(["black", "-q", str(p)], check=True, capture_output=True, timeout=30)
                formatted = True
                msg = "Auto-formatted with black"
            except Exception:
                pass
        if not formatted and shutil.which("ruff"):
            try:
                subprocess.run(["ruff", "format", "-q", str(p)], check=True, capture_output=True, timeout=30)
                formatted = True
                msg = "Auto-formatted with ruff"
            except Exception:
                pass
    elif p.suffix in (".ts", ".tsx", ".js", ".jsx"):
        if shutil.which("prettier"):
            try:
                subprocess.run(
                    ["prettier", "--write", "--log-level=error", str(p)],
                    check=True,
                    capture_output=True,
                    timeout=30,
                )
                formatted = True
                msg = "Auto-formatted with prettier"
            except Exception:
                pass
    elif p.suffix == ".toml":
        if shutil.which("taplo"):
            try:
                subprocess.run(["taplo", "format", str(p)], check=True, capture_output=True, timeout=30)
                formatted = True
                msg = "Auto-formatted with taplo"
            except Exception:
                pass
    elif p.suffix == ".sh":
        if shutil.which("shfmt"):
            try:
                subprocess.run(["shfmt", "-w", str(p)], check=True, capture_output=True, timeout=30)
                formatted = True
                msg = "Auto-formatted with shfmt"
            except Exception:
                pass

    if formatted:
        print(f"[Human Format] {msg}: {file_path}")


if __name__ == "__main__":
    main()
