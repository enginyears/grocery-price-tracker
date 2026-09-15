import re

def parse_pack_and_normalize(pack_str, price, mrp=None, url=""):
    """
    Parses arbitrary pack strings and calculates normalized price per standard reference unit,
    preserving the product verification URL.
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
        rate_per_unit = price
        std_unit = "1 Unit"
        
    discount_pct = round(((mrp - price) / mrp) * 100) if mrp > price else 0
    
    return {
        'pack_size': pack_str,
        'selling_price': price,
        'mrp': mrp,
        'std_unit': std_unit,
        'rate_per_unit': rate_per_unit,
        'discount_pct': max(0, discount_pct),
        'url': url or ""
    }
