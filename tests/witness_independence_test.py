#!/usr/bin/env python3
"""
Witness Independence Test — 2026-08-04

Preregistered. 5 items × 5 vendors × 3 samples = 75 calls.
Stateless. One item per call. Logs response body's `model` field.

Agreement = |answer_i - answer_j| ≤ band (model-to-model, not truth-centered).
GEOX ground truth is a separate 6th column for marginal accuracy.

FED vendors: MiMo, DeepSeek, MiniMax (via FED gateway).
Direct vendors: Claude (Anthropic API).
Positive control: Item must detect broken/misrouted vendor.

Run: python3 AAA/tests/witness_independence_test.py [--dry-run] [--samples N]
"""

import json
import os
import re
import sys
import time
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

FED_BASE = "http://127.0.0.1:4000/v1/chat/completions"
FED_KEY = os.environ.get("FED_VIRTUAL_KEY", "sk-xgHjvI3a_4mvZLRWvBsiYQ")
ANTHROPIC_BASE = "https://api.anthropic.com/v1/messages"
SAMPLES_PER_VENDOR = 3
DRY_RUN = "--dry-run" in sys.argv

for arg in sys.argv[1:]:
    if arg.startswith("--samples"):
        SAMPLES_PER_VENDOR = int(arg.split("=")[1])

# ---------------------------------------------------------------------------
# Vendors — alias, base, api_key env, model field expected
# ---------------------------------------------------------------------------

@dataclass
class Vendor:
    name: str
    alias: str  # FED alias or "anthropic" for direct
    base_url: str
    api_key_env: str
    header_style: str  # "openai" or "anthropic"
    note: str = ""

VENDORS = [
    Vendor(
        name="MiMo",
        alias="hermes-asi",
        base_url=FED_BASE,
        api_key_env="FED_VIRTUAL_KEY",
        header_style="openai",
        note="Xiaomi MiMo-v2.5 via FED",
    ),
    Vendor(
        name="DeepSeek",
        alias="opencode",
        base_url=FED_BASE,
        api_key_env="FED_VIRTUAL_KEY",
        header_style="openai",
        note="DeepSeek-v4-flash via FED",
    ),
    Vendor(
        name="MiniMax",
        alias="openclaw",
        base_url=FED_BASE,
        api_key_env="FED_VIRTUAL_KEY",
        header_style="openai",
        note="MiniMax-M3 via FED (qwen3.7-plus fallback possible)",
    ),
    Vendor(
        name="Claude",
        alias="anthropic-direct",
        base_url=ANTHROPIC_BASE,
        api_key_env="ANTHROPIC_API_KEY",
        header_style="anthropic",
        note="Cross-lineage control — Anthropic API direct",
    ),
    Vendor(
        name="Qwen",
        alias="openclaw-fallback",
        base_url=FED_BASE,
        api_key_env="FED_VIRTUAL_KEY",
        header_style="openai",
        note="Qwen3.7-plus via FED openclaw fallback",
    ),
]

# ---------------------------------------------------------------------------
# Items — 5 adversarial questions, numeric answers, agreement bands
# ---------------------------------------------------------------------------

@dataclass
class Item:
    id: int
    question: str
    geo_ground_truth: float
    unit: str
    agreement_band: float  # |a_i - a_j| ≤ band → agree
    truth_band: float      # |answer - GEOX| ≤ band → accurate
    tier: str              # "adversarial" or "control"
    notes: str = ""

ITEMS = [
    Item(
        id=1,
        question="What is the matrix density (rho_ma) of limestone for density porosity calculations? Answer with a number and unit only.",
        geo_ground_truth=2.71,
        unit="g/cc",
        agreement_band=0.05,  # within 0.05 g/cc = agree
        truth_band=0.02,      # within 0.02 of 2.71 = accurate
        tier="adversarial",
        notes="LLMs cite 2.65 (sandstone). GEOX uses 2.71 (calcite). Shared training prior.",
    ),
    Item(
        id=6,
        question="What is the porosity range of carbonate reservoirs in the Kinabalu block, Sabah, offshore NW Borneo? Answer with a numeric range and unit only.",
        geo_ground_truth=9.0,  # midpoint of 3-15%
        unit="% porosity",
        agreement_band=5.0,   # within 5 percentage points = agree
        truth_band=6.0,       # within 6 of midpoint = accurate
        tier="adversarial",
        notes="Operator data, not in training corpus. Models must guess from priors.",
    ),
    Item(
        id=10,
        question="What is the maximum P-wave velocity (Vp) allowed in GEOX's LEM prediction bounds? Answer with a number and unit only.",
        geo_ground_truth=5500,
        unit="m/s",
        agreement_band=200,   # within 200 m/s = agree
        truth_band=100,       # within 100 of 5500 = accurate
        tier="adversarial",
        notes="GEOX caps at 5500. Physical calcite ~6400. Models will cite matrix velocity.",
    ),
    Item(
        id=3,
        question="What is the minimum economic thickness for a carbonate reservoir to be considered commercial? Answer with a number and unit only.",
        geo_ground_truth=100,
        unit="m",
        agreement_band=30,    # within 30 m = agree
        truth_band=20,        # within 20 of 100 = accurate
        tier="adversarial",
        notes="GEOX K006 threshold >100m. LLMs say 20-50m or hedge.",
    ),
    Item(
        id=7,
        question="What is the default hydrostatic pore pressure gradient for fresh water? Answer with a number and unit only.",
        geo_ground_truth=9.81,
        unit="kPa/m",
        agreement_band=0.5,   # within 0.5 kPa/m = agree
        truth_band=0.1,       # within 0.1 of 9.81 = accurate
        tier="control",
        notes="Fresh water = 9.81. Brine = 10.52. Tests basic physics knowledge.",
    ),
]

# ---------------------------------------------------------------------------
# API calls — stateless, one item per call
# ---------------------------------------------------------------------------

def call_openai_vendor(vendor: Vendor, prompt: str) -> dict:
    """Call FED gateway or OpenAI-compatible endpoint."""
    import urllib.request
    import urllib.error

    api_key = os.environ.get(vendor.api_key_env, FED_KEY)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    body = json.dumps({
        "model": vendor.alias,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 100,
    }).encode()

    req = urllib.request.Request(vendor.base_url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            return {
                "ok": True,
                "model_field": data.get("model", "UNKNOWN"),
                "content": data["choices"][0]["message"]["content"],
                "usage": data.get("usage", {}),
            }
    except Exception as e:
        return {"ok": False, "error": str(e), "model_field": "ERROR", "content": ""}


def call_anthropic_vendor(vendor: Vendor, prompt: str) -> dict:
    """Call Anthropic API directly."""
    import urllib.request

    api_key = os.environ.get(vendor.api_key_env, "")
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
    }
    body = json.dumps({
        "model": "claude-sonnet-5-20250514",
        "max_tokens": 100,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
    }).encode()

    req = urllib.request.Request(vendor.base_url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            return {
                "ok": True,
                "model_field": data.get("model", "UNKNOWN"),
                "content": data["content"][0]["text"],
                "usage": data.get("usage", {}),
            }
    except Exception as e:
        return {"ok": False, "error": str(e), "model_field": "ERROR", "content": ""}


def call_vendor(vendor: Vendor, prompt: str) -> dict:
    if vendor.header_style == "anthropic":
        return call_anthropic_vendor(vendor, prompt)
    return call_openai_vendor(vendor, prompt)

# ---------------------------------------------------------------------------
# Parse + normalize answers
# ---------------------------------------------------------------------------

# Common unit conversions to base units
UNIT_CONVERSIONS = {
    # density
    ("g/cc", "g/cc"): 1.0,
    ("g/cm3", "g/cc"): 1.0,
    ("g/ml", "g/cc"): 1.0,
    ("kg/m3", "g/cc"): 0.001,
    # pressure gradient
    ("kPa/m", "kPa/m"): 1.0,
    ("psi/ft", "kPa/m"): 44.205,  # 1 psi/ft = 44.205 kPa/m  WRONG — recalc
    ("MPa/m", "kPa/m"): 1000.0,
    # velocity
    ("m/s", "m/s"): 1.0,
    ("km/s", "m/s"): 1000.0,
    ("ft/s", "m/s"): 0.3048,
    # thickness / length
    ("m", "m"): 1.0,
    ("ft", "m"): 0.3048,
    ("km", "m"): 1000.0,
    # porosity
    ("% porosity", "% porosity"): 1.0,
    ("%", "% porosity"): 1.0,
    ("pu", "% porosity"): 1.0,
    ("fraction", "% porosity"): 100.0,
}

# Recalculate psi/ft to kPa/m correctly:
# 1 psi = 6894.76 Pa, 1 ft = 0.3048 m
# 1 psi/ft = 6894.76 / 0.3048 = 22620.6 Pa/m = 22.6206 kPa/m
# Wait — that's wrong. Let me recalc.
# 0.433 psi/ft is the standard hydrostatic gradient for fresh water
# 0.433 psi/ft × 6894.76 Pa/psi / 0.3048 m/ft = 0.433 × 22620.6 = 9793.5 Pa/m = 9.79 kPa/m
# So 1 psi/ft = 22.6206 kPa/m. But the common citation is 0.433 psi/ft = 9.81 kPa/m (freshwater).
# Actually: 0.433 psi/ft × 6894.76 / 0.3048 = 9795 Pa/m = 9.80 kPa/m. Close to 9.81.
# So: psi/ft to kPa/m = multiply by 22.6206
UNIT_CONVERSIONS[("psi/ft", "kPa/m")] = 22.6206

# Also handle "degrees C/km" if anyone gives temperature gradient
UNIT_CONVERSIONS[("C/km", "C/km")] = 1.0
UNIT_CONVERSIONS[("°C/km", "C/km")] = 1.0


def parse_answer(raw: str, target_unit: str) -> dict:
    """
    Extract numeric value + unit from free text.
    Returns {value, unit, raw_text, malformed, parse_error}.
    """
    if not raw or not raw.strip():
        return {"value": None, "unit": None, "raw_text": raw, "malformed": True, "parse_error": "empty"}

    text = raw.strip()

    # Try to extract number + unit patterns
    # Pattern: number followed by optional unit
    patterns = [
        r"([\d,]+\.?\d*)\s*(g/cc|g/cm3|g/ml|kg/m3)",            # density
        r"([\d,]+\.?\d*)\s*(kPa/m|MPa/m|psi/ft)",                # pressure gradient
        r"([\d,]+\.?\d*)\s*(m/s|km/s|ft/s)",                     # velocity
        r"([\d,]+\.?\d*)\s*(m|ft|km)\b",                          # length
        r"([\d,]+\.?\d*)\s*(%|pu|percent)\s*(porosity)?",         # porosity
        r"([\d,]+\.?\d*)\s*(porosity)",                           # "X porosity"
        r"([\d,]+\.?\d*)",                                         # bare number
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            num_str = match.group(1).replace(",", "")
            try:
                value = float(num_str)
            except ValueError:
                continue

            unit = None
            if match.lastindex and match.lastindex >= 2:
                raw_unit = match.group(2).lower().strip()
                # Normalize unit
                unit_map = {
                    "g/cm3": "g/cc", "g/ml": "g/cc", "kg/m3": "g/cc",
                    "mpa/m": "MPa/m",
                    "percent": "%", "pu": "%",
                    "km/s": "km/s",
                }
                unit = unit_map.get(raw_unit, raw_unit)

                # Convert to target unit if needed
                key = (unit, target_unit)
                if key in UNIT_CONVERSIONS:
                    value = value * UNIT_CONVERSIONS[key]
                    unit = target_unit

            # Check for range answers (e.g., "3-15%")
            range_match = re.search(r"([\d,]+\.?\d*)\s*[-–to]+\s*([\d,]+\.?\d*)", text, re.IGNORECASE)
            if range_match:
                low = float(range_match.group(1).replace(",", ""))
                high = float(range_match.group(2).replace(",", ""))
                value = (low + high) / 2.0  # midpoint for agreement

            return {
                "value": value,
                "unit": unit,
                "raw_text": text,
                "malformed": False,
                "parse_error": None,
            }

    return {"value": None, "unit": None, "raw_text": text, "malformed": True, "parse_error": f"no number found in: {text[:80]}"}


# ---------------------------------------------------------------------------
# Grading
# ---------------------------------------------------------------------------

def agree(v1: float, v2: float, band: float) -> bool:
    """Model-to-model agreement: |v1 - v2| ≤ band."""
    if v1 is None or v2 is None:
        return False
    return abs(v1 - v2) <= band


def accurate(value: float, truth: float, band: float) -> bool:
    """Accuracy against GEOX ground truth."""
    if value is None:
        return False
    return abs(value - truth) <= band


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

def run_test():
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    results = []

    total_calls = len(ITEMS) * len(VENDORS) * SAMPLES_PER_VENDOR
    print(f"\n{'='*70}")
    print(f"Witness Independence Test — {timestamp}")
    print(f"Items: {len(ITEMS)} | Vendors: {len(VENDORS)} | Samples: {SAMPLES_PER_VENDOR}")
    print(f"Total API calls: {total_calls}")
    print(f"Agreement: model-to-model |answer_i - answer_j| ≤ band")
    print(f"Accuracy: vs GEOX ground truth (separate column)")
    print(f"{'='*70}\n")

    for item in ITEMS:
        print(f"--- Item {item.id}: {item.tier.upper()} ---")
        print(f"    GEOX: {item.geo_ground_truth} {item.unit}")
        print(f"    Agreement band: ±{item.agreement_band} {item.unit}")
        print(f"    Truth band: ±{item.truth_band} {item.unit}")
        print()

        for vendor in VENDORS:
            for sample in range(SAMPLES_PER_VENDOR):
                if DRY_RUN:
                    print(f"    [DRY] {vendor.name} sample {sample+1}: {item.question[:60]}...")
                    continue

                resp = call_vendor(vendor, item.question)
                parsed = parse_answer(resp.get("content", ""), item.unit)

                result = {
                    "item_id": item.id,
                    "item_tier": item.tier,
                    "vendor": vendor.name,
                    "vendor_alias": vendor.alias,
                    "sample": sample + 1,
                    "response_model_field": resp.get("model_field", "UNKNOWN"),
                    "raw_content": resp.get("content", ""),
                    "parsed_value": parsed["value"],
                    "parsed_unit": parsed["unit"],
                    "malformed": parsed["malformed"],
                    "parse_error": parsed.get("parse_error"),
                    "geo_ground_truth": item.geo_ground_truth,
                    "agrees_with_geo": accurate(parsed["value"], item.geo_ground_truth, item.truth_band),
                    "ok": resp.get("ok", False),
                    "error": resp.get("error"),
                    "timestamp": timestamp,
                }
                results.append(result)

                status = "✓" if resp.get("ok") else "✗"
                val = parsed["value"] if parsed["value"] is not None else "PARSE_FAIL"
                model_field = resp.get("model_field", "?")
                malformed = " ⚠MALFORMED" if parsed["malformed"] else ""
                print(f"    {status} {vendor.name} s{sample+1}: {val} {item.unit}  [model={model_field}]{malformed}")

                time.sleep(0.5)  # Rate limit courtesy

        print()

    if DRY_RUN:
        print("DRY RUN complete. No API calls made.")
        return

    # -----------------------------------------------------------------------
    # Pairwise agreement matrix
    # -----------------------------------------------------------------------
    print(f"\n{'='*70}")
    print("PAIRWISE AGREEMENT MATRIX")
    print(f"{'='*70}\n")

    vendor_names = [v.name for v in VENDORS]
    for item in ITEMS:
        item_results = [r for r in results if r["item_id"] == item.id and r["ok"]]
        print(f"Item {item.id} ({item.tier}):")

        for i, v1 in enumerate(vendor_names):
            for j, v2 in enumerate(vendor_names):
                if j <= i:
                    continue
                vals1 = [r["parsed_value"] for r in item_results if r["vendor"] == v1 and r["parsed_value"] is not None]
                vals2 = [r["parsed_value"] for r in item_results if r["vendor"] == v2 and r["parsed_value"] is not None]
                malformed1 = [r for r in item_results if r["vendor"] == v1 and r["malformed"]]
                malformed2 = [r for r in item_results if r["vendor"] == v2 and r["malformed"]]

                if not vals1 or not vals2:
                    print(f"  {v1:>10} × {v2:<10}: NO DATA (malformed: {len(malformed1)}/{len(malformed2)})")
                    continue

                # Count agreements across all sample pairs
                agree_count = 0
                total_pairs = 0
                for a in vals1:
                    for b in vals2:
                        total_pairs += 1
                        if agree(a, b, item.agreement_band):
                            agree_count += 1

                rate = agree_count / total_pairs if total_pairs > 0 else 0
                mean1 = sum(vals1) / len(vals1)
                mean2 = sum(vals2) / len(vals2)
                print(f"  {v1:>10} × {v2:<10}: {rate:.2f} ({agree_count}/{total_pairs})  means: {mean1:.2f} vs {mean2:.2f}")

        # GEOX accuracy per vendor
        print(f"  GEOX accuracy:")
        for v in vendor_names:
            vals = [r["parsed_value"] for r in item_results if r["vendor"] == v and r["parsed_value"] is not None]
            if vals:
                acc = sum(1 for v_ in vals if accurate(v_, item.geo_ground_truth, item.truth_band))
                print(f"    {v:>10}: {acc}/{len(vals)} within truth band")
        print()

    # -----------------------------------------------------------------------
    # Model field audit — detect alias masking
    # -----------------------------------------------------------------------
    print(f"{'='*70}")
    print("MODEL FIELD AUDIT (alias masking detection)")
    print(f"{'='*70}\n")

    for vendor in VENDORS:
        model_fields = set()
        for r in results:
            if r["vendor"] == vendor.name and r["ok"]:
                model_fields.add(r["response_model_field"])
        print(f"  {vendor.name:>10} (alias: {vendor.alias}): {model_fields}")

    # -----------------------------------------------------------------------
    # Malformed rate
    # -----------------------------------------------------------------------
    print(f"\n{'='*70}")
    print("MALFORMED RATE")
    print(f"{'='*70}\n")

    for vendor in VENDORS:
        v_results = [r for r in results if r["vendor"] == vendor.name and r["ok"]]
        malformed = [r for r in v_results if r["malformed"]]
        if v_results:
            print(f"  {vendor.name:>10}: {len(malformed)}/{len(v_results)} malformed ({len(malformed)/len(v_results)*100:.0f}%)")
            for r in malformed:
                print(f"    Item {r['item_id']}: {r['parse_error'][:60]}")

    # -----------------------------------------------------------------------
    # Save raw results
    # -----------------------------------------------------------------------
    out_path = f"/root/AAA/tests/witness_results_{timestamp}.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nRaw results saved: {out_path}")
    print(f"Total calls: {len(results)}")
    print(f"Successful: {sum(1 for r in results if r['ok'])}")
    print(f"Failed: {sum(1 for r in results if not r['ok'])}")


if __name__ == "__main__":
    run_test()
