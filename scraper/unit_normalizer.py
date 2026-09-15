import re

def parse_pack_and_normalize(pack_str, price, mrp=None):
    """
    Parses arbitrary pack strings and calculates normalized price per standard reference unit.
    
    Standard Reference Units:
    - Weight: 1 kg (or 100g for herbs/chilli/garlic)
    - Volume: 1 Litre
    - Count: 1 Piece / 1 Dozen
    
    Returns:
        dict: {
            'pack_size': str,
            'selling_price': float,
            'mrp': float,
            'std_unit': str,
            'rate_per_unit': float,
            'discount_pct': int
        }
    """
    if not pack_str or not price:
        return None
        
    s = str(pack_str).lower().strip()
    price = float(price)
    mrp = float(mrp) if mrp else price
    
    # 1. Litres / Millilitres (Liquids)
    if 'l' in s or 'ml' in s or 'litre' in s:
        ml_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:ml|milli)', s)
        l_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:l|ltr|litre)', s)
        
        volume_litres = 1.0
        if ml_match:
            volume_litres = float(ml_match.group(1)) / 1000.0
        elif l_match:
            volume_litres = float(l_match.group(1))
            
        rate_per_unit = round(price / volume_litres, 2) if volume_litres > 0 else price
        std_unit = "1 Litre"
        
    # 2. Grams / Kilograms (Solid Produce & Staples)
    elif 'g' in s or 'kg' in s or 'gm' in s:
        kg_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:kg|kilo)', s)
        g_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:g|gm|gram)', s)
        
        weight_kg = 1.0
        if kg_match:
            weight_kg = float(kg_match.group(1))
        elif g_match:
            weight_kg = float(g_match.group(1)) / 1000.0
            
        rate_per_unit = round(price / weight_kg, 2) if weight_kg > 0 else price
        std_unit = "1 kg"
        
    # 3. Count / Pieces / Dozen
    elif 'pc' in s or 'piece' in s or 'bunch' in s or 'unit' in s:
        pc_match = re.search(r'(\d+)\s*(?:pc|piece|unit|bunch)', s)
        count = float(pc_match.group(1)) if pc_match else 1.0
        rate_per_unit = round(price / count, 2) if count > 0 else price
        std_unit = "1 Piece"
        
    elif 'dozen' in s or 'doz' in s:
        rate_per_unit = price
        std_unit = "1 Dozen"
        
    else:
        # Fallback default assuming 1 unit
        rate_per_unit = price
        std_unit = "1 Unit"
        
    discount_pct = round(((mrp - price) / mrp) * 100) if mrp > price else 0
    
    return {
        'pack_size': pack_str,
        'selling_price': price,
        'mrp': mrp,
        'std_unit': std_unit,
        'rate_per_unit': rate_per_unit,
        'discount_pct': max(0, discount_pct)
    }

# Unit tests
if __name__ == '__main__':
    test_cases = [
        ("100 g", 20, 25),      # Expected: 200/kg
        ("250 g", 30, 35),      # Expected: 120/kg
        ("500 gm", 45, 50),     # Expected: 90/kg
        ("1 kg", 25, 30),       # Expected: 25/kg
        ("5 kg", 420, 480),     # Expected: 84/kg
        ("900 ml pouch", 135, 150), # Expected: 150/L
        ("1 Litre", 145, 160),  # Expected: 145/L
        ("1 pc", 25, 30),       # Expected: 25/pc
    ]
    for p, pr, mrp in test_cases:
        res = parse_pack_and_normalize(p, pr, mrp)
        print(f"Pack: {p:>14} | Price: Rs.{pr:>3} -> Std: {res['std_unit']} | Normalized Rate: Rs.{res['rate_per_unit']}/unit ({res['discount_pct']}% OFF)")
