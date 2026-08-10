"""
Tool Classification Engine — Evaluates MCP tools against classification_policy.yaml.

Canonical Policy: /root/AAA/governance/classification_policy.yaml
Applies:
  1. Token extraction
  2. Mode overrides
  3. Verbs & Patterns matching (SEAL -> GOVERN -> MUTATE -> OBSERVE)
  4. Organ authority ceiling capping
  5. Fail-safe default: OBSERVE

DITEMPA BUKAN DIBERI — Forged, not given.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional
import yaml

POLICY_PATH = Path("/root/AAA/governance/classification_policy.yaml")

ToolClass = Literal["OBSERVE", "GOVERN", "MUTATE", "SEAL"]


class ClassificationEngine:
    """Evaluates and assigns constitutional action classes to MCP tools."""

    def __init__(self, policy_path: Path = POLICY_PATH) -> None:
        self.policy_path = policy_path
        self._policy = self._load_policy()

    def _load_policy(self) -> dict:
        if not self.policy_path.exists():
            return {}
        with open(self.policy_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def reload(self) -> None:
        self._policy = self._load_policy()

    def classify_tool(
        self,
        tool_name: str,
        server_or_organ: str = "",
        mode: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Classify a single tool and return full constitutional metadata."""
        if not self._policy:
            return {
                "tool_name": tool_name,
                "server": server_or_organ,
                "action_class": "OBSERVE",
                "effective_class": "OBSERVE",
                "authority_ceiling": "UNBOUNDED",
                "reason": "Default fallback (policy unavailable)",
            }

        # Step 1: Tokenize
        clean_name = tool_name.lower().strip()
        tokens = set(re.split(r"[_\-:]", clean_name))

        # Step 2: Check mode overrides if mode provided or tool matches
        mode_overrides = self._policy.get("mode_overrides", [])
        for mo in mode_overrides:
            if mo.get("tool") == clean_name:
                modes_map = mo.get("modes", {})
                if mode and mode in modes_map:
                    base_class = modes_map[mode]
                    return self._apply_organ_ceiling(clean_name, server_or_organ, base_class, f"Mode override ({mode})")

        # Step 3: Verbs and pattern rules from verb_rules
        verb_rules = self._policy.get("verb_rules", {})
        base_class: ToolClass = "OBSERVE"
        matched_rule = "Default OBSERVE"

        # Check SEAL
        seal_cfg = verb_rules.get("SEAL", {})
        if self._matches_rule(clean_name, tokens, seal_cfg):
            base_class = "SEAL"
            matched_rule = "SEAL verb/pattern match"
        else:
            # Check GOVERN
            govern_cfg = verb_rules.get("GOVERN", {})
            if self._matches_rule(clean_name, tokens, govern_cfg):
                base_class = "GOVERN"
                matched_rule = "GOVERN verb/pattern match"
            else:
                # Check MUTATE
                mutate_cfg = verb_rules.get("MUTATE", {})
                if self._matches_rule(clean_name, tokens, mutate_cfg):
                    base_class = "MUTATE"
                    matched_rule = "MUTATE verb/pattern match"
                else:
                    # Check OBSERVE
                    observe_cfg = verb_rules.get("OBSERVE", {})
                    if self._matches_rule(clean_name, tokens, observe_cfg):
                        base_class = "OBSERVE"
                        matched_rule = "OBSERVE verb/pattern match"

        # Step 4: Apply organ authority ceiling
        return self._apply_organ_ceiling(clean_name, server_or_organ, base_class, matched_rule)

    def _matches_rule(self, tool_name: str, tokens: set[str], class_cfg: dict) -> bool:
        verbs = set(class_cfg.get("verbs", []))
        if tokens.intersection(verbs):
            return True

        patterns = class_cfg.get("patterns", [])
        for pat in patterns:
            if re.search(pat, tool_name, re.IGNORECASE):
                return True
        return False

    def _apply_organ_ceiling(
        self,
        tool_name: str,
        organ_name: str,
        base_class: ToolClass,
        rule_desc: str,
    ) -> Dict[str, Any]:
        organ_overrides = self._policy.get("organ_overrides", {})
        organ_key = organ_name.upper()

        # Match organ key
        matched_organ_cfg = None
        for k, v in organ_overrides.items():
            if k.upper() == organ_key or k.lower() == organ_name.lower():
                matched_organ_cfg = v
                break

        if not matched_organ_cfg:
            return {
                "tool_name": tool_name,
                "server": organ_name,
                "action_class": base_class,
                "effective_class": base_class,
                "authority_ceiling": "UNBOUNDED",
                "reason": rule_desc,
            }

        authority_ceiling = matched_organ_cfg.get("authority_ceiling", "UNBOUNDED")
        max_class = matched_organ_cfg.get("max_class", base_class)

        # Check organ specific exceptions
        exceptions = matched_organ_cfg.get("exception", [])
        for exc in exceptions:
            if exc.get("tool") == tool_name:
                return {
                    "tool_name": tool_name,
                    "server": organ_name,
                    "action_class": exc.get("class", base_class),
                    "effective_class": exc.get("class", base_class),
                    "authority_ceiling": authority_ceiling,
                    "reason": f"Organ exception: {exc.get('note', '')}",
                }

        # Hierarchy: OBSERVE (1) < GOVERN (2) < MUTATE (3) < SEAL (4)
        order = {"OBSERVE": 1, "GOVERN": 2, "MUTATE": 3, "SEAL": 4}
        effective_class = base_class
        if order.get(base_class, 1) > order.get(max_class, 4):
            effective_class = max_class
            rule_desc += f" (Capped by organ ceiling {authority_ceiling} -> {max_class})"

        return {
            "tool_name": tool_name,
            "server": organ_name,
            "action_class": base_class,
            "effective_class": effective_class,
            "authority_ceiling": authority_ceiling,
            "reason": rule_desc,
        }


# Global instance
_classifier = ClassificationEngine()


def classify_tool(tool_name: str, server_or_organ: str = "", mode: Optional[str] = None) -> Dict[str, Any]:
    return _classifier.classify_tool(tool_name, server_or_organ, mode)
