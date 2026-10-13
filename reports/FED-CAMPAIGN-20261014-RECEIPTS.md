# FED REALITY-ALIGNMENT CAMPAIGN — RECEIPTS & FAILURE LEDGER (2026-10-13/14)

**Class:** evidence ledger for reviewable PRs · **Compiler:** FI-008 (kimi-code) · **Acceptance authority:** ARIF alone
**Rule honored:** fix what evidence proves · preserve every failure · no invented declarations · seal only after independent verification (555-ASI queued; nothing here is self-sealed).

## 1. Executed & wire-proven (live)
| Change | Surfaces | Evidence | Rollback |
|---|---|---|---|
| Spend callback v2→v2.3 (HOST_MAP providers; P1.5-B actor resolution: metadata→vk-alias→lane-group→unknown; CONADICTION fail-closed) | A-FORGE/scripts/fed_spend_callback.py | 14/14 host fixtures · **T8 wire row 20:27:36.525Z** `deepseek\|deepseek-flash\|kimi-code/FI-008\|1.0` · bare-no-metadata → honest `unknown` | .bak-v23-20261013T202258Z |
| Governed litellm reload | litellm-federation | pre pid 2074874 → post pid 2091763, ready 20s, healthy 200, canaries 4/4 | container restart w/ bak config |
| MiMo V2.6 migration P1/P2/P3/P6 (333-AGI executed from FI-008 staging) | SOT, fed_router, middleware, AGENT_MODEL_MAP | .bak-20261014-mimo-p16 files · alias rows kept w/ remove_by 2026-10-21T10:00+08 · P4 verified already-applied (20× v2.6-flash fallbacks) | bak files + git revert |
| DeepSeek truth-fix: balance $4.15 (was $1.94/$18.53 contradicting DBs), route_health witness row, eureka E1–E5 | token_bank.db, fed_state.db, AAA eurekas | probe receipts in DB notes (18:36Z/02:57Z) · alias-resolution probe (requested v4-flash → resolved deepseek-flash fp aeb56401) | .bak-20261013T184700Z |
| AAA subagent pool: +deepseek/deepseek-flash, +deepseek/deepseek-v4-pro direct lanes | .kimi-code/config.toml | tomllib parse · hash 4fd2555c… | .bak-20261013T184805Z |
| Hermes: +2 FED-independent DeepSeek direct fallbacks; gateway restarts ×2 clean | .hermes/config.yaml | yaml parse (hermes venv) · 1 proc, NRestarts=0 | .bak-20261013T184805Z |
| mcp.json literal→env swaps ×5 (zai ×4, composio) | .kimi-code/mcp.json | 0 literal patterns post-swap | .bak-envswap-20261013T202258Z |
| Transcript redaction ×36 files (sk-cp literals) | kimi session trees | post-scan 0; backups quarantined /root/.secrets/quarantine/… (0700) — purge after rotation | quarantine dir |
| Skills mesh hygiene: 6 broken + 3 dupe symlinks removed | AAA/skills, .kimi-code/skills | broken links 0 · mesh 942 intact | link list recorded in session + git D entries |
| P5-narrow witness refresh (mimo v2.5 rows: alias→upstream, commercial CONTRADICTED) | token_bank route_health | witness_receipt fi008-T8 | .bak DB |

## 2. Failures & contradictions PRESERVED (not flattened)
- **Option A (P1.5 caller-side hermes rewrite): REJECTED** — would break FED-independent direct lanes (group name sent to provider endpoints = model-not-found) + collapses fallback diversity + inverts "alias never determines actor". Full adjudication: `/root/forge_work/2026-10-14/p1.5-identity-packet/REVIEW-FI008.md`.
- **90,574 historical `openai|unknown` rows: KEPT untouched** (raw ledger preserved; correction = derived view only, not yet applied).
- **MiMo commercial: CONTRADICTED** (portal expired+100.2% ↔ wire serving 200s) — both witnesses recorded in DB witness_evidence; portal verdict = ARIF.
- **fed_state capture claims not reproduced**: lifecycle-classes-in-route_health (DECLARED, not wired), registry "4/30 enriched" (0/21 measured), fixtures 12/12 manifest (unlocated) — recorded in session reports; superseded by P1.5 wire evidence where applicable.
- **Dedup sweep phantom claim** ("kimi minimax-direct removed"): kimi config hash-identical through the window — documented in session adjudication; sweep otherwise confirmed (3/4 surfaces).
- **openclaw.json mtime anomaly** (July mtime vs observed v4-pro→v4-flash change): restore-without-receipt; flagged, unresolved.
- callback_err.log witness (v2.2+) retained; KVM4 RC=7 transient vs later 200 witness: both recorded.

## 3. Not executed (class-gated, honest)
Portal witnesses (MiMo/Qwen/z.ai/MiniMax) · rotations · DeepSeek topup · Ed25519 bootstrap (333-AGI identity) · Option B vk-* key minting (callback step-2 READY) · KVM4 role · MiMo interactive-vs-cascade policy · W2 registries / W3 vocabulary (chron routing_keys contract) · 555-ASI independent verification · 888-APEX judgment · fed-sync to FLOW (post-merge).

## 4. PR discipline
Commits scoped to campaign-attributable files only; other lanes' dirty files left untouched for their owners. No secrets committed (scan: 0 long-literal patterns across all staged files). Live-deployed state = the committed state (no paper/production split). Revert = normal git revert + documented bak paths.

DITEMPA BUKAN DIBERI ⚒️
