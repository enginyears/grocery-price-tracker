# 🛒 Multi-Platform Grocery Price Tracker & Analytics Dashboard

An automated, intelligent grocery and essentials price comparison engine for **PIN 743133 (Noapara / Shyamnagar, West Bengal)**.

Tracks, standardizes, and compares prices across **Blinkit, Flipkart Minutes, JioMart, BigBasket, and Local Mandi rates**, updating a live Google Sheets Dashboard featuring a **full embedded 30-day interactive Line Chart** and automated hands-off daily refreshes via **GitHub Actions**.

---

## 🌟 Key Features

1. **📊 Interactive Dashboard with Full Embedded Line Chart**:
   - **X-Axis**: Dates across the last 30 days.
   - **Y-Axis**: Price amount (₹ / Standard Unit).
   - **Multi-line Series**: Dynamic colored curves for **Blinkit, Flipkart Minutes, JioMart, BigBasket, and Local Market Rate**, re-rendering instantly whenever a product is selected.
   - **KPI Highlights**: Shows the cheapest platform today, biggest discount %, and total tracked essentials.
2. **⚖️ Smart Unit Normalization**:
   - Compares apples-to-apples by converting non-uniform pack sizes (100g, 250g, 500g, 1kg, 900ml, 1L, 5L) to **Rate per 1 kg / 1 Litre / 1 Piece**.
3. **🥦 4 Category Tabs**:
   - `🥦 Vegetables`, `🍎 Fruits`, `🌾 Grains & Staples`, `🛢️ Oils & Ghee`.
   - Displays Pack Size, Offer Price, Rate per Std Unit, Discount %, 30-Day Average, and 30-Day Lowest Rate.
4. **🛒 Local Market Logging (`🛒 Local_Market_Log`)**:
   - Enter offline mandi purchases to compare street rates against quick commerce delivery apps.
5. **⏰ Completely Hands-Off Daily Refresh**:
   - Runs automatically on GitHub Actions at 7:00 AM IST daily — no browser or PC required.

---

## 🚀 Setup Instructions

### Step 1: Initialize the Google Sheet
1. Open your Google Sheet: [Track Grocerry](https://docs.google.com/spreadsheets/d/1QRup-IhBdksnQ-no3eOW_cxRxYvFs951I5BZhDD63aI/edit)
2. In Google Sheets, navigate to **Extensions > Apps Script**.
3. Delete any default code in the editor, copy the contents of [`apps_script/Code.gs`](apps_script/Code.gs), and paste it into `Code.gs`.
4. Click **Save** (💾).
5. In the toolbar, select **`setupGroceryTracker`** from the function dropdown and click **Run**.
   * *When prompted, authorize the script to format and manage the sheet.*
   * All sheets (`📊 Dashboard`, category tabs, `Local_Market_Log`, and `Price_History`) with the embedded line chart will be created instantly!

### Step 2: Deploy Webhook for Automated Daily Crawls
1. In the Apps Script editor, click **Deploy > New deployment** (top right).
2. Click the gear icon next to "Select type" and select **Web app**.
3. Set the following settings:
   * **Description**: `Daily Grocery Price Webhook`
   * **Execute as**: `Me`
   * **Who has access**: `Anyone`
4. Click **Deploy**.
5. Copy the **Web App URL** (it ends with `/exec`).

### Step 3: Link to GitHub Actions
1. Push this repository to your GitHub account:
   ```bash
   git remote add origin https://github.com/<YOUR_USERNAME>/grocery-price-tracker.git
   git branch -M main
   git push -u origin main
   ```
2. In your GitHub repository, go to **Settings > Secrets and variables > Actions**.
3. Click **New repository secret**:
   * **Name**: `GOOGLE_SHEET_WEBHOOK_URL`
   * **Secret**: Paste your Google Apps Script Web App URL from Step 2.
4. Click **Add secret**.

🎉 **That's it!** GitHub Actions will automatically run every morning at 7:00 AM IST, scrape the latest prices, and push them to your Google Sheet without you needing to do anything. You can also trigger a manual run anytime by visiting the **Actions** tab on GitHub and clicking **Run workflow**.

---

## 📁 Repository Structure

```
grocery-price-tracker/
├── .github/
│   └── workflows/
│       └── daily_price_tracker.yml  # GitHub Actions cron scheduler (7 AM IST)
├── apps_script/
│   └── Code.gs                      # Google Apps Script (Dashboard, Chart, Webhook)
├── scraper/
│   ├── unit_normalizer.py           # Standardizes 100g/250g/500g/1kg/1L
│   ├── matcher.py                   # Canonical entity mapping & fuzzy matcher
│   ├── scrapers.py                  # Scraper modules for Blinkit, Flipkart, Jio, BB
│   └── main.py                      # Main pipeline orchestrator & webhook publisher
├── requirements.txt
├── .gitignore
└── README.md
```
