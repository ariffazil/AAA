"""
spec_lock.py — Lossless Constraint Persistence (INV-L3-PIN)
═══════════════════════════════════════════════════════════════════════════════

Task constraints live in an externalized SPEC.lock.json that NEVER enters the
context compression pool. After every context compaction, the agent MUST
re-read SPEC.lock.json before executing any file-write or bash action.

Schema:
{
  "version": 1,
  "task_id": str,
  "created_at": ISO8601,
  "updated_at": ISO8601,
  "constraints": {
    "locus":     [str],          # Allowed files/modules (glob patterns)
    "signal":    str,            # Target state / problem description
    "done":      [str],          # Acceptance criteria (verifiable)
    "done_v":    str,            # Exact verification command
    "negative":  [str],          # Explicit "do NOT touch" constraints
    "frozen":    [str],          # Files frozen at read-time (content-hash pinned)
  },
  "state": {
    "requires_spec_reread": bool,  # Set True after compaction
    "last_reread_at": ISO8601|null,
    "compaction_count": int,
  },
  "hash": str  # sha256 of constraints block (integrity check)
}

Governance:
  - Created at task start, never deleted during task
  - Updated only by explicit agent action (not auto-merge)
  - negative constraints are IMMUTABLE once set (append-only)
  - frozen files: content hash captured at read-time, mutation blocked if hash mismatch

DITEMPA BUKAN DIBERI ⚒️
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ── Configuration ────────────────────────────────────────────────────────────
_SPEC_LOCK_DIR = Path(
    os.environ.get(
        "ARIFOS_SPEC_LOCK_DIR",
        "/root/.local/share/arifos/state",
    )
)

SPEC_LOCK_FILENAME = "SPEC.lock.json"


# ── Schema ───────────────────────────────────────────────────────────────────


def _empty_spec(
    task_id: str,
    locus: list[str] | None = None,
    signal: str = "",
    done: list[str] | None = None,
    done_v: str = "",
    negative: list[str] | None = None,
) -> dict[str, Any]:
    """Create a new SPEC.lock.json with the mandatory four fields."""
    now = datetime.now(timezone.utc).isoformat()
    constraints = {
        "locus": locus or [],
        "signal": signal,
        "done": done or [],
        "done_v": done_v,
        "negative": negative or [],
        "frozen": [],
    }
    return {
        "version": 1,
        "task_id": task_id,
        "created_at": now,
        "updated_at": now,
        "constraints": constraints,
        "state": {
            "requires_spec_reread": False,
            "last_reread_at": None,
            "compaction_count": 0,
        },
        "hash": _hash_constraints(constraints),
    }


def _hash_constraints(constraints: dict[str, Any]) -> str:
    """Deterministic hash of the constraints block."""
    raw = json.dumps(constraints, sort_keys=True, default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


# ── File Operations ──────────────────────────────────────────────────────────


def spec_lock_path(task_id: str | None = None) -> Path:
    """Return path to SPEC.lock.json. Creates directory if needed."""
    _SPEC_LOCK_DIR.mkdir(parents=True, exist_ok=True)
    return _SPEC_LOCK_DIR / SPEC_LOCK_FILENAME


def create_spec_lock(
    task_id: str,
    locus: list[str] | None = None,
    signal: str = "",
    done: list[str] | None = None,
    done_v: str = "",
    negative: list[str] | None = None,
) -> dict[str, Any]:
    """Create and persist a new SPEC.lock.json.

    Returns the spec dict.
    """
    spec = _empty_spec(task_id, locus, signal, done, done_v, negative)
    path = spec_lock_path(task_id)
    path.write_text(json.dumps(spec, indent=2, default=str))
    return spec


def read_spec_lock() -> dict[str, Any] | None:
    """Read the current SPEC.lock.json. Returns None if not found."""
    path = spec_lock_path()
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return None


def mark_compaction() -> dict[str, Any] | None:
    """Mark that a context compaction just occurred.

    Sets requires_spec_reread = True and increments compaction_count.
    Returns updated spec, or None if no spec exists.
    """
    spec = read_spec_lock()
    if spec is None:
        return None

    now = datetime.now(timezone.utc).isoformat()
    spec["state"]["requires_spec_reread"] = True
    spec["state"]["compaction_count"] = spec["state"].get("compaction_count", 0) + 1
    spec["updated_at"] = now

    path = spec_lock_path()
    path.write_text(json.dumps(spec, indent=2, default=str))
    return spec


def mark_reread() -> dict[str, Any] | None:
    """Mark that SPEC.lock.json has been re-read after compaction.

    Sets requires_spec_reread = False and updates last_reread_at.
    Returns updated spec, or None if no spec exists.
    """
    spec = read_spec_lock()
    if spec is None:
        return None

    now = datetime.now(timezone.utc).isoformat()
    spec["state"]["requires_spec_reread"] = False
    spec["state"]["last_reread_at"] = now
    spec["updated_at"] = now

    path = spec_lock_path()
    path.write_text(json.dumps(spec, indent=2, default=str))
    return spec


def requires_reread() -> bool:
    """Check if SPEC.lock.json must be re-read before acting.

    Returns True if requires_spec_reread is True.
    """
    spec = read_spec_lock()
    if spec is None:
        return False
    return spec["state"].get("requires_spec_reread", False)


def check_locus(file_path: str) -> bool:
    """Check if a file path is within the declared locus.

    Returns True if allowed (no locus declared, or path matches).
    Returns False if explicitly outside locus.
    """
    import fnmatch

    spec = read_spec_lock()
    if spec is None:
        return True  # No spec = no locus restriction

    locus = spec["constraints"].get("locus", [])
    if not locus:
        return True  # Empty locus = unrestricted

    # Normalize path
    normalized = os.path.normpath(file_path)

    for pattern in locus:
        norm_pattern = os.path.normpath(pattern)
        if fnmatch.fnmatch(normalized, norm_pattern):
            return True
        # Directory pattern: "src/api/" matches "src/api/routes.py"
        if pattern.endswith("/") or pattern.endswith(os.sep):
            dir_prefix = norm_pattern.rstrip(os.sep) + os.sep
            if normalized.startswith(dir_prefix):
                return True
        # Also check basename match
        if fnmatch.fnmatch(os.path.basename(normalized), pattern):
            return True

    return False


def check_negative(file_path: str) -> bool:
    """Check if a file path is in the negative (do-not-touch) list.

    Returns True if the file IS in the negative list (should be BLOCKED).
    Returns False if the file is NOT in the negative list (allowed).
    """
    import fnmatch

    spec = read_spec_lock()
    if spec is None:
        return False

    negative = spec["constraints"].get("negative", [])
    if not negative:
        return False

    normalized = os.path.normpath(file_path)

    for pattern in negative:
        norm_pattern = os.path.normpath(pattern)
        if fnmatch.fnmatch(normalized, norm_pattern):
            return True
        # Directory pattern: "src/database/migrations/" matches files inside
        if pattern.endswith("/") or pattern.endswith(os.sep):
            dir_prefix = norm_pattern.rstrip(os.sep) + os.sep
            if normalized.startswith(dir_prefix):
                return True
        if fnmatch.fnmatch(os.path.basename(normalized), pattern):
            return True

    return False


def freeze_file(file_path: str) -> str | None:
    """Capture content hash of a file at read-time.

    Returns the hash string, or None if file doesn't exist.
    """
    path = Path(file_path)
    if not path.exists():
        return None

    content = path.read_bytes()
    file_hash = hashlib.sha256(content).hexdigest()[:16]

    spec = read_spec_lock()
    if spec is None:
        return file_hash

    frozen = spec["constraints"].get("frozen", [])
    entry = f"{file_path}:{file_hash}"
    if entry not in frozen:
        frozen.append(entry)
        spec["constraints"]["frozen"] = frozen
        spec["updated_at"] = datetime.now(timezone.utc).isoformat()
        lock_path = spec_lock_path()
        lock_path.write_text(json.dumps(spec, indent=2, default=str))

    return file_hash


def verify_frozen(file_path: str) -> bool:
    """Check if a frozen file's content hash still matches.

    Returns True if OK (no freeze, or hash matches).
    Returns False if hash MISMATCH (file was mutated while frozen).
    """
    spec = read_spec_lock()
    if spec is None:
        return True

    frozen = spec["constraints"].get("frozen", [])
    for entry in frozen:
        if ":" not in entry:
            continue
        path_str, expected_hash = entry.rsplit(":", 1)
        if os.path.normpath(file_path) == os.path.normpath(path_str):
            # Check current hash
            path = Path(file_path)
            if not path.exists():
                return False  # Frozen file was deleted
            current_hash = hashlib.sha256(path.read_bytes()).hexdigest()[:16]
            return current_hash == expected_hash

    return True  # Not frozen = OK


def validate_spec_integrity() -> bool:
    """Verify the stored hash matches the current constraints.

    Returns True if integrity is OK.
    """
    spec = read_spec_lock()
    if spec is None:
        return False

    expected = _hash_constraints(spec["constraints"])
    return spec.get("hash") == expected
