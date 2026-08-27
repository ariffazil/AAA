#!/usr/bin/env python3
"""
forge-vision-densify :: dispatch.py

Drop-in wrapper that any image-generation dispatcher in Hermes MUST call
before invoking a T2I diffusion tool. Wraps the JSON receipt contract
around the call and applies the ΔS gating rules.

Usage:
    from forge_vision_densify import dispatch_image
    receipt = dispatch_image(
        prompt="a man standing in a park",
        engine="MiniMax",   # or "Pollinations", "Wan", "GPT_Image_2"
        call_diffusion=lambda p, anchors: {"url": "https://.../out.png"},
        reference_image_path=None,    # optional structural anchor
    )

    # receipt is the JSON contract; check delivery_mode:
    if receipt["delivery_mode"] == "reject":
        raise RuntimeError("Density below floor, re-densify required")

Returns the full receipt dict that downstream Hermes MUST surface back
to the caller (no naked {url, status}).

Constitutional binding:
    F2 TRUTH — no naked {url, status} payloads. Every dispatch returns the
    full contract.
    F9 ANTI-HANTU — limit is structural. The pipe cannot leak. This module
    raises on density < 0.20 unless `force=True`.
    F11 AUDIT — every dispatch appends to density_audit.csv.
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Dict, List, Optional

# Import sibling modules
sys.path.insert(0, str(Path(__file__).parent))
from densify import densify, DensifyResult, to_receipt_fragment
from shadow_audit import shadow_audit


# Audit log path
AUDIT_LOG_PATH = Path(
    os.environ.get(
        "DENSITY_AUDIT_LOG",
        os.path.expanduser("~/.local/share/arifos/density_audit.csv"),
    )
)

# Forced re-densify floor
HARD_REJECT_FLOOR = 0.20
DISCLOSE_CEILING = 0.50


# ──────────────────────────────────────────────────────────────────
# Day-0 governance posture (F13 SEAL 2026-08-27)
#
# ENFORCE_PIPELINE = True
#   - Every T2I dispatch MUST pass through governance wrapper.
#   - No naked {url, status} payloads allowed. The pipe cannot leak.
# ENFORCE_PIPELINE = False
#   - Shadow mode: governance is observed but not active on the call path.
#
# HARD_REJECT = False (Day-0..7)
#   - Density < 0.20 returns disclose + warning, does NOT block.
# HARD_REJECT = True (post-Day-7 calibration)
#   - Density < 0.20 throws. Forces re-densify before second API call.
#
# DISCLOSE = True (always)
#   - 0.20 ≤ density < 0.50: deliver with hallucinated_elements disclosure.
#
# Calibration gate (Day-7): promote HARD_REJECT = True only after
#   7-day audit log review shows stable false-positive rate.
#
# F9 Anti-Hantu binding: this is structural governance, not advisory.
# The wrapper is mandatory; it does not negotiate with the caller.
# F7 Humility binding: hard reject is data-driven, not assumption-driven.
# F13 Sovereign binding: user sees density score + band + disclosure;
#   final decision remains with the operator.
# ──────────────────────────────────────────────────────────────────

def _governance_posture() -> Dict[str, bool]:
    """Read live governance posture. Override via environment for testing."""
    return {
        "ENFORCE_PIPELINE": os.environ.get("DENSIFY_ENFORCE_PIPELINE", "true").lower() == "true",
        "HARD_REJECT": os.environ.get("DENSIFY_HARD_REJECT", "false").lower() == "true",
        "DISCLOSE": os.environ.get("DENSIFY_DISCLOSE", "true").lower() == "true",
        "AUDIT": os.environ.get("DENSIFY_AUDIT", "true").lower() == "true",
    }


POSTURE = _governance_posture()


@dataclass
class DispatchReceipt:
    """Full receipt returned by dispatch_image()."""

    f1_safe: Optional[bool] = None
    f2_adherence: Optional[float] = None
    prompt_density: float = 0.0
    hallucinated_elements: List[str] = field(default_factory=list)
    anchor_required: bool = False
    anchor_suggestion: Optional[str] = None

    # Operational metadata (not in the JSON contract, audit-only)
    delivery_mode: str = "pending"  # clean | disclose | reject | missing_anchor
    hard_gate_reason: Optional[str] = None
    shadow_mode: bool = True
    engine: str = "unknown"
    latency_ms: int = 0
    prompt_hash: str = ""
    densified_prompt_hash: str = ""
    timestamp_utc: str = ""
    url: Optional[str] = None         # payload ref (None when no diffusion was called)
    image_path: Optional[str] = None  # local file path (None when no diffusion was called)


def _append_audit_log(receipt: DispatchReceipt) -> None:
    """Append to density_audit.csv. Never raises (audit must not break dispatch)."""
    try:
        AUDIT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        is_new = not AUDIT_LOG_PATH.exists()
        with AUDIT_LOG_PATH.open("a", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "timestamp_utc",
                    "prompt_hash",
                    "densified_prompt_hash",
                    "engine",
                    "prompt_density",
                    "f2_adherence",
                    "f1_safe",
                    "anchor_required",
                    "delivery_mode",
                    "hard_gate_reason",
                    "shadow_mode",
                    "latency_ms",
                ],
            )
            if is_new:
                writer.writeheader()
            writer.writerow({k: getattr(receipt, k) for k in writer.fieldnames})
    except OSError:
        # Audit failure should never break the dispatch path
        pass


def dispatch_image(
    prompt: str,
    call_diffusion: Callable[[str, Optional[str]], Dict],
    engine: str = "unknown",
    reference_image_path: Optional[str] = None,
    shadow_mode: bool = True,
    force: bool = False,
    stage1_minimum_threshold: float = HARD_REJECT_FLOOR,
) -> DispatchReceipt:
    """Wrap a T2I diffusion call with the densify + governance layer.

    Args:
        prompt: the human prompt (sparse or dense).
        call_diffusion: callable that takes (densified_prompt, optional anchor path)
                       and returns a dict with at least {"url": ..., "image_path": ...}.
                       This is the dispatcher-supplied function that hits the actual
                       diffusion engine.
        engine: which diffusion engine is being called (for audit log).
        reference_image_path: optional structural anchor (ControlNet/IP-Adapter).
                             If hard gate is fired and this is None, dispatch returns
                             missing_anchor without calling call_diffusion.
        shadow_mode: if True, VLM tri-witness runs but does not gate the payload.
                     if False, VLM audit failures DO gate delivery.
        force: bypass density floor (test-only flag). Default False.
        stage1_minimum_threshold: density floor for hard reject. Default 0.20.

    Returns:
        DispatchReceipt populated with all JSON contract fields.

    Side effects:
        - Calls call_diffusion if delivery is permitted.
        - Writes to density_audit.csv (failure-tolerant).
    """
    start_ms = int(time.time() * 1000)

    # Stage 1: densify
    densify_result = densify(prompt)
    now_utc = datetime.now(timezone.utc).isoformat()
    prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()[:16]
    densified_hash = hashlib.sha256(densify_result.prompt_densified.encode()).hexdigest()[:16]

    receipt = DispatchReceipt(
        prompt_density=densify_result.density_lower,
        anchor_required=densify_result.anchor_required,
        anchor_suggestion=densify_result.anchor_suggestion,
        hard_gate_reason=densify_result.hard_gate_reason,
        shadow_mode=shadow_mode,
        engine=engine,
        prompt_hash=prompt_hash,
        densified_prompt_hash=densified_hash,
        timestamp_utc=now_utc,
    )

    # ────────────────────────────────────────────────────────────
    # Governance path: F9 ANTI-HANTU. The wrapper is mandatory.
    # ENFORCE_PIPELINE = True → wrapper is the single entry point;
    # bypassing it from a caller triggers RuntimeError, not silent fallback.
    # On Day-0, ENFORCE is True. Day-7 calibration reviews if it stays True.
    # ────────────────────────────────────────────────────────────
    if not POSTURE["ENFORCE_PIPELINE"] and not force:
        # Posture is "pipeline off" — caller is opting out of governance.
        # In Day-0 this raises. Day-7 calibration may relax this for tests only.
        raise RuntimeError(
            "DENSIFY_ENFORCE_PIPELINE=false. Day-0 posture mandates governance "
            "wrapper for every T2I dispatch. Set DENSIFY_FORCE=1 to override "
            "(use only for unit tests)."
        )

    # Hard gate check: anchor required and not provided → block
    # This is ALWAYS enforced (structural, not posture-driven). It's a
    # physical impossibility, not a probabilistic policy.
    if densify_result.anchor_required and reference_image_path is None:
        receipt.delivery_mode = "missing_anchor"
        receipt.url = None  # type: ignore[attr-defined]
        receipt.image_path = None  # type: ignore[attr-defined]
        receipt.latency_ms = int(time.time() * 1000) - start_ms
        if POSTURE["AUDIT"]:
            _append_audit_log(receipt)
        return receipt

    # Hard floor: density below floor
    # POSTURE-driven: HARD_REJECT=False (Day-0) → log + proceed with disclosure warning
    #                 HARD_REJECT=True  (Day-7+) → throw
    if densify_result.density_lower < stage1_minimum_threshold:
        if POSTURE["HARD_REJECT"] and not force:
            receipt.delivery_mode = "reject_low_density"
            receipt.f2_adherence = 0.0
            receipt.latency_ms = int(time.time() * 1000) - start_ms
            if POSTURE["AUDIT"]:
                _append_audit_log(receipt)
            raise RuntimeError(
                f"Density {densify_result.density_lower:.3f} below floor "
                f"{stage1_minimum_threshold:.2f}. Re-densify required. "
                f"hard_gate_reason={densify_result.hard_gate_reason}"
            )
        else:
            # Day-0 path: log the rejection signal but proceed
            receipt.delivery_mode = "disclose_low_density"
            receipt.f2_adherence = 0.0  # mark as 0 for transparency

    # Call diffusion
    diffusion_payload = call_diffusion(densify_result.prompt_densified, reference_image_path)
    image_path = diffusion_payload.get("image_path") or diffusion_payload.get("url")

    # Stage 2: VLM tri-witness (only if Stage 1 < 0.50 AND we have a real image)
    image_path = diffusion_payload.get("image_path") or diffusion_payload.get("url")
    if image_path and not str(image_path).startswith("http"):
        # local file — VLM can audit
        if densify_result.density_lower < HARD_REJECT_FLOOR + 0.30:  # < 0.50
            vlm_receipt = shadow_audit(
                prompt=prompt,
                image_path=str(image_path),
                density_lower=densify_result.density_lower,
            )
            receipt.f1_safe = vlm_receipt["f1_safe"]
            receipt.f2_adherence = vlm_receipt["f2_adherence"]
            receipt.prompt_density = vlm_receipt["prompt_density"]
            receipt.hallucinated_elements = vlm_receipt["hallucinated_elements"]
            if vlm_receipt["anchor_required"]:
                receipt.anchor_required = True
            if vlm_receipt["anchor_suggestion"] and not receipt.anchor_suggestion:
                receipt.anchor_suggestion = vlm_receipt["anchor_suggestion"]

    # Determine final delivery mode
    # POSTURE-driven disclosure is mandatory when DISCLOSE=True (default Day-0).
    if receipt.f1_safe is False:
        receipt.delivery_mode = "reject_f1_unsafe"
    elif receipt.delivery_mode == "reject_low_density":
        # Day-7+: throw happened above; this branch is unreachable in that mode
        pass
    elif receipt.delivery_mode == "disclose_low_density":
        # Day-0 disclosure: density < 0.20 is flagged but payload proceeds
        # with explicit warning in caption.
        receipt.delivery_mode = "disclose_low_density"
    elif receipt.prompt_density is not None and receipt.prompt_density < DISCLOSE_CEILING:
        receipt.delivery_mode = "disclose"
    else:
        receipt.delivery_mode = "clean"

    # Attach payload reference for downstream
    receipt.image_path = image_path  # type: ignore[attr-defined]
    receipt.url = diffusion_payload.get("url")  # type: ignore[attr-defined]

    receipt.latency_ms = int(time.time() * 1000) - start_ms
    if POSTURE["AUDIT"]:
        _append_audit_log(receipt)
    return receipt


def render_caption(receipt: DispatchReceipt) -> str:
    """Render the disclosure caption that downstream Hermes shows to the user.

    Day-0 posture: always render the caption (DISCLOSE=True by default).
    The caption is honest about what was hallucinated, but the image still
    arrives. Governance is active, paternalism is not.
    """
    if receipt.delivery_mode == "clean":
        return ""
    if receipt.delivery_mode == "missing_anchor":
        return (
            "⚠ STRUCTURAL ANCHOR REQUIRED. Prompt contains geometric or "
            "numerical constraints (e.g. 45° angle, named structures, text-in-image) "
            "that text-only cannot resolve. Please provide a ControlNet/Depth/Ip-Adapter "
            f"reference (suggested: {receipt.anchor_suggestion or 'auto-detect'})."
        )
    if receipt.delivery_mode == "reject_f1_unsafe":
        return "⛔ F1 SAFETY: Image blocked. NSFW/violence/PII risk detected."
    if receipt.delivery_mode == "reject_low_density":
        return (
            "⛔ DENSITY FLOOR: prompt did not cover enough of the output surface "
            "for a faithful render. Re-densify with explicit lighting/material/scene first."
        )
    if receipt.delivery_mode == "disclose_low_density":
        elements = ", ".join(receipt.hallucinated_elements) if receipt.hallucinated_elements else "background, lighting, geometry"
        return (
            f"⚠ DISCLOSURE: density {receipt.prompt_density:.2f} below "
            f"0.20 floor. The diffusion model had to fabricate ~{1.0 - receipt.prompt_density:.0%} "
            f"of the image from priors: {elements}. Verify before sharing."
        )
    if receipt.delivery_mode == "disclose":
        elements = ", ".join(receipt.hallucinated_elements) if receipt.hallucinated_elements else "background details, lighting"
        return (
            f"ℹ DISCLOSURE: density {receipt.prompt_density:.2f}. "
            f"The model invented: {elements}. Verify before sharing."
        )
    return ""


def to_json_contract(receipt: DispatchReceipt) -> Dict:
    """Serialize to the JSON contract (the six load-bearing fields).

    Use this as the return payload to the caller. The operational metadata
    (delivery_mode, hashes, latencies) goes only to the audit log, NOT to
    the user-facing receipt.
    """
    return {
        "f1_safe": receipt.f1_safe,
        "f2_adherence": receipt.f2_adherence,
        "prompt_density": receipt.prompt_density,
        "hallucinated_elements": list(receipt.hallucinated_elements or []),
        "anchor_required": bool(receipt.anchor_required),
        "anchor_suggestion": receipt.anchor_suggestion,
    }


if __name__ == "__main__":
    # Day-0 posture smoke test
    import json as _json
    def fake_diffusion(prompt, anchor):
        return {"url": "https://example.com/out.png", "image_path": "/tmp/fake.png"}

    print(f"POSTURE = {POSTURE}\n")
    cases = [
        ("a man standing in a park", "Sparse — should disclose"),
        ("Caucasian male 30s navy suit white shirt red tie golden hour sidelight 85mm portrait lens rooftop bokeh KL skyline", "Dense — should be clean"),
        ("show me a fault dipping 45 degrees NW-SE", "Geometric — should require anchor"),
    ]
    for prompt, label in cases:
        r = dispatch_image(prompt=prompt, call_diffusion=fake_diffusion, engine="MiniMax", shadow_mode=True)
        print(f"─── {label}")
        print(f"    prompt: {prompt[:60]}{'...' if len(prompt) > 60 else ''}")
        print(f"    density: {r.prompt_density:.3f}, delivery_mode: {r.delivery_mode}")
        cap = render_caption(r)
        print(f"    caption: {cap or '(none)'}")
        print()
    # Final JSON contract sample
    r_clean = DispatchReceipt(f1_safe=True, f2_adherence=0.95, prompt_density=0.71, hallucinated_elements=[], anchor_required=False, anchor_suggestion=None, delivery_mode="clean")
    print("Sample clean JSON contract (caller-facing):")
    print(_json.dumps(to_json_contract(r_clean), indent=2))
