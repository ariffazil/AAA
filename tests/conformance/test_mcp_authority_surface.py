#!/usr/bin/env python3
"""
Contract test — MCP capability authority surface (S-01 canary).

Invariants under test:
  1. The generator emits the xerj lane with a POSITIVE read-tool allowlist.
  2. Mutation tools are never part of the emitted lane.
  3. READ_ONLY without an explicit allowlist fails closed.
  4. Unknown/unclassified tools are never implicitly allowed.
  5. Generation is deterministic.
  6. Active runtime harness configs are unchanged by generation-to-temp.

Scope note: this test governs the xerj declaration only. It does NOT claim
ownership of the full MCP surface (15 of 23 live Kimi servers remain
out-of-band; adjudication is a separate slice).

Run:
  python3 -m pytest tests/conformance/test_mcp_authority_surface.py -q
  python3 -m unittest tests.conformance.test_mcp_authority_surface -v
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = REPO / "scripts"
REGISTRY = REPO / "federation" / "AAA_CAPABILITY_REGISTRY.yaml"
LAUNCHER_MAP = REPO / "federation" / "launcher_map.yaml"
GENERATOR = SCRIPTS / "aaa_mcp_json_generator.py"

sys.path.insert(0, str(SCRIPTS))
import aaa_mcp_json_generator as gen  # noqa: E402

MUTATION_TOOLS = {"xerj_memory_store", "xerj_brain_link", "xerj_brain_unlink"}
LIVE_CONFIGS = [
    Path("/root/.kimi-code/mcp.json"),
    Path("/root/.mcp.json"),
    Path("/root/.qwen/settings.json"),
    Path("/root/.config/opencode/opencode.json"),
    Path("/root/.gemini/settings.json"),
    Path("/root/.codex/config.toml"),
    Path("/root/HERMES/config.yaml"),
]


def _generate(target: Path, receipt_dir: Path) -> subprocess.CompletedProcess:
    env = dict(os.environ, MCPGEN_RECEIPT_DIR=str(receipt_dir))
    return subprocess.run(
        [
            sys.executable,
            str(GENERATOR),
            str(REGISTRY),
            str(LAUNCHER_MAP),
            str(target),
        ],
        capture_output=True,
        text=True,
        timeout=60,
        env=env,
    )


def _xerj_backend() -> dict:
    registry = yaml.safe_load(REGISTRY.read_text())
    return registry["axes"]["remember"]["canonical_capabilities"]["memory.recall"]["backends"]["xerj"]


def _hashes(paths: list[Path]) -> dict[str, str]:
    out = {}
    for p in paths:
        if p.exists():
            out[str(p)] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


class XerjAuthoritySurfaceTests(unittest.TestCase):
    def test_xerj_is_generated_with_read_allowlist(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / "mcp.json"
            cp = _generate(target, Path(td) / "receipts")
            self.assertEqual(cp.returncode, 0, cp.stderr or cp.stdout)

            cfg = json.loads(target.read_text())
            xerj = cfg["mcpServers"]["xerj"]
            args = xerj["args"]

            self.assertIn("--include-tools", args)
            emitted = args[args.index("--include-tools") + 1].split(",")
            self.assertEqual(set(emitted), set(_xerj_backend()["allowed_tools"]))

    def test_xerj_generated_lane_excludes_mutation_tools(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / "mcp.json"
            cp = _generate(target, Path(td) / "receipts")
            self.assertEqual(cp.returncode, 0, cp.stderr or cp.stdout)

            args = json.loads(target.read_text())["mcpServers"]["xerj"]["args"]
            emitted = set(args[args.index("--include-tools") + 1].split(","))
            self.assertTrue(emitted.isdisjoint(MUTATION_TOOLS))

    def test_read_only_backend_without_allowlist_fails_closed(self):
        backend = {
            "authority_class": "READ_ONLY",
            "mutation_allowed": False,
            "known_tools": ["xerj_search"],
            "forbidden_tools": [],
            # allowed_tools deliberately absent
        }
        with self.assertRaises(gen.ConfigurationError):
            gen.validate_authority("xerj", backend)

    def test_unknown_tool_is_not_implicitly_allowed(self):
        backend = {
            "authority_class": "READ_ONLY",
            "mutation_allowed": False,
            "known_tools": ["xerj_search", "xerj_new_unknown_tool"],
            "allowed_tools": ["xerj_search"],
            "forbidden_tools": [],
            "tool_surface_sha256": gen.tool_surface_sha256(["xerj_search", "xerj_new_unknown_tool"]),
        }
        with self.assertRaises(gen.AuthorityClassificationError):
            gen.validate_authority("xerj", backend)

    def test_forbidden_tool_in_allowlist_fails(self):
        known = ["xerj_search", "xerj_memory_store"]
        backend = {
            "authority_class": "READ_ONLY",
            "mutation_allowed": False,
            "known_tools": known,
            "allowed_tools": known,
            "forbidden_tools": ["xerj_memory_store"],
            "tool_surface_sha256": gen.tool_surface_sha256(known),
        }
        with self.assertRaises(gen.AuthorityClassificationError):
            gen.validate_authority("xerj", backend)

    def test_generation_is_deterministic(self):
        with tempfile.TemporaryDirectory() as td:
            a = Path(td) / "a.json"
            b = Path(td) / "b.json"
            receipts = Path(td) / "receipts"
            self.assertEqual(_generate(a, receipts).returncode, 0)
            self.assertEqual(_generate(b, receipts).returncode, 0)
            self.assertEqual(a.read_bytes(), b.read_bytes())

    def test_runtime_configs_unchanged_by_temp_generation(self):
        before = _hashes(LIVE_CONFIGS)
        with tempfile.TemporaryDirectory() as td:
            cp = _generate(Path(td) / "mcp.json", Path(td) / "receipts")
            self.assertEqual(cp.returncode, 0, cp.stderr or cp.stdout)
        after = _hashes(LIVE_CONFIGS)
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main(verbosity=2)
