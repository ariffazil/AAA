---
name: malaysian-family-law
description: "Syariah family law — nafkah, custody, divorce, MS2 forms."
tags: [malaysia, syariah, family-law, nafkah, custody, divorce, BM, mahkamah]
related_skills: [malaysian-tenancy-consumer-dispute]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Malaysian Syariah Family Law

Covers Syariah family court matters in Malaysia: child maintenance (nafkah anak), custody (hadanah), divorce (cerai), marriage disputes, and related procedures.

## Jurisdiction Scope

| Court Type | Matters | Key Law |
|---|---|---|
| **Mahkamah Rendah Syariah** | Nafkah anak, cerai, hadanah (first instance) | State Enakmen — varies by state |
| **Mahkamah Tinggi Syariah** | Appeals, higher-value disputes | State Enakmen |
| **Mahkamah Syariah (Federal)** | Federal territory matters | Enakmen Tatacara Mal Mahkamah Syariah (Federal) |

**Critical:** Family law in Malaysia is STATE-based. Each state has its own Enakmen. Penang's is **Enakmen Undang-Undang Keluarga Islam (Pulau Pinang) 2004**. Kedah, Selangor, etc. have different versions. Always check which state's law applies.

## Nafkah Anak (Child Maintenance)

### Legal Basis
- **Seksyen 73** Enakmen Undang-Undang Keluarga Islam (Pulau Pinang) 2004
- Parent obligation under Hukum Syarak + statutory law
- Applies to biological children regardless of marital status

### What Can Be Claimed
| Item | Typical Range | Notes |
|---|---|---|
| Nafkah bulanan | RM500–2,000/month | Depends on child's needs + father's ability |
| Perbelanjaan Hari Raya | RM200–1,000/year | Aidilfitri + Aidiladha |
| Perbelanjaan persekolahan | RM500–2,000/year | Uniform, books, fees |
| Perbelanjaan perubatan | As needed | Medical, dental |
| Lain-lain | Case-by-case | Clothing, transport, etc. |

### Court Considers Two Factors
1. **Kebutuhan anak** — actual needs (food, shelter, education, healthcare)
2. **Kemampuan bapa** — father's income and financial capacity

**If claimed amount exceeds father's ability**, court will reduce. E.g., if father earns RM2,000/month, court won't order RM1,500 nafkah — more likely RM500–800.

### Procedure (Penang)
1. Plaintif (usually mother) files **Borang MS2** (Saman) at Mahkamah Rendah Syariah
2. Statement of Claim (Pernyataan Tuntutan) attached — details of claim, amount, breakdown
3. Defendant served with saman — must appear or file pembelaan (defence)
4. If defendant no-shows → court can hear ex parte (one-sided)
5. Hearing → court issues order
6. Payments ordered to be made to plaintiff's bank account

### Key Forms
| Form | Purpose |
|---|---|
| **Borang MS2** | Saman (Summons) |
| **Borang MS3** | Pembelaan (Defence) |
| **Borang MS4** | Perbalahan (Reply) |
| **Borang MS15** | Perintah/Orde |

## Hadanah (Custody)

### Legal Presumption
- Child under 7: **mother** has priority (Seksyen 77)
- Child over 7: court considers child's own preference
- Father remains financially responsible regardless of custody

### Factors Court Considers
1. Child's welfare and best interest (kepentingan terbaik kanak-kanak)
2. Moral and religious upbringing
3. Financial capability of custodian
4. Stability of home environment
5. Child's own wish (if mature enough)

## Cerai (Divorce)

### Types
| Type | Who Initiates | Process |
|---|---|---|
| **Cerai talak** | Husband | Pronounce talak (1st, 2nd, or 3rd) |
| **Cerai taklik** | Wife | Based on conditions in akad nikah |
| **Fasakh** | Wife | Application to court — cruelty, desertion, etc. |
| **Khuluk** | Wife | Wife returns mahr (duit hantaran) in exchange for divorce |

### Fasakh Grounds (Seksyen 47)
- Husband absent/missing
- Husband fails to provide nafkah
- Husband cruel / threatens safety
- Husband imprisoned 3+ years
- Husband impotent
- Husband marries second wife without permission (in some states)

## Important Notes for Agents

### What You CAN Do
- Analyse court documents (saman, pernyataan tuntutan, perintah)
- Explain legal concepts in plain BM
- Draft correspondence between parties
- Compare claim amounts with precedent ranges
- Identify procedural requirements and deadlines
- Explain rights and obligations under specific state Enakmen

### What You CANNOT Do
- Give formal legal advice (always caveat: "bukan peguam")
- Represent anyone in court
- Predict exact court outcome (depends on judge, specific evidence)
- Replace a Peguam Syarie for hearing preparation
- File documents on anyone's behalf

### Communication Style
- **Language**: Bahasa Malaysia (default), English for legal terms
- **Tone**: Plain, human, empathetic. Not robotic. Not legal-jargon-heavy.
- **Format**: WhatsApp-first. Short paragraphs. Key numbers bolded.
- **Audience**: Often a person in emotional distress. Lead with empathy, not procedure.
- **Always include**: "Ini bukan nasihat undang-undang formal. Sila rujuk Peguam Syarie."

## Pitfalls

1. **State law varies.** Never cite Seksyen 73 Penang when the case is in Kedah. Check which state's Enakmen applies. Same section number, different state = different law.

2. **Claimed amount ≠ ordered amount.** Nafkah claims are opening bids. Court will cross-examine and adjust. Don't tell clients "you will get RM1,500" — tell them "you claimed RM1,500, court will decide based on both sides."

3. **Ex parte risk.** If defendant doesn't respond within the time limit, court can hear the case without them. This is a real risk — advise early response.

4. **AI-guided procedure is common now.** Increasingly, parties are using ChatGPT/AI to guide themselves through Syariah court procedure. Be aware: AI may give correct procedure but wrong strategy, or miss state-specific nuances. The agent should verify state-specific law, not trust the AI output.

5. **Confidentiality.** Family law matters are deeply personal. Never share details outside the immediate conversation. F5 privacy applies.

6. **Scanned court documents have no text layer.** CamScanner / phone-camera PDFs (the majority of Syariah filings) return EMPTY from pdftotext — that is not "unreadable". Working path: `pdftoppm -png -r 80 <file.pdf> <prefix>` then read each page image with vision. Render and look before ever telling the user a document can't be read.

7. **Families conflate proceedings.** A user says "cerai" while the document in hand is a **nafkah anak saman** — a separate proceeding that can run before, during, or after any divorce petition. Always identify WHICH document you hold (nafkah saman ≠ petisi cerai/fasakh/khuluk ≠ hadanah) and state the distinction plainly. The family's mental model of "the case" is often one proceeding behind the paper reality.

8. **Case facts go stale — re-verify before narrating.** Hearing dates, case status, even WHICH matter is live (pusaka settled vs. hearing pending) drift in stored memory. Verify against the source document or the sovereign BEFORE building any timeline or emotional narrative. One unverified date this session produced a full wrong-premise narrative that had to be retracted.

9. **A saman is one-sided by design.** Summons + pernyataan tuntutan is the PLAINTIFF's version of events — never present the claim narrative as established fact. The defendant's side arrives formally via Borang MS3 (pembelaan); ask the lawyer whether one has been filed before concluding what "really happened". When briefing a skeptical relative who "doesn't agree" with the divorce: both spouses usually carry one-sided stories of the same event — the family's job is to hold that gap open, not fill it. Watch for claim phrases that reassign history (e.g. "hutang sejak sebelum kahwin" shifts blame away from the marriage itself): such framing is motive-bearing even when factually true, and a fact can be true AND strategically deployed at the same time.

10. **Order ≠ money (enforcement gap).** A nafkah order can be won and still be uncollectable — the court cannot extract cash from a defendant who is hiding, jobless, or being drained by informal lenders (along). If along are active around the defendant, prepare the family early: "menang atas kertas, kosong dalam tangan". Along harassment (posters, threats, paint) is criminal-intimidation evidence: document it (photo, date, police report), hand it to the lawyer, never negotiate with along directly. See `references/along-informal-debt.md` for reading along operations as evidence.

11. **Never import person-attributes from adjacent files.** Every attribute in a case narrative (occupation, habits, "dia doktor") needs a source line in the document or testimony. Bleeding a detail in from another person's file or an unverified fragment is fabrication with family-law blast radius — the sovereign WILL test it ("mana hang dapat info tu?"), and rightly so.

12. **CTOS/CCRIS is the falsifiable object in a hearsay-heavy case.** When the family narrative arrives as voice notes + one-sided stories, the credit report is the one motive-free document. Read it as data: score, outstanding vs limit ratios, write-offs, saman list, and above all the **first trade line date** — it arbitrates timeline disputes ("hutang sejak sebelum kahwin" vs "tumbuh semasa kahwin"): often BOTH are half-true (one pre-marriage line, several post-marriage lines). Borrower psychology reads from the pattern: survival-spiral (open line → cover line → default) ≠ con-artist ≠ business failure. But a CTOS brief pasted into a chat by a family member is still second-hand — quote its numbers, mark them as transcribed, and keep the "why did the first line open" hole explicitly open.

13. **The paying sibling is a party in everything but name.** In this federation's family cases, an elder sibling often funds the lawyer, flights, and family costs while holding zero formal standing. Their leverage is moral + informational, not procedural: (a) as paymaster they may request a document checklist + per-step cost estimate from the lawyer they fund — frame it as project management, not interference; (b) their cooperation request to the plaintiff must be short, dated, and unemotional ("hantar minggu ini"); (c) warn them early that being the reliable payer converts to "bad guy" status in family memory (two-lawyer pattern) — the counter is receipts + one clean boundary conversation after the hearing, not withdrawal mid-case.

## References

See `references/` directory for:
- `references/scanned-pdf-vision-recipe.md` — pdftoppm + vision transcription path for CamScanner/phone-scanned court PDFs (pdftotext returns empty on these)
- `references/along-informal-debt.md` — reading along (informal lender) collection tactics as evidence: escalation ladder, whose-family-gets-harassed compass, poster forensics, enforcement-gap briefing for nafkah orders

## Related
- `malaysian-tenancy-consumer-dispute` — Civil court consumer/tenancy matters (different jurisdiction)
- `counseling` — Decision advisory for personal/financial matters
- `hospital-patient-advocacy` — Malaysian medical system navigation
