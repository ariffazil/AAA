"""
registries/tool_authority.py — Canonical authority resolution for gate_tool_ingress()
═══════════════════════════════════════════════════════════════════════════════════
Forged 2026-07-17 · PR 2 — Registry-owned authorization context

Single source of truth. Every organ's SCT gate must resolve authority from
this module using tool_name. Callers never self-declare required_authority,
action_class, or require_sct.

Mapping contract:
  execution_kind × risk_tier → (action_class, required_authority, require_sct)

DITEMPA BUKAN DIBERI — Authority is derived, not declared.
"""

from __future__ import annotations

import yaml
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

TOOLS_YAML = Path(__file__).parent / "tools.yaml"


@dataclass(frozen=True)
class ToolAuthority:
    """Resolved authority contract for a single tool from the canonical registry."""
    tool_id: str
    action_class: str          # OBSERVE | MUTATE | UNKNOWN
    required_authority: str    # OBSERVE_ONLY | AUTHENTICATED_OBSERVE | MUTATE | MUTATE_PRIVILEGED | UNKNOWN
    require_sct: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "tool_id": self.tool_id,
            "action_class": self.action_class,
            "required_authority": self.required_authority,
            "require_sct": self.require_sct,
        }


# execution_kind × risk_tier → (action_class, required_authority, require_sct)
_ACTION_CLASS_MAP: dict[tuple[str, str], tuple[str, str, bool]] = {
    ("read",    "low"):    ("OBSERVE",  "OBSERVE_ONLY",           False),
    ("read",    "medium"): ("OBSERVE",  "OBSERVE_ONLY",           True),
    ("read",    "high"):   ("OBSERVE",  "AUTHENTICATED_OBSERVE",  True),
    ("observe", "low"):    ("OBSERVE",  "OBSERVE_ONLY",           False),
    ("observe", "medium"): ("OBSERVE",  "OBSERVE_ONLY",           True),
    ("observe", "high"):   ("OBSERVE",  "AUTHENTICATED_OBSERVE",  True),
    ("execute", "low"):    ("MUTATE",   "MUTATE",                 True),
    ("execute", "medium"): ("MUTATE",   "MUTATE",                 True),
    ("execute", "high"):   ("MUTATE",   "MUTATE_PRIVILEGED",      True),
}


@lru_cache(maxsize=None)
def _load_registry() -> dict[str, dict]:
    """Load and cache the canonical tools.yaml registry."""
    raw = yaml.safe_load(TOOLS_YAML.read_text())
    return {t["id"]: t for t in raw["tools"]}


def resolve_tool_authority(tool_id: str) -> ToolAuthority:
    """Resolve authority contract for a tool from the canonical registry.

    Returns UNKNOWN action_class if tool is not registered — caller must HOLD.
    Never raises; unknown tools get a safe-closed response.
    """
    registry = _load_registry()
    tool = registry.get(tool_id)
    if tool is None:
        return ToolAuthority(
            tool_id=tool_id,
            action_class="UNKNOWN",
            required_authority="UNKNOWN",
            require_sct=True,  # fail-closed: unknown tools require SCT
        )
    kind = tool.get("execution_kind", "execute")
    tier = tool.get("risk_tier", "high")
    action_class, required_authority, require_sct = _ACTION_CLASS_MAP.get(
        (kind, tier),
        ("UNKNOWN", "UNKNOWN", True),  # fail-closed for unmapped combos
    )
    return ToolAuthority(
        tool_id=tool_id,
        action_class=action_class,
        required_authority=required_authority,
        require_sct=require_sct,
    )


def validate_registry_consistency() -> list[str]:
    """Return list of tools in tools.yaml missing from the mapping, if any."""
    registry = _load_registry()
    issues: list[str] = []
    for tid, tool in registry.items():
        kind = tool.get("execution_kind", "execute")
        tier = tool.get("risk_tier", "high")
        if (kind, tier) not in _ACTION_CLASS_MAP:
            issues.append(
                f"{tid}: execution_kind={kind!r} × risk_tier={tier!r} has no mapping"
            )
    return issues
