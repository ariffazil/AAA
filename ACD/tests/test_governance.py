"""ACD governance tests — no-execution guarantee, CLI semantics, audit non-rubber-stamp,
map-territory discipline (ACTIVE requires runtime evidence)."""

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Capability patterns (imports + call sites), not bare words — comments must not false-positive.
FORBIDDEN_TOKENS = [
    "import subprocess",
    "subprocess.Popen",
    "subprocess.run",
    "import socket",
    "socket.socket",
    "import urllib",
    "urllib.request",
    "import requests",
    "requests.get",
    "requests.post",
    "http.client",
    "os.system(",
    "os.popen(",
    "eval(",
    "exec(",
    "shutil.rmtree",
]

CLI = str(ROOT / "cli" / "acd_cli.py")


def run_cli(tmp_path, *args):
    env = dict(os.environ)
    env["ACD_RECEIPTS_DIR"] = str(tmp_path)
    return subprocess.run([sys.executable, CLI, *args], capture_output=True, text=True, env=env, timeout=60)


def test_core_and_cli_have_no_execution_capability():
    for rel in ("core/acd_core.py", "core/acd_memory.py", "cli/acd_cli.py"):
        src = (ROOT / rel).read_text()
        for token in FORBIDDEN_TOKENS:
            assert token not in src, f"{rel} contains forbidden capability token: {token}"


def test_status_never_claims_production_activation(tmp_path):
    from core.acd_core import ACDCore

    st = ACDCore(receipts_dir=tmp_path).status()
    assert st["production_activated"] is False
    assert st["runtime"] in ("PRESENT", "DOCTRINE_ONLY", "UNKNOWN")
    assert st["runtime"] != "ACTIVE"


def test_cli_dream_status_does_not_run_a_cycle(tmp_path):
    r = run_cli(tmp_path, "dream", "status")
    assert r.returncode == 0
    assert "core_version" in r.stdout
    assert list(tmp_path.glob("*.json")) == []


def test_cli_bare_dream_runs_one_bounded_cycle(tmp_path):
    r = run_cli(tmp_path, "dream")
    assert r.returncode == 0
    files = list(tmp_path.glob("*.json"))
    assert len(files) == 1
    rec = json.loads(files[0].read_text())
    assert rec["runtime_status"] == "COMPLETED"
    assert rec["ontology"] == "SIMULATED"
    assert rec["external_actions_attempted"] == 0
    assert rec["external_actions_executed"] == 0
    assert rec["shadow"] is True


def test_cli_purpose_argument_still_runs_cycle(tmp_path):
    r = run_cli(tmp_path, "dream", "advance the mission")
    assert r.returncode == 0
    assert len(list(tmp_path.glob("*.json"))) == 1


def test_cli_propose_creates_held_petition(tmp_path):
    assert run_cli(tmp_path, "dream").returncode == 0
    r = run_cli(tmp_path, "dream", "propose")
    assert r.returncode == 0
    assert "888_HOLD" in r.stdout
    petitions = list((tmp_path / "petitions").glob("*.json"))
    assert len(petitions) == 1
    pet = json.loads(petitions[0].read_text())
    assert pet["held"] is True
    assert pet["adjudicator"] == "HUMAN_SOVEREIGN"
    assert "authorized_by" not in pet  # not applied, not self-authorized


def test_audit_flags_tampered_receipt(tmp_path):
    assert run_cli(tmp_path, "dream").returncode == 0
    f = list(tmp_path.glob("*.json"))[0]
    rec = json.loads(f.read_text())
    rec["constitutional_verdict"] = "VOID"  # tamper without rehashing
    f.write_text(json.dumps(rec))
    id8 = f.stem.split("_")[-1]
    r = run_cli(tmp_path, "dream", "audit", id8)
    out = r.stdout
    assert '"content_hash_valid": false' in out
    assert '"audit_result": "FAIL"' in out


def test_audit_passes_untampered_receipt(tmp_path):
    assert run_cli(tmp_path, "dream").returncode == 0
    f = list(tmp_path.glob("*.json"))[0]
    id8 = f.stem.split("_")[-1]
    r = run_cli(tmp_path, "dream", "audit", id8)
    assert '"audit_result": "PASS"' in r.stdout
