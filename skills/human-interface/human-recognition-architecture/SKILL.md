---
name: human-recognition-architecture
description: "Use when verifying a person from photos or video."
version: 1.0.0
owner: AAA
category: human-interface
tags: [identity, biometric, recognition, physique, topography, consent, vision, f2, f9]
floor_scope: [F1, F2, F6, F9, F11, F13]
autonomy_tier: T1
capability_tier: fed-multimodal-vision
ecology_state: WARM
---

# Human Recognition Architecture

How this federation answers "is this the person?" and "how has this person's body changed?" without
ever letting a body — or a scene — become a name.

Applies to inbound recognition: a shared photo or video that may contain a known person, and to
modelling a person's body so a future image can be corroborated against it.

## Rule 0 — two stores, never one

|  | Identity store | Topography store |
|---|---|---|
| Question | "Is this the consenting person?" | "What is this body doing / how has it changed?" |
| Anchors | face template + name + history + relations | pose-normalised bone ratios |
| Permanence | name/history/relations permanent; biometric rented (TTL'd) | state drifts weekly; invariants drift over years |
| If wrong | names the wrong human — worst possible outcome | mis-describes a body — recoverable |
| Power | may assert identity, under quorum | **corroborate only, never assert** |

If the two merge, every gym photo becomes a name. A body is the least permanent thing about a person
(it moves with cut/bulk, pump, flexion, clothing, lens and viewpoint) so it must never carry the
identity load. The permanent load belongs to **name + history + relations**, which do not expire; the
biometric witness is rented and TTL'd.

**Identity never inherits by association.** Context priors set the *candidate list*; only an anchor
comparison against a registered reference produces a name. A confident read on photo A does not
transfer to photo B — not same day, not same scene, not same group. When there is no anchor match, or
no consent on file, say "aku tak pasti siapa". A wrong name is worse than no name.

## The recognition pipeline (order matters)

```
media ingest → frames + contact sheet
  → person detection
  → consent / enrolled-subject scope check      ← BEFORE any template extraction
  → quality assessment
  → modality extractors (face | pose | silhouette | gait)
  → modality-specific comparison
  → gated decision + uncertainty + audit event
  → verdict: verified | probable | insufficient_evidence | no_match
```

Every modality contributes an **estimate plus its uncertainty plus its acquisition conditions**. A
similarity number without provenance is not comparable to the same number measured another way.

## Gates (binding)

1. **Consent before template.** No enrolment, no comparison, for any third party. Check the consent
   scope and the enrolment record before reaching for any reference-image flag — a flag that exists
   is not an authorisation to use it.
2. **No 1:N, ever.** Verify a known, consenting subject. No population search, no scraping, no name
   inference from an image alone.
3. **Abstain upward.** Occlusion, foreshortening, poor framing or missing coverage → return
   `insufficient_evidence`. Never estimate through a gap; an abstention is a valid answer.
4. **No single witness is authority.** Quorum ≥3. A mismatch between modalities escalates —
   never resolves silently toward the more confident-looking signal.
5. **Templates, not photos.** Store derived values + provenance; delete raw media after extraction
   unless the subject explicitly wants an archive.
6. **Human veto stands.** Recognition output is a recommendation; the irreversible decision (acting on
   an identity, enrolling, deleting) is the sovereign's.

## Face is a witness, not the whole court

A face read is the most discriminative *controlled* modality and the right first choice — but it is
one witness among several, not a god-mode signal. Do not let a high-confidence face score silently
override a contradicting modality; that is a mismatch, and mismatches escalate.

Reserve the strongest warnings for the failure that thresholds cannot fix: **scene pattern-matching**.
Backstage + tan + muscular + the right group screams a name and is routinely wrong. No threshold
value catches that, because the error happens before any comparison runs.

## Scale-relative, not absolute

Model relations, not pixels. Normalise every detection before measuring: translate to a body-local
origin, rotate to a canonical axis, and divide by a **robust** scale reference. Absolute pixel widths
and apparent heights are meaningless across distance, crop and resolution.

Full recipe, the invariant catalogue, the coverage-group rule and the implementation traps:
`references/physique-topography-invariants.md`.

## Verifying a recognition claim before you make it

- **Read the metadata, not just the pixels.** A name in a title or an on-screen caption is a *source
  claim*, not your identification. Say where the name came from — "the video names itself" is honest;
  presenting it as a face match is not.
- **Report which modality actually carried the verdict.** A visual-only read is not a face match.
- **Beware a text lane masquerading as speech** — a fabricated transcript beside real frames can
  contaminate a recognition claim. Check the transcript actually came from speech.
- **Re-check before naming, every single time.** The cost of a pause is zero; the cost of a wrong name
  is the trust in every future call.

## Related

| This skill | Other skills |
|---|---|
| Inbound recognition + body modelling | `image-identity-transfer` — outbound generation, preserving a face in a render |
| The comp-circuit and person-ID workflow for physique subjects | `malaysian-physique-circuit` (user-owned; `person-id-workflow.md` is its ID procedure) |
| Where a subject's private record lives | `relationship-memory-isolation` |

DITEMPA BUKAN DIBERI.
