"""
F1–F13 Floor Benchmark Suite.

Self-contained pytest test suite that tests the arifOS kernel (localhost:8088)
against the constitutional floor coverage matrix.

Each floor file implements 3–5 test cases that call live MCP tools and
verify verdicts against expected outcomes.

Usage:
    pytest benchmarks/floors/ -v
    python -m benchmarks.floors.run_all

DITEMPA BUKAN DIBERI — Forged, not given.
"""

__version__ = "v2026.06.14"
__author__ = "FORGE-000Ω"
__license__ = "F13 SOVEREIGN — Arif Fazil"
