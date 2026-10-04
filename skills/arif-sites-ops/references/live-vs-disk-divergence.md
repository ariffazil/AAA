# Live Webroot vs Disk Divergence (verified 2026-08-07)

## Symptom

A crawler (EMD, Copilot, research agent) reports a finding that looks like a real defect — e.g. "/world/makcikgpt/ is a landing surface, not a directory index" — but the live page is actually fully populated. Or vice versa: the live page looks fine to a human, but the static source on disk is a stub.

## Root cause

Caddy rewrites/routes serve content from paths that don't always match the webroot file tree. On this profile:

- `/var/www/html/arif/<route>/index.html` on disk MAY NOT be what Caddy serves at `https://arif-fazil.com/<route>/`. The on-disk file can be a 105-byte stub while the served page is a 22-link directory.
- Example observed 2026-08-07: `/var/www/html/arif/world/makcikgpt/index.html` = 105 bytes (`<title>MakcikGPT</title>`), but `curl -s https://arif-fazil.com/world/makcikgpt/` returns a full directory page with 22 `<a href>` article links and `<title>MakcikGPT — Civic Intelligence in Bahasa Makcik | arif-fazil.com</title>`. The on-disk file is a fallback, not the served artifact.

## Investigation procedure (do this BEFORE agreeing with a third-party diagnostic)

1. `curl -sf "https://arif-fazil.com/<route>/" | head -c 1500` — see what Caddy ACTUALLY serves. Don't trust the file on disk.
2. `curl -sI "https://arif-fazil.com/<route>/"` — confirm 200 and `content-type` (text/html vs text/plain matters for llms.txt vs pages).
3. `ls -la /var/www/html/arif/<route>/` — what the webroot contains. May be a stub.
4. `grep -n "<route>\|<path>" /etc/caddy/Caddyfile` — which matcher handles the path; what `try_files` / `rewrite` / `reverse_proxy` it runs.
5. If a rewrite targets another path, follow it: `ls /var/www/html/arif/<target-route>/`.

## Diagnose a third-party claim in 3 questions

A crawler / subagent / sibling reports "X is broken / Y is empty / Z is denied". Before carrying that as truth, ask:

| Question | If NO, the claim is suspect |
|---|---|
| Can you reproduce the failure with a fresh `curl -sf`? | Stale signal, bot-detection, or rate-limit — not a real defect |
| Does `curl -sI` show 200 + expected `content-type`? | Permission/cache signal, not access denial |
| Does the live response body contain the content the diagnostic says is missing? | The diagnostic ran on the wrong URL or wrong extraction mode (e.g. JS-disabled fetch on a SPA route) |

## Live diagnostics that failed this test (2026-08-07)

| Claim | Live evidence that rebuts it |
|---|---|
| "llms.txt triggers PERMISSION_DENIED" | `curl -sI https://arif-fazil.com/llms.txt` → 200, plain text, lists 24 MakcikGPT entries + canonical landing |
| "/world/makcikgpt/ is a landing page, not a directory index" | `curl -s https://arif-fazil.com/world/makcikgpt/` → full directory, 22 `<a href>` article links, real `<title>MakcikGPT — Civic Intelligence in Bahasa Makcik</title>` |
| "Article list behind authentication" | `/sitemap.xml` returns 200 with 23 makcikgpt entries; `robots.txt` allows all major user-agents with `Content-Signal: ai-input=yes` |

## The lesson

**Caddy serves from rewrite targets, not necessarily from webroot-relative paths. Always curl the live URL before believing what the file on disk looks like.** And: third-party crawler diagnostics are evidence to verify, not truth to carry forward. After a contradictable live finding, reissue the diagnostic — the verdict should change with the evidence, not lag it.

## When to add this to your own diagnostic response

When a 888 / EMD / sibling agent reports VOID or UNKNOWN on a path, follow the 3-question table above BEFORE responding with SEALS. If the live evidence contradicts the diagnostic, say so explicitly — the architecture tell-truth doctrine means honest rebuttals are SEALable, silent agreement with a false finding is F2 violation.