#!/usr/bin/env python3
"""Inventory, categorise and drift-check a skill library.

Mechanical half of skill-library taxonomy work. Answers in one pass:

  1. Which skills are uncategorised (sit at the library root)?
  2. Which existing category does each most resemble?      TF-IDF nearest centroid
  3. Which pairs / clusters are near-duplicates?           cosine + union-find
  4. Which already exist in the canonical catalog, and whose copy is newer?
                                                           sha256 + mtime drift state

Category is derived from DIRECTORY PATH, never from frontmatter -- a root-level dir is
uncategorised. Drift states gate every merge decision: never merge a CANON_NEWER entry,
and never merge a LOCAL_NEWER entry before pushing it back to canonical.

Outputs CSV + JSON + markdown into --out.

Usage:
  python3 skill-taxonomy-classifier.py
  python3 skill-taxonomy-classifier.py --skills-root /root/.hermes/skills \
      --canonical-root /root/AAA/skills --out /tmp/skill-taxonomy --min-sim 0.22
"""
import argparse
import collections
import csv
import hashlib
import itertools
import json
import math
import os
import re

EXCLUDED = (".archive", ".hub", ".curator", ".git", "node_modules", ".venv")
FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---", re.S)
TOKEN = re.compile(r"[a-z0-9][a-z0-9+#._-]{1,}")
PREFIXES = (
    "forge-", "aaa-", "agi-", "asi-", "apex-", "audit-", "rsi-", "hermes-",
    "kernel-", "flame-", "well-", "wealth-",
)
STOP = set("""
a an the and or of to in for with on by is are be as at from that this it its use when using
skill skills agent apply applies run running via into your you we our their they them he she new
all any not no do does done can could should would will shall may might have has had been being
after before during while if then else than so such only also more most other others some each
every step steps example examples file files path paths note notes see section check ensure make
made
""".split())


def read_skill(path, rel):
    with open(path, encoding="utf-8", errors="replace") as handle:
        text = handle.read()
    match = FRONTMATTER.match(text)
    block = match.group(1) if match else ""
    body = text[match.end():] if match else text

    def field(key):
        found = re.search(r"^%s:\s*(.+)$" % key, block, re.M)
        return found.group(1).strip().strip("\"'") if found else ""

    parts = rel.split(os.sep)
    return {
        "rel": rel,
        "name": field("name") or os.path.basename(rel),
        "desc": field("description"),
        "tags": field("tags"),
        "body": body,
        "category": parts[0] if len(parts) > 1 else "",
        "sha": hashlib.sha256(text.encode()).hexdigest(),
        "chars": len(text),
        "mtime": os.path.getmtime(path),
    }


def scan(root):
    skills = {}
    if not os.path.isdir(root):
        return skills
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith((".", "__"))]
        if "SKILL.md" not in filenames:
            continue
        if any(part in EXCLUDED for part in dirpath.split(os.sep)):
            continue
        rel = os.path.relpath(dirpath, root)
        skills[rel] = read_skill(os.path.join(dirpath, "SKILL.md"), rel)
    return skills


def norm_name(value):
    low = value.lower()
    for prefix in PREFIXES:
        if low.startswith(prefix):
            return low[len(prefix):]
    return low


def tokens(value):
    return [t for t in TOKEN.findall((value or "").lower()) if t not in STOP]


def vector(rec, body_chars):
    counts = collections.Counter()
    for word in tokens(rec["name"]):
        counts[word] += 3
    for word in tokens(rec["desc"]):
        counts[word] += 2
    for word in tokens(rec["tags"]):
        counts[word] += 2
    for word in tokens(rec["body"][:body_chars]):
        counts[word] += 1
    return counts


def build_vectors(skills, body_chars):
    raw = {rel: vector(rec, body_chars) for rel, rec in skills.items()}
    total = max(len(raw), 1)
    doc_freq = collections.Counter()
    for counts in raw.values():
        for word in counts:
            doc_freq[word] += 1

    def idf(word):
        return math.log((1 + total) / (1 + doc_freq[word])) + 1.0

    vectors = {}
    for rel, counts in raw.items():
        weighted = {w: c * idf(w) for w, c in counts.items()}
        norm = math.sqrt(sum(v * v for v in weighted.values())) or 1.0
        vectors[rel] = {w: v / norm for w, v in weighted.items()}
    return vectors


def cosine(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(v * b.get(w, 0.0) for w, v in a.items())


def drift_map(local, canonical):
    index = {}
    for rel, rec in canonical.items():
        base = os.path.basename(rel)
        for key in (base.lower(), norm_name(base), rec["name"].lower()):
            index.setdefault(key, rec)
    out = {}
    for rel, rec in local.items():
        base = os.path.basename(rel)
        hit = index.get(base.lower()) or index.get(norm_name(base)) or index.get(rec["name"].lower())
        if hit is None:
            out[rel] = ("CANON_ABSENT", "")
        elif hit["sha"] == rec["sha"]:
            out[rel] = ("IDENTICAL", hit["rel"])
        elif hit["mtime"] > rec["mtime"]:
            out[rel] = ("CANON_NEWER", hit["rel"])
        else:
            out[rel] = ("LOCAL_NEWER", hit["rel"])
    return out


def cluster(paths, vectors, min_sim):
    parent = {p: p for p in paths}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    pairs = []
    for left, right in itertools.combinations(paths, 2):
        sim = cosine(vectors[left], vectors[right])
        if sim >= min_sim:
            pairs.append((sim, left, right))
            root_left, root_right = find(left), find(right)
            if root_left != root_right:
                parent[root_right] = root_left
    pairs.sort(reverse=True)
    groups = collections.defaultdict(list)
    for p in paths:
        groups[find(p)].append(p)
    clusters = sorted((sorted(g) for g in groups.values() if len(g) > 1), key=len, reverse=True)
    return pairs, clusters


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--skills-root", default="/root/.hermes/skills")
    ap.add_argument("--canonical-root", default="/root/AAA/skills")
    ap.add_argument("--out", default="/tmp/skill-taxonomy")
    ap.add_argument("--min-sim", type=float, default=0.20, help="cosine threshold for near-duplicate pairs")
    ap.add_argument("--top-k", type=int, default=3, help="nearest neighbours recorded per skill")
    ap.add_argument("--body-chars", type=int, default=4000)
    args = ap.parse_args()

    skills = scan(args.skills_root)
    canonical = scan(args.canonical_root)
    uncategorised = {rel: rec for rel, rec in skills.items() if not rec["category"]}
    labelled = {rel: rec for rel, rec in skills.items() if rec["category"]}
    print("skills on disk: %d (labelled %d, uncategorised %d)" % (len(skills), len(labelled), len(uncategorised)))

    vectors = build_vectors(skills, args.body_chars)

    centroids = {}
    by_category = collections.defaultdict(list)
    for rel, rec in labelled.items():
        by_category[rec["category"]].append(rel)
    for category, members in by_category.items():
        acc = collections.Counter()
        for rel in members:
            acc.update(vectors[rel])
        norm = math.sqrt(sum(v * v for v in acc.values())) or 1.0
        centroids[category] = {w: v / norm for w, v in acc.items()}

    drift = drift_map(skills, canonical) if canonical else {}
    uncat_paths = list(uncategorised)
    pairs, clusters = cluster(uncat_paths, vectors, args.min_sim)

    rows = []
    for rel in sorted(uncategorised):
        rec = uncategorised[rel]
        ranked = sorted(
            ((cosine(vectors[rel], c_vec), cat) for cat, c_vec in centroids.items()),
            reverse=True,
        )
        neighbours = sorted(
            ((cosine(vectors[rel], vectors[other]), other) for other in vectors if other != rel),
            reverse=True,
        )[: args.top_k]
        state, canon_rel = drift.get(rel, ("NO_CANONICAL_ROOT", ""))
        rows.append({
            "rel": rel,
            "name": rec["name"],
            "kb": rec["chars"] // 1024,
            "predicted_category": ranked[0][1] if ranked else "",
            "pred_score": round(ranked[0][0], 3) if ranked else 0.0,
            "alt_categories": " | ".join("%s:%.2f" % (c, s) for s, c in ranked[1:4]),
            "nearest": " | ".join("%s:%.2f" % (n, s) for s, n in neighbours),
            "top_neighbour": neighbours[0][1] if neighbours else "",
            "top_neighbour_sim": round(neighbours[0][0], 3) if neighbours else 0.0,
            "drift_state": state,
            "canonical_rel": canon_rel,
        })

    os.makedirs(args.out, exist_ok=True)
    fields = list(rows[0].keys()) if rows else ["rel"]
    with open(os.path.join(args.out, "uncategorised.csv"), "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    payload = {
        "skills_root": args.skills_root,
        "canonical_root": args.canonical_root,
        "counts": {"total": len(skills), "labelled": len(labelled), "uncategorised": len(uncategorised)},
        "drift_states": dict(collections.Counter(r["drift_state"] for r in rows)),
        "predicted_categories": dict(collections.Counter(r["predicted_category"] for r in rows)),
        "clusters": [
            {"size": len(g), "members": g,
             "suggested_target": sorted(g, key=lambda p: -uncategorised[p]["chars"])[0]}
            for g in clusters
        ],
        "rows": rows,
    }
    with open(os.path.join(args.out, "uncategorised.json"), "w") as handle:
        json.dump(payload, handle, indent=1)

    lines = ["# Skill taxonomy - uncategorised bucket", ""]
    lines.append("on disk %d | labelled %d | uncategorised %d" % (len(skills), len(labelled), len(uncategorised)))
    lines.append("")
    lines.append("## Drift vs canonical (%s)" % args.canonical_root)
    lines.append("")
    for state, count in sorted(collections.Counter(r["drift_state"] for r in rows).items()):
        lines.append("- %s: %d" % (state, count))
    lines.append("")
    lines.append("## Near-duplicate clusters (cosine >= %s)" % args.min_sim)
    lines.append("")
    for group in clusters:
        biggest = sorted(group, key=lambda p: -uncategorised[p]["chars"])[0]
        lines.append("### %d members -> suggested target: %s" % (len(group), biggest))
        for rel in group:
            lines.append("- %s (%sK)" % (rel, uncategorised[rel]["chars"] // 1024))
        lines.append("")
    lines.append("## Predicted category histogram")
    lines.append("")
    for category, count in collections.Counter(r["predicted_category"] for r in rows).most_common():
        lines.append("- %s: %d" % (category, count))
    with open(os.path.join(args.out, "REPORT.md"), "w") as handle:
        handle.write("\n".join(lines) + "\n")

    print("uncategorised: %d" % len(uncategorised))
    print("drift states: %s" % dict(collections.Counter(r["drift_state"] for r in rows)))
    print("near-duplicate clusters: %d (pairs %d)" % (len(clusters), len(pairs)))
    print("artifacts: %s" % args.out)


if __name__ == "__main__":
    main()
