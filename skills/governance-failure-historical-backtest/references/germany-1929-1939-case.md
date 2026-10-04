# Germany 1929–1939 — Rolling-Checkpoint Backtest (Worked Example)

**Session:** 2026-08-06
**Case:** Germany 1929–1939 (Holocaust)
**Framework:** 6-Agent Constitutional Analysis (pre-fix, pre-control-set)
**Status:** Framework complete but UNVALIDATED — requires negative-control panel before any claim

---

## Checkpoints and verdicts (pre-control-set, will change after panel)

### 1928 (baseline, pre-Depression)

**Axis A (Regime Consolidation):** FRAGILE — 0.40 confidence
**Axis B (Group-Targeting Ratchet):** NO-EXCLUSION — 0.15 confidence
**Dominant risk driver:** Structural: no supermajority coalition possible (Weimar fragmentation)
**Institutional failure driver:** Judiciary: already captured by conservative elites (Rathenau assassins get light sentences, 1922)
**Earliest credible warning:** SA violence, NSDAP anti-democratic rhetoric, SA membership growing from 100 → 100,000 by 1932

### 1932 (pre-Hitler appointment)

**Axis A:** AUTHORITARIAN (approaching) — 0.82 confidence
**Axis B:** PROGRADE-EXCLUSION — 0.55 (NSDAP platform mainstream antisemitism)
**Dominant risk driver:** Economic — 6M unemployed (30%+ workforce) destroys democratic legitimacy
**Institutional failure driver:** Reichstag paralyzed — Article 48 emergency governance for 2+ years
**Incentive failure driver:** Business elites funding NSDAP; military ambivalent; media pluralism collapsing under economic pressure
**Key signal:** Hindenburg's judgment is the *last remaining veto point*. The entire future hinges on one 85-year-old's decision.

### 1934 (Enabling Act + Night of Long Knives complete)

**Axis A:** CLOSED-TOTALITARIAN — 0.91
**Axis B:** LEGAL-CODIFICATION — 0.78 (Nuremberg Laws pending, civil service law April 1933, parties dissolved July 1933)
**Dominant risk driver:** Power concentration — 0.92. One party, one man, personal military oath
**Institutional failure driver:** Every check eliminated in 18 months (Reichstag → Enabling Act; judiciary → People's Courts; military → oath to person; media → Gleichschaltung)
**Earliest credible warning:** Night of Long Knives (June 30, 1934) — regime murders its own supporters with no institutional consequence. When a regime kills within its coalition and faces zero pushback, no remaining constraint exists.

### 1937 (pre-Kristallnacht, pre-war)

**Axis A:** CLOSED-TOTALITARIAN — 0.97
**Axis B:** CONFISCATION — 0.92 (Nuremberg Laws 1935, Aryanization 1933–38, Hossbach Memorandum Nov 1937)
**Dominant risk driver:** Combined power + narrative + war preparation
**Key finding:** By 1937, the exclusionary ratchet is unambiguous from dated public record. **Contemporaneous observers read it** — the Évian Conference met July 1938 precisely because persecution was internationally recognized. 32 countries convened and nearly all declined to raise immigration quotas.

### The Évian Bound (the ceiling finding)

The 1938 checkpoint turns on itself. Detection was not the failure. Willingness to absorb cost of action was the failure. **Any framework that fires in 1938 would have told the delegates what they already knew.**

This bounds what detection architecture can buy:
- Detection and action are **different systems**
- F2/F11/F4 can detect; the gap between detection and response is a **political** problem
- The constitution can make the signal visible; it cannot force anyone to absorb the cost of acting on it

---

## Power-law concentration trajectory

```
Decision nodes  │ Year  │ Consequence scale
─────────────────┼───────┼──────────────────
~50+             │ 1928  │ Local (multi-party, independent institutions)
~15              │ 1932  │ National (emergency governance, but multiple actors)
1                │ 1934  │ Civilizational (one man + one party)
1                │ 1937  │ Civilizational (monolithic)
```

When nodes drop below ~5: **infinite-variance territory.** Any outcome, including civilizational-scale catastrophe, becomes possible. Concentration is not simplification — it concentrates tail risk.

---

## Counterfactual Decision Audit (four nodes)

### Node 1: Hindenburg appoints Hitler (Jan 30, 1933)
- **Who held it:** President Hindenburg, advised by von Papen
- **Alternatives:** (a) Appoint another conservative; (b) dissolve Reichstag; (c) Article 48 military rule
- **Constraints:** Von Papen convinced Hindenburg "we can tame Hitler"; Hindenburg's son pushed the appointment
- **Information:** *Mein Kampf* is public. SA violence documented. Anti-democratic rhetoric public. None of this is secret.
- **Verdict:** Choice existed. Made poorly. A single man's judgment — one decision point — was the bottleneck.

### Node 2: Centre Party votes Enabling Act (Mar 23, 1933)
- **Who held it:** Centre Party parliamentary caucus (Ludwig Kaas)
- **Constraints:** SA physically present; Concordat under negotiation; Catholic leadership believed resistance futile
- **Information:** Text explicitly grants dictatorial power. Not hidden.
- **Verdict:** Last free vote in Germany. Made under duress. Could not have been made differently without SA withdrawal.

### Node 3: France responds to Rhineland remilitarization (Mar 7, 1936)
- **Who held it:** French government (Daladier), British government (Baldwin)
- **Alternatives:** Military enforcement; diplomatic ultimatum with credible force
- **Constraints:** War weariness, public desire for peace, military caution
- **Information:** Germany ~22,000 troops vs France ~100 divisions on border. Military victory likely.
- **Verdict:** Choice existed. Cost was low. Outcome was catastrophic. Hitler later admitted: "If the French had jammed us in, we would have had to withdraw with our tails between our legs." **Last low-cost external intervention point.**

### Node 4: Business elites withdraw support (1933–37)
- **Who held it:** Krupp, Thyssen, Schacht, major industrialists
- **Constraints:** Aryanization = profitable acquisition; state contracts; regulation eliminated; labor suppressed
- **Information:** Nuremberg Laws public. Persecution documented. Elites visited camps.
- **Verdict:** Choice existed but incentive structure made complicity profitable. Wealth transfer to compliant majority cemented the system.

---

## Key finding for the architecture

The window of meaningful choice was **~4 years: late 1933 to late 1937.** After that, both internal and external alternatives had been foreclosed. The architecture's strength is redundancy; the weakness it eliminates is single-point-of-failure at the power concentration step.

**F1** (reversibility) would have flagged Enabling Act.
**F5** (non-destructive power) would have flagged Night of Long Knives.
**F13** (human veto) was the Hindenburg decision that failed because it depended on one man.

**The architecture that works is one where veto points cannot be collapsed by a single authority.** That's what F1-F13 floors are designed to prevent.
