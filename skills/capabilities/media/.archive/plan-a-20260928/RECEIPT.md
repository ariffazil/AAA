# PLAN A · media-symlink-repair — Lineage Receipt

> **Stamped:** 2026-09-28 KVM8, sovereign authority: ARIF
> **Executor:** HERMES, mode-first gate PASS, OBSERVE_ONLY state cleared.
> **Operation:** repair three broken symlinks in capabilities/media/ by
> re-pointing at the conventional sibling-skill path (../../<name>), matching the
> live `token-plan-image` convention.

## Repairs

| Symlink (dead → live) | Old target | Canonical SKILL.md sha256 |
|---|---|---|
| image-analyzer-vision | /root/.hermes/profiles/aaa-hermes/skills/image-analyzer-vision/SKILL.md | (recorded at exec) |
| token-plan-speech      | /root/.hermes/profiles/aaa-hermes/skills/token-plan-speech/SKILL.md       | (recorded at exec) |
| token-plan-video       | /root/.hermes/profiles/aaa-hermes/skills/token-plan-video/SKILL.md        | (recorded at exec) |

## Convention

`telegram-ops`, `token-plan-image`, `forge-tailwind-tokens`, etc. already
follow the relative sibling-skill layout. Plan A brings the three broken
media-cluster entries into the same convention.

## Archive

This file lives at `/root/AAA/skills/capabilities/media/.archive/plan-a-20260928/RECEIPT.md`.
It is the lineage fossil for the three replacements — **preserved per F2 TRUTH**.

## Rollback

```bash
cd /root/AAA/skills/capabilities/media
for n in image-analyzer-vision token-plan-speech token-plan-video; do
  ln -sfn /root/.hermes/profiles/aaa-hermes/skills/$n/SKILL.md $n
done
```

The rollback restores the original dead-pointer targets. This state is
known-broken; restore it only for forensics.

