---
name: travel-advisory-research
description: Research current travel requirements, border-crossing rules, road-trip checklists, and safety advisories using authoritative sources plus practical cross-checks.
---

# Travel Advisory Research

Use this skill when the user asks about travel requirements, driving across borders, entry documents, advisories, latest issues, safety conditions, floods/weather, immigration rules, or vehicle paperwork for a trip.

## Workflow

0. **If the user has no concrete trip yet, produce a reusable template**
   - Offer a **generic checklist** (clearly labeled generic) plus a short "what to confirm when dates/nationality are known" section.
   - Do **not** over-claim "latest rules" if the user hasn't provided nationality/dates/route specifics.

1. **Timestamp the check**
   - Record the current UTC/local date/time with a tool before saying anything is "latest".
   - State the timestamp in the final answer.

2. **Prioritize official sources**
   - Immigration / border authority for entry forms and visa/arrival rules.
   - Embassy / consulate pages for country-specific instructions.
   - Foreign ministry travel advisories for safety/security.
   - Disaster/weather agencies for floods, storms, closures, or health risks.
   - Use travel blogs/forums only as practical supplements, never as the sole basis for legal requirements.

3. **Separate requirements from advisories**
   - Structure the final as:
     - Required documents / actions
     - Vehicle-specific requirements, if driving
     - Latest issues / warnings
     - Practical checklist
     - Sources or source notes

4. **Cross-check "latest issues"**
   - Search for recent news and official advisories using date terms and destination names.
   - Watch for stale results: search engines may surface future-looking or old pages. Confirm publication date where possible.
   - **Capture recency signals** when pages don't show clear dates:
     - Prefer explicit "Last updated" text on-page.
     - If absent, use HTTP `Last-Modified` (via `HEAD`) as a weak-but-useful indicator and label it as such.
     - If neither is available, say "update date not shown".
   - If current official pages are sparse, say so and label claims by source/date.

5. **Driving-across-border checklist**
   - Passport validity / visa or exemption.
   - Arrival card / digital declaration requirements.
   - Driver license / IDP expectations.
   - Vehicle registration/title/original grant requirements.
   - Insurance requirements in destination country.
   - Temporary import permit / customs exit obligations.
   - Permission letter if vehicle is not owned by the traveler.
   - Border wait times, holiday congestion, cash/SIM/navigation.

6. **Final-answer style**
   - For Telegram, avoid tables. Use bullets and short labeled sections.
   - Give a direct conclusion first when the user asks "can I go / what do I need".
   - Mention uncertainty explicitly if official confirmation is missing.

## Pitfalls

- Do not answer "latest" from memory; always check current sources.
- Do not treat travel blogs as law. Use them to identify forms/processes, then verify against official immigration/customs/embassy sources where possible.
- Do not mix safety warnings for nearby regions into the exact destination without explaining geography and route relevance.
- Do not forget the return/exit requirement for temporary vehicle import permits; failure to close them can cause fines or future entry issues.
- **"VEP" is not a real Thailand vehicle entry term.** The correct process is "temporary import of personal vehicles" under Thai Customs (en.customs.go.th). Using "VEP" risks spreading misinformation — always use the official Thai Customs terminology.
- **Financed / loan vehicles**: a letter from the financier (NOC) is **strongly recommended / praktikal**, not strictly "wajib" for all cases. Frame it accordingly to avoid over-claiming requirements.
- **Border crossing operational differences**: Bukit Kayu Hitam vs Padang Besar differences (queue times, facilities, holiday congestion) are **operational notes**, not legal requirements. Label them as such.

## References

- `references/malaysia-thailand-driving-hatyai.md` — condensed session notes for Malaysia → Hat Yai by car, including TDAC, vehicle paperwork, flood/security advisories, and useful source URLs.