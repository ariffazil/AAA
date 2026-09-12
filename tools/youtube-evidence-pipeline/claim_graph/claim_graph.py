#!/usr/bin/env python3
"""
Step 5: Typed Claim Graph v0.1.0

Converts evidence segments (from transcript, ASR, OCR, or visual observation)
into typed claims with epistemic labels and corroboration status.

Input: evidence-segments.jsonl (from any upstream evidence producer)
Output: typed-claims.json + typed-claims.jsonl + receipt.json

This is a pure logic transformation — no API calls, no network, no LLM.
It classifies evidence into claim types and assigns epistemic labels
based on source modality and content patterns.

Usage:
    python3 claim_graph.py <evidence-segments.jsonl> [--output-dir DIR]
"""

import argparse
import hashlib
import json
import os
import re
import sys
import uuid
from datetime import datetime, timezone

VERSION = "0.1.0"
TOOL_NAME = "claim_graph"


def sha256_bytes(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode("utf-8")).hexdigest()


# --- Claim classification ---

QUOTATION_PATTERN = re.compile(r'^["\u201c\u201f](.+?)["\u201d]$|^"(.+)"$')
RECOMMENDATION_WORDS = {"should", "recommend", "suggest", "must", "need to", "important to", "critical to"}
COMPARISON_WORDS = {"compared to", "versus", "vs", "better than", "worse than", "more than", "less than"}


def classify_claim(text):
    """
    Classify a text segment into claim type and extract structured fields.
    Returns: {claim_type, statement, confidence, epistemic_label, limitations}
    """
    if not text or not text.strip():
        return None

    text = text.strip()

    # Check for quotation
    quote_match = QUOTATION_PATTERN.match(text)
    if quote_match:
        return {
            "claim_type": "quote",
            "statement": text,
            "confidence": 0.9,
            "epistemic_label": "OBS",
            "limitations": ["Direct transcription of spoken word; intent not verified"],
        }

    # Check for recommendation
    text_lower = text.lower()
    if any(word in text_lower for word in RECOMMENDATION_WORDS):
        return {
            "claim_type": "recommendation",
            "statement": text,
            "confidence": 0.6,
            "epistemic_label": "INT",
            "limitations": [
                "Recommendation attributed to speaker; effectiveness not verified",
                "Context-specific; may not apply generally",
            ],
        }

    # Check for comparison
    if any(word in text_lower for word in COMPARISON_WORDS):
        return {
            "claim_type": "comparison",
            "statement": text,
            "confidence": 0.7,
            "epistemic_label": "DER",
            "limitations": [
                "Comparison derived from speaker assertion; independent data not verified",
            ],
        }

    # Check for numbers/data patterns
    has_numbers = bool(re.search(r'\d+\.?\d*[%$KMBkmb]|\$\d+|RM\s*\d+|\d{4}[-/]\d{2}', text))
    if has_numbers:
        return {
            "claim_type": "factual",
            "statement": text,
            "confidence": 0.7,
            "epistemic_label": "OBS",
            "limitations": [
                "Contains numerical claims; source accuracy depends on ASR/OCR precision",
                "Independent verification recommended for financial/specific data",
            ],
        }

    # Default: factual observation
    return {
        "claim_type": "factual",
        "statement": text,
        "confidence": 0.75,
        "epistemic_label": "OBS",
        "limitations": [
            "Transcription observation; truth not independently verified",
        ],
    }


# --- Main pipeline ---

def build_claim_graph(evidence_path, output_dir=None):
    """
    Read evidence segments and produce typed claims.
    Returns receipt dict.
    """
    run_id = f"claim-graph:{uuid.uuid4().hex[:12]}"

    if output_dir is None:
        output_dir = os.path.dirname(evidence_path) or "."
    os.makedirs(output_dir, exist_ok=True)

    # Validate input
    if not os.path.exists(evidence_path):
        return _failure_receipt(run_id, "input_validation", "file_not_found",
                                f"Evidence file does not exist: {evidence_path}")

    # Read evidence segments
    segments = []
    try:
        with open(evidence_path) as f:
            for line in f:
                line = line.strip()
                if line:
                    segments.append(json.loads(line))
    except json.JSONDecodeError as e:
        return _failure_receipt(run_id, "input_parsing", "invalid_jsonl",
                                f"Invalid JSONL: {e}")

    if not segments:
        return _failure_receipt(run_id, "input_validation", "empty_evidence",
                                "No evidence segments found")

    # Process each segment into claims
    claims = []
    for seg in segments:
        text = seg.get("text", "")
        if not text or not text.strip():
            continue

        classification = classify_claim(text)
        if classification is None:
            continue

        claim_id = f"claim:{uuid.uuid4().hex[:8]}"

        claim = {
            "id": claim_id,
            "source_evidence_id": seg.get("id"),
            "video_asset_id": seg.get("video_asset_id"),
            "timestamp_seconds": seg.get("timestamp_seconds"),
            "modality": seg.get("modality"),
            "frame_id": seg.get("frame_id"),
            "claim_type": classification["claim_type"],
            "statement": classification["statement"],
            "confidence": classification["confidence"],
            "epistemic_label": classification["epistemic_label"],
            "corroboration_status": "unreviewed",
            "limitations": classification["limitations"],
            "derived_by": f"claim_graph_v{VERSION}",
            "content_class": "typed_claim",
        }

        # Compute claim hash (content-bearing fields only)
        claim_hash = sha256_bytes({
            "statement": claim["statement"],
            "claim_type": claim["claim_type"],
            "source_evidence_id": claim["source_evidence_id"],
            "modality": claim["modality"],
        })
        claim["claim_hash"] = claim_hash

        claims.append(claim)

    # Write claims JSON
    claims_json_path = os.path.join(output_dir, "typed-claims.json")
    with open(claims_json_path, "w") as f:
        json.dump({"claims": claims, "total": len(claims)}, f, indent=2, ensure_ascii=False)

    # Write claims JSONL
    claims_jsonl_path = os.path.join(output_dir, "typed-claims.jsonl")
    with open(claims_jsonl_path, "w") as f:
        for claim in claims:
            f.write(json.dumps(claim, ensure_ascii=False) + "\n")

    # Aggregate
    claim_types = {}
    epistemic_dist = {}
    modalities = set()
    for c in claims:
        ct = c["claim_type"]
        claim_types[ct] = claim_types.get(ct, 0) + 1
        el = c["epistemic_label"]
        epistemic_dist[el] = epistemic_dist.get(el, 0) + 1
        if c.get("modality"):
            modalities.add(c["modality"])

    # Build receipt
    receipt = {
        "run_id": run_id,
        "capability_id": "media.youtube.claim_graph",
        "tool_version": VERSION,
        "status": "success",
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "input": {
            "evidence_path": os.path.abspath(evidence_path),
            "segment_count": len(segments),
        },
        "evidence": {
            "claim_count": len(claims),
            "claim_types": claim_types,
            "epistemic_distribution": epistemic_dist,
            "modalities_processed": list(modalities),
            "content_class": "typed_claim_graph",
        },
        "network": {
            "allowed": True,
            "external_api": None,
            "media_downloaded": False,
            "cookies_used": False,
            "external_write": False,
        },
        "error": None,
    }

    # Write receipt
    receipt_path = os.path.join(output_dir, "receipt.json")
    with open(receipt_path, "w") as f:
        json.dump(receipt, f, indent=2)

    return receipt


def _failure_receipt(run_id, stage, error_class, message):
    return {
        "run_id": run_id,
        "capability_id": "media.youtube.claim_graph",
        "tool_version": VERSION,
        "status": "failed",
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "input": {},
        "evidence": None,
        "network": {"allowed": True, "external_api": None, "media_downloaded": False,
                     "cookies_used": False, "external_write": False},
        "error": {"stage": stage, "class": error_class, "message": message},
    }


def main():
    parser = argparse.ArgumentParser(description="Claim graph v0.1.0: evidence → typed claims")
    parser.add_argument("evidence", help="Path to evidence-segments.jsonl")
    parser.add_argument("--output-dir", default=None, help="Output directory")
    args = parser.parse_args()

    receipt = build_claim_graph(args.evidence, args.output_dir)
    print(json.dumps(receipt, indent=2))
    sys.exit(0 if receipt.get("status") == "success" else 1)


if __name__ == "__main__":
    main()
