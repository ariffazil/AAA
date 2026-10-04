# Cron Resolver Base Path — The 2026-08-06 Misstep

## What happened

While patching the cron path-mismatch bug (see `cron-script-location-vs-jobsjson-2026-08-06.md`), I patched two `jobs.json` entries:

| Job | Old `script:` | New `script:` |
|---|---|---|
| `eureka-promote` | `eureka-promote.sh` | `cron/scripts/eureka-promote.sh` |
| `SyedOS Receipt Watcher` | `syedos-quiet.sh` | `cron/scripts/syedos-quiet.sh` |

I did this because the scripts live at `/root/HERMES/cron/scripts/` and the patch seemed to add a `cron/scripts/` prefix to point there.

## Why it may be wrong

I never read the cron runner source. I inferred the resolver base from the pattern of working jobs:

| Working job | `script:` value | Actual script location | Inferred resolution base |
|---|---|---|---|
| `morning-brief` | `morning-brief.sh` | `/root/HERMES/scripts/morning-brief.sh` | `/root/HERMES/scripts/` |
| `steel` | `steel.sh` | `/root/HERMES/scripts/steel.sh` | `/root/HERMES/scripts/` |
| `entropy-watch` | `entropy-watch.sh` | `/root/HERMES/scripts/entropy-watch.sh` | `/root/HERMES/scripts/` |
| `forge→vault auto-ingest` | `git_to_vault.py` | `/root/HERMES/scripts/git_to_vault.py` | `/root/HERMES/scripts/` |

All working jobs are bare names from `/root/HERMES/scripts/`. So the scheduler **plausibly resolves relative paths against `/root/HERMES/scripts/`**, not `/root/HERMES/`.

If that inference is correct, my "fix" re-broke the jobs:

- `jobs.json`: `cron/scripts/eureka-promote.sh`
- Resolved: `/root/HERMES/scripts/cron/scripts/eureka-promote.sh`
- Actual file: `/root/HERMES/cron/scripts/eureka-promote.sh`
- Status: ❌ still broken (different path, still wrong)

## The correct fix (if my inference is right)

`mv` the files into the convention directory:

```bash
mv /root/HERMES/cron/scripts/eureka-promote.sh /root/HERMES/scripts/eureka-promote.sh
mv /root/HERMES/cron/scripts/syedos-quiet.sh /root/HERMES/scripts/syedos-quiet.sh
```

Then jobs.json stays as `eureka-promote.sh` (bare name) and `syedos-quiet.sh` — matching the working-job convention.

## The lesson

**Never infer a resolver base from data alone. Read the source.** Git/SCC conventions resolve repo-relative; cron may not. The right probe sequence:

1. Find the cron runner entrypoint (`_probe_job.py` or the scheduler's main loop).
2. Find where the `script:` field is read.
3. Find how it's resolved (absolute? CWD-relative? config-relative?).
4. Apply the fix against the actual resolution, not the inferred one.

Until the resolver source is read, this patch is a coin flip — could be right, could have made it worse.

## What I told Arif

I flagged the ambiguity in the session response. The flag itself is the lesson: when you can't verify the resolution, do NOT claim the fix is correct. State the assumption, offer three resolution paths, and HOLD.

## Cross-references

- `cron-script-location-vs-jobsjson-2026-08-06.md` — the original 3-bug analysis that led to this misstep
- §3.1 of SKILL.md — "repeated sequential closed questions are void-widening" — this patch is part of that meta-pattern: I made a low-confidence fix, then followed with "nak aku buat A, B, or C?" options menus. The right move was to either (a) read the resolver source first and commit, or (b) HOLD with the ambiguity flagged. The middle path — patch and offer options — is the worst of both worlds: action without confidence, then request for permission on top.