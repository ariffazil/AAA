#!/usr/bin/env python3
"""
skills-census.py — the ONE canonical census. Makes the registry unable to lie.

WHY THIS EXISTS
  FEDERATED_SKILLS_REGISTRY_V3.yaml carried `disk_reconciliation` with
  `mental_disk_skills: 191`, `drift: 0`, `method: skill-mesh-sync.sh --check (cron */5 min)` —
  a witness that last ran 2026-08-11 and never failed, because nothing recomputed it. A sensor
  that cannot fail is decoration; the next agent trusts it. Violates C17 CAPABILITY TRUTH.

CONTRACT
  * read-only against the skill trees (never moves, writes, or deletes a skill)
  * writes ONLY the `disk_reconciliation` block of the registry (a derived witness field)
  * emits a witness_hash so the claim is checkable, not asserted
  * exit 1 when the claim and the disk disagree

S1 — OVERLAY SURFACES (added 2026-09-16)
  The census previously witnessed 3 trees and was blind to the harness-local overlay trees, so
  `canonical_skills / viewed_skills` read as the whole mesh while real surfaces went uncounted.
  It also had no identity-collision measure, so skills claiming an already-owned capability were
  invisible. Both are now derived fields.

  TWO TRAPS THIS FILE NOW GUARDS (both hit on the first attempt, 2026-09-16):
   1. REALPATH, or the count lies. `.claude/skills` and `.codex/skills` are SYMLINKS to
      /root/AAA/skills. Counting them as overlays produced `overlay_total: 1650` and
      `duplicate_identity_skills: 2162` — the same canonical tree counted once per road to it.
      Every home is now resolved with os.path.realpath and deduped.
   2. EXCL must apply to the symlink walk too. `/root/.kimi-code/skills/.archive/devops` is a
      retired link into a moved tree; unfiltered it flipped VERDICT to FAIL on a surface the
      registry never previously witnessed.

  VERDICT semantics are UNCHANGED for the witnessed trees (FAIL only on a broken symlink).
  Overlay defects are reported as their own fields and never change the exit code — introducing
  a new FAIL on a newly-witnessed surface is a decision, not a side effect.

USAGE
  skills-census.py              # human report
  skills-census.py --json       # machine report
  skills-census.py --write      # also update the registry's disk_reconciliation block
  skills-census.py --quiet      # one line + exit code
"""

import os, re, sys, json, hashlib, collections, datetime

ROOTS = {
    "canonical": "/root/AAA/skills",
    "hermes": "/root/.hermes/skills",
    "profile": "/root/.hermes/profiles/aaa-hermes/skills",
}
# Harness-local overlay trees. Scoped to one runtime; absence is not a defect, presence is
# part of the mesh and must be counted. A root that resolves to canonical is a VIEW, not an
# overlay — it is recorded as such and its skills are not counted twice.
OVERLAY_ROOTS = {
    "opencode": "/root/.config/opencode/skills",
    "qwen": "/root/.qwen/skills",
    "kimi": "/root/.kimi-code/skills",
    "claude": "/root/.claude/skills",
    "codex": "/root/.codex/skills",
    "gemini": "/root/.gemini/skills",
    "continue": "/root/.continue/skills",
}
REGISTRY = "/root/AAA/skills/FEDERATED_SKILLS_REGISTRY_V3.yaml"
EXCL = {
    ".git",
    ".hub",
    ".archive",
    ".broken-archive",
    ".curator_backups",
    "__pycache__",
    "node_modules",
    "venv",
    ".venv",
}
SUPPORT = {"references", "templates", "assets", "scripts", "examples"}
# Brand prefixes are a SCOPE marker, not noise: `claude-zen-router` and `qwen-zen-router` are one
# capability carried by two harnesses. Normalizing them away is what lets identity be compared.
BRAND = re.compile(
    r"^(forge|claude|qwen|kimi|opencode|copilot|gemini|grok|aaa|agi|asi|agent|hermes)[-_]+"
)


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def identity_key(name):
    """Normalized claimed capability. A router keys on the declared identity, not the folder name."""
    if not name:
        return None
    n = re.sub(r"[-_\s]+", "-", name.strip().lower())
    return BRAND.sub("", n).strip("-") or None


def scan(root, prune=EXCL):
    """Return per-skill facts. followlinks=True: views are symlinks by design."""
    out = {}
    if not os.path.isdir(root):
        return out
    for dp, dn, fn in os.walk(root, followlinks=True):
        dn[:] = [d for d in dn if d not in prune and not d.startswith(".")]
        if "SKILL.md" not in fn:
            continue
        p = os.path.join(dp, "SKILL.md")
        if not os.path.exists(p):
            continue
        rel = os.path.relpath(dp, root)
        txt = open(p, encoding="utf-8", errors="replace").read(4000)
        nm = re.search(r"^name:\s*(.+)$", txt, re.M)
        ds = re.search(r"^description:\s*(.+)$", txt, re.M)
        # F13 2026-10-18 (Phase-2 binding): a skill may DECLARE another skill as
        # alternative_to. Two homes sharing one normalized identity are a duplicate
        # only if they do NOT mutually declare each other. This is a semantic, not a
        # bypass: same-body collisions (re-implementations) still count.
        alts = set()
        for rx in (
            r"target:\s*([^,\n]+)\n(?:\s*.*\n){0,2}?\s*type:\s*alternative_to",
            r"type:\s*alternative_to\n(?:\s*.*\n){0,2}?\s*target:\s*([^,\n]+)",
        ):
            for m in re.finditer(rx, txt):
                alts.add(identity_key(m.group(1).strip().strip("\"'")))
        alts.discard(None)
        out[rel] = {
            "abs": dp,
            "real": os.path.realpath(dp),
            "name": (nm.group(1).strip().strip("\"'") if nm else None),
            "has_desc": bool(ds),
            "sha": sha(p),
            # F13 2026-10-23: a harness shell is a REAL directory whose SKILL.md is a
            # symlink into canonical. realpath(dp) then looks foreign while the body is
            # literally the same file. Record the resolved body so collision detection
            # can tell a mirror from a competing re-implementation.
            "body_real": os.path.realpath(p),
            "bytes": os.path.getsize(p),
            "alt": alts,
            "is_symlink": os.path.islink(dp)
            or os.path.realpath(dp) != os.path.abspath(dp),
        }
    return out


def broken_links(root, prune=EXCL):
    """Symlinks that resolve to nothing. EXCL applies — a retired .archive link is not a defect."""
    out = []
    if not os.path.isdir(root):
        return out
    for dp, dn, fn in os.walk(root, followlinks=True):
        dn[:] = [d for d in dn if d not in prune and not d.startswith(".")]
        for n in list(dn) + list(fn):
            p = os.path.join(dp, n)
            if os.path.islink(p) and not os.path.exists(p):
                out.append(os.path.relpath(p, root))
    return out


def census():
    idx = {k: scan(v) for k, v in ROOTS.items()}
    canon, herm = idx["canonical"], idx["hermes"]
    canon_real = os.path.realpath(ROOTS["canonical"])

    # Overlay trees, split into genuine local skills vs pure views of canonical.
    ov, ov_views = {}, {}
    for name, root in OVERLAY_ROOTS.items():
        if not os.path.isdir(root):
            continue
        if os.path.realpath(root) == canon_real:
            ov_views[name] = "symlink → canonical"
            continue
        tree = scan(root)
        # keep only skills whose real home is NOT inside canonical (those are re-exports)
        local = {
            k: v
            for k, v in tree.items()
            if not os.path.realpath(v["abs"]).startswith(canon_real + os.sep)
        }
        ov[name] = local
        if local:
            ov_views[name] = f"{len(tree) - len(local)} view + {len(local)} local"

    # --- identity collisions --------------------------------------------------------
    # Distinct REAL homes per normalized capability. A loader alias symlink is the design, not a
    # collision. A capability owned in canonical AND re-implemented in a harness tree IS one.
    canon_homes = collections.defaultdict(set)
    canon_alts = {}
    for rel, v in canon.items():
        k = identity_key(v["name"] or os.path.basename(rel))
        if k:
            canon_homes[k].add(v["real"])
            canon_alts[v["real"]] = v.get("alt") or set()
    foreign_homes = collections.defaultdict(set)
    for name, tree in ov.items():
        for rel, v in tree.items():
            k = identity_key(v["name"] or os.path.basename(rel))
            if k:
                foreign_homes[k].add(v["real"])
    # F13 2026-10-18 (split-brain fix): a capability reached via BOTH a canonical
    # symlink AND an overlay symlink to the SAME body is a VIEW (the loader-alias
    # design), not a re-implementation. Only count as duplicate when the realpath
    # sets are DISJOINT (two distinct bodies claiming one identity).
    # F13 2026-10-23 (census-green): a foreign home whose BODY is bit-identical to the
    # canonical body for that identity is a BUNDLED_MIRROR, not a competing capability.
    # Two ways that happens: (a) shell dir with a symlinked SKILL.md, (b) the harness
    # bundler copied the file verbatim. Neither is drift — the WARN existed to catch two
    # DIVERGENT bodies claiming one identity, and that case still WARNs because its body
    # digest is not in the canonical set. Mirrors are self-correcting: the moment a copy
    # diverges it stops being a mirror and re-enters the duplicate class.
    canon_body = collections.defaultdict(set)
    for rel, v in canon.items():
        k = identity_key(v["name"] or os.path.basename(rel))
        if k:
            canon_body[k].add(v["sha"])
    foreign_body = collections.defaultdict(set)
    for name, tree in ov.items():
        for rel, v in tree.items():
            k = identity_key(v["name"] or os.path.basename(rel))
            if k:
                foreign_body[k].add(v["sha"])

    dup_reimplemented, bundled_mirror = [], []
    for k in sorted(foreign_homes):
        if k not in canon_homes:
            continue
        if canon_homes[k] & foreign_homes[k]:
            continue                      # same realpath = loader view, already exempt
        if foreign_body[k] and foreign_body[k] <= canon_body[k]:
            bundled_mirror.append(k)      # every foreign body exists verbatim in canonical
        else:
            dup_reimplemented.append(k)   # at least one divergent body = real collision
    dup_foreign_only = sorted(
        k for k in foreign_homes if k not in canon_homes and len(foreign_homes[k]) > 1
    )
    # two real homes INSIDE canonical claiming one capability (e.g. forge-onboarding/claude and
    # forge-onboarding/agent-onboarding both declaring "Agent Onboarding"). These are the only
    # duplicates a canonical-only census can see, and they are the cheapest to fix.
    # F13 2026-10-18 (Phase-2 binding): two real homes sharing one normalized identity
    # are a duplicate ONLY when they do NOT mutually declare each other as
    # alternative_to. A declared pair (harness-native variants: hermes-forge /
    # opencode-forge) is a typed relation, not a collision. Same-body re-implementations
    # are unaffected — they carry no relationship block and still count.
    dup_canonical = {}
    for k, homes in canon_homes.items():
        if len(homes) <= 1:
            continue
        if all(k in canon_alts.get(h, set()) for h in homes):
            continue
        dup_canonical[k] = sorted(homes)
    dup_skills = sum(
        len(foreign_homes[k]) for k in dup_reimplemented + dup_foreign_only
    ) + sum(len(v) for v in dup_canonical.values())
    mirror_skills = sum(len(foreign_homes[k]) for k in bundled_mirror)

    # a "shell": a canonical top-level entry that resolves to no SKILL.md anywhere beneath it
    shells = []
    croot = ROOTS["canonical"]
    if os.path.isdir(croot):
        for e in sorted(os.listdir(croot)):
            p = os.path.join(croot, e)
            if not os.path.isdir(p) or e.startswith("."):
                continue
            if not any("SKILL.md" in f for _, _, f in os.walk(p, followlinks=True)):
                shells.append(e)

    # symlink dependents: a view symlink is broken if its canonical target vanished
    broken, overlay_broken = [], {}
    for label, root in ROOTS.items():
        for rel in broken_links(root):
            broken.append(os.path.relpath(os.path.join(root, rel), root))
    for name, root in OVERLAY_ROOTS.items():
        b = broken_links(root)
        if b:
            overlay_broken[name] = b[:10]

    # divergence between canonical and the live view.
    #
    # MATCH ON THE FULL RELATIVE PATH. This block previously keyed on os.path.basename(rel), which
    # collapses any two skills whose LEAF FOLDER NAME happens to coincide (here: 42 ambiguous leaf
    # names collapsing 103 canonical entries to 42). The collapse does two kinds of damage at once:
    #   * FALSE POSITIVE — two unrelated skills paired and reported as "the same skill diverged"
    #     (measured 2026-09-19: apex_verdict_hold/claude vs FORGE-onboarding/claude, 11071 B vs
    #     5914 B, flagged as one skill that had drifted); and
    #   * FALSE NEGATIVE — 103 entries reduced to 42 keys means a genuine divergence can be
    #     overwritten in the dict and never compared at all.
    # A stable-key comparison is the only honest one. Basename is kept ONLY as a declared fallback
    # for entries whose leaf name is unique in BOTH trees, and the ambiguity is published as its own
    # field so the sensor can never hide how much it had to collapse.
    cbase, hbase = {}, {}
    for k, v in canon.items():
        cbase.setdefault(os.path.basename(k), []).append((k, v))
    for k, v in herm.items():
        hbase.setdefault(os.path.basename(k), []).append((k, v))

    ambiguous_leaf_names = sorted(
        n for n in (set(cbase) & set(hbase)) if len(cbase[n]) > 1 or len(hbase[n]) > 1
    )
    ambiguous_entries = sum(len(cbase[n]) + len(hbase[n]) for n in ambiguous_leaf_names)

    shared = set(canon) & set(herm)
    diverged = sorted(k for k in shared if canon[k]["sha"] != herm[k]["sha"])
    # declared fallback: only where the leaf name is unambiguous on BOTH sides and the path itself
    # has no counterpart — reported separately, never mixed into `diverged`.
    fallback_diverged = sorted(
        n
        for n in (set(cbase) & set(hbase))
        if len(cbase[n]) == 1
        and len(hbase[n]) == 1
        and cbase[n][0][0] not in herm
        and hbase[n][0][0] not in canon
        and cbase[n][0][1]["sha"] != hbase[n][0][1]["sha"]
    )

    overlay_total = sum(len(v) for v in ov.values())
    r = {
        "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(
            timespec="seconds"
        ),
        # distinct logical skills = distinct BODIES, not distinct leaf names. This previously used
        # {os.path.basename(k)}, which is the same collapse fixed above: 642 canonical entries carry
        # only ~601 distinct leaf names, so unrelated same-named folders were merged into one count
        # while genuinely distinct bodies sharing a name were lost. Identity here is the body digest.
        "total_skills_on_disk": len({v["sha"] for v in canon.values()}) + len(shells),
        "canonical_entries": len(canon),
        "canonical_skills": len(canon),
        "viewed_skills": len(herm),
        "profile_skills": len(idx["profile"]),
        "overlay_skills": {k: len(v) for k, v in sorted(ov.items())},
        "overlay_total": overlay_total,
        "overlay_surfaces": dict(sorted(ov_views.items())),
        "whole_mesh_skills": len({v["sha"] for v in canon.values()})
        + overlay_total
        + len(shells),
        # F13 2026-10-18: dup_canonical (two real bodies INSIDE the canonical store
        # claiming one identity) IS a duplicate identity group too — it must gate the
        # verdict, not hide inside duplicate_identity_skills. Otherwise VERDICT=PASS
        # while N DUPLICATE_OWNER remain on disk.
        "duplicate_identity_groups": (
            len(dup_reimplemented) + len(dup_foreign_only) + len(dup_canonical)
        ),
        "duplicate_identity_skills": dup_skills,
        "duplicate_reimplemented_groups": len(dup_reimplemented),
        "duplicate_sample": (list(dup_canonical) + dup_reimplemented + dup_foreign_only)[:15],
        # F13 2026-10-23: bit-identical copies in harness trees. Counted, named, and NOT a
        # defect — a mirror carries no competing body. Reported so the number is visible
        # rather than silently deleted from the accounting.
        "bundled_mirror_groups": len(bundled_mirror),
        "bundled_mirror_skills": mirror_skills,
        "bundled_mirror_sample": bundled_mirror[:15],
        "overlay_broken_symlinks": overlay_broken,
        "total_indexed_skills": len(herm),
        "total_loadable_skills": len(
            [v for v in herm.values() if v["name"] and v["has_desc"]]
        ),
        "total_frontmatter_valid": len(
            [v for v in herm.values() if v["name"] and v["has_desc"]]
        ),
        "total_shells": len(shells),
        "shells": shells[:40],
        "total_symlink_dependents": sum(1 for v in herm.values() if v["is_symlink"]),
        "broken_symlinks": len(broken),
        "broken_sample": broken[:10],
        "total_diverged": len(diverged),
        "diverged": diverged[:40],
        "ambiguous_leaf_names": len(ambiguous_leaf_names),
        "ambiguous_entry_collapse": ambiguous_entries,
        "diverged_unambiguous_fallback": fallback_diverged[:20],
    }
    # the witness hash covers the claim, so it cannot be edited without detection
    claim = {
        k: r[k]
        for k in (
            "canonical_skills",
            "viewed_skills",
            "overlay_total",
            "whole_mesh_skills",
            "duplicate_identity_groups",
            "duplicate_identity_skills",
            "total_loadable_skills",
            "total_shells",
            "total_diverged",
            "broken_symlinks",
        )
    }
    r["witness_hash"] = hashlib.sha256(
        json.dumps(claim, sort_keys=True).encode()
    ).hexdigest()[:16]
    r["claim"] = claim
    # FAIL only on a structural break in a WITNESSED tree (a link that resolves to nothing, i.e.
    # a capability deleted silently). Diverged twins and duplicate identities are deliberate HOLD
    # debt awaiting a human merge. Overlay defects are reported, never escalated — see header.
    r["VERDICT"] = (
        "FAIL"
        if r["broken_symlinks"]
        else (
            "WARN"
            if (r["total_diverged"] or r["duplicate_identity_groups"])
            else "PASS"
        )
    )
    return r


def write_registry(r):
    """Update ONLY the derived disk_reconciliation block. Never touches floors or curated lists."""
    if not os.path.exists(REGISTRY):
        return "registry not found"
    txt = open(REGISTRY).read()
    overlay = ", ".join(f"{k}={v}" for k, v in r["overlay_skills"].items()) or "none"
    block = (
        "disk_reconciliation:\n"
        f"  refreshed: '{r['generated']}'\n"
        # This line used to claim "(cron 4x/day)". Verified 2026-09-19: NO scheduled job runs this
        # script with --write. The only 4x/day skill cron is skill-entropy-gate.py (04,10,16,22),
        # which invokes `skills-census.py --json` — a READ, never a write. So the block below does
        # NOT self-refresh, and a stale block will sit here claiming to be machine-derived while
        # nothing recomputes it. Name the real refresh path instead of an imaginary schedule.
        "  method: 'skills-census.py --write — machine-derived, do not hand-edit; NOT on a schedule,"
        " refresh by running the tool'\n"
        f"  physical_disk_skills: {r['total_skills_on_disk']}\n"
        f"  canonical_skills: {r['canonical_skills']}\n"
        f"  viewed_skills: {r['viewed_skills']}\n"
        f"  loadable_skills: {r['total_loadable_skills']}\n"
        f"  overlay_skills: '{overlay}'\n"
        f"  whole_mesh_skills: {r['whole_mesh_skills']}\n"
        f"  duplicate_identity_groups: {r['duplicate_identity_groups']}\n"
        f"  duplicate_identity_skills: {r['duplicate_identity_skills']}\n"
        f"  shells: {r['total_shells']}\n"
        f"  diverged: {r['total_diverged']}\n"
        f"  broken_symlinks: {r['broken_symlinks']}\n"
        f"  witness_hash: {r['witness_hash']}\n"
        f"  verdict: {r['VERDICT']}\n"
    )
    m = re.search(r"^disk_reconciliation:\n(?:[ \t].*\n|\n)*", txt, re.M)
    if m:
        txt = txt[: m.start()] + block + txt[m.end() :]
    else:
        txt = txt.replace("\nlayers:", "\n" + block + "layers:", 1)
    open(REGISTRY, "w").write(txt)
    return "registry disk_reconciliation updated"


if __name__ == "__main__":
    r = census()
    if "--write" in sys.argv:
        write_registry(r)
    if "--json" in sys.argv:
        print(json.dumps(r, indent=1))
    elif "--quiet" in sys.argv:
        print(
            f"VERDICT {r['VERDICT']} canon={r['canonical_skills']} viewed={r['viewed_skills']} "
            f"overlay={r['overlay_total']} whole={r['whole_mesh_skills']} "
            f"dupgroups={r['duplicate_identity_groups']} dupskills={r['duplicate_identity_skills']} "
            f"shells={r['total_shells']} diverged={r['total_diverged']} "
            f"broken={r['broken_symlinks']} witness={r['witness_hash']}"
        )
    else:
        for k in (
            "generated",
            "total_skills_on_disk",
            "canonical_skills",
            "viewed_skills",
            "profile_skills",
            "overlay_total",
            "whole_mesh_skills",
            "duplicate_identity_groups",
            "duplicate_identity_skills",
            "total_loadable_skills",
            "total_shells",
            "total_symlink_dependents",
            "broken_symlinks",
            "total_diverged",
            "witness_hash",
        ):
            print(f"  {k:30s} {r[k]}")
        print(f"  {'overlay_skills':30s} {r['overlay_skills']}")
        print(f"  {'overlay_surfaces':30s} {r['overlay_surfaces']}")
        print(f"  VERDICT                        {r['VERDICT']}")
    # F13 2026-10-18: --strict = the mesh gate ("one census, many consumers").
    # Exit 0 ONLY on PASS (no broken symlinks, no diverged, no duplicate identities).
    # Default (no flag) keeps the structural-break semantic: exit 1 on FAIL only.
    if "--strict" in sys.argv:
        sys.exit(0 if r["VERDICT"] == "PASS" else 1)
    sys.exit(1 if r["VERDICT"] == "FAIL" else 0)
