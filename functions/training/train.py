# train.py - Script di training modello ML (Fase 3)
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os

# Path del dataset pulito prodotto nella fase 2
data_path = "/data/processed/OnlineRetail_cleaned.csv"
print(f"[Training] Caricamento dataset pulito da {data_path} ...")
df = pd.read_csv(data_path)

# Suddivisione in feature (X) e target (y)
# Presumiamo che la colonna target sia 'TotalPrice', creata in fase 2
y = df['TotalPrice']
X = df.drop('TotalPrice', axis=1)

# Inizializza e addestra un modello di regressione (es. regressione lineare)
model = LinearRegression()
model.fit(X, y)

# Crea directory di output del modello se non esiste
os.makedirs("/data/model", exist_ok=True)
model_path = "/data/model/model.pkl"
# Salva il modello serializzato su file .pkl
joblib.dump(model, model_path)
print(f"[Training] Modello addestrato salvato in {model_path}. Coefficienti: {getattr(model, 'coef_', None)}")
