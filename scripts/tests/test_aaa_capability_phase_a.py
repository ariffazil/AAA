#!/usr/bin/env python3
"""
test_aaa_capability_phase_a.py — isolated unit tests for Phase A.

Run via:  python3 -m unittest test_aaa_capability_phase_a -v

Authorized by F13 directive, 2026-08-11 (SEAL_PHASE_A_ONLY).
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

# Ensure /root/AAA/scripts is on path
HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent
sys.path.insert(0, str(SCRIPTS))

from aaa_capability_loader import (  # noqa: E402
    CANONICAL_AXES,
    DOCTRINE_CANONICAL_NAMES,
    CapabilityBackend,
    CapabilityIndex,
    RegistryLoadError,
    load_registry,
)
from aaa_capability_validator import (  # noqa: E402
    INVARIANT_KEYS,
    ValidationReport,
    validate,
)
from aaa_capability_init import (  # noqa: E402
    InitReceipt,
    RECEIPT_DIR,
    _build_indicators,
    run_init,
    write_receipt,
)


REGISTRY_PATH = Path("/root/AAA/federation/AAA_CAPABILITY_REGISTRY.yaml")


# --- Fixtures (minimal valid registries for unit tests) ---

VALID_REGISTRY_YAML = """
version: v1
sovereign: ARIF
status: DRAFT
architectural_ratification:
  verdict: SEAL_ARCHITECTURE
  issued_by: ARIF
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
          hindsight: { F_rating: SAFE, enabled: false, seal: pending, transport: http, url: http://127.0.0.1:18087/mcp }
  understand:
    canonical_capabilities:
      code.navigate:
        backends:
          serena: { F_rating: HOLD, enabled: false, seal: pending, transport: stdio, gate: A-FORGE_lease }
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
          VAULT999: { F_rating: SAFE, enabled: true, transport: filesystem }
"""


# --- Loader tests ---

class LoaderTests(unittest.TestCase):

    def test_load_real_registry(self):
        """The actual registry file on disk must load."""
        index = load_registry(REGISTRY_PATH)
        self.assertIsInstance(index, CapabilityIndex)
        self.assertEqual(index.version, "v1")
        self.assertEqual(index.sovereign, "ARIF")
        self.assertEqual(index.architectural_verdict, "SEAL_ARCHITECTURE")
        # All 7 axes present
        for axis in CANONICAL_AXES:
            self.assertIn(axis, index.axes, f"axis '{axis}' missing from registry")
            self.assertGreater(len(index.axes[axis]), 0, f"axis '{axis}' empty")
        # All 7 doctrine capabilities present
        for cap in DOCTRINE_CANONICAL_NAMES:
            self.assertIn(cap, index.canonical_names, f"doctrine capability '{cap}' missing")
        # All backends disabled (per F13 directive)
        for name, b in index.backends.items():
            if name not in ("VAULT999", "arifFlow"):
                self.assertFalse(b.enabled, f"backend '{name}' should be disabled")
        # SHA-256 computed
        self.assertEqual(len(index.source_sha256), 64)
        # All backends have F_rating + transport + seal
        for b in index.backends.values():
            self.assertIn(b.F_rating, ("SAFE", "REVIEW", "HOLD"))
            self.assertIn(b.transport, ("stdio", "http", "filesystem"))
            self.assertIn(b.seal, ("pending", "ratifying", "sealed", "void"))

    def test_load_minimal_valid_registry(self):
        """A minimal valid registry (with all 7 axes + 7 doctrine caps) parses."""
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
            f.write(VALID_REGISTRY_YAML)
            path = f.name
        try:
            index = load_registry(path)
            self.assertEqual(len(index.axes), 7)
            self.assertEqual(len(index.canonical_names), 7)
            self.assertEqual(index.catalogued_count, 7)
            self.assertEqual(index.enabled_count, 1)  # VAULT999 is enabled
        finally:
            os.unlink(path)

    def test_missing_file_raises(self):
        with self.assertRaises(RegistryLoadError):
            load_registry("/tmp/does-not-exist-zzz.yaml")

    def test_unknown_axis_rejected(self):
        bad_yaml = VALID_REGISTRY_YAML.replace("sense:", "nonsense:")
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
            f.write(bad_yaml)
            path = f.name
        try:
            with self.assertRaises(RegistryLoadError) as cm:
                load_registry(path)
            self.assertIn("Unknown axis", str(cm.exception))
        finally:
            os.unlink(path)

    def test_invalid_F_rating_rejected(self):
        bad_yaml = VALID_REGISTRY_YAML.replace("F_rating: REVIEW", "F_rating: BOGUS")
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
            f.write(bad_yaml)
            path = f.name
        try:
            with self.assertRaises(RegistryLoadError):
                load_registry(path)
        finally:
            os.unlink(path)

    def test_empty_axes_rejected(self):
        bad_yaml = VALID_REGISTRY_YAML.replace(
            "canonical_capabilities:\n      reality.search:",
            "canonical_capabilities: {}"
        )
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
            f.write(bad_yaml)
            path = f.name
        try:
            with self.assertRaises(RegistryLoadError):
                load_registry(path)
        finally:
            os.unlink(path)


# --- Validator tests ---

class ValidatorTests(unittest.TestCase):

    def setUp(self):
        self.index = load_registry(REGISTRY_PATH)

    def test_real_registry_is_ready_readonly(self):
        report = validate(self.index)
        self.assertTrue(report.schema_valid)
        for inv in ("INV-11", "INV-12", "INV-13", "INV-14", "INV-15", "INV-16", "INV-17.a", "INV-17.b"):
            self.assertTrue(report.invariants_ok[inv], f"{inv} should be ok")
        self.assertTrue(report.is_ready_readonly)
        self.assertEqual(report.fail_closed_reasons, ())
        # All 7 doctrine capabilities are seen
        self.assertEqual(len(report.doctrine_capabilities_seen), 7)

    def test_enabled_without_seal_fails_closed(self):
        bad_yaml = VALID_REGISTRY_YAML.replace(
            "brave-search: { F_rating: REVIEW, enabled: false, seal: pending, transport: stdio }",
            "brave-search: { F_rating: REVIEW, enabled: true,  seal: pending, transport: stdio }"
        )
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
            f.write(bad_yaml)
            path = f.name
        try:
            index = load_registry(path)
            report = validate(index)
            self.assertFalse(report.is_ready_readonly)
            reasons = " ".join(report.fail_closed_reasons)
            self.assertIn("enabled_without_seal:brave-search", reasons)
        finally:
            os.unlink(path)

    def test_credential_leak_detected(self):
        # Inject a token-like literal into a backend note
        bad_yaml = VALID_REGISTRY_YAML.replace(
            "brave-search: { F_rating: REVIEW, enabled: false, seal: pending, transport: stdio }",
            "brave-search: { F_rating: REVIEW, enabled: false, seal: pending, transport: stdio, note: 'token ghp_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' }"
        )
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
            f.write(bad_yaml)
            path = f.name
        try:
            index = load_registry(path)
            report = validate(index)
            self.assertFalse(report.is_ready_readonly)
            reasons = " ".join(report.fail_closed_reasons)
            self.assertIn("credential_leak:", reasons)
            self.assertIn("brave-search", reasons)
        finally:
            os.unlink(path)

    def test_write_tools_ungated_fails(self):
        bad_yaml = VALID_REGISTRY_YAML.replace(
            "github: { F_rating: HOLD, enabled: false, seal: pending, transport: stdio, gate: A-FORGE_lease }",
            "github: { F_rating: HOLD, enabled: false, seal: pending, transport: stdio }"
        )
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
            f.write(bad_yaml)
            path = f.name
        try:
            index = load_registry(path)
            report = validate(index)
            self.assertFalse(report.invariants_ok["INV-16"])
            reasons = " ".join(report.fail_closed_reasons)
            self.assertIn("write_tools_ungated:github", reasons)
        finally:
            os.unlink(path)

    def test_doctrine_capabilities_missing_fails(self):
        # Remove one doctrine cap (reality.search) by emptying the sense axis
        bad_yaml = VALID_REGISTRY_YAML.replace(
            "sense:\n    canonical_capabilities:\n      reality.search:",
            "sense:\n    canonical_capabilities:\n      noncanonical:"
        )
        # Also need to add a backends key under noncanonical
        bad_yaml = bad_yaml.replace(
            "        backends:\n          brave-search:",
            "        backends:\n          dummy:"
        )
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
            f.write(bad_yaml)
            path = f.name
        try:
            index = load_registry(path)
            report = validate(index)
            self.assertFalse(report.is_ready_readonly)
            reasons = " ".join(report.fail_closed_reasons)
            self.assertIn("doctrine_capabilities_missing", reasons)
            self.assertIn("reality.search", reasons)
        finally:
            os.unlink(path)


# --- INIT tests ---

class InitTests(unittest.TestCase):

    def test_real_registry_init_returns_ready_readonly(self):
        receipt = run_init(REGISTRY_PATH)
        self.assertEqual(receipt.verdict, "READY_READONLY")
        self.assertEqual(receipt.receipt_type, "CAPABILITY_INIT")
        ind = receipt.indicators
        self.assertEqual(ind["REGISTRY"], "loaded")
        self.assertEqual(ind["SCHEMA"], "valid")
        self.assertEqual(ind["AXES"], 7)
        self.assertGreaterEqual(ind["BACKENDS"], 22)
        # Per F13 directive: all 22 non-witness backends disabled
        # Witness surface (VAULT999, arifFlow) may be enabled.
        self.assertGreaterEqual(ind["ENABLED"], 2)
        self.assertLessEqual(ind["ENABLED"], 2)
        self.assertEqual(ind["LEASES"], 0)
        self.assertEqual(ind["CREDENTIALS_EXPOSED"], 0)
        self.assertEqual(ind["MUTATIONS"], 0)
        self.assertEqual(ind["VERDICT"], "READY_READONLY")

    def test_init_with_missing_file_returns_hold(self):
        receipt = run_init("/tmp/does-not-exist-phase-a.yaml")
        self.assertEqual(receipt.verdict, "HOLD")
        self.assertEqual(receipt.receipt_type, "CAPABILITY_HOLD")
        self.assertIn("YAML_MISSING_OR_INVALID", receipt.fail_closed_reasons[0])
        ind = receipt.indicators
        self.assertEqual(ind["REGISTRY"], "not_loaded")
        self.assertEqual(ind["SCHEMA"], "not_validated")
        self.assertEqual(ind["VERDICT"], "HOLD")

    def test_init_receipt_serializable_to_json(self):
        receipt = run_init(REGISTRY_PATH)
        d = receipt.to_dict()
        # Round-trip through json
        s = json.dumps(d)
        d2 = json.loads(s)
        self.assertEqual(d2["verdict"], "READY_READONLY")
        self.assertEqual(d2["registry_sha256"], receipt.registry_sha256)

    def test_init_receipt_persists_to_disk(self):
        receipt = run_init(REGISTRY_PATH)
        path = write_receipt(receipt, dest_dir=tempfile.mkdtemp())
        self.assertIsNotNone(path)
        self.assertTrue(Path(path).exists())
        with open(path) as f:
            data = json.load(f)
        self.assertEqual(data["verdict"], "READY_READONLY")


# --- Negative proof tests (no side effects) ---

class NoSideEffectsTests(unittest.TestCase):

    def test_no_subprocess_spawned(self):
        """Verify the scripts do not import subprocess or threading in a way that spawns."""
        import aaa_capability_loader
        import aaa_capability_validator
        import aaa_capability_init
        # subprocess should not be imported by any of these
        for mod in (aaa_capability_loader, aaa_capability_validator, aaa_capability_init):
            self.assertFalse(hasattr(mod, "subprocess"),
                             f"{mod.__name__} should not reference subprocess")

    def test_no_network_module_imported(self):
        """Verify the scripts do not import networking modules."""
        import aaa_capability_loader
        import aaa_capability_validator
        import aaa_capability_init
        forbidden = ("requests", "urllib3", "httpx", "aiohttp", "socket")
        for mod in (aaa_capability_loader, aaa_capability_validator, aaa_capability_init):
            for f in forbidden:
                self.assertFalse(hasattr(mod, f),
                                 f"{mod.__name__} should not import {f}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
