---
description: Probe all FI coder CLIs live (qwen/kimi/opencode/codex/claude/grok/gemini) and report the mesh matrix
---

Probe every FI coder CLI in the federation with a minimal falsification prompt. For each: run the CLI's one-shot mode asking it to reply with an exact marker string, capture output tail, and classify PASS / FAIL / EXTERNAL (quota/balance).

Current invocations (verify against disk before trusting — these drift):

- Kimi: `kimi -m zai-coding-plan/glm-5.3 -p "Reply with exactly: KIMI-MESH-OK"`
- OpenCode: `opencode run --model litellm-federation/forge-777 "Reply with exactly: OPENCODE-MESH-OK"`
- Codex: `codex exec --skip-git-repo-check "Reply with exactly: CODEX-MESH-OK"` (goes through :4010 middleware)
- Grok: `grok -p "..."` (402 = balance exhausted → EXTERNAL flag, not a mesh defect)
- Gemini: `GEMINI_CLI_TRUST_WORKSPACE=true gemini -p "..."` (429 = quota → EXTERNAL)

Rules: timeout each at 90s; one retry only for transient network; never mask an error as pass; classify external billing/quota failures separately from mesh defects. End with the matrix table + any root-cause fix performed (probe the correct layer before claiming absence — 401 on health = UP, conn-refused = DOWN).
