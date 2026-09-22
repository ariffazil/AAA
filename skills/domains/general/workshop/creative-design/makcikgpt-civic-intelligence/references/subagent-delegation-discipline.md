# Subagent Delegation Discipline — Article Forging

When delegating any MakcikGPT article work to a background `delegate_task` subagent, three drift modes are predictable. Constrain upfront, audit after.

## The Three Drift Modes

### 1. Component / Asset Drift
Subagent given "create article TS file" may ALSO write React components (panels, pages), video assets, audit reports, or companion articles.

**Constraint directive:** "ONLY create `<slug>.ts`, `<slug>.md`, and modify `index.ts`. Do NOT create components, panels, pages, video assets, or any file outside this trio. If you think you need anything else, STOP and ask."

**Post-delegation audit:**
```bash
git status --short sites/arif-fazil.com/ -- '*.tsx' '*.ts' | grep -v 'src/data/makcikgpt/\|src/data/essays.json'
```
Anything listed there is drift.

### 2. Slug Rename Mid-Task
Subagent may rename the slug (e.g., `truth-dalam-void` → `truth-sembunyi-dalam-void`) without warning, creating an orphan .ts file with the old slug. Both files share the same internal `slug` field, causing React duplicate key warnings and 404s.

**Constraint directive:** "The slug is `<exact-slug>`. Do NOT rename it for any reason. If you find the slug conflicts with existing content, STOP and report back — do not auto-rename."

**Post-delegation audit:**
```bash
ls /root/arif-fazil.com/sites/arif-fazil.com/src/data/makcikgpt/<topic-keyword>*.ts
```
Expected: exactly one file.

### 3. Probe-for-Existing Skipped
Subagent given "write article X" may write a fresh draft without checking whether existing content already covers similar territory. The subagent then OVERWRITES the existing draft.

**Constraint directive:** "First, run these greps. If matching content exists, READ it before writing:
```
ls /root/arif-fazil.com/sites/arif-fazil.com/src/data/makcikgpt/
grep -l '<core-concept-keyword>' /root/arif-fazil.com/sites/arif-fazil.com/src/data/makcikgpt/*.ts
```
If similar content exists, READ it before writing. Either build on it or explicitly fork a different angle."

**Post-delegation check:** `git log --diff-filter=M --oneline src/data/makcikgpt/` — recent modifications should match the delegation scope, not surprise overwrites.

## Build/Deploy Boundary

Subagents are FORGE tools, not deploy authorities. Always state:
"Do NOT run `npm run build`, `make deploy`, `caddy reload`, or any deploy command. Create files only."

Main thread owns: `npm run build`, `rsync dist/ → webroot`, smoke tests, deploy verification.

## Audit Block — Run Before Accepting Subagent Output

```bash
# 1. Slug uniqueness in source
ls /root/arif-fazil.com/sites/arif-fazil.com/src/data/makcikgpt/<slug>*.ts

# 2. Index registration (1 = import only)
grep -c "from './<slug>'" /root/arif-fazil.com/sites/arif-fazil.com/src/data/makcikgpt/index.ts

# 3. Meta entry
grep -c "slug: '<slug>'" /root/arif-fazil.com/sites/arif-fazil.com/src/data/makcikgpt/index.ts

# 4. Out-of-scope source files (drift detection)
git status --short sites/arif-fazil.com/ -- '*.tsx' '*.ts' \
  | grep -v 'src/data/makcikgpt/\|src/data/essays.json'

# 5. Mark mirror created
ls /root/arif-fazil.com/sites/arif-fazil.com/public/makcikgpt-md/<slug>.md
```

Any failure → fix in main thread before proceeding to build. Subagent output is a draft, not a deployable artifact, until audit passes.

## Proven Failures

- **2026-09-22 (Kenapa Syarikat Tu Hantu):** Existing 16k-char article silently overwritten with sub-shorter draft. Probe-for-existing would have caught it.
- **2026-09-22 (Yang x Diungkap):** Subagent renamed slug mid-write, created two .ts files, broke deployment. Locked-slug directive would have prevented it.
- **2026-09-22 (Yang x Diungkap, also):** Subagent authored `reality-over-everything.ts` as a third article without being asked. Component-scope directive would have prevented it.
- **2026-09-22 (Yang x Diungkap, also):** Main thread fixed the URL drift in source files (renamed `...sembunyi-...ts` → `...-dalam-void.ts`) but the index.ts was already written by the subagent using the un-suffixed slug, so the rename broke registration. When fixing a subagent's slug drift, also re-verify `index.ts` matches the actual filename on disk before deploy.
- **2026-09-22 (Yang x Diungkap, also):** Stale URL served 200 with SPA "Artikel Tidak Dijumpai" fallback. The Caddy 301 redirect unblocked it in ~3 min, but the user still saw the wrong page because their browser cached the SPA fallback HTML. After Caddy fix, ALWAYS tell the user to hard-reload / clear cache / try incognito — the server-side fix is invisible until the client refetches.
- **2026-09-22 (Reality Over Everything):** Sibling subagent dispatched in parallel overwrote main thread's `index.ts` edits mid-flight. Multi-subagent dispatch on the same file is a race; serialize file writes through main thread or accept the conflict-cost.
