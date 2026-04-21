from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing


INPUT_CANDIDATES = [
	Path(r"C:/Users/PHUyJo3/OneDrive - NESTLE/Documents/projects/data/iowa/GoalMain.csv"),
	Path(r"C:/Users/PHUyJo3/OneDrive - NESTLE/Documents/projects/iowa/data/GoalMain.csv"),
]
OUTPUT_FILE = Path(r"C:/Users/PHUyJo3/OneDrive - NESTLE/Documents/projects/iowa/data/forecast_bottles_sold.csv")


def resolve_input_file() -> Path:
	for candidate in INPUT_CANDIDATES:
		if candidate.exists():
			return candidate
	raise FileNotFoundError(f"No input CSV found in candidates: {INPUT_CANDIDATES}")


def load_monthly_series(input_file: Path) -> pd.Series:
	df = pd.read_csv(input_file, usecols=["date", "bottles_sold"])
	df["date"] = pd.to_datetime(df["date"], errors="coerce")
	df["bottles_sold"] = pd.to_numeric(df["bottles_sold"], errors="coerce")
	df = df.dropna(subset=["date", "bottles_sold"])

	monthly = (
		df.set_index("date")["bottles_sold"]
		.resample("MS")
		.sum()
		.asfreq("MS")
		.fillna(0.0)
	)
	return monthly.astype(float)


def fit_model(train: pd.Series) -> ExponentialSmoothing:
	seasonal = "add" if len(train) >= 24 else None
	seasonal_periods = 12 if seasonal else None

	model = ExponentialSmoothing(
		train,
		trend="add",
		seasonal=seasonal,
		seasonal_periods=seasonal_periods,
		initialization_method="estimated",
	)
	return model.fit(optimized=True)


def main() -> None:
	input_file = resolve_input_file()
	monthly = load_monthly_series(input_file)

	horizon = 6
	if len(monthly) <= horizon + 6:
		raise ValueError("Not enough history. Need at least 12 monthly points.")

	train = monthly.iloc[:-horizon]
	test = monthly.iloc[-horizon:]

	fitted = fit_model(train)
	test_pred = fitted.forecast(horizon)
	mape = ((test - test_pred).abs() / test.replace(0, np.nan)).mean() * 100

	final_fit = fit_model(monthly)
	future_steps = 12
	future_pred = final_fit.forecast(future_steps)

	residual_std = (train - fitted.fittedvalues).std(ddof=1)
	z_score = 1.96

	forecast_df = pd.DataFrame(
		{
			"date": future_pred.index,
			"bottles_sold_forecast": future_pred.values,
			"forecast_lower_95": future_pred.values - z_score * residual_std,
			"forecast_upper_95": future_pred.values + z_score * residual_std,
			"model": "HoltWintersAdditive",
		}
	)

	OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
	forecast_df.to_csv(OUTPUT_FILE, index=False)

	print(f"Input file: {input_file}")
	print(f"Rows used for model: {len(monthly)} monthly points")
	print(f"Validation MAPE (last {horizon} months): {mape:.2f}%")
	print(f"Forecast output: {OUTPUT_FILE}")
	print("\nPreview:")
	print(forecast_df.head(5).to_string(index=False))


if __name__ == "__main__":
	main()