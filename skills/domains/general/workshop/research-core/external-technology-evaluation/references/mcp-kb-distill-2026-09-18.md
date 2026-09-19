# mcp-kb (kubed-io/mcp-kb) — Evaluation — 2026-09-18

**Source:** https://github.com/kubed-io/mcp-kb · Reddit r/mcp post by u/burbular
**Trigger:** Arif shared link; OpenClaw also gave a verdict in-thread ("not for our bus, watchlist").
**Mode:** 4 (Capability Equivalence) + 5 (Repo Distill). Question asked: *"is this useful for bus?"*

## Repo truth (gh api + probe, 2026-09-18T19:49Z)

| Field | Value |
|---|---|
| Created | 2026-09-04T21:02:45Z |
| Pushed | 2026-09-18T16:58:20Z |
| Release | v0.1.0 tagged 2026-09-18T17:01:13Z (~2h before evaluation) |
| Stars / forks / watchers | 0 / 0 / 0 |
| Commits | 82 |
| License | MIT |
| Size | 1222 KB (~7.6k LOC Python incl. tests; 36 test files) |
| Contributors | kferrone (77) + 2 bots (solo org; 18 public repos, 0 followers) |
| Stack | FastMCP 4, HTTP/stdio, Docker image `kubed/mcp-kb` |

Arif/OpenClaw's "82 commits, solo org" claim: **VERIFIED**. "0 stars": **VERIFIED**.

## What it actually is

A read-only catalogue server. Config declares three lists — `sources` (git / WebDAV / file), `plugins` (a folder of skills+prompts under a source), `libraries` (the first URI segment; a marketplace, a plugin list, or a query). Everything served under a `skill://` URI grammar; reading is the only operation. Resources are the interface; `list_resources` / `read_resource` / `list_prompts` / `get_prompt` are offered as mirror *tools* only to clients lacking the real primitives.

## Capability-equivalence probe — the decisive part

**We already serve this surface.** Live probe of arifOS MCP `:8088`:

- `resources/list` → **`skill://index`** — *"Federation skill directory — counts computed live. Use skill://{name}/SKILL.md."*
- `skill://index` reads back live counts (13 prompts, 35 resources, 13 hooks).
- 13 prompts + 35 resources registered on the kernel.

**And the primitive is in our stack already:** `fastmcp/server/providers/skills/directory_provider.py` ships inside `/root/GEOX/.venv`, `/root/WELL/.venv`, `/root/WEALTH/.venv` (fastmcp 3.4.4–3.4.6).

⇒ **Capability gap on the core mechanic = 0.** Correct verdict is HOLD / watchlist, consistent with the MarkPDFdown precedent (capability gap 0 → do not install).

## Is it useful for the BUS? — NO

The bus is the dispatch layer: `/root/AAA/a2a-server/wake_bus.js`, `/root/AAA/src/gateway/wake_bus.ts`, NATS `:4222` (live, 8 connections) + monitor `:8222`. mcp-kb has **no publish, no subscribe, no dispatch, no event** — it is a read-only catalogue. Different job. Answer: not for bus.

## The three genuine deltas worth stealing (semantics, not dependency)

1. **Scope ceiling pinned in a header/credential, not a tool argument.** `X-Skill-Library` / `X-Skill-Categories` / `X-Skill-Tags`; a header beats the URL, so a scope pinned inside a credential is one the caller cannot edit away — *"there is no way for a model to ask for material it was not given."* This is our **authority-envelope doctrine applied to skill delivery**: `EffectiveCapability = Capability ∩ AuthorizedEnvelope`, made mechanical for a skill catalogue.
2. **Ref-pinning as claim state.** `?ref=<commit>` for an external source = cannot move = no refresh needed; tracking a branch = `refresh:` interval + rebuild only if the commit moved. That is state-transition discipline for third-party skill material (pin = sealed; branch = ESTIMATED needing revalidation).
3. **Prompt dialect collapse.** One canonical prompt form parsed from its own frontmatter, Claude Code commands (`$ARGUMENTS`), and Copilot `.prompt.md` (`${input:name:hint}`) — dialect detection by strongest signal first (`catalogue/prompts/detect.py`). We have no cross-dialect prompt import.

**Selector semantics detail** (`plugins/select.py`): categories AND tags narrow each other; within categories only OR (a plugin has exactly one); within tags, a comma = all-of and a separate item = any-of (one comma rule for YAML and query string alike). Clean, worth copying verbatim if we ever build scoped skill install.

## Where it *would* be relevant (not the bus)

Our own skill mesh is the real pain (census 2026-09-18): 638 skills on disk, 708 canonical, 805 whole-mesh, **453 loadable**, 29 duplicate identity groups (77 skills), 390 symlink dependents, 3 diverged, **VERDICT WARN**; per-harness overlays (kimi 109 local, qwen 28, opencode 18, gemini 12).

A scope ceiling on our existing `skill://` surface would let a narrow worker (CCC worker, bus agent, OpenClaw lane) receive one slice instead of 805. That is a *wiring* change to something we already run — not an adoption of mcp-kb.

## Verdict

**HOLD / watchlist.** Do not ship. Do not adopt the dependency (FastMCP 4 + Docker image + config file + cache volume) — we already own the mechanic. Keep the note. If ever revisited, take the scope-ceiling semantics and the ref-pin rule, and apply them to `skill://` on `:8088`.

Guard rail: v0.1.0, 2 hours old, 0 stars, one human contributor. Green — not infrastructure trust.
