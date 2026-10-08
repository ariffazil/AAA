"""P2 deprecation stub test fixtures.

These verify that the 10 'advertised but not mounted' tools now return
honest DEPRECATED notices with the canonical replacement, instead of
'Unknown tool' errors.
"""
import json
import sys
import unittest
import urllib.request
import urllib.error
from pathlib import Path

URL = "http://127.0.0.1:8088/mcp"
SID = "SEAL-P2-TEST-2026-10-06"
META = {"io.modelcontextprotocol/protocolVersion": "2026-07-28",
        "io.modelcontextprotocol/clientCapabilities": {}}

DEPRECATED_TOOLS = [
    "arif_critique",
    "arif_compose",
    "arif_kernel_intercept",
    "arif_measure",
    "arif_ops_measure",
    "arif_bridge_connect",
    "wealth_dscr_leverage",
    "wealth_emv_downside",
    "wealth_irr_yield",
    "wealth_npv_reward",
]


class TestP2Deprecation(unittest.TestCase):
    """P2: all 10 advertised tools return DEPRECATED instead of Unknown."""

    def call(self, tool):
        body = {
            "jsonrpc": "2.0", "id": 1, "method": "tools/call",
            "params": {"name": tool, "arguments": {}, "_meta": META},
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "MCP-Protocol-Version": "2026-07-28",
            "Mcp-Method": "tools/call",
            "X-ArifOS-Actor": "arif",
            "mcp-session-id": SID,
            "Mcp-Name": tool,
        }
        req = urllib.request.Request(URL, json.dumps(body).encode(), headers)
        try:
            resp = urllib.request.urlopen(req, timeout=10)
            return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            return {"error": f"HTTP {e.code}", "body": e.read().decode()[:200]}
        except Exception as e:
            return {"error": str(e)}

    def test_1_no_unknown_tool_error(self):
        """T1: none of the 10 tools return 'Unknown tool' anymore."""
        for tool in DEPRECATED_TOOLS:
            resp = self.call(tool)
            self.assertNotIn("error", resp, f"{tool} should not return error")
            result = resp.get("result", {})
            content = result.get("content", [])
            # The text should mention DEPRECATED or WRONG_ORGAN
            self.assertTrue(
                any("DEPRECATED" in (c.get("text", "")) or "WRONG_ORGAN" in (c.get("text", ""))
                    for c in content if isinstance(c, dict)),
                f"{tool}: no DEPRECATED/WRONG_ORGAN marker in response",
            )

    def test_2_deprecation_response_shape(self):
        """T2: each tool returns the documented deprecation shape."""
        for tool in DEPRECATED_TOOLS:
            resp = self.call(tool)
            result = resp.get("result", {})
            self.assertIn("status", result, f"{tool}: missing status")
            self.assertIn(
                result["status"], ("DEPRECATED", "WRONG_ORGAN"),
                f"{tool}: unexpected status {result.get('status')}",
            )
            self.assertIn("tool", result)
            self.assertEqual(result["tool"], tool)
            self.assertIn("canonical_replacement", result)
            self.assertIn("f13_authorization", result, "must include F13 authorization field")

    def test_3_arif_critique_specific(self):
        """T3: arif_critique specifically recommends arif_heart_critique."""
        resp = self.call("arif_critique")
        result = resp.get("result", {})
        self.assertEqual(result.get("status"), "DEPRECATED")
        self.assertEqual(result.get("canonical_replacement"), "arif_heart_critique")

    def test_4_wealth_specific_points_to_wealth_mcp(self):
        """T4: wealth_* tools (not on arifOS) point to WEALTH MCP."""
        for tool in ["wealth_dscr_leverage", "wealth_emv_downside", "wealth_irr_yield", "wealth_npv_reward"]:
            resp = self.call(tool)
            result = resp.get("result", {})
            self.assertEqual(result.get("status"), "WRONG_ORGAN")
            self.assertIn("WEALTH MCP", result.get("canonical_replacement", ""))


if __name__ == "__main__":
    unittest.main(verbosity=2)
