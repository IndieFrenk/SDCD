# app.py - Servizio Flask per inferenza (Fase 4)
from flask import Flask, request, jsonify
import joblib
import json
import numpy as np

app = Flask(__name__)

# All'avvio dell'app, carica il modello ML e la mappatura country->codice
model = joblib.load("/data/model/model.pkl")
with open("/data/processed/country_mapping.json", "r") as f:
    country_map = json.load(f)

@app.route("/predict", methods=["POST"])
def predict():
    """
    Endpoint per richiedere una predizione.
    Ci si attende un JSON nel corpo della richiesta con le feature necessarie.
    Esempio di JSON atteso: {"Quantity": 10, "UnitPrice": 2.5, "Country": "France"}
    """
    data = request.get_json(force=True)
    try:
        # Estrae le feature dalla richiesta
        qty = data.get("Quantity")
        price = data.get("UnitPrice")
        country = data.get("Country")
        # Applica le stesse trasformazioni del preprocessing:
        # converti Country da nome a codice numerico usando la mappatura
        country_code = country_map[str(country)] if country is not None else 0
        # Costruisce il vettore delle feature per il modello
        X = np.array([[qty, price, country_code]], dtype=float)
        # Ottiene la predizione dal modello
        prediction = model.predict(X)
        # Prepara la risposta
        result = {"predicted_value": prediction[0]}
    except Exception as e:
        # Gestione errori (ad es. campi mancanti o formato errato)
        result = {"error": str(e)}
    return jsonify(result)

# Avvio dell'app Flask in modalità produzione (host=0.0.0.0 per accesso esterno)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
