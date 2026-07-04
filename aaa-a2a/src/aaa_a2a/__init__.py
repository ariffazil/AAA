"""aaa-a2a — Constitutional Python wrapper around the official a2a-sdk.

This package is the constitutional plane of the AAA control plane. It wraps the
official A2A SDK with F1-F13 floor enforcement, identity verification, verdict
routing, and VAULT999 audit. It does NOT implement transport — that is the job
of the official SDK and the existing Express server on port 3001.

Layer 3 of the federation:
    AAA (constitutional, Python)   ← this package
        └── middleware/  (floors, identity, verdicts, audit)
        └── registry/    (agent_cards, discovery)
        └── routing/     (organ_router, tool_router)

DITEMPA BUKAN DIBERI.
"""

from __future__ import annotations

__version__ = "0.1.0-phase2-stub"
__phase__ = "Phase 2 — ConstitutionalMiddleware stubs"
__sovereign__ = "Arif (F13, 888)"

__all__ = ["__version__", "__phase__", "__sovereign__"]