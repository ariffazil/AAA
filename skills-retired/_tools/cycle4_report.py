#!/usr/bin/env python3
"""CYCLE 4 — final report generator. Five tables + the ghost ledger, all from measured data."""
import os, re, json, glob, hashlib, collections, datetime

CANON = "/root/AAA/skills"
OUT = "/root/AAA/skills-retired/2026-09-19-namespace-collapse"
yaml = __import__("yaml")
EXCL = {"references", "templates", "assets", "scripts", "examples", "__pycache__"}

# ---- index canonical ----
S = {}
for dp, dn, fn in os.walk(CANON, followlinks=True):
    dn[:] = [d for d in dn if d not in EXCL and not d.startswith(".")]
    if "SKILL.md" not in fn:
        continue
    p = os.path.join(dp, "SKILL.md")
    t = open(p, encoding="utf-8", errors="replace").read()
    fm = t.split("---")[1] if t.startswith("---") else ""
    nm = re.search(r"^name:\s*(.+)$", fm, re.M)
    d = re.search(r'description:\s*(.+?)(?=\n[a-z_]+:|\n---|\Z)', fm, re.S)
    rel = os.path.relpath(dp, CANON)
    S[rel] = {"sha": hashlib.sha256(open(p, "rb").read()).hexdigest(),
              "name": (nm.group(1).strip().strip("\"'") if nm else os.path.basename(rel)),
              "base": os.path.basename(rel),
              "desc": re.sub(r"\s+", " ", (d.group(1) if d else "")).strip().strip("\"'>|")[:120]}

BRAND = re.compile(r"^(forge|claude|qwen|kimi|opencode|copilot|gemini|grok|aaa|agi|asi|agent|hermes)[-_]+", re.I)
norm = lambda x: BRAND.sub("", x.lower()).replace("_", "-")

# ---- T1 IIR ----
bodies = collections.Counter(v["sha"] for v in S.values())
mesh_paths, mesh_bodies = 4449, 893
L = []
L.append("=" * 92)
L.append("CYCLE 4 — IDENTITY INFLATION & GHOST AUDIT   (ARIF, 2026-09-19)")
L.append("=" * 92)
L.append("")
L.append("T1. IDENTITY INFLATION RATIO")
L.append(f"    canonical store : {len(S)} loadable identities / {len(bodies)} unique bodies"
         f"   -> IIR {len(S)/len(bodies):.2f}")
L.append(f"    whole mesh      : {mesh_paths} loadable identities / {mesh_bodies} unique bodies"
         f"   -> IIR {mesh_paths/mesh_bodies:.2f}")
L.append(f"    decomposition   : of the {mesh_paths - mesh_bodies} redundancy paths,"
         f" {mesh_paths - len(S)} are MESH MOUNTS of the same store")
L.append(f"                      (canonical tree is mounted by 5 harness homes), and"
         f" {len(S) - len(bodies)} are duplicated bodies inside the store itself.")
L.append("    reading         : address inflation (same body, many roads) >> capability inflation.")
L.append("                      The mesh number is large because of mounts, not because the")
L.append("                      federation holds 5x the capabilities. Do not read it as famine.")
L.append("")

# ---- T2 duplicate capability families ----
L.append("T2. TOP DUPLICATE CAPABILITY FAMILIES (one capability, N identities on disk)")
gm = collections.defaultdict(list)
for rel, v in S.items():
    gm[norm(v["base"])].append(rel)
fam = sorted([(k, v) for k, v in gm.items() if len(v) > 1], key=lambda x: -len(x[1]))
for k, v in fam[:20]:
    d = "DIFFERENT BODY" if len({S[x]["sha"] for x in v}) > 1 else "same body (pure address)"
    L.append(f"  n={len(v)}  [{k}]  {d}")
    for x in sorted(v):
        L.append(f"        {x}")
L.append("")

# ---- T3 audit-overlap ----
QUESTIONS = {
    "was this really enforced?": r"(control|mechanism|enforcement|proxy|named|declared|name-requires)",
    "does this claim survive the first-party record?": r"(first-party|relationship|human-bond|human-relationship|evidence-audit)",
    "how do I seal/record a decision?": r"(doctrine-sealing|seal-ritual|canon-doctrine|seal-discipline|propose-seal|sealing)",
    "is the agent's claim true?": r"(claim|fabrication|finding|receipt|instructed-|inherited-)",
    "is the deployment what it says?": r"(deploy|deployment|release-attestation|runtime-drift|drift)",
    "who owns the skill library?": r"^skill-|^skills-",
    "does this human read match reality?": r"(bond-reality|relationship-reality|human-state|persona-read|public-persona)",
}
L.append("T3. TOP AUDIT-OVERLAP FAMILIES (grouped by the QUESTION ANSWERED, not the name)")
for q, pat in QUESTIONS.items():
    hits = [rel for rel in S if re.search(pat, S[rel]["base"], re.I)]
    if len(hits) < 2:
        continue
    L.append(f"  \"{q}\"  -> {len(hits)} identities")
    for h in sorted(hits)[:12]:
        L.append(f"        {h}")
    if len(hits) > 12:
        L.append(f"        ... +{len(hits)-12} more")
L.append("")

# ---- T4 incident fossils ----
FOSSIL = re.compile(r"(ipv6|hang-fix|throttle|disk-pressure|delivery-storm|datacenter-ip|"
                    r"202[0-9]-[0-9]{2}|-storm$|outage)", re.I)
L.append("T4. INCIDENT FOSSILS (name carries the one-off event, not the capability)")
for rel in sorted(S):
    if FOSSIL.search(S[rel]["base"]):
        L.append(f"  {rel}   :: {S[rel]['desc'][:80]}")
L.append("")

# ---- T5 aliases pretending ----
L.append("T5. ALIASES PRETENDING TO BE SKILLS (body is a redirect)")
for rel, v in sorted(S.items()):
    head = open(os.path.join(CANON, rel, "SKILL.md"), encoding="utf-8", errors="replace").read()[:1000]
    if re.search(r"^\s*ALIAS|ALIAS →|superseded_by:|^\s*frozen:|^\s*freeze_path:", head, re.M | re.I):
        L.append(f"  {rel}   :: {v['desc'][:90]}")
L.append("")

# ---- T6 ghost audit ----
d = json.load(open(os.path.join(OUT, "CYCLE4-GHOST-AUDIT.json")))
L.append("T6. GHOST AUDIT — registry surface vs reality")
L.append(f"    named capabilities across surfaces : {sum(d['totals'].values())}")
for k, n in sorted(d["totals"].items(), key=lambda x: -x[1]):
    L.append(f"      {k:24s} {n}")
L.append("")
seen = set()
L.append("    TRUE GHOSTS (name referenced, no loadable body, no successor declared):")
for r in d["rows"]:
    if r["status"] == "ghost" and r["name"] not in seen:
        seen.add(r["name"])
        L.append(f"      NAME {r['name']:36s} REG {r['surface'][:34]:34s} "
                 f"BODY none  OWNER {r['owner'] or '-':8s} STATUS ghost")
L.append(f"    unique ghost names: {len(seen)}")
L.append("")
L.append(f"    DETECTOR FALSE POSITIVES MEASURED: {d['detector_rescued']} names that a naive")
L.append("      pass called ghost were resolved once the index covered all skill roots and")
L.append("      composite keys were normalised. Rule: a ghost claim needs the same warrant as")
L.append("      a presence claim — sweep every root before calling a capability dead.")
L.append("")

# ---- postscript ----
L.append("=" * 92)
L.append("WHAT THIS AUDIT DID NOT DO")
L.append("=" * 92)
L.append("  * No skill was created, renamed for aesthetics, or given a new doctrine name.")
L.append("  * No mutation was made from the ghost list: a ghost is a REGISTRY defect. Repairing")
L.append("    it means editing hand-maintained governance files, which is an ownership decision.")
L.append("  * The knowledge layer (know-physics / know-math / know-language / +1) is confirmed")
L.append("    ghost: BOOTSTRAP phase 7 names 3 of them, the registry layer block names 4, and")
L.append("    only liveness.json exists on disk. Pre-existing, unchanged by this pass.")

txt = "\n".join(L)
open(os.path.join(OUT, "CYCLE4-REPORT.txt"), "w").write(txt)
print(txt[:7000])
print("\n... [truncated in console] full report:", os.path.join(OUT, "CYCLE4-REPORT.txt"))
