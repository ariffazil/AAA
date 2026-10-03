---
type: F2_RECEIPT (post-aggregate drift closure)
date: 2026-10-03
operator: kimi-code/FI-008 (read-only witness lane)
session: SEAL-261a6622cc354edc
trigger: Witness closure (T1) measured live SKILL.md ≠ FINAL aggregate hash; this receipt closes the chain
---

# RECEIPT — forge-fastmcp v3.2.0 post-aggregate drift closure

## Measurement (this session, 2026-10-03 ~14:40 UTC)

| | Claimed (V3_2_0_FINAL aggregate) | Measured live |
|---|---|---|
| SHA256 | `08e22d55a448fc3d553e9ac862dd1dae4f03b984431ba70cbfcaeaf90ff27ed0` | `6da4ee9131ab208e774ce51ab6468555ac1665aa3517a4cc79729b137e5d10c4` |
| Bytes | 52,599 | 55,203 |
| Lines | 849 | 876 |

Delta: +2,604 B / +27 lines. Live + frozen mtimes identical: 2026-10-03 21:01:12 +0800 (same minute as receipt writes — the edit and the receipts landed together; the aggregate hash was never refreshed).

## What the 27 lines are (DER — marker-based, not byte-proven)

- OBS: live file contains `### 2f — Surface-truth falsification recipe (NEW 2026-10-03, T-007…)` at L354 and `### 2h — 3-layer namespace enumeration (NEW 2026-10-03, T-007-extended…)` at L382.
- OBS: **no Stage 2g exists** — the "payload hygiene audit" section that RECEIPT_KERNEL_PAYLOAD_LEAK listed as "Forthcoming Stage 2g doctrine patch" is still absent; numbering skips 2g.
- OBS: changelog last entry remains v3.2.0 (L874) — the 2h addition has **no changelog entry**.
- DER: prior receipts recorded 2f as APPLIED pre-aggregate (PATCH-D-001 ✅) and 2h as "⏳ to apply next" — so the post-aggregate delta ≈ the Stage 2h section (+ possibly 2f refinement).
- UNKNOWN (honest): exact byte attribution. The 08e22d55 content is preserved nowhere — no frozen copy, and `/root/AAA` git tracks only an 11 KB skills-cold variant (`skills-cold/.frozen/2026-09-20-mcp-consolidation/restored-by-convergence-pass/forge-fastmcp/SKILL.md`, HEAD `26eaec7c…`, 11,091 B). The live `/root/.claude/skills/forge-fastmcp/SKILL.md` is untracked by any repo found this session. Byte-diff therefore impossible; identification rests on section markers + receipt status, which is consistent but not byte-proof.

## Verdict

- Drift **explained**: documented doctrine patch (Stage 2h), not corruption, not attack.
- Receipt chain now **closed**: `091ffcfaf…` (frozen) → `c4a956b4…` → `b95ed9d4…` → `08e22d55…` → `6da4ee91…` (this receipt).
- Two bounded cosmetic gaps remain: (1) 2h lacks a changelog entry; (2) 2g is promised-but-absent — the same phantom-citation class the aggregate already caught once. Apply or strike it.
- Promotion binary (F13 → Arif): **RIPE** — promote v3.2.0 canonical at `6da4ee91…`, or hold at SABAR.

## Self-audit

All hashes measured this session (sha256sum + wc). No unprobed tool name cited. Session SEAL-261a6622cc354edc, read-only except this receipt.

DITEMPA BUKAN DIBERI ⚒️
