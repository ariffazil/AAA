# Survivability Audit — Document Transmission Testing (2026-08-09)

**Protocol:** ARIFOS::M365_COPILOT_KERNEL::v1.1 (Arif-designed, versioned)
**Question it answers:** "If the author disappeared tomorrow, would a capable agent arriving in
2035 reconstruct the same system from the documents alone?"

## Core idea

A documentation set is NOT tested by whether humans can read it. It is tested by whether a
**zero-context agent** — no prior sessions, no tribal knowledge, no AGENTS.md — can reconstruct
the system's meaning and structure from the artifacts alone. This measures TRANSMISSIBILITY,
not quality. "Do not optimize the system. Do not propose features. Measure transmissibility."

## Method (5 phases)

1. **Spawn a zero-context subagent** via `delegate_task` (role=leaf, NO prior context passed).
   CRITICAL: the executor must be genuinely ignorant. A federation-resident agent (OpenClaw,
   555-ASI) is CONTAMINATED — its predictions are memory, not document-fidelity. Only a fresh
   subagent is a valid measurement instrument.
2. **Constrain inputs:** read ONLY the artifacts under test (explicit file list, in order).
   Forbid terminal/network/web_search. Instruct: "answer UNKNOWN if the documents don't cover
   it — never guess." UNKNOWN is honest data ("document failed to teach this"), not failure.
3. **Have it predict** (without probing): organs+ports, authority chain, gates, rules, purpose —
   each prediction CITED to document+section.
4. **Grade vs live reality** (your probes: `curl :port/health`, `ss -tlnp`, live surfaces).
   Pre-register the grading matrix BEFORE the subagent returns (so scores can't be contested).
   Score per category: correct / incorrect / missing / ambiguous.
5. **Survival score 0-10** per transmission category (Identity / Governance / Operational /
   World Model). 10 = survives complete model replacement.

## Two-run design (run #1 vs run #2 delta)

Run the protocol with two input sets to ISOLATE the value of individual artifacts:
- Run #1: identity + constitution + a BROKEN pointer (FEDERATION.md = broken symlink) + README
- Run #2: identity + constitution + the REAL machine canon (canon/federation.json)

Result: run #1 reconstructed soul-without-body (identity/rules perfect, floors UNKNOWN);
run #2 reconstructed skeleton+law (all 8 organs + ports + postures, 13 floors with one-liners,
doctrine). The delta IS the measurement: one correct pointer converts "soul without body" →
"soul with skeleton and law".

## Findings pattern (what to look for)

- **Transmission failures are POINTERS, not content.** The content (federation.json + .well-known
  + machine/map.json) transmitted at ~95% fidelity; the failures were: FEDERATION.md broken
  symlink (named path resolves to nothing), HERMES port stale in BOTH README and the machine
  canon (8644 vs live 18089/18789) — a false operational fact measured TWICE by two independent
  subagents. A doc that is confident, coherent, and wrong is the dangerous case: an agent will
  connect to the dead port and fail.
- **Name ≠ content.** `canon/FEDERATION` doesn't exist; `canon/federation.json` does. Protocol
  writers name paths from memory; reality lives where the file actually is.
- **Oral tradition is measurable.** Operational gates (T3: rm -rf, DROP TABLE, money) and the
  deploy contract lived ONLY in AGENTS.md — not site-crawlable. A tool-injected AGENTS.md snippet
  surfaced in BOTH subagent runs (the read tool auto-attaches subdirectory AGENTS.md context) —
  an accidental side-channel that improved transmission. Flag it: survival partly depends on
  tooling side-effects, not the artifacts.
- **Site-level agent surfaces that exist** (.well-known/agent.json, capability.json,
  identity.json, webmcp.json, llms.txt, machine/map.json, 999/verify) transmit the world model
  in machine-readable form — a crawler arriving in 2035 gets MORE than the canonical files.

## Epistemic discipline

- Every prediction graded as correct/incorrect REQUIRES a live probe as ground truth (OBS).
- Incorrect predictions that trace to the DOCUMENT (not the subagent) = drift findings.
- The subagent's own honesty (reporting "file not found", flagging tool-injected leaks) is part
  of the data — an honest UNKNOWN beats a confident guess.

## Reusable command skeleton

```bash
# Spawn (delegate_task): goal = "Read exactly N files: <paths>. WITHOUT probing, predict:
# organs+ports, authority, gates, rules, purpose. Cite every claim. UNKNOWN for gaps."
# context = "You are the SUBJECT of a measurement. No terminal/network/other files.
# UNKNOWN = honest data, not failure. Answers graded vs live state."

# Grade vs live:
for p in 8088 7071 7073 3001 8081 18082 18083; do curl -sf localhost:$p/health >/dev/null && echo "$p up"; done
curl -s https://<site>/.well-known/identity.json | head -c 300   # machine identity
curl -s https://<site>/999/verify                                # seal chain truth

# Pre-registered matrix: category | live truth | prediction | verdict (TEPAT/SALAH/UNKNOWN)
```

## Output shape

Reconstruction summary (Phase A, per-item confidence) → Prediction fidelity report (B+C) →
Memory gap report (D: taught well / implied-not-stated / likely misunderstandings / oral
tradition / drift risks) → Survival scores (E) → Direct evidence-based answer to the
survival question.
