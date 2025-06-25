# Dockerfile per funzione di Data Cleaning (Fase 2)
FROM python:3.9

# Installa le dipendenze necessarie (pandas per data processing)
RUN pip install pandas

WORKDIR /app
COPY cleaning.py ./

# Esegui lo script di cleaning all'avvio del container
CMD ["python", "cleaning.py"]
