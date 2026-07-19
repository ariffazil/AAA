"""
WAJIB 1 — Execution Category Tests

Tests 2, 3, 8: executor self-approval, unleased mutation, command vs outcome.
"""

import pytest
import urllib.request
import json

AFORGE_MCP = "http://localhost:7072"


def _post_mcp(method: str, params: dict = None) -> dict:
    """Send a JSON-RPC MCP request to A-FORGE."""
    body = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params or {},
    }
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        f"{AFORGE_MCP}/mcp",
        data=data,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return {
            "error": {
                "code": e.code,
                "message": str(e),
            },
            "status_code": e.code,
        }


class TestExecution:

    def test_unleased_mutation_fails_closed(self, federation_healthy):
        """
        TEST 3: Unleased mutation fails closed.
        
        Sending a forge_execute without lease_id or valid session must fail.
        """
        # Attempt mutation without any auth
        resp = _post_mcp("tools/call", {
            "name": "forge_execute",
            "arguments": {"task": "echo unauthorized"},
        })
        
        # Must not succeed
        is_error = "error" in resp
        has_failure = not resp.get("result", {}).get("content", [{}])[0].get("text", "").startswith("✅")
        
        assert is_error or has_failure, \
            f"Unleased mutation should have been blocked but got: {json.dumps(resp, indent=2)[:500]}"

    def test_forge_shell_denied_without_auth(self, federation_healthy):
        """
        TEST 3 extended: forge_shell (high-risk) must be denied without auth.
        A-FORGE should return POLICY_DENY for unauthenticated stateless-client.
        """
        resp = _post_mcp("tools/call", {
            "name": "forge_shell",
            "arguments": {"command": "echo test", "cwd": "/tmp"},
        })
        
        # A-FORGE correctly denies with POLICY_DENY for stateless-client
        result_text = str(resp)
        is_denied = (
            "POLICY_DENY" in result_text
            or "DENY" in result_text
            or "error" in resp
            or "denied" in result_text.lower()
        )
        
        assert is_denied, \
            f"forge_shell without auth must be POLICY_DENY, got: {json.dumps(resp, indent=2)[:500]}"

    @pytest.mark.xfail(strict=True, reason="WAJIB 2: Independent verification lane not yet built")
    def test_executor_cannot_approve_own_execution(self):
        """
        TEST 2: Executor (A-FORGE) cannot approve its own execution.
        forge_approve must refuse — only arifOS can adjudicate.
        """
        resp = _post_mcp("tools/call", {
            "name": "forge_approve",
            "arguments": {"holdId": "test-fake-hold"},
        })
        # forge_approve code says "Refuses approval — cannot self-authorize"
        assert "error" in resp or "refuse" in str(resp).lower() or "cannot" in str(resp).lower()

    def test_command_success_not_equal_outcome_verification(self):
        """
        TEST 8: Command success (exit code 0) ≠ outcome verification.
        
        Requires the independent verification lane (WAJIB 2) to be built.
        Once built: execute a mutation that reports success, then verify
        the verifier lane independently confirms or denies the outcome.
        """
        pass  # Will be implemented when WAJIB 2 is complete
