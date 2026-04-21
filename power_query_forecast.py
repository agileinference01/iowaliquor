from __future__ import annotations

import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing


def build_monthly_forecast(dataset: pd.DataFrame, horizon: int = 12) -> pd.DataFrame:
    required = {"date", "bottles_sold"}
    missing = required - set(dataset.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df = dataset[["date", "bottles_sold"]].copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["bottles_sold"] = pd.to_numeric(df["bottles_sold"], errors="coerce")
    df = df.dropna(subset=["date", "bottles_sold"])

    monthly = (
        df.set_index("date")["bottles_sold"]
        .resample("MS")
        .sum()
        .asfreq("MS")
        .fillna(0.0)
        .astype(float)
    )

    if len(monthly) < 3:
        raise ValueError(
            f"Need at least 3 monthly points to forecast, got {len(monthly)}. "
            "If running in Power Query editor preview, click 'Close & Apply' to "
            "refresh with the full dataset instead of the preview sample."
        )

    seasonal = "add" if len(monthly) >= 24 else None
    seasonal_periods = 12 if seasonal else None

    # Use multiplicative trend when only a few points are available
    trend = "add" if len(monthly) >= 6 else "add"
    model = ExponentialSmoothing(
        monthly,
        trend=trend,
        seasonal=seasonal,
        seasonal_periods=seasonal_periods,
        initialization_method="estimated",
    )
    fitted = model.fit(optimized=True)

    future = fitted.forecast(horizon)
    residual_std = (monthly - fitted.fittedvalues).std(ddof=1)
    z_score = 1.96

    out = pd.DataFrame(
        {
            "date": future.index,
            "bottles_sold_forecast": future.values,
            "forecast_lower_95": future.values - z_score * residual_std,
            "forecast_upper_95": future.values + z_score * residual_std,
            "model": "HoltWintersAdditive",
        }
    )

    out["forecast_lower_95"] = out["forecast_lower_95"].clip(lower=0)
    out["date"] = out["date"].dt.date
    return out


# Power Query entry point:
# - Power BI provides input data as a pandas DataFrame called dataset.
# - Expose output in a DataFrame variable for Power Query to import.
if "dataset" in globals():
    result = build_monthly_forecast(dataset, horizon=12)
