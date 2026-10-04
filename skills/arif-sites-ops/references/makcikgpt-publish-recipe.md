# MakcikGPT article publishing recipe (verified 2026-08-09)

Session evidence: two articles ("Syaitan yang Ingat Dirinya Malaikat", "13 Sebab
Tengku Taufik Kena Berhenti Sekarang") published after two failed attempts that
earned "Pembohong hang" and "Manusia first!!" from Arif. Failure modes captured here.

## Canonical paths (the #1 failure mode)

```text
/var/www/html/arif/makcikgpt-md/<slug>.html    ← WRITE HERE (what Caddy serves)
/var/www/html/arif/makcikgpt-md/index.html     ← landing page, must be updated
/var/www/html/arif/world/makcikgpt/            ← TRAP: NOT the serve root for articles
```

Caddy handler `handle /world/makcikgpt/*` does `uri strip_prefix /world/makcikgpt`
then `root * /var/www/html/arif/makcikgpt-md`. Writing to `world/makcikgpt/<slug>/`
produces a file Caddy never serves. A sibling agent may also rebuild
`makcikgpt-md/` wholesale (observed 2026-08-09 06:47) — your files vanish;
keep a copy in `/tmp` or a proposal zone until confirmed live.

## Steps

1. **Write the article** to `/var/www/html/arif/makcikgpt-md/<slug>.html`
   (full HTML shell: same head/style pattern as existing articles — Fraunces/
   Newsreader/IBM Plex Mono, `.makcik-header` + `.makcik-voice` + `.makcik-fact`
   blocks, forge-black bg). Copy the structure of the newest existing article.
2. **Fix permissions immediately**: `chmod 644 <file>`. A root-owned `0600` file
   is invisible to Caddy's worker (symptom: 200 on the WRONG content, or 404,
   while `curl` as root from the same box appears to work).
3. **Update the index** (`makcikgpt-md/index.html`) — it has TWO lists:
   - Grouped `<details class="zen-reveal">` per series (M1 Energy / M2 Governance /
     M3 Tech & Sovereignty / M4 Economy / M5 Politics), entry format:
     `<li><a href="/world/makcikgpt/<slug>">Title</a> <span class="date">YYYY-MM-DD · seal 999</span></li>`
   - Hidden `<ul class="flat-list">` for feed readers, entry format:
     `<li><a href="/world/makcikgpt/<slug>">Title</a> <span class="date">— Series M<n>#<seq>, YYYY-MM-DD · seal 999</span></li>`
   Add to BOTH. PETRONAS/oil/gas/rightsizing pieces → Series M1.
   Also bump the "NN articles · updated YYYY-MM-DD" line and the meta description
   article count (they drift otherwise).
4. **Use python for index inserts, not blind sed.** A sed pattern matching both
   list sections inserted the entry twice per section (4 duplicates observed).
   Python with a seen-flag dedupe is the verified-safe path; if you must sed,
   grep-count afterwards and clean duplicates.
5. **Verify ALL gates before telling Arif it's live:**
   ```bash
   SLUG=<slug>
   curl -s -o /dev/null -w "%{http_code}\n" "https://arif-fazil.com/world/makcikgpt/$SLUG"
   curl -s "https://arif-fazil.com/world/makcikgpt/$SLUG" | grep -oP "<title>\K[^<]+"
   curl -s "https://arif-fazil.com/world/makcikgpt/?v=$(date +%s)" | grep -c "$SLUG"   # must be ≥1
   ```
   Article 200 + correct title + index link present + landing page unbroken +
   other articles unbroken = publish complete. Anything less = not published.

## Trailing-slash behaviour

`/world/makcikgpt/<slug>/` → 301 → `/world/makcikgpt/<slug>` → 200. This is
normal Caddy canonicalisation, not a bug. Probe without the trailing slash when
verifying; `curl -L` follows the redirect fine either way.

## Persona and content rules (Arif, 2026-08-09)

- **No author attribution.** Never put Arif's name, "Geoscientist", UW-Madison,
  or any identity marker in the article. Voice = MakcikGPT persona only.
  Arif: "Jangan letak nama aku, letak persona makcikgpt. Aku ni bukan anak raja.
  Aku share artikel x dak sapa baca." The persona IS the distribution strategy.
- **Register:** bahasa makcik kampung — short sentences, "Makcik nak tanya...",
  kedai-runcit/getah analogies for financial concepts, `.makcik-fact` blocks for
  every number. Viral-first: a makcik kampung must be able to read and forward it.
- **Facts:** every number from audited sources (AFS, IFR), tagged `[OBS]` in the
  footer. "Semua nombor diaudit. Tiada ramalan. Tiada spekulasi."
- Footer sign-off: `— MakcikGPT · Civic Intelligence · <date> · [OBS]` +
  "Enjin melapor. Manusia yang putuskan. Yang benar dikarang, bukan diberi."
- 888-APEX pre-review is optional; if F6 MARUAH flags strong language, anchor the
  attack on the SYSTEM not the person (one sentence does it) — Arif overrode F6
  caution for the CEO pieces explicitly, but the systemic framing kept the article
  defensible.

## Discovery surfaces

`/world/makcikgpt/llms.txt` carries the article inventory for agents. It is
rebuilt by the index generator (`scripts/generate-makcik-index.cjs` per the
index footer) — if you hand-edit the index, check whether llms.txt needs the
same entry, or note the drift for the next rebuild.
