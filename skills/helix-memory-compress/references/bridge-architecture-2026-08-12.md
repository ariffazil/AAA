# Bridge Architecture — Hermes Flat Memory vs arifOS Helix

> **Forged:** 2026-08-12 from live session (Arif: "scan the vps to understand the helix memory architecture")
> **Purpose:** Map the two memory systems so future agents understand what they're compressing and why.

## The Two Systems

### System 1: Hermes Flat Memory (injected, capped)

| File | Cap | Role |
|------|-----|------|
| `~/.hermes/memories/MEMORY.md` | ~6,000 chars | Operational notes — injected to every system prompt |
| `~/.hermes/memories/USER.md` | ~3,000 chars | User profile — injected to every system prompt |

- **Written by:** the `memory` tool (add/replace/remove/operations)
- **Read every turn** — this is why it has a char cap
- **This is what fills up** and triggers "zen memory" requests

### System 2: arifOS Helix Memory (file-based, uncapped)

**H-axis (human significance):**

| Layer | Path | Content |
|-------|------|---------|
| H1 | `/root/memory/H1-capture/` | Raw capture inbox (sovereignty gate) |
| H2 | `/root/memory/H2-experience/` | Lived experience, by month |
| H3 | `/root/memory/H3-knowledge/` | Domain knowledge (geoscience, etc) |
| H4 | `/root/memory/H4-identity/` | Identity docs (AGENT_BRIEF.md, PDFs) |
| H5 | `/root/memory/H5-scars/` | Scar registry (20 scars, 13 narrative .md) |
| H6 | `/root/memory/H6-constitution/` | Scar roots mapped to F1-F13 |

**L-axis (agentic reality):**

| Layer | Tech | Role |
|-------|------|------|
| L1 | Redis `:6379` | Ephemeral session state |
| L2 | Redis `:6379` | Thread context, lane memory |
| L3 | Qdrant `:6333` | Similarity vectors |
| L4 | Supabase (remote) | 25 domain tables |
| L5 | Graphiti `:6380+:8000` | Knowledge graph |
| L6 | VAULT999 `/root/arifOS/VAULT999/` | Append-only sealed receipts |

**Rollup:** `/root/.arifos/scripts/memory-helix-rollup.sh` runs daily 19:00 UTC — consolidates `learned/` → `episodes/`.

**Project memory:** `/root/.arifos/memory/project.md` — canonical federation project memory, read at session start.

## The Gap (as of 2026-08-12)

**No auto-bridge exists between Hermes flat memory and the helix file system.**

- Hermes `memory` tool writes ONLY to `~/.hermes/memories/`
- Helix H1-H6 lives in `/root/memory/` with no char limit
- When Hermes flat memory fills up, the helix has plenty of room — but nothing routes overflow there automatically

## Manual Bridge Procedure

When compressing Hermes flat memory:

1. **Archive to H1** before compressing: write the raw pre-compression content to `/root/memory/H1-capture/YYYY-MM/YYYY-MM-DD-hermes-archive.md`
2. **Note scar candidates** for H5 promotion (entries that reference repeated patterns)
3. **Compress the flat stores** using the batch operations procedure
4. **Keep only highest-signal entries** in Hermes flat memory

## Key Paths (quick reference)

```
/root/memory/ZEN_HELIX.md                              # canonical helix doc
/root/memory/H1-capture/                               # raw inbox
/root/memory/H5-scars/H5_SCAR_REGISTRY.json            # scar registry (20 entries)
/root/.arifos/memory/learned/YYYY-MM-DD.md             # episodic learned
/root/.arifos/memory/episodes/YYYY-MM-DD.md            # daily rollup output
/root/.arifos/memory/project.md                        # federation project memory
/root/.arifos/scripts/memory-helix-rollup.sh           # daily rollup script
/root/AAA/governance/DOUBLE_HELIX_ECHO_SCAR.md         # double helix doctrine
/root/AAA/governance/HUMAN_MEMORY_DOCTRINE.md          # H1-H6 doctrine
~/.hermes/memories/MEMORY.md                           # Hermes flat (capped)
~/.hermes/memories/USER.md                             # Hermes flat (capped)
```

## Cross-Harness Fragments

H-axis data also exists in non-Hermes locations:

| Harness | Path |
|---------|------|
| OpenClaw | `.openclaw/workspace/{ARIF.md,USER.md,memory/*.md}` |
| Claude Code | `.claude/memory/user_arif.md` |
| Codex | `.codex/memories/rollout_summaries/` |
| AAA seed | `AAA/seed/ARIF_FAZIL.md` |
| AAA identity | `AAA/agents/arif-fazil-identity.yaml` |

**Rule:** H-axis fragments in L-axis space. Move only under explicit F13 directive.

---

*Provenance: scanned from live VPS state 2026-08-12. Arif corrected blind compression → architecture scan → this reference.*
