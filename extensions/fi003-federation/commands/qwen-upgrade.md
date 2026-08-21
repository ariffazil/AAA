---
description: Atomic-swap upgrade of the Qwen Code release install (SHA256-verified, rollback-preserved)
---

Upgrade Qwen Code at /root (release install, NOT npm). Procedure (proven 2026-08-14/21):

1. `qwen --version` — record current OLD version.
2. Fetch expected hash: `curl -fsSL https://github.com/QwenLM/qwen-code/releases/download/vNEW/SHA256SUMS | grep linux-x64`
3. Download tarball to /tmp, verify `sha256sum` MATCHES. Mismatch → abort, report.
4. `mv /root/.local/lib/qwen-code /root/.local/lib/qwen-code.old.OLD`
5. `tar -xzf /tmp/qwen-code-NEW.tar.gz -C /root/.local/ && mv /root/.local/qwen-code /root/.local/lib/qwen-code`
6. Write `/root/.local/lib/qwen-code/.qwen-rollback-info.json` with preservedVersion/updatedTo/timestamp/reason/rollback command.
7. Verify `qwen --version` → NEW. Clean tarball.
8. `settings.json` is never touched — yolo/empty-deny + provider entries survive (config is version-agnostic).

Rollback: `mv /root/.local/lib/qwen-code.old.OLD /root/.local/lib/qwen-code`. The running session keeps the old binary in memory; next launch gets the new one. Never force-push, never delete the .old tree same-day.
