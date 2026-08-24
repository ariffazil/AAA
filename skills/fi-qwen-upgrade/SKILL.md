---
id: fi-qwen-upgrade
name: fi-qwen-upgrade
version: 1.0.0
description: "Atomic-swap upgrade of the Qwen Code release install (SHA256-verified, rollback-preserved). Use when Arif says 'upgrade qwen', 'qwen update', 'new qwen version', or when `qwen update` refuses with a misleading git-clone message."
owner: 333-AGI
risk_tier: medium
floor_scope: [F1, F2, F11]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Qwen Code Atomic-Swap Upgrade

Qwen Code at /root is a release tarball install at `/root/.local/lib/qwen-code/`, NOT npm and NOT a git clone. `qwen update` refuses with a misleading "git clone" message; `npm install -g` writes to the wrong path. Manual atomic-swap is the only working upgrade (proven 2026-08-14/18/21).

## Procedure

1. `qwen --version` — record current OLD version.
2. Fetch expected hash: `curl -fsSL https://github.com/QwenLM/qwen-code/releases/download/vNEW/SHA256SUMS | grep linux-x64`
3. Download tarball to /tmp, verify `sha256sum` MATCHES. **Mismatch → abort, report.**
4. `mv /root/.local/lib/qwen-code /root/.local/lib/qwen-code.old.OLD` (preserve active — F1 reversibility)
5. `tar -xzf /tmp/qwen-code-NEW.tar.gz -C /root/.local/ && mv /root/.local/qwen-code /root/.local/lib/qwen-code`
6. Write `/root/.local/lib/qwen-code/.qwen-rollback-info.json` with preservedVersion / updatedTo / timestamp / reason / rollback command.
7. Verify `qwen --version` → NEW. Clean tarball.
8. `settings.json` is never touched — yolo/empty-deny + provider entries survive (config is version-agnostic).

## Rollback

`mv /root/.local/lib/qwen-code.old.OLD /root/.local/lib/qwen-code`. The running session keeps the old binary in memory; next launch gets the new one. Never delete the `.old` tree same-day.
