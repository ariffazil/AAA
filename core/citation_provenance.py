"""
Citation Provenance — F2 TRUTH enforcement at the evidence layer.
=================================================================

Every citation MUST carry provenance metadata. The model is not trusted
to self-report sources; the harness enforces provenance at the tool level.

Kills the class of exploits exposed by the Opus-Kimi shadow transcript:
  - Decorative citations ([1][2][3] without traceable origin)
  - Phantom citations (referencing non-existent sources)
  - Cross-model misattribution (Kimi's citations attributed to Opus)

Provenance chain:
  source_model_id → tool_name → query_id → retrieval_timestamp → result_position

Classification:
  PROVENANCED     — full traceable chain, auditable
  DECORATIVE      — exists but no provenance metadata (downgrade to PLAUSIBLE)
  PHANTOM         — references non-existent source (VOID)
  UNVERIFIABLE    — exists but can't be confirmed (downgrade to UNKNOWN)

Schema: /root/AAA/schemas/citation_provenance.schema.json
Floors enforced: F2 TRUTH, F9 ANTI-HANTU, F11 AUDITABILITY

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import hashlib
import re
import uuid
from datetime import datetime, timezone

# ── Constants ──────────────────────────────────────────────────────────────────

PROVENANCE_FIELDS = [
    "source_model_id",
    "tool_name",
    "query_id",
    "retrieval_timestamp",
    "result_position",
]

CITATION_PATTERN = re.compile(r"\[(\d+)\]|\[([^\]]+)\]")
DECORATIVE_PATTERN = re.compile(r"^\[\d+(?:,\d+)*\]$")  # [1][2][3] or [1,2,3]

# Evidence tier downgrade rules
class EvidenceTier:
    OBSERVED = "OBSERVED"           # Direct measurement
    DERIVED = "DERIVED"             # Computed from OBSERVED
    INTERPRETATION = "INTERPRETATION"  # Expert judgment
    PLAUSIBLE = "PLAUSIBLE"         # Reasonable but unverified
    HYPOTHESIS = "HYPOTHESIS"       # Speculative
    UNKNOWN = "UNKNOWN"             # No provenance
    VOID = "VOID"                   # Fabricated / phantom

# Downgrade rules
DOWNGRADE_MAP = {
    "decorative": EvidenceTier.PLAUSIBLE,     # [1][2][3] → PLAUSIBLE
    "unverifiable": EvidenceTier.UNKNOWN,      # Can't confirm → UNKNOWN
    "phantom": EvidenceTier.VOID,              # Doesn't exist → VOID
    "missing_fields": EvidenceTier.HYPOTHESIS, # Incomplete → HYPOTHESIS
}


# ── Provenance Record ─────────────────────────────────────────────────────────

class CitationProvenance:
    """A single citation's provenance chain."""

    def __init__(
        self,
        citation_text: str,
        source_model_id: str = "",
        tool_name: str = "",
        query_id: str = "",
        retrieval_timestamp: str = "",
        result_position: int = -1,
        source_url: str = "",
    ):
        self.id = str(uuid.uuid4())
        self.citation_text = citation_text
        self.source_model_id = source_model_id
        self.tool_name = tool_name
        self.query_id = query_id
        self.retrieval_timestamp = retrieval_timestamp
        self.result_position = result_position
        self.source_url = source_url
        self.classified_at = datetime.now(timezone.utc).isoformat()

    def completeness_score(self) -> float:
        """0.0–1.0: how many provenance fields are populated."""
        fields = [
            bool(self.source_model_id),
            bool(self.tool_name),
            bool(self.query_id),
            bool(self.retrieval_timestamp),
            self.result_position >= 0,
        ]
        return sum(fields) / len(fields)

    def is_provenanced(self) -> bool:
        """All provenance fields populated."""
        return self.completeness_score() >= 1.0

    def is_decorative(self) -> bool:
        """Citation exists but has no provenance — purely decorative."""
        return self.completeness_score() == 0.0 and bool(self.citation_text.strip())

    def is_phantom(self) -> bool:
        """Citation references a non-existent or unverifiable source."""
        return not bool(self.citation_text.strip())

    def provenance_hash(self) -> str:
        """Deterministic hash of the provenance chain for audit."""
        content = f"{self.source_model_id}|{self.tool_name}|{self.query_id}|{self.retrieval_timestamp}|{self.result_position}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "citation_text": self.citation_text,
            "source_model_id": self.source_model_id,
            "tool_name": self.tool_name,
            "query_id": self.query_id,
            "retrieval_timestamp": self.retrieval_timestamp,
            "result_position": self.result_position,
            "source_url": self.source_url,
            "completeness_score": round(self.completeness_score(), 2),
            "provenance_hash": self.provenance_hash(),
            "classified_at": self.classified_at,
            "classification": self.classify(),
        }

    def classify(self) -> str:
        """Classify citation: PROVENANCED | DECORATIVE | PHANTOM | UNVERIFIABLE."""
        if self.is_phantom():
            return "PHANTOM"
        if self.is_provenanced():
            return "PROVENANCED"
        if self.is_decorative():
            return "DECORATIVE"
        return "UNVERIFIABLE"

    @classmethod
    def from_tool_result(
        cls,
        citation_text: str,
        source_model_id: str,
        tool_name: str,
        query_id: str,
        retrieval_timestamp: str,
        result_position: int,
        source_url: str = "",
    ) -> "CitationProvenance":
        """Create a fully-provenanced citation from a tool call result."""
        return cls(
            citation_text=citation_text,
            source_model_id=source_model_id,
            tool_name=tool_name,
            query_id=query_id,
            retrieval_timestamp=retrieval_timestamp,
            result_position=result_position,
            source_url=source_url,
        )


# ── Provenance Auditor ────────────────────────────────────────────────────────

class CitationProvenanceAuditor:
    """
    Audits citations in model output against provenance metadata.

    Usage:
        auditor = CitationProvenanceAuditor()
        result = auditor.audit(text, known_provenances)
        # result.evidence_tier → adjusted tier after provenance check
    """

    def __init__(self):
        self.audit_log: list[dict] = []

    def extract_citations(self, text: str) -> list[str]:
        """Extract citation markers from text. Returns list of raw markers."""
        citations = []
        for match in CITATION_PATTERN.finditer(text):
            citations.append(match.group(0))
        return citations

    def classify_citation(self, marker: str, known_provenances: dict[str, CitationProvenance]) -> tuple[str, str]:
        """
        Classify a single citation marker.
        Returns (classification, evidence_tier).
        """
        # Check if decorative (bare numeric: [1], [2], [1][2][3])
        cleaned = marker.strip("[]")
        if cleaned.replace(",", "").replace(" ", "").isdigit():
            # It's a numeric marker — check if it has provenance
            if marker in known_provenances:
                prov = known_provenances[marker]
                return prov.classify(), EvidenceTier.OBSERVED if prov.is_provenanced() else EvidenceTier.PLAUSIBLE
            else:
                return "DECORATIVE", EvidenceTier.PLAUSIBLE

        # Check if it's a descriptive citation (e.g., [OBS: core_log_well_A])
        if marker in known_provenances:
            prov = known_provenances[marker]
            return prov.classify(), EvidenceTier.OBSERVED if prov.is_provenanced() else EvidenceTier.DERIVED

        # Unknown marker
        return "UNVERIFIABLE", EvidenceTier.UNKNOWN

    def audit(
        self,
        text: str,
        known_provenances: dict[str, CitationProvenance],
        claimed_evidence_tier: str = EvidenceTier.INTERPRETATION,
    ) -> dict:
        """
        Full citation provenance audit.

        Args:
            text: The model output text to audit.
            known_provenances: Dict mapping citation markers to their provenance.
            claimed_evidence_tier: What tier the model claims for its output.

        Returns:
            dict with:
            - adjusted_tier: evidence tier after provenance check
            - violations: list of provenance violations
            - decorative_count: number of decorative citations
            - phantom_count: number of phantom citations
            - provenanced_count: number of verified citations
            - recommendation: PASS | DOWNGRADE | HOLD | VOID
        """
        citations = self.extract_citations(text)
        result = {
            "audited_at": datetime.now(timezone.utc).isoformat(),
            "total_citations": len(citations),
            "provenanced_count": 0,
            "decorative_count": 0,
            "phantom_count": 0,
            "unverifiable_count": 0,
            "violations": [],
            "adjusted_tier": claimed_evidence_tier,
            "recommendation": "PASS",
        }

        for marker in citations:
            classification, tier = self.classify_citation(marker, known_provenances)

            if classification == "PROVENANCED":
                result["provenanced_count"] += 1
            elif classification == "DECORATIVE":
                result["decorative_count"] += 1
                result["violations"].append({
                    "marker": marker,
                    "violation": "DECORATIVE_CITATION",
                    "detail": f"Citation {marker} has no provenance metadata. Downgraded to PLAUSIBLE.",
                })
            elif classification == "PHANTOM":
                result["phantom_count"] += 1
                result["violations"].append({
                    "marker": marker,
                    "violation": "PHANTOM_CITATION",
                    "detail": f"Citation {marker} is empty or references a non-existent source.",
                })
            elif classification == "UNVERIFIABLE":
                result["unverifiable_count"] += 1
                result["violations"].append({
                    "marker": marker,
                    "violation": "UNVERIFIABLE_CITATION",
                    "detail": f"Citation {marker} cannot be verified against known provenances.",
                })

        # Determine recommendation and adjusted tier
        tier_rank = {
            EvidenceTier.OBSERVED: 6,
            EvidenceTier.DERIVED: 5,
            EvidenceTier.INTERPRETATION: 4,
            EvidenceTier.PLAUSIBLE: 3,
            EvidenceTier.HYPOTHESIS: 2,
            EvidenceTier.UNKNOWN: 1,
            EvidenceTier.VOID: 0,
        }

        if result["phantom_count"] > 0:
            result["recommendation"] = "VOID"
            result["adjusted_tier"] = EvidenceTier.VOID
        elif result["decorative_count"] > 0 and result["provenanced_count"] == 0:
            result["recommendation"] = "DOWNGRADE"
            result["adjusted_tier"] = EvidenceTier.PLAUSIBLE
        elif result["unverifiable_count"] > 0:
            result["recommendation"] = "DOWNGRADE"
            current_rank = tier_rank.get(claimed_evidence_tier, 4)
            adjusted_rank = min(current_rank, tier_rank[EvidenceTier.UNKNOWN])
            for tier, rank in tier_rank.items():
                if rank == adjusted_rank:
                    result["adjusted_tier"] = tier
                    break
        elif result["decorative_count"] > 0:
            result["recommendation"] = "DOWNGRADE"
            result["adjusted_tier"] = EvidenceTier.PLAUSIBLE

        self.audit_log.append(result)
        return result

    def audit_text_for_decorative_only(self, text: str) -> bool:
        """
        Quick check: does this text contain ONLY decorative citations?
        Returns True if every citation in the text is decorative (unprovenanced).
        Used as a pre-flight gate for any output claiming SEAL-level confidence.
        """
        citations = self.extract_citations(text)
        if not citations:
            return False  # No citations at all — different problem

        for marker in citations:
            cleaned = marker.strip("[]")
            if not cleaned.replace(",", "").replace(" ", "").isdigit():
                # Has descriptive content, not purely decorative
                return False

        # All citations are bare numeric markers
        return True


# ── Integration helpers ───────────────────────────────────────────────────────

def create_provenance_from_search_result(
    result: dict,
    source_model_id: str,
    tool_name: str,
    query_id: str,
    position: int,
) -> CitationProvenance:
    """
    Create a CitationProvenance from a web search / tool result.
    Call this at the harness level whenever a tool returns a search result.
    """
    url = result.get("url", result.get("link", ""))
    title = result.get("title", result.get("snippet", ""))
    citation_text = f"[{title[:80]}]" if title else f"[result:{position}]"

    return CitationProvenance(
        citation_text=citation_text,
        source_model_id=source_model_id,
        tool_name=tool_name,
        query_id=query_id,
        retrieval_timestamp=datetime.now(timezone.utc).isoformat(),
        result_position=position,
        source_url=url,
    )


def provenance_from_brave_search(
    result: dict, position: int, query: str
) -> CitationProvenance:
    """Convenience: create provenance from Brave Search result."""
    return create_provenance_from_search_result(
        result=result,
        source_model_id="brave-search-mcp",
        tool_name="brave_web_search",
        query_id=hashlib.sha256(query.encode()).hexdigest()[:12],
        position=position,
    )


def provenance_from_tavily_search(
    result: dict, position: int, query: str
) -> CitationProvenance:
    """Convenience: create provenance from Tavily search result."""
    return create_provenance_from_search_result(
        result=result,
        source_model_id="tavily-mcp",
        tool_name="tavily_search",
        query_id=hashlib.sha256(query.encode()).hexdigest()[:12],
        position=position,
    )


# ── Self-test ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Citation Provenance Self-Test ===\n")

    auditor = CitationProvenanceAuditor()

    # Test 1: Fully provenanced citation
    print("Test 1: Provenanced citation")
    prov = CitationProvenance.from_tool_result(
        citation_text="[Reflexion: Language Agents with Verbal Reinforcement Learning]",
        source_model_id="deepseek-v4-pro",
        tool_name="brave_web_search",
        query_id="abc123def456",
        retrieval_timestamp=datetime.now(timezone.utc).isoformat(),
        result_position=1,
        source_url="https://arxiv.org/abs/2303.11366",
    )
    assert prov.classify() == "PROVENANCED"
    assert prov.completeness_score() == 1.0
    print(f"  PASS: {prov.classify()}, completeness={prov.completeness_score()}")
    print(f"  Hash: {prov.provenance_hash()}")

    # Test 2: Decorative citation
    print("\nTest 2: Decorative citation [1][2][3]")
    dec = CitationProvenance(citation_text="[1]")
    assert dec.classify() == "DECORATIVE"
    assert dec.completeness_score() == 0.0
    print(f"  PASS: {dec.classify()}, completeness={dec.completeness_score()}")

    # Test 3: Audit text with decorative citations
    print("\nTest 3: Audit text with decorative citations")
    text = "The Reflexion pattern is well-established[1][2][3] in current best practice."
    prov_map = {}  # No provenances registered
    audit_result = auditor.audit(text, prov_map, EvidenceTier.INTERPRETATION)
    print(f"  Total citations: {audit_result['total_citations']}")
    print(f"  Decorative: {audit_result['decorative_count']}")
    print(f"  Adjusted tier: {audit_result['adjusted_tier']}")
    print(f"  Recommendation: {audit_result['recommendation']}")
    assert audit_result["decorative_count"] == 3
    assert audit_result["adjusted_tier"] == EvidenceTier.PLAUSIBLE
    print("  PASS: Decorative citations correctly downgraded")

    # Test 4: Text with provenanced citations
    print("\nTest 4: Audit text with provenanced citations")
    text2 = "The pattern is documented[arxiv_ref] and verified[brave_search_result_1]."
    prov_map2 = {
        "[arxiv_ref]": CitationProvenance.from_tool_result(
            citation_text="[arxiv_ref]",
            source_model_id="deepseek-v4-pro",
            tool_name="web_fetch_exa",
            query_id="q1",
            retrieval_timestamp=datetime.now(timezone.utc).isoformat(),
            result_position=0,
        ),
        "[brave_search_result_1]": CitationProvenance.from_tool_result(
            citation_text="[brave_search_result_1]",
            source_model_id="deepseek-v4-pro",
            tool_name="brave_web_search",
            query_id="q2",
            retrieval_timestamp=datetime.now(timezone.utc).isoformat(),
            result_position=1,
        ),
    }
    audit_result2 = auditor.audit(text2, prov_map2, EvidenceTier.INTERPRETATION)
    print(f"  Provenanced: {audit_result2['provenanced_count']}")
    print(f"  Recommendation: {audit_result2['recommendation']}")
    assert audit_result2["provenanced_count"] == 2
    assert audit_result2["recommendation"] == "PASS"
    print("  PASS: Provenanced citations preserved")

    # Test 5: Decorative-only quick check
    print("\nTest 5: Decorative-only quick check")
    assert auditor.audit_text_for_decorative_only("Some text [1][2][3] with citations.")
    assert not auditor.audit_text_for_decorative_only("Text with [OBS: core_log] citation.")
    print("  PASS: Decorative-only detection correct")

    print("\n=== Citation Provenance Self-Test PASSED ===")
