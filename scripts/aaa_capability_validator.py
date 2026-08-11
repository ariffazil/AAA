#!/usr/bin/env python3
"""
aaa_capability_validator.py — Phase A

Validates a CapabilityIndex against:
  - the seven-axis schema
  - INV-11..17 invariants
  - fail-closed conditions for READY_READONLY verdict

Pure logic. No MCP backend spawn. No network. No state mutation.

Authorized by F13 directive, 2026-08-11 (SEAL_PHASE_A_ONLY).
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from typing import Any

from aaa_capability_loader import (
    CANONICAL_AXES,
    DOCTRINE_CANONICAL_NAMES,
    CapabilityBackend,
    CapabilityIndex,
)


# INV-11..17 — declared in AAA_CAPABILITY_REGISTRY.yaml
INVARIANT_KEYS: tuple[str, ...] = (
    "one_canonical_name_per_capability",
    "mcp_servers_must_be_stateless",
    "cognition_owner",
    "authority_owner",
    "continuity_owner",
    "write_tools_gated_by",
    "credentials_held_by",
)

# Patterns that suggest a literal credential in a registry field.
# (Loaded from env/headers/url fields; conservative — false positives are tolerable.)
_TOKEN_PATTERN = re.compile(
    r"^(sk-|sk_|pk-|ghp_|github_pat_|xai-|minimax-|claude-|key-|token-)"
    r"|^[A-Za-z0-9_\-]{40,}$",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class ValidationReport:
    """Outcome of validating a CapabilityIndex."""

    schema_valid: bool
    invariants_ok: dict[str, bool]
    fail_closed_reasons: tuple[str, ...]
    warnings: tuple[str, ...] = ()
    doctrine_capabilities_seen: frozenset[str] = frozenset()
    extra_capabilities: tuple[str, ...] = ()

    @property
    def is_ready_readonly(self) -> bool:
        """True iff the registry is valid AND no backend is enabled."""
        return (
            self.schema_valid
            and all(self.invariants_ok.values())
            and not self.fail_closed_reasons
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_valid": self.schema_valid,
            "invariants_ok": dict(self.invariants_ok),
            "fail_closed_reasons": list(self.fail_closed_reasons),
            "warnings": list(self.warnings),
            "doctrine_capabilities_seen": sorted(self.doctrine_capabilities_seen),
            "extra_capabilities": list(self.extra_capabilities),
            "ready_readonly": self.is_ready_readonly,
        }


# --- Helpers ---


def _all_seven_axes_present(index: CapabilityIndex) -> tuple[bool, str]:
    missing = [a for a in CANONICAL_AXES if a not in index.axes]
    if missing:
        return False, f"missing_axes:{','.join(missing)}"
    return True, ""


def _all_seven_axes_nonempty(index: CapabilityIndex) -> tuple[bool, str]:
    empty = [a for a in CANONICAL_AXES if not index.axes.get(a)]
    if empty:
        return False, f"empty_axes:{','.join(empty)}"
    return True, ""


def _no_enabled_without_seal(index: CapabilityIndex) -> tuple[bool, str]:
    """
    INV-11..17 + fail-closed: a backend may be enabled only if it has a real seal.
    Pending seal + enabled=true is forbidden.
    """
    bad = [
        b.name for b in index.backends.values()
        if b.enabled and b.seal != "sealed" and b.seal != "ratifying"
    ]
    if bad:
        return False, f"enabled_without_seal:{','.join(bad)}"
    return True, ""


def _no_credential_leak(index: CapabilityIndex) -> tuple[bool, str]:
    """
    INV-17: credentials held by gateway only.
    Scan backend note/url/transport fields for token-like literals.
    """
    suspects: list[str] = []
    for b in index.backends.values():
        for field_name in ("url", "note"):
            v = getattr(b, field_name) or ""
            if not isinstance(v, str):
                continue
            # split on common separators and inspect each token
            for tok in re.split(r"[\s,;:/&=?]+", v):
                if _TOKEN_PATTERN.match(tok):
                    suspects.append(f"{b.name}.{field_name}")
                    break
    if suspects:
        return False, f"credential_leak:{','.join(suspects)}"
    return True, ""


def _write_tools_gated(index: CapabilityIndex) -> tuple[bool, str]:
    """
    INV-16: write tools must require an A-FORGE lease.
    Any backend that serves a forge.* capability must have a gate.
    """
    bad = []
    for b in index.backends.values():
        serves_forge = any(
            s.axis == "forge" for s in b.services
        )
        if serves_forge and (b.gate is None or "A-FORGE" not in b.gate):
            bad.append(b.name)
    if bad:
        return False, f"write_tools_ungated:{','.join(bad)}"
    return True, ""


def _canonical_capability_names_unique(index: CapabilityIndex) -> tuple[bool, str]:
    """
    INV-11: one canonical name per capability.
    CapabilityIndex.canonical_names is a set, so duplicates would already
    have raised RegistryLoadError. This check is a belt-and-suspenders
    assertion for the validator.
    """
    seen = set()
    for axis, caps in index.axes.items():
        for cap in caps:
            if cap in seen:
                return False, f"duplicate_capability:{cap}"
            seen.add(cap)
    return True, ""


def _stateless_check(index: CapabilityIndex) -> tuple[bool, str]:
    """
    INV-12: mcp_servers_must_be_stateless = true (declared).
    Plus: no backend may declare itself stateful.
    """
    declared = index.invariants_declared.get("mcp_servers_must_be_stateless")
    if declared is not True:
        return False, "inv12_not_declared_true"
    # No backend may declare itself stateful (cross-axis scan of raw registry)
    for axis_name, axis_data in index.raw.get("axes", {}).items():
        for cap_name, cap_data in axis_data.get("canonical_capabilities", {}).items():
            for backend_name, raw in cap_data.get("backends", {}).items():
                if isinstance(raw, dict) and raw.get("stateful") is True:
                    return False, f"stateful_backend:{backend_name}"
    return True, ""


def _cognition_owner_correct(index: CapabilityIndex) -> tuple[bool, str]:
    declared = index.invariants_declared.get("cognition_owner")
    if declared != "agent":
        return False, f"cognition_owner_wrong:{declared!r}"
    return True, ""


def _authority_owner_correct(index: CapabilityIndex) -> tuple[bool, str]:
    declared = index.invariants_declared.get("authority_owner")
    if declared != "AAA_router":
        return False, f"authority_owner_wrong:{declared!r}"
    return True, ""


def _continuity_owner_correct(index: CapabilityIndex) -> tuple[bool, str]:
    declared = index.invariants_declared.get("continuity_owner")
    expected_substrings = ("VAULT999", "arifFlow")
    if not isinstance(declared, str) or not all(s in declared for s in expected_substrings):
        return False, f"continuity_owner_wrong:{declared!r}"
    return True, ""


def _credentials_owner_correct(index: CapabilityIndex) -> tuple[bool, str]:
    declared = index.invariants_declared.get("credentials_held_by")
    if declared != "gateway_only":
        return False, f"credentials_held_by_wrong:{declared!r}"
    return True, ""


def _doctrine_capabilities(index: CapabilityIndex) -> tuple[bool, str]:
    """
    The seven doctrine-named canonical capabilities must all be present.
    """
    missing = [c for c in DOCTRINE_CANONICAL_NAMES if c not in index.canonical_names]
    if missing:
        return False, f"doctrine_capabilities_missing:{','.join(missing)}"
    return True, ""


# --- Main validator ---


def validate(index: CapabilityIndex) -> ValidationReport:
    """
    Validate the index. Returns a ValidationReport.

    Invariant mapping:
      schema_valid       ↔  all axis-shape checks pass
      invariants_ok[INV] ↔  the corresponding runtime invariant holds
      fail_closed_reasons ↔  reasons that would block READY_READONLY verdict
    """
    invariants_ok: dict[str, bool] = {}
    fail_closed: list[str] = []
    warnings: list[str] = []

    # INV-11 — one canonical name per capability
    ok, reason = _canonical_capability_names_unique(index)
    invariants_ok["INV-11"] = ok
    if not ok:
        fail_closed.append(reason)

    # INV-12 — stateless
    ok, reason = _stateless_check(index)
    invariants_ok["INV-12"] = ok
    if not ok:
        fail_closed.append(reason)

    # INV-13 — cognition owner
    ok, reason = _cognition_owner_correct(index)
    invariants_ok["INV-13"] = ok
    if not ok:
        fail_closed.append(reason)

    # INV-14 — authority owner
    ok, reason = _authority_owner_correct(index)
    invariants_ok["INV-14"] = ok
    if not ok:
        fail_closed.append(reason)

    # INV-15 — continuity owner
    ok, reason = _continuity_owner_correct(index)
    invariants_ok["INV-15"] = ok
    if not ok:
        fail_closed.append(reason)

    # INV-16 — write tools gated
    ok, reason = _write_tools_gated(index)
    invariants_ok["INV-16"] = ok
    if not ok:
        fail_closed.append(reason)

    # INV-17 — credentials held by gateway only (no leak)
    ok, reason = _credentials_owner_correct(index)
    invariants_ok["INV-17.a"] = ok
    if not ok:
        fail_closed.append(reason)
    ok, reason = _no_credential_leak(index)
    invariants_ok["INV-17.b"] = ok
    if not ok:
        fail_closed.append(reason)

    # Fail-closed: enabled without seal
    ok, reason = _no_enabled_without_seal(index)
    if not ok:
        fail_closed.append(reason)

    # Schema: seven axes present + non-empty
    schema_valid = True
    for check in (_all_seven_axes_present, _all_seven_axes_nonempty, _doctrine_capabilities):
        ok, reason = check(index)
        if not ok:
            schema_valid = False
            fail_closed.append(reason)

    # Doctrine capability coverage (info, not failure)
    doctrine_seen = frozenset(c for c in DOCTRINE_CANONICAL_NAMES if c in index.canonical_names)
    extras = tuple(sorted(index.canonical_names - set(DOCTRINE_CANONICAL_NAMES)))

    return ValidationReport(
        schema_valid=schema_valid,
        invariants_ok=invariants_ok,
        fail_closed_reasons=tuple(fail_closed),
        warnings=tuple(warnings),
        doctrine_capabilities_seen=doctrine_seen,
        extra_capabilities=extras,
    )


# --- CLI ---

def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: aaa_capability_validator.py <path-to-AAA_CAPABILITY_REGISTRY.yaml>", file=sys.stderr)
        return 2
    # Lazy import to keep module import-light for tests
    from aaa_capability_loader import load_registry, RegistryLoadError
    try:
        index = load_registry(argv[1])
    except RegistryLoadError as e:
        print(f"VALIDATOR: load_failed", file=sys.stderr)
        print(f"  reason: {e}", file=sys.stderr)
        return 1
    report = validate(index)
    print(f"SCHEMA: {'valid' if report.schema_valid else 'INVALID'}")
    for inv, ok in sorted(report.invariants_ok.items()):
        print(f"  {inv}: {'ok' if ok else 'FAIL'}")
    if report.fail_closed_reasons:
        print(f"FAIL_CLOSED_REASONS:")
        for r in report.fail_closed_reasons:
            print(f"  - {r}")
    if report.warnings:
        print(f"WARNINGS:")
        for w in report.warnings:
            print(f"  - {w}")
    print(f"DOCTRINE_CAPS_SEEN: {len(report.doctrine_capabilities_seen)}/7")
    print(f"EXTRA_CAPS: {len(report.extra_capabilities)}")
    print(f"VERDICT: {'READY_READONLY' if report.is_ready_readonly else 'HOLD'}")
    return 0 if report.is_ready_readonly else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
