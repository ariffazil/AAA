# Question Categories — Lawful vs Unlawful, With Worked Examples

The Question Budget law limits human-facing questions to five categories. This file
shows worked examples so the next session can pattern-match.

## The five lawful categories

### 1. Authority

The agent is about to mutate state that the agent cannot mutate without an envelope.

```
LAWFUL: "Aku jumpa two patches — one edit /root/AAA/canon/foo.md, satu edit
        /root/.hermes/config.yaml. Yang kedua restart gateway. Confirm both boleh
        proceed?"

UNLAWFUL: "Can I have permission to make changes?" — too vague, not a single decision,
          the human cannot say yes/no cleanly.
```

### 2. Preference that cannot be inferred

The agent can read MEMORY/USER but the taste / identity / recipient is unnamed.

```
LAWFUL: "Voice mana untuk TTS — V8 Nusantara atau V9 i-ARIF? Budget ada untuk V8
        je; V9 ada quota."

UNLAWFUL: "Apa tone kau nak aku pakai dalam email ni?" — the agent has the tone
          doctrine in user profile; load USER.md and default.
```

### 3. Values

The decision depends on what the human holds as load-bearing.

```
LAWFUL: "Banner dah 19/9 — kau nak register domain dulu atau jalan dengan subdomain
        first?" — pace vs money, the user picks.

UNLAWFUL: "Patut ke aku focus benda ni?" — the human has already decided by asking.
          The agent asking back is whiff-of-failure.
```

### 4. Irreversible risk

Paid boundaries, real-world blast radius, public surface, deletion of sealed canon.

```
LAWFUL: "Aku jumpa file yang protected_instruction_files flag off — confirm
        proceed dengan edit sebelum aku run?"

UNLAWFUL: "Should I be careful about this?" — the language is generic, the test is
          not. The question must name the consequence.
```

### 5. Conflicting objectives

Two of the human's stated goals pull apart, and the agent cannot pick without
overriding one.

```
LAWFUL: "Tone nak penang kampung untuk group chat, tapi rules-heavy L2 ask — satu
        approach. Tone nak formal-professional untuk CP, tapi kau prefer casual —
        other approach. Which one tonight?"

UNLAWFUL: "Lots of options here…" — the agent has not done the work to identify the
          conflict; the human has to do it.
```

## The five unlawful categories (anti-patterns)

### A. Implementation / architecture / framework asks

"Repo mana?" / "Folder mana?" / "Architecture mana?" — the agent has access to the
filesystem and the registry. Run `find`, run `skills_list`, default to the most
recently-modified, and disclose.

The fix is in `bridge-protocol`'s pitfall §"human attention membrane":

> NEVER ask Arif technical / implementation / schema / naming / architecture /
> framework / library / tooling / style / config / file layout / error output /
> "which do you prefer" questions. Asks HOW is an **attention leak**.

### B. "What should I do?" / "What does the human want?"

The agent has the context: USER.md, MEMORY.md, the prior turn, the federation state.
"What should I do?" is the agent admitting it has not read any of those.

### C. Multi-choice menus where one option is the default

Three options presented when option 1 has 90% probability is exam-mode. Drop two,
default, disclose.

### D. Re-checking already-checked facts

"Did you mean X?" after the agent's own probe returned X. The probe was the check.
Trust it.

### E. Asking for confirmation of work the agent hasn't done yet

"Confirm aku boleh run the patch?" before the agent has even read the patch. The
confirm-before-probe is the failure mode — see `bridge-protocol` pitfall 11a (probe
then deliver, never confess-then-probe).

## A note on the boundary

The five lawful categories are NOT "what the human will answer" — they are "what
the human OWNS in this conversation." Authority, taste, values, irreversible risk,
and conflict-between-stated-goals all sit with the human by constitution. The agent
asking about any of them is *recognition*, not *export*.

The unlawful categories are "things the agent could have done but punted to the
human." Each one represents work the agent owed the system.

## Where the boundary breaks

When a question LOOKS lawful but is actually unlawful, the discipline is to ask one
more probe before surfacing:

```
LAWFUL-SHAPED BUT UNLAWFUL:
"Tone mana kau nak?" — looks like preference, but the taste is in USER.md. Probe first.

LAWFUL-SHAPED AND LAWFUL:
"Tone mana untuk email Kak Su?" — named recipient, no human-card on file for Kak
Su, no probe available. Lawful because there's no other path.
```

The probe-first decision tree in `references/probe-first-decision-tree.md` runs
before the category check.

## Closing — every question is a contract

When the agent asks the human a question, the agent is implicitly saying:

> The system that I have access to — files, memory, subagents, tools, the search
> index, the well-registry — does not contain this answer. Asking you is the last
> available move.

That contract is a real claim. If the system *does* contain the answer, the agent
has fabricated the ask — the contract was a lie. The Question Budget is the rule
that makes the contract enforce itself: the probe first, the ask only when the probe
has failed verifiably.
