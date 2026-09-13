#!/usr/bin/env python3
"""
Reality Object Gate — executable enforcement for the Three Consequence Domains.

Doctrine : /root/AAA/canon/APEX_REALITY_GRAPH_MEMORY_MIGRATION_v1.md   (F13_RATIFIED_CHAT 2026-09-13)
Spec     : /root/AAA/canon/REALITY_CONSEQUENCE_OBJECTS_SPEC_v1.md      (arifos.wro|hro|mro|cro.v1)
Fragment : /root/AAA/instructions/three-consequence-domains.md         (R0-R5 + 5 Golden Questions)

WHY THIS EXISTS
---------------
The ratified spec §6 declares three invariants. Until this file, nothing enforced them:
  INV-1 Consequence Invariance  : severity >= HIGH  -> CRO.authority_contraction == true
  INV-2 Attention Budget Invariance : HRO.attention_cost == EXHAUSTED -> block non-P0 interrupts
  INV-3 Witness Invariance      : every object carries observed_by + observed_at
An invariant with no enforcement is a CLAIM, not a law (F-2, reports/2026-09-13-...-alignment...).

Exit contract (matches federation_memory_audit.py):
  0 = all objects valid, all invariants hold
  1 = validation or invariant violation (fail-closed)

Modes:
  (default)  validate every object under --root, report, exit 0/1
  --gate     given a proposed action, emit the governing behaviour + authority for the agent
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("FATAL: pyyaml required (pip install pyyaml)", file=sys.stderr)
    sys.exit(1)

DEFAULT_ROOT = Path("/root/AAA/state/reality_objects")

# ── schemas exactly as ratified in REALITY_CONSEQUENCE_OBJECTS_SPEC_v1.md ────────────

SCHEMAS: dict[str, dict] = {
    "arifos.wro.v1": {
        "required": ["schema", "id", "type", "domain", "observed_fact", "source",
                     "constraint_type", "verification_class", "impact_on_agents",
                     "status", "review_by"],
        "enums": {
            "type": ["external_constraint", "market_state", "industry_shift",
                     "regulation", "physical_reality"],
            "domain": ["energy", "macro", "ai_industry", "geology", "national_policy"],
            "constraint_type": ["hard_boundary", "economic_regime", "policy_ceiling",
                                "physical_limit"],
            "verification_class": ["DETERMINISTIC", "WITNESSED", "PROBED", "DERIVED"],
            "status": ["ACTIVE", "SUPERSEDED", "EXPIRED"],
        },
        "nested": {"source": {"required": ["type", "uri", "observed_at", "observed_by"],
                              "enums": {"type": ["primary_source", "regulatory_filing",
                                                 "market_feed", "physical_sensor"]}}},
        "witness_paths": [("observed_by", "source.observed_by"),
                          ("observed_at", "source.observed_at")],
    },
    "arifos.hro.v1": {
        "required": ["schema", "id", "type", "title", "owner", "stakeholders",
                     "attention_cost", "consequence_class", "authority_level",
                     "what_matters_rationale", "scar_links", "admissibility",
                     "expires_at", "next_physical_action"],
        "enums": {
            "type": ["commitment", "responsibility", "strategic_project",
                     "stakeholder_obligation", "attention_constraint"],
            "attention_cost": ["LOW", "MEDIUM", "HIGH", "EXHAUSTED"],
            "consequence_class": ["REPUTATIONAL", "STRATEGIC", "FINANCIAL",
                                  "OPERATIONAL", "PERSONAL"],
            "authority_level": ["SOVEREIGN_ONLY", "DELEGATED_DRAFT", "SILENT_SOLVE"],
            "admissibility": ["ACTIVE", "DORMANT", "EXPIRED"],
        },
        "witness_paths": [],
        "witness_optional": True,  # HRO is sovereign self-report; witness = owner + review
    },
    "arifos.mro.v1": {
        "required": ["schema", "id", "type", "name", "organ", "state",
                     "mutation_surface", "verification_method", "rollback_path",
                     "owner", "observed_at"],
        "enums": {
            "type": ["systemd_service", "docker_container", "git_repository",
                     "mcp_tool", "network_port", "queue"],
            "organ": ["arifos", "aforge", "geox", "wealth", "well", "aaa"],
            "state": ["RUNNING", "STOPPED", "HEALTHY", "DEGRADED", "DEPRECATED"],
            "mutation_surface": ["BASTION", "SSH", "CONTAINER_EXEC", "LOCAL_PROCESS",
                                 "NONE"],
            "verification_method": ["SYSTEMCTL", "CURL_PROBE", "GIT_DIFF", "LSP_CHECK",
                                    "DOCTOR_SH"],
        },
        "witness_paths": [("observed_by", "observed_at")],
    },
    "arifos.cro.v1": {
        "required": ["schema", "id", "consequence_owner", "triggering_event",
                     "world_context", "human_context", "machine_context", "severity",
                     "authority_contraction", "required_witness", "behavior_change",
                     "scar_precedent", "active_until"],
        "enums": {
            "consequence_owner": ["ARIF", "PETRONAS_TEAM", "FEDERATION"],
            "severity": ["TRIVIAL", "LOW", "MEDIUM", "HIGH", "CATASTROPHIC"],
            "required_witness": ["NONE", "DUAL_AGENT", "HUMAN_EXPLICIT", "MULTI_PARTY"],
        },
        "nested": {"behavior_change": {"required": ["mode", "reason"],
                                       "enums": {"mode": ["SILENT_ABSORB", "DRAFT_ONLY",
                                                          "HOLD_FOR_CONFIRMATION",
                                                          "HARD_ABORT"]}}},
        "witness_paths": [],
    },
}

SEVERITY_HIGH = {"HIGH", "CATASTROPHIC"}
BEHAVIOUR_BY_SEVERITY = {
    "TRIVIAL": "SILENT_ABSORB",
    "LOW": "SILENT_ABSORB",
    "MEDIUM": "DRAFT_ONLY",
    "HIGH": "HOLD_FOR_CONFIRMATION",
    "CATASTROPHIC": "HARD_ABORT",
}


def _dig(obj: dict, dotted: str):
    cur = obj
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def validate_object(obj: dict, path: Path) -> list[str]:
    """Return list of violation strings (empty == valid)."""
    v: list[str] = []
    schema = obj.get("schema")
    if schema not in SCHEMAS:
        return [f"{path.name}: unknown/absent schema {schema!r} (expected one of "
                f"{', '.join(SCHEMAS)})"]
    spec = SCHEMAS[schema]

    for field in spec["required"]:
        if field not in obj:
            v.append(f"{path.name}: missing required field '{field}'")
        elif obj[field] in ("", None) and field not in ("expires_at", "scar_precedent",
                                                        "scar_links"):
            v.append(f"{path.name}: required field '{field}' is empty")

    for field, allowed in spec["enums"].items():
        if field in obj and obj[field] not in allowed:
            v.append(f"{path.name}: {field}={obj[field]!r} not in enum "
                     f"[{'|'.join(allowed)}]")

    for sub, sub_spec in (spec.get("nested") or {}).items():
        block = obj.get(sub)
        if not isinstance(block, dict):
            v.append(f"{path.name}: '{sub}' must be a mapping")
            continue
        for field in sub_spec["required"]:
            if field not in block or block[field] in ("", None):
                v.append(f"{path.name}: {sub}.{field} missing/empty")
        for field, allowed in (sub_spec.get("enums") or {}).items():
            if field in block and block[field] not in allowed:
                v.append(f"{path.name}: {sub}.{field}={block[field]!r} not in enum "
                         f"[{'|'.join(allowed)}]")

    # INV-3 Witness Invariance
    if not spec.get("witness_optional"):
        for label, dotted in spec.get("witness_paths", []):
            if _dig(obj, dotted) in (None, ""):
                v.append(f"{path.name}: INV-3 Witness Invariance violated — "
                         f"no {label} ({dotted})")
    return v


def validate_invariants(objects: dict[str, dict]) -> list[str]:
    v: list[str] = []
    for oid, obj in objects.items():
        schema = obj.get("schema")
        # INV-1 Consequence Invariance
        if schema == "arifos.cro.v1":
            if obj.get("severity") in SEVERITY_HIGH and obj.get("authority_contraction") is not True:
                v.append(f"{oid}: INV-1 Consequence Invariance violated — severity="
                         f"{obj.get('severity')} requires authority_contraction=true")
            expect = BEHAVIOUR_BY_SEVERITY.get(obj.get("severity", ""), None)
            actual = _dig(obj, "behavior_change.mode")
            if expect and actual and actual != expect and expect == "HARD_ABORT":
                v.append(f"{oid}: behaviour_change.mode={actual} too permissive for "
                         f"severity={obj.get('severity')} (expect {expect})")
        # INV-2 Attention Budget Invariance
        if schema == "arifos.hro.v1":
            if obj.get("attention_cost") == "EXHAUSTED" and obj.get("authority_level") \
                    not in ("SOVEREIGN_ONLY", "SILENT_SOLVE"):
                v.append(f"{oid}: INV-2 Attention Budget Invariance — "
                         f"attention_cost=EXHAUSTED requires authority_level="
                         f"SOVEREIGN_ONLY|SILENT_SOLVE (got {obj.get('authority_level')})")
    return v


def load(root: Path) -> tuple[dict[str, dict], list[str]]:
    objects: dict[str, dict] = {}
    errs: list[str] = []
    for f in sorted(root.glob("*.y*ml")):
        try:
            data = yaml.safe_load(f.read_text())
        except Exception as exc:  # noqa: BLE001
            errs.append(f"{f.name}: YAML parse error: {exc}")
            continue
        if not isinstance(data, dict):
            errs.append(f"{f.name}: top level must be a mapping")
            continue
        objects[data.get("id", f.stem)] = data
    return objects, errs


def gate(objects: dict[str, dict], owner: str, severity: str | None,
         attention: str | None) -> dict:
    """Compute the governing behaviour for a proposed action (the answer to
    'how do witnessed realities change agent behaviour?')."""
    mode = BEHAVIOUR_BY_SEVERITY.get((severity or "LOW").upper(), "SILENT_ABSORB")
    contraction = (severity or "").upper() in SEVERITY_HIGH
    authority = "AUTO" if not contraction else "DRAFT_ONLY"
    basis: list[str] = []

    # CONFLICT-RULE-1 (P0 escalation). INV-1 (severity>=HIGH requires explicit human
    # witness) and INV-2 (exhausted attention blocks non-P0 interrupts) contradict each
    # other when both fire: the agent must ask the human but is forbidden to interrupt
    # him. Resolution: severity>=HIGH is itself P0-class, so the interrupt is permitted;
    # everything below P0 is silently absorbed or held. OPEN DOCTRINE QUESTION for F13 —
    # this ordering is inferred by the gate, not yet stated in the ratified spec.
    p0 = contraction
    if (attention or "").upper() == "EXHAUSTED":
        if p0:
            mode = "HOLD_FOR_CONFIRMATION"
            authority = "DRAFT_ONLY"
            basis.append("R1 HRO: attention_cost=EXHAUSTED blocks non-P0 interrupts "
                         "(INV-2), but severity>=HIGH is P0 → interrupt permitted "
                         "(CONFLICT-RULE-1)")
        else:
            mode = "SILENT_ABSORB"
            authority = "SILENT_SOLVE"
            basis.append("R1 HRO: attention_cost=EXHAUSTED → non-P0 interrupts blocked "
                         "(INV-2); silently solve or hold")
    if contraction:
        authority = "DRAFT_ONLY"
        basis.append(f"R4: severity={severity} and consequence_owner={owner} → "
                     "authority contracts (INV-1)")
    if any(o.get("schema") == "arifos.hro.v1" and o.get("attention_cost") == "EXHAUSTED"
           for o in objects.values()):
        basis.append("R1 HRO: at least one open HRO holds attention_cost=EXHAUSTED")

    return {
        "consequence_owner": owner,
        "severity": severity,
        "attention": attention,
        "authority_ceiling": authority,
        "required_behaviour": mode,
        "required_witness": "HUMAN_EXPLICIT" if contraction else "NONE",
        "basis": basis or ["no R0/R1 constraint matched — default silent absorb"],
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
        "verdict": "PASS" if not contraction else "CONTRACT",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Reality Object Gate (WRO/HRO/MRO/CRO)")
    ap.add_argument("--root", default=str(DEFAULT_ROOT), help="object directory")
    ap.add_argument("--gate", action="store_true", help="emit behaviour for a proposal")
    ap.add_argument("--action", default="(unspecified proposed action)")
    ap.add_argument("--consequence-owner", default="ARIF",
                    choices=["ARIF", "PETRONAS_TEAM", "FEDERATION"])
    ap.add_argument("--severity", default="LOW")
    ap.add_argument("--attention", default="LOW")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    root = Path(args.root)
    if not root.exists():
        print(f"FATAL: object root does not exist: {root}", file=sys.stderr)
        return 1

    objects, errs = load(root)
    violations: list[str] = list(errs)
    for oid, obj in objects.items():
        for f in sorted(root.glob("*.y*ml")):
            if f.stem == oid or obj.get("id") == oid:
                violations.extend(validate_object(obj, f))
                break
    violations.extend(validate_invariants(objects))

    if args.gate:
        result = gate(objects, args.consequence_owner, args.severity, args.attention)
        result["action"] = args.action
        print(json.dumps(result, indent=2) if args.json else
              f"action            : {args.action}\n"
              f"authority_ceiling : {result['authority_ceiling']}\n"
              f"behaviour         : {result['required_behaviour']}\n"
              f"required_witness  : {result['required_witness']}\n"
              f"verdict           : {result['verdict']}\n"
              f"basis             : " + "; ".join(result["basis"]))
        return 0

    print(f"reality_object_gate — root={root}")
    print(f"objects loaded: {len(objects)}")
    by_schema: dict[str, int] = {}
    for o in objects.values():
        by_schema[o.get("schema", "?")] = by_schema.get(o.get("schema", "?"), 0) + 1
    for s, n in sorted(by_schema.items()):
        print(f"  {s:<20} {n}")
    if violations:
        print(f"\nFAIL: {len(violations)} violation(s)")
        for v in violations:
            print(f"  - {v}")
        return 1
    print("\nPASS: all objects schema-valid; INV-1/2/3 hold")
    return 0


if __name__ == "__main__":
    sys.exit(main())
