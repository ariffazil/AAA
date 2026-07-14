#!/usr/bin/env python3
"""
import_linter.py — Federation enum drift detector (P2.2 closure 2026-07-14)

Scans all federation organs (arifOS, A-FORGE, GEOX, WEALTH, WELL, AAA)
for local definitions of canonical enum classes that MUST be imported
from the federation source-of-truth.

Canonical source: /root/arifOS/arifosmcp/schemas/federation_enums.py

Banned local definitions (re-declarations that cause drift):
  - class EvidenceQuality(...)
  - class ConfidenceLevel(...)
  - class EpistemicTag(...)
  - class OutputClass(...)
  - class Verdict(...)

When found, the linter exits 1 with a per-file report. CI gate that
calls this script on every push prevents new drift from being merged.

Usage:
  python import_linter.py                    # scan defaults
  python import_linter.py --paths a b c     # scan explicit roots
  python import_linter.py --strict          # exit 1 on warnings too

DITEMPA BUKAN DIBERI — One schema to govern them all.
"""

from __future__ import annotations

import argparse
import ast
import sys
from dataclasses import dataclass, field
from pathlib import Path


CANONICAL_PATH = Path("/root/arifOS/arifosmcp/schemas/federation_enums.py")
BANNED_CLASSES = {"EvidenceQuality", "ConfidenceLevel", "EpistemicTag", "OutputClass", "Verdict"}
DEFAULT_SCAN_ROOTS = [
    Path("/root/arifOS"),
    Path("/root/A-FORGE"),
    Path("/root/GEOX"),
    Path("/root/WEALTH"),
    Path("/root/WELL"),
    Path("/root/AAA"),
]


@dataclass
class DriftFinding:
    file: Path
    line: int
    class_name: str
    severity: str  # 'ERROR' or 'WARN'
    context: str = ""

    def render(self) -> str:
        return f"{self.severity}  {self.file}:{self.line}  class {self.class_name}  ({self.context})"


@dataclass
class LintReport:
    scanned_files: int = 0
    findings: list[DriftFinding] = field(default_factory=list)
    errors: int = 0
    warnings: int = 0

    def add(self, f: DriftFinding) -> None:
        self.findings.append(f)
        if f.severity == "ERROR":
            self.errors += 1
        else:
            self.warnings += 1

    def render(self) -> str:
        lines = [
            f"FEDERATION ENUM LINTER REPORT",
            f"  Canonical source: {CANONICAL_PATH}",
            f"  Scanned files:    {self.scanned_files}",
            f"  Errors:           {self.errors}",
            f"  Warnings:         {self.warnings}",
            "",
        ]
        if self.findings:
            lines.append("FINDINGS:")
            for f in self.findings:
                lines.append("  " + f.render())
        else:
            lines.append("OK — no drift detected. Federation enums are unified.")
        return "\n".join(lines)


def _is_canonical_file(p: Path) -> bool:
    """Skip the canonical source itself + vendored libs."""
    s = str(p)
    if s == str(CANONICAL_PATH):
        return True
    if "/.venv/" in s or "/site-packages/" in s or "/__pycache__/" in s:
        return True
    if "/.claude/worktrees/" in s:
        return True
    if "/build/lib/" in s:
        return True
    if s.endswith(".bak") or s.endswith(".bak.2026-07-14"):
        return True
    return False


def _scan_file(p: Path) -> list[DriftFinding]:
    findings: list[DriftFinding] = []
    try:
        source = p.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source, filename=str(p))
    except (SyntaxError, ValueError, FileNotFoundError, PermissionError, IsADirectoryError, OSError):
        return findings

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name in BANNED_CLASSES:
            # Get the base class context to differentiate
            bases = []
            for b in node.bases:
                try:
                    bases.append(ast.unparse(b))
                except Exception:
                    pass
            context = "extends " + ", ".join(bases) if bases else "no bases"

            # Heuristic: is this a re-definition (extends Enum/StrEnum/IntEnum) or
            # a Pydantic model with the same name? Enum re-defs = ERROR.
            is_enum = any("Enum" in b for b in bases)
            severity = "ERROR" if is_enum else "WARN"
            findings.append(
                DriftFinding(
                    file=p,
                    line=node.lineno,
                    class_name=node.name,
                    severity=severity,
                    context=context,
                )
            )
    return findings


def lint(roots: list[Path], strict: bool = False) -> LintReport:
    report = LintReport()
    for root in roots:
        if not root.exists():
            continue
        for py in root.rglob("*.py"):
            if _is_canonical_file(py):
                continue
            report.scanned_files += 1
            for f in _scan_file(py):
                report.add(f)
    if strict and report.warnings > 0:
        # Promote warnings to errors for strict mode
        report.errors += report.warnings
        report.warnings = 0
    return report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Federation enum drift detector (P2.2 closure).",
    )
    parser.add_argument(
        "--paths",
        nargs="*",
        type=Path,
        default=DEFAULT_SCAN_ROOTS,
        help="Paths to scan (default: federation organ roots)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors",
    )
    args = parser.parse_args()

    report = lint(args.paths, strict=args.strict)
    print(report.render())
    return 1 if report.errors > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
