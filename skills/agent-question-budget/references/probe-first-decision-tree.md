# Probe-First Decision Tree — Choosing the Cheapest Probe Before Asking

The Question Budget's first test: "Is the answer already in the system?" The cheap
probe is always preferred over a clarifying question to the human. This file is the
decision tree for what that probe looks like for the common cases the human will
notice.

## Five cases where the probe is cheap and the question is costly

### Case 1: Naming a person ("Do you remember X?" / "Tell me about X")

The probe sequence — cheapest first:

```
1. ~/.hermes/memories/MEMORY.md         — agent's notes (2200 chars)
2. ~/.hermes/memories/USER.md           — user profile (1375 chars)
3. ~/.hermes/carry_forward.json         — last ~185 typed entries
4. search_files() across project tree   — HAMPA, /root/memory/evidence/, /root/AAA/
5. ~/.hermes/cache/documents/           — WhatsApp / Telegram logs
6. mailread check                       — Gmail if relevant to the named person
```

Failure mode: agent says "takde rekod" / "aku tak ingat" without opening any file.
That is an unevidenced claim about the system's state — same weight as fabricating
the answer from training data.

### Case 2: Naming a file or path ("Where is X?" / "Find me the file")

Cheapest probe:

```
1. find /root -maxdepth 5 -name '<pattern>' 2>/dev/null | head -10
2. search_files files '<pattern>' path='/'  (if first run is too slow)
3. check ~/.local/share/arifos/ for symlinked working trees
```

Failure mode: agent says "I don't have access" without running `find`. Even if the
find returns nothing, "find returned 0 hits across /root, /home, /opt" is *evidence* —
the absence is now documented.

### Case 3: Naming a date / time / event ("When did X happen?")

Cheapest probe:

```
1. date '+%H:%M %Z %z'                              — wall clock for "now"
2. ~/.hermes/carry_forward.json                     — anchored entries with ISO timestamps
3. session-temporal-read.py                         — session close timestamp
4. mailread search <keyword>                        — Gmail by date range if relevant
```

**Hard rule (MANDAAT TEMPORAL):** Never guess the time of day. The failure mode is
"Hang rasa ni tengahari ni" when it is 17:30. Always run `date` first. Same discipline
for "hari ni", "minggu ni", "bulan ni" — they all collapse without a clock probe.

### Case 4: Reading a value (state, port, count, status)

Cheapest probe:

```
1. terminal() with the relevant probe — curl, ss, ps, du, stat, etc.
2. read_file() if the value is in a known log/cache
3. delegate_task() for a bounded read on a slow surface
```

Anti-pattern: "Aku rasa port 4000 down." vs `curl -s -o /dev/null -w '%{http_code}'
http://127.0.0.1:4000/` — the latter takes <1s, the former is a fabrication the human
has to test.

### Case 5: Picking a tool / model / profile

Cheapest probe:

```
1. skills_list <category>          — already in agent context
2. read_file config.yaml <path>   — already in agent context
3. federation call-map            — already in agent context
```

Failure mode: agent asks "Alat apa kau nak aku guna?" when `skills_list` would have
returned 6+ relevant skills in <1s. **Run skills_list, filter to top 3 candidates,
default to the most reversible, disclose in one line.**

## The escalating-cost probe ladder

When the cheap probe fails, escalate — but escalate the **probe**, not the question
to the human:

```
CHEAP        memory read         <0.1s    always run first
             file glob           <0.5s
             grep on a known log <0.5s
             terminal probe      <1s
MEDIUM       web search          1-3s     when internal is empty
             web_extract         1-5s     when a specific page is named
             subagent in parallel 5-15s   when the work itself is bounded
EXPENSIVE    delegate_task with 30-120s   when the work spans multiple surfaces
             multiple goals
HUMAN ASK    NEVER               ∞        only after the ladder is exhausted
```

The human ask is not a step on the ladder — it is the **floor** under the ladder,
the place the agent stands on when the ladder fails. Reaching the floor costs
attention; one rung up saves it.

## Two escalating rules

**Rule A — domain-specific overrides.** Some surfaces are constitutionally
inaccessible from the agent's seat:
- A persona's private chat (the human only) → no probe → route to human
- A second human's DM the agent isn't paired with → no probe → ask human which surface
- Mail that requires re-auth → no probe → tell human "token expired, re-auth?"

These are NOT the agent failing the budget — they are gate conditions where the
budget's law says "ask, because there is nothing else."

**Rule B — the empirical check.** After a probe, the result must be reported
*verifiably*. A probe that returned `HTTP 200` is a fact. A probe that returned
`HTTP 200` and "the response says X" is two facts. Do not collapse them. If you say
"port 4000 is up", name the probe and the response code in the same line.

## Pitfall — the probe that pretends to be a probe

Running a probe whose result the agent cannot use is a fake probe. Examples:
- `skills_list` and then asking the human to pick (the list was the probe; pick now)
- `find` returning 0 hits and then saying "I couldn't find it" (the result IS the find)
- `mailread check` returning `INVALID_CRED` and then saying "I don't have mail access" (the result is the diagnosis; tell human to re-auth)

The probe returns either a fact or a noise reading. The agent's job is to read both.

## Closing — the human is not the cache layer

The Question Budget exists because the agent's working memory + filesystem +
subagents + web is a deeply capable cache. The human is not part of that cache — they
are the SOT (source of truth). The Question Budget is what keeps the agent from
treating the SOT like a cache. When in doubt: run one more probe. The cost of an
unused probe is seconds; the cost of an asked question is attention the agent cannot
replace.
