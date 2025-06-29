import os
import pandas as pd
import json

datafile = os.getenv("DATASET_FILE", "OnlineRetail.csv")
input_path = os.path.join("/data/raw", datafile)

print(f"[Cleaning] Caricamento dataset {input_path} ...")

df = pd.read_csv(input_path, encoding="unicode_escape") 
df.dropna(inplace=True)

if 'Quantity' in df.columns:
    df = df[df['Quantity'] >= 0]
    
if 'Quantity' in df.columns and 'UnitPrice' in df.columns:
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

if 'Country' in df.columns:
    countries = sorted(df['Country'].unique())
    country_map = {country: idx for idx, country in enumerate(countries)}
    df['CountryCode'] = df['Country'].map(country_map)
    with open("/data/processed/country_mapping.json", "w") as f:
        json.dump(country_map, f)
    df.drop('Country', axis=1, inplace=True)

for col in ['InvoiceNo', 'StockCode', 'Description', 'CustomerID', 'InvoiceDate']:
    if col in df.columns:
        df.drop(col, axis=1, inplace=True)

output_path = "/data/processed/OnlineRetail_cleaned.csv"
df.to_csv(output_path, index=False)
print(f"[Cleaning] Completato! Dati puliti salvati in {output_path} ({len(df)} record).")
