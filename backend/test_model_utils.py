# backend/test_model_utils.py

from model_utils import predict_next_month_expenses

# Path to the same CSV used for training or a new one
csv_path = "expense2.csv"  # Adjust if in another folder

# Get predictions
predictions = predict_next_month_expenses(csv_path)

# Print the results
print("📊 Predicted Next Month's Expenses:")
for category, amount in predictions.items():
    print(f"{category}: ₹{amount}")
