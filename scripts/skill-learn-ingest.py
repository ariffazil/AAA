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

# Live roots, searched case-insensitively when the direct path misses.
# Added 2026-09-15: the direct-path-only resolver rejected every atom whose
# skill_id case differed from the on-disk dir (e.g. "forge-verify-runtime" →
# /root/.hermes/skills/FORGE-verify-runtime), so the queue jammed silently for
# 12 days. Authored Hermes skills live under the live profile tree; they were
# not in HOMES at all.
SEARCH_ROOTS = (
    "/root/.hermes/skills", "/root/AAA/skills", "/root/HERMES/skills",
    "/root/GEOX/skills", "/root/WEALTH/skills", "/root/WELL/skills",
)
_RESOLVE_CACHE = {}


def canonical_dir(sid):
    for pre, home in HOMES.items():
        if sid.startswith(pre):
            return os.path.join(home, sid)
    return os.path.join(AAA, sid)


def resolve_skill_dir(sid):
    """Direct home first; then case-insensitive search of live roots (nested ok)."""
    direct = canonical_dir(sid)
    if os.path.isfile(os.path.join(direct, "SKILL.md")):
        return direct
    if sid in _RESOLVE_CACHE:
        return _RESOLVE_CACHE[sid]
    want = sid.lower()
    for root in SEARCH_ROOTS:
        if not os.path.isdir(root):
            continue
        for dirpath, dirnames, _files in os.walk(root):
            dirnames[:] = [d for d in dirnames
                           if not d.startswith(".") and d not in ("node_modules", "__pycache__")]
            if os.path.basename(dirpath).lower() == want and \
                    os.path.isfile(os.path.join(dirpath, "SKILL.md")):
                _RESOLVE_CACHE[sid] = dirpath
                return dirpath
    _RESOLVE_CACHE[sid] = direct
    return direct

def valid(atom):
    return all(atom.get(k) for k in ("skill_id", "lesson", "agent", "evidence")) and \
           len(atom["lesson"]) <= 500 and len(atom["evidence"]) >= 10


def dead_letter(qf, reason):
    """Move a rejected atom out of the scan path, keeping it as evidence.

    A rejection that stays in the queue is re-checked every hour forever (measured:
    one atom rejected 288x over 12 days). But the queue directory itself is scanned
    by `glob("*.json")` only, so a `.rejected` sibling is already out of the scan —
    except that it still clutters the directory and the .done/.rejected set grows
    without bound. Moving both to subdirectories keeps the queue listing meaningful.
    """
    sub = "rejected" if reason != "duplicate" else "done"
    d = os.path.join(QUEUE, sub)
    os.makedirs(d, exist_ok=True)
    os.rename(qf, os.path.join(d, os.path.basename(qf)))

merged, rejected = [], []
for qf in sorted(glob.glob(f"{QUEUE}/*.json")):
    try: atom = json.load(open(qf))
    except Exception: rejected.append((qf, "unparseable")); dead_letter(qf, "unparseable"); continue
    if not valid(atom):
        rejected.append((qf, "invalid-schema")); dead_letter(qf, "invalid-schema"); continue
    sk = os.path.join(resolve_skill_dir(atom["skill_id"]), "SKILL.md")
    if not os.path.isfile(sk):
        # Dead-letter 2026-09-15: re-rejecting forever re-created the 12-day jam.
        # Re-sweep by moving the file back to the queue root once the skill exists.
        rejected.append((qf, "skill-not-found")); dead_letter(qf, "skill-not-found"); continue
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
    dead_letter(qf, "duplicate")

print(f"[{datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}] merged={len(merged)} rejected={len(rejected)}")
for m in merged: print("  MERGED", m)
for r in rejected: print("  REJECT", r)
