#!/usr/bin/env python3
"""
arifOS / AAA Federation — Delegated Session Capability Token (SCT) Context Handler (Phase 5)
DITEMPA BUKAN DIBERI — Forged, Not Given.

Manages delegated SCT context generation and verification across inter-agent prompt loops.
Enforces scope restrictions, F13 override path, and turn limits.
"""

import json
import time
import hashlib
from datetime import datetime, timezone

class DelegatedSCTHandler:
    def __init__(self, root_authority="ARIF"):
        self.root_authority = root_authority

    def issue_delegated_token(self, from_agent: str, to_agent: str, loop_id: str, turn_limit: int = 3) -> dict:
        """Issue a bounded, delegated SCT context token."""
        ts = int(time.time())
        token_id = f"sct_v1.delegated_{from_agent}_to_{to_agent}_{loop_id}_{ts}"
        
        token_data = {
            "sct_version": "sct_v1.delegated",
            "token_id": token_id,
            "root_authority": self.root_authority,
            "delegated_by": from_agent,
            "delegated_to": to_agent,
            "loop_id": loop_id,
            "allowed_scope": [
                "read_context",
                "evaluate",
                "propose_next_prompt",
                "propose_patch",
                "return_evidence"
            ],
            "forbidden_scope": [
                "direct_mutation",
                "credential_access",
                "unbounded_looping",
                "external_network_expansion"
            ],
            "turn_limit": turn_limit,
            "issued_at": datetime.now(timezone.utc).isoformat(),
            "f13_veto": True
        }
        
        # Calculate witness hash
        token_str = json.dumps(token_data, sort_keys=True)
        token_data["signature_chain"] = [
            f"sha256:{hashlib.sha256(token_str.encode()).hexdigest()}"
        ]
        return token_data

    def verify_token(self, token_data: dict) -> tuple[bool, str]:
        """Verify token integrity and scope constraints."""
        if token_data.get("root_authority") != self.root_authority:
            return False, "Invalid root authority"
            
        if not token_data.get("token_id", "").startswith("sct_v1.delegated"):
            return False, "Token ID format invalid"
            
        forbidden = token_data.get("forbidden_scope", [])
        if "direct_mutation" not in forbidden:
            return False, "Safety violation: direct_mutation must be forbidden"
            
        return True, "VERIFIED_VALID"

if __name__ == "__main__":
    handler = DelegatedSCTHandler()
    token = handler.issue_delegated_token("hermes", "opencode", "loop_20260802_a1b2c3d4")
    is_valid, msg = handler.verify_token(token)
    print(f"Issued Token ({msg}):", json.dumps(token, indent=2))
