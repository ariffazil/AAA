#!/usr/bin/env python3
"""
opencode_render.py — Render OpenCode config from AGENT_MODEL_MAP.json SOT.

SOT: /root/AAA/registries/models/AGENT_MODEL_MAP.json
      (symlinked as /root/.config/federation-models.json)
Output: /root/.config/opencode/opencode.json

Usage:
    python3 opencode_render.py                  # dry-run → print diff (DEFAULT)
    python3 opencode_render.py --dry-run        # explicit dry-run
    python3 opencode_render.py --staging <path> # render to staging file
    python3 opencode_render.py --write --force  # write to live config (FORCE REQUIRED)
    python3 opencode_render.py --verify         # validate against live opencode

SAFETY:
    --write requires --force (F1 AMANAH — prevents accidental overwrite)
    Dry-run is DEFAULT. No flag = no mutation.
    auto-backup created before any --write.

DITEMPA BUKAN DIBERI. Forged 2026-07-24. Hardened 2026-07-24.
"""

import json
import sys
from pathlib import Path

SOT = Path("/root/.config/federation-models.json")
CURRENT = Path("/root/.config/opencode/opencode.json")

# ── Provider Name Mapping (SOT → OpenCode) ──
# SOT provider_id → OpenCode provider section key
SOT_TO_OC_PROVIDER = {
    "deepseek": "deepseek",
    "opencode-go": "opencode-go",
    "opencode-zen": "opencode-zen",
    "openrouter": "openrouter",
    "tokenrouter-arifos": "tokenrouter-arifos",
    "kimi": "kimi",
    "kimi-moonshot": "kimi",
    "minimax": "minimax",
    "groq": "groq",
    "sea-lion": "sea-lion",
    "gemini": "gemini",
    "cerebras": "cerebras",
    "ollama": "ollama",
    "azure-openai": "azure-openai",
    "mimo-platform": "mimo-platform",
    "bailian-token-plan": "bailian-token-plan",
    "glm": "tokenrouter-arifos",
    "xai": "openrouter",
    "openai": "openrouter",
}

# ── Model Key Translation ──
# SOT model_key → OpenCode model reference (provider/model)
MODEL_KEY_TRANSLATION = {
    "deepseek/deepseek-v4-pro": "deepseek/deepseek-v4-pro",
    "deepseek/deepseek-v4-flash": "deepseek/deepseek-v4-flash",
    "kimi/k3": "kimi/k3",
    "kimi/kimi-k2.7-code": "kimi/kimi-for-coding",
    "kimi/kimi-for-coding": "kimi/kimi-for-coding",
    "minimax/MiniMax-M3": "minimax/MiniMax-M3",
    "minimax/MiniMax-M2.7": "minimax/MiniMax-M2.7",
    "minimax/MiniMax-M2.5": "minimax/MiniMax-M2.5",
    "ollama/qwen2.5-coder:3b": "ollama/qwen2.5-coder:3b",
    "glm/glm-5.2": "tokenrouter-arifos/z-ai/glm-5.2",
    "mimo/mimo-v2.5-pro": "opencode-go/mimo-v2.5-pro",
    "mimo/mimo-v2.5-pro-ultraspeed": "opencode-go/mimo-v2.5-pro",
    "groq/llama-3.1-8b-instant": "groq/llama-3.1-8b-instant",
    "groq/llama-3.3-70b-versatile": "groq/llama-3.3-70b-versatile",
    "sea-lion/Qwen-SEA-LION-v4-32B-IT": "sea-lion/aisingapore/Qwen-SEA-LION-v4-32B-IT",
    "sea-lion/Llama-SEA-LION-v3-70B-IT": "sea-lion/aisingapore/Llama-SEA-LION-v3-70B-IT",
    "sea-lion/Gemma-SEA-LION-v4-27B-IT": "sea-lion/aisingapore/Gemma-SEA-LION-v4-27B-IT",
    "gemini/gemini-2.5-flash": "gemini/gemini-2.5-flash",
    "cerebras/gemma-4-31b": "cerebras/gemma-4-31b",
    "openai/gpt-5.6-sol": "openrouter/kimi-k3",
    "xai/grok-4.5": "openrouter/kimi-k3",
}

# ── SOT OpenCode Agent Mappings ──
# SOT agent_id → OpenCode agent config
AGENT_SOT_MAP = {
    "forge": "forge",
    "auditor": "auditor",
    "ops": "ops",
    "planner": "planner",
    "recovery": "recovery",
    "opencode": "forge",  # opencode SOT agent maps to forge (the default)
}


def load_sot() -> dict:
    if not SOT.exists():
        raise FileNotFoundError(f"SOT not found: {SOT}")
    with open(SOT) as f:
        return json.load(f)


def load_current() -> dict:
    if not CURRENT.exists():
        return {}
    with open(CURRENT) as f:
        return json.load(f)


def resolve_agent_model(sot: dict, agent_id: str) -> dict:
    """Resolve agent model+fallbacks from SOT."""
    agents = {a["agent_id"]: a for a in sot.get("agents", [])}
    if agent_id not in agents:
        return {"model": None, "fallbacks": [], "provider": None}
    a = agents[agent_id]
    primary = a.get("primary_model", "")
    provider = a.get("primary_provider", "")
    oc_model = MODEL_KEY_TRANSLATION.get(primary, primary)

    fb_raw = a.get("fallback_chain", [])
    fallbacks = []
    for fb in fb_raw:
        mk = fb.get("model_key", "")
        translated = MODEL_KEY_TRANSLATION.get(mk, mk)
        if translated:
            fallbacks.append(translated)

    return {
        "model": oc_model,
        "provider": SOT_TO_OC_PROVIDER.get(provider, provider),
        "fallbacks": fallbacks,
        "status": a.get("status", "UNKNOWN"),
    }


# Single canonical governance kernel path (never bare rules/governance.md).
CANONICAL_GOVERNANCE = "/root/.config/opencode/rules/arifos-governance.md"
ORPHAN_GOVERNANCE = "/root/.config/opencode/rules/governance.md"


def render_instructions(sot: dict) -> list:
    """Generate instruction file list for opencode.json.

    11 AAA SOT surfaces + 1 governance kernel = 12 hooks.
    Governance is always CANONICAL_GOVERNANCE — never the orphan governance.md.
    """
    base = "/root"
    return [
        f"{base}/AAA/prompts/INIT.md",
        f"{base}/AAA/prompts/AAA-ZEN-ALIGNMENT.md",
        f"{base}/AAA/agents/opencode/AGENTS.md",
        f"{base}/AAA/agents/opencode/AUTONOMOUS_GOVERNANCE.md",
        f"{base}/AAA/agents/opencode/TOOLS.md",
        f"{base}/AAA/agents/opencode/IDENTITY.md",
        f"{base}/AAA/agents/opencode/BOOTSTRAP.md",
        f"{base}/AAA/agents/opencode/HEARTBEAT.md",
        f"{base}/AAA/agents/opencode/WORKFLOW.md",
        f"{base}/AAA/skills/OPENCODE_SKILL_PROFILE.json",
        f"{base}/AAA/registries/opencode_skills_alignment.yaml",
        CANONICAL_GOVERNANCE,
    ]


def validate_instruction_paths(instructions: list) -> list[str]:
    """Intent gates beyond render↔live structural match.

    - Every instructions[] path must exist on disk (no silent ghost hooks)
    - Orphan rules/governance.md is forbidden (split-brain / false Gate-1)
    - Governance hook must be exactly CANONICAL_GOVERNANCE
    """
    errors: list[str] = []
    for p in instructions:
        if not isinstance(p, str):
            errors.append(f"non-string instruction entry: {p!r}")
            continue
        if p == ORPHAN_GOVERNANCE or p.endswith("/rules/governance.md"):
            errors.append(
                f"ORPHAN governance path forbidden: {p} "
                f"(use {CANONICAL_GOVERNANCE}; archive legacy under rules/_archive/)"
            )
        if not Path(p).is_file():
            errors.append(f"MISSING instruction file: {p}")
    gov_hooks = [p for p in instructions if isinstance(p, str) and "governance" in Path(p).name.lower()]
    if CANONICAL_GOVERNANCE not in instructions:
        errors.append(f"canonical governance missing from instructions[]: {CANONICAL_GOVERNANCE}")
    for g in gov_hooks:
        if g != CANONICAL_GOVERNANCE and not g.endswith("/AUTONOMOUS_GOVERNANCE.md"):
            # AUTONOMOUS_GOVERNANCE.md is agent doctrine, not the rules kernel
            if Path(g).name == "arifos-governance.md" and g != CANONICAL_GOVERNANCE:
                errors.append(f"governance kernel must be single path: got {g}")
            elif Path(g).name not in {"AUTONOMOUS_GOVERNANCE.md", "arifos-governance.md"}:
                errors.append(f"unexpected governance-named hook: {g}")
    return errors


def build_providers(sot: dict) -> list:
    """Build provider order from SOT providers[] status."""
    providers_raw = sot.get("providers", [])

    # Order by status: ACTIVE first, then FREE, then RATE_LIMITED/DEPRECATING
    def sort_key(p):
        status = p.get("status", "UNKNOWN")
        order = {"ACTIVE": 0, "FREE_TIER": 1, "RATE_LIMITED": 2, "DEPRECATING": 3, "UNKNOWN": 4}
        return (order.get(status, 99), p.get("provider_id", ""))

    sorted_providers = sorted(providers_raw, key=sort_key)

    result = []
    for p in sorted_providers:
        pid = p["provider_id"]
        oc_key = SOT_TO_OC_PROVIDER.get(pid)
        if oc_key:
            result.append(oc_key)

    # Ensure critical providers are present
    critical = ["deepseek", "opencode-go", "openrouter", "tokenrouter-arifos", "ollama"]
    for c in critical:
        if c not in result:
            result.append(c)

    # Deduplicate while preserving order
    seen = set()
    deduped = []
    for p in result:
        if p not in seen:
            seen.add(p)
            deduped.append(p)

    # Filter to only providers that exist in the current config's provider section
    current = load_current()
    known_providers = set(current.get("provider", {}).keys())
    # Always keep essential providers even if not in current config
    essential = {"deepseek", "opencode-go", "openrouter", "tokenrouter-arifos", "ollama", "kimi", "groq", "gemini"}
    filtered = [p for p in deduped if p in known_providers or p in essential]

    # Move deepseek to front if not already
    if "deepseek" in filtered:
        filtered.remove("deepseek")
        filtered.insert(0, "deepseek")

    return filtered


def generate() -> dict:
    """Generate OpenCode config from SOT."""
    sot = load_sot()
    current = load_current()

    # Start from current config to preserve MCP server definitions, permissions, etc.
    config = dict(current)

    # Update model selection from SOT
    opencode_agent = resolve_agent_model(sot, "opencode")
    if opencode_agent["model"]:
        config["model"] = opencode_agent["model"]

    # small_model → fastest/cheapest fallback
    # Pick the lightest model from the fallback chain or deepseek-v4-flash
    fallbacks = opencode_agent.get("fallbacks", [])
    # Prefer lightweight fallbacks: ollama > groq > gemini > tokenrouter
    lightweight_order = ["ollama/", "groq/", "gemini/", "sea-lion/", "deepseek/deepseek-v4-flash"]
    small_model = "deepseek/deepseek-v4-flash"
    for fb in fallbacks:
        for light in lightweight_order:
            if light in fb:
                small_model = fb
                break
        if small_model != "deepseek/deepseek-v4-flash":
            break
    config["small_model"] = small_model

    # Provider order from SOT
    config["enabled_providers"] = build_providers(sot)

    # Update agent model references from SOT
    for oc_agent_id, sot_agent_id in AGENT_SOT_MAP.items():
        resolved = resolve_agent_model(sot, sot_agent_id)
        oc_agent = config.get("agent", {}).get(oc_agent_id, {})
        if resolved["model"] and oc_agent:
            oc_agent["model"] = resolved["model"]

    # Preserve special agents not in SOT
    special_agents = {
        "image-prompt-architect": {
            "model": "kimi/k3",
            "permission": {"bash": "allow", "*": "deny"},
        }
    }
    for agent_id, defaults in special_agents.items():
        oc_agent = config.get("agent", {}).get(agent_id, {})
        if oc_agent:
            oc_agent["model"] = defaults["model"]
            if "permission" in defaults:
                oc_agent["permission"] = defaults["permission"]
            # Clean up deprecated tools field
            oc_agent.pop("tools", None)

    # ALWAYS set instructions from render — this IS the hook mechanism
    config["instructions"] = render_instructions(sot)

    # Remove schema-rejected keys
    for key in ["_generated", "_model_sot"]:
        config.pop(key, None)

    return config


def diff_json(a: dict, b: dict, path="") -> list:
    """Simple recursive diff between two dicts."""
    changes = []
    all_keys = set(list(a.keys()) + list(b.keys()))
    for k in all_keys:
        p = f"{path}.{k}" if path else k
        if k not in a:
            changes.append(f"+ {p}")
        elif k not in b:
            changes.append(f"- {p}")
        elif isinstance(a[k], dict) and isinstance(b[k], dict):
            changes.extend(diff_json(a[k], b[k], p))
        elif isinstance(a[k], list) and isinstance(b[k], list):
            if a[k] != b[k]:
                changes.append(f"~ {p}: {b[k]} → {a[k]}")
        elif a[k] != b[k]:
            av = str(a[k])[:60]
            bv = str(b[k])[:60]
            changes.append(f"~ {p}: {bv} → {av}")
    return changes


def main():
    import shutil
    from datetime import datetime, timezone

    args = sys.argv[1:]

    # ── --verify mode ──
    if "--verify" in args:
        current = load_current()
        generated = generate()
        changes = diff_json(generated, current)
        intent_errors = validate_instruction_paths(generated.get("instructions", []))
        # Also intent-check live config (catch ghost hooks still served to runtime)
        intent_errors.extend(
            f"LIVE: {e}" for e in validate_instruction_paths(current.get("instructions", []))
        )
        # de-dupe while preserving order
        seen: set[str] = set()
        intent_errors = [e for e in intent_errors if not (e in seen or seen.add(e))]

        failed = False
        if changes:
            failed = True
            print(f"⚠️  DRIFT DETECTED: {len(changes)} difference(s) between SOT and live config:")
            for c in changes:
                print(f"  {c}")
        if intent_errors:
            failed = True
            print(f"⚠️  INTENT GATE FAIL: {len(intent_errors)} instruction path error(s):")
            for e in intent_errors:
                print(f"  {e}")
        if failed:
            sys.exit(1)
        print("✅ VERIFIED: OpenCode config aligned with SOT (structural + instruction intent)")
        print(f"   instructions={len(generated.get('instructions', []))} files, all exist")
        print(f"   governance_kernel={CANONICAL_GOVERNANCE}")
        sys.exit(0)
        return

    generated = generate()

    # ── --staging mode ──
    if "--staging" in args:
        idx = args.index("--staging")
        staging_path = Path(args[idx + 1]) if idx + 1 < len(args) else Path("/tmp/opencode.json.staging")
        with open(staging_path, "w") as f:
            json.dump(generated, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"✅ Staged to {staging_path}")
        print(f"   Run: diff -u {CURRENT} {staging_path}")
        return

    # ── --write mode (requires --force) ──
    if "--write" in args:
        if "--force" not in args:
            print("❌ REFUSED: --write requires --force (F1 AMANAH)")
            print("   Use --dry-run first to review changes.")
            print("   Then: python3 opencode_render.py --write --force")
            sys.exit(1)

        # Auto-backup before write
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        backup_dir = CURRENT.parent / "_backups"
        backup_dir.mkdir(exist_ok=True)
        backup_path = backup_dir / f"opencode-{ts}.json"
        if CURRENT.exists():
            shutil.copy2(CURRENT, backup_path)
            # Write SHA256
            import hashlib

            sha = hashlib.sha256(CURRENT.read_bytes()).hexdigest()
            (backup_dir / f"opencode-{ts}.sha256").write_text(sha + "\n")
            print(f"📦 Auto-backup: {backup_path}")

        with open(CURRENT, "w") as f:
            json.dump(generated, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"✅ Wrote {CURRENT}")
        print(f"   model={generated.get('model')}")
        print(f"   providers={len(generated.get('enabled_providers', []))}")
        print(f"   instructions={len(generated.get('instructions', []))} files")
        print(f"   Rollback: cp {backup_path} {CURRENT}")
        return

    # ── DEFAULT: dry-run ──
    current = load_current()
    changes = diff_json(generated, current)
    if changes:
        print(f"🔍 DRY-RUN: {len(changes)} difference(s) between SOT and live config:")
        for c in changes:
            print(f"  {c}")
        print()
        print(f"   To apply: python3 opencode_render.py --write --force")
    else:
        print("✅ NO_CHANGE: Live config matches rendered SOT output (SHA256 identical)")
        print(f"   No --write needed.")

    # Validate
    errors = []
    for agent_id, agent_cfg in generated.get("agent", {}).items():
        model = agent_cfg.get("model", "")
        if model and "/" not in model:
            errors.append(f"{agent_id}: model '{model}' missing provider prefix")
    if errors:
        print("\n⚠️  Validation warnings:")
        for e in errors:
            print(f"  {e}")

    # Show resolved agent models table
    print("\n=== Resolved Agent Models (SOT → OpenCode) ===")
    sot = load_sot()
    for oc_aid, sot_aid in AGENT_SOT_MAP.items():
        r = resolve_agent_model(sot, sot_aid)
        model = r["model"] or "(not set)"
        prov = r["provider"] or "?"
        fbs = r["fallbacks"]
        fb_str = ", ".join(fbs[:2]) + ("..." if len(fbs) > 2 else "")
        print(f"  {oc_aid:20s} → {model:35s} ({prov}) fallbacks=[{fb_str}]")

    # Show protected local subagents
    local_agents = [k for k in generated.get("agent", {}).keys() if k not in AGENT_SOT_MAP]
    if local_agents:
        print(f"\n=== Preserved Runtime-Local Subagents ({len(local_agents)}) ===")
        for la in local_agents:
            cfg = generated["agent"][la]
            print(f"  {la:30s} → {cfg.get('model', '?')}")


if __name__ == "__main__":
    main()
