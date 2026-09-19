"""Tests for AAA lib invocation_log — the Tuas 2 telemetry contract."""

from __future__ import annotations

import json
import time
from pathlib import Path

import pytest

import sys

sys.path.insert(0, "/root/AAA/lib")

from invocation_log import (  # noqa: E402
    exercise_count,
    instrument,
    log_invocation,
    timed,
)


def test_writes_one_json_line(tmp_path: Path):
    p = tmp_path / "inv.jsonl"
    assert log_invocation("WELL", "well_daily_checkin", actor_id="arif", path=p) is True
    lines = p.read_text().strip().splitlines()
    assert len(lines) == 1
    rec = json.loads(lines[0])
    assert rec["organ"] == "WELL"
    assert rec["tool"] == "well_daily_checkin"
    assert rec["actor_id"] == "arif"
    assert rec["ok"] is True
    assert rec["ts"].endswith("Z")


def test_creates_parent_dir(tmp_path: Path):
    p = tmp_path / "deep" / "nested" / "inv.jsonl"
    assert log_invocation("GEOX", "geox_claim", path=p) is True
    assert p.exists()


def test_never_raises_on_bad_path(tmp_path: Path):
    """Telemetry must never break the thing it measures."""
    blocked = tmp_path / "afile"
    blocked.write_text("x")
    # a directory path where a file is expected, under a file (impossible)
    bad = blocked / "nope" / "inv.jsonl"
    assert log_invocation("AAA", "t", path=bad) is False  # swallowed, not raised


def test_extra_filters_non_scalars(tmp_path: Path):
    p = tmp_path / "inv.jsonl"
    log_invocation("AAA", "t", extra={"rows": 5, "obj": {"a": 1}, "ok": True}, path=p)
    rec = json.loads(p.read_text().strip())
    assert rec["extra"] == {"rows": 5, "ok": True}  # dict dropped


def test_error_is_truncated(tmp_path: Path):
    p = tmp_path / "inv.jsonl"
    log_invocation("AAA", "t", error="x" * 5000, path=p)
    rec = json.loads(p.read_text().strip())
    assert len(rec["error"]) == 200


def test_append_only_ordering(tmp_path: Path):
    p = tmp_path / "inv.jsonl"
    for i in range(5):
        log_invocation("WELL", f"tool_{i}", path=p)
    tools = [json.loads(l)["tool"] for l in p.read_text().strip().splitlines()]
    assert tools == [f"tool_{i}" for i in range(5)]


def test_timed_logs_success_with_duration(tmp_path: Path):
    p = tmp_path / "inv.jsonl"
    with timed("arifFlow", "POST /ingest", actor_id="live-test", path=p) as ctx:
        ctx["extra"] = {"rows": 3}
    rec = json.loads(p.read_text().strip())
    assert rec["tool"] == "POST /ingest"
    assert rec["ok"] is True
    assert rec["extra"] == {"rows": 3}
    assert rec["duration_ms"] >= 0


def test_timed_logs_failure_and_reraises(tmp_path: Path):
    p = tmp_path / "inv.jsonl"
    with pytest.raises(ValueError):
        with timed("WELL", "boom", path=p):
            raise ValueError("nope")
    rec = json.loads(p.read_text().strip())
    assert rec["ok"] is False
    assert rec["error"] == "ValueError"


def test_instrument_decorator(tmp_path: Path):
    p = tmp_path / "inv.jsonl"

    @instrument("GEOX", path=p)
    def do_thing(x):
        return x * 2

    assert do_thing(3) == 6
    rec = json.loads(p.read_text().strip())
    assert rec["organ"] == "GEOX"
    assert rec["tool"] == "do_thing"
    assert rec["ok"] is True


# --- the readback that turns a proxy into a measurement -------------------


def test_exercise_count_distinct_tools_and_actors(tmp_path: Path):
    p = tmp_path / "inv.jsonl"
    log_invocation("AAA", "t1", actor_id="a", path=p)
    log_invocation("AAA", "t1", actor_id="b", path=p)
    log_invocation("AAA", "t2", actor_id="a", path=p)
    got = exercise_count("AAA", window_days=30, path=p)
    assert got["total"] == 3
    assert got["distinct_tools"] == 2
    assert got["distinct_actors"] == 2


def test_exercise_count_window_excludes_old(tmp_path: Path):
    p = tmp_path / "inv.jsonl"
    log_invocation("AAA", "new", path=p)
    old = {
        "ts": "2020-01-01T00:00:00Z",
        "organ": "AAA",
        "tool": "ancient",
        "actor_id": None,
        "ok": True,
        "epoch": time.time() - 999 * 86400,
    }
    with p.open("a") as fh:
        fh.write(json.dumps(old) + "\n")
    got = exercise_count("AAA", window_days=30, path=p)
    assert got["distinct_tools"] == 1
    assert got["total"] == 1


def test_exercise_count_counts_unparsable_not_silently(tmp_path: Path):
    """A log with corrupt lines is itself a finding."""
    p = tmp_path / "inv.jsonl"
    log_invocation("AAA", "good", path=p)
    with p.open("a") as fh:
        fh.write("this is not json\n")
    got = exercise_count("AAA", window_days=30, path=p)
    assert got["unparsable"] == 1
    assert got["distinct_tools"] == 1


def test_exercise_count_absent_log_says_so(tmp_path: Path):
    got = exercise_count("WELL", path=tmp_path / "nope.jsonl")
    assert got["total"] == 0
    assert "log absent" in got["note"]


def test_organ_filter(tmp_path: Path):
    p = tmp_path / "inv.jsonl"
    log_invocation("AAA", "t", path=p)
    log_invocation("WELL", "t", path=p)
    assert exercise_count("AAA", path=p)["total"] == 1
    assert exercise_count(None, path=p)["total"] == 2
    assert exercise_count(None, path=p)["organs_seen"] == ["AAA", "WELL"]


def test_format_matches_geox_precedent(tmp_path: Path):
    """Seven organs wire against this shape; it must not drift."""
    p = tmp_path / "inv.jsonl"
    log_invocation("GEOX", "geox_claim", actor_id="arif", duration_ms=1.5, session_id="S1", path=p)
    rec = json.loads(p.read_text().strip())
    for key in ("ts", "organ", "tool", "session_id", "actor_id", "ok", "duration_ms", "epoch"):
        assert key in rec, f"missing contract key: {key}"
