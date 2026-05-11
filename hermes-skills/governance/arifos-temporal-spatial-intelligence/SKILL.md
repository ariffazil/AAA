---
name: arifos-temporal-spatial-intelligence
description: Temporal-spatial intelligence for real-world recommendations. Triggers on food/restaurant/travel/entertainment tasks. Ensures recommendations are currently open and spatially relevant.
trigger: food OR restaurant OR hotel OR travel OR activity OR entertainment OR open OR hours OR tonight OR now
---

# Temporal-Spatial Intelligence (arifOS F1-F13)

## Trigger Conditions
Any recommendation task involving:
- Food/restaurants/bars/entertainment venues
- Travel, accommodation, activities, tours
- Real-world services with operating hours
- ANY task where "is it open?" and "where is it?" matter

## The 4-Question Rule

For every such task, research MUST answer:

### Q1: IS IT OPEN RIGHT NOW?
- Current time + day in target location
- Check today specifically (Saturday 9pm ≠平时的hours)
- Thai mall hours: 10am-9pm weekdays, 10am-10pm weekends
- Many Thai restaurants close 9-10pm even Saturday

### Q2: SPATIAL CONTEXT
- Where is the user RIGHT NOW?
- Distance + travel time + traffic
- If near mall → prioritize mall options
- If far → prioritize what's nearby

### Q3: TEMPORAL CONTEXT
- Day of week (Thai weekend = Fri-Sat or Sat-Sun)
- Public holidays in Thailand
- Seasonal (rainy season = outdoor places close early)
- Ramadan = Muslim restaurants may have limited hours

### Q4: CONTINGENCY (ALWAYS)
- If top choice is closed, what is the NEXT option?
- List 3 alternatives with current open status
- Include phone numbers
- Never present single point of failure

## Implementation Protocol

```
Step 1: Check current time + day in target location
Step 2: Search "PLACE_NAME open now" + "PLACE_NAME hours today"
Step 3: If closed → immediately pivot to alternatives
Step 4: Verify halal/status with live sources
Step 5: Present options ranked by:
         [OPEN NOW] > [LIKELY OPEN] > [UNCONFIRMED]
Step 6: Include phone numbers for quick calls
```

## Anti-Failure Pattern

❌ WRONG (static ranking):
"Mandarin Suki Rattakarn ⭐4.6 (604 reviews) — #1 recommendation"
→ Fails when it's closed

✅ CORRECT (availability-first):
"Mandarin Rattakarn: STATUS UNKNOWN — call 086 696 3231 before driving"
"Khlong Hae Halal: LIKELY OPEN Saturday night — backup #1"
"Rim Rua: LIKELY OPEN late night ทะเลเผา — backup #2"
"If all closed: Street market or 7-11 suki — emergency backup"

## Knowledge Base

**Thai Mall Hours:**
- Weekdays: 10am-9pm
- Weekends: 10am-10pm
- Public holidays: may differ

**Thai Restaurant Peak:**
- Lunch: 12pm
- Dinner: 6-8pm
- After 9pm: many close even Saturday

## Failure Case Study: Hat Yai (2026-05-09)

**What happened:**
1. Brave Search API returned generic Thai news, NOT restaurant live status
2. Arif + family drove to Mandarin Central (CLOSED) → Mandarin Rattakarn (CLOSED) → Mall closing 9pm
3. All 5 ranked recommendations were based on static review data (⭐4.6, 604 reviews) — no real-time open verification
4. Failure caused real-world consequence: family drove around Hat Yai 9pm+ with 18-month-old Naufal

**Key lessons learned:**

### API Limitation
- Search APIs (Brave, Google, etc.) do NOT reliably return live open/closed status for local Thai restaurants
- Bangkok/Thai news dominates results; local restaurant hours are rarely indexed in real-time
- Never trust API results as sole verification of current availability

### Verification Hierarchy (when API fails)
1. **Call the restaurant directly** — most reliable (phone: 086 696 3231 for Mandarin Suki Rattakarn)
2. **Check Google Maps "24-hour" or today's hours** — sometimes live
3. **Check Facebook/Line page for tonight's hours** — often updated same-day
4. **Ask locals or taxi driver** — real-time ground truth
5. **Drive-by verification** — last resort if all else fails

### Anti-Halucination Pattern
- A restaurant appearing in search results with high rating does NOT mean it's open right now
- Review count (604 reviews) and rating (⭐4.6) measure quality, not availability
- F2 TRUTH: must verify current state, not assume based on historical data

### Required Response Pattern (updated)
```
❌ WRONG: "Mandarin Suki Rattakarn ⭐4.6 (604 reviews) — #1 recommendation"
✅ CORRECT: 
  "Mandarin Rattakarn — QUALITY: ⭐4.6/604 reviews | AVAILABILITY: UNKNOWN | ACTION: Call 086 696 3231 before driving"
  "Khlong Hae Halal — QUALITY: ⭐4.4/2192 reviews | AVAILABILITY: LIKELY OPEN (Saturday late night) | ACTION: Backup if #1 closes"
  "Rim Rua — QUALITY: ⭐4.2/1692 reviews | AVAILABILITY: LIKELY OPEN (late night ทะเลเผา) | ACTION: Emergency backup"
  "If all closed: Street market → 7-11 suki → survive mode"
```

### Temporal-Spatial Must Precede Quality Ranking
- Research flow: Location → Time → Day → Check availability → THEN quality rank
- Not: Quality rank → give list → hope places are open

**Always: availability first, quality second, contingency always.**

## Governance Note

This failure violates:
- **F6 Empathy**: consequence for user (family drove, place closed)
- **F8 Genius**: elegant solution, not just "acceptable"
- **F2 Truth**: not verifying current state

Lesson from Hat Yai (2026-05-09): Arif + family drove to Mandarin Central (closed), then Mandarin Rattakarn (closed), mall closing 9pm. Last dinner deserved better than wrong static data.

**Always: availability first, quality second, contingency always.**