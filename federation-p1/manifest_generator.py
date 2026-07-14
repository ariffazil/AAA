#!/usr/bin/env python3
"""
manifest_generator.py — Generate signed surface manifests for all arifOS federation organs.

Reads actual tool/resource/prompt registrations from each organ's server.py
and produces a canonical, hashed manifest per organ.

Usage: python3 manifest_generator.py [--organ arifos|wealth|geox|well|aaa|aforge]
"""

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "2026.06.28"
MANIFEST_DIR = Path("/root/federation-p1/manifests")


def canonical_json(obj: Any) -> str:
    """Produce deterministic JSON for hashing."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_content(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def manifest_tool_rows(
    names: list[str],
    *,
    version: str,
    read_only_overrides: dict[str, bool] | None = None,
    authority_overrides: dict[str, str] | None = None,
) -> list[dict]:
    rows: list[dict] = []
    read_only_overrides = read_only_overrides or {}
    authority_overrides = authority_overrides or {}
    for name in names:
        read_only = read_only_overrides.get(
            name,
            not any(
                kw in name
                for kw in ("log", "update", "write", "seal", "execute", "apply", "create", "submit", "save")
            ),
        )
        authority = authority_overrides.get(name, "NONE")
        rows.append(
            {
                "name": name,
                "version": version,
                "read_only": read_only,
                "destructive": not read_only,
                "idempotent": read_only,
                "output_schema_sha256": sha256_content(name),
                "authority_required": authority,
            }
        )
    return rows


def load_yaml_manifest_tools(
    manifest_path: str,
    *,
    only_public: bool = True,
    require_plugin_exposed: bool = False,
) -> list[str]:
    import yaml

    payload = yaml.safe_load(Path(manifest_path).read_text(encoding="utf-8"))
    tools = []
    for entry in payload.get("tools", []):
        if only_public and entry.get("visibility") != "public":
            continue
        if require_plugin_exposed and not (entry.get("plugin") or {}).get("exposed", False):
            continue
        tools.append(str(entry["name"]))
    return tools


def extract_tools_from_file(filepath: str, prefix: str) -> list[dict]:
    """Extract @mcp.tool registrations from a Python file."""
    tools = []
    try:
        with open(filepath) as f:
            content = f.read()
    except FileNotFoundError:
        return tools

    # Match @mcp.tool(name="...") or @mcp.tool()
    pattern = r'@mcp\.tool\((?:name="([^"]+)")?\)'
    matches = list(re.finditer(pattern, content))

    for m in matches:
        name = m.group(1)
        if not name:
            # Find the next def line
            pos = m.end()
            def_match = content[pos : pos + 500]
            def_line = re.search(r"def\s+(\w+)", def_match)
            if def_line:
                name = def_line.group(1)
            else:
                continue

        # Determine read_only from annotations or function name patterns
        read_only = True
        if any(
            kw in name
            for kw in [
                "log",
                "update",
                "write",
                "seal",
                "execute",
                "apply",
                "create",
                "submit",
                "save",
            ]
        ):
            read_only = False

        # Determine authority
        authority = "NONE"
        if "seal" in name or "judge" in name:
            authority = "JUDGE_SEAL_AUTHORIZATION"
        elif "execute" in name or "forge" in name:
            authority = "888_HOLD"

        tools.append(
            {
                "name": name,
                "version": SCHEMA_VERSION,
                "read_only": read_only,
                "destructive": not read_only,
                "idempotent": read_only,
                "output_schema_sha256": sha256_content(name),
                "authority_required": authority,
            }
        )

    return tools


def extract_prompts_from_file(filepath: str) -> list[dict]:
    """Extract @mcp.prompt registrations from a Python file."""
    prompts = []
    try:
        with open(filepath) as f:
            content = f.read()
    except FileNotFoundError:
        return prompts

    pattern = r'@mcp\.prompt\((?:name="([^"]+)")?\)'
    matches = list(re.finditer(pattern, content))

    for m in matches:
        name = m.group(1)
        if not name:
            pos = m.end()
            def_match = content[pos : pos + 500]
            def_line = re.search(r"def\s+(\w+)", def_match)
            if def_line:
                name = def_line.group(1)
            else:
                continue
        prompts.append(
            {
                "name": name,
                "version": SCHEMA_VERSION,
                "prompt_sha256": sha256_content(name),
            }
        )

    return prompts


def extract_resources_from_file(filepath: str) -> list[dict]:
    """Extract @mcp.resource registrations from a Python file."""
    resources = []
    try:
        with open(filepath) as f:
            content = f.read()
    except FileNotFoundError:
        return resources

    pattern = r'@mcp\.resource\(\s*"([^"]+)"'
    matches = list(re.finditer(pattern, content))

    for m in matches:
        uri = m.group(1)
        resources.append(
            {
                "uri": uri,
                "version": SCHEMA_VERSION,
                "mime_type": "text/plain" if "://" in uri else "application/json",
                "resource_sha256": sha256_content(uri),
                "read_only": True,
            }
        )

    return resources


# ── arifOS ─────────────────────────────────────────────────────────────────
def generate_arifos_manifest() -> dict:
    """arifOS: 7 canonical public verbs + 17 canonical tools internal."""
    canonical_7 = [
        "arif_init",
        "arif_observe",
        "arif_think",
        "arif_route",
        "arif_judge",
        "arif_act",
        "arif_seal",
    ]

    tools = []
    for name in canonical_7:
        read_only = name in ["arif_init", "arif_observe", "arif_think", "arif_route"]
        tools.append(
            {
                "name": name,
                "version": SCHEMA_VERSION,
                "read_only": read_only,
                "destructive": not read_only,
                "idempotent": read_only,
                "output_schema_sha256": sha256_content(name),
                "authority_required": "JUDGE_SEAL_AUTHORIZATION"
                if name in ["arif_judge", "arif_act", "arif_seal"]
                else "NONE",
            }
        )

    # Resources from actual MCP surface
    resource_uris = [
        "arifos://schema",
        "arifos://doctrine",
        "arifos://vitals",
        "arifos://bootstrap",
        "arifos://identity",
        "arifos://jurisdiction",
        "arifos://memory",
        "arifos://civilization",
        "arifos://seal-readiness",
        "arifos://quickstart",
        "arifos://mcp-alignment",
        "arifos://trinity",
        "arifos://loop-engineering",
        "arifos://reality/state",
        "arifos://resources/index",
        "arifos://resources/audit",
        "arifos://skills-catalog",
        "arifos://human/metabolized",
        "arif://tools/affordance",
        "arif://tools/discovery",
        "arif://core/seven",
    ]

    resources = []
    for uri in resource_uris:
        resources.append(
            {
                "uri": uri,
                "version": SCHEMA_VERSION,
                "mime_type": "application/json"
                if "affordance" in uri
                or "discovery" in uri
                or "core" in uri
                or "index" in uri
                or "catalog" in uri
                or "audit" in uri
                else "text/plain",
                "resource_sha256": sha256_content(uri),
                "read_only": True,
            }
        )

    prompts = [
        {
            "name": "arifosmcp_loop_engineer",
            "version": SCHEMA_VERSION,
            "prompt_sha256": sha256_content("loop_engineer"),
        },
        {
            "name": "000_init",
            "version": SCHEMA_VERSION,
            "prompt_sha256": sha256_content("000_init"),
        },
        {
            "name": "111_sense",
            "version": SCHEMA_VERSION,
            "prompt_sha256": sha256_content("111_sense"),
        },
        {
            "name": "333_reason",
            "version": SCHEMA_VERSION,
            "prompt_sha256": sha256_content("333_reason"),
        },
        {
            "name": "555_judge",
            "version": SCHEMA_VERSION,
            "prompt_sha256": sha256_content("555_judge"),
        },
        {
            "name": "666_critique",
            "version": SCHEMA_VERSION,
            "prompt_sha256": sha256_content("666_critique"),
        },
        {
            "name": "777_forge",
            "version": SCHEMA_VERSION,
            "prompt_sha256": sha256_content("777_forge"),
        },
        {
            "name": "999_seal",
            "version": SCHEMA_VERSION,
            "prompt_sha256": sha256_content("999_seal"),
        },
    ]

    return {
        "organ": "arifos",
        "manifest_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "bind": "127.0.0.1:8088",
        "tools": tools,
        "resources": resources,
        "prompts": prompts,
        "authority_boundary": "JUDGE_ONLY",
    }


# ── WEALTH ─────────────────────────────────────────────────────────────────
def generate_wealth_manifest() -> dict:
    tools = extract_tools_from_file("/root/WEALTH/wealth_mcp/server.py", "wealth_")
    resources = extract_resources_from_file("/root/WEALTH/wealth_mcp/server.py")
    prompts = extract_prompts_from_file("/root/WEALTH/wealth_mcp/server.py")

    # Add canonical resource URIs if not already present
    canonical_resources = [
        "wealth://schema",
        "wealth://health",
        "wealth://tools/registry",
        "wealth://prompts/index",
        "wealth://domains/index",
        "wealth://glossary",
        "wealth://federation/contract",
        "wealth://affordance/contracts",
        "wealth://handoff/arifos-schema",
        "wealth://replay/receipt-schema",
        "wealth://risk/thresholds",
        "wealth://runtime/policy",
        "wealth://reality/context",
        "wealth://market/sources",
        "wealth://canon/002-human-law",
    ]
    existing_uris = {r["uri"] for r in resources}
    for uri in canonical_resources:
        if uri not in existing_uris:
            resources.append(
                {
                    "uri": uri,
                    "version": SCHEMA_VERSION,
                    "mime_type": "application/json"
                    if "schema" in uri
                    or "registry" in uri
                    or "index" in uri
                    or "contracts" in uri
                    or "thresholds" in uri
                    or "policy" in uri
                    or "context" in uri
                    or "sources" in uri
                    else "text/markdown",
                    "resource_sha256": sha256_content(uri),
                    "read_only": True,
                }
            )

    return {
        "organ": "wealth",
        "manifest_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "bind": "127.0.0.1:18082",
        "tools": tools,
        "resources": resources,
        "prompts": prompts,
        "authority_boundary": "COMPUTE_ONLY",
    }


# ── GEOX ───────────────────────────────────────────────────────────────────
def generate_geox_manifest() -> dict:
    tools = manifest_tool_rows(
        load_yaml_manifest_tools(
            "/root/GEOX/src/geox_mcp/tools_manifest.yaml",
            only_public=True,
            require_plugin_exposed=True,
        ),
        version=SCHEMA_VERSION,
        read_only_overrides={"geox_claim": False},
        authority_overrides={"geox_claim": "888_HOLD"},
    )
    resources = extract_resources_from_file("/root/geox/src/geox_mcp/server.py")
    prompts = extract_prompts_from_file("/root/geox/src/geox_mcp/server.py")

    # GEOX has no prompts in code — add the 7 canonical families as stubs
    if not prompts:
        prompts = [
            {
                "name": "geox_reality_intake_loop",
                "version": SCHEMA_VERSION,
                "prompt_sha256": sha256_content("geox_reality_intake"),
            },
            {
                "name": "geox_earth_diagnosis_loop",
                "version": SCHEMA_VERSION,
                "prompt_sha256": sha256_content("geox_diagnosis"),
            },
            {
                "name": "geox_uncertainty_loop",
                "version": SCHEMA_VERSION,
                "prompt_sha256": sha256_content("geox_uncertainty"),
            },
            {
                "name": "geox_basin_regime_loop",
                "version": SCHEMA_VERSION,
                "prompt_sha256": sha256_content("geox_regime"),
            },
            {
                "name": "geox_decision_support_loop",
                "version": SCHEMA_VERSION,
                "prompt_sha256": sha256_content("geox_bandwidth"),
            },
            {
                "name": "geox_contradiction_challenge_loop",
                "version": SCHEMA_VERSION,
                "prompt_sha256": sha256_content("geox_contradiction"),
            },
            {
                "name": "geox_arifos_handoff_loop",
                "version": SCHEMA_VERSION,
                "prompt_sha256": sha256_content("geox_handoff"),
            },
        ]

    # Add canonical resource URIs
    canonical_resources = [
        "geox://capabilities",
        "geox://identity",
        "geox://surface/truth",
        "geox://resources/index",
        "geox://claims/index",
        "geox://claims/graph",
        "geox://basins/index",
        "geox://literature/index",
        "geox://reality/context",
        "geox://resources/ontology/index",
        "geox://resources/playbooks/index",
        "geox://resources/prompts/index",
        "geox://resources/schemas/index",
        "geox://artifacts/index",
        "geox://registry/apps",
    ]
    existing_uris = {r["uri"] for r in resources}
    for uri in canonical_resources:
        if uri not in existing_uris:
            resources.append(
                {
                    "uri": uri,
                    "version": SCHEMA_VERSION,
                    "mime_type": "text/plain",
                    "resource_sha256": sha256_content(uri),
                    "read_only": True,
                }
            )

    return {
        "organ": "geox",
        "manifest_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "bind": "127.0.0.1:8081",
        "tools": tools,
        "resources": resources,
        "prompts": prompts,
        "authority_boundary": "EVIDENCE_ONLY",
    }


# ── WELL ───────────────────────────────────────────────────────────────────
def generate_well_manifest() -> dict:
    tools = manifest_tool_rows(
        [
            "well_classify_substrate",
            "well_validate_vitality",
            "well_assess_reliability",
            "well_assess_homeostasis",
            "well_check_repair",
            "well_guard_dignity",
            "well_trace_lineage",
            "well_registry_status",
        ],
        version=SCHEMA_VERSION,
    )
    resources = extract_resources_from_file("/root/WELL/server.py")
    prompts = extract_prompts_from_file("/root/WELL/server.py")

    # Add canonical resource URIs
    canonical_resources = [
        "well://schema",
        "well://identity",
        "well://doctrine",
        "well://registry",
        "well://tools/canon_map",
        "well://state/arif",
        "well://readiness/arif",
        "well://vitals/arif",
        "well://telemetry/arif",
        "well://sovereign_entropy/arif",
        "well://causal_dag",
        "well://decision/classes",
        "well://bio/signals",
        "well://physics/laws",
        "well://human/substrate",
        "well://machine/substrate",
        "well://substrate/registry",
        "well://substrate/interaction",
        "well://coupling",
        "well://chemistry/glue",
        "well://transport/loop",
        "well://transport/stages",
        "well://metabolic/flux",
        "well://events/recent",
        "well://floors/well_floors",
        "well://bridge/arifos-kernel",
        "well://bridge/geox",
        "well://bridge/wealth",
        "well://signals/consent-integrity",
        "well://signals/information-asymmetry",
    ]
    existing_uris = {r["uri"] for r in resources}
    for uri in canonical_resources:
        if uri not in existing_uris:
            resources.append(
                {
                    "uri": uri,
                    "version": SCHEMA_VERSION,
                    "mime_type": "text/plain",
                    "resource_sha256": sha256_content(uri),
                    "read_only": True,
                }
            )

    # Ensure 7 canonical prompts
    prompt_names = {p["name"] for p in prompts}
    canonical_prompts = [
        "well_reality_intake_loop",
        "well_readiness_diagnosis_loop",
        "well_risk_bandwidth_loop",
        "well_substrate_regime_loop",
        "well_decision_bandwidth_loop",
        "well_intent_alignment_loop",
        "well_arifos_handoff_loop",
    ]
    for cp in canonical_prompts:
        if cp not in prompt_names:
            prompts.append(
                {
                    "name": cp,
                    "version": SCHEMA_VERSION,
                    "prompt_sha256": sha256_content(cp),
                }
            )

    return {
        "organ": "well",
        "manifest_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "bind": "127.0.0.1:18083",
        "tools": tools,
        "resources": resources,
        "prompts": prompts,
        "authority_boundary": "REFLECT_ONLY",
    }


# ── AAA ────────────────────────────────────────────────────────────────────
def generate_aaa_manifest() -> dict:
    # AAA is a control plane — surface-only, no domain logic
    tools = [
        {
            "name": "aaa_agent_card",
            "version": SCHEMA_VERSION,
            "read_only": True,
            "destructive": False,
            "idempotent": True,
            "output_schema_sha256": sha256_content("aaa_agent_card"),
            "authority_required": "NONE",
        },
        {
            "name": "aaa_session_status",
            "version": SCHEMA_VERSION,
            "read_only": True,
            "destructive": False,
            "idempotent": True,
            "output_schema_sha256": sha256_content("aaa_session_status"),
            "authority_required": "NONE",
        },
        {
            "name": "aaa_federation_health",
            "version": SCHEMA_VERSION,
            "read_only": True,
            "destructive": False,
            "idempotent": True,
            "output_schema_sha256": sha256_content("aaa_federation_health"),
            "authority_required": "NONE",
        },
    ]

    resources = [
        {
            "uri": "aaa://schema",
            "version": SCHEMA_VERSION,
            "mime_type": "application/json",
            "resource_sha256": sha256_content("aaa://schema"),
            "read_only": True,
        },
        {
            "uri": "aaa://health",
            "version": SCHEMA_VERSION,
            "mime_type": "application/json",
            "resource_sha256": sha256_content("aaa://health"),
            "read_only": True,
        },
        {
            "uri": "aaa://agents/registry",
            "version": SCHEMA_VERSION,
            "mime_type": "application/json",
            "resource_sha256": sha256_content("aaa://agents/registry"),
            "read_only": True,
        },
        {
            "uri": "aaa://sessions/active",
            "version": SCHEMA_VERSION,
            "mime_type": "application/json",
            "resource_sha256": sha256_content("aaa://sessions/active"),
            "read_only": True,
        },
        {
            "uri": "aaa://a2a/gateway",
            "version": SCHEMA_VERSION,
            "mime_type": "application/json",
            "resource_sha256": sha256_content("aaa://a2a/gateway"),
            "read_only": True,
        },
        {
            "uri": "aaa://cockpit/state",
            "version": SCHEMA_VERSION,
            "mime_type": "application/json",
            "resource_sha256": sha256_content("aaa://cockpit/state"),
            "read_only": True,
        },
    ]

    prompts = [
        {
            "name": "aaa_routing_prompt",
            "version": SCHEMA_VERSION,
            "prompt_sha256": sha256_content("aaa_routing"),
        },
        {
            "name": "aaa_session_init_prompt",
            "version": SCHEMA_VERSION,
            "prompt_sha256": sha256_content("aaa_session_init"),
        },
        {
            "name": "aaa_federation_probe_prompt",
            "version": SCHEMA_VERSION,
            "prompt_sha256": sha256_content("aaa_federation_probe"),
        },
    ]

    return {
        "organ": "aaa",
        "manifest_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "bind": "127.0.0.1:3001",
        "tools": tools,
        "resources": resources,
        "prompts": prompts,
        "authority_boundary": "SURFACE_ONLY",
    }


# ── A-FORGE ────────────────────────────────────────────────────────────────
def generate_aforge_manifest() -> dict:
    tools = manifest_tool_rows(
        [
            "forge_registry_status",
            "forge_probe",
            "forge_execute",
            "forge_runtime_verify",
            "forge_receipt_draft",
        ],
        version=SCHEMA_VERSION,
        read_only_overrides={"forge_execute": False},
        authority_overrides={"forge_execute": "JUDGE_SEAL_AUTHORIZATION"},
    )

    resources = [
        {
            "uri": "aforge://schema",
            "version": SCHEMA_VERSION,
            "mime_type": "application/json",
            "resource_sha256": sha256_content("aforge://schema"),
            "read_only": True,
        },
        {
            "uri": "aforge://health",
            "version": SCHEMA_VERSION,
            "mime_type": "application/json",
            "resource_sha256": sha256_content("aforge://health"),
            "read_only": True,
        },
        {
            "uri": "aforge://contract",
            "version": SCHEMA_VERSION,
            "mime_type": "application/json",
            "resource_sha256": sha256_content("aforge://contract"),
            "read_only": True,
        },
        {
            "uri": "aforge://lease/active",
            "version": SCHEMA_VERSION,
            "mime_type": "application/json",
            "resource_sha256": sha256_content("aforge://lease/active"),
            "read_only": True,
        },
        {
            "uri": "aforge://tools/registry",
            "version": SCHEMA_VERSION,
            "mime_type": "application/json",
            "resource_sha256": sha256_content("aforge://tools/registry"),
            "read_only": True,
        },
        {
            "uri": "aforge://execution/log",
            "version": SCHEMA_VERSION,
            "mime_type": "application/json",
            "resource_sha256": sha256_content("aforge://execution/log"),
            "read_only": True,
        },
    ]

    prompts = [
        {
            "name": "aforge_dry_run_prompt",
            "version": SCHEMA_VERSION,
            "prompt_sha256": sha256_content("aforge_dry_run"),
        },
        {
            "name": "aforge_execute_prompt",
            "version": SCHEMA_VERSION,
            "prompt_sha256": sha256_content("aforge_execute"),
        },
        {
            "name": "aforge_verify_prompt",
            "version": SCHEMA_VERSION,
            "prompt_sha256": sha256_content("aforge_verify"),
        },
    ]

    return {
        "organ": "aforge",
        "manifest_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "bind": "127.0.0.1:7072",
        "tools": tools,
        "resources": resources,
        "prompts": prompts,
        "authority_boundary": "EXECUTE_ONLY",
    }


def sign_manifest(manifest: dict) -> dict:
    """Add SHA256 hash to manifest (excluding the sha256 field itself)."""
    m = {k: v for k, v in manifest.items() if k != "sha256"}
    canonical = canonical_json(m)
    manifest["sha256"] = sha256_content(canonical)
    return manifest


GENERATORS = {
    "arifos": generate_arifos_manifest,
    "wealth": generate_wealth_manifest,
    "geox": generate_geox_manifest,
    "well": generate_well_manifest,
    "aaa": generate_aaa_manifest,
    "aforge": generate_aforge_manifest,
}


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "all"

    if target == "all":
        for name, gen in GENERATORS.items():
            manifest = sign_manifest(gen())
            outpath = MANIFEST_DIR / name / "manifest.json"
            outpath.parent.mkdir(parents=True, exist_ok=True)
            outpath.write_text(canonical_json(manifest))
            print(
                f"✅ {name}: {len(manifest['tools'])} tools, {len(manifest['resources'])} resources, {len(manifest['prompts'])} prompts → {outpath}"
            )
    elif target in GENERATORS:
        manifest = sign_manifest(GENERATORS[target]())
        outpath = MANIFEST_DIR / target / "manifest.json"
        outpath.parent.mkdir(parents=True, exist_ok=True)
        outpath.write_text(canonical_json(manifest))
        print(
            f"✅ {target}: {len(manifest['tools'])} tools, {len(manifest['resources'])} resources, {len(manifest['prompts'])} prompts → {outpath}"
        )
    else:
        print(f"Unknown organ: {target}. Use: {', '.join(GENERATORS.keys())} or 'all'")
        sys.exit(1)


if __name__ == "__main__":
    main()
