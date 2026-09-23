# Exam-Mode Recovery — When the Agent Has Fired a Multi-Question Batch

This is the failure mode where the agent's draft contains 2+ questions in one turn
to the human. The user has either:
- Not yet pushed back (recovery is preemptive — catch the draft before send)
- Already pushed back ("exam mode", "aku penat nak jawab soalan x penting",
  "tarik balik", "cukup satu")

## Detection (pre-send)

**Count `?` in the draft.** Two or more `?` in CONVERSE mode is exam-mode.

For EXPLAIN mode, allow 0–2 if load-bearing. For INSPECT mode (F13 sovereign only,
`inspection_mode = true` signal), no limit.

**Watch for these aliases** — they look like single questions but are actually nested
sub-questions:
- "Apa kau nak aku buat — A, B, atau C?" (1 visible `?`, 3+ sub-options)
- "Default aku ni, atau kau nak override?" (1 `?`, 2 sub-questions)
- "Faham, atau nak aku explain lagi?" (1 `?`, decision + nested diagnostic)

Treat each sub-option as a question for budget purposes. Strip the embedded ones;
keep the outermost if it's the only survivor.

## Recovery procedure (post-pushback)

When the user has already corrected ("exam mode" / "cukup satu" / "tarik balik"):

1. **One-line acknowledge.** "Aik — exam mode. Aku tarik balik tiga tu, tanya satu
   je."
2. **Count the open question explicitly.** "Yang aku masih tanya: [the one thing]."
3. **Re-issue one tight question.** Replace the menu with the single highest-stakes
   ambiguity. Drop the rest; the agent will absorb them.
4. **Disclose the default for the others.** "Untuk dua lagi: aku default X dan Y,
   cakap kalau lain."

The recovery does NOT include:
- A second apology ("aku承认 lagi" — see `bridge-protocol` rule about single-ack)
- A defence of the original menu ("aku tanya sebab…")
- A promise to remember in prose (the next session will skim it; a skill update
  carries it properly — which is what this file is for)

## Recovery procedure (pre-send, agent catches itself)

When the agent's pre-flight linter or self-check reveals multi-question:

1. **Rank the questions by stakes.** Which one, if unanswered, blocks the work? That
   is the one that survives.
2. **Drop the rest to defaults.** Each dropped question gets a default + 1-line
   declaration: "Default X. Cakap kalau salah."
3. **Strip menu chrome.** No "Option A / B / C", no "1. ... 2. ... 3. ..." — flat
   question in line, defaults after.

The dialog BEFORE recovery:

```
BAD (3 questions):
"Repo mana nak aku edit? Folder structure macam mana? Atau nak aku run dulu?"

RECOVERY (1 question + 2 defaults):
"Aku nak run dalam /root/AAA/* berdasarkan kamu punya config. Folder default aku
ikut convention biasa — cakap kalau kau nak struktur lain. Confirm jalan?"
```

The recovery carries the same work forward but costs the human **one** answer, not
three.

## The "user wanted N" trap

When the user explicitly asks "tanya aku 7 soalan" / "ask me 5 things":

That is a *cycle*, not a *batch*. ONE per turn. The agent tracks which question
number it is on (3/7, 4/7, etc.) and acknowledges cycle progress when the user asks.

The mechanism: a numbered programme is the user giving the agent a turn-budget. The
agent's job is to spend the budget over time, not to fire it in one round. The same
discipline applies to any numbered programme — checklists, todo lists, decision
trees. Use them as the shape of the conversation, not the contents of one turn.

## The "tell me everything" trap

When the user says "tell me everything about X" or "everything we know on X":

```
GRADIENT:
weak mode (essay from training data) → use this only when probe-empty
mid mode (memory + graph read + 1-line summary)
strong mode (memory + graph + web + subagent in parallel + synthesis)
```

Default: **mid mode**. Bump to strong mode when:
- The topic touches the human's professional domain (PETRONAS, F13 family, commercial
  surface)
- The user has corrected the same probe-empty pattern in this session
- The question is bounded by a recent artifact (a file, a paste, a recent event)

The user's "tell me everything" is not a license to fire all the lights in the
agent's context — it is a request for a probe with adequate depth.

## Closing — the asymmetry

The Question Budget is asymmetric by design. Asking has small upside (maybe the
answer helps) and large downside (the human's attention is now spent). Absorbing
has large upside (the human can keep moving) and small downside (the agent's probe
took some seconds).

Pre-flight each ask against the asymmetry. The math usually says: probe one more
time, then ask.
