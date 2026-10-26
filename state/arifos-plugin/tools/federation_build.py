#!/usr/bin/env python3
"""federation_build.py v2 — skill projection + drift census + INIT guard + integrity.
Consumer: all AAA warga + weekly cron. Failure classes named: (1) registry staleness
(13/255 vs live 22-25/778, 2026-10-22) (2) projection drift/broken pointers (3) INIT
block clobber by harness regen. FP-01 generated outputs · FP-03 pointers never copies
· FP-06 receipts every run · AUTO-MAINTENANCE ONLY (additive links + verbatim block
restore). NEVER deletes, NEVER touches governance/, identities/, hooks, or frozen trees
(HAROM#4: healer may not heal its own gate). Removals + plugin installs = report-only,
picker pen stays sovereign (FP-05)."""
import datetime, json, os, re, sys, urllib.request

ROOT = "/root"
SRC = os.path.join(ROOT, "AAA", "skills")
PLUGIN = os.path.join(ROOT, "AAA", "state", "arifos-plugin")
TARGETS = ["/root/.kimi-code/skills", "/root/.qwen/skills", "/root/.codex/skills",
           "/root/.gemini/skills", "/root/.config/opencode/skills", "/root/.claude/skills", "/root/.grok/skills"]
ENTRY_FILES = ["/root/AGENTS.md", "/root/.kimi-code/AGENTS.md", "/root/.config/opencode/AGENTS.md",
               "/root/CLAUDE.md", "/root/QWEN.md", "/root/GEMINI.md"]
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
CATEGORIES = ["governance", "research", "engineering", "execution", "memory", "communication", "domain"]
RULES = {
    "governance": r"audit|judge|seal|authorit|constitution|floor|govern|haram|halal|witness|claim|f13|kernel|verdict|court|adil|faham|salam|promot|sovereign|invariant|bijaksana",
    "research": r"research|source|literature|evidence|fact|probe|contradiction|falsif|verif|tengok|rasa|observ|census|drift|reality|calibrat|predict",
    "engineering": r"code|arch|refactor|debug|deploy|build|test|ci[-_]|rust|python|mcp|plugin|api|server|engineer|infra|docker|git|compile",
    "execution": r"execut|runbook|task[-_]?plan|release|rollback|ops|cron|forge|run[-_]|tempa",
    "memory": r"memory|receipt|lesson|scar|eureka|knowledge|atlas|recall|ingest|carri?y?[-_]?forward|vault|distill",
    "communication": r"brief|report|memo|summari|email|render|voice|telegram|present|writ|makcik|bridge|human|narat",
    "domain": r"geox|wealth|well[-_]?|petronas|geoscience|market|capital|reservoir|audio|somatic|asr|tts|music|basin|seismic|petro|glof|chron",
}
NUM_CORE = re.compile(r"^\d{3}-")
INIT_MARKER = "AAA-FEDERATION-INIT"
INIT_BLOCK = """<!-- BEGIN AAA-FEDERATION-INIT · v1 · staged SOT: /root/AAA/state/arifos-plugin/prompts/FEDERATION-INIT-v1.md -->
### FEDERATION INIT v1 (binding summary · sovereign 2026-10-22)
- Authority: ARIF=sovereign · arifOS=law · AAA=institution · A-FORGE=hands. Authority never self-widens (VOID).
- Capability = Declared ∩ Callable ∩ Authorized ∩ Competent. Installed≠Operational. Probe before trust.
- Skills: /root/AAA/skills — referenced, NEVER copied. ONE loop = APEX-ZEN Reality Loop. Receipt on every mutation.
- Roles: lane:333 propose · lane:555 verify · lane:888 judge · A-FORGE execute (requires seal_verdict_id).
- Session boot: identity, authority, capability visibility, active tools/skills/MCPs/hooks, constraints, task. Unknown → state UNKNOWN.
- Full contract: /root/AAA/state/arifos-plugin/prompts/FEDERATION-INIT-v1.md
<!-- END AAA-FEDERATION-INIT -->"""


def classify(name):
    hits = [c for c in CATEGORIES if re.search(RULES[c], name, re.I)]
    if NUM_CORE.match(name):
        hits.append("governance")
    return sorted(set(hits)) or ["unclassified"]


def skill_index():
    entries, dist = {}, {}
    for name in sorted(os.listdir(SRC)):
        p = os.path.join(SRC, name)
        if not os.path.isdir(p) or name.startswith("."):
            continue
        cats = classify(name)
        entries[name] = cats
        for c in cats:
            dist[c] = dist.get(c, 0) + 1
    n_top = len([x for x in os.listdir(SRC)])
    n_dirs_real = len([x for x in os.listdir(SRC) if os.path.isdir(os.path.join(SRC, x)) and not os.path.islink(os.path.join(SRC, x))])
    n_dirs_link = len([x for x in os.listdir(SRC) if os.path.isdir(os.path.join(SRC, x)) and os.path.islink(os.path.join(SRC, x))])
    out = {"_GENERATED": "federation_build.py — DO NOT HAND-EDIT (FP-01)", "generated_at": NOW,
           "source_of_truth": SRC, "skill_count": len(entries), "distribution": dist, "index": entries,
           "definitions": {
               "skill_count": "non-hidden top-level entries where isdir() true (real dirs + symlink-dirs)",
               "distribution": "MULTI-LABEL counts — one skill may count in several categories; sum > skill_count by design",
               "top_entries_ls": n_top, "real_dirs": n_dirs_real, "symlink_dirs": n_dirs_link,
               "note": "SKILL.md recursive count is larger (nested domain trees under skills/domains/**)"}}
    with open(os.path.join(PLUGIN, "capabilities", "skill-index.generated.json"), "w") as f:
        json.dump(out, f, indent=1)
    return len(entries), dist


def project(target):
    """Additive pointer projection. Repairs stale/broken pointers; preserves real content."""
    os.makedirs(target, exist_ok=True)
    linked = kept = preserved = repaired = 0
    for name in sorted(os.listdir(SRC)):
        src = os.path.join(SRC, name)
        if not os.path.isdir(src) or name.startswith("."):
            continue
        dst = os.path.join(target, name)
        if os.path.islink(dst):
            if os.readlink(dst) == src:
                kept += 1
            else:
                try:
                    os.remove(dst); os.symlink(src, dst); repaired += 1
                except OSError:
                    preserved += 1
        elif os.path.exists(dst):
            preserved += 1  # copies preserved — conversion = picker pen, never auto (stability first)
        else:
            try:
                os.symlink(src, dst); linked += 1
            except OSError:
                preserved += 1
    return linked, kept, repaired, preserved


def pointer_integrity(target):
    broken = 0
    if not os.path.isdir(target):
        return -1
    for name in os.listdir(target):
        p = os.path.join(target, name)
        if os.path.islink(p) and not os.path.exists(p):
            broken += 1
    return broken


def init_guard():
    """Report missing INIT markers; restore verbatim block only (transport, not authoring)."""
    status = {}
    for f in ENTRY_FILES:
        try:
            txt = open(f, encoding="utf-8", errors="ignore").read()
        except OSError:
            status[f] = "UNREADABLE"
            continue
        if INIT_MARKER in txt:
            status[f] = "WIRED"
        elif os.access(f, os.W_OK):
            with open(f, "a", encoding="utf-8") as fh:
                fh.write("\n" + INIT_BLOCK + "\n")
            status[f] = "RESTORED_VERBATIM"
        else:
            status[f] = "MISSING_READONLY"
    return status


def drift_census():
    def jload(p):
        try:
            return json.load(open(p))
        except Exception:
            return None

    def count_servers(p):
        d = jload(p) or {}
        for k in ("mcpServers", "servers", "mcp"):
            if isinstance(d.get(k), dict):
                return len(d[k])
        return -1

    live = {"kimi_mcp": count_servers(os.path.join(ROOT, ".kimi-code", "mcp.json")),
            "opencode_mcp": count_servers(os.path.join(ROOT, ".config", "opencode", "opencode.json")),
            "one_mcp": count_servers(os.path.join(ROOT, ".config", "1mcp", "mcp.json"))}
    for label, path in (("skills_AAA", SRC), ("skills_kimi", TARGETS[0]), ("skills_qwen", TARGETS[1]),
                        ("skills_codex", TARGETS[2]), ("skills_gemini", TARGETS[3]),
                        ("skills_opencode", TARGETS[4]), ("skills_claude", TARGETS[5])):
        try:
            live[label] = len([d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))])
        except Exception:
            live[label] = -1
    reg = jload(os.path.join(ROOT, ".config", "capability_registry.json")) or {}
    declared = {"registry_mcp": reg.get("mcp_servers_configured"),
                "registry_skill_AAA": (reg.get("skill_libraries") or {}).get("AAA"),
                "refreshed_at": reg.get("refreshed_at")}
    return declared, live


def arif_notify(payload):
    """Metabolism ingest via arifFlow REST :7073/ingest. Shape verified live 2026-10-22:
    receipt_id, created_at, cooling_decision(None|Hold|Clamp|Bypass) required.
    Best-effort; never breaks the run."""
    import subprocess, uuid
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    body = {"receipt_id": str(uuid.uuid4()), "actor_id": "fi-008-cron",
            "session_id": "SEAL-619c8884c1ad4134", "step_type": "Execute", "step_number": 1,
            "cost_ns": 0, "epistemic_label": "Derivation", "floor_verdict": "Pass",
            "witness_organs": ["arifos"], "payload": payload,
            "created_at": now, "timestamp": now, "cooling_decision": "None"}
    try:
        out = subprocess.run(["curl", "-s", "-m", "5", "-X", "POST",
                              "http://127.0.0.1:7073/ingest",
                              "-H", "Content-Type: application/json",
                              "-d", json.dumps(body)], capture_output=True, text=True, timeout=8)
        return "INGESTED" if '"error"' not in out.stdout[:25] else "SKIP (%s)" % out.stdout[:60]
    except Exception as e:
        return "SKIP (%s)" % type(e).__name__


def main():
    check_only = "--check" in sys.argv
    os.makedirs(os.path.join(PLUGIN, "receipts"), exist_ok=True)
    n, dist = skill_index()
    proj = {}
    if not check_only:
        for t in TARGETS:
            if os.path.isdir(t):
                proj[t] = dict(zip(("linked", "kept", "repaired", "preserved"), project(t)))
    broken = {t: pointer_integrity(t) for t in TARGETS if os.path.isdir(t)}
    init = init_guard()
    declared, live = drift_census()
    problems = []
    if any(v > 0 for v in broken.values()):
        problems.append(f"broken_pointers={broken}")
    if any(v == "MISSING_READONLY" or v == "UNREADABLE" for v in init.values()):
        problems.append(f"init_guard={init}")
    if declared.get("registry_skill_AAA") not in (None, live.get("skills_AAA")):
        problems.append(f"registry_stale: {declared.get('registry_skill_AAA')} vs live {live.get('skills_AAA')}")
    receipt = {"_GENERATED": "federation_build.py — DO NOT HAND-EDIT (FP-06)", "run_at": NOW,
               "mode": "check" if check_only else "apply-additive",
               "skill_index": {"skills": n, "distribution": dist},
               "projection": proj, "pointer_integrity": broken, "init_guard": init,
               "drift": {"registry_declared": declared, "live_disk": live},
               "problems": problems,
               "state_labels": {"projection": "PRODUCED — runtime consumption per-harness",
                                "claude_grok_codex": "whole-dir symlinks to SOT (pointer pure) — no copies exist; REFUTED claim corrected 2026-10-22"}}
    with open(os.path.join(PLUGIN, "receipts", "drift.generated.json"), "w") as f:
        json.dump(receipt, f, indent=1)
    verdict = "CLEAN" if not problems else "DRIFT"
    print(f"[{verdict}] skills={n} mode={receipt['mode']}")
    print(f"projection: " + "; ".join(f"{os.path.basename(k)}={v}" for k, v in proj.items()) or "check-only")
    print(f"broken_pointers: {broken}")
    print(f"init_guard: {init}")
    print(f"registry vs live: mcp {declared.get('registry_mcp')} vs {live.get('kimi_mcp')}/{live.get('opencode_mcp')};"
          f" skills {declared.get('registry_skill_AAA')} vs {live.get('skills_AAA')}")
    if problems:
        print("problems: " + " | ".join(problems))
        note = {"step_type": "Execute", "actor_id": "fi-008-cron", "payload": {"alert": "federation drift", "problems": problems}}
        print("arifFlow notify:", arif_notify(note))
    sys.exit(0 if not problems else 2)


if __name__ == "__main__":
    main()
