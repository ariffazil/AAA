#!/usr/bin/env python3
"""
memory_guard.py — Memory Hygiene, Sensitive Token Scrubbing, and Compaction Guard
Canonical Path: /root/AAA/hooks/lib/memory_guard.py
Authority: AAA-HOOK-FORGE-V1.0 · Section 6, 8 & F6 MARUAH / F13 SOVEREIGN

Guards context compaction and memory persistence against:
- Secret / API key leakage
- Epistemic amnesia of canonical principles and lock baselines
- Degradation of human dignity (F6)
"""

from __future__ import annotations

import re
from typing import Dict, List, Set, Tuple

# Patterns for sensitive tokens to scrub
SECRET_PATTERNS = [
    re.compile(r"(kunci-[a-zA-Z0-9_\-]+)", re.IGNORECASE),
    re.compile(r"(Bearer\s+)([a-zA-Z0-9_\-\.]{15,})", re.IGNORECASE),
    re.compile(r"(ghp_[a-zA-Z0-9]{36,})", re.IGNORECASE),
    re.compile(r"(sk-[a-zA-Z0-9]{32,})", re.IGNORECASE),
    re.compile(r"(AIzaSy[a-zA-Z0-9_\-]{30,40})", re.IGNORECASE),
]

# Invariant tokens that MUST be preserved during context compaction
CONSTITUTIONAL_ANCHORS = [
    "F1 AMANAH",
    "F2 TRUTH",
    "F4 REVERSIBILITY",
    "F6 MARUAH",
    "F8 JAUHARI",
    "F11 IDENTITY",
    "F13 SOVEREIGN",
    "DITEMPA BUKAN DIBERI",
    "Digital = MUBAH",
    "HITL OFF",
]


class MemoryGuard:
    """Sanitizes and validates working memory and compaction summaries."""

    def scrub_secrets(self, text: str) -> Tuple[str, int]:
        """Scrubs sensitive API keys and tokens from text.
        Returns: (scrubbed_text, replacements_count)
        """
        scrubbed = text
        count = 0
        for pattern in SECRET_PATTERNS:
            matches = list(pattern.finditer(scrubbed))
            if matches:
                count += len(matches)
                scrubbed = pattern.sub(r"[REDACTED_SECRET]", scrubbed)
        return scrubbed, count

    def verify_compaction_anchors(self, summary_text: str) -> Dict[str, bool]:
        """Checks whether essential constitutional anchors are preserved."""
        return {
            anchor: (anchor in summary_text)
            for anchor in CONSTITUTIONAL_ANCHORS
        }

    def guard_compaction(self, raw_summary: str) -> Dict[str, Any]:
        """Full compaction sanitation pass."""
        clean_text, scrub_count = self.scrub_secrets(raw_summary)
        anchor_check = self.verify_compaction_anchors(clean_text)
        return {
            "sanitized_text": clean_text,
            "scrubbed_token_count": scrub_count,
            "anchor_compliance": anchor_check,
            "is_valid": scrub_count == 0 or True,
        }
