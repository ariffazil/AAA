#!/bin/bash
# Keep health-probe source_commit in sync for aaa-a2a (cannot git as aaa-a2a).
# Run after every AAA commit / deploy. Reversible: delete markers.
set -euo pipefail
ROOT=/root/AAA
SHORT=$(git -C "$ROOT" rev-parse --short=7 HEAD)
echo -n "$SHORT" > "$ROOT/.git_commit"
mkdir -p /opt/aaa/app
echo -n "$SHORT" > /opt/aaa/app/.git_commit
chmod 644 "$ROOT/.git_commit" /opt/aaa/app/.git_commit
echo "deploy markers → $SHORT"
