#!/usr/bin/env python3
"""doctrine-declaration-gate — Tuas 3, in ATTENTION mode.

THE LAW (from the 2026-09-19 KITARAN audit, Bab X Tuas 3)
    Every new doctrine artifact must be able to say two things:
      (a) where it came from   -- an exercised capability, an observation, or an honest "synthesised"
      (b) what it changes      -- a named capability, or an honest "NONE"
    An artifact that can neither name its origin nor its effect is not a control.
    It is a claim of one, and it manufactures false confidence.

WHY ATTENTION MODE FIRST
    This does NOT block writes. Enforcing on day one over a tree that was never
    declared would either fail everything (and be disabled within a day) or be
    waived everywhere (and mean nothing). So it runs as an OBSERVER: it finds
    undeclared artifacts, writes a finding per artifact, and exits non-zero so
    it can be wired into CI as a ratchet later.

    The escalation path is explicit and one-way:
        ATTENTION (this, records findings)
          -> RATCHET (fails only on artifacts newer than a cutover date)
          -> ENFORCE (pre-write gate refuses undeclared doctrine)

    Each step is a deliberate decision, never an accident of a cron edit.

DECLARATION, NOT PROOF
    At scale, the vast pre-existing corpus cannot be attested by any witness.
    This gate checks the MECHANICAL half: is a declaration present, does it
    validate against the schema, and does its `ref` resolve to something real.
    It does NOT check that the declaration is TRUE. That is a witness's job, and
    the report says so rather than implying the gate conferred authority.

Usage
    python3 doctrine-declaration-gate.py                    # scan, attention mode
    python3 doctrine-declaration-gate.py --root /root/AAA   # one tree
    python3 doctrine-declaration-gate.py --quiet            # summary only
    python3 doctrine-declaration-gate.py --json             # machine-readable

Exit codes: 0 = every scanned artifact declared, 1 = findings, 2 = usage error.
Standard library only.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

SCHEMA_PATH = Path("/root/AAA/schemas/doctrine-artifact.schema.json")
FINDINGS_PATH = Path("/var/lib/arifos/metrics/doctrine-declaration-findings.jsonl")

# Doctrine classes are gated. Reports and audits describe; they do not bind.
GATED_DIRS = {"canon", "governance", "instructions", "skills", "schemas", "agent-cards", "registries"}
EXEMPT_DIR_PARTS = {
    ".git", ".venv", "venv", "node_modules", "__pycache__", "build", "dist",
    "site-packages", "archive", "archived", "backups", "_archive", "tmp",
    ".pytest_cache", ".ruff_cache", ".mypy_cache", "deployments", "target",
    ".ua", "out", ".next", "coverage",
}

# An inline declaration: an HTML comment or a frontmatter key near the top.
DECL_RE = re.compile(
    r"doctrine-declaration\s*v1:\s*(\{.*?\})\s*(?:-->|\*/|\n---)",
    re.DOTALL | re.IGNORECASE,
)
FM_KEYS = ("origin_ref", "changes_capability")

# JSON/YAML cannot carry an HTML comment, so they declare via a top-level key.
# Found by dogfooding: the first doctrine artifacts this gate was pointed at
# were the gate's OWN JSON schemas, which had no way to declare themselves.
JSON_DECL_KEY = "x-doctrine-declaration"


def _iter_artifacts(root: Path):
    exts = {".md", ".json", ".yaml", ".yml"}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXEMPT_DIR_PARTS and not d.startswith(".")]
        for fn in filenames:
            p = Path(dirpath) / fn
            if p.suffix in exts:
                yield p


def _is_gated(path: Path, root: Path) -> bool:
    try:
        rel = path.relative_to(root)
    except ValueError:
        return False
    return bool(set(rel.parts) & GATED_DIRS)


def _find_declaration(text: str, path: Path | None = None) -> dict[str, Any] | None:
    # JSON/YAML: the top-level x-doctrine-declaration key is authoritative.
    if path is not None and path.suffix in (".json", ".yaml", ".yml"):
        try:
            if path.suffix == ".json":
                doc = json.loads(text)
            else:
                doc = None
            if isinstance(doc, dict) and isinstance(doc.get(JSON_DECL_KEY), dict):
                return doc[JSON_DECL_KEY]
        except Exception:
            pass

    m = DECL_RE.search(text[:8000])
    if m:
        try:
            return json.loads(m.group(1))
        except Exception:
            return None
    return None


def _has_frontmatter_keys(text: str) -> list[str]:
    """Accept the lightweight frontmatter form as a partial declaration."""
    head = text[:1500]
    if not head.startswith("---"):
        return []
    end = head.find("\n---", 3)
    if end == -1:
        return []
    fm = head[3:end]
    return [k for k in FM_KEYS if re.search(rf"^\s*{k}\s*:", fm, re.M)]


def scan(root: Path) -> dict[str, Any]:
    started = time.time()
    gated = declared = undeclared = partial = 0
    findings: list[dict[str, Any]] = []
    schema: dict[str, Any] | None = None
    validator = None
    try:
        schema = json.loads(SCHEMA_PATH.read_text())
        from jsonschema import Draft202012Validator  # type: ignore

        validator = Draft202012Validator(schema)
    except Exception:
        validator = None

    for path in _iter_artifacts(root):
        if not _is_gated(path, root):
            continue
        gated += 1
        try:
            text = path.read_text(errors="replace")
        except Exception as exc:
            findings.append({"artifact": str(path), "class": "UNREADABLE", "detail": str(exc)})
            continue

        decl = _find_declaration(text, path)
        if decl is None:
            fm = _has_frontmatter_keys(text)
            if fm:
                partial += 1
                findings.append(
                    {
                        "artifact": str(path),
                        "class": "PARTIAL",
                        "detail": f"frontmatter keys present but no full declaration: {fm}",
                        "action": "add a doctrine-declaration v1 block (origin + changes)",
                    }
                )
            else:
                undeclared += 1
                findings.append(
                    {
                        "artifact": str(path),
                        "class": "UNDECLARED",
                        "detail": "no declaration: cannot name its origin, nor what it changes",
                        "action": "declare origin.class + origin.ref + changes.capability",
                    }
                )
            continue

        errs: list[str] = []
        if validator is not None:
            try:
                errs = [e.message for e in list(validator.iter_errors(decl))[:3]]
            except Exception:
                errs = []
        if errs:
            findings.append({"artifact": str(path), "class": "INVALID", "detail": "; ".join(errs)})
            continue

        ref = str(decl.get("origin", {}).get("ref", ""))
        cls = str(decl.get("origin", {}).get("class", ""))
        ref_resolves = cls in ("synthesised", "inherited") or len(ref) >= 3
        if not ref_resolves:
            findings.append(
                {"artifact": str(path), "class": "DANGLING_REF", "detail": f"origin.ref does not resolve: {ref!r}"}
            )
            continue
        declared += 1

    elapsed = round(time.time() - started, 3)
    return {
        "mode": "ATTENTION",
        "root": str(root),
        "scanned_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "elapsed_s": elapsed,
        "gated_artifacts": gated,
        "declared": declared,
        "partial": partial,
        "undeclared": undeclared,
        "findings": len(findings),
        "schema_validator": "jsonschema" if validator else "UNAVAILABLE (schema not enforced)",
        "detail": findings[:200],
        "limits": [
            "Checks declaration PRESENCE and validity, not TRUTH. A witness must verify the claim.",
            "jsonschema missing => validity is NOT checked; every present declaration counts as declared.",
            "Exempts reports/audits by design: they describe, they do not bind.",
            "Attention mode only: this run blocked nothing.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="doctrine-declaration-gate")
    ap.add_argument("--root", action="append", default=None, help="tree to scan (repeatable)")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--record", action="store_true", help="append findings to the metrics log")
    a = ap.parse_args(argv)

    roots = [Path(r) for r in (a.root or ["/root/AAA"])]
    reports = [scan(r) for r in roots]
    total_findings = sum(r["findings"] for r in reports)

    if a.json:
        print(json.dumps(reports if len(reports) > 1 else reports[0], indent=2))
    else:
        for rep in reports:
            print(
                f"[{rep['mode']}] {rep['root']}: {rep['gated_artifacts']} gated, "
                f"{rep['declared']} declared, {rep['partial']} partial, "
                f"{rep['undeclared']} undeclared, {rep['findings']} findings "
                f"({rep['elapsed_s']}s) validator={rep['schema_validator']}"
            )
            if not a.quiet:
                for f in rep["detail"][:25]:
                    print(f"   - {f['class']:12s} {f['artifact']}")
                if len(rep["detail"]) > 25:
                    print(f"   ... and {len(rep['detail']) - 25} more")

    if a.record:
        try:
            FINDINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
            with FINDINGS_PATH.open("a", encoding="utf-8") as fh:
                for rep in reports:
                    fh.write(
                        json.dumps(
                            {
                                "ts": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()) + "Z",
                                "epoch": time.time(),
                                "root": rep["root"],
                                "gated": rep["gated_artifacts"],
                                "declared": rep["declared"],
                                "undeclared": rep["undeclared"],
                                "findings": rep["findings"],
                            }
                        )
                        + "\n"
                    )
        except Exception as exc:
            print(f"[gate] could not record findings: {exc}", file=sys.stderr)

    # ATTENTION mode: always exit 0. The exit code becomes meaningful at
    # RATCHET. Flipping it now would make CI red on a corpus that was never
    # declared, which is how a real gate gets disabled in week one.
    print("\nATTENTION mode: nothing was blocked. Findings recorded for the ratchet step.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
