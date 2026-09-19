#!/usr/bin/env python3
"""claim_kernel — the explanatory-class axis for federation claims.

WHY THIS EXISTS
---------------
The federation already tracks ONE axis of a claim: *how it was obtained*.
`AAA/claim_ledger` enforces claim_type in {OBS, DER, INT, SPEC, VOID, FIQH}.
GEOX tracks claim *lifecycle* (DRAFT -> SEALED). WEALTH tracks *entity binding*
(named institution <=> external URI). Hermes had a reality-claim gate, now dead.

What NONE of them track is the second, orthogonal axis: *what KIND of
explanation the claim is*. That absence is what lets a true, moving, and
completely unfalsifiable sentence sit in a ledger beside a measured one and
be cited as if it were a reason.

  axis 1  claim_type   OBS / DER / INT / SPEC / VOID / FIQH   how obtained
  axis 2  claim_class  MECHANISM / PATTERN / NARRATIVE         what kind

THE LAW (F13-ratified in spirit; derived 2026-09-19):
  A NARRATIVE-class claim may be true, valuable and worth reading, and still
  carry zero explanatory power. Therefore it may be PUBLISHED, but it may not
  be the SOLE JUSTIFICATION for a mutation.

  UNCLASSIFIED fails closed: undeclared class is not action-eligible.

FOUR CHECKS, ALL MECHANICAL
---------------------------
  1. classify()             — declared class + lint for likely mismatch
  2. require_baseline()     — comparative claims must name their baseline
  3. causal_invariance()    — Turchin test: does the cause discriminate?
  4. rope_test()            — capability exists on disk but is not wired

Check 4 is the "has the well, holds the rope" state: positional access is not
capability, and an artifact with zero call sites is not a working organ.

USAGE
-----
  python3 claim_kernel.py selftest
  python3 claim_kernel.py classify "Melayu itu bangsa yang hebat"
  python3 claim_kernel.py lint-file path/to/claim.txt
  python3 claim_kernel.py rope /root/.hermes/hooks/reality-claim-gate

  from claim_kernel import classify, require_baseline, causal_invariance, rope_test
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Iterable, Optional

SCHEMA = "claim_kernel/v1"

# --------------------------------------------------------------------------
# Axis 1 — how the claim was obtained. Mirrors AAA/claim_ledger. Do not extend
# this set here; the ledger is the authority for axis 1.
# --------------------------------------------------------------------------
CLAIM_TYPES = ("OBS", "DER", "INT", "SPEC", "VOID", "FIQH")

# --------------------------------------------------------------------------
# Axis 2 — what kind of explanation this is. THIS is the new axis.
# --------------------------------------------------------------------------
MEASURED = "MEASURED"     # a quantity/observation with a number and a source
MECHANISM = "MECHANISM"   # testable cause with a stated pathway
PATTERN = "PATTERN"       # recurs across cases; cause still contested
NARRATIVE = "NARRATIVE"   # no mechanism, no measure, not falsifiable
UNCLASSIFIED = "UNCLASSIFIED"  # undeclared — fail closed
CLAIM_CLASSES = (MEASURED, MECHANISM, PATTERN, NARRATIVE, UNCLASSIFIED)

# Only these may justify a mutation.
ACTION_ELIGIBLE_CLASSES = (MEASURED, MECHANISM, PATTERN)

# --------------------------------------------------------------------------
# Markers. Deliberately small and auditable: every term here was chosen because
# it is a signal a reader can verify by eye, not because it scores well.
# --------------------------------------------------------------------------
_NARRATIVE_MARKERS = (
    # essence / destiny / blood predicates — the identity-story grammar
    r"\btakdir\b", r"\bdestiny\b", r"\bchosen\b", r"\bterpilih\b",
    r"\bbangsa\b.*\b(hebat|agung|unggul|istimewa|mulia)\b",
    r"\b(hebat|agung|unggul|istimewa|mulia)\b.*\bbangsa\b",
    r"\bblood\b", r"\binnate\b", r"\bsememangnya\b", r"\bmemang\b.*\bsifat\b",
    r"\brace\b.*\b(superior|inferior|inherent)\b",
    r"\bnaturally\b.*\b(better|worse|superior)\b",
    # superlative without a measure attached
    r"\b(paling|terhebat|terbaik|terburuk|greatest|worst|best)\b(?!.*\b(by|pada|dengan|measured|rate|%))",
    # moral verdicts standing in for a cause
    r"\b(lazy|malas|greedy|tamak|bodoh|stupid|corrupt)\b.*\b(because|sebab|kerana)\b",
)

_MECHANISM_MARKERS = (
    r"\bcaused by\b", r"\bmechanism\b", r"\bpathway\b",
    r"\bbecause\b.*\b(which|that)\b.*\b(produces|leads to|causes)\b",
    r"\bsebab\b.*\byang\b.*\bmembawa\b",
    r"\bincentive\b", r"\binsentif\b", r"\bperverse incentive\b",
    r"\bcost\b.*\bbenefit\b", r"\bmarket\b.*\bdemand\b",
    r"\bvia\b.*\b(channel|route|transmission)\b",
    r"\bfirst[- ]passage\b", r"\bdrift\b.*\bterm\b", r"\belasticity\b",
)

_PATTERN_MARKERS = (
    r"\bacross\b.*\b(cases|centuries|countries|periods|samples)\b",
    r"\brecur", r"\brepetitive\b", r"\bcorrelat",
    r"\bin \d+ (of|out of) \d+\b", r"\b\d+\s*(cases|instances|samples|episodes)\b",
    r"\bmerentas\b", r"\bcorak yang sama\b", r"\bsame pattern\b",
    r"\bsurvival\b.*\brate\b", r"\bbase rate\b", r"\bhit rate\b",
)

# A measurement is not an explanation — but it is evidence, and it is
# action-eligible. Number + unit, with no causal connector attached.
_MEASURED_MARKERS = (
    r"\d+(\.\d+)?\s*%",
    r"\brm\s?\d", r"\busd\s?\d", r"\$\s?\d",
    r"\b\d+(\.\d+)?\s*(bn|million|billion|bn|k|mmboe|bcf|mmstb|bopd|acres?)\b",
    r"\bbaseline\s*[:=]", r"\bmeasured\b", r"\bdiukur\b", r"\brekod menunjukkan\b",
    r"\b(audited|reported|declared)\b.*\d", r"\b\d+(\.\d+)?\s*(per cent|pct)\b",
)

# Comparative claims need a declared baseline. This is the two-economy error:
# a lament attached to the wrong era.
_COMPARATIVE_MARKERS = (
    r"\bdeclined? from\b", r"\bfell to\b", r"\bcompared (to|with)\b",
    r"\bmore than\b", r"\bless than\b", r"\bversus\b", r"\bvs\.?\b",
    r"\bnaik dari\b", r"\bturun dari\b", r"\bberbanding\b", r"\blebih .* daripada\b",
    r"\bworse than\b", r"\bbetter than\b", r"\bimproved? from\b",
)

_BASELINE_DECLARATION_RE = re.compile(
    r"\bbaseline\s*[:=]\s*\S+|\bcompared? to\s+(the\s+)?(19|20)\d\d|\bvs\.?\s+(19|20)\d\d"
    r"|\bfrom\s+(19|20)\d\d\b|\bsejak\s+(19|20)\d\d\b",
    re.IGNORECASE,
)

_COMPARATIVE_RE = re.compile("|".join(_COMPARATIVE_MARKERS), re.IGNORECASE)
_NARRATIVE_RE = re.compile("|".join(_NARRATIVE_MARKERS), re.IGNORECASE)
_MECHANISM_RE = re.compile("|".join(_MECHANISM_MARKERS), re.IGNORECASE)
_PATTERN_RE = re.compile("|".join(_PATTERN_MARKERS), re.IGNORECASE)
_MEASURED_RE = re.compile("|".join(_MEASURED_MARKERS), re.IGNORECASE)


# ==========================================================================
# 1. CLASSIFY
# ==========================================================================
@dataclass
class ClassVerdict:
    claim_text: str
    declared: str
    inferred: str
    agree: bool
    action_eligible: bool
    narrative_hits: list = field(default_factory=list)
    mechanism_hits: list = field(default_factory=list)
    pattern_hits: list = field(default_factory=list)
    note: str = ""
    schema: str = SCHEMA

    def to_dict(self) -> dict:
        return asdict(self)


def classify(claim_text: str, declared: str = UNCLASSIFIED) -> ClassVerdict:
    """Classify a claim's explanatory kind.

    `declared` is what the author asserts. The lint compares it against markers
    in the text. Disagreement is NOT an accusation — it is a prompt to re-read.
    The only hard rule: an undeclared claim is not action-eligible.
    """
    declared = (declared or UNCLASSIFIED).upper().strip()
    if declared not in CLAIM_CLASSES:
        declared = UNCLASSIFIED

    nar = sorted({m.group(0).lower() for m in _NARRATIVE_RE.finditer(claim_text)})
    mec = sorted({m.group(0).lower() for m in _MECHANISM_RE.finditer(claim_text)})
    pat = sorted({m.group(0).lower() for m in _PATTERN_RE.finditer(claim_text)})
    mea = sorted({m.group(0).lower() for m in _MEASURED_RE.finditer(claim_text)})

    # Inference order matters. A stated pathway outranks a number, because a
    # causal connector is the stronger claim. A number outranks recurrence,
    # because "4.6%" is verifiable where "it recurs" is an observation about
    # the observer. Narrative is last: it is what remains when neither a
    # pathway nor a quantity is present.
    if mec:
        inferred = MECHANISM
    elif mea:
        inferred = MEASURED
    elif pat:
        inferred = PATTERN
    elif nar:
        inferred = NARRATIVE
    else:
        inferred = UNCLASSIFIED

    agree = (inferred == declared) or inferred == UNCLASSIFIED or declared == UNCLASSIFIED
    eligible = declared in ACTION_ELIGIBLE_CLASSES

    note = ""
    if declared == UNCLASSIFIED:
        note = "Undeclared class. Not action-eligible (fail-closed)."
    elif declared == NARRATIVE:
        note = "Narrative: publishable, not a justification for mutation."
    elif not agree:
        note = f"Declared {declared} but the text reads as {inferred}. Re-read before use."
    if nar and declared == MECHANISM:
        note = ("Declared MECHANISM but carries narrative markers "
                f"({', '.join(nar[:3])}). A pathway must be stated.")

    return ClassVerdict(
        claim_text=claim_text,
        declared=declared,
        inferred=inferred,
        agree=agree,
        action_eligible=eligible,
        narrative_hits=nar,
        mechanism_hits=mec,
        pattern_hits=pat,
        note=note,
    )


# ==========================================================================
# 2. BASELINE
# ==========================================================================
@dataclass
class BaselineVerdict:
    comparative: bool
    has_baseline: bool
    ok: bool
    note: str = ""
    schema: str = SCHEMA

    def to_dict(self) -> dict:
        return asdict(self)


def require_baseline(claim_text: str) -> BaselineVerdict:
    """A comparative claim must name what it is comparing against.

    The failure this prevents: praising a maritime age and mourning an agrarian
    one in the same breath, as if they were one baseline. Two economies, two
    eras, one lament attached to the wrong one.
    """
    comparative = bool(_COMPARATIVE_RE.search(claim_text))
    has_baseline = bool(_BASELINE_DECLARATION_RE.search(claim_text))
    if not comparative:
        return BaselineVerdict(comparative=False, has_baseline=has_baseline, ok=True,
                               note="Not comparative.")
    ok = has_baseline
    note = "" if ok else ("Comparative claim with no declared baseline. "
                          "Name the era, unit or reference case it is measured from.")
    return BaselineVerdict(comparative=True, has_baseline=has_baseline, ok=ok, note=note)


# ==========================================================================
# 3. CAUSAL INVARIANCE — the Turchin test
# ==========================================================================
@dataclass
class InvarianceVerdict:
    cause: str
    n_positive: int
    n_negative: int
    in_positive: bool
    in_negative: bool
    verdict: str
    note: str = ""
    schema: str = SCHEMA

    def to_dict(self) -> dict:
        return asdict(self)


def causal_invariance(cause: str, positive_cases: Iterable[dict],
                      negative_cases: Iterable[dict],
                      key: str = "features") -> InvarianceVerdict:
    """Does the proposed cause actually discriminate?

    Same mechanism found across England 14c, France 17c, Russia 19c, America
    21c — four peoples, four religions, one pattern. When the pattern is
    invariant across the variable you are testing, the variable is not the
    cause. This function is that argument, executable.

    positive_cases = cases where the outcome HAPPENED
    negative_cases = cases where it did NOT
    Each case: {key: [feature, ...]}
    """
    def _has(cases, c):
        cl = c.lower()
        for case in cases:
            feats = case.get(key, []) or []
            if any(cl in str(f).lower() for f in feats):
                return True
        return False

    pos = list(positive_cases)
    neg = list(negative_cases)
    in_pos = _has(pos, cause)
    in_neg = _has(neg, cause)

    if in_pos and in_neg:
        verdict = "CAUSE_NOT_DISCRIMINATING"
        note = (f"'{cause}' appears in both the positive and the negative cases. "
                "It cannot distinguish them, so it cannot be the cause. "
                "It is a background condition, not a mechanism.")
    elif in_pos and not in_neg:
        verdict = "CAUSE_SURVIVES_CHALLENGE"
        note = (f"'{cause}' is present in the positive cases and absent in the "
                "negative cases. It survives this test — not proven, merely not "
                "yet refuted. Name the pathway next.")
    elif not in_pos:
        verdict = "CAUSE_ABSENT_WHERE_OUTCOME_OCCURS"
        note = f"'{cause}' does not appear in the positive cases at all."
    else:
        verdict = "INSUFFICIENT_CASES"
        note = "Add negative cases; a cause with no contrast cannot be tested."

    return InvarianceVerdict(
        cause=cause, n_positive=len(pos), n_negative=len(neg),
        in_positive=in_pos, in_negative=in_neg, verdict=verdict, note=note,
    )


# ==========================================================================
# 4. ROPE TEST — positional access is not capability
# ==========================================================================
@dataclass
class RopeVerdict:
    target: str
    artifact_exists: bool
    call_sites: int
    state: str
    searched_name: str = ""
    scanned_files: int = 0
    name_specificity: str = "OK"
    note: str = ""
    schema: str = SCHEMA

    def to_dict(self) -> dict:
        return asdict(self)


# A stem this short, or this common, is not a signature. Searching for it
# returns incidental prose, not call sites — and a count built on it is a
# confident number that means nothing.
_GENERIC_NAMES = {
    "server", "client", "handler", "main", "app", "core", "utils", "util",
    "config", "index", "test", "tests", "base", "common", "tools", "tool",
    "api", "models", "model", "router", "state", "types", "health", "gate",
}
_EXEC_EXTS = (".py", ".rs", ".ts", ".js", ".sh")


def rope_test(target: str, search_root: str = "/root",
              exts: tuple = (".py", ".rs", ".ts", ".js", ".sh", ".yaml", ".yml"),
              max_files: int = 40000) -> RopeVerdict:
    """'Meski telah memiliki telaga / Tangan masih memegang tali.'

    An artifact on disk that is never referenced is HOLDING_THE_ROPE: the well
    is owned, the position grants access, and the water still does not move.
    A ghost capability — named as if it works, resolving to nothing — is the
    same defect with the sign flipped.

    Two false-confidence traps this function refuses to fall into:

    * A directory whose only contents are backups is NOT wired, however many
      times its name appears across the tree. A name in prose is not a caller.
      Checked structurally, first, before any search.
    * A generic stem ('server', 'handler', 'config') is not a signature. No
      count built on one is reported as WIRED.
    """
    p = Path(target)
    if not p.exists():
        return RopeVerdict(target=target, artifact_exists=False, call_sites=0,
                           state="PHANTOM_ABSENCE",
                           note="No artifact resolves at this path right now.")

    # ---- structural check first: is there a LIVE entry point at all? ----
    if p.is_dir():
        entries = [f for f in p.iterdir()
                   if f.is_file() and ".bak" not in f.name and f.name != ".DS_Store"]
        backups = [f for f in p.iterdir() if f.is_file() and ".bak" in f.name]
        live_exec = [f for f in entries if f.suffix in _EXEC_EXTS]
        if not live_exec:
            return RopeVerdict(
                target=target, artifact_exists=True, call_sites=0,
                state="HOLDING_THE_ROPE", searched_name="",
                note=(f"No live entry point. {len(backups)} backup file(s) present, "
                      "0 executable files. The hook exists as history, not as code."),
            )
        names = {f.stem for f in live_exec}
    else:
        names = {p.stem}

    names = sorted(n for n in names if n and n not in ("__init__",))
    if not names:
        return RopeVerdict(target=target, artifact_exists=True, call_sites=0,
                           state="HOLDING_THE_ROPE",
                           note="Artifact resolves but carries no live entry point.")

    # ---- name specificity: refuse to report a number we cannot stand behind ----
    primary = max(names, key=len)
    specificity = "OK"
    if primary.lower() in _GENERIC_NAMES or len(primary) < 5:
        specificity = "GENERIC"

    pat = re.compile("|".join(re.escape(n) for n in names))
    root = Path(search_root)
    abs_target = str(p.resolve())
    hits = 0
    scanned = 0
    skip = ("node_modules", ".git", "site-packages", "__pycache__", ".venv",
            "venv", "dist", "build", ".hermes/skills", "skills-archive",
            ".archive", "skills-retired", ".backups")
    for f in root.rglob("*"):
        if scanned >= max_files:
            break
        if not f.is_file() or f.suffix not in exts:
            continue
        sp = str(f)
        if any(s in sp for s in skip):
            continue
        try:
            if str(f.resolve()) == abs_target:
                continue
        except Exception:
            pass
        scanned += 1
        try:
            txt = f.read_text(errors="ignore")
        except Exception:
            continue
        if pat.search(txt):
            hits += 1

    if specificity == "GENERIC":
        state = "INCONCLUSIVE_NAME"
        note = (f"Stem {primary!r} is too generic to be a call signature "
                f"({hits} incidental match(es) over {scanned} files). "
                "Rename the module, or probe by explicit import path.")
    elif hits > 0:
        state = "WIRED"
        note = f"{len(names)} live name(s) referenced by {hits} of {scanned} scanned files."
    else:
        state = "HOLDING_THE_ROPE"
        note = (f"Artifact exists and has a live entry point, but no file outside "
                f"itself references {names}. The well is owned; the rope is held.")

    return RopeVerdict(target=target, artifact_exists=True, call_sites=hits,
                       state=state, searched_name=primary, scanned_files=scanned,
                       name_specificity=specificity, note=note)


# ==========================================================================
# ACTION ELIGIBILITY — the one gate other organs import
# ==========================================================================
def action_eligible(claim_text: str, declared: str = UNCLASSIFIED) -> dict:
    """Full gate: may this claim justify a mutation?

    Returns {eligible: bool, reasons: [str], verdict: {...}}.
    Fail-closed. Narrative and undeclared claims are publishable but not
    usable as the sole justification for a write.
    """
    cv = classify(claim_text, declared)
    bv = require_baseline(claim_text)
    reasons = []
    if not cv.action_eligible:
        reasons.append(f"class={cv.declared} is not action-eligible")
    if not bv.ok:
        reasons.append(bv.note)
    if not cv.agree:
        reasons.append(cv.note)
    return {
        "eligible": not reasons,
        "reasons": reasons,
        "class_verdict": cv.to_dict(),
        "baseline_verdict": bv.to_dict(),
        "schema": SCHEMA,
    }


# ==========================================================================
# SELFTEST — every claim in this file is exercised against a case
# ==========================================================================
_SELFTEST = [
    # (text, declared, expect_eligible, expect_inferred)
    ("Melayu itu bangsa yang hebat dan terpilih", NARRATIVE, False, NARRATIVE),
    ("Melayu itu bangsa yang hebat dan terpilih", MECHANISM, False, NARRATIVE),
    ("Literasi universal ditetapkan pada 70M; bandar Islam kemudian bangkit "
     "dan permintaan untuk orang celik huruf meningkat, insentif berubah",
     MECHANISM, True, MECHANISM),
    ("Kitaran yang sama muncul across 4 cases: England, Perancis, Rusia, Amerika",
     PATTERN, True, PATTERN),
    ("Financing growth fell to 4.6% baseline: 2024 = 14.1%", MEASURED, True, MEASURED),
    # a measurement declared as a mechanism: the lint must catch the overclaim
    ("Financing growth fell to 4.6% baseline: 2024 = 14.1%", MECHANISM, False, MEASURED),
    ("Kadar menurun berbanding dulu", MECHANISM, False, UNCLASSIFIED),
    ("Tiada rekod awam yang boleh disahkan", UNCLASSIFIED, False, UNCLASSIFIED),
]


def selftest() -> int:
    fails = 0
    print(f"{'#':<3}{'class':<12}{'inferred':<14}{'elig':<6}note")
    for i, (txt, declared, want_elig, want_inf) in enumerate(_SELFTEST, 1):
        r = action_eligible(txt, declared)
        got_elig = r["eligible"]
        got_inf = r["class_verdict"]["inferred"]
        ok = (got_elig == want_elig) and (got_inf == want_inf)
        if not ok:
            fails += 1
        print(f"{i:<3}{declared:<12}{got_inf:<14}{str(got_elig):<6}"
              f"{'OK ' if ok else 'FAIL'}{'' if ok else ' want=' + want_inf + '/' + str(want_elig)}")
        if not ok:
            for reason in r["reasons"]:
                print(f"      - {reason}")

    # invariance
    pos = [{"features": ["elite overproduction", "state fiscal stress"]}]
    neg = [{"features": ["elite overproduction"]}]
    iv = causal_invariance("elite overproduction", pos, neg)
    if iv.verdict != "CAUSE_NOT_DISCRIMINATING":
        fails += 1
        print(f"FAIL invariance: {iv.verdict}")
    else:
        print(f"OK  invariance -> {iv.verdict}")

    # rope
    rv = rope_test("/root/AAA/lib/claim_kernel/claim_kernel.py")
    print(f"OK  rope(self) -> {rv.state} sites={rv.call_sites}")

    # rope must not be fooled by a directory that holds only backups
    dead = rope_test("/root/.hermes/hooks/reality-claim-gate")
    if dead.state == "HOLDING_THE_ROPE":
        print(f"OK  rope(dead hook) -> {dead.state}")
    else:
        fails += 1
        print(f"FAIL rope(dead hook) -> {dead.state} (expected HOLDING_THE_ROPE)")
        print(f"      {dead.note}")

    print(f"\n{'ALL PASS' if fails == 0 else str(fails) + ' FAILURE(S)'}")
    return 1 if fails else 0


# ==========================================================================
# CLI
# ==========================================================================
def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(prog="claim_kernel",
                                 description=(__doc__ or "").split("WHY")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("selftest")

    c = sub.add_parser("classify")
    c.add_argument("text")
    c.add_argument("--declared", default=UNCLASSIFIED)

    lf = sub.add_parser("lint-file")
    lf.add_argument("path")
    lf.add_argument("--declared", default=UNCLASSIFIED)

    el = sub.add_parser("eligible")
    el.add_argument("text")
    el.add_argument("--declared", default=UNCLASSIFIED)

    r = sub.add_parser("rope")
    r.add_argument("target")

    a = ap.parse_args(argv)

    if a.cmd == "selftest":
        return selftest()
    if a.cmd == "classify":
        print(json.dumps(classify(a.text, a.declared).to_dict(), indent=2))
        return 0
    if a.cmd == "lint-file":
        txt = Path(a.path).read_text()
        print(json.dumps(classify(txt, a.declared).to_dict(), indent=2))
        return 0
    if a.cmd == "eligible":
        res = action_eligible(a.text, a.declared)
        print(json.dumps(res, indent=2))
        return 0 if res["eligible"] else 1
    if a.cmd == "rope":
        print(json.dumps(rope_test(a.target).to_dict(), indent=2))
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
