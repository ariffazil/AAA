# Essay publish + crawler 3-layer lesson bank (2026-08-07 session)

Session-specific knowledge bank for the essay 27 ("I'm Not a Programmer") publish,
the makcikgpt discovery audit, and the F1 syedos lockdown. Sibling-aware: when the
sibling already shipped the static shell + llms.txt + articles.json, **adopt** the
sibling's surface, don't re-inject.

---

## 1. Sibling-already-shipped check (before any essay publish)

Before writing the new `.ts` essay file, run:

```bash
ls /root/arif-fazil.com/sites/arif-fazil.com/src/data/essays/ | grep -iE "<slug-fragment>|<number-fragment>"
grep -l "isDirectPublication: true" /root/arif-fazil.com/sites/arif-fazil.com/src/data/essays/*.ts | head -10
```

If the slug/number is already present under a different filename (e.g. `27-i-didnt-invent-a-token.ts`
for what you thought was `27-i-am-not-a-programmer.ts`), **the sibling has already shipped it**.
Delete your duplicate, upgrade the sibling's body only if needed, and skip steps 2 and 3 of the
canonical recipe. Adopt-and-reconcile costs ~3 minutes; re-do costs ~30.

**Real example (essay 27):**
- My first cut: wrote `28-i-am-not-a-programmer-i-accidentally-invented-a-new-question-for-ai.ts`
- Sibling had already shipped `27-i-didnt-invent-a-token-i-invented-a-question.ts` with the same body
- Right move: delete my 28 file, upgrade the sibling's 27 footer only
- Wrong move: keep both, fight a slug-collision in `index.ts`

## 2. EssayPage.tsx EPISTEMIC_BLURB wiring (5th register detail)

The SPA EssayPage hero strip needs a per-slug epistemic blurb entry in the
`EPISTEMIC_BLURB` map in `src/pages/EssayPage.tsx`. Schema:

```tsx
const EPISTEMIC_BLURB: Record<string, string> = {
  // existing entries
  '<slug>': 'Epistemic Tag: INT — <one-line interpretive context>',
};
```

Falls back to `DEFAULT_EPISTEMIC` if missing — the page still renders, but the
epistemic posture reads as generic INT. Always add the slug-specific entry.

Also add the dynamic INT chip logic for proper rendering:
```tsx
<span className="px-2 py-0.5 border border-forge-iron text-forge-dim">
  {essay.tags?.find((t: string) => /^(INT|OBS|DER|UNK|SPEC)$/i.test(t))?.toUpperCase()
    || (EPISTEMIC_BLURB[essay.slug] ? 'INT' : 'INT')}
</span>
```

This ensures the chip renders even when the slug isn't in the map.

## 3. Branch protection + self-approval deadlock

GitHub's `required_approving_review_count=1` blocks the owner from self-approving their
own PR — `gh pr review --approve` returns "Review Can not approve your own pull request".
This blocks merging solo-authored PRs into protected branches.

**Workaround sequence** (use the option Arif prefers; sequence is also embeddable as
a `git-forge` shell wrapper later):

1. **Approve via GitHub UI** — fastest for one-off, leaves audit trail. Arif clicks 1 button.
2. **Temporarily set `required_approving_review_count=0`** — actually fails because GitHub
   requires integer ≥ 0 in some API versions and rejects with `422`. Skip this path.
3. **Direct push to feature branch + admin-merge without PR** — fastest, but loses the
   PR audit trail. Acceptable for solo work; risky for shared repos.
4. **PR + reviewer request from another GitHub collaborator** — cleanest for teams but
   this repo only has one collaborator (the owner).

For this profile: prefer option 1 (UI click). The deadlock cost ~10 minutes to discover
and is now codified here.

## 4. llms.txt discovery surface — `makcikgpt-md/` not `world/makcikgpt/`

Caddy routes bot User-Agents (GPTBot, ClaudeBot, etc.) to a separate render surface:

```caddyfile
@ai-bot-world {
    header_regexp User-Agent (?i)GPTBot|ClaudeBot|PerplexityBot|OAI-SearchBot|anthropic-ai|Google-Extended|Bytespider|Amazonbot|ChatGPT|curl|python-requests|node-fetch|Go-http-client
    path /world/makcikgpt/*
}
handle @ai-bot-world {
    uri strip_prefix /world/makcikgpt
    root * /var/www/html/arif/makcikgpt-md
    try_files {path} {path}.html {path}/index.html /index.html
    file_server
}
```

This means:
- `/world/makcikgpt/llms.txt` (bot UA) → serves from `/var/www/html/arif/makcikgpt-md/llms.txt`
- `/world/makcikgpt/llms.txt` (browser UA) → served from `/var/www/html/arif/makcikgpt/index.html`
  via the SPA fallback (deceptive-200 if no real file exists)

**Always write llms.txt to `/var/www/html/arif/makcikgpt-md/llms.txt`** (and the matching
`/root/arif-fazil.com/sites/arif-fazil.com/public/world/makcikgpt/llms.txt` source) for
bot discoverability. Browser-UA hits will still hit the SPA, but crawlers get the real file.

## 5. Crawler 3-layer diagnostic doctrine (reusable across all sites)

When a crawler reports a content-discovery failure, the failure is in one of three
distinct layers — NOT the same thing:

| Layer | Question | Diagnostic | Verdict if broken |
|---|---|---|---|
| **Discovery** | Can the crawler find the content? | `curl -sI https://arif-fazil.com/<path>/llms.txt \| head -2` | llms.txt / sitemap / robots.txt returns 404 or wrong content-type |
| **Permission** | Is the crawler allowed? | `curl -sI ... -A "GPTBot"` + check robots.txt Disallow list | robots.txt blocks, or CSP/CORS denies (NOT the case here) |
| **Extraction** | Can the crawler actually get the payload? | Browser `browser_navigate` to URL + check rendered DOM | SPA-only path returns empty shell to JS-disabled crawlers |

**Real failure pattern (2026-08-07):** A crawler reported "permission denied" on
`/world/makcikgpt/llms.txt`. Root cause was NOT permission — robots.txt had 0 disallow
rules. Root cause was **extraction**: the SPA fallback was returning HTML soup at
the llms.txt path because no real file existed. Fix: write real `llms.txt` at
`makcikgpt-md/llms.txt` (per layer 4 above), and the deceptive 200 turns into a real
200 with `content-type: text/plain`.

**Lesson:** don't conflate layers. "Crawler failed" = check all three, name the actual
layer, fix only that. Embodying this in skill, not memory, because the diagnostic
sequence is a class of task not a one-off.

## 6. SyeDOS F1 lockdown (VHost under version control, runtime uninterrupted)

Live sovereign surface at `syedos.arif-fazil.com` (gold trading, heal, nasilemak, rental
SWOT, dashboard). Was running with zero Git perimeter — a single `rm -rf` would destroy
the dashboard. Locked 2026-08-07:

```bash
cd /var/www/html/syedos
git init
git branch -M main
git add .  # 12 files, ~1.2 MB
git commit -m "chore(core): initial commit, F1 lockdown of live syedos vhost"
gh repo create ariffazil/syedos --private --description "Live SyeDOS dashboard..."
git remote add origin git@github.com:ariffazil/syedos.git
git push -u origin main
git commit --amend -m "<proper F1 lockdown message>"  # if initial commit message was generic
git push --force-with-lease  # amend requires force-push on first push
```

**Why `--force-with-lease`:** The initial commit message that GitHub generated on `gh repo
create --push` was a generic "init: ..." — different from the F1 lockdown message we
wanted. Amended the local commit then forced-pushed with lease (safe — refuses if remote
moved). The single force-push on a freshly-created repo with one commit carries zero
risk; on a populated repo, force-push without lease is a self-destructive act.

**Repo is private** — gold trading dashboard contains personal financial context (named
after friend Syed @rico_ricaldo_33). The "Ditempa Bukan Diberi" brand + the named
photo require a private surface, not a public fork.

## 7. Compose-repo dead drop cleanup pattern

Stale drops (e.g. `/root/compose/` with only a `sekrits/` subdir, no `docker-compose.yml`)
are not "L3 ASSET repos" — they're leftover directories that the canon registry
inherited from a one-time git init. Verify with:

```bash
ls /root/<repo>/ | grep -E "\.yml$|\.yaml$|\.toml$|Dockerfile$|README"
git -C /root/<repo> log -1 --format="%ai %s"
[ -z "$(git -C /root/<repo> remote get-url origin 2>/dev/null)" ] && echo "no-remote"
```

If `ls` shows only docs/secrets/test directories, no Docker/orchestration files,
and the remote is unset — it's a dead drop. Quarantine:

```bash
mv /root/<repo> /root/_quarantine_<repo>_<YYYY-MM-DD>
```

Don't `rm -rf` immediately — quarantine preserves F1 reversibility for 30 days.
After 30 days, if no recovery signal, `rm -rf` is fine.

## 8. CasE-Sensitive webroot disambiguation

Linux paths are case-sensitive but humans aren't. `/root/WEALTH` and `/root/wealth`
exist in parallel (the second is a stale Sprint 1 snapshot, the first is the live
organ). Systemd WorkingDirectory pin points to the canonical one. For any cleanup:

```bash
systemctl show wealth-organ.service | grep WorkingDirectory
```

Whatever systemd points to is canon — never delete that path. The other is a
candidate for quarantine. Case-insensitive grep (`grep -ri`) finds both; case-sensitive
operations (`rm -rf`) are precision weapons — verify before you swing.

## 9. Fedora/RHEL vs Debian python3 quirk (recurring across sessions)

`which python3` on this host returns `/root/WEALTH/.venv/bin/python3` (a venv), not the
system Python. The system Python at `/usr/bin/python3.13` is the one that has
`weasyprint` installed. When running matplotlib / weasyprint / Pillow for the
PDF generation pipeline, ALWAYS use the absolute path:

```bash
PY=/usr/bin/python3.13
$PY -c "import weasyprint; print(weasyprint.__version__)"  # verify
$PY build_charts.py
```

The venv Python doesn't have weasyprint/Pillow/matplotlib-system-wide. Pre-existing
skill pitfall (in `pdf-report-generation`), but worth re-stating here because it's
the SAME trap whether you're building PDF charts or building a static HTML render.

## 10. Repo count discipline — the "12 not 27" principle (Arif, 2026-08-07)

> "Aku benci git ni. Aku dah lama suruh jangan banyak sangat repo."

Live project repos under `/root/`: 12-ish (core federation 8 + L3 assets 4). Anything
beyond that is either a workspace (`.openclaw/workspace-*`), a quarantine
(`_quarantine_*`), or noise (`.codex/`, `.nvm/`, `forge_work/`). The audit pattern:

1. `find /root -maxdepth 3 -name ".git" -type d` → all .git dirs
2. Filter out workspaces, quarantines, codex/nvm caches, sibling sandboxes
3. Cross-reference with `web-canon/canon/federation.json` `assets` + `organs` arrays
4. Anything not in the canon OR not a quarantine = drift → investigate

After 2026-08-07 cleanup: 18 total `.git` dirs (4 noise + 14 project), 3 quarantined.
Arif's "12 not 27" was aspirational; reality is ~14 after the cleanup, with 3 quarantined
ready for cleanup in 30 days.

## 11. F1 reversibility pre-flight (the actual lesson from the publish loop)

The hardest F1 lesson of this session was NOT about file ops — it was about
**commit-before-claim**. Three times in the session I said "essay 27 is published"
or "PR 64 is merged" before the operation had actually completed. Always verify
the operation's return code BEFORE claiming success:

```bash
git push origin main 2>&1 | tail -3  # check for "rejected" or "error"
gh pr view 64 --json state  # confirm "MERGED" not just "MERGEABLE"
curl -sI <url> | head -1  # HTTP/1.1 200 OK not assumed
```

The commit-and-push sequence must end with an explicit verification probe. If verification
fails, the operation is NOT complete. Tell the user the truth: "PR 64 is OPEN, blocked
by GitHub self-approval rule. Need your call on how to seal."

## 12. Verifying what siblings shipped (before redoing)

Three sibling shipments were discovered in this session that changed my behavior:

1. **Essay 27 static shell** at `public/words/writing/i-didnt-invent-a-token-i-invented-a-question/{index.html,index.md}`
   was already on disk before my session started. My first cut was a duplicate.

2. **AAA dirty file RSI-recursive-improvement/SKILL.md** turned out to be a phantom —
   my own `cat` invocation triggered the mtime update. Always re-probe before
   committing a "fix" for a dirty state.

3. **PR #64 vs PR #65**: PR #65 (sibling's parallel fix on `feat/seal-essay-27-spa-cleanup-20260807`)
   does SPA cleanup AND bundles with other work. PR #64 (my branch `chore/essay-27-seal`)
   does essay 27 + AUTHOR-FORGED-FOOTER + makcikgpt llms.txt. They're complementary;
   closing both means double-coverage. The right move is to close PR #65 (already
   merged as part of `#62` upstream), keep PR #64 for the essay 27 specific work,
   and let sibling ship the SPA cleanup separately.

Discovery-before-redo saves 30+ minutes per missed sibling.