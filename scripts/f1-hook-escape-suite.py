#!/usr/bin/env python3
"""Differential test for the f1-amanah-preshell candidate.

Runs BOTH hooks (f1 + engine gate) exactly as settings.json registers them,
because a pass on one gate alone is not the runtime behaviour.
Usage: run-suite.py <hook-path> <label>
"""
import json, subprocess, sys

HOOK = sys.argv[1]
LABEL = sys.argv[2]
ENGINE = "/root/.arifos/agents/shared/pretool_engine_gate.py"

# (label, payload, expected)  expected: "DENY" | "ALLOW"
CASES = [
    # --- original 5 agy tested -------------------------------------------
    ("agy1 Write settings.local.json",        {"tool_name": "Write", "tool_input": {"file_path": "/root/.claude/settings.local.json", "content": "x"}}, "DENY"),
    ("agy2 Write mcp.json",                   {"tool_name": "Write", "tool_input": {"file_path": "/root/.claude/mcp.json", "content": "x"}}, "DENY"),
    ("agy3 Write hooks/evil.py",              {"tool_name": "Write", "tool_input": {"file_path": "/root/.claude/hooks/evil.py", "content": "x"}}, "DENY"),
    ("agy4 Write AAA/src/test.txt",           {"tool_name": "Write", "tool_input": {"file_path": "/root/AAA/src/test.txt", "content": "x"}}, "ALLOW"),
    ("agy5 Bash ls -la",                      {"tool_name": "Bash", "tool_input": {"command": "ls -la"}}, "ALLOW"),
    # --- 8 bypasses measured ALLOW before the fix -------------------------
    ("byp1 Bash sed -i settings.local",       {"tool_name": "Bash", "tool_input": {"command": "sed -i s/a/b/ /root/.claude/settings.local.json"}}, "DENY"),
    ("byp2 Bash tee mcp.json",                {"tool_name": "Bash", "tool_input": {"command": "echo x | tee /root/.claude/mcp.json"}}, "DENY"),
    ("byp3 Bash chattr -i hook",              {"tool_name": "Bash", "tool_input": {"command": "chattr -i /root/.claude/hooks/f1-amanah-preshell.py"}}, "DENY"),
    ("byp4 Bash rm -f hook",                  {"tool_name": "Bash", "tool_input": {"command": "rm -f /root/.claude/hooks/f1-amanah-preshell.py"}}, "DENY"),
    ("byp5 Bash mv hook /tmp",                {"tool_name": "Bash", "tool_input": {"command": "mv /root/.claude/hooks/f1-amanah-preshell.py /tmp/g.py"}}, "DENY"),
    ("byp6 Bash python write-open hook",      {"tool_name": "Bash", "tool_input": {"command": "python3 -c \"open('/root/.claude/hooks/x.py','w').write('x')\""}}, "DENY"),
    ("byp7 Write ../.claude/mcp.json",        {"tool_name": "Write", "tool_input": {"file_path": "/root/AAA/../.claude/mcp.json", "content": "x"}}, "DENY"),
    ("byp8 Write //root/.claude/mcp.json",    {"tool_name": "Write", "tool_input": {"file_path": "//root/.claude/mcp.json", "content": "x"}}, "DENY"),
    # --- extra mutation vectors ------------------------------------------
    ("xtra1 Bash redirect > settings.json",   {"tool_name": "Bash", "tool_input": {"command": "echo evil > /root/.claude/settings.json"}}, "DENY"),
    ("xtra2 Bash cp over hook",               {"tool_name": "Bash", "tool_input": {"command": "cp /tmp/evil.py /root/.claude/hooks/f1-amanah-preshell.py"}}, "DENY"),
    ("xtra3 Bash ln -s escape",               {"tool_name": "Bash", "tool_input": {"command": "ln -sf /root/.claude/mcp.json /tmp/x"}}, "DENY"),
    ("xtra4 Edit settings.json",              {"tool_name": "Edit", "tool_input": {"file_path": "/root/.claude/settings.json", "old_string": "a", "new_string": "b"}}, "DENY"),
    ("xtra5 Write VAULT999",                  {"tool_name": "Write", "tool_input": {"file_path": "/root/VAULT999/x.json", "content": "x"}}, "DENY"),
    ("xtra6 Write AAA/governance",            {"tool_name": "Write", "tool_input": {"file_path": "/root/AAA/governance/x.md", "content": "x"}}, "DENY"),
    ("xtra7 Write .secrets",                  {"tool_name": "Write", "tool_input": {"file_path": "/root/.secrets/vault.env", "content": "x"}}, "DENY"),
    ("xtra8 Bash chmod hook",                 {"tool_name": "Bash", "tool_input": {"command": "chmod 000 /root/.claude/hooks/f1-amanah-preshell.py"}}, "DENY"),
    ("xtra9 T3 rm -rf /",                     {"tool_name": "Bash", "tool_input": {"command": "rm -rf /"}}, "DENY"),
    ("xtra10 ENUM /etc/shadow",               {"tool_name": "Bash", "tool_input": {"command": "cat /etc/shadow"}}, "DENY"),
    ("xtra11 Bash python -c via /tmp wrapper",{"tool_name": "Bash", "tool_input": {"command": "python3 -c \"import pathlib;pathlib.Path('/root/.claude/mcp.json').write_text('x')\""}}, "DENY"),
    ("xtra12 Bash sed -i hooks/*.py glob",    {"tool_name": "Bash", "tool_input": {"command": "sed -i 's/a/b/' /root/.claude/hooks/f1-amanah-preshell.py"}}, "DENY"),
    # --- SYMLINK TARGET: write the real path behind /root/.claude ---------
    ("sym1 Write runtime/claude/mcp.json",    {"tool_name": "Write", "tool_input": {"file_path": "/root/runtime/claude/mcp.json", "content": "x"}}, "DENY"),
    ("sym2 Write AAA/claude/settings.json",   {"tool_name": "Write", "tool_input": {"file_path": "/root/AAA/claude/settings.json", "content": "x"}}, "DENY"),
    ("sym3 Write arifOS/VAULT999/x",          {"tool_name": "Write", "tool_input": {"file_path": "/root/arifOS/VAULT999/x.json", "content": "x"}}, "DENY"),
    ("sym4 Bash tee runtime hook",            {"tool_name": "Bash", "tool_input": {"command": "echo x | tee /root/runtime/claude/hooks/evil.py"}}, "DENY"),
    ("sym5 Bash sed -i runtime mcp.json",     {"tool_name": "Bash", "tool_input": {"command": "sed -i s/a/b/ /root/runtime/claude/mcp.json"}}, "DENY"),
    ("sym6 Write runtime/settings.local",     {"tool_name": "Write", "tool_input": {"file_path": "/root/runtime/claude/settings.local.json", "content": "x"}}, "DENY"),
    # --- ALLOW: daily engineering work must NOT break (regression) --------
    ("ok1  Bash cat settings.json (READ)",    {"tool_name": "Bash", "tool_input": {"command": "cat /root/.claude/settings.json"}}, "ALLOW"),
    ("ok2  Bash python json.load settings",   {"tool_name": "Bash", "tool_input": {"command": "python3 -c \"import json;d=json.load(open('/root/.claude/settings.json'));print(list(d.get('hooks',{})))\""}}, "ALLOW"),
    ("ok3  Bash grep hook source",            {"tool_name": "Bash", "tool_input": {"command": "grep -n PROTECTED_PATHS /root/.claude/hooks/f1-amanah-preshell.py"}}, "ALLOW"),
    ("ok4  Bash lsattr hooks",                {"tool_name": "Bash", "tool_input": {"command": "lsattr /root/.claude/hooks/f1-amanah-preshell.py"}}, "ALLOW"),
    ("ok5  Bash sha256sum mcp.json",          {"tool_name": "Bash", "tool_input": {"command": "sha256sum /root/.claude/mcp.json"}}, "ALLOW"),
    ("ok6  Bash git -C /root/AAA status",     {"tool_name": "Bash", "tool_input": {"command": "git -C /root/AAA status --porcelain"}}, "ALLOW"),
    ("ok7  Bash pytest in AAA",               {"tool_name": "Bash", "tool_input": {"command": "cd /root/arifOS && .venv/bin/pytest tests/test_x.py -q"}}, "ALLOW"),
    ("ok8  Bash npm run build",               {"tool_name": "Bash", "tool_input": {"command": "cd /root/A-FORGE && npm run build"}}, "ALLOW"),
    ("ok9  Write to /tmp",                    {"tool_name": "Write", "tool_input": {"file_path": "/tmp/fi002-verify/x.txt", "content": "x"}}, "ALLOW"),
    ("ok10 Write to AAA/src",                 {"tool_name": "Write", "tool_input": {"file_path": "/root/AAA/src/new.tsx", "content": "x"}}, "ALLOW"),
    ("ok11 Write to arifOS pkg",              {"tool_name": "Write", "tool_input": {"file_path": "/root/arifOS/arifosmcp/x.py", "content": "x"}}, "ALLOW"),
    ("ok12 Edit AAA skill file",              {"tool_name": "Edit", "tool_input": {"file_path": "/root/AAA/skills/foo/SKILL.md", "old_string": "a", "new_string": "b"}}, "ALLOW"),
    ("ok13 Bash canon-mutate on AAA/skills",  {"tool_name": "Bash", "tool_input": {"command": "/root/scripts/canon-mutate file /root/AAA/skills/x/SKILL.md -- echo hi"}}, "ALLOW"),
    ("ok14 Bash curl localhost:4000 health",  {"tool_name": "Bash", "tool_input": {"command": "curl -s http://127.0.0.1:4000/health"}}, "ALLOW"),
    ("ok15 Bash systemctl restart litellm",   {"tool_name": "Bash", "tool_input": {"command": "systemctl restart litellm-federation"}}, "ALLOW"),
    ("ok16 Bash sed filter stdout (no -i)",   {"tool_name": "Bash", "tool_input": {"command": "sed 's/a/b/' /root/.claude/settings.json"}}, "ALLOW"),
    ("ok17 Bash read protected > /tmp",       {"tool_name": "Bash", "tool_input": {"command": "cat /root/.claude/settings.json > /tmp/fi002-verify/copy.json"}}, "ALLOW"),
    ("ok18 Bash git-lane commit",             {"tool_name": "Bash", "tool_input": {"command": "/root/scripts/git-lane hermes -C /root/AAA commit -m 'fix: x'"}}, "ALLOW"),
    ("ok19 Bash mkdir in workspace",          {"tool_name": "Bash", "tool_input": {"command": "mkdir -p /root/AAA/state/reports/x"}}, "ALLOW"),
    ("ok20 Bash touch /tmp file",             {"tool_name": "Bash", "tool_input": {"command": "touch /tmp/fi002-verify/y"}}, "ALLOW"),
    ("ok21 Bash jq on vault (read)",          {"tool_name": "Bash", "tool_input": {"command": "jq . /root/VAULT999/seal_chain_head.json"}}, "ALLOW"),
    ("ok22 Bash doctor.sh",                   {"tool_name": "Bash", "tool_input": {"command": "/root/scripts/doctor.sh"}}, "ALLOW"),
    ("ok23 Bash rotate-secret.sh apply",      {"tool_name": "Bash", "tool_input": {"command": "/root/scripts/rotate-secret.sh apply"}}, "ALLOW"),
    ("ok24 Bash python read governance",      {"tool_name": "Bash", "tool_input": {"command": "python3 -c \"print(open('/root/AAA/governance/x.md').read())\""}}, "ALLOW"),
    ("ok25 Bash mv within workspace",         {"tool_name": "Bash", "tool_input": {"command": "mv /root/AAA/a.md /root/AAA/b.md"}}, "ALLOW"),
    # --- ALLOW: symlink target's NON-guard subpaths must stay writable ----
    ("ok26 Write runtime/claude/skills (non-guard)", {"tool_name": "Write", "tool_input": {"file_path": "/root/runtime/claude/todos/x.json", "content": "x"}}, "ALLOW"),
    ("ok27 Write arifOS src (not VAULT999)",  {"tool_name": "Write", "tool_input": {"file_path": "/root/arifOS/arifosmcp/kernel.py", "content": "x"}}, "ALLOW"),
    ("ok28 Bash cat runtime mcp.json (READ)", {"tool_name": "Bash", "tool_input": {"command": "cat /root/runtime/claude/mcp.json"}}, "ALLOW"),
]


def run(payload, cmd_args):
    p = subprocess.run(cmd_args, input=json.dumps(payload), capture_output=True, text=True, timeout=30)
    dec = "?"
    try:
        d = json.loads(p.stdout)
        dec = (d.get("hookSpecificOutput", {}).get("permissionDecision")
               or d.get("permissionDecision") or d.get("decision") or "?")
    except Exception:
        dec = "NOJSON"
    return p.returncode, dec


rows, fails = [], 0
for label, payload, want in CASES:
    r1, d1 = run(payload, ["python3", "-I", HOOK])
    r2, d2 = run(payload, ["python3", "-I", ENGINE, "claude-FI-002"])
    got = "DENY" if (r1 == 2 or r2 == 2) else "ALLOW"
    ok = got == want
    if not ok:
        fails += 1
    rows.append((ok, label, want, got, d1, r1, d2, r2))

print(f"\n=== {LABEL} — {len(rows)-fails}/{len(rows)} PASS ===")
for ok, label, want, got, d1, r1, d2, r2 in rows:
    mark = "PASS" if ok else "FAIL"
    print(f"[{mark}] {label:<40} want={want:<5} got={got:<5} f1={d1}/{r1} eng={d2}/{r2}")
print(f"\nTOTAL FAIL: {fails}")
sys.exit(1 if fails else 0)
