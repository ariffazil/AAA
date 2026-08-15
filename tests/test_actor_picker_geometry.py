"""RCR guard — FED actor-picker geometry invariants.

Doctrine: /root/AAA/federation/FED_ACTOR_ENVELOPE_DOCTRINE.md
Canon: "State is no longer topology." (F13, 2026-08-15)

These tests make the falsifier machine-checkable:
    next model release = 1 SOT edit (fed_signatures cascades),
    0 picker edits. If any of these tests break on a model
    release, the geometry failed — not the model.
"""

import json
from pathlib import Path

import pytest

pytest.importorskip("yaml", reason="pyyaml required for SOT checks")

ROOT = Path("/root")
OPENCODE_JSON = ROOT / ".config/opencode/opencode.json"
FED_SIGNATURES = ROOT / "AAA/federation/fed_signatures.yaml"

ACTORS = {"agi-333", "asi-555", "forge-777", "apex-888"}

# Any picker key containing one of these is a model identity leaking
# into topology — the exact disease the doctrine cures.
MODEL_IDENTITY_TOKENS = (
    "glm", "gemini", "kimi", "minimax", "mimo", "qwen",
    "deepseek", "wan", "grok", "gpt", "claude", "llama",
)


def _picker_keys():
    if not OPENCODE_JSON.exists():
        pytest.skip("opencode.json not present")
    cfg = json.loads(OPENCODE_JSON.read_text())
    return set(cfg["provider"]["litellm-federation"]["models"])


def _actor_geometry():
    if not FED_SIGNATURES.exists():
        pytest.skip("fed_signatures.yaml not present")
    import yaml
    sot = yaml.safe_load(FED_SIGNATURES.read_text())
    return sot["actor_geometry"]


def test_picker_is_exactly_four_actors():
    assert _picker_keys() == ACTORS


def test_picker_carries_no_model_identity():
    for key in _picker_keys():
        for token in MODEL_IDENTITY_TOKENS:
            assert token not in key.lower(), (
                f"model identity '{token}' leaked into picker key '{key}' — "
                "State is not topology. Fix: move it to fed_signatures cascades."
            )


def test_sot_cascades_cover_exactly_the_actors():
    geo = _actor_geometry()
    assert set(geo["cascades"]) == ACTORS
    assert set(geo["picker"]["actors"]) == ACTORS


def test_sot_cascades_are_nonempty_and_ranked():
    for actor, cascade in _actor_geometry()["cascades"].items():
        assert cascade, f"{actor} cascade empty"
        # cascades are ordered lists — primary first
        assert isinstance(cascade, list)


def test_compat_alias_table_has_kill_date():
    compat = _actor_geometry()["compat_aliases"]
    assert compat["kill_date"], "compat aliases without kill-date = permanent theatre"
