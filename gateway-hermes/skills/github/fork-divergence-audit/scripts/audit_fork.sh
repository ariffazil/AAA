#!/usr/bin/env bash
# audit_fork.sh — measure a fork's divergence from upstream. READ-ONLY: only
# updates FETCH_HEAD, never touches the working tree (safe on live install dirs).
# Usage: audit_fork.sh /path/to/repo [upstream-url] [branch]
#   upstream-url omitted -> tries the 'upstream' remote, else errors.
set -euo pipefail

REPO="${1:?usage: audit_fork.sh /path/to/repo [upstream-url] [branch]}"
BRANCH="${3:-main}"

cd "$REPO"

echo "== local HEAD =="
git log -1 --format="%h %ad %s" --date=short

echo "== remotes =="
git remote -v | head -4

UPSTREAM="${2:-$(git remote get-url upstream 2>/dev/null || true)}"
if [ -z "$UPSTREAM" ]; then
  echo "!! no upstream URL given and no 'upstream' remote configured" >&2
  exit 1
fi

echo "== fetching upstream ($UPSTREAM $BRANCH) — FETCH_HEAD only, working tree untouched =="
git fetch -q "$UPSTREAM" "$BRANCH"

echo "== drift =="
echo "behind upstream: $(git rev-list --count HEAD..FETCH_HEAD) commits  (magnitude signal — history rewrites can inflate)"
echo "ahead (carried): $(git rev-list --count FETCH_HEAD..HEAD) commits  (exact)"
echo "base (merge-base): $(git merge-base HEAD FETCH_HEAD)"

echo "== carried commits =="
git log --oneline FETCH_HEAD..HEAD

echo "== file surface per carried commit (=> protected files for the ledger) =="
for c in $(git log --format=%h FETCH_HEAD..HEAD); do
  echo "-- $c"
  git show --stat --format="%s" "$c" | tail -n +2 | head -15
done
