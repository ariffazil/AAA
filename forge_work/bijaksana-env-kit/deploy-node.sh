#!/usr/bin/env bash
# BIJAKSANA ENV KIT — deploy to a mesh node (KVM4 / KVM2).
# Usage: deploy-node.sh <host>   (host = ssh alias or IP, e.g. root@100.64.0.5)
# Contract: probe first · install (idempotent) · verify reach · report. No canon touched.
set -euo pipefail
h="${1:?usage: deploy-node.sh <host>}"
KIT="$(cd "$(dirname "$0")" && pwd)"

echo "── 1. PROBE $h (identity, disk, existing env)"
ssh "$h" 'echo "host: $(hostname) · uid: $(id -u)"; df -h / | tail -1; grep -c "AAA-BIJAKSANA" /root/.bashrc 2>/dev/null || echo "no existing block"'

echo "── 2. SHIP kit"
ssh "$h" 'mkdir -p /root/bin /usr/local/bin'
scp -q "$KIT/reality-card.sh" "$KIT/fileprobe.sh" "$KIT/bashrc-bijaksana.block" "$KIT/bijaksana-env-install.sh" "$h:/root/bin/"

echo "── 3. INSTALL + VERIFY (same gate as KVM8: syntax check, auto-revert, env -i reach)"
ssh "$h" 'chmod +x /root/bin/*.sh && /root/bin/bijaksana-env-install.sh && ln -sf /root/bin/reality-card.sh /usr/local/bin/reality && ln -sf /root/bin/fileprobe.sh /usr/local/bin/fileprobe && bash -n /root/.bashrc && env -i bash -c "reality | head -3" && fileprobe /etc/hostname --no-content | grep safety && echo "═══ DEPLOY-OK ═══"'
