Power Query Formula.Firewall fix for Python step

Problem
- Error: Formula.Firewall when query GoalMain runs Python and also references other queries (for example FactMain).
- Cause: Power Query privacy firewall blocks data combination between sources/queries and Python evaluation.

Recommended fix (single-query pattern)
- Build one dedicated forecast query where Source is the file/folder data source directly.
- Do not set Source = GoalMain or Source = FactMain.
- Run Python as the last transformation step.
- Pass only required columns into Python with Table.SelectColumns and Table.Buffer.

M template (Advanced Editor)

let
    Source = Folder.Files("C:\Users\PHUyJo3\OneDrive - NESTLE\Documents\projects\data\iowa"),
    FilteredHidden = Table.SelectRows(Source, each [Attributes]?[Hidden]? <> true),
    CsvOnly = Table.SelectRows(FilteredHidden, each Text.Lower([Extension]) = ".csv"),
    AddedData = Table.AddColumn(CsvOnly, "Data", each Csv.Document([Content], [Delimiter=",", Encoding=1252, QuoteStyle=QuoteStyle.None])),
    Expanded = Table.ExpandTableColumn(AddedData, "Data", {"Column1", "Column2", "Column21"}, {"invoice_and_item_number", "date", "bottles_sold"}),
    PromotedHeaders = Table.PromoteHeaders(Expanded, [PromoteAllScalars=true]),
    KeptColumns = Table.SelectColumns(PromotedHeaders, {"date", "bottles_sold"}),
    Typed = Table.TransformColumnTypes(KeptColumns, {{"date", type date}, {"bottles_sold", Int64.Type}}),
    // Table.Buffer forces Power Query to materialise ALL rows before Python runs.
    // Without this, the editor preview sends only ~1000 sample rows, which may
    // cover fewer than 12 months and trigger "Need at least 12 monthly points".
    Buffered = Table.Buffer(Typed),
    PythonResult = Python.Execute(
"import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

df = dataset[['date','bottles_sold']].copy()
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['bottles_sold'] = pd.to_numeric(df['bottles_sold'], errors='coerce')
df = df.dropna(subset=['date','bottles_sold'])

monthly = (
    df.set_index('date')['bottles_sold']
      .resample('MS')
      .sum()
      .asfreq('MS')
      .fillna(0.0)
      .astype(float)
)

if len(monthly) < 3:
    raise ValueError(f'Need at least 3 monthly points, got {len(monthly)}. Use Close & Apply to refresh with full data, not editor preview.')

seasonal = 'add' if len(monthly) >= 24 else None
seasonal_periods = 12 if seasonal else None

model = ExponentialSmoothing(
    monthly,
    trend='add',
    seasonal=seasonal,
    seasonal_periods=seasonal_periods,
    initialization_method='estimated'
)
fitted = model.fit(optimized=True)
future = fitted.forecast(12)
residual_std = (monthly - fitted.fittedvalues).std(ddof=1)

result = pd.DataFrame({
    'date': future.index.date,
    'bottles_sold_forecast': future.values,
    'forecast_lower_95': np.maximum(future.values - 1.96 * residual_std, 0),
    'forecast_upper_95': future.values + 1.96 * residual_std,
    'model': 'HoltWintersAdditive'
})",
        [dataset = Buffered]
    ),
    ResultTable = PythonResult{[Name="result"]}[Value],
    FinalTypes = Table.TransformColumnTypes(ResultTable, {{"date", type date}, {"bottles_sold_forecast", type number}, {"forecast_lower_95", type number}, {"forecast_upper_95", type number}, {"model", type text}})
in
    FinalTypes

If firewall still appears
- In Power BI Desktop: File -> Options and settings -> Options -> Privacy.
- Set all involved sources to the same privacy level (Organizational is common).
- If needed for local development, enable Ignore the Privacy levels and potentially improve performance.

Notes
- Python step requires pandas, numpy, statsmodels, matplotlib in the Python environment configured in Power BI Desktop.
- Your reusable function script is in power_query_forecast.py.
- matplotlib is installed and required (even though forecast script doesn't directly use it).

Validate Python environment before testing Power BI query
- Run this in your venv to confirm all required packages are installed:

```
python -c "import pandas; import numpy; import statsmodels; import matplotlib; print('All packages OK')"
```

- If any import fails, install it:
  `pip install pandas numpy statsmodels matplotlib scikit-learn`

- After installing packages, restart Power BI Desktop.

Python Access Is Denied fix (DataSourceKind=Python)
- This is usually an environment permission issue, not an M query logic issue.

1) Set Python home in Power BI to your user-writable interpreter
- Power BI Desktop -> File -> Options and settings -> Options -> Python scripting.
- Set Home Directory to:
    C:\Users\PHUyJo3\OneDrive - NESTLE\Documents\projects\iowa\.venv\Scripts
- Restart Power BI Desktop after changing this.

2) Run Power BI Desktop as Administrator once (test)
- Right-click Power BI Desktop -> Run as administrator.
- If this fixes it, your normal user lacks access to Python executable or temp paths.

3) Confirm folder permissions for these locations
- Python exe folder:
    C:\Users\PHUyJo3\OneDrive - NESTLE\Documents\projects\iowa\.venv\Scripts
- Project folder:
    C:\Users\PHUyJo3\OneDrive - NESTLE\Documents\projects\iowa
- Windows temp folder (used by Python engine):
    %LOCALAPPDATA%\Temp
- Ensure your user has Read/Execute on the python path and Write on temp.

4) Check ransomware/Controlled Folder Access
- Windows Security -> Virus & threat protection -> Ransomware protection.
- If Controlled folder access is ON, allow:
    - PBIDesktop.exe
    - python.exe from your .venv

5) Quick smoke test in Power Query Python step
- Use this tiny script first. If this fails, forecasting code is not the problem:

import os
import tempfile
import pandas as pd

tmp = tempfile.gettempdir()
probe = os.path.join(tmp, "pbi_python_probe.txt")
with open(probe, "w", encoding="utf-8") as f:
        f.write("ok")

result = pd.DataFrame({
        "temp_dir": [tmp],
        "probe_file": [probe],
        "can_write": [os.path.exists(probe)],
        "rows_in_dataset": [len(dataset)]
})

6) If smoke test passes but forecast fails
- Install packages in the same interpreter configured in Power BI:
    - pip install pandas numpy statsmodels
- Keep Python query output variable named result.
- Keep Python step at the end of the query and pass buffered table only.

7) OneDrive path edge case
- If permissions still fail, create a local non-OneDrive venv, for example:
    C:\dev\pyenvs\pbi-forecast
- Point Power BI Python home there and retry.
