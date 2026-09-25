#!/usr/bin/env python3
"""
compile.py — arif-core SOT → per-harness plugin views
Canonical Path: /root/AAA/plugins/adapters/compile.py

Reads manifest.yaml (SOT) + organs.yaml (endpoint SOT) and emits dist/
views for each target harness. Views are build artifacts (FP-01): a view
may be deleted and rebuilt at any time; the SOT may not.

Never hardcodes ports (FP-07): organ URLs are resolved from organs.yaml
components that declare mcp_port. Organs without mcp_port are skipped.
"""

from __future__ import annotations

import hashlib
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

import yaml

AAA = Path("/root/AAA")
MANIFEST = AAA / "plugins" / "arif-core" / "manifest.yaml"
ORGANS = AAA / "federation" / "organs.yaml"
DIST = AAA / "plugins" / "dist"
CODEX_ADAPTER = AAA / "hooks" / "adapters" / "codex"
GROK_ADAPTER = AAA / "hooks" / "adapters" / "grok"
GEMINI_ADAPTER = AAA / "hooks" / "adapters" / "gemini"

# All 12 codex lifecycle events — closes finding R8 (VERIFY trc-arif-core-verify-fi008-7d21c4).
# Adapter CODEX_EVENT_MAP already maps every name; shim is advisory-only (FP-02).
CODEX_HOOK_WIRING = {
    "SessionStart":     ["SessionStart"],
    "SessionEnd":       ["SessionEnd"],
    "UserPromptSubmit": ["UserPromptSubmit"],
    "PreToolUse":       ["PreToolUse"],
    "PermissionRequest": ["PermissionRequest"],
    "PostToolUse":      ["PostToolUse"],
    "SubagentStart":    ["SubagentStart"],
    "SubagentStop":     ["SubagentStop"],
    "Stop":             ["Stop"],
    "Interrupt":        ["Interrupt"],
    "PreCompact":       ["PreCompact"],
    "PostCompact":      ["PostCompact"],
}

# Grok documented hook surface (bundled README 2026-09-23): "pre/post-tool-use,
# session start/end" ONLY. Anything beyond these four is absent, never faked (FP-04).
GROK_HOOK_WIRING = {
    "SessionStart": ".*",
    "PreToolUse": "Bash|Write|Edit",
    "PostToolUse": ".*",
    "SessionEnd": ".*",
}


def utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def resolve_organs() -> dict:
    """FP-07: organ URLs from the SOT only. Skip entries without mcp_port."""
    data = yaml.safe_load(ORGANS.read_text())
    out = {}
    for comp in data.get("components", []):
        port = comp.get("mcp_port")
        if not port:
            continue
        iface = (comp.get("interfaces") or {}).get("mcp", "/mcp")
        out[comp["id"]] = {"type": "http", "url": f"http://127.0.0.1:{port}{iface}"}
    return out


def emit_codex(man: dict, organs: dict, trace_id: str) -> list:
    base = DIST / "codex" / "arif-core"
    (base / "skills" / "arif-core-federation").mkdir(parents=True, exist_ok=True)
    written = []

    plugin = {
        "name": man["plugin"]["name"],
        "version": man["plugin"]["version"],
        "description": " ".join(man["plugin"]["description"].split()),
        "author": man["plugin"]["author"],
        "skills": "./skills/",
        # R7 (VERIFY trc-arif-core-verify-fi008-7d21c4): codex validator rejects a
        # top-level "hooks" field — hooks.json is auto-discovered beside the manifest.
        "mcpServers": "./.mcp.json",
        "interface": {
            "displayName": man["plugin"]["interface"]["category"] and man["plugin"]["display_name"],
            "shortDescription": "arifOS federation runtime wiring (sensors + organs + skills pointer)",
            "category": man["plugin"]["interface"]["category"],
            "capabilities": man["plugin"]["interface"]["capabilities"],
            "defaultPrompt": [" ".join(man["plugin"]["interface"]["default_prompt"].split())],
        },
    }
    (base / "plugin.json").write_text(json.dumps(plugin, indent=2) + "\n")
    written.append("plugin.json")

    hooks_json = {"description": "arif-core advisory sensors → AAA Hook Mesh (FP-02: never judges)", "hooks": {}}
    shim = "python3 /root/AAA/hooks/adapters/codex/shim.py"
    for canonical, natives in CODEX_HOOK_WIRING.items():
        for native in natives:
            hooks_json["hooks"].setdefault(native, []).append({
                "matcher": "^Bash$" if native == "PreToolUse" else ".*",
                "hooks": [{"type": "command", "command": f"{shim} {native}", "timeout": 10,
                           "statusMessage": "mesh-sensor"}],
            })
    (base / "hooks.json").write_text(json.dumps(hooks_json, indent=2) + "\n")
    written.append("hooks.json")

    (base / ".mcp.json").write_text(json.dumps({"mcpServers": organs}, indent=2) + "\n")
    written.append(".mcp.json")

    skill = f"""---
name: arif-core-federation
description: USE WHEN working inside an arifOS federation harness — canonical skills, organs, and hook-mesh laws live in AAA, not in this plugin.
---

# arif-core-federation (pointer skill — FP-03, no copies)

This plugin is a **packaging layer**. Capability lives in the substrate:

- Canonical skills: `/root/AAA/skills/` (555+ names; never mirror them)
- Hook mesh contract: `/root/AAA/hooks/lib/adapter_contract.py`
- Organ endpoints: `/root/AAA/federation/organs.yaml` (live health beats file)
- Kernel verbs: init → observe → think → route → memory → judge → forge → seal

Standing laws inherited by every session: F1-F13 floors; hooks are sensors,
never judges (FP-02); receipts carry trace_id; CAPABILITY ≠ AUTHORITY.
"""
    (base / "skills" / "arif-core-federation" / "SKILL.md").write_text(skill)
    written.append("skills/arif-core-federation/SKILL.md")
    return written


def emit_qwen(man: dict, organs: dict, trace_id: str) -> list:
    base = DIST / "qwen" / "arif-core"
    (base / "skills" / "arif-core").mkdir(parents=True, exist_ok=True)
    written = []

    qwen_md = f"""# arif-core · AAA Federation (Qwen Code view)

Build artifact of `/root/AAA/plugins/arif-core/manifest.yaml` ({utc()}) — do not hand-edit.

- Organs resolve from `/root/AAA/federation/organs.yaml`; snippet in `mcp-config.snippet.json`.
- Hook-mesh sensors: `/root/AAA/hooks/adapters/qwen/` (+ contract in `/root/AAA/hooks/lib/`).
- Install = explicit forge step (FP-05): copy into `~/.qwen/extensions/` is sovereign-gated.
- Hooks are sensors, never judges (FP-02). Skills referenced, never copied (FP-03).
"""
    (base / "QWEN.md").write_text(qwen_md)
    written.append("QWEN.md")

    (base / "mcp-config.snippet.json").write_text(json.dumps({"mcpServers": organs}, indent=2) + "\n")
    written.append("mcp-config.snippet.json")

    snippet = {
        "_comment": "INSTALL-FORGE-STEP ONLY: merge into Qwen Code settings hooks config (FP-05).",
        "hooks": {
            "UserPromptSubmit": [{"type": "command", "command": "python3 /root/AAA/hooks/adapters/codex/shim.py UserPromptSubmit", "timeout": 10}],
            "SessionStart": [{"type": "command", "command": "python3 /root/AAA/hooks/adapters/codex/shim.py SessionStart", "timeout": 10}]
        },
        "_note": "Qwen adapter maps session open/seal; full action.* coverage rides the mesh engine upgrade."
    }
    (base / "hooks.settings-snippet.json").write_text(json.dumps(snippet, indent=2) + "\n")
    written.append("hooks.settings-snippet.json")

    skill = """---
name: arif-core
description: USE WHEN working inside an arifOS federation harness — canonical skills, organs, and hook-mesh laws live in AAA, not in this plugin.
---

Pointer skill. Canonical skills: `/root/AAA/skills/`. Organ SOT:
`/root/AAA/federation/organs.yaml`. Kernel verbs are the session arc.
F1-F13 binding; CAPABILITY ≠ AUTHORITY; receipts carry trace_id.
"""
    (base / "skills" / "arif-core" / "SKILL.md").write_text(skill)
    written.append("skills/arif-core/SKILL.md")
    return written


def emit_grok(man: dict, organs: dict, trace_id: str) -> list:
    """Grok CLI view — built 2026-09-25 (F13 'buat adapter grok/gemini').

    Native surfaces (per bundled README, verified on-host):
    - hooks: JSON files in .grok/hooks/ OR [[hooks.<Event>]] TOML tables in config
    - MCP: [mcp_servers.<id>] with url = (streamable HTTP; live config.toml proves the shape)
    - skills: SKILL.md dirs under ~/.grok/skills/
    Both distribution forms of the hook wiring are emitted; the installer uses ONE (FP-05).
    """
    base = DIST / "grok" / "arif-core"
    (base / "skills" / "arif-core-federation").mkdir(parents=True, exist_ok=True)
    written = []
    shim = "python3 /root/AAA/hooks/adapters/grok/shim.py"

    hooks_json = {
        "description": "arif-core advisory sensors → AAA Hook Mesh (FP-02: never judges). "
                       "Grok documented surface: Pre/PostToolUse + SessionStart/End only.",
        "hooks": {},
    }
    for native, matcher in GROK_HOOK_WIRING.items():
        hooks_json["hooks"][native] = [{
            "matcher": matcher,
            "hooks": [{"type": "command", "command": f"{shim} {native}", "timeout": 10}],
        }]
    (base / "hooks.json").write_text(json.dumps(hooks_json, indent=2) + "\n")
    written.append("hooks.json")

    def toml_str(v: str) -> str:
        return json.dumps(v)  # JSON string escaping is valid TOML basic-string escaping

    toml = [f"# arif-core compiled view for Grok CLI — build artifact ({utc()}), do not hand-edit (FP-01).",
            "# Install = explicit forge step (FP-05): merge into ~/.grok/config.toml.",
            "# Hooks here are the config-layer form; hooks.json beside this file is the",
            "# .grok/hooks/ file form of the SAME wiring — install exactly one form.",
            ""]
    for oid, o in sorted(organs.items()):
        toml += [
            f"[mcp_servers.{oid}]",
            f"url = {toml_str(o['url'])}",
            "enabled = true",
            "startup_timeout_sec = 90",
            "tool_timeout_sec = 120",
            "",
            f"[mcp_servers.{oid}.headers]",
            'Accept = "application/json, text/event-stream"',
            "",
        ]
    for native, matcher in GROK_HOOK_WIRING.items():
        toml += [
            f"[[hooks.{native}]]",
            f"matcher = {toml_str(matcher)}",
            "",
            f"  [[hooks.{native}.hooks]]",
            '  type = "command"',
            f"  command = {toml_str(f'{shim} {native}')}",
            "  timeout = 10",
            "",
        ]
    (base / "config.arif-core.toml").write_text("\n".join(toml))
    written.append("config.arif-core.toml")

    skill = """---
name: arif-core-federation
description: USE WHEN working inside an arifOS federation harness — canonical skills, organs, and hook-mesh laws live in AAA, not in this plugin.
---

# arif-core-federation (pointer skill — FP-03, no copies)

Packaging layer only. Capability lives in the substrate:

- Canonical skills: `/root/AAA/skills/` (555+ names; never mirror)
- Hook mesh contract: `/root/AAA/hooks/lib/adapter_contract.py`
- Organ endpoints: `/root/AAA/federation/organs.yaml` (live health beats file)
- Kernel verbs: init → observe → think → route → memory → judge → forge → seal

Standing laws: F1-F13 floors; hooks are sensors, never judges (FP-02);
receipts carry trace_id; CAPABILITY ≠ AUTHORITY.
"""
    (base / "skills" / "arif-core-federation" / "SKILL.md").write_text(skill)
    written.append("skills/arif-core-federation/SKILL.md")
    return written


def emit_gemini(man: dict, organs: dict, trace_id: str) -> list:
    """Gemini CLI view — built 2026-09-25 (F13 'buat adapter grok/gemini').

    Honest surface (FP-04): gemini-cli has NO documented/configured lifecycle
    hook mechanism on this host (/root/.gemini/hooks/ empty since 2026-08-13).
    What IS real: settings.json mcpServers (hand-wired today; this fragment
    makes it compiled-parity). Hooks row = ABSENT, never faked.
    """
    base = DIST / "gemini" / "arif-core"
    base.mkdir(parents=True, exist_ok=True)
    written = []

    (base / "settings-mcpServers.fragment.json").write_text(
        json.dumps({"mcpServers": organs}, indent=2) + "\n")
    written.append("settings-mcpServers.fragment.json")

    gemini_md = f"""# arif-core · AAA Federation (Gemini CLI view)

Build artifact of `/root/AAA/plugins/arif-core/manifest.yaml` ({utc()}) — do not hand-edit (FP-01).

- Organs: `settings-mcpServers.fragment.json` — merge into `~/.gemini/settings.json`
  (`mcpServers` block). Host settings.json is hand-wired (12 servers, 2026-09-25);
  this fragment is the compiled parity guard from organs.yaml (FP-07, no hardcoded ports).
- Hooks: **ABSENT** — no gemini-cli lifecycle hook surface documented on-host
  (2026-09-25). Adapter + shim exist (`hooks/adapters/gemini/`) with a
  declared-absent event map; any future native hook lands unmapped-class until mapped.
- Install = explicit forge step (FP-05). Hooks are sensors, never judges (FP-02).
"""
    (base / "GEMINI.md").write_text(gemini_md)
    written.append("GEMINI.md")
    return written


def coverage_matrix(organs: dict) -> str:
    rows = [
        ("Plugin manifest (I-01..I-06)", "EMITTED", "EMITTED", "EXISTS (claude-code-federation)", "EMITTED (config+hooks+skill view)", "EMITTED (fragment + GEMINI.md)"),
        ("Lifecycle hooks — session", "FULL (SessionStart/End + Pre/PostCompact)", "DEGRADED (open/seal only)", "FULL (existing plugin)", "PARTIAL (SessionStart/End wired; documented surface = 4 events)", "ABSENT (no gemini hook mechanism on-host, verified 2026-09-25)"),
        ("Lifecycle hooks — action.*", "FULL (Pre/Post/Permission/Interrupt + SubagentStart/Stop)", "DEGRADED — mesh engine upgrade", "FULL", "PARTIAL (Pre/PostToolUse wired)", "ABSENT"),
        ("Hook enforcement", "KERNEL-LAYER (advisory sensors, FP-02)", "KERNEL-LAYER", "KERNEL-LAYER", "KERNEL-LAYER", "KERNEL-LAYER (n/a until surface exists)"),
        ("MCP organ surfaces", "FULL (organs.yaml-resolved)", "FULL (organs.yaml-resolved)", "FULL", "FULL (config.arif-core.toml, url= HTTP form)", "FULL (settings fragment; host already hand-wired 12 servers incl. all 6 organs)"),
        ("Skills", "POINTER (no copies, FP-03)", "POINTER", "FULL LIBRARY (rich surface)", "POINTER (SKILL.md, grok skills format)", "n/a (gemini has no skills surface)"),
        ("Codex decision-wire schema", "VERIFIED advisory-shape harmless (trc-arif-core-verify-fi008-7d21c4); real-runner calibration pending", "n/a", "n/a", "n/a (grok response schema undocumented; shim advisory)", "n/a"),
        ("Install step", "FORGE-GATED (F13 pen)", "FORGE-GATED", "INSTALLED (pre-existing)", "FORGE-GATED (merge config OR drop hooks.json — one form only)", "FORGE-GATED (merge fragment)"),
    ]
    lines = [
        "# arif-core coverage matrix (FP-04 — honest, per harness)",
        "",
        f"_Built {utc()} · organs resolved from organs.yaml: {len(organs)} ({', '.join(sorted(organs)) or 'none'})_",
        "",
        "| Invariant | codex | qwen | claude | grok | gemini |",
        "|---|---|---|---|---|---|",
    ]
    lines += [f"| {a} | {b} | {c} | {d} | {e} | {f} |" for a, b, c, d, e, f in rows]
    return "\n".join(lines) + "\n"


def main() -> int:
    man = yaml.safe_load(MANIFEST.read_text())
    organs = resolve_organs()

    sot_material = MANIFEST.read_bytes() + CODEX_ADAPTER.joinpath("adapter.py").read_bytes() \
        + GROK_ADAPTER.joinpath("adapter.py").read_bytes() + GEMINI_ADAPTER.joinpath("adapter.py").read_bytes()
    sot_sha = hashlib.sha256(sot_material).hexdigest()
    trace_id = f"trc-arif-core-{uuid.uuid4().hex[:12]}"

    if not DIST.exists():
        DIST.mkdir(parents=True)

    codex_files = emit_codex(man, organs, trace_id)
    qwen_files = emit_qwen(man, organs, trace_id)
    grok_files = emit_grok(man, organs, trace_id)
    gemini_files = emit_gemini(man, organs, trace_id)
    (DIST / "coverage-matrix.md").write_text(coverage_matrix(organs))

    receipt = {
        "trace_id": trace_id,
        "built_at": utc(),
        "sot_sha256": sot_sha,
        "plugin": {"name": man["plugin"]["name"], "version": man["plugin"]["version"]},
        "organs_resolved": sorted(organs.keys()),
        "views": {
            "codex": codex_files,
            "qwen": qwen_files,
            "claude": "existing_surface (claude-code-federation)",
            "grok": grok_files,
            "gemini": gemini_files,
        },
        "claim_state": "BUILT_NOT_INSTALLED",
        "next_gates": [
            "codex: validate emitted view (validate_plugin.py + I-01..I-41) — VERIFY lane",
            "codex: cross-check decision-response wire schema (from_canonical note)",
            "grok/gemini: VERIFY lane pass on emitted views (TOML/JSON schema + shim smoke)",
            "all: install per harness = explicit forge step (FP-05, F13 pen)",
            "author.email confirmation (currently domain-derived, SOVEREIGN-CONFIRM)",
        ],
    }
    (DIST / "build_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")

    print(json.dumps({"trace_id": trace_id, "sot_sha256": sot_sha[:16],
                      "organs": len(organs), "views": [len(codex_files), len(qwen_files)]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
