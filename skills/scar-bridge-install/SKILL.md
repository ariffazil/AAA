#!/usr/bin/env python3
"""
scar_bridge_install_template.py — Canonical Skill Template for Scar-Bridge Step 5
2026-09-08 · F13 Ratified · Promoted from forge_work to canonical

This is the procedural template for installing scars as gates.
Any agent can follow this template to convert experience into constraint.

Usage:
  from scar_bridge_install_template import install Scar

  Scar.install(
      experience_trace=trace,
      channels=W3Attestation(human=0.9, ai=0.85, external=0.8),
      target=GateTarget.RUNTIME  # or CONSTITUTIONAL or FEDERATION
  )
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional
import hashlib
import time


class GateTarget(Enum):
    RUNTIME = "runtime"                    # auto-install, non-constitutional
    CONSTITUTIONAL = "constitutional"      # requires F13 ceremony
    FEDERATION = "federation"              # requires F13 + all organs


class ScarSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class W3Attestation:
    """Tri-witness: ∛(Human × AI × External). Scar threshold = 0.85."""
    human: float
    ai: float
    external: float
    threshold: float = 0.85

    def compute(self) -> float:
        return (self.human * self.ai * self.external) ** (1/3)

    @property
    def passes(self) -> bool:
        return self.compute() >= self.threshold


@dataclass
class Scar:
    """A scar is a compressed constraint from experience."""
    scar_id: str
    expectation: str
    consequence: str
    compression: str      # one-line pattern
    constraint: str       # what must not happen again
    severity: ScarSeverity
    fingerprint: str      # SHA-256 of constraint for gate matching
    installed_at: float
    target: GateTarget
    active: bool

    @staticmethod
    def install(
        experience_trace: dict,
        channels: W3Attestation,
        target: GateTarget = GateTarget.RUNTIME,
    ) -> "Scar":
        """Step 5: Install scar as gate.

        Pipeline: observe → compress → attest → classify → INSTALL → witness → enforce

        This is the bridge from information to constraint.
        Without this step, experience accumulates but never changes behavior.
        """
        # Compress
        tool = experience_trace.get("tool", "unknown")
        success = experience_trace.get("success", True)
        feedback = experience_trace.get("feedback_self", "")

        if not success:
            expectation = f"{tool} should succeed"
            consequence = f"Failed: {feedback[:80]}"
            compression = f"{tool} fails when: {feedback[:80]}"
            constraint = f"Do not repeat: {feedback[:100]}"
            severity = ScarSeverity.MEDIUM
        else:
            expectation = f"{tool} should produce improvement"
            consequence = f"capability_change={experience_trace.get('capability_change', 0):+.2f}"
            compression = f"{tool} works when: {feedback[:80]}"
            constraint = f"Preserve conditions for {tool} success"
            severity = ScarSeverity.LOW

        # Attest
        w3 = channels.compute()

        # Classify
        if severity == ScarSeverity.CRITICAL:
            target = GateTarget.FEDERATION
        elif severity == ScarSeverity.HIGH:
            target = GateTarget.CONSTITUTIONAL

        # Install
        fingerprint = hashlib.sha256(constraint.encode()).hexdigest()[:16]

        return Scar(
            scar_id=f"scar_{experience_trace.get('trace_id', 'unknown')}",
            expectation=expectation,
            consequence=consequence,
            compression=compression,
            constraint=constraint,
            severity=severity,
            fingerprint=fingerprint,
            installed_at=time.time(),
            target=target,
            active=channels.passes,
        )

    def enforce(self, intent: str) -> dict:
        """Step 7: Check intent against scar fingerprint."""
        intent_fp = hashlib.sha256(intent.encode()).hexdigest()[:16]

        if self.active and self.fingerprint == intent_fp:
            return {
                "verdict": "BLOCKED",
                "scar_id": self.scar_id,
                "reason": self.constraint,
                "w3": self.compute(),
                "action": "888_HOLD" if self.target != GateTarget.RUNTIME else "auto_hold",
            }
        return {"verdict": "PASS", "scar_id": self.scar_id}

    def compute(self) -> float:
        """Re-compute W3 from stored attestation."""
        # Store attestation values in constraint field for persistence
        return 0.0  # placeholder — real impl stores W3 components


# ── Template Usage ────────────────────────────────────────────────────────────

USAGE = """
TEMPLATE USAGE:

1. After any experience trace with significant outcome:
   scar = Scar.install(
       experience_trace={"trace_id": "...", "tool": "...", ...},
       channels=W3Attestation(human=0.9, ai=0.85, external=0.8),
       target=GateTarget.RUNTIME
   )

2. Scar is now a gate. Wire into execution paths:
   if scar.active:
       result = scar.enforce(intent)
       if result["verdict"] == "BLOCKED":
           return HOLD  # scar blocks this action

3. For constitutional scars (touching F1-F13):
   target=GateTarget.CONSTITUTIONAL  # requires F13 ceremony

4. For federation-wide scars:
   target=GateTarget.FEDERATION  # requires F13 + all organs

PROVENANCE:
  Source: Universal Human Doctrines #10
  Ratified: 2026-09-08 F13
  Origin: Experience metabolism investigation (Stage 2 confirmed)
"""

if __name__ == "__main__":
    print(USAGE)
