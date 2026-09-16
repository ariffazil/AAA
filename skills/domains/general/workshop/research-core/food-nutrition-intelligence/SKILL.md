---
name: food-nutrition-intelligence
description: Use when user asks about food calories or nutrition data — text queries, photo-based estimation, and health/supplement research.
version: 2.0.0
author: Hermes (arifOS)
license: MIT
hermes:
  tags: [nutrition, calories, food, dietary, usda-api, photo-analysis, peptide-research]
  related_skills: [web-access-fallbacks, AGI-multimodal-bridge]
---

# Food Nutrition Intelligence

## When to Use
- User asks about calories ("berapa kalori", "how many calories")
- User asks about nutritional content (protein, fat, carbs)
- User asks about food composition or dietary analysis
- User sends food image and asks about nutrition
- User asks about a specific supplement, peptide, or health product's effects/side effects

## Primary Method: USDA FoodData Central API

The USDA provides a free, reliable API for food nutrition data. No API key required for basic use (DEMO_KEY works for low-volume queries).

### Endpoint
```
https://api.nal.usda.gov/fdc/v1/foods/search?query={food_name}&api_key=DEMO_KEY
```

### Key Nutrient IDs in Response
- `1008`: Energy (kcal)
- `1003`: Protein (g)
- `1004`: Total lipid/fat (g)
- `1005`: Carbohydrate (g)

### Response shape (FDC v1 foods/search)
Each `foods[].foodNutrients[]` entry is FLAT: `{"nutrientId": 1003, "nutrientName": "Protein", "value": 25.7, "unitName": "g", ...}`. Parse with `{x["nutrientId"]: x["value"] for x in f["foodNutrients"]}`. There is NO nested `nutrient` object and no `amount` key — the old nested shape (`x["nutrient"]["id"]`, `x["amount"]`) silently returns None for every nutrient.

### Example Query
Query: `grilled salmon fillet`
Result: 259 kcal/100g, 25.92g protein, 16.48g fat, 0g carbs

## Workflow: Text Query
1. Parse food item from user query
2. Query USDA API with food description
3. Extract energy (kcal) and macronutrients from `foodNutrients` array
4. Estimate portion size (see below)
5. Scale nutrition data to portion size
6. Present results with source attribution

## Workflow: Photo-Based Estimation
When user sends a food photo and asks about calories:

1. **Identify components visually** — list each distinct food item on the plate
2. **Estimate portions** using visual cues (plate diameter ~25cm, cutlery size, table setting)
3. **Query USDA API per component** — don't query "IKEA meal"; query "grilled salmon fillet", "mashed potato", "creamy dill sauce", "steamed broccoli" separately
4. **Sum per-component totals** for the meal
5. **Cross-check against known restaurant data** — if a chain (McDonald's, IKEA, Starbucks) publishes nutrition info, use that instead of USDA proxy
6. **Present component breakdown** — user sees where each calorie comes from

### Component Breakdown Pattern (from IKEA salmon session)
```
Salmon fillet (×2): 259 kcal/100g × ~150g each = ~776 kcal
Mashed potato: ~100 kcal/100g × ~150g = ~150 kcal
Creamy dill sauce: ~200 kcal/100g × ~50g = ~100 kcal
Mixed veggies: ~35 kcal/100g × ~100g = ~35 kcal
Chocolate mousse: ~250 kcal/cup
Total: ~1,336 kcal
```

The component breakdown is more useful to the user than a single number — they can see which item contributes most and make trade-off decisions.

## Research Fallbacks for Niche Topics
When user asks about a specific food, supplement, or health product that USDA doesn't cover well (e.g., peptides, proprietary supplements):

1. **Wikipedia REST API** — fast structured data:
   ```bash
   curl -sL "https://en.wikipedia.org/w/api.php?action=query&titles=<topic>&prop=extracts&explaintext=true&format=json"
   ```
2. **PubMed E-utilities** — peer-reviewed research:
   ```bash
   curl -sL "https://pubmed.ncbi.nlm.nih.gov/?term=<query>"
   ```
3. **Specialized sites** — peptides.org, healthline.com, etc. via direct curl
4. **If all web search fails** — see `web-access-fallbacks` skill for the full ladder

## Pitfalls
- Malaysian menu species mapping: "saba" = Pacific mackerel (query `mackerel Pacific cooked`), restaurant salmon = farmed Atlantic (query `salmon Atlantic farmed cooked`). Benchmarks in `references/malaysian-menu-fish.md`.
- Restaurant preparations may differ from USDA generic data (more oil, different sauces)
- Sauces and cooking oils significantly affect calorie count — always note this
- Always mention the data source (USDA proxy vs restaurant-published data)
- For major chains (McDonald's, Starbucks, etc.), check if they publish nutrition info directly before falling back to USDA
- IKEA does not publish calorie data on their Malaysian website — use USDA as proxy
- When estimating from photos, acknowledge uncertainty — "approximately" or "estimated" is honest
- For peptides/supplements: no robust human data means you MUST caveat heavily — don't present animal study results as established fact
- WADA banned list changes — check current status for any performance-related supplement

## Portion Size Estimation
When user provides an image or description, estimate based on standard restaurant portions:
- Protein (fish/chicken/meat): 120-150g per fillet
- Starch (rice/potatoes/pasta): 150-200g
- Vegetables: 80-100g
- Sauces: 30-50g
- Dessert: 100-150g

When user provides an image, identify items visually and estimate based on plate size relative to known objects (cutlery, table setting).

## Verification
- Confirm USDA API response contains `foodNutrients` array
- Verify energy value (nutrientId 1008) is present and reasonable (50-2000 kcal/100g)
- Check that total meal calories fall within expected range (500-2500 kcal)
- If result seems off, try alternative food description (e.g., "salmon fillet baked" vs "grilled salmon")
