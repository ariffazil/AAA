#!/usr/bin/env python3
"""
route_task — Model routing intelligence for arifOS federation.

Reads MODEL_TOOL_MANIFEST.json, classifies task by keywords,
returns best runtime with reason, tools, authority, verdict.

Usage:
    python3 route_task.py "Find latest oil price"
    python3 route_task.py "Run federation health check"
    python3 route_task.py "Find ARIF's PETRONAS emails about Kinabalu"

Exit codes: 0=routed, 1=no capable runtime, 2=manifest missing
"""

import json
import sys
import os
import re

MANIFEST = "/root/AAA/docs/MODEL_TOOL_MANIFEST.json"

# ── Domain classification rules ──────────────────────────────────
# Each rule: (domain, keywords, priority)
# Higher priority = checked first. First match wins.

RULES = [
    # Enterprise / M365
    (
        "enterprise_search",
        [
            "petronas",
            "email",
            "outlook",
            "calendar",
            "meeting",
            "teams",
            "sharepoint",
            "onedrive",
            "m365",
            "copilot",
            "office365",
            "my emails",
            "my calendar",
            "schedule meeting",
        ],
        100,
    ),
    # Web research (live data)
    (
        "web_research",
        [
            "latest",
            "current",
            "today",
            "news",
            "search the web",
            "find online",
            "look up",
            "what is the price",
            "exchange rate",
            "oil price",
            "stock price",
            "market data",
        ],
        90,
    ),
    # Computation (needs code execution)
    (
        "computation",
        [
            "calculate",
            "compute",
            "run code",
            "execute python",
            "monte carlo",
            "simulation",
            "npv",
            "irr",
            "fibonacci",
            "plot",
            "chart",
            "graph",
            "analyze data",
        ],
        85,
    ),
    # GEOX domain
    (
        "geox",
        [
            "seismic",
            "well log",
            "petrophysics",
            "basin",
            "stratigraphy",
            "porosity",
            "permeability",
            "geological",
            "reservoir",
            "prospect",
            "volumetrics",
            "well tie",
            "biostrat",
            "geophysics",
            "well correlation",
        ],
        80,
    ),
    # WEALTH domain
    (
        "wealth",
        [
            "npv",
            "irr",
            "cashflow",
            "portfolio",
            "capital",
            "investment",
            "financial",
            "budget",
            "runway",
            "burn rate",
            "conservation",
            "risk assessment",
            "stock",
            "forex",
            "commodity",
            "zakat",
            "epf",
        ],
        80,
    ),
    # WELL domain
    (
        "well",
        [
            "fatigue",
            "sleep",
            "vitality",
            "readiness",
            "my health",
            "health status",
            "stress",
            "cognitive",
            "dignity",
            "wellness",
            "energy level",
        ],
        70,
    ),
    # GitHub operations
    (
        "github",
        ["github", "pull request", "issue", "repo", "repository", "git push", "git commit", "merge", "branch"],
        60,
    ),
    # Browser automation
    ("browser", ["browse", "open website", "screenshot", "click on", "fill form", "web automation", "puppeteer"], 50),
    # Infrastructure
    ("infrastructure", ["vps", "server", "docker", "container", "deploy", "restart", "systemd", "port", "cron"], 40),
    # Federation ops (default for tool/agent work)
    (
        "federation_ops",
        [
            "federation",
            "health check",
            "tool",
            "agent",
            "session",
            "audit",
            "seal",
            "vault",
            "judge",
            "constitutional",
            "forge",
            "arif",
            "organ",
            "witness",
        ],
        30,
    ),
]


def classify_task(description: str) -> tuple[str, list[str]]:
    """Classify task description into domain. Returns (domain, matched_keywords)."""
    desc_lower = description.lower()
    matched = {}

    for domain, keywords, priority in RULES:
        for kw in keywords:
            if kw.lower() in desc_lower:
                if domain not in matched:
                    matched[domain] = []
                matched[domain].append(kw)

    if not matched:
        return "federation_ops", ["default"]

    # Pick domain with highest priority (first in RULES order)
    best_domain = max(matched.keys(), key=lambda d: next(p for dn, _, p in RULES if dn == d))
    return best_domain, matched[best_domain]


def load_manifest() -> dict:
    """Load the model tool manifest."""
    if not os.path.exists(MANIFEST):
        print(json.dumps({"error": "manifest_missing", "path": MANIFEST}))
        sys.exit(2)
    with open(MANIFEST) as f:
        return json.load(f)


def route(description: str) -> dict:
    """Route a task to the best runtime. Returns routing decision."""
    manifest = load_manifest()
    routing_rules = manifest.get("routing_rules", {})
    runtimes = manifest.get("runtimes", {})

    domain, matched_keywords = classify_task(description)

    # Look up routing rule
    rule = routing_rules.get(domain, {})
    primary = rule.get("primary")
    fallback = rule.get("fallback")
    reason = rule.get("reason", "no routing rule found")

    # Resolve runtime details
    runtime_name = primary.split("/")[0] if primary else None
    model_name = primary.split("/")[1] if primary and "/" in primary else None
    runtime = runtimes.get(runtime_name, {})

    # Determine available tools
    builtin_tools = []
    federation_tools = False

    if model_name and model_name in runtime.get("models", {}):
        model = runtime["models"][model_name]
        builtin_tools = [
            t for t, v in model.get("builtin_tools", {}).items() if isinstance(v, dict) and v.get("available")
        ]
        federation_tools = model.get("federation_tools", {}).get("available", False)
    elif runtime_name == "m365-copilot":
        # M365 has runtime-level tools, not model-level
        for category, tools in runtime.get("builtin_tools", {}).items():
            if isinstance(tools, list):
                builtin_tools.append(category)
        federation_tools = False

    # Determine authority level
    authority = "read_only"
    side_effects = runtime.get("side_effect_permissions", {})
    if side_effects or runtime.get("side_effects", {}).get("approval_required"):
        authority = "read_with_approval"

    # Build verdict
    verdict = "SEAL" if primary else "HOLD"
    if not primary and not fallback:
        verdict = "VOID"

    return {
        "domain": domain,
        "matched_keywords": matched_keywords,
        "runtime": runtime_name,
        "model": model_name,
        "reason": reason,
        "builtin_tools": builtin_tools,
        "federation_tools": federation_tools,
        "authority": authority,
        "fallback": fallback,
        "verdict": verdict,
        "provider_info": {
            "product": runtime.get("product", "?"),
            "environment": runtime.get("environment", "?"),
        },
    }


def tool_discover(intent: str) -> dict:
    """Discover available tool families without loading full schemas.
    Returns tool families that match the intent, so the harness can
    load only the relevant schemas on demand."""
    manifest = load_manifest()

    # Tool family catalog — name, tier, tools, trigger keywords
    families = {
        "github": {
            "tier": 2,
            "count": 8,
            "native_count": 15,
            "tools": [
                "forge_github",
                "forge_github_create_issue",
                "forge_github_create_pull_request",
                "forge_github_get_file",
                "forge_github_search_code",
                "forge_github_search_repos",
                "forge_github_create_or_update_file",
                "github_* (native)",
            ],
            "triggers": ["github", "pull request", "issue", "repo", "branch", "merge"],
        },
        "browser": {
            "tier": 2,
            "count": 7,
            "native_count": 15,
            "tools": [
                "forge_browser_navigate",
                "forge_browser_screenshot",
                "forge_browser_click",
                "forge_browser_type",
                "forge_browser_extract_text",
                "forge_browser_evaluate_js",
                "chrome-devtools_* (native)",
            ],
            "triggers": ["browse", "screenshot", "click", "website", "web automation", "form"],
        },
        "infrastructure": {
            "tier": 2,
            "count": 9,
            "native_count": 15,
            "tools": [
                "forge_vps_ports",
                "forge_vps_services",
                "forge_vps_cron",
                "forge_journalctl",
                "forge_netdata_alarms",
                "forge_netdata_metrics",
                "forge_probe_site",
                "forge_boundaries_assert",
                "hostinger-vps_* (native)",
            ],
            "triggers": ["vps", "server", "docker", "container", "deploy", "port", "cron", "systemd"],
        },
        "data_search": {
            "tier": 2,
            "count": 20,
            "tools": ["supabase_*", "qdrant_*", "context7_*", "perplexity_*", "meyhem_*", "sequential-thinking_*"],
            "triggers": ["database", "sql", "vector", "similarity", "library docs", "deep research"],
        },
        "geox": {
            "tier": 1,
            "count": 13,
            "tools": [
                "geox_observe",
                "geox_compute",
                "geox_interpret",
                "geox_model",
                "geox_prospect",
                "geox_claim",
                "geox_spatial",
                "geox_govern",
                "geox_evidence",
                "geox_bridge",
                "geox_surface_status",
                "geox_tie_preflight",
                "geox_tie_receipt",
            ],
            "triggers": ["seismic", "well log", "petrophysics", "basin", "reservoir", "geological"],
        },
        "wealth": {
            "tier": 1,
            "count": 19,
            "tools": [
                "wealth_capital_primitive",
                "wealth_capital_health",
                "wealth_capital_diagnose",
                "wealth_capital_market",
                "wealth_capital_ledger",
                "wealth_capital_wisdom",
                "wealth_wealth_omni_wisdom",
                "wealth_wealth_monte_carlo_simulate",
                "wealth_wealth_fiscal_breakeven",
                "wealth_wealth_institutional_stress_index",
                "wealth_wealth_collapse_signature_scan",
                "wealth_wealth_bid_surface",
                "wealth_wealth_optimize_mwc",
                "wealth_wealth_power_audit",
                "wealth_wealth_capture_scan",
                "wealth_wealth_boundary_governance",
                "wealth_wealth_judge_handoff",
                "wealth_wealth_beautiful_mouse_scan",
                "wealth_capital_registry",
            ],
            "triggers": ["npv", "irr", "cashflow", "portfolio", "capital", "investment", "financial"],
        },
        "well": {
            "tier": 1,
            "count": 18,
            "tools": [
                "well_readiness",
                "well_validate_vitality",
                "well_assess_homeostasis",
                "well_guard_dignity",
                "well_classify_substrate",
                "well_detect_boundary",
                "well_measure_gradient",
                "well_trace_lineage",
                "well_signal_coverage",
                "well_health_check",
                "well_registry_status",
                "well_assess_sovereign_entropy",
                "well_assess_livelihood",
                "well_assess_metabolism",
                "well_assess_reliability",
                "well_check_repair",
                "well_compute_metabolic_flux",
                "well_medical_boundary",
            ],
            "triggers": ["fatigue", "sleep", "vitality", "readiness", "stress", "dignity"],
        },
    }

    intent_lower = intent.lower()
    matches = []
    for name, family in families.items():
        for trigger in family["triggers"]:
            if trigger in intent_lower:
                matches.append(
                    {
                        "family": name,
                        "tier": family["tier"],
                        "tools_available": family["count"],
                        "native_count": family.get("native_count", 0),
                        "sample_tools": family["tools"][:5],
                        "requires_schema_load": True,
                    }
                )
                break

    if not matches:
        # Default: core tools are always loaded
        matches.append(
            {"family": "core (already loaded)", "tier": 0, "tools_available": 48, "requires_schema_load": False}
        )

    return {
        "intent": intent,
        "matches": matches,
        "recommendation": f"Load {len(matches)} tool family(ies)" if matches else "Use T0 core tools",
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: route_task.py <task description>")
        print("       route_task.py --discover <intent>")
        sys.exit(1)

    if sys.argv[1] == "--discover":
        intent = " ".join(sys.argv[2:])
        result = tool_discover(intent)
        print(json.dumps(result, indent=2))
        sys.exit(0)

    description = " ".join(sys.argv[1:])
    result = route(description)

    # Compact output
    print(json.dumps(result, indent=2))

    # Exit code based on verdict
    if result["verdict"] == "SEAL":
        sys.exit(0)
    elif result["verdict"] == "HOLD":
        sys.exit(1)
    else:
        sys.exit(2)


if __name__ == "__main__":
    main()
