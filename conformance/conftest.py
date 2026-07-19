"""
arifOS Negative Conformance Suite — shared fixtures.

WAJIB 1: 18 "must never happen" tests.
Unimplemented tests = xfail(strict=True). Absent test = forgotten.
"""

import pytest
import urllib.request
import json
import os
import subprocess
from pathlib import Path


# ── Live endpoints ────────────────────────────────────────────
ARIFOS = "http://localhost:8088"
AFORGE_MCP = "http://localhost:7072"
AFORGE_SENSE = "http://localhost:7071"
GEOX = "http://localhost:8081"
WEALTH = "http://localhost:18082"
WELL = "http://localhost:18083"
AAA = "http://localhost:3001"
VAULT999_FILE = "/root/arifOS/VAULT999/outcomes.jsonl"


def _get(url: str, timeout: int = 10) -> dict:
    """GET a JSON endpoint."""
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode())


def _post(url: str, body: dict, timeout: int = 10) -> dict:
    """POST JSON to an endpoint."""
    data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode())


@pytest.fixture(scope="session")
def arifos_health():
    """Verify arifOS kernel is reachable."""
    return _get(f"{ARIFOS}/health")


@pytest.fixture(scope="session")
def aforge_health():
    """Verify A-FORGE MCP is reachable."""
    return _get(f"{AFORGE_MCP}/health")


@pytest.fixture(scope="session")
def geox_health():
    """Verify GEOX is reachable."""
    return _get(f"{GEOX}/health")


@pytest.fixture(scope="session")
def wealth_health():
    """Verify WEALTH is reachable."""
    return _get(f"{WEALTH}/health")


@pytest.fixture(scope="session")
def well_health():
    """Verify WELL is reachable."""
    return _get(f"{WELL}/health")


@pytest.fixture(scope="session")
def aaa_health():
    """Verify AAA is reachable."""
    return _get(f"{AAA}/health")


@pytest.fixture(scope="session")
def vault999_lines():
    """Read VAULT999 outcomes.jsonl."""
    p = Path(VAULT999_FILE)
    if not p.exists():
        return []
    return p.read_text().strip().split("\n")


@pytest.fixture(scope="session")
def federation_healthy(arifos_health, aforge_health, geox_health, wealth_health, well_health, aaa_health):
    """Precondition: all 6 organs respond to health checks."""
    organs = {
        "arifOS": arifos_health.get("status"),
        "A-FORGE MCP": aforge_health.get("status"),
        "GEOX": geox_health.get("status"),
        "WEALTH": wealth_health.get("status"),
        "WELL": well_health.get("status"),
        "AAA": aaa_health.get("status"),
    }
    degraded = [k for k, v in organs.items() if v not in ("healthy", "degraded")]
    if degraded:
        pytest.skip(f"Organs not ready: {degraded}")
    return organs
