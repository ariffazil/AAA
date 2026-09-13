"""
admissibility_gate.py — Federated Memory Admissibility & Retrieval Gate Contract
================================================================================

CONTRACT SPECIFICATION & CANONICAL ADAPTER.
Canonical Implementation: arifosmcp.memory.admissibility (arifOS repo)
Authority: F13 SOVEREIGN (Muhammad Arif bin Fazil)
Ratified: 2026-09-13 (P0.75 Memory Authority Consolidation)

This module satisfies the AAA contract interface by delegating directly to
the single canonical engine in arifosmcp.memory.admissibility, eliminating
the dual-implementation fork.
"""

from __future__ import annotations

from arifosmcp.memory.admissibility import MemoryAdmissibilityGate

__all__ = ["MemoryAdmissibilityGate"]
