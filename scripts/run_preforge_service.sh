#!/usr/bin/env bash
# Pre-Forge Constitutional Gate — service runner
# DITEMPA BUKAN DIBERI

set -euo pipefail
cd /root/AAA
exec env -i PATH=/usr/bin:/bin:/usr/local/bin HOME=/root PYTHONUNBUFFERED=1 PYTHONPATH=/root/AAA python3 /root/AAA/core/pre_forge_service.py
