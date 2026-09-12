#!/usr/bin/env python3
"""
OpenClaw Semantic Router v1.0.0

LLM-based intent classification fallback when regex confidence < threshold.
Uses FED :4000 flash lane (free inference) for classification.

Architecture:
  1. Regex router runs first (fast, deterministic, free)
  2. If regex confidence < 0.7 → semantic router kicks in
  3. Semantic router calls FED flash lane for classification
  4. Result cached in Redis L1 (TTL 5min) for repeated patterns

Forged: 2026-09-12 by 333-AGI under F13 directive
DITEMPA BUKAN DIBERI
"""

from __future__ import annotations

import json
import os
import time
import hashlib
import urllib.request
import urllib.error
from typing import Any, Optional
from dataclasses import dataclass, field, asdict


# ─── Constants ───────────────────────────────────────────────────────────
FED_FLASH_URL = os.environ.get("FED_FLASH_URL", "http://127.0.0.1:4000/v1/chat/completions")
FED_MODEL = os.environ.get("FED_MODEL", "agi-333")
FED_TIMEOUT = int(os.environ.get("FED_TIMEOUT", "10"))
CONFIDENCE_THRESHOLD = float(os.environ.get("SEMANTIC_ROUTER_THRESHOLD", "0.7"))
CACHE_TTL_SECONDS = int(os.environ.get("SEMANTIC_CACHE_TTL", "300"))  # 5 min

# Rule ID → description mapping for LLM context
RULE_DESCRIPTIONS = {
    "R01_HOLD_ESCALATE": "Emergency/hold/stop/override — constitutional escalation to arifOS",
    "R02_RESEARCH": "Research, analysis, audit, investigation, deep dive — route to Hermes",
    "R03_CODE_EXECUTE": "Code, git, docker, deploy, build, fix, patch, refactor — route to A-FORGE/OpenCode",
    "R04_POSITION_QUICK": "Quick position/portfolio check — local cache or WEALTH",
    "R05_EARTH_DOMAIN": "Geology, seismic, basin, petrophysics, well logs — route to GEOX",
    "R06_CAPITAL_DOMAIN": "NPV, IRR, market, FX, commodity, portfolio, risk — route to WEALTH",
    "R07_VITALITY_DOMAIN": "Sleep, fatigue, health, vitality, stress — route to WELL",
    "R08_SYSTEM_STATUS": "System/federation/organ health/status — route to AAA",
    "R09_DELIVER_ARTIFACT": "Send/deliver/report/brief/artifact — local cache or Hermes",
    "R10_DEFAULT_TRIAGE": "Unclear/ambiguous — route to Hermes for triage",
}

# Multi-intent detection patterns
MULTI_INTENT_INDICATORS = [
    " and ",
    " then ",
    " also ",
    " plus ",
    " after that ",
    " serta ",
    " lepas tu ",
    " pastu ",
    " sekali ",
    ",",  # comma-separated intents
]


@dataclass
class SemanticResult:
    """Result from semantic classification."""

    rule_id: str
    confidence: float
    is_multi_intent: bool = False
    sub_intents: list[dict] = field(default_factory=list)
    raw_response: str = ""
    latency_ms: int = 0
    source: str = "semantic"  # semantic | cached | regex_ambiguous
    cached: bool = False


class SemanticRouter:
    """
    LLM-based intent classifier for OpenClaw.
    Falls back from regex when confidence < threshold.
    """

    def __init__(self, *, cache_dir: str = "/tmp/openclaw-semantic-cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        self._cache: dict[str, tuple[float, SemanticResult]] = {}

    # ─── Public API ──────────────────────────────────────────────────

    def classify(
        self,
        query: str,
        *,
        regex_candidates: list[dict] | None = None,
        person_id: str = "unknown",
        context: dict | None = None,
    ) -> SemanticResult:
        """
        Classify intent using LLM when regex is ambiguous.

        Args:
            query: User message text
            regex_candidates: List of {rule_id, confidence, pattern} from regex router
            person_id: For cache key
            context: Additional context (channel, language, etc.)

        Returns:
            SemanticResult with rule_id, confidence, and multi-intent info
        """
        start_ms = int(time.time() * 1000)

        # Check cache first
        cache_key = self._cache_key(query, person_id)
        cached = self._cache_get(cache_key)
        if cached:
            cached.cached = True
            return cached

        # Detect multi-intent
        is_multi, segments = self._detect_multi_intent(query)

        # Build LLM prompt
        prompt = self._build_prompt(query, regex_candidates, is_multi, segments, context)

        # Call FED flash lane
        try:
            raw_response = self._call_fed(prompt)
            result = self._parse_response(raw_response, is_multi, segments)
        except Exception as e:
            # Fallback to best regex candidate or default
            result = self._fallback_result(regex_candidates, str(e))

        result.latency_ms = int(time.time() * 1000) - start_ms
        result.is_multi_intent = is_multi

        # Cache result
        self._cache_set(cache_key, result)

        return result

    def classify_multi(
        self,
        query: str,
        *,
        person_id: str = "unknown",
        context: dict | None = None,
    ) -> list[SemanticResult]:
        """
        Classify multi-intent message → list of SemanticResults.
        Each sub-intent gets its own classification.
        """
        is_multi, segments = self._detect_multi_intent(query)
        if not is_multi:
            return [self.classify(query, person_id=person_id, context=context)]

        results = []
        for segment in segments:
            segment = segment.strip()
            if not segment:
                continue
            r = self.classify(segment, person_id=person_id, context=context)
            results.append(r)

        return results if results else [self.classify(query, person_id=person_id, context=context)]

    # ─── Multi-Intent Detection ──────────────────────────────────────

    def _detect_multi_intent(self, query: str) -> tuple[bool, list[str]]:
        """Detect if message contains multiple intents."""
        query_lower = query.lower()

        # Check for explicit multi-intent indicators
        for indicator in MULTI_INTENT_INDICATORS:
            if indicator in query_lower:
                # Split on the indicator
                parts = [p.strip() for p in query.split(indicator) if p.strip()]
                if len(parts) >= 2:
                    # Validate each segment is substantial (>5 chars)
                    substantial = [p for p in parts if len(p) > 5]
                    if len(substantial) >= 2:
                        return True, substantial

        return False, [query]

    # ─── LLM Classification ─────────────────────────────────────────

    def _build_prompt(
        self,
        query: str,
        regex_candidates: list[dict] | None,
        is_multi: bool,
        segments: list[str],
        context: dict | None,
    ) -> str:
        """Build classification prompt for FED flash lane."""
        rules_text = "\n".join(f"  {rid}: {desc}" for rid, desc in RULE_DESCRIPTIONS.items())

        candidates_text = ""
        if regex_candidates:
            candidates_text = "\nRegex candidates (may be ambiguous):\n"
            for c in regex_candidates[:3]:
                candidates_text += f"  - {c.get('rule_id', '?')} (confidence: {c.get('confidence', 0):.2f})\n"

        multi_hint = ""
        if is_multi:
            multi_hint = f"\nThis message contains {len(segments)} sub-intents. Classify the PRIMARY intent."

        context_hint = ""
        if context:
            context_hint = f"\nContext: {json.dumps(context)[:200]}"

        return f"""You are an intent classifier for an AI agent orchestrator.
Classify this user message into exactly ONE rule ID.

RULES:
{rules_text}

USER MESSAGE: "{query}"
{candidates_text}{multi_hint}{context_hint}

Respond with ONLY a JSON object:
{{"rule_id": "R##_XXXX", "confidence": 0.0-1.0, "reason": "one line"}}

If the message is truly ambiguous, use R10_DEFAULT_TRIAGE with low confidence."""

    def _call_fed(self, prompt: str) -> str:
        """Call FED flash lane for classification."""
        payload = json.dumps(
            {
                "model": FED_MODEL,
                "messages": [
                    {"role": "system", "content": "You are a precise intent classifier. Respond with ONLY valid JSON."},
                    {"role": "user", "content": prompt},
                ],
                "max_tokens": 200,
                "temperature": 0.1,
            }
        ).encode()

        req = urllib.request.Request(
            FED_FLASH_URL,
            data=payload,
            method="POST",
            headers={"Content-Type": "application/json"},
        )

        with urllib.request.urlopen(req, timeout=FED_TIMEOUT) as resp:
            data = json.loads(resp.read().decode())
            return data["choices"][0]["message"]["content"]

    def _parse_response(
        self,
        raw: str,
        is_multi: bool,
        segments: list[str],
    ) -> SemanticResult:
        """Parse LLM response into SemanticResult."""
        # Extract JSON from response
        raw = raw.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0].strip()

        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            # Try to find JSON in response
            import re

            match = re.search(r"\{[^}]+\}", raw)
            if match:
                parsed = json.loads(match.group())
            else:
                return SemanticResult(
                    rule_id="R10_DEFAULT_TRIAGE",
                    confidence=0.3,
                    raw_response=raw,
                )

        rule_id = parsed.get("rule_id", "R10_DEFAULT_TRIAGE")
        confidence = float(parsed.get("confidence", 0.5))

        # Validate rule_id exists
        if rule_id not in RULE_DESCRIPTIONS:
            rule_id = "R10_DEFAULT_TRIAGE"
            confidence = 0.3

        result = SemanticResult(
            rule_id=rule_id,
            confidence=confidence,
            raw_response=raw,
        )

        # If multi-intent, store sub-intent info
        if is_multi and len(segments) > 1:
            result.sub_intents = [{"segment": seg, "index": i} for i, seg in enumerate(segments)]

        return result

    def _fallback_result(
        self,
        regex_candidates: list[dict] | None,
        error: str,
    ) -> SemanticResult:
        """Fallback when LLM fails — use best regex candidate or default."""
        if regex_candidates:
            best = max(regex_candidates, key=lambda c: c.get("confidence", 0))
            return SemanticResult(
                rule_id=best.get("rule_id", "R10_DEFAULT_TRIAGE"),
                confidence=best.get("confidence", 0.5),
                source="regex_ambiguous",
                raw_response=f"Fallback from LLM error: {error}",
            )

        return SemanticResult(
            rule_id="R10_DEFAULT_TRIAGE",
            confidence=0.3,
            source="fallback",
            raw_response=f"LLM error: {error}",
        )

    # ─── Cache ───────────────────────────────────────────────────────

    def _cache_key(self, query: str, person_id: str) -> str:
        """Generate cache key from query + person_id."""
        content = f"{person_id}:{query.lower().strip()}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def _cache_get(self, key: str) -> Optional[SemanticResult]:
        """Get from in-memory cache with TTL check."""
        if key in self._cache:
            ts, result = self._cache[key]
            if time.time() - ts < CACHE_TTL_SECONDS:
                return result
            del self._cache[key]
        return None

    def _cache_set(self, key: str, result: SemanticResult) -> None:
        """Store in in-memory cache."""
        self._cache[key] = (time.time(), result)
        # Evict old entries (keep max 1000)
        if len(self._cache) > 1000:
            oldest = sorted(self._cache.items(), key=lambda x: x[1][0])[:500]
            for k, _ in oldest:
                del self._cache[k]


# ─── Module-level singleton ─────────────────────────────────────────────
_router: SemanticRouter | None = None


def get_semantic_router() -> SemanticRouter:
    """Get or create the singleton SemanticRouter."""
    global _router
    if _router is None:
        _router = SemanticRouter()
    return _router


def classify_intent(
    query: str,
    *,
    regex_candidates: list[dict] | None = None,
    person_id: str = "unknown",
    context: dict | None = None,
) -> SemanticResult:
    """Convenience function for one-shot classification."""
    return get_semantic_router().classify(
        query,
        regex_candidates=regex_candidates,
        person_id=person_id,
        context=context,
    )


def classify_multi_intents(
    query: str,
    *,
    person_id: str = "unknown",
    context: dict | None = None,
) -> list[SemanticResult]:
    """Convenience function for multi-intent classification."""
    return get_semantic_router().classify_multi(
        query,
        person_id=person_id,
        context=context,
    )


# ─── CLI ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python semantic_router.py 'user message'")
        print("  --multi  Detect and classify multiple intents")
        sys.exit(1)

    query = sys.argv[1]
    multi_mode = "--multi" in sys.argv

    if multi_mode:
        results = classify_multi_intents(query, person_id="cli-test")
        for i, r in enumerate(results):
            print(f"\n--- Intent {i + 1} ---")
            print(json.dumps(asdict(r), indent=2))
    else:
        result = classify_intent(query, person_id="cli-test")
        print(json.dumps(asdict(result), indent=2))
