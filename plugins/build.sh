#!/usr/bin/env bash
# build.sh — arif-core: compile SOT → per-harness views + receipt
# Canonical: /root/AAA/plugins/build.sh
# Views are artifacts (FP-01): safe to delete and rebuild. Never hand-edit.
set -euo pipefail

chmod +x /root/AAA/hooks/adapters/codex/adapter.py /root/AAA/hooks/adapters/codex/shim.py

python3 /root/AAA/plugins/adapters/compile.py
echo "--- dist ---"
find /root/AAA/plugins/dist -type f | sort
