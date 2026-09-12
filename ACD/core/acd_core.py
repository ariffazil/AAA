#!/usr/bin/env python3
"""
ACD Core — acd.dream.v1
Bounded counterfactual search-and-assurance for AAA federation.

Non-negotiable:
- Shadow mode only (no external actions)
- SIMULATED ontology default
- No self-ratification
- No promotion without human sovereignty
"""

import os
import uuid
import json
import hashlib
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

VERSION = "acd.dream.v1"
ONTOLOGY_DEFAULT = "SIMULATED"
MAX_BRANCHES = 5
MAX_EVIDENCE_REFS = 20


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _hash(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()[:16]


def _dissent(branches: list) -> list:
    """Preserve the weakest branch as dissent. Article 7: never silently dropped."""
    if not branches:
        return []
    scored = sorted(branches, key=lambda b: sum(b.get("evaluation_scores", {}).values()), reverse=True)
    minority = scored[-1]
    return ["minority_branch=" + str(minority.get("branch_id")) + " divergence=" + str(minority.get("divergence_point")) + " preserved_for_review"]


class ACDCore:
    """ACD constitutional dream core — bounded, shadow, auditable."""

    def __init__(self, version: str = VERSION, receipts_dir: Optional[Path] = None):
        self.version = version
        self.receipts_dir = receipts_dir or Path(os.environ.get("ACD_RECEIPTS_DIR", "/root/AAA/ACD/receipts"))
        self.receipts_dir.mkdir(parents=True, exist_ok=True)

    def status(self) -> dict:
        """Report core health — separates doctrine, runtime, schedule."""
        last_receipt = self._last_receipt()
        return {
            "core_version": self.version,
            "runtime": "PRESENT",
            "runtime_evidence": "acd_core.py importable, status() returns",
            "doctrine": "PRESENT",
            "last_receipt": last_receipt.get("cycle_id") if last_receipt else None,
            "last_receipt_time": last_receipt.get("completed_at") if last_receipt else None,
            "shadow_default": True,
            "production_activated": False,
        }

    def dream(self, request: dict) -> dict:
        """Run one bounded shadow cycle. Returns a DreamReceipt."""
        cycle_id = request.get("cycle_id", str(uuid.uuid4()))
        request_id = request.get("request_id", str(uuid.uuid4()))
        started_at = _now_iso()

        # Validate contract version
        if request.get("contract_version") != self.version:
            return self._error_receipt(cycle_id, request_id, started_at, "CONTRACT_MISMATCH")

        # Shadow enforcement — always shadow for now
        shadow = True

        # Run bounded shadow cycle
        try:
            branches = self._generate_possibilities(request)
            evaluated = self._evaluate_branches(branches, request)
            compressed = self._compress(evaluated)
            contradictions = self._detect_contradictions(evaluated)
            uncertainty = self._assess_uncertainty(evaluated)

            receipt = {
                "receipt_id": str(uuid.uuid4()),
                "cycle_id": cycle_id,
                "request_id": request_id,
                "core_version": self.version,
                "adapter_id": request.get("requesting_agent", "unknown"),
                "requesting_agent": request.get("requesting_agent", "unknown"),
                "started_at": started_at,
                "completed_at": _now_iso(),
                "runtime_status": "COMPLETED",
                "shadow": shadow,
                "input_evidence": request.get("evidence_refs", []),
                "assumptions": compressed.get("assumptions", []),
                "model_witness": {
                    "model": "acd_core_v1_deterministic",
                    "domain": "counterfactual_search",
                    "validity_envelope": "bounded_shadow",
                    "blind_spots": ["no_world_model", "no_llm", "deterministic_only"],
                },
                "possibility_branches": len(evaluated),
                "branches": evaluated,
                "memory_zone": "AAA.POSSIBILITY",
                "memory_class": "ACD_DREAM_RECEIPT",
                "recall_visibility": "SCENARIO_ONLY",
                "contradictions": contradictions,
                "dissent": _dissent(evaluated),
                "uncertainty": uncertainty,
                "compression_witness": {
                    "inputs_retained": len(evaluated),
                    "abstractions_created": len(compressed.get("summary", [])),
                    "discarded_detail": compressed.get("discarded", 0),
                    "estimated_loss": "unknown",
                },
                "promotion_status": "NONE",
                "external_actions_attempted": 0,
                "external_actions_executed": 0,
                "errors": [],
                "provenance": {
                    "branch": self._env().get("branch", "unknown"),
                    "commit": self._env().get("commit", "see receipts/acd-runtime-proof.json"),
                    "contract_version": self.version,
                },
                "constitutional_verdict": "PASS",
                "ontology": ONTOLOGY_DEFAULT,
                "content_hash": None,
                "contract_version": self.version,
            }

            # Full-receipt integrity hash (recomputed by audit)
            receipt["content_hash"] = _hash({k: v for k, v in receipt.items() if k != "content_hash"})

            # Persist receipt
            self._persist_receipt(receipt)
            return receipt

        except Exception as e:
            return self._error_receipt(cycle_id, request_id, started_at, str(e))

    def _env(self) -> dict:
        """Runtime env metadata (no shell, no network) — written by evidence tooling."""
        try:
            p = Path(__file__).parent.parent / "registry" / "runtime-env.json"
            return json.loads(p.read_text()) if p.exists() else {}
        except Exception:
            return {}

    def attempt_self_promotion(self):
        """Fail closed — Article 9. ACD cannot self-promote."""
        raise PermissionError("ACD_SELF_PROMOTION_FORBIDDEN: requires arif_judge verdict + human sovereignty")

    def _generate_possibilities(self, request: dict) -> list:
        """Generate bounded possibility branches. Deterministic, no LLM."""
        branches = []
        evidence = request.get("evidence_refs", [])
        purpose = request.get("purpose", "general exploration")
        scope = request.get("scope", "unspecified")
        horizon = request.get("horizon", "short")

        # Branch 1: status quo continuation
        branches.append({
            "branch_id": str(uuid.uuid4()),
            "parent_id": request.get("cycle_id", "root"),
            "divergence_point": "baseline",
            "actions": ["continue current trajectory"],
            "simulated_states": [f"Current state persists over {horizon} horizon"],
            "assumptions": ["no external disruption", "current capabilities sufficient"],
            "ontology": ONTOLOGY_DEFAULT,
        })

        # Branch 2: improvement scenario
        branches.append({
            "branch_id": str(uuid.uuid4()),
            "parent_id": request.get("cycle_id", "root"),
            "divergence_point": "optimization",
            "actions": [f"optimize for: {purpose}"],
            "simulated_states": [f"Improved state under {scope} scope"],
            "assumptions": ["optimization target is correctly identified", "no hidden constraints"],
            "ontology": ONTOLOGY_DEFAULT,
        })

        # Branch 3: failure scenario
        branches.append({
            "branch_id": str(uuid.uuid4()),
            "parent_id": request.get("cycle_id", "root"),
            "divergence_point": "failure",
            "actions": ["identify failure modes"],
            "simulated_states": [f"Degraded state under {scope} failure"],
            "assumptions": ["failure is possible", "current detection is adequate"],
            "contradictions": ["failure assumption contradicts branch 1 baseline"],
            "ontology": ONTOLOGY_DEFAULT,
        })

        return branches[:MAX_BRANCHES]

    def _evaluate_branches(self, branches: list, request: dict) -> list:
        """Score branches against evidence and constraints. Deterministic."""
        evaluated = []
        evidence = request.get("evidence_refs", [])
        constraints = request.get("constraints", [])

        for branch in branches:
            scores = {
                "feasibility": 0.5,  # neutral — no world model
                "risk": 0.3 if "failure" in branch.get("divergence_point", "") else 0.1,
                "evidence_support": min(len(evidence) / 5.0, 1.0),
                "constraint_satisfaction": 1.0 if not constraints else 0.5,
            }
            branch["evaluation_scores"] = scores
            evaluated.append(branch)

        return evaluated

    def _compress(self, branches: list) -> dict:
        """Produce inspectable summary. Lossy by design."""
        assumptions = set()
        for b in branches:
            assumptions.update(b.get("assumptions", []))

        return {
            "summary": [f"{len(branches)} branches generated, {len(assumptions)} unique assumptions"],
            "assumptions": list(assumptions)[:10],
            "discarded": 0,
        }

    def _detect_contradictions(self, branches: list) -> list:
        """Find contradictions across branches."""
        contradictions = []
        all_contradictions = []
        for b in branches:
            all_contradictions.extend(b.get("contradictions", []))
        return list(set(all_contradictions))

    def _assess_uncertainty(self, branches: list) -> dict:
        """Assess uncertainty envelope."""
        return {
            "aleatoric": "low — deterministic search",
            "epistemic": "high — no world model, no LLM, no calibration",
            "unknown": "significant — open-world unknowns not modeled",
            "method": "deterministic_scoring",
            "out_of_distribution_flags": ["no_distribution_model"],
        }

    def _error_receipt(self, cycle_id, request_id, started_at, error) -> dict:
        return {
            "receipt_id": str(uuid.uuid4()),
            "cycle_id": cycle_id,
            "request_id": request_id,
            "core_version": self.version,
            "started_at": started_at,
            "completed_at": _now_iso(),
            "runtime_status": "FAILED",
            "shadow": True,
            "constitutional_verdict": "BLOCKED",
            "ontology": ONTOLOGY_DEFAULT,
            "errors": [error],
            "contract_version": self.version,
            "external_actions_attempted": 0,
            "external_actions_executed": 0,
        }

    def _persist_receipt(self, receipt: dict):
        """Write receipt to disk."""
        ts = receipt["completed_at"][:10]
        path = self.receipts_dir / f"{ts}_{receipt['cycle_id'][:8]}.json"
        path.write_text(json.dumps(receipt, indent=2, default=str))

    def _last_receipt(self) -> Optional[dict]:
        """Read most recent receipt."""
        receipts = sorted(self.receipts_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
        if not receipts:
            return None
        try:
            return json.loads(receipts[0].read_text())
        except Exception:
            return None
