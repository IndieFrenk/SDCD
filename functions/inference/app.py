
from flask import Flask, request, jsonify
import joblib
import json
import numpy as np

app = Flask(__name__)

model = joblib.load("/data/model/model.pkl")
with open("/data/processed/country_mapping.json", "r") as f:
    country_map = json.load(f)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(force=True)
    try:
        qty = data.get("Quantity")
        price = data.get("UnitPrice")
        country = data.get("Country")
        country_code = country_map[str(country)] if country is not None else 0
        X = np.array([[qty, price, country_code]], dtype=float)
        prediction = model.predict(X)
        result = {"predicted_value": prediction[0]}
    except Exception as e:
        result = {"error": str(e)}
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
