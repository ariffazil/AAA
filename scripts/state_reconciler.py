#!/usr/bin/env python3
"""state_reconciler.py — AAA state reconciliation (PR-2 FEDERATION-SOT).

Implements the README promise: AAA establishes ``ObservedState_A ?= ObservedState_B``.
It does NOT establish ``Claim = AbsoluteTruth``. Reconciliation, not verification.

Design laws:
  - Per-dimension conclusions ONLY. A component is never collapsed into one
    verdict: WEALTH internal transport UP + external ingress DOWN yields
    ``WEALTH_INTERNAL_TRANSPORT_UP`` and ``WEALTH_EXTERNAL_INGRESS_DOWN`` —
    never "WEALTH is down".
  - Same (component, dimension) with conflicting states from different sources
    emits a typed CONTRADICTION carrying both sources. It is never averaged.
  - Stale observations (source_age_seconds above threshold) emit STALE findings;
    the age is preserved, not hidden.
  - AdvertisedVsRuntime: dimension ``advertised_tools`` vs ``accepted_tools``
    catches connector/runtime disagreement (the GEOX case) as
    ADVERTISED_NOT_ACCEPTED with the tool names.
  - UNKNOWN_TOOL_NAME distinguishes "tool never declared" from
    "tool declared but broken" (the WELL case).

Importable subsystem + CLI:
    python3 scripts/state_reconciler.py federation/runtime-state.json
        -> prints a compressed human summary
        -> writes federation/runtime-state.reconciled.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = REPO_ROOT / "federation" / "runtime-state.json"
RECONCILER_ID = "scripts/state_reconciler.py v1 (FI-008 · PR-2 FEDERATION-SOT)"

STALE_THRESHOLD_SECONDS = 300.0
TOOL_LIST_DIMENSIONS = {"advertised_tools", "accepted_tools"}
TOOL_INVOCATION_DIMENSION = "tool_invocation"
UNKNOWN_TOOL_STATE = "UNKNOWN_TOOL"

# Finding kinds
K_CONCLUSION = "CONCLUSION"
K_CONTRADICTION = "CONTRADICTION"
K_STALE = "STALE"
K_ADVERTISED_NOT_ACCEPTED = "ADVERTISED_NOT_ACCEPTED"
K_ADVERTISED_MATCHED = "ADVERTISED_VS_RUNTIME_MATCHED"
K_TOOL_SURFACE_UNMEASURED = "TOOL_SURFACE_UNMEASURED"
K_UNKNOWN_TOOL_NAME = "UNKNOWN_TOOL_NAME"


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _norm_slug(*parts: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", "_".join(parts)).strip("_").upper()


@dataclass
class Observation:
    """One live observation, shaped per README 'State Reconciliation' fields."""

    component: str
    dimension: str
    state: str
    observed_at: str
    source: str
    source_age_seconds: float
    confidence: float
    probe_method: str
    failure_reason: Optional[str] = None
    # Optional payload extension (e.g. {"tools": [...]} for tool-list dimensions,
    # {"tool": ..., "error": ...} for tool_invocation). Never required.
    detail: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, raw: Dict[str, Any]) -> "Observation":
        missing = [
            key for key in
            ("component", "dimension", "state", "observed_at", "source",
             "probe_method")
            if key not in raw
        ]
        if missing:
            raise ValueError(f"observation missing required fields: {missing}")
        return cls(
            component=str(raw["component"]),
            dimension=str(raw["dimension"]),
            state=str(raw["state"]),
            observed_at=str(raw["observed_at"]),
            source=str(raw["source"]),
            source_age_seconds=float(raw.get("source_age_seconds", 0.0) or 0.0),
            confidence=float(raw.get("confidence", 0.0) or 0.0),
            probe_method=str(raw["probe_method"]),
            failure_reason=raw.get("failure_reason"),
            detail=raw.get("detail") if isinstance(raw.get("detail"), dict) else None,
        )


@dataclass
class Finding:
    """Typed reconciliation output. ALWAYS dimension-scoped; never a component
    single verdict."""

    kind: str
    component: str
    dimension: str
    conclusion: str
    sources: List[str] = field(default_factory=list)
    detail: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "kind": self.kind,
            "component": self.component,
            "dimension": self.dimension,
            "conclusion": self.conclusion,
            "sources": list(self.sources),
            "detail": dict(self.detail),
        }


@dataclass
class ReconciliationResult:
    observations: List[Observation]
    entries: List[Finding]

    @property
    def summary(self) -> Dict[str, int]:
        counts: Dict[str, int] = {k: 0 for k in (
            K_CONCLUSION, K_CONTRADICTION, K_STALE, K_ADVERTISED_NOT_ACCEPTED,
            K_ADVERTISED_MATCHED, K_TOOL_SURFACE_UNMEASURED, K_UNKNOWN_TOOL_NAME,
        )}
        for entry in self.entries:
            counts[entry.kind] = counts.get(entry.kind, 0) + 1
        counts["observations"] = len(self.observations)
        counts["components"] = len({o.component for o in self.observations})
        return counts

    def conclusion_ids(self) -> set:
        return {e.conclusion for e in self.entries}

    def to_dict(self, input_path: str = "") -> Dict[str, Any]:
        return {
            "reconciled_at": _utcnow_iso(),
            "reconciler": RECONCILER_ID,
            "input": input_path,
            "summary": self.summary,
            "note": (
                "Reconciliation, not verification: ObservedState_A ?= ObservedState_B. "
                "Every finding is dimension-scoped; no component-level single verdict exists in this shape."
            ),
            "entries": [e.to_dict() for e in self.entries],
        }


def _tools_from(obs: Observation) -> List[str]:
    if not obs.detail:
        return []
    tools = obs.detail.get("tools")
    if isinstance(tools, list):
        return [str(t) for t in tools]
    return []


def _group(observations: List[Observation]) -> Dict[Tuple[str, str], List[Observation]]:
    groups: Dict[Tuple[str, str], List[Observation]] = {}
    for obs in observations:
        groups.setdefault((obs.component, obs.dimension), []).append(obs)
    return groups


def _emit_group_findings(component: str, dimension: str,
                         group: List[Observation], entries: List[Finding]) -> None:
    states = {obs.state for obs in group}
    sources = [obs.source for obs in group]

    if len(states) == 1:
        state = next(iter(states))
        entries.append(Finding(
            kind=K_CONCLUSION, component=component, dimension=dimension,
            conclusion=_norm_slug(component, dimension, state),
            sources=sources,
            detail={
                "state": state,
                "observation_count": len(group),
                "failure_reasons": [o.failure_reason for o in group if o.failure_reason],
            },
        ))
    elif len(states) > 1:
        # Same dimension, conflicting states across sources -> CONTRADICTION.
        # Preserved, not averaged, not resolved into a single verdict.
        entries.append(Finding(
            kind=K_CONTRADICTION, component=component, dimension=dimension,
            conclusion=_norm_slug(component, dimension, "CONTRADICTION"),
            sources=sources,
            detail={
                "conflicting_states": sorted(states),
                "by_source": [
                    {"source": obs.source, "state": obs.state,
                     "observed_at": obs.observed_at}
                    for obs in group
                ],
                "resolution": "conflict preserved — reconcile sources, do not average",
            },
        ))

    for obs in group:
        if obs.source_age_seconds > STALE_THRESHOLD_SECONDS:
            entries.append(Finding(
                kind=K_STALE, component=component, dimension=dimension,
                conclusion=_norm_slug(component, dimension, "STALE"),
                sources=[obs.source],
                detail={
                    "source_age_seconds": obs.source_age_seconds,
                    "threshold_seconds": STALE_THRESHOLD_SECONDS,
                    "observed_at": obs.observed_at,
                    "state": obs.state,
                },
            ))


def _advertised_vs_runtime(observations: List[Observation],
                           entries: List[Finding]) -> None:
    """AdvertisedVsRuntime check: connector advertises tools its runtime rejects."""
    by_component: Dict[str, Dict[str, List[Observation]]] = {}
    for obs in observations:
        if obs.dimension in TOOL_LIST_DIMENSIONS:
            by_component.setdefault(obs.component, {}).setdefault(obs.dimension, []).append(obs)

    for component, dims in by_component.items():
        advertised = dims.get("advertised_tools", [])
        accepted = dims.get("accepted_tools", [])
        if not advertised or not accepted:
            continue

        accepted_states = {o.state for o in accepted}
        if accepted_states & {"UNREACHABLE", "UNKNOWN"}:
            # Cannot claim a mismatch when the accepted side was never measured.
            entries.append(Finding(
                kind=K_TOOL_SURFACE_UNMEASURED, component=component,
                dimension="advertised_tools:accepted_tools",
                conclusion=_norm_slug(component, "advertised_vs_runtime", "UNMEASURED"),
                sources=[o.source for o in advertised + accepted],
                detail={"accepted_states": sorted(accepted_states),
                        "resolution": "no mismatch claim without a measured accepted surface"},
            ))
            continue

        adv_set = set()
        for obs in advertised:
            adv_set.update(_tools_from(obs))
        acc_set = set()
        for obs in accepted:
            acc_set.update(_tools_from(obs))

        not_accepted = sorted(adv_set - acc_set)
        if not_accepted:
            entries.append(Finding(
                kind=K_ADVERTISED_NOT_ACCEPTED, component=component,
                dimension="advertised_tools:accepted_tools",
                conclusion=_norm_slug(component, "advertised_not_accepted"),
                sources=[o.source for o in advertised + accepted],
                detail={
                    "tools": not_accepted,
                    "advertised_count": len(adv_set),
                    "accepted_count": len(acc_set),
                    "resolution": "connector advertises more than its runtime accepts",
                },
            ))
        else:
            entries.append(Finding(
                kind=K_ADVERTISED_MATCHED, component=component,
                dimension="advertised_tools:accepted_tools",
                conclusion=_norm_slug(component, "advertised_vs_runtime", "MATCHED"),
                sources=[o.source for o in advertised + accepted],
                detail={"advertised_count": len(adv_set), "accepted_count": len(acc_set)},
            ))


def _unknown_tool_names(observations: List[Observation],
                        entries: List[Finding]) -> None:
    """Distinguish 'tool never declared' from 'tool declared but broken'."""
    declared_by_component: Dict[str, set] = {}
    for obs in observations:
        if obs.dimension == "advertised_tools":
            declared_by_component.setdefault(obs.component, set()).update(_tools_from(obs))

    for obs in observations:
        if obs.dimension != TOOL_INVOCATION_DIMENSION or obs.state != UNKNOWN_TOOL_STATE:
            continue
        tool = (obs.detail or {}).get("tool")
        if not tool:
            entries.append(Finding(
                kind=K_UNKNOWN_TOOL_NAME, component=obs.component,
                dimension=TOOL_INVOCATION_DIMENSION,
                conclusion=_norm_slug(obs.component, "tool_name", "UNCLASSIFIABLE"),
                sources=[obs.source],
                detail={"error": obs.failure_reason or (obs.detail or {}).get("error"),
                        "classification": "UNCLASSIFIABLE_NO_TOOL_NAME"},
            ))
            continue
        declared = declared_by_component.get(obs.component)
        if declared is None:
            classification = "DECLARATION_UNMEASURED"
        elif tool in declared:
            classification = "DECLARED_BUT_BROKEN"
        else:
            classification = "NEVER_DECLARED"
        entries.append(Finding(
            kind=K_UNKNOWN_TOOL_NAME, component=obs.component,
            dimension=TOOL_INVOCATION_DIMENSION,
            conclusion=_norm_slug(obs.component, "unknown_tool_name", classification),
            sources=[obs.source],
            detail={
                "tool": str(tool),
                "classification": classification,
                "error": obs.failure_reason or (obs.detail or {}).get("error"),
                "declared_tools_sample": sorted(declared)[:12] if declared else [],
            },
        ))


def reconcile(observations: List[Observation]) -> ReconciliationResult:
    """Group observations by (component, dimension) and emit typed findings."""
    entries: List[Finding] = []
    for (component, dimension), group in sorted(_group(observations).items()):
        _emit_group_findings(component, dimension, group, entries)
    _advertised_vs_runtime(observations, entries)
    _unknown_tool_names(observations, entries)
    return ReconciliationResult(observations=list(observations), entries=entries)


def load_observations(path: Path) -> List[Observation]:
    with path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    raw_list = payload.get("observations", payload if isinstance(payload, list) else [])
    return [Observation.from_dict(raw) for raw in raw_list]


def render_summary(result: ReconciliationResult) -> str:
    counts = result.summary
    lines = [
        f"reconciled: {counts['observations']} observations · "
        f"{counts['components']} components · "
        f"conclusions {counts.get(K_CONCLUSION, 0)} · "
        f"contradictions {counts.get(K_CONTRADICTION, 0)} · "
        f"stale {counts.get(K_STALE, 0)} · "
        f"advertised-not-accepted {counts.get(K_ADVERTISED_NOT_ACCEPTED, 0)} · "
        f"unknown-tool-name {counts.get(K_UNKNOWN_TOOL_NAME, 0)}",
    ]
    by_component: Dict[str, List[Finding]] = {}
    for entry in result.entries:
        by_component.setdefault(entry.component, []).append(entry)
    for component in sorted(by_component):
        parts = []
        for entry in by_component[component]:
            tag = entry.kind if entry.kind != K_CONCLUSION else entry.detail.get("state", "")
            src = entry.sources[0] if entry.sources else "?"
            parts.append(f"{entry.dimension}={tag} ({src})")
        lines.append(f"  {component:<9} " + " · ".join(parts))
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="AAA state reconciler (README ObservedState_A ?= ObservedState_B)")
    parser.add_argument("input", nargs="?", default=str(DEFAULT_INPUT),
                        help=f"path to runtime-state json (default: {DEFAULT_INPUT})")
    parser.add_argument("--output", default=None,
                        help="output path (default: <input stem>.reconciled.json alongside input)")
    args = parser.parse_args(argv)

    input_path = Path(args.input)
    try:
        observations = load_observations(input_path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"RECONCILER INPUT ERROR: {exc}", file=sys.stderr)
        return 1

    result = reconcile(observations)

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_name(input_path.stem + ".reconciled.json")

    payload = result.to_dict(input_path=str(input_path))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
        fh.write("\n")

    print(render_summary(result))
    print(f"wrote {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
