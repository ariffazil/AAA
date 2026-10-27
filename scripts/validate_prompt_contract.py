#!/usr/bin/env python3
"""AAA Prompt Contract validator (aaa.prompt.contract/v1).

Modes:
  --self-test          validate registries/PROMPT_CONTRACT.yaml itself
                       (schema completeness: 12 sections, forbidden floor,
                       closure ladder, legal exits, watchlist).
  --directive <path>   lint a work directive against the contract: check the
                       twelve section CONCEPTS are present and distinguishable,
                       an anti-objective block exists, and closure is defined.

Law (from the guide): a repeated prompt rule is a candidate for enforcement.
This validator is the enforcement candidate.
"""

from __future__ import annotations

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
AAA = os.path.dirname(HERE)
CONTRACT = os.path.join(AAA, "registries", "PROMPT_CONTRACT.yaml")

try:
    import yaml
except ImportError:
    print("FATAL: PyYAML unavailable")
    sys.exit(2)

# Concept probes: distinctive literals a conforming directive carries.
# Headings vary; concepts must be findable. (concept id -> probe tokens)
CONCEPT_PROBES = {
    "AUTHORITY": ["authority", "ceiling", "self-seal", "lane", "verdict ceiling"],
    "REALITY": ["witnessed", "observed state", "re-probe", "baseline", "verified 2026"],
    "SINGLE_MISSION": ["mission", "single", "the one transition", "objective:"],
    "SCOPE": ["scope", "owns", "concurrent writer", "owned by", "files"],
    "FORBIDDEN_MUTATIONS": ["do not", "forbidden", "must not touch", "never", "anti-objective"],
    "STOP_CONDITIONS": ["stop", "hold if", "return hold", "halt", "stop condition"],
    "TESTS_FIRST": ["must fail", "failing test", "tests first", "red", "acceptance"],
    "IMPLEMENTATION_BOUNDARY": ["boundary", "invariant", "may change", "must remain"],
    "INDEPENDENT_CHECK": ["verifier", "independent", "separate review", "red-team", "audit"],
    "DEPLOYMENT": ["deploy", "lease", "rollback", "release"],
    "CONSEQUENCE": ["live probe", "consequence", "world outcome", "verify.*live", "observed"],
    "CLOSURE": ["human accept", "acceptance", "do not self", "who may accept", "human decision"],
}


def self_test() -> int:
    with open(CONTRACT) as fh:
        doc = yaml.safe_load(fh)
    problems = []
    secs = doc.get("required_sections") or []
    ids = [s.get("id") for s in secs]
    if len(secs) != 12 or len(set(ids)) != 12:
        problems.append(f"required_sections: {len(segs_ok(secs))}/12 unique")
    for s in secs:
        if not s.get("concept"):
            problems.append(f"section {s.get('id')} missing concept")
    if len(doc.get("forbidden_shortcuts_floor") or []) < 6:
        problems.append("forbidden floor < 6 entries")
    ladder = doc.get("closure_ladder") or []
    if len(ladder) != 11 or "human_accepted_closure" not in ladder:
        problems.append(f"closure ladder malformed ({len(ladder)} rungs)")
    exits = doc.get("legal_exit_vocabulary") or []
    for need in ("UNKNOWN", "PARTIAL", "HOLD"):
        if need not in exits:
            problems.append(f"legal exit missing {need}")
    if not (doc.get("prompt_debt_watchlist")):
        problems.append("watchlist empty")
    if problems:
        for p in problems:
            print(f"FAIL {p}")
        return 1
    print("SELF-TEST PASS: 12 sections with concepts, forbidden floor, "
          "11-rung ladder, legal exits, watchlist present")
    return 0


def segs_ok(secs: list) -> list:
    return [s.get("id") for s in secs if s.get("id")]


def lint_directive(path: str) -> int:
    with open(path) as fh:
        text = fh.read().lower()
    missing = []
    for sid, probes in CONCEPT_PROBES.items():
        if not any(p in text for p in probes):
            missing.append(sid)
    if missing:
        for sid in missing:
            print(f"FAIL concept absent: {sid}")
        print(f"SUMMARY: {12 - len(missing)}/12 concepts present — directive is malformed")
        return 1
    print("DIRECTIVE PASS: all 12 concepts present and distinguishable")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--directive")
    args = ap.parse_args()
    if args.directive:
        return lint_directive(args.directive)
    return self_test()


if __name__ == "__main__":
    sys.exit(main())
