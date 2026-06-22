#!/usr/bin/env bash
set -euo pipefail
python3 /root/.openclaw/workspace/tmp/wiki_normalize_links.py
python3 /root/arifOS/wiki/scripts/generate_views.py
