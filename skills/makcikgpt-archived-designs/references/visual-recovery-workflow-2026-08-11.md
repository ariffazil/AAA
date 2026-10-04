# Visual Recovery Workflow — 2026-08-11 session reference

> **Session:** design-restore-2026-08-11T1437Z
> **Outcome:** Primer Dark landing restored, 82 articles dark-mode injected,
> DESIGN_INVARIANTS.md + design-lint.sh + 3-layer defense locked in.
> **Git commit:** `264d609` · 7 files · +946 / -246
> **VAULT999 receipt:** `design-restore-2026-08-11T1437Z`
> **chain_hash:** `04da323ef014dceda03461b5...`

This is the canonical playbook for **deep archive extraction + visual
recovery**. Use it any time the user complains the current visual is
broken or ugly — the archived git version is the design contract.

## Why this exists

Arif's verbatim rejection on 2026-08-11:
> *"Buruk. Aku x mau ni.. deep archive extraction"*

The current `/world/makcikgpt/` had drifted 4 times since 2026-07-31 —
each agent added "helpful" chrome (epistemic tags, WHERE AM I cards,
Source of truth footer, Canonical landing line) until the journalism
brand looked like a GitHub repo. The fix was NOT to redesign from
current. The fix was to find the **archived good state** in git and
restore it.

## The drift trail (the disease)

| Date | Commit | What was added |
|---|---|---|
| 2026-07-31 | `767596c` | Primer Dark landing (clean baseline — THIS IS THE RECOVERY TARGET) |
| 2026-08-04 | `34fed66` | + epistemic tags + pairings + "read next" navigation |
| 2026-08-08 | `3fe612d` | + zen-pulse WHERE/WHY/WHAT card |
| 2026-08-10 | `051d799` | + Source of truth footer |
| 2026-08-11 | (today) | + Canonical landing + Rendered by |

## The 6-step workflow (verified in session)

### Step 1 — Extract archived HTML to a working directory

```bash
mkdir -p /tmp/makcikgpt-archive
git show 767596c:sites/arif-fazil.com/makcikgpt/index.html > /tmp/makcikgpt-archive/index.html
git show 767596c:sites/arif-fazil.com/public/makcikgpt-md/petronas-dna.html > /tmp/makcikgpt-archive/articles/petronas-dna.html
git show 767596c:sites/arif-fazil.com/public/makcikgpt-md/chennah-bangang.html > /tmp/makcikgpt-archive/articles/chennah-bangang.html
```

### Step 2 — Serve locally on a free port

```bash
cd /tmp/makcikgpt-archive && python3 -m http.server 8765 &
sleep 2
curl -sf -o /dev/null -w "HTTP:%{http_code} SIZE:%{size_download}\n" http://127.0.0.1:8765/index.html
```

### Step 3 — browser_navigate + browser_vision for visual proof

- `browser_navigate` to `http://127.0.0.1:8765/index.html`
- `browser_vision` with question like "Show the full page — every element
  from top to bottom"
- Screenshot auto-saved to `~/.hermes/profiles/aaa-hermes/cache/screenshots/`
- Vision model returns a text description of the rendered visual

### Step 4 — Screenshot the CURRENT (broken) state for comparison

- `browser_navigate` to `https://arif-fazil.com/world/makcikgpt/`
- Same `browser_vision` flow
- The two screenshots now let the user see BEFORE vs AFTER in their chat

### Step 5 — Wait for explicit approval (or proceed if directive is clear)

Arif's pattern:
- "Ok this is nicer" → proceed
- "Hmm. Mana yang lagi senang" → ask for direction
- "Buruk. Aku x mau ni" → deep archive extraction

### Step 6 — Restore + lock in 3-layer defense

```bash
# 6a. Swap generator template (keep data binding, replace CSS/structure)
#     Edit scripts/generate-makcik-index.cjs to use Primer Dark template
node scripts/generate-makcik-index.cjs

# 6b. Sync to live webroot
cp public/makcikgpt-md/index.html /var/www/html/arif/makcikgpt-md/index.html
chown www-data:www-data /var/www/html/arif/makcikgpt-md/index.html
chmod 644 /var/www/html/arif/makcikgpt-md/index.html

# 6c. Inject dark mode CSS into existing article HTMLs (idempotent)
bash scripts/inject-article-styles.sh
# → injected=82 · skipped=1 (the index.html which has its own styling)

# 6d. Write DESIGN_INVARIANTS.md as canonical design SOT
#     - Human-first priority order
#     - The 5 Rein forbidden patterns
#     - Per-surface visual contracts
#     - Recovery procedure from git archive

# 6e. Write design-lint.sh as auto-block
#     Scans public/**/*.html + src/**/*.{tsx,ts,css} for forbidden patterns
#     Exit 1 on any violation

# 6f. Wire design-lint.sh to npm run build prebuild
#     Add `bash scripts/design-lint.sh` to the prebuild script chain
#     Any future agent adding chrome → build fails

# 6g. Fix any pre-existing chrome leaks (e.g. governance page)
#     "Source of truth:" → "Floors canon" + data-meta attribute
```

## Key code patterns

### Generator template (Primer Dark)

```js
// In generate-makcik-index.cjs
function buildIndexHtml(pieces) {
  const today = new Date().toISOString().slice(0, 10);
  const sortedDesc = pieces.slice().sort((a, b) =>
    b.date.localeCompare(a.date)
  );
  // ... extract data, build Primer Dark HTML
  return `<!DOCTYPE html>
<html lang="ms">
<head>
  <!-- Google Fonts: Inter + JetBrains Mono -->
  <style>
    :root {
      --bg:#0a0a0a; --bg-card:#1a1a1a;
      --red:#e0301e; --blue:#1f3fd4; --yellow:#f2b705;
      --fg:#f0f0f0; --fg-muted:#9a9a9a;
    }
    /* ... Primer Dark styles */
  </style>
</head>
<body>
  <!-- Topbar with tricolor pills: SEAL 999 (red) · BM (yellow) · DATE (blue) -->
  <!-- Hero with white/blue/red/yellow flow: "Makcik Tanya. Kuasa Jawab." -->
  <!-- Stats: 22 ARTIKEL · 5 SIRI · 999 SEAL · BM -->
  <!-- Pull-quote with yellow left border -->
  <!-- Terbaru (red ●) · Siri (blue ◆) · Semua (yellow ■) -->
  <!-- Footer with persona signature -->
</body>
</html>`;
}
```

### Article CSS injector (idempotent)

```bash
# scripts/inject-article-styles.sh
# Sentinel: "MAKCIKGPT ARTICLE — Primer Dark reader"
# Only injects if sentinel isn't present
# Skips index.html (landing has its own styling)
```

### Chrome-lint pattern

```bash
# scripts/design-lint.sh
FORBIDDEN_PATTERNS=(
  "Canonical landing:"
  "WHERE AM I?"
  "WHY CARE?"
  "Source of truth:"
  "Rendered by"
  "Generated by"
  "src/data/essays.json"
  "scripts/generate-makcik-index.cjs"
)

for pattern in "${FORBIDDEN_PATTERNS[@]}"; do
  if grep -F -- "$pattern" "$file" >/dev/null 2>&1; then
    echo "❌ FORBIDDEN CHROME: '$pattern'"
    echo "   file: $REL_PATH · line: $LINES"
    VIOLATIONS=$((VIOLATIONS + 1))
  fi
done
```

## Chrome-creep drift trail (the disease, for the record)

Drift between 2026-07-31 → 2026-08-11:

```
2026-07-31  767596c  Primer Dark baseline (CLEAN)
2026-08-04  34fed66  + epistemic tags, pairings, "read next"
2026-08-08  3fe612d  + zen-pulse WHERE/WHY/WHAT card
2026-08-10  051d799  + "Source of truth: src/data/essays.json"
2026-08-11  (today)  + "Canonical landing:" + "Rendered by scripts/"
```

Each addition was "small." Combined, they turned a journalism brand into
a GitHub repo. The 5 Rein are the patterns that enabled this drift.

## Files sealed in this session

| File | Status | Purpose |
|---|---|---|
| `DESIGN_INVARIANTS.md` | NEW | Canonical design SOT — what is/isn't allowed in visual surfaces |
| `scripts/design-lint.sh` | NEW | Auto-block — fails build if any Rein appears in visual HTML |
| `scripts/inject-article-styles.sh` | NEW | Idempotent retrofitter — injects dark-mode CSS into article HTMLs |
| `scripts/generate-makcik-index.cjs` | EDITED | Restored Primer Dark template (tricolor topbar, hero, stats, quote, series cards, footer) |
| `public/governance/index.html` | EDITED | Fixed "Source of truth:" leak → "Floors canon" + data-meta attribute |
| `public/makcikgpt-md/index.html` | REGENERATED | From updated generator — Primer Dark live |
| `package.json` | EDITED | Added `bash scripts/design-lint.sh` to prebuild hook |

## Verification commands

```bash
# Lint passes?
bash /root/arif-fazil.com/sites/arif-fazil.com/scripts/design-lint.sh
# → ✅ PASSED — no agent-chrome detected (542 files scanned)

# Landing live?
curl -sf -o /dev/null -w "%{http_code}\n" https://arif-fazil.com/world/makcikgpt/
# → 200

# Article live + dark mode?
curl -sf -o /dev/null -w "%{http_code}\n" https://arif-fazil.com/world/makcikgpt/petronas-dna
# → 200

# Git commit?
git -C /root/arif-fazil.com log --oneline -1
# → 264d609 feat(site): restore Primer Dark landing + dark-mode articles, lock design SOT

# VAULT999 receipt?
tail -1 /root/arifOS/VAULT999/outcomes.jsonl | jq .
# → {session_id: "design-restore-2026-08-11T1437Z", ...}
```

## Anti-patterns to avoid

- ❌ **Redesigning from current state** — perpetuates drift. Find archive first.
- ❌ **Patching only what's visible** — chrome is structural. Rebuild template.
- ❌ **`cp` of archived HTML** — data binding diverges. Adapt template only.
- ❌ **Skipping local serve + screenshot** — user is visual, decide from images.
- ❌ **Treating `git show` output as final** — it's text. Render with browser.
- ❌ **Single-pass restoration without lint** — without design-lint.sh, drift returns.

## See also

- `FORGE-agentic-web-builder` skill — chrome-creep doctrine + 3-layer fix
- `arif-site-human-first-audit` skill — anti-bulldoze pattern + 4-lane audit
- `essay-publish-pipeline` skill — chrome pitfall + design language match
- `/root/arif-fazil.com/sites/arif-fazil.com/DESIGN_INVARIANTS.md` — the SOT
- `/root/arif-fazil.com/sites/arif-fazil.com/scripts/design-lint.sh` — the auto-block
