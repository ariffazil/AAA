#!/usr/bin/env python3
"""CYCLE 4 (precise) — ghost audit per registry surface, using each file's OWN schema.
No greedy key-scanning: only fields that actually NAME a capability are read.
Status: verified | ghost | orphaned | retired-but-referenced | absorbed-successor
"""
import os, re, json, hashlib, collections, datetime, sys

CANON = "/root/AAA/skills"
OUT = "/root/AAA/skills-retired/2026-09-19-namespace-collapse"
EXCL = {"references", "templates", "assets", "scripts", "examples", "node_modules"}
yaml = __import__("yaml")

# ---------- live index ----------
live_paths, live_names, bodies = {}, set(), collections.Counter()
for dp, dn, fn in os.walk(CANON, followlinks=True):
    dn[:] = [d for d in dn if d not in EXCL and not d.startswith(".")]
    if "SKILL.md" not in fn:
        continue
    p = os.path.join(dp, "SKILL.md")
    t = open(p, encoding="utf-8", errors="replace").read()
    fm = t.split("---")[1] if t.startswith("---") else ""
    nm = re.search(r"^name:\s*(.+)$", fm, re.M)
    rel = os.path.relpath(dp, CANON)
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    live_paths[rel.lower()] = rel
    live_names.add(os.path.basename(rel).lower())
    if nm:
        live_names.add(nm.group(1).strip().lower())
    bodies[h] += 1

# ---------- successor map from today's ledgers ----------
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
for k, v in {"mcp-shopping-list-2026-09": "mcp-sota-shopping-list",
             "mcp-dual-era-transport": "mcp-testing",
             "wisdom-scar-session-audit": "scar-integration",
             "sovereign-recognize": "audience-scoped-disclosure",
             "forge-mcp-testing": "mcp-testing",
             "cognitive-level-assertion-protocol": "claim-receipt-discipline",
             "forge-federation-manifest": "FORGE-federation-manifest",
             "rsi-federation-mesh": "rsi-federation-mesh"}.items():
    succ.setdefault(k, v)

def status(name):
    n = (name or "").strip().lower()
    if not n:
        return "empty"
    if n in live_names or n in live_paths:
        return "verified"
    # a name may point at a path that exists under a taxonomy dir
    if any(n == os.path.basename(p) for p in live_paths.values()):
        return "verified"
    if n in succ:
        t = (succ[n] or "").lower()
        return "retired-but-referenced" if t and (t in live_names) else (
            "absorbed-successor" if t else "orphaned")
    return "ghost"

rows = []
def add(surface, name, owner="", loc=""):
    rows.append({"surface": surface, "name": name, "owner": owner, "loc": loc,
                 "status": status(name)})

# ---------- 1. SKILL_ALIAS_TABLE.json ----------
A = json.load(open(os.path.join(CANON, "SKILL_ALIAS_TABLE.json")))
for a in A.get("aliases", []):
    add("SKILL_ALIAS_TABLE.aliases(v3_name)", a.get("v3_name", ""), a.get("primary_home", ""),
        a.get("primary_path", ""))
    add("SKILL_ALIAS_TABLE.aliases(primary_disk_name)", a.get("primary_disk_name", ""),
        a.get("primary_home", ""), a.get("primary_path", ""))
    for r in a.get("related", []) or []:
        if isinstance(r, dict):
            add("SKILL_ALIAS_TABLE.aliases(related)", r.get("name", ""), r.get("home", ""),
                r.get("path", ""))
for k, v in (A.get("reverse_disk_to_v3") or {}).items():
    add("SKILL_ALIAS_TABLE.reverse_disk_to_v3", k)
for k, v in (A.get("harness_native") or {}).items():
    if isinstance(v, list):
        for x in v:
            add("SKILL_ALIAS_TABLE.harness_native", x)
    else:
        add("SKILL_ALIAS_TABLE.harness_native", k)
for x in (A.get("unresolved") or []):
    add("SKILL_ALIAS_TABLE.unresolved", x if isinstance(x, str) else str(x))

# ---------- 2. OWNERSHIP_MAP.yaml ----------
O = yaml.safe_load(open(os.path.join(CANON, "OWNERSHIP_MAP.yaml")))
for ph, body in (O.get("phases") or {}).items():
    for ow in (body or {}).get("owners", []) or []:
        add(f"OWNERSHIP_MAP.{ph}.(owner)", ow.get("id", ""), ow.get("id", ""), ow.get("path", ""))
        for ab in (ow.get("absorbed") or []):
            add(f"OWNERSHIP_MAP.{ph}.absorbed", ab, ow.get("id", ""), ow.get("path", ""))

# ---------- 3. GENEALOGY.json ----------
G = json.load(open(os.path.join(CANON, "GENEALOGY.json")))
for name, rec in (G.get("skills") or {}).items():
    add("GENEALOGY.skills", name, "", (rec or {}).get("path", "") if isinstance(rec, dict) else "")

# ---------- 4. FEDERATED_SKILLS_REGISTRY_V3.yaml ----------
R = yaml.safe_load(open(os.path.join(CANON, "FEDERATED_SKILLS_REGISTRY_V3.yaml")))
for layer, body in (R.get("layers") or {}).items():
    for s in (body or {}).get("skills", []) or []:
        add(f"REGISTRY_V3.layers.{layer}", s if isinstance(s, str) else str(s))
for prof, body in (R.get("agent_profiles") or {}).items():
    if isinstance(body, dict):
        for s in (body.get("skills") or []):
            add(f"REGISTRY_V3.agent_profiles.{prof}", s if isinstance(s, str) else str(s))

# ---------- 5. BOOTSTRAP_MANIFEST.json ----------
B = json.load(open(os.path.join(CANON, "BOOTSTRAP_MANIFEST.json")))
for s in B.get("universal_skills", []) or []:
    add("BOOTSTRAP.universal_skills", s if isinstance(s, str) else str(s))

# ---------- 6. PLACEMENT_MANIFEST.json ----------
P = json.load(open(os.path.join(CANON, "PLACEMENT_MANIFEST.json")))
def walk_place(o, path="placement"):
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, dict) and ("path" in v or "generation" in v or "address" in v):
                add(f"PLACEMENT.{path}", k, "", v.get("path", ""))
            else:
                walk_place(v, path + "." + str(k))
    elif isinstance(o, list):
        for v in o:
            walk_place(v, path)
walk_place(P)

# ---------- report ----------
by = collections.defaultdict(lambda: collections.Counter())
for r in rows:
    by[r["surface"]][r["status"]] += 1

print("=" * 88)
print("GHOST AUDIT — every registry surface, tested against loadable bodies")
print("=" * 88)
print(f"{'surface':46s} {'named':>6s} {'verif':>6s} {'ghost':>6s} {'orphan':>7s} {'absorbed':>9s} {'ret-ref':>8s}")
for s in sorted(by):
    c = by[s]
    print(f"{s:46s} {sum(c.values()):6d} {c['verified']:6d} {c['ghost']:6d} "
          f"{c['orphaned']:7d} {c['absorbed-successor']:9d} {c['retired-but-referenced']:8d}")

tot = collections.Counter(r["status"] for r in rows)
print("\nTOTAL NAMED CAPABILITIES ACROSS SURFACES:", len(rows))
for k, v in tot.most_common():
    print(f"   {k:24s} {v}")

ghosts = [r for r in rows if r["status"] == "ghost"]
print(f"\n--- GHOSTS ({len(ghosts)}) — named, no body, no declared successor ---")
for r in ghosts[:70]:
    print(f"  {r['surface'][:44]:44s} {r['name'][:40]:40s} owner={r['owner'] or '-'}")

json.dump({"generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "loaded_identities": len(live_paths), "unique_bodies": len(bodies),
           "IIR": round(len(live_paths) / len(bodies), 3),
           "totals": dict(tot), "rows": rows},
          open(os.path.join(OUT, "CYCLE4-GHOST-AUDIT.json"), "w"), indent=2)
print("\nwrote", os.path.join(OUT, "CYCLE4-GHOST-AUDIT.json"))
