# Proposal-zone lifecycle — the 3-file pattern for site proposals

Proven on `/work/` page (2026-08-11). Every new static HTML page that lives under
`dist/<path>/index.html` must go through a proposal zone before F13 promotion.
The zone is the only writable location for the proposal agent; the 3-file shape
is the canonical deliverable.

---

## The 3 files

| File | Role | Contains |
|---|---|---|
| `index.html` | The page itself | Inline CSS, zero external JS dependencies, ready to drop into dist/ |
| `README.md` | Human-browsable narrative | What was built, why, design choices, deploy path, rollback path, open notes |
| `FORGE_RECEIPT.json` | Machine-readable audit trail | SHA256 of each file, timestamps, compliance flags, promotion path, incidents |

**What FORGE_RECEIPT.json must cover:**

```json
{
  "mission_id": "<mission>/v<N>",
  "agent": "<agent-id>",
  "authority": "PROPOSAL",
  "state": "awaiting_f13_review",
  "created_at": { "utc": "...", "myt": "...", "tz": "Asia/Kuala_Lumpur", "iso_week": "..." },
  "subject": {
    "intended_path": "sites/arif-fazil.com/dist/<path>/index.html",
    "intended_url": "https://arif-fazil.com/<path>/",
    "proposal_zone": "forge_work/proposals/<agent-id>/<mission>/v<N>/",
    "promotion_requirement": "F13 SOVEREIGN seal + verify-pages gate"
  },
  "files_written": [
    {
      "path": "/root/forge_work/proposals/<agent-id>/<mission>/v<N>/index.html",
      "role": "deliverable",
      "size_bytes": ...,
      "lines": ...,
      "sha256": "<sha256>",
      "encoding": "utf-8",
      "self_contained": true,
      "works_without_js": true,
      "sections": ["header", "section 1: ...", "section 2: ...", "..."],
      "jargon_scan": {
        "forbidden_tokens_checked": ["F1-F13", "VAULT999", "MCP", "A2A", "GEOX", "AAA"],
        "result": "PASS — no federation-internal terms"
      }
    },
    {
      "path": "/root/forge_work/proposals/<agent-id>/<mission>/v<N>/README.md",
      "role": "proposal_narrative",
      "size_bytes": ...,
      "lines": ...,
      "sha256": "<sha256>",
      "sections": ["what was built", "design choices", "deployment path", "rollback path"]
    },
    {
      "path": "/root/forge_work/proposals/<agent-id>/<mission>/v<N>/FORGE_RECEIPT.json",
      "role": "governance_receipt",
      "sha256": "<self_hash_or_pending>"
    }
  ],
  "file_hashes": {
    "index.html": "<sha256>",
    "README.md": "<sha256>"
  },
  "deployment_blocked_reason": "FAIL-CLOSED — no dist/ mutation without F13 seal",
  "compliance": {
    "file_authority_yaml": "FAIL-CLOSED respected — no writes outside forge_work/proposals/<agent-id>/<mission>/v<N>/",
    "dist_mutation": false,
    "canon_mutation": false,
    "no_jargon_hard_rule": "PASS",
    "no_react_no_vite_no_build": "PASS — pure static HTML, inline CSS",
    "self_contained": "PASS — works with JS disabled"
  },
  "promotion_path": {
    "step_1": "F13 SOVEREIGN reviews proposal",
    "step_2": "Copy index.html to sites/arif-fazil.com/dist/<path>/index.html",
    "step_3": "Confirm route in Caddy @spa_routes + _redirects",
    "step_4": "make verify-pages → HTTP 200 for <path>",
    "step_5": "Reload Caddy"
  },
  "rollback_path": {
    "trigger": "F13 vetoes or rejects",
    "step_1": "Delete sites/arif-fazil.com/dist/<path>/index.html",
    "step_2": "Delete forge_work/proposals/<agent-id>/<mission>/v<N>/ to retire",
    "no_dependents": "No Caddy config, _redirects, or canon touched"
  },
  "observer_notes": ["..."],
  "governance_incidents": [],
  "verification": {
    "type": "ad-hoc",
    "script": "/tmp/hermes-verify-<topic>.sh",
    "last_run": "2026-08-11T00:00:00Z",
    "note": "No canonical test suite — static HTML, spec compliance only"
  }
}
```

---

## FAIL-CLOSED: what agents may NOT do

The proposal agent writes ONLY to `forge_work/proposals/<agent-id>/<mission>/v<N>/`.

**Forbidden:**

- Writing to `sites/arif-fazil.com/dist/<path>/index.html` — this is a DERIVED path, hand_edit: false
- Writing to `sites/arif-fazil.com/public/<path>/`
- Editing `canon/navigation.json`, `_redirects`, `/etc/caddy/Caddyfile`
- Running `npm run build` or `deploy-site.sh`
- Marking the work as "deployed" or "verified"

Promotion (copy to dist/, route wiring, verify-pages, Caddy reload) is F13's sovereign act.

---

## Sibling FAIL-CLOSED dist/ mutation — detection + recovery

When multiple agents write to the same proposal zone, a sibling may:

1. Write a different version with a conflicting content model (different section count, wrong voice, jargon)
2. Write directly to `dist/<path>/index.html`, completely bypassing F13

**Detection:**
```bash
# After ANY sibling activity near the proposal zone, probe dist/
ls -la /root/arif-fazil.com/sites/arif-fazil.com/dist/<path>/index.html

# If it exists, verify its hash — does it match your proposal?
sha256sum /root/arif-fazil.com/sites/arif-fazil.com/dist/<path>/index.html
```

**Recovery:**
1. Read the sibling's files. Compare content model against the delegation brief, NOT against the sibling's output.
2. **The brief is the source of truth.** Overwrite the sibling's forge_work files with brief-aligned versions.
3. If the sibling wrote to dist/, **delete that dist/<path>/index.html** (single `rm`).
4. Record the incident in `FORGE_RECEIPT.json` under `governance_incidents[]`.

**Why this is DIFFERENT from post-deploy md5sum reconciliation:** post-deploy, a sibling may enrich a live (F13-approved) page — adopt theirs if better. Proposal-stage, the sibling is writing to dist/ WITHOUT F13 seal — the cleanup is a `rm`, not a `cp` from the live webroot.

---

## Ad-hoc verification script template

Copy, adapt, run, delete. The script verifies spec compliance, not visual quality.

```bash
#!/usr/bin/env bash
# Ad-hoc verification for <topic> proposal
# Created by <agent-id>, <date>.
set -uo pipefail

PROPOSAL="/root/forge_work/proposals/<agent-id>/<mission>/v<N>"
INDEX="$PROPOSAL/index.html"
README="$PROPOSAL/README.md"
RECEIPT="$PROPOSAL/FORGE_RECEIPT.json"

PASS=0; FAIL=0; WARN=0
ok()   { printf "  \033[32mPASS\033[0m  %s\n" "$1"; PASS=$((PASS+1)); }
fail() { printf "  \033[31mFAIL\033[0m  %s\n" "$1"; FAIL=$((FAIL+1)); }
warn() { printf "  \033[33mWARN\033[0m  %s\n" "$1"; WARN=$((WARN+1)); }
head() { printf "\n\033[1m%s\033[0m\n" "$1"; }

# ─── ADAPT: replace placeholders (TOPIC, PATH, JARGON_PATTERN, SECTIONS, TOKENS, LINKS) ───

TOPIC="<topic>"
EXPECTED_INDEX_HASH="<sha256>"
EXPECTED_README_HASH="<sha256>"
JARGON_PATTERN='F1-F13|constitutional floors|VAULT999|\bMCP\b|\bA2A\b|\bGEOX\b|\bAAA\b|\bfederation\b'
SECTIONS=('id="section-1"' 'id="section-2"' 'id="section-3"')
DESIGN_TOKENS=('#0A0A0A' '#141414' '#D4A853' '#E8E8E8')
FONTS=('Fraunces' 'Cabinet Grotesk' 'IBM Plex Mono')
FOOTER_LINKS=('/essays/' '/doctrine/' '/999/')
TAGLINE='Ditempa Bukan Diberi'

# ─── 1. File existence ────────────────────────────────────────────────────
head "1. File existence"
for f in "$INDEX" "$README" "$RECEIPT"; do
  [[ -f "$f" ]] && ok "$(basename "$f") ($(stat -c '%s' "$f") bytes)" || fail "$(basename "$f") MISSING"
done

# ─── 2. JSON validity ─────────────────────────────────────────────────────
head "2. JSON validity"
python3 -c "import json; json.load(open('$RECEIPT')); print('')" 2>/dev/null \
  && ok "FORGE_RECEIPT.json is valid JSON" \
  || fail "FORGE_RECEIPT.json is NOT valid JSON"

# ─── 3. SHA256 receipt matches disk ───────────────────────────────────────
head "3. SHA256 receipt matches reality"
ACTUAL_IDX=$(sha256sum "$INDEX" | awk '{print $1}')
ACTUAL_RM=$(sha256sum "$README" | awk '{print $1}')
[[ "$ACTUAL_IDX" == "$EXPECTED_INDEX_HASH" ]] && ok "index.html matches receipt" || fail "index.html HASH MISMATCH"
[[ "$ACTUAL_RM" == "$EXPECTED_README_HASH" ]] && ok "README.md matches receipt" || fail "README.md HASH MISMATCH"

# ─── 4. No federation-internal jargon ─────────────────────────────────────
head "4. No federation-internal jargon"
if grep -E "$JARGON_PATTERN" "$INDEX" >/dev/null 2>&1; then
  fail "Forbidden jargon found:" && grep -oE "$JARGON_PATTERN" "$INDEX" | sort -u | sed 's/^/    /'
else
  ok "No federation-internal terms"
fi

# ─── 5. Section anchors present ───────────────────────────────────────────
head "5. Sections present"
for sec in "${SECTIONS[@]}"; do
  grep -q "$sec" "$INDEX" && ok "anchor: $sec" || fail "anchor MISSING: $sec"
done

# ─── 6. Section 1 item count ──────────────────────────────────────────────
head "6. Section 1 item count"
EXPECTED_ITEMS=<N>
ACTUAL_ITEMS=$(grep -c '<h3>' "$INDEX" 2>/dev/null || echo 0)
[[ "$ACTUAL_ITEMS" -eq "$EXPECTED_ITEMS" ]] && ok "Section 1: $ACTUAL_ITEMS items" || fail "Section 1: $ACTUAL_ITEMS items (expected $EXPECTED_ITEMS)"

# ─── 7. Section 2 item count ──────────────────────────────────────────────
head "7. Section 2 item count"
EXPECTED_Q=<N>
ACTUAL_Q=$(python3 -c "import re; m=re.search(r'<ol class=\"questions\">(.*?)</ol>', open('$INDEX').read(), re.S); print(len(re.findall(r'<li>', m.group(1)) if m else 0))")
[[ "$ACTUAL_Q" -eq "$EXPECTED_Q" ]] && ok "Section 2: $ACTUAL_Q questions" || fail "Section 2: $ACTUAL_Q questions (expected $EXPECTED_Q)"

# ─── 8. Footer links ──────────────────────────────────────────────────────
head "8. Footer links"
for link in "${FOOTER_LINKS[@]}"; do
  grep -q "href=\"$link\"" "$INDEX" && ok "footer: $link" || fail "footer MISSING: $link"
done

# ─── 9. Design tokens ─────────────────────────────────────────────────────
head "9. Design tokens (inline CSS)"
for token in "${DESIGN_TOKENS[@]}"; do
  grep -q "$token" "$INDEX" && ok "token: $token" || fail "token MISSING: $token"
done
grep -qE 'max-width: 720px|max-width: var\(--max-width\)' "$INDEX" \
  && ok "container max-width: 720px" || fail "container max-width not 720px"

# ─── 10. Font stack ───────────────────────────────────────────────────────
head "10. Font stack"
for font in "${FONTS[@]}"; do
  grep -q "$font" "$INDEX" && ok "font: $font" || fail "font MISSING: $font"
done

# ─── 11. Self-containment ─────────────────────────────────────────────────
head "11. Self-containment"
grep -qE 'src="main\.tsx"|src="/src/main' "$INDEX" && fail "Vite/React extern detected" || ok "no React/Vite reference"
grep -c '<style>' "$INDEX" | awk '{if ($1>=1) exit 0; exit 1}' && ok "inline <style> present" || fail "no inline <style>"

# ─── 12. Tagline / motto ──────────────────────────────────────────────────
head "12. Tagline"
grep -q "$TAGLINE" "$INDEX" && ok "tagline present" || fail "tagline MISSING"

# ─── 13. META tags ────────────────────────────────────────────────────────
head "13. META tags"
for meta in 'og:title' 'og:description' 'twitter:card' 'canonical' 'llms-full-content'; do
  grep -qi "$meta" "$INDEX" && ok "meta: $meta" || warn "meta MISSING: $meta"
done

# ─── 14. No dist/ mutation (FAIL-CLOSED check) ────────────────────────────
head "14. No dist/ mutation"
DIST_PATH="/root/arif-fazil.com/sites/arif-fazil.com/dist/<path>/index.html"
[[ -f "$DIST_PATH" ]] && fail "dist/<path>/index.html EXISTS — sibling violation" || ok "dist/<path>/index.html does not exist"

# ─── 15. Timestamp hygiene ────────────────────────────────────────────────
head "15. Timestamp hygiene"
TS_UTC=$(python3 -c "import json; print(json.load(open('$RECEIPT'))['created_at']['utc'])")
[[ -n "$TS_UTC" ]] && ok "UTC timestamp present: $TS_UTC" || fail "UTC timestamp MISSING"
TS_MYT=$(python3 -c "import json; print(json.load(open('$RECEIPT'))['created_at']['myt'])")
[[ -n "$TS_MYT" ]] && ok "MYT timestamp present: $TS_MYT" || fail "MYT timestamp MISSING"

# ─── 16. README required sections ─────────────────────────────────────────
head "16. README required sections"
for section in 'What was built' 'Design choices' 'Deployment path' 'Rollback plan'; do
  grep -qi "$section" "$README" && ok "README: $section" || fail "README section MISSING: $section"
done

# ─── REPORT ───────────────────────────────────────────────────────────────
echo ""
echo "════════════════════════════════════════════════════"
printf "  PASS: %d   FAIL: %d   WARN: %d\n" "$PASS" "$FAIL" "$WARN"
echo "════════════════════════════════════════════════════"
[[ "$FAIL" -eq 0 ]] && { echo "  ✓ All hard checks pass (warnings are advisory)"; exit 0; }
echo "  ✗ Hard checks failed — review output above"; exit 1
```

**Adaptation guide:**

- Replace `<agent-id>`, `<mission>`, `<topic>`, `<N>`, `<path>` with actual values
- Replace `EXPECTED_INDEX_HASH`, `EXPECTED_README_HASH` with the actual sha256sum values
- Replace `JARGON_PATTERN` — add or remove tokens depending on the delegation brief's no-jargon rule
- Replace `SECTIONS[]` — the exact `id="..."` anchors or section-count check
- Replace `DESIGN_TOKENS[]` — the exact color hexes from the design brief
- Replace `FONTS[]` — the font families referenced
- Replace `FOOTER_LINKS[]` — the exact paths expected in footer links
- Replace `TAGLINE` — the expected motto or brand text

**Run:** `chmod +x /tmp/hermes-verify-<topic>.sh && bash /tmp/hermes-verify-<topic>.sh`

**Clean up:** `rm /tmp/hermes-verify-<topic>.sh`

---

## Promotion path (F13's job after approving the proposal)

1. **Seal:** F13 reviews the proposal at `forge_work/proposals/<agent-id>/<mission>/v<N>/`
2. **Copy:** Move `index.html` to `sites/arif-fazil.com/dist/<path>/index.html`
3. **Route:** Confirm `<path>` is reachable (Caddy `@spa_routes` + `_redirects`)
4. **Gate:** `make verify-pages` → HTTP 200 for `<path>/`
5. **Reload:** `sudo systemctl reload caddy`

---

## Rollback path (if F13 vetoes)

1. Delete `sites/arif-fazil.com/dist/<path>/index.html`
2. Delete `forge_work/proposals/<agent-id>/<mission>/v<N>/` to retire the proposal
3. No Caddy config, no `_redirects`, no canon touched — zero routing cleanup needed

---

*Proven on the /work/ page proposal (2026-08-11).*
