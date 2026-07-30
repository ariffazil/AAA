#!/usr/bin/env python3
"""
FEDERATION MODEL ROUTER — 3-Layer Multimodal Intelligence Routing
=================================================================
Arif's Wolf Cabinet Model: MuleRouter (80%) · OpenRouter (15%) · Ollama (5%)

ROUTING LOGIC:
  vision       → MuleRouter first (4 models, fixed price)
  text/chat    → MuleRouter first for Hermes, OpenRouter for constitutional
  constitutional → OpenRouter ONLY (multi-provider DeepSeek V4 Pro)
  recovery     → Ollama local (qwen3:8b)

USAGE:
  python3 federation_model_router.py --task "describe this seismic section" --modality vision --agent opencode
  python3 federation_model_router.py --task "what is AVO" --modality text --agent hermes
  python3 federation_model_router.py --task "judge this deployment" --modality text --agent 888-apex

DITEMPA BUKAN DIBERI — Forged 2026-07-30
"""

import json, os, sys, argparse
from typing import Optional, Dict, List, Any

MODEL_MAP_PATH = "/root/AAA/registries/models/AGENT_MODEL_MAP.json"

# ── ROUTING MATRIX ──
# (modality, agent_type, priority) → (provider, model, fallback_chain)

ROUTING = {
    # ── VISION ──
    ("vision", "*", "quality"): ("mulerouter", "mulerouter/qwen-vl-max", "mulerouter_vision_chain"),
    ("vision", "*", "speed"): ("mulerouter", "mulerouter/qwen3-omni-flash", "mulerouter_vision_chain"),
    ("vision", "*", "balanced"): ("mulerouter", "mulerouter/qwen3-vl-plus", "mulerouter_vision_chain"),
    ("vision", "*", "default"): ("mulerouter", "mulerouter/qwen-vl-max", "mulerouter_vision_chain"),
    # ── TEXT ──
    ("text", "hermes", "speed"): ("mulerouter", "mulerouter/deepseek-v4-flash", "hermes_mulerouter_fast_chain"),
    ("text", "hermes", "default"): ("mulerouter", "mulerouter/deepseek-v4-flash", "hermes_mulerouter_fast_chain"),
    ("text", "opencode", "default"): ("openrouter", "deepseek/deepseek-v4-pro", "deepseek_primary_chain"),
    ("text", "forge", "default"): ("openrouter", "deepseek/deepseek-v4-pro", "deepseek_primary_chain"),
    ("text", "*", "speed"): ("mulerouter", "mulerouter/qwen3-max", "deepseek_primary_chain"),
    ("text", "*", "default"): ("openrouter", "deepseek/deepseek-v4-pro", "deepseek_primary_chain"),
    # ── CONSTITUTIONAL (never routes to MuleRouter as primary) ──
    ("constitutional", "*", "default"): ("openrouter", "deepseek/deepseek-v4-pro", "deepseek_primary_chain"),
    # ── OMNI / MULTIMODAL ──
    ("omni", "*", "default"): ("mulerouter", "mulerouter/qwen3-omni-flash", "mulerouter_vision_chain"),
    # ── RECOVERY ──
    ("recovery", "*", "default"): ("ollama", "ollama/qwen3:8b", None),
}


def load_model_map() -> Dict:
    with open(MODEL_MAP_PATH) as f:
        return json.load(f)


def detect_modality(task: str, agent_type: str) -> str:
    """Auto-detect if task needs vision based on keywords."""
    vision_keywords = [
        "image",
        "picture",
        "photo",
        "screenshot",
        "see",
        "look",
        "visual",
        "seismic section",
        "well log",
        "map",
        "diagram",
        "chart",
        "graph",
        "describe this",
        "what is this",
        "what do you see",
        "analyze this",
        "interpret this",
    ]
    task_lower = task.lower()
    if any(kw in task_lower for kw in vision_keywords):
        return "vision"

    constitutional_keywords = ["judge", "seal", "verdict", "hold", "void", "constitutional", "floor"]
    if any(kw in task_lower for kw in constitutional_keywords) or agent_type in ["888-apex", "apex"]:
        return "constitutional"

    return "text"


def route(
    task: str, modality: str = "auto", agent_type: str = "opencode", priority: str = "default", fallback_index: int = 0
) -> Dict[str, Any]:
    """
    Route a task to the correct model/provider.

    Returns: {
        'provider': str,
        'model': str,
        'endpoint_url': str,
        'api_key_ref': str,
        'fallback_chain': list,
        'fallback_index': int,
        'modality': str,
        'reason': str
    }
    """

    # Auto-detect modality if needed
    if modality == "auto":
        modality = detect_modality(task, agent_type)

    model_map = load_model_map()

    # Try agent-specific routing first, then wildcard
    key = (modality, agent_type, priority)
    if key not in ROUTING:
        key = (modality, "*", priority)
    if key not in ROUTING:
        key = (modality, "*", "default")
    if key not in ROUTING:
        # Ultimate fallback
        key = ("text", "*", "default")

    provider_id, model_key, chain_id = ROUTING[key]

    # Resolve provider details
    provider = next((p for p in model_map["providers"] if p["provider_id"] == provider_id), {})

    # Resolve model details
    model = next((m for m in model_map["models"] if m.get("model_key") == model_key), {})

    # Get fallback chain
    chain = model_map["fallback_chains"].get(chain_id, {}).get("chain", [])

    # If we're in fallback mode, pick the Nth model in the chain
    if fallback_index > 0 and fallback_index < len(chain):
        fallback_model_key = chain[fallback_index]
        # Resolve fallback provider from model key prefix
        fb_provider_id = fallback_model_key.split("/")[0]
        fb_provider = next((p for p in model_map["providers"] if p["provider_id"] == fb_provider_id), provider)
        return {
            "provider": fb_provider_id,
            "model": fallback_model_key,
            "endpoint_url": fb_provider.get("endpoint_url", ""),
            "api_key_ref": fb_provider.get("api_key_ref", ""),
            "fallback_chain": chain,
            "fallback_index": fallback_index,
            "modality": modality,
            "reason": f"Fallback #{fallback_index} — {fb_provider_id} via chain {chain_id}",
            "status": fb_provider.get("status", "UNKNOWN"),
        }

    reason_map = {
        ("vision", "mulerouter"): "MuleRouter — 4 vision models, fixed price, 1030-2406ms tested",
        ("text", "mulerouter"): "MuleRouter — fixed price, predictable cost for high-volume",
        ("text", "openrouter"): "OpenRouter — multi-provider redundancy for constitutional/code",
        (
            "constitutional",
            "openrouter",
        ): "OpenRouter ONLY — multi-provider DeepSeek V4 Pro. Constitutional cannot single-point-fail.",
        ("omni", "mulerouter"): "MuleRouter ONLY surface with omni-modal (vision+text+audio)",
        ("recovery", "ollama"): "Ollama local — zero cost, always available, sovereign recovery",
    }

    return {
        "provider": provider_id,
        "model": model_key,
        "endpoint_url": provider.get("endpoint_url", ""),
        "api_key_ref": provider.get("api_key_ref", ""),
        "fallback_chain": chain,
        "fallback_index": 0,
        "modality": modality,
        "reason": reason_map.get(
            (modality, provider_id), f"Routed via {provider_id} — {modality} task for {agent_type}"
        ),
        "status": provider.get("status", "UNKNOWN"),
    }


def cli():
    parser = argparse.ArgumentParser(description="Federation Model Router — 3-Layer Multimodal Intelligence")
    parser.add_argument("--task", "-t", type=str, required=True, help="Task description")
    parser.add_argument(
        "--modality",
        "-m",
        type=str,
        default="auto",
        choices=["auto", "text", "vision", "constitutional", "omni", "recovery"],
    )
    parser.add_argument(
        "--agent", "-a", type=str, default="opencode", help="Agent type: opencode, hermes, 555-asi, 888-apex, forge"
    )
    parser.add_argument(
        "--priority", "-p", type=str, default="default", choices=["speed", "quality", "balanced", "default"]
    )
    parser.add_argument("--fallback", "-f", type=int, default=0, help="Fallback index (0=primary)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    result = route(
        task=args.task,
        modality=args.modality,
        agent_type=args.agent,
        priority=args.priority,
        fallback_index=args.fallback,
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        # Human-readable output
        fb = result["fallback_chain"]
        fb_display = " → ".join(fb[:4]) + ("..." if len(fb) > 4 else "")

        print(f"""
╔══════════════════════════════════════════════════════════╗
║  FEDERATION MODEL ROUTER — 3-Layer Routing              ║
╠══════════════════════════════════════════════════════════╣
║  Task:     {args.task[:50]:<45s} ║
║  Agent:    {args.agent:<45s} ║
║  Modality: {result["modality"]:<45s} ║
╠══════════════════════════════════════════════════════════╣
║  🎯 ROUTED TO:                                          ║
║  Provider: {result["provider"]:<45s} ║
║  Model:    {result["model"]:<45s} ║
║  Status:   {result["status"]:<45s} ║
╠══════════════════════════════════════════════════════════╣
║  📋 Reason: {result["reason"][:48]:<48s} ║
╠══════════════════════════════════════════════════════════╣
║  🔄 Fallback chain ({"#" + str(result["fallback_index"]) if result["fallback_index"] > 0 else "PRIMARY"}):     ║
║  {fb_display:<52s} ║
╚══════════════════════════════════════════════════════════╝
""")


if __name__ == "__main__":
    cli()
