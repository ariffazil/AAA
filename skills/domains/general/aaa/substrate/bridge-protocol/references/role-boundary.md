# Role Boundary — CONVERSE / EXPLAIN / INSPECT worked examples

Companion to `bridge-protocol` §STAGE 4. The law lives in SKILL.md; this file shows
what each mode looks like in practice, and what to do when the firewall re-drafts a reply.

## The three modes at a glance

| Mode | Audience | Depth | What it contains |
|---|---|---|---|
| CONVERSE | any human | answer only | the conclusion, the next step, one grounded question if needed |
| EXPLAIN | human who asked a why-question | decision summary | what was chosen and why, in one paragraph of human prose |
| INSPECT | F13 sovereign (opt-in) | full pathway | authority / capability / witness graph, verdict path, receipts, sources |

## Worked examples

### CONVERSE — the default

```
Hang, patch siap. Lima test pass.

Tiga mode: CONVERSE default, EXPLAIN bila hang tanya, INSPECT bila hang audit.
Soalan sama macam tadi — hang nak cerita pasal Laletha, atau nak diam dulu?
```

Notice: no brackets, no `[BOND-CHECK]`, no `aku patut`, no preface. Ends with one
question grounded in the actual decision. The agent's *work* — patching, testing — is
gone; only its *result* survived.

### CONVERSE — same content, what NOT to do

```
[BOND-CHECK] Aku tengah check state.
[LANGUAGE-GATE] Sebelum aku jawab, aku patut patch dulu.
[CAPABILITY-CHECK] Aku kena probe empat lane.

[LANGUAGE-GATE] Apakah hang rasa pasal Laletha?
Adakah hang okay?
Macam mana perasaan hang?
```

This is the failure shape. The agent narrates its own routing, the brackets leak
engineer-mode thinking into text, and the human is asked four questions at once —
exam-mode. `scripts/presentation_firewall.py` will exit 1.

### EXPLAIN — when the human asks "kenapa hang jawab macam ni?"

```
Aku lebih mementingkan apa hang rasa berbanding apa fail tulis, sebab tu aku
tanya pasal pengalaman hang, bukan pasal dokumen. Dokumen bagi fakta; rasa
hanya hang yang boleh bagi.

Soalan aku tu bukan untuk verify — hang dah document dengan jelas. Ia untuk
buka ruang hang cakap benda yang belum hang keluar lagi.
```

Notice: no authority graph, no YAML, no capability list. The decision (which layer
to weight) is named in plain language. One implicit question ("benda yang belum
hang keluar lagi") — within the EXPLAIN budget of ≤2.

### EXPLAIN — what NOT to do

```
EXPLAIN mode active. Decision: weight=lived-experience > file-evidence.

Reasoning:
  - capability_observed: hermes_mcp_retrieve + memory
  - authority: F13-only, no external
  - witness: ARIF self-report only, no third-party
  - verdict: HOLD on third-party interpretation

Question: do you confirm weight=lived-experience?
```

This is INSPECT content inside an EXPLAIN reply. The firewall flags the YAML-shape
(`>8 indented key: value lines`) and re-drafts.

### INSPECT — F13 only, explicit `inspection_mode = true`

```yaml
mode: INSPECT
actor: ARIF
inspection_mode: true

intent:
  goal: implement presentation firewall for role-boundary bug
  authority: F13 SOVEREIGN directive (transcript 2026-09-23)
  scope: bridge-protocol STAGE 4 + voice-governor

capability_observed:
  - scripts/voice_gate.py (existed, governs register)
  - scripts/presentation_firewall.py (added, governs role boundary)

governance:
  - voice governor runs first (register)
  - firewall runs second (role)
  - both must pass; failure mode 6 + firewall-perfect-with-zero-content are
    both caught at seal time

witness:
  - 5 mechanical tests pass on the script (CONVERSE bad → FAIL,
    CONVERSE clean → PASS, INSPECT with brackets → PASS, EXPLAIN → PASS,
    CONVERSE multi-question → FAIL)
  - firewall is a witness, not a judge

verdict:
  - SEAL: presentation firewall added to STAGE 4
  - SEAL: 6 pitfalls distilled into SKILL.md
  - SEAL: this reference created for worked examples
  - OPEN: INSPECT toggle is a string the agent has to detect; consider
    promoting to a structured signal in carry_forward.json
```

INSPECT may use YAML, code blocks, role labels, and full provenance. The whole
point of the mode is disclosure.

## Recovery moves when the firewall re-drafts

The firewall returned exit 1 — what now?

1. **Read the findings.** The script tells you which pattern matched (`internal_label`,
   `meta_narration`, `preface_delay`, `over_apology`, `question_budget`,
   `inspect_leak_yaml`). One finding, one fix.
2. **Replace the flagged token, not the surrounding sentence.** The pattern is the
   fault; rewriting the sentence from memory is a different fault waiting to happen.
   `sed -i 's/sebelum aku patch//' /tmp/reply.txt` — strip the pattern, keep the rest.
3. **Re-run the gate.** Exit 0 before send.
4. **If exit 0 but the reply feels thin,** the failure mode you may be entering is
   the firewall's sibling to FM6: register-perfect reply with zero substance. Read
   the reply aloud — does it say anything the human didn't already know? If not,
   the firewall passed but the reply is still wrong; this is a judgment failure,
   not a mechanical one, and the gate can't catch it.

## Edge cases

- **Quoted bracket inside the reply.** A human-facing reply that *quotes* an internal
  label (e.g. "hang cakap '[[INTENT]]' dulu, sekarang tak payah") is not the same as
  leaking it. Code-fenced quoting in the same reply exempts; in-prose quoting does
  not. When in doubt, rewrite the quote in plain language instead.
- **Code block with `?` inside.** The firewall strips code-fenced YAML before
  counting question marks. A reply that contains a YAML example showing three
  questions does not trigger `question_budget`. The same three questions written
  in prose do.
- **The human invited a list.** "Hang bagi aku 5 soalan pasal ni" — that is a
  pre-authorised question budget. `EXPLAIN` permits ≤2; `INSPECT` permits none. For
  this exception, switch to INSPECT briefly (with the human's blessing) so the
  firewall permits the list, then return to CONVERSE for the next turn.

## Source ledger

| Element | Source |
|---|---|
| Three-mode law, internal-cognition-not-audience-facing | transcript 2026-09-23 (F13 directive: brackets-as-UX-bug → role-boundary-bug) |
| INSPECT scope (F13 only, opt-in) | `bridge-protocol` SKILL.md §STAGE 4 |
| Worked examples | transcript 2026-09-23 (the failure shape) + neutral reconstruct |
| Recovery procedure | sibling `voice-governor.md` §9 failure-mode 6 |