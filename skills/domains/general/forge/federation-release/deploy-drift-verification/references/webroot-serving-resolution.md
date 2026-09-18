# Webroot serving resolution — which file actually answers a URL

Companion to the "layer above the artifact" section. Worked values come from a Caddy-fronted
React SPA host with a split config and split roots; re-probe rather than trusting the numbers,
the shapes are what carry over.

## The config is a dispatcher plus per-site files

```
/etc/caddy/Caddyfile              # global: TLS defaults, shared snippets, import line
/etc/caddy/vhosts/<host>.conf     # every handler, redirect and matcher for one host
```

`Caddyfile` ends with `import /etc/caddy/vhosts/*.conf`. Grepping it for a site's handlers returns
nothing — which reads as "the rule is gone" and invites a futile restore of config that was never
broken. Validate and reload still target `Caddyfile` (the import graph resolves); only *editing*
moves to the vhost.

```bash
grep -n 'import /etc/caddy/vhosts' /etc/caddy/Caddyfile
ls -t /etc/caddy/vhosts/<host>.conf.bak-* | head -3   # last agent's intent, and why
```

Timestamped `.bak-<ts>-<tag>` files sit beside each vhost. Read the newest before editing — it is
the cheapest record of what changed last and under what authorization.

## Two matchers decide everything

- `@static_dirs` — an explicit path list served by `file_server`, rooted at the site webroot.
- `@spa_routes` — path prefixes handed to the catch-all (shell + JS bundle).

**Membership in `@spa_routes`, not the existence of a file, decides what a visitor sees.** A route
under that matcher renders client-side, and any static file at the same path is dead weight.

```bash
grep -n '@spa_routes\|@static_dirs' /etc/caddy/vhosts/<host>.conf
```

Corollary for authoring: a React route that exists in the app's route table but is absent from
`@spa_routes` 404s; adding the route file alone publishes nothing.

## Worked check — a page that exists twice

| Where | Size | Answers the URL? |
|---|---|---|
| React route in `src/pages/` | — | **yes** |
| `<webroot>/<path>/index.html` | ~47 KB | **no** |

The live title is the shell's and the response is bundle-sized (~9 KB), not the file's. Editing the
webroot copy changes nothing a visitor can see.

## Split roots

Handlers inside one site block can root at different trees — a top-level webroot for some surfaces,
a nested one for the rest. A deploy that syncs only the primary root leaves the others stale while
reporting success.

```bash
grep -n 'root \*' /etc/caddy/vhosts/<host>.conf | sort -u
```

Where the repo ships a secondary-root sync script, it is part of the deploy: run it last, and treat
a non-zero exit as a failed deploy rather than a cosmetic warning.

## Closure probe

```bash
curl -s "$URL" | grep -o '<title>[^<]*'              # what the visitor gets
curl -s "$URL" | wc -c                              # bundle-sized = the shell answered
grep -o '<title>[^<]*' <webroot>/<path>/index.html  # what you were about to edit
```

For an SPA route the only receipt is a string unique to the new content appearing in the served JS
bundle. A `200`, and even a correct-looking shell title, prove nothing about your change.

## Authoring consequence

When the deliverable is a new page on an SPA route, the publish path is: source component → route
entry → rebuilt bundle → sync → sync secondary roots. Every step after the first is invisible in
isolation, which is why the content grep on the bundle is the step that closes it.
