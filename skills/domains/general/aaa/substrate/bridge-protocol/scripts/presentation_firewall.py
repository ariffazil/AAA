#!/usr/bin/env python3
"""
presentation_firewall.py - STAGE 4 of bridge-protocol: the role boundary gate.

Complement to voice_gate.py. The voice governor makes a reply LEGIBLE.
The presentation firewall makes a reply BEHAVE — i.e. speak in the right
role, with the right depth, to the right audience.

Default mode: CONVERSE. Anything more is escalation.

USAGE
    python3 presentation_firewall.py --file /tmp/reply.txt
    python3 presentation_firewall.py --file /tmp/reply.txt --mode EXPLAIN
    python3 presentation_firewall.py --file /tmp/reply.txt --mode INSPECT
    cat reply.txt | python3 presentation_firewall.py

EXIT CODES
    0 = mechanical pass
    1 = re-draft (internal label, meta-narration, preface, over-apology)
    2 = mode violation (used INSPECT features in CONVERSE mode, etc.)
    3 = usage / input error

WHY THIS EXISTS
The transcript 2026-09-23 showed: brackets, role-labels, "aku patut",
"aku kena", "sebelum aku mula", over-apology chains — all leaking
from internal cognition into human-facing reply. Voice gate caught
register. Nothing caught role boundary.

HONEST SCOPE
This is a WITNESS. Counts what is countable. Catches the mechanical
patterns. Does not judge taste, does not judge whether the reply is
actually good. Green means: no mechanical leakage survived. It does
NOT mean the reply is right.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from typing import Iterable


# --------------------------------------------------------------------------
# Pattern banks. Each: (regex, label, fix-suggestion)
# --------------------------------------------------------------------------

# 1. Internal labels that should NEVER appear in human-facing reply
INTERNAL_LABEL: list[tuple[str, str, str | None]] = [
    (r"\[\s*BOND-CHECK\s*\]", "internal_label", "buang — bukan untuk manusia"),
    (r"\[\s*RASA\s*\]", "internal_label", "buang"),
    (r"\[\s*CAPABILITY-CHECK\s*\]", "internal_label", "buang"),
    (r"\[\s*LANGUAGE-GATE\s*\]", "internal_label", "buang"),
    (r"\[\s*SCAR-POLICY\s*\]", "internal_label", "buang"),
    (r"\[\s*SHADOW-CHECK\s*\]", "internal_label", "buang"),
    (r"\[\s*OBS\s*\]", "internal_label", "buang"),
    (r"\[\s*DER\s*\]", "internal_label", "buang"),
    (r"\[\s*INT\s*\]", "internal_label", "buang"),
    (r"\[\s*SPEC\s*\]", "internal_label", "buang"),
    (r"\[\s*ACT\s*\]", "internal_label", "buang"),
    (r"\[\s*WITNESS\s*\]", "internal_label", "buang"),
    (r"\[\[INTENT\]\]", "internal_label_double", "buang — bracket scaffold bocor"),
    (r"\[\[CAPABILITY\]\]", "internal_label_double", "buang"),
    (r"\[\[AUTHORITY\]\]", "internal_label_double", "buang"),
    (r"\[\[WITNESS\]\]", "internal_label_double", "buang"),
    (r"\[\[REALITY\]\]", "internal_label_double", "buang"),
    (r"\[\[GOVERNANCE\]\]", "internal_label_double", "buang"),
    (r"\[\[DELIBERATION\]\]", "internal_label_double", "buang"),
    (r"\[\[VERDICT\]\]", "internal_label_double", "buang"),
    (r"\[\[EXECUTION\]\]", "internal_label_double", "buang"),
    (r"\[\[RECEIPT\]\]", "internal_label_double", "buang"),
]

# 2. Meta-narration: narrator describing their own process
META_NARRATION: list[tuple[str, str, str | None]] = [
    (r"\baku patut\b", "meta_narration", "langsung buat, jangan cakap patut"),
    (r"\baku kena\b", "meta_narration", "buat atau tak buat — jangan narate"),
    (r"\baku tengah (jalan|buat|check|dog|probe|run)\b", "meta_narration",
     "kasih result, bukan progress"),
    (r"\bsebelum aku (mula|patch|jawab|explain|check)\b", "preface_delay",
     "mula dengan jawapan, bukan preface"),
    (r"\blet me (check|think|explain|dog|probe)\b", "meta_narration_en",
     "kasih result, bukan progress"),
    (r"\bi['']ll (check|look|investigate|dog)\b", "meta_narration_en",
     "kasih result, bukan progress"),
    (r"\bi['']m going to\b", "meta_narration_en", "kasih result"),
    (r"\baku nak (tanya|explain|patch|update)\b", "intent_narration",
     "buat, jangan narate niat"),
]

# 3. Over-apology chains (the "aku承认 lagi" pattern)
APOLOGY_WORDS: list[str] = [
    r"\baku承认\b", r"\bsorry\b", r"\bmaaf\b", r"\bminta maaf\b",
    r"\bi apologize\b", r"\bmy bad\b", r"\baku silap\b",
]


# --------------------------------------------------------------------------
# Data classes
# --------------------------------------------------------------------------

@dataclass
class Finding:
    kind: str
    pattern: str
    line: int = 0
    snippet: str = ""


@dataclass
class Report:
    mode: str
    findings: list[Finding] = field(default_factory=list)
    passed: bool = True

    def to_dict(self) -> dict:
        return {
            "mode": self.mode,
            "passed": self.passed,
            "findings": [
                {"kind": f.kind, "pattern": f.pattern,
                 "line": f.line, "snippet": f.snippet}
                for f in self.findings
            ],
        }


# --------------------------------------------------------------------------
# Core checks
# --------------------------------------------------------------------------

def check_internal_labels(text: str) -> list[Finding]:
    out: list[Finding] = []
    for i, line in enumerate(text.splitlines(), 1):
        for rx, label, _ in INTERNAL_LABEL:
            if re.search(rx, line, re.IGNORECASE):
                out.append(Finding(
                    kind=label, pattern=rx,
                    line=i, snippet=line.strip()[:80]))
    return out


def check_meta_narration(text: str) -> list[Finding]:
    out: list[Finding] = []
    for i, line in enumerate(text.splitlines(), 1):
        for rx, label, _ in META_NARRATION:
            if re.search(rx, line, re.IGNORECASE):
                out.append(Finding(
                    kind=label, pattern=rx,
                    line=i, snippet=line.strip()[:80]))
    return out


def check_apology_budget(text: str) -> list[Finding]:
    """Catch the over-apology chain. One apology OK. More than one = leak."""
    out: list[Finding] = []
    combined = "|".join(APOLOGY_WORDS)
    matches = list(re.finditer(combined, text, re.IGNORECASE))
    if len(matches) > 1:
        # find first line where the 2nd apology appears
        snippets = [text[max(0, m.start()-20):m.end()+20] for m in matches]
        out.append(Finding(
            kind="over_apology",
            pattern=combined,
            line=0,
            snippet=f"{len(matches)} apology phrases: {snippets[1][:60]}..."))
    return out


def check_question_budget(text: str, mode: str) -> list[Finding]:
    """One question per turn is the rule. List-mode exception only if human invited."""
    # Strip code fences to avoid false positives from YAML/examples
    stripped = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    stripped = re.sub(r"`[^`]+`", "", stripped)
    # Count question marks
    q_count = stripped.count("?")
    # In CONVERSE: max 1 question (the "one grounded question if needed")
    if mode == "CONVERSE" and q_count > 1:
        return [Finding(
            kind="question_budget",
            pattern=r"\?",
            line=0,
            snippet=f"{q_count} questions in CONVERSE mode; expected 1")]
    # In EXPLAIN: 0-1 questions OK
    if mode == "EXPLAIN" and q_count > 2:
        return [Finding(
            kind="question_budget",
            pattern=r"\?",
            line=0,
            snippet=f"{q_count} questions in EXPLAIN mode; expected ≤2")]
    return []


def check_inspect_leak_in_converse(text: str, mode: str) -> list[Finding]:
    """If CONVERSE mode but reply contains full YAML/capability/authority graph blocks,
    that's INSPECT content leaking."""
    if mode != "CONVERSE":
        return []
    out: list[Finding] = []
    # Heuristic: large YAML/code block in CONVERSE reply = leak
    yaml_block = re.search(r"```ya?ml", text, re.IGNORECASE)
    code_block = re.search(r"```", text)
    if yaml_block:
        out.append(Finding(
            kind="inspect_leak_yaml",
            pattern=r"```ya?ml",
            line=0,
            snippet="YAML block in CONVERSE mode — INSPECT features leak"))
    # Many `:` followed by indented content = YAML-ish
    yaml_like_lines = sum(
        1 for line in text.splitlines()
        if re.match(r"^\s+\w+:", line)
    )
    if yaml_like_lines > 8:
        out.append(Finding(
            kind="inspect_leak_yaml_inline",
            pattern=r"^\s+\w+:",
            line=0,
            snippet=f"{yaml_like_lines} YAML-style lines in CONVERSE reply"))
    return out


# --------------------------------------------------------------------------
# Main gate
# --------------------------------------------------------------------------

def run_gate(text: str, mode: str) -> Report:
    """mode: CONVERSE | EXPLAIN | INSPECT

    INSPECT mode = full disclosure to F13 sovereign.
    Internal labels (brackets), meta-narration, YAML blocks — all allowed.
    Only checks: that the reply claims the right role context.

    CONVERSE / EXPLAIN = default. Internal labels forbidden.
    """
    report = Report(mode=mode)

    if mode == "INSPECT":
        # In INSPECT, the only mechanical check is that the reply looks
        # like an audit / pathway dump (YAML/code blocks present) rather
        # than a stray conversation reply that happens to mention a bracket.
        # No leakage check — full disclosure is the point.
        return report

    # CONVERSE / EXPLAIN: all mechanical checks apply
    report.findings.extend(check_internal_labels(text))
    report.findings.extend(check_meta_narration(text))
    report.findings.extend(check_apology_budget(text))
    report.findings.extend(check_inspect_leak_in_converse(text, mode))
    report.findings.extend(check_question_budget(text, mode))

    if report.findings:
        report.passed = False

    return report


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="presentation_firewall — STAGE 4 of bridge-protocol",
    )
    p.add_argument("--file", help="path to reply text")
    p.add_argument("--mode", default="CONVERSE",
                   choices=["CONVERSE", "EXPLAIN", "INSPECT"])
    p.add_argument("--json", action="store_true",
                   help="emit JSON report")
    args = p.parse_args(argv)

    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                text = f.read()
        except OSError as e:
            print(f"error: cannot read {args.file}: {e}", file=sys.stderr)
            return 3
    else:
        text = sys.stdin.read()

    if not text.strip():
        print("error: empty input", file=sys.stderr)
        return 3

    report = run_gate(text, args.mode)

    if args.json:
        import json as _json
        print(_json.dumps(report.to_dict(), indent=2))
    else:
        if report.passed:
            print(f"PASS ({report.mode}): no mechanical leakage found")
            return 0
        else:
            print(f"FAIL ({report.mode}): {len(report.findings)} finding(s)")
            for f in report.findings:
                where = f"line {f.line}" if f.line else "text"
                print(f"  [{f.kind}] {where}: {f.snippet}")
            print()
            print("re-draft before sending")
            return 1

    return 0 if report.passed else 1


if __name__ == "__main__":
    sys.exit(main())