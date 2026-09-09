#!/usr/bin/env python3
"""
Trauma Theorem — Scar-Weight Middleware Parser v1.0.0

Loads the scar-weight registry, scans input text for entity aliases,
and injects the corresponding response_modifier into agent context.

Usage:
  # As pre-processor (pipe input)
  echo "Tengku Taufik announced layoffs" | python3 trauma-theorem-parser.py

  # As importable module
  from trauma_theorem_parser import TraumaParser
  parser = TraumaParser()
  result = parser.metabolize("Tengku Taufik announced layoffs")
  print(result["modifiers"])  # [response_modifier strings]
  print(result["entities"])   # [{entity, w_scar, archetype, breaches}]
"""

import json
import re
import sys
from pathlib import Path
from typing import Optional

REGISTRY_PATH = Path("/root/AAA/scar-weight-registry.json")


class TraumaParser:
    def __init__(self, registry_path: Optional[Path] = None):
        self.registry_path = registry_path or REGISTRY_PATH
        self._registry = None
        self._alias_map = {}  # lowercase_alias -> entity_index

    def _load_registry(self):
        if self._registry is None:
            with open(self.registry_path) as f:
                self._registry = json.load(f)
            self._build_alias_map()
        return self._registry

    def _build_alias_map(self):
        """Build lowercase alias -> entity index mapping for O(1) lookup."""
        assert self._registry is not None
        for idx, entity in enumerate(self._registry["entities"]):
            for alias in entity.get("aliases", []):
                self._alias_map[alias.lower()] = idx

    def validate_registry(self) -> dict:
        """Validate all entities against the schema contract. Returns validation report."""
        registry = self._load_registry()
        contract = registry.get("schema_contract", {}).get("fields", {})
        results = {"valid": True, "entities": [], "errors": []}

        for idx, entity in enumerate(registry["entities"]):
            entity_result = {"index": idx, "entity": entity.get("entity", "?"), "valid": True, "missing": []}

            for field_name, field_spec in contract.items():
                if field_spec.get("required", False):
                    if field_name not in entity:
                        entity_result["missing"].append(field_name)
                        entity_result["valid"] = False
                    elif field_spec.get("type") == "number":
                        val = entity[field_name]
                        if not isinstance(val, (int, float)):
                            entity_result["missing"].append(f"{field_name} (not a number)")
                            entity_result["valid"] = False
                        elif val < field_spec.get("min", 0) or val > field_spec.get("max", 1):
                            entity_result["missing"].append(f"{field_name} (out of range {field_spec.get('min')}-{field_spec.get('max')})")
                            entity_result["valid"] = False
                    elif field_spec.get("type") == "string":
                        if not isinstance(entity[field_name], str):
                            entity_result["missing"].append(f"{field_name} (not a string)")
                            entity_result["valid"] = False

            if not entity_result["valid"]:
                results["valid"] = False
                results["errors"].append(entity_result)
            results["entities"].append(entity_result)

        return results

    def metabolize(self, text: str) -> dict:
        """
        Scan input text for entity aliases. Return matched entities with modifiers.
        
        Returns:
            {
                "entities": [{entity, w_scar, archetype, breaches, severity}],
                "modifiers": [response_modifier strings],
                "max_w_scar": float,
                "f2_required": bool,
                "delta_s_positive": bool
            }
        """
        registry = self._load_registry()
        text_lower = text.lower()

        matched_indices = set()
        for alias, idx in self._alias_map.items():
            if alias in text_lower:
                matched_indices.add(idx)

        entities = []
        modifiers = []
        max_w_scar = 0.0

        for idx in sorted(matched_indices):
            entity = registry["entities"][idx]
            w = entity.get("w_scar", 0.0)
            max_w_scar = max(max_w_scar, w)

            breaches = entity.get("governance_breaches", [])
            severity = "LOW"
            if w >= 0.8:
                severity = "CRITICAL"
            elif w >= 0.5:
                severity = "HIGH"
            elif w >= 0.3:
                severity = "MEDIUM"

            entities.append({
                "entity": entity["entity"],
                "w_scar": w,
                "archetype": entity.get("archetype", "unknown"),
                "breaches": [{"floor": b["floor"], "name": b["floor_name"], "desc": b["description"]} for b in breaches],
                "severity": severity
            })

            if entity.get("response_modifier"):
                modifiers.append(entity["response_modifier"])

        return {
            "entities": entities,
            "modifiers": modifiers,
            "max_w_scar": max_w_scar,
            "f2_required": max_w_scar > 0.8,
            "delta_s_positive": max_w_scar > 0.3,
            "match_count": len(matched_indices)
        }

    def inject_context(self, text: str, existing_context: str = "") -> str:
        """
        Full pre-processor pipeline: scan text, build context modifier, return augmented context.
        This is what gets prepended to the agent's system prompt.
        """
        result = self.metabolize(text)

        if result["match_count"] == 0:
            return existing_context

        lines = []
        if existing_context:
            lines.append(existing_context)
            lines.append("")

        lines.append("--- SCAR-WEIGHT CONTEXT (auto-injected by Trauma Theorem) ---")
        for modifier in result["modifiers"]:
            lines.append(modifier)

        if result["f2_required"]:
            lines.append("[SYSTEM] F2 Truth floor ACTIVE — max W_scar > 0.8. Elevated scrutiny on all claims from matched entities.")

        lines.append(f"[SYSTEM] Entities detected: {result['match_count']}. Max W_scar: {result['max_w_scar']}. ΔS>0: {result['delta_s_positive']}.")
        lines.append("--- END SCAR-WEIGHT CONTEXT ---")

        return "\n".join(lines)


def main():
    """CLI mode: read from stdin or argument, output JSON result."""
    parser = TraumaParser()

    # Validate first
    validation = parser.validate_registry()
    if not validation["valid"]:
        print(json.dumps({"error": "Registry validation failed", "details": validation["errors"]}, indent=2))
        sys.exit(1)

    # Get input
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = sys.stdin.read().strip()

    if not text:
        print(json.dumps({"error": "No input text provided"}))
        sys.exit(1)

    result = parser.metabolize(text)
    context = parser.inject_context(text)

    output = {
        "input": text,
        "result": result,
        "injected_context": context
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
