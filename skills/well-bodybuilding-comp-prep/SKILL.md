---
name: well-bodybuilding-comp-prep
version: 1.0.0
owner: 333-AGI
risk_tier: T1
floor_scope: [F2, F4, F7]
autonomy_tier: T1
description: "AI-powered bodybuilding competition preparation — covers training periodization, nutrition/macro programming, peak week protocols, posing analysis, progress tracking, stage tan optimization, and show-day checklist. Activates when user asks about bodybuilding prep, competition diet, posing routine, peak week, or physique scoring."
---

# WELL Bodybuilding Competition Prep

AI-powered bodybuilding competition preparation for any federation (NPC, IFBB, MR KL, etc).

## When to Use

- User asks about bodybuilding / physique competition prep
- Need nutrition / macro / diet plan for cutting / contest prep
- Posing routine design or stage presentation coaching
- Peak week water/carb depletion/reload protocol
- Progress photo analysis (body composition tracking)
- Competition day checklist
- Stage tan / lighting / oil optimization

---

## 1. TRAINING PERIODIZATION (16-20 Week Prep)

### Phase 1: Off-Season to Contest Declaration (Week 16-12)
- **Volume High** - 4-5 sets x 10-12 reps per exercise
- **Frequency:** 5-6 days/week (Push/Pull/Legs x 2)
- **Goal:** Maximum hypertrophy before cut begins
- **Recovery:** 1 rest day, deload every 4th week

### Phase 2: Fat Loss Phase (Week 12-4)
- **Volume Medium** - 3-4 sets x 8-12 reps
- **Cardio:** 20-40 min LISS 3-4x/week + 15 min HIIT 2x/week
- **Key Rule:** Keep intensity (weight) HIGH, reduce volume only
- **Don't** drop weight to chase reps - that's how you lose muscle

### Phase 3: Peak Week (Week 4-1)
- See Section 3 below - water/carb manipulation

### Phase 4: Show Day (Week 0)
- See Section 5 below

### Common Mistakes (Malaysian Competitors)
1. Cutting too fast (lose muscle, look flat on stage)
2. Dropping sodium too early (kills vascularity)
3. Training legs the day before show (flat, no pump)
4. Trying new exercises/foods in final 4 weeks
5. Skipping posing practice until 1 week before

---

## 2. NUTRITION AND MACRO PROGRAMMING

### Step 1: Calculate Baseline
```python
# Harris-Benedict BMR (Malaysian athletes - bodyweight in kg, height in cm)
BMR = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)

# Activity multiplier: 1.55 (moderate) to 1.725 (very active bodybuilder)
TDEE = BMR * activity_multiplier
```

### Step 2: Contest Prep Deficit
- **Week 16-12:** TDEE - 300 kcal (slow cut, preserve muscle)
- **Week 12-8:** TDEE - 500 kcal (accelerate)
- **Week 8-4:** TDEE - 700 kcal (aggressive but monitored)
- **Week 4-1:** Maintain or small deficit (peak week = carb manipulation not deficit)

### Step 3: Macro Split (Bodybuilding)
| Phase | Protein | Carbs | Fat |
|---|---|---|---|
| Off-season | 2.2-2.5g/kg | 4-6g/kg | 1-1.5g/kg |
| Early cut | 2.4-2.7g/kg | 2-3g/kg | 0.8-1g/kg |
| Late cut | 2.7-3.0g/kg | 1.5-2g/kg | 0.6-0.8g/kg |
| Peak week | 3g/kg | 6-10g/kg (reload) | 0.5g/kg |

### Step 4: Food Sources (Malaysian Context)
**High Protein (accessible, affordable):**
- Ikan pari/tilapia (clean, low fat)
- Ayam breast (budget-friendly)
- Telur (whole + whites)
- Dada ayam perap (meal prep friendly)
- Whey isolate (post-workout)

**Carb Sources (for reload):**
- White rice (fast absorption)
- Jasmine rice
- Potato/sweet potato
- Roti canai (sparingly, high calorie)

**Avoid During Prep:**
- Nasi lemak (fat bomb)
- Mee goreng (high sodium, low protein ratio)
- Roti john (calorie bomb)
- Teh tarik (hidden sugar)
- Air kosong is your best friend

---

## 3. PEAK WEEK PROTOCOL

### Standard 7-Day Peak Week
| Day | Water | Sodium | Carbs | Training |
|---|---|---|---|---|
| Mon | 8-10L | Normal (4-5g) | Low (<100g) | HIGH volume (deplete) |
| Tue | 8-10L | Normal | Low | HIGH volume (deplete) |
| Wed | 6-8L | Low (2g) | Low | Medium (deplete) |
| Thu | 4-6L | Low (1-2g) | LOW | Light (pump only) |
| Fri | 3-4L | Low (<1g) | HIGH (6-10g/kg) | NO training |
| Sat (show) | Sip only | Normal | Normal meals | PUMP UP backstage |
| Sun (show 2) | Sip only | Normal | Normal meals | PUMP UP backstage |

### Critical Rules
1. **NEVER** change foods in peak week - stick to tested staples
2. **Sodium** manipulation is more important than water
3. **Carb reload** Thursday night to Saturday = the "supercompensation" effect
4. If you look flat on Friday - slightly more carbs (50-100g)
5. If you look watery - reduce water, increase walking
6. **Deplete Mon-Wed, reload Thu-Fri** is the classic protocol

---

## 4. POSING AND STAGE PRESENTATION

### Mandatory Poses (Bodybuilding)
1. Front Double Biceps
2. Front Lat Spread
3. Side Chest
4. Side Triceps
5. Back Double Biceps
6. Back Lat Spread
7. Abdominal and Thigh
8. Most Muscular (Hands on Hip / Crab)

### Physique / Sport Physique (MR KL categories)
- **Athletic Physique:** Mandatory quarter turns + 30s routine
- **Sport Physique:** Quarter turns + mandatory poses
- Focus on: V-taper, symmetry, condition, stage presence

### AI Posing Analysis (What Hermes Can Do)
- Take progress video - analyze pose angles with Gemini vision
- Check: lat spread width, symmetry, vacuum pose, conditioning
- Compare with reference competitors from same category
- Identify weak poses for targeted improvement

### Stage Presence Tips
1. **Walk:** Slow, deliberate, 3 steps between poses
2. **Eye contact:** Judges, then audience sweep
3. **Smile:** Genuine confidence, not forced
4. **Oil:** Apply thin layer 15 min before stage, reapply as needed
5. **Tan:** Even, no streaks, dark enough for stage lights

---

## 5. COMPETITION TAN AND STAGE OPTIMIZATION

### Tan Protocol
- **2 coats** minimum (3 for very light skin)
- **First coat:** Day before show, evening
- **Second coat:** Show morning, 3-4 hours before stage
- **Touch-up:** Backstage, 15-20 min before
- **Product:** Pro Tan / Dream Tan / Jan Tana (available in MY via Shopee)

### Stage Light Consideration
- Stage lights are **warm tungsten** - tan should be **warm bronze** (not orange)
- Darker skin (Malay) needs less product but more even application
- Oil applied AFTER tan - oil makes muscles pop under light
- Re-oil every time you go backstage (sweat kills oil sheen)

### Posing Trunks
- **Bodybuilding:** Black, tight, V-cut
- **Physique:** Board shorts (longer) or trunk style
- Make sure trunks fit properly - no wardrobe malfunction on stage

---

## 6. PROGRESS PHOTO AI TRACKING

### Weekly Photo Protocol (Hermes-Trackable)
1. **Same time** every week (morning, fasted, after bathroom)
2. **Same lighting** (natural light from one window)
3. **4 angles:** Front relaxed, side relaxed, back relaxed, front double bicep
4. **Same distance** from camera (use tape mark on floor)
5. **No pump** - morning fasted = consistent baseline

### What Hermes Can Analyze
- **Week-over-week comparison:** fat loss rate, muscle retention
- **Symmetry audit:** left vs right imbalance, upper vs lower
- **Condition tracking:** vascularity, muscle separation, skin quality
- **Warning signs:** flat muscles (too much deficit), watery (sodium issue)

---

## 7. SUPPLEMENT STACK (Evidence-Based)

### Tier 1: Proven
| Supplement | Dose | Purpose |
|---|---|---|
| Creatine Monohydrate | 5g/day | Strength, fullness (STOP in peak week) |
| Whey Protein | 25-50g post-workout | Convenience protein |
| Caffeine | 3-6mg/kg pre-workout | Performance, fat oxidation |
| Fish Oil (Omega-3) | 2-3g/day | Inflammation, joint health |
| Vitamin D3 | 2000-5000 IU/day | Hormonal support |

### Tier 2: Optional
| Supplement | Dose | Purpose |
|---|---|---|
| Beta-Alanine | 3-6g/day | Endurance (tingling is normal) |
| Citrulline Malate | 6-8g pre-workout | Pump, blood flow |
| Ashwagandha | 600mg/day | Stress, cortisol management |
| Multivitamin | 1/day | Micronutrient insurance |

### Malaysian Supplement Sources
- Shopee Malaysia (bulk pricing)
- GNC Malaysia
- Local supplement shops (Gym Zone, etc.)
- Whey importers (bulk from iHerb)

---

## 8. SHOW DAY CHECKLIST

### Morning of Show
- Wake up 4-5 hours before stage time
- Light breakfast (rice + chicken, tested food)
- Second tan coat applied
- Oil applied (thin layer)
- Pose practice (15 min pump-up with bands)
- Check-in at venue
- Backstage: warm up, pump up (push-ups + curls)
- Touch up oil/tan before walking on stage

### Backstage Kit
- Posing trunks (backup pair)
- Tan product (for touch-ups)
- Oil (for sheen)
- Towels (black - won't show tan)
- Baby wipes (for accidental tan smudges)
- Food: rice cakes, peanut butter, banana, honey
- Water bottle (small sips)
- Resistance bands (for pump-up)
- Phone + charger
- ID / registration confirmation
- Cash (for entries, parking)
- Spare safety pins

---

## 9. MENTAL PREP AND RECOVERY

### Last 4 Weeks (The Mental Game)
- Expect: mood swings (from calorie deficit + low carbs)
- Accept: you WILL feel flat, watery, and doubt yourself
- Trust: the process works - your coach/plan is designed for this
- Sleep: 7-9 hours minimum (cortisol control)
- Manage: social media scrolling (comparison kills confidence)

### Post-Show
- **Reverse diet** - slowly increase carbs/calories over 4-8 weeks
- **Don't binge** - the most dangerous period for rebound weight gain
- **Take show-day photos** - you will look different vs 4 weeks later
- **Celebrate** - you did something 99% of people never attempt

---

## 10. AI CAPABILITIES SUMMARY (What Hermes Can Actually Do)

| Capability | How | Tool |
|---|---|---|
| Progress photo comparison | Weekly photos - Gemini vision analysis | vision_analyze |
| Macro calculation | Harris-Benedict + custom deficit curve | Terminal python |
| Meal plan generation | Malaysian food database + macro targets | Hermes text gen |
| Peak week calendar | Template-based with adjustments | Hermes text gen |
| Competition tan timing | Show-day countdown + checklist | Hermes text gen |
| Posing video analysis | Frame extraction + pose assessment | vision_analyze |
| Supplement stack audit | Compare user intake vs evidence base | Hermes text gen |
| Show-day checklist | Template-based, customizable | Hermes text gen |
| PR tracking | Weight, reps, volume per exercise | Terminal/file tracking |
| Category research | Search federation rules, categories, judging criteria | Web search |
| **Competition promo images** | **Edit real photo to backstage/stage scenes for social media** | **gemini-image.py --image (nano banana)** |
| **Promo image editing** | **Add people, change background, dramatic lighting** | **gemini-image.py --model gemini-2.5-flash-image** |
| **Old photo enhancement** | **Restore old competition screenshots to HD** | **gemini-image.py --model gemini-3-pro-image** |

### Competition Photo Enhancement (old IG screenshots — verified 2026-08-12)
When user provides old competition photo from IG Story/screenshot:
1. Use **Gemini 3 Pro** (not Flash) for restoration
2. Prompt: "Ultra HD upscale... Remove compression artifacts, noise, blur... Sharpen to 8K"
3. Manage expectations — screenshot source = limited resolution ceiling
4. For true HD, user needs original camera photo

### Competition Promo Image Workflow
1. Get reference photo of athlete
2. Edit into stage/backstage scene using Gemini Flash nano banana
3. Prompt should specify: event name, category, posing trunks, oil, lighting
4. Verify output before delivery — identity must look like the real person

---

## Pitfalls (Malaysia-Specific)

1. **Heat + competition tan = sweat disaster.** Apply antiperspirant before tan.
2. **Flight meals** - if travelling interstate for show, bring own food (airport food = macro nightmare).
3. **Judging bias** - Malaysian shows sometimes favor certain physiques. Know your category's judging criteria.
4. **Gym culture** - most Malaysian gyms don't have posing mirrors. Book a posing session or use bathroom mirror.
5. **Budget** - competition prep is expensive (entry fees, tan, trunks, travel, supplements). Budget RM500-2000+ total.
6. **Coach dependency** - many Malaysian competitors rely on gym coaches who don't understand competition prep. Get a prep-specific coach or use evidence-based resources.

---

## MR KL 2026 Specific (from poster analysis)

- **Event:** MR KL 2026 Body Building and Physique Championship
- **Date:** 5-6 September 2026
- **Location:** TLKB Metropolitan Kepong, KL
- **Registration:** RM250 (Final Call, closes 31 Aug 11:59PM)
- **Categories:** 12 bodybuilding + 5 physique classes
- **Eligibility:** All Malaysians except PDRM/ATM/Bomba
- **Sport Physique prizes:** 1st RM1,500 + medal + cert
- **Contact:** 012-3444005 | 016-9957363
- **Organizer:** official_klbbf
- **Time from now:** ~24 days to show (as of Aug 12)
- **Implication:** Must be in FINAL CUTTING PHASE - peak week starts ~Aug 25 if 1-week protocol
