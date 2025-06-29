import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os

data_path = "/data/processed/OnlineRetail_cleaned.csv"
print(f"[Training] Caricamento dataset pulito da {data_path} ...")
df = pd.read_csv(data_path)
y = df['TotalPrice']
X = df.drop('TotalPrice', axis=1)
model = LinearRegression()
model.fit(X, y)
os.makedirs("/data/model", exist_ok=True)
model_path = "/data/model/model.pkl"
joblib.dump(model, model_path)
print(f"[Training] Modello addestrato salvato in {model_path}. Coefficienti: {getattr(model, 'coef_', None)}")
