# Root Entropy Audit — AAA (Cockpit / A2A Gateway)
> **Generated:** 2026-06-20 22:01 UTC
> **Repo:** /root/AAA | 63 root files
> **For:** Any agent with write access to audit and act.

---

## Quick Hits

### 🔴 DELETE
| # | File | Reason |
|---|------|--------|
| 1 | `entropy-report.json` | Generated artifact. Untracked. |
| 2 | `BOOTSTRAP_MINIMAL.md` | Bootstrap doc — likely one-time use. Review then delete. |
| 3 | `BOOTSTRAP_CONTEXT.md` | Bootstrap doc — likely one-time use. Review then delete. |
| 4 | `FEDERATION_COCKPIT.md` | Content likely subsumed by FEDERATION_CONTRACT.md + AAA_FEDERATION_CONSTITUTION.md. |
| 5 | `SELF_AUDIT.md` | If identical to arifOS root version, delete this copy. If AAA-specific, keep. |

### 🟠 ARCHIVE (historical)
| # | File | Move to |
|---|------|---------|
| 6 | `INIT_PROMPT.md` | `_archive/` (initialization prompt, likely historical) |
| 7 | `NEXT_FORGE.md` | `_archive/` (planning doc — if items are done, archive) |

### 🟡 MERGE
| # | Files | Action |
|---|-------|--------|
| 8 | `AGENTS.md` ↔ `CLAUDE.md` | Likely overlap. AAA has both — audit for duplicate content. |
| 9 | 6× `agent-card-*.json` + `agent-card.json` | 7 agent card files. Consolidate into `AAA_AGENTS_REGISTRY.json`. |
| 10 | `AAA_ADR_002.md` + `AAA_FEDERATION_CONSTITUTION.md` | Both constitutional docs. Audit for overlap. |

### 🟢 MOVE (wrong location)
| # | File | Move to |
|---|------|---------|
| 11 | `CNAME` + `_headers` + `_redirects` + `robots.txt` + `sitemap.xml` + `index.html` + `humans.txt` | → `public/` (Cloudflare Pages / web assets — 7 files) |
| 12 | `TOOL_MANIFEST.json` + `llms.txt` + `llms.json` | → `.aaa/` (generated files — 3 files) |
| 13 | `canonical_schema_contract.json` | → `schemas/` |
| 14 | `federation-profile.yml` | → `config/` |
| 15 | `railway.json` | → `config/` or delete if Railway unused |
| 16 | `components.json` | → `src/` (shadcn/ui config) |
| 17 | `SUBSTRATE_NAMESPACES.md` | → `docs/` |

### 🔵 OBSERVATIONS (not file actions)
- 63 root files — highest among all organs except WEALTH (65)
- `.env` exists at root — verify it's in `.gitignore` and not tracked
- `automation-health.md` — unclear purpose
- `UNIFIED_AGENT.md` — may overlap with AAA_FEDERATION_CONSTITUTION.md

---

*DITEMPA BUKAN DIBERI — Cockpit clarity requires root clarity.*
