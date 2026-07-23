"""AAA email intent envelope.

AAA is a connection plane, not an execution organ. This module only constructs
an email intent that can be judged by arifOS and executed by A-FORGE. It never
loads provider credentials or performs network I/O.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence


class GovernanceRequiredError(RuntimeError):
    """Raised when legacy code attempts direct delivery from AAA."""


@dataclass(frozen=True)
class EmailIntent:
    subject: str
    body: str
    recipients: tuple[str, ...]
    content_type: str = "text/plain"
    reply_to: str | None = None
    action_class: str = "EXTERNAL_COMMUNICATION"
    executor: str = "A-FORGE"
    judge: str = "arifOS"

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def build_email_intent(
    subject: str,
    body: str,
    to: str | Sequence[str],
    *,
    html: bool = False,
    reply_to: str | None = None,
) -> EmailIntent:
    """Build a provider-neutral intent for the governed execution lane."""
    recipients = (to,) if isinstance(to, str) else tuple(to)
    if not subject.strip():
        raise ValueError("email subject cannot be empty")
    if not body.strip():
        raise ValueError("email body cannot be empty")
    if not recipients or any(not value.strip() for value in recipients):
        raise ValueError("at least one non-empty recipient is required")
    return EmailIntent(
        subject=subject,
        body=body,
        recipients=recipients,
        content_type="text/html" if html else "text/plain",
        reply_to=reply_to,
    )


def send_email(*args, **kwargs) -> bool:
    """Fail closed: direct outbound email from AAA is constitutionally invalid."""
    intent = build_email_intent(*args, **kwargs)
    raise GovernanceRequiredError(
        "AAA cannot send external communications directly; submit this EmailIntent "
        f"to arifOS for judgment and A-FORGE execution (recipients={len(intent.recipients)})"
    )


def build_agent_alert(
    agent_name: str,
    status: str,
    detail: str = "",
    to: str = "arifbfazil@gmail.com",
) -> EmailIntent:
    subject = f"[AAA] {agent_name} — {status}"
    body = f"Agent: {agent_name}\nStatus: {status}\n"
    if detail:
        body += f"\n{detail}\n"
    return build_email_intent(subject, body, to)


def build_federation_health(
    organ_states: dict[str, bool],
    to: str = "arifbfazil@gmail.com",
) -> EmailIntent:
    degraded = [name for name, healthy in organ_states.items() if not healthy]
    status = "ALL HEALTHY" if not degraded else f"{len(degraded)} DEGRADED"
    lines = [f"Federation Health Check — {len(organ_states)} organs"]
    lines.extend(f"{'OK' if healthy else 'DEGRADED'}: {name}" for name, healthy in organ_states.items())
    if degraded:
        lines.append(f"Degraded: {', '.join(degraded)}")
    return build_email_intent(
        subject=f"[AAA] Federation Health — {status}",
        body="\n".join(lines),
        to=to,
    )


__all__ = [
    "EmailIntent",
    "GovernanceRequiredError",
    "build_agent_alert",
    "build_email_intent",
    "build_federation_health",
    "send_email",
]
