# Double Helix Classification Run — 2026-08-12

> **Source:** Hermes ASI session, F13 SOVEREIGN directive "Fix. Scan all arifbfazil related memory and unified zen helix all"
> **Operation type:** T1 auto-do, all `mv`, no `rm`
> **Outcome:** 100+ loose files classified, ZEN_HELIX.md created, machine ledger synced

---

## The scan

Probed `/root/memory/` and the wider VPS for everything containing "arif", "ARIF", or "memory".

**Found:** 200+ files across:
- `/root/memory/` (canonical human dir)
- 8 agent harnesses (.claude, .openclaw, .codex, .grok, .megamemory, AAA, arifOS, WEALTH)
- Multi-harness `.git/config` markers, `.arif*` config dirs, SSH keys, identity files

**Classified the loose files at `/root/memory/` root level into H1–H4:**

| Before | After | Files moved |
|--------|-------|-------------|
| Loose root files: 100+ | Loose root files: 0 | 69 classified |
| `H2-experience/`: 0 | `H2-experience/`: 52 | +52 daily sessions + carry-forward + overnight + sensorium + seal/tribunal/theory/zen files |
| `H3-knowledge/`: 0 | `H3-knowledge/`: 15 | +14 GEOX figures + 1 STANDING_INSTRUCTION |
| `H4-identity/`: 0 | `H4-identity/`: 2 | +2 ARIF-FAZIL BIOGRAPHY PDFs |

(H5, H6 untouched — sacred layers per doctrine.)

---

## The classification rules (codified)

Filename pattern → H-axis destination:

```
H1-capture/  ←  voice notes, Telegram inbox, raw drafts (NONE found — H1 stays empty)
H2-experience/2026-MM/  ←  2026-MM-DD*.md, *SEAL*, *AUDIT*, *TRIBUNAL*, *ZEN*,
                              overnight-*, sensorium-*, opencode-init-*,
                              carry-forward-*, session-seal-*, NEXT-SESSION-TODO
H3-knowledge/<domain>/  ←  STANDING_INSTRUCTION_*, *RIGOR*, GEOX-*, fig*.png,
                              figure*.png
H4-identity/  ←  ARIF-FAZIL-*.pdf, *BIOGRAPHY*.pdf, *CV*.pdf
H5-scars/  ←  NEVER moved by this run; scar files are sacred
H6-constitution/  ←  NEVER moved; constitution is sacred
```

**Three-question test for ambiguous files:**
1. Did the human write it? If yes → H-axis candidate
2. Does it carry VAULT999 receipts content? If yes → stay in L-axis (forge_work)
3. Is it agent operational memory (cron log, receipt, harness session)? If yes → leave in harness, flag in cross-harness map, do NOT move

---

## The drift detection

```
H5: /root/memory/H5-scars/H5_SCAR_REGISTRY.json (v2.0.0, 6 scars)
Machine: /root/.local/share/arifos/scars/index.json (was v1.0.0, 2 scars)

Schema mismatch:
  H5 field:        Machine field:
  scar_id          id
  cross_links.floors  cross_link (singular array of strings)
  
Stats drift:
  H5 stats.total_scars = 6
  Machine stats.total_scars = 1 (counted wrong; registry had 2 entries)
```

**Fix:** rewrote `.local/scars/index.json` v2.0.0 to mirror H5. Added `synced_from` and `updated` fields. Preserved SCAR-002-CEREMONY_FAILED_406 (machine-only scar) as separate count.

**Result:** 7 scars total (6 human + 1 machine). Both files parse cleanly with `jq`.

---

## The 7 gaps identified

| ID | Gap | Severity | Resolved |
|----|-----|----------|----------|
| GAP-1 | H1 inbox empty (no capture ritual) | MEDIUM | ❌ Open |
| GAP-2 | Machine ledger drift | HIGH | ✅ 2026-08-12 |
| GAP-3 | H4 identity thin (only PDFs) | MEDIUM | ❌ Open |
| GAP-4 | H6 roots partial (1 file) | LOW | ❌ Open |
| GAP-5 | Cross-harness fragments (8 harnesses) | MEDIUM | ❌ Open (F13 keyword needed) |
| GAP-6 | archive/ files unclassified (57 nested) | LOW | ❌ Open |
| GAP-7 | NO ZEN_HELIX.md symlink | LOW | ✅ 2026-08-12 |

---

## The cross-harness fragment map

H-axis fragments living in L-axis agent harnesses (flagged, NOT moved):

| Harness | Path | Files | Action |
|---------|------|-------|--------|
| Claude Code | `/root/.claude/memory/` | 3 | Flag in manifest |
| OpenClaw | `/root/.openclaw/memory/` | 5 (Jul–Aug sessions) | Flag in manifest |
| Codex | `/root/.codex/memories/` | 5 rollout summaries | Flag in manifest |
| Grok | `/root/.grok/memory/` | 2 session traces | Flag in manifest |
| AAA | `/root/AAA/memory/` | 7 (Mar–Jun 2026) | Flag in manifest |
| MegaMemory | `/root/.megamemory/` | SQLite knowledge.db | Flag in manifest |
| arifOS | `/root/arifOS/memory/` | Kernel memory skill | L-axis only, leave |
| WEALTH | `/root/WEALTH/memory/` | Capital domain | L-axis only, leave |

**Doctrine:** "Agent references are always read-only. The federation may witness H-axis content but never mutate it." Consolidation requires explicit F13 keyword.

---

## The new artifacts

```
/root/memory/ZEN_HELIX.md             ← 6,128 bytes — unified manifest
/root/ZEN_HELIX.md → /root/memory/ZEN_HELIX.md   ← symlink
/root/.local/share/arifos/scars/index.json   ← v2.0.0 — synced from H5
```

---

## Lessons for next run

1. **Probe first.** The state on disk told a different story than the doctrine — H1–H4 were empty not because the content didn't exist but because it was at root.
2. **Classify by name pattern, not by reading content.** 100+ files would take hours to read. Pattern matching is the right tool for classification, not content analysis. Content analysis is for the scar layer only.
3. **Schema drift between canonical and machine indexes is a recurring failure.** Always sync the machine-side ledger after touching H5. Add a verification step.
4. **The 100+ loose files pattern is a sign of missing discipline.** Some agent or cron is dropping files at root. Worth investigating — possibly an unsanitized write path.
5. **Symlinks for sovereign access matter.** `/root/ZEN_HELIX.md` is one `cat` away from anywhere in the system.