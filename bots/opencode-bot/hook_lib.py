"""
hook_lib.py — Shared helpers for opencode-bot constitutional hooks.
Owner: arif
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

# Writable under opencode-bot.service hardening
CACHE_DIR = Path(os.environ.get("OPENCODE_CACHE_DIR", "/root/.hermes/cache/opencode-bot"))
AUDIT_LOG = CACHE_DIR / "mcp-audit.jsonl"
TELEMETRY_DIR = CACHE_DIR / "telemetry"
SUMMARY_DIR = Path(__file__).resolve().parent / "session-summaries"

TIER_A_PAT = re.compile(
    r"server\.py|constitutional_map\.py|tool_registry\.json|mcp-arifos\.json|"
    r"pyproject\.toml|Dockerfile|docker-compose\.yml|AGENTS\.md|monolith\.py|"
    r"cli\.ts|AgentEngine\.ts",
    re.IGNORECASE,
)
CONSTITUTIONAL_PAT = re.compile(r"FLOORS|constitutional|000/|arifOS/000", re.IGNORECASE)


def ensure_dirs() -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    TELEMETRY_DIR.mkdir(parents=True, exist_ok=True)
    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)


def read_event() -> dict[str, Any]:
    try:
        return json.loads(sys.stdin.read())
    except Exception:
        return {}


def write_output(payload: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(payload, indent=2))
    sys.stdout.flush()


def allow(
    event: str,
    reason: str,
    metadata: Optional[dict[str, Any]] = None,
) -> None:
    write_output(
        {
            "hookSpecificOutput": {
                "hookEventName": event,
                "permissionDecision": "allow",
                "permissionDecisionReason": reason,
                "metadata": metadata or {},
            }
        }
    )


def deny(
    event: str,
    reason: str,
    metadata: Optional[dict[str, Any]] = None,
) -> None:
    write_output(
        {
            "hookSpecificOutput": {
                "hookEventName": event,
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
                "metadata": metadata or {},
            }
        }
    )


def audit_log(record: dict[str, Any]) -> None:
    ensure_dirs()
    line = json.dumps(record, default=str)
    try:
        with AUDIT_LOG.open("a") as f:
            f.write(line + "\n")
    except Exception as exc:
        # fail-open for audit: log to stderr but don't crash
        print(f"[hook_lib] audit log failed: {exc}", file=sys.stderr)


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def extract_command(tool_input: dict[str, Any]) -> str:
    return tool_input.get("command", "")


def extract_file_path(tool_input: dict[str, Any]) -> str:
    return tool_input.get("file_path", "")


def sha256_file(path: str) -> str:
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return "unknown"


def git_diff_stat(file_path: str) -> str:
    try:
        p = Path(file_path)
        result = subprocess.run(
            ["git", "diff", "--stat", p.name],
            cwd=p.parent,
            capture_output=True,
            text=True,
            timeout=3,
        )
        return result.stdout.strip().splitlines()[-1].strip() if result.stdout else ""
    except Exception:
        return ""


def detect_repo(path_or_cmd: str) -> str:
    s = path_or_cmd.lower()
    if "arifos" in s:
        return "arifOS"
    if "a-forge" in s or "a_forge" in s:
        return "A-FORGE"
    if "geox" in s:
        return "geox"
    if "wealth" in s:
        return "WEALTH"
    if "well" in s:
        return "WELL"
    return "unknown"


def unique_repos(text: str) -> set[str]:
    return set(re.findall(r"arifOS|A-FORGE|A_FORGE|geox|GEOX|WEALTH|wealth|WELL|well", text))


def is_tier_a(path: str) -> bool:
    return bool(TIER_A_PAT.search(path))


def is_constitutional(path: str) -> bool:
    return bool(CONSTITUTIONAL_PAT.search(path))


def chaos_band(delta_s: float) -> tuple[str, bool, str]:
    if delta_s < 0.25:
        return "green", False, "CLAIM"
    if delta_s < 0.55:
        return "yellow", False, "PLAUSIBLE"
    if delta_s < 0.80:
        return "orange", True, "PLAUSIBLE"
    return "red", True, "CLAIM"


def compute_delta_pre(
    files_score: float,
    spread_score: float,
    churn_score: float,
    canonical_score: float,
    irreversibility_score: float,
) -> float:
    return round(
        0.25 * files_score
        + 0.20 * spread_score
        + 0.25 * churn_score
        + 0.20 * canonical_score
        + 0.10 * irreversibility_score,
        4,
    )
