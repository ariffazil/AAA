import pytest

from email_transport import GovernanceRequiredError, build_email_intent, send_email


def test_email_intent_contains_no_provider_credentials() -> None:
    intent = build_email_intent("Status", "All healthy", "owner@example.test")

    payload = intent.to_dict()
    assert payload["executor"] == "A-FORGE"
    assert payload["judge"] == "arifOS"
    assert "api_key" not in payload
    assert "provider" not in payload


def test_aaa_cannot_send_email_directly() -> None:
    with pytest.raises(GovernanceRequiredError, match="cannot send"):
        send_email("Status", "All healthy", "owner@example.test")
