#!/usr/bin/env python3
"""Tests for employment-coverage-monitor.py — the ATTENTION-MODE ratchet.

Run:  python3 -m pytest /root/AAA/tests/test_enforcement_coverage_monitor.py -q

The monitor's filename has hyphens (it is a CLI, not a package module), so it
is loaded by path rather than imported.

What is actually being proven here:
  * first run establishes a BASELINE and does NOT scream 30 false alarms
  * a genuinely new ungated path is caught            (the postern opening)
  * a removed path is credited as CLOSED, permanently (the ratchet)
  * running twice over unchanged readings yields ZERO new findings
  * a malformed reading never raises and never earns a CLOSED credit
  * the monitor never writes into the readings dir and never blocks (exit 0)
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

MONITOR_PATH = Path("/root/AAA/scripts/enforcement-coverage-monitor.py")


@pytest.fixture(scope="module")
def monitor():
    assert MONITOR_PATH.exists(), f"monitor missing at {MONITOR_PATH}"
    spec = importlib.util.spec_from_file_location("enforcement_coverage_monitor", MONITOR_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --------------------------------------------------------------------------
# fixtures / helpers
# --------------------------------------------------------------------------
def make_reading(organ, ungated, gated, total, observed="2026-09-19T12:00:00+08:00"):
    """One schema-shaped asabiyyah reading."""
    return {
        "reading_version": 1,
        "organ": organ,
        "host": "forge",
        "observed_at": observed,
        "metrics": {
            "enc": {
                "name": "enc",
                "value": round(gated / total, 4) if total else None,
                "state": "MEASURED" if total else "NOT_APPLICABLE",
                "source": "test fixture",
                "observed_at": observed,
            }
        },
        "evidence": {
            "gated_paths": gated,
            "total_paths": total,
            "ungated": list(ungated),
        },
    }


def write_reading(readings_dir: Path, organ: str, ungated, gated, total):
    p = readings_dir / f"{organ}.json"
    p.write_text(json.dumps(make_reading(organ, ungated, gated, total), indent=2), encoding="utf-8")
    return p


def baseline_organs(readings_dir: Path):
    """Two organs, 3 ungated paths total."""
    write_reading(readings_dir, "AAA", ["filesystem-direct-write", "git-commit-no-verify"], 3, 6)
    write_reading(readings_dir, "WELL", ["well_log"], 5, 21)


def run(monitor, readings_dir, register, findings, capsys, *extra):
    code = monitor.main(
        [
            "--readings-dir", str(readings_dir),
            "--register", str(register),
            "--findings", str(findings),
            *extra,
        ]
    )
    out = capsys.readouterr().out
    return code, out


def report(monitor, readings_dir, register, findings, capsys, *extra):
    code, out = run(monitor, readings_dir, register, findings, capsys, "--json", *extra)
    return code, json.loads(out)


def ledger(findings: Path):
    if not findings.exists():
        return []
    rows = []
    for line in findings.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def deltas(findings: Path):
    return [r for r in ledger(findings) if r.get("kind") == "DELTA"]


@pytest.fixture()
def env(tmp_path):
    readings = tmp_path / "asabiyyah"
    readings.mkdir()
    return {
        "readings": readings,
        "register": tmp_path / "enforcement-coverage-register.json",
        "findings": tmp_path / "metrics" / "enforcement-coverage-findings.jsonl",
    }


# --------------------------------------------------------------------------
# 1. baseline — the decisive requirement
# --------------------------------------------------------------------------
def test_first_run_is_baseline_not_alarm(monitor, env, capsys):
    baseline_organs(env["readings"])
    code, rep = report(monitor, env["readings"], env["register"], env["findings"], capsys)

    assert code == 0, "attention mode must exit 0"
    assert rep["bootstrap"] is True
    assert rep["new_ungated_count"] == 0, "a first run must not report the baseline as new alarms"
    assert rep["closed_count"] == 0
    assert rep["totals"]["organs"] == 2
    assert rep["totals"]["ungated_paths"] == 3
    assert env["register"].exists()
    reg = json.loads(env["register"].read_text())
    assert reg["register_version"] == 1
    assert reg["mode"] == "ATTENTION"
    assert len(reg["paths"]) == 3
    assert all(r["status"] == "OPEN" for r in reg["paths"].values())
    # the baseline is recorded as an event, with new_ungated explicitly 0
    base = [r for r in ledger(env["findings"]) if r["kind"] == "BASELINE"]
    assert len(base) == 1
    assert base[0]["new_ungated"] == 0
    assert base[0]["baseline_ungated"] == 3
    assert deltas(env["findings"]) == []


def test_baseline_runs_on_the_eight_live_readings_without_alarm(monitor, tmp_path, capsys):
    """Same guarantee against the real /var/lib/arifos/asabiyyah readings."""
    live = Path("/var/lib/arifos/asabiyyah")
    if not live.exists() or not list(live.glob("*.json")):
        pytest.skip("live readings not present on this host")
    code, rep = report(monitor, live, tmp_path / "r.json", tmp_path / "f.jsonl", capsys)
    assert code == 0
    assert rep["bootstrap"] is True
    assert rep["new_ungated_count"] == 0
    assert rep["totals"]["organs"] == 8
    assert rep["totals"]["ungated_paths"] > 0


# --------------------------------------------------------------------------
# 2. NEW_UNGATED — a postern opens
# --------------------------------------------------------------------------
def test_new_ungated_path_is_detected(monitor, env, capsys):
    baseline_organs(env["readings"])
    report(monitor, env["readings"], env["register"], env["findings"], capsys)

    write_reading(
        env["readings"], "AAA",
        ["filesystem-direct-write", "git-commit-no-verify", "posix-bash-redirect"],
        2, 6,
    )
    code, rep = report(monitor, env["readings"], env["register"], env["findings"], capsys)

    assert code == 0, "finding a new postern must still not block anything"
    assert rep["bootstrap"] is False
    assert rep["new_ungated_count"] == 1
    assert rep["new_ungated"][0]["path"] == "posix-bash-redirect"
    assert rep["new_ungated"][0]["organ"] == "AAA"
    assert rep["new_ungated"][0]["classification"] == "NEW_UNGATED"
    assert rep["new_ungated"][0]["reopened"] is False
    assert rep["new_ungated"][0]["severity"] == "HIGH"

    d = deltas(env["findings"])
    assert [r["class"] for r in d] == ["NEW_UNGATED"]
    assert d[0]["path"] == "posix-bash-redirect"


def test_coverage_regression_is_visible_in_ratchet(monitor, env, capsys):
    """Adding an ungated path lowers coverage; worst-ever must be kept forever."""
    baseline_organs(env["readings"])
    _, first = report(monitor, env["readings"], env["register"], env["findings"], capsys)
    assert first["organs"]["AAA"]["enc"] == pytest.approx(3 / 6)

    write_reading(env["readings"], "AAA", ["a", "b", "c"], 1, 6)  # coverage 1/6
    _, second = report(monitor, env["readings"], env["register"], env["findings"], capsys)
    assert second["organs"]["AAA"]["enc"] == pytest.approx(1 / 6)
    assert second["organs"]["AAA"]["ratchet"]["min_enc_seen"] == pytest.approx(1 / 6)

    write_reading(env["readings"], "AAA", ["a"], 5, 6)  # recovery
    _, third = report(monitor, env["readings"], env["register"], env["findings"], capsys)
    assert third["organs"]["AAA"]["enc"] == pytest.approx(5 / 6)
    # the bad day is not averaged away
    assert third["organs"]["AAA"]["ratchet"]["min_enc_seen"] == pytest.approx(1 / 6)
    assert third["organs"]["AAA"]["ratchet"]["max_ungated_seen"] >= 3
    assert third["closed_count"] == 2


# --------------------------------------------------------------------------
# 3. CLOSED — credit, and the ratchet remembers
# --------------------------------------------------------------------------
def test_closed_path_is_credited_and_retained(monitor, env, capsys):
    baseline_organs(env["readings"])
    report(monitor, env["readings"], env["register"], env["findings"], capsys)

    # git-commit-no-verify is now gated -> the postern shut
    write_reading(env["readings"], "AAA", ["filesystem-direct-write"], 4, 6)
    code, rep = report(monitor, env["readings"], env["register"], env["findings"], capsys)

    assert code == 0
    assert rep["closed_count"] == 1
    assert rep["closed"][0]["path"] == "git-commit-no-verify"
    assert rep["new_ungated_count"] == 0

    reg = json.loads(env["register"].read_text())
    closed_key = "AAA|git-commit-no-verify"
    assert closed_key not in reg["paths"], "a closed postern must leave the open ledger"
    assert closed_key in reg["closed"], "a closed postern must be remembered forever"
    assert reg["closed"][closed_key]["credited"] is True
    assert reg["closed"][closed_key]["status"] == "CLOSED"

    assert [r["class"] for r in deltas(env["findings"])] == ["CLOSED"]


def test_reopened_path_is_flagged_not_treated_as_neutral(monitor, env, capsys):
    baseline_organs(env["readings"])
    report(monitor, env["readings"], env["register"], env["findings"], capsys)
    write_reading(env["readings"], "AAA", ["filesystem-direct-write"], 4, 6)   # closed
    report(monitor, env["readings"], env["register"], env["findings"], capsys)
    write_reading(env["readings"], "AAA", ["filesystem-direct-write", "git-commit-no-verify"], 3, 6)
    _, rep = report(monitor, env["readings"], env["register"], env["findings"], capsys)

    assert rep["new_ungated_count"] == 1
    row = rep["new_ungated"][0]
    assert row["path"] == "git-commit-no-verify"
    assert row["reopened"] is True, "re-opening a credited postern must be called out"
    reg = json.loads(env["register"].read_text())
    assert "AAA|git-commit-no-verify" not in reg["closed"]


# --------------------------------------------------------------------------
# 4. idempotency
# --------------------------------------------------------------------------
def test_second_run_over_unchanged_readings_reports_nothing(monitor, env, capsys):
    baseline_organs(env["readings"])
    report(monitor, env["readings"], env["register"], env["findings"], capsys)
    write_reading(env["readings"], "WELL", ["well_log", "well_daily_checkin"], 5, 21)
    _, r2 = report(monitor, env["readings"], env["register"], env["findings"], capsys)
    assert r2["new_ungated_count"] == 1  # well_daily_checkin is genuinely new
    d_before = len(deltas(env["findings"]))

    _, r3 = report(monitor, env["readings"], env["register"], env["findings"], capsys)
    _, r4 = report(monitor, env["readings"], env["register"], env["findings"], capsys)

    for r in (r3, r4):
        assert r["bootstrap"] is False
        assert r["new_ungated_count"] == 0
        assert r["closed_count"] == 0
        assert r["new_ungated"] == []
        assert r["closed"] == []
        assert r["ratchet_changed"] is False

    assert len(deltas(env["findings"])) == d_before, "no new DELTA lines on an unchanged rerun"
    assert r3["ratchet_hash"] == r4["ratchet_hash"] == r2["ratchet_hash"]
    assert r3["unchanged_count"] == r4["unchanged_count"] == 4  # AAA:2 + WELL:2

    # The register's change-defining content is stable across runs. Only
    # liveness counters (last_seen/times_seen) and run telemetry advance --
    # that is what makes the ratchet checkable rather than merely asserted.
    # paths/organs are compared below in stripped form, so they are excluded
    # from the top-level scalar comparison.
    volatile_top = {"generated_at", "run_count", "paths", "organs"}

    def substantive(path: Path):
        d = json.loads(path.read_text())
        top = {k: v for k, v in d.items() if k not in volatile_top}
        paths = {
            k: {kk: vv for kk, vv in r.items() if kk not in ("last_seen", "times_seen")}
            for k, r in d["paths"].items()
        }
        organs = {}
        for o, r in d["organs"].items():
            row = {kk: vv for kk, vv in r.items() if kk != "last_change_at"}
            row["ratchet"] = {
                kk: vv for kk, vv in (r.get("ratchet") or {}).items() if kk != "last_change_at"
            }
            organs[o] = row
        return top, paths, organs, d["closed"], d["totals"]

    before = substantive(env["register"])
    _, r5 = report(monitor, env["readings"], env["register"], env["findings"], capsys)
    after = substantive(env["register"])

    assert before == after, "unchanged readings must not move anything but the run counters"
    assert before[0]["ratchet_hash"] == after[0]["ratchet_hash"] == r5["ratchet_hash"]
    # run_count is the one thing that must advance: it is the witness that the
    # monitor actually ran (no data is not the same as all clear).
    live_register = json.loads(env["register"].read_text())
    assert live_register["run_count"] == r5["run_count"]
    assert live_register["run_count"] > 1
    assert live_register["prev_ratchet_hash"] == r5["ratchet_hash"], (
        "an unchanged run must record the same ratchet hash it inherited"
    )


def test_run_heartbeat_is_appended_every_run_but_is_not_a_finding(monitor, env, capsys):
    baseline_organs(env["readings"])
    report(monitor, env["readings"], env["register"], env["findings"], capsys)
    report(monitor, env["readings"], env["register"], env["findings"], capsys)
    rows = ledger(env["findings"])
    runs = [r for r in rows if r["kind"] == "RUN"]
    assert len(runs) == 2, "a run ledger entry proves the monitor ran (no data != all clear)"
    assert runs[-1]["new_ungated"] == 0
    assert deltas(env["findings"]) == []


# --------------------------------------------------------------------------
# 5. malformed input — never raises, never earns a credit
# --------------------------------------------------------------------------
def test_malformed_readings_never_raise_and_stay_out_of_the_diff(monitor, env, capsys):
    baseline_organs(env["readings"])
    report(monitor, env["readings"], env["register"], env["findings"], capsys)

    (env["readings"] / "GEOX.json").write_text("{ this is not json", encoding="utf-8")
    (env["readings"] / "broken2.json").write_text("[]", encoding="utf-8")
    (env["readings"] / "HERMES.json").write_text(
        json.dumps({"organ": "NOPE", "evidence": {}}), encoding="utf-8"
    )
    (env["readings"] / "WEALTH.json").write_text(
        json.dumps({"organ": "WEALTH", "evidence": {"gated_paths": 1, "total_paths": 4, "ungated": "oops"}}),
        encoding="utf-8",
    )

    code, rep = report(monitor, env["readings"], env["register"], env["findings"], capsys)
    assert code == 0
    assert isinstance(rep, dict)
    reasons = " ".join(m["reason"] for m in rep["malformed_readings"])
    assert "bad_json" in reasons
    assert "not_an_object" in reasons
    assert "unknown_organ" in reasons
    assert "ungated_not_a_list" in reasons
    # malformed organ readings must not be read as "its posterns closed"
    assert rep["closed_count"] == 0
    assert rep["new_ungated_count"] == 0


def test_missing_reading_carries_state_forward_not_closed(monitor, env, capsys):
    baseline_organs(env["readings"])
    report(monitor, env["readings"], env["register"], env["findings"], capsys)

    (env["readings"] / "WELL.json").unlink()  # probe broke / not published
    code, rep = report(monitor, env["readings"], env["register"], env["findings"], capsys)

    assert code == 0
    assert "WELL" in rep["stale_organs"]
    assert rep["organs"]["WELL"]["stale_carried_forward"] is True
    assert rep["closed_count"] == 0, "a missing reading is not a closed postern"
    reg = json.loads(env["register"].read_text())
    assert "WELL|well_log" in reg["paths"], "carried-forward rows stay open"


# --------------------------------------------------------------------------
# 6. read-only + never blocks
# --------------------------------------------------------------------------
def test_readings_are_never_modified(monitor, env, capsys):
    baseline_organs(env["readings"])
    before = {p.name: p.read_bytes() for p in sorted(env["readings"].glob("*"))}
    # several runs, including one that finds a change, must leave readings alone
    report(monitor, env["readings"], env["register"], env["findings"], capsys)
    write_reading(env["readings"], "WELL", ["well_log", "well_new"], 5, 21)
    report(monitor, env["readings"], env["register"], env["findings"], capsys)
    after_change = {p.name: p.read_bytes() for p in sorted(env["readings"].glob("*"))}

    assert set(after_change) == set(before), "the monitor must not create files in the readings dir"
    assert after_change["AAA.json"] == before["AAA.json"], "untouched reading must be byte-identical"
    assert after_change["WELL.json"] != before["WELL.json"], "the fixture rewrite is the only writer"

    # with no further fixture writes, a run is byte-neutral against the readings
    report(monitor, env["readings"], env["register"], env["findings"], capsys)
    final = {p.name: p.read_bytes() for p in sorted(env["readings"].glob("*"))}
    assert final == after_change


def test_dry_run_writes_nothing(monitor, env, capsys):
    baseline_organs(env["readings"])
    report(monitor, env["readings"], env["register"], env["findings"], capsys)
    size_before = env["findings"].stat().st_size
    reg_before = env["register"].read_bytes()

    report(monitor, env["readings"], env["register"], env["findings"], capsys, "--dry-run")
    assert env["findings"].stat().st_size == size_before
    assert env["register"].read_bytes() == reg_before


def test_refuses_to_write_outside_state_root_or_tempdir(monitor, env, capsys):
    baseline_organs(env["readings"])
    code = monitor.main(
        [
            "--readings-dir", str(env["readings"]),
            "--register", "/root/AAA/evil-register.json",
            "--findings", str(env["findings"]),
        ]
    )
    assert code == 3, "must refuse to write into an organ repo"
    assert not Path("/root/AAA/evil-register.json").exists()


def test_strict_exit_is_opt_in_only(monitor, env, capsys):
    """Default must never signal failure; escalation is a deliberate flag."""
    baseline_organs(env["readings"])
    report(monitor, env["readings"], env["register"], env["findings"], capsys)
    write_reading(env["readings"], "AAA", ["a", "b", "c", "d"], 2, 6)

    code, _ = run(monitor, env["readings"], env["register"], env["findings"], capsys)
    assert code == 0, "attention mode exits 0 even with new posterns"

    # a second change, this time observed with the opt-in flag
    write_reading(env["readings"], "AAA", ["a", "b", "c", "d", "e"], 2, 6)
    code2, _ = run(
        monitor, env["readings"], env["register"], env["findings"], capsys, "--strict-exit"
    )
    assert code2 == 1, "--strict-exit is the only thing that may ever return nonzero"

    # and once the change is registered, even strict-exit returns to 0
    code3, _ = run(
        monitor, env["readings"], env["register"], env["findings"], capsys, "--strict-exit"
    )
    assert code3 == 0


def test_reset_baseline_is_explicit_and_rebaselines(monitor, env, capsys):
    baseline_organs(env["readings"])
    report(monitor, env["readings"], env["register"], env["findings"], capsys)
    write_reading(env["readings"], "AAA", ["x", "y", "z"], 2, 6)

    _, rep = report(monitor, env["readings"], env["register"], env["findings"], capsys, "--reset-baseline")
    assert rep["bootstrap"] is True
    assert rep["new_ungated_count"] == 0
    assert rep["bootstrap_reason"] == "reset_baseline_requested"


def test_long_multiline_paths_are_canonicalised(monitor, env, capsys):
    """The live readings carry paragraph-long paths; whitespace must not churn identity."""
    baseline_organs(env["readings"])
    long_path = "outbound_chat_send: the agent's final reply reaches the chat channel\n  after the tool loop; no gate observes the send"
    write_reading(env["readings"], "AAA", ["filesystem-direct-write", long_path], 3, 6)
    report(monitor, env["readings"], env["register"], env["findings"], capsys)

    write_reading(env["readings"], "AAA", ["filesystem-direct-write", "outbound_chat_send: the agent's final reply reaches the chat channel after the tool loop; no gate observes the send"], 3, 6)
    _, rep = report(monitor, env["readings"], env["register"], env["findings"], capsys)
    assert rep["new_ungated_count"] == 0, "rewrapped whitespace is the same path, not a new postern"
    assert rep["closed_count"] == 0
    assert rep["unchanged_count"] == 3  # AAA:2 + WELL:1, all still open
