"""
TOOL_AUTHORITY_REGISTRY — PR 2 registry-owned action class.

Law:
  Callers MUST NOT self-declare action_class / authority.
  Authority comes from AAA registries/tools.yaml (execution_kind + risk_tier
  + approval_policy), mapped once at load time.

  Unknown tool:
    - domain organs (geox/wealth/well): default OBSERVE (evidence-only organs)
    - a-forge / unknown organ: HOLD via CAPABILITY_UNKNOWN when strict,
      or MUTATE+require_sct when name heuristics say side-effect

  Never trust arguments["action_class"].

DITEMPA BUKAN DIBERI — Forged, Not Given.
"""

from __future__ import annotations

import logging
import os
import re
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

logger = logging.getLogger("federation.tool_authority")

# Candidate paths for the canonical tools registry
_TOOLS_YAML_CANDIDATES = (
    Path(os.environ.get("AAA_TOOLS_YAML", "")),
    Path("/root/AAA/registries/tools.yaml"),
    Path(__file__).resolve().parents[1] / "registries" / "tools.yaml",
)

# Action classes (server-owned)
ACTION_OBSERVE = "OBSERVE"
ACTION_MUTATE = "MUTATE"
ACTION_ANALYZE = "ANALYZE"  # compute without host mutation — treated like OBSERVE for SCT
ACTION_UNKNOWN = "UNKNOWN"

# Authority bands (must match federation_sct AUTHORITY_RANK)
AUTH_OBSERVE = "OBSERVE_ONLY"
AUTH_OPERATOR = "OPERATOR"
AUTH_LIMITED = "LIMITED_MUTATE"
AUTH_FULL = "FULL"
AUTH_SOVEREIGN = "SOVEREIGN"

# Domain organs that are evidence-only by default when tool not in YAML
_DOMAIN_ORGANS = frozenset({"geox", "wealth", "well", "geox_mcp", "wealth_mcp"})

# Name tokens that imply side effect even if not in registry
_MUTATE_NAME_RE = re.compile(
    r"(write|delete|deploy|execute|mutate|shell|git_commit|drop|rm_|put_|post_|"
    r"create|update|patch|seal|approve|abort|lock|register|scar|forge_execute|"
    r"pipeline_run|sandbox_run)",
    re.I,
)
_OBSERVE_NAME_RE = re.compile(
    r"(read|get_|list_|status|health|probe|search|query|observe|think|route|"
    r"screenshot|extract|dryrun|memory$|registry_status|docs_lookup)",
    re.I,
)


@dataclass(frozen=True)
class ToolAuthority:
    """Server-owned authority record for one tool."""

    tool_id: str
    action_class: str
    required_authority: str
    require_sct: bool
    execution_kind: str
    risk_tier: str
    known: bool
    source: str  # "tools.yaml" | "organ_default" | "name_heuristic" | "unknown"
    organ_hint: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _normalize_id(name: str) -> str:
    """geox_query / geox-query / GEOX Query → geox-query style + underscore form."""
    s = (name or "").strip().lower()
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s


def _alt_ids(name: str) -> list[str]:
    n = _normalize_id(name)
    unders = n.replace("-", "_")
    return list(dict.fromkeys([n, unders, name.strip().lower() if name else ""]))


def _map_execution_to_authority(
    execution_kind: str,
    risk_tier: str,
    approval_policy: str,
) -> tuple[str, str, bool]:
    """Map tools.yaml fields → (action_class, required_authority, require_sct)."""
    kind = (execution_kind or "read").strip().lower()
    risk = (risk_tier or "low").strip().lower()
    approval = (approval_policy or "on-demand").strip().lower()

    if kind in ("read", "observe"):
        # Read paths: OBSERVE. High-risk reads still OBSERVE but may want SCT optional.
        action = ACTION_OBSERVE
        if risk == "high" and approval == "hold":
            # Sensitive read (e.g. wealth-query hold) — still no SCT required for observe
            return action, AUTH_OBSERVE, False
        return action, AUTH_OBSERVE, False

    if kind in ("execute", "write", "mutate"):
        action = ACTION_MUTATE
        require_sct = True
        if risk == "high" or approval == "hold":
            # High-stakes mutation
            return action, AUTH_LIMITED, require_sct
        if risk == "medium":
            return action, AUTH_LIMITED, require_sct
        return action, AUTH_OPERATOR, require_sct

    # Unknown execution_kind → conservative MUTATE
    return ACTION_MUTATE, AUTH_LIMITED, True


def _load_tools_yaml() -> list[dict[str, Any]]:
    for path in _TOOLS_YAML_CANDIDATES:
        if path and str(path) and path.is_file():
            try:
                import yaml  # type: ignore

                data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
                tools = data.get("tools") if isinstance(data, dict) else None
                if isinstance(tools, list):
                    logger.debug("tool_authority: loaded %d tools from %s", len(tools), path)
                    return tools
            except Exception as exc:
                logger.warning("tool_authority: failed to load %s: %s", path, exc)
    logger.warning("tool_authority: tools.yaml not found — registry empty")
    return []


@lru_cache(maxsize=1)
def _registry_index() -> dict[str, ToolAuthority]:
    """Build normalized-id → ToolAuthority index from tools.yaml."""
    index: dict[str, ToolAuthority] = {}
    for raw in _load_tools_yaml():
        if not isinstance(raw, dict):
            continue
        tid = str(raw.get("id") or "").strip()
        if not tid:
            continue
        kind = str(raw.get("execution_kind") or "read")
        risk = str(raw.get("risk_tier") or "low")
        approval = str(raw.get("approval_policy") or "on-demand")
        action, auth, require_sct = _map_execution_to_authority(kind, risk, approval)
        server_ref = str(raw.get("server_ref") or "")
        organ_hint = ""
        if "geox" in server_ref:
            organ_hint = "geox"
        elif "wealth" in server_ref:
            organ_hint = "wealth"
        elif "well" in server_ref:
            organ_hint = "well"
        elif "forge" in server_ref or "a-forge" in server_ref or "aforge" in server_ref:
            organ_hint = "a-forge"
        elif "arifos" in server_ref:
            organ_hint = "arifos"

        rec = ToolAuthority(
            tool_id=tid,
            action_class=action,
            required_authority=auth,
            require_sct=require_sct,
            execution_kind=kind,
            risk_tier=risk,
            known=True,
            source="tools.yaml",
            organ_hint=organ_hint,
        )
        for alt in _alt_ids(tid):
            if alt:
                index[alt] = rec
        # Also index bare name if present
        name = str(raw.get("name") or "")
        if name:
            for alt in _alt_ids(name):
                if alt and alt not in index:
                    index[alt] = rec
    return index


def reload_registry() -> int:
    """Force reload (tests). Returns entry count."""
    _registry_index.cache_clear()
    return len(_registry_index())


def _organ_default(tool_name: str, organ: str) -> ToolAuthority:
    """Server-owned default when tool not listed in tools.yaml."""
    org = (organ or "unknown").strip().lower()
    tid = tool_name or "unknown"

    if org in _DOMAIN_ORGANS:
        # Evidence organs — default OBSERVE (still fail-closed if SCT present+invalid)
        return ToolAuthority(
            tool_id=tid,
            action_class=ACTION_OBSERVE,
            required_authority=AUTH_OBSERVE,
            require_sct=False,
            execution_kind="read",
            risk_tier="medium",
            known=False,
            source="organ_default",
            organ_hint=org,
        )

    # A-FORGE / AAA / unknown — name heuristics (server-owned, not caller)
    if _OBSERVE_NAME_RE.search(tid) and not _MUTATE_NAME_RE.search(tid):
        return ToolAuthority(
            tool_id=tid,
            action_class=ACTION_OBSERVE,
            required_authority=AUTH_OBSERVE,
            require_sct=False,
            execution_kind="read",
            risk_tier="low",
            known=False,
            source="name_heuristic",
            organ_hint=org,
        )

    if _MUTATE_NAME_RE.search(tid) or org in ("a-forge", "aforge", "forge", "aaa"):
        return ToolAuthority(
            tool_id=tid,
            action_class=ACTION_MUTATE,
            required_authority=AUTH_LIMITED,
            require_sct=True,
            execution_kind="execute",
            risk_tier="high",
            known=False,
            source="name_heuristic",
            organ_hint=org,
        )

    # Last resort — unknown capability HOLD signal via action_class UNKNOWN
    return ToolAuthority(
        tool_id=tid,
        action_class=ACTION_UNKNOWN,
        required_authority=AUTH_LIMITED,
        require_sct=True,
        execution_kind="unknown",
        risk_tier="high",
        known=False,
        source="unknown",
        organ_hint=org,
    )


def resolve_tool_authority(
    tool_name: str,
    *,
    organ: str = "unknown",
    strict_unknown: bool = False,
) -> ToolAuthority:
    """Resolve server-owned authority for a tool.

    Args:
        tool_name: MCP tool name as invoked.
        organ: Organ calling the gate (geox, wealth, well, a-forge, …).
        strict_unknown: If True, unknown tools get action_class=UNKNOWN (HOLD).
                        If False, organ/name defaults apply (safer rollout).
    """
    index = _registry_index()
    for alt in _alt_ids(tool_name):
        if alt in index:
            return index[alt]

    if strict_unknown:
        return ToolAuthority(
            tool_id=tool_name,
            action_class=ACTION_UNKNOWN,
            required_authority=AUTH_LIMITED,
            require_sct=True,
            execution_kind="unknown",
            risk_tier="high",
            known=False,
            source="unknown",
            organ_hint=organ,
        )
    return _organ_default(tool_name, organ)


def strip_caller_action_class(arguments: dict[str, Any] | None) -> dict[str, Any]:
    """Remove caller-supplied authority claims from args (non-mutating copy)."""
    if not isinstance(arguments, dict):
        return {}
    out = dict(arguments)
    for key in (
        "action_class",
        "actionClass",
        "required_authority",
        "require_sct",
        "authority_band",
        "authority",
    ):
        # Do not strip session authority fields that are identity, only escalation claims.
        # 'authority' alone is ambiguous — only strip if paired with action_class self-declare.
        if key in ("action_class", "actionClass", "required_authority", "require_sct", "authority_band"):
            out.pop(key, None)
    return out


def effective_gate_params(
    tool_name: str,
    *,
    organ: str = "unknown",
    caller_require_sct: bool = False,
    caller_required_authority: str = AUTH_OBSERVE,
    use_registry: bool = True,
    strict_unknown: bool = False,
) -> tuple[ToolAuthority, bool, str, dict[str, Any] | None]:
    """Compute effective (authority, require_sct, required_authority, reject_or_None).

    Stricter-wins: registry require_sct OR caller require_sct.
    Registry required_authority is floor; caller may raise but not lower.
    """
    if not use_registry:
        # Legacy path — still never trust action_class; use caller flags only
        auth = ToolAuthority(
            tool_id=tool_name,
            action_class=ACTION_OBSERVE if not caller_require_sct else ACTION_MUTATE,
            required_authority=caller_required_authority or AUTH_OBSERVE,
            require_sct=caller_require_sct,
            execution_kind="legacy",
            risk_tier="unknown",
            known=False,
            source="legacy_caller_flags",
            organ_hint=organ,
        )
        return auth, caller_require_sct, caller_required_authority or AUTH_OBSERVE, None

    rec = resolve_tool_authority(tool_name, organ=organ, strict_unknown=strict_unknown)

    if rec.action_class == ACTION_UNKNOWN and strict_unknown:
        return rec, True, rec.required_authority, {
            "error": "CAPABILITY_UNKNOWN",
            "message": (
                f"Tool '{tool_name}' is not in the server authority registry "
                f"and organ '{organ}' has no safe default. HOLD."
            ),
            "tool": tool_name,
            "organ": organ,
            "registry": rec.to_dict(),
            "_epistemic": {
                "output_class": "GOVERNANCE_TEMPLATE",
                "authority_claim": "GATE_REJECTED",
                "tagged_by": "tool-authority-registry",
                "schema_version": "2.0.0",
            },
        }

    # require_sct: OR of registry and caller (caller can only tighten)
    require_sct = bool(rec.require_sct or caller_require_sct)

    # authority floor: take the higher of registry vs caller
    rank = (AUTH_OBSERVE, AUTH_OPERATOR, AUTH_LIMITED, AUTH_FULL, AUTH_SOVEREIGN)
    reg_a = rec.required_authority if rec.required_authority in rank else AUTH_OBSERVE
    call_a = caller_required_authority if caller_required_authority in rank else AUTH_OBSERVE
    required = reg_a if rank.index(reg_a) >= rank.index(call_a) else call_a

    return rec, require_sct, required, None


__all__ = [
    "ACTION_OBSERVE",
    "ACTION_MUTATE",
    "ACTION_ANALYZE",
    "ACTION_UNKNOWN",
    "ToolAuthority",
    "resolve_tool_authority",
    "strip_caller_action_class",
    "effective_gate_params",
    "reload_registry",
]
