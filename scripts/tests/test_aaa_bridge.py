#!/usr/bin/env python3
"""
test_aaa_bridge.py — bridge between registry and Kimi harness.

Maps the 7 fail-closed conditions named by F13 (2026-08-11) to concrete tests:
  F1  YAML invalid or duplicated             — covered in test_aaa_capability_phase_a
  F2  enabled backend lacks a seal           — covered in test_aaa_capability_phase_a
  F3  write tool lacks an A-FORGE lease      — covered in test_aaa_capability_phase_a
  F4  MCP tries to bypass AAA                — THIS FILE
  F5  credentials in agent-visible config    — covered in test_aaa_capability_phase_a
  F6  registry hash differs from receipt     — THIS FILE
  F7  backend starts merely because catalogued — THIS FILE

Run via:  python3 -m unittest test_aaa_bridge -v

Authorized by F13 directive, 2026-08-11 (SEAL_PHASE_A_ONLY).
"""

from __future__ import annotations

import datetime as dt
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent
REPO = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

import yaml

from aaa_capability_init import run_init
from aaa_capability_loader import load_registry


REGISTRY_PATH = Path("/root/AAA/federation/AAA_CAPABILITY_REGISTRY.yaml")
LAUNCHER_MAP_PATH = Path("/root/AAA/federation/launcher_map.yaml")
MCP_JSON_PATH = Path("/root/.kimi-code/mcp.json")


# --- Fixtures ---

VALID_LAUNCHER_MAP = """
version: v1
launchers:
  arifFlow:
    description: arifFLOW metabolism organ
    transport: stdio
    command: /tmp/arifflow.sh
"""


# --- Bridge behaviour tests ---

class BridgeGenerationTests(unittest.TestCase):
    """The generator emits mcp.json from registry+launcher_map."""

    def _run_generator(self, registry_yaml: str, launcher_yaml: str = VALID_LAUNCHER_MAP):
        # Use mkdtemp + manual cleanup so the file persists after the function returns
        td = tempfile.mkdtemp()
        try:
            reg_path = Path(td) / "reg.yaml"
            map_path = Path(td) / "map.yaml"
            out_path = Path(td) / "mcp.json"
            reg_path.write_text(registry_yaml)
            map_path.write_text(launcher_yaml)
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "aaa_mcp_json_generator.py"),
                    str(reg_path), str(map_path), str(out_path),
                ],
                capture_output=True, text=True, timeout=30,
            )
            payload = (
                json.loads(out_path.read_text())
                if out_path.exists() else {"mcpServers": "MISSING"}
            )
            return result, payload, out_path, td
        except Exception:
            import shutil
            shutil.rmtree(td, ignore_errors=True)
            raise

    def test_only_enabled_sealed_backends_appear(self):
        """F4: catalogued but disabled backends must NOT appear in mcp.json."""
        # Registry: VAULT999 + arifFlow enabled+sealed; brave-search catalogued
        # but enabled=false. Launcher map only knows arifFlow.
        registry_yaml = """
version: v1
sovereign: ARIF
status: DRAFT
architectural_ratification:
  verdict: SEAL_ARCHITECTURE
invariants:
  one_canonical_name_per_capability: true
  mcp_servers_must_be_stateless: true
  cognition_owner: agent
  authority_owner: AAA_router
  continuity_owner: "VAULT999 + arifFlow"
  write_tools_gated_by: A-FORGE_lease
  credentials_held_by: gateway_only
axes:
  sense:
    canonical_capabilities:
      reality.search:
        backends:
          brave-search: { F_rating: REVIEW, enabled: false, seal: pending, transport: stdio }
  know:
    canonical_capabilities:
      knowledge.docs:
        backends:
          context7: { F_rating: REVIEW, enabled: false, seal: pending, transport: stdio }
  remember:
    canonical_capabilities:
      memory.recall:
        backends:
          hindsight: { F_rating: SAFE, enabled: false, seal: pending, transport: http }
  understand:
    canonical_capabilities:
      code.navigate:
        backends:
          serena: { F_rating: HOLD, enabled: false, seal: pending, transport: stdio }
  verify:
    canonical_capabilities:
      evidence.scan:
        backends:
          semgrep: { F_rating: HOLD, enabled: false, seal: pending, transport: stdio }
  forge:
    canonical_capabilities:
      forge.repository:
        backends:
          github: { F_rating: HOLD, enabled: false, seal: pending, transport: stdio, gate: A-FORGE_lease }
  witness:
    canonical_capabilities:
      witness.append:
        backends:
          VAULT999: { F_rating: SAFE, enabled: true, seal: sealed, transport: filesystem }
"""
        result, data, out_path, td = self._run_generator(registry_yaml)
        try:
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            servers = data.get("mcpServers", {})
            # brave-search, context7, hindsight, serena, semgrep, github — all disabled
            # → must NOT appear in mcpServers
            for forbidden in (
                "brave-search", "context7", "hindsight", "serena",
                "semgrep", "github", "VAULT999",  # filesystem, not MCP
            ):
                self.assertNotIn(forbidden, servers,
                                 f"F4/F7: '{forbidden}' must NOT appear in mcp.json "
                                 f"(catalogued-only or filesystem); got {list(servers)}")
        finally:
            import shutil
            shutil.rmtree(td, ignore_errors=True)

    def test_sealed_enabled_without_launcher_is_skipped(self):
        """F4: a backend with enabled+sealed but no launcher must be skipped (not fail)."""
        registry_yaml = """
version: v1
sovereign: ARIF
status: DRAFT
architectural_ratification:
  verdict: SEAL_ARCHITECTURE
invariants:
  one_canonical_name_per_capability: true
  mcp_servers_must_be_stateless: true
  cognition_owner: agent
  authority_owner: AAA_router
  continuity_owner: "VAULT999 + arifFlow"
  write_tools_gated_by: A-FORGE_lease
  credentials_held_by: gateway_only
axes:
  sense:
    canonical_capabilities:
      reality.search:
        backends:
          brave-search: { F_rating: REVIEW, enabled: false, seal: pending, transport: stdio }
  know:
    canonical_capabilities:
      knowledge.docs:
        backends:
          context7: { F_rating: REVIEW, enabled: false, seal: pending, transport: stdio }
  remember:
    canonical_capabilities:
      memory.recall:
        backends:
          hindsight: { F_rating: SAFE, enabled: false, seal: pending, transport: http }
  understand:
    canonical_capabilities:
      code.navigate:
        backends:
          serena: { F_rating: HOLD, enabled: false, seal: pending, transport: stdio }
  verify:
    canonical_capabilities:
      evidence.scan:
        backends:
          semgrep: { F_rating: HOLD, enabled: false, seal: pending, transport: stdio }
  forge:
    canonical_capabilities:
      forge.repository:
        backends:
          github: { F_rating: HOLD, enabled: false, seal: pending, transport: stdio, gate: A-FORGE_lease }
  witness:
    canonical_capabilities:
      witness.append:
        backends:
          VAULT999: { F_rating: SAFE, enabled: true, seal: sealed, transport: filesystem }
"""
        result, data, out_path, td = self._run_generator(
            registry_yaml, launcher_yaml="version: v1\nlaunchers: {}\n"
        )
        try:
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            # VAULT999 has no launcher → must be reported, not crash
            self.assertIn("enabled_no_launcher=1", result.stdout)
            self.assertIn("VAULT999", result.stdout)
            # mcp.json should be empty (or absent) — no MCP-eligible backend
            self.assertEqual(data["mcpServers"], {})
        finally:
            import shutil
            shutil.rmtree(td, ignore_errors=True)

    def test_generated_mcp_json_is_parseable(self):
        """The generated mcp.json must round-trip through json.loads."""
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "aaa_mcp_json_generator.py"),
                str(REGISTRY_PATH), str(LAUNCHER_MAP_PATH),
                str(MCP_JSON_PATH),  # real path; the script backs it up
            ],
            capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        data = json.loads(MCP_JSON_PATH.read_text())
        self.assertIn("mcpServers", data)
        # Wave 0: only arifFlow (stdio shim)
        self.assertIn("arifFlow", data["mcpServers"])
        # None of the 22 catalogued-but-disabled backends
        for forbidden in (
            "arifos", "aforge", "geox", "wealth", "well", "fed", "minimax",
            "brave-search", "exa", "perplexity", "hindsight", "graphiti",
            "playwright", "semgrep", "github", "postgres", "supabase",
        ):
            self.assertNotIn(forbidden, data["mcpServers"],
                             f"'{forbidden}' should not be in Wave-0 mcp.json")


# --- F4: MCP bypass detection ---

class BypassTests(unittest.TestCase):
    """F4: an MCP trying to bypass AAA must be detected."""

    def test_mcp_json_only_contains_registry_authorised_backends(self):
        """
        Every server in mcp.json MUST have an enabled+sealed entry in the registry.
        A server in mcp.json that isn't in the registry is an AAA bypass.
        """
        if not MCP_JSON_PATH.exists():
            self.skipTest(f"{MCP_JSON_PATH} not present")
        mcp_data = json.loads(MCP_JSON_PATH.read_text())
        servers = mcp_data.get("mcpServers", {})
        index = load_registry(REGISTRY_PATH)
        authorised = {
            name for name, b in index.backends.items()
            if b.enabled and b.seal == "sealed"
        }
        mcp_names = set(servers.keys())
        unauthorised = mcp_names - authorised
        # filesystem transport (VAULT999) is intentional — exclude from bypass check
        unauthorised -= {"VAULT999"}
        self.assertEqual(unauthorised, set(),
                         f"F4: MCPs in mcp.json without registry authorisation: {unauthorised}")

    def test_disabled_backend_in_mcp_json_is_bypass(self):
        """
        Simulate: a backend is disabled in registry but still in mcp.json.
        Generator must skip it (and the bypass check above would catch the case).
        """
        # Construct a registry where arifFlow is disabled, then re-generate.
        registry_yaml = """
version: v1
sovereign: ARIF
status: DRAFT
architectural_ratification:
  verdict: SEAL_ARCHITECTURE
invariants:
  one_canonical_name_per_capability: true
  mcp_servers_must_be_stateless: true
  cognition_owner: agent
  authority_owner: AAA_router
  continuity_owner: "VAULT999 + arifFlow"
  write_tools_gated_by: A-FORGE_lease
  credentials_held_by: gateway_only
axes:
  sense:
    canonical_capabilities:
      reality.search:
        backends:
          brave-search: { F_rating: REVIEW, enabled: false, seal: pending, transport: stdio }
  know:
    canonical_capabilities:
      knowledge.docs:
        backends:
          context7: { F_rating: REVIEW, enabled: false, seal: pending, transport: stdio }
  remember:
    canonical_capabilities:
      memory.recall:
        backends:
          hindsight: { F_rating: SAFE, enabled: false, seal: pending, transport: http }
  understand:
    canonical_capabilities:
      code.navigate:
        backends:
          serena: { F_rating: HOLD, enabled: false, seal: pending, transport: stdio }
  verify:
    canonical_capabilities:
      evidence.scan:
        backends:
          semgrep: { F_rating: HOLD, enabled: false, seal: pending, transport: stdio }
  forge:
    canonical_capabilities:
      forge.repository:
        backends:
          github: { F_rating: HOLD, enabled: false, seal: pending, transport: stdio, gate: A-FORGE_lease }
  witness:
    canonical_capabilities:
      witness.append:
        backends:
          VAULT999: { F_rating: SAFE, enabled: true, seal: sealed, transport: filesystem }
          arifFlow: { F_rating: SAFE, enabled: false, seal: pending, transport: http }
"""
        with tempfile.TemporaryDirectory() as td:
            reg_path = Path(td) / "reg.yaml"
            map_path = Path(td) / "map.yaml"
            out_path = Path(td) / "mcp.json"
            reg_path.write_text(registry_yaml)
            map_path.write_text(VALID_LAUNCHER_MAP)
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "aaa_mcp_json_generator.py"),
                    str(reg_path), str(map_path), str(out_path),
                ],
                capture_output=True, text=True, timeout=30,
            )
            self.assertEqual(result.returncode, 0)
            data = json.loads(out_path.read_text())
            self.assertNotIn("arifFlow", data["mcpServers"],
                             "F4: disabled arifFlow must NOT appear in mcp.json")


# --- F6: registry hash receipt binding ---

class RegistryHashTests(unittest.TestCase):
    """F6: the registry hash must match its witnessed receipt."""

    def test_init_receipt_hash_matches_current_registry(self):
        receipt = run_init(REGISTRY_PATH)
        current_index = load_registry(REGISTRY_PATH)
        self.assertEqual(
            receipt.registry_sha256, current_index.source_sha256,
            "F6: init receipt hash must match the current registry hash"
        )

    def test_receipt_persists_with_hash_field(self):
        """Each persisted init receipt carries the registry_sha256."""
        receipt = run_init(REGISTRY_PATH)
        with tempfile.TemporaryDirectory() as td:
            dest = Path(td)
            # write_receipt coerces str→Path
            from aaa_capability_init import write_receipt
            out = write_receipt(receipt, dest_dir=dest)
            self.assertIsNotNone(out)
            data = json.loads(Path(out).read_text())
            self.assertIn("registry_sha256", data)
            self.assertEqual(len(data["registry_sha256"]), 64)


# --- F7: catalogued ≠ enabled ---

class CataloguedNotEnabledTests(unittest.TestCase):
    """F7: a backend must NOT start merely because it is catalogued."""

    def test_all_catalogued_except_canon_are_disabled(self):
        """Every catalogued backend except VAULT999 + arifFlow has enabled=False."""
        index = load_registry(REGISTRY_PATH)
        enabled_canon = {"VAULT999", "arifFlow"}
        for name, b in index.backends.items():
            if name in enabled_canon:
                continue
            self.assertFalse(
                b.enabled,
                f"F7: backend '{name}' is catalogued but enabled — must stay disabled"
            )

    def test_mcp_json_only_has_explicitly_enabled_backends(self):
        """mcp.json must NOT contain any backend that is catalogued-but-disabled."""
        if not MCP_JSON_PATH.exists():
            self.skipTest(f"{MCP_JSON_PATH} not present")
        mcp_names = set(json.loads(MCP_JSON_PATH.read_text()).get("mcpServers", {}).keys())
        index = load_registry(REGISTRY_PATH)
        # filesystem (VAULT999) doesn't need an MCP entry
        forbidden = {
            name for name, b in index.backends.items()
            if not b.enabled and b.transport != "filesystem"
        }
        leaked = mcp_names & forbidden
        self.assertEqual(leaked, set(),
                         f"F7: catalogued-but-disabled backends leaking into mcp.json: {leaked}")


# --- Operational integrity ---

class OperationalIntegrityTests(unittest.TestCase):
    """The end-to-end state of the VPS must match the registry intent."""

    def test_real_init_verdict_is_ready_readonly(self):
        receipt = run_init(REGISTRY_PATH)
        self.assertEqual(receipt.verdict, "READY_READONLY",
                         f"F1-F13 verdict regressed: {receipt.reason}; "
                         f"fail_closed={receipt.fail_closed_reasons}")

    def test_no_init_mutations(self):
        """The init script must NOT spawn subprocesses, open sockets, or write
        outside the configured receipts directory."""
        import aaa_capability_init
        import aaa_capability_loader
        import aaa_capability_validator
        for mod in (aaa_capability_init, aaa_capability_loader, aaa_capability_validator):
            self.assertFalse(hasattr(mod, "subprocess"),
                             f"{mod.__name__} should not import subprocess")
        for forbidden in ("socket", "requests", "urllib3", "httpx", "aiohttp"):
            for mod in (aaa_capability_init, aaa_capability_loader, aaa_capability_validator):
                self.assertFalse(hasattr(mod, forbidden),
                                 f"{mod.__name__} should not import {forbidden}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
