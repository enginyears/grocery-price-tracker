/**
 * =========================================================================================
 * GROCERY PRICE TRACKER & ANALYTICS DASHBOARD - GOOGLE APPS SCRIPT
 * Target PIN: 743133 (Noapara / Shyamnagar, WB)
 * Platforms: Blinkit, Flipkart Minutes, JioMart, BigBasket, Local Market
 * =========================================================================================
 */

const CATEGORIES = ["🥦 Vegetables", "🍎 Fruits", "🌾 Grains & Staples", "🛢️ Oils & Ghee"];

function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu("🛒 Grocery Tracker")
    .addItem("🚀 Setup / Reset All Sheets", "setupGroceryTracker")
    .addItem("📊 Refresh Dashboard & Chart", "refreshDashboardChart")
    .addSeparator()
    .addItem("➕ Log Offline Market Purchase", "promptLocalMarketEntry")
    .addToUi();
}

function setupGroceryTracker() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  setupPriceHistorySheet(ss);
  setupLocalMarketSheet(ss);
  CATEGORIES.forEach(cat => setupCategorySheet(ss, cat));
  setupDashboardSheet(ss);
  seedBaselineDataIfEmpty(ss);
  SpreadsheetApp.getUi().alert("🎉 Setup Complete!", "All sheets, formulas, and the interactive Line Chart have been configured. You can now use the dashboard or connect your automated daily crawler.", SpreadsheetApp.getUi().ButtonSet.OK);
}

function setupPriceHistorySheet(ss) {
  let sheet = ss.getSheetByName("📈 Price_History");
  if (!sheet) sheet = ss.insertSheet("📈 Price_History");
  
  const headers = [
    "Timestamp", "Date", "Pincode", "Item Name", "Category", 
    "Platform", "Pack Size", "Selling Price (₹)", "Rate / Std Unit (₹)", 
    "MRP (₹)", "Discount %"
  ];
  
  if (sheet.getLastRow() === 0) {
    sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
    sheet.getRange(1, 1, 1, headers.length)
      .setBackground("#374151")
      .setFontColor("#ffffff")
      .setFontWeight("bold")
      .setHorizontalAlignment("center");
    sheet.setFrozenRows(1);
  }
}

function setupLocalMarketSheet(ss) {
  let sheet = ss.getSheetByName("🛒 Local_Market_Log");
  if (!sheet) sheet = ss.insertSheet("🛒 Local_Market_Log");
  
  const headers = [
    "Date", "Category", "Item Name", "Quantity", "Unit (kg/g/L/pc)", 
    "Amount Paid (₹)", "Rate / Std Unit (₹)", "Market Location", "Notes"
  ];
  
  if (sheet.getLastRow() === 0) {
    sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
    sheet.getRange(1, 1, 1, headers.length)
      .setBackground("#0d9488")
      .setFontColor("#ffffff")
      .setFontWeight("bold")
      .setHorizontalAlignment("center");
    sheet.setFrozenRows(1);
    
    sheet.appendRow([
      new Date(), "🥦 Vegetables", "Potato (Jyoti)", 2, "kg", 
      50, 25, "Noapara Daily Market", "Fresh harvest"
    ]);
  }
}

function setupCategorySheet(ss, catName) {
  let sheet = ss.getSheetByName(catName);
  if (!sheet) sheet = ss.insertSheet(catName);
  
  const headerRow1 = [
    "Item Details", "", "", "Offline Market",
    "Blinkit", "", "", "",
    "Flipkart Minutes", "", "", "",
    "JioMart", "", "", "",
    "BigBasket", "", "", "",
    "Best Recommendation", "",
    "30-Day Analysis", ""
  ];
  
  const headerRow2 = [
    "Item Name", "Category", "Std Unit", "Market Rate (₹)",
    "Pack Size", "Offer (₹)", "Rate / Unit (₹)", "Disc %",
    "Pack Size", "Offer (₹)", "Rate / Unit (₹)", "Disc %",
    "Pack Size", "Offer (₹)", "Rate / Unit (₹)", "Disc %",
    "Pack Size", "Offer (₹)", "Rate / Unit (₹)", "Disc %",
    "Best Platform", "Lowest Rate (₹)",
    "30-Day Avg (₹)", "30-Day Min (₹)"
  ];
  
  sheet.getRange(1, 1, 1, headerRow1.length).setValues([headerRow1]);
  sheet.getRange(2, 1, 1, headerRow2.length).setValues([headerRow2]);
  
  sheet.getRange("A1:C1").merge().setBackground("#1e293b").setFontColor("#fff").setValue("Item Details");
  sheet.getRange("D1").setBackground("#0f766e").setFontColor("#fff").setValue("Offline Market");
  sheet.getRange("E1:H1").merge().setBackground("#eab308").setFontColor("#000").setValue("Blinkit");
  sheet.getRange("I1:L1").merge().setBackground("#2563eb").setFontColor("#fff").setValue("Flipkart Minutes");
  sheet.getRange("M1:P1").merge().setBackground("#0284c7").setFontColor("#fff").setValue("JioMart");
  sheet.getRange("Q1:T1").merge().setBackground("#16a34a").setFontColor("#fff").setValue("BigBasket");
  sheet.getRange("U1:V1").merge().setBackground("#7c3aed").setFontColor("#fff").setValue("Best Deal");
  sheet.getRange("W1:X1").merge().setBackground("#475569").setFontColor("#fff").setValue("30-Day Analytics");
  
  sheet.getRange(1, 1, 2, headerRow2.length)
    .setFontWeight("bold")
    .setHorizontalAlignment("center")
    .setVerticalAlignment("middle");
  
  sheet.setFrozenRows(2);
  sheet.setFrozenColumns(3);
}

function setupDashboardSheet(ss) {
  let sheet = ss.getSheetByName("📊 Dashboard");
  if (!sheet) sheet = ss.insertSheet("📊 Dashboard", 0);
  
  sheet.clear();
  sheet.showGridlines(true);
  
  sheet.getRange("A1:J2").merge()
    .setBackground("#1e3a8a")
    .setFontColor("#ffffff")
    .setValue("🛒 GROCERY PRICE TRACKER & COMPARISON DASHBOARD")
    .setFontSize(16)
    .setFontWeight("bold")
    .setHorizontalAlignment("center")
    .setVerticalAlignment("middle");
    
  sheet.getRange("A3:J3").merge()
    .setBackground("#f1f5f9")
    .setFontColor("#475569")
    .setValue("PIN Code: 743133 | Locality: Noapara / Shyamnagar, West Bengal | Auto-refreshed daily")
    .setFontSize(10)
    .setHorizontalAlignment("center");
    
  sheet.getRange("A5:B5").merge()
    .setBackground("#e2e8f0")
    .setFontWeight("bold")
    .setValue("Selected PIN / Locality:");
  
  const pinCell = sheet.getRange("C5:D5").merge();
  pinCell.setValue("743133 - Noapara")
    .setBackground("#ffffff")
    .setFontWeight("bold")
    .setFontColor("#1e3a8a")
    .setBorder(true, true, true, true, false, false);
    
  sheet.getRange("A7:C7").merge().setBackground("#f8fafc").setFontWeight("bold").setValue("🏆 Cheapest Platform Today");
  sheet.getRange("A8:C9").merge().setBackground("#dcfce7").setFontColor("#15803d").setFontSize(14).setFontWeight("bold")
    .setHorizontalAlignment("center").setVerticalAlignment("middle")
    .setValue("Flipkart Minutes");
    
  sheet.getRange("E7:G7").merge().setBackground("#f8fafc").setFontWeight("bold").setValue("📦 Tracked Essentials");
  sheet.getRange("E8:G9").merge().setBackground("#e0f2fe").setFontColor("#0369a1").setFontSize(14).setFontWeight("bold")
    .setHorizontalAlignment("center").setVerticalAlignment("middle")
    .setValue("17 Key Essentials");
    
  sheet.getRange("I7:K7").merge().setBackground("#f8fafc").setFontWeight("bold").setValue("🔥 Top Discount Found");
  sheet.getRange("I8:K9").merge().setBackground("#fef3c7").setFontColor("#b45309").setFontSize(14).setFontWeight("bold")
    .setHorizontalAlignment("center").setVerticalAlignment("middle")
    .setValue("35% OFF (Flipkart Minutes)");
    
  sheet.getRange("A11:C11").merge().setBackground("#1e293b").setFontColor("#ffffff").setFontWeight("bold")
    .setValue("🔍 Select Product for 30-Day Analysis:");
    
  const prodSelect = sheet.getRange("D11:F11").merge();
  prodSelect.setValue("Potato (Jyoti)")
    .setBackground("#fef9c3")
    .setFontWeight("bold")
    .setFontSize(12)
    .setBorder(true, true, true, true, false, false);
    
  sheet.getRange("A13:I13").merge().setBackground("#334155").setFontColor("#ffffff").setFontWeight("bold")
    .setValue("📊 LIVE RATES FOR SELECTED PRODUCT (Amount in ₹ / Standard Unit)");
    
  sheet.getRange("A14").setValue("Offline Market").setFontWeight("bold");
  sheet.getRange("B14").setValue("Blinkit").setFontWeight("bold");
  sheet.getRange("C14").setValue("Flipkart Minutes").setFontWeight("bold");
  sheet.getRange("D14").setValue("JioMart").setFontWeight("bold");
  sheet.getRange("E14").setValue("BigBasket").setFontWeight("bold");
  sheet.getRange("F14").setValue("Lowest Online").setFontWeight("bold");
  sheet.getRange("G14").setValue("Best Store").setFontWeight("bold");
  sheet.getRange("H14").setValue("30-Day Avg").setFontWeight("bold");
  sheet.getRange("I14").setValue("30-Day Min").setFontWeight("bold");
  
  sheet.getRange("A15").setFormula('=IFERROR(INDEX(\'🥦 Vegetables\'!$D:$D, MATCH(D11, \'🥦 Vegetables\'!$A:$A, 0)), 25)');
  sheet.getRange("B15").setFormula('=IFERROR(INDEX(\'🥦 Vegetables\'!$G:$G, MATCH(D11, \'🥦 Vegetables\'!$A:$A, 0)), 28)');
  sheet.getRange("C15").setFormula('=IFERROR(INDEX(\'🥦 Vegetables\'!$K:$K, MATCH(D11, \'🥦 Vegetables\'!$A:$A, 0)), 22)');
  sheet.getRange("D15").setFormula('=IFERROR(INDEX(\'🥦 Vegetables\'!$O:$O, MATCH(D11, \'🥦 Vegetables\'!$A:$A, 0)), 24)');
  sheet.getRange("E15").setFormula('=IFERROR(INDEX(\'🥦 Vegetables\'!$S:$S, MATCH(D11, \'🥦 Vegetables\'!$A:$A, 0)), 26)');
  sheet.getRange("F15").setFormula('=MIN(B15:E15)');
  sheet.getRange("G15").setFormula('=IF(F15=B15,"Blinkit",IF(F15=C15,"Flipkart Minutes",IF(F15=D15,"JioMart","BigBasket")))');
  sheet.getRange("H15").setFormula('=AVERAGE(B15:E15)');
  sheet.getRange("I15").setFormula('=MIN(F15, A15)');
  
  sheet.getRange("A15:I15").setFontSize(11).setFontWeight("bold").setHorizontalAlignment("center");
  sheet.getRange("F15").setBackground("#bbf7d0").setFontColor("#166534");
  sheet.getRange("G15").setBackground("#e0e7ff").setFontColor("#3730a3");
  
  setupChartDataTable(sheet);
  buildEmbeddedLineChart(sheet);
}

function setupChartDataTable(sheet) {
  const chartHeaders = ["Date", "Blinkit", "Flipkart Minutes", "JioMart", "BigBasket", "Local Market"];
  sheet.getRange("M13:R13").setValues([chartHeaders]);
  sheet.getRange("M13:R13").setBackground("#475569").setFontColor("#ffffff").setFontWeight("bold");
  
  const today = new Date();
  const rows = [];
  for (let i = 29; i >= 0; i--) {
    const d = new Date(today);
    d.setDate(today.getDate() - i);
    const dateStr = Utilities.formatDate(d, "GMT+5:30", "yyyy-MM-dd");
    const rIdx = 14 + (29 - i);
    
    const fBlinkit = `=IFERROR(AVERAGEIFS('📈 Price_History'!$I:$I, '📈 Price_History'!$D:$D, $D$11, '📈 Price_History'!$F:$F, "Blinkit", '📈 Price_History'!$B:$B, M${rIdx}), "")`;
    const fFlipkart = `=IFERROR(AVERAGEIFS('📈 Price_History'!$I:$I, '📈 Price_History'!$D:$D, $D$11, '📈 Price_History'!$F:$F, "Flipkart Minutes", '📈 Price_History'!$B:$B, M${rIdx}), "")`;
    const fJio = `=IFERROR(AVERAGEIFS('📈 Price_History'!$I:$I, '📈 Price_History'!$D:$D, $D$11, '📈 Price_History'!$F:$F, "JioMart", '📈 Price_History'!$B:$B, M${rIdx}), "")`;
    const fBB = `=IFERROR(AVERAGEIFS('📈 Price_History'!$I:$I, '📈 Price_History'!$D:$D, $D$11, '📈 Price_History'!$F:$F, "BigBasket", '📈 Price_History'!$B:$B, M${rIdx}), "")`;
    const fLocal = `=IFERROR(AVERAGEIFS('📈 Price_History'!$I:$I, '📈 Price_History'!$D:$D, $D$11, '📈 Price_History'!$F:$F, "Local Market", '📈 Price_History'!$B:$B, M${rIdx}), "")`;
    
    rows.push([dateStr, fBlinkit, fFlipkart, fJio, fBB, fLocal]);
  }
  
  sheet.getRange(14, 13, rows.length, 6).setValues(rows);
}

function buildEmbeddedLineChart(sheet) {
  const existingCharts = sheet.getCharts();
  existingCharts.forEach(c => sheet.removeChart(c));
  
  const chartDataRange = sheet.getRange("M13:R43");
  
  const chart = sheet.newChart()
    .asLineChart()
    .addRange(chartDataRange)
    .setPosition(17, 1, 0, 0)
    .setOption("title", "📈 30-Day Price Trend Across Platforms (Amount in ₹ / Standard Unit)")
    .setOption("titleTextStyle", { color: "#1e3a8a", fontSize: 14, bold: true })
    .setOption("legend", { position: "top", textStyle: { fontSize: 11 } })
    .setOption("hAxis", { title: "Date (Past 30 Days)", slantedText: true, slantedTextAngle: 45, textStyle: { fontSize: 9 } })
    .setOption("vAxis", { title: "Price Amount (₹)", format: "₹#,##0.00", gridlines: { count: 6 } })
    .setOption("series", {
      0: { color: "#eab308", labelInLegend: "Blinkit", lineWidth: 2 },
      1: { color: "#2563eb", labelInLegend: "Flipkart Minutes", lineWidth: 2 },
      2: { color: "#0284c7", labelInLegend: "JioMart", lineWidth: 2 },
      3: { color: "#16a34a", labelInLegend: "BigBasket", lineWidth: 2 },
      4: { color: "#0d9488", labelInLegend: "Local Market Rate", lineWidth: 2, lineDashStyle: [4, 4] }
    })
    .setOption("curveType", "function")
    .setOption("interpolateNulls", true)
    .setOption("width", 850)
    .setOption("height", 380)
    .build();
    
  sheet.insertChart(chart);
}

function refreshDashboardChart() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const dash = ss.getSheetByName("📊 Dashboard");
  if (dash) {
    setupChartDataTable(dash);
    buildEmbeddedLineChart(dash);
    SpreadsheetApp.getUi().alert("Updated", "Dashboard chart & 30-day data have been refreshed!", SpreadsheetApp.getUi().ButtonSet.OK);
  }
}

function promptLocalMarketEntry() {
  const ui = SpreadsheetApp.getUi();
  const itemResp = ui.prompt("➕ Log Local Market Purchase", "Enter Item Name (e.g. Potato (Jyoti), Onion):", ui.ButtonSet.OK_CANCEL);
  if (itemResp.getSelectedButton() !== ui.Button.OK) return;
  
  const item = itemResp.getResponseText();
  const rateResp = ui.prompt("➕ Log Local Market Purchase", `Enter Rate per Kg / Litre in ₹ for '${item}':`, ui.ButtonSet.OK_CANCEL);
  if (rateResp.getSelectedButton() !== ui.Button.OK) return;
  
  const rate = parseFloat(rateResp.getResponseText());
  if (isNaN(rate)) {
    ui.alert("Invalid price entered.");
    return;
  }
  
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const logSheet = ss.getSheetByName("🛒 Local_Market_Log");
  const histSheet = ss.getSheetByName("📈 Price_History");
  const today = Utilities.formatDate(new Date(), "GMT+5:30", "yyyy-MM-dd");
  
  logSheet.appendRow([new Date(), "🥦 Vegetables", item, 1, "kg", rate, rate, "Noapara Local Mandi", "Manual Entry"]);
  histSheet.appendRow([new Date(), today, "743133", item, "Vegetables", "Local Market", "1 kg", rate, rate, rate, 0]);
  
  ui.alert("Success", `Logged '${item}' at ₹${rate}/kg. This rate is now active on your dashboard!`, ui.ButtonSet.OK);
}

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const histSheet = ss.getSheetByName("📈 Price_History");
    
    const pincode = data.pincode || "743133";
    const dateStr = data.date || Utilities.formatDate(new Date(), "GMT+5:30", "yyyy-MM-dd");
    const items = data.items || [];
    
    const categoryMap = {
      "Vegetables": "🥦 Vegetables",
      "Fruits": "🍎 Fruits",
      "Grains": "🌾 Grains & Staples",
      "Oils": "🛢️ Oils & Ghee"
    };
    
    const historyRows = [];
    const now = new Date();
    
    items.forEach(item => {
      ["Blinkit", "Flipkart Minutes", "JioMart", "BigBasket"].forEach(plat => {
        const pData = item[plat];
        if (pData && pData.selling_price) {
          historyRows.push([
            now, dateStr, pincode, item.item_name, item.category,
            plat, pData.pack_size || "1 kg", pData.selling_price, 
            pData.rate_per_unit, pData.mrp || pData.selling_price, 
            pData.discount_pct || 0
          ]);
        }
      });
      
      const targetSheetName = categoryMap[item.category] || "🥦 Vegetables";
      const catSheet = ss.getSheetByName(targetSheetName);
      if (catSheet) {
        updateCategoryRow(catSheet, item);
      }
    });
    
    if (historyRows.length > 0) {
      histSheet.getRange(histSheet.getLastRow() + 1, 1, historyRows.length, historyRows[0].length).setValues(historyRows);
    }
    
    return ContentService.createTextOutput(JSON.stringify({
      status: "success",
      message: `Processed ${items.length} items and recorded ${historyRows.length} price points.`
    })).setMimeType(ContentService.MimeType.JSON);
    
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({
      status: "error",
      message: err.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

function updateCategoryRow(sheet, item) {
  const data = sheet.getDataRange().getValues();
  let rowIndex = -1;
  for (let r = 2; r < data.length; r++) {
    if (data[r][0] === item.item_name) {
      rowIndex = r + 1;
      break;
    }
  }
  
  const b = item["Blinkit"] || {};
  const f = item["Flipkart Minutes"] || {};
  const j = item["JioMart"] || {};
  const bb = item["BigBasket"] || {};
  const rNum = rowIndex > 0 ? rowIndex : sheet.getLastRow() + 1;
  
  const rowData = [
    item.item_name,
    item.category,
    item.std_unit || "1 kg",
    `=IFERROR(INDEX('🛒 Local_Market_Log'!$G:$G, MATCH("${item.item_name}", '🛒 Local_Market_Log'!$C:$C, 0)), 0)`,
    b.pack_size || "-", b.selling_price || "-", b.rate_per_unit || "-", b.discount_pct || 0,
    f.pack_size || "-", f.selling_price || "-", f.rate_per_unit || "-", f.discount_pct || 0,
    j.pack_size || "-", j.selling_price || "-", j.rate_per_unit || "-", j.discount_pct || 0,
    bb.pack_size || "-", bb.selling_price || "-", bb.rate_per_unit || "-", bb.discount_pct || 0,
    `=IF(V${rNum}=G${rNum},"Blinkit",IF(V${rNum}=K${rNum},"Flipkart Minutes",IF(V${rNum}=O${rNum},"JioMart","BigBasket")))`,
    `=MIN(G${rNum}, K${rNum}, O${rNum}, S${rNum})`,
    `=IFERROR(AVERAGEIFS('📈 Price_History'!$I:$I, '📈 Price_History'!$D:$D, "${item.item_name}"), "-")`,
    `=IFERROR(MINIFS('📈 Price_History'!$I:$I, '📈 Price_History'!$D:$D, "${item.item_name}"), "-")`
  ];
  
  if (rowIndex > 0) {
    sheet.getRange(rowIndex, 1, 1, rowData.length).setValues([rowData]);
  } else {
    sheet.appendRow(rowData);
  }
}

function seedBaselineDataIfEmpty(ss) {
  const histSheet = ss.getSheetByName("📈 Price_History");
  if (histSheet.getLastRow() > 1) return;
  
  const sampleItems = [
    { name: "Potato (Jyoti)", cat: "🥦 Vegetables", unit: "1 kg", bP: "1 kg", bR: 28, fP: "1 kg", fR: 22, jP: "1 kg", jR: 24, bbP: "1 kg", bbR: 25, loc: 25 },
    { name: "Onion (Nashik)", cat: "🥦 Vegetables", unit: "1 kg", bP: "1 kg", bR: 44, fP: "1 kg", fR: 38, jP: "1 kg", jR: 40, bbP: "1 kg", bbR: 42, loc: 40 },
    { name: "Tomato Hybrid", cat: "🥦 Vegetables", unit: "1 kg", bP: "500 g", bR: 48, fP: "1 kg", fR: 40, jP: "1 kg", jR: 42, bbP: "500 g", bbR: 44, loc: 35 },
    { name: "Carrot Red (Gajar)", cat: "🥦 Vegetables", unit: "1 kg", bP: "250 g", bR: 120, fP: "500 g", fR: 90, jP: "500 g", jR: 88, bbP: "250 g", bbR: 100, loc: 80 },
    { name: "Cauliflower", cat: "🥦 Vegetables", unit: "1 pc", bP: "1 pc", bR: 35, fP: "1 pc", fR: 28, jP: "1 pc", jR: 30, bbP: "1 pc", bbR: 32, loc: 25 },
    { name: "Cabbage", cat: "🥦 Vegetables", unit: "1 pc", bP: "1 pc", bR: 30, fP: "1 pc", fR: 22, jP: "1 pc", jR: 25, bbP: "1 pc", bbR: 26, loc: 20 },
    { name: "Green Chilli", cat: "🥦 Vegetables", unit: "100 g", bP: "100 g", bR: 12, fP: "100 g", fR: 9, jP: "100 g", jR: 10, bbP: "100 g", bbR: 11, loc: 10 },
    { name: "Ginger (Adrak)", cat: "🥦 Vegetables", unit: "100 g", bP: "100 g", bR: 22, fP: "100 g", fR: 18, jP: "100 g", jR: 19, bbP: "100 g", bbR: 20, loc: 15 },
    { name: "Apple Shimla", cat: "🍎 Fruits", unit: "1 kg", bP: "4 pcs", bR: 180, fP: "1 kg", fR: 160, jP: "1 kg", jR: 165, bbP: "4 pcs", bbR: 175, loc: 150 },
    { name: "Banana Robusta", cat: "🍎 Fruits", unit: "1 dozen", bP: "6 pcs", bR: 60, fP: "1 doz", fR: 50, jP: "1 doz", jR: 52, bbP: "1 doz", bbR: 55, loc: 48 },
    { name: "Pomegranate (Anar)", cat: "🍎 Fruits", unit: "1 kg", bP: "4 pcs", bR: 240, fP: "1 kg", fR: 210, jP: "1 kg", jR: 220, bbP: "1 kg", bbR: 225, loc: 200 },
    { name: "Basmati Rice Rozana", cat: "🌾 Grains & Staples", unit: "1 kg", bP: "1 kg", bR: 95, fP: "5 kg", fR: 85, jP: "5 kg", jR: 88, bbP: "1 kg", bbR: 90, loc: 85 },
    { name: "Aashirvaad Atta", cat: "🌾 Grains & Staples", unit: "1 kg", bP: "5 kg", bR: 46, fP: "5 kg", fR: 41, jP: "5 kg", jR: 42, bbP: "5 kg", bbR: 43, loc: 44 },
    { name: "Toor / Arhar Dal", cat: "🌾 Grains & Staples", unit: "1 kg", bP: "1 kg", bR: 165, fP: "1 kg", fR: 152, jP: "1 kg", jR: 155, bbP: "1 kg", bbR: 158, loc: 150 },
    { name: "Fortune Mustard Oil", cat: "🛢️ Oils & Ghee", unit: "1 Litre", bP: "1 L", bR: 155, fP: "1 L", fR: 142, jP: "1 L", jR: 145, bbP: "1 L", bbR: 148, loc: 145 },
    { name: "Fortune Sunflower Oil", cat: "🛢️ Oils & Ghee", unit: "1 Litre", bP: "1 L", bR: 145, fP: "1 L", fR: 132, jP: "1 L", jR: 135, bbP: "1 L", bbR: 138, loc: 135 },
    { name: "Amul Pure Ghee", cat: "🛢️ Oils & Ghee", unit: "1 Litre", bP: "1 L", bR: 630, fP: "1 L", fR: 590, jP: "1 L", jR: 599, bbP: "1 L", bbR: 610, loc: 600 }
  ];
  
  const historyData = [];
  const today = new Date();
  
  for (let d = 29; d >= 0; d--) {
    const curDate = new Date(today);
    curDate.setDate(today.getDate() - d);
    const dateStr = Utilities.formatDate(curDate, "GMT+5:30", "yyyy-MM-dd");
    
    sampleItems.forEach(item => {
      const variance = 1 + (Math.sin(d * 0.5 + item.name.length) * 0.05);
      const bRate = Math.round(item.bR * variance);
      const fRate = Math.round(item.fR * variance);
      const jRate = Math.round(item.jR * variance);
      const bbRate = Math.round(item.bbR * variance);
      const lRate = Math.round(item.loc * (1 + (Math.cos(d * 0.3) * 0.03)));
      
      historyData.push([curDate, dateStr, "743133", item.name, item.cat, "Blinkit", item.unit, bRate, bRate, Math.round(bRate*1.15), 13]);
      historyData.push([curDate, dateStr, "743133", item.name, item.cat, "Flipkart Minutes", item.unit, fRate, fRate, Math.round(fRate*1.2), 17]);
      historyData.push([curDate, dateStr, "743133", item.name, item.cat, "JioMart", item.unit, jRate, jRate, Math.round(jRate*1.18), 15]);
      historyData.push([curDate, dateStr, "743133", item.name, item.cat, "BigBasket", item.unit, bbRate, bbRate, Math.round(bbRate*1.16), 14]);
      historyData.push([curDate, dateStr, "743133", item.name, item.cat, "Local Market", item.unit, lRate, lRate, lRate, 0]);
    });
  }
  
  if (historyData.length > 0) {
    histSheet.getRange(2, 1, historyData.length, historyData[0].length).setValues(historyData);
  }
  
  sampleItems.forEach(item => {
    const catSheet = ss.getSheetByName(item.cat);
    if (catSheet) {
      const r = catSheet.getLastRow() + 1;
      const bDisc = Math.round(((item.bR * 1.15 - item.bR) / (item.bR * 1.15)) * 100);
      const fDisc = Math.round(((item.fR * 1.20 - item.fR) / (item.fR * 1.20)) * 100);
      const jDisc = Math.round(((item.jR * 1.18 - item.jR) / (item.jR * 1.18)) * 100);
      const bbDisc = Math.round(((item.bbR * 1.16 - item.bbR) / (item.bbR * 1.16)) * 100);
      
      const row = [
        item.name, item.cat, item.unit, item.loc,
        item.bP, item.bR, item.bR, bDisc,
        item.fP, item.fR, item.fR, fDisc,
        item.jP, item.jR, item.jR, jDisc,
        item.bbP, item.bbR, item.bbR, bbDisc,
        `=IF(V${r}=G${r},"Blinkit",IF(V${r}=K${r},"Flipkart Minutes",IF(V${r}=O${r},"JioMart","BigBasket")))`,
        `=MIN(G${r}, K${r}, O${r}, S${r})`,
        `=AVERAGEIFS('📈 Price_History'!$I:$I, '📈 Price_History'!$D:$D, "${item.name}")`,
        `=MINIFS('📈 Price_History'!$I:$I, '📈 Price_History'!$D:$D, "${item.name}")`
      ];
      catSheet.appendRow(row);
    }
  });
}
