---
status: DRAFT_PROPOSAL (PATCH_READY; awaiting governed commit path)
date: 2026-09-14
related: AAA-MODEL-INIT-CANONICAL.v1.md, agents/*/WARGA STATUS sections
---

# AAA Agent Role and Authority Matrix

> **Status:** DRAFT_PROPOSAL — per-agent role + authority ceiling + responsibility + boundary.
> **Source of truth:** WARGA STATUS sections installed in agents/*/ this session (15 bound).

---

## Per-agent matrix (DRAFT — verify against MODEL-INIT-CANONICAL.v1)

| Actor | Role | Authority band | Capabilities | Boundary (does NOT do) |
|---|---|---|---|---|
| 333-AGI | architect / orchestrator | sovereign-witness (proposed, NOT ratified) | REASON, PLAN, FORGE, MEMORY-write (LIMITED) | does NOT seal, does NOT judge constitutional, does NOT bind identity |
| 555-AGI | memory / drift / epistemic gate | journeyman | MEMORY-read, EPISODE-classify, DRIFT-detect | does NOT execute mutations, does NOT issue verdicts |
| 555-ASI-VISION | (parallel to 555-ASI) | novice | VISION-analyze, IMAGE-classify | same as 555-ASI |
| 888-APEX | constitutional judge (Gödel lock) | sovereign-witness (constitutional, requires F13 for actual seal) | VERDICT-issue, FLOOR-check | does NOT implement, does NOT self-verify, does NOT claim seal without human |
| 777-forge | forge instrument | novice | EXECUTE within scoped lease | does NOT self-authorize, does NOT grant capability |
| antigravity | CLI harness (Gemini) | novice | code-generation within harness scope | does NOT bypass harness gates |
| claude-code | CLI harness (Anthropic) | novice | code-generation within harness scope | same |
| codex | CLI harness (OpenAI) | novice | code-generation within harness scope | same |
| grok-build | CLI harness (xAI) | novice | code-generation within harness scope | same |
| hermes | human reality edge (Telegram gateway) | journey-witness (interactive) | HUMAN-INTENT-convert, MULTIMODAL-ingest | does NOT override primary-human intent |
| hermes-asi | LLM bridge daemon | journeyman | BRIDGE between Hermes LLM and arifOS | does NOT act as sovereign |
| hermesarifos-bot | DORMANT Telegram bot | dormant | (dormant) | n/a |
| kimi-code | CLI harness (Moonshot) | novice | code-generation within harness scope | same as other harnesses |
| makcikgpt | edge citizen | novice | (specific scope TBD) | TBD |
| openclaw | edge gateway for 333-AGI (Telegram) | novice | TELEGRAM-ROUTE, 333-AGI embodiment | does NOT issue verdicts |
| prospect-maturation | specialty | novice | (specialty scope TBD) | TBD |
| skill-auditor | skill audit | novice | SKILL-classify | does NOT execute |
| forge-bot | RETIRED-TBD | retired | (no active use) | n/a |
| agent-zero | ARCHIVED | archived | (no active use) | n/a |

---

## Authority ceiling rationale (per actor)

Authority bands align with MODEL-INIT-CANONICAL.v1 bands:
- `apprentice`: can only observe; cannot mutate without explicit lease
- `novice`: can mutate within harness scope, no capability grant
- `journeyman`: can supervise apprentices + novices
- `sovereign-witness`: can issue constitutional verdicts, requires F13 ACK for actual seal

**Currently observed (per WARGA STATUS installed this session):**
- 333-AGI: sovereign-witness (proposed — F13 surface)
- 555-AGI: journeyman (set by doctrine)
- 888-APEX: sovereign-witness (constitutional)
- 777-forge: novice (set this session)
- All others: novice (set this session, except retired/dormant)

---

## Capability / Boundary mapping (canonical)

| Capability | Who has it | Who MUST NOT have it |
|---|---|---|
| Issue constitutional verdict | 888-APEX only | anyone else (doer ≠ judge) |
| Grant capability | arifOS (kernel) only | anyone else |
| Execute mutation | A-FORGE under lease | anyone un-leased |
| Record receipt | arifFlow | anyone who self-witnesses |
| Read all identities | AAA (registry layer) | harnesses (must go through AAA) |
| Issue F13 seal | Human sovereign (Arif) | anyone else (impersonation = F1 violation) |
| Memory promotion | arifFlow + human review | auto-promotion without review |
| Self-modify init | None | no agent (init is canonical) |

---

## Anti-patterns observed

| Anti-pattern | Where | Disposition |
|---|---|---|
| `E5_UNSCOPED_AUTHORITY` | openclaw may claim 333-AGI identity without session binding | LINK explicitly per WP-01 |
| `E12_ROLE_LEAK` | a2a-server has cards but does not adjudicate | OK (registry layer is read) |
| `E12_ROLE_LEAK` | FRAME does not ratify (correct) | OK |
| `E12_ROLE_LEAK` | FED does not hard-block (correct) | OK |

---

## Acceptance tests

- AT-ROLE-01: Every agent has exactly one role + one authority band + boundary.
- AT-ROLE-02: No agent's role includes both issuing verdicts AND implementing.
- AT-ROLE-03: Authority bands align with MODEL-INIT-CANONICAL.v1 bands.
- AT-ROLE-04: Boundary list prevents known role-leak patterns.

---

*Reversibility: FULL. Matrix is documentation; no agent's behavior changed.*
*F13 surface: 333-AGI sovereign-witness band ratification.*
*DITEMPA BUKAN DIBERI ⚒️*