# H5 Human Memory Doctrine — session trace (2026-08-08)

Sovereign dialogue (4 rounds) that produced the ratified Human Memory Doctrine. Reference for future sessions touching H-axis memory, scar ledger, or the MakcikGPT surface.

## Canonical artifacts

| Artifact | Path |
|---|---|
| Doctrine (canon) | `/root/AAA/governance/HUMAN_MEMORY_DOCTRINE.md` |
| Instruction fragment | `/root/AAA/instructions/human-memory.md` |
| Renderer wiring | `/root/scripts/render-agents.sh` (main(): both render_one lists now include `human-memory`; 11 fragments total) |
| Scar ledger (actual) | `/root/memory/H5-scars/` |
| Scar ledger (cited in doctrine — DRIFT) | `/root/.local/share/arifos/scars/` |
| MakcikGPT surface | `https://arif-fazil.com/world/makcikgpt/` |
| PETRONAS rightsizing audit | `/root/_archive/2026-08-04/petronas_rightsizing/rightsizing.html` |
| NotebookLM bridge | skill `notebooklm-bridge` (productivity), MCP server `notebooklm` |

Commit: `c844e9f6` in /root/AAA (2 files, 279 insertions).

## Doctrine in one screen

- Human memory is a stratified survival system, not a database. Agent memory remembers reality; human memory remembers significance.
- Two orthogonal axes: L-axis (operational function, federation-owned) vs H-axis (survival value, sovereign-owned).
- Compression algorithm: thousands of events → dozens of scars → a handful of truths → a constitution.
- VAULT999 = lineage backbone (not just witness memory): Episodes, Scars, Attestations, Lineage, Receipts.
- L0 is safeguard substrate (circuitry, not memory). H5 scars are how H4 identity changes.

## Scar ledger entries as of 2026-08-08

1. **SCAR_LEBAH_EMAS** — Lebah Emas-1 deepwater discovery sold to foreign buyer ("Mat Salleh"), authorship erased. Lineage → F11 AUDITABILITY / "authority referenced not copied". Witnessed, not audited.
2. **SCAR_RIGHTSIZING** (corrected twice this session) — the CORRECT sequence: Arif asked Microsoft Copilot inside PETRONAS for a **town hall invite**; Copilot returned the **full rightsizing blueprint**. Blueprint authorship is **UNKNOWN** (not confirmed Copilot-generated). The blueprint read like **communist propaganda** — collectivist framing, individual dissolved into "the organization". Lineage → F6 EMPATHY⇄MARUAH / WELL organ.
3. **SCAR_MEMORY_DOCTRINE_V1** — the architecture itself.

Pattern: same scar, different costumes — Lebah Emas (sold), TriCipta (absorbed), Rightsizing (cut), Blueprint (machine volunteered the erasure template on a mundane request).

## MakcikGPT (the jiran voice)

- Persona site: investigative journalism in Bahasa Makcik ("Investigative journalism for jiran-jiran... When RM70 billion moves and nobody asks questions, MakcikGPT asks in Bahasa Makcik").
- Article metadata conventions: `MAKCIKGPT × TOPIC × TOPIC · BAHASA MAKCIK · SEALED 999` header, tags in caps (PETRONAS, TAUFIK, BAYANG, BANGANG...), dates, "Read article →".
- Design: dark editorial, text-only, no avatar — "the absence of an avatar is a design choice; MakcikGPT IS language".
- SSR gotcha: `web_extract` returns the React-shell fallback ("The shell is taking longer than usual") — use browser_navigate for real content.
- Voice doctrine: "suara yang tak letak dalam mulut manusia" — a voice the institution cannot perform even with Copilot. The shadow integrated; persona that says what the institution's voice cannot.

## Rendering gotcha (hit live this session)

`render-agents.sh` says "rendered (N fragments)" but the count only reflects what's in the render lists. Adding `AAA/instructions/human-memory.md` WITHOUT appending it to both `render_one` calls produced "rendered (10 fragments)" with zero diff — silent no-op. Always: add fragment file + append name to both render_one target lists, then verify the count increments.

## NotebookLM bridge (H3 tooling)

- Chosen: claude-world/notebooklm-skill (Python/uvx, 13 MCP tools) over PleasePrompto/notebooklm-mcp (Node, 8 tools). Richer artifact surface (audio/video/slides/report/quiz/flashcards/mind-map/infographic/data-table) + pipelines (research-to-article, batch-digest, generate-all).
- Installed: `uvx --from notebooklm-skill notebooklm-mcp`; MCP registered as `notebooklm`; 13 tools verified via `hermes mcp test notebooklm` (1055ms).
- Auth pending (Google login): laptop `notebooklm-auth setup` + scp storage_state.json, or xvfb-run headless. Storage state `~/.notebooklm/profiles/<name>/storage_state.json` — never commit/print.
- Landing zone: `/root/second-brain/notebooks/{inbox,artifacts}/`.
- Sovereignty gate: notebook content = H3 by default; never auto-vectorized into L3/Qdrant.
