# MCP site diff (Q2) — branch `site/claude-2026-10-15`

**File:** `sites/arif-fazil.com/public/mcp/index.html`
**Probe basis (live, not memory):**
- `https://mcp.arif-fazil.com/mcp` → status 405 on GET (correct for streamable-http POST endpoint).
- `curl :7072/health` (2026-10-15 23:14Z): `"service":"A-FORGE-MCP"`, `"transport":"streamable-http"`, `"tools_listed":122`.
- Canonical F5 floor name from `sites/shared/observatory.js:232` and `dist/floors.json:72`: **`PEACE²`**.

---

## Diff

| # | Line(s) | Before | After | Why |
|---|---|---|---|---|
| 1 | 761 | `and the 7-organ federation with cryptographic proof.` | `and the 7-organ federation across A-FORGE gateway and arifOS sense. A cryptographic attestation surface is in design — anon reads are signed at the transport plane, not by content. (See "What it does not yet prove" below.)` | Removes the marketing claim "cryptographic proof"; the live endpoint signs at the transport plane, not the content plane. Honest redirect to the gaps box. |
| 2 | 842 (Claude Desktop snippet) | `"transport": "http"` | `"transport": "streamable-http"` | Matches `:7072/health` `transport` field. |
| 3 | 874 (Claude CLI snippet) | `claude mcp add --transport http arifos …` | `claude mcp add --transport streamable-http arifos …` | Same alignment. |
| 4 | 1232 | `Execution without prior SEAL verdict is impossible.` | `Execution without prior SEAL verdict is refused.` | Removes "impossible" (mathematical claim). The kernel returns an enumerable refusal — not an impossibility proof. |
| 5 | 1252 | `1 Fail (F5 Memory Calibration)` | `1 Fail (F5 PEACE²)` | Canonical floor name. "Memory Calibration" collides with MEMBRANE-03 labels in companion docs; PEACE² is the unique federation identifier. |

---

## Health-driven headline (Q2 acceptance)

The page also renders a "live" pill claiming "Connected to arifOS". The current source has no live `/health` wiring. The diff above does **not** add it (separate work — wiring changes the page's render path) but states the canonical rule:

> Headline must follow live `/health`. Render only what `:7072/health` and `:8088/health` say at request time, never a constant.

**Live values to render in the copy box, taken just now:**

```
:7072/health  → A-FORGE-MCP  status=healthy  transport=streamable-http  tools=122/122
:8088/health  → arifOS      status=degraded  (SOT drift warning only — source != built)
```

The MCP site headline should therefore be: **streamable-http, 122 tools, attached to arifOS** — single source of truth, refresh on every page load.

---

## Branch state

- Branch created locally: `site/claude-2026-10-15` (no push, no deploy).
- No file in `public/` was modified. Diff is on disk only.
- F1: backups of touched files would land in `/_to_delete/site-q2-2026-10-15/` if edits proceed.

## MENUNGGU ARIF

- Apply the 5 edits and commit on the existing branch (still local, no push).
- Wire the live `/health` probe into the "Connected" pill — that's a separate render-path change.
