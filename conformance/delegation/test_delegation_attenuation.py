"""
WAJIB 1 — Delegation Category Tests

Test 15: Child authority must not exceed parent authority.
"""

import pytest


class TestDelegation:

    @pytest.mark.xfail(strict=True, reason="WAJIB 4: Delegation attenuation not yet built")
    def test_child_cannot_exceed_parent_authority(self):
        """
        TEST 15: Delegated child cannot exceed parent authority.

        Once WAJIB 4 is complete, verify:
        - OBSERVE parent → MUTATE child: DENIED
        - Expired parent → child call: DENIED
        - Revoked parent → existing child: DENIED
        - Missing lineage → DENIED
        - Child re-delegation when prohibited: DENIED
        - Scope widening by child: DENIED
        - Session ID substitution: DENIED
        - Parallel child authority aggregation: DENIED
        """
        pytest.skip("Not yet implemented — awaiting WAJIB dependency")
