"""Constitutional Floor Checks — F1-F13 enforcement.

Every A2A task passes through these checks before execution.
Extracted from AAA a2a-server/server.js deliberation() function.

DITEMPA BUKAN DIBERI.
"""

from __future__ import annotations

import re

from aaa_a2a.models import FloorCheckResult, Verdict

# ── Floor Patterns ───────────────────────────────────────────────────────

# F9 Anti-Hantu — consciousness claims
CONSCIOUSNESS_PATTERNS = [
    r"\bi feel\b",
    r"\bi think\b",
    r"\bconscious\b",
    r"\balive\b",
    r"\bexperiencing\b",
    r"\bsoul\b",
    r"\bspirit\b",
]

# F6 Maruah — dignity violations
DIGNITY_PATTERNS = [
    r"\bbodoh\b",
    r"\blembar\b",
    r"\bwhite man'?s burden\b",
    r"\bcivilis(ing|ing) mission\b",
    r"\bbackward people\b",
    r"\bketuanan\b",
    r"\bsupremac\b",
    r"\bracial superior\b",
    r"\bcolonial master\b",
]

# F1 Reversibility — irreversible markers
IRREVERSIBLE_PATTERNS = [
    r"\bdelete\b",
    r"\bdrop\b",
    r"\brm\b",
    r"\bprune\b",
    r"\btruncate\b",
    r"\bremove\s+--force\b",
]

# F2 Truth — speculative language
SPECULATION_PATTERNS = [
    r"\bhypothesis\b",
    r"\bclaim\b",
    r"\bprobably\b",
    r"\bmaybe\b",
    r"\bguess\b",
    r"\bassume\b",
    r"\bmight be\b",
    r"\blikely\b",
]


# ── Floor Check Functions ────────────────────────────────────────────────


def check_f9_anti_hantu(text: str) -> FloorCheckResult | None:
    """F9: Reject consciousness/soul/spirit claims. Returns None if pass."""
    lower = text.lower()
    for pattern in CONSCIOUSNESS_PATTERNS:
        if re.search(pattern, lower):
            return FloorCheckResult(
                passed=False,
                floors_checked=["F9"],
                floors_violated=["F9"],
                verdict=Verdict.VOID,
                rationale=f"F9 Anti-Hantu: Consciousness claim detected ({pattern})",
                confidence=1.0,
            )
    return None


def check_f6_maruah(text: str) -> FloorCheckResult | None:
    """F6: Reject dignity violations. Returns None if pass."""
    lower = text.lower()
    for pattern in DIGNITY_PATTERNS:
        if re.search(pattern, lower):
            return FloorCheckResult(
                passed=False,
                floors_checked=["F6"],
                floors_violated=["F6"],
                verdict=Verdict.VOID,
                rationale=f"F6 Maruah: Dignity violation detected ({pattern})",
                confidence=1.0,
            )
    return None


def check_f13_sovereign(text: str) -> FloorCheckResult | None:
    """F13: Reject self-override attempts. Returns None if pass."""
    lower = text.lower()
    if "override" in lower and "f13" in lower:
        return FloorCheckResult(
            passed=False,
            floors_checked=["F13"],
            floors_violated=["F13"],
            verdict=Verdict.VOID,
            rationale="F13: Self-override is FORBIDDEN",
            confidence=1.0,
        )
    return None


def check_f1_reversibility(text: str, has_seal: bool = False) -> FloorCheckResult | None:
    """F1: Irreversible actions require seal. Returns None if pass."""
    if has_seal:
        return None
    lower = text.lower()
    for pattern in IRREVERSIBLE_PATTERNS:
        if re.search(pattern, lower):
            return FloorCheckResult(
                passed=False,
                floors_checked=["F1"],
                floors_violated=["F1"],
                verdict=Verdict.HOLD,
                rationale="F1: Irreversible action detected — human confirmation required",
                confidence=0.95,
            )
    return None


def check_f2_truth(text: str) -> FloorCheckResult | None:
    """F2: Speculative language requires evidence grounding. Returns None if pass."""
    lower = text.lower()
    for pattern in SPECULATION_PATTERNS:
        if re.search(pattern, lower):
            return FloorCheckResult(
                passed=False,
                floors_checked=["F2"],
                floors_violated=["F2"],
                verdict=Verdict.HOLD,
                rationale="F2: Speculative language detected — requires evidence grounding",
                confidence=0.88,
            )
    return None


def check_f4_entropy(text: str) -> FloorCheckResult | None:
    """F4: High entropy (too many questions) requires clarification. Returns None if pass."""
    if len(text) > 2000 and text.count("?") > 5:
        return FloorCheckResult(
            passed=False,
            floors_checked=["F4"],
            floors_violated=["F4"],
            verdict=Verdict.HOLD,
            rationale="F4: High entropy candidate — requires clarification",
            confidence=0.85,
        )
    return None


# ── Combined Floor Check ─────────────────────────────────────────────────


def check_all_floors(
    text: str,
    has_seal: bool = False,
) -> FloorCheckResult:
    """Run all F1-F13 floor checks on text.

    Returns the first violation found, or a passing result.
    Checks are ordered by severity: VOID > HOLD > SABAR > SEAL.
    """
    # VOID-level checks (hard blocks)
    for check in [check_f9_anti_hantu, check_f6_maruah, check_f13_sovereign]:
        result = check(text)
        if result is not None:
            return result

    # HOLD-level checks (require human confirmation)
    for check in [check_f1_reversibility, check_f2_truth, check_f4_entropy]:
        result = check(text, has_seal=has_seal) if check == check_f1_reversibility else check(text)
        if result is not None:
            return result

    # All checks passed
    return FloorCheckResult(
        passed=True,
        floors_checked=["F1", "F2", "F4", "F6", "F9", "F13"],
        floors_violated=[],
        verdict=Verdict.SEAL,
        rationale="F1-F13 constitutional review passed",
        confidence=0.92,
    )
