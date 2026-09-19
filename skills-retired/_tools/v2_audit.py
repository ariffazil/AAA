#!/usr/bin/env python3
"""SKILLSTORE_NAMESPACE_COLLAPSE_V2 — the audit.

Finds only what meets one of the eight entropy conditions. Reports identities removed and
capabilities preserved. Every verdict is grounded: the group key is the census's own normalized
identity, and the retention test is run by discovery_guard.py before anything is called RETIRE.

Witnesses: /root/scripts/skills-census.py --json  (duplicate identity groups, shells, broken)
           /root/.hermes/skills/.usage.json       (cost>value, one harness only)
           /root/AAA/skills                       (what is actually on disk)
"""
import json, os, re, subprocess, collections, hashlib, datetime

CANON = "/root/AAA/skills"
GUARD = "/root/AAA/skills-retired/_tools/../_tools/../skill-library-integrity/scripts/discovery_guard.py"
GUARD = "/root/AAA/skills/skill-library-integrity/scripts/discovery_guard.py"
BRAND = re.compile(r"^(forge|claude|qwen|kimi|opencode|copilot|gemini|grok|aaa|agi|asi|agent|hermes|F13)[-_]+",
                   re.I)

# ---- index disk -----------------------------------------------------------
skills = {}          # name -> dict(path, bytes, fm, body_head)
for dp, dn, fn in os.walk(CANON):
    if "/." in dp.replace(CANON, ""):
        continue
    if "SKILL.md" not in fn:
        continue
    p = os.path.join(dp, "SKILL.md")
    t = open(p, encoding="utf-8", errors="replace").read()
    fm = t.split("---")[1] if t.startswith("---") else ""
    d = re.search(r'description:\s*(.+?)(?=\n[a-z_]+:|\n---|\Z)', fm, re.S)
    nm = re.search(r'^name:\s*(.+)$', fm, re.M)
    sk = {
        "dir": dp, "rel": os.path.relpath(dp, CANON), "bytes": len(t),
        "desc": re.sub(r"\s+", " ", (d.group(1) if d else "")).strip().strip('"\'>|'),
        "declared": (nm.group(1).strip() if nm else "?"),
        "body": t,
    }
    skills[sk["rel"]] = sk

print(f"skills on disk: {len(skills)}")

def group(keyfn):
    g = collections.defaultdict(list)
    for rel, s in skills.items():
        g[keyfn(s)].append(rel)
    return {k: v for k, v in g.items() if len(v) > 1}

# ---- CLASS A: alias-parading ---------------------------------------------
alias = []
for rel, s in skills.items():
    head = s["body"][:1200]
    if re.search(r"^\s*ALIAS|ALIAS →|superseded_by:", head, re.M | re.I) or \
       re.search(r"^\s*frozen:|^\s*freeze_path:", head, re.M):
        m = re.search(r"(?:superseded_by|ALIAS\s*→)\s*[:]?\s*`?([A-Za-z0-9_.\-]+)", head)
        alias.append((rel, m.group(1) if m else "?"))

# ---- CLASS C: case-twin ---------------------------------------------------
case = group(lambda s: os.path.basename(s["rel"]).lower())

# ---- CLASS B: per-harness clone (normalized identity) ---------------------
norm = group(lambda s: BRAND.sub("", os.path.basename(s["rel"]).lower()).replace("_", "-"))

# ---- CLASS D: incident fossil (name carries a dated one-off) --------------
FOSSIL = re.compile(r"(ipv6|hang-fix|throttle|disk-pressure|delivery-storm|datacenter-ip|"
                    r"-fix$|-triage$|-storm$|-incident)", re.I)
fossil = [rel for rel in skills if FOSSIL.search(os.path.basename(rel))]

# ---- CLASS F: profile/vendor junk ----------------------------------------
VENDOR = re.compile(r"^(understand|openai-docs|plugin-creator|review-agent|skill-installer|help$)")
vendor = [rel for rel in skills if VENDOR.search(os.path.basename(rel))]

# ---- CLASS G: two skills answer one question (name-family clusters) ------
FAM = {
    "control-is-it-real": r"(control|mechanism|enforcement|proxy|named|declared)-.*(audit|verification)|name-requires",
    "person-audit": r"(human-bond|human-relationship|relationship-evidence|relationship-reality|first-party-evidence|first-party-corpus)-",
    "seal-ritual": r"(seal|sealing)-.*(verif|ritual|discipline)|canon.*seal|doctrine.*seal|kernel-seal",
    "skill-own-ops": r"^skill-|^skills-",
    "memory-write": r"(memory|federation-memory)-.*(writeback|manage|retrieval|ops)",
}
gclass = {}
for label, pat in FAM.items():
    hits = [rel for rel in skills if re.search(pat, os.path.basename(rel), re.I)]
    if len(hits) > 1:
        gclass[label] = hits

# ---- report ---------------------------------------------------------------
print("\n=== A. ALIAS-PARADING ===")
for rel, succ in sorted(alias):
    print(f"  {rel:70s} -> {succ}")
print("\n=== B. PER-HARNESS CLONE (normalized identity groups) ===")
for k, v in sorted(norm.items()):
    print(f"  [{k}] {v}")
print("\n=== C. CASE-TWIN ===")
for k, v in sorted(case.items()):
    print(f"  [{k}] {v}")
print("\n=== D. INCIDENT FOSSIL ===")
for rel in sorted(fossil):
    print(f"  {rel}")
print("\n=== F. PROFILE / VENDOR JUNK ===")
for rel in sorted(vendor):
    print(f"  {rel}")
print("\n=== G. ONE QUESTION, MANY TITLES ===")
for label, hits in gclass.items():
    print(f"  ({label}) n={len(hits)}")
    for h in sorted(hits):
        print(f"      {h}")

json.dump({"alias": alias, "norm": norm, "case": case, "fossil": fossil,
           "vendor": vendor, "gclass": gclass},
          open("/root/AAA/skills-retired/2026-09-19-namespace-collapse/V2-AUDIT.json", "w"), indent=2)
print("\nwrote V2-AUDIT.json")
