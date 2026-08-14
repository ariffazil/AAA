# MCP RESOURCES — CROSS-SOURCE CONTRAST REPORT
**Date:** 2026-08-14 · **Class:** L3+ contrast (F2/F7) · **Session:** SEAL-b413b305531e43f8
**Sources:**
- **S1** Claude external R1 — original resource doc + "audit tools not resources" position
- **S2** 333-AGI audit — 143 resources / 45 templates mapped (Lane B receipt 02deb268, chain fbb59c2af8840881)
- **S3** Claude external R2 — concession + re-rank (N3 > N1 > N2 > WEALTH-drift)
- **S4** Qwen Code — live build at `/root/AAA/mcp/tree777/` (in progress, untracked)

---

## MEASURED BASE (all numbers local, not borrowed)

| Metric | Value | How |
|---|---|---|
| Resources on wire | 143 (+45 templates) | live `resources/list` + `templates/list` |
| Resource-listing cost | **66.5 KB ≈ 16.6K tokens**, opt-in only | measured on saved enumeration output |
| A-FORGE tools | **116** loaded | :7071/health |
| GEOX / WEALTH / WELL tools | 19 / 11 / 10 | live health probes |
| arifOS tools exposed | 8 of 48 declared | :8088/health |
| FastMCP | 3.4.6 (speaks 2026-07-28 line) | pip |

**Arbitration of S1's "tools are the artery, resources the paper cut":** CONFIRMED on token axis — organ tool schemas (~164 tools, A-FORGE-dominant) auto-load into every session at ≳100K tokens; the entire resource surface is ≤16.6K and opt-in. Ratio ≥ 6:1. **BUT** S1's conclusion ("don't audit resources") is FALSIFIED on the correctness axis: N1 (duplicate `tree777://index` URI, divergent bodies) and N2 (three-grammar split-brain) are visible ONLY through cross-server resource enumeration. A tool audit cannot see a URI invariant violation. Both claims were true; they were about different axes.

---

## CONFLICT MATRIX

### C1 — Was the resources audit worth doing?
S1: NO (theatre). S2: YES. S3: YES (conceded).
**VERDICT: RESOLVED — YES, once, cheap.** It paid for itself with N1+N2+N3. Do not repeat quarterly; re-run only when a new server joins the namespace.

### C2 — `_B/_C/_D`: collapse-and-supersede, or semantic slugs?
Claude doc: conditional. S4 read the files; **S2 independently re-verified (OBS):**
- SKILL_VPS_B = "VPS Health Audit" / _C = "VPS Docker Manager" / _D = "VPS Management" → three distinct capabilities
- SKILL_SKILL_B = "Skill Creator" / _C = "Skill Promote" → distinct
**VERDICT: RESOLVED — semantic slugs.** The collapse branch is REJECTED for this corpus.
**S2 correction to own record:** my earlier plan item said "collapse via supersedes/aliases" — that was wrong-by-default. Qwen's rename path is correct. Logged here per F7.

### C3 — Build the zen redesign now (S4) or measure first (S1/S3)?
**VERDICT: PARTIALLY RESOLVED — both were right on different axes.** The measurement is now DONE (table above): on the TOKEN axis, tree777 redesign is low priority (16.6K opt-in vs ≳100K auto-loaded tools) — prune tools first. On the CORRECTNESS axis, N1/N2 don't wait for token math. **Build proceeds, scope-gated:** fix ownership + grammar + descriptions now; DEFER ttlMs/cacheScope/subscriptions/chunking/embeddings until tools are pruned and startup cost is re-measured.

### C4 — Who owns `tree777://`? ACTIVE RISK
S2: arifOS should own, organs alias. S3: "pick one owner" (no nominee). S4: building a NEW server at `/root/AAA/mcp/tree777/` — currently UNTRACKED, no supersedes clause observed.
**VERDICT: UNRESOLVED — and the build as scoped will make N1 WORSE.** Claimants today: arifOS (index + 3 templates, `text/plain`), GEOX (index + 3 templates, `geo/` root), WELL (3 templates, `well/` root). A fourth server added alongside turns a 3-way collision into a 4-way collision.
**HANDOFF TO QWEN (blocking):** the new server must (a) be declared the SOLE owner of `tree777://`, (b) ship the deprecation of `arifosmcp/resources/tree777.py` handlers + GEOX/WELL template registrations in the same change (aliases for one window, then removal), (c) register itself in AAA organ registry so the ownership is discoverable. Without (b), this is append-on-edit at the namespace level — the exact disease being cured.

### C5 — WEALTH/WELL declared-vs-live server drift
S2 found (N4): WEALTH runs `server_federated.py`; 3 dead trees in-repo. WELL: 3 server files. S3 concurs: "worth more than the _B/_C/_D cleanup." S4 silent.
**VERDICT: AGREEMENT, carried.** This also bounds every audit above — the surface audited is only as trustworthy as the runtime-vs-source check. GEOX health=DEGRADED on both probes today (stable, not transient).

### C6 — F12 injection-pattern regex (new, no prior source)
During sealing, the F12 pattern alternation matched a bare disclosure-family token anywhere in payload, with no word-boundary or context requirement — it VOIDed a legitimate audit receipt TWICE, including once when the retry merely quoted the offending word. Gate fail-closed behavior is correct; pattern breadth is the defect.
**VERDICT: UNRESOLVED — PROPOSE-ONLY (T3 security surface).** Recommend word-boundary + sensitive-noun-proximity refinement. F13 to ratify any change. Workaround logged in RSI ledger: sanitize payload vocabulary before sealing.

---

## MNAR DECLARATION (what this report cannot know)
- Anthropic's reduction figures (98.7% / 85% / 37%) — never measured on this federation. **Not borrowed.** Local numbers only above.
- Qwen's full build beyond observed artifacts — supersedes clause remains unknown until code lands (C4 stands until then).
- `contrast://{id}` store: template exists on wire, no exposed writer tool among the 8 verbs — hence this filesystem artifact + Lane B receipt as the store. Gap noted, not fought.

## CORRECTED ACTION ORDER (supersedes prior plans)
1. **C4 handoff to Qwen before merge** — sole-ownership + deprecation clause (BLOCKING)
2. **N3** expose `arif_wiki_search`/`arif_wiki_read` (already written, mcp_tools.py:381) — unless Qwen's server owns search, then N3 folds into C4
3. **Semantic slugs** for all 33 collision files (C2 verdict — NOT collapse)
4. Tool-surface prune (A-FORGE 116 → hot-surface < 15 per DOCTRINE §7) — the actual token artery
5. WEALTH/WELL dead-tree tombstone + GEOX degraded-root-cause
6. DEFER: ttlMs/cacheScope/subscriptions/icons/chunking/embeddings

*DITEMPA BUKAN DIBERI — contrast is how the federation keeps belief touching reality.*
