"""Regression: secrets-audit must print findings, never crash, never call hashes secrets."""

from __future__ import annotations

import pytest

from scripts.ci.secrets_scan_new_findings import (
    DISABLED_PLUGINS,
    build_scan_cmd,
    finding_sort_key,
    new_findings_against_baseline,
    print_findings,
)


def test_sorted_raw_tuples_typeerror_is_the_bug_we_fixed():
    # Crash only fires when two rows share a filename — sorted then compares dicts.
    findings = [
        ("a.py", {"type": "Hex High Entropy String", "line_number": 1, "hashed_secret": "aa"}),
        ("a.py", {"type": "AWSKeyDetector", "line_number": 2, "hashed_secret": "bb"}),
    ]
    with pytest.raises(TypeError):
        sorted(findings)


def test_sort_key_does_not_crash_on_dicts():
    findings = [
        ("b.py", {"type": "Hex High Entropy String", "line_number": 1, "hashed_secret": "aa"}),
        ("a.py", {"type": "AWSKeyDetector", "line_number": 2, "hashed_secret": "bb"}),
        ("a.py", {"type": "AWSKeyDetector", "hashed_secret": "cc"}),  # missing line_number
    ]
    ordered = sorted(findings, key=finding_sort_key)
    assert [f[0] for f in ordered] == ["a.py", "a.py", "b.py"]


def test_entropy_plugins_are_disabled():
    cmd = build_scan_cmd()
    assert "HexHighEntropyString" in DISABLED_PLUGINS
    assert "Base64HighEntropyString" in DISABLED_PLUGINS
    assert "KeywordDetector" in DISABLED_PLUGINS
    disabled = [cmd[i + 1] for i, x in enumerate(cmd) if x == "--disable-plugin"]
    assert set(DISABLED_PLUGINS) <= set(disabled)


def test_new_findings_skips_baseline_hashes():
    current = {
        "results": {
            "a.py": [
                {"hashed_secret": "known", "type": "AWSKeyDetector", "line_number": 1},
                {"hashed_secret": "fresh", "type": "AWSKeyDetector", "line_number": 2},
            ]
        }
    }
    baseline = {"results": {"a.py": [{"hashed_secret": "known"}]}}
    new = new_findings_against_baseline(current, baseline)
    assert len(new) == 1
    assert new[0][1]["hashed_secret"] == "fresh"


def test_print_findings_emits_every_row(capsys):
    findings = [
        ("hooks/x.py", {"type": "AWSKeyDetector", "line_number": 9, "hashed_secret": "deadbeefdeadbeef"}),
        ("tests/f.py", {"type": "GitHubTokenDetector", "line_number": 3, "hashed_secret": "cafebabecafebabe"}),
    ]
    print_findings(findings)
    out = capsys.readouterr().out
    assert "2 finding(s)" in out
    assert "AWSKeyDetector=1" in out
    assert "GitHubTokenDetector=1" in out
    assert "hooks/x.py:9" in out
    assert "tests/f.py:3" in out
    assert "Do not baseline SHA-256" in out
