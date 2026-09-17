"""
test_identity_resolver.py — receipts for the identity interceptor gate.

Proves SCAR-2026-09-15-001 cannot recur: a kata nama am (common noun) can no
longer blind-resolve to an identity, and an unreadable registry HOLDs rather
than passing.

Run:  python -m pytest /root/AAA/tests/constitutional/test_identity_resolver.py -v
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, "/root/AAA/registry/routing")

from identity_resolver import (  # noqa: E402
    IdentityHold,
    Verdict,
    _reset_cache,
    assert_clear,
    guard,
    identity_bound,
    load_registry,
    resolve,
)

REGISTRY = Path("/root/AAA/registry/routing/identity_continuity.yaml")


@pytest.fixture(autouse=True)
def _fresh_registry():
    _reset_cache()
    yield
    _reset_cache()


# ── Preconditions ────────────────────────────────────────────────────────────


def test_registry_is_readable_and_carries_both_layers():
    reg = load_registry(force=True)
    assert reg is not None, "registry must parse — the gate depends on it"
    assert reg.named_actor_patterns, "named_actors (kata nama khas) must be present"
    assert reg.ambiguous_patterns, "ambiguous_categories (kata nama am) must be present"
    assert reg.legacy_rules, "legacy_handling map must be present"


def test_abang_sado_is_not_registered_as_a_named_actor():
    """The original weld: the class must live outside named_actors."""
    reg = load_registry(force=True)
    assert reg is not None
    assert not any(p.search("abang sado") for p in reg.named_actor_patterns), (
        "REGRESSION: 'abang sado' is a common noun and must never sit in named_actors"
    )
    assert any(p.search("abang sado") for p in reg.ambiguous_patterns)


# ── The core scar ────────────────────────────────────────────────────────────


def test_common_noun_alone_never_resolves():
    r = resolve("abang sado", capability="identity_bound", registry=load_registry(force=True))
    assert r.verdict is Verdict.REQUIRE_DISAMBIGUATION
    assert r.classes and not r.instances
    assert r.resolved_actor is None
    assert r.blocked is True


@pytest.mark.parametrize("subject", ["sado", "Abang Sado", "ABANG SADO"])
def test_common_noun_case_insensitive(subject):
    r = resolve(subject, registry=load_registry(force=True))
    assert r.verdict is Verdict.REQUIRE_DISAMBIGUATION


def test_common_noun_blocks_execution():
    with pytest.raises(IdentityHold) as ei:
        assert_clear("abang sado", capability="biometric")
    assert ei.value.result.verdict is Verdict.REQUIRE_DISAMBIGUATION


def test_decorator_never_executes_a_blocked_call():
    calls = []

    @identity_bound(capability="biometric")
    def enroll(subject: str):
        calls.append(subject)
        return "enrolled"

    assert enroll("Syed") == "enrolled"
    with pytest.raises(IdentityHold):
        enroll("abang sado")
    assert calls == ["Syed"], "the blocked call must not have reached the function body"


# ── Proper nouns still work ──────────────────────────────────────────────────


def test_proper_noun_resolves_to_one_actor():
    r = resolve("Syed", registry=load_registry(force=True))
    assert r.verdict is Verdict.PASS_INSTANCE
    assert r.resolved_actor == "syed"
    assert r.blocked is False


def test_class_plus_instance_records_both_without_collapsing():
    r = resolve("Syed — an abang sado node", registry=load_registry(force=True))
    assert r.instances and r.classes, "both layers must be visible to the caller"
    assert r.verdict is Verdict.PASS_INSTANCE
    assert "do not collapse" in r.reason


def test_no_identity_claim_passes():
    r = resolve("summarise the weekly federation report", registry=load_registry(force=True))
    assert r.verdict is Verdict.PASS
    assert r.blocked is False


# ── Legacy unconformity (F13 HOLD: map, never re-deposit) ────────────────────


@pytest.mark.parametrize(
    "subject",
    ["Syed (Abang Sado)", "Syed Khairuddin (Abang Sado)", "Display: Abang Sado"],
)
def test_legacy_collapsed_headers_force_dual_evaluation(subject):
    r = resolve(subject, registry=load_registry(force=True))
    assert r.verdict is Verdict.REQUIRE_DISAMBIGUATION
    assert r.legacy_hits


def test_historical_header_is_intercepted_not_rewritten():
    """Old rock layers stay; the registry intercepts them at parse time."""
    helix = Path("/root/AAA/docs/HELIX_MEMORY_STRUCTURE.md")
    if not helix.exists():
        pytest.skip("HELIX record absent")
    text = helix.read_text(encoding="utf-8", errors="ignore")
    assert "Syed Khairuddin (Abang Sado)" in text, "historical header must remain verbatim"
    r = resolve("Syed Khairuddin (Abang Sado)", registry=load_registry(force=True))
    assert r.verdict is Verdict.REQUIRE_DISAMBIGUATION


# ── T2I routing law ──────────────────────────────────────────────────────────


def test_t2i_forbidden_on_named_actor():
    r = resolve("Syed", capability="t2i", registry=load_registry(force=True))
    assert r.verdict is Verdict.DENY_T2I
    assert "I2I" in r.reason


def test_t2i_on_common_noun_still_disambiguates_first():
    r = resolve("abang sado", capability="t2i", registry=load_registry(force=True))
    assert r.verdict is Verdict.REQUIRE_DISAMBIGUATION


# ── Fail-safe: F1 > F2 ───────────────────────────────────────────────────────


def test_missing_registry_holds_not_passes(tmp_path):
    missing = tmp_path / "does-not-exist.yaml"
    _reset_cache()
    reg = load_registry(missing, force=True)
    assert reg is None
    r = resolve("Syed", capability="t2i", registry=reg)
    assert r.verdict is Verdict.HOLD_REGISTRY_UNREADABLE
    assert r.blocked is True


def test_malformed_registry_holds_not_passes(tmp_path):
    bad = tmp_path / "broken.yaml"
    bad.write_text("self_reference_patterns: [this: is: not: valid\n", encoding="utf-8")
    reg = load_registry(bad, force=True)
    assert reg is None, "a registry that cannot be trusted must return None"
    r = resolve("abang sado", registry=reg)
    assert r.verdict is Verdict.HOLD_REGISTRY_UNREADABLE
    assert r.blocked is True


def test_empty_registry_holds_not_passes(tmp_path):
    empty = tmp_path / "empty.yaml"
    empty.write_text("version: 1.0.0\nrouting_law:\n  id: X\n", encoding="utf-8")
    assert load_registry(empty, force=True) is None
    assert resolve("Syed", registry=None).blocked is True


def test_junk_input_is_safe():
    reg = load_registry(force=True)
    for weird in ["", "   ", "!!!" * 400]:
        r = resolve(weird, registry=reg)
        assert r.verdict in (Verdict.PASS, Verdict.REQUIRE_DISAMBIGUATION)


# ── Receipt ──────────────────────────────────────────────────────────────────


def test_blocked_decision_is_written_to_the_ledger(tmp_path, monkeypatch):
    import identity_resolver as ir

    ledger = tmp_path / "intercept.jsonl"
    monkeypatch.setattr(ir, "LEDGER_PATH", ledger)
    guard("abang sado", capability="t2i")
    lines = ledger.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    import json

    rec = json.loads(lines[0])
    assert rec["verdict"] == "REQUIRE_DISAMBIGUATION"
    assert rec["classes"]
