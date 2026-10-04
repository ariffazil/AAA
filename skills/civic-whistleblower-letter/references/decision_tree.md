># Send vs Hold vs Correct-and-Resend — Decision Tree

When the user wants to send a civic whistleblower letter, this is the decision flow.

## Step 0: Emotional State Check

```
Is the user in emotional crisis? (panic attack, "I want him to die", incoherent)
  -> YES: Apply rage-to-grace pathway. STOP. Do not proceed to Step 1 until calm returns.
  -> NO: Continue.
```

## Step 1: Evidence Audit (Hard Gate)

Before writing ANY letter, verify every claim against primary sources.

```
Does every claim trace to a public, auditable source?
  -> NO:  HOLD. Identify the gap. Do not write around it.
  -> YES: Continue.

Are there claims that can be falsified by a 30-second Google search?
  -> YES: HOLD. Remove or rewrite. (Common examples: "no inquiry happened",
          "Shell and BP didn't cut jobs", "PM made no statement on X".)
  -> NO:  Continue.

Is the baseline defensible?
  -> NO (baseline shopping detected): REWRITE. Measure from a defensible
          anchor (appointment date, peak, average) and explain the choice.
  -> YES: Continue.

Is there independent external audit available?
  -> NO:  RUN external audit (delegate_task or apex-judge isolate with full evidence).
          Do not self-judge.
  -> YES: Continue.
```

## Step 2: Framing Check

```
Does the letter name individuals with moral labels (devil, corrupt, evil)?
  -> YES: REDIRECT. Apply the Three Hands pattern. Name offices, not individuals.
          The holders may be named for F11 AUDITABILITY but not labeled morally.
  -> NO:  Continue.

Does the letter contain geopolitical analogies or inflammatory metaphors?
  -> YES: REWRITE using tersurat/tersirat. The reader must connect dots,
          not be told by the author.
  -> NO:  Continue.

Does the letter have a single, specific, measurable request?
  -> NO:  REWRITE. "Declare publicly when dividend extraction rate exceeds 65%"
          is a request. "Stop being corrupt" is not.
  -> YES: Continue.

Does the letter identify the audience as ONE specific MP or committee?
  -> NO:  REDUCE distribution. Send to 1-4 recipients, not 99.
  -> YES: Continue.

Does the letter contain the author's identifying information in the visual or footer?
  -> YES: STRIP. Replace with anonymous attribution ("Seorang Warganegara Malaysia").
          Remove GitHub URLs, model names ("Hermes ASI"), and any path that
          de-anonymizes within 4 clicks.
  -> NO:  Continue.
```

## Step 3: ZKPC Visual Check

```
Does the letter contain a cryptographic seal (SHA-256 + Merkle root)?
  -> NO:  ADD. Use templates/zkpc_visualization.py. Every data row needs a hash.
  -> YES: Continue.

Are the hashes computed from the SAME data shown in the letter's tables?
  -> NO:  RECOMPUTE. The hashes must match the visible data, not paraphrased numbers.
  -> YES: Continue.

Is the Merkle root displayed prominently?
  -> NO:  PROMOTE. The root should be visible to anyone glancing at the letter.
  -> YES: Continue.
```

## Step 4: Apex-Judge Pre-Publish Gate

```
Has apex-judge isolate been run on the FINAL letter content + ZKPC seal?
  -> NO:  RUN apex-judge isolate. Cite receipt.
  -> YES: Continue.

What was the verdict?
  -> VOID:    DO NOT SEND. Roll back, fix, re-isolate.
  -> HOLD:    Wait for F13 disposition. If user is F13, ask for explicit approval.
  -> SABAR:   Proceed with caveats.
  -> SEAL:    Continue to Step 5.
```

## Step 5: Final Send Decision

```
Is the user (F13) explicitly directing send?
  -> NO:  Present the final draft + apex receipt + ZKPC seal summary.
          Wait for explicit F13 approval. Do not auto-send.
  -> YES: Confirm recipient list (1-4 max), then send.

Has the user been informed of remaining risks?
  -> NO:  Inform. The risks are: career action, legal exposure, no impact if
          letter is dismissed. These must be on record before send.
  -> YES: Send. Log to VAULT999 with seal.
```

## Step 6: Post-Send

- Log to VAULT999 with full provenance
- Save HTML + PDF to forge_work/<date>-civic-letter-<topic>/
- If media picks up, prepare neutral fact-sheet (not the letter itself)
- Watch for institutional response (7-14 days)
- Document in carry_forward.json: status, recipient responses, observed impact

## When to HOLD (not send)

HOLD if any of these is true:

- Evidence audit reveals uncorrectable gaps
- User is in ongoing emotional crisis
- Letter contains personal attacks that cannot be reframed
- Apex-judge returns HOLD or VOID
- Distribution would be mass-blast (>5 recipients)
- Author identity is exposed in the visual or footer
- Single specific measurable request is missing
- No primary source for any major claim

## When to RESEND (correct and try again)

RESEND (new draft, new send) if:

- External audit identified specific false claims
- User provided additional verifiable evidence
- Apex-judge returned SABAR with fixable issues
- Letter was framed as personal attacks but can be reframed as institutional

Do NOT resend the same letter with minor edits. The audit findings must be substantively addressed.

## When to NEVER SEND

NEVER SEND if:

- User wants to attack individuals with moral labels AND refuses to redirect
- User is unable to verify the data with primary sources
- User wants to mass-blast 50+ recipients
- User wants to use the letter as political weapon against PM/cabinet without specific policy evidence
- Apex-judge returns VOID after corrective iteration
- The evidence base is fabricated or cannot be sourced