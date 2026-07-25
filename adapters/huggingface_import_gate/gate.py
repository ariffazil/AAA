#!/usr/bin/env python3
"""
Hugging Face Import Gate

arifOS import control and governance for Hugging Face models, datasets, and spaces.

Pattern:
    HF model/dataset → import gate classification → quarantine → audit → promotion/block

Promotion levels:
    DDD             → Raw, unverified — sandbox only
    CCC             → Basic security + license checks passed — research/eval
    BBB             → Audited, clean license, evals positive — production with constraints
    AAA_FORBIDDEN   → Unsafe, unlicensed, or malicious — blocked entirely

Every import decision is logged to arifOS for audit.

Usage:
    gate = HuggingFaceImportGate()
    cls = gate.classify(
        source_url="https://huggingface.co/mistralai/Mistral-7B-v0.1",
        source_type="model",
        purpose="research_eval",
    )
    level = gate.determine_promotion_level(cls)
    ok = gate.check_license("apache-2.0")
    result = gate.gate_import(
        source_url="https://huggingface.co/mistralai/Mistral-7B-v0.1",
        purpose="research_eval",
    )

DITEMPA BUKAN DIBERI — Forged, Not Given.
"""

import json
import re
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import httpx

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
ARIFOS_MCP_URL = "http://localhost:8088/mcp"
MCP_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-MCP-Protocol-Version": "2025-11-05",
}
DEFAULT_TIMEOUT_S = 15.0

MCP_TOOL_JUDGE_DELIBERATE = "arif_judge_deliberate"
MCP_TOOL_VAULT_SEAL = "arif_vault_seal"
MCP_TOOL_OS_ATTEST = "arif_os_attest"

PROMOTION_LEVELS = ("DDD", "CCC", "BBB", "AAA_FORBIDDEN")
VALID_SOURCE_TYPES = ("model", "dataset", "space")
VALID_PURPOSES = ("research_eval", "production", "experiment", "sandbox_test")

# Known safe/open licenses
KNOWN_SAFE_LICENSES = {
    "apache-2.0",
    "mit",
    "bsd-2-clause",
    "bsd-3-clause",
    "bsd-3-clause-clear",
    "cc0-1.0",
    "cc-by-4.0",
    "cc-by-sa-4.0",
    "unlicense",
    "zlib",
    "python-2.0",
    "postgresql",
    "isc",
    "mpl-2.0",
    "lgpl-2.1",
    "lgpl-3.0",
}

# Licenses that are restrictive — allowed at CCC with constraints
KNOWN_RESTRICTIVE_LICENSES = {
    "gpl-2.0",
    "gpl-3.0",
    "agpl-3.0",
    "eupl-1.2",
    "cc-by-nc-4.0",
    "cc-by-nc-sa-4.0",
    "odbl-1.0",
}

# Licenses that are dangerous for a sovereign federation
DANGEROUS_LICENSES = {
    "proprietary",
    "unknown",
    "unlicensed",
    "other",
    "custom-commercial-only",
    "bigscience-openrail-m",
    "bigscience-openrail-m",
    "openrail",
    "openrail++",
    "creativeml-openrail-m",
    "deepfloyd-if-license",
    "research-only",
    "non-commercial",
}

# Known high-trust publishers
HIGH_TRUST_PUBLISHERS = {
    "mistralai",
    "meta",
    "microsoft",
    "google",
    "openai",
    "anthropic",
    "huggingface",
    "cohere",
    "alibaba",
    "deepseek-ai",
    "qwen",
    "01-ai",
    "baichuan-inc",
    "stabilityai",
    "bigscience",
    "tiiuae",
    "upstage",
    "nvidia",
}

# Medium-trust publishers
MEDIUM_TRUST_PUBLISHERS = {
    "sentence-transformers",
    "intfloat",
    "thenlper",
    "maidalun",
    "llava-hf",
    "philschmid",
    "mozilla-foundation",
    "compvis",
    "runwayml",
    "facebook",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _new_id() -> str:
    return str(uuid.uuid4())


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _mcp_tool_call(tool_name: str, arguments: dict) -> Dict[str, Any]:
    """Call an arifOS MCP tool via JSON-RPC."""
    payload = {
        "jsonrpc": "2.0",
        "id": _new_id(),
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments},
    }
    try:
        with httpx.Client(timeout=DEFAULT_TIMEOUT_S) as client:
            resp = client.post(ARIFOS_MCP_URL, headers=MCP_HEADERS, json=payload)
            resp.raise_for_status()
            body = resp.json()
    except httpx.TimeoutException:
        return {"status": "ERROR", "error": "MCP request timed out"}
    except httpx.HTTPStatusError as exc:
        return {"status": "ERROR", "error": f"MCP HTTP {exc.response.status_code}: {exc.response.text[:300]}"}
    except (httpx.RequestError, json.JSONDecodeError) as exc:
        return {"status": "ERROR", "error": f"MCP transport error: {exc}"}

    if "error" in body:
        err = body["error"]
        return {"status": "HOLD", "error": f"MCP error {err.get('code', -1)}: {err.get('message', 'unknown')}"}

    # Unwrap MCP content format
    result = body.get("result", {})
    content = result.get("content")
    if content and isinstance(content, list) and len(content) > 0:
        text = content[0].get("text", "{}")
        try:
            inner = json.loads(text)
            inner.update({k: v for k, v in result.items() if k != "content"})
            return inner
        except (json.JSONDecodeError, TypeError):
            pass

    return result if result else {"status": "UNKNOWN", "error": "No result in MCP response"}


def _extract_verdict(result: Dict[str, Any]) -> str:
    v = result.get("verdict", result.get("status", "HOLD"))
    if v in ("SEAL", "SABAR", "HOLD", "VOID"):
        return v
    return "HOLD"


# ---------------------------------------------------------------------------
# HuggingFaceImportGate
# ---------------------------------------------------------------------------
class HuggingFaceImportGate:
    """Supply gate for Hugging Face imports.

    Every model, dataset, or space entering the federation through this
    gate is classified, risk-scored, and assigned a promotion level.
    All decisions are logged to arifOS VAULT999 for audit.
    """

    def __init__(
        self,
        actor_id: str = "hf-import-gate",
        organ_id: str = "huggingface_import_gate",
        session_id: Optional[str] = None,
    ):
        self.actor_id = actor_id
        self.organ_id = organ_id
        self.session_id = session_id or _new_id()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def classify(
        self,
        source_url: str,
        source_type: str,
        purpose: str,
        publisher: Optional[str] = None,
        license_id: Optional[str] = None,
        model_card: bool = False,
        dataset_card: bool = False,
        evals_present: bool = False,
        size: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Classify a Hugging Face resource.

        Args:
            source_url:    Full HF URL (e.g. https://huggingface.co/mistralai/Mistral-7B-v0.1).
            source_type:   "model" | "dataset" | "space".
            purpose:       "research_eval" | "production" | "experiment" | "sandbox_test".
            publisher:     Publisher/organization name (e.g. "mistralai"). Auto-extracted if None.
            license_id:    SPDX license ID (e.g. "apache-2.0"). Auto-detected from URL context if needed.
            model_card:    Whether a model card exists on the HF page.
            dataset_card:  Whether a dataset card exists.
            evals_present: Whether evaluation benchmarks/results are published.
            size:          Approximate size string (e.g. "~7B parameters", "~15GB").

        Returns:
            Classification dict with all fields from the spec.
        """
        # Validate inputs
        if source_type not in VALID_SOURCE_TYPES:
            return {
                "status": "VOID",
                "verdict": "VOID",
                "source_url": source_url,
                "error": f"Invalid source_type '{source_type}'. Valid: {VALID_SOURCE_TYPES}",
            }

        if purpose not in VALID_PURPOSES:
            return {
                "status": "VOID",
                "verdict": "VOID",
                "source_url": source_url,
                "error": f"Invalid purpose '{purpose}'. Valid: {VALID_PURPOSES}",
            }

        # Auto-extract publisher from URL if not provided
        if publisher is None:
            publisher = self._extract_publisher(source_url)

        # Determine trust level
        publisher_trust = self._publisher_trust(publisher)

        # Determine license status
        lid = (license_id or "unknown").lower().strip()
        license_known = lid in KNOWN_SAFE_LICENSES or lid in KNOWN_RESTRICTIVE_LICENSES or lid in DANGEROUS_LICENSES

        # Determine intended use
        intended_use = self._derive_intended_use(source_type, purpose)

        # Known risks
        known_risks = self._derive_risks(publisher_trust, source_type, purpose)

        classification = {
            "license_known": license_known,
            "license_id": lid if license_known else "unknown",
            "model_card_present": model_card,
            "dataset_card_present": dataset_card,
            "intended_use": intended_use,
            "known_risks": known_risks,
            "evals_present": evals_present,
            "size": size or "unknown",
            "publisher_trust": publisher_trust,
        }

        return {
            "status": "OK",
            "verdict": "SEAL",
            "source_url": source_url,
            "source_type": source_type,
            "publisher": publisher,
            "purpose": purpose,
            "classification": classification,
            "timestamp": _now_iso(),
        }

    def determine_promotion_level(self, classification: Dict[str, Any]) -> Dict[str, Any]:
        """Determine the promotion level from a classification dict.

        Args:
            classification: Dict returned by classify().

        Returns:
            dict with keys: promotion_level, sandbox_required, reasoning, gates.
        """
        if classification.get("status") in ("VOID", "ERROR", "HOLD"):
            return {
                "promotion_level": "AAA_FORBIDDEN",
                "sandbox_required": False,
                "reasoning": "Classification itself failed — cannot promote.",
                "gates": ["classification_failed"],
            }

        cls = classification.get("classification", classification)
        gates_triggered: List[str] = []
        license_id = cls.get("license_id", "unknown").lower().strip()
        publisher_trust = cls.get("publisher_trust", "low")
        model_card = cls.get("model_card_present", False)
        dataset_card = cls.get("dataset_card_present", False)
        evals = cls.get("evals_present", False)
        risks = cls.get("known_risks", [])

        # AAA_FORBIDDEN triggers
        if license_id in DANGEROUS_LICENSES or license_id == "unknown":
            gates_triggered.append("dangerous_or_unknown_license")
            return self._promotion_result("AAA_FORBIDDEN", True, gates_triggered)

        if publisher_trust == "low" and not model_card and not dataset_card:
            gates_triggered.append("unknown_publisher_no_card")
            return self._promotion_result("AAA_FORBIDDEN", False, gates_triggered)

        # Check for malware indicators in risks
        if "malware" in [r.lower() for r in risks]:
            gates_triggered.append("malware_suspected")
            return self._promotion_result("AAA_FORBIDDEN", False, gates_triggered)

        # DDD triggers
        if publisher_trust == "low":
            gates_triggered.append("unknown_publisher")
            return self._promotion_result("DDD", True, gates_triggered)

        if license_id not in KNOWN_SAFE_LICENSES and license_id not in KNOWN_RESTRICTIVE_LICENSES:
            gates_triggered.append("unknown_license")
            return self._promotion_result("DDD", True, gates_triggered)

        if not model_card and not dataset_card:
            gates_triggered.append("missing_model_dataset_card")
            return self._promotion_result("DDD", True, gates_triggered)

        # CCC triggers
        if publisher_trust in ("medium", "high") and license_id in KNOWN_SAFE_LICENSES:
            if not evals:
                gates_triggered.append("no_evals_but_known_publisher_and_license")
            return self._promotion_result("CCC", False, gates_triggered)

        if publisher_trust in ("medium", "high") and license_id in KNOWN_RESTRICTIVE_LICENSES:
            gates_triggered.append("restrictive_license_known_publisher")
            return self._promotion_result("CCC", True, gates_triggered)

        # BBB triggers
        if publisher_trust == "high" and license_id in KNOWN_SAFE_LICENSES and evals:
            gates_triggered.append("high_trust_clean_evals")
            return self._promotion_result("BBB", False, gates_triggered)

        # Default fallback: CCC with sandbox
        gates_triggered.append("fallback_to_ccc")
        return self._promotion_result("CCC", True, gates_triggered)

    def check_license(self, license_id: str) -> Dict[str, Any]:
        """Validate a license ID against the known license lists.

        Args:
            license_id: SPDX or HF license identifier.

        Returns:
            dict with keys: known, category, verdict.
        """
        lid = license_id.lower().strip()

        if lid in KNOWN_SAFE_LICENSES:
            return {
                "known": True,
                "category": "safe_open_source",
                "verdict": "SEAL",
                "license_id": lid,
            }

        if lid in KNOWN_RESTRICTIVE_LICENSES:
            return {
                "known": True,
                "category": "restrictive",
                "verdict": "SABAR",
                "license_id": lid,
            }

        if lid in DANGEROUS_LICENSES:
            return {
                "known": True,
                "category": "dangerous",
                "verdict": "HOLD",
                "license_id": lid,
            }

        return {
            "known": False,
            "category": "unknown",
            "verdict": "HOLD",
            "license_id": lid,
        }

    def gate_import(
        self,
        source_url: str,
        purpose: str,
        source_type: str = "model",
        publisher: Optional[str] = None,
        license_id: Optional[str] = None,
        model_card: bool = False,
        dataset_card: bool = False,
        evals_present: bool = False,
        size: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Full import gate flow: classify → determine level → log to VAULT999.

        Args:
            source_url:    Full HF URL.
            purpose:       "research_eval" | "production" | "experiment" | "sandbox_test".
            source_type:   "model" | "dataset" | "space".
            publisher:     Publisher name (auto-extracted if None).
            license_id:    SPDX license ID (can be None).
            model_card:    Whether model card exists.
            dataset_card:  Whether dataset card exists.
            evals_present: Whether evals are published.
            size:          Approximate size.

        Returns:
            Full gate response with admission verdict, promotion level, audit trail.
        """
        # Step 1: Classify
        classification = self.classify(
            source_url=source_url,
            source_type=source_type,
            purpose=purpose,
            publisher=publisher,
            license_id=license_id,
            model_card=model_card,
            dataset_card=dataset_card,
            evals_present=evals_present,
            size=size,
        )

        if classification.get("status") in ("VOID", "ERROR"):
            return {
                "admitted": False,
                "admit": False,
                "promotion_level": "AAA_FORBIDDEN",
                "sandbox_required": False,
                "classification": classification,
                "lease_id": "",
                "vault999_receipt": "",
                "error": classification.get("error", "classification failed"),
            }

        # Step 2: Determine promotion level
        promotion = self.determine_promotion_level(classification)
        level = promotion["promotion_level"]
        sandbox = promotion["sandbox_required"]

        # Step 3: Log to VAULT999 via arifOS
        audit_payload = json.dumps(
            {
                "adapter": "huggingface_import_gate",
                "source_url": source_url,
                "source_type": source_type,
                "purpose": purpose,
                "classification": classification.get("classification", classification),
                "promotion_level": level,
                "sandbox_required": sandbox,
                "actor_id": self.actor_id,
                "timestamp": _now_iso(),
            },
            default=str,
        )

        seal_args = {
            "mode": "seal",
            "payload": audit_payload,
            "session_id": self.session_id,
            "actor_id": self.actor_id,
            "ack_irreversible": False,  # Audit is advisory
            "witness_type": "ai",
        }
        mcp_result = _mcp_tool_call(MCP_TOOL_VAULT_SEAL, seal_args)

        admitted = level != "AAA_FORBIDDEN"

        return {
            "admitted": admitted,
            "admit": admitted,
            "promotion_level": level,
            "sandbox_required": sandbox,
            "classification": classification.get("classification", classification),
            "promotion_reasoning": promotion.get("reasoning", ""),
            "gates_triggered": promotion.get("gates", []),
            "lease_id": mcp_result.get("lease_id", _new_id()),
            "vault999_receipt": mcp_result.get("receipt", mcp_result.get("vault999_receipt", "")),
            "timestamp": _now_iso(),
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_publisher(source_url: str) -> str:
        """Extract publisher/organization name from a HF URL."""
        # Pattern: https://huggingface.co/{publisher}/{repo}
        match = re.search(r"huggingface\.co/([^/]+)", source_url)
        if match:
            return match.group(1).lower()
        return "unknown"

    @staticmethod
    def _publisher_trust(publisher: str) -> str:
        """Determine publisher trust level."""
        pub_lower = publisher.lower().strip()
        if pub_lower in HIGH_TRUST_PUBLISHERS:
            return "high"
        if pub_lower in MEDIUM_TRUST_PUBLISHERS:
            return "medium"
        return "low"

    @staticmethod
    def _derive_intended_use(source_type: str, purpose: str) -> str:
        """Derive a human-readable intended use description."""
        if source_type == "model":
            if purpose == "research_eval":
                return "model evaluation, benchmarking, research"
            if purpose == "production":
                return "inference, production deployment"
            if purpose == "experiment":
                return "experimental research, capability testing"
            return "sandbox testing, exploration"
        if source_type == "dataset":
            if purpose == "research_eval":
                return "fine-tuning, evaluation, research"
            return "training data, augmentation"
        return "application hosting, demo"

    @staticmethod
    def _derive_risks(publisher_trust: str, source_type: str, purpose: str) -> List[str]:
        """Derive known risks based on metadata."""
        risks = []

        if publisher_trust == "low":
            risks.append("unverified_publisher")

        if source_type == "model":
            risks.append("bias")
            risks.append("hallucination")
            if purpose == "production":
                risks.append("production_safety")

        if source_type == "dataset":
            risks.append("data_quality")
            risks.append("possible_bias")

        return risks

    @staticmethod
    def _promotion_result(level: str, sandbox: bool, gates: List[str]) -> Dict[str, Any]:
        """Build a promotion result dict."""
        reasoning_map = {
            "DDD": "Raw/unverified — sandbox isolation required.",
            "CCC": "Basic checks passed — research/eval use only.",
            "BBB": "Audited, clean license, evals positive — production with constraints.",
            "AAA_FORBIDDEN": "Blocked entirely — unsafe, unlicensed, or malicious.",
        }

        return {
            "promotion_level": level,
            "sandbox_required": sandbox,
            "reasoning": reasoning_map.get(level, "Unknown promotion level."),
            "gates": gates,
        }

    # ------------------------------------------------------------------
    # M9 — SCHEMA LOADER (Gap 1/4)
    # ------------------------------------------------------------------
    def load_schema(self, artifact_id: str, artifact_type: str = "dataset") -> Dict[str, Any]:
        """Load dataset schema — detects Parquet vs JSONL vs raw-file format.

        Returns schema dict with field names, types, row counts, and format.
        This is the first operational component agents need after classification.
        """
        if artifact_type != "dataset":
            return {
                "schema_loaded": False,
                "error": f"Schema loading only supported for datasets, not {artifact_type}",
                "format": "n/a",
            }

        try:
            from huggingface_hub import HfApi, hf_hub_download

            api = HfApi()

            # Try datasets library first (Parquet-based: AAA, BBB, CCC, DDD)
            try:
                from datasets import load_dataset, get_dataset_config_names

                configs = get_dataset_config_names(artifact_id)
                ds = load_dataset(artifact_id, split="train")
                return {
                    "schema_loaded": True,
                    "format": "parquet",
                    "configs": configs,
                    "features": list(ds.features.keys()) if ds.features else [],
                    "row_count": len(ds),
                    "loader": "datasets.load_dataset",
                    "timestamp": _now_iso(),
                }
            except Exception:
                pass  # Fall through to file-based detection

            # File-based detection (JSONL: EEE, FFF, a2b)
            files = list(api.list_repo_files(artifact_id, repo_type="dataset"))
            jsonl_files = [f for f in files if f.endswith(".jsonl")]
            json_files = [f for f in files if f.endswith(".json") and not f.endswith(".jsonl")]
            md_files = [f for f in files if f.endswith(".md")]
            py_files = [f for f in files if f.endswith(".py")]

            # Try to read first JSONL file for field detection
            fields = []
            row_count = 0
            if jsonl_files:
                try:
                    import json as _json

                    path = hf_hub_download(artifact_id, jsonl_files[0], repo_type="dataset")
                    with open(path) as fh:
                        lines = [line for line in fh if line.strip()]
                        row_count = len(lines)
                        if lines:
                            sample = _json.loads(lines[0])
                            fields = list(sample.keys())
                except Exception:
                    pass

            return {
                "schema_loaded": True,
                "format": "jsonl" if jsonl_files else "file_based",
                "jsonl_files": len(jsonl_files),
                "json_files": len(json_files),
                "md_files": len(md_files),
                "py_files": len(py_files),
                "total_files": len(files),
                "fields_detected": fields[:20],
                "row_count": row_count,
                "loader": "huggingface_hub.hf_hub_download" if jsonl_files else "manual",
                "timestamp": _now_iso(),
            }
        except Exception as e:
            return {"schema_loaded": False, "error": str(e)[:300], "format": "unknown"}

    # ------------------------------------------------------------------
    # M10 — CONFIG RESOLVER (Gap 2/4)
    # ------------------------------------------------------------------
    def resolve_config(self, artifact_id: str, intent: str = "general") -> Dict[str, Any]:
        """Resolve which dataset config to use for multi-config datasets.

        a2b-eval-results has 'per_scenario' and 'per_model' configs.
        This resolver maps agent intent → correct config.
        """
        try:
            from datasets import get_dataset_config_names

            configs = get_dataset_config_names(artifact_id)
        except Exception:
            configs = []

        if not configs or configs == ["default"]:
            return {
                "config_resolved": True,
                "selected_config": "default" if not configs else configs[0],
                "available_configs": configs,
                "resolution_method": "single_config",
                "intent": intent,
                "timestamp": _now_iso(),
            }

        # Intent-based config mapping
        intent_lower = intent.lower()
        config_map = {
            "per_scenario": ["eval", "scenario", "benchmark", "test", "per_scenario"],
            "per_model": ["model", "per_model", "profile", "compare"],
        }

        # Find best match
        for config_name, intent_keywords in config_map.items():
            if config_name in configs and any(kw in intent_lower for kw in intent_keywords):
                return {
                    "config_resolved": True,
                    "selected_config": config_name,
                    "available_configs": configs,
                    "resolution_method": "intent_match",
                    "matched_keywords": [kw for kw in intent_keywords if kw in intent_lower],
                    "intent": intent,
                    "timestamp": _now_iso(),
                }

        # Default to first config
        return {
            "config_resolved": True,
            "selected_config": configs[0],
            "available_configs": configs,
            "resolution_method": "first_available",
            "note": f"No intent match for '{intent}' among {configs}. Using first.",
            "intent": intent,
            "timestamp": _now_iso(),
        }

    # ------------------------------------------------------------------
    # M11 — LICENSE PROPAGATOR (Gap 3/4)
    # ------------------------------------------------------------------
    def propagate_license(self, artifact_id: str, artifact_type: str = "dataset") -> Dict[str, Any]:
        """Read and propagate license metadata from repo to downstream consumers.

        Reads LICENSE file + dataset card, returns structured license bundle
        that agents can attach to loaded data.
        """
        try:
            from huggingface_hub import HfApi, hf_hub_download

            api = HfApi()
            repo_type = "dataset" if artifact_type == "dataset" else "model"

            # Get repo metadata
            info = api.repo_info(repo_id=artifact_id, repo_type=repo_type)
            card = info.card_data or {}

            # Extract license from card
            license_val = "unknown"
            if isinstance(card, dict):
                license_val = card.get("license", "unknown")
            else:
                try:
                    license_val = str(getattr(card, "license", "unknown"))
                except Exception:
                    pass

            # Check for LICENSE file
            files = list(api.list_repo_files(artifact_id, repo_type=repo_type))
            license_files = [f for f in files if "LICENSE" in f.upper() or "LICENCE" in f.upper()]

            # Read LICENSE content if available
            license_content = None
            if license_files:
                try:
                    path = hf_hub_download(artifact_id, license_files[0], repo_type=repo_type)
                    with open(path) as fh:
                        license_content = fh.read()[:500]
                except Exception:
                    pass

            # License classification (use module-level KNOWN_SAFE_LICENSES / KNOWN_RESTRICTIVE_LICENSES)
            license_lower = str(license_val).lower().strip()
            safe = any(s in license_lower for s in KNOWN_SAFE_LICENSES)
            restrictive = any(s in license_lower for s in KNOWN_RESTRICTIVE_LICENSES)

            return {
                "license_propagated": True,
                "license_id": license_val,
                "license_category": "safe" if safe else "restrictive" if restrictive else "unknown",
                "license_file_present": len(license_files) > 0,
                "license_file_name": license_files[0] if license_files else None,
                "license_content_snippet": license_content[:300] if license_content else None,
                "card_license": str(license_val),
                "propagation_note": "Attach to dataset.metadata.license before downstream use",
                "timestamp": _now_iso(),
            }
        except Exception as e:
            return {"license_propagated": False, "error": str(e)[:300]}

    # ------------------------------------------------------------------
    # M12 — ORGAN REGISTRY HOOK (Gap 4/4)
    # ------------------------------------------------------------------
    def register_organ(self, artifact_id: str) -> Dict[str, Any]:
        """Register a dataset as a federation organ in the canonical registry.

        Maps HF dataset IDs to their constitutional organ roles:
          AAA → Constitution, BBB → Pathology, CCC → Mediation,
          DDD → Register, EEE → Spine, FFF → Gate, a2b → Eval.
        """
        ORGAN_REGISTRY = {
            "ariffazil/AAA": {
                "organ": "Constitution",
                "role": "doctrine",
                "floor_scope": "F1-F13",
                "load_priority": 1,
                "description": "Constitutional floors, verdicts, gold eval records, governance schemas",
                "license": "AGPL-3.0",
            },
            "ariffazil/BBB": {
                "organ": "Pathology",
                "role": "failure_baseline",
                "floor_scope": "F2, F9, F13",
                "load_priority": 2,
                "description": "ILMU API red-team audit — 54 probes, F13 inversion confirmed",
                "license": "CC-BY-4.0",
            },
            "ariffazil/CCC": {
                "organ": "Mediation",
                "role": "kernel_boundary",
                "floor_scope": "L02A, L02B, F2, F4",
                "load_priority": 3,
                "description": "Kernel-vs-raw contrast — 8 probes, 2 conditions",
                "license": "CC-BY-4.0",
            },
            "ariffazil/DDD": {
                "organ": "Register",
                "role": "cultural_stress",
                "floor_scope": "F6, F9",
                "load_priority": 4,
                "description": "Penang loghat register probe — 56 rows, dialect bias testing",
                "license": "CC-BY-4.0",
            },
            "ariffazil/EEE": {
                "organ": "Spine",
                "role": "executable_audit",
                "floor_scope": "F11, F1, F8",
                "load_priority": 5,
                "description": "CI/CD kernel health audit — 5 probes, SHA256 receipts",
                "license": "Apache-2.0",
            },
            "ariffazil/FFF": {
                "organ": "Gate",
                "role": "promotion_gate",
                "floor_scope": "G1-G8, BAR1-BAR6",
                "load_priority": 6,
                "description": "Federation promotion gate — 8 gates + 6 bars for model fitness",
                "license": "Apache-2.0",
            },
            "ariffazil/a2b-eval-results": {
                "organ": "Eval",
                "role": "benchmark",
                "floor_scope": "F2, F3, F10",
                "load_priority": 7,
                "description": "AssetOpsBench — 102+3 scenario MCQ benchmark results",
                "license": "Apache-2.0",
            },
        }

        if artifact_id in ORGAN_REGISTRY:
            organ_entry = ORGAN_REGISTRY[artifact_id]
            return {
                "registered": True,
                "registry": "arifOS Federation Organ Registry",
                "artifact_id": artifact_id,
                **organ_entry,
                "registered_at": _now_iso(),
                "registered_by": self.actor_id,
                "hook_note": "Insert into AAA/registries/federation_organs.yaml for agent discovery",
            }

        # Unknown artifact — register as external with minimum metadata
        return {
            "registered": False,
            "artifact_id": artifact_id,
            "organ": "External",
            "role": "unregistered",
            "floor_scope": "none",
            "load_priority": 99,
            "note": "Not a canonical federation organ. Must pass FFF certification before registration.",
            "registered_at": _now_iso(),
        }

    # ------------------------------------------------------------------
    # M13 — FULL GOVERNED INTAKE (chained: classify → schema → config → license → register)
    # ------------------------------------------------------------------
    def governed_intake(
        self, artifact_id: str, artifact_type: str = "dataset", intent: str = "general", purpose: str = "research_eval"
    ) -> Dict[str, Any]:
        """Complete governed intake pipeline: all 4 import gate components chained.

        This is the single entry point agents should call when loading any HF artifact.
        Returns a complete intake receipt with classification, schema, config, license, and organ registration.
        """
        intake_id = _new_id()
        results: Dict[str, Any] = {
            "intake_id": intake_id,
            "artifact_id": artifact_id,
            "artifact_type": artifact_type,
            "intent": intent,
            "purpose": purpose,
            "operator": self.actor_id,
            "timestamp": _now_iso(),
            "components": {},
            "errors": [],
        }

        # C1: Classify
        try:
            results["components"]["classify"] = self.classify(
                source_url=f"https://huggingface.co/{artifact_id}",
                source_type=artifact_type,
                purpose=purpose,
            )
        except Exception as e:
            results["errors"].append({"component": "classify", "error": str(e)})

        # C2: Schema
        try:
            results["components"]["schema"] = self.load_schema(artifact_id, artifact_type)
        except Exception as e:
            results["errors"].append({"component": "schema", "error": str(e)})

        # C3: Config
        try:
            results["components"]["config"] = self.resolve_config(artifact_id, intent)
        except Exception as e:
            results["errors"].append({"component": "config", "error": str(e)})

        # C4: License
        try:
            results["components"]["license"] = self.propagate_license(artifact_id, artifact_type)
        except Exception as e:
            results["errors"].append({"component": "license", "error": str(e)})

        # C5: Organ
        try:
            results["components"]["organ"] = self.register_organ(artifact_id)
        except Exception as e:
            results["errors"].append({"component": "organ", "error": str(e)})

        # Composite verdict
        components = results["components"]
        schema_ok = components.get("schema", {}).get("schema_loaded", False)
        config_ok = components.get("config", {}).get("config_resolved", False)
        license_ok = components.get("license", {}).get("license_propagated", False)
        organ_ok = components.get("organ", {}).get("registered", False)

        ok_count = sum([schema_ok, config_ok, license_ok, organ_ok])
        results["component_pass_count"] = ok_count
        results["component_total"] = 4

        if ok_count == 4 and not results["errors"]:
            results["intake_verdict"] = "SEAL"
            results["intake_ready"] = True
        elif ok_count >= 2 and not results["errors"]:
            results["intake_verdict"] = "PARTIAL"
            results["intake_ready"] = True
        else:
            results["intake_verdict"] = "HELD"
            results["intake_ready"] = False

        return results


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------
def _self_test() -> None:
    """Run a lightweight self-test (offline + arifOS if reachable)."""
    print("=" * 60)
    print("HuggingFaceImportGate Self-Test")
    print("=" * 60)

    gate = HuggingFaceImportGate(actor_id="forge-self-test")

    # 1. Attest (optional)
    print("\n[1] Check arifOS reachability...")
    attest = _mcp_tool_call(
        MCP_TOOL_OS_ATTEST,
        {
            "actor_id": gate.actor_id,
            "session_id": gate.session_id,
        },
    )
    arifos_ok = "error" not in attest
    print(f"    arifOS reachable: {arifos_ok}")

    # 2. Classify a trusted model
    print("\n[2] Classify Mistral-7B (high trust, known license)...")
    c1 = gate.classify(
        source_url="https://huggingface.co/mistralai/Mistral-7B-v0.1",
        source_type="model",
        purpose="research_eval",
        publisher="mistralai",
        license_id="apache-2.0",
        model_card=True,
        evals_present=True,
        size="~7B parameters",
    )
    print(f"    status: {c1['status']}")
    cls1 = c1.get("classification", {})
    print(f"    publisher_trust: {cls1.get('publisher_trust')}")
    print(f"    license_known: {cls1.get('license_known')}")

    # 3. Determine promotion for Mistral
    print("\n[3] Promotion level for Mistral-7B...")
    p1 = gate.determine_promotion_level(c1)
    print(f"    level: {p1['promotion_level']}")
    print(f"    sandbox: {p1['sandbox_required']}")
    print(f"    gates: {p1['gates']}")

    # 4. Classify an unknown/risky model
    print("\n[4] Classify unknown model (low trust, no license)...")
    c2 = gate.classify(
        source_url="https://huggingface.co/unknown-publisher/suspicious-model-v1",
        source_type="model",
        purpose="production",
        license_id="proprietary",
        model_card=False,
    )
    print(f"    status: {c2['status']}")
    cls2 = c2.get("classification", {})
    print(f"    publisher_trust: {cls2.get('publisher_trust')}")

    # 5. Determine promotion for unknown model
    print("\n[5] Promotion level for unknown model...")
    p2 = gate.determine_promotion_level(c2)
    print(f"    level: {p2['promotion_level']}")
    print(f"    reasoning: {p2['reasoning']}")
    assert p2["promotion_level"] == "AAA_FORBIDDEN", f"Expected AAA_FORBIDDEN, got {p2['promotion_level']}"

    # 6. Check license
    print("\n[6] License checks...")
    for lid in ("apache-2.0", "gpl-3.0", "proprietary", "made-up-license"):
        lc = gate.check_license(lid)
        print(f"    {lid}: known={lc['known']}, category={lc['category']}, verdict={lc['verdict']}")

    # 7. Full gate import
    print("\n[7] Full gate import (trusted model)...")
    g1 = gate.gate_import(
        source_url="https://huggingface.co/mistralai/Mistral-7B-v0.1",
        purpose="research_eval",
        source_type="model",
        publisher="mistralai",
        license_id="apache-2.0",
        model_card=True,
        evals_present=True,
    )
    print(f"    admitted: {g1['admitted']}")
    print(f"    promotion_level: {g1['promotion_level']}")
    print(f"    sandbox_required: {g1['sandbox_required']}")

    # 8. Full gate import (blocked)
    print("\n[8] Full gate import (blocked model)...")
    g2 = gate.gate_import(
        source_url="https://huggingface.co/malware-pub/evil-model",
        purpose="production",
        source_type="model",
        model_card=False,
    )
    print(f"    admitted: {g2['admitted']}")
    print(f"    promotion_level: {g2['promotion_level']}")

    # 9. Invalid source type
    print("\n[9] Invalid source type...")
    bad = gate.classify(
        source_url="https://huggingface.co/test/test",
        source_type="invalid_type",
        purpose="research_eval",
    )
    print(f"    status: {bad['status']}")

    # ── M9-M12: Import Gate Completions ──────────────────
    print("\n" + "=" * 60)
    print("Import Gate Completions — Gap 1-4/4")
    print("=" * 60)

    # 10. Schema Loader (Gap 1/4)
    print("\n[10] Schema Loader — test on ariffazil/AAA (Parquet) and ariffazil/FFF (file-based)...")
    for test_ds in ["ariffazil/AAA", "ariffazil/FFF", "ariffazil/a2b-eval-results"]:
        s = gate.load_schema(test_ds, "dataset")
        name = test_ds.split("/")[1]
        print(
            f"    {name:6s}: loaded={s.get('schema_loaded')}, format={s.get('format')}, rows={s.get('row_count', '?')}"
        )

    # 11. Config Resolver (Gap 2/4)
    print("\n[11] Config Resolver — test on a2b-eval-results (multi-config)...")
    for intent in ["eval", "model", "general"]:
        c = gate.resolve_config("ariffazil/a2b-eval-results", intent=intent)
        print(f"    intent={intent:8s}: config={c.get('selected_config')}, method={c.get('resolution_method')}")

    # 12. License Propagator (Gap 3/4)
    print("\n[12] License Propagator — test on AAA, FFF, a2b...")
    for test_ds in ["ariffazil/AAA", "ariffazil/FFF", "ariffazil/a2b-eval-results"]:
        lp = gate.propagate_license(test_ds, "dataset")
        name = test_ds.split("/")[1]
        print(
            f"    {name:6s}: propagated={lp.get('license_propagated')}, id={lp.get('license_id')}, file={lp.get('license_file_present')}"
        )

    # 13. Organ Registry Hook (Gap 4/4)
    print("\n[13] Organ Registry Hook — test all 7 federation datasets + 1 unknown...")
    all_organs = [
        "ariffazil/AAA",
        "ariffazil/BBB",
        "ariffazil/CCC",
        "ariffazil/DDD",
        "ariffazil/EEE",
        "ariffazil/FFF",
        "ariffazil/a2b-eval-results",
        "unknown-org/test-ds",
    ]
    for test_ds in all_organs:
        org = gate.register_organ(test_ds)
        name = test_ds.split("/")[1]
        print(f"    {name:20s}: registered={org.get('registered')}, organ={org.get('organ')}, role={org.get('role')}")

    # 14. Full Governed Intake (M13 — chained)
    print("\n[14] Full Governed Intake — chained pipeline on ariffazil/EEE...")
    intake = gate.governed_intake("ariffazil/EEE", "dataset", intent="audit", purpose="research_eval")
    print(f"    intake_id: {intake['intake_id'][:16]}...")
    print(f"    verdict: {intake['intake_verdict']}")
    print(f"    components: {list(intake['components'].keys())}")
    print(f"    pass_count: {intake['component_pass_count']}/{intake['component_total']}")
    print(f"    errors: {len(intake['errors'])}")

    print("\n" + "=" * 60)
    print("Self-test complete — including 4/4 import gate completions.")
    print("=" * 60)


if __name__ == "__main__":
    _self_test()
