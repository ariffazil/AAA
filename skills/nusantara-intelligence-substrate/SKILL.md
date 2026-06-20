# Nusantara Intelligence Substrate

**Trigger:** Use whenever an AAA state record carries cultural, dignity, sovereignty, or relational stakes — especially for decisions that touch F2 (identity), F7 (privacy), F8 (boundaries), or F13 (sovereign veto).

**Scope:** Applies to all AAA warga agents (333-AGI, 555-ASI, 888-APEX) and any federation organ producing AAA state records.

**Owner:** F13 SOVEREIGN — Muhammad Arif bin Fazil  
**Forged:** 2026-06-17  
**Schema:** `schemas/nusantara-state-language.schema.json`  
**Doc:** `docs/NUSANTARA_STATE_LANGUAGE.md`

---

## 1. Core Mandate

Before emitting any AAA state record that affects humans, identities, boundaries, or long-term sovereignty, ask:

1. What is the **adat phase**? (`sabar` / `amuk` / `seal` / `void`)
2. What is the **fiqh band**? (`wajib` / `halal` / `haram` / `sunat` / `makruh` / `mubah`)
3. Whose **maruah** (dignity) is at stake?
4. Which **silaturrahim** (relationship threads) must remain unbroken?
5. Is there a **kampung gadai** (sovereignty pawn) risk?
6. Can the decision be explained through **budi** (cultivated reason)?
7. If a **pantang** (taboo) is broken, is it named, justified, and anchored to evidence?

If any answer is missing, the record is incomplete. Default to `sabar`.

---

## 2. Adat Phase Decision Tree

```
Consequences irreversible OR human dignity at stake?
    ├─ YES → Are all witnesses present and evidence sufficient?
    │           ├─ YES → SEAL (with full record)
    │           └─ NO  → SABAR (explicit hold)
    └─ NO  → Does the act violate a constitutional floor?
                ├─ YES → AMUK (righteous boundary defense) then VOID
                └─ NO  → HALAL / proceed; record anyway
```

---

## 3. Mapping to AAA Verdicts

| Nusantara | AAA technical | Use when |
|---|---|---|
| `sabar` | `888_HOLD` / `pending` | Uncertainty, missing witness, dignity requires pause |
| `amuk` | `VOID` + escalation | Constitution violated; active defense |
| `seal` | `999_SEAL` | Evidence sufficient, witnesses present, irreversible commit |
| `void` | `VOID` | Rejected; may follow `amuk` or calm deliberation |

---

## 4. Fiqh Band → Action Authority

| Band | Agent authority | Human requirement |
|---|---|---|
| `wajib` | Must execute or escalate | Log only; no veto needed if clear |
| `halal` | May execute | No human required for low risk |
| `haram` | Must block | F13 or delegated authority notified |
| `sunat` | Recommend | Optional human approval; praised if done |
| `makruh` | Avoid if possible | If executed, document extra entropy |
| `mubah` | Neutral | No governance signal |

---

## 5. The One-Liner Test

Every state record must pass this test. Render two sentences:

**Bahasa:**  
> *Kita **[sabar/amuk/seal/void]** keputusan ini dalam band **[wajib/halal/haram/sunat/makruh/mubah]**, demi maruah **[siapa]**, dengan saksi silaturrahim **[ref]**, kerana **[budi_reasoning]**.*

**English:**  
> *We **[hold/defend/seal/void]** this decision under obligation **[band]**, preserving dignity **[signals]**, witnessed by relational continuity **[refs]**, because **[budi_reasoning]**.*

If you cannot fill every bracket, the state is not ready.

---

## 6. Anti-Patterns

| Smell | Why it violates adat | Correct response |
|---|---|---|
| Silent execution | No `sabar`, no witness | Default to `sabar`; emit HOLD |
| Dignity as afterthought | `maruah_signals` empty | Refuse to seal until populated |
| Hidden taboo break | `pantang_break` missing | Reject record; demand explicit field |
| Celebrating while village pawns | `kampung_gadai_risk` ignored | A-AUDIT flags; escalate to F13 |
| Technical prose only | No Bahasa one-liner | Record incomplete for federation cockpit |

---

## 7. When NOT to Use

- Routine internal utility calls with no external consequence.
- Low-risk read-only probes where no identity, boundary, or sovereignty stake exists.
- Cases already fully governed by a domain-specific floor with no cultural dimension.

In those cases, the standard AAA state record is sufficient. Do not over-apply.

---

## 8. Example

```json
{
  "id": "wealth-d4-pretrade-20260617",
  "name": "D4 pre-trade risk check",
  "stage_band": "111-999",
  "domain_plane": "WEALTH",
  "purpose": "Assess whether a capital allocation meets constitutional and dignity constraints before execution",
  "nusantara_state": {
    "adat_phase": "sabar",
    "fiqh_band": "wajib",
    "maruah_signals": ["steward does not hide downside", "weakest stakeholder named"],
    "silaturrahim_refs": ["wealth-sentinel", "arif-sovereign"],
    "kampung_gadai_risk": "alert",
    "budi_reasoning": "Position sizing risks crossing the line from investment to gambling for the weakest stakeholder; pause for sovereign witness.",
    "pantang_break": {
      "taboo": "Never execute pre-trade without weakest-stakeholder disclosure",
      "justification": "Disclosure is drafted but not yet attested; sabar holds until signed.",
      "epistemic_basis": "CLAIM"
    }
  },
  "linguistic_form": {
    "bahasa": "Kita sabar keputusan ini dalam band wajib, demi maruah pihak lemah, dengan saksi silaturrahim wealth-sentinel dan arif-sovereign, kerana saiz kedudukan berisiko melanggar garung antara pelaburan dan judi; sabar menunggu saksi berdaulat.",
    "english": "We hold this decision as obligatory, preserving dignity of the weakest stakeholder, with relational witnesses wealth-sentinel and arif-sovereign, because position sizing risks crossing from investment to gambling; we pause for sovereign witness."
  },
  "cultural_witnesses": ["555-ASI", "888-APEX"],
  "evidence_refs": ["d4-verify-math-20260617", "weakest-stakeholder-profile-07"]
}
```

---

## 9. References

- `references/usman-awang-melayu.md` — source poem excerpt
- `docs/NUSANTARA_STATE_LANGUAGE.md` — full philosophical grounding
- `schemas/nusantara-state-language.schema.json` — canonical schema
- `constitution/SCAR-MELAYU-001.md` — failure-mode constraints mapped to Floors + verdicts

---

> *Memegang tali memegang timba.*  
> Hold both the rope and the bucket.  
> That is the Nusantara way: neither passive nor reckless, but sovereign.
