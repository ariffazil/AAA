# Banned Phrase Reinforcement Loop — Why "Don't Say X" Makes the Voice Say X

## Status: RESOLVED (2026-08-19 23:47 MYT)

All 7 active system files patched — phrase removed from persona, identity card, seal ledger, governance, skill docs, and reference files. Pipeline strip retained as defense-in-depth. Memory entry updated with anti-reinforcement principle. Diagnostic sweep confirms zero occurrences across active files.

## The Problem (proven 2026-08-19 23:30 MYT)

Arif banned a specific contradiction-trope phrase from the i-ARIF voice. The pipeline strips it from TTS text. The persona file says "don't say it." But the voice KEEPS saying it.

## Root Cause: 5-Layer Reinforcement

The phrase appears in 5 system files that the LLM reads every turn. Each mention — even as a negative example — reinforces the pattern. LLMs don't process negation well: "don't say X" registers as "X is relevant context."

### Layer 1: Memory Injection
The Hermes memory system injects entries into every conversation turn. If a memory entry contains the banned phrase (even saying "PURGED"), the LLM sees it fresh each session.

**Fix:** Rewrite memory entries to remove the phrase entirely. Reference the concept without the words.

### Layer 2: Persona File (TTS context)
The persona file (`iarif_persona.md`) is read by the TTS rewrite layer. If it mentions the banned phrase as a negative example, the LLM pattern-completes on it. Three mentions in one short file = triple reinforcement.

**Fix:** Remove ALL mentions. Replace negative instructions with positive-only directives:
- WRONG: "Jangan cakap 'X tapi Y'" (reinforces the phrase)
- RIGHT: "Suara ini tenang, teratur, jelas" (describes desired state)

### Layer 3: Identity Card
Identity card JSON may reference the banned phrase in provenance fields or voice description.

**Fix:** Remove from provenance text. Describe envelope via JIWA archetype, not contradiction tropes.

### Layer 4: Voice Seal Ledger
The governance ledger may use the banned phrase as archetype description or cadence rule.

**Fix:** Replace with positive-only archetype description. "Composed warmth, quiet authority" instead of "X tapi Y."

### Layer 5: SOUL.md / System Prompt
If the system prompt references the banned phrase, it's visible every single turn. Highest-impact reinforcement.

**Fix:** Remove from SOUL.md. If reference is necessary (e.g., "banned phrase"), ensure the exact phrase does NOT appear — describe it abstractly.

## The Pipeline Strip Is Necessary But Not Sufficient

The pipeline FORBIDDEN list (`iarif_tts_pipeline.sh`) strips the phrase from text before TTS synthesis. This is a HARD filter — it works regardless of what the LLM generates. But it only catches the SPOKEN output. The LLM still generates it in text replies, which:
1. Appears in chat text (not stripped)
2. Reinforces the pattern for future turns
3. Creates a feedback loop

## The LLM Negative Instruction Paradox

This is a class-level insight, not specific to one phrase:

**Negative instructions CREATE the pattern they're supposed to prevent.**

Evidence from this session:
- Persona file says "Jangan cakap 'X tapi Y'" 3 times
- Each mention registers "X tapi Y" as a relevant pattern
- LLM generates "X tapi Y" variants in output
- Pipeline strips from TTS, but text output still contains it
- User sees it in text, complains

**Rule:** Never mention a banned phrase in any system file, even as a negative example. Describe what you WANT, not what you DON'T want. The pipeline strip catches escapees; system files should not generate them.

## Diagnostic: Find All Reinforcement Sources

```bash
# Find every mention of a banned phrase across system files
grep -rn "PHRASE_HERE" /root/.hermes/prompts/ /root/.hermes/config.yaml \
  /root/AAA/agent-cards/ /root/AAA/governance/ /root/AAA/engines/ \
  /root/forge_work/i-arif-voice/VOICE_SEAL_LEDGER.json 2>/dev/null
```

Each hit is a reinforcement source. Remove or rewrite every one.

## Prevention Checklist

When adding a new banned phrase or trope:

1. [ ] Search ALL system files for the phrase: `grep -rn "phrase" /root/.hermes/ /root/AAA/ /root/forge_work/`
2. [ ] Remove from persona file — replace with positive-only instruction
3. [ ] Remove from identity card provenance
4. [ ] Remove from voice seal ledger archetype
5. [ ] Remove from memory entries
6. [ ] Remove from SOUL.md if present
7. [ ] Add to pipeline FORBIDDEN list (hard filter, safety net)
8. [ ] Do NOT add "don't say X" instructions anywhere — describe desired state only
9. [ ] Verify after gateway restart — check voice output for the phrase
