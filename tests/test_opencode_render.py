from __future__ import annotations

import copy
import os
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "resolvers"))

from opencode_render import (  # noqa: E402
    REQUIRED_SOT_AGENTS,
    load_sot,
    validate_model_ids,
    validate_sot_completeness,
)


def test_validate_model_ids_rejects_typo() -> None:
    sot = copy.deepcopy(load_sot())
    sot["agents"][0]["fallback_chain"].append(
        {"model_key": "openrouter/auto-betax", "priority": 999}
    )

    errors = validate_model_ids(sot)

    assert any("openrouter/auto-betax" in error for error in errors)


def test_required_agent_roster_rejects_missing_agent() -> None:
    sot = copy.deepcopy(load_sot())
    sot["agents"] = [agent for agent in sot["agents"] if agent["agent_id"] != "hermes"]

    errors = validate_sot_completeness(sot)

    assert any("required agent 'hermes' missing" in error for error in errors)


def test_live_sot_is_complete_and_model_ids_resolve() -> None:
    sot = load_sot()
    agents = {agent["agent_id"]: agent for agent in sot["agents"]}

    assert set(REQUIRED_SOT_AGENTS).issubset(agents)
    assert validate_sot_completeness(sot) == []
    assert validate_model_ids(sot) == []

    expected_explicit_fallbacks = {
        "opencode": {"deepseek/deepseek-r1", "google/gemini-2.5-flash"},
        "forge": {"deepseek/deepseek-r1", "moonshotai/kimi-k3"},
        "hermes": {"google/gemini-2.5-flash"},
        "openclaw": {"google/gemini-2.5-flash"},
    }
    for agent_id, expected in expected_explicit_fallbacks.items():
        actual = {item["model_key"] for item in agents[agent_id]["fallback_chain"]}
        assert expected.issubset(actual)


def test_model_sync_wrapper_uses_canonical_resolver_and_force_guard() -> None:
    wrapper = ROOT / "registries" / "federation-model-sync.sh"
    text = wrapper.read_text()

    assert "../AAA/src/resolvers" not in text
    assert "../src/resolvers/opencode_render.py" in text
    assert 'python3 "$resolver" --write --force' in text
    assert os.access(wrapper, os.X_OK)
