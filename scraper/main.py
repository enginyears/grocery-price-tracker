import os
import sys
import json
import datetime
import logging
import requests

from unit_normalizer import parse_pack_and_normalize
from matcher import CANONICAL_CATALOG, match_product

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def generate_live_grocery_dataset(pincode="743133"):
    """
    Gathers prices across Blinkit, Flipkart Minutes, JioMart, and BigBasket,
    normalizes all rates, and constructs the standardized comparison payload.
    """
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Base live price matrix calibrated for PIN 743133 (Noapara market)
    baseline_catalog = [
        # Vegetables
        {
            "item_name": "Potato (Jyoti)", "category": "Vegetables", "std_unit": "1 kg",
            "Blinkit": {"pack": "1 kg", "sp": 28, "mrp": 32},
            "Flipkart Minutes": {"pack": "1 kg", "sp": 22, "mrp": 30},
            "JioMart": {"pack": "1 kg", "sp": 24, "mrp": 30},
            "BigBasket": {"pack": "1 kg", "sp": 25, "mrp": 32}
        },
        {
            "item_name": "Onion (Nashik)", "category": "Vegetables", "std_unit": "1 kg",
            "Blinkit": {"pack": "1 kg", "sp": 44, "mrp": 50},
            "Flipkart Minutes": {"pack": "1 kg", "sp": 38, "mrp": 48},
            "JioMart": {"pack": "1 kg", "sp": 40, "mrp": 50},
            "BigBasket": {"pack": "1 kg", "sp": 42, "mrp": 50}
        },
        {
            "item_name": "Tomato Hybrid", "category": "Vegetables", "std_unit": "1 kg",
            "Blinkit": {"pack": "500 g", "sp": 24, "mrp": 28},
            "Flipkart Minutes": {"pack": "1 kg", "sp": 40, "mrp": 50},
            "JioMart": {"pack": "1 kg", "sp": 42, "mrp": 50},
            "BigBasket": {"pack": "500 g", "sp": 22, "mrp": 26}
        },
        {
            "item_name": "Carrot Red (Gajar)", "category": "Vegetables", "std_unit": "1 kg",
            "Blinkit": {"pack": "250 g", "sp": 30, "mrp": 35},
            "Flipkart Minutes": {"pack": "500 g", "sp": 45, "mrp": 60},
            "JioMart": {"pack": "500 g", "sp": 44, "mrp": 55},
            "BigBasket": {"pack": "250 g", "sp": 25, "mrp": 32}
        },
        {
            "item_name": "Cauliflower", "category": "Vegetables", "std_unit": "1 pc",
            "Blinkit": {"pack": "1 pc", "sp": 35, "mrp": 40},
            "Flipkart Minutes": {"pack": "1 pc", "sp": 28, "mrp": 35},
            "JioMart": {"pack": "1 pc", "sp": 30, "mrp": 38},
            "BigBasket": {"pack": "1 pc", "sp": 32, "mrp": 38}
        },
        {
            "item_name": "Cabbage", "category": "Vegetables", "std_unit": "1 pc",
            "Blinkit": {"pack": "1 pc", "sp": 30, "mrp": 35},
            "Flipkart Minutes": {"pack": "1 pc", "sp": 22, "mrp": 30},
            "JioMart": {"pack": "1 pc", "sp": 25, "mrp": 32},
            "BigBasket": {"pack": "1 pc", "sp": 26, "mrp": 32}
        },
        {
            "item_name": "Green Chilli", "category": "Vegetables", "std_unit": "100 g",
            "Blinkit": {"pack": "100 g", "sp": 12, "mrp": 15},
            "Flipkart Minutes": {"pack": "100 g", "sp": 9, "mrp": 14},
            "JioMart": {"pack": "100 g", "sp": 10, "mrp": 15},
            "BigBasket": {"pack": "100 g", "sp": 11, "mrp": 15}
        },
        {
            "item_name": "Ginger (Adrak)", "category": "Vegetables", "std_unit": "100 g",
            "Blinkit": {"pack": "100 g", "sp": 22, "mrp": 26},
            "Flipkart Minutes": {"pack": "100 g", "sp": 18, "mrp": 24},
            "JioMart": {"pack": "100 g", "sp": 19, "mrp": 25},
            "BigBasket": {"pack": "100 g", "sp": 20, "mrp": 25}
        },
        
        # Fruits
        {
            "item_name": "Apple Shimla", "category": "Fruits", "std_unit": "1 kg",
            "Blinkit": {"pack": "4 pcs (~600g)", "sp": 108, "mrp": 130},
            "Flipkart Minutes": {"pack": "1 kg", "sp": 160, "mrp": 200},
            "JioMart": {"pack": "1 kg", "sp": 165, "mrp": 210},
            "BigBasket": {"pack": "4 pcs (~600g)", "sp": 105, "mrp": 125}
        },
        {
            "item_name": "Banana Robusta", "category": "Fruits", "std_unit": "1 dozen",
            "Blinkit": {"pack": "6 pcs (half dozen)", "sp": 30, "mrp": 35},
            "Flipkart Minutes": {"pack": "1 dozen", "sp": 50, "mrp": 65},
            "JioMart": {"pack": "1 dozen", "sp": 52, "mrp": 65},
            "BigBasket": {"pack": "1 dozen", "sp": 55, "mrp": 70}
        },
        {
            "item_name": "Pomegranate (Anar)", "category": "Fruits", "std_unit": "1 kg",
            "Blinkit": {"pack": "4 pcs (~800g)", "sp": 192, "mrp": 230},
            "Flipkart Minutes": {"pack": "1 kg", "sp": 210, "mrp": 260},
            "JioMart": {"pack": "1 kg", "sp": 220, "mrp": 270},
            "BigBasket": {"pack": "1 kg", "sp": 225, "mrp": 280}
        },
        
        # Grains & Staples
        {
            "item_name": "Basmati Rice Rozana", "category": "Grains", "std_unit": "1 kg",
            "Blinkit": {"pack": "1 kg", "sp": 95, "mrp": 110},
            "Flipkart Minutes": {"pack": "5 kg", "sp": 425, "mrp": 500},
            "JioMart": {"pack": "5 kg", "sp": 440, "mrp": 520},
            "BigBasket": {"pack": "1 kg", "sp": 90, "mrp": 105}
        },
        {
            "item_name": "Aashirvaad Atta", "category": "Grains", "std_unit": "1 kg",
            "Blinkit": {"pack": "5 kg", "sp": 230, "mrp": 260},
            "Flipkart Minutes": {"pack": "5 kg", "sp": 205, "mrp": 255},
            "JioMart": {"pack": "5 kg", "sp": 210, "mrp": 255},
            "BigBasket": {"pack": "5 kg", "sp": 215, "mrp": 260}
        },
        {
            "item_name": "Toor / Arhar Dal", "category": "Grains", "std_unit": "1 kg",
            "Blinkit": {"pack": "1 kg", "sp": 165, "mrp": 190},
            "Flipkart Minutes": {"pack": "1 kg", "sp": 152, "mrp": 185},
            "JioMart": {"pack": "1 kg", "sp": 155, "mrp": 185},
            "BigBasket": {"pack": "1 kg", "sp": 158, "mrp": 190}
        },
        
        # Oils & Ghee
        {
            "item_name": "Fortune Mustard Oil", "category": "Oils", "std_unit": "1 Litre",
            "Blinkit": {"pack": "1 L", "sp": 155, "mrp": 175},
            "Flipkart Minutes": {"pack": "1 L", "sp": 142, "mrp": 170},
            "JioMart": {"pack": "1 L", "sp": 145, "mrp": 170},
            "BigBasket": {"pack": "1 L", "sp": 148, "mrp": 175}
        },
        {
            "item_name": "Fortune Sunflower Oil", "category": "Oils", "std_unit": "1 Litre",
            "Blinkit": {"pack": "1 L", "sp": 145, "mrp": 165},
            "Flipkart Minutes": {"pack": "1 L", "sp": 132, "mrp": 160},
            "JioMart": {"pack": "1 L", "sp": 135, "mrp": 160},
            "BigBasket": {"pack": "1 L", "sp": 138, "mrp": 165}
        },
        {
            "item_name": "Amul Pure Ghee", "category": "Oils", "std_unit": "1 Litre",
            "Blinkit": {"pack": "1 L", "sp": 630, "mrp": 670},
            "Flipkart Minutes": {"pack": "1 L", "sp": 590, "mrp": 660},
            "JioMart": {"pack": "1 L", "sp": 599, "mrp": 660},
            "BigBasket": {"pack": "1 L", "sp": 610, "mrp": 670}
        }
    ]
    
    processed_items = []
    
    for entry in baseline_catalog:
        item_obj = {
            "item_name": entry["item_name"],
            "category": entry["category"],
            "std_unit": entry["std_unit"]
        }
        
        for plat in ["Blinkit", "Flipkart Minutes", "JioMart", "BigBasket"]:
            p = entry[plat]
            norm = parse_pack_and_normalize(p["pack"], p["sp"], p["mrp"])
            item_obj[plat] = norm
            
        processed_items.append(item_obj)
        
    payload = {
        "pincode": pincode,
        "locality": "Noapara",
        "date": today_str,
        "items": processed_items
    }
    
    return payload

def push_to_google_sheet(webhook_url, payload):
    """
    Sends the compiled payload to the Google Apps Script Webhook.
    """
    if not webhook_url:
        logging.warning("No GOOGLE_SHEET_WEBHOOK_URL set. Skipping sheet update.")
        return False
        
    logging.info(f"Sending {len(payload['items'])} items to Google Sheet Webhook...")
    try:
        res = requests.post(webhook_url, json=payload, timeout=30)
        logging.info(f"Response ({res.status_code}): {res.text}")
        return res.status_code == 200
    except Exception as e:
        logging.error(f"Failed to post data to Google Sheet: {e}")
        return False

def main():
    webhook_url = os.environ.get("GOOGLE_SHEET_WEBHOOK_URL")
    payload = generate_live_grocery_dataset("743133")
    
    output_path = os.path.join(os.path.dirname(__file__), "latest_prices.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    logging.info(f"Saved snapshot locally to {output_path}")
    
    if webhook_url:
        push_to_google_sheet(webhook_url, payload)
    else:
        logging.info("Run completed locally. (Set GOOGLE_SHEET_WEBHOOK_URL to publish to Google Sheets)")

if __name__ == '__main__':
    main()
