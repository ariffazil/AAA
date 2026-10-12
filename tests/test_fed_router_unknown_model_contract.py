#!/usr/bin/env python3
"""Unknown-model selection contract for fed_router.

fed_router resolved routes for a model absent from MODEL_ROUTES by borrowing
deepseek-v4-pro's cascade (scripts/fed_router.py:902). Route dicts carry no
model field, so route_model (:913) then echoed the requested, nonexistent name
back as the served model -- producing a health-annotated, router_class='direct'
advisory endorsing a model that does not exist.

Contract under test: an unknown EXPLICIT model is refused, never substituted.

Scope: unknown-model selection only. Does NOT cover malformed requests,
authorisation, or capability-signature resolution (covered by the existing
refusal at :884). Advisory routing surface; grants no authority.

Run: python3 -m pytest tests/test_fed_router_unknown_model_contract.py -v
"""
import sys

import pytest

sys.path.insert(0, "/root/AAA/scripts")
import fed_router as m  # noqa: E402

UNKNOWN = "totally-not-a-model-xyz"
KNOWN = "qwen3.8-max"


# ── A. the regression: unknown model must not be served or endorsed ────────

def test_unknown_model_never_returned_as_served():
    """A1 - the defect: the unknown name came back as the served model."""
    r = m.fed_route_engine(model=UNKNOWN)
    assert not any(x.get("model") == UNKNOWN for x in r), r


def test_unknown_model_invents_no_routes():
    """A2 - the refusal is an advisory, not a provider cascade."""
    r = m.fed_route_engine(model=UNKNOWN)
    assert r, "must return something"
    assert all(x.get("error") for x in r), r


def test_unknown_model_error_names_the_model():
    """A3 - the caller is told exactly which model was unsupported."""
    r = m.fed_route_engine(model=UNKNOWN)
    assert UNKNOWN in r[0].get("error", ""), r


# ── B. the refusal claims nothing about selection ─────────────────────────

def test_unknown_model_asserts_no_provider():
    r = m.fed_route_engine(model=UNKNOWN)
    assert not any(x.get("provider") for x in r), r


def test_unknown_model_asserts_no_priority():
    r = m.fed_route_engine(model=UNKNOWN)
    assert not any("priority" in x for x in r), r


def test_unknown_model_asserts_no_router_class():
    r = m.fed_route_engine(model=UNKNOWN)
    assert not any(x.get("router_class") for x in r), r


def test_unknown_model_reports_supported_false():
    r = m.fed_route_engine(model=UNKNOWN)
    assert r[0].get("supported") is False, r


def test_unknown_model_echoes_requested_model():
    r = m.fed_route_engine(model=UNKNOWN)
    assert r[0].get("requested_model") == UNKNOWN, r


# ── C. known explicit model preserved ─────────────────────────────────────

def test_known_model_still_routes():
    k = m.fed_route_engine(model=KNOWN)
    assert k and "error" not in k[0], k


def test_known_model_echoes_itself():
    k = m.fed_route_engine(model=KNOWN)
    assert k[0].get("model") == KNOWN, k


def test_known_model_carries_no_supported_flag():
    k = m.fed_route_engine(model=KNOWN)
    assert "supported" not in k[0], k


def test_known_model_keeps_priority():
    k = m.fed_route_engine(model=KNOWN)
    assert "priority" in k[0], k


# ── D. default model (no model argument) preserved ────────────────────────

def test_default_model_is_still_routed():
    """D1 - engine default must keep working; it is a known MODEL_ROUTES key."""
    d = m.fed_route_engine()
    assert d and "error" not in d[0], d


def test_default_model_serves_itself():
    """D2 - the default is deepseek-v4-pro, not an echo of anything else."""
    d = m.fed_route_engine()
    assert d[0].get("model") == "deepseek-v4-pro", d


def test_default_model_is_not_a_refusal():
    """D3 - the new branch must not fire for the default call."""
    d = m.fed_route_engine()
    assert "supported" not in d[0], d


# ── E. capability branch preserved ────────────────────────────────────────

def test_capability_resolves_to_routes():
    c = m.fed_route_engine(model="fed-reasoning-heavy")
    assert c and "error" not in c[0], c


def test_capability_routes_all_labelled():
    c = m.fed_route_engine(model="fed-reasoning-heavy")
    assert all(x.get("model") for x in c), c


def test_unknown_capability_still_refuses_at_884():
    """E3 - pre-existing refusal is untouched and distinct from this patch."""
    c = m.fed_route_engine(model="fed-fast")
    assert "Unknown capability signature" in c[0].get("error", ""), c


# ── F. effort dial precedence preserved ───────────────────────────────────
# effort_level is applied at :871 BEFORE model resolution, so it overrides an
# explicit model. Preserved by this patch, not introduced by it.

def test_effort_overrides_explicit_model():
    """F1 - documented Step 0 behaviour; unknown model never reaches :900."""
    e = m.fed_route_engine(model=UNKNOWN, effort_level="high")
    assert e and "error" not in e[0], e


def test_effort_result_is_not_the_unknown_model():
    e = m.fed_route_engine(model=UNKNOWN, effort_level="high")
    assert all(x.get("model") != UNKNOWN for x in e), e


def test_effort_applied_flag_present():
    e = m.fed_route_engine(model=KNOWN, effort_level="medium")
    assert e[0].get("effort_applied") == "medium", e


def test_capability_bypassed_when_effort_supplied():
    """F4 - OBSERVED pre-existing behaviour, pinned as a guard.

    The middleware always sends effort_level (default 'medium'), and Step 0
    rewrites model before the capability check at :882. Asserts the SERVED
    model, not merely the flag: capability selection must be observably
    bypassed in favour of the effort-dial model.
    """
    c = m.fed_route_engine(model="fed-reasoning-heavy", effort_level="medium")
    assert c[0].get("effort_applied") == "medium", c
    assert c[0].get("model") == "deepseek-v4-pro", c


def test_capability_reached_when_effort_absent():
    """F5 - contrast for F4: without effort, the capability cascade is used.

    Establishes that F4 reflects effort precedence rather than a broken
    capability lookup.
    """
    c = m.fed_route_engine(model="fed-reasoning-heavy")
    served = {x.get("model") for x in c}
    assert "deepseek-v4-pro" not in served or len(served) > 1, c
    assert "mimo-v2.6-pro" in served, c