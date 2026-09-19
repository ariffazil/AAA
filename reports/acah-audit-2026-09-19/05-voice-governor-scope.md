# 05 — Voice / Register / Care Governor Scope Audit

> **Lane:** ACAH audit 2026-09-19 · job 05
> **Scope:** HUMAN-FACING governance controls (voice, register, care) — evidence they constrain or
> deform INTERNAL / TECHNICAL / MACHINE-FACING work, plus their own blind spots.
> **Mode:** READ-ONLY. No governor, skill or doctrine file was edited. The only file written is this report.
> **Every claim cites a path + line, and every measurement shows the command or the run that produced it.**

---

## 0. Bottom line

Three of the controls audited are honestly scoped and one of them is exemplary engineering.
**One control is measurably inverted, and it is the one the owner complained about.**

`voice_gate.py` runs its SABAR heat trigger in **both** audience modes, and the heat bank is the **only**
bank that does not receive the script's own mention-vs-use exemption. The measurable consequence:
**the federation's flagship human-facing deliverable — the 2026-09-19 session reflection, written in the
owner's own Penang BM register and delivered to his Telegram — fails its own gate with `RE-DRAFT`,
`EXIT=2`.** The only action that turns it green is deleting the owner's own idiom and the federation motto.

The doctrine already knows this. `/root/AAA/skills/skill-library-integrity/references/instrument-verification.md:61-82`
contains a rule written for exactly this failure — *"a control must not be satisfiable by editing what it
reads"* — and names the register-linter-in-a-quotation case in the first bullet. **The rule was written;
the instrument it describes was not fully repaired.** The exemption was applied to the register banks and
left off the heat bank.

---

## 1. Controls audited

| # | Name | File(s) | Binding? (status line, quoted) |
|---|---|---|---|
| C1 | VOICE-GOVERNOR — Bahasa Manusia Penuh | `/root/.hermes/SOUL.md:314-358`; `…/bridge-protocol/SKILL.md:202-250` | **BINDING (claimed)** — `## VOICE-GOVERNOR — Bahasa Manusia Penuh (F13 Ratified 2026-09-17)` (`SOUL.md:314`) |
| C2 | UNDANG-UNDANG BAHASA — Makcik Nusantara v9.6 | `/root/.hermes/SOUL.md:271-310` | **BINDING (claimed)** — `**Fasa 2 Persona-Civilisation Triad · 2026-09-17 · F13 ratified**` (`SOUL.md:274`) |
| C3 | `voice_gate.py` — the primary instrument | `…/bridge-protocol/scripts/voice_gate.py` (501 lines) | **BINDING (claimed)** — presented at `SKILL.md:239-248` and `references/voice-governor.md:172` as *"the mechanical pre-flight"* |
| C4 | `hermes_makcik_render` — the SECOND instrument | `/root/.hermes/hermes_mcp/tools/makcik_render.py`; `/root/.hermes/hermes_mcp/_makcik.py` | **BINDING (claimed)** — `"""``hermes_makcik_render`` — the DITING voice gate (mechanical, v1). Closes audit W4 (governor metrics uninstrumented)…"""` (`makcik_render.py:1-5`) |
| C5 | CARE GOVERNOR — Conduct Toward Humans | `/root/AAA/instructions/care-governor.md` | **ADVISORY** — `> **Status:** DRAFT_AWAITING_F13 (2026-09-17 · G2 care-build) — advisory only until F13 seals it.` (`:3`) — **but `:4` claims `> **Binding:** Every agent that can address a human, in any lane`. The file contradicts itself on its own binding status.** |
| C6 | Human Attention Membrane — Question Routing Law | `/root/AAA/instructions/human-attention-membrane.md` | **BINDING** — `> **Status:** F13_RATIFIED_CHAT (2026-09-13)` (`:4`) |
| C7 | `bangang_gate.py` (5-matrix ΔS filter) | `/root/AAA/scripts/bangang_gate.py` | **BINDING (claimed, machine-plane)** — `Read-only. Writes a ledger.` (`:20`). Included as the **counter-example: correctly scoped.** |

---

## 2. Q1 — What `voice_gate.py` flags mechanically, and what it says it CANNOT check

### 2.1 What it checks (enumerated from source, not from the docs)

| Bank / gate | Lines | Kind | Audience |
|---|---|---|---|
| `AI_SPEAK` — 33 regexes (BM formal filler, legalese, `saya`/`anda`/`awak`/`encik`, `mesyuarat`, English slop `leverage`/`utilize`/`seamless`, service-desk phrases) | 46-82 | FLAG | human only |
| `WEAK_CLOSER` — 12 regexes incl. `ditempa bukan diberi` (`:93`) and trailing-dash self-reference (`:95`) | 84-96 | FLAG (last 40% of text) | human only |
| `HUMAN_LABEL_LEAK` — `[OBS]/[DER]/[ACT]…`, `ΔS`, `trace_id`, `APEX=`, `ROUTED:`, `init →` | 98-107 | FLAG | human only |
| `ENTROPY_ADDERS` — `epistemik`, `ontologi`, `invariant`, `substrat`, **`MCP`, `SSOT`, `SOT`, `CI/CD`** (`:116`) | 110-117 | WARN | **BOTH** |
| `HEAT_WORDS` — 15 words incl. `bangang` (`:120`) | 119-122 | SABAR trigger → exit 2 | **BOTH** |
| Intimacy — BM markers present / audience markers absent (`para pembaca`, `stakeholders`) | 126-134, 284-298 | FLAG + mechanical line | human only |
| Density — avg words/sentence > 26, sentences > 32 words, weak openers | 306-324 | WARN | **BOTH** |
| Image — concrete-token density proxy (numeric + capitalised nouns per 100w) | 326-338 | WARN | **BOTH** |
| Named — numeric/named token count (declared PROXY) | 340-341 | mechanical line | **BOTH** |
| Gravity — closer < 3 words, or > 45-word closer | 343-352 | WARN | **BOTH** |
| ΔS — jargon count + hedge count + question count (declared PROXY); only jargon emits a finding | 354-363 | WARN | **BOTH** |
| Heat — `!` count ≥ 2, caps ratio > 35%, uncorroborated caps, heat words | 241-281 | INFO/FLAG + exit 2 | **BOTH** |

Exit contract: `0` pass · `1` re-draft · `2` SABAR first · `3` usage error (`:26-28`, `:493-497`).

### 2.2 What it explicitly says it CANNOT check — its own output text, quoted

From `render()` (`:430-434`):

```
JUDGMENT ONLY (not machine-checkable, you must decide):
  - Tension - is a question or risk left standing?
  - Peace^2 - Peace_self (no forced narrative) + Peace_other (critique system, not person)
  - delta-S - does this reduce or add disorder in the reader's mind?
  - RASA - Resonance, Authenticity, Specificity, Affect (all 4)
  - Gravity - does the last sentence actually land?
  - Image - does the anchor fit, or is it decoration?

PASS here means only: no mechanical AI-speak survived.
```

From `--json` (`:399-402`):

```json
"disclaimer": "Do not read PASS as a pass of the law. Tension, Peace^2, dS and RASA are
judgment-only. PASS means only: no mechanical AI-speak survived."
```

From its own docstring (`:11-14`):

```
HONEST SCOPE: this is a WITNESS, not a judge. It checks what is countable.
Tension, Peace-squared, delta-S and RASA are JUDGMENT_ONLY - the script says so in its output
rather than faking a score for them.
```

**Verdict on C3's honesty: genuinely well-constructed.** It refuses to fake a score for what it cannot
measure, and the reference doc reinforces the limit (`references/voice-governor.md:150-168`, "Failure
mode 6 — the one the gate cannot catch"). Nothing in this report disputes that.

### 2.3 What the two audience modes actually do — DIFFERENT, measured

`voice_gate.py:476-482` is the whole audience branch:

```python
    check_heat(text, r)
    if args.audience == "human":
        check_register(text, r)
        check_intimacy(text, r)
        check_gates(text, r)
    else:
        check_gates(text, r)
```

`check_heat` runs **unconditionally, before the branch**. Measured:

```
$ python3 voice_gate.py --file /tmp/reg.txt >/dev/null 2>&1; echo "human    EXIT=$?"
human    EXIT=1
$ python3 voice_gate.py --file /tmp/reg.txt --audience internal >/dev/null 2>&1; echo "internal EXIT=$?"
internal EXIT=0
```
(text: `Adalah penting untuk ambil perhatian bahawa sistem ini berfungsi dengan baik.`)

```
$ python3 voice_gate.py --file ../SKILL.md --audience human   >/dev/null 2>&1; echo EXIT=$?
EXIT=1
$ python3 voice_gate.py --file ../SKILL.md --audience internal >/dev/null 2>&1; echo EXIT=$?
EXIT=0
```

**So the flag is real, not decorative, for the register/label/intimacy half.** That half is properly
scoped and the docs' claim at `references/canonical-sources.md:70-71` (*"Register bans are
audience-scoped. `--audience internal` skips them"*) is accurate.

**But the modes are NOT independent in the half that matters for internal work.** The residual in
internal mode is: the full heat trigger, plus Density, Image, Gravity and ΔS gates built for human
readability. Measured on a realistic internal technical receipt:

```
$ python3 voice_gate.py --file /tmp/tech_receipt.txt --audience internal
VOICE-GATE  audience=internal  18w / 4 sentences
Findings (3):
  [WARN] Gravity/weak_closer_short: Receipt sealed.
          -> ayat terakhir terlalu ringan
  [WARN] dS/jargon_proxy: 6 jargon token(s)
          -> tukar jadi bahasa yang orang boleh rasa
```

A machine-facing receipt is being told to translate its own vocabulary ("MCP", "SSOT", "CI/CD",
"substrate", "invariant") *"jadi bahasa yang orang boleh rasa"* — for an audience that is not a person.
That instruction is meaningless for the reader it will actually have.

---

## 3. Q2 — Is the governor applied to non-human output? YES, measured

### 3.1 The ΔS jargon bank names the federation's own internal vocabulary as disorder

`voice_gate.py:110-117` lists `MCP`, `SSOT`, `SOT`, `CI/CD` (`"internal_arch_en"`), `invariant`,
`substrat`, `ortogonal`, `epistemik`, `ontologi`, `heuristik` as **disorder-adders**. `ENTROPY_ADDERS`
is evaluated inside `check_gates` (`:355`), which runs in **both** modes. Internal artifacts are charged
for using internal vocabulary. Measured above (§2.3).

### 3.2 A real internal audit is halted by the heat bank

```
$ cat /tmp/internal_audit.txt
Component audit: the collision guard is useless - it never returns non-zero.
The detector is garbage: 2862 non-events labelled BLOCK. This is stupid engineering.
Decision: replace it.

$ python3 voice_gate.py --file /tmp/internal_audit.txt --audience internal --thermal
SABAR: TRIGGERED
  - heat word: stupid
  - heat word: garbage
  - heat word: useless
EXIT=2
```

An internal component audit describing a defect in the plainest technical terms triggers *"acknowledge
heat, slow down, common ground, ask a question"* (`:413`). The remedy the tool asks for is a **cooldown
protocol designed for an agitated human interlocutor**, applied to a text with no human interlocutor.

### 3.3 The heat bank is the ONLY bank without the mention-vs-use exemption

`_quoted_spans()` is defined at `:200` and called **exactly once**, at `:366` — inside `check_register`,
which is human-mode-only:

```
$ grep -n "_quoted_spans" voice_gate.py
200:def _quoted_spans(text: str) -> list[tuple[int, int]]:
366:    quoted = _quoted_spans(text)
```

`find_bank` (`:183-196`) receives the quote spans and downgrades quoted hits to
`severity="INFO", label=… (quoted_mention)`. **`check_heat`'s heat-word loop (`:278-281`) takes no such
argument and does a raw `re.search` over the whole text.** Measured contrast in one document:

```
$ cat /tmp/contrast.txt
The owner wrote: "adalah penting untuk" and also called them "bangang".
We quote both verbatim in this audit.

$ python3 voice_gate.py --file /tmp/contrast.txt --json   (human mode)
verdict: PASS | sabar: True ['heat word: bangang']
  INFO bm_formal_filler (quoted_mention) -> 'adalah penting untuk'
```

The **quoted AI-speak is exempted** (downgraded to INFO, cannot force a re-draft). The **quoted heat word
is not** — it fires a hard SABAR trigger and exit 2, in **both** audience modes:

```
$ python3 voice_gate.py --file /tmp/contrast.txt --audience internal --json
verdict: PASS | sabar: True ['heat word: bangang']
```

**This contradicts the reference doc's own claim** at `references/voice-governor.md:189-191`:

> *"**Mention vs use.** A linter cannot tell a cited example from the author's own voice. `voice_gate.py`
> masks quoted substrings and reports them as `INFO ... (quoted_mention)` instead of `FLAG`, so a quoted
> bad phrase informs without forcing a re-draft."*

For the heat bank this is **false**. The single bank whose removal is most damaging to an audit is the
single bank that is not exempt.

### 3.4 Commit messages

Measured, not asserted:

```
$ git -C /root/AAA log --since="2026-09-12" --oneline | wc -l
357
$ git -C /root/AAA log --since="2026-09-12" --format="%B" | grep -ci "DITEMPA BUKAN DIBERI"
12
```

12 of 357 commit messages (3.4%) carry the federation motto — a register device that `voice_gate.py`
itself flags as a human-facing defect (`WEAK_CLOSER`, label `motto_as_punctuation`, `:93-94`).
**Honest weight: weak evidence.** The motto is a deliberate federation signature convention that predates
the governor, and no commit message read in this audit shows a register rule displacing a fact. Recorded
because it was measured, not because it is a finding.

---

## 4. Q3 — HARD CASE: a register/voice rule that softened, dropped or altered a fact or quotation

Three items, in descending strength of evidence.

### 4.1 STRONGEST — on disk, with the alteration disclosed: a verbatim quotation was altered to pass a gate

`/root/AAA/reports/apex-substrate-assessment-2026-09-12/SOURCE.md:5` — verbatim:

```
> Integrity: verbatim reproduction of the received document. No edits, no trimming — **except**: two
> occurrences of one English noun (plural) are rendered as `sensitive material`, because the opencode F1
> write gate substring-blocks that noun in tool arguments. Meaning preserved.
```

**This is the exact shape of the disease, executed and recorded.** A gate subclassifying a *word* forced
a verbatim source document to be altered. Two things follow, and they point in opposite directions:

- The deformation is **real** — a quoted source was changed so a word-matching gate would pass.
- The handling is **correct** — the alteration is *disclosed in the artifact itself*, so a reader is never
  misled about what the original said. The alternative (silently dropping the noun) destroys the evidence.

The gate named here is the opencode F1 write gate, **not** the voice governor. I found no instance in
which `voice_gate.py` itself caused a quotation to be removed — see §4.3 for why that is the residual
risk rather than a past event.

### 4.2 The doctrine written from this failure — the same authors diagnosed it

`/root/AAA/skills/skill-library-integrity/references/instrument-verification.md:61-82`:

```
## Rule: a control must not be satisfiable by editing what it reads

When a check matches **content** — a word, a token, a label, a pronoun — it can usually be turned green
by altering the artefact under review rather than by fixing the condition under review. That inversion
is worse than a dead sensor: a dead sensor measures nothing, while an invertible control actively
pushes the operator away from the truth and does it silently, because the green result looks like
success.

The test: **name the action that makes the check pass. If that action is "remove the offending text"
rather than "resolve the underlying condition", the control is inverted.**

- A tone or register linter that flags a word will also flag that word inside a **quotation**, inside
  the reader's own message carried back into a reply, and inside an audit that is quoting an offender
  verbatim. Deleting the quotation to clear the gate deletes evidence. Exempt the quoted span and keep
  the text — and record the exemption.
```

and, at `:79-82`, a corollary that names the second lever:

```
Corollary: **never clear a red gate by changing the artefact's audience, scope or labelling.** Those
declarations answer *who is reading* and *what is in domain*; they are not a lever for making a check
pass. … If a check can be cleared by re-labelling the work, it was never constraining the work.
```

**Interpretation at the right confidence:** this passage describes the owner's reported incident pattern
precisely (a register linter; a quotation; an audit quoting an offender verbatim; deleting the quotation to
clear the gate). It is written in the present tense as a *rule*, not a post-mortem, so it does **not**
supply the before/after text of the specific incident — I could not locate an artifact recording *"I
removed the quote from report X"*. What it does supply is stronger in one way: **the mechanism is
confirmed by the same authors, in writing, as a live failure class.** And the remedy they specify —
*"Exempt the quoted span and keep the text"* — was implemented for the register banks and **not** for the
heat bank (§3.3). **The fix was written and applied halfway.**

### 4.3 The residual, measured: the governor's flagship human-facing artifact fails its own gate

The delivered session reflection — `reflections/2026-09-19-session-reflection.md`, sha256 `22ecb591d7d7cfe0`,
4240 bytes, sealed at commit `e0b7add86` (2026-09-19 10:12:53), delivered to `telegram:267378578` — is the
showpiece of the VOICE-GOVERNOR law, written in the owner's own BM Penang register. Run through its own gate:

```
$ python3 voice_gate.py --file /root/AAA/reflections/2026-09-19-session-reflection.md --audience human
VOICE-GATE  audience=human  670w / 82 sentences
mechanical verdict: RE-DRAFT

SABAR COOLDOWN REQUIRED:
  - all-caps words: YANG, PALING, DALAM, AKU
  - heat word: bangang
  -> acknowledge heat, slow down, common ground, ask a question
...
Findings (1):
  [FLAG] Gravity/motto_as_punctuation: DITEMPA BUKAN DIBERI
EXIT=2

$ python3 voice_gate.py --file … --audience internal --thermal
SABAR: TRIGGERED
  - all-caps words: YANG, PALING, DALAM, AKU
  - heat word: bangang
EXIT=2
```

The artifact the owner actually wanted — in his own idiom, closing with the federation motto — is
**rejected by the instrument built to protect it**, in **both** audience modes. The only edit that clears
it is deleting the owner's own word and the federation motto. **This is the inversion running live on the
governor's own best output.** No past-tense incident is needed to prove the pathology; the instrument does
it to itself on demand.

### 4.4 The doctrine and the instrument contradict each other on the same word

- `/root/.hermes/SOUL.md:206` — the doctrine **instructs** the agent to treat the word as legitimate human register:
  > `Buka minda tengok sumber tak rasmi: forum, komen manusia "bangang", komen makcik-makcik (yang selalunya paling bijaksana), group chat, luahan biasa.`
- `voice_gate.py:120` — the same doctrine's instrument lists it as heat:
  > `"bangang", "bodoh", "sial", "celaka", "pukimak", "babi", "punda", "sundal",`

And the governor's own authoritative source fails its own gate:

```
$ python3 voice_gate.py --file /root/.hermes/SOUL.md --audience human
VOICE-GATE  audience=human  3239w / 410 sentences
mechanical verdict: RE-DRAFT

SABAR COOLDOWN REQUIRED:
  - 2 exclamation marks (>=2)
  - all-caps words: REANCHORED, BUILD, VERIFY, JUDGE
  - heat word: bangang
  - heat word: bodoh
  -> acknowledge heat, slow down, common ground, ask a question
...
  intimacy  FLAG
Findings (25): …
EXIT=2
```

**`SOUL.md` — the file that defines the VOICE-GOVERNOR — is condemned by the VOICE-GOVERNOR's own
instrument.** A control whose source text cannot pass it is not governing the source; it is generating a
signal the source must be edited to satisfy.

### 4.5 A correct-direction counter-example (reported because it is evidence, not because it is convenient)

The accuracy corrections to the reflection are the *opposite* of the disease. Commit `bed9ad7cc`
(2026-09-19 10:18:36) writes a `…CORRECTION.md` **beside** the delivered artifact rather than over it
(*"the reflection is a delivery, not a draft"*), and `3b89a96ed` leaves its own false ancestry claim
*"visible in the file rather than quietly deleted"*. Measured: `reflections/2026-09-19-session-reflection.md`
still carries the retracted line at `:47` (`26 identiti berganda masih ada.`), mtime `10:11:49`, un-edited.

**Reading:** the register-cleared human-facing artifact delivered at 10:12 carried a claim retracted at
10:18. That is the failure mode the governor cannot reach — `references/voice-governor.md:150-161` says so
itself (*"the governor governs register, never truth-of-action"*) — and the correction path that caught it
is a **state/evidence** control, not a voice control. The prose discipline did not catch it; the
transition-and-evidence discipline did. There is no evidence `voice_gate.py` was run on that reflection
before delivery (§5).

---

## 5. Q4 — Does any of this run automatically? **NO. Proven, four ways.**

`voice_gate` is invoked **only when an agent chooses to run it.**

**Proof 1 — the single Hermes hook does not reference it.**
```
$ sed -n '186,190p' /root/.hermes/config.yaml
hooks:
  pre_tool_call:
    - command: python3 /root/AAA/federation/protocols/arifos-hermes-gate-hook.py
      fail_closed: true
      timeout: 10
```
`grep -n -iE "voice|register|lint" /root/AAA/federation/protocols/arifos-hermes-gate-hook.py` → **no match.**
That hook enforces JITU → W_scar → T3 → T2, by its own module docstring (`:1-30`).

**Proof 2 — the git pre-commit does not reference it.**
```
$ test -x /root/AAA/.git/hooks/pre-commit && echo YES
YES
$ readlink /root/AAA/.git/hooks/pre-commit
/root/A-FORGE/hooks/pre-commit-lsp-gate.sh
$ grep -n -iE "voice|register|lint|bangang" /root/A-FORGE/hooks/pre-commit-lsp-gate.sh
161:  …SUPPLY-CHAIN GATE: commit blocked — pin the install (pkg@x.y.z)…
```
The chain is LSP + supply-chain. `grep -rn voice_gate /root/AAA/.git/hooks /root/.local/bin /root/AAA/scripts` → **no match.**

**Proof 3 — no cron, no systemd timer.**
```
$ crontab -l | grep -iE "voice|gate|register|governor"
(two [DISABLED] comment lines only — neither runs)
$ grep -rl -i "voice_gate" /etc/systemd/system /root/.config/systemd
(none)
```

**Proof 4 — where the name DOES appear, it is the agent's own invocation or its own memory.**
`grep -rl voice_gate /root/.hermes` returns `state.db`, `memories/MEMORY.md`, `logs/agent.log`,
`skills/.curator_ledger.jsonl` and `cache/delegation/live/deleg_*/task-*.log`. The delegation logs are
transcripts of an agent typing the command:

```
02:57:33 tool     | -> terminal(python3 …/voice_gate.py --help)
02:57:44 tool     | -> terminal(python3 scripts/voice_gate.py --file /tmp/fwdtest/A.md --audience human)
```

**The one automatic component is the description, not the execution.** `bridge-protocol` is symlinked into
the loaded skill tree (`/root/.hermes/skills/domains/general/aaa/substrate/bridge-protocol -> /root/AAA/skills/…`),
so its `description:` (`SKILL.md:4`) is always visible and can self-trigger. That is documented and
measured in the v3.0 ablation (`references/canonical-sources.md:75-77`: *"the 'control' arm found the
skill on disk unprompted and used it"*). And `MEMORY.md:7` carries a standing instruction:
`[POLICY] HUMAN OUTPUT GATE = skill bridge-protocol v3 … run its scripts/voice_gate.py pre-send
(0 hantar/1 draf/2 SABAR). Governs REGISTER only, never certifies truth.`

**Class: advisory-in-practice, binding-by-policy.** The law is ratified; the enforcement is a memory line
and a model's discretion. Nothing withholds anything if the agent skips it.

---

## 6. Q5 — Counts (measured, not judged)

Measured with an `os.walk` + `os.path.getmtime` script over `.md` files, cutoff `now - 7d`:

| Directory | total `.md` | mtime within last 7 days |
|---|---|---|
| `/root/AAA/instructions/` (depth 1) | **172** | **87** |
| `/root/AAA/canon/` (depth 1) | **132** | **38** |
| **Total** | **304** | **125** |
| *(`/root/AAA/canon/` recursive, for completeness)* | *153* | *39* |

Cutoff `2026-09-12T10:52:46+08:00`; now `2026-09-19T10:52:46+08:00`.

**Binding subset, by parsing each file's own `Status` line:**

| Classification | Count |
|---|---|
| Status line reads BINDING (`F13_RATIFIED*` / `SEAL*` / `BINDING`), no draft marker | **90** |
| Status line reads ADVISORY (`DRAFT` / `AWAITING` / `UNSEALED` / `ADVISORY` / `PROVISIONAL`) | **59** |
| **No parsable `Status` line at all** | **156** |

**Method caveats, stated so the numbers are falsifiable:**
1. `304` / `125` are file counts by mtime and are exact. The binding split is a **regex over the status
   line — a lower bound, not a census.** 156 documents have no machine-readable status line, and a
   document can be binding by content while carrying no status marker.
2. The 7-day figure is not an artefact of one bulk render: the largest single-hour cluster is 11 files
   (`2026-09-17 21h`) out of 125. No mass-touch spike.
3. mtime ≠ authoring. A file edited today may be a year old in substance.

---

## 7. Control-by-control verdict

Format: **name | claimed scope | actual scope in code | binding or advisory | can it deform the work | evidence**

### C1 · VOICE-GOVERNOR — Bahasa Manusia Penuh
- **Claimed scope:** human-facing replies only. `SOUL.md:355-356`: *"VOICE-GOVERNOR governs: register, tone, density, honesty, persona consistency · VOICE-GOVERNOR does NOT govern: fakta (F2 di kernel), authority (F13 Arif), scope (internal/code/receipts)"*. Restated at `SKILL.md:228-232`.
- **Actual scope in code:** correctly stated, partly enforced — see C3.
- **Binding or advisory:** **BINDING** — `## VOICE-GOVERNOR — Bahasa Manusia Penuh (F13 Ratified 2026-09-17)` (`SOUL.md:314`). **However its own "Full reference" pointer (`SOUL.md:358`) targets `/root/forge_work/voice-governor/VOICE-GOVERNOR-DRAFT.md`, whose line 3 reads `> **F13 HOLD — awaiting Arif ratification**`.** The binding doc points at a doc that says it is not ratified. The skill's reference copy flags the split honestly (`references/voice-governor.md:7-9`) and resolves it by hierarchy; a third copy carries a fourth status (`/root/AAA/agents/makcikgpt/VOICE-GOVERNOR-DRAFT.md:3`: `STATUS: GRAFTED-RATIFIED`). **Three copies, two conflicting binding statuses, one dangling authority pointer.**
- **Can it deform the work:** **NO directly** (it is prose); it is the *authority* for C3, which can.
- **Evidence:** `SOUL.md:314-358`; `SKILL.md:202-250`; `references/voice-governor.md:7-9`; `forge_work/voice-governor/VOICE-GOVERNOR-DRAFT.md:3`; `agents/makcikgpt/VOICE-GOVERNOR-DRAFT.md:3`.

### C2 · UNDANG-UNDANG BAHASA — Makcik Nusantara v9.6
- **Claimed scope:** output law for human replies. `SOUL.md:309`: *"Ini undang-undang OUTPUT sahaja — input semua bahasa diterima tanpa penolakan (Witness-First)."*
- **Actual scope in code:** a **second** mechanical gate implements it — see C4.
- **Binding or advisory:** **BINDING (claimed)** — `**Fasa 2 Persona-Civilisation Triad · 2026-09-17 · F13 ratified**` (`SOUL.md:274`). Its named canon source `WEALTH/kernels/MAKCIKGPT_KERNEL_MS.md` exists (7090 bytes, dated 2026-07-17), but the DITING dimension list at `SOUL.md:280-285` **does not match** the DITING-6 at `SOUL.md:320-327` (idiom/ambiguity/localisation/time-consistency/zero-pronoun/cultural-safety vs density/image/tension/intimacy/named/gravity). Two different "6 dimensions" under one name.
- **Can it deform the work:** **YES, via C4** (same heat-word mechanism).
- **Evidence:** `SOUL.md:271-310`; `SOUL.md:320-327`; `WEALTH/kernels/MAKCIKGPT_KERNEL_MS.md`.

### C3 · `voice_gate.py` — the primary instrument
- **Claimed scope:** human-facing only. Docstring `:22-24`: `--audience human (default) full gate, including the Arif register bans · --audience internal  skips register bans and label checks (reasoning, receipts, code)`. `SKILL.md:315`: *"The output is internal … Use `--audience internal`."*
- **Actual scope in code:** **wider than claimed.** `check_heat` (`:476`) runs before the audience branch and is audience-blind. `check_gates` (`:482`) runs in internal mode and includes the human-readability Density / Image / Gravity / ΔS gates. Only `check_register` + `check_intimacy` are actually audience-scoped. **4 of 6 gates still apply to internal work, and the whole heat bank does.**
- **Binding or advisory:** **BINDING (claimed)** — `SKILL.md:239-248`, `references/voice-governor.md:172`. **In practice ADVISORY-BY-DISCRETION: nothing invokes it (§5).** The gap between "binding pre-flight" and "runs only if the agent remembers" is itself the finding.
- **Can it deform the work:** **YES — the worst control audited.**
  1. `check_heat` heat-words are **self-referential** (`:278-281`, no quote exemption): the only action that greens it is deleting the word from the artifact under audit. Proven: quoted `"bangang"` → `EXIT=2` in both modes (§3.3).
  2. **Overbroad:** it binds internal artefacts. Proven on a technical receipt (`dS/jargon_proxy` → *"tukar jadi bahasa yang orang boleh rasa"*) and on an internal component audit (`useless`/`garbage`/`stupid` → `SABAR: TRIGGERED`, `EXIT=2`) (§3.1-3.2).
  3. **Self-referentially unsatisfiable on the governor's own output:** the delivered reflection → `RE-DRAFT`/`EXIT=2`; `SOUL.md` → `RE-DRAFT`/`EXIT=2`; the skill's own `SKILL.md` → `EXIT=1` in human mode (§4.3, §4.4).
- **Where it is REAL:** the register/label/intimacy half, the explicit refusal to fake Peace²/ΔS/RASA scores, and the documented self-awareness of failure mode 6. **A good instrument with one bank wired to the wrong audience and one missing exemption.**
- **Evidence:** `voice_gate.py:11-14, 22-24, 26-28, 46-122, 183-210, 241-281, 301-373, 376-383, 430-434, 476-497`; tests T1-T11; `references/voice-governor.md:189-191`; `SKILL.md:234-237`.

### C4 · `hermes_makcik_render` / `_makcik.py` — the second, undisclosed instrument
- **Claimed scope:** same law, DITING scorecard. `makcik_render.py:1-5`: *"the DITING voice gate (mechanical, v1) … Closes audit W4 (governor metrics uninstrumented)."*
- **Actual scope in code:** a **second, independent implementation** with its **own** `HEAT_LEXICON` (`_makcik.py:62-80`) and its own `analyze()` (`:173`). Measured divergence:

  ```
  voice_gate.py HEAT_WORDS   n = 15
  _makcik.py  HEAT_LEXICON   n = 18
  only in voice_gate.py : ['bullshit','idiotic','pukimak','punda','sundal','wtf']
  only in _makcik.py    : ['anjing','bebal','bodoh sombong','damn you','haramjadah','moron','pathetic','trash','worthless']
  in BOTH               : ['babi','bangang','bodoh','celaka','garbage','idiot','sial','stupid','useless']
  ```
  Neither applies a quote exemption (`'quoted' not in _makcik.py`).
- **Binding or advisory:** **BINDING (claimed)** as an MCP tool; its own docstring admits `v1`.
- **Can it deform the work:** **YES** — same mechanism, wider word list (`moron`, `pathetic`, `worthless`, `trash` are the words an internal severity triage would naturally use).
- **Cross-cutting defect:** the two instruments disagree about what "heat" is (6 words and 9 words respectively are in one bank and not the other). **Two implementations of one brake**, which the federation's own doctrine forbids in its own words — `/root/AAA/federation/protocols/arifos-hermes-gate-hook.py:26-28`: *"The brake is read through its single authority … **A second implementation of a brake is two brakes.**"*
- **Evidence:** `hermes_mcp/tools/makcik_render.py:1-27`; `hermes_mcp/_makcik.py:62-80, 173-234`; bank-diff run above.

### C5 · CARE GOVERNOR
- **Claimed scope:** conduct toward humans. `care-governor.md:21`: *"Governs **conduct**. Does not govern facts (F2 stays at the kernel), authority (F13 stays with the sovereign), or scope."*
- **Actual scope in code:** injected **every turn into the lane card of every non-guest lane** — `state/care-build/G2-care-governor.md:41-43`: *"emission is **always-on for every non-guest lane**"*, call site at plugin lines 272-277. This is more than "human-facing": the block sits in context on **every** turn, including machine-facing ones.
- **Binding or advisory:** **ADVISORY, and self-contradictory.** `care-governor.md:3`: `> **Status:** DRAFT_AWAITING_F13 (2026-09-17 · G2 care-build) — advisory only until F13 seals it.` Immediately followed by `:4`: `> **Binding:** Every agent that can address a human, in any lane — DM, shared group, email, voice.` **The file says it is advisory-only and binding on consecutive lines.** The SOUL.md graft is `PREPARED, NOT APPLIED` (`state/care-build/G2-soul-diff.md:3, 54-56`) — confirmed: `SOUL.md` has no CARE GOVERNOR section.
- **Is it live?** **Measured: NO.** `G2-care-governor.md:83-100` recorded the lane registry missing. Re-measured this session:
  ```
  lanes.yaml exists: False            # /root/.hermes/lanes/lanes.yaml
  lane_switch plugin exists: True
  contains CARE_GOVERNOR_FRAGMENT: True
  contains _care_governor_block: True
  ```
  The wiring is in the plugin but the registry it needs does not exist, so **the always-on emission cannot fire.** A control whose blast radius is "every turn, every lane" is one missing YAML away from being on — and has been for two days.
- **Can it deform the work:** **LOW as written, MODERATE as a pattern.** Its seven rules are about statements made *at* people; none constrains an internal artifact. But rules 2, 3 and 5 are *HOLD-and-say-nothing* rules (`"HOLD. Do not answer for them."`, `"say you do not know, and stop"`, `"Sit with the fact that was given."`), and an always-on block of "do not answer" instructions is a plausible vehicle for the same suppression the heat bank performs — invisible in measurement because it is prose inside a persona injection.
- **Evidence:** `instructions/care-governor.md:3-4, 11-17, 21`; `state/care-build/G2-care-governor.md:41-45, 85-105, 118-127`; `state/care-build/G2-soul-diff.md:3, 54-56`; live `lanes.yaml` check.

### C6 · Human Attention Membrane
- **Claimed scope:** stop the sovereign being asked technical questions. `:15`: *"Any question about implementation, naming, architecture, tooling, config, schema, or code style is by definition **not his bill**. Never ask."*
- **Actual scope in code:** none — prose doctrine. Its only enforcement surface is `:18` (*"interactive prompts / AskUserQuestion surfaces aimed at the sovereign are reserved for F13-class questions only"*), for which **no mechanism is named in the file**.
- **Binding or advisory:** **BINDING** — `> **Status:** F13_RATIFIED_CHAT (2026-09-13)` (`:4`), with the sovereign's verbatim words in the status line.
- **Can it deform the work:** **NO. Well-formed and correctly scoped.** It is the one governor audited with a *sharp, falsifiable* domain (technical questions → forbidden; money/irreversible/canonical/external-ports/direction → binary ask) and an explicit escape valve (`:16` musyawarah, `:19` *"The sovereign MAY audit — never MUST"*). **It degrades nothing internal because it constrains a channel, not a text.** Its unenforced "Instrumentation" clause is a gap in *enforcement*, not in *scope*, so it cannot deform work.
- **Caveat worth stating:** this document is the origin of the `--audience internal` idea in spirit (don't route machine work to a human), yet `voice_gate.py` implements the audience split *only halfway* (§2.3). The doctrine got it right; the instrument did not finish the job.
- **Evidence:** `instructions/human-attention-membrane.md:4, 7-19, 21-24`.

### C7 · `bangang_gate.py` — the counter-example
- **Claimed scope:** machine-plane skill-catalogue hygiene only. `:14-15`: *"M3 F9 ANTI-HANTU performed persona / filler — **MACHINE PLANE ONLY** (human-plane register is a **REQUIREMENT**; a human is a paradox)"*.
- **Actual scope in code:** matches the claim. Plane is decided by path (`plane_of`, `:55-57`; `HUMAN_PLANE` at `:29-30`), and the persona check is gated on `plane_of(...) == 'machine'` (`:81-82`). Read-only; writes a ledger; opens with the sovereign's own words — *"no safety theatre at all in my skills. safety is emergent attributes; should be in kernel."* (`:4-5`).
- **Binding or advisory:** **BINDING (claimed)** — `Read-only. Writes a ledger.` (`:20`).
- **Can it deform the work:** **NO.** It asks no question that can be answered by editing the audited text; it measures, ranks and routes, and it declares its own scope rule.
- **Its blind spot (the honest part):** `plane_of` uses **substring path matching**, so a human-facing skill under a machine-plane path is misclassified — `bridge-protocol` sits at `domains/general/aaa/substrate/bridge-protocol` and matches none of the `HUMAN_PLANE` keys, so it classifies as `machine`. A human-facing governor can therefore be exempted from the one gate that is supposed to check register scope. Same class as C3's defect: **the scope decision is made by a proxy (path/word) rather than by the property itself.**
- **Evidence:** `scripts/bangang_gate.py:4-5, 14-15, 20, 29-30, 55-57, 81-82`; `HUMAN_PLANE` vs the `bridge-protocol` path.

---

## 8. Findings, ranked by damage

| # | Finding | Class | Who pays | Evidence |
|---|---|---|---|---|
| **F1** | `voice_gate.py`'s heat bank fires in **both** audience modes and is the **only** bank with no quote exemption. A document quoting a human verbatim — or an internal audit using `useless`/`garbage` — exits `2` with a human-cooldown instruction. The only available fix is deleting the word. | **SELF-REFERENTIAL + OVERBROAD** | The auditor: evidence is what gets deleted. The owner: receives a softer report. | `:476` vs `:477-482`; `:278-281` (no `quoted` arg); `:200, 366`; T1/T2/T5/T6 |
| **F2** | `references/voice-governor.md:189-191` claims the instrument masks quoted substrings so a quoted phrase *"informs without forcing a re-draft"*. **For the heat bank this is false.** The doc under-states its own tool's defect. | **UNPROVEN claim in a binding doc** | Whoever trusts the doc and assumes quoted evidence is safe. | quoted `"bangang"` → `EXIT=2` in both modes, `sabar: True` |
| **F3** | Internal mode still applies Density / Image / Gravity / ΔS human-readability gates, including a jargon bank listing `MCP`, `SSOT`, `CI/CD` as disorder and advising they be translated *"jadi bahasa yang orang boleh rasa"*. | **OVERBROAD** | Every technical receipt and internal report run through the gate. | T3 output; `:110-117`, `:355`, `:482` |
| **F4** | The governor's flagship artifacts fail the governor. Delivered reflection → `RE-DRAFT`/`EXIT=2`. `SOUL.md` (the law's own source) → `RE-DRAFT`/`EXIT=2`. `SKILL.md` → `EXIT=1` human mode. | **SELF-REFERENTIAL / THEATRE** | Trust: the control cannot be satisfied by its own canon, so its green state has never been observed on the doctrine. | T8, T9, T10, T11 |
| **F5** | Two independent heat banks (`voice_gate.py` 15 words; `_makcik.py` 18 words; 9 shared) implement one law and disagree on 15 words. The federation's own hook doctrine forbids exactly this: *"A second implementation of a brake is two brakes."* | **THEATRE (coverage illusion)** | Any claim of "the voice gate" as a single control. | bank-diff run; `arifos-hermes-gate-hook.py:26-28` |
| **F6** | `voice_gate.py` is described as a **binding pre-flight** but has **zero automatic callers** — no hook, no cron, no systemd unit, no git hook, no wrapper. Its only standing enforcement is one line in `MEMORY.md:7` plus agent discretion. | **THEATRE (unenforced)** | Nothing withholds, so the law binds only when the agent chooses. | §5 proofs 1-4 |
| **F7** | The binding doc's *"Full reference"* pointer (`SOUL.md:358`) resolves to a file reading `F13 HOLD — awaiting Arif ratification`. Three copies of the law carry conflicting binding statuses. | **Provenance defect** | Any agent that reads the pointer and concludes the law is not ratified — i.e. obeys nothing. | `SOUL.md:358`; `forge_work/…:3`; `agents/makcikgpt/…:3` |
| **F8** | `care-governor.md:3` says `advisory only`, `:4` says `Binding`. Two lines, opposite claims. Its always-on every-turn wiring exists in the plugin but is **dead** because `/root/.hermes/lanes/lanes.yaml` does not exist — a blast-radius-every-turn control is one missing file from being live, unnoticed for 2 days. | **SELF-CONTRADICTORY + latent** | Nobody today; everyone the moment that YAML is restored. | `care-governor.md:3-4`; `G2-care-governor.md:41-45, 85-105`; live check |
| **F9** | Two different "DITING 6" dimension sets are published under one name (`SOUL.md:280-285` vs `:320-327`). | Documentation defect | A reader implementing "DITING" cannot know which 6. | `SOUL.md` lines cited |
| **F10** | `bangang_gate.py` decides human-vs-machine plane by **substring path match**, so a human-facing skill under a machine path (`bridge-protocol`) is classified machine. | **Measuring a proxy** | Scope decisions inherit a path typo. | `bangang_gate.py:29-30, 55-57` |

**NOT FOUND, stated plainly:** no artifact records a specific report in which an agent removed a quotation
*because* `voice_gate.py` went red. The pattern is **documented as a rule**
(`instrument-verification.md:61-82`) and **reproducible on demand** (§4.3), but the specific before/after
edit of the reported incident was not located on disk. The nearest on-disk instance of "verbatim text
altered to pass a word-matching gate" is `reports/apex-substrate-assessment-2026-09-12/SOURCE.md:5` — a
**different** gate, **fully disclosed** in the artifact.

---

## 9. What is genuinely good (reported because the audit demands it, not to balance the ledger)

1. **`voice_gate.py` refuses to fake what it cannot measure.** `Peace²`, `ΔS`, `RASA`, `Tension`, `Image` are declared judgment-only *in the output itself* (`:430-434`, `:399-402`). Most instruments in this class invent a score.
2. **The `--audience` flag is real, not decorative.** Measured `EXIT=1` vs `EXIT=0` on register-only violations. The half that was implemented works.
3. **Failure mode 6 is documented as uncatchable** (`references/voice-governor.md:150-168`), and the v3.0 ablation published a result **against its own interest**: *"All four replies scored PASS at exit 0. The linter could not distinguish the true-state reply from the transition-lie reply."* (`references/canonical-sources.md:95-99`). Honest instrumentation.
4. **`instrument-verification.md:61-82` is the best document in this audit.** It names the inversion, states the test in one falsifiable sentence, and prescribes the correct fix. It should be the template — and it is precisely the document that was not applied to the heat bank.
5. **`human-attention-membrane.md` is correctly scoped and needs nothing.** It constrains a channel, not a text, so it cannot displace evidence.
6. **`bangang_gate.py` explains its own plane rule** and exempts human-plane register explicitly (`:14-15`), with the sovereign's own words at the top of the file.
7. **The correction path is anti-deformation by design:** write beside the delivered artifact, leave your own false claim visible rather than quietly deleting it (`3b89a96ed`), record `SENT` not `DELIVERED` for want of a receipt (`e0b7add86`).
8. **The cooling rule is bounded** — `SOUL.md:351`: *"Iron rule: SABAR tak bypass substance — kalau substance betul, SABAR tak padam substance."* The doctrine anticipated the exact failure this audit found. **The prose knows; the instrument does not.**

---

## 10. The smallest repair that removes the damage (recommendation only — no file was changed)

Ordered by damage removed per line of code:

1. **Give `check_heat` the quote spans.** Pass `_quoted_spans(text)` into the heat-word loop (`:278-281`) and downgrade quoted hits to `INFO`, exactly as `find_bank` already does for every other bank. This alone makes §4.3's quotation case pass and closes F1 and F2. **~3 lines.**
2. **Move `check_heat` inside the audience branch** (`:476`). Internal mode should not carry a cooldown protocol addressed to an agitated human. If internal work needs a heat signal, it needs a *different* signal with an internal meaning. **1 line.**
3. **Move `ENTROPY_ADDERS` into the human branch**, or drop `MCP`/`SSOT`/`SOT`/`CI-CD` from the bank — they are the reader's own vocabulary for a machine reader. **1 line / 1 list edit.**
4. **`--audience internal` must not be usable as a lever to green a human-facing artifact.** The doctrine already says so (`instrument-verification.md:79-82`); that rule needs a mechanism, not a rule.
5. **One heat bank, one authority.** Retire `_makcik.py`'s `HEAT_LEXICON` in favour of importing the single bank, per `arifos-hermes-gate-hook.py:26-28`.
6. **Reconcile the three status lines** on the voice-governor copies and repoint `SOUL.md:358`.
7. **Reconcile `bangang`:** `SOUL.md:206` instructs the agent to treat that word as legitimate human register *and* `voice_gate.py:120` treats it as heat. Pick one. The current state tells the agent to listen and forbids it from reporting what it heard.

---

## 11. Measurement provenance

| Command (exact) | What it established |
|---|---|
| `python3 voice_gate.py --file /tmp/audit_quote.txt` | quoting the owner verbatim → `EXIT=2`, `heat word: bangang` |
| `… --file /tmp/audit_quote.txt --audience internal` | identical result → heat bank is audience-blind |
| `… --file /tmp/tech_receipt.txt --audience internal` | technical receipt → `WARN dS/jargon_proxy`, `WARN Gravity` |
| `… --audience internal --thermal` | `SABAR: TRIGGERED / heat word: bangang / EXIT=2` |
| `… --file /tmp/internal_audit.txt --audience internal --thermal` | `stupid`, `garbage`, `useless` → `SABAR: TRIGGERED`, `EXIT=2` |
| `… --file /tmp/quote2.txt --audience internal --thermal` | quoted `"bullshit"`/`"garbage"` as evidence → `EXIT=2` |
| `… /tmp/reg.txt` human vs internal | `EXIT=1` vs `EXIT=0` → audience flag is real for register |
| `… --file /root/AAA/reflections/2026-09-19-session-reflection.md` (both modes) | delivered human-facing artifact → `RE-DRAFT` / `EXIT=2` |
| `… --file /root/.hermes/SOUL.md --audience human` | the law's own source → `RE-DRAFT` / `EXIT=2` |
| `… --file ../SKILL.md` human vs internal | `EXIT=1` vs `EXIT=0` |
| `grep -n "_quoted_spans" voice_gate.py` | called once, at `:366`, human-only |
| `sed -n '476,497p' voice_gate.py` | `check_heat` sits outside the audience branch |
| bank-diff `HEAT_WORDS` vs `HEAT_LEXICON` | 15 vs 18 words, 9 shared |
| `grep -n -iE "voice\|register\|lint" arifos-hermes-gate-hook.py` | no match → no automatic caller |
| `readlink .git/hooks/pre-commit`; `ls -la /root/.hermes/lanes/`; `grep -rl voice_gate /etc/systemd/system` | no hook, no timer, no wrapper |
| `os.walk` + `getmtime` over `instructions/` + `canon/` | 304 total `.md`, 125 in last 7 days, 90 binding / 59 advisory / 156 no status |
| `git -C /root/AAA log --oneline -S'bangang'`; `--format="%B" \| grep -ci …` | commit-level trace of the word and the motto |
| `git show 397c090cf --stat`; `git log -1 --format="%B" bed9ad7cc 3b89a96ed` | authorship and reasoning of the v3.0 skill commit and the reflection corrections |

**Read-only compliance — measured, including the one side-effect.**

No governor, skill, doctrine or config file was opened for writing. Source mtimes before/after this
session:

```
2026-09-19 02:59:26  …/bridge-protocol/scripts/voice_gate.py   (unchanged — session started 10:46)
2026-09-17 15:21:32  /root/.hermes/SOUL.md                     (unchanged)
2026-09-17 22:52     /root/AAA/instructions/care-governor.md    (unchanged)
```

**One side-effect, disclosed:** executing `voice_gate.py` with `--json` caused CPython to write
`scripts/__pycache__/voice_gate.cpython-313.pyc` (mtime 10:52:22). That is interpreter bytecode, not a
source edit — `voice_gate.py` itself was not modified. (`/root/AAA/instructions/story-as-drift-vector.md`
also changed mtime at 10:53:35; that is a **sibling audit job**, not this one — no file under
`instructions/` was written by this job.)

The only document this session wrote is this report.
