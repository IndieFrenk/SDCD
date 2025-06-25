# convert_excel_to_csv.py
import pandas as pd
import os

# Percorso file Excel in input
input_excel = "/data/raw/OnlineRetail.xlsx"
# Percorso file CSV in output (nome previsto dal cleaning)
output_csv = "/data/raw/OnlineRetail.csv"

print(f"[Convertitore] Lettura file Excel da: {input_excel}")

try:
    df = pd.read_excel(input_excel)
    print(f"[Convertitore] Excel caricato: {len(df)} righe.")
except Exception as e:
    print(f"[Errore] Impossibile leggere il file Excel: {e}")
    exit(1)

# Esportazione in CSV con separatore virgola e encoding UTF-8
try:
    df.to_csv(output_csv, index=False, encoding="utf-8")
    print(f"[Convertitore] File CSV salvato in: {output_csv}")
except Exception as e:
    print(f"[Errore] Impossibile salvare il file CSV: {e}")
    exit(1)
