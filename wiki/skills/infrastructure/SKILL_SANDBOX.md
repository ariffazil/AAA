---
title: "SKILL: Cloudflare Sandbox SDK"
type: skill
version: 1.0.0
category: cloud
risk_band: MEDIUM
floors: []
evidence_required: false
sources: [/root/.agents/skills/sandbox-sdk/SKILL.md]
confidence: high
---

# SKILL: Cloudflare Sandbox SDK

> **Build secure, isolated code execution environments on Cloudflare Workers.**
> **Source:** `/root/.agents/skills/sandbox-sdk/SKILL.md`
> **Agent:** OpenCode (Ω-FORGE)
> **Forged:** 2026-05-17

---

## Trigger Conditions

- Building AI code interpreters
- Secure code execution for untrusted code
- CI/CD systems with isolated builds
- Interactive development environments
- Keywords: sandbox-sdk, cloudflare sandbox, code execution, isolation, docker

---

## Retrieval Directive

**Prefer retrieval over pre-training.** Fetch `https://developers.cloudflare.com/sandbox/` for latest docs.

---

## Quick Reference

| Task | Method |
|------|--------|
| Get sandbox | `getSandbox(env.Sandbox, 'user-123')` |
| Run command | `await sandbox.exec('python script.py')` |
| Run code (interpreter) | `await sandbox.runCode(code, { language: 'python' })` |
| Write file | `await sandbox.writeFile('/workspace/app.py', content)` |
| Read file | `await sandbox.readFile('/workspace/app.py')` |
| List files | `await sandbox.listFiles('/workspace')` |
| Expose port | `await sandbox.exposePort(8080)` |
| Destroy | `await sandbox.destroy()` |

---

## Code Interpreter (Recommended for AI)

```typescript
const ctx = await sandbox.createCodeContext({ language: 'python' });
await sandbox.runCode('import pandas as pd; data = [1,2,3]', { context: ctx });
const result = await sandbox.runCode('sum(data)', { context: ctx });
// result.results[0].text = "6"
```

**Languages:** `python`, `javascript`, `typescript`

---

## When to Use What

| Need | Use | Why |
|------|-----|-----|
| Shell commands | `exec()` | Direct control, streaming |
| LLM-generated code | `runCode()` | Rich outputs, state persistence |
| Build/test pipelines | `exec()` | Exit codes, stderr capture |

---

## Extending the Dockerfile

```dockerfile
FROM docker.io/cloudflare/sandbox:0.7.0
RUN pip install requests beautifulsoup4
EXPOSE 8080
```

---

## Anti-Patterns

- ❌ Use internal clients (`CommandClient`, `FileClient`) — use `sandbox.*` methods
- ❌ Skip the Sandbox export — Worker won't deploy
- ❌ Hardcode sandbox IDs for multi-user — use user/session identifiers
- ❌ Forget cleanup — call `destroy()` for temporary sandboxes

---

## Related Pages

- [[skill-agents-sdk]] — Agents SDK integration
- [[skill-durable-objects]] — Durable Objects
- [[SCHEMA.md]] — TREE777 governance schema

---

*DITEMPA BUKAN DIBERI — Sandbox isolated. Code executed securely.*
