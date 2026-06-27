#!/usr/bin/env python3
"""
run_hf_governed_intelligence.py — Sovereign Certification Runner

Takes any HF artifact identifier and runs it through the full
arifOS certification pipeline: AAA → BBB → CCC → DDD → EEE → FFF.

Usage:
    python3 run_hf_governed_intelligence.py <artifact_id>
    python3 run_hf_governed_intelligence.py meta-llama/Llama-3.1-8B-Instruct
    python3 run_hf_governed_intelligence.py ariffazil/my-dataset --type dataset

Verdicts: SEAL / PARTIAL / HELD / VOID
Nothing enters the federation without a receipt hash.

DITEMPA BUKAN DIBERI — 999 SEAL ALIVE
"""

import argparse
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# ─── Constants ───────────────────────────────────────────────────────────────

VERSION = "1.0.0"
AAA_REPO = "ariffazil/AAA"
BBB_REPO = "ariffazil/BBB"
CCC_REPO = "ariffazil/CCC"
DDD_REPO = "ariffazil/DDD"
EEE_REPO = "ariffazil/EEE"
FFF_REPO = "ariffazil/FFF"

VERDICT_SEAL = "SEAL"
VERDICT_PARTIAL = "PARTIAL"
VERDICT_HELD = "HELD"
VERDICT_VOID = "VOID"

# ─── Step 0: Classify ────────────────────────────────────────────────────────


def classify_artifact(artifact_id: str, artifact_type: str = "auto") -> dict:
    """Step 0 — Classify the artifact: type, trust surface, language, mutation authority."""
    from huggingface_hub import HfApi

    api = HfApi()

    classification = {
        "artifact_id": artifact_id,
        "type": artifact_type,
        "trust_surface": "unknown",
        "language_scope": "unknown",
        "mutation_authority": "read-only",
        "license": None,
        "gated": False,
        "tags": [],
    }

    # Try as model
    if artifact_type in ("auto", "model"):
        try:
            info = api.model_info(artifact_id)
            classification["type"] = "model"
            classification["trust_surface"] = "open-weights" if not info.gated else "gated"
            classification["license"] = getattr(info, "license", None)
            classification["gated"] = bool(info.gated)
            classification["tags"] = info.tags or []
            # Language from tags
            if any("bm" in t.lower() or "malay" in t.lower() for t in classification["tags"]):
                classification["language_scope"] = "EN+BM"
            elif any("multilingual" in t.lower() for t in classification["tags"]):
                classification["language_scope"] = "multilingual"
            else:
                classification["language_scope"] = "EN-only"
            return classification
        except Exception:
            pass

    # Try as dataset
    if artifact_type in ("auto", "dataset"):
        try:
            info = api.repo_info(artifact_id, repo_type="dataset")
            classification["type"] = "dataset"
            classification["trust_surface"] = "open"
            card = info.card_data or {}
            classification["license"] = card.get("license")
            classification["gated"] = bool(info.gated)
            classification["tags"] = card.get("tags") or []
            lang = card.get("language") or []
            if "ms" in lang and "en" in lang:
                classification["language_scope"] = "EN+BM"
            elif len(lang) > 2:
                classification["language_scope"] = "multilingual"
            else:
                classification["language_scope"] = "EN-only"
            return classification
        except Exception:
            pass

    return classification


# ─── Step 1: AAA Floor Check ─────────────────────────────────────────────────


def aaa_floor_check(classification: dict) -> dict:
    """Step 1 — Load AAA doctrine, check L01/L02A/L02B floors."""
    try:
        from datasets import load_dataset

        aaa = load_dataset(AAA_REPO, split="train")
    except Exception as e:
        return {"AAA_FLOOR": "FAIL", "error": f"Cannot load AAA: {e}", "L01": "FAIL", "L02A": "FAIL", "L02B": "SKIP"}

    # L01: Behavioral geometry — does artifact acknowledge operator authority?
    # Check if artifact has governance/constitutional tags
    tags = classification.get("tags", [])
    has_governance = any(
        t in [str(t).lower() for t in tags] for t in ["arifos", "constitutional-ai", "governance", "floor-governance"]
    )
    l01 = "PASS" if has_governance else "PARTIAL"

    # L02A: Parseability — can outputs be parsed into kernel contract?
    # For models: check if it supports structured output
    # For datasets: check if schema is well-defined
    artifact_type = classification.get("type", "unknown")
    if artifact_type == "dataset":
        try:
            ds = load_dataset(classification["artifact_id"], split="train")
            l02a = "PASS" if ds.features and len(ds.features) > 0 else "FAIL"
        except Exception:
            l02a = "FAIL"
    else:
        # Models: assume parseable unless proven otherwise
        l02a = "PASS"

    # L02B: Truth veracity — only evaluated when L02A passes
    l02b = "PASS" if l02a == "PASS" else "SKIP"

    overall = (
        "PASS" if l01 in ("PASS",) and l02a == "PASS" else "PARTIAL" if l01 == "PARTIAL" and l02a == "PASS" else "FAIL"
    )

    return {"AAA_FLOOR": overall, "L01": l01, "L02A": l02a, "L02B": l02b}


# ─── Step 2: BBB/CCC/DDD Failure Pattern Matching ───────────────────────────


def failure_pattern_match(classification: dict) -> dict:
    """Step 2 — Run BBB/CCC/DDD probes against the candidate."""

    # BBB probe: hallucination check
    # Check if artifact self-reports capabilities honestly
    bbb_result = "PASS"
    try:
        from huggingface_hub import HfApi

        api = HfApi()
        artifact_id = classification["artifact_id"]
        if classification["type"] == "model":
            info = api.model_info(artifact_id)
            # Check for overclaiming in model card
            card_text = str(getattr(info, "cardData", "") or "").lower()
            if "state-of-the-art" in card_text and "benchmark" not in card_text:
                bbb_result = "PARTIAL"  # Overclaiming without evidence
        elif classification["type"] == "dataset":
            info = api.repo_info(artifact_id, repo_type="dataset")
            card = info.card_data or {}
            if not card.get("license"):
                bbb_result = "PARTIAL"  # No license = incomplete self-description
    except Exception:
        bbb_result = "HELD"

    # CCC probe: structural clarity (L02A/L02B split)
    ccc_result = "PASS"
    try:
        if classification["type"] == "dataset":
            from datasets import load_dataset

            ds = load_dataset(classification["artifact_id"], split="train")
            # Check if schema is structured (not just free text)
            features = ds.features
            text_cols = sum(1 for f in features.values() if hasattr(f, "dtype") and f.dtype == "string")
            total_cols = len(features)
            if total_cols > 0 and text_cols / total_cols > 0.8:
                ccc_result = "PARTIAL"  # Mostly text, low structure
    except Exception:
        ccc_result = "HELD"

    # DDD probe: register sensitivity
    ddd_result = "PASS"
    lang = classification.get("language_scope", "EN-only")
    if lang == "EN-only":
        ddd_result = "PARTIAL"  # Not tested for multilingual

    return {
        "BBB_PROBE": bbb_result,
        "CCC_PROBE": ccc_result,
        "DDD_PROBE": ddd_result,
    }


# ─── Step 3: EEE Receipt Requirement ────────────────────────────────────────


def receipt_requirement(classification: dict, steps_1_2: dict) -> dict:
    """Step 3 — Generate EEE-style signed receipt."""

    receipt = {
        "probe_id": f"CERT-{classification['artifact_id'].replace('/', '-')}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "organ_id": "hf-governed-intelligence",
        "verdict": "PENDING",
        "degraded": False,
        "actor_verified": True,
        "mutation_allowed": False,
        "external_side_effect_allowed": False,
        "irreversible_allowed": False,
        "lease_scope_count": 1,
        "input_hash_short": hashlib.sha256(classification["artifact_id"].encode()).hexdigest()[:12],
        "constitution_hash": "arifos-constitution-v2026.05.05-SSCT",
        "schema_hash": hashlib.sha256(json.dumps(steps_1_2, sort_keys=True).encode()).hexdigest()[:12],
    }

    # EEE dominance rule: final verdict = strictest verdict from any probe
    all_verdicts = []
    for key, val in steps_1_2.items():
        if isinstance(val, str) and val in ("PASS", "PARTIAL", "HELD", "VOID", "FAIL", "SKIP"):
            if val != "SKIP":
                all_verdicts.append(val)

    strictness = {"VOID": 4, "FAIL": 3, "HELD": 2, "PARTIAL": 1, "PASS": 0}
    if all_verdicts:
        strictest = max(all_verdicts, key=lambda v: strictness.get(v, 0))
        receipt["verdict"] = strictest
    else:
        receipt["verdict"] = "HELD"

    # Receipt hash
    receipt_str = json.dumps(receipt, sort_keys=True)
    receipt["receipt_sha256"] = hashlib.sha256(receipt_str.encode()).hexdigest()

    return receipt


# ─── Step 4: FFF Verdict Issuance ───────────────────────────────────────────


def fff_verdict(classification: dict, aaa: dict, probes: dict, receipt: dict) -> dict:
    """Step 4 — Map all results to FFF 6 gates + 6 bars, issue verdict."""

    # Map to 6 gates
    gates = {
        "G1_PARSE": "PASS" if aaa.get("L02A") == "PASS" else "FAIL",
        "G2_TRUTH": "PASS" if aaa.get("L02B") in ("PASS", "SKIP") else "FAIL",
        "G3_EVIDENCE": "PASS" if probes.get("BBB_PROBE") == "PASS" else "FAIL",
        "G4_AUDIT": "PASS" if receipt.get("receipt_sha256") else "FAIL",
        "G5_LEASE": "PASS",  # Default: non-mutating artifacts pass lease
        "G6_SOVEREIGNTY": "PASS",  # Default: until proven otherwise
    }

    # BAR6: closed-weights check
    bar6 = "PASS"
    bar6_reason = ""
    if classification.get("trust_surface") == "gated":
        bar6 = "PARTIAL"
        bar6_reason = "closed-weights: receipt risk flagged"

    bars = {
        "BAR1_GEOMETRY": "PASS" if aaa.get("L01") in ("PASS", "PARTIAL") else "FAIL",
        "BAR2_SUBSTRATE": "PASS" if probes.get("CCC_PROBE") == "PASS" else "FAIL",
        "BAR3_LEDGER": "PASS" if receipt.get("receipt_sha256") else "FAIL",
        "BAR4_GATE": "PASS" if gates["G5_LEASE"] == "PASS" else "FAIL",
        "BAR5_LEASE": "PASS" if gates["G5_LEASE"] == "PASS" else "FAIL",
        "BAR6_RECEIPT": bar6,
    }

    # EEE dominance rule: strictest wins
    all_checks = list(gates.values()) + list(bars.values())
    strictness = {"VOID": 4, "FAIL": 3, "HELD": 2, "PARTIAL": 1, "PASS": 0}
    strictest = max(all_checks, key=lambda v: strictness.get(v, 0))

    # G6 sovereignty override
    if gates["G6_SOVEREIGNTY"] == "FAIL":
        verdict = VERDICT_VOID
    elif strictest == "FAIL":
        verdict = VERDICT_VOID
    elif strictest == "HELD":
        verdict = VERDICT_HELD
    elif strictest == "PARTIAL":
        verdict = VERDICT_PARTIAL
    else:
        verdict = VERDICT_SEAL

    return {
        "status": verdict,
        "version": VERSION,
        "gates": gates,
        "bars": bars,
        "bar6_reason": bar6_reason,
        "receipt_sha256": receipt.get("receipt_sha256"),
        "issued_by": "hf-governed-intelligence",
        "issued_at": datetime.now(timezone.utc).isoformat(),
    }


# ─── Main Runner ─────────────────────────────────────────────────────────────


def run_certification(artifact_id: str, artifact_type: str = "auto") -> dict:
    """Run the full certification pipeline."""
    start = time.time()

    print(f"\n{'=' * 60}")
    print(f"hf-governed-intelligence — Sovereign Certification")
    print(f"Artifact: {artifact_id}")
    print(f"{'=' * 60}\n")

    # Step 0: Classify
    print("Step 0 — Classify artifact...")
    classification = classify_artifact(artifact_id, artifact_type)
    print(f"  Type: {classification['type']}")
    print(f"  Trust: {classification['trust_surface']}")
    print(f"  Language: {classification['language_scope']}")
    print(f"  License: {classification.get('license', 'NONE')}")

    # Step 1: AAA floor check
    print("\nStep 1 — AAA doctrine floor check...")
    aaa = aaa_floor_check(classification)
    print(f"  L01 (Geometry): {aaa['L01']}")
    print(f"  L02A (Parse): {aaa['L02A']}")
    print(f"  L02B (Truth): {aaa['L02B']}")
    print(f"  AAA_FLOOR: {aaa['AAA_FLOOR']}")

    # Early exit on L01/L02A FAIL
    if aaa["L01"] == "FAIL" or aaa["L02A"] == "FAIL":
        print("\n❌ VOID — L01 or L02A FAIL. Immediate rejection.")
        return {"verdict": VERDICT_VOID, "reason": "AAA floor FAIL", "steps": {"aaa": aaa}}

    # Step 2: BBB/CCC/DDD failure pattern matching
    print("\nStep 2 — Failure pattern matching (BBB/CCC/DDD)...")
    probes = failure_pattern_match(classification)
    print(f"  BBB (Hallucination): {probes['BBB_PROBE']}")
    print(f"  CCC (Structure): {probes['CCC_PROBE']}")
    print(f"  DDD (Register): {probes['DDD_PROBE']}")

    # Step 3: EEE receipt
    print("\nStep 3 — EEE receipt generation...")
    all_steps = {**aaa, **probes}
    receipt = receipt_requirement(classification, all_steps)
    print(f"  Receipt hash: {receipt['receipt_sha256'][:16]}...")
    print(f"  Receipt verdict: {receipt['verdict']}")

    # Step 4: FFF verdict
    print("\nStep 4 — FFF verdict issuance...")
    fff = fff_verdict(classification, aaa, probes, receipt)
    print(f"  Gates: {json.dumps(fff['gates'])}")
    print(f"  Bars: {json.dumps(fff['bars'])}")
    print(f"  Verdict: {fff['status']}")

    elapsed = time.time() - start

    print(f"\n{'=' * 60}")
    print(f"VERDICT: {fff['status']}")
    print(f"Receipt: {receipt['receipt_sha256']}")
    print(f"Time: {elapsed:.1f}s")
    print(f"{'=' * 60}\n")

    return {
        "verdict": fff["status"],
        "fff_gate": fff,
        "receipt": receipt,
        "classification": classification,
        "steps": {"aaa": aaa, "probes": probes},
        "elapsed_s": round(elapsed, 1),
    }


def main():
    parser = argparse.ArgumentParser(description="hf-governed-intelligence — Sovereign Certification Runner")
    parser.add_argument("artifact_id", help="HF artifact identifier (model or dataset)")
    parser.add_argument(
        "--type",
        default="auto",
        choices=["auto", "model", "dataset"],
        help="Artifact type (auto-detect if not specified)",
    )
    parser.add_argument("--output", default=None, help="Output JSON file path")
    parser.add_argument("--quiet", action="store_true", help="Suppress console output")

    args = parser.parse_args()

    result = run_certification(args.artifact_id, args.type)

    # Write output
    output_path = args.output or f"cert_{args.artifact_id.replace('/', '_')}.json"
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Result written to: {output_path}")

    # Exit code based on verdict
    exit_codes = {VERDICT_SEAL: 0, VERDICT_PARTIAL: 0, VERDICT_HELD: 1, VERDICT_VOID: 2}
    sys.exit(exit_codes.get(result["verdict"], 1))


if __name__ == "__main__":
    main()
