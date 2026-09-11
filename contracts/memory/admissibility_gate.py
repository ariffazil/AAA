"""
admissibility_gate.py — Federated Memory Admissibility & Retrieval Gate
Enforces SRO v1 retrieval policy across operational and historical query modes.
Governs arif_memory, Hermes, AGY FI-009, and S4 graph projection.
"""

from __future__ import annotations

import os
import yaml
from datetime import datetime, timezone
from typing import Dict, Any, Tuple, Optional

POLICY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "memory-admissibility-policy.yaml")


class MemoryAdmissibilityGate:
    def __init__(self, policy_path: str = POLICY_FILE):
        self.policy_path = policy_path
        self.policy = self._load_policy()

    def _load_policy(self) -> Dict[str, Any]:
        if os.path.exists(self.policy_path):
            with open(self.policy_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        return {}

    def evaluate(
        self,
        point: Dict[str, Any],
        mode: str = "operational_default",
        current_time: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Evaluate a single memory point against admissibility rules.

        Modes:
          - "operational_default": For agent execution, reasoning, tool selection.
          - "historical_lineage": For audit, forensics, and knowledge evolution.
        """
        now = current_time or datetime.now(timezone.utc)
        payload = point.get("payload", {}) if "payload" in point else point
        point_id = point.get("id", payload.get("memory_id", "unknown"))

        sro = payload.get("sro")
        if not isinstance(sro, dict) or sro.get("sro_version") != 1:
            return {
                "admissible": False,
                "point_id": point_id,
                "code": "EXCLUDED_SCHEMA_INVALID",
                "reason": "Point does not conform to SRO v1 contract (missing sro or sro_version != 1).",
                "mode": mode,
                "effective_status": "UNKNOWN"
            }

        expiry_dict = sro.get("expiry") or {}
        raw_status = expiry_dict.get("status", "ACTIVE")
        expires_at_str = expiry_dict.get("expires_at")
        review_by_str = expiry_dict.get("review_by")

        # Resolve temporal expiry
        effective_status = raw_status
        is_temporally_expired = False
        if expires_at_str:
            try:
                exp_dt = datetime.fromisoformat(expires_at_str.replace("Z", "+00:00"))
                if now > exp_dt:
                    effective_status = "EXPIRED"
                    is_temporally_expired = True
            except Exception:
                pass

        # Resolve supersession
        supersession_dict = sro.get("supersession") or {}
        superseded_by = supersession_dict.get("superseded_by")
        if superseded_by:
            effective_status = "SUPERSEDED"

        # Resolve staleness warning
        warning = None
        if effective_status == "ACTIVE" and review_by_str:
            try:
                rev_dt = datetime.fromisoformat(review_by_str.replace("Z", "+00:00"))
                if now > rev_dt:
                    effective_status = "STALE"
                    warning = "MEMORY_STALE_REVIEW_REQUIRED"
            except Exception:
                pass

        # ── Operational Mode Gate ──
        if mode == "operational_default":
            if effective_status == "EXPIRED":
                return {
                    "admissible": False,
                    "point_id": point_id,
                    "code": "EXCLUDED_EXPIRED",
                    "reason": f"Memory has expired (status={raw_status}, past_date={is_temporally_expired}).",
                    "mode": mode,
                    "effective_status": effective_status
                }

            if effective_status == "SUPERSEDED":
                return {
                    "admissible": False,
                    "point_id": point_id,
                    "code": "EXCLUDED_SUPERSEDED",
                    "reason": f"Memory superseded by successor claim {superseded_by}.",
                    "mode": mode,
                    "effective_status": effective_status,
                    "superseded_by": superseded_by
                }

            # Confidence floor check
            truth_class_data = payload.get("truth_class", {})
            tc = truth_class_data.get("class", "INT") if isinstance(truth_class_data, dict) else str(truth_class_data or "INT")
            confidence = truth_class_data.get("confidence") if isinstance(truth_class_data, dict) else None
            
            floors = {"OBS": 0.90, "DER": 0.75, "INT": 0.65, "SPEC": 0.50}
            floor = floors.get(tc, 0.65)

            if confidence is not None and confidence < floor:
                return {
                    "admissible": False,
                    "point_id": point_id,
                    "code": "EXCLUDED_LOW_CONFIDENCE",
                    "reason": f"Confidence {confidence} below required floor {floor} for truth class {tc}.",
                    "mode": mode,
                    "effective_status": effective_status
                }

            return {
                "admissible": True,
                "point_id": point_id,
                "code": "ADMISSIBLE",
                "reason": "Memory satisfies SRO v1 operational admissibility gate.",
                "mode": mode,
                "effective_status": effective_status,
                "warning": warning
            }

        # ── Historical Mode Gate ──
        elif mode == "historical_lineage":
            return {
                "admissible": True,
                "point_id": point_id,
                "code": "ADMISSIBLE_HISTORICAL",
                "reason": "Admissible under historical audit mode with lineage markers.",
                "mode": mode,
                "effective_status": effective_status,
                "superseded_by": superseded_by,
                "historical_banner": "RETRIEVED_UNDER_HISTORICAL_AUDIT_MODE_NOT_OPERATIONAL_FACT"
            }

        else:
            return {
                "admissible": False,
                "point_id": point_id,
                "code": "INVALID_MODE",
                "reason": f"Unknown query mode '{mode}'.",
                "mode": mode,
                "effective_status": effective_status
            }
