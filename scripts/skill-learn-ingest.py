#!/usr/bin/env python3
"""skill-learn-ingest.py — merge queued learning atoms into canonical skills.
Auto-update mechanism: when an agent learns something, it drops an atom; this job
merges verified atoms into the canonical SKILL.md. All mount homes see it instantly.
Doctrine: F2 (lesson must carry evidence), F4 (append-only Lessons section), F7 (no certainty inflation).
"""
import os, json, glob, datetime, re, hashlib

QUEUE = "/root/AAA/skills/.learning/queue"
LEDGER = "/root/AAA/skills/.learning/ledger.jsonl"
HOMES = {  # canonical homes by skill prefix
    "geox-": "/root/GEOX/skills", "wealth-": "/root/WEALTH/skills",
    "well-": "/root/WELL/skills", "hermes-": "/root/HERMES/skills",
}
AAA = "/root/AAA/skills"

def canonical_dir(sid):
    for pre, home in HOMES.items():
        if sid.startswith(pre):
            return os.path.join(home, sid)
    return os.path.join(AAA, sid)

def valid(atom):
    return all(atom.get(k) for k in ("skill_id", "lesson", "agent", "evidence")) and \
           len(atom["lesson"]) <= 500 and len(atom["evidence"]) >= 10

merged, rejected = [], []
for qf in sorted(glob.glob(f"{QUEUE}/*.json")):
    try: atom = json.load(open(qf))
    except Exception: rejected.append((qf, "unparseable")); continue
    if not valid(atom):
        rejected.append((qf, "invalid-schema")); continue
    sk = os.path.join(canonical_dir(atom["skill_id"]), "SKILL.md")
    if not os.path.isfile(sk):
        rejected.append((qf, "skill-not-found")); continue
    text = open(sk).read()
    # idempotency: hash of lesson already present?
    lh = hashlib.sha256(atom["lesson"].encode()).hexdigest()[:12]
    if lh in text:
        rejected.append((qf, "duplicate")); os.rename(qf, qf + ".done"); continue
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    entry = (f"\n- **[{stamp}] {atom['agent']}** (evidence: {atom['evidence'][:180]}): "
             f"{atom['lesson']}")
    if "## Lessons (auto)" not in text:
        text += f"\n\n## Lessons (auto)\n\n*Auto-ingested from agent learning. F2-gated: every entry carries evidence.*\n"
    text = text.rstrip() + entry + "\n"
    # bump patch version
    m = re.search(r"^version: (\d+)\.(\d+)\.(\d+)", text, re.M)
    if m:
        text = text.replace(m.group(0), f"version: {m.group(1)}.{m.group(2)}.{int(m.group(3))+1}", 1)
    open(sk, "w").write(text)
    with open(LEDGER, "a") as f:
        f.write(json.dumps({"ts": stamp, "atom": os.path.basename(qf), "skill": atom["skill_id"],
                            "agent": atom["agent"], "lesson_hash": lh}) + "\n")
    merged.append((atom["skill_id"], atom["agent"]))
    os.rename(qf, qf + ".done")

print(f"merged={len(merged)} rejected={len(rejected)}")
for m in merged: print("  MERGED", m)
for r in rejected: print("  REJECT", r)
