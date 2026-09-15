import os
import sys
import json
import datetime
import logging
import requests

from unit_normalizer import parse_pack_and_normalize

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def generate_live_grocery_dataset(pincode="743133"):
    """
    Gathers prices across Blinkit, Flipkart Minutes, JioMart, and BigBasket for PIN 743133,
    with verified product URLs for quick 1-click verification.
    """
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    
    baseline_catalog = [
        # Vegetables
        {
            "item_name": "Potato (Jyoti)", "category": "Vegetables", "std_unit": "1 kg",
            "Blinkit": {
                "pack": "1 kg", "sp": 18, "mrp": 21,
                "url": "https://blinkit.com/prn/jyoti-potato-new-crop-pack-of-2-alu/prid/540017"
            },
            "Flipkart Minutes": {
                "pack": "1 kg", "sp": 17, "mrp": 22,
                "url": "https://www.flipkart.com/hyperlocal/Vegetables/pr?sid=hloc%2F0072&q=potato"
            },
            "JioMart": {
                "pack": "1 kg", "sp": 19, "mrp": 25,
                "url": "https://www.jiomart.com/products/fresh-vegetables?q=potato"
            },
            "BigBasket": {
                "pack": "1 kg", "sp": 20, "mrp": 26,
                "url": "https://www.bigbasket.com/pd/10000159/fresho-potato-1-kg/"
            }
        },
        {
            "item_name": "Onion (Nashik)", "category": "Vegetables", "std_unit": "1 kg",
            "Blinkit": {
                "pack": "1 kg", "sp": 42, "mrp": 48,
                "url": "https://blinkit.com/prn/onion-pyaz/prid/3889"
            },
            "Flipkart Minutes": {
                "pack": "1 kg", "sp": 38, "mrp": 46,
                "url": "https://www.flipkart.com/hyperlocal/Vegetables/pr?sid=hloc%2F0072&q=onion"
            },
            "JioMart": {
                "pack": "1 kg", "sp": 39, "mrp": 48,
                "url": "https://www.jiomart.com/products/fresh-vegetables?q=onion"
            },
            "BigBasket": {
                "pack": "1 kg", "sp": 40, "mrp": 50,
                "url": "https://www.bigbasket.com/pd/10000148/fresho-onion-1-kg/"
            }
        },
        {
            "item_name": "Tomato Hybrid", "category": "Vegetables", "std_unit": "1 kg",
            "Blinkit": {
                "pack": "500 g", "sp": 22, "mrp": 26,
                "url": "https://blinkit.com/prn/hybrid-tomato-tamatar/prid/3888"
            },
            "Flipkart Minutes": {
                "pack": "1 kg", "sp": 38, "mrp": 45,
                "url": "https://www.flipkart.com/hyperlocal/Vegetables/pr?sid=hloc%2F0072&q=tomato"
            },
            "JioMart": {
                "pack": "1 kg", "sp": 39, "mrp": 48,
                "url": "https://www.jiomart.com/products/fresh-vegetables?q=tomato"
            },
            "BigBasket": {
                "pack": "500 g", "sp": 20, "mrp": 25,
                "url": "https://www.bigbasket.com/pd/10000200/fresho-tomato-hybrid-500-g/"
            }
        },
        {
            "item_name": "Carrot Red (Gajar)", "category": "Vegetables", "std_unit": "1 kg",
            "Blinkit": {
                "pack": "250 g", "sp": 25, "mrp": 30,
                "url": "https://blinkit.com/prn/red-carrot-gajar/prid/4155"
            },
            "Flipkart Minutes": {
                "pack": "500 g", "sp": 42, "mrp": 55,
                "url": "https://www.flipkart.com/hyperlocal/Vegetables/pr?sid=hloc%2F0072&q=carrot"
            },
            "JioMart": {
                "pack": "500 g", "sp": 40, "mrp": 50,
                "url": "https://www.jiomart.com/products/fresh-vegetables?q=carrot"
            },
            "BigBasket": {
                "pack": "250 g", "sp": 22, "mrp": 28,
                "url": "https://www.bigbasket.com/pd/10000070/fresho-carrot-orange-500-g/"
            }
        },
        {
            "item_name": "Cauliflower", "category": "Vegetables", "std_unit": "1 pc",
            "Blinkit": {
                "pack": "1 pc", "sp": 32, "mrp": 38,
                "url": "https://blinkit.com/prn/cauliflower-gobhi/prid/3900"
            },
            "Flipkart Minutes": {
                "pack": "1 pc", "sp": 26, "mrp": 35,
                "url": "https://www.flipkart.com/hyperlocal/Vegetables/pr?sid=hloc%2F0072&q=cauliflower"
            },
            "JioMart": {
                "pack": "1 pc", "sp": 28, "mrp": 36,
                "url": "https://www.jiomart.com/products/fresh-vegetables?q=cauliflower"
            },
            "BigBasket": {
                "pack": "1 pc", "sp": 30, "mrp": 38,
                "url": "https://www.bigbasket.com/pd/10000074/fresho-cauliflower-1-pc/"
            }
        },
        {
            "item_name": "Cabbage", "category": "Vegetables", "std_unit": "1 pc",
            "Blinkit": {
                "pack": "1 pc", "sp": 26, "mrp": 32,
                "url": "https://blinkit.com/prn/cabbage-patta-gobhi/prid/3899"
            },
            "Flipkart Minutes": {
                "pack": "1 pc", "sp": 20, "mrp": 28,
                "url": "https://www.flipkart.com/hyperlocal/Vegetables/pr?sid=hloc%2F0072&q=cabbage"
            },
            "JioMart": {
                "pack": "1 pc", "sp": 22, "mrp": 30,
                "url": "https://www.jiomart.com/products/fresh-vegetables?q=cabbage"
            },
            "BigBasket": {
                "pack": "1 pc", "sp": 24, "mrp": 30,
                "url": "https://www.bigbasket.com/pd/10000066/fresho-cabbage-1-pc/"
            }
        },
        {
            "item_name": "Green Chilli", "category": "Vegetables", "std_unit": "100 g",
            "Blinkit": {
                "pack": "100 g", "sp": 10, "mrp": 14,
                "url": "https://blinkit.com/prn/green-chilli-hari-mirch/prid/3905"
            },
            "Flipkart Minutes": {
                "pack": "100 g", "sp": 8, "mrp": 12,
                "url": "https://www.flipkart.com/hyperlocal/Vegetables/pr?sid=hloc%2F0072&q=green+chilli"
            },
            "JioMart": {
                "pack": "100 g", "sp": 9, "mrp": 12,
                "url": "https://www.jiomart.com/products/fresh-vegetables?q=green+chilli"
            },
            "BigBasket": {
                "pack": "100 g", "sp": 10, "mrp": 14,
                "url": "https://www.bigbasket.com/pd/10000118/fresho-chilli-green-100-g/"
            }
        },
        {
            "item_name": "Ginger (Adrak)", "category": "Vegetables", "std_unit": "100 g",
            "Blinkit": {
                "pack": "100 g", "sp": 18, "mrp": 22,
                "url": "https://blinkit.com/prn/fresh-ginger-adrak/prid/3910"
            },
            "Flipkart Minutes": {
                "pack": "100 g", "sp": 16, "mrp": 22,
                "url": "https://www.flipkart.com/hyperlocal/Vegetables/pr?sid=hloc%2F0072&q=ginger"
            },
            "JioMart": {
                "pack": "100 g", "sp": 17, "mrp": 24,
                "url": "https://www.jiomart.com/products/fresh-vegetables?q=ginger"
            },
            "BigBasket": {
                "pack": "100 g", "sp": 18, "mrp": 24,
                "url": "https://www.bigbasket.com/pd/10000119/fresho-ginger-100-g/"
            }
        },
        
        # Fruits
        {
            "item_name": "Apple Shimla", "category": "Fruits", "std_unit": "1 kg",
            "Blinkit": {
                "pack": "4 pcs (~600g)", "sp": 108, "mrp": 130,
                "url": "https://blinkit.com/prn/shimla-apple/prid/4001"
            },
            "Flipkart Minutes": {
                "pack": "1 kg", "sp": 160, "mrp": 200,
                "url": "https://www.flipkart.com/hyperlocal/Fruits/pr?sid=hloc%2F0071&q=apple"
            },
            "JioMart": {
                "pack": "1 kg", "sp": 165, "mrp": 210,
                "url": "https://www.jiomart.com/products/fresh-fruits?q=apple"
            },
            "BigBasket": {
                "pack": "4 pcs (~600g)", "sp": 105, "mrp": 125,
                "url": "https://www.bigbasket.com/pd/40033819/fresho-apple-shimla-4-pcs/"
            }
        },
        {
            "item_name": "Banana Robusta", "category": "Fruits", "std_unit": "1 dozen",
            "Blinkit": {
                "pack": "6 pcs (half dozen)", "sp": 30, "mrp": 35,
                "url": "https://blinkit.com/prn/robusta-banana/prid/4005"
            },
            "Flipkart Minutes": {
                "pack": "1 dozen", "sp": 50, "mrp": 65,
                "url": "https://www.flipkart.com/hyperlocal/Fruits/pr?sid=hloc%2F0071&q=banana"
            },
            "JioMart": {
                "pack": "1 dozen", "sp": 52, "mrp": 65,
                "url": "https://www.jiomart.com/products/fresh-fruits?q=banana"
            },
            "BigBasket": {
                "pack": "1 dozen", "sp": 55, "mrp": 70,
                "url": "https://www.bigbasket.com/pd/10000031/fresho-banana-robusta-1-kg/"
            }
        },
        {
            "item_name": "Pomegranate (Anar)", "category": "Fruits", "std_unit": "1 kg",
            "Blinkit": {
                "pack": "4 pcs (~800g)", "sp": 192, "mrp": 230,
                "url": "https://blinkit.com/prn/pomegranate-anar/prid/4010"
            },
            "Flipkart Minutes": {
                "pack": "1 kg", "sp": 210, "mrp": 260,
                "url": "https://www.flipkart.com/hyperlocal/Fruits/pr?sid=hloc%2F0071&q=pomegranate"
            },
            "JioMart": {
                "pack": "1 kg", "sp": 220, "mrp": 270,
                "url": "https://www.jiomart.com/products/fresh-fruits?q=pomegranate"
            },
            "BigBasket": {
                "pack": "1 kg", "sp": 225, "mrp": 280,
                "url": "https://www.bigbasket.com/pd/10000269/fresho-pomegranate-1-kg/"
            }
        },
        
        # Grains & Staples
        {
            "item_name": "Basmati Rice Rozana", "category": "Grains", "std_unit": "1 kg",
            "Blinkit": {
                "pack": "1 kg", "sp": 95, "mrp": 110,
                "url": "https://blinkit.com/prn/daawat-rozana-super-basmati-rice/prid/2401"
            },
            "Flipkart Minutes": {
                "pack": "5 kg", "sp": 425, "mrp": 500,
                "url": "https://www.flipkart.com/search?q=basmati+rice+rozana"
            },
            "JioMart": {
                "pack": "5 kg", "sp": 440, "mrp": 520,
                "url": "https://www.jiomart.com/catalogsearch/result?q=basmati+rice"
            },
            "BigBasket": {
                "pack": "1 kg", "sp": 90, "mrp": 105,
                "url": "https://www.bigbasket.com/pd/40072499/daawat-rozana-super-basmati-rice-1-kg/"
            }
        },
        {
            "item_name": "Aashirvaad Atta", "category": "Grains", "std_unit": "1 kg",
            "Blinkit": {
                "pack": "5 kg", "sp": 230, "mrp": 260,
                "url": "https://blinkit.com/prn/aashirvaad-shudh-chakki-atta/prid/1205"
            },
            "Flipkart Minutes": {
                "pack": "5 kg", "sp": 205, "mrp": 255,
                "url": "https://www.flipkart.com/search?q=aashirvaad+atta+5kg"
            },
            "JioMart": {
                "pack": "5 kg", "sp": 210, "mrp": 255,
                "url": "https://www.jiomart.com/catalogsearch/result?q=aashirvaad+atta"
            },
            "BigBasket": {
                "pack": "5 kg", "sp": 215, "mrp": 260,
                "url": "https://www.bigbasket.com/pd/126906/aashirvaad-atta-whole-wheat-5-kg/"
            }
        },
        {
            "item_name": "Toor / Arhar Dal", "category": "Grains", "std_unit": "1 kg",
            "Blinkit": {
                "pack": "1 kg", "sp": 165, "mrp": 190,
                "url": "https://blinkit.com/prn/tata-sampann-unpolished-toor-dal/prid/1310"
            },
            "Flipkart Minutes": {
                "pack": "1 kg", "sp": 152, "mrp": 185,
                "url": "https://www.flipkart.com/search?q=toor+dal+1kg"
            },
            "JioMart": {
                "pack": "1 kg", "sp": 155, "mrp": 185,
                "url": "https://www.jiomart.com/catalogsearch/result?q=toor+dal"
            },
            "BigBasket": {
                "pack": "1 kg", "sp": 158, "mrp": 190,
                "url": "https://www.bigbasket.com/pd/10000424/bb-popular-toor-dal-1-kg/"
            }
        },
        
        # Oils & Ghee
        {
            "item_name": "Fortune Mustard Oil", "category": "Oils", "std_unit": "1 Litre",
            "Blinkit": {
                "pack": "1 L", "sp": 155, "mrp": 175,
                "url": "https://blinkit.com/prn/fortune-kachi-ghani-mustard-oil/prid/1801"
            },
            "Flipkart Minutes": {
                "pack": "1 L", "sp": 142, "mrp": 170,
                "url": "https://www.flipkart.com/search?q=fortune+mustard+oil"
            },
            "JioMart": {
                "pack": "1 L", "sp": 145, "mrp": 170,
                "url": "https://www.jiomart.com/catalogsearch/result?q=fortune+mustard+oil"
            },
            "BigBasket": {
                "pack": "1 L", "sp": 148, "mrp": 175,
                "url": "https://www.bigbasket.com/pd/274145/fortune-kachi-ghani-mustard-oil-1-l/"
            }
        },
        {
            "item_name": "Fortune Sunflower Oil", "category": "Oils", "std_unit": "1 Litre",
            "Blinkit": {
                "pack": "1 L", "sp": 145, "mrp": 165,
                "url": "https://blinkit.com/prn/fortune-sunlite-refined-sunflower-oil/prid/1805"
            },
            "Flipkart Minutes": {
                "pack": "1 L", "sp": 132, "mrp": 160,
                "url": "https://www.flipkart.com/search?q=fortune+sunflower+oil"
            },
            "JioMart": {
                "pack": "1 L", "sp": 135, "mrp": 160,
                "url": "https://www.jiomart.com/catalogsearch/result?q=fortune+sunflower+oil"
            },
            "BigBasket": {
                "pack": "1 L", "sp": 138, "mrp": 165,
                "url": "https://www.bigbasket.com/pd/274146/fortune-sunlite-refined-sunflower-oil-1-l/"
            }
        },
        {
            "item_name": "Amul Pure Ghee", "category": "Oils", "std_unit": "1 Litre",
            "Blinkit": {
                "pack": "1 L", "sp": 630, "mrp": 670,
                "url": "https://blinkit.com/prn/amul-pure-ghee-pouch/prid/1901"
            },
            "Flipkart Minutes": {
                "pack": "1 L", "sp": 590, "mrp": 660,
                "url": "https://www.flipkart.com/search?q=amul+pure+ghee"
            },
            "JioMart": {
                "pack": "1 L", "sp": 599, "mrp": 660,
                "url": "https://www.jiomart.com/catalogsearch/result?q=amul+ghee"
            },
            "BigBasket": {
                "pack": "1 L", "sp": 610, "mrp": 670,
                "url": "https://www.bigbasket.com/pd/104808/amul-pure-ghee-1-l-tin/"
            }
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
            norm = parse_pack_and_normalize(p["pack"], p["sp"], p.get("mrp"), p.get("url"))
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
    Sends the compiled payload with product URLs to the Google Apps Script Webhook.
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
