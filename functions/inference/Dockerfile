# Dockerfile per servizio di Inferenza (Fase 4)
FROM python:3.9

# Installiamo Flask e scikit-learn (il modello è un oggetto scikit-learn, quindi serve la libreria per poterlo deserializzare)
RUN pip install flask scikit-learn

WORKDIR /app
COPY app.py ./

# Espone la porta 5000 (per documentazione, l'esposizione reale avviene con -p in esecuzione)
EXPOSE 5000

# Comando di avvio: esegue l'app Flask
CMD ["python", "app.py"]
