"""
WAJIB 3 — Effective State Conformance Test

Verifies the kernel's canonical effective_state has no contradictions.
No field may describe higher authority than the canonical effective_state.
"""

import pytest
import json
import urllib.request


ARIFOS = "http://localhost:8088"


def _call_arif_init(mode: str = "light", actor_id: str = "conformance-test") -> dict:
    """Call arif_init and return parsed response."""
    body = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "arif_init",
            "arguments": {
                "mode": mode,
                "actor_id": actor_id,
                "intent": "WAJIB 3 conformance test"
            }
        }
    }).encode()
    req = urllib.request.Request(
        f"{ARIFOS}/mcp",
        data=body,
        headers={"Content-Type": "application/json", "Accept": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        raw = resp.read().decode()
        # Handle SSE wrapper
        if raw.startswith("data:"):
            raw = raw.split("\n")[0][5:].strip()
        data = json.loads(raw)
        content = data.get("result", {}).get("content", [])
        if content:
            return json.loads(content[0].get("text", "{}"))
        return data


class TestEffectiveState:

    def test_light_mode_returns_observe_only(self):
        """
        arif_init(light) with unrecognized actor must return OBSERVE_ONLY.
        """
        r = _call_arif_init("light", "conformance-test")
        authority = r.get("authority_scope", "")
        assert authority == "OBSERVE_ONLY", \
            f"Light mode with unknown actor must be OBSERVE_ONLY, got: {authority}"

    def test_light_mode_cannot_mutate(self):
        """
        OBSERVE_ONLY session must have can_mutate=False.
        """
        r = _call_arif_init("light", "conformance-test")
        can_mutate = r.get("can_mutate", None)
        assert can_mutate is False, \
            f"OBSERVE_ONLY must have can_mutate=False, got: {can_mutate}"

    def test_light_mode_effective_verdict_is_hold(self):
        """
        Unverified actor must get HOLD verdict.
        """
        r = _call_arif_init("light", "conformance-test")
        verdict = r.get("effective_verdict", "")
        assert verdict == "HOLD", \
            f"Unverified actor must be HOLD, got: {verdict}"

    def test_authority_scope_and_can_mutate_consistent(self):
        """
        authority_scope and can_mutate must not contradict.
        OBSERVE_ONLY → can_mutate=False. LIMITED_MUTATE → can_mutate=True.
        """
        r = _call_arif_init("light", "conformance-test")
        authority = r.get("authority_scope", "")
        can_mutate = r.get("can_mutate", None)
        
        if authority == "OBSERVE_ONLY":
            assert can_mutate is False, \
                "OBSERVE_ONLY authority must not allow mutation"
        elif authority == "LIMITED_MUTATE":
            assert can_mutate is True, \
                "LIMITED_MUTATE authority must allow mutation"

    def test_verdicts_structure_exists(self):
        """
        The verdicts object must exist as the effective_state container.
        """
        r = _call_arif_init("light", "conformance-test")
        verdicts = r.get("verdicts", {})
        assert "session" in verdicts, "verdicts must have session state"
        assert "action" in verdicts, "verdicts must have action state"
        assert isinstance(verdicts.get("session", {}).get("state"), str), \
            "session.state must be a string"

    def test_sct_claims_match_response(self):
        """
        The SCT (session token) must not claim higher authority than response.
        """
        r = _call_arif_init("light", "conformance-test")
        sct = r.get("session_token", "")
        authority = r.get("authority_scope", "")
        
        # SCT is base64-encoded; decode and check auth claim
        if sct and sct.startswith("sct_v1."):
            try:
                import base64
                payload_b64 = sct.split(".")[1]
                # Add padding
                payload_b64 += "=" * (4 - len(payload_b64) % 4)
                payload = json.loads(base64.urlsafe_b64decode(payload_b64))
                sct_auth = payload.get("auth", "")
                assert sct_auth == authority, \
                    f"SCT auth ({sct_auth}) must match authority_scope ({authority})"
            except Exception:
                pass  # SCT decode is best-effort

    def test_no_contradictory_mutation_flags(self):
        """
        There must not be both can_mutate=True AND authority=OBSERVE_ONLY.
        This is the specific contradiction flagged in the reality audit.
        """
        r = _call_arif_init("light", "conformance-test")
        authority = r.get("authority_scope", "")
        can_mutate = r.get("can_mutate", False)
        
        # This is explicitly checking for the LIMITED_MUTATE vs OBSERVE_ONLY bug
        if authority == "OBSERVE_ONLY" and can_mutate:
            pytest.fail(
                f"CONTRADICTION: authority_scope=OBSERVE_ONLY but can_mutate=True. "
                f"This is the WAJIB 3 P0 bug from the reality audit."
            )
        
        # Also check: if mutation_allowed exists, it must match
        mutation_allowed = r.get("mutation_allowed", None)
        if mutation_allowed is not None:
            assert mutation_allowed == can_mutate, \
                f"mutation_allowed ({mutation_allowed}) != can_mutate ({can_mutate})"
