#!/usr/bin/env python3
"""
contest_prep_calculator.py — Bodybuilding contest prep macro calculator

Usage:
    python3 contest_prep_calculator.py --weight 78 --height 170 --age 30 --gender male --bodyfat 15 --weeks 16

Output: Full macro breakdown per phase (off-season, early cut, late cut, peak week)
"""

import argparse
import math

def calculate_bmr(weight_kg, height_cm, age, gender="male"):
    """Harris-Benedict BMR"""
    if gender == "male":
        bmr = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)
    return round(bmr, 1)

def calculate_tdee(bmr, activity="moderate"):
    """Total Daily Energy Expenditure"""
    multipliers = {
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.65,
        "very_active": 1.725
    }
    return round(bmr * multipliers.get(activity, 1.55), 0)

def calculate_macros(weight_kg, tdee, phase="early_cut"):
    """Calculate macros for a given phase"""
    phases = {
        "off_season": {"cal_offset": 0, "protein": (2.2, 2.5), "carbs": (4, 6), "fat": (1, 1.5)},
        "early_cut": {"cal_offset": -300, "protein": (2.4, 2.7), "carbs": (2, 3), "fat": (0.8, 1)},
        "late_cut": {"cal_offset": -500, "protein": (2.7, 3), "carbs": (1.5, 2), "fat": (0.6, 0.8)},
        "aggressive_cut": {"cal_offset": -700, "protein": (3, 3.2), "carbs": (1, 1.5), "fat": (0.5, 0.7)},
        "peak_week_deplete": {"cal_offset": -300, "protein": (3, 3.2), "carbs": (0.5, 1), "fat": (0.5, 0.7)},
        "peak_week_reload": {"cal_offset": -100, "protein": (2.5, 3), "carbs": (6, 10), "fat": (0.5, 0.8)},
    }
    
    p = phases.get(phase, phases["early_cut"])
    target_cal = tdee + p["cal_offset"]
    target_cal = max(target_cal, 1200)
    
    # Use mid-range values
    protein_g = round((p["protein"][0] + p["protein"][1]) / 2 * weight_kg)
    fat_g = round((p["fat"][0] + p["fat"][1]) / 2 * weight_kg)
    
    # Carbs = remaining calories
    protein_cal = protein_g * 4
    fat_cal = fat_g * 9
    carb_cal = max(0, target_cal - protein_cal - fat_cal)
    carb_g = round(carb_cal / 4)
    
    return {
        "phase": phase,
        "target_calories": round(target_cal),
        "protein_g": protein_g,
        "protein_per_kg": round(protein_g / weight_kg, 1),
        "carbs_g": carb_g,
        "carbs_per_kg": round(carb_g / weight_kg, 1),
        "fat_g": fat_g,
        "fat_per_kg": round(fat_g / weight_kg, 1),
    }

def print_plan(weight_kg, height_cm, age, gender, bodyfat, weeks):
    """Print full contest prep plan"""
    lean_mass = weight_kg * (1 - bodyfat / 100)
    
    print("=" * 60)
    print("BODYBUILDING CONTEST PREP CALCULATOR")
    print("=" * 60)
    print(f"\nAthlete Profile:")
    print(f"  Weight: {weight_kg} kg")
    print(f"  Height: {height_cm} cm")
    print(f"  Age: {age} years")
    print(f"  Gender: {gender}")
    print(f"  Body Fat: {bodyfat}%")
    print(f"  Lean Mass: {lean_mass:.1f} kg")
    print(f"  Prep Duration: {weeks} weeks")
    
    bmr = calculate_bmr(weight_kg, height_cm, age, gender)
    tdee = calculate_tdee(bmr, "active")
    
    print(f"\nMetabolic Baseline:")
    print(f"  BMR: {bmr} kcal")
    print(f"  TDEE (active): {tdee} kcal")
    
    # Target show weight (estimate 5-10% loss)
    target_loss = weight_kg * 0.08
    show_weight = weight_kg - target_loss
    weekly_loss = target_loss / weeks
    
    print(f"\nTarget:")
    print(f"  Show Weight: ~{show_weight:.1f} kg ({target_loss:.1f} kg loss)")
    print(f"  Weekly Rate: {weekly_loss:.2f} kg/week")
    
    if weekly_loss > 0.8:
        print(f"  WARNING: Loss rate > 0.8 kg/week risks muscle loss!")
    
    print(f"\n{'='*60}")
    print(f"PHASE-BY-PHASE MACRO BREAKDOWN")
    print(f"{'='*60}")
    
    phases = [
        ("Off-Season (Weeks {0}-{1})".format(weeks, max(weeks-4, 1)), "off_season"),
        ("Early Cut (Weeks {0}-{1})".format(max(weeks-4, 1), max(weeks-8, 1)), "early_cut"),
        ("Late Cut (Weeks {0}-{1})".format(max(weeks-8, 1), 5), "late_cut"),
        ("Peak Week - Deplete", "peak_week_deplete"),
        ("Peak Week - Reload", "peak_week_reload"),
    ]
    
    for label, phase in phases:
        m = calculate_macros(weight_kg, tdee, phase)
        print(f"\n--- {label} ---")
        print(f"  Calories: {m['target_calories']} kcal")
        print(f"  Protein:  {m['protein_g']}g ({m['protein_per_kg']}g/kg)")
        print(f"  Carbs:    {m['carbs_g']}g ({m['carbs_per_kg']}g/kg)")
        print(f"  Fat:      {m['fat_g']}g ({m['fat_per_kg']}g/kg)")
    
    print(f"\n{'='*60}")
    print("MALAYSIAN FOOD EXAMPLES (per meal)")
    print(f"{'='*60}")
    print("""
  Breakfast:  2 whole eggs + 2 whites + 1 cup jasmine rice + 1 cup sayur
              ~30g P | 50g C | 15g F | 455 kcal
  
  Lunch:      200g ayam breast + 1.5 cup white rice + broccoli
              ~50g P | 75g C | 8g F | 572 kcal
  
  Pre-WO:     1 scoop whey + 1 banana
              ~25g P | 30g C | 2g F | 230 kcal
  
  Dinner:     200g ikan tilapia + 1 cup sweet potato + salad
              ~40g P | 40g C | 6g F | 366 kcal
  
  Before Bed: 200g greek yogurt + 30g almonds
              ~20g P | 10g C | 18g F | 290 kcal
""")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Contest Prep Macro Calculator")
    parser.add_argument("--weight", type=float, required=True, help="Body weight in kg")
    parser.add_argument("--height", type=float, required=True, help="Height in cm")
    parser.add_argument("--age", type=int, required=True, help="Age in years")
    parser.add_argument("--gender", default="male", choices=["male", "female"])
    parser.add_argument("--bodyfat", type=float, default=15, help="Estimated body fat %%")
    parser.add_argument("--weeks", type=int, default=16, help="Weeks until show")
    args = parser.parse_args()
    
    print_plan(args.weight, args.height, args.age, args.gender, args.bodyfat, args.weeks)
