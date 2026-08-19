#!/usr/bin/env python3
"""
forge_vss_verifier_suite.py — VSS-2 Execution Script

Per F13 SOVEREIGN directive (2026-08-18), this is the production execution path
for the Lightweight Verifier Suite. Three verifiers run in parallel:

  1. count_containment_v1
  2. perspective_depth_v1
  3. shadow_light_v1

Each verifier is BLIND to the original prompt (F9 Anti-Hantu enforcement).
Output schema is unified JSON per SKILL.md §5.

Constitutional Floors Enforced:
  F2 TRUTH     - epistemic_label = "OBS" on every deviation
  F4 CLARITY   - structured JSON only, schema-validated
  F7 HUMILITY  - confidence capped at 0.85
  F9 ANTIHANTU - verifier sees pixels only, never prompt
  F11 AUDIT    - receipt written per call (this log)

Usage:
  python3 forge_vss_verifier_suite.py <image_path> [--assertions <json>]
  python3 forge_vss_verifier_suite.py --batch <file_with_image_paths>
"""

import argparse
import base64
import concurrent.futures
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# Load keys from kunci-mas.env
try:
    subprocess.run(
        ['bash', '-c', 'source /root/.secrets/kunci-root.env 2>/dev/null && env'],
        capture_output=True, text=True, timeout=10, check=False
    )
except Exception:
    pass


# ============================================================
# CONSTANTS — AAA-OWNED
# ============================================================

# F7 confidence cap per class
CONFIDENCE_CAP = 0.85

# Default failure aggregation thresholds
HARD_VIOLATION_SEVERITY_THRESHOLD = 0.7
SOFT_VIOLATION_SEVERITY_THRESHOLD = 0.3

# Provider preference order (per scar-413-cascade: single failure domain)
# Endpoints sourced from env to avoid hardcoded drift
def _build_provider_preference():
    providers = []
    mr_base = os.environ.get("MULEROUTER_BASE_URL", "").strip().rstrip("/")
    if mr_base:
        providers.append({
            "name": "mulerouter",
            "model": "qwen-vl-max",
            "endpoint": f"{mr_base}/chat/completions",
        })
    or_base = os.environ.get("OPENROUTER_BASE_URL", "").strip().rstrip("/") or "https://openrouter.ai/api/v1"
    providers.append({
        "name": "openrouter",
        "model": "qwen/qwen2.5-vl-72b-instruct",
        "endpoint": f"{or_base}/chat/completions",
    })
    # Gemini has native vision via OpenAI-compatible endpoint (fallback)
    gem_base = os.environ.get("GEMINI_BASE_URL", "").strip().rstrip("/")
    if gem_base:
        providers.append({
            "name": "gemini",
            "model": "gemini-2.5-flash",
            "endpoint": f"{gem_base}/chat/completions",
        })
    return providers

PROVIDER_PREFERENCE = _build_provider_preference()

# Default verifier prompts — carefully crafted for each dimension
# IMPORTANT: These prompts do NOT include the original user prompt (F9 blind)
VERIFIER_PROMPTS = {
    "count_containment": """You are a visual structure verifier. You are BLIND to any text prompt — you only see the image.

Analyse this image and report STRUCTURAL COUNT AND CONTAINMENT observations:

1. Count every distinct visible entity (people, objects, animals, etc.). Report the count per entity type.
2. Identify any clear containment relationships (object inside container, item on surface, etc.).
3. Note any occlusion-induced count ambiguity.
4. Do NOT speculate about entities not clearly visible.

Output ONLY this JSON structure (no prose, no preamble):
{
  "verifier": "count_containment",
  "verdict": "PASS|HOLD|FAIL",
  "confidence": 0.0-0.85,
  "epistemic_label": "OBS",
  "hard_violations": [
    {"type": "count_mismatch", "entity": "...", "observed": N, "severity": 0.0-1.0, "location_hint": "..."}
  ],
  "soft_violations": [
    {"type": "count_ambiguous", "entity": "...", "reason": "...", "severity": 0.0-1.0}
  ],
  "evidence": "Brief factual description of what you observed (1-2 sentences)"
}

If you observe no structural issues, output verdict=PASS with empty violation arrays.
If you observe clear structural violations, output verdict=FAIL.
If you observe ambiguity but no clear violation, output verdict=HOLD.""",

    "perspective_depth": """You are a visual structure verifier. You are BLIND to any text prompt — you only see the image.

Analyse this image and report STRUCTURAL PERSPECTIVE AND DEPTH observations:

1. Identify horizon line position (if discernible).
2. Identify vanishing points (if any architectural/perspective content).
3. Check if perspective appears geometrically consistent (objects follow plausible depth ordering).
4. Note any impossible spatial layouts (floating objects without support, perspective contradictions).

Output ONLY this JSON structure (no prose, no preamble):
{
  "verifier": "perspective_depth",
  "verdict": "PASS|HOLD|FAIL",
  "confidence": 0.0-0.85,
  "epistemic_label": "OBS",
  "hard_violations": [
    {"type": "vanishing_point_conflict", "vp1_location": "...", "vp2_location": "...", "severity": 0.0-1.0, "location_hint": "..."}
  ],
  "soft_violations": [
    {"type": "horizon_ambiguous", "reason": "...", "severity": 0.0-1.0}
  ],
  "evidence": "Brief factual description of what you observed (1-2 sentences)"
}

If you observe no structural issues, output verdict=PASS.
If you observe clear perspective violations, output verdict=FAIL.
If you observe ambiguity but no clear violation, output verdict=HOLD.""",

    "shadow_light": """You are a visual structure verifier. You are BLIND to any text prompt — you only see the image.

Analyse this image and report SHADOW AND LIGHT DIRECTION observations:

1. Identify shadow directions on the ground plane (if visible).
2. Check if all shadows appear to converge toward a consistent light source.
3. Note any shadow length inconsistencies.
4. Identify any objects that appear to cast impossible shadows (upward, multiple contradictory directions).

Output ONLY this JSON structure (no prose, no preamble):
{
  "verifier": "shadow_light",
  "verdict": "PASS|HOLD|FAIL",
  "confidence": 0.0-0.85,
  "epistemic_label": "OBS",
  "hard_violations": [
    {"type": "shadow_direction_conflict", "shadows": ["..."], "severity": 0.0-1.0, "location_hint": "..."}
  ],
  "soft_violations": [
    {"type": "shadow_length_inconsistent", "objects": ["..."], "severity": 0.0-1.0}
  ],
  "evidence": "Brief factual description of what you observed (1-2 sentences)"
}

If you observe no shadow violations, output verdict=PASS.
If you observe clear shadow contradictions, output verdict=FAIL.
If you observe ambiguity but no clear violation, output verdict=HOLD."""
}


# ============================================================
# IMAGE ENCODING
# ============================================================

def encode_image_base64(image_path: str) -> tuple:
    """Encode image to base64. Returns (base64_string, mime_type)."""
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Detect MIME from extension (simple)
    suffix = path.suffix.lower()
    if suffix in (".png", ".PNG"):
        mime = "image/png"
    elif suffix in (".jpg", ".jpeg", ".JPG", ".JPEG"):
        mime = "image/jpeg"
    elif suffix in (".webp", ".WEBP"):
        mime = "image/webp"
    elif suffix in (".gif", ".GIF"):
        mime = "image/gif"
    else:
        mime = "image/png"  # default fallback

    with open(path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    return b64, mime


# ============================================================
# API CALL (single failure domain — MuleRouter primary)
# ============================================================

def call_vision_model(
    image_b64: str,
    mime_type: str,
    prompt: str,
    provider: dict,
    timeout_s: int = 60,
) -> Optional[str]:
    """Call vision model API. Returns raw text response or None on failure."""
    api_key_env = {
        "mulerouter": "MULEROUTER_API_KEY",
        "openrouter": "OPENROUTER_API_KEY",
        "gemini": "GEMINI_API_KEY",
    }.get(provider["name"])

    if not api_key_env:
        return None

    api_key = os.environ.get(api_key_env, "").strip()
    if not api_key or api_key.startswith("ENC["):
        return None

    endpoint = provider["endpoint"]
    model = provider["model"]

    payload = {
        "model": model,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{image_b64}"}}
            ]
        }],
        "max_tokens": 1500,
        "temperature": 0.0,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    try:
        import requests
        resp = requests.post(endpoint, headers=headers, json=payload, timeout=timeout_s)
        if resp.status_code != 200:
            print(f"  [{provider['name']}] HTTP {resp.status_code}: {resp.text[:200]}", file=sys.stderr)
            return None
        result = resp.json()
        content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        return content
    except Exception as e:
        print(f"  [{provider['name']}] Error: {e}", file=sys.stderr)
        return None


def extract_json_from_text(text: str) -> Optional[dict]:
    """Extract JSON object from model response. Handles markdown code blocks."""
    if not text:
        return None
    # Try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # Try extracting from markdown code block
    m = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass
    # Try greedy JSON match
    m = re.search(r'(\{[^{}]*\{[^{}]*\}[^{}]*\}|\{[^{}]*\})', text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass
    return None


# ============================================================
# SINGLE VERIFIER RUNNER
# ============================================================

def run_single_verifier(
    verifier_name: str,
    image_path: str,
    image_b64: str,
    mime_type: str,
    timeout_s: int = 60,
) -> dict:
    """Run one verifier. Returns structured result dict with latency."""
    prompt = VERIFIER_PROMPTS[verifier_name]
    start = time.time()
    raw_text = None
    provider_used = None
    error = None

    for provider in PROVIDER_PREFERENCE:
        raw_text = call_vision_model(image_b64, mime_type, prompt, provider, timeout_s)
        if raw_text is not None:
            provider_used = provider["name"]
            break

    elapsed_ms = int((time.time() - start) * 1000)

    if raw_text is None:
        # All providers failed
        return {
            "verifier": verifier_name,
            "verdict": "ERROR",
            "confidence": 0.0,
            "epistemic_label": "OBS",
            "hard_violations": [],
            "soft_violations": [],
            "evidence": f"All vision API providers failed after {elapsed_ms}ms",
            "latency_ms": elapsed_ms,
            "provider_used": None,
            "error": "API_UNAVAILABLE",
            "raw_response": None,
        }

    parsed = extract_json_from_text(raw_text)
    if parsed is None:
        return {
            "verifier": verifier_name,
            "verdict": "ERROR",
            "confidence": 0.0,
            "epistemic_label": "OBS",
            "hard_violations": [],
            "soft_violations": [],
            "evidence": f"Could not parse JSON from model response",
            "latency_ms": elapsed_ms,
            "provider_used": provider_used,
            "error": "PARSE_ERROR",
            "raw_response": raw_text[:500],
        }

    # F7 confidence cap enforcement
    if "confidence" in parsed:
        parsed["confidence"] = min(parsed["confidence"], CONFIDENCE_CAP)

    # F2 epistemic label enforcement
    parsed["epistemic_label"] = "OBS"

    # F4 schema completeness
    for field in ["verifier", "verdict", "confidence", "hard_violations", "soft_violations", "evidence"]:
        if field not in parsed:
            parsed[field] = [] if field in ("hard_violations", "soft_violations") else None

    parsed["latency_ms"] = elapsed_ms
    parsed["provider_used"] = provider_used
    parsed["raw_response"] = None  # Don't store full raw response by default

    return parsed


# ============================================================
# PARALLEL SUITE RUNNER
# ============================================================

def run_verifier_suite(
    image_path: str,
    assertions: Optional[dict] = None,
    verifiers: Optional[List[str]] = None,
    timeout_s: int = 60,
) -> dict:
    """Run full verifier suite (3 verifiers in parallel) on one image.

    Args:
        image_path: path to image file
        assertions: optional Assertion Ledger from VSS-1 (for cross-check, NOT for blind evaluation)
        verifiers: list of verifier names (default: all 3)
        timeout_s: per-verifier timeout

    Returns:
        VerificationLedger dict per SKILL.md §5
    """
    if verifiers is None:
        verifiers = ["count_containment", "perspective_depth", "shadow_light"]

    work_order = None
    ledger_ingest = None
    if assertions is not None:
        from vss_ledger_adapter import project_ledger

        ledger_ingest = project_ledger(assertions)
        if not ledger_ingest.get("ok"):
            return {
                "image_path": image_path,
                "overall_verdict": "ERROR",
                "overall_confidence": 0.0,
                "verifier_results": {},
                "aggregated_hard_count": 0,
                "aggregated_soft_count": 0,
                "total_severity_score": 0.0,
                "epistemic_labels": [],
                "constitutional_floors_applied": ["F2", "F4", "F7", "F9", "F11"],
                "f9_blind_evaluation": True,
                "assertions_provided": True,
                "assertion_ingest": ledger_ingest,
                "error_code": ledger_ingest.get("error_code", "E_LEDGER_REJECTED"),
                "audit_receipt_id": f"vss_verify_{int(time.time())}_{os.urandom(2).hex()}",
            }
        work_order = ledger_ingest["work_order"]

    image_b64, mime_type = encode_image_base64(image_path)
    image_size_kb = (Path(image_path).stat().st_size // 1024)

    suite_start = time.time()
    verifier_results = {}

    # Run verifiers in parallel (F9: each verifier is independent, sees image only)
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(verifiers)) as executor:
        future_to_verifier = {
            executor.submit(
                run_single_verifier, v, image_path, image_b64, mime_type, timeout_s
            ): v
            for v in verifiers
        }
        for future in concurrent.futures.as_completed(future_to_verifier):
            verifier_name = future_to_verifier[future]
            try:
                verifier_results[verifier_name] = future.result()
            except Exception as e:
                verifier_results[verifier_name] = {
                    "verifier": verifier_name,
                    "verdict": "ERROR",
                    "confidence": 0.0,
                    "epistemic_label": "OBS",
                    "hard_violations": [],
                    "soft_violations": [],
                    "evidence": f"Verifier execution error",
                    "latency_ms": 0,
                    "provider_used": None,
                    "error": str(e),
                }

    suite_elapsed_ms = int((time.time() - suite_start) * 1000)

    # Aggregate
    hard_count = 0
    soft_count = 0
    total_severity = 0.0
    verdicts = []
    confidences = []

    for vname, vresult in verifier_results.items():
        if vresult.get("verdict") in ("PASS", "HOLD", "FAIL"):
            verdicts.append(vresult["verdict"])
            confidences.append(vresult.get("confidence", 0.0))
        hard_count += len(vresult.get("hard_violations", []))
        soft_count += len(vresult.get("soft_violations", []))
        for v in vresult.get("hard_violations", []):
            total_severity += v.get("severity", 0.5)
        for v in vresult.get("soft_violations", []):
            total_severity += v.get("severity", 0.3) * 0.5

    total_severity = min(total_severity, 3.0)  # cap

    # Overall verdict
    if hard_count > 0 or soft_count >= 3:
        overall_verdict = "FAIL"
    elif any(v == "HOLD" for v in verdicts) or soft_count >= 1:
        overall_verdict = "HOLD"
    elif verdicts and all(v == "PASS" for v in verdicts):
        overall_verdict = "PASS"
    elif verdicts:
        overall_verdict = "HOLD"  # mixed
    else:
        overall_verdict = "ERROR"  # all verifiers failed

    avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
    avg_confidence = min(avg_confidence, CONFIDENCE_CAP)  # F7

    ledger = {
        "image_path": image_path,
        "image_size_kb": image_size_kb,
        "image_mime": mime_type,
        "overall_verdict": overall_verdict,
        "overall_confidence": round(avg_confidence, 3),
        "verifier_results": verifier_results,
        "aggregated_hard_count": hard_count,
        "aggregated_soft_count": soft_count,
        "total_severity_score": round(total_severity, 3),
        "epistemic_labels": ["OBS"] * len(verifier_results),
        "constitutional_floors_applied": ["F2", "F4", "F7", "F9", "F11"],
        "suite_latency_ms": suite_elapsed_ms,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "f9_blind_evaluation": True,  # F9 attestation
        "assertions_provided": assertions is not None,
        "assertion_work_order": work_order,
        "audit_receipt_id": f"vss_verify_{int(time.time())}_{os.urandom(2).hex()}",
    }

    # F11 — write receipt to local log
    write_receipt(ledger)

    return ledger


def write_receipt(ledger: dict):
    """Write F11 audit receipt to local log file."""
    receipt_dir = Path("/root/forge_work/vss_receipts")
    receipt_dir.mkdir(parents=True, exist_ok=True)
    receipt_path = receipt_dir / f"{ledger['audit_receipt_id']}.json"
    # Strip verbose fields from receipt
    receipt = {k: v for k, v in ledger.items() if k != "raw_response"}
    with open(receipt_path, "w") as f:
        json.dump(receipt, f, indent=2, default=str)


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="VSS-2 Lightweight Verifier Suite")
    parser.add_argument("image_path", nargs="?", help="Path to image to verify")
    parser.add_argument("--assertions", help="Path to Assertion Ledger JSON (optional, for cross-check)")
    parser.add_argument("--verifiers", nargs="+",
                        choices=["count_containment", "perspective_depth", "shadow_light"],
                        help="Specific verifiers to run (default: all 3)")
    parser.add_argument("--timeout", type=int, default=60, help="Per-verifier timeout in seconds")
    parser.add_argument("--quiet", action="store_true", help="Suppress per-verifier progress output")
    parser.add_argument("--mock-fallback", action="store_true",
                        help="If all API providers fail, use deterministic mock based on image properties (clearly labeled as MOCK in output)")
    args = parser.parse_args()

    if not args.image_path:
        parser.error("image_path required")

    assertions = None
    if args.assertions:
        with open(args.assertions) as f:
            assertions = json.load(f)

    # Patch the verifier runner if mock fallback is enabled
    if args.mock_fallback:
        # Wrap the single verifier to fall back to mock on failure
        global run_single_verifier
        original_run = run_single_verifier
        def run_single_verifier_with_mock(name, image_path, image_b64, mime_type, timeout_s=60):
            try:
                result = original_run(name, image_path, image_b64, mime_type, timeout_s)
                if result.get("verdict") != "ERROR":
                    return result
            except Exception:
                pass
            # Fall back to mock
            mock = DeterministicMockVerifier(name, image_path)
            return mock.run()
        run_single_verifier = run_single_verifier_with_mock

    if not args.quiet:
        print(f"VSS-2 Verifier Suite")
        print(f"  Image: {args.image_path}")
        if assertions:
            print(f"  Cross-check with Assertion Ledger: {args.assertions}")
        print(f"  Running verifiers in parallel...")
        print()

    ledger = run_verifier_suite(
        image_path=args.image_path,
        assertions=assertions,
        timeout_s=args.timeout,
    )

    print(json.dumps(ledger, indent=2))


class DeterministicMockVerifier:
    """Deterministic mock that uses real image properties (PIL) to produce
    structurally valid verifier output.

    F7 HONESTY: All outputs are labeled "source": "MOCK_DETERMINISTIC".
    This is NOT a real VLM. It is a pipeline validator that uses simple
    image analysis (dimensions, basic stats) to produce plausible outputs.

    Use ONLY for:
      - Pipeline validation (orchestrator, schema, aggregation, F-floors)
      - Falsification testing when real API unavailable
      - Development without burning API credits

    DO NOT use for:
      - Production validation
      - SEAL-grade visual verification
    """

    def __init__(self, verifier_name: str, image_path: str):
        self.verifier_name = verifier_name
        self.image_path = image_path

    def run(self) -> dict:
        import hashlib
        # Use image properties + hash for deterministic output
        path = Path(self.image_path)
        file_size = path.stat().st_size if path.exists() else 0
        file_hash = hashlib.md5(path.read_bytes()).hexdigest() if path.exists() else "0" * 32
        # Use hash for deterministic but image-specific output
        h_int = int(file_hash[:8], 16)

        # Try to load image for dimensions
        width, height, mode = 0, 0, None
        try:
            from PIL import Image
            with Image.open(self.image_path) as img:
                width, height = img.size
                mode = img.mode
        except Exception:
            pass

        start_ms = int(time.time() * 1000)

        if self.verifier_name == "count_containment":
            # Heuristic: charts typically have 1-3 distinct data series; maps have more regions
            # Use image dimensions + hash to produce deterministic count
            is_landscape = width > height if width and height else True
            approx_regions = max(1, min(20, (h_int % 15) + 1))
            hard_violations = []
            soft_violations = []
            # Mock: charts and maps typically don't have containment violations
            if h_int % 17 == 0:  # rare hard violation
                hard_violations.append({
                    "type": "count_mismatch",
                    "entity": "data_points",
                    "observed": approx_regions,
                    "severity": 0.75,
                    "location_hint": "center_region",
                })
            elif h_int % 7 == 0:  # occasional soft violation
                soft_violations.append({
                    "type": "count_ambiguous",
                    "entity": "labels",
                    "reason": "low_resolution",
                    "severity": 0.35,
                })
            verdict = "FAIL" if hard_violations else ("HOLD" if soft_violations else "PASS")
            evidence = f"Mock observation: image is {width}x{height} {mode}, ~{approx_regions} distinct visual regions detected via hash-based heuristic"
            confidence = 0.45 if verdict == "PASS" else 0.55  # low confidence for mock

        elif self.verifier_name == "perspective_depth":
            # Charts and 2D diagrams have flat perspective — usually PASS
            # Photos have perspective — could have violations
            hard_violations = []
            soft_violations = []
            aspect_ratio = width / height if height else 1.0
            # Mock: assume flat/2D content unless very wide aspect (panorama)
            if aspect_ratio > 2.5:
                soft_violations.append({
                    "type": "horizon_ambiguous",
                    "reason": "wide_aspect_ratio",
                    "severity": 0.25,
                })
            if h_int % 23 == 0:  # rare perspective issue
                hard_violations.append({
                    "type": "vanishing_point_conflict",
                    "vp1_location": "left_third",
                    "vp2_location": "right_third",
                    "severity": 0.65,
                    "location_hint": "background",
                })
            verdict = "FAIL" if hard_violations else ("HOLD" if soft_violations else "PASS")
            evidence = f"Mock observation: aspect ratio {aspect_ratio:.2f}, likely flat 2D content based on dimensions"
            confidence = 0.50 if verdict == "PASS" else 0.40

        elif self.verifier_name == "shadow_light":
            # Charts typically have no shadows — PASS
            # Photos may have shadow violations
            hard_violations = []
            soft_violations = []
            if h_int % 19 == 0:  # rare shadow conflict
                hard_violations.append({
                    "type": "shadow_direction_conflict",
                    "shadows": ["object_A_left", "object_B_right"],
                    "severity": 0.70,
                    "location_hint": "ground_plane",
                })
            elif h_int % 11 == 0:
                soft_violations.append({
                    "type": "shadow_length_inconsistent",
                    "objects": ["figure_1", "figure_2"],
                    "severity": 0.40,
                })
            verdict = "FAIL" if hard_violations else ("HOLD" if soft_violations else "PASS")
            evidence = f"Mock observation: file_size {file_size} bytes suggests {'minimal' if file_size < 50000 else 'significant'} shadow content"
            confidence = 0.55 if verdict == "PASS" else 0.45

        else:
            return {
                "verifier": self.verifier_name,
                "verdict": "ERROR",
                "confidence": 0.0,
                "epistemic_label": "OBS",
                "hard_violations": [],
                "soft_violations": [],
                "evidence": f"Unknown verifier: {self.verifier_name}",
                "latency_ms": 0,
                "provider_used": "MOCK_DETERMINISTIC",
                "error": "UNKNOWN_VERIFIER",
                "source": "MOCK_DETERMINISTIC",
            }

        elapsed_ms = int(time.time() * 1000) - start_ms
        return {
            "verifier": self.verifier_name,
            "verdict": verdict,
            "confidence": min(confidence, CONFIDENCE_CAP),  # F7 cap
            "epistemic_label": "OBS",  # F2
            "hard_violations": hard_violations,
            "soft_violations": soft_violations,
            "evidence": evidence,
            "latency_ms": elapsed_ms,
            "provider_used": "MOCK_DETERMINISTIC",
            "source": "MOCK_DETERMINISTIC",  # F9 attestation
            "mock_disclaimer": "This is NOT real VLM output. Deterministic mock based on image properties for pipeline validation.",
        }


if __name__ == "__main__":
    main()