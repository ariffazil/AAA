#!/usr/bin/env python3
"""
Step 6: Video-to-Skill Draft v0.1.0

Converts typed claims into a procedure_candidate draft artifact.
NOT an approved skill. NOT executable. Requires human review + 888_HOLD.

Input: typed-claims.json (from claim_graph.py)
Output: procedure-candidate.yaml + receipt.json

This is a template-based extraction — no LLM, no network.
It identifies procedural claims (recommendations, steps, comparisons)
and structures them into a procedure candidate schema.

Usage:
    python3 video_skill.py <typed-claims.json> [--output-dir DIR] [--source-video ID]
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
TOOL_NAME = "video_skill"


def sha256_bytes(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode("utf-8")).hexdigest()


# --- Procedure extraction ---

def extract_procedure_from_claims(claims):
    """
    Extract procedural content from typed claims.
    Identifies: recommendations, steps, tools, risks, preconditions.
    """
    procedural_types = {"recommendation", "factual"}
    procedural_claims = [c for c in claims if c.get("claim_type") in procedural_types]

    if not procedural_claims:
        return None

    # Extract potential steps (claims containing imperative-ish language)
    steps = []
    tools_mentioned = set()
    risks = []

    for i, claim in enumerate(procedural_claims):
        statement = claim.get("statement", "")
        claim_type = claim.get("claim_type", "")

        # Look for step-like patterns
        is_step = any(marker in statement.lower() for marker in [
            "first", "then", "next", "after", "before", "step",
            "run", "execute", "install", "configure", "set up",
            "create", "build", "deploy", "run", "use",
        ])

        if is_step or claim_type == "recommendation":
            steps.append({
                "order": len(steps) + 1,
                "instruction": statement,
                "evidence_ref": claim.get("source_evidence_id"),
                "confidence": claim.get("confidence", 0.7),
                "epistemic_label": claim.get("epistemic_label", "OBS"),
            })

        # Look for tool mentions
        tool_patterns = [
            r'\b(python|pip|npm|docker|git|curl|ffmpeg|tesseract|yt-dlp)\b',
            r'\b(install|run|execute|build|deploy)\s+(\S+)',
        ]
        for pattern in tool_patterns:
            matches = re.findall(pattern, statement, re.IGNORECASE)
            for m in matches:
                if isinstance(m, tuple):
                    tools_mentioned.add(m[1])
                else:
                    tools_mentioned.add(m)

        # Look for risk language
        risk_words = {"risk", "danger", "warning", "caution", "careful", "avoid", "never", "don't"}
        if any(word in statement.lower() for word in risk_words):
            risks.append(statement)

    if not steps:
        return None

    return {
        "steps": steps[:20],  # cap at 20 steps
        "tools": list(tools_mentioned)[:10],
        "risks": risks[:10],
    }


def yaml_quote(s):
    """Quote a YAML string if it contains special characters."""
    if any(c in s for c in ":#{}[]|>&*!%@`\"\n"):
        return f'"{s.replace(chr(10), "\\n").replace('"', '\\"')}"'
    return s


def write_procedure_yaml(candidate, output_path):
    """Write procedure candidate as YAML (no external deps)."""
    lines = []
    cand_id = candidate["id"]
    source_vid = candidate["source_video"]
    created = candidate["created_at"]
    ver = candidate["version"]
    lines.append(f'id: "proc:{cand_id}"')
    lines.append(f'source_video: "{source_vid}"')
    lines.append(f'created_at: "{created}"')
    lines.append(f'version: "{ver}"')
    lines.append('')
    lines.append('source_evidence:')
    for ref in candidate.get("source_evidence_refs", []):
        lines.append(f'  - "{ref}"')
    lines.append('')
    lines.append(f'purpose: {yaml_quote(candidate.get("purpose", "Extracted from video evidence"))}')
    lines.append('')
    lines.append('preconditions:')
    lines.append('  - "Video evidence has been extracted and claims generated"')
    lines.append('  - "Human review required before any activation"')
    lines.append('')
    lines.append('steps:')
    for step in candidate.get("steps", []):
        lines.append(f'  - order: {step["order"]}')
        lines.append(f'    instruction: {yaml_quote(step["instruction"])}')
        lines.append(f'    evidence_ref: "{step.get("evidence_ref", "unknown")}"')
        lines.append(f'    confidence: {step.get("confidence", 0.7)}')
    lines.append('')
    lines.append('tools_required:')
    for tool in candidate.get("tools", []):
        lines.append(f'  - "{tool}"')
    lines.append('')
    lines.append('risks:')
    for risk in candidate.get("risks", []):
        lines.append(f'  - {yaml_quote(risk)}')
    lines.append('')
    lines.append('reversibility: "mixed"')
    lines.append('')
    lines.append('verification:')
    lines.append('  test_case_required: true')
    lines.append('  source_independent_corroboration_required: true')
    lines.append('')
    lines.append('governance:')
    lines.append('  state: draft_only')
    lines.append('  activation_gate: "888_HOLD"')
    lines.append('  human_review_required: true')
    lines.append('  created_by: "video_skill_v0.1.0"')

    with open(output_path, "w") as f:
        f.write("\n".join(lines) + "\n")


def build_video_skill(claims_path, output_dir=None, source_video=None):
    """
    Main pipeline: typed claims → procedure candidate.
    Returns receipt dict.
    """
    run_id = f"video-skill:{uuid.uuid4().hex[:12]}"

    if output_dir is None:
        output_dir = os.path.dirname(claims_path) or "."
    os.makedirs(output_dir, exist_ok=True)

    # Validate input
    if not os.path.exists(claims_path):
        return _failure_receipt(run_id, "input_validation", "file_not_found",
                                f"Claims file does not exist: {claims_path}")

    # Read claims
    try:
        with open(claims_path) as f:
            data = json.load(f)
        claims = data.get("claims", []) if isinstance(data, dict) else data
    except json.JSONDecodeError as e:
        return _failure_receipt(run_id, "input_parsing", "invalid_json",
                                f"Invalid JSON: {e}")

    if not claims:
        return _failure_receipt(run_id, "input_validation", "empty_claims",
                                "No claims found")

    if source_video is None:
        # Try to infer from first claim
        source_video = claims[0].get("video_asset_id", "unknown")

    # Extract procedure
    procedure = extract_procedure_from_claims(claims)
    if procedure is None:
        return _failure_receipt(run_id, "extraction", "no_procedural_content",
                                "No procedural content found in claims")

    # Build candidate
    candidate_id = uuid.uuid4().hex[:8]
    candidate = {
        "id": candidate_id,
        "source_video": source_video,
        "source_evidence_refs": [
            c.get("source_evidence_id") for c in claims[:20]
            if c.get("source_evidence_id")
        ],
        "purpose": "Procedure extracted from video evidence (draft — requires human review)",
        "steps": procedure["steps"],
        "tools": procedure["tools"],
        "risks": procedure["risks"],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "version": VERSION,
    }

    # Write YAML
    yaml_path = os.path.join(output_dir, f"procedure-candidate-{candidate_id}.yaml")
    write_procedure_yaml(candidate, yaml_path)

    # Write JSON
    json_path = os.path.join(output_dir, "procedure-candidate.json")
    with open(json_path, "w") as f:
        json.dump(candidate, f, indent=2, ensure_ascii=False)

    # Build receipt
    receipt = {
        "run_id": run_id,
        "capability_id": "media.youtube.video_to_skill",
        "tool_version": VERSION,
        "status": "success",
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "input": {
            "claims_path": os.path.abspath(claims_path),
            "claim_count": len(claims),
            "source_video": source_video,
        },
        "evidence": {
            "candidate_id": candidate_id,
            "step_count": len(procedure["steps"]),
            "tools_mentioned": len(procedure["tools"]),
            "risks_identified": len(procedure["risks"]),
            "governance_state": "draft_only",
            "activation_gate": "888_HOLD",
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
        "capability_id": "media.youtube.video_to_skill",
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
    parser = argparse.ArgumentParser(description="Video-to-skill v0.1.0: claims → procedure draft")
    parser.add_argument("claims", help="Path to typed-claims.json")
    parser.add_argument("--output-dir", default=None, help="Output directory")
    parser.add_argument("--source-video", default=None, help="Source video ID")
    args = parser.parse_args()

    receipt = build_video_skill(args.claims, args.output_dir, args.source_video)
    print(json.dumps(receipt, indent=2))
    sys.exit(0 if receipt.get("status") == "success" else 1)


if __name__ == "__main__":
    main()
