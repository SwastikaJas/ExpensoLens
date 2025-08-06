# backend/model_utils.py

import pandas as pd
import joblib
import os

# Load model
#MODEL_PATH = os.path.join("models", "expense_predictor.pkl")
#model = joblib.load(MODEL_PATH)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(ROOT_DIR, "models", "expense_predictor.pkl")

model = joblib.load(MODEL_PATH)

def predict_next_month_expenses(expense_csv_path):
    # Read uploaded expenses CSV
    df = pd.read_csv(expense_csv_path, parse_dates=["Date"])

    # Prepare month-year column
    df["YearMonth"] = df["Date"].dt.to_period("M").astype(str)

    # Group total amount per category per month
    grouped = df.groupby(["YearMonth", "Category"])["Amount"].sum().reset_index()

    # Create numeric month index
    month_map = {month: idx for idx, month in enumerate(sorted(grouped["YearMonth"].unique()))}
    grouped["MonthIndex"] = grouped["YearMonth"].map(month_map)

    # Find next month index
    next_month_index = max(grouped["MonthIndex"]) + 1

    # Unique categories
    categories = grouped["Category"].unique()

    # Prepare input for prediction
    prediction_input = pd.DataFrame({
        "MonthIndex": [next_month_index] * len(categories),
        "Category": categories
    })

    # Predict amounts
    predicted_amounts = model.predict(prediction_input)

    # Combine predictions
    prediction_result = dict(zip(categories, map(lambda x: round(x, 2), predicted_amounts)))

    return prediction_result
