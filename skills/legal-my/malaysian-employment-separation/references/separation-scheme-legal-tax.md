# Separation Schemes, Retrenchment Benefits and Termination-Payment Tax — Malaysia

Depth notes for `malaysian-employment-separation`. Not legal or tax advice — this is the rule set
with its conditions, so that the person can be told what to verify and with whom.

## 1. Statutory framework — exact wording

**Employment (Termination and Lay-Off Benefits) Regulations 1980**, made under s.60J Employment
Act 1955 (amended since; check currency).

Reg 6(1) — the minimum, verbatim in substance:

> the amount of termination or lay-off benefits payment to which an employee is entitled in any
> case shall not be less than —
> (a) ten days' wages for every year of employment under a continuous contract of service … if he
> has been employed by that employer for a period of less than two years; or
> (b) fifteen days' wages for every year of employment … if he has been employed by that employer
> for two years or more but less than five years; or
> (c) twenty days' wages for every year of employment … if he has been employed by that employer
> for five years or more,
> and pro-rata as respect an incomplete year, calculated to be nearest month.

Reg 6(2) — a day's wages is the average **true** day's wages over the 12 completed months'
service immediately preceding the relevant date.

Reg 3(1) — entitlement requires a continuous contract of not less than 12 months ending with the
relevant date (gaps totalling 30 days or less aggregate).

Reg 4 — **no** benefits where the termination is by reason of retirement age under the contract,
misconduct after due inquiry, or **voluntarily by the employee**. This is the regulation behind
the "never resign" rule.

Reg 4(2)–(3) — no benefits where the contract is renewed or the employee re-engaged on
not-less-favourable terms taking effect immediately, or where such an offer was made at least
7 days before the effective date and unreasonably refused. Prior service still counts toward a
later termination.

Reg 6(4) — benefits are **in addition to** notice or pay in lieu.

Reg 11 — payment due within 7 days after the relevant date; failure is an offence.
Reg 12 — employer must give a written statement of the amount and how it was calculated.
Reg 13 — disputes go through the Labour Department / Director General route.

**Coverage carve-out (verify against current law).** Since 1 January 2023 the Employment Act
applies to all employees, but employees whose monthly wages **exceed RM4,000** are excluded from
s.60J — i.e. from the termination/lay-off minimum these Regulations implement. Manual-labour
employees remain covered regardless of wage. For a professional above the line, the minimum is
not the floor. Unfair-dismissal protection is a **separate statute** (Industrial Relations Act)
and does apply regardless of wage — do not conflate the two.

## 2. Tax — compensation for loss of employment

**Rule.** Exempt: **RM10,000 for every completed year of service** with the same employer or with
companies in the same group, for terminations on or after 1 July 2008 (RM6,000 for 1 July 2008
back to 2003; lower again before that). Chargeable to the extent it exceeds the cap.

**Worked behaviours worth knowing:**
- The exemption is **restricted to the amount received.** A payment below the cap is wholly exempt.
- **Completed** years only — 11 years 3 months counts 11; 12 years 10 months counts 12.
- Aggregation across group companies applies where service continues through a change of employer
  entity and management/control substantially remains with the same persons.
- Ill health: **full** exemption where the Director General is satisfied the payment is on account
  of loss of employment due to ill health, certified in writing by a Medical Board.
- **Directors:** the exemption does **not** apply to a payment by a controlled company to a
  director who is not a full-time service director — such compensation is fully taxable. Ordinary
  employees are unaffected.

**Characterisation.** The characteristics and nature of the payment prevail over its form and
label. A sum that is in substance a gratuity for past services is assessed as a perquisite and
loses the exemption; a lump sum paid on premature termination of an employment with a prospect of
continuing to retirement age is compensation. For a mid-career exit under a downsizing scheme the
compensation characterisation is the natural one — but it is a factual determination. Read how
the scheme computes the payment (a years-of-service formula reads as compensation; a long-service
recognition payment does not) and have the characterisation stated in the document.

**Timing.** Taxed in the year of **receipt**; a negotiated settlement is deemed received on the
date it was concluded and signed, an award on the date of the order. Malaysia assesses
individuals on a calendar/current-year basis. **No mechanism to spread or apportion** the payment
or the exemption across tax years was found in the ruling or the guidance — treat "there may be a
way to split it" as false until a licensed agent shows otherwise.

**The receipt year is still a lever, even though apportionment is not.** A single payment cannot be
split, but *which* year takes it follows from the payment date, and the year of assessment runs on
the calendar. A lump received in a year that also carries a full year of salary stacks on top of
that salary's chargeable income and is taxed at the top band reached; the same lump received in a
year with no employment income starts from the bottom of the progressive bands. The arithmetic that
isolates the effect, and the one to show the person:

```
marginal tax borne by the lump = tax(other income + lump - exemption) - tax(other income)
value of deferring            = marginal tax borne  -  tax(lump - exemption)
```

Deferral is worth nothing if the receiving year is also a salaried year — check before recommending
it, and never present the mechanic as a spread-over, which does not exist. `scripts/exit_package_calc.py`
computes both. Route the figure itself to a licensed agent (SKILL.md, Advisory stance 2).

> Confirm the current public ruling's status with the tax authority before relying on it. Portal
> reorganisations have broken legacy ruling URLs, and the rule is restated on the authority's
> exemptions page. Do not cite a dead URL as the source.

## 3. The discretionary-clause pattern

Separation-scheme clause lists commonly run to five items, of which one or two carry explicit
age/tenure minimums (typically the "rejuvenation" clause: 20+ years **and** age 50+), while the
rest are pure company discretion — "maximum potential or maximum salary", "functional skill no
longer relevant to business requirements", "any other situation deemed appropriate".

Consequences worth stating to the person:
- A mid-career employee can only reach the **discretionary** clauses. There is no clause they
  qualify for by right.
- Therefore a refusal is **not** a documentation error to be corrected — it is discretion, and it
  can be exercised differently on a later request.
- Scheme language often allows the conversation to be **initiated by either party**, which means an
  employee request is procedurally available even though approval is not guaranteed.
- Refusal language often points to a fallback: those not placed may be offered the scheme, and if
  they decline, best-effort placement, and then retrenchment with compensation. Get the fallback
  terms, because that is the real floor.
- Watch for an internal criterion deployed in a refusal that appears nowhere in the clause list (a
  mobility-recency rule, a minimum-time-in-post rule). When it exists only in the refusal letter,
  name it as such and ask which clause was applied.

## 4. Case law on "voluntary" schemes

Second-hand via law-firm and IR-consultancy case notes (the Industrial Court publishes no openly
searchable award database) — treat as indicative and verify before quoting to the person:

- A scheme presented as "accept this or be retrenched" has been treated as a **retrenchment
  threat**, and the resulting dismissal as unlawful under s.20 Industrial Relations Act 1967.
- A mutual separation agreement has been held **void** where it was procured under indirect
  pressure (Federal Court level).
- The consistent judicial requirements for a valid VSS/MSS: genuine voluntariness, finality
  (waiver of further claims), and fair benefits. Benefits at or below the statutory minimum can
  lead a court to treat the exit as a disguised retrenchment.

**Unfair dismissal window:** s.20 Industrial Relations Act 1967 — a claim for reinstatement or
compensation for unfair dismissal must generally be filed within **60 days** of the dismissal.
Separate from any separation scheme, and relevant when the treatment was procedurally improper.

## 5. EPF / KWSP

- Three-account structure since the 2024 restructuring: **Akaun Persaraan 75%**, **Akaun Sejahtera
  15%**, **Akaun Fleksibel 10%** of monthly contributions.
- **Housing withdrawals come only from Akaun Sejahtera.** Eligible member: citizen/PR, active
  member, below 55, sufficient Sejahtera balance.
- Two broad categories: **buy/build** (limited by purchase price, loan amount and the Sejahtera
  balance, subject to SPA recency rules) and **reduce/redeem an outstanding housing loan** (limited
  by the outstanding balance or the Sejahtera balance, whichever is lower, with a minimum
  withdrawal and a repeat interval, and panel-bank/active-loan conditions).
- **Practical use in an exit plan:** a small remaining housing loan can be cleared from Akaun
  Sejahtera so the cash package stays intact as runway. Do not default to "clear the loan with the
  package" — that converts liquid runway into illiquid equity at the exact moment liquidity is
  what the person needs. Compare the loan rate against what the cash can safely earn before
  recommending either.
- Retirement savings are not runway. Two pools of money with one purpose each beats one pool with
  two purposes.

## 6. Employment insurance (EIS / LINDUNG KERJAYA)

Voluntary and mutual separation schemes are listed among the qualifying causes of loss of
employment. This is a **claim the person makes themselves** — it is not offered in the exit
package and is not affected by how the scheme is described. Check eligibility and the filing
window early; do not leave it to the employer to mention.

## 7. Source access lanes

Primary material for the Regulations and the retrenchment process: the Labour Department's own site
and its retrenchment FAQ, plus the Regulations PDF (served on the `jtksm` subdomain even where the
parent ministry portal does not). The retrenchment-management guideline PDF is a scanned image
without a text layer — OCR it, or cite it second-hand via a law-firm article.

Tax authority: the exemptions page restates the loss-of-employment rule; the public ruling gives
the computation. Legacy direct PDF paths have broken after portal reorganisations — resolve the
current path rather than citing a dead one.

EPF: the members' site may not serve automated fetches. Expect to use indexed page summaries and
reputable Malaysian secondary sources, then have the person **verify on i-Akaun or at a branch**
before acting. State that in the advice rather than presenting the number as settled.

## 8. Calibration — how large is this really

When a person believes their employer's cut is uniquely brutal, check it against the sector:
major integrated peers have announced cuts in the 20% range of global headcount and comparable
percentage reductions in exploration and subsurface functions. Also compare against the employer's
own earlier exercises — a prior round of under a thousand positions is the natural yardstick for
whether a current programme is a step change or a continuation.

This cuts both ways and should be used honestly: it is a reason **not** to over-react to the size
of the cut, and equally not a reason to treat the programme as routine. State which claim the
comparison supports.

## 9. What to say when a figure cannot be sourced

The one-line discipline: an unsourced figure is worse than no figure, because it invites a
debunk that takes the verified material with it. If a number matters to the advice and cannot be
sourced, say "I could not verify this" and name what would settle it. A verified smaller number
beats an unverifiable larger one every time.
