# EUREKA — SystemPrompt Core × arifOS Federation: Dialectic Contrast Distillation

> **Status:** DRAFT_AWAITING_F13 (2026-10-21 · FI-008)
> **Source:** https://github.com/systempromptio/systemprompt-core @ `b400079b6bb4b7efd89cce3e44c3a46255370874` (probed live 2026-10-21, clone at /tmp/systemprompt-core)
> **License warning (F13-class):** BSL-1.1 (BUSL-1.1) — source-available, **evaluation/non-production only**; production needs a commercial license; converts to Apache-2.0 four years post-publication. **All adoption below is clean-room idea transfer, never code copy.**
> **Kin:** Representation≠Reality · HUMA Edge Reality Bridge · Proxy-Reality Paradox · Scar-2026-10-03-002 · Scar-2026-10-02 (session_actor_mismatch)

---

## 0. What was ingested (compressed)

SystemPrompt Core = a **Rust governance library** for a control plane: identity (OAuth2/OIDC/WebAuthn), an Anthropic-compatible model gateway (`/v1/messages`), governed MCP tool execution + hosted A2A agents, policy enforcement (scope checks, secret scanning, blocklists, rate limits), and correlated audit in PostgreSQL 18+. Extensions register at **compile/link time** via the `inventory` crate into one trusted process. 43 workspace crates, edition 2024, nightly toolchain pinned, ~monthly release cadence, 22,864 test functions + 11 fuzz targets. **Intake audit verdict: README tracks source unusually tightly** — every capability claim located at its cited path; the doc even volunteers its own negative facts. Three drifts found: changelog 0.71.0 ahead of tag 0.70.0 (present tense ≠ released state), README says extensions provide "model providers" (trait has tool providers only — model routing is manifest config), README says "Rust 1.96+" (repo actually pins nightly).

---

## 1. The Dialectic — THESIS / ANTITHESIS / SYNTHESIS

| Axis | THESIS — SystemPrompt Core | ANTITHESIS — arifOS Federation | SYNTHESIS — what survives |
|---|---|---|---|
| **Governance shape** | Compiled monolith: policy rules in-process, `evaluate(&PolicyContext) -> Decision` | Constitutional federation: separate organs (arifOS law/Python · arifFlow flow/Rust · A-FORGE hands/TS), floors F1–F13 | Both converge on **pre-dispatch evaluation with an explicit Decision**. Ours adds the verdict grammar theirs lacks (SEAL/HOLD/SABAR/VOID vs allow/warn/deny/pending) |
| **Audit** | Postgres `governance_decisions` — **append-only enforced at the DB grant layer** (UPDATE refused even to owner), `act_chain` JSONB, `trace_id` as its OWN key (never overloads `session_id`) | VAULT999 immutable ledger + hash-chained receipts (`previous_receipt_hash`), JCS canonical bytes (RFC 8785) | Their mechanical enforcement > our convention. Their `trace_id` separation solves a bug class we already carry a scar for |
| **Extension model** | Compile-time `inventory` registration; startup validates dependency graph + reserved API paths | Runtime MCP federation; process isolation where needed; skills/knowledge indexes | Compile-time trust is compact and drift-free **inside** one boundary; process isolation is required **across** trust boundaries. Both true; boundary choice is the design act |
| **Enforcement** | Record-then-block: DecisionAudit always lands BEFORE the 403; fail-closed (429/503); `require_approval` = the only `Decision::Pending` | Fail-closed advisory gate in arifFlow; 888_HOLD as the pending-human class | **Pending ≠ Deny** as a first-class distinction — we already have it (HOLD). Their pattern confirms it is the correct primitive |
| **Credential boundary** | Secrets to child-process env (`env_clear()` + inject), never model context; `secret_scan` policy rule denies on secret patterns in tool args | Mail-gateway token custody (uid 977, unix socket, AppArmor) — same principle, one surface only | The principle generalizes: **credentials reach processes, never model context, on EVERY tool surface** |
| **Trust honesty** | Threat model volunteers negatives: "a model gateway alone cannot govern every action on a laptop", no RLS/tenant isolation, tool outputs trusted | Declared-vs-observed (arifFlow AGENTS.md §4), Representation≠Reality, HUMA intake audit | Independent convergence on the same epistemic discipline — external corroboration of our doctrine |
| **Failure discipline** | 22,864 tests, fuzz tiers, property/contract suites, per-crate CHANGELOG enforced by CI | "Safety is emergence" (F13 2026-10-18) | Their test mass is the mechanical half of our doctrine: safety as engineered artifact, not performed fear |

## 2. Eureka insights distilled (E1–E7)

- **E1 — `trace_id` must be its own key.** SPC never overloads `session_id`; enforcement sites without a session still correlate via `trace_id` + `CallId`. Our Scar-2026-10-02 (`session_actor_mismatch`) is the same disease: an overloaded identity key. **Rule: correlation identifiers get their own column; identity keys never double as correlation keys.**
- **E2 — Append-only must be mechanical, not declared.** `governance_decisions` refuses UPDATE at the grant layer, for every role including owner. Our "immutable" surfaces rely on convention + hash chains. **Rule: any surface we call append-only must enforce it at the storage layer, not the application layer.**
- **E3 — Record-before-block.** SPC writes DecisionAudit then returns 403. A denied action still leaves a trace. Anti-shadow by construction: refusals are events, not absences. **Rule: every deny/HOLD path emits its record first.**
- **E4 — Pending is a verdict class, not a soft deny.** `require_approval` → `Decision::Pending` is the only producer; distinct from deny. Mirrors 888_HOLD. External confirmation that HOLD-as-primary is the right primitive (kin: A-Z Doctrine).
- **E5 — Negative facts are first-class documentation.** Their threat model names what the gateway CANNOT govern. Combined with their intake drifts (changelog-ahead-of-tag), it restates our law: present tense is a claim; a negative needs the same warrant as a positive.
- **E6 — Startup dependency-graph validation.** `ExtensionRegistry::validate_dependencies()` topo-sorts and rejects reserved path collisions at boot, not at first call. Apply to our own registries (skills federation manifest, organ graph): **validate the graph when the system starts, not when the failure happens.**
- **E7 — License boundary is a governance surface.** BSL-1.1 evaluation-only means: ideas yes, code no. Any future production use of SPC itself = F13-class licensing decision, not an engineering decision.

## 3. Alignment actions (proposal tier — not executed)

| # | Action | Tier | Rationale |
|---|---|---|---|
| A1 | Audit our Postgres-backed surfaces (FED, CHRON, a-forge) for append-only-at-DB and trace_id-vs-session_id conformance | T1 reversible | Closes E1/E2 mechanically |
| A2 | Secret-pattern scanning as a policy rule in mcp-governance-interceptor's policy.rs (when built) | T2, clean-room | Closes a real gate gap; interceptor is source-only today |
| A3 | Startup graph validation for skills_index.federation.json organ roots | T2 | E6; cheap, catches registry drift at boot |
| A4 | If SPC is ever evaluated operationally: budget for commercial license first | F13-class | E7; no engineering shortcut exists |

## 4. Epistemic labels

- Workspace/crate/test facts: **OBS** (probed at HEAD b400079b)
- Contrast verdicts: **INT** (interpretation of two observed systems)
- Alignment actions A1–A4: **SPEC** (proposals, unratified)
- The thesis/antithesis frame is a reading aid, not a measured structure.

---
DITEMPA BUKAN DIBERI ⚒️ · Distilled by FI-008 · awaiting F13 ratification
