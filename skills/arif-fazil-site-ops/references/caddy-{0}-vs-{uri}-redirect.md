# Caddy `{0}` vs `{uri}` wildcard redirect quick-reference

Captured 2026-08-07 from the `/writing/*` → `/words/writing/*` redirect chain fix.

## The bug (15 min lost)

```caddyfile
redir /writing/* /words/writing{uri} 308
```

For input `/writing/the-agi-paradox-...`, Caddy:

- `{uri}` = `/writing/the-agi-paradox-...` (the FULL request URI)
- The redirect target becomes `/words/writing/writing/the-agi-paradox-...`
  (the `/writing/` prefix is **doubled** because `{uri}` already included it).

Result: 308 to a 404 path. Browser follows, gets 404, gives up.

## The fix (option A — wildcard capture)

```caddyfile
redir /writing/* /words/writing/{0} 308
```

`{0}` is the first wildcard `*` capture segment, equal to `the-agi-paradox-...`
only — no leading `/writing/`.

## Why option A is risky

Caddy's `{0}` expansion in `redir` directives is **inconsistent across
versions**. On the Aug 2026 install (Caddy 2.x), `{0}` silently produced an
empty string for some requests, breaking the redirect target to
`/words/writing/` (no slug appended). This caused an entirely different
failure mode: 308 to `/words/writing/` → 200 (the listing page) instead of
the actual essay.

**Detection:**
```bash
curl -sIL https://arif-fazil.com/writing/the-agi-paradox-... | grep -E 'HTTP|location:'
# Symptom:  location: /words/writing/     (no slug — {0} was empty)
# Expected:  location: /words/writing/the-agi-paradox-...   ({0} worked)
```

## The fix (option B — recommended)

**Don't redirect slugs in Caddy at all.** Only redirect the top-level path.
The SPA handles per-slug routing.

```caddyfile
redir /writing   /words/writing/   308
redir /writing/  /words/writing/   308
# DO NOT add:  redir /writing/* /words/writing/{0} 308   ← too risky
```

For per-essay URLs, the SPA's React Router at `/words/writing/:slug`
already resolves the slug via `EssayPage` → `getEssay(slug)`. As long as
the Caddyfile `@agent_shells` matcher includes `/words` (or `/words*` in
`@spa_routes`), the SPA fallback `try_files {path} {path}/index.html
/index.html =404` will serve the React index.html and the client router
will resolve `:slug` correctly.

## The full `@agent_shells` requirement

For SPA-rendered nav-canon paths (like `/words/writing/<slug>/`):

1. `@agent_shells` matcher must include the path prefix:
   ```caddyfile
   @agent_shells path /missions /missions/ /missions/* /economics ... /words /words/ /words/*
   ```

2. Inside the `@agent_shells` handle, the `@writing_spa` matcher
   (or equivalent per-section fallback) must extend to the new path:
   ```caddyfile
   @writing_spa path /writing/* /words/writing/* /words/writing
   try_files @writing_spa {path} {path}/index.html /index.html =404
   ```

3. `@spa_routes` global matcher also needs the path:
   ```caddyfile
   @spa_routes path / ... /words* /work* ...
   ```

If any of these three is missing, the path 404s at the static_dirs layer
before ever reaching the SPA fallback.

## Triple-check after Caddyfile edits

```bash
sudo caddy validate --config /etc/caddy/Caddyfile   # Always
sudo systemctl reload caddy                         # Reload, never restart

# Three-layer test
echo "=== Top-level legacy redirect ==="
curl -sI https://arif-fazil.com/writing/ | head -2     # 308 to /words/writing/

echo "=== Per-essay via SPA fallback ==="
curl -sI https://arif-fazil.com/words/writing/the-agi-paradox-.../ | head -2   # 200

echo "=== Static file dir still works (if it exists) ==="
curl -sI https://arif-fazil.com/words/writing/index.html | head -2   # 200
```

## Related

- Skill body: "Caddy `{uri}` is FULL URI — use `{0}` for wildcard capture" pitfall
- Skill body: "Adding a nav-canon path to the SPA" pitfall (full recipe)
- Skill body: "Caddy routing order" (which matcher fires first)