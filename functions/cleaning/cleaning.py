# cleaning.py - Script di data cleaning (Fase 2)
import os
import pandas as pd
import json

# Legge il nome del file dataset dalla variabile d'ambiente (con default)
datafile = os.getenv("DATASET_FILE", "OnlineRetail.csv")
input_path = os.path.join("/data/raw", datafile)

print(f"[Cleaning] Caricamento dataset {input_path} ...")
# Carica il dataset (CSV). Se fosse Excel, si potrebbe usare pd.read_excel.
df = pd.read_csv(input_path, encoding="unicode_escape")  # encoding fix per caratteri speciali

# Rimozione di righe con valori nulli in qualsiasi colonna
df.dropna(inplace=True)

# Rimozione di record con quantità negativa (ordini resi)
if 'Quantity' in df.columns:
    df = df[df['Quantity'] >= 0]

# Aggiunta colonna TotalPrice (fatturato per riga d'ordine)
if 'Quantity' in df.columns and 'UnitPrice' in df.columns:
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

# Codifica variabile categorica "Country" -> numero intero (CountryCode)
if 'Country' in df.columns:
    countries = sorted(df['Country'].unique())
    country_map = {country: idx for idx, country in enumerate(countries)}
    df['CountryCode'] = df['Country'].map(country_map)
    # Salva la mappatura country->codice su file JSON per utilizzo futuro (in inferenza)
    with open("/data/processed/country_mapping.json", "w") as f:
        json.dump(country_map, f)
    # Opzionalmente, si potrebbe droppare la colonna originale
    df.drop('Country', axis=1, inplace=True)

# Elimina colonne non rilevanti per il modello (esempio: identificativi, descrizioni)
for col in ['InvoiceNo', 'StockCode', 'Description', 'CustomerID', 'InvoiceDate']:
    if col in df.columns:
        df.drop(col, axis=1, inplace=True)

# Salva il dataset pulito in CSV nella cartella di output
output_path = "/data/processed/OnlineRetail_cleaned.csv"
df.to_csv(output_path, index=False)
print(f"[Cleaning] Completato! Dati puliti salvati in {output_path} ({len(df)} record).")
