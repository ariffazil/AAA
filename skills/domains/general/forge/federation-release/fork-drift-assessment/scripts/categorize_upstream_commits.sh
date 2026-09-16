#!/usr/bin/env bash
# categorize_upstream_commits.sh — categorize the commits between a local ref and
# an upstream ref into security / critical / feature / fix buckets.
#
# Per fork-drift-assessment SKILL.md ("Support files"):
#   Run with `[upstream_ref] [local_ref]` (defaults: `origin/main` and `HEAD`).
#   Produces security/critical/feature/fix breakdown.
#
# Usage:
#   bash scripts/categorize_upstream_commits.sh
#   bash scripts/categorize_upstream_commits.sh upstream/main HEAD
#
# Run it inside the fork/install directory (the repo you are assessing).

set -uo pipefail

UPSTREAM="${1:-origin/main}"
LOCAL="${2:-HEAD}"

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "FATAL: not inside a git repository" >&2
  exit 2
fi

if ! git rev-parse --verify --quiet "$UPSTREAM" >/dev/null; then
  echo "FATAL: upstream ref '$UPSTREAM' not found. Known remotes:" >&2
  git remote -v >&2
  exit 2
fi

COUNT=$(git rev-list --count "$LOCAL..$UPSTREAM")
echo "== fork-drift: $LOCAL..$UPSTREAM  ($COUNT commits missing locally) =="
echo "   upstream=$UPSTREAM  local=$LOCAL"
echo

SEC=$(mktemp); CRIT=$(mktemp); FEAT=$(mktemp); FIX=$(mktemp); OTHER=$(mktemp)
trap 'rm -f "$SEC" "$CRIT" "$FEAT" "$FIX" "$OTHER"' EXIT

# Subject + full body per commit, so classification sees the real message.
git log --no-merges --format='%h %s%n%b<<<END>>>' "$LOCAL..$UPSTREAM" \
| awk -v sec="$SEC" -v crit="$CRIT" -v feat="$FEAT" -v fix="$FIX" -v other="$OTHER" '
    { buf = buf $0 "\n" }
    /<<<END>>>/ {
      msg = tolower(buf)
      if (msg ~ /(cve-|vulnerab|security|sanitiz|injection|xss|csrf|exploit|auth bypass|privilege escalat|unsafe deserial)/)
        print buf >> sec
      else if (msg ~ /(breaking|critical|data loss|corrupt|panic|segfault|crash|regression|revert)/)
        print buf >> crit
      else if (msg ~ /(^| )(feat|add|implement|introduce|support|new )/)
        print buf >> feat
      else if (msg ~ /(^| )(fix|bug|patch|correct|repair|hotfix)/)
        print buf >> fix
      else
        print buf >> other
      buf = ""
    }
  '

emit() {
  local label="$1" file="$2"
  local n; n=$(grep -c '<<<END>>>' "$file" 2>/dev/null || echo 0)
  printf '\n-- %s (%s)\n' "$label" "$n"
  [ "$n" -gt 0 ] && sed 's/<<<END>>>//' "$file" | sed '/^$/d' | sed 's/^/   /' | head -80
}

emit "SECURITY" "$SEC"
emit "CRITICAL" "$CRIT"
emit "FEATURE"  "$FEAT"
emit "FIX"      "$FIX"
emit "OTHER"    "$OTHER"

echo
printf '== summary ==\n'
for pair in "security:$SEC" "critical:$CRIT" "feature:$FEAT" "fix:$FIX" "other:$OTHER"; do
  lbl="${pair%%:*}"; f="${pair#*:}"
  printf '   %-9s %s\n' "$lbl" "$(grep -c '<<<END>>>' "$f" 2>/dev/null || echo 0)"
done
