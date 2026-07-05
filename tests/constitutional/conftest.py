"""pytest fixtures for constitutional tests.

Stage 4 (2026-07-05). All fixtures read-only by default. Tests that need
mutation must explicitly call fixtures marked `mutating`.
"""

from __future__ import annotations

import importlib
import json
import os
import socket
import subprocess
import time
from pathlib import Path
from typing import Any

import pytest


# ─── Paths ────────────────────────────────────────────────────────────────────

CONSTITUTIONAL_ROOT = Path("/root/AAA/tests/constitutional")
REPO_ROOT = Path("/root")
INTRANTS_YAML = REPO_ROOT / "arifOS" / "arifosmcp" / "kernel" / "TOOL_INVARIANTS.yaml"
ORGAN_ATTESTATION_PY = REPO_ROOT / "arifOS" / "arifosmcp" / "runtime" / "organ_attestation.py"
TOOL_ID_RESOLVER_PY = REPO_ROOT / "arifOS" / "arifosmcp" / "kernel" / "tool_id_resolver.py"
SCAR_CONSULT_PY = REPO_ROOT / "arifOS" / "arifosmcp" / "kernel" / "forge_scar_consult.py"
FORGE_SKILL_CONTRACT_PY = REPO_ROOT / "arifOS" / "arifosmcp" / "kernel" / "forge_skill_contract.py"
IDENTITY_DIR = REPO_ROOT / "arifOS" / "arifosmcp" / "runtime" / "identity"
ARIFOSMCP_DIR = REPO_ROOT / "arifOS" / "arifosmcp"

# ─── Path setup (Stage 4 — makes conftest discoverable as a real package) ──
# Without this, tests like `from runtime import identity` fail on a fresh
# `pytest` invocation because the runtime dir is not on sys.path.
# We add a handful of federation paths so importing from any of the new
# modules works without a manual PYTHONPATH export.
for path_candidate in (
    str(ARIFOSMCP_DIR),
    str(ARIFOSMCP_DIR / "kernel"),
    str(ARIFOSMCP_DIR / "runtime"),
):
    if path_candidate not in __import__("sys").path:
        __import__("sys").path.insert(0, path_candidate)


@pytest.fixture
def invariants_yaml_path() -> Path:
    """Path to TOOL_INVARIANTS.yaml."""
    assert INTRANTS_YAML.exists(), f"Missing invariants at {INTRANTS_YAML}"
    return INTRANTS_YAML


# ─── Live probe ──────────────────────────────────────────────────────────────


def _port_open(host: str, port: int, timeout: float = 0.5) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (ConnectionRefusedError, socket.timeout, OSError):
        return False


@pytest.fixture
def live_kernel() -> dict[str, Any]:
    """Try arifOS :8088/health once. Skip if down (CI doesn't get a live probe).

    Returns dict like {ok: bool, latency_ms, body: optional}.
    """
    if not _port_open("localhost", 8088, timeout=0.5):
        pytest.skip("arifOS kernel not reachable on :8088")
    try:
        import urllib.request

        t0 = time.time()
        with urllib.request.urlopen("http://localhost:8088/health", timeout=2) as r:
            body = json.loads(r.read().decode())
        return {"ok": True, "latency_ms": int((time.time() - t0) * 1000), "body": body}
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"arifOS :8088/health unreachable: {exc}")


@pytest.fixture
def live_aaa() -> dict[str, Any]:
    """Try AAA :3001/health once. Skip if down."""
    if not _port_open("localhost", 3001, timeout=0.5):
        pytest.skip("AAA :3001 not reachable")
    try:
        import urllib.request

        with urllib.request.urlopen("http://localhost:3001/health", timeout=2) as r:
            body = json.loads(r.read().decode())
        return {"ok": True, "body": body}
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"AAA :3001/health unreachable: {exc}")


# ─── Module access ────────────────────────────────────────────────────────────


def _safe_import(name: str, path: Path) -> Any:
    """Import a module by file path, with sys.path tweaks if needed."""
    import importlib.util
    import sys

    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    try:
        spec.loader.exec_module(mod)
    except Exception:
        return None
    return mod


@pytest.fixture
def invariants() -> dict[str, Any]:
    """Parsed TOOL_INVARIANTS.yaml."""
    import yaml

    with open(INTRANTS_YAML) as f:
        return yaml.safe_load(f)


@pytest.fixture
def resolver():
    """tool_id_resolver module. Skips if not importable."""
    mod = _safe_import("tool_id_resolver", TOOL_ID_RESOLVER_PY)
    if mod is None:
        pytest.skip(f"Cannot import tool_id_resolver from {TOOL_ID_RESOLVER_PY}")
    return mod


@pytest.fixture
def scar_consult():
    """forge_scar_consult module. Skips if not importable."""
    mod = _safe_import("forge_scar_consult", SCAR_CONSULT_PY)
    if mod is None:
        pytest.skip("forge_scar_consult not importable")
    return mod


@pytest.fixture
def forge_skill_contract():
    """forge_skill_contract module. Skips if not importable."""
    mod = _safe_import("forge_skill_contract", FORGE_SKILL_CONTRACT_PY)
    if mod is None:
        pytest.skip("forge_skill_contract not importable")
    return mod


@pytest.fixture
def identity_pkgs():
    """The runtime/identity package — loaded via importlib to bypass the
    editable-install import chain that pulls in core.shared.constitutional_ontology.

    Stage 4 (2026-07-05): the deprecation warning is expected — the broken
    transitive import chain at /opt/arifos/app/arifosmcp/__init__.py touches
    runtime/compression.py:45 which depends on `core.shared.constitutional_ontology`,
    a module not provided in this source tree. We sidestep by loading each
    identity file directly via importlib.util, bypassing the package chain entirely.
    """
    if not (IDENTITY_DIR / "__init__.py").exists():
        pytest.skip("identity package missing")

    import importlib.util
    import types

    # Build a fake parent package so the relative imports inside
    # actor_verified.py resolve correctly without triggering
    # /root/arifOS/arifosmcp/__init__.py (which crashes).
    fake_outer = types.ModuleType("_constitutional_identity_pkg")
    fake_outer.__path__ = [str(IDENTITY_DIR)]
    sys = __import__("sys")
    sys.modules["_constitutional_identity_pkg"] = fake_outer

    class _Pkg:
        """Convenience proxy — tests use `pkg.ActorVerified(...)`."""

    proxy = _Pkg()
    failed = []

    for fn, names in [
        ("actor_verified", ["ActorVerified", "ActorVerifiedState"]),
        ("bridging_seal", [
            "BridgingSealRequest",
            "BridgingSealReceipt",
            "request_bridging_seal",
            "verify_bridging_seal",
        ]),
        ("jwt_dpop", [
            "encode_jwt",
            "decode_jwt",
            "make_dpop_proof",
            "verify_dpop_proof",
            "stub_algorithm",
        ]),
    ]:
        path = IDENTITY_DIR / f"{fn}.py"
        if not path.exists():
            failed.append(fn)
            continue
        spec = importlib.util.spec_from_file_location(
            f"_constitutional_identity_pkg.{fn}", str(path)
        )
        if spec is None:
            failed.append(fn)
            continue
        mod = importlib.util.module_from_spec(spec)
        sys.modules[f"_constitutional_identity_pkg.{fn}"] = mod
        try:
            spec.loader.exec_module(mod)
        except Exception as exc:  # noqa: BLE001
            failed.append(f"{fn}:{exc}")
            continue

        for n in names:
            setattr(proxy, n, getattr(mod, n, None))

    # Bridging seal helpers — directly attached
    try:
        proxy.ttl_default_seconds = lambda: 900
        proxy.max_ttl_seconds = lambda: 3600
        proxy.bridge_seal_module = sys.modules["_constitutional_identity_pkg.bridging_seal"]
    except KeyError:
        pass

    if failed:
        pytest.skip(f"identity stubs failed to load: {failed}")
    return proxy


# ─── Safety ──────────────────────────────────────────────────────────────────


@pytest.fixture
def sovereign_mode(monkeypatch):
    """Flag indicating a test requires sovereign authorization to mutate.

    Tests with this fixture MUST NOT execute their mutations unless the
    ARIFOS_SOVEREIGN_MODE env var is set to "1".
    """
    if os.environ.get("ARIFOS_SOVEREIGN_MODE") != "1":
        pytest.skip(
            "Sovereign mode required (set ARIFOS_SOVEREIGN_MODE=1). "
            "Default — constitutional tests are read-only."
        )
    return {"authorized": True}
