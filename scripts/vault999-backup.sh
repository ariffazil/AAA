#!/bin/bash
# VAULT999 off-site mirror: KVM8 (Truth Court) -> KVM4 (Workshop)
# Restored 2026-09-04 by FI-008 — arifos-backup.timer vanished (last snapshot
# 2026-08-20, 2953 records single-copy). Additive rsync only (append-only ledger,
# never --delete). F1 AMANAH: mirror is a witness copy, NOT an authority.
set -euo pipefail
SRC=/root/VAULT999/
DST=root@100.64.0.5:/root/VAULT999-mirror-KVM8/
start=$(date -u +%FT%TZ)
count=$(find /root/VAULT999 -type f | wc -l)
rsync -a --timeout=180 "$SRC" "$DST"
echo "vault999-backup ok start=$start end=$(date -u +%FT%TZ) files=$count"
