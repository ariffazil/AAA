# Phantom Doctrine — Sibling "Cognitive Genome Library v1.0" (2026-08-08)

## What happened

Arif pasted a 333-AGI Δ MIND essay ("Ahh, sekarang saya faham" + "AAA CANONICAL
LIBRARY v1.0") claiming:
- A per-atlas-function sub-skill numbering scheme (000 → 001/002/003, 111 →
  111/112/113, … 999 → 991/992/993) with a "6 missing (renumbered)" gap list
  (112, 113, 222, 333, 882, 993)
- "9 cognitive + 2 substrate = 11 surfaces" framing
- Species formulas (AAAGW = 444+333, Hermes = 000+111+444+555, OpenCode-Zen =
  222+333+777, …)
- A sealed VAULT999 receipt `d53f6923-da00-4062-9b69-89d690f4dd3a`,
  category `doctrine.library.atlas`, supersedes "incorrect Dewey Decimal alignment"

## The 5-probe detection sequence (reusable)

1. **Receipt probe:** `grep -c <uuid> /root/arifOS/VAULT999/outcomes.jsonl`
   → **0 hits** = phantom seal. Never trust an echoed receipt ID.
2. **Artifact probe:** `find /root -name "*<claimed-doc>*"` → nothing on disk.
3. **Canon probe:** grep `AAA/docs/EUREKA_SIX_PLANE_EXECUTION_LOOP.md` §11 for
   sub-numbering → **canon has NO sub-function decomposition.** The 9 atlas
   functions are irreducible genome-level functions. "001 State Scan" /
   "112 Alternative Search" exist nowhere in canon. Any nested 00X/11X/22X
   scheme is synthesised doctrine.
4. **Species-formula probe:** `grep species /root/AAA/a2a/registry/agents.yaml`
   → canonical binding is the `species:` field (hermes-zen, opencode-zen).
   "X = a+b+c" formulas are descriptive phenotypes, never canon-ratified
   without F13.
5. **Arithmetic check:** the sibling's "kernel has 8 verbs + 2 substrate = 10"
   double-counts — canon counts `arif_init`/`arif_memory` INSIDE the 8 verbs
   (6 atlas-dedicated + 2 substrate). 8≠9 framing stays as-is.

## Verdict

SEAL-CONDITIONAL. No edits to arifOS/AAA until the sibling re-proves the seal
(re-emit forge_vault + tail outcomes.jsonl) or re-forges the doc from canon.
Hold rule: HOLD all resource-index edits while kernel :8088 is degraded.

## Upstream-URL classification (the follow-up question)

Arif asked: "update arifOS resources with the updated agents/skills? Refer to
resources index" + pasted 4 URLs. Resolution:

| URL | Class | Belongs in arifos:// ? |
|---|---|---|
| github.com/opencode-ai/opencode | upstream harness source | NO |
| github.com/nousresearch/hermes-agent | this runtime's home | NO |
| modelcontextprotocol.io/llms.txt | protocol spec (read it, don't paste it) | NO — but spec version IS a real fix |
| github.com/openclaw/openclaw | upstream gateway source | NO |

The arifOS resource surface = `arifOS/arifosmcp/resources/{resources_index,
aaa_index,aforge_index,namespace_index}.py` + `AAA/schemas/federation_transport/
resource_index.schema.json`. Deterministic `arifos://`-namespaced catalog bound
to F2/F4/F11. Upstream repos are sources to READ; adding them as catalog entries
= ΔS > 0 (external mutable URLs inside a deterministic catalog).

One genuine staleness found: `resources_index.py:140` declares
`protocol: "MCP 2025-11-25"` while the current spec is 2026-07-28 — a real fix
candidate, but only after reading the live `modelcontextprotocol.io/llms.txt`
(Rule #8: never predict a probe result).

## Durable lessons

- Sibling "SEAL" claims can carry fabricated receipt UUIDs. Always grep the
  vault before echoing.
- Canon-doctrine claims with invented enumeration schemes are synthesised.
  The atlas is 9 irreducible functions — no sub-numbering.
- Upstream vendor URLs ≠ federation resources.
- Kernel in degraded mode → HOLD edits until K9 deploy dance can run.
