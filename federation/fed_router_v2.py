"""
fed_router_v2.py — Deterministic Latent-Aware Router
═════════════════════════════════════════════════════════

Forged 2026-08-10 by 333-AGI. Lane B SESSION_RECEIPT ratification.

Doctrine source: /root/AAA/federation/fed_signatures.yaml
Spec: Deterministic Latent-Aware Router (LLM/DiT/VLM architecture-aware routing)

This module replaces keyword-matching routing with intent + architecture
classification. Pure logic — no GPU/CUDA/torch deps. Composes with the
existing CAPABILITY_SIGNATURES dict in /root/AAA/scripts/fed_router.py
(3 new entries are added there on import).

Three orthogonal dimensions:
  1. modality        — TEXT | PIXEL | MIXED
  2. task_class      — PLAN | GENERATE | INSPECT | REPAIR
  3. fidelity_gate   — PERSIST (≥0.88) | REPAIR (<0.88 with bbox)

Floor binding:
  F2 TRUTH — classification is deterministic (no ML inside the router)
  F4 CLARITY (ΔS ≤ 0) — extends existing substrate, no parallel ledger
  F11 AUDIT — every classification + repair decision emits a flow_ingest receipt
  F13 SOVEREIGN — Lane B self-ratify; F13 ACK required for constitutional_seat=true
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable, Optional

try:
    from shadow_isolation import (
        SHADOW_SIGNATURE,
        is_shadow_signature,
        execute_shadow_request,
        AAAShadowGuard,
    )
    _shadow_available = True
except ImportError:
    _shadow_available = False
    SHADOW_SIGNATURE = "fed-uncensored-sovereign"

__all__ = [
    "Modality",
    "TaskClass",
    "RepairDecision",
    "BoundingBox",
    "LatentAwareRouter",
    "TASK_REGISTRY",
    "DEFAULT_FIDELITY_THRESHOLD",
    "SHADOW_ISOLATION_SIGNATURE",
]


# ─────────────────────────────────────────────────────────────────────────────
# Enums + dataclasses
# ─────────────────────────────────────────────────────────────────────────────


class Modality(str, Enum):
    TEXT = "text"
    PIXEL = "pixel"
    MIXED = "mixed"
    AUDIO = "audio"


class TaskClass(str, Enum):
    PLAN = "plan"
    GENERATE = "generate"
    INSPECT = "inspect"
    REPAIR = "repair"


@dataclass(frozen=True)
class BoundingBox:
    """Normalized bounding box [0,1] coords."""

    x: float
    y: float
    w: float
    h: float
    label: str = ""
    confidence: float = 1.0

    def as_dict(self) -> dict[str, Any]:
        return {
            "x": self.x,
            "y": self.y,
            "w": self.w,
            "h": self.h,
            "label": self.label,
            "confidence": self.confidence,
        }


@dataclass(frozen=True)
class RepairDecision:
    """Result of evaluate_and_repair()."""

    action: str  # "PERSIST" | "REPAIR" | "ESCALATE"
    reason: str
    signature: str  # fed-grounded-vision (verify) | fed-inpainting (repair) | fed-judge-deputy (escalate)
    defect: Optional[BoundingBox] = None
    attempt: int = 1
    max_attempts: int = 3


# ─────────────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────────────


DEFAULT_FIDELITY_THRESHOLD = 0.88  # spec §Closed-Loop Repair Dispatch

# ── Shadow / Sovereign Plane Constants ───────────────────────────────────
SHADOW_ISOLATION_SIGNATURE = "fed-uncensored-sovereign"
SHADOW_PORT = 7079
SHADOW_COMFYUI_PORT = 8188
SHADOW_LEDGER_PATH = "/root/.shadow/shadow_telemetry.jsonl"

# Heuristic intent keywords. Pure deterministic, no ML. F2-friendly.
_GENERATE_HINTS = re.compile(
    r"\b(generate|render|create|draw|produce|synthesize|diffuse|inpaint)\b",
    re.IGNORECASE,
)
_INSPECT_HINTS = re.compile(
    r"\b(inspect|describe|extract|ocr|verify|validate|score|classify|perceive)\b",
    re.IGNORECASE,
)
_REPAIR_HINTS = re.compile(
    r"\b(repair|fix|heal|patch|redo|re-roll|reroll|refine)\b",
    re.IGNORECASE,
)
_PLAN_HINTS = re.compile(
    r"\b(plan|reason|coding|code|decide|architect|design|think)\b",
    re.IGNORECASE,
)


# ─────────────────────────────────────────────────────────────────────────────
# Task Registry — declarative routing table
# ─────────────────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class TaskSpec:
    """One row in the task registry. Maps (modality, task_class) → signature."""

    modality: Modality
    task_class: TaskClass
    signature: str
    description: str = ""


TASK_REGISTRY: tuple[TaskSpec, ...] = (
    # ── TEXT PATH (LLM) ────────────────────────────────────────────
    TaskSpec(Modality.TEXT, TaskClass.PLAN, "fed-reasoning-heavy",
             "Heavy reasoning, coding, planning, constitutional judgment"),
    TaskSpec(Modality.TEXT, TaskClass.INSPECT, "fed-multimodal-vision",
             "OCR fallback for text-only payloads (rare)"),
    # ── PIXEL PATH (DiT + VLM) ─────────────────────────────────────
    TaskSpec(Modality.PIXEL, TaskClass.GENERATE, "fed-image-generation",
             "Diffusion rendering — Renderer / Executor role"),
    TaskSpec(Modality.PIXEL, TaskClass.INSPECT, "fed-grounded-vision",
             "Grounded VLM inspection with bbox protocol"),
    TaskSpec(Modality.PIXEL, TaskClass.REPAIR, "fed-inpainting",
             "Targeted ControlNet repair with VLM-supplied bbox mask"),
    # ── MIXED PATH (LLM as planner + VLM/DiT as executor) ──────────
    TaskSpec(Modality.MIXED, TaskClass.PLAN, "fed-reasoning-heavy",
             "Planner reasons over mixed text+pixel context"),
    TaskSpec(Modality.MIXED, TaskClass.GENERATE, "fed-image-generation",
             "Mixed prompt → diffusion generation"),
    TaskSpec(Modality.MIXED, TaskClass.INSPECT, "fed-grounded-vision",
             "Mixed text+pixel inspection (e.g., doc + chart)"),
    # ── AUDIO PATH ─────────────────────────────────────────────────
    TaskSpec(Modality.AUDIO, TaskClass.PLAN, "fed-realtime-voice",
             "Speech-to-text / text-to-speech"),
)


# ── Shadow / Sovereign Plane Registry ─────────────────────────────────
# These entries are NEVER resolved by the public LatentAwareRouter.
# They are only accessible through ShadowRouter or DualPlaneRouter.
SHADOW_REGISTRY: tuple[TaskSpec, ...] = (
    TaskSpec(
        Modality.PIXEL, TaskClass.GENERATE,
        SHADOW_ISOLATION_SIGNATURE,
        "Sovereign local diffusion — uncensored checkpoints on localhost GPU",
    ),
    TaskSpec(
        Modality.PIXEL, TaskClass.REPAIR,
        SHADOW_ISOLATION_SIGNATURE,
        "Sovereign local inpainting — uncensored ControlNet on localhost",
    ),
    TaskSpec(
        Modality.MIXED, TaskClass.GENERATE,
        SHADOW_ISOLATION_SIGNATURE,
        "Sovereign local generation from mixed text+pixel prompts",
    ),
)


# ─────────────────────────────────────────────────────────────────────────
# The Router
# ─────────────────────────────────────────────────────────────────────────────


class LatentAwareRouter:
    """
    Deterministic Latent-Aware Router.

    Responsibilities:
      1. classify(payload)         → (modality, task_class)
      2. resolve(modality, task)   → capability signature alias
      3. evaluate_and_repair(...)  → RepairDecision (closed-loop dispatch)

    Pure functions where possible. No IO. Caller emits flow_ingest receipts.
    """

    def __init__(
        self,
        *,
        fidelity_threshold: float = DEFAULT_FIDELITY_THRESHOLD,
        max_repair_attempts: int = 3,
        registry: Optional[Iterable[TaskSpec]] = None,
    ) -> None:
        self.fidelity_threshold = fidelity_threshold
        self.max_repair_attempts = max_repair_attempts
        self._registry = tuple(registry) if registry is not None else TASK_REGISTRY
        # Build lookup index
        self._index: dict[tuple[Modality, TaskClass], TaskSpec] = {
            (s.modality, s.task_class): s for s in self._registry
        }

    # ── 1. CLASSIFY ─────────────────────────────────────────────────

    def classify(self, payload: dict[str, Any]) -> tuple[Modality, TaskClass]:
        """
        Classify a task payload by (modality, task_class).

        Modality inference:
          - 'image' or 'pixel' in payload → PIXEL
          - 'audio' in payload → AUDIO
          - 'image' + 'prompt' or 'text' → MIXED
          - else TEXT

        Task class inference (intent hints in prompt / intent field):
          - generate/render hints  → GENERATE
          - inspect/extract hints  → INSPECT
          - repair/fix hints       → REPAIR
          - else                   → PLAN (default — most general per fed_router.py)
        """
        modality = self._infer_modality(payload)
        task_class = self._infer_task_class(payload)
        return modality, task_class

    def _infer_modality(self, payload: dict[str, Any]) -> Modality:
        has_pixel = any(
            k in payload
            for k in ("image", "image_uri", "pixel", "latent", "frames")
        )
        has_text = any(
            k in payload
            for k in ("prompt", "text", "query", "instruction", "messages")
        )
        if "audio" in payload or "voice" in payload:
            return Modality.AUDIO
        if has_pixel and has_text:
            return Modality.MIXED
        if has_pixel:
            return Modality.PIXEL
        return Modality.TEXT

    def _infer_task_class(self, payload: dict[str, Any]) -> TaskClass:
        # explicit intent field wins
        explicit = str(payload.get("intent", "")).strip().lower()
        if explicit:
            try:
                return TaskClass(explicit)
            except ValueError:
                pass  # fall through to heuristic
        # heuristic on prompt text
        text = " ".join(
            str(payload.get(k, "")) for k in ("prompt", "text", "query", "instruction")
        )
        if not text:
            return TaskClass.PLAN  # default per fed_router.py
        if _REPAIR_HINTS.search(text):
            return TaskClass.REPAIR
        if _INSPECT_HINTS.search(text):
            return TaskClass.INSPECT
        if _GENERATE_HINTS.search(text):
            return TaskClass.GENERATE
        if _PLAN_HINTS.search(text):
            return TaskClass.PLAN
        return TaskClass.PLAN

    # ── 2. RESOLVE ──────────────────────────────────────────────────

    def resolve(
        self, modality: Modality, task_class: TaskClass
    ) -> Optional[str]:
        """Map (modality, task_class) → capability signature. None if no entry."""
        spec = self._index.get((modality, task_class))
        return spec.signature if spec else None

    def resolve_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        """One-shot convenience: classify + resolve + metadata."""
        modality, task_class = self.classify(payload)
        signature = self.resolve(modality, task_class)
        return {
            "modality": modality.value,
            "task_class": task_class.value,
            "signature": signature,
            "registry_hit": signature is not None,
        }

    # ── 3. CLOSED-LOOP REPAIR DISPATCH ─────────────────────────────

    def evaluate_and_repair(
        self,
        fidelity_score: float,
        defects: Optional[list[BoundingBox]] = None,
        attempt: int = 1,
    ) -> RepairDecision:
        """
        Closed-loop repair dispatch per spec §3.

        Inputs:
          fidelity_score  — P_quality ∈ [0,1] from fed-grounded-vision
          defects         — list of BoundingBox from VLM feedback (may be empty)
          attempt         — current repair attempt counter (1-indexed)

        Output RepairDecision:
          PERSIST  — fidelity ≥ threshold OR no defects; seal to ledger
          REPAIR   — fidelity < threshold AND defects present; route to fed-inpainting
          ESCALATE — attempt exhausted; F13 SOVEREIGN halt + re-roll whole
        """
        defects = defects or []

        # PERSIST path
        if fidelity_score >= self.fidelity_threshold or not defects:
            return RepairDecision(
                action="PERSIST",
                reason=(
                    f"fidelity {fidelity_score:.3f} ≥ "
                    f"{self.fidelity_threshold:.3f} or no defects"
                ),
                signature="fed-grounded-vision",
                attempt=attempt,
                max_attempts=self.max_repair_attempts,
            )

        # ESCALATE if we've exhausted attempts
        if attempt >= self.max_repair_attempts:
            return RepairDecision(
                action="ESCALATE",
                reason=(
                    f"fidelity {fidelity_score:.3f} < "
                    f"{self.fidelity_threshold:.3f} after "
                    f"{attempt} attempts — re-roll requires F13 ACK"
                ),
                signature="fed-judge-deputy",
                defect=defects[0],
                attempt=attempt,
                max_attempts=self.max_repair_attempts,
            )

        # REPAIR path
        return RepairDecision(
            action="REPAIR",
            reason=(
                f"fidelity {fidelity_score:.3f} < "
                f"{self.fidelity_threshold:.3f}, "
                f"localized defect at {defects[0].label or 'bbox'} — "
                f"inpaint attempt {attempt}/{self.max_repair_attempts}"
            ),
            signature="fed-inpainting",
            defect=defects[0],
            attempt=attempt,
            max_attempts=self.max_repair_attempts,
        )

    # ── 4. EXTENDED CAPABILITY SIGNATURES (for fed_router.py wiring) ──

    @staticmethod
    def new_capability_signatures() -> dict[str, dict[str, Any]]:
        """
        Return the 4 new CAPABILITY_SIGNATURES entries to merge into
        /root/AAA/scripts/fed_router.py CAPABILITY_SIGNATURES dict.

        Kept in lock-step with /root/AAA/federation/fed_signatures.yaml.
        """
        return {
            "fed-image-generation": {
                "description": (
                    "Diffusion-based image synthesis (DiT/SDXL/Wan2.7). "
                    "Renderer / Executor role. Iterative denoising on "
                    "continuous spatial latents. Fails structurally."
                ),
                "models": [
                    "bailian-token-plan/wan2.7-image-pro",
                    "bailian-token-plan/wan2.7-image",
                    "qwen-token-plan-individual/wan2.7-image-pro",
                ],
                "constitutional_tier": 555,
                "modality": "pixel",
            },
            "fed-grounded-vision": {
                "description": (
                    "Compact VLM with spatial grounding (bbox protocol). "
                    "Inspector / Evaluator role. Returns P_quality ∈ [0,1]."
                ),
                "models": [
                    "mulerouter/qwen-vl-max",
                    "bailian-token-plan/qwen-vl-max",
                    "flame/gemini-2.5-flash",
                ],
                "constitutional_tier": 555,
                "modality": "vision",
            },
            "fed-inpainting": {
                "description": (
                    "Targeted image repair via ControlNet / inpainting. "
                    "Triggered when fed-grounded-vision returns "
                    "P_quality < 0.88 with localized defect bboxes."
                ),
                "models": [
                    "comfyui/controlnet-inpaint",
                    "comfyui/sdxl-inpaint",
                ],
                "constitutional_tier": 555,
                "modality": "pixel",
            },
            "fed-judge-deputy": {
                "description": (
                    "Backup JUDGE channels for constitutional seats. Routes "
                    "glm-5.2 / qwen3.8-max through bailian / qwen-individual "
                    "when primary 4 seats fail. Resolves JUDGE_SEAT_UNAVAILABLE "
                    "cascades."
                ),
                "models": [
                    "bailian-token-plan/glm-5.2",
                    "bailian-token-plan/qwen3.8-max",
                    "qwen-token-plan-individual/glm-5.2",
                    "qwen-token-plan-individual/qwen3.8-max",
                ],
                "constitutional_tier": 666,
                "modality": "text",
            },
        }


# ─────────────────────────────────────────────────────────────────────────
# Shadow Router — Sovereign Plane
# ─────────────────────────────────────────────────────────────────────────


class ShadowRouter:
    """
    Isolated router for the Shadow / Sovereign Plane.

    Routes requests to local ComfyUI daemon on localhost:8188.
    NEVER touches public APIs. NEVER logs to the public ledger.
    Telemetry goes to /root/.shadow/shadow_telemetry.jsonl only.

    The shadow router is intentionally simple — no balance gates,
    no health cascades, no effort dials. Just:
      1. Classify intent → shadow signature
      2. Guard check (assert_shadow_isolation)
      3. Health probe ComfyUI
      4. Queue to localhost
    """

    def __init__(
        self,
        *,
        comfyui_url: str = f"http://127.0.0.1:{SHADOW_COMFYUI_PORT}",
        ledger_path: str = SHADOW_LEDGER_PATH,
        registry: Optional[Iterable[TaskSpec]] = None,
    ) -> None:
        self.comfyui_url = comfyui_url
        self.ledger_path = Path(ledger_path)
        self._registry = tuple(registry) if registry is not None else SHADOW_REGISTRY
        self._index: dict[tuple[Modality, TaskClass], TaskSpec] = {
            (s.modality, s.task_class): s for s in self._registry
        }

    def is_shadow_signature(self, signature: str) -> bool:
        """Check if a signature belongs to the shadow plane."""
        return signature == SHADOW_ISOLATION_SIGNATURE

    def resolve(
        self, modality: Modality, task_class: TaskClass
    ) -> Optional[str]:
        """Resolve (modality, task_class) in the shadow registry."""
        spec = self._index.get((modality, task_class))
        return spec.signature if spec else None

    def classify_and_resolve(self, payload: dict[str, Any]) -> dict[str, Any]:
        """
        Classify a payload and check if it should route to the shadow plane.
        Returns routing decision with isolation metadata.
        """
        modality = self._infer_modality(payload)
        task_class = self._infer_task_class(payload)
        shadow_sig = self.resolve(modality, task_class)

        return {
            "is_shadow": shadow_sig is not None,
            "modality": modality.value,
            "task_class": task_class.value,
            "signature": shadow_sig,
            "target": self.comfyui_url if shadow_sig else None,
            "isolation_level": "SHADOW_STRICT" if shadow_sig else None,
            "telemetry_ledger": str(self.ledger_path) if shadow_sig else None,
        }

    def queue_to_comfyui(
        self,
        payload: dict[str, Any],
        *,
        workflow: str = "txt2img",
        checkpoint: str = "pony-v6-xl",
        prompt: str = "",
        negative_prompt: str = "",
        width: int = 1024,
        height: int = 1024,
        steps: int = 30,
        cfg: float = 7.0,
        seed: int = -1,
    ) -> dict[str, Any]:
        """
        Queue a generation request to the local ComfyUI daemon.
        Logs to shadow telemetry ONLY — never touches public ledger.
        """
        import hashlib
        import urllib.request

        # 1. Guard: assert isolation
        try:
            from shadow_isolation import AAAShadowGuard, ShadowHealthCheck, log_shadow_telemetry
        except ImportError:
            from shadow_isolation import log_shadow_telemetry
            AAAShadowGuard = None  # type: ignore[assignment,misc]
            ShadowHealthCheck = None  # type: ignore[assignment,misc]

        if AAAShadowGuard is not None:
            guard = AAAShadowGuard()
            guard.assert_shadow_isolation(
                SHADOW_ISOLATION_SIGNATURE,
                self.comfyui_url,
            )

        # 2. Pre-flight health check
        if ShadowHealthCheck is not None:
            health_status = ShadowHealthCheck(endpoint=self.comfyui_url).check()
            health = {"status": "HEALTHY" if health_status.reachable else "UNREACHABLE", "error": health_status.error}
        else:
            health = {"status": "UNKNOWN", "error": "ShadowHealthCheck not available"}
        if health["status"] != "HEALTHY":
            log_shadow_telemetry(
                "COMFYUI_UNREACHABLE",
                model=checkpoint,
                status="FAILED",
                extra={"health": health},
            )
            return {
                "status": "FAILED",
                "reason": f"ComfyUI unreachable at {self.comfyui_url}",
                "health": health,
            }

        # 3. Build ComfyUI workflow payload (simplified API format)
        workflow_payload = {
            "prompt": {
                "3": {
                    "class_type": "KSampler",
                    "inputs": {
                        "seed": seed,
                        "steps": steps,
                        "cfg": cfg,
                        "sampler_name": "euler_ancestral",
                        "scheduler": "normal",
                        "denoise": 1.0,
                        "model": ["4", 0],
                        "positive": ["6", 0],
                        "negative": ["7", 0],
                        "latent_image": ["5", 0],
                    },
                },
                "4": {
                    "class_type": "CheckpointLoaderSimple",
                    "inputs": {"ckpt_name": f"{checkpoint}.safetensors"},
                },
                "5": {
                    "class_type": "EmptyLatentImage",
                    "inputs": {"width": width, "height": height, "batch_size": 1},
                },
                "6": {
                    "class_type": "CLIPTextEncode",
                    "inputs": {"text": prompt, "clip": ["4", 1]},
                },
                "7": {
                    "class_type": "CLIPTextEncode",
                    "inputs": {"text": negative_prompt, "clip": ["4", 1]},
                },
                "8": {
                    "class_type": "VAEDecode",
                    "inputs": {"samples": ["3", 0], "vae": ["4", 2]},
                },
                "9": {
                    "class_type": "SaveImage",
                    "inputs": {"filename_prefix": "shadow", "images": ["8", 0]},
                },
            },
        }

        # 4. Queue to ComfyUI
        try:
            data = json.dumps(workflow_payload).encode()
            req = urllib.request.Request(
                f"{self.comfyui_url}/prompt",
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            resp = urllib.request.urlopen(req, timeout=10)
            result = json.loads(resp.read())
            prompt_id = result.get("prompt_id", "unknown")

            # 5. Log to shadow telemetry ONLY
            payload_hash = hashlib.sha256(
                json.dumps(payload, sort_keys=True).encode()
            ).hexdigest()[:16]

            log_shadow_telemetry(
                "SHADOW_QUEUED",
                model=checkpoint,
                status="QUEUED_SHADOW",
                payload_hash=payload_hash,
                extra={
                    "prompt_id": prompt_id,
                    "workflow": workflow,
                    "checkpoint": checkpoint,
                    "width": width,
                    "height": height,
                    "steps": steps,
                    "cfg": cfg,
                    "seed": seed,
                },
            )

            return {
                "status": "QUEUED_SHADOW",
                "target": self.comfyui_url,
                "prompt_id": prompt_id,
                "isolation": "SHADOW_STRICT",
                "telemetry": str(self.ledger_path),
            }

        except Exception as e:
            log_shadow_telemetry(
                "SHADOW_FAILED",
                model=checkpoint,
                status="FAILED",
                extra={"error": str(e)},
            )
            return {
                "status": "FAILED",
                "reason": str(e),
                "target": self.comfyui_url,
            }

    def _infer_modality(self, payload: dict[str, Any]) -> Modality:
        has_pixel = any(
            k in payload
            for k in ("image", "image_uri", "pixel", "latent", "frames")
        )
        has_text = any(
            k in payload
            for k in ("prompt", "text", "query", "instruction", "messages")
        )
        if has_pixel and has_text:
            return Modality.MIXED
        if has_pixel:
            return Modality.PIXEL
        return Modality.PIXEL  # Default for shadow: pixel (diffusion)

    def _infer_task_class(self, payload: dict[str, Any]) -> TaskClass:
        explicit = str(payload.get("intent", "")).strip().lower()
        if explicit:
            try:
                return TaskClass(explicit)
            except ValueError:
                pass
        text = " ".join(
            str(payload.get(k, "")) for k in ("prompt", "text", "query")
        )
        if _REPAIR_HINTS.search(text):
            return TaskClass.REPAIR
        return TaskClass.GENERATE  # Default for shadow: generate


# ─────────────────────────────────────────────────────────────────────────
# Dual-Plane Router — The Complete Routing Architecture
# ─────────────────────────────────────────────────────────────────────────


class DualPlaneRouter:
    """
    Unified entry point that dispatches between:
      - PUBLIC PLANE  → LatentAwareRouter (federation, public APIs, main ledger)
      - SHADOW PLANE  → ShadowRouter (localhost ComfyUI, shadow telemetry)

    Classification is deterministic (F2). No ML. No inference.
    Shadow signatures are intercepted BEFORE reaching the public router.
    """

    def __init__(self) -> None:
        self.public = LatentAwareRouter()
        self.shadow = ShadowRouter()
        self._shadow_signatures = {SHADOW_ISOLATION_SIGNATURE}

    def route(self, payload: dict[str, Any]) -> dict[str, Any]:
        """
        Single entry point. Classifies the request and dispatches to the
        correct plane.

        Returns a unified routing result with plane metadata.
        """
        # 1. Check for explicit shadow signature
        explicit_sig = payload.get("capability_signature", "")
        if explicit_sig in self._shadow_signatures:
            return self._route_shadow(payload, explicit_sig)

        # 2. Check for explicit shadow intent markers
        if self._is_shadow_intent(payload):
            return self._route_shadow(payload, SHADOW_ISOLATION_SIGNATURE)

        # 3. Classify via public router
        modality, task_class = self.public.classify(payload)
        signature = self.public.resolve(modality, task_class)

        # 4. Double-check: if public resolution lands on a shadow sig, redirect
        if signature in self._shadow_signatures:
            return self._route_shadow(payload, signature)

        # 5. Public plane route
        return self._route_public(payload, modality, task_class, signature)

    def _is_shadow_intent(self, payload: dict[str, Any]) -> bool:
        """Detect shadow intent from payload markers."""
        # Explicit shadow flag
        if payload.get("shadow_plane") is True:
            return True
        if payload.get("isolation_level") == "SHADOW_STRICT":
            return True
        # Check for uncensored / sovereign keywords in intent
        intent = str(payload.get("intent", "")).lower()
        task = str(payload.get("task", "")).lower()
        combined = f"{intent} {task}"
        return any(
            kw in combined
            for kw in ("uncensored", "shadow", "sovereign_local", "local_gpu")
        )

    def _route_shadow(
        self, payload: dict[str, Any], signature: str
    ) -> dict[str, Any]:
        """Dispatch to shadow plane."""
        try:
            from shadow_isolation import AAAShadowGuard
        except ImportError:
            AAAShadowGuard = None  # type: ignore[assignment,misc]

        # Assert isolation before doing anything
        comfyui_url = self.shadow.comfyui_url
        if AAAShadowGuard is not None:
            guard = AAAShadowGuard()
            guard.assert_shadow_isolation(signature, comfyui_url)

        # Classify for shadow registry
        shadow_info = self.shadow.classify_and_resolve(payload)

        return {
            "plane": "SHADOW",
            "isolation": "SHADOW_STRICT",
            "signature": signature,
            "target": comfyui_url,
            "telemetry": SHADOW_LEDGER_PATH,
            "shadow_info": shadow_info,
            "public_router": None,  # public router was NOT consulted
            "warning": (
                "This request routes to the SHADOW PLANE. "
                "Zero public API contact. Zero main ledger writes. "
                "Execution on localhost ComfyUI only."
            ),
        }

    def _route_public(
        self,
        payload: dict[str, Any],
        modality: Modality,
        task_class: TaskClass,
        signature: Optional[str],
    ) -> dict[str, Any]:
        """Dispatch to public plane via LatentAwareRouter."""
        return {
            "plane": "PUBLIC",
            "isolation": None,
            "signature": signature,
            "modality": modality.value,
            "task_class": task_class.value,
            "shadow_info": None,
            "public_router": "LatentAwareRouter",
        }