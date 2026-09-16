#!/usr/bin/env python3
"""
mutation-authority-probe.py — READ-ONLY. Measures whether protected-state writes in a repo
carry an *authority record*, as distinct from an evidence record.

Why this exists (2026-09-16, incident 7b4a228ce):
  A commit resolved an identity question correctly, cited its evidence chain, and mutated
  `governance/GOTONG_ROYONG.md` with no authority reference of any kind. Separately, the A4
  regime already logs every harness commit to `state/a4_exceptions.jsonl` — but it records
  `actor` from `git config user.name`, a LABEL, not an identity.

  So the honest question is not "was the mutation authorized?" (unknowable from the artifacts).
  It is the measurable one:

      of the commits that touched protected paths, how many carry anything that names
      WHO (session), FOR WHAT (objective), and UNDER WHAT ENVELOPE (scope/expiry)?

  That is enforcement COVERAGE. Coverage is prior to prevention rate: a gate can block 100%
  of what it sees and still leave the surface open (this session's own sentinel proved the
  point by passing grok on its prompt echo while every real call returned 402).

This script mutates nothing. It reads git log + the A4 log and prints a report.

USAGE
  mutation-authority-probe.py [--repo /root/AAA] [--last 60] [--worktree]
"""
import argparse, json, os, re, subprocess, sys, collections

PROTECTED = [
    "governance/", "canon/", "instructions/", "registries/", "registry/",
    "skills/FEDERATED_SKILLS_REGISTRY_V3.yaml", "agent-cards/",
    "prompts/", "constitution", "scars/",
]
PROTECTED_SUFFIX = ("/AGENTS.md", "/SOUL.md", "/CLAUDE.md", "/AGENTS-AUTONOMY.md")
GENERATED_OK = ["docs/", "reports/", "forge_work/", "state/", "skills-archive/"]
# an authority record must name at least: an envelope/scope, and a session or objective
ENVELOPE_RE = re.compile(r"envelope|scope|authoriz|authorised|authorized|delegat|lease|ALLOW|HOLD", re.I)
IDENTITY_RE = re.compile(r"session[_ -]?id|objective|obj_id|task_id|run_id|ttl|expir", re.I)


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True).stdout


def classify(path):
    for p in PROTECTED:
        if path.startswith(p):
            return "PROTECTED"
    for s in PROTECTED_SUFFIX:
        if path.endswith(s):
            return "PROTECTED"
    for g in GENERATED_OK:
        if path.startswith(g):
            return "generated/doc"
    return "other"


def load_a4(path):
    idx = {}
    if not os.path.exists(path):
        return idx
    for line in open(path, errors="replace"):
        try:
            r = json.loads(line)
        except Exception:
            continue
        sha = (r.get("sha") or "")[:9]
        if sha:
            idx[sha] = r
    return idx


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="/root/AAA")
    ap.add_argument("--last", type=int, default=60)
    ap.add_argument("--a4", default="/root/AAA/state/a4_exceptions.jsonl")
    ap.add_argument("--worktree", action="store_true", help="also grade the uncommitted diff")
    a = ap.parse_args()

    a4 = load_a4(a.a4)
    shas = [s for s in git(a.repo, "log", "--format=%H", f"-{a.last}").split() if s]
    rows, stats = [], collections.Counter()
    for sha in shas:
        meta = git(a.repo, "show", "-s", "--format=%h%x1f%an%x1f%ad%x1f%s", "--date=short", sha).strip().split("\x1f")
        if len(meta) < 4:
            continue
        short, author, date, subject = meta[0], meta[1], meta[2], meta[3]
        body = git(a.repo, "show", "-s", "--format=%b", sha)
        files = [f for f in git(a.repo, "show", "--name-only", "--format=", sha).split("\n") if f.strip()]
        classes = collections.Counter(classify(f) for f in files)
        prot = classes["PROTECTED"]
        rec = a4.get(short, {})
        env = bool(ENVELOPE_RE.search((subject or "") + "\n" + (body or "")))
        ident = bool(IDENTITY_RE.search((subject or "") + "\n" + (body or "")))
        stats["commits"] += 1
        if prot:
            stats["touching_protected"] += 1
            stats["protected_files"] += prot
        if env:
            stats["with_envelope_word"] += 1
        if ident:
            stats["with_session_or_objective"] += 1
        if prot and not env:
            stats["protected_without_envelope"] += 1
        if prot and not ident:
            stats["protected_without_identity"] += 1
        rows.append((short, date, author, prot, classes.get("generated/doc", 0), "env" if env else "-",
                     "id" if ident else "-", rec.get("actor", "no-a4-record"), subject[:58]))

    print(f"repo={a.repo}  window=last {len(rows)} commits")
    print(f"  commits touching PROTECTED paths           : {stats['touching_protected']}")
    print(f"  ... without any authority/envelope language: {stats['protected_without_envelope']}")
    print(f"  ... without any session/objective reference: {stats['protected_without_identity']}")
    print(f"  commits mentioning envelope language       : {stats['with_envelope_word']}")
    print(f"  commits mentioning session/objective       : {stats['with_session_or_objective']}")
    dist = collections.Counter(r[2] for r in rows)
    print(f"  author (git config user.name) distribution : {dict(dist)}")
    print()
    print("  sha      date        prot  doc  auth  id   a4-actor      subject")
    for r in rows[:28]:
        if r[3] or r[4]:
            print(f"  {r[0]:8s} {r[1]:10s} {r[3]:4d} {r[4]:4d}  {r[5]:4s} {r[6]:4s} {r[7]:12s}  {r[8]}")

    if a.worktree:
        print("\n--- UNCOMMITTED WORKTREE (graded, not blocked) ---")
        out = git(a.repo, "status", "--porcelain")
        for line in out.splitlines():
            st, path = line[:2].strip(), line[3:].strip()
            c = classify(path)
            if c != "other":
                print(f"  {st:2s} {c:12s} {path}")

    cov = (1 - (stats["protected_without_envelope"] / stats["touching_protected"])) if stats["touching_protected"] else 1.0
    print(f"\nENFORCEMENT_COVERAGE (protected commits carrying envelope language) = {cov:.2%}")
    print("NOTE: this measures the ARTIFACT surface only. A harness with a root shell can write")
    print("      protected state without producing a commit at all — those attempts never enter")
    print("      this denominator. Coverage of the artifact surface is an upper bound on coverage.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
