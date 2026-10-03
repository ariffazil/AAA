# AAA Skills Renderer v1 — Spec (F13-stage, no build)
**Problem:** `/root/AAA/skills/`, `/root/.claude/skills/`, `/root/.agents/skills/` are 3x independent copies (DIR, not symlink). Coherent by sample, fragile structurally.

**Solution:** Single source of truth + rendered projection.

## Architecture

```
/root/AAA/skills/                  ← WRITABLE (canonical)
/root/.claude/skills/ → rendered   ← READ-ONLY projection
/root/.agents/skills/ → rendered   ← READ-ONLY projection
/root/.codex/skills/ → rendered   ← READ-ONLY projection
```

## Renderer (`/root/AAA/scripts/aaa_skills_render.py`)

- T1-AUTO cron: every 6 hours
- Reads `/root/AAA/skills/<skill>/SKILL.md` and `/root/AAA/skills/<skill>/references/`
- Generates `/root/.claude/skills/<skill>/SKILL.md` (same content)
- Writes manifest: `/root/.claude/skills/aaa_skills_manifest.json`:
  ```json
  {
    "rendered_at": "2026-10-03T15:00:00Z",
    "skills_count": 580,
    "hash_manifest": {"000-salam": "sha256:c0e20ff8...", ...}
  }
  ```
- Drift check: if manifest hash mismatch, FAIL loud
- Idempotent: re-running produces same result

## Harness-specific rendering (v1 = just copy, v2 = adapter per harness)

- v1: same SKILL.md for all harnesses (current behavior)
- v2: per-harness adapter (e.g. Claude might want different frontmatter, different `allowed-tools` field)

## Skills profile (anti-Hermes-chaos)

Currently 580 skills exposed to every agent. Should be:

```yaml
claude-code:
  include: [engineering/**, audit/**, core/federation/**]
  exclude: [personal/**, telegram/**, relationship/**]
codex:
  include: [forge/**, audit/**, core/federation/**]
  exclude: [personal/**, relationship/**]
```

Default profile (no harness-specific config) = union of includes only.

## Reversibility

Renderer is idempotent. Projections are read-only (chmod 555). If renderer breaks, harnesses still work from previous projection (no live dependency).

## Reversibility

None — this is spec only.
