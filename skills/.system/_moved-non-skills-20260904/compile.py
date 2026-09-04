#!/usr/bin/env python3
"""
AAA Skill Compiler — skills/compile.py
Reads canonical SKILL.md frontmatter (host_compatibility) and generates
vendor-specific adapter files under each skill's directory.

Vendor output layout (per skill):
  skills/<id>/
  ├── SKILL.md              ← canonical (Claude Code)
  ├── claude/SKILL.md       ← copy for tools that look in subdirs
  ├── openai/README.md      ← OpenAI / Codex adapter
  ├── kimi/skill.md         ← Kimi Code adapter
  ├── opencode/README.md    ← OpenCode agent config fragment
  ├── grok/skill.md         ← Grok Build adapter
  ├── copilot/<id>.agent.md ← GitHub Copilot CLI agent
  ├── continue/skill.md     ← Continue.dev skill
  ├── antigravity/skill.md  ← Google Antigravity skill
  ├── openclaw/system.md    ← OpenClaw system override
  ├── mcp/manifest.json     ← MCP tool manifest
  ├── hermes/skill.md       ← Hermes ASI internal
  └── apex/skill.md         ← APEX Judge internal

Usage:
  python skills/compile.py                    # compile all skills (skip existing)
  python skills/compile.py aaa-agentic-governance
  python skills/compile.py --force            # overwrite all
  python skills/compile.py --dry-run          # preview only
  python skills/compile.py --list             # list skills + their declared targets
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Callable

import yaml

SKILLS_DIR = Path(__file__).parent

# vendor id → (subdir, filename | None means <skill-id>.agent.md)
VENDOR_MAP: dict[str, tuple[str, str | None]] = {
    "claude":        ("claude",       "SKILL.md"),
    "claude-code":   ("claude",       "SKILL.md"),
    "codex":         ("openai",       "README.md"),
    "openai":        ("openai",       "README.md"),
    "kimi":          ("kimi",         "skill.md"),
    "opencode":      ("opencode",     "README.md"),
    "grok":          ("grok",         "skill.md"),
    "copilot":       ("copilot",      None),
    "continue":      ("continue",     "skill.md"),
    "antigravity":   ("antigravity",  "skill.md"),
    "openclaw":         ("openclaw",  "system.md"),
    "openclaw-gateway": ("openclaw",  "system.md"),  # alias used by some skills
    "copilot-cli":      ("copilot",   None),          # alias used by some skills
    "mcp":              ("mcp",       "manifest.json"),
    "hermes-asi":    ("hermes",       "skill.md"),
    "hermes":        ("hermes",       "skill.md"),   # alias used by some skills
    "apx-judge":     ("apex",         "skill.md"),
    "kimi-code":     ("kimi",         "skill.md"),   # alias for kimi
    "claude":        ("claude",       "SKILL.md"),   # alias for claude-code
    "any-aaa-agent": ("claude",       "SKILL.md"),   # wildcard → canonical
}

FOOTER = "\n---\n*DITEMPA BUKAN DIBERI — arifOS Federation*\n"


# ---------------------------------------------------------------------------
# Frontmatter parser
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split YAML frontmatter from markdown body."""
    m = re.match(r"^---\n(.*?)\n---\n?(.*)", text, re.DOTALL)
    if not m:
        return {}, text
    meta = yaml.safe_load(m.group(1)) or {}
    return meta, m.group(2).strip()


# ---------------------------------------------------------------------------
# Generators — one per vendor
# ---------------------------------------------------------------------------

def gen_claude(meta: dict, body: str, skill_dir: Path) -> str:
    """Claude: verbatim copy of canonical SKILL.md."""
    return (skill_dir / "SKILL.md").read_text(encoding="utf-8")


def gen_openai(meta: dict, body: str, skill_dir: Path) -> str:
    sid   = meta.get("id", skill_dir.name)
    name  = meta.get("name", sid)
    desc  = meta.get("description", "")
    risk  = meta.get("risk_tier", "low")
    tools = meta.get("dependencies", {}).get("tools", [])

    fn_name = re.sub(r"[^a-z0-9_]", "_", sid.lower())
    tool_stub = {
        "type": "function",
        "function": {
            "name": fn_name,
            "description": desc,
            "parameters": {
                "type": "object",
                "properties": {
                    "context": {
                        "type": "string",
                        "description": "Brief context for this skill invocation",
                    }
                },
                "required": [],
            },
        },
    }

    tools_note = f"Tools: {', '.join(tools)}" if tools else "Tools: see canonical"
    return (
        f"# {name} — OpenAI / Codex Adapter\n\n"
        f"> **Canonical:** `skills/{sid}/SKILL.md`  \n"
        f"> **Risk tier:** {risk} | {tools_note}\n\n"
        f"{desc}\n\n"
        "## Trigger Conditions\n\n"
        f"See canonical skill → *When to Use* section.\n\n"
        "## Tool Definition Stub\n\n"
        f"```json\n{json.dumps(tool_stub, indent=2)}\n```\n"
        + FOOTER
    )


def gen_kimi(meta: dict, body: str, skill_dir: Path) -> str:
    sid     = meta.get("id", skill_dir.name)
    name    = meta.get("name", sid)
    desc    = meta.get("description", "")
    version = meta.get("version", "1.0.0")
    risk    = meta.get("risk_tier", "low")

    front = {
        "skill_id": sid,
        "name": name,
        "version": str(version),
        "description": desc,
        "risk_tier": risk,
        "canonical_source": f"skills/{sid}/SKILL.md",
        "platform": "kimi",
    }
    return (
        f"---\n{yaml.dump(front, default_flow_style=False, allow_unicode=True).strip()}\n---\n\n"
        f"# {name}\n\n"
        f"{desc}\n\n"
        "## When to Invoke\n\n"
        f"Follow the canonical playbook at `skills/{sid}/SKILL.md` → *When to Use*.\n"
        + FOOTER
    )


def gen_opencode(meta: dict, body: str, skill_dir: Path) -> str:
    sid  = meta.get("id", skill_dir.name)
    name = meta.get("name", sid)
    desc = meta.get("description", "")
    risk = meta.get("risk_tier", "low")

    agent_fragment = json.dumps(
        {
            "agents": {
                sid: {
                    "description": desc,
                    "risk_tier": risk,
                    "canonical_skill": f"skills/{sid}/SKILL.md",
                }
            }
        },
        indent=2,
    )
    return (
        f"# {name} — OpenCode Adapter\n\n"
        f"> **Canonical:** `skills/{sid}/SKILL.md` | **Risk:** {risk}\n\n"
        f"{desc}\n\n"
        "## OpenCode Agent Config Fragment\n\n"
        f"```json\n{agent_fragment}\n```\n\n"
        "Trigger conditions and full procedure: `skills/{sid}/SKILL.md`\n"
        + FOOTER
    )


def gen_grok(meta: dict, body: str, skill_dir: Path) -> str:
    sid     = meta.get("id", skill_dir.name)
    name    = meta.get("name", sid)
    desc    = meta.get("description", "")
    version = meta.get("version", "1.0.0")
    risk    = meta.get("risk_tier", "low")

    front = {
        "name": sid,
        "version": str(version),
        "description": desc,
        "risk_tier": risk,
        "canonical": f"skills/{sid}/SKILL.md",
    }
    return (
        f"---\n{yaml.dump(front, default_flow_style=False, allow_unicode=True).strip()}\n---\n\n"
        f"# {name}\n\n"
        f"{desc}\n\n"
        "## Usage\n\n"
        f"Invoke via `/skill {sid}` in Grok Build.  \n"
        f"Full procedure at `skills/{sid}/SKILL.md`.\n"
        + FOOTER
    )


def gen_copilot(meta: dict, body: str, skill_dir: Path) -> str:
    sid   = meta.get("id", skill_dir.name)
    name  = meta.get("name", sid)
    desc  = meta.get("description", "")
    risk  = meta.get("risk_tier", "low")
    tools = meta.get("dependencies", {}).get("tools", ["read_file", "write_file", "run_terminal_command"])

    tool_lines = "\n".join(f"  - {t}" for t in tools)
    front_raw  = (
        f"name: \"{name}\"\n"
        f"description: \"{desc}\"\n"
        f"risk_tier: {risk}\n"
        f"tools:\n{tool_lines}\n"
        f"canonical_skill: skills/{sid}/SKILL.md\n"
    )
    return (
        f"---\n{front_raw}---\n\n"
        f"# {name}\n\n"
        f"{desc}\n\n"
        "## Procedure\n\n"
        f"Full governed playbook at `skills/{sid}/SKILL.md`.\n"
        + FOOTER
    )


def gen_continue(meta: dict, body: str, skill_dir: Path) -> str:
    sid  = meta.get("id", skill_dir.name)
    name = meta.get("name", sid)
    desc = meta.get("description", "")
    risk = meta.get("risk_tier", "low")

    front = {"name": name, "description": desc}
    return (
        f"---\n{yaml.dump(front, default_flow_style=False, allow_unicode=True).strip()}\n---\n\n"
        f"# {name}\n\n"
        f"> Risk: {risk} | Canonical: `skills/{sid}/SKILL.md`\n\n"
        f"{desc}\n\n"
        "## Instructions\n\n"
        f"Follow the canonical playbook at `skills/{sid}/SKILL.md`.\n"
        + FOOTER
    )


def gen_antigravity(meta: dict, body: str, skill_dir: Path) -> str:
    sid     = meta.get("id", skill_dir.name)
    name    = meta.get("name", sid)
    desc    = meta.get("description", "")
    version = meta.get("version", "1.0.0")

    return (
        f"# {name}\n\n"
        f"**Skill ID:** `{sid}` | **Version:** {version}  \n"
        f"**Canonical:** `skills/{sid}/SKILL.md`\n\n"
        f"{desc}\n\n"
        "## Antigravity Invocation\n\n"
        f"This skill runs as an Antigravity skill bundle.  \n"
        f"Full procedure and governance constraints: `skills/{sid}/SKILL.md`.\n"
        + FOOTER
    )


def gen_openclaw(meta: dict, body: str, skill_dir: Path) -> str:
    sid     = meta.get("id", skill_dir.name)
    name    = meta.get("name", sid)
    desc    = meta.get("description", "")
    version = meta.get("version", "1.0.0")
    risk    = meta.get("risk_tier", "low")

    return (
        f"# {name} — OpenClaw Override\n\n"
        f"> **Skill:** {sid} v{version}  \n"
        f"> **Format:** OpenClaw system.md override section  \n"
        f"> **Canonical source:** `skills/{sid}/SKILL.md`\n\n"
        "---\n\n"
        "## Skill Override Block\n\n"
        "Append to OpenClaw agent `system.md`:\n\n"
        "```\n"
        f"SKILL: {sid} (arifOS Federation)\n"
        f"{'=' * (len(sid) + 22)}\n"
        f"{desc}\n"
        f"Risk tier: {risk}\n"
        f"Full playbook: skills/{sid}/SKILL.md\n"
        "```\n"
        + FOOTER
    )


def gen_mcp(meta: dict, body: str, skill_dir: Path) -> str:
    sid     = meta.get("id", skill_dir.name)
    name    = meta.get("name", sid)
    desc    = meta.get("description", "")
    version = meta.get("version", "1.0.0")
    risk    = meta.get("risk_tier", "low")
    servers = meta.get("dependencies", {}).get("servers", [])
    floors  = meta.get("floors", [])

    manifest = {
        "manifest_version": "1.0",
        "name": sid,
        "display_name": name,
        "description": desc,
        "version": str(version),
        "risk_tier": risk,
        "canonical_skill": f"skills/{sid}/SKILL.md",
        "dependencies": {"servers": servers},
        "arifos": {
            "floors": floors,
            "owner": meta.get("owner", "AAA"),
            "knowledge_basis": meta.get("knowledge_basis", {}),
        },
    }
    return json.dumps(manifest, indent=2)


def gen_hermes(meta: dict, body: str, skill_dir: Path) -> str:
    sid  = meta.get("id", skill_dir.name)
    name = meta.get("name", sid)
    desc = meta.get("description", "")

    front = {"agent": "hermes-asi", "skill_id": sid, "name": name, "canonical": f"skills/{sid}/SKILL.md"}
    return (
        f"---\n{yaml.dump(front, default_flow_style=False, allow_unicode=True).strip()}\n---\n\n"
        f"# {name} — Hermes ASI Adapter\n\n"
        f"{desc}\n\n"
        "## Invocation\n\n"
        f"Route to `{sid}` via Hermes relay.  \n"
        f"Constitutional constraints: `skills/{sid}/SKILL.md`.\n"
        + FOOTER
    )


def gen_apex(meta: dict, body: str, skill_dir: Path) -> str:
    sid  = meta.get("id", skill_dir.name)
    name = meta.get("name", sid)
    desc = meta.get("description", "")

    front = {
        "agent": "apx-judge",
        "skill_id": sid,
        "name": name,
        "authority": "888_JUDGE",
        "canonical": f"skills/{sid}/SKILL.md",
    }
    return (
        f"---\n{yaml.dump(front, default_flow_style=False, allow_unicode=True).strip()}\n---\n\n"
        f"# {name} — APEX Judge Adapter\n\n"
        f"{desc}\n\n"
        "## APEX Invocation\n\n"
        "This skill requires 888_JUDGE authority.  \n"
        f"Route via APEX deliberation path: `skills/{sid}/SKILL.md`.\n"
        + FOOTER
    )


GENERATORS: dict[str, Callable] = {
    "claude":       gen_claude,
    "claude-code":  gen_claude,
    "codex":        gen_openai,
    "openai":       gen_openai,
    "kimi":         gen_kimi,
    "opencode":     gen_opencode,
    "grok":         gen_grok,
    "copilot":      gen_copilot,
    "continue":     gen_continue,
    "antigravity":  gen_antigravity,
    "openclaw":         gen_openclaw,
    "openclaw-gateway": gen_openclaw,
    "copilot-cli":      gen_copilot,
    "mcp":              gen_mcp,
    "hermes-asi":   gen_hermes,
    "apx-judge":    gen_apex,
}


# ---------------------------------------------------------------------------
# Core compile logic
# ---------------------------------------------------------------------------

def compile_skill(
    skill_dir: Path,
    *,
    force: bool = False,
    dry_run: bool = False,
) -> list[str]:
    """Compile one skill directory. Returns log lines."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return []

    text = skill_md.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)
    sid = meta.get("id", skill_dir.name)
    compat = meta.get("host_compatibility", [])

    if not compat:
        return [f"  SKIP  {sid}: host_compatibility not declared"]

    log: list[str] = []
    for vendor in compat:
        if vendor not in VENDOR_MAP:
            log.append(f"  WARN  {sid}/{vendor}: unknown vendor — add to VENDOR_MAP")
            continue

        subdir, filename = VENDOR_MAP[vendor]
        if filename is None:
            filename = f"{sid}.agent.md"

        out_dir  = skill_dir / subdir
        out_file = out_dir / filename

        if out_file.exists() and not force:
            log.append(f"  EXISTS {sid}/{subdir}/{filename}")
            continue

        gen_fn = GENERATORS.get(vendor)
        if not gen_fn:
            log.append(f"  WARN  {sid}/{vendor}: no generator defined")
            continue

        content = gen_fn(meta, body, skill_dir)

        if not dry_run:
            out_dir.mkdir(parents=True, exist_ok=True)
            out_file.write_text(content, encoding="utf-8")

        tag = "DRY  " if dry_run else "WRITE"
        log.append(f"  {tag} {sid}/{subdir}/{filename}")

    return log


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="AAA Skill Compiler — generates vendor-specific adapters from SKILL.md",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "target",
        nargs="?",
        default="all",
        help="skill-id to compile, or 'all' (default)",
    )
    parser.add_argument("--force",   action="store_true", help="Overwrite existing vendor files")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--list",    action="store_true", help="List skills and their declared targets")
    args = parser.parse_args()

    if args.target == "all":
        skill_dirs = sorted(
            d for d in SKILLS_DIR.iterdir()
            if d.is_dir() and (d / "SKILL.md").exists()
        )
    else:
        candidate = SKILLS_DIR / args.target
        if not candidate.exists():
            print(f"ERROR: skill '{args.target}' not found in {SKILLS_DIR}", file=sys.stderr)
            sys.exit(1)
        skill_dirs = [candidate]

    if args.list:
        print(f"{'SKILL':40s}  TARGETS")
        print("-" * 70)
        for d in skill_dirs:
            text = (d / "SKILL.md").read_text(encoding="utf-8")
            meta, _ = parse_frontmatter(text)
            compat = meta.get("host_compatibility", [])
            print(f"{d.name:40s}  {', '.join(compat) or '(none)'}")
        return

    prefix = "[DRY RUN] " if args.dry_run else ""
    written = 0
    skipped = 0

    for skill_dir in skill_dirs:
        log = compile_skill(skill_dir, force=args.force, dry_run=args.dry_run)
        if log:
            print(f"\n{skill_dir.name}:")
            for line in log:
                print(line)
                if "WRITE" in line and "DRY" not in line:
                    written += 1
                elif "EXISTS" in line:
                    skipped += 1

    print(f"\n{prefix}Done. {written} files written, {skipped} already existed (use --force to overwrite).")


if __name__ == "__main__":
    main()
