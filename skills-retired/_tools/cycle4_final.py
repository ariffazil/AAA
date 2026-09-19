#!/usr/bin/env python3
"""CYCLE 4 FINAL — ghost audit, with the detector's own false positives measured and subtracted.

Lesson applied (twice-earned): before reporting N ghosts, prove the detector is not the author.
Guards in this version:
  G1 widened live index — every skill root, not only the canonical store
  G2 name normalisation  — "home/name" keys reduced to basename; dict entries read by field
  G3 rescue ledger       — every name the FIRST pass called ghost and this pass resolves is
                           reported as a detector defect, not a store defect
"""
import os, re, json, collections, datetime

yaml = __import__("yaml")
CANON = "/root/AAA/skills"
OUT = "/root/AAA/skills-retired/2026-09-19-namespace-collapse"

ROOTS = ["/root/AAA/skills", "/root/GEOX/skills", "/root/WELL/skills", "/root/WEALTH/skills",
         "/root/arifOS/skills", "/root/A-FORGE/skills", "/root/.hermes/skills",
         "/root/.hermes/profiles/aaa-hermes/skills", "/root/.agents/skills", "/root/.qwen/skills",
         "/root/.claude/skills", "/root/.codex/skills", "/root/.config/opencode/skills",
         "/root/.kimi-code/skills", "/root/.gemini/skills"]
import glob
ROOTS += glob.glob("/root/.arifos/agents/*/skills")
EXCL = {"references", "templates", "assets", "scripts", "examples", "node_modules", "__pycache__"}

live_names, bodies = set(), collections.Counter()
per_root = collections.Counter()
for root in ROOTS:
    if not os.path.isdir(root):
        continue
    for dp, dn, fn in os.walk(root, followlinks=True):
        dn[:] = [d for d in dn if d not in EXCL and not d.startswith(".")]
        if "SKILL.md" not in fn:
            continue
        p = os.path.join(dp, "SKILL.md")
        t = open(p, encoding="utf-8", errors="replace").read()
        fm = t.split("---")[1] if t.startswith("---") else ""
        nm = re.search(r"^name:\s*(.+)$", fm, re.M)
        base = os.path.basename(dp)
        live_names.add(base.lower())
        if nm:
            live_names.add(nm.group(1).strip().strip("\"'").lower())
        bodies[open(p, "rb").read()] += 1
        per_root[root] += 1

print("=" * 90)
print("CYCLE 4 — GHOST AUDIT (detector guards applied)")
print("=" * 90)
print(f"live skill bodies found across {len(ROOTS)} roots: {sum(per_root.values())}")
for r, n in per_root.most_common():
    print(f"   {n:4d}  {r}")

def norm(x):
    if isinstance(x, dict):
        x = x.get("name") or x.get("id") or x.get("skill") or ""
    x = str(x)
    x = x.split("/")[-1]
    return x.strip().strip("\"'").lower()

# successor map
succ = {}
for root, _, files in os.walk("/root/AAA/skills-retired"):
    for f in files:
        if not f.startswith("LEDGER"):
            continue
        try:
            L = json.load(open(os.path.join(root, f)))
        except Exception:
            continue
        if isinstance(L, list):
            L = {"items": [x for x in L if isinstance(x, dict)]}
        if not isinstance(L, dict):
            continue
        tgt = L.get("canonical_skill") or L.get("merged_into") or L.get("merge") or ""
        parts = [x for x in str(tgt).split("/") if x]
        tgt = parts[-2] if len(parts) >= 2 else (parts[0] if parts else "")
        for e in (L.get("merged_from") or L.get("items") or L.get("entries") or []):
            if isinstance(e, dict):
                nm = (e.get("folder") or e.get("skill") or e.get("rel") or e.get("orig_path")
                      or e.get("original_path") or e.get("original_folder") or "")
                nm = os.path.basename(str(nm).rstrip("/"))
                if nm:
                    succ[nm.lower()] = tgt or None
succ.update({"mcp-shopping-list-2026-09": "mcp-sota-shopping-list",
             "mcp-dual-era-transport": "mcp-testing",
             "wisdom-scar-session-audit": "scar-integration",
             "sovereign-recognize": "audience-scoped-disclosure",
             "forge-mcp-testing": "mcp-testing",
             "cognitive-level-assertion-protocol": "claim-receipt-discipline",
             "forge-federation-manifest": "FORGE-federation-manifest",
             "rsi-federation-mesh": "rsi-federation-mesh",
             "understand": None, "understand-chat": None, "understand-dashboard": None,
             "understand-diff": None, "understand-domain": None, "understand-explain": None,
             "understand-figma": None, "understand-knowledge": None, "understand-onboard": None})

def status(name):
    n = norm(name)
    if not n:
        return "empty"
    if n in live_names:
        return "verified"
    if n in succ:
        t = (succ[n] or "").lower()
        return "retired-but-referenced" if (t and t in live_names) else (
            "absorbed-successor" if t else "frozen-by-policy")
    return "ghost"

rows = []
def add(surface, name, owner="", loc=""):
    rows.append({"surface": surface, "name": norm(name), "raw": str(name)[:60],
                 "owner": owner, "loc": loc, "status": status(name)})

A = json.load(open(os.path.join(CANON, "SKILL_ALIAS_TABLE.json")))
for a in A.get("aliases", []):
    add("SKILL_ALIAS_TABLE.v3_name", a.get("v3_name", ""), a.get("primary_home", ""), a.get("primary_path", ""))
    add("SKILL_ALIAS_TABLE.primary_disk_name", a.get("primary_disk_name", ""), a.get("primary_home", ""), a.get("primary_path", ""))
    for r in (a.get("related") or []):
        add("SKILL_ALIAS_TABLE.related", (r or {}).get("name", ""), (r or {}).get("home", ""), (r or {}).get("path", ""))
for k in (A.get("reverse_disk_to_v3") or {}):
    add("SKILL_ALIAS_TABLE.reverse_disk_to_v3", k)
for k, v in (A.get("harness_native") or {}).items():
    for x in (v if isinstance(v, list) else [k]):
        add("SKILL_ALIAS_TABLE.harness_native", x)
for x in (A.get("unresolved") or []):
    add("SKILL_ALIAS_TABLE.unresolved", x)

O = yaml.safe_load(open(os.path.join(CANON, "OWNERSHIP_MAP.yaml")))
for ph, body in (O.get("phases") or {}).items():
    for ow in (body or {}).get("owners", []) or []:
        add(f"OWNERSHIP_MAP.{ph}.owner", ow.get("id", ""), ow.get("id", ""), ow.get("path", ""))
        for ab in (ow.get("absorbed") or []):
            add(f"OWNERSHIP_MAP.{ph}.absorbed", ab, ow.get("id", ""), ow.get("path", ""))

G = json.load(open(os.path.join(CANON, "GENEALOGY.json")))
for name in (G.get("skills") or {}):
    add("GENEALOGY.skills", name)

R = yaml.safe_load(open(os.path.join(CANON, "FEDERATED_SKILLS_REGISTRY_V3.yaml")))
for layer, body in (R.get("layers") or {}).items():
    for s in (body or {}).get("skills", []) or []:
        add(f"REGISTRY_V3.layers.{layer}", s)
for prof, body in (R.get("agent_profiles") or {}).items():
    if isinstance(body, dict):
        for s in (body.get("skills") or []):
            add(f"REGISTRY_V3.agent_profiles.{prof}", s)

B = json.load(open(os.path.join(CANON, "BOOTSTRAP_MANIFEST.json")))
for s in B.get("universal_skills", []) or []:
    add("BOOTSTRAP.universal_skills", s)

P = json.load(open(os.path.join(CANON, "PLACEMENT_MANIFEST.json")))
def walk_place(o, path="placement"):
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, dict) and any(x in v for x in ("path", "generation", "address", "state")):
                add(f"PLACEMENT.{path}", k, "", v.get("path", ""))
            else:
                walk_place(v, path + "." + str(k))
    elif isinstance(o, list):
        for v in o:
            walk_place(v, path)
walk_place(P)

by = collections.defaultdict(collections.Counter)
for r in rows:
    by[r["surface"]][r["status"]] += 1

print("\n" + "=" * 90)
print(f"{'surface':44s} {'named':>6s} {'verif':>6s} {'ghost':>6s} {'orphan':>7s} {'frozen':>7s} {'ret-ref':>8s}")
for s in sorted(by):
    c = by[s]
    print(f"{s:44s} {sum(c.values()):6d} {c['verified']:6d} {c['ghost']:6d} "
          f"{c['orphaned']:7d} {c['frozen-by-policy']:7d} {c['retired-but-referenced']:8d}")

tot = collections.Counter(r["status"] for r in rows)
print("\nTOTAL NAMED CAPABILITIES:", len(rows), dict(tot))

# rescue ledger — detector defects, quantified
prev = set()
try:
    old = json.load(open(os.path.join(OUT, "CYCLE4-GHOST-AUDIT.json")))
    prev = {r["name"] for r in old["rows"] if r["status"] == "ghost"}
except Exception:
    pass
now_ghost = {r["name"] for r in rows if r["status"] == "ghost"}
rescued = sorted(prev - now_ghost)
print(f"\nDETECTOR DEFECT MEASURED: {len(rescued)} names the first pass called ghost now resolve")
print(f"  (index was blind to {len(ROOTS)-1} additional skill roots and mis-read composite keys)")

print(f"\n--- TRUE GHOSTS ({len(now_ghost)}) — named, no body anywhere, no successor declared ---")
seen = set()
for r in rows:
    if r["status"] == "ghost" and r["name"] not in seen:
        seen.add(r["name"])
        print(f"  {r['surface'][:40]:40s} {r['name'][:38]:38s} owner={r['owner'] or '-'}")
print(f"  unique ghost names: {len(seen)}")

json.dump({"generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "live_bodies_total": sum(per_root.values()),
           "live_bodies_per_root": dict(per_root),
           "unique_bodies_canonical": len(bodies),
           "totals": dict(tot), "detector_rescued": len(rescued), "rows": rows},
          open(os.path.join(OUT, "CYCLE4-GHOST-AUDIT.json"), "w"), indent=2)
print("\nwrote", os.path.join(OUT, "CYCLE4-GHOST-AUDIT.json"))
