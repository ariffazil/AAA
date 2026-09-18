#!/usr/bin/env python3
"""docforge.dispatch — get the sealed artifact to a human, and record that it landed.

STATE TRANSITION DISCIPLINE, APPLIED TO SENDING
  "Sent" is not a state. The chain is:

      PRODUCED != SENT != DELIVERED != OBSERVED != ACKNOWLEDGED

  A build that exits 0 has PRODUCED. Handing bytes to `hermes send` and reading
  its exit code gets you to SENT, and only if the transport confirms. Nothing
  here claims DELIVERED — that needs a receive-side signal that Hermes does not
  have for a bot push, so the field stays unset rather than being filled with a
  comfortable guess.

  This matters because the failure mode is silent: a briefing that quietly never
  arrives looks identical to one that arrived and was not read, right up until
  the morning the reader notices they have had no brief for a week.

WHAT IS ACTUALLY MEASURED
  `hermes send` returns a JSON result when asked. That result is recorded
  verbatim, not summarised, so a later audit can see what the transport said
  rather than what this module wished it had said.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class DeliveryResult:
    state: str            # PRODUCED | SENT | FAILED | TRANSPORT_ABSENT
    target: str
    artifact: str
    detail: str = ""
    transport_raw: dict | None = None

    def as_dict(self) -> dict:
        return {
            "state": self.state, "target": self.target,
            "artifact": self.artifact, "detail": self.detail,
            "transport_raw": self.transport_raw,
            "chain_note": ("PRODUCED != SENT != DELIVERED != OBSERVED != "
                           "ACKNOWLEDGED — this record reaches SENT at best; "
                           "no receive-side signal exists for a bot push."),
        }


def transport_available() -> tuple[bool, str]:
    p = shutil.which("hermes")
    if not p:
        return False, "hermes CLI not on PATH"
    try:
        r = subprocess.run([p, "send", "--help"], capture_output=True,
                           text=True, timeout=60)
        if r.returncode != 0:
            return False, f"hermes send unusable: exit {r.returncode}"
        return True, p
    except Exception as exc:  # noqa: BLE001
        return False, f"hermes send probe failed: {exc}"


def send(artifact: Path, target: str, caption: str = "",
         sidecar: Path | None = None) -> DeliveryResult:
    """Push the PDF (and its sidecar) to a target. Records what really happened."""
    ok, detail = transport_available()
    if not ok:
        return DeliveryResult("TRANSPORT_ABSENT", target, artifact.name, detail)
    if not artifact.is_file():
        return DeliveryResult("FAILED", target, artifact.name,
                              f"artifact missing: {artifact}")

    # MEDIA:<path> is the CLI's attachment mechanism; the caption rides with it.
    body = caption.strip()
    body += f"\n\nMEDIA:{artifact}"
    if sidecar and sidecar.is_file():
        body += f"\nMEDIA:{sidecar}"

    r = subprocess.run(["hermes", "send", "-t", target, "--json", body],
                       capture_output=True, text=True, timeout=180)
    raw: dict | None = None
    try:
        raw = json.loads(r.stdout)
    except Exception:  # noqa: BLE001 - keep the text if it is not JSON
        raw = {"stdout": r.stdout.strip()[:4000], "stderr": r.stderr.strip()[:2000]}

    if r.returncode != 0:
        return DeliveryResult("FAILED", target, artifact.name,
                              f"hermes send exit {r.returncode}: "
                              f"{r.stderr.strip()[:300] or r.stdout.strip()[:300]}",
                              raw)
    # A zero exit is SENT. It is explicitly NOT called delivered.
    return DeliveryResult("SENT", target, artifact.name,
                          "transport accepted the message; delivery and reading "
                          "are unverified and unverifiable from this side", raw)
