#!/usr/bin/env python3
"""
aaa-registry compile — canonical compiler for the arifOS AAA model supply-chain registry.

Reads (canonical, hand-governed):
  registry/organizations|families|releases|offerings|routes|aliases|
          probes|evaluations|policies|assignments|incidents/  (*.yaml)
  registry/catalog/*.yaml        (legacy compatibility projection, preserved)

Generates (deterministic projections — never hand-edit, never write back):
  registry/generated/{catalog,provider-map,family-tree,route-resolution-map,
                      agent-assignment-map,freshness-report,drift-report}.json
  registry/compiled/{FEDERATION_MODEL.json,REGISTRY_INDEX.md,model-state.json,manifest.json}
                    (legacy consumers unchanged in shape)

DETERMINISM CONTRACT: same inputs -> byte-identical outputs.
  - every timestamp is derived from max(source mtimes), never wall clock
  - JSON: sort_keys, compact-ish stable separators, UTF-8, trailing newline
  - source_commit = git HEAD at compile time (changes only when the repo changes)

Authority: registry objects are facts; policies/ govern use; runtime truth comes only
from probes/. HTTP 200 != identity. Catalog claims != runtime truth.

DITEMPA BUKAN DIBERI.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import yaml

try:
    import jsonschema
except ImportError:
    jsonschema = None

GENERATOR_VERSION = "aaa-supply-chain-compiler/2.0.0"

REGISTRY = Path(__file__).parent
CATALOG_DIR = REGISTRY / "catalog"
COMPILED_DIR = REGISTRY / "compiled"
GENERATED_DIR = REGISTRY / "generated"
SCHEMA_DIR = REGISTRY / "schema"

ENTITY_DIRS = [
    "organizations", "families", "releases", "offerings", "routes",
    "aliases", "probes", "evaluations", "policies", "assignments", "incidents",
]
ENTITY_ID_FIELDS = {
    "organizations": "organization_id", "families": "family_id",
    "releases": "release_id", "offerings": "offering_id", "routes": "route_id",
    "aliases": "alias_id", "probes": "probe_id", "evaluations": "evaluation_id",
    "policies": "policy_id", "assignments": "assignment_id",
    "incidents": "incident_id",
}

SECRET_PATTERNS = re.compile(
    r"(?<![A-Za-z0-9_-])(?:sk|tp|gho|ghp|ghs)-[A-Za-z0-9]{20,}|"
    r"AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY-----"
)

ENTITY_SCHEMA_FILES = {
    "organizations": "organization.schema.json",
    "families": "family.schema.json",
    "releases": "release.schema.json",
    "offerings": "offering.schema.json",
    "routes": "route.schema.json",
    "aliases": "alias.schema.json",
    "probes": "probe.schema.json",
    "evaluations": "evaluation.schema.json",
    "policies": "policy.schema.json",
    "assignments": "assignment.schema.json",
    "incidents": "incident.schema.json",
}


class DateEncoder(json.JSONEncoder):
    def default(self, obj: object):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super().default(obj)


def dumps(obj: object, *, pretty: bool = True) -> str:
    if pretty:
        out = json.dumps(obj, cls=DateEncoder, sort_keys=True, indent=2, ensure_ascii=False)
    else:
        out = json.dumps(obj, cls=DateEncoder, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return out + "\n"


def content_hash(data) -> str:
    if isinstance(data, (dict, list)):
        data = dumps(data, pretty=False).rstrip("\n")
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


# ── loading ────────────────────────────────────────────────────────────────────

def _load_yaml(path: Path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_entities() -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for d in ENTITY_DIRS:
        p = REGISTRY / d
        out[d] = []
        if not p.exists():
            continue
        for fp in sorted(p.glob("*.yaml")):
            data = _load_yaml(fp)
            if data:
                data["_source_file"] = f"{d}/{fp.name}"
                out[d].append(data)
    return out


def load_catalog() -> list[dict]:
    records = []
    if not CATALOG_DIR.exists():
        return records
    for path in sorted(CATALOG_DIR.glob("*.yaml")):
        try:
            data = _load_yaml(path)
            if data:
                data["_source_file"] = f"catalog/{path.name}"
                records.append(data)
        except Exception as e:  # noqa: BLE001
            print(f"ERROR: Failed to load catalog/{path.name}: {e}")
    return records


def load_schema() -> dict:
    legacy = REGISTRY / "schema" / "model.schema.json"
    return json.loads(legacy.read_text()) if legacy.exists() else {}


# ── determinism inputs ─────────────────────────────────────────────────────────

def _source_paths() -> list[Path]:
    paths: list[Path] = []
    for d in ENTITY_DIRS:
        p = REGISTRY / d
        if p.exists():
            paths.extend(sorted(p.glob("*.yaml")))
    if CATALOG_DIR.exists():
        paths.extend(sorted(CATALOG_DIR.glob("*.yaml")))
    return paths


def derived_generated_at() -> str:
    """max source mtime, UTC — deterministic for fixed inputs."""
    ts = 0.0
    for p in _source_paths():
        try:
            ts = max(ts, p.stat().st_mtime)
        except OSError:
            continue
    if ts == 0.0:
        return "1970-01-01T00:00:00+00:00"
    return datetime.fromtimestamp(ts, timezone.utc).isoformat()


def source_commit() -> str:
    try:
        return subprocess.run(
            ["git", "-C", str(REGISTRY), "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=10, check=True,
        ).stdout.strip()
    except Exception:  # noqa: BLE001
        return "UNKNOWN"


# ── validation (entities) ──────────────────────────────────────────────────────

def validate_entity_schemas(entities: dict[str, list[dict]]) -> list[str]:
    errors: list[str] = []
    if jsonschema is None:
        return errors  # structural checks below still run
    for d, records in entities.items():
        schema_path = SCHEMA_DIR / ENTITY_SCHEMA_FILES[d]
        if not schema_path.exists():
            errors.append(f"schema-missing: {schema_path.name} for {d}/")
            continue
        schema = json.loads(schema_path.read_text())
        for r in records:
            clean = {k: v for k, v in r.items() if not k.startswith("_")}
            try:
                jsonschema.validate(clean, schema)
            except jsonschema.ValidationError as e:
                src = r.get("_source_file", "?")
                errors.append(f"{src}: {e.json_path}: {e.message}")
    return errors


def check_duplicate_ids(entities: dict[str, list[dict]]) -> list[str]:
    errors: list[str] = []
    for d, records in entities.items():
        seen: dict[str, str] = {}
        idf = ENTITY_ID_FIELDS[d]
        for r in records:
            eid = r.get(idf, "?")
            if eid in seen:
                errors.append(f"duplicate {idf} '{eid}' in {seen[eid]} and {r.get('_source_file', '?')}")
            seen[eid] = r.get("_source_file", "?")
    return errors


def check_references(entities: dict[str, list[dict]]) -> list[str]:
    errors: list[str] = []
    orgs = {o.get("organization_id") for o in entities.get("organizations", [])}
    fams = {f.get("family_id") for f in entities.get("families", [])}
    rels = {r.get("release_id") for r in entities.get("releases", [])}
    offs = {o.get("offering_id") for o in entities.get("offerings", [])}
    rts = {r.get("route_id") for r in entities.get("routes", [])}

    def src(r): return r.get("_source_file", "?")

    for f in entities.get("families", []):
        for ref in f.get("developer_refs", []):
            if ref not in orgs:
                errors.append(f"{src(f)}: developer_ref '{ref}' not in organizations/")
        for ref in f.get("release_refs", []):
            if ref not in rels:
                errors.append(f"{src(f)}: release_ref '{ref}' not in releases/")
    for r in entities.get("releases", []):
        if r.get("family_ref") not in fams:
            errors.append(f"{src(r)}: family_ref '{r.get('family_ref')}' not in families/")
        for ref in r.get("developer_refs", []):
            if ref not in orgs:
                errors.append(f"{src(r)}: developer_ref '{ref}' not in organizations/")
    for o in entities.get("offerings", []):
        if o.get("provider_ref") not in orgs:
            errors.append(f"{src(o)}: provider_ref '{o.get('provider_ref')}' not in organizations/")
    for r in entities.get("routes", []):
        if r.get("offering_ref") is not None and r["offering_ref"] not in offs:
            errors.append(f"{src(r)}: offering_ref '{r['offering_ref']}' not in offerings/")
        if r.get("router_ref") is not None and r["router_ref"] not in orgs:
            errors.append(f"{src(r)}: router_ref '{r['router_ref']}' not in organizations/")
        if r.get("inference_host_ref") is not None and r["inference_host_ref"] not in orgs:
            errors.append(f"{src(r)}: inference_host_ref '{r['inference_host_ref']}' not in organizations/")
    for a in entities.get("aliases", []):
        rr = a.get("route_ref")
        if rr is not None and rr not in rts:
            errors.append(f"{src(a)}: route_ref '{rr}' not in routes/")
    for p in entities.get("probes", []):
        if p.get("route_ref") not in rts:
            errors.append(f"{src(p)}: route_ref '{p.get('route_ref')}' not in routes/")
    for a in entities.get("assignments", []):
        for rr in a.get("allowed_route_refs", []):
            if rr not in rts:
                errors.append(f"{src(a)}: allowed_route_ref '{rr}' not in routes/")
    for i in entities.get("incidents", []):
        if i.get("route_ref") is not None and i["route_ref"] not in rts:
            errors.append(f"{src(i)}: route_ref '{i['route_ref']}' not in routes/")
    # releases referenced by families must also list the family (bidirectional)
    rel_fam = {r.get("release_id"): r.get("family_ref") for r in entities.get("releases", [])}
    for f in entities.get("families", []):
        for ref in f.get("release_refs", []):
            if ref in rel_fam and rel_fam[ref] != f.get("family_id"):
                errors.append(f"{src(f)}: release '{ref}' belongs to family '{rel_fam[ref]}'")
    return errors


def check_conflation(entities: dict[str, list[dict]]) -> list[str]:
    """An org only credited as developer where it declares model_developer."""
    errors: list[str] = []
    org_types = {o.get("organization_id"): set(o.get("organization_types", [])) for o in entities.get("organizations", [])}
    for f in entities.get("families", []):
        for ref in f.get("developer_refs", []):
            if ref in org_types and "model_developer" not in org_types[ref]:
                errors.append(
                    f"conflation: {ref} credited as developer of family '{f.get('family_id')}' "
                    f"but its organization_types lack model_developer"
                )
    for r in entities.get("releases", []):
        for ref in r.get("developer_refs", []):
            if ref in org_types and "model_developer" not in org_types[ref]:
                errors.append(f"conflation: {ref} credited as developer of release '{r.get('release_id')}' without model_developer type")
    return errors


def check_secrets(paths=None) -> list[str]:
    errors: list[str] = []
    paths = paths if paths is not None else _source_paths()
    for p in paths:
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        m = SECRET_PATTERNS.search(text)
        if m:
            errors.append(f"secret-like value '{m.group(0)[:6]}…' found in {p.relative_to(REGISTRY)}")
    return errors


def check_freshness_split(entities: dict[str, list[dict]]) -> list[str]:
    """family_freshness and route_freshness must stay separate and present."""
    warnings: list[str] = []
    today = date.today().isoformat()
    for r in entities.get("routes", []):
        rf = r.get("route_freshness", {})
        ra = rf.get("review_after")
        if ra and str(ra) < today:
            warnings.append(f"route {r.get('route_id')}: stale (review_after={ra}, action={rf.get('stale_action')})")
    for f in entities.get("families", []):
        ff = f.get("family_freshness", {})
        ra = ff.get("review_after")
        if ra and str(ra) < today:
            warnings.append(f"family {f.get('family_id')}: stale (review_after={ra})")
    return warnings


def check_probe_append_only(entities: dict[str, list[dict]]) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for p in entities.get("probes", []):
        pid = p.get("probe_id", "?")
        if pid in seen:
            errors.append(f"probe '{pid}' appears more than once — probes/ is append-only")
        seen.add(pid)
        if not re.fullmatch(r"probe-[0-9]{8}t[0-9]{6}z-[a-z0-9-]+", pid):
            errors.append(f"probe id '{pid}' violates naming grammar")
    return errors


# ── legacy catalog validation (preserved semantics) ────────────────────────────

def _to_str(val) -> str | None:
    if val is None:
        return None
    if isinstance(val, (date, datetime)):
        return val.isoformat()
    return str(val)


def validate_record(record: dict, schema: dict) -> list[str]:
    """Legacy catalog validation with two compat shims:
    - provider-projection files (no `identity`, e.g. zai.yaml) are provider maps, not model records
    - freshness-split files carry family_freshness/route_freshness instead of legacy `freshness`
    """
    errors: list[str] = []
    if "identity" not in record:
        if "provider" not in record:
            errors.append("catalog file has neither 'identity' (model record) nor 'provider' (provider projection)")
        return errors
    clean = {k: v for k, v in record.items() if not k.startswith("_")}
    if "freshness" not in clean and ("family_freshness" in clean or "route_freshness" in clean):
        clean["freshness"] = clean.get("family_freshness") or clean.get("route_freshness")
    if jsonschema and schema:
        try:
            jsonschema.validate(clean, schema)
        except jsonschema.ValidationError as e:
            errors.append(f"{e.json_path}: {e.message}")
        except Exception as e:  # noqa: BLE001
            errors.append(f"Schema error: {e}")
    else:
        required = ["schema_version", "identity", "capability", "hazards", "freshness"]
        for field in required:
            if field not in clean:
                errors.append(f"Missing required field: {field}")
        ident = clean.get("identity", {})
        if "id" not in ident:
            errors.append("identity.id missing")
        if "status" not in ident:
            errors.append("identity.status missing")
    return errors


def check_duplicates(records: list[dict]) -> list[str]:
    errors: list[str] = []
    seen: dict[str, str] = {}
    for r in records:
        model_id = r.get("identity", {}).get("id", "unknown")
        if model_id in seen:
            errors.append(f"Duplicate model ID '{model_id}' in {seen[model_id]} and {r.get('_source_file', '?')}")
        seen[model_id] = r.get("_source_file", "?")
    return errors


def check_evidence_refs(records: list[dict]) -> list[str]:
    warnings: list[str] = []
    for r in records:
        model_id = r.get("identity", {}).get("id", "unknown")
        refs = list(r.get("capability", {}).get("evidence_refs", []))
        for h in r.get("hazards", []):
            refs.extend(h.get("evidence_refs", []))
        for ref in refs:
            if ref.startswith("ev:") and len(ref.split(":")) < 3:
                warnings.append(f"{model_id}: malformed evidence ref '{ref}'")
    return warnings


def check_freshness(records: list[dict]) -> list[str]:
    warnings: list[str] = []
    today = date.today().isoformat()
    for r in records:
        model_id = r.get("identity", {}).get("id", "unknown")
        review_after = _to_str(r.get("freshness", {}).get("review_after"))
        if review_after and review_after < today:
            warnings.append(f"{model_id}: stale (review_after={review_after}, action={r.get('freshness', {}).get('stale_action', 'warn')})")
    return warnings


# ── legacy generated views (shape preserved) ───────────────────────────────────

def generate_federation_model(records: list[dict]) -> dict:
    models = []
    for r in records:
        ident = r.get("identity")
        if not ident or "id" not in ident:
            continue  # provider-projection file (e.g. zai.yaml) — not a model record
        cap = r.get("capability", {})
        hazards = r.get("hazards", [])
        freshness = r.get("freshness", {})
        severity_order = {"low": 0, "medium": 1, "high": 2, "critical": 3}
        max_severity = "low"
        floor_deltas: dict[str, str] = {}
        for h in hazards:
            sev = h.get("severity", "low")
            if severity_order.get(sev, 0) > severity_order.get(max_severity, 0):
                max_severity = sev
            for floor, delta in h.get("floor_deltas", {}).items():
                if delta != "standard":
                    floor_deltas[floor] = delta
        models.append({
            "model_key": ident["id"],
            "provider": ident.get("provider", "unknown"),
            "family": ident.get("family", "unknown"),
            "variant": ident.get("variant"),
            "route": ident.get("route", "unknown"),
            "status": ident.get("status", "unknown"),
            "context_window": ident.get("context_window"),
            "modality": ident.get("modality", []),
            "jurisdiction": ident.get("jurisdiction", "UNKNOWN"),
            "capabilities": cap.get("allowed_tasks", []),
            "capability_confidence": cap.get("confidence", "untested"),
            "hazards": [h["id"] for h in hazards if "id" in h],
            "max_hazard_severity": max_severity,
            "floor_deltas": floor_deltas,
            "forbidden": r.get("forbidden", []),
            "requires_human_ack_for": r.get("requires_human_ack_for", []),
            "censorship": r.get("censorship"),
            "pricing": r.get("pricing"),
            "freshness": {
                "review_after": _to_str(freshness.get("review_after")),
                "stale_action": freshness.get("stale_action"),
                "last_verified": _to_str(freshness.get("last_verified")),
            },
        })
    return {
        "schema": "arifos-federation-model-registry-v2",
        "compiler": "aaa-registry compile",
        "record_count": len(models),
        "models": models,
        "default_for_unlisted": {
            "risk_tier": "guarded",
            "forbidden": ["self_authorize", "seal_without_judge", "irreversible_commit"],
            "requires_human_ack_for": ["all_irreversible"],
        },
    }


def generate_index(records, errors, warnings, generated_at_iso: str) -> str:
    lines = [
        "# Model Registry Index",
        "",
        f"> **Compiled:** {generated_at_iso}",
        "> **Compiler:** aaa-registry compile (deterministic — timestamp derived from sources)",
        f"> **Records:** {len(records)}",
        "> **Authority:** F13 SOVEREIGN (Arif Fazil)",
        "",
        "---",
        "",
        "## Active models",
        "",
        "| ID | Provider | Status | Hazards | Confidence | Review After |",
        "|----|----------|--------|---------|------------|--------------|",
    ]
    for r in records:
        ident = r.get("identity", {})
        cap = r.get("capability", {})
        hazards = r.get("hazards", [])
        hc = len(hazards)
        hi = sum(1 for h in hazards if h.get("severity") in ("high", "critical"))
        lines.append(
            f"| `{ident.get('id', '?')}` | {ident.get('provider', '?')} | {ident.get('status', '?')} "
            f"| {hc} ({hi} high+) | {cap.get('confidence', '?')} | {_to_str(r.get('freshness', {}).get('review_after')) or '?'} |"
        )
    for title, items in (("Errors", errors), ("Warnings", warnings)):
        if items:
            lines.extend(["", f"## {title}", ""])
            lines.extend(f"- {'❌' if title == 'Errors' else '⚠️'} {e}" for e in items)
    lines.extend(["", "---", "", "*Generated by aaa-registry compile. Do not hand-edit.*", "*DITEMPA BUKAN DIBERI*", ""])
    return "\n".join(lines) + "\n"


def generate_model_state(records: list[dict]) -> dict:
    models: dict[str, dict] = {}
    severity_rank = {"low": 0, "medium": 1, "high": 2, "critical": 3}
    today = date.today().isoformat()
    for r in records:
        ident = r.get("identity", {})
        model_id = ident.get("id", "unknown")
        freshness = r.get("freshness", {})
        review_str = _to_str(freshness.get("review_after"))
        is_stale = review_str is not None and review_str < today
        hazards = r.get("hazards", [])
        max_sev, max_rank = "none", -1
        for h in hazards:
            rank = severity_rank.get(h.get("severity", "low"), 0)
            if rank > max_rank:
                max_rank, max_sev = rank, h.get("severity", "low")
        models[model_id] = {
            "status": ident.get("status", "unknown"),
            "stale": is_stale,
            "stale_action": freshness.get("stale_action") if is_stale else None,
            "hazard_count": len(hazards),
            "max_severity": max_sev,
            "confidence": r.get("capability", {}).get("confidence", "untested"),
        }
    return {"models": models}


# ── normalized projections ─────────────────────────────────────────────────────

def _projection_meta(generated_at_iso: str) -> dict:
    return {
        "generated": True,
        "generator_version": GENERATOR_VERSION,
        "source_commit": source_commit(),
        "generated_at": generated_at_iso,
        "source_paths": [str(p.relative_to(REGISTRY)) for p in _source_paths()],
    }


def build_provider_map(entities: dict[str, list[dict]]) -> dict:
    orgs = {o["organization_id"]: o for o in entities.get("organizations", [])}
    out: dict[str, dict] = {}
    for o in entities.get("organizations", []):
        oid = o["organization_id"]
        out[oid] = {
            "canonical_name": o.get("canonical_name"),
            "organization_types": o.get("organization_types", []),
            "jurisdiction": o.get("jurisdiction", {}).get("value") if isinstance(o.get("jurisdiction"), dict) else None,
            "evidence_status": o.get("evidence_status"),
            "offerings": [],
        }
    off_by_org: dict[str, list] = {}
    for off in entities.get("offerings", []):
        off_by_org.setdefault(off.get("provider_ref", "?"), []).append({
            "offering_id": off.get("offering_id"),
            "plan": off.get("plan"),
            "billing_class": off.get("billing_class"),
            "alias_policy": off.get("alias_policy"),
            "quota_state": off.get("quota_state"),
            "advertised_model_count": len(off.get("advertised_models", [])),
            "routes": [r.get("route_id") for r in entities.get("routes", []) if r.get("offering_ref") == off.get("offering_id")],
        })
    for oid, offs in off_by_org.items():
        if oid in out:
            out[oid]["offerings"] = offs
    return out


def build_family_tree(entities: dict[str, list[dict]]) -> dict:
    tree: dict[str, dict] = {}
    rels_by_fam: dict[str, list] = {}
    for r in entities.get("releases", []):
        rels_by_fam.setdefault(r.get("family_ref", "?"), []).append({
            "release_id": r.get("release_id"),
            "lifecycle": (r.get("lifecycle") or {}).get("status"),
            "distribution": r.get("distribution"),
            "release_date": (r.get("release_date") or {}).get("value"),
            "knowledge_cutoff": (r.get("knowledge_cutoff") or {}).get("value"),
            "developer_refs": r.get("developer_refs", []),
        })
    for f in entities.get("families", []):
        fid = f.get("family_id")
        tree[fid] = {
            "canonical_name": f.get("canonical_name"),
            "developer_refs": f.get("developer_refs", []),
            "lineage_evidence": f.get("lineage_evidence"),
            "family_freshness": f.get("family_freshness"),
            "releases": rels_by_fam.get(fid, []),
        }
    return tree


def build_route_resolution_map(entities: dict[str, list[dict]]) -> dict:
    latest_probe: dict[str, dict] = {}
    for p in sorted(entities.get("probes", []), key=lambda x: x.get("observed_at", "")):
        latest_probe[p.get("route_ref")] = {
            "probe_id": p.get("probe_id"),
            "observed_at": p.get("observed_at"),
            "requested_model": p.get("requested_model"),
            "resolved_model": p.get("resolved_model"),
            "http_status": p.get("http_status"),
            "verdict": p.get("verdict"),
            "evidence_status": p.get("evidence_status"),
        }
    out: dict[str, dict] = {}
    for r in entities.get("routes", []):
        rid = r.get("route_id")
        out[rid] = {
            "offering_ref": r.get("offering_ref"),
            "router_ref": r.get("router_ref"),
            "protocol": r.get("protocol"),
            "endpoint_ref": r.get("endpoint_ref"),
            "mutability_class": r.get("mutability_class"),
            "failure_domain": r.get("failure_domain"),
            "route_freshness": r.get("route_freshness"),
            "aliases": [
                {"alias_id": a.get("alias_id"), "requested_model": a.get("requested_model"),
                 "expected_resolution": a.get("expected_resolution"),
                 "resolution_policy": a.get("resolution_policy"),
                 "mismatch_verdict": a.get("mismatch_verdict")}
                for a in entities.get("aliases", []) if a.get("route_ref") == rid
            ],
            "latest_probe": latest_probe.get(rid),
        }
    return out


def build_agent_assignment_map(entities: dict[str, list[dict]]) -> dict:
    fd_by_route = {r.get("route_id"): r.get("failure_domain") for r in entities.get("routes", [])}
    out = []
    for a in entities.get("assignments", []):
        out.append({
            "assignment_id": a.get("assignment_id"),
            "AAA_role": a.get("AAA_role"),
            "allowed_model_refs": a.get("allowed_model_refs", []),
            "allowed_route_refs": a.get("allowed_route_refs", []),
            "failure_domains": [fd_by_route.get(rr) for rr in a.get("allowed_route_refs", [])],
            "independence": a.get("independence"),
            "forbidden_tasks": a.get("forbidden_tasks", []),
            "data_boundary": a.get("data_boundary"),
        })
    return {"assignments": out}


def build_freshness_report(entities: dict[str, list[dict]], generated_at_iso: str) -> dict:
    today = generated_at_iso[:10]
    fam_rows, route_rows = [], []
    for f in entities.get("families", []):
        ff = f.get("family_freshness", {})
        ra = _to_str(ff.get("review_after"))
        fam_rows.append({
            "family_id": f.get("family_id"), "scope": "family",
            "last_verified": _to_str(ff.get("last_verified")), "review_after": ra,
            "stale": bool(ra and ra < today), "stale_action": ff.get("stale_action"),
        })
    for r in entities.get("routes", []):
        rf = r.get("route_freshness", {})
        ra = _to_str(rf.get("review_after"))
        route_rows.append({
            "route_id": r.get("route_id"), "scope": "route",
            "last_verified": _to_str(rf.get("last_verified")), "review_after": ra,
            "stale": bool(ra and ra < today), "stale_action": rf.get("stale_action"),
        })
    return {"family_freshness": fam_rows, "route_freshness": route_rows}


def build_drift_report(entities: dict[str, list[dict]]) -> dict:
    return {
        "open_unverified_incidents": [
            {"incident_id": i.get("incident_id"), "type": i.get("incident_type"),
             "status": i.get("status"), "evidence_status": i.get("evidence_status"),
             "requested_model": i.get("requested_model"), "resolved_model": i.get("resolved_model")}
            for i in entities.get("incidents", []) if i.get("status") in ("open", "UNVERIFIED")
        ],
        "all_incidents_preserved": len(entities.get("incidents", [])),
        "floating_aliases": [
            {"alias_id": a.get("alias_id"), "route_ref": a.get("route_ref"),
             "requested_model": a.get("requested_model"), "expected_resolution": a.get("expected_resolution")}
            for a in entities.get("aliases", []) if a.get("resolution_policy") in ("floating", "UNKNOWN")
        ],
        "floating_mutability_routes": [
            r.get("route_id") for r in entities.get("routes", [])
            if str(r.get("mutability_class", "")).endswith("FLOATING")
        ],
        "unknown_developer_families": [
            f.get("family_id") for f in entities.get("families", []) if not f.get("developer_refs")
        ],
    }


# ── main ───────────────────────────────────────────────────────────────────────

def compile_registry() -> int:
    print("=" * 60)
    print("aaa-registry compile (supply-chain v2)")
    print("=" * 60)

    entities = load_entities()
    catalog = load_catalog()
    generated_at = derived_generated_at()
    print(f"\nLoaded entities: " + ", ".join(f"{d}={len(v)}" for d, v in entities.items() if v))
    print(f"Loaded legacy catalog records: {len(catalog)}")
    print(f"Derived generated_at: {generated_at}")

    errors: list[str] = []
    warnings: list[str] = []

    errors += validate_entity_schemas(entities)
    errors += check_duplicate_ids(entities)
    errors += check_references(entities)
    errors += check_conflation(entities)
    errors += check_secrets()
    errors += check_probe_append_only(entities)
    warnings += check_freshness_split(entities)

    schema = load_schema()
    for r in catalog:
        for e in validate_record(r, schema):
            errors.append(f"{r.get('_source_file', '?')}: {e}")
    errors += check_duplicates(catalog)
    warnings += check_evidence_refs(catalog)
    warnings += check_freshness(catalog)

    print(f"\nValidation: {len(errors)} errors, {len(warnings)} warnings")
    for e in errors:
        print(f"  ❌ {e}")
    for w in warnings:
        print(f"  ⚠️ {w}")

    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    COMPILED_DIR.mkdir(parents=True, exist_ok=True)

    meta = _projection_meta(generated_at)

    def emit(name: str, payload: dict) -> None:
        doc = dict(meta)
        doc.update(payload)
        (GENERATED_DIR / name).write_text(dumps(doc), encoding="utf-8")

    emit("catalog.json", {"entities": {d: [{k: v for k, v in r.items() if not k.startswith("_")} for r in v] for d, v in entities.items()},
                          "legacy_catalog_records": len(catalog)})
    emit("provider-map.json", {"providers": build_provider_map(entities)})
    emit("family-tree.json", {"families": build_family_tree(entities)})
    emit("route-resolution-map.json", {"routes": build_route_resolution_map(entities)})
    emit("agent-assignment-map.json", build_agent_assignment_map(entities))
    emit("freshness-report.json", build_freshness_report(entities, generated_at))
    emit("drift-report.json", build_drift_report(entities))

    fed_model = generate_federation_model(catalog)
    fed_model["compiled_at"] = generated_at
    fed_json = dumps(fed_model)
    (COMPILED_DIR / "FEDERATION_MODEL.json").write_text(fed_json, encoding="utf-8")

    index_md = generate_index(catalog, errors, warnings, generated_at)
    (COMPILED_DIR / "REGISTRY_INDEX.md").write_text(index_md, encoding="utf-8")

    model_state = generate_model_state(catalog)
    state_json = dumps(model_state)
    (COMPILED_DIR / "model-state.json").write_text(state_json, encoding="utf-8")

    gen_hashes = {p.name: content_hash(p.read_text(encoding="utf-8")) for p in sorted(GENERATED_DIR.glob("*.json"))}
    manifest = {
        "compiled_at": generated_at,
        "compiler": "aaa-registry compile",
        "generator_version": GENERATOR_VERSION,
        "source_commit": meta["source_commit"],
        "record_count": len(catalog),
        "entity_counts": {d: len(v) for d, v in entities.items()},
        "errors": len(errors),
        "warnings": len(warnings),
        "hashes": {
            "FEDERATION_MODEL.json": content_hash(fed_json),
            "REGISTRY_INDEX.md": content_hash(index_md),
            "model-state.json": content_hash(state_json),
            **gen_hashes,
        },
    }
    (COMPILED_DIR / "manifest.json").write_text(dumps(manifest), encoding="utf-8")
    print(f"\nGenerated {len(gen_hashes)} projections + 4 legacy views")
    print(f"Registry digest: {content_hash(manifest)[:16]}…")

    if errors:
        print(f"\n⚠️  {len(errors)} errors — review before deploying")
        return 1
    print("\n✅ Compile complete — no errors")
    return 0


if __name__ == "__main__":
    sys.exit(compile_registry())
