
"""TIER 1 v2 — corrected census. Keys skills by RELATIVE PATH, not basename.
v1 defect: keying by realpath basename collapsed 12 legitimately-distinct skills
(audit-seal/ vs substrate/audit-seal/, "claude" x3 in different parents).
Reported 339 where the truth is 351. Third measurement artifact of the session.
"""
import hashlib, json, os, time
from collections import defaultdict

STORES = {
    "hermes_live":    "/root/.hermes/skills",
    "aaa_live":       "/root/AAA/skills",
    "profile_aaa":    "/root/.hermes/profiles/aaa-hermes/skills",
    "hermes_archive": "/root/.hermes/skills-archive",
}
LIVE = ["hermes_live", "aaa_live", "profile_aaa"]

def census(root):
    """{relative_path_key: absolute_SKILL.md_path}. Relative key = collision-safe."""
    out = {}
    if not os.path.isdir(root):
        return out
    for dp, dn, fn in os.walk(root):
        if "SKILL.md" in fn:
            rel = os.path.relpath(os.path.realpath(dp), os.path.realpath(root))
            out[rel] = os.path.realpath(os.path.join(dp, "SKILL.md"))
    return out

data = {k: census(v) for k, v in STORES.items()}

def leaf_names(d):
    return {os.path.basename(k) for k in d}

live_leaves = set()
for k in LIVE:
    live_leaves |= leaf_names(data[k])
arch_leaves = leaf_names(data["hermes_archive"])
archived_only = sorted(arch_leaves - live_leaves)

# duplicate leaf-names WITHIN a live store = real collision risk for name-based lookup
dupes = {}
for k in LIVE:
    c = defaultdict(list)
    for rel in data[k]:
        c[os.path.basename(rel)].append(rel)
    d = {n: v for n, v in c.items() if len(v) > 1}
    if d:
        dupes[k] = d

manifest_path = "/root/.hermes/skills/.bundled_manifest"
manifest_entries = 0
manifest_mtime = None
if os.path.exists(manifest_path):
    manifest_entries = sum(1 for l in open(manifest_path) if l.strip())
    manifest_mtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(manifest_path)))

result = {
    "taken_at_local": time.strftime("%Y-%m-%d %H:%M:%S %Z", time.localtime()),
    "method": "os.walk on ABSOLUTE store roots; key = relative path from store root "
              "(collision-safe); leaf-name used ONLY for cross-store archived-only set math",
    "v1_defect_corrected": "v1 keyed by realpath basename -> collapsed 12 distinct "
                           "skills, reported 339 for hermes_live. Truth is 351.",
    "per_store_skill_files": {k: len(v) for k, v in data.items()},
    "hermes_live_bundled_manifest_entries": manifest_entries,
    "hermes_live_bundled_manifest_mtime": manifest_mtime,
    "intra_store_duplicate_leaf_names": {k: {n: v for n, v in d.items()} for k, d in dupes.items()},
    "archive_total": len(arch_leaves),
    "archived_only_count": len(archived_only),
    "archived_only_names": archived_only,
    "STABILITY_WARNING": "This store is NOT static. tools/skills_sync.py runs at every "
                         "gateway/session startup and relocates FORGE-act-federation-ingress "
                         "<-> FORGE-sct-federation-ingress (6 relocations logged 2026-09-11 "
                         "11:28 -> 2026-09-12 00:57). 12 concurrent sessions touched skills "
                         "tonight; 31 curator patch refusals. Any count is a timestamped "
                         "snapshot, never a settled fact.",
}

OUT = "/root/AAA/reports/skill-store-census-2026-09-12.json"
with open(OUT, "w") as f:
    json.dump(result, f, indent=2)
h = hashlib.sha256(open(OUT, "rb").read()).hexdigest()

print("PER-STORE SKILL.md FILES")
for k, v in result["per_store_skill_files"].items():
    print(f"   {k:16s} {v}")
print()
print("hermes_live bundled manifest entries:", manifest_entries, "mtime", manifest_mtime)
print("intra-store duplicate leaf-names:", {k: list(v) for k, v in dupes.items()})
print("archive total:", result["archive_total"], " archived-only:", result["archived_only_count"])
print()
print("WROTE", OUT)
print("SHA256", h)
