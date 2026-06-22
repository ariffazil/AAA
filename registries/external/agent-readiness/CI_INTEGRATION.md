# agent-readiness-action — CI Integration Snippets

> **Phase 5 (awaits 888)**: add to AAA / arifOS / arif-sites CI workflows.
> **Status**: documented here for when 888 approves.

## Minimum (per-deploy gate)

```yaml
- uses: lingzhong/agent-readiness-action@v0.1
  with:
    url: https://aaa.arif-fazil.com
```

Default `min-level: 2`. Ratchet up as we build out `.well-known/`.

## With deploy preview

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    outputs:
      url: ${{ steps.publish.outputs.url }}
    steps:
      - id: publish
        # ...your deploy step, setting `url` output

  agent-readiness:
    needs: deploy
    runs-on: ubuntu-latest
    steps:
      - name: Check Agent Readiness
        uses: lingzhong/agent-readiness-action@v0.1
        with:
          url: ${{ needs.deploy.outputs.url }}
          min-level: 4
```

## Suggested gates per domain (DER from 2026-06-22 standing)

| Domain | min-level | Rationale |
|---|:---:|---|
| `aaa.arif-fazil.com` | 5 | Cockpit — must be Agent-Native (highest bar) |
| `arifos.arif-fazil.com` | 4 | Kernel — must expose MCP + Agent card |
| `geox.arif-fazil.com` | 4 | Same |
| `wealth.arif-fazil.com` | 4 | Same |
| `well.arif-fazil.com` | 4 | Same |
| `arif-fazil.com` | 3 | Top-level site — minimum Agent-Readable |

## Soft-fail defaults

This action is **soft-fail by default** — if the scanner is unreachable or
returns malformed JSON, the step emits `::warning::` and passes. Rationale:
"a third-party outage shouldn't block your deploy." Set
`fail-on-scanner-unavailable: true` to flip to hard-fail.

For our case: prefer **hard-fail** because the scanner reports OUR OWN state
on OUR OWN domains — if scanner is down, something is wrong.

## Examples

Full examples in upstream repo:
- Cloudflare Pages: `examples/cloudflare-pages.yml`
- Vercel: `examples/vercel.yml`
- GitHub Pages: `examples/github-pages.yml`

## Standalone script (for local debugging)

```bash
URL=https://aaa.arif-fazil.com ./scripts/check-readiness.sh
```

This is best-effort local debugging — the supported surface is the
composite GitHub Action.
