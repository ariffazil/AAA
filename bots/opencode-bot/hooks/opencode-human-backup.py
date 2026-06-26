#!/usr/bin/env python3
"""HUMAN BACKUP — Auto-backup before any file edit. Silent. Fail-open."""
from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import hook_lib as h


def main() -> None:
    event = h.read_event()
    tool_name = event.get("tool_name", "unknown")
    tool_input = event.get("tool_input", {})
    session_id = event.get("session_id", "unknown")
    file_path = h.extract_file_path(tool_input) if tool_name in ("WriteFile", "StrReplaceFile") else ""

    if not file_path or not Path(file_path).exists():
        return

    backup_dir = Path(__file__).resolve().parent.parent / "backups" / session_id
    backup_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    backup_path = backup_dir / f"{Path(file_path).name}.bak.{timestamp}"
    try:
        shutil.copy2(file_path, backup_path)
        print(f"[Human Backup] Original saved to: {backup_path}")
    except Exception:
        pass


if __name__ == "__main__":
    main()
