---
id: forge-git-seal
name: forge-git-seal
description: Batch-seal dirty repos with decision-trail commits.
risk_tier: low
floor_scope: [F1, F2]
autonomy_tier: T1
tags: [git, commit, seal, federation, batch]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Forge Git Seal

> DITEMPA BUKAN DIBERI — every commit is a decision trail for the next agent.

## Procedure

### 1. Survey all repos

```bash
for d in /root/{arifOS,A-FORGE,AAA,GEOX,WEALTH,WELL,arif-fazil.com,arifFlow}; do
  if [ -d "$d/.git" ]; then
    dirty=$(git -C "$d" status -s 2>/dev/null | wc -l)
    [ "$dirty" -gt 0 ] && echo "$(basename $d): $dirty dirty"
  fi
done
git -C /root/.hermes status -s 2>/dev/null | wc -l
```

### 2. Batch small repos first

Commit independent repos in parallel. Smallest diff first, then medium, then large (AAA, hermes last).

```bash
cd /root/<repo> && git add -A && git commit -m "<message>"
```

### 3. Decision-trail commit messages

Every commit must include WHAT, WHY, and FOR FUTURE AGENTS.

```
seal: <short summary>

<what changed>

<rationale>

FOR FUTURE AGENTS: <what they need to know>
```

Pitfall: "update files" commits are invisible to future agents. Write as if the next agent has zero context.

### 4. Handle pre-commit gates

Read the gate's verdict before deciding anything. Three outcomes, three different moves:

- **PASSED** — final line reads `⬡ PRE-COMMIT HARD GATES: PASSED`. Proceed.
- **Advisory only** — `MUSYAWARAH GATE [DRY-RUN]` / `[WOULD-HOLD]` counts, LSP warnings on files you did not touch. These do not block; commit normally.
- **BLOCKED** — a named rule plus a named file, e.g. `DOCTRINE-STATUS GATE: commit blocked — R3 instructions/X.md …`. **Never `--no-verify`.** The gate found a real defect: fix it, then re-commit.

**When the blocked file is GENERATED, patch the generator, not the file.** A hand-added
label on a generated artifact is erased by its next regeneration, so the same block returns
for the next agent — who is then the one tempted to bypass it. Grep the repo for the
filename to find the writer (renderer, emitter, scaffold) and make it emit the required
line. That converts a recurring block into a permanent fix.

Worked rule in this estate: a new `.md` under `instructions/` or `governance/` must carry a
`Status:` line (doctrine-status gate). A generated, non-authority artifact satisfies it by
declaring itself **from the generator**:
`Status: generated index (non-doctrine artifact, holds no authority) — do not edit by hand`.

Only when the source fix is genuinely out of reach (a third-party file you may not edit) is a
bypass a candidate — and then declare it in the commit body as a deviation, with the reason.
An undeclared `--no-verify` is indistinguishable from a hidden defect.

### 5. Verify clean state

```bash
for d in /root/{arifOS,A-FORGE,AAA,GEOX,WEALTH,WELL,arif-fazil.com,arifFlow,hermes}; do
  [ -d "$d/.git" ] && count=$(git -C "$d" status -s 2>/dev/null | wc -l) && \
    [ "$count" -eq 0 ] && echo "OK $(basename $d)" || echo "DIRTY $(basename $d)"
done
```

## Pitfalls

- Don't commit secrets. Scan for .env files first (repo-cleanup mode=secret).
- Don't commit state files: jobs.json, *.lock, deliveries.db.
- For code repos, review `git diff --cached --stat` before committing.
- First line under 72 chars for `git log --oneline` compatibility.
- **A commit seal is not a history rewrite.** Never "fix" a stale or oversized record by rewriting history — supersede it in a new commit. Evicting a blob from history is a separate governed act with its own snapshot/pin/verify discipline: `git-history-hygiene`.
- **One writer per repo at a time.** If another lane is rebasing, filtering or pruning, your `git status`/`git log` reads are of a moving target — see `concurrent-agent-writers`.
- **`git add -A` over a tree holding data dumps commits them to history forever.** An oversized vector-DB export, a `.jsonl` receipt pile, a model blob inside a source repo: after `git add -A`, `git reset -- <that path>` and state the exclusion in the commit body (`data, not source; belongs in backups`). A silent exclusion reads as an oversight; a stated one is a decision a future agent can honour.
- **A repo dirty on a dozen unrelated surfaces is several lanes' in-flight work, not one change.** Commit it as an explicit checkpoint: say so in the body, name the parent commit as the pre-checkpoint state, and state plainly that nothing beyond the repo's own gates was verified. Do not fabricate a review that did not happen, and do not leave the tree dirty to avoid facing it.
- **Runtime-state files in the dirty set are expected, not drift.** Session registries, cursors, `jobs.json` and flow offsets change by themselves; say so in `FOR FUTURE AGENTS` so the next reader does not chase them as a defect.
- **A repo seal is only the lowest of four seal layers.** `repo (git commit)` ≠ `receipt file on disk` ≠ `session ledger / carry_forward` ≠ `kernel VAULT999`. Report the layer you reached *with its state* — `repo=SEALED (<sha>) · receipt=SEALED (<path>) · VAULT999=PENDING F13`; a bare "sealed" is a claim about the top layer. When the vault layer is not yours to write, do not end with a chat sentence: write a hand-off packet (`/root/arifOS/VAULT999/seal_requests/<ID>.json`, schema `arifos.seal_request.v2` — copy the shape of an existing packet, including `state_evidence.before/after` and a `fixes_declined_by_design` list with reasons) and present ONE binary to the sovereign: append, or refuse. **Never bind with another actor's private key or claim their `actor_id` to earn the vault line** — that is self-issuing an envelope, and it defeats the one thing the gate checks. A missing key of your own is a governance fact to report, not an obstacle to route around.

## Federation repo map

| Repo | Gate |
|------|------|
| hermes | None (direct) |
| AAA | Pre-commit (LSP + musyawarah) |
| arifOS | Pre-commit (musyawarah) |
| GEOX | Pre-commit (musyawarah + LSP) |
| arifFlow | Pre-commit (musyawarah) |
| WELL/arif-fazil.com | Pre-commit (minimal) |
| A-FORGE/WEALTH | Pre-commit (full) |

---
Forged 2026-09-18. DITEMPA BUKAN DIBERI.