# backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
from model_utils import predict_next_month_expenses  # Custom prediction logic

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

@app.route("/predict", methods=["POST"])
def predict():
    # Check if file part exists in request
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    # Check if filename is empty
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    try:
        # Save uploaded CSV temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            file.save(tmp.name)
            temp_path = tmp.name

        # Run prediction logic (your model)
        prediction = predict_next_month_expenses(temp_path)

        # Clean up temporary file
        os.remove(temp_path)

        # Return result as JSON
        return jsonify({"prediction": prediction}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
