# F&B Product Category Taxonomy

## Standard Categories for Malaysian F&B

### 🍔 Burger
- Keywords: BURGER, PATTY
- Price range: MYR 5.00 - 12.00
- Average: MYR 7.90 (based on KPJD data)

### 🥪 Sandwich
- Keywords: SANDWICH, TOAST, WRAP
- Price range: MYR 3.00 - 8.00
- Average: MYR 3.90 (based on KPJD data)

### ☕ Hot Drinks
- Keywords: MILO, KOPI, TEH, COFFEE, LATTE, CAPPUCCINO, HOT CHOCOLATE
- Price range: MYR 2.00 - 6.00
- Average: MYR 2.90 (based on KPJD data)

### 🥤 Cold Drinks
- Keywords: MILK, STRAWBERRY, CHOCOLATE, CHOCO, ZUS, ICED, COLD, SHAKE
- Price range: MYR 2.00 - 7.00
- Average: MYR 3.50 (based on KPJD data)

### 🍟 Sides & Snacks
- Keywords: FRIES, NUGGET, CASHEW, ROLLS, CHIPS, ONION RING
- Price range: MYR 2.00 - 6.00
- Average: MYR 3.50 (based on KPJD data)

### 📦 Other
- Keywords: SPRITZER, DRINHO, MINERAL, WATER, CAN, BOTTLE
- Price range: MYR 1.00 - 3.00
- Average: MYR 1.90 (based on KPJD data)

## Category Mapping Logic

```python
def categorize_product(product_name: str) -> str:
    """Map product name to F&B category."""
    p = product_name.upper()
    
    if 'BURGER' in p:
        return '🍔 Burger'
    elif 'SANDWICH' in p:
        return '🥪 Sandwich'
    elif any(x in p for x in ['MILO', 'KOPI', 'TEH', 'COFFEE', 'LATTE', 'CAPPUCCINO']):
        return '☕ Hot Drinks'
    elif any(x in p for x in ['MILK', 'CHOCOLATE', 'CHOCO', 'STRAWBERRY', 'ZUS', 'SHAKE']):
        return '🥤 Cold Drinks'
    elif any(x in p for x in ['FRIES', 'NUGGET', 'CASHEW', 'ROLLS', 'CHIPS']):
        return '🍟 Sides & Snacks'
    elif any(x in p for x in ['SPRITZER', 'DRINHO', 'MINERAL', 'WATER']):
        return '📦 Other Drinks'
    else:
        return '📦 Lain-lain'
```

## Price Benchmarks (Malaysian F&B, 2026)

| Category | Low | Average | High |
|----------|-----|---------|------|
| Burger | 5.00 | 7.90 | 12.00 |
| Sandwich | 3.00 | 3.90 | 8.00 |
| Hot Drinks | 2.00 | 2.90 | 6.00 |
| Cold Drinks | 2.00 | 3.50 | 7.00 |
| Sides | 2.00 | 3.50 | 6.00 |
| Water/Soda | 1.00 | 1.90 | 3.00 |

## Upsell Opportunities

Based on typical F&B patterns:
1. **Bundle deals**: Burger + Drink = MYR 9.90 (vs separate MYR 10.80)
2. **Combo meals**: Burger + Fries + Drink = MYR 12.90
3. **Happy hour**: Discount on drinks during slow periods
4. **Loyalty program**: 10th purchase free

## Revenue Share Benchmarks

For a typical burger stall:
- Burger: 50-60% of revenue (hero product)
- Drinks: 25-35% of revenue (high margin)
- Sides: 10-15% of revenue (add-on)

If drinks are below 25%, consider:
- Better drink placement on menu
- Bundle deals with drinks
- New drink offerings
