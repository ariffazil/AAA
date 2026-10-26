# RECEIPT — Git state correction + reset

**Time:** 2026-10-08 09:54 UTC
**Trigger:** Arif's correction that I had advised opening redundant PRs.

## What I got wrong

I wrote:
> "Paling minimum — buka PR untuk branch squashed, biar CI jalan, merge dari UI"
> "Atau — merge branch 4-commit (lebih simple)"

Both suggestions were wrong:
- `origin/main` was already at `52b1d98` (the 4-commit refinement).
- `feat/kinabalu-refine-squashed` (`bdfd825`) had identical content to
  `main`. `git diff origin/main..feat/kinabalu-refine-squashed` was
  empty.
- Opening either PR would either be a no-op merge or cause conflicts.

This is the F14 / claimed-before-checking pattern Arif has logged as
`scar-2026-09-28-claimed-before-checking-twice` and cousins. Arif
caught it and called it. I correct it now.

## What I did to fix it

1. Verified the content-equality: `diff` between
   `git diff origin/main..feat/kinabalu-refine` and
   `git diff origin/main..feat/kinabalu-refine-squashed` is empty.
2. Reset local `main` to `origin/main` (`52b1d98`) with
   `git reset --hard origin/main`. The squashed `bdfd825` is now an
   orphan local commit, not on any branch.
3. Did NOT push anything. Did NOT delete any branches. Did NOT touch
   origin state.

## Git state at the time of this receipt

```
origin/main                                       = 52b1d98  (canonical)
local main                                        = 52b1d98  (synced)
origin/feat/kinabalu-xsection-models               = be0d018  (left over)
origin/feat/kinabalu-refine                       = 52b1d98  (left over; = main tip)
origin/feat/kinabalu-refine-squashed              = bdfd825  (left over; content = main..be0d018)
local feat/kinabalu-refine                        = 52b1d98
local feat/kinabalu-refine-squashed               = bdfd825
local bdfd825 (orphan)                            = bdfd825
tag v2026.10.08                                   = (auto-tag-date)
tag v2026.10.08-kinabalu                          = (manual)
```

`v2026.10.08-kinabalu` points at the now-orphan `bdfd825`; its content
is identical to what is in main. Fine for now (the tag still names
a real, reachable commit), but worth re-tagging onto `52b1d98` if
Arif wants the tag to point at the canonical HEAD. Not done in this
receipt.

## What was NOT done (held for Arif's word)

- Did NOT delete the three leftover branches.
- Did NOT re-tag.
- Did NOT SSH to VPS.
- Did NOT deploy.
- Did NOT push anything.

## The remaining work (one item, one operator)

The only thing left between `be0d018` on `origin/main` and a live
`arif-fazil.com` is the VPS-side deploy — the agent has no SSH key
to `arif-forge` and cannot run `scripts/deploy-vps.sh`. Arif, from
his laptop, proposed:

1. Read-only SSH to inspect VPS state.
2. Run deploy on Arif's word.
3. Verify live.
4. (Later) delete leftover branches with Arif's approval.

The agent will not act on this receipt's findings. The next move is
Arif's, from his machine.
