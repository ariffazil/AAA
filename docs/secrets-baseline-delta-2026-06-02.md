# AAA Secrets Baseline — Proposed Delta (197 new entries)

**Review gate:** this is the trust-list expansion. Each entry below is flagged by `detect-secrets` as a potential secret. **None are in my new `composio/` files.** All 197 are pre-existing in AAA repo (baseline stale since 2026-05-22).

**Authority required (F13 + 888_HOLD):** this delta adds entries to the trusted-secrets allowlist. Per your directive, this needs explicit human review before merge.

---

## By file (grouped, with type counts)

| File | New | Types |
|------|-----|-------|
| `wiki/.arifos/wiki_files.jsonl` | 164 | Hex High Entropy String ×164 |
| `.secrets.baseline` | 26 | Hex High Entropy String ×13, Secret Keyword ×13 |
| `contracts/mcp_surface.yaml` | 2 | Secret Keyword ×2 |
| `scripts/deepseek-forge/README.md` | 2 | Secret Keyword ×2 |
| `a2a-server/server.js` | 1 | Telegram Bot Token ×1 |
| `.github/workflows/secrets-audit.yml` | 1 | Hex High Entropy String ×1 |
| `src/gateway/server.ts` | 1 | Telegram Bot Token ×1 |
| `wiki/.arifos/wiki_files.jsonl` (additional) | 1 | Secret Keyword ×1 |

## Categorization (recommended verdicts)

| Detector type | Count | Recommended verdict |
|---|---|---|
| **Hex High Entropy String** | 178 | Likely false positive (file content hashes, wiki metadata) — needs eyeball spot-check on 1-2 |
| **Secret Keyword** | 18 | Needs per-entry review (could be real) |
| **Telegram Bot Token** | 2 | Likely false positive (`bot\d+:` regex matches `bot_token` strings) — confirm |

## Per-file analysis (recommended review depth)

### `wiki/.arifos/wiki_files.jsonl` — 164 hex strings

These are likely wiki file content hashes / sha256 metadata. The detector flags any 32+ char hex string as high-entropy. **Recommendation:** eyeball 1-2 entries to confirm they're hashes (not API keys), then bulk-allow.

### `.secrets.baseline` itself — 26 entries

The baseline file gets flagged when its own content triggers patterns. This is self-referential and expected. **Recommendation:** bulk-allow (the baseline is by definition trusted).

### `contracts/mcp_surface.yaml` + `scripts/deepseek-forge/README.md` — 4 entries

These are documentation/config files. The "Secret Keyword" detector may match words like `password`, `api_key`, `token` in YAML keys or doc text. **Recommendation:** eyeball to confirm context is documentation, not actual secrets.

### `a2a-server/server.js` + `src/gateway/server.ts` — 2 entries (Telegram Bot Token)

The `bot\d+:[A-Za-z0-9_-]{20,}` regex matches any token-shaped string. The AAA repo has Telegram bot config (hermes-asi-gateway). **Recommendation:** check whether the matched line is the actual bot token (if so, REMOVE — that's a real secret), or a sample/config reference (if so, allow).

### `.github/workflows/secrets-audit.yml` — 1 entry

The workflow file itself contains the regex patterns the scanner looks for. Self-referential. **Recommendation:** bulk-allow.

---

## Recommended review flow

1. **First pass (5 min):** eyeball the 2 Telegram Bot Token matches. Confirm whether they are real tokens or config references.
2. **Second pass (5 min):** spot-check 1-2 hex strings from `wiki/.arifos/wiki_files.jsonl`. Confirm they're hashes.
3. **Bulk allow (1 min):** once first two passes pass, regenerate baseline via:
   ```bash
   detect-secrets scan . > .secrets.baseline
   ```
4. **Commit + PR (separate from composio embodiment):**
   - `chore(aaa): regenerate secrets baseline — 197 trust entries reviewed`
   - Add this diff summary to the PR body.
   - Wait for human approval before merge.

---

**Status:** Diff summary prepared. Awaiting your review of the Telegram Bot Token entries and the hex strings before regeneration. **Baseline regeneration is held (888_HOLD).**

DITEMPA BUKAN DIBERI
