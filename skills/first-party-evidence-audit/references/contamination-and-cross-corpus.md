# Contamination and Cross-Corpus Counting

Topical depth for `first-party-corpus-audit`. Load when prior narratives exist, or when more than one
corpus is in play.

## The contamination vectors

A narrative can enter an audit from four directions. Grade every one of them before using anything:

| Vector | What it looks like | Treatment |
|---|---|---|
| **Fiction** | a persona bible, roleplay bible, character sheet, generated dialogue | craft material. Never evidence about a person. |
| **Population literature** | psychology/sociology research offered as explanation for one individual | framing only, with a causal clause or `ASSOCIATION_ONLY`. Cannot speak to an individual. |
| **Agent synthesis** | a summary or map an earlier session wrote *from* the same corpus | an object of the audit, not an input. Label it as such in the corpus inventory. |
| **Generated media** | synthetic images/audio living beside real ones in an archive | mark as generated in the inventory so they are never counted as records. |

## The feedback loop to look for

```
fiction or literature
   → agent synthesis
      → stored in a private lane as if it were a finding
         → read as evidence by the next session
            → promoted to "fact"
```

Once a synthesis document sits in the same directory as real evidence, later readers cannot tell them
apart by position. Countermeasure: **every synthesis artifact carries its provenance and its status in
its own header** — what it was derived from, that it is synthesis, and what it must not be used for.
Keep a one-line corpus inventory at the top of each audit that separates first-party sources from
synthesised ones.

## The recurring mechanism

Fiction and population literature frequently share a **shape**, and a shape that fits two sources
feels confirmed. The trap is then reading that shape back onto a real person as biography. Name the
mechanism explicitly in the deliverable when you find it — naming it is what stops the next session
repeating it.

## Cross-corpus counting rule

A multi-corpus audit reliably produces sections that are individually true and collectively
contradictory (*"never says X"* beside *"both have said X"*). Usually the cause is an unlabelled scope
qualifier.

**Every count must carry four things in the same sentence: corpus · exact token · speaker · addressee.**

- Which corpus, with its date range.
- The literal token, not a paraphrase of it (an affection word translated into "affection" loses the
  distinction that matters).
- Who said it.
- Who it was said to — and whether the addressee is one person, a group, or unresolved.

A line addressed to two people is not an exclusive declaration to one of them. A line addressed to a
room is not a line addressed to a person. **An unresolved addressee is `UNKNOWN`, not an inference.**

Paragraph-level scope ("since <month>", "in this window") does not survive being read next to a
section heading — if the scope matters, it belongs in the clause, not the paragraph.

## Reporting a correction

When an internal contradiction is found — by you, by a reviewer, or by the user:

1. Re-verify against the corpora **before** amending, and show the verification table.
2. Amend **append-only**, in a dated amendment: state the defect, the corrected figure, and the
   generalisation that prevents a recurrence.
3. Withdraw the specific sentence that was wrong, explicitly, rather than leaving it standing beside
   the correction.
4. If the defect invalidates a downstream statistic, mark the downstream figure as superseded in the
   same amendment.
