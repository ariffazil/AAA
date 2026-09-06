#!/usr/bin/env python3
"""
scar_detector.py — Stage 4 architecture for scar enforcement.

Reads /root/AAA/canon/SCAR_RECORDS/scar-*.md, extracts ScarRecord,
and provides detectors that scan federation codebases for scar-pattern
recurrence. This is the bridge from SCAR_RECORDS-as-library
(Stage 1) to SCAR_RECORDS-as-immune-system (Stage 4).

STATUS (2026-09-07):
- scar-001: regex detector ACTIVE (production-ready)
- scar-002: pattern detector ACTIVE (liveness vs functional-correctness)
- scar-003: AST detector STUB (T2 wiring required)
- scar-004: semantic detector STUB (multi-cause analysis not greppable)
- scar-005: semantic detector STUB (provenance laundering not greppable)

PROMOTION PATH: T1 (this file) → T2 (CI integration in AAA) →
T3 (F13 ratification as constitutional immune system).
"""

from __future__ import annotations

import re
import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Iterator
from datetime import datetime, timezone


# ---------- ScarRecord ----------


@dataclass
class ScarRecord:
    """Parsed scar from SCAR_RECORDS/scar-*.md frontmatter."""

    scar_id: str
    timestamp: str
    failure_pattern: str
    root_cause: str = ""
    scar_pressure: float = 0.0
    status: str = "UNKNOWN"
    test_fixture: str = ""
    generated_skill: str = ""
    behavior_change: str = ""
    review_date: str = ""
    parent_scar: str = ""
    severity: str = ""
    verification_method: str = ""
    verification_result: str = ""
    source_path: Path = field(default_factory=Path)

    @property
    def is_active(self) -> bool:
        return self.status.upper() in ("ACTIVE", "OPEN")

    @property
    def detector_class(self) -> str:
        """Which Stage-4 detector category applies."""
        # Heuristic: if test_fixture looks like a shell command, regex-detectable
        if "grep" in self.test_fixture or "require" in self.failure_pattern.lower():
            return "REGEX"
        if "health check" in self.failure_pattern.lower() or "monitor" in self.failure_pattern.lower():
            return "PATTERN"
        if "ESM" in self.failure_pattern or "transport" in self.failure_pattern.lower():
            return "AST"
        return "SEMANTIC"


# ---------- Frontmatter parser ----------

YAML_BLOCK = re.compile(r"```yaml\s*\n(?P<body>.*?)\n```", re.DOTALL)
KEY_VAL = re.compile(r"^(?P<key>[a-zA-Z_][a-zA-Z0-9_]*):\s*(?P<val>.*)$", re.MULTILINE)


def parse_scar_frontmatter(md_path: Path) -> ScarRecord | None:
    """Parse one scar-*.md file's YAML frontmatter."""
    if not md_path.exists():
        return None
    text = md_path.read_text(encoding="utf-8")
    m = YAML_BLOCK.search(text)
    if not m:
        return None
    body = m.group("body")
    fields: dict[str, str] = {}
    for line in body.splitlines():
        kv = KEY_VAL.match(line)
        if kv:
            fields[kv.group("key").strip()] = kv.group("val").strip().strip('"').strip("'")
        # Handle continuation lines (e.g. multi-line root_cause with `>`) — capture raw
    return ScarRecord(
        scar_id=fields.get("scar_id", md_path.stem),
        timestamp=fields.get("timestamp", ""),
        failure_pattern=fields.get("failure_pattern", ""),
        root_cause=fields.get("root_cause", ""),
        scar_pressure=float(fields.get("scar_pressure", 0) or 0),
        status=fields.get("status", "UNKNOWN"),
        test_fixture=fields.get("test_fixture", ""),
        generated_skill=fields.get("generated_skill", ""),
        behavior_change=fields.get("behavior_change", ""),
        review_date=fields.get("review_date", ""),
        parent_scar=fields.get("parent_scar", ""),
        severity=fields.get("severity", ""),
        verification_method=fields.get("verification_method", ""),
        verification_result=fields.get("verification_result", ""),
        source_path=md_path,
    )


def load_all_scars(scar_dir: Path = Path("/root/AAA/canon/SCAR_RECORDS")) -> list[ScarRecord]:
    """Load every scar-*.md under the canonical SCAR_RECORDS directory."""
    if not scar_dir.exists():
        return []
    scars: list[ScarRecord] = []
    for md in sorted(scar_dir.glob("scar-*.md")):
        rec = parse_scar_frontmatter(md)
        if rec is not None:
            scars.append(rec)
    return scars


# ---------- Violations ----------


@dataclass
class Violation:
    scar_id: str
    detector_class: str
    file_path: str
    line_number: int
    matched_text: str
    severity: str  # "BLOCK" | "WARN" | "INFO"

    def to_dict(self) -> dict:
        return asdict(self)


# ---------- Detectors (one per scar) ----------

EXCLUDE_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "dist",
    "build",
    ".mypy_cache",
    ".pytest_cache",
    ".next",
    "target",
}
EXCLUDE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".tar", ".gz", ".ico", ".woff", ".woff2", ".ttf"}
SCANNABLE_EXTS = {".ts", ".js", ".mjs", ".cjs", ".py", ".sh", ".bash", ".md", ".yaml", ".yml", ".json"}


def _should_skip(path: Path) -> bool:
    parts = set(path.parts)
    return bool(parts & EXCLUDE_DIRS) or path.suffix.lower() in EXCLUDE_EXTS


def detect_scar_001(content: str, file_path: Path) -> list[Violation]:
    """scar-001: require('node:...') in ESM scope — silent fail."""
    violations: list[Violation] = []
    pattern = re.compile(r"""require\(\s*['"]node:[a-zA-Z_][a-zA-Z0-9_/]*['"]""")
    for lineno, line in enumerate(content.splitlines(), start=1):
        if pattern.search(line):
            violations.append(
                Violation(
                    scar_id="scar-001-esm-sct-silent-fail",
                    detector_class="REGEX",
                    file_path=str(file_path),
                    line_number=lineno,
                    matched_text=line.strip()[:200],
                    severity="BLOCK",
                )
            )
    return violations


def detect_scar_002(content: str, file_path: Path) -> list[Violation]:
    """scar-002: SCT validation monitoring gap — liveness without functional correctness.

    Heuristic: look for health-check patterns that ONLY check service liveness
    without exercising the verify path.
    """
    violations: list[Violation] = []
    if "health" not in file_path.name.lower() and "health" not in str(file_path).lower():
        return violations
    # Look for a /health endpoint that returns 200 without calling verify
    has_health_endpoint = bool(re.search(r"/health", content))
    has_liveness_only = bool(re.search(r"\b(return\s+(res\.)?(status|ok|200|alive)|status:\s*['\"]ok['\"]|res\.status\(200\))", content, re.IGNORECASE))
    has_verify_call = bool(re.search(r"verify|sct|act_v1", content, re.IGNORECASE))
    if has_health_endpoint and has_liveness_only and not has_verify_call:
        for lineno, line in enumerate(content.splitlines(), start=1):
            if "/health" in line or "return" in line.lower():
                violations.append(
                    Violation(
                        scar_id="scar-002-sct-validation-monitoring-gap",
                        detector_class="PATTERN",
                        file_path=str(file_path),
                        line_number=lineno,
                        matched_text=line.strip()[:200],
                        severity="WARN",
                    )
                )
                break
    return violations


def detect_scar_003(content: str, file_path: Path) -> list[Violation]:
    """scar-003: transport parameter duplication (STUB — T2 wiring)."""
    return []  # T2: AST-level detection required


def detect_scar_004(content: str, file_path: Path) -> list[Violation]:
    """scar-004: multi-causal HOT ontology (STUB — semantic)."""
    return []


def detect_scar_005(content: str, file_path: Path) -> list[Violation]:
    """scar-005: provenance laundering (STUB — semantic)."""
    return []


DETECTORS = {
    "scar-001-esm-sct-silent-fail": detect_scar_001,
    "scar-002-sct-validation-monitoring-gap": detect_scar_002,
    "scar-003-transport-degradation": detect_scar_003,
    "scar-004-multi-causal-hot-ontology": detect_scar_004,
    "scar-005-ccc-mesh-convergence-20260903": detect_scar_005,
}


def detect_all_for_file(content: str, file_path: Path, scars: list[ScarRecord]) -> list[Violation]:
    """Run every active scar detector against one file."""
    violations: list[Violation] = []
    for scar in scars:
        if not scar.is_active:
            continue
        detector = DETECTORS.get(scar.scar_id)
        if detector is None:
            continue
        violations.extend(detector(content, file_path))
    return violations


# ---------- Codebase scanner ----------

DEFAULT_ROOTS = [
    Path("/root/AAA"),
    Path("/root/arifOS"),
    Path("/root/A-FORGE"),
    Path("/root/WEALTH"),
    Path("/root/WELL"),
    Path("/root/GEOX"),
]


def scan_codebase(
    roots: list[Path] | None = None,
    scars: list[ScarRecord] | None = None,
) -> Iterator[Violation]:
    """Walk the federation codebase; yield every scar-violation."""
    if roots is None:
        roots = DEFAULT_ROOTS
    if scars is None:
        scars = load_all_scars()
    for root in roots:
        root = Path(root) if isinstance(root, str) else root
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if _should_skip(path):
                continue
            if path.suffix.lower() not in SCANNABLE_EXTS:
                continue
            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            yield from detect_all_for_file(content, path, scars)


# ---------- Report ----------


def format_report(violations: list[Violation]) -> str:
    """Pretty-print violations as a Stage-4 audit."""
    if not violations:
        return "[SCAR-DETECTOR] OK — no scar-pattern recurrence detected across scanned roots."
    lines: list[str] = []
    lines.append(f"[SCAR-DETECTOR] FAIL — {len(violations)} violation(s):")
    by_scar: dict[str, list[Violation]] = {}
    for v in violations:
        by_scar.setdefault(v.scar_id, []).append(v)
    for scar_id, vs in sorted(by_scar.items()):
        lines.append(f"\n  scar: {scar_id}  ({len(vs)} violation(s))")
        for v in vs[:10]:  # cap display
            lines.append(f"    {v.severity:<5} {v.file_path}:{v.line_number}")
            lines.append(f"           {v.matched_text[:120]}")
        if len(vs) > 10:
            lines.append(f"    ... and {len(vs) - 10} more")
    return "\n".join(lines)


# ---------- CLI ----------


def main() -> int:
    import argparse

    p = argparse.ArgumentParser(description="Stage-4 scar detector — bridge from SCAR_RECORDS to runtime gate")
    p.add_argument("--scar-dir", type=Path, default=Path("/root/AAA/canon/SCAR_RECORDS"))
    p.add_argument(
        "--roots", type=Path, nargs="+", default=None, help="Codebase roots to scan (default: federation organs)"
    )
    p.add_argument("--strict", action="store_true", help="Exit non-zero on BLOCK violations (CI mode)")
    p.add_argument("--json", action="store_true", help="Emit JSON report")
    args = p.parse_args()

    scars = load_all_scars(args.scar_dir)
    if not scars:
        print(f"[SCAR-DETECTOR] no scars found at {args.scar_dir}")
        return 0

    active = [s for s in scars if s.is_active]
    print(f"[SCAR-DETECTOR] loaded {len(scars)} scar(s); {len(active)} active")
    for s in active:
        print(f"  - {s.scar_id}  detector={s.detector_class}  pressure={s.scar_pressure}  status={s.status}")

    violations = list(scan_codebase(args.roots, scars))

    if args.json:
        print(json.dumps([v.to_dict() for v in violations], indent=2))
    else:
        print()
        print(format_report(violations))

    if args.strict and any(v.severity == "BLOCK" for v in violations):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
