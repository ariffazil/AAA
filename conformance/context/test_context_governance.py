"""
WAJIB 1 — Context Category Tests

Test 17: Agent-authored boot context cannot become policy without ratification.
"""

import pytest
from pathlib import Path


class TestContextGovernance:

    def test_next_agent_init_exists(self):
        """NEXT_AGENT_INIT.md must exist and be readable."""
        p = Path("/root/AAA/prompts/NEXT_AGENT_INIT.md")
        assert p.exists(), "NEXT_AGENT_INIT.md not found"
        content = p.read_text()
        assert len(content) > 50, "NEXT_AGENT_INIT.md is too short"

    def test_desired_state_is_draft_only(self):
        """DESIRED_STATE.md must be marked DRAFT TARGET STATE."""
        p = Path("/root/AAA/docs/DESIRED_STATE.md")
        if p.exists():
            content = p.read_text()
            assert "DRAFT" in content, "DESIRED_STATE.md must declare DRAFT status"

    def test_reality_audit_exists(self):
        """REALITY_AUDIT must exist and be committed."""
        p = Path("/root/AAA/docs/REALITY_AUDIT_2026-07-19.md")
        assert p.exists(), "REALITY_AUDIT not found"

    @pytest.mark.xfail(strict=True, reason="WAJIB 9: Context governance manifest not yet built")
    def test_agent_authored_boot_context_cannot_become_policy(self):
        """
        TEST 17: Agent-authored boot context cannot become policy without ratification.

        Once WAJIB 9 is complete, verify:
        - Every durable context artifact has a classification (Observation,
          Operational handoff, Guidance, Policy, Constitution, Memory)
        - Guidance cannot upgrade to Policy without kernel review
        - Agent-authored INIT files are advisory, never binding
        - context_manifest fields are enforced (author, approval, expiry, hash)
        """
        pytest.skip("Not yet implemented — awaiting WAJIB dependency")
