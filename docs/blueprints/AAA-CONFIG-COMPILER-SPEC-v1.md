# AAA Config Compiler v1 — Spec (F13-stage, no build)
**Problem:** Live configs in 5+ harnesses drift independently. Today: Codex `config.toml`, Claude `settings.json`, Kimi `mcp.json`, Qwen settings, OpenCode `opencode.json` — each edited by hand, no canonical source.

**Solution:** ONE compiler, ONE desired state, N renderers.

## Architecture

```
/root/AAA/agents/<harness>/
  config/
    settings.template.json    ← canonical desired state
    mcp.profile.yaml
    skills.profile.yaml
    hooks.profile.yaml
    permissions.policy.yaml
                        │
                        ▼
            aaa-config-compiler.py
                        │
                        ├── render → /root/.codex/config.toml (via Codex adapter)
                        ├── render → /root/.claude/settings.json (via Claude adapter)
                        ├── render → /root/.kimi-code/mcp.json
                        ├── render → /root/.qwen-code/settings.json
                        └── render → /root/.opencode/opencode.json
```

## Render contract (C_i)

```
C_i = C_AAA_canonical ⊕ C_harness_adapter ⊕ C_machine ⊕ S_secret
```

| Component | GitHub? | Notes |
|---|---|---|
| C_AAA_canonical | YES | desired state, declarative |
| C_harness_adapter | YES | per-harness rendering rules |
| C_machine | NO | host-specific (paths, ports) |
| S_secret | NO | injected last, never in git |

## Where secrets come in

- Templates reference `${ENV_VAR}` placeholders
- Renderer reads `~/.secrets/vault.env` and substitutes
- If env var missing → render fails LOUD (no silent fallback)
- Renderer never reads `~/.secrets/` directly into the template file

## Drift detection

- After render, compute sha256 of `/root/.claude/settings.json` (excluding `permissions.allow` which is host-specific)
- Compare to manifest hash in `/root/AAA/agents/<harness>/config/manifest.json`
- If mismatch: log warning, do NOT auto-correct (human decides)

## Reverse direction (manual edit → drift)

- If human edits `/root/.claude/settings.json` directly, next render overwrites
- Recovery: `git checkout` from AAA, re-render

## Reversibility

None — this is spec only.
