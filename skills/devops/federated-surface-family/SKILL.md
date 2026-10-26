---
name: federated-surface-family
description: Use when building or linking a page family on a static site
---

# Federated Surface Family

Pattern for making many pages feel like ONE site without flattening their identities: shared navigation frame, per-surface accent identity, data-driven file sets, bidirectional family cross-links. Hardened against the static-site failure modes that silently break it. Canonical live example: the Bayang family on arif-fazil.com (PM Bayang, AI Labs Bayang, Kerusi Bayang, MakcikGPT under `/world/`).

## The pattern (in build order)

1. **Extract, don't rewrite.** When promoting a flat article into a family surface, extract the body programmatically from the source artifact and re-skin only the chrome. Content mutation during a design migration = fabrication risk; the source document is CANON.
2. **Ship the full file set per surface:** `index.html` + `index.json` (machine parity) + `index.md` (text mirror) + `llms.txt`. A surface missing any witness is fragile — the markdown mirror is what survives a browser-lane failure.
3. **Shared frame, individual identity.** Every surface carries the site nav canon plus a FAMILY nav cross-linking its siblings; each surface keeps its own accent colour. The parent hub lists every member. A reader must always know which room they're in AND that they're still in the same house.
4. **Wire every direction.** New member → add to every sibling's nav, add to the parent hub listing, and sweep ALL existing navs for stale links. Legacy navs accumulate dead entries over time (old 11-link navs with several 404 destinations are the common residue); a new surface is the cheap moment to fix them.
5. **Verify the reader's path, not the file.** Final gate: every hub/listing link serves its own `<title>` and returns the expected content marker; sibling surfaces unchanged.

## Diagnosis pitfalls (each verified in production)

- **Split roots:** a path prefix may be served from a DIFFERENT webroot than its parent (e.g. `/world/*` → `/var/www/html/arif` but `/world/politics/*` → `/var/www/html` on the same vhost). Before editing any live page, prove which copy serves it: `md5sum` every candidate copy against `curl -s <url> | md5sum`. Patch the serving copy, then mirror to the other so a future handler change can't resurrect stale content. Two copies disagreeing is a scope fact, not a contradiction.
- **try_files self-loop:** a fallback chain ending in the hub's own `index.html` turns a deleted page into an HTTP 200 that serves the hub itself. 200 is not link health — verify each listing link serves its OWN `<title>`; hub-title-returned = dead link masquerading. If only `index.html.bak-*` remains, restore from it (`cp` + chmod 644); the content is intact — rebuilding is wasted entropy.
- **SPA fallback fake-200:** a remembered URL may never have existed — the SPA shell answers any unknown path with 200 and a generic title. Run archive archaeology (`find` across deploy snapshots/backups + `git log --grep`) before believing "it used to exist". Empty archaeology = build new, don't hunt a ghost. Diagnostic: generic site `<title>` + no unique content marker = shell.
- **Bot lane ≠ browser lane:** a URL can serve raw markdown to curl's default Accept and a JS shell to a browser Accept. Probe with full browser headers (`-A "Mozilla/5.0 …" -H "Accept: text/html,application/xhtml+xml"`) when answering "what does a human see".
- **Regex anchors on multi-line HTML:** section markup like `<section class="x">\n<h1>Name</h1>` breaks single-line regex assumptions — allow `\s*` between tags, and dedupe slugs when the same name can appear twice (append `-1`, `-2`). After structural edits, balance-check tags (open count == close count for section/details/nav/table/div) before shipping.

## Anti-over-engineering gate

Before adopting an external design brief (multi-phase prompt, N-component system, M deliverables), audit it against what the page already has: epistemic labels, text mirrors, and plain-language status labels often already exist. Adopt only the delta (orientation strip, layered TOC, progressive disclosure of dense sections via `<details>`); reject the rest as museum-building. Verify adversarial claims inside the brief ("page returns 403") by probing with multiple user-agents before accepting the premise — agents self-report their own tool failures as site facts.

## Rollback discipline

`cp <page> <page>.bak-<tag>` before structural surgery. Keep the backup in place after success — it is the restore path for the next agent, not trash.

## Known overlap (for the curator)

`arif-sites-ops` (in skills.external_dirs, read-only to autonomous curation) is the site-level umbrella this pattern grew out of. If consolidated, fold this skill's pitfalls into its Pitfalls section; until then both stay, this one is the portable pattern, that one the site map.