#!/usr/bin/env python3
"""LIVING CORPSE AUDIT v2 — three false-positive classes removed.

v1 said 331 dead paths / 152 skills. Inspection showed most were the detector's fault:
  FP1  a path inside `references/<dated-session>.md` is a RECEIPT, not an instruction.
       A cache file expiring is expected; it does not make a skill unexecutable.
  FP2  `/root/.hermes/cache/...` and other declared-transient roots are expected to rotate.
  FP3  the immutable test matched NEGATED lines ("cite it; never write it") and reported them
       as write targets — the exact inversion of what the text said.
  FP4  MISSING-BIN was pure noise (2,547 findings from prose words). Removed entirely.

v2 keeps only what makes a skill unexecutable:
  DEAD-PATH (SKILL.md only)   the instruction surface names a non-transient path that is gone
  DEAD-SCRIPT (SKILL.md only) a scripts/ reference that exists nowhere
  IMMUTABLE-TARGET            an immutable path named as a write target, negation-aware
  HISTORICAL-REF (separate, informational) dead paths inside reference logs
"""
import os, re, json, datetime, subprocess, collections

CANON = "/root/AAA/skills"
OUT = "/root/AAA/skills-retired/2026-09-19-living-corpses"
SKIP = {".archive", ".frozen", ".archive-2026-09-18", ".profile-archive", ".system",
        "node_modules", "__pycache__", ".git", ".venv", "site-packages"}
TRANSIENT = ("/root/.hermes/cache/", "/tmp/", "/var/tmp/", "/root/.cache/",
             "/root/.hermes/pastes/", "/run/", "/proc/")
NEGATION = re.compile(r"\bnever\b|\bnot\b|\bcite\b|forbidden|do not|don't|instead of|"
                      r"do NOT|avoid|read-only|cite-only|historical", re.I)
WRITE_INTENT = re.compile(r"\bappend\b|>>|write (?:to|it|the)|update\b|record\b|push\b", re.I)

PATH_RE = re.compile(r"`?(/(?:root|opt|etc|var|usr|home|srv)/[A-Za-z0-9_./@\-]{3,90})`?")
SCRIPT_RE = re.compile(r"`?(scripts/[A-Za-z0-9_\-./]+\.(?:py|sh|js|ts))`?")

print("# indexing /root names ...", flush=True)
INDEX = set()
for dp, dn, fn in os.walk("/root", followlinks=False):
    dn[:] = [d for d in dn if d not in ("node_modules", "__pycache__", ".git", "site-packages")]
    INDEX.update(dn); INDEX.update(fn)
print(f"# {len(INDEX)} names indexed", flush=True)
ROOT_SCRIPTS = set(os.listdir("/root/scripts")) if os.path.isdir("/root/scripts") else set()

def state(p):
    if os.path.exists(p):
        return "present"
    b = os.path.basename(p.rstrip("/"))
    return ("moved" if b in INDEX else "missing") if b else "unknown"

def immutable(p):
    try:
        o = subprocess.run(["lsattr", "-d", p], capture_output=True, text=True, timeout=5).stdout
        return bool(o.strip()) and "i" in o.split()[0]
    except Exception:
        return False

def transient(p):
    return any(p.startswith(t) for t in TRANSIENT)

corpses, hist = {}, {}
stats = collections.Counter()
n_sk = 0
for dp, dn, fn in os.walk(CANON, followlinks=True):
    dn[:] = [d for d in dn if d not in SKIP and not d.startswith(".")]
    if "SKILL.md" not in fn:
        continue
    n_sk += 1
    sk = os.path.relpath(dp, CANON)
    main = os.path.join(dp, "SKILL.md")
    local_scripts = set()
    sc = os.path.join(dp, "scripts")
    if os.path.isdir(sc):
        for r, _, rf in os.walk(sc):
            local_scripts.update(rf)

    def scan(path, label, is_main):
        try:
            t = open(path, encoding="utf-8", errors="replace").read()
        except OSError:
            return [], [], []
        dl, dsl, iml = [], [], []
        for m in sorted(set(PATH_RE.findall(t))):
            if "*" in m or transient(m):
                continue
            # guard: a placeholder or truncated tail is a TEMPLATE, not a path
            if m.endswith(("-", ".", "/")) or re.search(r"YYYY|MM-DD|XXX|<|\$\{|%s|\.\.\.", m):
                continue
            # guard: documented EXAMPLE names are illustrations, not instructions
            if re.search(r"/(foo|bar|baz|qux|example|sample|myfile|placeholder|path/to|"
                         r"your[-_]file|myfile)\b", m, re.I):
                continue
            # guard: the regex stops at a char outside its class; if the following char in the
            # source is one of those, the match is a fragment of a longer path or a variable
            i = t.find(m)
            while i != -1:
                nxt = t[i + len(m): i + len(m) + 1]
                if nxt in ("<", "$", "{", "*", "%", "?"):
                    break
                i = t.find(m, i + 1)
            if i != -1:
                continue
            st = state(m)
            if st == "missing":
                (dl if is_main else dl).append([label, m])
            elif st == "present" and immutable(m):
                for line in t.splitlines():
                    if m in line and WRITE_INTENT.search(line) and not NEGATION.search(line):
                        iml.append([label, m, line.strip()[:110]])
                        break
        for m in sorted(set(SCRIPT_RE.findall(t))):
            b = os.path.basename(m)
            if b not in local_scripts and b not in ROOT_SCRIPTS and b not in INDEX:
                dsl.append([label, m])
        return dl, dsl, iml

    dl, dsl, iml = scan(main, "SKILL.md", True)
    h = {"count": 0, "sample": []}
    rd = os.path.join(dp, "references")
    if os.path.isdir(rd):
        for r, _, rf in os.walk(rd):
            for f in rf:
                if not f.endswith((".md", ".txt")):
                    continue
                a, b, c = scan(os.path.join(r, f), "references/" + f, False)
                if a:
                    h["count"] += len(a)
                    h["sample"] += a[:3]
    if dl or dsl or iml:
        corpses[sk] = {"dead_paths": dl[:12], "dead_scripts": dsl[:8], "immutable_targets": iml[:5],
                       "n": [len(dl), len(dsl), len(iml)]}
        stats["skills_with_corpses"] += 1
    if h["count"]:
        hist[sk] = h
        stats["skills_with_historical_refs"] += 1
    stats["dead_paths_in_skill_md"] += len(dl)
    stats["dead_scripts_in_skill_md"] += len(dsl)
    stats["immutable_write_targets"] += len(iml)
    stats["dead_paths_in_references"] += h["count"]

os.makedirs(OUT, exist_ok=True)
ranked = sorted(corpses.items(), key=lambda x: -(x[1]["n"][0] + 2 * x[1]["n"][1] + 5 * x[1]["n"][2]))
json.dump({"generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "skills_scanned": n_sk, "totals": dict(stats),
           "corpses": corpses, "historical_reference_noise": {k: v["count"] for k, v in hist.items()}},
          open(os.path.join(OUT, "LIVING-CORPSES.json"), "w"), indent=2)

L = ["LIVING CORPSE AUDIT v2 — instructions that cannot be executed",
     f"generated {datetime.datetime.now(datetime.timezone.utc).isoformat()}",
     f"witness: {CANON} — {n_sk} skills scanned, read-only",
     "",
     "v1 reported 331 dead paths across 152 skills. Three false-positive classes were then removed",
     "(dated receipts in references/, declared-transient cache roots, negated 'never write it' lines)",
     "and the noisy MISSING-BIN test was dropped. What follows is only what makes a skill UNEXECUTABLE.",
     "",
     f"skills with a corpse in SKILL.md  : {stats['skills_with_corpses']}",
     f"DEAD-PATH in SKILL.md             : {stats['dead_paths_in_skill_md']}",
     f"DEAD-SCRIPT in SKILL.md           : {stats['dead_scripts_in_skill_md']}",
     f"IMMUTABLE path named as write tgt : {stats['immutable_write_targets']}",
     "",
     f"(informational) dead paths inside reference logs: {stats['dead_paths_in_references']}"
     f" across {stats['skills_with_historical_refs']} skills — these are receipts, not instructions",
     "", "=" * 88, "RANKED", "=" * 88]
for sk, d in ranked:
    L.append("")
    L.append(f"### {sk}   [dead_paths={d['n'][0]} dead_scripts={d['n'][1]} immutable={d['n'][2]}]")
    for lab, p in d["dead_paths"]:
        L.append(f"    DEAD-PATH    {p}")
    for lab, p in d["dead_scripts"]:
        L.append(f"    DEAD-SCRIPT  {p}")
    for lab, p, ln in d["immutable_targets"]:
        L.append(f"    IMMUTABLE    {p}   <- {ln}")
open(os.path.join(OUT, "LIVING-CORPSES.txt"), "w").write("\n".join(L))
print("\n".join(L[:80]))
print(f"\nTOTALS: {dict(stats)}")
