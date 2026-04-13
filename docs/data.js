window.DOC_DATA = [
  // --- Measures ---
  { name: "0000_Blank", type: "Measure", table: "_Measures", formula: "BLANK()", description: "" },
  { name: "0100_Number of Bottles Sold", type: "Measure", table: "_Measures", formula: "sum(GoalMain[bottles_sold])", description: "Total number of bottles sold." },
  { name: "0101_Bottle Volume Sold", type: "Measure", table: "_Measures", formula: "sum(GoalMain[volume_sold_liters])", description: "Total bottle volume sold in liters." },
  { name: "0102_Sales Amount", type: "Measure", table: "_Measures", formula: "sum(GoalMain[sale_dollars])", description: "Total sales amount in dollars." },
  { name: "0104_Cost of Goods Sold", type: "Measure", table: "_Measures", formula: "SUMX(GoalMain, GoalMain[state_bottle_cost]*GoalMain[bottles_sold])", description: "Total cost of goods sold." },
  { name: "0105_Gross Profit", type: "Measure", table: "_Measures", formula: "[0102_Sales Amount]-[0104_Cost of Goods Sold]", description: "Gross profit (sales minus cost of goods sold)." },
  { name: "0106_Gross Margin Pct", type: "Measure", table: "_Measures", formula: "DIVIDE([0105_Gross Profit], [0102_Sales Amount], BLANK())", description: "Gross margin as a percentage." },
  // ... (add all other measures, functions, and calculated columns in this format)

  // --- Functions ---
  { name: "WeekStart", type: "Function", formula: "(_date : DATETIME) => _date - WEEKDAY(_date,2) + 1", description: "Returns the start date of the week for a given date." },
  { name: "MonthStart", type: "Function", formula: "(_date : DATETIME) => EOMONTH(_date,-1) + 1", description: "Returns the first day of the month for a given date." },
  { name: "QuarterStart", type: "Function", formula: "(_date : DATETIME) => var _month = (3*INT((MONTH(_date)-1)/3))+1 RETURN DATE(YEAR(_date), _month, 1)", description: "Returns the first day of the quarter for a given date." },
  { name: "YearStart", type: "Function", formula: "(_date : DATETIME) => DATE(YEAR(_date),1,1)", description: "Returns the first day of the year for a given date." },
  // ... (add all other functions)

  // --- Calculated Columns ---
  // Example: { name: "Profit Margin", type: "Calculated Column", table: "FactMain", formula: "[Profit] / [Sales]", description: "Profit margin for each row." },
];
