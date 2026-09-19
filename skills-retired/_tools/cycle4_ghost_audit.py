#!/usr/bin/env python3
"""CYCLE 4 — ghosts, not duplicates.  Plus the Identity Inflation Ratio (IIR).

Definitions used (stated, because a ratio is only as honest as its denominator):
  loaded identity  = one PATH a loader can enumerate a SKILL.md from (the name an agent can ask for)
  unique capability= one distinct BODY (sha256 of the resolved SKILL.md). PROXY: two capabilities
                     that share a byte-identical body are counted as one — sound for clones
                     (which is the case being measured), wrong in principle for coincidence.
  routing identity = one distinct frontmatter `name:` (the field the loader dedupes on, first-wins)

IIR = loaded identities / unique capabilities        (higher = more identity inflation)

Ghost test, per registry surface, for every NAMED capability:
  verified               body loadable now
  ghost                  named, no body, no successor named anywhere
  orphaned               named, body gone, but a successor explicitly declared
  retired-but-referenced named, and we retired it today, and a successor exists
  false-positive         name resolves to a DIFFERENT live capability (normalisation artefact)
"""
import os, re, json, hashlib, collections, datetime

CANON = "/root/AAA/skills"
REG = CANON
OUT = "/root/AAA/skills-retired/2026-09-19-namespace-collapse"
EXCL = {".git", "__pycache__", "node_modules", ".venv", "references", "templates", "assets",
        "scripts", "examples"}

def sha(p):
    h = hashlib.sha256()
    try:
        with open(p, "rb") as f:
            for b in iter(lambda: f.read(1 << 16), b""):
                h.update(b)
    except OSError:
        return "UNREADABLE"
    return h.hexdigest()

# ---------- 1. what the loader can actually ask for, and what body it gets ----------
LOADED = []           # (path, rel, body_sha, routing_name)
for dp, dn, fn in os.walk(CANON, followlinks=True):
    dn[:] = [d for d in dn if d not in EXCL and not d.startswith(".")]
    if "SKILL.md" in fn:
        p = os.path.join(dp, "SKILL.md")
        t = open(p, encoding="utf-8", errors="replace").read()
        m = re.search(r"^name:\s*(.+)$", t.split("---")[1] if t.startswith("---") else "", re.M)
        LOADED.append({"path": p, "rel": os.path.relpath(dp, CANON), "sha": sha(p),
                       "routing": (m.group(1).strip() if m else os.path.basename(dp))})

paths = len(LOADED)
bodies = collections.Counter(x["sha"] for x in LOADED)
unique_bodies = len(bodies)
routing = collections.Counter(x["routing"].lower() for x in LOADED)
unique_routing = len(routing)

print("=" * 72)
print("IDENTITY INFLATION RATIO (canonical store, resolved through symlinks)")
print("=" * 72)
print(f"  loaded identities (paths)      : {paths}")
print(f"  unique bodies (sha256)         : {unique_bodies}")
print(f"  unique routing names           : {unique_routing}")
print(f"  IIR  = loaded / unique bodies  : {paths/unique_bodies:.2f}")
print(f"  IIR' = loaded / routing names  : {paths/unique_routing:.2f}")

print(f"\n  most-duplicated bodies (1 body, N identities):")
for s, n in bodies.most_common(12):
    if n > 1:
        rels = [x["rel"] for x in LOADED if x["sha"] == s]
        print(f"   {n:3d}x  {s[:12]}  {rels}")
dup_paths = sum(n - 1 for n in bodies.values() if n > 1)

# ---------- 2. the ghost audit over every registry surface ----------
SURFACES = {
    "FEDERATED_SKILLS_REGISTRY_V3.yaml": os.path.join(REG, "FEDERATED_SKILLS_REGISTRY_V3.yaml"),
    "SKILL_ALIAS_TABLE.json":            os.path.join(REG, "SKILL_ALIAS_TABLE.json"),
    "OWNERSHIP_MAP.yaml":                os.path.join(REG, "OWNERSHIP_MAP.yaml"),
    "GENEALOGY.json":                    os.path.join(REG, "GENEALOGY.json"),
    "PLACEMENT_MANIFEST.json":           os.path.join(REG, "PLACEMENT_MANIFEST.json"),
    "BOOTSTRAP_MANIFEST.json":           os.path.join(REG, "BOOTSTRAP_MANIFEST.json"),
}
try:
    import yaml
except ImportError:
    yaml = None

def load_any(p):
    t = open(p, encoding="utf-8", errors="replace").read()
    if p.endswith((".yaml", ".yml")):
        return yaml.safe_load(t) if yaml else None
    try:
        return json.loads(t)
    except Exception:
        return None

# live name index: every folder name + every frontmatter name that currently resolves
live = set()
for x in LOADED:
    live.add(os.path.basename(x["rel"]).lower())
    live.add(x["routing"].lower())

# successor map from today's ledgers (retired -> survivor)
old2new = {}
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
        items = L.get("merged_from") or L.get("items") or L.get("entries") or []
        tgt = L.get("canonical_skill") or L.get("merged_into") or L.get("merge") or ""
        tgt = [x for x in str(tgt).split("/") if x]
        tgt = tgt[-2] if len(tgt) >= 2 else (tgt[0] if tgt else "")
        for e in items:
            if not isinstance(e, dict):
                continue
            nm = (e.get("folder") or e.get("skill") or e.get("rel") or e.get("orig_path")
                  or e.get("original_path") or e.get("original_folder") or "")
            nm = os.path.basename(str(nm).rstrip("/"))
            if nm:
                old2new[nm.lower()] = tgt or None

def classify(name):
    n = name.strip().lower()
    if not n:
        return "empty"
    if n in live:
        return "verified"
    if n in old2new:
        return "retired-but-referenced" if old2new[n] and old2new[n].lower() in live else "orphaned"
    return "ghost"

# ---------- 3. pull every named capability out of each surface ----------
NAMES_PER_SURFACE = {}

def names_from(obj, out):
    """Collect every plausible capability name: dict keys, string leaf values under
    name-ish keys, and list entries."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(k, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.\- ]{3,64}", k):
                out.add(k)
            if isinstance(v, str) and re.search(r"name|skill|owner|id|path|home|v3_name",
                                                str(k), re.I):
                b = os.path.basename(v.rstrip("/"))
                if b and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.\-]{3,64}", b):
                    out.add(b)
            names_from(v, out)
    elif isinstance(obj, list):
        for v in obj:
            if isinstance(v, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.\-]{3,64}", v):
                out.add(v)
            else:
                names_from(v, out)

for label, path in SURFACES.items():
    if not os.path.isfile(path):
        NAMES_PER_SURFACE[label] = None
        continue
    obj = load_any(path)
    if obj is None:
        NAMES_PER_SURFACE[label] = None
        continue
    s = set()
    names_from(obj, s)
    NAMES_PER_SURFACE[label] = s

print("\n" + "=" * 72)
print("GHOST AUDIT — registry surface vs reality")
print("=" * 72)
print(f"{'surface':36s} {'names':>6s} {'verified':>9s} {'ghost':>7s} {'orphan':>7s} {'retired-ref':>12s}")
allrows = []
for label, s in NAMES_PER_SURFACE.items():
    if s is None:
        print(f"{label:36s}  (not parseable / absent)")
        continue
    c = collections.Counter(classify(n) for n in s)
    print(f"{label:36s} {len(s):6d} {c['verified']:9d} {c['ghost']:7d} "
          f"{c['orphaned']:7d} {c['retired-but-referenced']:12d}")
    for n in sorted(s):
        st = classify(n)
        if st != "verified":
            allrows.append({"surface": label, "name": n, "status": st,
                            "successor": old2new.get(n.lower())})

print(f"\nNON-VERIFIED NAMES ACROSS ALL SURFACES: {len(allrows)}")
for r in allrows[:60]:
    print(f"  {r['status']:22s} {r['surface']:34s} {r['name']:44s} -> {r['successor'] or ''}")

json.dump({"generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "loaded_identities": paths, "unique_bodies": unique_bodies,
           "unique_routing_names": unique_routing,
           "IIR_loaded_per_body": round(paths / unique_bodies, 2),
           "duplicate_identity_paths": dup_paths,
           "non_verified": allrows,
           "per_surface": {k: (len(v) if v is not None else None)
                           for k, v in NAMES_PER_SURFACE.items()}},
          open(os.path.join(OUT, "CYCLE4-GHOST-AUDIT.json"), "w"), indent=2)
print("\nwrote", os.path.join(OUT, "CYCLE4-GHOST-AUDIT.json"))
