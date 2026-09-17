#!/usr/bin/env python3
"""
SKILL OWNER CHECK — the pre-flight the anti-bloat rule needs.

Directive (F13, 2026-09-16):
    "Before creating or preserving any skill, find the existing owner. If an owner exists,
     patch the owner. New skill only when authority, side effect, or runtime contract is
     genuinely different."

The rule is sound and the machine violates it constantly — including the session that wrote
the rule. This tool makes it cheap to obey: one command, before `create`.

    python3 /root/AAA/instructions/skill-owner-check.py rasa
    python3 /root/AAA/instructions/skill-owner-check.py rasa shadow layer

What it reports
---------------
  name collisions    the same skill name living at 2+ paths (the routing hazard)
  content divergence whether those copies agree or have drifted
  overlap cluster    other skills whose name/tags/description share your keywords
  verdict            PATCH-EXISTING (an owner is there) or NO-OWNER (new skill is defensible)

Read-only. Never writes. Never deletes.
"""

from __future__ import annotations

import hashlib
import os
import re
import sys
from collections import defaultdict

ROOTS = [
    "/root/.hermes/skills",
    "/root/AAA/skills",
    "/root/HERMES/skills",
    "/root/.agents/skills",
]
SKIP_DIRS = {"node_modules", "__pycache__", ".curator_backups", "skills-archive",
             ".hub", ".system", ".archive-20260912", "archive", ".git"}


def load_all():
    """Return {name: [(path, sha, frontmatter_text)]} for every SKILL.md on disk."""
    out = defaultdict(list)
    for root in ROOTS:
        if not os.path.isdir(root):
            continue
        for dp, dn, fn in os.walk(root):
            dn[:] = [d for d in dn if d not in SKIP_DIRS and not d.startswith(".")]
            if "SKILL.md" not in fn:
                continue
            p = os.path.join(dp, "SKILL.md")
            try:
                text = open(p, encoding="utf-8", errors="ignore").read()
            except OSError:
                continue
            sha = hashlib.sha256(text.encode("utf-8", "ignore")).hexdigest()[:16]
            out[os.path.basename(dp)].append((p, sha, text[:4000]))
    return out


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    return m.group(1) if m else ""


def overlap(text, keywords):
    """Score a skill's routing surface (name + description + tags + triggers) against keywords."""
    fm = frontmatter(text).lower()
    body = text.lower()
    hits = [k for k in keywords if k.lower() in fm]
    body_hits = [k for k in keywords if k.lower() in body and k.lower() not in fm]
    return len(hits) * 3 + len(body_hits), hits, body_hits


def main(keywords):
    skills = load_all()
    print(f"\n=== SKILL OWNER CHECK — keywords: {', '.join(keywords)} ===")
    print(f"    scanned {sum(len(v) for v in skills.values())} SKILL.md files across "
          f"{len([r for r in ROOTS if os.path.isdir(r)])} roots; "
          f"{len(skills)} unique names\n")

    # --- 1. exact name collisions for this keyword ----------------------------------------
    print("  [1] NAME COLLISIONS (same name at 2+ paths)")
    collisions = 0
    for name, copies in sorted(skills.items()):
        if not any(k.lower() in name.lower() for k in keywords):
            continue
        if len(copies) < 2:
            continue
        collisions += 1
        shas = {c[1] for c in copies}
        status = "IDENTICAL" if len(shas) == 1 else f"DIVERGED ({len(shas)} distinct bodies)"
        print(f"    {name}  [{status}]")
        for p, sha, _ in copies:
            print(f"        {sha}  {p.replace('/root/', '~/')}")
    if not collisions:
        print("    none")

    # --- 2. overlap cluster ------------------------------------------------------------------
    print("\n  [2] OVERLAP CLUSTER (skills whose routing surface shares your keywords)")
    scored = []
    for name, copies in skills.items():
        best = 0
        best_info = None
        for p, sha, text in copies:
            sc, hits, body = overlap(text, keywords)
            if sc > best:
                best, best_info = sc, (p, hits, body)
        if best >= 3:
            scored.append((best, name, best_info))
    scored.sort(reverse=True)
    for sc, name, (p, hits, _body) in scored[:14]:
        print(f"    {sc:>3}  {name:<40} fm-hits={hits}")
    if not scored:
        print("    none — no existing skill routes on these keywords")

    # --- 3. verdict ---------------------------------------------------------------------------
    print("\n  [3] VERDICT")
    if scored:
        top_sc, top_name, (top_path, _, _) = scored[0]
        print(f"    PATCH-EXISTING. Strongest owner: {top_name}")
        print(f"      path: {top_path.replace('/root/', '~/')}")
        if collisions:
            print(f"    ...and {collisions} name collision(s) must be reconciled FIRST — a new skill")
            print(f"        added on top of two diverged copies makes three, not one.")
        print(f"    Per the directive, a new skill is defensible only if authority boundary,")
        print(f"    input modality, side effects, output contract or failure semantics differ")
        print(f"    materially. Wording, domain label or persona differing is not enough.")
    else:
        print("    NO-OWNER FOUND. A new skill is defensible — no existing skill routes on these")
        print("    keywords. Re-run this check with broader terms before creating, since a")
        print("    near-miss owner under a different name is the common case.")

    print("\n  Read-only check. Nothing was written or deleted.\n")
    return 0


if __name__ == "__main__":
    kws = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not kws:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(kws))
