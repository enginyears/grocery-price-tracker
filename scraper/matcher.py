import re

# Canonical catalog mapping rules for PIN 743133 essentials
CANONICAL_CATALOG = [
    # Vegetables
    {"name": "Potato (Jyoti)", "category": "Vegetables", "std_unit": "1 kg", "aliases": ["jyoti potato", "potato jyoti", "aloo jyoti", "potato / aloo", "fresh potato"]},
    {"name": "Onion (Nashik)", "category": "Vegetables", "std_unit": "1 kg", "aliases": ["onion", "pyaz", "nasik onion", "red onion", "fresh onion"]},
    {"name": "Tomato Hybrid", "category": "Vegetables", "std_unit": "1 kg", "aliases": ["tomato", "hybrid tomato", "tamatar", "tomato hybrid fresh"]},
    {"name": "Carrot Red (Gajar)", "category": "Vegetables", "std_unit": "1 kg", "aliases": ["carrot", "gajar", "red carrot", "carrot red"]},
    {"name": "Cauliflower", "category": "Vegetables", "std_unit": "1 pc", "aliases": ["cauliflower", "phool gobi", "phulgobi"]},
    {"name": "Cabbage", "category": "Vegetables", "std_unit": "1 pc", "aliases": ["cabbage", "patta gobi", "bandhagobi"]},
    {"name": "Green Chilli", "category": "Vegetables", "std_unit": "100 g", "aliases": ["green chilli", "hari mirch", "chilli green"]},
    {"name": "Ginger (Adrak)", "category": "Vegetables", "std_unit": "100 g", "aliases": ["ginger", "adrak", "fresh ginger"]},
    
    # Fruits
    {"name": "Apple Shimla", "category": "Fruits", "std_unit": "1 kg", "aliases": ["apple shimla", "shimla apple", "royal gala apple", "fresh apple"]},
    {"name": "Banana Robusta", "category": "Fruits", "std_unit": "1 dozen", "aliases": ["banana robusta", "robusta banana", "kela", "banana"]},
    {"name": "Pomegranate (Anar)", "category": "Fruits", "std_unit": "1 kg", "aliases": ["pomegranate", "anar", "dalim"]},
    
    # Grains & Staples
    {"name": "Basmati Rice Rozana", "category": "Grains", "std_unit": "1 kg", "aliases": ["basmati rice", "rozana basmati", "india gate rozana", "daawat rozana"]},
    {"name": "Aashirvaad Atta", "category": "Grains", "std_unit": "1 kg", "aliases": ["aashirvaad atta", "aashirvaad superior", "sharbati atta", "whole wheat atta"]},
    {"name": "Toor / Arhar Dal", "category": "Grains", "std_unit": "1 kg", "aliases": ["toor dal", "arhar dal", "tuvar dal"]},
    
    # Oils & Ghee
    {"name": "Fortune Mustard Oil", "category": "Oils", "std_unit": "1 Litre", "aliases": ["fortune mustard", "kachi ghani mustard oil", "mustard oil fortune"]},
    {"name": "Fortune Sunflower Oil", "category": "Oils", "std_unit": "1 Litre", "aliases": ["fortune sunflower", "sunlite sunflower oil", "sunflower oil fortune"]},
    {"name": "Amul Pure Ghee", "category": "Oils", "std_unit": "1 Litre", "aliases": ["amul ghee", "amul pure ghee", "cow ghee amul"]}
]

def match_product(title):
    """
    Matches an incoming scraped title to our canonical product catalog.
    """
    clean_title = re.sub(r'[^a-zA-Z0-9\s]', ' ', title.lower())
    words = set(clean_title.split())
    
    best_item = None
    max_score = 0
    
    for item in CANONICAL_CATALOG:
        for alias in item["aliases"]:
            alias_words = set(alias.split())
            if alias_words.issubset(words):
                score = len(alias_words) * 2
                if score > max_score:
                    max_score = score
                    best_item = item
                    
    return best_item
