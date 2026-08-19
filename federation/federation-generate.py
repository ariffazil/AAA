#!/usr/bin/env python3
"""
federation-generate.py — ONE source, many views.
Reads federation.yaml → emits:
  agents/<name>/agent.yaml   ← A2A-shaped card per agent (the SELF)
  out/organ-view.yaml        ← organ-tier servers only
  out/capability-index.json  ← capability → servers mapping
  out/call-view.yaml         ← role → server derivation
  out/drift-report.txt       ← all counts from one source
  out/.checksums.sha256      ← integrity enforcement (generated files are read-only)

Design: federation.yaml = THE WHOLE (R∉S). agent.yaml = THE SELF (derived).
The self cannot define the federation. The federation defines what each self
may expose. A2A opaque execution, sovereignty baked in.

Enforcement: generated files are chmod 444 + checksum-verified.
A hand-edit is overwritten on next regeneration. Convention becomes containment.
"""
import yaml
import json
import sys
import hashlib
import stat
from pathlib import Path

FED_PATH = Path(__file__).parent / "federation.yaml"
OUT_DIR = Path(__file__).parent / "out"
AGENTS_DIR = Path(__file__).parent / "agents"

def load():
    with open(FED_PATH) as f:
        return yaml.safe_load(f)

def sha256_of(path):
    """Compute SHA256 of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def write_and_lock(path, content):
    """Write content, then chmod 444 (read-only). Generated files cannot be hand-edited."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    path.chmod(stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)  # 444

def servers_for(agent_id, agent_def, roles, servers):
    """Derive server list from role's capability grants."""
    role_name = agent_def["role"]
    grants = set(roles[role_name]["grant"])
    out = []
    for sid, sdef in servers.items():
        if set(sdef.get("capability", [])) & grants:
            out.append(sid)
    return sorted(out)

def skills_for(agent_id, agent_def, roles, skills, servers):
    """Derive skill list from role's capability grants + server capabilities."""
    role_name = agent_def["role"]
    grants = set(roles[role_name]["grant"])
    agent_servers = set(servers_for(agent_id, agent_def, roles, servers))
    out = []
    for skid, skdef in skills.items():
        if not isinstance(skdef, dict):
            continue
        owner = skdef.get("owner")
        if owner and owner in agent_servers:
            out.append({"id": skid, "owner": owner})
    return sorted(out, key=lambda s: s["id"])

def self_test(servers, roles, agents, skills):
    """Validate federation.yaml integrity before generating views."""
    fails = []
    warnings = []

    # Test 1: every capability in every role grant resolves to ≥1 server
    all_server_caps = set()
    for sdef in servers.values():
        all_server_caps.update(sdef.get("capability", []))

    for rname, rdef in roles.items():
        for cap in rdef["grant"]:
            if cap not in all_server_caps:
                fails.append(f"role '{rname}' grants capability '{cap}' but no server provides it")

    # Test 2: every server capability is granted by ≥1 role
    all_role_caps = set()
    for rdef in roles.values():
        all_role_caps.update(rdef["grant"])

    for sid, sdef in servers.items():
        for cap in sdef.get("capability", []):
            if cap not in all_role_caps:
                warnings.append(f"server '{sid}' has capability '{cap}' but no role grants it")

    # Test 3: every agent references a valid role
    for aid, adef in agents.items():
        if adef["role"] not in roles:
            fails.append(f"agent '{aid}' references unknown role '{adef['role']}'")

    # Test 4: 5 core organs exist
    core5 = {"arifos", "aforge", "geox", "wealth", "well"}
    missing = core5 - set(servers.keys())
    if missing:
        fails.append(f"core organs missing from server section: {missing}")

    # Test 5: every skill owner references a valid server
    for skid, skdef in skills.items():
        if not isinstance(skdef, dict):
            fails.append(f"skill '{skid}' is not a dict (YAML parse error)")
            continue
        owner = skdef.get("owner")
        if owner and owner not in servers:
            warnings.append(f"skill '{skid}' owner '{owner}' is not a known server")

    return fails, warnings

def generate(fed):
    servers = fed["server"]
    roles = fed["role"]
    agents = fed["agent"]
    skills = fed["skill"]

    # ── SELF-TEST before generating anything ──
    test_fails, test_warnings = self_test(servers, roles, agents, skills)
    if test_fails:
        print("=== SELF-TEST: FAIL ===")
        for f in test_fails:
            print(f"  ✗ {f}")
        for w in test_warnings:
            print(f"  ⚠ {w}")
        print("\nAborting — fix federation.yaml before generating.")
        return None, True

    OUT_DIR.mkdir(exist_ok=True)
    AGENTS_DIR.mkdir(exist_ok=True)
    generated_paths = []

    # ── VIEW 1: A2A agent cards (agents/<name>/agent.yaml) ──
    surface = {}
    for aid, adef in agents.items():
        agent_servers = servers_for(aid, adef, roles, servers)
        agent_skills = skills_for(aid, adef, roles, skills, servers)
        surface[aid] = agent_servers

        role_name = adef["role"]
        role_def = roles[role_name]
        fi = adef.get("fi", "")

        card = {
            "# Generated from federation.yaml": "DO NOT EDIT — edit federation.yaml",
            "name": aid,
            "description": f"{aid} — {role_def['description']}",
            "version": "1.0.0",
            "role": role_name,
            "fi": fi,
            "runtime": adef.get("runtime", "unknown"),
            "capabilities": {
                "streaming": True,
                "pushNotifications": False,
                "opaqueExecution": True,
            },
            "server": {
                sid: {
                    "port": servers[sid].get("port"),
                    "tier": servers[sid]["tier"],
                    "surface": servers[sid]["surface"],
                    "capability": servers[sid]["capability"],
                }
                for sid in agent_servers
            },
            "skill": agent_skills,
            "grant": sorted(role_def["grant"]),
            "securitySchemes": {
                "bearer": {
                    "type": "http",
                    "scheme": "bearer",
                    "description": "arifOS SCT token",
                }
            },
            "defaultInputModes": ["text"],
            "defaultOutputModes": ["text"],
        }
        if adef.get("note"):
            card["note"] = adef["note"]

        p = AGENTS_DIR / aid / "agent.yaml"
        # unlock before write (in case previously read-only)
        if p.exists():
            p.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
        yaml_content = yaml.dump(card, sort_keys=False, default_flow_style=False, width=120)
        write_and_lock(p, yaml_content)
        generated_paths.append(p)

    # ── VIEW 2: organ-view.yaml (tier=organ only) ──
    organ = {k: v for k, v in servers.items() if v.get("tier") == "organ"}
    organ_content = yaml.dump(
        {"# Generated from federation.yaml — DO NOT EDIT": "see federation.yaml",
         "organ": organ},
        sort_keys=False, default_flow_style=False)
    p = OUT_DIR / "organ-view.yaml"
    if p.exists():
        p.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
    write_and_lock(p, organ_content)
    generated_paths.append(p)

    # ── VIEW 3: capability-index.json (capability → servers) ──
    cap_idx = {}
    for sid, sdef in servers.items():
        for cap in sdef.get("capability", []):
            cap_idx.setdefault(cap, []).append(sid)
    p = OUT_DIR / "capability-index.json"
    if p.exists():
        p.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
    write_and_lock(p, json.dumps(cap_idx, indent=2, sort_keys=True))
    generated_paths.append(p)

    # ── VIEW 4: call-view.yaml (role → grants → servers) ──
    call = {}
    for rname, rdef in roles.items():
        grants = set(rdef["grant"])
        matched = sorted(sid for sid, sdef in servers.items()
                         if set(sdef.get("capability", [])) & grants)
        call[rname] = {"grant": sorted(grants), "server": matched}
    call_content = yaml.dump(
        {"# Generated from federation.yaml — DO NOT EDIT": "see federation.yaml",
         "role_call": call},
        sort_keys=False, default_flow_style=False)
    p = OUT_DIR / "call-view.yaml"
    if p.exists():
        p.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
    write_and_lock(p, call_content)
    generated_paths.append(p)

    # ── DRIFT REPORT ──
    declared = len(servers)
    registered = sum(1 for s in servers.values() if s.get("status") in ("live", "simulation"))
    public = sum(1 for s in servers.values() if s.get("surface") == "public")
    orphans = [k for k, v in skills.items()
               if not isinstance(v, dict) or v.get("owner") is None]

    lines = []
    lines.append("=" * 60)
    lines.append("DRIFT REPORT — derived from federation.yaml")
    lines.append("=" * 60)
    lines.append(f"declared servers  : {declared}")
    lines.append(f"registered (live) : {registered}")
    lines.append(f"public surface    : {public}")
    lines.append(f"orphan skills     : {len(orphans)}")
    if orphans:
        lines.append(f"  orphans: {orphans}")
    lines.append("")

    lines.append("ROLE-DERIVED PARITY (least-capability, not forced equality)")
    lines.append("-" * 60)
    for aid in sorted(surface, key=lambda x: -len(surface[x])):
        role = agents[aid]["role"]
        n_skills = len([s for s in skills.values()
                        if isinstance(s, dict) and s.get("owner") in set(surface[aid])])
        lines.append(f"  {aid:12s} [{role:10s}] -> {len(surface[aid])} servers, {n_skills} skills")
    lines.append("")

    core5 = {"arifos", "aforge", "geox", "wealth", "well"}
    invariant_fails = []
    for aid in agents:
        missing = core5 - set(surface[aid])
        if missing:
            invariant_fails.append(f"{aid} missing core organ(s): {missing}")

    lines.append("INVARIANT: 5 core organs universal to ALL agents")
    lines.append("-" * 60)
    if invariant_fails:
        for f in invariant_fails:
            lines.append(f"  FAIL: {f}")
    else:
        lines.append("  PASS — every agent has all 5 core organs")
    lines.append("")

    lines.append("ORPHAN CHECK: every skill has an owner")
    lines.append("-" * 60)
    if orphans:
        for o in orphans:
            lines.append(f"  ORPHAN: {o} (owner: null)")
    else:
        lines.append(f"  PASS — all {len(skills)} skills have owners")
    lines.append("")

    if test_warnings:
        lines.append("SELF-TEST WARNINGS (non-fatal)")
        lines.append("-" * 60)
        for w in test_warnings:
            lines.append(f"  ⚠ {w}")
        lines.append("")

    report = "\n".join(lines)
    p = OUT_DIR / "drift-report.txt"
    if p.exists():
        p.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
    write_and_lock(p, report)
    generated_paths.append(p)

    # ── CHECKSUMS — integrity enforcement ──
    # Generated files are read-only (444). Checksums detect tampering.
    checksums = {}
    for p in generated_paths:
        rel = p.relative_to(FED_PATH.parent)
        checksums[str(rel)] = sha256_of(p)

    checksum_path = OUT_DIR / ".checksums.sha256"
    if checksum_path.exists():
        checksum_path.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
    checksum_content = "\n".join(f"{h}  {p}" for p, h in sorted(checksums.items())) + "\n"
    write_and_lock(checksum_path, checksum_content)

    return report, bool(invariant_fails or orphans)

def main():
    fed = load()
    result = generate(fed)
    if result[0] is None:
        sys.exit(1)
    report, has_issues = result
    print(report)
    sys.exit(1 if has_issues else 0)

if __name__ == "__main__":
    main()
